"""The M02 gate: build the clauses and the table from the live sources at each entry's version, compare with `data/`, judge F2.1.

For each clause id in `data/clauses.json`: read the eCFR versioner's
`content_versions[]` for its section; if the clause's committed
`effective_date` is one of them, fetch the section's XML at that date,
rebuild its lettering and take the paragraph at the clause id's; write
`text`, `lead_in`, `source_note` and `effective_date` beside the Data
Owner's fields from `src/ingest/hand/clauses.json`. A date the versioner
does not list is not a version: nothing is fetched at it, and the clause
is named in `clauses_mismatched` with the dates the source lists.

For each row in `data/table.json`: read DailyMed's history for its set
id. If no version was published after the row's `label_read_on`, the
current SPL is the version in force on the read date; fetch it and
derive eight fields (`src/ingest/dailymed.py`) beside the Data Owner's
fields from `src/ingest/hand/table.json`. A version published after the
read date means the source at the row's version cannot be read by
machine: the row is named with its page URL and the result is UNSCORABLE.

The verdict is ledger row 2's F2.1 and nothing else:

  RED         any clause's `effective_date` is not a version the versioner lists for its section,
              or its `text`, `lead_in` or `source_note` is not what the section carries at that
              version; or any row's derived field differs from the SPL at its version.
              `clauses_mismatched` and `rows_mismatched` name each, the source's value beside
              the committed one.
  GREEN       every compared field of every clause and row equals the build.
  UNSCORABLE  a source could not be read at an entry's version (a network or HTTP failure, a
              label revised after its read date, a section whose lettering the reader could
              not rebuild), or anything raised. Never RED, never GREEN. Mismatches found before
              the unread entry are still written.

Compared: clauses `text`, `lead_in`, `source_note`, `effective_date`;
rows `ingredient`, `dosage_form`, `strengths`, `anda`, `label_revised`,
`format`, `section`, `section_title`. Recorded, not compared:
`ecfr_as_of` and `text_copied_on` (provenance, Unsure 10); `section_terms`
(a reading, not a structure, Unsure 11); every Data Owner field.

    uv run python -m src.ingest.gate --out-dir <dir> [--summary <md>]

Writes `<dir>/result.json`, `<dir>/clauses.json` and `<dir>/table.json`
(the built files, same shape as `data/`), and `<dir>/sources/` (every
response read, with an index). Exit 0 GREEN, 1 RED, 2 UNSCORABLE. The
result is evidence only when CI wrote it (P4), and it says whether it did.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import dailymed, ecfr, fetch

ROOT = Path(__file__).resolve().parents[2]
CLAUSE_FIELDS = ("text", "lead_in", "source_note", "effective_date")
ROW_FIELDS = ("ingredient", "dosage_form", "strengths", "anda", "label_revised", "format", "section", "section_title")
ROW_CARRIED = ("holder", "holder_fictional", "rld_nda", "label_read_on", "section_terms", "section_terms_read_on", "requirement")
ROW_ORDER = (
    "table_row", "holder", "holder_fictional", "ingredient", "dosage_form", "strengths", "anda", "rld_nda",
    "dailymed_set_id", "label_revised", "label_read_on", "format", "section", "section_title", "section_terms",
    "section_terms_read_on", "requirement",
)
CLAUSE_ORDER = (
    "citation", "text", "lead_in", "source_note", "ecfr_url", "ecfr_as_of", "effective_date", "text_copied_on",
    "existence_checked_by_hand_on", "note",
)
FALSIFIER = (
    "F2.1 a clause in data/clauses.json carries an effective_date the eCFR versioner does not list for its section, "
    "or a text that is not the paragraph at that version; or a row in data/table.json carries a DailyMed-sourced "
    "field the SPL in force on its label_read_on does not hold"
)


class Unscorable(Exception):
    """The inputs do not let the build be compared. Not a verdict."""


# ------------------------------------------------------------- provenance
def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def ci_context() -> dict[str, Any] | None:
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return None
    server, repo, run_id = (os.environ.get(k) for k in ("GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_RUN_ID"))
    return {
        "run_url": f"{server}/{repo}/actions/runs/{run_id}" if server and repo and run_id else None,
        "run_id": run_id,
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "workflow": os.environ.get("GITHUB_WORKFLOW"),
        "job": os.environ.get("GITHUB_JOB"),
        "event": os.environ.get("GITHUB_EVENT_NAME"),
        "ref": os.environ.get("GITHUB_REF"),
        "sha": os.environ.get("GITHUB_SHA"),
    }


def provenance() -> dict[str, Any]:
    ci = ci_context()
    try:
        commit: str | None = git("rev-parse", "HEAD")
        dirty: bool | None = bool(git("status", "--porcelain"))
    except Exception:  # noqa: BLE001  the commit is still recorded from CI's environment when git cannot answer
        commit, dirty = (ci or {}).get("sha"), None
    return {
        "what": "M02 gate: the clauses and the table built from the live sources at each entry's version, compared with data/; the verdict is ledger row 2's F2.1",
        "milestone": "M02",
        "ledger_row": 2,
        "falsifier": FALSIFIER,
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": commit,
        "dirty": dirty,
        "written_by_ci": ci is not None,
        "ci": ci,
        "fields_compared": {"clauses": list(CLAUSE_FIELDS), "rows": list(ROW_FIELDS)},
        "fields_recorded_not_compared": {
            "clauses": ["ecfr_as_of", "text_copied_on", "citation", "ecfr_url", "existence_checked_by_hand_on", "note"],
            "rows": ["section_terms", *ROW_CARRIED, "dailymed_set_id", "table_row"],
        },
    }


# ---------------------------------------------------------------- clauses
def build_clause(cid: str, committed: dict, hand: dict, as_of: str, today: str) -> tuple[dict, dict]:
    """One clause: the built object (data/ shape) and the comparison entry. Raises Unscorable when the source cannot be read."""
    section, path, definition = ecfr.parse_clause_id(cid)
    date = committed.get("effective_date")
    entry: dict[str, Any] = {"id": cid, "section": section, "effective_date": date, "reasons": [], "read": {}}
    built = {
        **{k: hand.get(k) for k in ("citation",)},
        "text": None, "lead_in": None, "source_note": None,
        "ecfr_url": hand.get("ecfr_url"), "ecfr_as_of": as_of, "effective_date": None, "text_copied_on": today,
        "existence_checked_by_hand_on": hand.get("existence_checked_by_hand_on"), "note": hand.get("note"),
    }
    try:
        ecfr.iso_date(date, field_name=f"{cid}.effective_date")
    except ValueError as exc:
        entry["reasons"].append(f"effective_date: committed {date!r} is not a date ({exc})")
        date = None
    try:
        versions = ecfr.section_versions(section)
    except (fetch.SourceUnread, fetch.FetchNotAllowedError, fetch.ResponseTooLargeError, ValueError) as exc:
        raise Unscorable(f"{cid}: the versioner could not be read for {section}: {exc}") from exc
    entry["read"]["versions"] = versions
    listed = date is not None and date in versions["dates"]
    entry["version_listed"] = listed
    if date is not None and not listed:
        entry["reasons"].append(f"effective_date: committed {date} is not a version the versioner lists for {section}; it lists {versions['dates']}")
    if listed:
        built["effective_date"] = date
        url = ecfr.section_url(section, date)
        entry["read"]["section_url"] = url
        try:
            xml = ecfr.fetch_section_xml(section, date)
        except (fetch.SourceUnread, fetch.FetchNotAllowedError, fetch.ResponseTooLargeError) as exc:
            raise Unscorable(f"{cid}: the section could not be read at {date}: {exc}") from exc
        try:
            parsed = ecfr.parse_section(xml, section)
        except (ecfr.ClauseNotLocated, ValueError) as exc:
            raise Unscorable(f"{cid}: the reader could not rebuild the lettering of {section} at {date}: {exc}") from exc
        built["source_note"] = parsed.source_note
        try:
            found = ecfr.locate(parsed, path, definition=definition, append_subparagraphs=bool(hand.get("append_subparagraphs")))
        except ecfr.ClauseNotLocated as exc:
            entry["reasons"].append(f"text: no paragraph at the clause's lettering in {section} at {date}: {exc}")
            found = None
        if found is not None:
            built["text"] = found["text"]
            built["lead_in"] = found["lead_in"] if hand.get("lead_in") else None
            entry["read"]["appended"] = found["appended"]
            entry["read"]["parent_paragraph"] = found["lead_in"]
    if not hand.get("lead_in"):
        built.pop("lead_in")
    fields = {}
    for name in CLAUSE_FIELDS:
        c, s = committed.get(name), built.get(name)
        if name == "lead_in" and "lead_in" not in committed and "lead_in" not in built:
            continue
        fields[name] = {"equal": c == s, "committed": c, "source": s}
        if c != s and not any(r.startswith(name + ":") for r in entry["reasons"]):
            entry["reasons"].append(f"{name}: differs from the source at {date}" if listed else f"{name}: not read, no version at {date}")
    entry["fields"] = fields
    entry["keys_not_compared"] = sorted(set(committed) - set(CLAUSE_FIELDS))
    entry["matched"] = not entry["reasons"]
    entry["why"] = "all equal" if entry["matched"] else "; ".join(entry["reasons"])
    ordered = {k: built[k] for k in CLAUSE_ORDER if k in built}
    return ordered, entry


# ------------------------------------------------------------------- rows
def build_row(committed: dict, hand: dict, today: str) -> tuple[dict, dict]:
    """One row: the built object (data/ shape) and the comparison entry. Raises Unscorable when the source cannot be read at the row's version."""
    rid = committed["table_row"]
    setid = dailymed.set_id(hand["dailymed_set_id"])
    read_on = ecfr.iso_date(hand["label_read_on"], field_name=f"{rid}.label_read_on")
    code = hand["section"]
    entry: dict[str, Any] = {"table_row": rid, "dailymed_set_id": setid, "label_read_on": read_on, "page": dailymed.page_url(setid), "reasons": [], "read": {}}
    try:
        hist = dailymed.history(setid)
    except (fetch.SourceUnread, fetch.FetchNotAllowedError, fetch.ResponseTooLargeError, ValueError, KeyError) as exc:
        raise Unscorable(f"{rid}: DailyMed's history could not be read for {setid}: {exc}") from exc
    entry["read"]["history"] = hist
    later = dailymed.published_after(hist, read_on)
    entry["published_after_read"] = later
    if later:
        raise Unscorable(
            f"{rid}: {len(later)} version(s) of {setid} published after label_read_on {read_on} "
            f"(latest {later[0]['spl_version']} on {later[0]['published']}); the SPL at the row's version cannot be read by machine, see {dailymed.page_url(setid)}"
        )
    try:
        xml = dailymed.fetch_spl(setid)
        label = dailymed.parse_spl(xml)
    except (fetch.SourceUnread, fetch.FetchNotAllowedError, fetch.ResponseTooLargeError, ValueError, AttributeError) as exc:
        raise Unscorable(f"{rid}: the SPL could not be read for {setid}: {exc}") from exc
    if label.set_id != setid:
        raise Unscorable(f"{rid}: the SPL served is set id {label.set_id}, not {setid}")
    if label.version != hist["current"]["spl_version"]:
        raise Unscorable(f"{rid}: the SPL served is version {label.version}; the history lists {hist['current']['spl_version']} as current")
    derived = dailymed.derive(label, code)
    entry["read"].update(derived["read"])
    entry["spl_version"] = label.version
    entry["effectiveTime"] = label.effective_time
    built = {**{k: hand.get(k) for k in ROW_CARRIED}, "table_row": rid, "dailymed_set_id": setid, **derived["fields"]}
    fields = {}
    for name in ROW_FIELDS:
        c, s = committed.get(name), built.get(name)
        fields[name] = {"equal": c == s, "committed": c, "source": s}
        if c != s:
            entry["reasons"].append(f"{name}: committed {c!r}, source {s!r}")
    entry["fields"] = fields
    entry["section_terms"] = {
        "compared": False,
        "committed": committed.get("section_terms"),
        "headings_read": derived["read"]["headings_read"],
        "why": "a reading, not a structure the SPL carries; the hand confirmation is owed (Unsure 8, 11)",
    }
    entry["matched"] = not entry["reasons"]
    entry["why"] = "all equal" if entry["matched"] else "; ".join(entry["reasons"])
    return {k: built.get(k) for k in ROW_ORDER}, entry


