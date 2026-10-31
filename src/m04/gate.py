"""The M04 gate: read what the baseline file serves and the side-by-side page shows, compare with a CI run of the frozen baseline, judge F4.1.

Reads `pages/api/baseline.json`, the ordinary assistant's served answers,
the `<script type="application/json" id="baseline-answer">` and
`id="agent-answer"` blocks of `pages/side-by-side.html`, the side-by-side
page's two columns, and `pages/api/answers.json`, the public API's served
answers, for the agent column. Then, in order:

1. `answers_unrun`: every served answer whose `run` is null, is not an
   object, lacks a field of the run record (`RUN_RECORD`) or holds it
   empty, or whose `written_by_ci` is not true. A read of the served file
   alone; no run of the baseline is needed, so the plant reads RED
   whatever the baseline run's state that day (M03 Unsure 4's rule).
2. `answers_disagreed`: every page baseline answer whose `id` the baseline
   file does not serve, or that is not equal to the file's entry of that
   `id` as parsed JSON (canonical form: sorted keys, no whitespace).
3. `agent_disagreed`: every page agent answer whose `id` the public API
   does not serve, or that is not equal to the API's entry of that `id`,
   canonical form. The M03 gate reads the detail page, not this one
   (M04 Unsure 4).
4. `baseline_changed`: true when `git diff m00 --quiet -- src/baseline/`
   exits non-zero in the checkout, that is when the control differs from
   its state at tag `m00` (P5; M04 Unsure 7). The tag's commit and the
   last commit touching `src/baseline/` are recorded beside it.
5. The run's observations: the file `src.baseline.run --out <file>` wrote
   in this job (`--observations`). The gate does not run the baseline
   itself; the workflow does, with the command `gate.yml` runs, and not
   one argument is added to `src/baseline/` (P5).
6. `answers_differing`: every served answer that carries a run record and
   whose `table_row`, `clause_id` or `answer_fields` is not what the
   run's observation of the same `id` holds, or whose `question` is not
   the golden's (`goldens/<id>.yaml`), or for whose `id` the run holds no
   observation. A served answer that is neither null nor an object, or
   whose `answer_fields` is not an object, cannot be compared: it is
   recorded as not read, so a RED on another served answer still comes
   first (M03 PR 3, Defect 1).

The verdict is ledger row 5's F4.1 and nothing else:

  RED         `answers_unrun`, `answers_disagreed`, `answers_differing` or `agent_disagreed` is
              non-empty, or `baseline_changed` is true.
  GREEN       every served answer carries a run record written by CI, is shown as served and equals
              the run's observation; every agent answer shown is the API's; `src/baseline/` equals
              `m00`; nothing unread.
  UNSCORABLE  nothing is RED and: a served file could not be read or parsed, the baseline file
              serves no answer, a served answer is neither null nor an object, the tag `m00` is not
              in the checkout or git could not answer, or the observations file was not written or
              could not be read (the baseline could not run). Never RED, never GREEN.

RED comes first (M04 PR 2, ruling 6). Nothing that fails after a served
file was read turns a RED into UNSCORABLE: a baseline file that cannot be
read leaves the agent column judged (M04 PR 3, Defect 1); git that cannot
be run leaves the freeze check unread and the served answers judged
(Defect 2); a summary that cannot be appended leaves `result.json` as
written (Defect 3).

No secret, no variable, no network: the gate reads the checkout and the
observations file only.

    uv run python -m src.m04.gate --out-dir <dir> --observations <file> [--summary <md>]

Writes `<dir>/result.json`. Exit 0 GREEN, 1 RED, 2 UNSCORABLE. The result
is evidence only when CI wrote it (P4), and it says whether it did.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
BASELINE_TAG = "m00"
BASELINE_DIR = "src/baseline/"
# The run record's fields on a served answer (M04 README "Carried to PR 2"; fixed here, Unsure 5). The lift writes them.
RUN_RECORD = ("run_url", "artifact", "commit", "baseline_commit", "started_at", "method", "written_by_ci")
ANSWER_FIELDS = ("impacted", "owed", "escalate")
FALSIFIER = (
    "F4.1 an ordinary-assistant answer the side-by-side page shows was not produced by a run of the frozen baseline "
    "(src/baseline/ as at tag m00) made by this repository's CI: it carries no run record, or its table_row, clause_id "
    "or answer_fields differ from what that baseline writes for its question; or the page shows an ordinary-assistant "
    "answer the baseline file does not serve; or the page shows an agent answer that is not the entry the public API serves"
)
BASELINE_BLOCK = "baseline-answer"
AGENT_BLOCK = "agent-answer"


def page_block(block_id: str) -> re.Pattern[str]:
    return re.compile(rf'<script\s+type="application/json"\s+id="{re.escape(block_id)}"\s*>(.*?)</script>', re.DOTALL)


class Unscorable(Exception):
    """The inputs do not let F4.1 be judged. Not a verdict."""


def rel(path: Path) -> str:
    """The path as the repository names it, or as given when it lies outside the repository."""
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


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
        "what": "M04 gate: what the baseline file serves and the side-by-side page shows, read and compared with what a CI run of the frozen baseline writes; the verdict is ledger row 5's F4.1",
        "milestone": "M04",
        "ledger_row": 5,
        "falsifier": FALSIFIER,
        "run_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": commit,
        "dirty": dirty,
        "written_by_ci": ci is not None,
        "ci": ci,
        "baseline_tag": BASELINE_TAG,
        "baseline_dir": BASELINE_DIR,
        "run_record_fields": list(RUN_RECORD),
        "fields_compared": ["question", "table_row", "clause_id", *(f"answer_fields.{f}" for f in ANSWER_FIELDS)],
        "env_note": "no secret, no variable and no network are read; the gate reads the checkout and the observations file only",
    }


# ---------------------------------------------------------------- reading
def read_served(path: Path) -> list[dict]:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Unscorable(f"{rel(path)} could not be read as JSON: {exc}") from exc
    answers = doc.get("answers") if isinstance(doc, dict) else None
    if not isinstance(answers, list) or not all(isinstance(a, dict) and isinstance(a.get("id"), str) for a in answers):
        raise Unscorable(f"{rel(path)} does not hold an `answers` list of objects with an `id`")
    if not answers:
        raise Unscorable(f"{rel(path)} serves no answer; there is nothing to judge")
    ids = [a["id"] for a in answers]
    if len(set(ids)) != len(ids):
        raise Unscorable(f"{rel(path)} serves one id more than once: {ids}")
    return answers


def read_page(path: Path, block_id: str) -> list[dict]:
    """The page's answers in one column: the JSON in its `id="<block_id>"` block, one object or a list of them."""
    try:
        html = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise Unscorable(f"{rel(path)} could not be read: {exc}") from exc
    blocks = page_block(block_id).findall(html)
    if not blocks:
        raise Unscorable(f'{rel(path)} has no <script type="application/json" id="{block_id}"> block')
    shown: list[dict] = []
    for block in blocks:
        try:
            obj = json.loads(block)
        except ValueError as exc:
            raise Unscorable(f"{rel(path)}: the {block_id} block is not JSON: {exc}") from exc
        items = obj if isinstance(obj, list) else [obj]
        if not all(isinstance(i, dict) and isinstance(i.get("id"), str) for i in items):
            raise Unscorable(f"{rel(path)}: the {block_id} block is not an object, or a list of objects, with an `id`")
        shown.extend(items)
    return shown


