"""The M04 lift: the pages rebuilt from the artifact of a CI run of the frozen baseline, so each ordinary-assistant answer carries that run's record.

One command. It does not change the gate (`src/m04/gate.py`), which judges
ledger row 5, and not one line of `src/baseline/` (P5); it writes what the
gate reads.

    uv run python -m src.m04.lift write --from <dir>

By hand, from the artifact `m04-gate-<sha>` of a run of the `m04` workflow
(`gh run download <run id>`). The artifact holds two files the same job
wrote: `observations.json`, what `uv run python -m src.baseline.run` wrote
over `goldens/` (the observation of each golden, the commit, `started_at`,
`method`), and `result.json`, the gate's own result with the run's URL,
`written_by_ci` and the last commit touching `src/baseline/`. `write`
rebuilds `pages/api/baseline.json` and `pages/side-by-side.html` from them
and `data/`:

- the served ids are the ones `pages/api/baseline.json` already serves;
  each entry's `question` is its golden's (`goldens/<id>.yaml`), which is
  what the baseline answered and what the gate compares against;
- `answer` is the run's observation of that id, verbatim: `table_row`,
  `clause_id` and the three `answer_fields`;
- `row` and `clause` are copies from `data/table.json` and
  `data/clauses.json` at their last commit when the table holds the
  answer's `table_row` and the clauses hold its `clause_id`, else null;
- `run` is the record the gate reads (M04 `rulings/pr2.md` 1): `run_url`,
  `artifact`, `commit`, `baseline_commit`, `started_at`, `method`,
  `written_by_ci`;
- `scripted` is false and there is no `PLANT` key; the file names, under
  `lift`, the run and the artifact it was written from.

`write` refuses an artifact whose `result.json` says CI did not write it,
whose two files name different commits, or that holds no observation of a
served id: a local run is not a record (P4). The page shows an answer only
with its row and its clause (SPEC/00 §11); the agent column is the entry
`pages/api/answers.json` serves, unchanged. Both columns are embedded as
the gate reads them, `id="baseline-answer"` and `id="agent-answer"`. The
rebuild is deterministic and writes LF on every platform: a reader
downloads the artifact the pages name, runs `write`, and compares.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any

import yaml

from src.m04.gate import ANSWER_FIELDS, ROOT, RUN_RECORD, git

ARTIFACT_PREFIX = "m04-gate-"
ANSWER_FIELD_MEANING = {
    "impacted": "this label's section must change because of what the question describes",
    "owed": "what the holder owes now: none; cbe-0 (a changes-being-effected supplement under 314.70(c)(6)(iii)(A)); "
    "follow-rld (keep the label the same as the reference listed drug's and adopt its change when it is approved, "
    "314.150(b)(10)); alert-report (a 15-day Alert report under 314.80(c)(1)(i))",
    "escalate": "an adverse drug experience in the question is both serious and unexpected (314.80(a)) against the "
    "label's 6 row; true starts the reporting path",
}
PAGE_TITLE = "pharmadelta: side by side, {ids}"


class Refused(Exception):
    """The artifact is not a record the pages may be written from."""


# ------------------------------------------------------------- the record
def read_artifact(from_dir: Path) -> tuple[dict, dict]:
    observations_path, result_path = from_dir / "observations.json", from_dir / "result.json"
    try:
        observations = json.loads(observations_path.read_text(encoding="utf-8"))
        result = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Refused(f"{from_dir} does not hold observations.json and result.json as JSON: {exc}") from exc
    if result.get("written_by_ci") is not True:
        raise Refused(f"{result_path} was not written by CI (written_by_ci {result.get('written_by_ci')!r}); a local run is not a record (P4)")
    ci = result.get("ci") or {}
    if not ci.get("run_url") or not ci.get("sha"):
        raise Refused(f"{result_path} names no run URL or no sha under `ci`")
    if observations.get("commit") != result.get("commit") or result.get("commit") != ci.get("sha"):
        raise Refused(
            f"the two files name different commits: observations.json {observations.get('commit')}, "
            f"result.json {result.get('commit')}, ci.sha {ci.get('sha')}"
        )
    if observations.get("dirty") is not False:
        raise Refused(f"observations.json was written from a dirty tree (dirty {observations.get('dirty')!r})")
    if not isinstance(observations.get("observations"), list):
        raise Refused("observations.json holds no `observations` list")
    baseline_commit = (result.get("baseline") or {}).get("baseline_commit")
    if not baseline_commit:
        raise Refused("result.json records no `baseline.baseline_commit`; the record needs the last commit touching src/baseline/")
    return observations, result


def run_record(observations: dict, result: dict) -> dict:
    """The seven fields the gate reads (`RUN_RECORD`), each from the artifact and nothing from this machine."""
    ci = result["ci"]
    record = {
        "run_url": ci["run_url"],
        "artifact": f"{ARTIFACT_PREFIX}{ci['sha']}",
        "commit": observations["commit"],
        "baseline_commit": result["baseline"]["baseline_commit"],
        "started_at": observations.get("started_at"),
        "method": observations.get("method"),
        "written_by_ci": result["written_by_ci"],
    }
    missing = [f for f in RUN_RECORD if record.get(f) in (None, "")]
    if missing:
        raise Refused(f"the artifact gives no value for {missing} of the run record")
    return {f: record[f] for f in RUN_RECORD}


def observation_answer(observation: dict) -> dict:
    fields = observation.get("answer_fields") if isinstance(observation.get("answer_fields"), dict) else {}
    return {
        "table_row": observation.get("table_row"),
        "clause_id": observation.get("clause_id"),
        "answer_fields": {f: fields.get(f) for f in ANSWER_FIELDS},
    }


def golden_question(goldens: Path, answer_id: str) -> str:
    path = goldens / f"{answer_id}.yaml"
    try:
        golden = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise Refused(f"{path} could not be read: {type(exc).__name__}: {exc}") from exc
    question = golden.get("question") if isinstance(golden, dict) else None
    if not isinstance(question, str) or not question:
        raise Refused(f"{path} holds no `question` string")
    return question


def build_entries(ids: list[str], observations: dict, result: dict, goldens: Path) -> list[dict]:
    table = {r["table_row"]: r for r in json.loads((ROOT / "data" / "table.json").read_text(encoding="utf-8"))}
    clauses = json.loads((ROOT / "data" / "clauses.json").read_text(encoding="utf-8"))
    by_id = {o["id"]: o for o in observations["observations"] if isinstance(o, dict) and isinstance(o.get("id"), str)}
    record = run_record(observations, result)
    entries = []
    for answer_id in ids:
        observation = by_id.get(answer_id)
        if observation is None:
            raise Refused(f"the artifact holds no observation of {answer_id}; the baseline runs over goldens/, so nothing it wrote could serve this id")
        answer = observation_answer(observation)
        row = table.get(answer["table_row"])
        found = clauses.get(answer["clause_id"])
        clause = {"id": answer["clause_id"], **found} if isinstance(found, dict) else None
        entries.append({
            "id": answer_id,
            "question": golden_question(goldens, answer_id),
            "answer": answer,
            "row": row,
            "clause": clause,
            "run": dict(record),
            "scripted": False,
        })
    return entries


def api_document(old: dict, record: dict, entries: list[dict], data_commit: str) -> dict:
    return {
        "what": old.get(
            "what",
            "The ordinary assistant's answers pharmadelta serves on the side-by-side page, one per question, each produced by a "
            "run of the frozen baseline (src/baseline/, a keyword matcher with no model, frozen at tag m00, SPEC/00 P5) made by "
            "this repository's CI, with the record of that run (milestones/M04/README.md). `answer` is what the run wrote for the "
            "question, verbatim; `row` and `clause` are copies of data/table.json and data/clauses.json at `data_commit` when the "
            "table holds the answer's row and the clauses hold its clause, else null. A number in this file is the row's or the "
            "clause's own data, or the run record's, never a measured result.",
        ),
        "baseline": old.get(
            "baseline",
            "src/baseline/ of this repository: answer.py, keyword matching over the question, the table and the clauses; run.py, "
            "the runner. No model, no network, no randomness. Frozen at tag m00 and never improved (SPEC/00 P5). It is the control "
            "the agent is compared with. It is a keyword matcher, not an assistant, and the page says so (milestones/M00/rulings/pr2.md 1).",
        ),
        "company": old.get("company", "Ardentia Generics is fictional; its portfolio and every 'our label' statement are invented (SPEC/00 §2, §9)"),
        "data_commit": data_commit,
        "lift": {
            "run_url": record["run_url"],
            "artifact": record["artifact"],
            "written_from": "observations.json and result.json in that artifact; `uv run python -m src.m04.lift write --from <dir>` "
            "rebuilds this file and pages/side-by-side.html from them",
        },
        "answers": entries,
    }


# --------------------------------------------------------------- the page
def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def code(value: Any) -> str:
    return f"<code>{esc(value if not isinstance(value, bool) else json.dumps(value))}</code>"


def json_text(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)


def script_json(obj: Any) -> str:
    """The object for a <script type="application/json"> block: `</` escaped as `<\\/`, which JSON reads back as `</`."""
    return json_text(obj).replace("</", "<\\/")


def answer_shown(entry: dict) -> bool:
    """An answer is shown only with its row and its clause (SPEC/00 §11)."""
    return isinstance(entry.get("answer"), dict) and isinstance(entry.get("row"), dict) and isinstance(entry.get("clause"), dict)


def render_answer(entry: dict, data_commit: str) -> list[str]:
    """The answer with its row and its clause, as the plant's page laid them out; nothing when any of the three is missing."""
    answer, row, clause = entry["answer"], entry["row"], entry["clause"]
    fields = answer.get("answer_fields") or {}
    out = ["<h3>The answer</h3>", "<table>", "  <tbody>"]
    out.append(f"        <tr><th scope=\"row\">table_row</th><td>{code(answer['table_row'])}</td></tr>")
    out.append(f"        <tr><th scope=\"row\">clause_id</th><td>{code(answer['clause_id'])}</td></tr>")
    for name in ANSWER_FIELDS:
        out.append(f"        <tr><th scope=\"row\">{esc(name)}</th><td>{code(fields.get(name))}</td></tr>")
    out += ["  </tbody>", "</table>"]
    out.append("<p>What each answer field means (<code>milestones/M00/fields.md</code>):</p>")
    out += ["<table>", "  <tbody>"]
    for name in ANSWER_FIELDS:
        out.append(f"        <tr><th scope=\"row\">{esc(name)}</th><td>{esc(ANSWER_FIELD_MEANING[name])}</td></tr>")
    out += ["  </tbody>", "</table>"]
    out.append("<h3>The row</h3>")
    out.append(f"<p>Row {code(row['table_row'])} of the label table, as <code>data/table.json</code> holds it at {code(data_commit)}. The holder is fictional; the label is real.</p>")
    out += ["<table>", "  <tbody>"]
    for k, v in row.items():
        out.append(f"        <tr><th scope=\"row\">{esc(k)}</th><td>{code(v)}</td></tr>")
    out += ["  </tbody>", "</table>"]
    out.append("<h3>The clause</h3>")
    out.append(f"<p>Clause {code(clause['id'])}, as <code>data/clauses.json</code> holds it at {code(data_commit)}.</p>")
    if clause.get("lead_in"):
        out.append(f"<blockquote><p>{esc(clause['lead_in'])}</p></blockquote>")
    out.append(f"<blockquote><p>{esc(clause.get('text'))}</p></blockquote>")
    out += ["<table>", "  <tbody>"]
    out.append(f"        <tr><th scope=\"row\">citation</th><td>{esc(clause.get('citation'))}</td></tr>")
    out.append(f"        <tr><th scope=\"row\">source note</th><td>{esc(clause.get('source_note'))}</td></tr>")
    out.append(f"        <tr><th scope=\"row\">eCFR</th><td><a href=\"{esc(clause.get('ecfr_url'))}\">{esc(clause.get('ecfr_url'))}</a></td></tr>")
    out.append(f"        <tr><th scope=\"row\">eCFR as of</th><td>{code(clause.get('ecfr_as_of'))}</td></tr>")
    out.append(f"        <tr><th scope=\"row\">effective date</th><td>{code(clause.get('effective_date'))}</td></tr>")
    out.append(f"        <tr><th scope=\"row\">text copied on</th><td>{code(clause.get('text_copied_on'))}</td></tr>")
    out.append(f"        <tr><th scope=\"row\">existence checked by hand on</th><td>{code(clause.get('existence_checked_by_hand_on'))}</td></tr>")
    if clause.get("note"):
        out.append(f"        <tr><th scope=\"row\">note</th><td>{esc(clause['note'])}</td></tr>")
    out += ["  </tbody>", "</table>"]
    return out