# ------------------------------------------------------------------- gate
def judge(clauses: list[dict], rows: list[dict], unreadable: list[dict]) -> dict:
    clauses_mismatched = [e["id"] for e in clauses if not e["matched"]]
    rows_mismatched = [e["table_row"] for e in rows if not e["matched"]]
    if unreadable:
        verdict = "UNSCORABLE"
        reason = "a source could not be read at an entry's version, so F2.1 is not judged: " + "; ".join(u["what"] for u in unreadable)
    elif clauses_mismatched or rows_mismatched:
        verdict = "RED"
        parts = []
        if clauses_mismatched:
            parts.append(f"clauses {', '.join(clauses_mismatched)} differ from the source at their version")
        if rows_mismatched:
            parts.append(f"rows {', '.join(rows_mismatched)} differ from the SPL at their version")
        reason = "F2.1 holds: " + "; ".join(parts)
    else:
        verdict = "GREEN"
        reason = "F2.1 does not hold: every compared field of every clause and row equals the build from the source at its version"
    return {
        "verdict": verdict,
        "reason": reason,
        "clauses_mismatched": clauses_mismatched,
        "rows_mismatched": rows_mismatched,
        "unreadable": unreadable,
        "counts": {
            "clauses": {"total": len(clauses), "matched": sum(e["matched"] for e in clauses)},
            "rows": {"total": len(rows), "matched": sum(e["matched"] for e in rows)},
            "unreadable": len(unreadable),
        },
    }


