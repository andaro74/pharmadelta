"""A DailyMed SPL reader: the history of a set id, its current SPL XML, and the row fields derived from it.

What DailyMed's v2 API gives (read 2026-10-11, `milestones/M02/README.md`):
`/spls/<setid>/history.json` lists every version with its published date;
`/spls/<setid>.xml` serves the current version only, whatever `version`
parameter is sent. So a row is read at its version only when no version
was published after the row's `label_read_on`; otherwise the source at
that version cannot be read by machine and the caller reports UNSCORABLE
(M02 PR 1, ruling 7).

The derived fields (`milestones/M00/fields.md`, the nine marked DailyMed,
less `section_terms`, which is a reading and not a structure; see
`milestones/M02/README.md` PR 2, Unsure 11):

  ingredient     the active ingredient's substance name on the products, lowercased
  dosage_form    the products' form code display name, lowercased
  strengths      each product's active quantity, "<value> <unit>", unique, ascending, "; "-joined
  anda           the products' approval id
  label_revised  the "Revised:" month DailyMed prints, by FDA's stylesheet rule (spl-common.xsl, template
                 effectiveDateHighlights, quoted in milestones/adoption/rulings/data-owner-cleanup.md 3):
                 the latest effectiveTime over the top-level sections of the structured body, excluding
                 the product data elements section (48780-1) and every section after the highest-numbered
                 standard section up to 17 (PLR_SECTIONS below), as YYYY-MM
  format         201.56(d) when the SPL carries Highlights (any <highlight> element), else 201.56(e)
  section        the row's section code, when the SPL has that section ("bw": a Boxed Warning section,
                 LOINC 34066-1; "N" or "N.N": a section whose title begins with that number)
  section_title  that section's title without its number; a boxed warning whose title is the generic
                 "BOXED WARNING" takes its first non-empty paragraph instead

The products must agree on ingredient, dosage form and ANDA; when they do
not, the field is written as null with the disagreement beside it.
"""

from __future__ import annotations

import datetime as dt
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from . import fetch

DAILYMED_API = "https://dailymed.nlm.nih.gov/dailymed/services/v2"
DAILYMED_PAGE = "https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid="
NS = {"h": "urn:hl7-org:v3"}
H = "{urn:hl7-org:v3}"
BOXED_WARNING = "34066-1"
PRODUCT_DATA_ELEMENTS = "48780-1"
# The standard sections of the PLR format (21 CFR 201.56(d), 201.57) and their LOINC section codes, the
# set FDA's stylesheet calls `$standardSections` (spl-common.xsl line 41 reads it from plr-sections.xml,
# beside the stylesheet) and cuts at as `maxSection17` (template `effectiveDateHighlights`). The numbers
# are plr-sections.xml's top-level `number` attributes, read 2026-10-25 by fetch at the build-fixes PR
# (milestones/adoption/rulings/build-fixes.md): 0 and 1 to 17, with two codes numbered 17. Nested
# entries of that file (8.1 to 8.5, 9.1 to 9.3, 12.1 to 12.4, 13.1 to 13.2) are not top-level and are not
# in the stylesheet's `$standardSections/v3:section`, so they are not here.
PLR_SECTIONS = {
    "34066-1": 0,   # BOXED WARNING
    "34067-9": 1,   # INDICATIONS & USAGE
    "34068-7": 2,   # DOSAGE & ADMINISTRATION
    "43678-2": 3,   # DOSAGE FORMS & STRENGTHS
    "34070-3": 4,   # CONTRAINDICATIONS
    "43685-7": 5,   # WARNINGS AND PRECAUTIONS
    "34084-4": 6,   # ADVERSE REACTIONS
    "34073-7": 7,   # DRUG INTERACTIONS
    "43684-0": 8,   # USE IN SPECIFIC POPULATIONS
    "42227-9": 9,   # DRUG ABUSE AND DEPENDENCE
    "34088-5": 10,  # OVERDOSAGE
    "34089-3": 11,  # DESCRIPTION
    "34090-1": 12,  # CLINICAL PHARMACOLOGY
    "43680-8": 13,  # NONCLINICAL TOXICOLOGY
    "34092-7": 14,  # CLINICAL STUDIES
    "34093-5": 15,  # REFERENCES
    "34069-5": 16,  # HOW SUPPLIED/STORAGE AND HANDLING
    "34076-0": 17,  # PATIENT COUNSELING INFORMATION (INFORMATION FOR PATIENTS)
    "38056-8": 17,  # SUPPLEMENTAL PATIENT MATERIAL SECTION (the stylesheet's second code numbered 17)
}
ACTIVE = frozenset({"ACTIB", "ACTIM", "ACTIR"})
_SETID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
_SECTION_CODE = re.compile(r"^(bw|\d+(?:\.\d+)?)$")
_NUMBERED_TITLE = re.compile(r"^(\d+(?:\.\d+)?)\s+(.*)$")