def render_baseline_column(entry: dict, data_commit: str) -> list[str]:
    out = [
        '<section class="column" id="ordinary-assistant">',
        "<h2>An ordinary assistant</h2>",
        "<p><code>src/baseline/</code>, the frozen baseline: keyword matching, no model, no network, no randomness.</p>",
    ]
    if answer_shown(entry):
        out += render_answer(entry, data_commit)
    else:
        answer = entry["answer"]
        if not isinstance(entry.get("row"), dict):
            what = f"The run wrote <code>table_row</code> {code(json.dumps(answer.get('table_row')))}, which is not a row of <code>data/table.json</code>"
        else:
            what = f"The run wrote <code>clause_id</code> {code(json.dumps(answer.get('clause_id')))}, which is not a clause of <code>data/clauses.json</code>"
        out += [
            '<div class="norow" role="note">',
            f"  <p><strong>No row found.</strong> {what}. This page shows no answer here: an answer is shown only with its row and its clause",
            "     (SPEC/00 §11). No row and no clause are copied in. What the run wrote is below, verbatim, and the run's record follows.</p>",
            "</div>",
            "<h3>What the run wrote, verbatim</h3>",
            f"<pre>{esc(json_text(answer))}</pre>",
        ]
    record = entry["run"]
    out += [
        "<h3>Where this answer came from</h3>",
        "<p>The record of the run that produced it: <code>uv run python -m src.baseline.run</code> over <code>goldens/</code>, made by this",
        f"   repository's CI in the <code>m04</code> workflow. The run linked under <code>run_url</code> wrote the observation; its artifact {code(record['artifact'])}",
        "   holds it in <code>observations.json</code> beside the gate's <code>result.json</code>. The time and the commits below are that run's.</p>",
        "<table>",
        "  <tbody>",
    ]
    for k in RUN_RECORD:
        v = record.get(k)
        if k == "run_url" and v:
            cell = f"<a href=\"{esc(v)}\">{esc(v)}</a>"
        elif k == "baseline_commit":
            cell = f"{code(v)} (the last commit touching <code>src/baseline/</code>, at or before tag <code>m00</code>)"
        elif k == "commit":
            cell = f"{code(v)} (the commit the run checked out)"
        else:
            cell = code(v)
        out.append(f"        <tr><th scope=\"row\">run.{esc(k)}</th><td>{cell}</td></tr>")
    out.append(f"        <tr><th scope=\"row\">scripted</th><td>{code(False)}</td></tr>")
    out += ["  </tbody>", "</table>", "</section>"]
    return out