def summary_markdown(result: dict) -> str:
    lines = [f"## M02 gate: {result['verdict']}", "", result["reason"] + ".", ""]
    lines.append(f"Commit `{result.get('commit') or 'unknown'}`" + (" (dirty tree)" if result.get("dirty") else "") + f", written by CI: `{result['written_by_ci']}`.")
    lines.append("")
    if "error" in result:
        err = result["error"]
        lines += [f"`{err['type']}: {err['message']}`", ""]
    if result.get("ecfr"):
        lines += [f"eCFR title 21 up to date as of `{result['ecfr']['up_to_date_as_of']}`; `text_copied_on` `{result.get('text_copied_on')}`.", ""]
    if result.get("clauses"):
        lines += ["| clause | effective_date | listed | text | lead_in | source_note | why |", "|---|---|---|---|---|---|---|"]
        for e in result["clauses"]:
            f = e.get("fields", {})
            def eq(name: str) -> str:
                return "n/a" if name not in f else ("yes" if f[name]["equal"] else "no")
            lines.append(f"| {e['id']} | {e['effective_date']} | {'yes' if e.get('version_listed') else 'no'} | {eq('text')} | {eq('lead_in')} | {eq('source_note')} | {e['why']} |")
        lines.append("")
    if result.get("rows"):
        lines += ["| row | SPL version | effectiveTime | fields unequal | why |", "|---|---|---|---|---|"]
        for e in result["rows"]:
            unequal = [n for n, v in e.get("fields", {}).items() if not v["equal"]]
            lines.append(f"| {e['table_row']} | {e.get('spl_version')} | {e.get('effectiveTime')} | {', '.join(unequal) or 'none'} | {e['why']} |")
        lines.append("")
    if result.get("unreadable"):
        lines += ["Unread at its version:", ""] + [f"- {u['what']}" for u in result["unreadable"]] + [""]
    if result["verdict"] == "UNSCORABLE":
        lines.append("UNSCORABLE is not a verdict on ledger row 2's F2.1. It is never RED and never GREEN.")
    else:
        lines.append("The verdict judges ledger row 2's F2.1 only. `section_terms` and the provenance fields are recorded, not compared.")
    return "\n".join(lines) + "\n"