def set_id(value: str) -> str:
    if not isinstance(value, str) or not _SETID.match(value):
        raise ValueError(f"not a DailyMed set id: {value!r}")
    return value


def page_url(setid: str) -> str:
    return DAILYMED_PAGE + set_id(setid)


# ---------------------------------------------------------------- history
def _published(value: str) -> str:
    """DailyMed prints `published_date` as `Nov 06, 2024`; return it as ISO."""
    return dt.datetime.strptime(value.strip(), "%b %d, %Y").date().isoformat()


def history(setid: str) -> dict:
    """Every version of the set id with its published date, newest first, and the current (highest) version."""
    url = f"{DAILYMED_API}/spls/{set_id(setid)}/history.json"
    data = fetch.get_json(url)
    rows = []
    for h in (data.get("data") or {}).get("history") or []:
        rows.append({"spl_version": int(h["spl_version"]), "published": _published(h["published_date"])})
    if not rows:
        raise ValueError(f"history.json lists no version for {setid}")
    rows.sort(key=lambda r: r["spl_version"], reverse=True)
    meta = data.get("metadata") or {}
    if str(meta.get("next_page_url", "null")) not in ("null", "None", ""):
        raise ValueError(f"history.json for {setid} has more than one page; the reader reads one")
    return {"url": url, "versions": rows, "current": rows[0], "title": (data.get("data") or {}).get("spl", {}).get("title")}


def published_after(hist: dict, read_on: str) -> list[dict]:
    """The versions published after the row's `label_read_on` (ISO)."""
    return [v for v in hist["versions"] if v["published"] > read_on]


# -------------------------------------------------------------------- SPL
def spl_url(setid: str) -> str:
    return f"{DAILYMED_API}/spls/{set_id(setid)}.xml"


def fetch_spl(setid: str) -> bytes:
    return fetch.get_bytes(spl_url(setid))


def _text(el: ET.Element | None) -> str:
    return " ".join("".join(el.itertext()).split()) if el is not None else ""


@dataclass
class Product:
    name: str
    generic_name: str | None
    form: str | None
    approval: str | None
    actives: list[dict] = field(default_factory=list)


@dataclass
class SectionNode:
    code: str | None
    code_name: str | None
    title: str
    effective_time: str | None
    paragraphs: list[tuple[str, list[str]]]  # (text, style codes)
    children: list[SectionNode]


@dataclass
class Label:
    set_id: str
    version: int
    effective_time: str
    title: str
    has_highlights: bool
    products: list[Product]
    sections: list[SectionNode]


def _section(el: ET.Element) -> SectionNode:
    code = el.find("h:code", NS)
    et = el.find("h:effectiveTime", NS)
    paragraphs = []
    text_el = el.find("h:text", NS)
    if text_el is not None:
        for p in text_el.iter(H + "paragraph"):
            styles = sorted({c.get("styleCode") for c in p.iter(H + "content") if c.get("styleCode")})
            paragraphs.append((_text(p), styles))
    return SectionNode(
        code=code.get("code") if code is not None else None,
        code_name=code.get("displayName") if code is not None else None,
        title=_text(el.find("h:title", NS)),
        effective_time=et.get("value") if et is not None else None,
        paragraphs=paragraphs,
        children=[_section(c) for c in el.findall("h:component/h:section", NS)],
    )