def render_agent_column(entry: dict, api: dict) -> list[str]:
    """The deployed agent's entry as `pages/api/answers.json` serves it, in the shape `pages/detail.html` shows it."""
    agent, call, door = entry.get("agent") or {}, entry.get("call") or {}, entry.get("door") or {}
    lift = api.get("lift") or {}
    out = [
        '<section class="column" id="deployed-agent">',
        "<h2>The deployed agent</h2>",
        f"<p>{code(agent.get('name'))}, {esc(agent.get('repository'))}, called through its door as <code>pharmadelta</code> by this repository's CI.</p>",
    ]
    if answer_shown(entry):
        out += render_answer(entry, api.get("data_commit"))
    else:
        answer = entry.get("answer")
        if answer is None:
            what = "The call returned no parsed answer"
        elif not isinstance(entry.get("row"), dict):
            what = f"The call returned <code>table_row</code> {code(json.dumps(answer.get('table_row')))}, which is not a row of <code>data/table.json</code>"
        else:
            what = f"The call returned <code>clause_id</code> {code(json.dumps(answer.get('clause_id')))}, which is not a clause of <code>data/clauses.json</code>"
        out += [
            '<div class="norow" role="note">',
            f"  <p><strong>No row found.</strong> {what} (<code>stop_reason</code> {code(door.get('stop_reason'))}).",
            "     This page shows no answer here: an answer is shown only with its row and its clause (SPEC/00 §11). No row and no clause are",
            "     copied in. What the call returned is below, verbatim, and the call's record follows.</p>",
            "</div>",
            "<h3>What the call returned, verbatim</h3>",
            "<p>The door's <code>parsed</code> object, or <code>null</code> when the agent's text held no JSON object:</p>",
            f"<pre>{esc(json_text(door.get('parsed')))}</pre>",
        ]
        if door.get("text"):
            out.append("<p>The agent's text on that call, verbatim. It is the agent's own words, not this page's:</p>")
            out.append(f"<pre>{esc(door['text'])}</pre>")
    out += [
        "<h3>Where this answer came from</h3>",
        "<p>The record of the call that produced it, made by this repository's CI as <code>pharmadelta</code>. The run linked under",
        f"   <code>run_url</code> wrote the record; its artifact {code(lift.get('artifact'))} holds the door's full reading.</p>",
        "<table>",
        "  <tbody>",
        f"        <tr><th scope=\"row\">agent</th><td>{code(agent.get('name'))}, {esc(agent.get('repository'))} at {code(agent.get('commit'))}, deployed on {esc(agent.get('platform'))}</td></tr>",
    ]
    for k, v in call.items():
        if k == "run_url" and v:
            cell = f"<a href=\"{esc(v)}\">{esc(v)}</a>"
        elif k == "door_host":
            cell = f"{code(v)} (the SHA-256 of the door URL's host; the host is not written, M03 Unsure 12)"
        else:
            cell = code(v)
        out.append(f"        <tr><th scope=\"row\">call.{esc(k)}</th><td>{cell}</td></tr>")
    out.append(f"        <tr><th scope=\"row\">door status</th><td>{code(door.get('status'))}, request id in {code(door.get('request_id_header'))}</td></tr>")
    out.append(f"        <tr><th scope=\"row\">scripted</th><td>{code(bool(entry.get('scripted')))}</td></tr>")
    out += ["  </tbody>", "</table>", "</section>"]
    return out


