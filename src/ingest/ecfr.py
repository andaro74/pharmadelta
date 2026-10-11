"""The eCFR half of regdelta's ingestion, ported and scoped to 21 CFR parts 201 and 314.

From `src/ingestion/processor.py` in the regdelta clone: `valid_version_dates`
(split the versioner's `content_versions[]` into ISO dates and rejections),
`latest_version_date` (kept for reference; the build never uses "latest",
it reads at the clause's own `effective_date`) and the XML reading in
`parse_ecfr_xml` (a DIV8 section is its HEAD, its flat P elements and its
CITA note). What is new here is the paragraph locator: eCFR's P elements
are flat, each starting with its own lettering, so the section's
hierarchy is rebuilt by walking them and the clause's paragraph is the
one whose rebuilt path equals the clause id's lettering.

regdelta's domain rule stands: a snapshot date is not an effective date.
This module never resolves "current" or today; a caller passes a date,
and `section_versions` says whether the source lists it.

Levels of CFR lettering, in the order the eCFR nests them:
  1 (a)  2 (1)  3 (i)  4 (A)  5 (<I>1</I>)  6 (<I>i</I>)
"""

from __future__ import annotations

import datetime as dt
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from . import fetch

ECFR_API = "https://www.ecfr.gov/api/versioner/v1"
TITLE = "21"
PARTS_IN_SCOPE = frozenset({"201", "314"})

_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SECTION = re.compile(r"^(\d+)\.(\d+)$")
_CLAUSE_ID = re.compile(r"^(?P<section>\d+\.\d+)(?P<markers>(?:\([^)]+\))*)(?:-(?P<definition>[A-Za-z]+))?$")
_MARKER = re.compile(r"\((\x01?)([a-z]+|\d+|[A-Z]+)\x02?\)")
_ROMAN = re.compile(r"^(?=[ivxlc])m*(c[md]|d?c{0,3})(x[cl]|l?x{0,3})(i[xv]|v?i{0,3})$")
_LETTERS = "abcdefghijklmnopqrstuvwxyz"


class ClauseNotLocated(Exception):
    """The paragraph at the clause's lettering is not in the section at that version."""


def iso_date(value: object, *, field_name: str = "date") -> str:
    """regdelta's `validate.iso_date`: a real calendar date in ISO form."""
    if not isinstance(value, str) or not _ISO.match(value):
        raise ValueError(f"{field_name} is not an ISO date (YYYY-MM-DD): {value!r}")
    try:
        dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} is not a real calendar date: {value!r}") from exc
    return value


def cfr_section(value: str) -> str:
    """A section of a part in scope; the part is the number before the dot."""
    m = _SECTION.match(value or "")
    if not m or m.group(1) not in PARTS_IN_SCOPE:
        raise ValueError(f"not a section of 21 CFR {sorted(PARTS_IN_SCOPE)}: {value!r}")
    return value


# --------------------------------------------------------------- versioner
def title_status() -> dict:
    """Title 21's row of `titles.json`: `up_to_date_as_of` is the snapshot date (`ecfr_as_of`)."""
    data = fetch.get_json(f"{ECFR_API}/titles.json")
    row = next((t for t in data.get("titles", []) if str(t.get("number")) == TITLE), None)
    if row is None:
        raise ValueError("titles.json has no row for title 21")
    return {
        "up_to_date_as_of": iso_date(row.get("up_to_date_as_of"), field_name="up_to_date_as_of"),
        "latest_amended_on": row.get("latest_amended_on"),
        "latest_issue_date": row.get("latest_issue_date"),
        "meta": data.get("meta"),
    }


def valid_version_dates(content_versions: list | None) -> tuple[list[str], list[str]]:
    """regdelta's `valid_version_dates`: ISO dates and the rejections, skip-and-report."""
    dates, rejected = [], []
    for v in content_versions or []:
        try:
            dates.append(iso_date((v or {}).get("date"), field_name="content_versions[].date"))
        except ValueError as exc:
            rejected.append(str(exc))
    return dates, rejected


