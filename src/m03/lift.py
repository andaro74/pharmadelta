"""The M03 lift: the call to the deployed agent that produces each served answer, made by this repository's CI as `pharmadelta`, and the pages written from its record.

Two commands. Neither changes the gate (`src/m03/gate.py`), which judges
ledger row 4; this module reuses the gate's sign-in and call and writes
what the gate reads.

    uv run python -m src.m03.lift call --out-dir <dir> [--summary <md>]

Runs in CI (`.github/workflows/m03-lift.yml`). Reads the questions
`pages/api/answers.json` serves, signs in to label-impact's identity pool
as `pharmadelta` with the repository secret (Cognito `InitiateAuth`,
`USER_PASSWORD_AUTH`, the gate's `sign_in`), asks the deployed agent each
question through its door (the gate's `ask_door`), and writes
`<dir>/call.json`: for each served answer, the call record (`subject`,
`issuer`, `door_host`, `request_id`, `called_at`, `agent`, `agent_commit`,
`run_url`, the fields M03 ruling pr2.md 7 fixed), the door's reading, and
the answer the call returned, verbatim: `table_row`, `clause_id` and the
answer fields of the door's `parsed`, or null when nothing parsed. The
URL, the pool id, the client id, the password and the token are never
written; `door_host` is the SHA-256 of the door URL's host (M03 Unsure 12).
Exit 0 when every call answered 200 with an observation and every record
is complete; 2 otherwise, and `call.json` says why. A run outside CI
writes `written_by_ci` false, and `write` refuses it: a local call is not
a record (P4).

    uv run python -m src.m03.lift write --from <dir>

By hand, from the artifact of a `call` run (`gh run download`). Rebuilds
`pages/api/answers.json` and `pages/detail.html` from `<dir>/call.json`
and `data/`. Each entry's `answer` is what its call returned; its `row`
and `clause` are copies from `data/table.json` and `data/clauses.json`
when the table holds the answer's `table_row` and the clauses hold its
`clause_id`, else null; `agent` and `call` carry the record; `scripted`
is false; there is no `PLANT` key. The page shows an answer only with its
row and its clause (SPEC/00 §11); otherwise it shows "no row found" with
the question, the call record and what the call returned, verbatim (M03
Unsure 26). The page embeds the same object the API serves. `write` is
deterministic: a reader downloads the artifact the pages name, runs it,
and compares.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import sys
import urllib.parse
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.m03.gate import (
    AGENT,
    CALL_RECORD,
    ENV,
    ROOT,
    SUBJECT,
    Unscorable,
    ask_door,
    check_url,
    ci_context,
    door_answer,
    git,
    read_served,
    sign_in,
    write_json,
)

# The deployed agent (milestones/M03/README.md, "The deployed agent, as read at open"): label-impact at 8cf0563,
# deployed on agentkeel m10. Its manifest admits the caller `pharmadelta` with issuer `self`.
AGENT_REPOSITORY = "agentkeel-studio/label-impact"
AGENT_COMMIT = "8cf0563"
AGENT_PLATFORM = "agentkeel m10"
ISSUER = "self"
ARTIFACT_PREFIX = "m03-lift-"
ANSWER_FIELD_MEANING = {
    "impacted": "this label's section must change because of what the question describes",
    "owed": "what the holder owes now: none; cbe-0 (a changes-being-effected supplement under 314.70(c)(6)(iii)(A)); "
    "follow-rld (keep the label the same as the reference listed drug's and adopt its change when it is approved, "
    "314.150(b)(10)); alert-report (a 15-day Alert report under 314.80(c)(1)(i))",
    "escalate": "an adverse drug experience in the question is both serious and unexpected (314.80(a)) against the "
    "label's 6 row; true starts the reporting path",
}


def host_hash(url: str) -> str:
    """The SHA-256 of the door URL's host, lower-cased: a fingerprint a reader with the variable can confirm; the host itself is never written (Unsure 12)."""
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return "sha256:" + hashlib.sha256(host.encode("utf-8")).hexdigest()


