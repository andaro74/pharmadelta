"""The M00 gate: compare each baseline observation with its golden and judge F0.1.

Reads the observations `src.baseline.run` wrote, the goldens and the data.
For every golden it records one match:

- `ordinary` and `trap`: the observation's `table_row` and `clause_id`
  equal the golden's, both exist in `data/`, and `answer_fields` is equal
  as a whole (same keys, same values).
- `guardrail` and `redteam`: the observation is the string `BLOCKED`.
  The baseline never produces it, so these are recorded as not matched
  (SPEC/00 §7).

The verdict is ledger row 0's falsifier F0.1 and nothing else: RED when
any `trap` is matched, naming each matched trap; otherwise GREEN. An
`ordinary` that is not matched is recorded, not judged. The result is
written as JSON; it is evidence only when CI wrote it (P4), and the
result says whether it did.

    uv run python -m src.gate.score --observations <obs.json> --out <result.json> [--summary <md>]

Exit status: 0 GREEN, 1 RED, 2 the inputs could not be scored.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
ANSWER_KINDS = ("ordinary", "trap")
BLOCK_KINDS = ("guardrail", "redteam")
BLOCKED = "BLOCKED"


class Unscorable(Exception):
    """The inputs do not let every golden be scored. Not a verdict."""


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def ci_context() -> dict[str, Any] | None:
    """Where this result was written, if GitHub Actions wrote it. None for a local run."""
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


def score_answer(expected: dict[str, Any], observed: Any, table_rows: set[str], clause_ids: set[str]) -> dict[str, Any]:
    """One `ordinary` or `trap` golden against one observation (SPEC/00 §6, fields.md)."""
    if not isinstance(observed, dict):
        return {"matched": False, "why": f"observation is not an answer object: {observed!r}"}
    exp_fields = expected.get("answer_fields") or {}
    obs_fields = observed.get("answer_fields")
    fields = {
        "table_row": observed.get("table_row") == expected.get("table_row"),
        "clause_id": observed.get("clause_id") == expected.get("clause_id"),
        "table_row_in_data": observed.get("table_row") in table_rows,
        "clause_id_in_data": observed.get("clause_id") in clause_ids,
        "answer_fields": isinstance(obs_fields, dict) and obs_fields == exp_fields,
    }
    per_field = {
        name: isinstance(obs_fields, dict) and name in obs_fields and obs_fields[name] == value
        for name, value in exp_fields.items()
    }
    missing = [] if not isinstance(obs_fields, dict) else sorted(set(obs_fields) - set(exp_fields))
    unmatched = [name for name, ok in fields.items() if not ok]
    unmatched += [f"answer_fields.{name}" for name, ok in per_field.items() if not ok]
    if missing:
        unmatched.append(f"answer_fields has keys not in the golden: {missing}")
    return {
        "matched": all(fields.values()),
        "fields": fields,
        "answer_fields": per_field,
        "why": "all equal" if all(fields.values()) else "not equal: " + "; ".join(unmatched),
    }


def score_block(observed: Any) -> dict[str, Any]:
    """One `guardrail` or `redteam` golden: the pass is the string BLOCKED, nothing else."""
    matched = observed == BLOCKED
    return {"matched": matched, "why": "blocked" if matched else "answered, not blocked; nothing here can block before P (SPEC/00 section 7)"}


def score(goldens: list[dict[str, Any]], observations: list[dict[str, Any]], table: list[dict[str, Any]], clauses: dict[str, Any]) -> dict[str, Any]:
    by_id: dict[str, dict[str, Any]] = {}
    for obs in observations:
        if obs["id"] in by_id:
            raise Unscorable(f"two observations for {obs['id']}")
        by_id[obs["id"]] = obs
    table_rows = {row["table_row"] for row in table}
    clause_ids = set(clauses)

    entries = []
    for golden in goldens:
        gid, kind, expected = golden["id"], golden["kind"], golden["expected"]
        if gid not in by_id:
            raise Unscorable(f"no observation for {gid}")
        obs = by_id.pop(gid)
        if obs.get("kind") != kind:
            raise Unscorable(f"{gid}: observation kind {obs.get('kind')!r} is not the golden's {kind!r}")
        observed: Any = obs.get("observed", BLOCKED) if obs.get("observed") == BLOCKED else {
            k: obs[k] for k in ("table_row", "clause_id", "answer_fields") if k in obs
        }
        if kind in ANSWER_KINDS:
            if not isinstance(expected, dict):
                raise Unscorable(f"{gid}: a {kind} golden's expected must be an answer object")
            result = score_answer(expected, observed, table_rows, clause_ids)
        elif kind in BLOCK_KINDS:
            if expected != BLOCKED:
                raise Unscorable(f"{gid}: a {kind} golden's expected must be {BLOCKED}")
            result = score_block(observed)
        else:
            raise Unscorable(f"{gid}: unknown kind {kind!r}")
        entries.append({"id": gid, "kind": kind, "expected": expected, "observed": observed, **result})
    if by_id:
        raise Unscorable(f"observations with no golden: {sorted(by_id)}")

    traps_matched = [e["id"] for e in entries if e["kind"] == "trap" and e["matched"]]
    counts = {
        kind: {"goldens": sum(e["kind"] == kind for e in entries), "matched": sum(e["kind"] == kind and e["matched"] for e in entries)}
        for kind in ANSWER_KINDS + BLOCK_KINDS
    }
    verdict = "RED" if traps_matched else "GREEN"
    reason = (
        f"F0.1 holds: the baseline's answer equals the golden's expected on trap {', '.join(traps_matched)}"
        if traps_matched
        else "F0.1 does not hold: no trap golden's expected equals the baseline's answer"
    )
    return {"verdict": verdict, "reason": reason, "traps_matched": traps_matched, "counts": counts, "goldens": entries}


def summary_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"## M00 gate: {result['verdict']}",
        "",
        result["reason"] + ".",
        "",
        f"Commit `{result['commit']}`" + (" (dirty tree)" if result["dirty"] else "") + f", written by CI: `{result['written_by_ci']}`.",
        "",
        "| golden | kind | matched | why |",
        "|---|---|---|---|",
    ]
    for e in result["goldens"]:
        lines.append(f"| {e['id']} | {e['kind']} | {'yes' if e['matched'] else 'no'} | {e['why']} |")
    lines.append("")
    lines.append("The verdict judges ledger row 0's F0.1 only: RED when a `trap` is matched. Other rows are recorded, not judged.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--observations", required=True, type=Path, help="the file src.baseline.run wrote")
    parser.add_argument("--out", required=True, type=Path, help="where to write the result JSON")
    parser.add_argument("--summary", type=Path, help="append a Markdown summary here (GITHUB_STEP_SUMMARY in CI)")
    parser.add_argument("--goldens", type=Path, default=ROOT / "goldens")
    parser.add_argument("--data", type=Path, default=ROOT / "data")
    args = parser.parse_args()

    run = json.loads(args.observations.read_text(encoding="utf-8"))
    goldens = [yaml.safe_load(p.read_text(encoding="utf-8")) for p in sorted(args.goldens.glob("g-*.yaml"))]
    table = json.loads((args.data / "table.json").read_text(encoding="utf-8"))
    clauses = json.loads((args.data / "clauses.json").read_text(encoding="utf-8"))

    try:
        scored = score(goldens, run["observations"], table, clauses)
    except Unscorable as exc:
        print(f"UNSCORABLE: {exc}", file=sys.stderr)
        return 2

    commit = git("rev-parse", "HEAD")
    ci = ci_context()
    result = {
        "what": "M00 gate: each baseline observation compared with its golden; the verdict is ledger row 0's F0.1",
        "milestone": "M00",
        "ledger_row": 0,
        "falsifier": "F0.1 the baseline's answer to a trap golden equals that golden's expected: same table_row, same clause_id, every answer field equal",
        "scored_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": commit,
        "dirty": bool(git("status", "--porcelain")),
        "observations_commit": run.get("commit"),
        "observations_method": run.get("method"),
        "written_by_ci": ci is not None,
        "ci": ci,
        **scored,
    }
    if run.get("commit") != commit:
        result["warning"] = "the observations were written at a different commit than this result"

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    text = summary_markdown(result)
    print(text)
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        with args.summary.open("a", encoding="utf-8") as fh:
            fh.write(text)
    return 1 if result["verdict"] == "RED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
