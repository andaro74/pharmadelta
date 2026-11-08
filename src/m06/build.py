"""The M06 build: the evidence package, built by this repository's CI from CI artifacts, this repository and label-impact's manifest, and written as an artifact.

    uv run python -m src.m06.build --out-dir <dir> [--summary <md>]

Runs in CI (`.github/workflows/m06-lift.yml`). It commits nothing: the zip
is downloaded from the run's artifact by hand, committed byte for byte
under `pages/evidence/`, and named in `pages/api/sign-off.json` by the
seat holder's own commit, which the M06 gate (`src/m06/gate.py`) reads
back. Only what this workflow writes is a record (SPEC/00 P4); a local
build writes `written_by_ci` false and is not committed.

What goes in (milestones/M06/README.md, "Unsure 16, ruled before the
lift"), each entry at its `path` in the zip, every entry with every field
of the gate's `ENTRY_RECORD`, null where its source does not use it:

- `artifact`: the `result.json` of the CI run each "Measured" cell of
  `milestones/README.md` cites for rows 0, 1, 2, 4, 5 and 6, with the M00
  run's `observations.json` (the baseline's report on scenarios 5 and 6,
  M05 Unsure 12). Each is downloaded in this run through GitHub's API as
  the gate downloads it (the gate's own `Artifacts`: the listing, then the
  archive, whose 302 to the blob store is fetched without the token and
  whose URL is written nowhere), by the run URL, the artifact's name and
  the file's name the entry records. The row is `ledger_row`.
- `repository`: `milestones/README.md`, `SPEC/00-overview.md`, every file
  under `goldens/` and the four served files under `pages/api/`, read from
  the checkout at the build's commit with `git show <sha>:<path>`; the
  entry's `commit` is that sha, 40 hex digits, the same as
  `package.commit` (Unsure 29). The served files are as at that commit,
  which precedes the signing commit: a signature cannot be inside the
  package it signs over.
- `agent`: `label-impact`'s `manifest.yaml` at each agent commit the
  served files name (`answers.json`'s and `break-it.json`'s `agent.commit`,
  `sign-off.json`'s `reviewer.seat_read_from.commit`), read through the
  contents API as the gate reads it, the short sha the file names resolved
  to the full one through `GET /repos/<agent>/commits/<sha>`.

Plus `manifest.json`, the list of entries, which the gate compares with
`package.entries`. The zip is deterministic: entries sorted by path, one
fixed timestamp, one compression; a reader with the same sources writes
the same bytes. Writes `<dir>/<basename>` (the zip, named by the basename
it is committed under, so the gate finds it in the artifact by
`Path(package.file).name`, Unsure 26) and `<dir>/build.json`: provenance,
the package's SHA-256 and size, the entries, every artifact listing and
download made with its expiry, the agent commits resolved, and `ok` with
`why`. When any source could not be read, or a member would hold a
token's prefix or the door's host or pool prefix, `ok` is false, the zip
is not written, and `build.json` says why: an incomplete package is no
package. Exit 0 when the zip was written, 2 otherwise. The token is read
from the environment and written nowhere.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.m06.gate import (
    AGENT_MANIFEST,
    AGENT_REPO,
    ENTRY_RECORD,
    ENV,
    REPO,
    Artifacts,
    api_json,
    ci_context,
    git,
    git_bytes,
    read_agent_file,
    sha256_hex,
    write_json,
)

PACKAGE_FILE = "pages/evidence/m06-evidence.zip"
ARTIFACT_PREFIX = "m06-package-"
PACKAGE_MANIFEST = "manifest.json"
# The CI runs the ledger's "Measured" cells cite (milestones/README.md), the artifact each wrote, the file taken, the row.
# Row 1's cell cites two runs, the PR run whose artifact it names and the `main` run that read the same; both are taken.
ARTIFACT_SOURCES: tuple[tuple[int, str, str, str], ...] = (
    (0, "https://github.com/andaro74/pharmadelta/actions/runs/38058191295", "m00-gate-47788c0a0b84854145e82e5fc70c9b22a87ab4ed", "result.json"),
    (0, "https://github.com/andaro74/pharmadelta/actions/runs/38058191295", "m00-gate-47788c0a0b84854145e82e5fc70c9b22a87ab4ed", "observations.json"),
    (1, "https://github.com/andaro74/pharmadelta/actions/runs/38077129178", "m01-gate-223de2d13d518ce23327373cfff9775a49c24e0f", "result.json"),
    (1, "https://github.com/andaro74/pharmadelta/actions/runs/38097865560", "m01-gate-8cdd851e8f4c02da3eb61307c2452010bc10ba84", "result.json"),
    (2, "https://github.com/andaro74/pharmadelta/actions/runs/38154731153", "m02-gate-e8c3690d3877f8603620f3cb56c9104e530ec824", "result.json"),
    (4, "https://github.com/andaro74/pharmadelta/actions/runs/41171470951", "m03-gate-0b8d2ec7598b61c30f861a3f2114c2a13e89ad71", "result.json"),
    (5, "https://github.com/andaro74/pharmadelta/actions/runs/41234548875", "m04-gate-4d926760c985e973bdd5d35f1c76f0db47660808", "result.json"),
    (6, "https://github.com/andaro74/pharmadelta/actions/runs/41266122812", "m05-gate-8734adbd4d77c84bc98c0d423bb04bb1dbc2d4bd", "result.json"),
)
REPOSITORY_FILES = ("milestones/README.md", "SPEC/00-overview.md")
REPOSITORY_DIRS = ("goldens",)
SERVED_FILES = ("pages/api/answers.json", "pages/api/baseline.json", "pages/api/break-it.json", "pages/api/sign-off.json")
# Where each served file names the agent's commit: the key under each entry of its list.
AGENT_COMMIT_KEYS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("pages/api/answers.json", "answers", ("agent", "commit")),
    ("pages/api/break-it.json", "scenarios", ("agent", "commit")),
    ("pages/api/sign-off.json", "signoffs", ("reviewer", "seat_read_from", "commit")),
)
# What no member may hold: a token's prefix (M06 Unsure 8, 21) or the door's host or pool prefix (M03 Unsure 12).
FORBIDDEN = re.compile(rb"ghs_[A-Za-z0-9]|ghp_[A-Za-z0-9]|github_pat_|execute-api|us-west-2_")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def provenance() -> dict[str, Any]:
    ci = ci_context()
    try:
        commit: str | None = git("rev-parse", "HEAD")
        dirty: bool | None = bool(git("status", "--porcelain"))
    except Exception:  # noqa: BLE001  the commit is still recorded from CI's environment when git cannot answer
        commit, dirty = (ci or {}).get("sha"), None
    return {
        "what": "M06 build: the evidence package pages/api/sign-off.json names, built from the CI artifacts the ledger's Measured cells cite, "
        "this repository at the build's commit and label-impact's manifest at the agent commits the served files name; written as an "
        "artifact, committed by hand, signed by the seat holder's own commit, read back by the M06 gate (milestones/M06/README.md, Close)",
        "milestone": "M06",
        "ledger_row": 7,
        "run_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": commit,
        "dirty": dirty,
        "written_by_ci": ci is not None,
        "ci": ci,
        "repository": REPO,
        "agent_repository": AGENT_REPO,
        "package_file": PACKAGE_FILE,
        "artifact": f"{ARTIFACT_PREFIX}{(ci or {}).get('sha') or commit}",
        "entry_record_fields": list(ENTRY_RECORD),
        "env_set": {name: bool(os.environ.get(var)) for name, var in ENV.items()},
        "env_note": "whether the environment held the workflow's token; its value is never written",
    }


def entry(path: str, data: bytes, source: str, *, run_url: str | None = None, artifact: str | None = None, name: str | None = None, commit: str | None = None, ledger_row: int | None = None) -> dict:
    """One entry record, every field of ENTRY_RECORD present, null where the source does not use it."""
    rec = {"path": path, "sha256": sha256_hex(data), "source": source, "run_url": run_url, "artifact": artifact, "name": name, "commit": commit, "ledger_row": ledger_row}
    assert tuple(rec) == ENTRY_RECORD
    return rec


def list_tree(commit: str, directory: str) -> list[str]:
    out = git("ls-tree", "-r", "--name-only", commit, f"{directory}/")
    return [line for line in out.splitlines() if line]


def agent_commits_named(commit: str, token: str | None, out: dict) -> tuple[dict[str, str], list[str]]:
    """The agent commits the served files name at `commit`, each resolved to its full sha; and what could not be resolved."""
    named: dict[str, list[str]] = {}
    for path, key, chain in AGENT_COMMIT_KEYS:
        try:
            doc = json.loads(git_bytes("show", f"{commit}:{path}").decode("utf-8"))
        except Exception as exc:  # noqa: BLE001  not at that commit, not JSON
            out.setdefault("agent_commit_reads", []).append({"file": path, "read": False, "why": type(exc).__name__})
            continue
        for item in (doc.get(key) or []) if isinstance(doc, dict) else []:
            value: Any = item
            for k in chain:
                value = value.get(k) if isinstance(value, dict) else None
            if isinstance(value, str) and re.fullmatch(r"[0-9a-f]{7,40}", value):
                named.setdefault(value, []).append(path)
        out.setdefault("agent_commit_reads", []).append({"file": path, "read": True, "key": f"{key}[].{'.'.join(chain)}"})
    resolved: dict[str, str] = {}
    failures: list[str] = []
    records = []
    for short, files in sorted(named.items()):
        got = api_json(f"/repos/{AGENT_REPO}/commits/{short}", token)
        full = (got["json"] or {}).get("sha") if got["read"] and isinstance(got["json"], dict) else None
        if isinstance(full, str) and SHA40.match(full) and full.startswith(short):
            resolved[short] = full
            records.append({"named": short, "named_by": sorted(set(files)), "sha": full, "status": got["status"]})
        else:
            failures.append(f"the agent commit {short!r} ({', '.join(sorted(set(files)))}) could not be resolved: {got.get('why') or 'no sha'}")
            records.append({"named": short, "named_by": sorted(set(files)), "sha": None, "status": got["status"], "why": got.get("why")})
    out["agent_commits"] = records
    return resolved, failures


def collect(commit: str, token: str | None, out: dict) -> tuple[dict[str, bytes], list[dict], list[str]]:
    """Every member's bytes and record, and why any source could not be read."""
    members: dict[str, bytes] = {}
    entries: list[dict] = []
    failures: list[str] = []
    artifacts = Artifacts(REPO, token)

    for row, run_url, artifact, member in ARTIFACT_SOURCES:
        path = f"artifacts/{artifact}/{member}"
        got = artifacts.file(run_url, artifact, member)
        if not got["read"]:
            failures.append(f"{path}: {got['why']}")
            continue
        if not got["found"]:
            failures.append(f"{path}: {got['why']}")
            continue
        members[path] = got["bytes"]
        entries.append(entry(path, got["bytes"], "artifact", run_url=run_url, artifact=artifact, name=member, ledger_row=row))
    out["artifacts_read"] = artifacts.reads

    repo_paths = list(REPOSITORY_FILES) + list(SERVED_FILES)
    for d in REPOSITORY_DIRS:
        try:
            repo_paths += list_tree(commit, d)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"repository/{d}/: git ls-tree failed: {type(exc).__name__}")
    for name in repo_paths:
        path = f"repository/{name}"
        try:
            data = git_bytes("show", f"{commit}:{name}")
        except subprocess.CalledProcessError as exc:
            err = (exc.stderr or b"").decode("utf-8", "replace").strip()
            failures.append(f"{path}: git show {commit[:7]}:{name} failed: {err[:160] or 'no message'}")
            continue
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{path}: git could not answer: {type(exc).__name__}")
            continue
        members[path] = data
        entries.append(entry(path, data, "repository", name=name, commit=commit))

    resolved, unresolved = agent_commits_named(commit, token, out)
    failures += unresolved
    if not resolved and not unresolved:
        failures.append("no served file names an agent commit; the package must carry label-impact's manifest")
    for short, full in sorted(resolved.items()):
        path = f"agent/label-impact/{full}/{AGENT_MANIFEST}"
        got = read_agent_file(AGENT_REPO, full, AGENT_MANIFEST, token)
        if not got["read"]:
            failures.append(f"{path}: {got['why']}")
            continue
        members[path] = got["bytes"]
        entries.append(entry(path, got["bytes"], "agent", name=AGENT_MANIFEST, commit=full))

    for path, data in sorted(members.items()):
        if FORBIDDEN.search(data):
            failures.append(f"{path} holds a token's prefix or the door's host or pool prefix; not packaged")
    entries.sort(key=lambda e: e["path"])
    return members, entries, failures