def section_versions(section: str) -> dict:
    """The versioner's `content_versions[]` for one section: the dates it lists, sorted, and the raw entries."""
    cfr_section(section)
    url = f"{ECFR_API}/versions/title-{TITLE}.json?section={section}"
    data = fetch.get_json(url)
    entries = data.get("content_versions") or []
    dates, rejected = valid_version_dates(entries)
    return {
        "url": url,
        "dates": sorted(set(dates)),
        "rejected": rejected,
        "entries": [
            {k: e.get(k) for k in ("date", "amendment_date", "issue_date", "substantive", "removed", "identifier")}
            for e in entries
        ],
        "meta": data.get("meta"),
    }


def latest_version_date(section: str) -> str:
    """regdelta's `latest_version_date`. Kept for reference; the build reads at the committed date, never "latest"."""
    v = section_versions(section)
    if not v["dates"]:
        raise ValueError(f"eCFR returned no usable content_versions for section {section}; rejected {v['rejected'][:3]}")
    return max(v["dates"])


def section_url(section: str, date: str) -> str:
    cfr_section(section)
    iso_date(date, field_name="effective_date")
    part = section.split(".")[0]
    return f"{ECFR_API}/full/{date}/title-{TITLE}.xml?part={part}&section={section}"


def fetch_section_xml(section: str, date: str) -> bytes:
    return fetch.get_bytes(section_url(section, date))


# --------------------------------------------------------------- paragraphs
@dataclass
class Paragraph:
    path: tuple[str, ...]  # the rebuilt lettering, e.g. ("c", "6", "iii", "A")
    lettered: bool  # False for a P that carries no marker of its own (a definition, continuation text)
    text: str
    index: int


@dataclass
class Section:
    section: str
    head: str
    source_note: str
    paragraphs: list[Paragraph] = field(default_factory=list)


def _text(el: ET.Element | None) -> str:
    """regdelta's `_text`: all text, whitespace collapsed to single spaces."""
    return " ".join("".join(el.itertext()).split()) if el is not None else ""


def _serialize(el: ET.Element) -> str:
    """The P's text with italic runs fenced by \\x01 and \\x02, so (<I>1</I>) can be told from (1)."""
    out = [el.text or ""]
    for child in el:
        inner = "".join(child.itertext())
        out.append(f"\x01{inner}\x02" if child.tag == "I" else inner)
        out.append(child.tail or "")
    return " ".join("".join(out).split())


def _level_candidates(marker: str, italic: bool) -> list[int]:
    if marker.isdigit():
        return [5] if italic else [2]
    if marker.isupper():
        return [4]
    if italic:
        return [6] if _ROMAN.match(marker) else []
    cands = []
    if len(marker) == 1:
        cands.append(1)
    if _ROMAN.match(marker):
        cands.append(3)
    return cands


def _roman_to_int(s: str) -> int:
    vals = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}
    total, prev = 0, 0
    for ch in reversed(s):
        v = vals[ch]
        total = total - v if v < prev else total + v
        prev = max(prev, v)
    return total


def _int_to_roman(n: int) -> str:
    out = ""
    pairs = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"), (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    for v, r in pairs:
        while n >= v:
            out, n = out + r, n - v
    return out


def _first(level: int) -> str:
    return {1: "a", 2: "1", 3: "i", 4: "A", 5: "1", 6: "i"}[level]


def _successor(level: int, marker: str) -> str | None:
    if level in (1, 4):
        letters = _LETTERS if level == 1 else _LETTERS.upper()
        i = letters.find(marker)
        return letters[i + 1] if 0 <= i < len(letters) - 1 else None
    if level in (2, 5):
        return str(int(marker) + 1)
    return _int_to_roman(_roman_to_int(marker) + 1)


def _place(path: list[str], marker: str, italic: bool, where: str) -> list[str]:
    """Return the path after `marker`: a later sibling at an existing level, or the first child one level down."""
    fits = []
    for level in _level_candidates(marker, italic):
        if level <= len(path) and _successor(level, path[level - 1]) == marker:
            fits.append(level)
        elif level == len(path) + 1 and marker == _first(level):
            fits.append(level)
    if len(fits) != 1:
        joined = "/".join(path) or "the section head"
        raise ClauseNotLocated(f"cannot place marker ({marker}) after {joined} at {where}: {len(fits)} readings")
    return path[: fits[0] - 1] + [marker]