def write_sources(out_dir: Path) -> dict[str, str]:
    """Every response read, as a file under sources/, and an index of file to URL."""
    src = out_dir / "sources"
    src.mkdir(parents=True, exist_ok=True)
    index = {}
    for url, body in fetch._cache.items():  # noqa: SLF001  the cache is the record of what was read
        stem = re.sub(r"[^A-Za-z0-9.=-]+", "_", url.split("://", 1)[1])[:120]
        name = f"{stem}.{hashlib.sha256(url.encode()).hexdigest()[:8]}"
        (src / name).write_bytes(body)
        index[name] = url
    (src / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    return index


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_result(args: argparse.Namespace, result: dict) -> None:
    write_json(args.out_dir / "result.json", result)
    text = summary_markdown(result)
    print(text)
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        with args.summary.open("a", encoding="utf-8") as fh:
            fh.write(text)


def run(args: argparse.Namespace) -> int:
    committed_clauses = json.loads((args.data / "clauses.json").read_text(encoding="utf-8"))
    committed_rows = json.loads((args.data / "table.json").read_text(encoding="utf-8"))
    hand_clauses = json.loads((args.hand / "clauses.json").read_text(encoding="utf-8"))
    hand_rows = {r["table_row"]: r for r in json.loads((args.hand / "table.json").read_text(encoding="utf-8"))}
    today = datetime.now(UTC).date().isoformat()

    missing = sorted(set(committed_clauses) - set(hand_clauses)) + sorted(set(r["table_row"] for r in committed_rows) - set(hand_rows))
    if missing:
        raise Unscorable(f"no hand entry for {missing}")
    try:
        status = ecfr.title_status()
    except (fetch.SourceUnread, fetch.FetchNotAllowedError, fetch.ResponseTooLargeError, ValueError) as exc:
        raise Unscorable(f"the eCFR titles endpoint could not be read: {exc}") from exc
    as_of = status["up_to_date_as_of"]

    built_clauses, clause_entries, unreadable = {}, [], []
    for cid, committed in committed_clauses.items():
        try:
            built, entry = build_clause(cid, committed, hand_clauses[cid], as_of, today)
        except Unscorable as exc:
            unreadable.append({"kind": "clause", "id": cid, "what": str(exc)})
            continue
        built_clauses[cid] = built
        clause_entries.append(entry)
    built_rows, row_entries = [], []
    for committed in committed_rows:
        try:
            built, entry = build_row(committed, hand_rows[committed["table_row"]], today)
        except Unscorable as exc:
            unreadable.append({"kind": "row", "id": committed["table_row"], "what": str(exc)})
            continue
        built_rows.append(built)
        row_entries.append(entry)

    write_json(args.out_dir / "clauses.json", built_clauses)
    write_json(args.out_dir / "table.json", built_rows)
    sources = write_sources(args.out_dir)
    result = {
        **provenance(),
        "ecfr": status,
        "text_copied_on": today,
        **judge(clause_entries, row_entries, unreadable),
        "clauses": clause_entries,
        "rows": row_entries,
        "sources": sources,
    }
    write_result(args, result)
    return {"GREEN": 0, "RED": 1}.get(result["verdict"], 2)


def unscorable(args: argparse.Namespace, exc: BaseException) -> int:
    refused = isinstance(exc, Unscorable)
    result = {
        **provenance(),
        "verdict": "UNSCORABLE",
        "reason": "the build could not be compared, so F2.1 is not judged: " + ("the gate refused the inputs" if refused else "the gate raised"),
        "error": {"type": type(exc).__name__, "message": str(exc), "traceback": None if refused else traceback.format_exc()},
    }
    print(f"UNSCORABLE: {type(exc).__name__}: {exc}", file=sys.stderr)
    if not refused:
        traceback.print_exc()
    try:
        write_result(args, result)
    except Exception as write_exc:  # noqa: BLE001  the exit code stays 2 even when the result cannot be written
        print(f"UNSCORABLE: could not write {args.out_dir}: {write_exc!r}", file=sys.stderr)
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out-dir", required=True, type=Path, help="where result.json, the built files and sources/ are written")
    parser.add_argument("--summary", type=Path, help="append a Markdown summary here (GITHUB_STEP_SUMMARY in CI)")
    parser.add_argument("--data", type=Path, default=ROOT / "data")
    parser.add_argument("--hand", type=Path, default=ROOT / "src" / "ingest" / "hand")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    try:
        return run(args)
    except Exception as exc:  # noqa: BLE001  every failure to compare is UNSCORABLE, written and exit 2; never the RED code
        return unscorable(args, exc)


if __name__ == "__main__":
    raise SystemExit(main())