def read_golden_question(goldens: Path, answer_id: str) -> tuple[str | None, str | None]:
    """The golden's `question`, or None and why. The baseline runs over goldens/, so a served id must be a golden's."""
    path = goldens / f"{answer_id}.yaml"
    try:
        golden = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return None, f"{rel(path)} could not be read: {type(exc).__name__}"
    question = golden.get("question") if isinstance(golden, dict) else None
    if not isinstance(question, str):
        return None, f"{rel(path)} holds no `question` string"
    return question, None


def read_observations(path: Path | None) -> dict:
    """The file `src.baseline.run --out` wrote: `observations`, a list of objects with an `id`, and its provenance."""
    if path is None:
        raise Unscorable("no observations file was given (--observations): the baseline did not run for this gate")
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Unscorable(f"the observations file {rel(path)} could not be read as JSON (the baseline could not run): {exc}") from exc
    observations = doc.get("observations") if isinstance(doc, dict) else None
    if not isinstance(observations, list) or not all(isinstance(o, dict) and isinstance(o.get("id"), str) for o in observations):
        raise Unscorable(f"the observations file {rel(path)} does not hold an `observations` list of objects with an `id`")
    return doc


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def run_record_check(entry: dict) -> dict:
    run = entry.get("run")
    if run is None:
        return {"has_record": False, "why": "run is null"}
    if not isinstance(run, dict):
        return {"has_record": False, "why": f"run is a {type(run).__name__}, not an object"}
    missing = [f for f in RUN_RECORD if f not in run or run[f] in (None, "")]
    if missing:
        return {"has_record": False, "why": f"run lacks {missing}", "missing": missing}
    if run.get("written_by_ci") is not True:
        return {"has_record": False, "why": f"run.written_by_ci is {run.get('written_by_ci')!r}, not true"}
    return {"has_record": True, "why": "a run record written by CI, every field present"}