def render_page(baseline_api: dict, agent_api: dict) -> str:
    entries = baseline_api["answers"]
    agent_by_id = {a["id"]: a for a in agent_api.get("answers") or [] if isinstance(a, dict) and isinstance(a.get("id"), str)}
    agent_entries = [agent_by_id[e["id"]] for e in entries if e["id"] in agent_by_id]
    baseline_block = entries[0] if len(entries) == 1 else entries
    agent_block = agent_entries[0] if len(agent_entries) == 1 else agent_entries
    scripted = [e["id"] for e in entries if e.get("scripted")]
    lift = baseline_api["lift"]
    parts = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(PAGE_TITLE.format(ids=', '.join(e['id'] for e in entries)))}</title>",
        "<style>",
        "  body { font-family: Georgia, serif; max-width: 72rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; color: #1a1a1a; background: #fff; }",
        "  .columns { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: start; }",
        "  @media (max-width: 60rem) { .columns { grid-template-columns: 1fr; } }",
        "  .column { border: 1px solid #ccc; padding: 0 1rem 1rem; }",
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
        "  <p><strong>pharmadelta</strong> · side-by-side page</p>",
        "  <p>pharmadelta is an independent open-source demo and is not affiliated with any pharmaceutical company.",
        "     The company, Ardentia Generics, is fictional; its portfolio and every “our label” statement are invented.",
        "     The label is a real public-domain label of an old off-patent generic, read from DailyMed.</p>",
        "  <p>This page shows the same question answered by an ordinary assistant and by the deployed agent (SPEC/00 §1).",
        "     The ordinary assistant is this repository's frozen baseline, <code>src/baseline/</code>: a keyword matcher over the question, the",
        "     label table and the clauses, with no model, frozen at tag <code>m00</code> and never improved (SPEC/00 P5). It is the control",
        "     the agent is compared with, not an assistant anyone would ship. The agent is <code>label-impact</code>, a tenant of agentkeel,",
        "     called through its door as the caller <code>pharmadelta</code>. The left column copies <code>api/baseline.json</code>; the right",
        "     column copies <code>api/answers.json</code>, the same entry the detail page <a href=\"detail.html\">detail.html</a> shows.</p>",
        "  <p>Every ordinary-assistant answer on this page is a real run of the frozen baseline (SPEC/00 §11), made by this repository's CI:",
        f"     <a href=\"{esc(lift['run_url'])}\">{esc(lift['run_url'])}</a>, artifact {code(lift['artifact'])}. The page was rebuilt from",
        "     that artifact by <code>src/m04/lift.py</code>.</p>",
        "</header>",
    ]
    if scripted:
        parts += [
            '<div class="scripted" role="note">',
            f"  <p><strong>Illustration.</strong> The ordinary-assistant answers {esc(', '.join(scripted))} below were written by hand. No run of the baseline produced them (SPEC/00 §11, P8).</p>",
            "</div>",
        ]
    for e in entries:
        parts.append("<h1>Does this rule change touch our label, and what do we owe?</h1>")
        parts.append("<h2>The question</h2>")
        parts.append(f"<blockquote><p>{esc(e.get('question'))}</p></blockquote>")
        parts.append('<div class="columns">')
        parts += render_baseline_column(e, baseline_api["data_commit"])
        agent_entry = agent_by_id.get(e["id"])
        if agent_entry is not None:
            parts += render_agent_column(agent_entry, agent_api)
        else:
            parts += [
                '<section class="column" id="deployed-agent">',
                "<h2>The deployed agent</h2>",
                f"<p><code>api/answers.json</code> serves no entry for {code(e['id'])}; the public API answers the question first.</p>",
                "</section>",
            ]
        parts.append("</div>")
    parts += [
        "<h2>The same answers, as the files serve them</h2>",
        "<p>The first object below is the entry in <code>api/baseline.json</code>; the second is the entry in <code>api/answers.json</code>.",
        "   Each is the same JSON value its file holds. A reader of the page reads them from here.</p>",
        "<h3>The ordinary assistant's entry</h3>",
        '<script type="application/json" id="baseline-answer">',
        script_json(baseline_block),
        "</script>",
        f"<pre>{esc(json_text(baseline_block))}</pre>",
        "<h3>The deployed agent's entry</h3>",
        '<script type="application/json" id="agent-answer">',
        script_json(agent_block),
        "</script>",
        f"<pre>{esc(json_text(agent_block))}</pre>",
        "<footer>",
        "  <p>This demo produces the evidence a validation would need. It is not medical information: the agent assesses",
        "     regulatory impact on labeling and never answers a treatment question (SPEC/00 §2). The authority for what this demo claims is",
        "     <code>SPEC/00-overview.md</code>; what was measured is in <code>milestones/README.md</code>. No number on this page is a",
        "     measured result: the row's and the clause's numbers are their own data, and the run record's and the call record's are",
        "     the CI runs', linked above.</p>",
        "</footer>",
        "</body>",
        "</html>",
    ]
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------- write
def write(args: argparse.Namespace) -> int:
    try:
        observations, result = read_artifact(args.from_dir)
        old = json.loads(args.api.read_text(encoding="utf-8")) if args.api.exists() else {}
        ids = [a["id"] for a in old.get("answers") or [] if isinstance(a, dict) and isinstance(a.get("id"), str)]
        if not ids:
            raise Refused(f"{args.api} serves no answer; there is no id to rebuild")
        entries = build_entries(ids, observations, result, args.goldens)
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    data_commit = git("log", "-1", "--format=%h", "--", "data/")
    api = api_document(old, entries[0]["run"], entries, data_commit)
    agent_api = json.loads(args.agent_api.read_text(encoding="utf-8"))
    args.api.parent.mkdir(parents=True, exist_ok=True)
    # LF on every platform, as .gitattributes stores the files: a rebuild on Windows then equals the committed bytes (M03 Unsure 33).
    args.api.write_text(json_text(api) + "\n", encoding="utf-8", newline="\n")
    args.page.write_text(render_page(api, agent_api), encoding="utf-8", newline="\n")
    for e in entries:
        print(f"{e['id']}: {'answer shown with its row and its clause' if answer_shown(e) else 'no row found; the page shows what the run wrote and its record'}; run {e['run']['run_url']}; started {e['run']['started_at']}")
    print(f"wrote {args.api} and {args.page} from {args.from_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_write = sub.add_parser("write", help="by hand: rebuild the pages from an m04 run's artifact")
    p_write.add_argument("--from", dest="from_dir", required=True, type=Path, help="the directory holding observations.json and result.json")
    p_write.add_argument("--api", type=Path, default=ROOT / "pages" / "api" / "baseline.json")
    p_write.add_argument("--agent-api", type=Path, default=ROOT / "pages" / "api" / "answers.json")
    p_write.add_argument("--page", type=Path, default=ROOT / "pages" / "side-by-side.html")
    p_write.add_argument("--goldens", type=Path, default=ROOT / "goldens")
    args = parser.parse_args()
    return write(args)


if __name__ == "__main__":
    raise SystemExit(main())