def provenance() -> dict[str, Any]:
    ci = ci_context()
    try:
        commit: str | None = git("rev-parse", "HEAD")
        dirty: bool | None = bool(git("status", "--porcelain"))
    except Exception:  # noqa: BLE001  the commit is still recorded from CI's environment when git cannot answer
        commit, dirty = (ci or {}).get("sha"), None
    return {
        "what": "M03 lift: the call to the deployed agent through its door as pharmadelta that produces each answer "
        "pages/api/answers.json serves; the record the gate reads (milestones/M03/README.md, Close)",
        "milestone": "M03",
        "run_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": commit,
        "dirty": dirty,
        "written_by_ci": ci is not None,
        "ci": ci,
        "agent": AGENT,
        "agent_repository": AGENT_REPOSITORY,
        "agent_commit": AGENT_COMMIT,
        "subject": SUBJECT,
        "issuer": ISSUER,
        "call_record_fields": list(CALL_RECORD),
        "env_set": {name: bool(os.environ.get(var)) for name, var in ENV.items()},
        "env_note": "which of the secret and the three variables the environment held; their values are never written. "
        "door_host is the SHA-256 of the door URL's host, never the host",
    }


# ---------------------------------------------------------------- call
def call(args: argparse.Namespace) -> int:
    out = provenance()
    env = {name: os.environ.get(var) or None for name, var in ENV.items()}
    missing = [ENV[name] for name, value in env.items() if not value]
    calls: list[dict] = []
    if missing:
        out.update(ok=False, why=f"the environment lacks {missing}: no sign-in, no call", calls=calls)
        return finish(args, out)
    try:
        check_url(env["url"])
    except Unscorable as exc:
        out.update(ok=False, why=f"the door: {exc}", calls=calls)
        return finish(args, out)
    served = read_served(args.api)
    token, out["sign_in"] = sign_in(env["pool_id"], env["client_id"], env["password"])
    if token is None:
        out.update(ok=False, why=f"the sign-in failed: {out['sign_in'].get('error')} ({out['sign_in'].get('message')})", calls=calls)
        return finish(args, out)

    run_url = (out["ci"] or {}).get("run_url")
    door_host = host_hash(env["url"])
    ok = True
    for a in served:
        called_at = datetime.now(UTC).isoformat(timespec="seconds")
        if isinstance(a.get("question"), str):
            reading = ask_door(env["url"], token, a["question"])
        else:
            reading = {"asked": False, "why": "the served answer has no question string"}
        record = {
            "subject": SUBJECT,
            "issuer": ISSUER,
            "door_host": door_host,
            "request_id": reading.get("request_id"),
            "called_at": called_at,
            "agent": AGENT,
            "agent_commit": AGENT_COMMIT,
            "run_url": run_url,
        }
        record_missing = [f for f in CALL_RECORD if record.get(f) in (None, "")]
        observed = bool(reading.get("asked") and reading.get("status") == 200 and not reading.get("error") and not reading.get("refused"))
        entry_ok = observed and not record_missing
        why = (
            "the door answered 200 with an observation and the record is complete" if entry_ok
            else f"the record lacks {record_missing}" if observed
            else f"the door answered {reading.get('status')} ({reading.get('error') or reading.get('refused')})" if reading.get("asked")
            else f"not asked ({reading.get('why')})"
        )
        ok = ok and entry_ok
        calls.append({
            "id": a["id"],
            "question": a.get("question"),
            "call": record,
            "record_missing": record_missing,
            "observed": observed,
            "answer": door_answer(reading.get("parsed")) if observed else None,
            "door": reading,
            "ok": entry_ok,
            "why": why,
        })
    out.update(ok=ok, calls=calls, why="every call answered 200 with an observation and every record is complete" if ok else "a call did not produce a complete record; see each call's `why`")
    return finish(args, out)


def finish(args: argparse.Namespace, out: dict) -> int:
    write_json(args.out_dir / "call.json", out)
    text = call_summary(out)
    print(text)
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        with args.summary.open("a", encoding="utf-8") as fh:
            fh.write(text)
    return 0 if out.get("ok") else 2