def served_answer_check(answer: Any) -> str | None:
    """Why a served `answer` cannot be compared, or None. Null and an object are compared; anything else is not read (M03 PR 3, Defect 1)."""
    if answer is None:
        return None
    if not isinstance(answer, dict):
        return f"the served answer is a {type(answer).__name__}, not null or an object, and cannot be compared"
    fields = answer.get("answer_fields")
    if fields is not None and not isinstance(fields, dict):
        return f"the served answer's answer_fields is a {type(fields).__name__}, not an object, and cannot be compared"
    return None


def unrun(served: list[dict]) -> tuple[list[str], dict[str, dict]]:
    checks = {a["id"]: run_record_check(a) for a in served}
    return [i for i, c in checks.items() if not c["has_record"]], checks


def disagreed(served: list[dict], shown: list[dict], source: str) -> tuple[list[str], list[dict]]:
    """Each page answer against the entry of the same id in `served`; `source` names the served file in the record."""
    by_id = {a["id"]: a for a in served}
    entries = []
    for page in shown:
        api = by_id.get(page["id"])
        if api is None:
            entries.append({"id": page["id"], "equal": False, "why": f"{source} serves no answer with this id"})
        elif canonical(api) != canonical(page):
            keys = sorted(k for k in set(api) | set(page) if canonical(api.get(k)) != canonical(page.get(k)))
            entries.append({"id": page["id"], "equal": False, "why": f"differs from {source}'s entry on {keys}", "keys": keys})
        else:
            entries.append({"id": page["id"], "equal": True, "why": f"equal to {source}'s entry as parsed JSON"})
    return [e["id"] for e in entries if not e["equal"]], entries


# ------------------------------------------------------------ the control
def git_error(exc: BaseException) -> str:
    """Why a git command gave no answer: its stderr when it ran and failed, else the OS error (git absent, not executable)."""
    if isinstance(exc, subprocess.CalledProcessError):
        return (exc.stderr or "").strip()[:200]
    return f"git could not be run: {type(exc).__name__}: {exc}"[:200]


def baseline_state() -> tuple[bool | None, dict]:
    """Whether `src/baseline/` differs from tag `m00` in the checkout, and the commits a reader checks it against.

    Never raises: when git cannot be run or the tag is not in the checkout, `changed` is None and `error` says why, so a
    RED read from the served files still comes first (M04 PR 3, Defect 2).
    """
    record: dict[str, Any] = {"tag": BASELINE_TAG, "dir": BASELINE_DIR, "command": f"git diff {BASELINE_TAG} --quiet -- {BASELINE_DIR}"}
    try:
        record["tag_commit"] = git("rev-parse", f"{BASELINE_TAG}^{{commit}}")
    except subprocess.CalledProcessError as exc:
        record.update(changed=None, error=f"the tag {BASELINE_TAG} is not in the checkout: {git_error(exc)}")
        return None, record
    except OSError as exc:
        record.update(changed=None, error=f"the tag {BASELINE_TAG} could not be resolved: {git_error(exc)}")
        return None, record
    try:
        record["baseline_commit"] = git("log", "-1", "--format=%H", "--", BASELINE_DIR) or None
    except (subprocess.CalledProcessError, OSError) as exc:
        record["baseline_commit"] = None
        record["baseline_commit_error"] = git_error(exc)
    try:
        proc = subprocess.run(["git", "diff", BASELINE_TAG, "--quiet", "--", BASELINE_DIR], cwd=ROOT, capture_output=True, text=True, check=False)
    except OSError as exc:
        record.update(changed=None, error=f"the freeze check could not be run: {git_error(exc)}")
        return None, record
    record["diff_exit"] = proc.returncode
    if proc.returncode not in (0, 1):
        record.update(changed=None, error=f"git diff exited {proc.returncode}: {proc.stderr.strip()[:200]}")
        return None, record
    changed = proc.returncode == 1
    record["changed"] = changed
    record["why"] = f"{BASELINE_DIR} differs from its state at tag {BASELINE_TAG}" if changed else f"{BASELINE_DIR} equals its state at tag {BASELINE_TAG}"
    return changed, record