def parse_section(xml_bytes: bytes, section: str) -> Section:
    """eCFR versioner XML (DIV8 SECTION) -> the section's paragraphs with their rebuilt lettering."""
    root = ET.fromstring(xml_bytes)
    div8 = root if root.tag == "DIV8" else root.find(".//DIV8")
    if div8 is None:
        raise ValueError(f"no DIV8 section element in the XML for {section}")
    if div8.get("N") != section:
        raise ValueError(f"the XML is section {div8.get('N')!r}, not {section!r}")
    out = Section(section=section, head=_text(div8.find("HEAD")), source_note=_text(div8.find("CITA")))
    path: list[str] = []
    for index, el in enumerate(div8):
        if el.tag not in ("P", "FP"):
            continue
        serialized = _serialize(el)
        pos, lettered = 0, False
        while True:
            m = _MARKER.match(serialized, pos)
            if m is None:
                # "(a) <I>Heading.</I> (1)(i) ...": markers after an italic heading continue the lettering.
                if not lettered or serialized[pos : pos + 2] != " \x01":
                    break
                end = serialized.find("\x02", pos)
                if end < 0 or not _MARKER.match(serialized, end + 2):
                    break
                pos = end + 2
                continue
            path = _place(path, m.group(2), bool(m.group(1)), f"P #{index} of {section}")
            lettered, pos = True, m.end()
        out.paragraphs.append(Paragraph(path=tuple(path), lettered=lettered, text=_text(el), index=index))
    return out


def parse_clause_id(clause_id: str) -> tuple[str, tuple[str, ...], str | None]:
    """`314.80(a)-serious` -> ("314.80", ("a",), "serious"); `314.70(c)(6)(iii)(A)` -> ("314.70", ("c","6","iii","A"), None)."""
    m = _CLAUSE_ID.match(clause_id)
    if not m:
        raise ValueError(f"not a clause id: {clause_id!r}")
    markers = tuple(re.findall(r"\(([^)]+)\)", m.group("markers")))
    return cfr_section(m.group("section")), markers, m.group("definition")


def describe(section: str, path: tuple[str, ...]) -> str:
    return section + "".join(f"({p})" for p in path)


def locate(sec: Section, path: tuple[str, ...], *, definition: str | None = None, append_subparagraphs: bool = False) -> dict:
    """The clause's paragraph in a parsed section: its text, its parent's text, and what was appended."""
    where = describe(sec.section, path)
    heads = [i for i, p in enumerate(sec.paragraphs) if p.lettered and p.path == path]
    if definition is not None:
        # The unlettered paragraphs under `path`, up to the next lettered one, are its definitions.
        if not heads:
            raise ClauseNotLocated(f"no paragraph {where} to hold the definition {definition!r}")
        candidates = []
        for p in sec.paragraphs[heads[0] + 1 :]:
            if p.lettered:
                break
            candidates.append(p)
        hits = [p for p in candidates if p.text.lower().startswith(definition.lower())]
        if len(hits) != 1:
            raise ClauseNotLocated(f"{len(hits)} definitions under {where} begin with {definition!r}")
        return {"text": hits[0].text, "lead_in": sec.paragraphs[heads[0]].text, "appended": []}
    if len(heads) != 1:
        raise ClauseNotLocated(f"{len(heads)} paragraphs lettered {where}")
    head = heads[0]
    appended = []
    if append_subparagraphs:
        for p in sec.paragraphs[head + 1 :]:
            if len(p.path) > len(path) and p.path[: len(path)] == path:
                appended.append(p.text)
            else:
                break
    parent = None
    if len(path) > 1:
        parents = [p for p in sec.paragraphs[:head] if p.lettered and p.path == path[:-1]]
        parent = parents[-1].text if parents else None
    text = " ".join([sec.paragraphs[head].text, *appended])
    return {"text": text, "lead_in": parent, "appended": appended}