def write_zip(members: dict[str, bytes], entries: list[dict]) -> bytes:
    """The package: manifest.json and each member at its path, sorted, one timestamp, deflated; the same sources give the same bytes."""
    manifest = (json.dumps(entries, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    all_members = {**members, PACKAGE_MANIFEST: manifest}
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for path in sorted(all_members):
            info = zipfile.ZipInfo(path, date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            info.create_system = 3
            zf.writestr(info, all_members[path], compresslevel=9)
    return buf.getvalue()


def summary_markdown(out: dict) -> str:
    lines = [f"## M06 build: {'package written' if out.get('ok') else 'no package'}", "", f"{out.get('why')}.", ""]
    lines.append(f"Commit `{out.get('commit') or 'unknown'}`" + (" (dirty tree)" if out.get("dirty") else "") + f", written by CI: `{out['written_by_ci']}`.")
    lines.append("")
    pkg = out.get("package") or {}
    if pkg:
        lines += [f"`{pkg.get('file')}`: {pkg.get('bytes')} bytes, SHA-256 `{pkg.get('sha256')}`, {len(out.get('entries') or [])} entries.", ""]
    if out.get("entries"):
        lines += ["| path | source | row | sha256 |", "|---|---|---|---|"]
        for e in out["entries"]:
            where = e["run_url"] if e["source"] == "artifact" else (e["commit"] or "")[:7]
            lines.append(f"| `{e['path']}` | {e['source']} ({where}) | {'' if e['ledger_row'] is None else e['ledger_row']} | `{e['sha256'][:12]}…` |")
        lines.append("")
    if out.get("failures"):
        lines += ["Not read:", ""] + [f"- {f}" for f in out["failures"]] + [""]
    lines.append("The package is a record only when CI wrote it (P4). It is committed by hand and signed by the seat holder's own commit; the M06 gate reads it back.")
    return "\n".join(lines) + "\n"


def finish(args: argparse.Namespace, out: dict) -> int:
    write_json(args.out_dir / "build.json", out)
    text = summary_markdown(out)
    print(text)
    if args.summary:
        try:
            args.summary.parent.mkdir(parents=True, exist_ok=True)
            with args.summary.open("a", encoding="utf-8") as fh:
                fh.write(text)
        except OSError as exc:  # the record is written; a summary that cannot be appended changes nothing
            print(f"the summary could not be appended: {exc!r}", file=sys.stderr)
    return 0 if out.get("ok") else 2


def build(args: argparse.Namespace) -> int:
    out = provenance()
    token = os.environ.get(ENV["token"]) or None
    commit = out.get("commit")
    ci_sha = (out.get("ci") or {}).get("sha")
    if not isinstance(commit, str) or not SHA40.match(commit):
        out.update(ok=False, why=f"the checkout's commit could not be read ({commit!r})", entries=[], failures=[])
        return finish(args, out)
    if ci_sha and ci_sha != commit:
        out.update(ok=False, why=f"the checkout is at {commit[:7]}, not the run's {ci_sha[:7]}; the package must describe the commit the run was made for", entries=[], failures=[])
        return finish(args, out)
    if out.get("dirty"):
        out.update(ok=False, why="the working tree is dirty; the package describes a commit, not a tree", entries=[], failures=[])
        return finish(args, out)

    members, entries, failures = collect(commit, token, out)
    out["entries"] = entries
    out["failures"] = failures
    if failures:
        out.update(ok=False, why=f"{len(failures)} source(s) could not be read or packaged; no zip written")
        return finish(args, out)

    data = write_zip(members, entries)
    basename = Path(PACKAGE_FILE).name
    (args.out_dir / basename).write_bytes(data)
    out["package"] = {
        "file": PACKAGE_FILE,
        "basename": basename,
        "sha256": sha256_hex(data),
        "bytes": len(data),
        "members": sorted(members) + [PACKAGE_MANIFEST],
        "commit": commit,
        "built_by": {"run_url": (out.get("ci") or {}).get("run_url"), "artifact": out["artifact"]},
        "written_by_ci": out["written_by_ci"],
    }
    out.update(ok=True, why=f"every source was read; {len(entries)} entries and {PACKAGE_MANIFEST} written to {basename}")
    return finish(args, out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out-dir", required=True, type=Path, help="where the zip and build.json are written")
    parser.add_argument("--summary", type=Path, help="append a Markdown summary here (GITHUB_STEP_SUMMARY in CI)")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    try:
        return build(args)
    except Exception as exc:  # noqa: BLE001  a build that raised leaves a record that says so and no zip; the type alone, since a message can quote a URL
        return finish(args, {**provenance(), "ok": False, "why": f"the build raised: {type(exc).__name__}", "entries": [], "failures": []})


if __name__ == "__main__":
    raise SystemExit(main())