# ----------------------------------------------------------- the run's answer
def observation_answer(observation: Any) -> dict | None:
    """The run's observation as the served `answer` is shaped: `table_row`, `clause_id`, `answer_fields`. None when there is none."""
    if not isinstance(observation, dict):
        return None
    fields = observation.get("answer_fields") if isinstance(observation.get("answer_fields"), dict) else {}
    return {
        "table_row": observation.get("table_row"),
        "clause_id": observation.get("clause_id"),
        "answer_fields": {f: fields.get(f) for f in ANSWER_FIELDS},
    }


def compare(served_answer: Any, served_question: Any, golden_question: str | None, observation: Any) -> dict:
    """The served answer against the run's observation; the served question against the golden's. Raises on no input."""
    run = observation_answer(observation)
    fields: dict[str, dict] = {"question": {"equal": served_question == golden_question, "served": served_question, "golden": golden_question}}
    if served_answer is not None and not isinstance(served_answer, dict):
        return {"equal": False, "why": "the served answer is not null or an object and cannot be compared", "fields": fields, "served": served_answer, "run": run}
    if run is None:
        return {"equal": False, "why": "the run holds no observation of this id", "fields": fields, "served": served_answer, "run": None}
    if served_answer is None:
        return {"equal": False, "why": "the served answer is null and the run wrote an observation", "fields": fields, "served": None, "run": run}
    served_fields = served_answer.get("answer_fields")
    served_fields = served_fields if isinstance(served_fields, dict) else {}
    for name in ("table_row", "clause_id"):
        s, r = served_answer.get(name), run.get(name)
        fields[name] = {"equal": s == r, "served": s, "run": r}
    for f in ANSWER_FIELDS:
        s, r = served_fields.get(f), run["answer_fields"].get(f)
        fields[f"answer_fields.{f}"] = {"equal": s == r, "served": s, "run": r}
    unequal = [k for k, v in fields.items() if not v["equal"]]
    return {"equal": not unequal, "why": "all equal" if not unequal else f"differs on {unequal}", "fields": fields, "unequal": unequal}


# ------------------------------------------------------------------- gate
def judge(served: list[dict], unrun_ids: list[str], disagreed_ids: list[str], differing_ids: list[str], agent_ids: list[str], changed: bool | None, unreadable: list[str]) -> dict:
    if unrun_ids or disagreed_ids or differing_ids or agent_ids or changed is True:
        verdict, parts = "RED", []
        if unrun_ids:
            parts.append(f"served answers {', '.join(unrun_ids)} carry no run record")
        if disagreed_ids:
            parts.append(f"page baseline answers {', '.join(disagreed_ids)} are not what the baseline file serves")
        if differing_ids:
            parts.append(f"served answers {', '.join(differing_ids)} differ from the run's observation")
        if agent_ids:
            parts.append(f"page agent answers {', '.join(agent_ids)} are not what the public API serves")
        if changed is True:
            parts.append(f"{BASELINE_DIR} differs from tag {BASELINE_TAG}")
        reason = "F4.1 holds: " + "; ".join(parts)
    elif unreadable:
        verdict = "UNSCORABLE"
        reason = "nothing is RED and a reading F4.1 needs could not be made: " + "; ".join(unreadable)
    else:
        verdict = "GREEN"
        reason = (
            "F4.1 does not hold: every served answer carries a run record written by CI, is shown as served and equals the run's "
            f"observation, every agent answer shown is the public API's, and {BASELINE_DIR} equals tag {BASELINE_TAG}"
        )
    return {
        "verdict": verdict,
        "reason": reason,
        "answers_unrun": unrun_ids,
        "answers_disagreed": disagreed_ids,
        "answers_differing": differing_ids,
        "agent_disagreed": agent_ids,
        "baseline_changed": changed,
        "unreadable": unreadable,
        "counts": {"served": len(served), "unrun": len(unrun_ids), "disagreed": len(disagreed_ids), "differing": len(differing_ids), "agent_disagreed": len(agent_ids)},
    }