def parse_spl(xml_bytes: bytes) -> Label:
    root = ET.fromstring(xml_bytes)
    if root.tag != H + "document":
        raise ValueError(f"not an SPL document: root element {root.tag!r}")
    products = []
    for mp in root.iter(H + "manufacturedProduct"):
        inner = mp.find("h:manufacturedProduct", NS)
        if inner is None:
            continue  # the author block's MANU entries carry no product
        form = inner.find("h:formCode", NS)
        approval = mp.find("h:subjectOf/h:approval/h:id", NS)
        actives = []
        for ing in inner.findall("h:ingredient", NS):
            if ing.get("classCode") not in ACTIVE:
                continue
            num = ing.find("h:quantity/h:numerator", NS)
            den = ing.find("h:quantity/h:denominator", NS)
            actives.append({
                "substance": _text(ing.find("h:ingredientSubstance/h:name", NS)),
                "numerator": (num.get("value"), num.get("unit")) if num is not None else None,
                "denominator": (den.get("value"), den.get("unit")) if den is not None else None,
            })
        products.append(Product(
            name=_text(inner.find("h:name", NS)),
            generic_name=_text(inner.find("h:asEntityWithGeneric/h:genericMedicine/h:name", NS)) or None,
            form=form.get("displayName") if form is not None else None,
            approval=approval.get("extension") if approval is not None else None,
            actives=actives,
        ))
    sections = [_section(s) for s in root.findall("h:component/h:structuredBody/h:component/h:section", NS)]
    return Label(
        set_id=root.find("h:setId", NS).get("root"),
        version=int(root.find("h:versionNumber", NS).get("value")),
        effective_time=root.find("h:effectiveTime", NS).get("value"),
        title=_text(root.find("h:title", NS)),
        has_highlights=root.find(".//h:highlight", NS) is not None,
        products=products,
        sections=sections,
    )


# ------------------------------------------------------------- derivation
def _agree(values: list, what: str) -> tuple[object, str | None]:
    distinct = sorted({str(v) for v in values})
    if len(distinct) == 1 and values[0] is not None:
        return values[0], None
    return None, f"the products do not agree on {what}: {distinct}"


def _strength(active: dict) -> str | None:
    if not active["numerator"]:
        return None
    value, unit = active["numerator"]
    den = active["denominator"]
    if den and den[0] not in (None, "1"):
        return f"{value} {unit}/{den[0]} {den[1]}"
    return f"{value} {unit}"


def _strength_key(s: str) -> float:
    try:
        return float(s.split()[0])
    except ValueError:
        return float("inf")


def _find_section(sections: list[SectionNode], code: str) -> SectionNode | None:
    if not _SECTION_CODE.match(code):
        raise ValueError(f"not a section code: {code!r}")
    if code == "bw":
        hits = [s for s in sections if s.code == BOXED_WARNING]
        return hits[0] if len(hits) == 1 else None
    stack = list(sections)
    hits = []
    while stack:
        s = stack.pop(0)
        m = _NUMBERED_TITLE.match(s.title)
        if m and m.group(1) == code:
            hits.append(s)
        stack.extend(s.children)
    return hits[0] if len(hits) == 1 else None


def _section_title(sec: SectionNode, code: str) -> str | None:
    if code == "bw":
        if sec.title and sec.title.strip().upper() != "BOXED WARNING":
            return sec.title
        for text, _styles in sec.paragraphs:
            if text:
                return text
        return None
    m = _NUMBERED_TITLE.match(sec.title)
    return m.group(2).strip() if m else None


