"""Run the baseline over the goldens and write raw observations (SPEC/00 P5).

A runner. It reads each golden's id, kind and question, never its
`expected`. It scores nothing and decides nothing; the gate that reads
these observations is M00 PR 2's, and only a CI-written result is evidence
(P4).

    uv run python -m src.baseline.run --out <file.json>
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import yaml

from src.baseline import answer as baseline

ROOT = Path(__file__).resolve().parents[2]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--goldens", type=Path, default=ROOT / "goldens")
    parser.add_argument("--data", type=Path, default=ROOT / "data")
    args = parser.parse_args()

    table = json.loads((args.data / "table.json").read_text(encoding="utf-8"))
    clauses = json.loads((args.data / "clauses.json").read_text(encoding="utf-8"))
    observations = []
    for path in sorted(args.goldens.glob("g-*.yaml")):
        golden = yaml.safe_load(path.read_text(encoding="utf-8"))
        entry = {"id": golden["id"], "kind": golden["kind"]}
        entry.update(baseline.answer(golden["question"], table, clauses))
        observations.append(entry)
        print(f"{entry['id']} {entry['kind']:<9} {entry['table_row']:<24} {entry['clause_id']:<22} {entry['answer_fields']}")

    result = {
        "what": "raw observations from the naive baseline; scores nothing; not evidence unless CI wrote it",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": git("rev-parse", "HEAD"),
        "dirty": bool(git("status", "--porcelain")),
        "method": "keyword matching; see src/baseline/answer.py",
        "model": None,
        "observations": observations,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