def summary_markdown(result: dict) -> str:
    lines = [f"## M04 gate: {result['verdict']}", "", result["reason"] + ".", ""]
    lines.append(f"Commit `{result.get('commit') or 'unknown'}`" + (" (dirty tree)" if result.get("dirty") else "") + f", written by CI: `{result['written_by_ci']}`.")
    lines.append("")
    if "error" in result:
        lines += [f"`{result['error']['type']}: {result['error']['message']}`", ""]
    if result.get("baseline"):
        b = result["baseline"]
        tag_commit = b.get("tag_commit")
        lines += [f"`{BASELINE_DIR}` against tag `{BASELINE_TAG}` (`{tag_commit[:7] if tag_commit else 'not resolved'}`): changed `{b.get('changed')}`" + (f"; `{b.get('error')}`" if b.get("error") else "") + ".", ""]
    if result.get("observations"):
        o = result["observations"]
        lines += [f"The run's observations: read `{o.get('read')}`, {o.get('count')} observations, commit `{(o.get('commit') or 'unknown')[:7]}`, started `{o.get('started_at')}`" + (f"; `{o.get('error')}`" if o.get("error") else "") + ".", ""]
    if result.get("served"):
        page_read = (result.get("page") or {}).get("read", True)
        lines += ["| served | run record | page equal | compared |", "|---|---|---|---|"]
        for e in result["served"]:
            cmp = e.get("comparison")
            cmp_s = f"not compared: {e.get('not_compared') or 'no run record'}" if cmp is None else ("equal" if cmp["equal"] else cmp["why"])
            page = e.get("page_equal")
            page_s = "page not read" if not page_read else ("not shown" if page is None else ("yes" if page else "no"))
            lines.append(f"| {e['id']} | {'yes' if e['run_record']['has_record'] else 'no: ' + e['run_record']['why']} | {page_s} | {cmp_s} |")
        lines.append("")
    if result.get("agent"):
        a = result["agent"]
        lines += ["| agent shown | API equal |", "|---|---|"] + [f"| {e['id']} | {'yes' if e['equal'] else 'no: ' + e['why']} |" for e in a.get("entries", [])] + [""]
    if result.get("unreadable"):
        lines += ["Not read:", ""] + [f"- {u}" for u in result["unreadable"]] + [""]
    if result["verdict"] == "UNSCORABLE":
        lines.append("UNSCORABLE is not a verdict on ledger row 5's F4.1. It is never RED and never GREEN.")
    else:
        lines.append("The verdict judges ledger row 5's F4.1 only. The run's observation of an unrun answer is recorded and decides nothing.")
    return "\n".join(lines) + "\n"


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_result(args: argparse.Namespace, result: dict) -> None:
    """Write `result.json`, print the summary, append it to `--summary` when one was given.

    The summary is a copy for the job page; `result.json` is the result. A summary that cannot be appended is
    reported on stderr and does not overturn the verdict already written (M04 PR 3, Defect 3).
    """
    write_json(args.out_dir / "result.json", result)
    text = summary_markdown(result)
    print(text)
    if args.summary:
        try:
            args.summary.parent.mkdir(parents=True, exist_ok=True)
            with args.summary.open("a", encoding="utf-8") as fh:
                fh.write(text)
        except OSError as exc:
            print(f"the summary could not be appended to {args.summary}: {exc!r}; result.json stands as written", file=sys.stderr)