def call_summary(out: dict) -> str:
    lines = [f"## M03 lift call: {'record written' if out.get('ok') else 'no record'}", "", f"{out.get('why')}.", ""]
    lines.append(f"Commit `{out.get('commit') or 'unknown'}`" + (" (dirty tree)" if out.get("dirty") else "") + f", written by CI: `{out['written_by_ci']}`.")
    lines.append("")
    if out.get("sign_in"):
        s = out["sign_in"]
        lines += [f"Sign-in as `{s.get('username')}`: signed in `{s.get('signed_in')}`" + (f", status `{s.get('status')}`" if s.get("status") is not None else "") + (f", `{s.get('error')}`" if s.get("error") else "") + ".", ""]
    if out.get("calls"):
        lines += ["| served | door status | request id | called_at | stop_reason | parsed | record |", "|---|---|---|---|---|---|---|"]
        for c in out["calls"]:
            d = c["door"]
            parsed = d.get("parsed")
            parsed_s = "null" if parsed is None else ("object" if isinstance(parsed, dict) else type(parsed).__name__)
            lines.append(f"| {c['id']} | {d.get('status') if d.get('asked') else 'not asked'} | {c['call'].get('request_id') or 'none'} | {c['call']['called_at']} | {d.get('stop_reason') or ''} | {parsed_s} | {'complete' if c['ok'] else c['why']} |")
        lines.append("")
    lines.append("A record is evidence only when CI wrote it (P4). `write` rebuilds the pages from this run's artifact; the gate judges row 4.")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------- write