def _headings_read(sec: SectionNode) -> list[str]:
    """What the section carries as headings, by structure: subsection titles and short styled paragraphs."""
    out = [c.title for c in sec.children if c.title]
    for text, styles in sec.paragraphs:
        if text and styles and len(text) <= 80:
            out.append(text)
    return out


def label_revised(label: Label) -> tuple[str | None, list[dict]]:
    """The "Revised:" month by the stylesheet's rule, as YYYY-MM, and the top-level sections it read.

    spl-common.xsl, template `effectiveDateHighlights` (quoted in
    milestones/adoption/rulings/data-owner-cleanup.md 3): over the top-level
    sections of the structured body, in document order, take each section's
    `effectiveTime/@value`, skipping the product data elements section
    (48780-1) and every section after the first occurrence of the
    highest-numbered standard section present (`maxSection17`); keep values
    longer than seven characters; the latest is the month. Subsections are
    not read. A label with no standard section has no cut: every top-level
    section but 48780-1 is read.
    """
    numbered = [(PLR_SECTIONS[s.code], i) for i, s in enumerate(label.sections) if s.code in PLR_SECTIONS]
    cut_code, cut_at = None, len(label.sections)
    if numbered:
        top = max(n for n, _ in numbered)
        cut_at = min(i for n, i in numbered if n == top)
        cut_code = label.sections[cut_at].code
    read = []
    for i, s in enumerate(label.sections):
        value = s.effective_time if s.effective_time and len(s.effective_time) > 7 and re.match(r"^\d{8}", s.effective_time) else None
        if s.code == PRODUCT_DATA_ELEMENTS:
            why = "excluded: product data elements (48780-1)"
        elif i > cut_at:
            why = f"excluded: after the highest-numbered standard section ({cut_code})"
        elif value is None:
            why = "excluded: no effectiveTime of eight or more characters"
        else:
            why = "read"
        read.append({"section": s.title, "code": s.code, "effective_time": s.effective_time, "why": why})
    values = [r["effective_time"][:8] for r in read if r["why"] == "read"]
    if not values:
        return None, read
    latest = max(values)
    return f"{latest[:4]}-{latest[4:6]}", read


def derive(label: Label, section_code: str) -> dict:
    """The derived fields for one row at `section_code`, plus what was read beside them."""
    notes: list[str] = []
    ingredient, why = _agree([", ".join(a["substance"] for a in p.actives) for p in label.products], "the active ingredient")
    notes += [why] if why else []
    dosage_form, why = _agree([p.form for p in label.products], "the dosage form")
    notes += [why] if why else []
    anda, why = _agree([p.approval for p in label.products], "the approval id")
    notes += [why] if why else []
    strengths = sorted({s for p in label.products for a in p.actives if (s := _strength(a))}, key=_strength_key)
    revised, times = label_revised(label)
    sec = _find_section(label.sections, section_code)
    fields = {
        "ingredient": ingredient.lower() if isinstance(ingredient, str) else None,
        "dosage_form": dosage_form.lower() if isinstance(dosage_form, str) else None,
        "strengths": "; ".join(strengths) if strengths else None,
        "anda": anda,
        "label_revised": revised,
        "format": "201.56(d)" if label.has_highlights else "201.56(e)",
        "section": section_code if sec is not None else None,
        "section_title": _section_title(sec, section_code) if sec is not None else None,
    }
    if sec is None:
        notes.append(f"the SPL has no section {section_code!r}")
    return {
        "fields": fields,
        "read": {
            "spl_version": label.version,
            "effectiveTime": label.effective_time,
            "section_effective_times": times,
            "section_found": {"title": sec.title, "code": sec.code, "effective_time": sec.effective_time} if sec is not None else None,
            "headings_read": _headings_read(sec) if sec is not None else [],
            "products": [
                {"name": p.name, "generic_name": p.generic_name, "form": p.form, "approval": p.approval, "actives": p.actives}
                for p in label.products
            ],
            "notes": notes,
        },
    }