def run(args: argparse.Namespace) -> int:
    unreadable: list[str] = []
    # The served files alone, first: RED on an unrun or disagreed answer needs no run of the baseline (M03 Unsure 4's rule).
    # A baseline file that cannot be read is recorded, not raised: the agent column is read from the page and the public
    # API alone, so `agent_disagreed` still reads RED first (M04 PR 3, Defect 1); with nothing RED the run is UNSCORABLE.
    try:
        served: list[dict] | None = read_served(args.api)
    except Unscorable as exc:
        served = None
        unreadable.append(str(exc))
    try:
        shown: list[dict] | None = read_page(args.page, BASELINE_BLOCK)
    except Unscorable as exc:
        shown, unreadable = None, [str(exc)]
    try:
        shown_agent: list[dict] | None = read_page(args.page, AGENT_BLOCK)
    except Unscorable as exc:
        shown_agent = None
        unreadable.append(str(exc))
    try:
        api: list[dict] | None = read_served(args.agent_api)
    except Unscorable as exc:
        api = None
        unreadable.append(f"the public API for the agent column: {exc}")
    unrun_ids, checks = unrun(served) if served is not None else ([], {})
    disagreed_ids, page_entries = disagreed(served, shown, rel(args.api)) if served is not None and shown is not None else ([], [])
    page_equal = {e["id"]: e["equal"] for e in page_entries}
    agent_ids, agent_entries = disagreed(api, shown_agent, rel(args.agent_api)) if api is not None and shown_agent is not None else ([], [])

    # The control: src/baseline/ against tag m00 (P5, Unsure 7).
    changed, baseline = baseline_state()
    if changed is None:
        unreadable.append(f"the freeze check could not be made: {baseline.get('error')}")

    # The run: the observations file the workflow's baseline step wrote. Read after the served files.
    observations_record: dict[str, Any] = {"path": rel(args.observations) if args.observations else None, "read": False}
    by_id: dict[str, dict] = {}
    try:
        doc = read_observations(args.observations)
    except Unscorable as exc:
        observations_record.update(error=str(exc), count=0)
        unreadable.append(str(exc))
    else:
        by_id = {o["id"]: o for o in doc["observations"]}
        observations_record.update(
            read=True, count=len(by_id), ids=sorted(by_id), started_at=doc.get("started_at"), commit=doc.get("commit"),
            dirty=doc.get("dirty"), method=doc.get("method"), model=doc.get("model"), what=doc.get("what"),
        )  # fmt: skip

    entries, differing_ids = [], []
    for a in served or []:
        entry: dict[str, Any] = {"id": a["id"], "run_record": checks[a["id"]], "page_equal": page_equal.get(a["id"]), "served_answer": a.get("answer")}
        shape = served_answer_check(a.get("answer"))
        entry["answer_shape"] = shape or "null or an object; can be compared"
        if shape:
            unreadable.append(f"{a['id']}: {shape}")
        golden_question, golden_why = read_golden_question(args.goldens, a["id"])
        entry["golden"] = {"path": rel(args.goldens / f"{a['id']}.yaml"), "read": golden_question is not None, "why": golden_why}
        entry["observation"] = by_id.get(a["id"])
        if not checks[a["id"]]["has_record"]:
            entry["comparison"], entry["not_compared"] = None, "no run record"
        elif shape:
            entry["comparison"], entry["not_compared"] = None, shape
        elif not observations_record["read"]:
            entry["comparison"], entry["not_compared"] = None, "the observations file was not read"
            unreadable.append(f"{a['id']}: a run answer that was not compared: the observations file was not read")
        else:
            entry["comparison"] = compare(a.get("answer"), a.get("question"), golden_question, by_id.get(a["id"]))
            if not entry["comparison"]["equal"]:
                differing_ids.append(a["id"])
        entries.append(entry)

    result = {
        **provenance(),
        **judge(served or [], unrun_ids, disagreed_ids, differing_ids, agent_ids, changed, unreadable),
        "baseline": baseline,
        "observations": observations_record,
        "served_read": served is not None,
        "served": entries,
        "page": {
            "read": shown is not None,
            "answers_shown": [p["id"] for p in shown] if shown else [],
            "entries": page_entries,
            "agent_read": shown_agent is not None,
            "agent_shown": [p["id"] for p in shown_agent] if shown_agent else [],
        },
        "agent": {"api": rel(args.agent_api), "read": api is not None, "entries": agent_entries},
    }
    write_result(args, result)
    return {"GREEN": 0, "RED": 1}.get(result["verdict"], 2)


def unscorable(args: argparse.Namespace, exc: BaseException) -> int:
    refused = isinstance(exc, Unscorable)
    result = {
        **provenance(),
        "verdict": "UNSCORABLE",
        "reason": "F4.1 is not judged: " + ("the gate refused the inputs" if refused else "the gate raised"),
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
    parser.add_argument("--out-dir", required=True, type=Path, help="where result.json is written")
    parser.add_argument("--observations", type=Path, help="the file src.baseline.run --out wrote in this job; absent, the baseline did not run")
    parser.add_argument("--summary", type=lambda s: Path(s) if s else None, help="append a Markdown summary here (GITHUB_STEP_SUMMARY in CI); empty means none")
    parser.add_argument("--api", type=Path, default=ROOT / "pages" / "api" / "baseline.json", help="the ordinary assistant's served answers")
    parser.add_argument("--agent-api", type=Path, default=ROOT / "pages" / "api" / "answers.json", help="the public API's served answers, for the agent column")
    parser.add_argument("--page", type=Path, default=ROOT / "pages" / "side-by-side.html")
    parser.add_argument("--goldens", type=Path, default=ROOT / "goldens")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    try:
        return run(args)
    except Exception as exc:  # noqa: BLE001  every failure to judge is UNSCORABLE, written and exit 2; never the RED code
        return unscorable(args, exc)


if __name__ == "__main__":
    raise SystemExit(main())