def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def json_text(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


def script_json(obj: Any) -> str:
    """The object for a <script type="application/json"> block: `</` escaped as `<\\/`, which JSON reads back as `</`."""
    return json_text(obj).replace("</", "<\\/")


def build_entries(doc: dict) -> list[dict]:
    table = {r["table_row"]: r for r in json.loads((ROOT / "data" / "table.json").read_text(encoding="utf-8"))}
    clauses = json.loads((ROOT / "data" / "clauses.json").read_text(encoding="utf-8"))
    entries = []
    for c in doc["calls"]:
        answer = c.get("answer")
        row = clause = None
        if isinstance(answer, dict):
            row = table.get(answer.get("table_row"))
            found = clauses.get(answer.get("clause_id"))
            if isinstance(found, dict):
                clause = {"id": answer.get("clause_id"), **found}
        door = c.get("door") or {}
        entries.append({
            "id": c["id"],
            "question": c.get("question"),
            "answer": answer,
            "row": row,
            "clause": clause,
            "agent": {"name": AGENT, "repository": AGENT_REPOSITORY, "commit": AGENT_COMMIT, "platform": AGENT_PLATFORM},
            "call": c["call"],
            "door": {
                "status": door.get("status"),
                "request_id_header": door.get("request_id_header"),
                "stop_reason": door.get("stop_reason"),
                "parsed": door.get("parsed"),
                "text": door.get("text"),
            },
            "scripted": False,
        })
    return entries


def api_document(old: dict, doc: dict, entries: list[dict], data_commit: str) -> dict:
    ci = doc.get("ci") or {}
    return {
        "what": "The public API of pharmadelta: the answers it serves, one per question, each produced by a call to the "
        "deployed agent through its door as the caller pharmadelta, made by this repository's CI, with the record of "
        "that call (milestones/M03/README.md). `answer` is what the call returned, verbatim; `row` and `clause` are "
        "copies of data/table.json and data/clauses.json at `data_commit` when the table holds the answer's row and the "
        "clauses hold its clause, else null. A number in this file is the row's or the clause's own data, or the call "
        "record's, never a measured result.",
        "agent": old.get("agent", f"{AGENT}, {AGENT_REPOSITORY}, the deployed agent (SPEC/00 §3, §6)"),
        "company": old.get("company", "Ardentia Generics is fictional; its portfolio and every 'our label' statement are invented (SPEC/00 §2, §9)"),
        "data_commit": data_commit,
        "lift": {
            "run_url": ci.get("run_url"),
            "artifact": f"{ARTIFACT_PREFIX}{ci.get('sha')}",
            "written_from": "call.json in that artifact; `uv run python -m src.m03.lift write --from <dir>` rebuilds this file and pages/detail.html from it",
        },
        "answers": entries,
    }


def answer_shown(entry: dict) -> bool:
    """An answer is shown only with its row and its clause (SPEC/00 §11)."""
    return isinstance(entry.get("answer"), dict) and isinstance(entry.get("row"), dict) and isinstance(entry.get("clause"), dict)


def page_title(entries: list[dict]) -> str:
    if len(entries) == 1:
        e = entries[0]
        if answer_shown(e):
            r = e["row"]
            return f"LabelKeel: {r.get('ingredient')} {r.get('dosage_form')}, {r.get('section')} {r.get('section_title')}"
        return f"LabelKeel: {e['id']}, no row found"
    return "LabelKeel: the answers the API serves"


def render_answer(e: dict, api: dict) -> str:
    out = []
    out.append(f"<h1>{esc('Does this rule change touch our label, and what do we owe?')}</h1>")
    out.append("<h2>The question</h2>")
    out.append(f"<blockquote><p>{esc(e.get('question'))}</p></blockquote>")
    answer, row, clause, call, door = e.get("answer"), e.get("row"), e.get("clause"), e["call"], e.get("door") or {}
    if answer_shown(e):
        out.append("<h2>The answer</h2>")
        out.append(f"<p>Row <code>{esc(answer['table_row'])}</code> under clause <code>{esc(answer['clause_id'])}</code>, as the agent answered on the call recorded below.</p>")
        out.append("<table>")
        out.append("  <thead><tr><th>Field</th><th>Value</th><th>Meaning (milestones/M00/fields.md)</th></tr></thead>")
        out.append("  <tbody>")
        fields = answer.get("answer_fields") or {}
        for name in ("impacted", "owed", "escalate"):
            out.append(f"        <tr><th scope=\"row\">{esc(name)}</th><td><code>{esc(json.dumps(fields.get(name)))}</code></td><td>{esc(ANSWER_FIELD_MEANING[name])}</td></tr>")
        out.append("  </tbody>")
        out.append("</table>")
        out.append(f"<h2>Its row: <code>{esc(row['table_row'])}</code></h2>")
        out.append(f"<p>One row of the label table, <code>data/table.json</code> at <code>{esc(api['data_commit'])}</code>, as the table holds it. "
                   "The DailyMed-sourced fields were read from the SPL at the set id on <code>label_read_on</code>; the holder is fictional (<code>holder_fictional</code>).</p>")
        out.append("<table>")
        out.append("  <tbody>")
        for k, v in row.items():
            out.append(f"        <tr><th scope=\"row\">{esc(k)}</th><td>{esc(v if not isinstance(v, bool) else json.dumps(v))}</td></tr>")
        out.append("  </tbody>")
        out.append("</table>")
        out.append(f"<h2>Its clause: {esc(clause.get('citation'))}</h2>")
        out.append(f"<p>From <code>data/clauses.json</code> at <code>{esc(api['data_commit'])}</code>. Text of the paragraph at the version of its section "
                   f"in force from <code>{esc(clause.get('effective_date'))}</code>, read from the eCFR; existence checked by hand on "
                   f"<code>{esc(clause.get('existence_checked_by_hand_on'))}</code> (SPEC/00 §10, P7).</p>")
        if clause.get("lead_in"):
            out.append(f"<blockquote><p>{esc(clause['lead_in'])}</p></blockquote>")
        out.append(f"<blockquote><p>{esc(clause.get('text'))}</p></blockquote>")
        out.append(f"<p>Source note: <code>{esc(clause.get('source_note'))}</code>. eCFR: <a href=\"{esc(clause.get('ecfr_url'))}\">{esc(clause.get('ecfr_url'))}</a>."
                   + (f"\n   Note: {esc(clause['note'])}" if clause.get("note") else "") + "</p>")
    else:
        out.append("<h2>No row found</h2>")
        if answer is None:
            what = "The call returned no parsed answer"
        elif not isinstance(row, dict):
            what = f"The call returned <code>table_row</code> <code>{esc(json.dumps(answer.get('table_row')))}</code>, which is not a row of <code>data/table.json</code>"
        else:
            what = f"The call returned <code>clause_id</code> <code>{esc(json.dumps(answer.get('clause_id')))}</code>, which is not a clause of <code>data/clauses.json</code>"
        out.append('<div class="norow" role="note">')
        out.append(f"  <p><strong>No row found.</strong> {what} (<code>stop_reason</code> <code>{esc(door.get('stop_reason'))}</code>). "
                   "This page shows no answer here: an answer is shown only with its row and its clause (SPEC/00 §11). "
                   "No row and no clause are copied in. What the call returned is below, verbatim, and the call's record follows.</p>")
        out.append("</div>")
        out.append("<h3>What the call returned, verbatim</h3>")
        out.append(f"<p>The door's <code>parsed</code> object, or <code>null</code> when the agent's text held no JSON object:</p>")
        out.append(f"<pre>{esc(json_text(door.get('parsed')))}</pre>")
        if door.get("text"):
            out.append("<p>The agent's text on that call, verbatim. It is the agent's own words, not this page's:</p>")
            out.append(f"<pre>{esc(door['text'])}</pre>")
    out.append("<h2>Where this answer came from</h2>")
    out.append("<p>The record of the call that produced it, made by this repository's CI as <code>pharmadelta</code>. "
               "The run linked under <code>run_url</code> wrote the record; its artifact holds the door's full reading.</p>")
    out.append("<table>")
    out.append("  <tbody>")
    a = e["agent"]
    out.append(f"        <tr><th scope=\"row\">agent</th><td><code>{esc(a['name'])}</code>, {esc(a['repository'])} at <code>{esc(a['commit'])}</code>, deployed on {esc(a['platform'])}</td></tr>")
    for k in CALL_RECORD:
        v = call.get(k)
        if k == "run_url" and v:
            cell = f"<a href=\"{esc(v)}\">{esc(v)}</a>"
        elif k == "door_host":
            cell = f"<code>{esc(v)}</code> (the SHA-256 of the door URL's host; the host is not written, M03 Unsure 12)"
        else:
            cell = f"<code>{esc(v)}</code>"
        out.append(f"        <tr><th scope=\"row\">call.{esc(k)}</th><td>{cell}</td></tr>")
    out.append(f"        <tr><th scope=\"row\">door status</th><td><code>{esc(door.get('status'))}</code>, request id in <code>{esc(door.get('request_id_header'))}</code></td></tr>")
    out.append(f"        <tr><th scope=\"row\">scripted</th><td><code>false</code></td></tr>")
    out.append("  </tbody>")
    out.append("</table>")
    return "\n".join(out)


def render_page(api: dict) -> str:
    entries = api["answers"]
    block = entries[0] if len(entries) == 1 else entries
    scripted = [e["id"] for e in entries if e.get("scripted")]
    parts = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(page_title(entries))}</title>",
        "<style>",
        "  body { font-family: Georgia, serif; max-width: 52rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; color: #1a1a1a; background: #fff; }",
        "  .scripted { border: 3px solid #b00020; padding: 0.75rem 1rem; background: #fff4f4; }",
        "  .scripted strong { color: #b00020; }",
        "  .norow { border: 3px solid #8a6d00; padding: 0.75rem 1rem; background: #fffbe6; }",
        "  .norow strong { color: #8a6d00; }",
        "  table { border-collapse: collapse; width: 100%; margin: 0.5rem 0 1rem; }",
        "  th, td { border: 1px solid #bbb; padding: 0.3rem 0.5rem; text-align: left; vertical-align: top; font-size: 0.95rem; }",
        "  th[scope=row] { width: 11rem; font-weight: normal; color: #444; }",
        "  blockquote { border-left: 4px solid #999; margin: 0.5rem 0; padding: 0.25rem 1rem; }",
        "  pre { white-space: pre-wrap; word-break: break-word; font-size: 0.85rem; background: #f6f6f6; padding: 0.5rem; }",
        "  footer { margin-top: 2rem; font-size: 0.9rem; color: #444; }",
        "  code { font-family: Consolas, monospace; }",
        "</style>",
        "</head>",
        "<body>",
        "<header>",
        "  <p><strong>pharmadelta</strong> · LabelKeel (a placeholder name for this page, SPEC/00 §11) · detail page</p>",
        "  <p>pharmadelta is an independent open-source demo and is not affiliated with any pharmaceutical company.",
        "     The company, Ardentia Generics, is fictional; its portfolio and every “our label” statement are invented.",
        "     The label is a real public-domain label of an old off-patent generic, read from DailyMed.</p>",
        f"  <p>Every answer on this page was produced by a call to the deployed agent, <code>{esc(AGENT)}</code>, through its door as the caller",
        f"     <code>{esc(SUBJECT)}</code>, made by this repository's CI: <a href=\"{esc(api['lift']['run_url'])}\">{esc(api['lift']['run_url'])}</a>,",
        f"     artifact <code>{esc(api['lift']['artifact'])}</code>. The API this page copies is <code>api/answers.json</code>.</p>",
        "</header>",
    ]
    if scripted:
        parts += [
            '<div class="scripted" role="note">',
            f"  <p><strong>Scripted.</strong> The answers {esc(', '.join(scripted))} below were written by hand. No call to the deployed agent produced them (P8).</p>",
            "</div>",
        ]
    for e in entries:
        parts.append(render_answer(e, api))
    parts += [
        "<h2>The same answer, as the API serves it</h2>",
        "<p>The object below is the entry in <code>api/answers.json</code>, the same JSON value. A reader of the page reads it from here.</p>",
        '<script type="application/json" id="answer">',
        script_json(block),
        "</script>",
        f"<pre>{esc(json_text(block))}</pre>",
        "<footer>",
        "  <p>This demo produces the evidence a validation would need. It is not medical information: the agent assesses",
        "     regulatory impact on labeling and never answers a treatment question (SPEC/00 §2). The authority for what this demo claims is",
        "     <code>SPEC/00-overview.md</code>; what was measured is in <code>milestones/README.md</code>. No number on this page is a",
        "     measured result: the row's and the clause's numbers are their own data, and the call record's are the CI run's, linked above.</p>",
        "</footer>",
        "</body>",
        "</html>",
    ]
    return "\n".join(parts) + "\n"


def write(args: argparse.Namespace) -> int:
    path = args.from_dir / "call.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not doc.get("written_by_ci"):
        print(f"refused: {path} was not written by CI; a local call is not a record (P4)", file=sys.stderr)
        return 2
    if not doc.get("ok"):
        print(f"refused: {path} holds no complete record: {doc.get('why')}", file=sys.stderr)
        for c in doc.get("calls") or []:
            print(f"  {c['id']}: {c['why']}", file=sys.stderr)
        return 2
    old = json.loads(args.api.read_text(encoding="utf-8")) if args.api.exists() else {}
    data_commit = git("log", "-1", "--format=%h", "--", "data/")
    entries = build_entries(doc)
    api = api_document(old, doc, entries, data_commit)
    args.api.parent.mkdir(parents=True, exist_ok=True)
    # LF on every platform, as .gitattributes stores the files: a rebuild on Windows then equals the committed bytes.
    args.api.write_text(json_text(api) + "\n", encoding="utf-8", newline="\n")
    args.page.write_text(render_page(api), encoding="utf-8", newline="\n")
    for e in entries:
        print(f"{e['id']}: {'answer shown with its row and its clause' if answer_shown(e) else 'no row found; the page shows the question, the record and what the call returned'}; request_id {e['call']['request_id']}; run {e['call']['run_url']}")
    print(f"wrote {args.api} and {args.page} from {path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_call = sub.add_parser("call", help="in CI: sign in, ask the door each served question, write call.json")
    p_call.add_argument("--out-dir", required=True, type=Path)
    p_call.add_argument("--summary", type=Path, help="append a Markdown summary here (GITHUB_STEP_SUMMARY in CI)")
    p_call.add_argument("--api", type=Path, default=ROOT / "pages" / "api" / "answers.json")
    p_write = sub.add_parser("write", help="by hand: rebuild the pages from a call run's artifact")
    p_write.add_argument("--from", dest="from_dir", required=True, type=Path, help="the directory holding call.json")
    p_write.add_argument("--api", type=Path, default=ROOT / "pages" / "api" / "answers.json")
    p_write.add_argument("--page", type=Path, default=ROOT / "pages" / "detail.html")
    args = parser.parse_args()
    if args.command == "call":
        args.out_dir.mkdir(parents=True, exist_ok=True)
        try:
            return call(args)
        except Exception as exc:  # noqa: BLE001  a call that raised leaves a file that says so, never a half record
            out = {**provenance(), "ok": False, "why": f"the lift raised: {type(exc).__name__}: {exc}", "calls": []}
            return finish(args, out)
    return write(args)


if __name__ == "__main__":
    raise SystemExit(main())
