"""The M07 gate: read the time served for the second agent and the pages, read the clock back from GitHub's records, judge F7.1.

Reads `pages/api/second-agent.json`, the times pharmadelta serves for its
second agent, and the `<script type="application/json" id="second-agent-<id>">`
blocks of `index.html` and every `pages/*.html`, the times a page shows.
Then, in order:

1. `times_unrecorded`: every served entry that serves a time
   (`elapsed_seconds` is not null) whose `clock` is null, is not an object,
   lacks a field of the clock record (`CLOCK_RECORD`, `READ_BY`) or holds it
   empty or in the wrong form: a repository that is not `owner/name`, an id
   that is not a positive integer, a time that is not an instant with an
   offset, a merge commit that is not 40 hex digits, a `read_by.run_url`
   that is not a run of this repository on github.com. A read of the served
   file alone; no network is needed, so the plant reads RED whatever
   GitHub's API says that day (M03 Unsure 4's rule).
2. `times_disagreed`: every page block whose `id` the served file does not
   serve, whose block is not named for its `id`, or that is not equal to
   the file's entry of that `id` as parsed JSON (canonical form: sorted
   keys, no whitespace). A page with no block shows no time and disagrees
   with nothing.
3. The read-back, for each served time that carries a clock record, and
   for no other, from GitHub's API:
   a. `GET /repos/<clock.repository>`: `full_name`, `id`, `created_at`,
      `template_repository.full_name`. 404 is an answer: the repository
      does not exist as this CI can read it.
   b. `GET /repos/<clock.repository>/pulls?state=all&sort=created&direction=asc&per_page=1`:
      the first pull request's `number`, `merged_at`, `merge_commit_sha`.
   c. `GET /repos/andaro74/agentkeel/actions/jobs/<clock.deploy_job>`:
      `run_id`, `name`, `conclusion`, `completed_at`, `run_attempt`. A job
      id is one attempt's; a re-run makes a new job with a new id, so the
      record names one attempt and its `completed_at` (Unsure 10).
   d. `GET /repos/andaro74/agentkeel/actions/runs/<clock.deploy_run>`:
      `path`, which must be agentkeel's `deploy.yml`.
4. `times_differing`: every such time where the entry's `repository` is
   not the record's; the repository does not exist, is not the one the
   record names by name and id, or was not created from
   `agentkeel-studio/agent-template`; the record's `created_at` is not the
   repository's; the first pull request is not the one the record names,
   is not merged, or its merge commit is not the record's; the job is not
   a `deploy-agent` job of the run the record names, its name does not
   carry the repository, its id and the merge commit, its conclusion is
   not `success`, or its `completed_at` is not the record's; the run is not
   a run of `deploy.yml`; or `elapsed_seconds` is not a whole number equal
   to the stop less the start, in the record and as GitHub answers. A read
   that could not be made (the API refusing, a body that is not JSON) is
   recorded under `unreadable` and decides nothing.

The job's name. agentkeel's `deploy-agent` is a matrix job with no name of
its own, so GitHub names each leg from the matrix row,
`deploy-agent (<repository>, <repository_id>, <commit>, <name>, <rollout>)`,
and cuts the name at 97 characters with `...` (read on label-impact's
deploy of 2026-11-11: the name ends inside the fourth value). For a longer
repository name the cut falls inside the commit. The gate reads the three
leading values by position: the repository and its id whole, and the
commit whole when the name holds 40 hex digits, else as a prefix of the
record's merge commit of at least `MIN_COMMIT_PREFIX` digits, and records
which (Unsure 20).

The verdict is ledger row 8's F7.1 and nothing else:

  RED         `times_unrecorded`, `times_disagreed` or `times_differing` is non-empty.
  GREEN       every served time carries a clock record that equals GitHub's records, the job
              concluded `success`, every page block is the file's entry; nothing unread.
  UNSCORABLE  nothing is RED and: the served file could not be read or parsed, it serves no
              entry, a page could not be read, or a read-back F7.1 needs could not be made.
              Never RED, never GREEN.

RED comes first. Nothing that fails after the served file was read turns a
RED into UNSCORABLE (M05 PR 3's rule, built in): every network and file
read is guarded, recorded by its status or its exception's type, and never
raised; a page that cannot be read is recorded under `unreadable` and the
lists stand; a read-back that raises keeps the differences found before it.

Hosts: GitHub's API (`GITHUB_API_URL`, else `https://api.github.com`) with
the workflow's `GITHUB_TOKEN`, sent as a bearer. Public records only: no
secret, no door, no pool (Unsure 5). Redirects are not followed, so the
token travels to the API host alone. The token is read from the
environment and never written. Seats are not read; the registry is not
read.

    uv run python -m src.m07.gate --out-dir <dir> [--summary <md>]

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
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REPO = "andaro74/pharmadelta"
PLATFORM_REPO = "andaro74/agentkeel"
TEMPLATE = "agentkeel-studio/agent-template"
DEPLOY_WORKFLOW = ".github/workflows/deploy.yml"
DEPLOY_JOB = "deploy-agent"
SERVED_FILE = "pages/api/second-agent.json"
INDEX_PAGE = "index.html"
PAGES_DIR = "pages"
# The clock record's fields on a served entry (M07 README "Carried to PR 2"; fixed here). The lift writes them.
CLOCK_RECORD = ("repository", "repository_id", "template", "created_at", "pull_request", "merge_commit", "deploy_run", "deploy_job", "completed_at", "conclusion", "read_by")
READ_BY = ("run_url", "artifact")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
HEX = re.compile(r"^[0-9a-f]+$")
MIN_COMMIT_PREFIX = 20  # the fewest hex digits of the merge commit a cut job name must still hold
RUN_URL = re.compile(r"^https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/actions/runs/([0-9]+)$")
PAGE_BLOCK = re.compile(r'<script\s+type="application/json"\s+id="second-agent-([^"]*)"\s*>(.*?)</script>', re.DOTALL)
ENV = {"token": "GITHUB_TOKEN"}
MAX_BODY = 8 * 1024 * 1024
FALSIFIER = (
    "F7.1 a time this repository serves for its second agent was not read by this repository's CI from GitHub's own "
    "records of the agent's creation and deploy: it carries no clock record; or the repository the record names does "
    "not exist or was not created from agentkeel-studio/agent-template; or the record's start is not that "
    "repository's created_at; or its stop is not the completed_at of a deploy-agent job of agentkeel's deploy.yml "
    "that names the agent and the merge commit of its first pull request and concluded success; or elapsed_seconds "
    "is not the stop less the start; or a page shows a time for the second agent that the served file does not serve"
)


class Unscorable(Exception):
    """The inputs do not let F7.1 be judged. Not a verdict."""


def rel(path: Path) -> str:
    """The path as the repository names it, or as given when it lies outside the repository."""
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def api_base() -> str:
    return (os.environ.get("GITHUB_API_URL") or "https://api.github.com").rstrip("/")


def is_int(value: Any) -> bool:
    """A whole number. `True` is not one."""
    return isinstance(value, int) and not isinstance(value, bool)


def instant(value: Any) -> datetime | None:
    """A time with an offset, as GitHub writes one (`2026-10-10T16:54:39Z`), or None."""
    if not isinstance(value, str) or "T" not in value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


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
        "what": "M07 gate: the time pharmadelta serves for its second agent, read for a clock record, and for each time with one the repository, its first pull request and the deploy job read back from GitHub's API and compared; the verdict is ledger row 8's F7.1",
        "milestone": "M07",
        "ledger_row": 8,
        "falsifier": FALSIFIER,
        "run_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": commit,
        "dirty": dirty,
        "written_by_ci": ci is not None,
        "ci": ci,
        "repository": REPO,
        "platform_repository": PLATFORM_REPO,
        "template": TEMPLATE,
        "served_file": SERVED_FILE,
        "api": api_base(),
        "clock_record_fields": list(CLOCK_RECORD),
        "read_by_fields": list(READ_BY),
        "clock_reading": {
            "start_from": "GET /repos/<clock.repository>: created_at, id, full_name, template_repository.full_name",
            "first_pull_request_from": "GET /repos/<clock.repository>/pulls?state=all&sort=created&direction=asc&per_page=1: number, merged_at, merge_commit_sha",
            "stop_from": f"GET /repos/{PLATFORM_REPO}/actions/jobs/<clock.deploy_job>: run_id, name, conclusion, completed_at, run_attempt",
            "workflow_from": f"GET /repos/{PLATFORM_REPO}/actions/runs/<clock.deploy_run>: path, which must be {DEPLOY_WORKFLOW}",
            "job_name": f"{DEPLOY_JOB} (<repository>, <repository_id>, <commit>, ...), cut by GitHub at 97 characters; the commit is read whole or as a prefix of at least {MIN_COMMIT_PREFIX} hex digits",
            "seats_read": False,
            "registry_read": False,
            "note": "public records only, with the workflow's own token; the gate defines no record, it reads GitHub's",
        },
        "env_set": {name: bool(os.environ.get(var)) for name, var in ENV.items()},
        "env_note": "whether the environment held the workflow's token; its value is never written",
    }


# ---------------------------------------------------------------- reading
def read_served(path: Path) -> list[dict]:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Unscorable(f"{rel(path)} could not be read as JSON: {type(exc).__name__}: {str(exc)[:160]}") from exc
    agents = doc.get("agents") if isinstance(doc, dict) else None
    if not isinstance(agents, list) or not all(isinstance(a, dict) and isinstance(a.get("id"), str) for a in agents):
        raise Unscorable(f"{rel(path)} does not hold an `agents` list of objects with an `id`")
    if not agents:
        raise Unscorable(f"{rel(path)} serves no entry; there is nothing to judge")
    ids = [a["id"] for a in agents]
    if len(set(ids)) != len(ids):
        raise Unscorable(f"{rel(path)} serves one id more than once: {ids}")
    return agents


def default_pages() -> list[Path]:
    """The front page and every HTML page under `pages/`."""
    return [ROOT / INDEX_PAGE, *sorted((ROOT / PAGES_DIR).glob("*.html"))]


def read_page(path: Path) -> list[dict]:
    """The page's times: the JSON in each `id="second-agent-<id>"` block, one object each. No block: the page shows no time."""
    try:
        html = path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:  # ValueError: a page that is not UTF-8
        raise Unscorable(f"{rel(path)} could not be read: {type(exc).__name__}: {str(exc)[:160]}") from exc
    shown: list[dict] = []
    for block_id, block in PAGE_BLOCK.findall(html):
        try:
            obj = json.loads(block)
        except ValueError as exc:
            raise Unscorable(f"{rel(path)}: the block second-agent-{block_id} is not JSON: {str(exc)[:160]}") from exc
        if not isinstance(obj, dict) or not isinstance(obj.get("id"), str):
            raise Unscorable(f"{rel(path)}: the block second-agent-{block_id} is not an object with an `id`")
        shown.append({"page": rel(path), "block_id": block_id, "entry": obj})
    return shown


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def missing_fields(record: dict, fields: tuple[str, ...]) -> list[str]:
    return [f for f in fields if f not in record or record[f] in (None, "")]


def clock_record_check(entry: dict) -> dict:
    """Whether the served `clock` is a clock record, and why not."""
    clock = entry.get("clock")
    if clock is None:
        return {"has_record": False, "why": "clock is null"}
    if not isinstance(clock, dict):
        return {"has_record": False, "why": f"clock is a {type(clock).__name__}, not an object"}
    missing = missing_fields(clock, CLOCK_RECORD)
    if missing:
        return {"has_record": False, "why": f"clock lacks {missing}", "missing": missing}
    for field in ("repository", "template"):
        if not isinstance(clock[field], str) or not REPOSITORY.match(clock[field]):
            return {"has_record": False, "why": f"clock.{field} is not an owner/name"}
    for field in ("repository_id", "pull_request", "deploy_run", "deploy_job"):
        if not is_int(clock[field]) or clock[field] <= 0:
            return {"has_record": False, "why": f"clock.{field} is not a positive whole number"}
    for field in ("created_at", "completed_at"):
        if instant(clock[field]) is None:
            return {"has_record": False, "why": f"clock.{field} is not a time with an offset"}
    if not isinstance(clock["merge_commit"], str) or not SHA40.match(clock["merge_commit"]):
        return {"has_record": False, "why": "clock.merge_commit is not a commit (40 hex digits)"}
    if not isinstance(clock["conclusion"], str):
        return {"has_record": False, "why": f"clock.conclusion is a {type(clock['conclusion']).__name__}, not a word"}
    read_by = clock["read_by"]
    if not isinstance(read_by, dict) or missing_fields(read_by, READ_BY):
        return {"has_record": False, "why": f"clock.read_by is not an object with {list(READ_BY)}"}
    run = RUN_URL.match(read_by["run_url"]) if isinstance(read_by["run_url"], str) else None
    if not run:
        return {"has_record": False, "why": "clock.read_by.run_url is not a run URL on github.com"}
    if run.group(1) != REPO:
        return {"has_record": False, "why": f"clock.read_by.run_url is a run of {run.group(1)}, not of {REPO}"}
    if not isinstance(read_by["artifact"], str):
        return {"has_record": False, "why": "clock.read_by.artifact is not a name"}
    return {"has_record": True, "why": "a clock record naming the repository, its first pull request, the deploy job and the run that read them, every field present"}


def unrecorded(served: list[dict]) -> tuple[list[str], dict[str, dict]]:
    """Every served entry that serves a time and carries no clock record."""
    checks: dict[str, dict] = {}
    for a in served:
        serves_time = a.get("elapsed_seconds") is not None
        checks[a["id"]] = {"serves_time": serves_time, "elapsed_seconds": a.get("elapsed_seconds"), "clock_record": clock_record_check(a)}
    return [i for i, c in checks.items() if c["serves_time"] and not c["clock_record"]["has_record"]], checks


def disagreed(served: list[dict], shown: list[dict]) -> tuple[list[str], list[dict]]:
    by_id = {a["id"]: a for a in served}
    entries = []
    for item in shown:
        page, block_id = item["entry"], item["block_id"]
        base = {"id": page["id"], "page": item["page"], "block": block_id}
        api = by_id.get(page["id"])
        if api is None:
            entries.append({**base, "equal": False, "why": "the file serves no entry with this id"})
        elif block_id != page["id"]:
            entries.append({**base, "equal": False, "why": f"shown in the block second-agent-{block_id}, not second-agent-{page['id']}"})
        elif canonical(api) != canonical(page):
            keys = sorted(k for k in set(api) | set(page) if canonical(api.get(k)) != canonical(page.get(k)))
            entries.append({**base, "equal": False, "why": f"differs from the file's entry on {keys}", "keys": keys})
        else:
            entries.append({**base, "equal": True, "why": "equal to the file's entry as parsed JSON"})
    ids: list[str] = []
    for e in entries:
        if not e["equal"] and e["id"] not in ids:
            ids.append(e["id"])
    return ids, entries


# --------------------------------------------------------------- transport
class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Redirects are not followed: the bearer token goes to the API host and nowhere else. A redirect is read as its status."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, D102
        return None


class Api:
    """GETs on GitHub's API, each recorded by path and status. The token is in no field."""

    def __init__(self, token: str | None) -> None:
        self.token = token
        self.reads: list[dict] = []

    def get(self, path: str) -> dict:
        """GET an API path as JSON. `status` is GitHub's, or None when no answer came; `read` is true on 200 with a JSON body."""
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "pharmadelta-m07-gate", "X-GitHub-Api-Version": "2022-11-28"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        out: dict[str, Any] = {"path": path, "status": None, "read": False, "json": None}
        try:
            with urllib.request.build_opener(NoRedirect()).open(urllib.request.Request(f"{api_base()}{path}", headers=headers), timeout=60) as resp:
                out["status"] = resp.status
                body = resp.read(MAX_BODY + 1)
            if len(body) > MAX_BODY:
                out["why"] = f"GET {path}: the body is larger than {MAX_BODY} bytes"
            elif out["status"] != 200:
                out["why"] = f"GET {path} answered {out['status']}"
            else:
                out["json"] = json.loads(body.decode("utf-8"))
                out["read"] = True
        except urllib.error.HTTPError as exc:
            out["status"] = exc.code
            out["why"] = f"GET {path} answered {exc.code}"
        except ValueError as exc:  # not UTF-8, not JSON
            out["why"] = f"GET {path} did not answer JSON: {type(exc).__name__}"
        except Exception as exc:  # noqa: BLE001  URLError, timeout, http.client's own
            out["why"] = f"GET {path}: {type(exc).__name__}: {str(exc)[:120]}"
        self.reads.append({k: v for k, v in out.items() if k != "json"})
        return out


# ---------------------------------------------------------------- read-back
def read_repository(api: Api, repository: str) -> dict:
    """GitHub's record of the repository: its name, id, creation time and the template it was created from."""
    got = api.get(f"/repos/{repository}")
    if got["status"] == 404:
        return {"read": True, "exists": False, "status": 404, "read_from": got["path"], "why": f"GitHub answered 404 for {repository}: it does not exist, or is not public"}
    if not got["read"] or not isinstance(got["json"], dict):
        return {"read": False, "status": got["status"], "why": got.get("why") or f"GET {got['path']} did not answer an object"}
    doc = got["json"]
    template = doc.get("template_repository") if isinstance(doc.get("template_repository"), dict) else {}
    return {
        "read": True,
        "exists": True,
        "status": 200,
        "read_from": got["path"],
        "full_name": doc.get("full_name"),
        "id": doc.get("id"),
        "created_at": doc.get("created_at"),
        "template": template.get("full_name"),
        "private": doc.get("private"),
        "archived": doc.get("archived"),
    }


def read_first_pull_request(api: Api, repository: str) -> dict:
    """The repository's first pull request, by creation time: its number, whether it merged, its merge commit."""
    got = api.get(f"/repos/{repository}/pulls?state=all&sort=created&direction=asc&per_page=1")
    if not got["read"] or not isinstance(got["json"], list):
        return {"read": False, "status": got["status"], "why": got.get("why") or f"GET {got['path']} did not answer a list"}
    if not got["json"] or not isinstance(got["json"][0], dict):
        return {"read": True, "found": False, "status": 200, "read_from": got["path"], "why": f"{repository} has no pull request"}
    pull = got["json"][0]
    return {
        "read": True,
        "found": True,
        "status": 200,
        "read_from": got["path"],
        "number": pull.get("number"),
        "state": pull.get("state"),
        "created_at": pull.get("created_at"),
        "merged_at": pull.get("merged_at"),
        "merge_commit": pull.get("merge_commit_sha") if pull.get("merged_at") else None,
    }


def read_job(api: Api, job_id: int) -> dict:
    """GitHub's record of one job of agentkeel's: one attempt's, by id."""
    got = api.get(f"/repos/{PLATFORM_REPO}/actions/jobs/{job_id}")
    if got["status"] == 404:
        return {"read": True, "found": False, "status": 404, "read_from": got["path"], "why": f"GitHub answered 404 for job {job_id} of {PLATFORM_REPO}"}
    if not got["read"] or not isinstance(got["json"], dict):
        return {"read": False, "status": got["status"], "why": got.get("why") or f"GET {got['path']} did not answer an object"}
    doc = got["json"]
    return {
        "read": True,
        "found": True,
        "status": 200,
        "read_from": got["path"],
        "id": doc.get("id"),
        "run_id": doc.get("run_id"),
        "run_attempt": doc.get("run_attempt"),
        "name": doc.get("name"),
        "workflow_name": doc.get("workflow_name"),
        "status_of_job": doc.get("status"),
        "conclusion": doc.get("conclusion"),
        "started_at": doc.get("started_at"),
        "completed_at": doc.get("completed_at"),
        "url": doc.get("html_url"),
    }


def read_run(api: Api, run_id: int) -> dict:
    """GitHub's record of the run the job belongs to: the workflow file it ran."""
    got = api.get(f"/repos/{PLATFORM_REPO}/actions/runs/{run_id}")
    if got["status"] == 404:
        return {"read": True, "found": False, "status": 404, "read_from": got["path"], "why": f"GitHub answered 404 for run {run_id} of {PLATFORM_REPO}"}
    if not got["read"] or not isinstance(got["json"], dict):
        return {"read": False, "status": got["status"], "why": got.get("why") or f"GET {got['path']} did not answer an object"}
    doc = got["json"]
    return {
        "read": True,
        "found": True,
        "status": 200,
        "read_from": got["path"],
        "id": doc.get("id"),
        "path": doc.get("path"),
        "event": doc.get("event"),
        "run_attempt": doc.get("run_attempt"),
        "conclusion": doc.get("conclusion"),
        "url": doc.get("html_url"),
    }


def parse_job_name(name: Any) -> dict:
    """The job and the matrix values GitHub put in its name, by position; `cut` when GitHub ended the name with `...`."""
    if not isinstance(name, str) or " (" not in name:
        return {"job": name if isinstance(name, str) else None, "values": [], "cut": False}
    job, _, rest = name.partition(" (")
    cut = rest.endswith("...")
    rest = rest[:-3] if cut else rest.removesuffix(")")
    return {"job": job, "values": [v.strip() for v in rest.split(", ")], "cut": cut}


def job_name_check(name: Any, repository: str, repository_id: int, merge_commit: str) -> dict:
    """Whether the job's name is a `deploy-agent` leg for this repository, its id and this merge commit, and what differs."""
    parsed = parse_job_name(name)
    values, differences = parsed["values"], []
    if parsed["job"] != DEPLOY_JOB:
        differences.append(f"the job is {parsed['job']!r}, not a {DEPLOY_JOB} job")
    if len(values) < 3:
        differences.append(f"the job's name carries {len(values)} values, not the repository, its id and the commit")
        return {**parsed, "commit_in_name": None, "commit_whole": None, "differences": differences}
    if values[0] != repository:
        differences.append(f"the job's name carries the repository {values[0]!r}, not {repository!r}")
    if values[1] != str(repository_id):
        differences.append(f"the job's name carries the repository id {values[1]!r}, not {repository_id}")
    commit = values[2]
    whole = bool(SHA40.match(commit))
    # A value that the cut ended is the last one; only then may the commit be a prefix.
    prefix_allowed = parsed["cut"] and len(values) == 3
    if whole:
        if commit != merge_commit:
            differences.append(f"the job's name carries the commit {commit[:12]}…, not the merge commit {merge_commit[:12]}…")
    elif prefix_allowed and HEX.match(commit) and len(commit) >= MIN_COMMIT_PREFIX:
        if not merge_commit.startswith(commit):
            differences.append(f"the job's name carries a commit beginning {commit[:12]}…, not the merge commit {merge_commit[:12]}…")
    else:
        differences.append(f"the job's name carries {commit!r} where the commit is, not 40 hex digits or a cut prefix of at least {MIN_COMMIT_PREFIX}")
    return {**parsed, "commit_in_name": commit, "commit_whole": whole, "differences": differences}


def read_back(entry: dict, api: Api) -> dict:
    """Everything F7.1 asks GitHub about one served time; what differs and what could not be read.

    A read that raises is a read not made and is recorded under `not_read`; the differences found before it stand
    (M05 PR 3's rule). `run()` keeps a last fence around this function for what it does not foresee.
    """
    differences: list[str] = []
    not_read: list[str] = []
    out: dict[str, Any] = {}
    try:
        _read_back(entry, api, out, differences, not_read)
    except Exception as exc:  # noqa: BLE001
        not_read.append(f"the read-back raised {type(exc).__name__}: {str(exc)[:160]}")
    out["differences"], out["not_read"] = differences, not_read
    out["equal"] = None if (not differences and not_read) else not differences
    return out


def _read_back(entry: dict, api: Api, out: dict[str, Any], differences: list[str], not_read: list[str]) -> None:
    clock = entry["clock"]
    repository, merge_commit = clock["repository"], clock["merge_commit"]
    start, stop = instant(clock["created_at"]), instant(clock["completed_at"])

    # The record against the entry and itself: no network.
    if entry.get("repository") != repository:
        differences.append(f"the entry's repository {entry.get('repository')!r} is not the record's {repository!r}")
    if clock["template"] != TEMPLATE:
        differences.append(f"the record's template {clock['template']!r} is not {TEMPLATE!r}")
    if clock["conclusion"] != "success":
        differences.append(f"the record's conclusion is {clock['conclusion']!r}, not 'success'")
    recorded = (stop - start).total_seconds()
    elapsed = entry.get("elapsed_seconds")
    out["elapsed"] = {"served": elapsed, "record_stop_less_start": recorded, "github_stop_less_start": None}
    if recorded <= 0:
        differences.append(f"the record's stop {clock['completed_at']} is not after its start {clock['created_at']}")
    if not is_int(elapsed):
        differences.append(f"elapsed_seconds is {elapsed!r}, not a whole number of seconds")
    elif elapsed != recorded:
        differences.append(f"elapsed_seconds {elapsed} is not the record's stop less its start ({recorded:g} s)")

    # The start: the repository.
    repo = read_repository(api, repository)
    out["repository"] = repo
    github_start = None
    if not repo["read"]:
        not_read.append(f"the repository {repository}: {repo['why']}")
    elif not repo["exists"]:
        differences.append(f"the repository the record names does not exist: {repo['why']}")
    else:
        if repo["full_name"] != repository:
            differences.append(f"GitHub names the repository {repo['full_name']!r}, not {repository!r}")
        if repo["id"] != clock["repository_id"]:
            differences.append(f"the repository's id is {repo['id']!r}, not the record's {clock['repository_id']}")
        if repo["template"] != TEMPLATE:
            differences.append(f"the repository was created from {repo['template']!r}, not from {TEMPLATE!r}")
        github_start = instant(repo["created_at"])
        if github_start is None:
            not_read.append(f"the repository's created_at {repo['created_at']!r} is not a time")
        elif github_start != start:
            differences.append(f"the record's start {clock['created_at']} is not the repository's created_at {repo['created_at']}")

    # The merge commit: the first pull request. Not asked of a repository that does not exist.
    if repo["read"] and not repo["exists"]:
        out["first_pull_request"] = {"read": False, "why": "the repository does not exist; not asked"}
    else:
        pull = read_first_pull_request(api, repository)
        out["first_pull_request"] = pull
        if not pull["read"]:
            not_read.append(f"the first pull request of {repository}: {pull['why']}")
        elif not pull["found"]:
            differences.append(pull["why"])
        else:
            if pull["number"] != clock["pull_request"]:
                differences.append(f"the first pull request is #{pull['number']}, not the record's #{clock['pull_request']}")
            if not pull["merged_at"]:
                differences.append(f"the first pull request #{pull['number']} is not merged (state {pull['state']!r})")
            elif pull["merge_commit"] != merge_commit:
                differences.append(f"the first pull request's merge commit is {str(pull['merge_commit'])[:12]}…, not the record's {merge_commit[:12]}…")

    # The stop: the deploy job, by id.
    job = read_job(api, clock["deploy_job"])
    out["deploy_job"] = job
    github_stop = None
    if not job["read"]:
        not_read.append(f"the deploy job {clock['deploy_job']}: {job['why']}")
    elif not job["found"]:
        differences.append(f"the job the record names does not exist: {job['why']}")
    else:
        if job["run_id"] != clock["deploy_run"]:
            differences.append(f"job {clock['deploy_job']} belongs to run {job['run_id']!r}, not the record's {clock['deploy_run']}")
        name = job_name_check(job["name"], repository, clock["repository_id"], merge_commit)
        out["deploy_job"]["name_read"] = name
        differences.extend(name["differences"])
        if job["conclusion"] != "success":
            differences.append(f"the job concluded {job['conclusion']!r}, not 'success'")
        if job["conclusion"] != clock["conclusion"]:
            differences.append(f"the record's conclusion {clock['conclusion']!r} is not the job's {job['conclusion']!r}")
        github_stop = instant(job["completed_at"])
        if github_stop is None:
            differences.append(f"the job has no completed_at ({job['completed_at']!r})")
        elif github_stop != stop:
            differences.append(f"the record's stop {clock['completed_at']} is not the job's completed_at {job['completed_at']}")

    # The workflow: the run the record names.
    run = read_run(api, clock["deploy_run"])
    out["deploy_run"] = run
    if not run["read"]:
        not_read.append(f"the deploy run {clock['deploy_run']}: {run['why']}")
    elif not run["found"]:
        differences.append(f"the run the record names does not exist: {run['why']}")
    elif run["path"] != DEPLOY_WORKFLOW:
        differences.append(f"run {clock['deploy_run']} is a run of {run['path']!r}, not of {DEPLOY_WORKFLOW}")

    # The time, from GitHub's two records.
    if github_start is not None and github_stop is not None:
        github_elapsed = (github_stop - github_start).total_seconds()
        out["elapsed"]["github_stop_less_start"] = github_elapsed
        if is_int(elapsed) and elapsed != github_elapsed:
            differences.append(f"elapsed_seconds {elapsed} is not GitHub's stop less GitHub's start ({github_elapsed:g} s)")


# ------------------------------------------------------------------- gate
def judge(served: list[dict], unrecorded_ids: list[str], disagreed_ids: list[str], differing_ids: list[str], unreadable: list[str]) -> dict:
    if unrecorded_ids or disagreed_ids or differing_ids:
        verdict, parts = "RED", []
        if unrecorded_ids:
            parts.append(f"times {', '.join(unrecorded_ids)} are served with no clock record")
        if disagreed_ids:
            parts.append(f"page times {', '.join(disagreed_ids)} are not what the file serves")
        if differing_ids:
            parts.append(f"times {', '.join(differing_ids)} were not read back as GitHub's records of the repository's creation and the agent's deploy")
        reason = "F7.1 holds: " + "; ".join(parts)
    elif unreadable:
        verdict = "UNSCORABLE"
        reason = "nothing is RED and a reading F7.1 needs could not be made: " + "; ".join(unreadable)
    else:
        verdict = "GREEN"
        reason = "F7.1 does not hold: every served time carries a clock record, the repository exists and was created from the template, the start is its created_at, the stop is the completed_at of the deploy-agent job for the first pull request's merge commit, the job concluded success, elapsed_seconds is the stop less the start, and every page block is the file's entry"
    return {
        "verdict": verdict,
        "reason": reason,
        "times_unrecorded": unrecorded_ids,
        "times_disagreed": disagreed_ids,
        "times_differing": differing_ids,
        "unreadable": unreadable,
        "counts": {"served": len(served), "unrecorded": len(unrecorded_ids), "disagreed": len(disagreed_ids), "differing": len(differing_ids)},
    }


def summary_markdown(result: dict) -> str:
    lines = [f"## M07 gate: {result['verdict']}", "", result["reason"] + ".", ""]
    lines.append(f"Commit `{result.get('commit') or 'unknown'}`" + (" (dirty tree)" if result.get("dirty") else "") + f", written by CI: `{result['written_by_ci']}`.")
    lines.append("")
    if "error" in result:
        lines += [f"`{result['error']['type']}: {result['error']['message']}`", ""]
    if result.get("served"):
        lines += ["| served | serves a time | clock record | shown on a page | repository | first pull request | deploy job | read back |", "|---|---|---|---|---|---|---|---|"]
        for e in result["served"]:
            rb = e.get("read_back") or {}
            record_s = "yes" if e["clock_record"]["has_record"] else "no: " + e["clock_record"]["why"]
            shown = e.get("page_equal")
            shown_s = "on no page" if shown is None else ("as served" if shown else "not as served")
            if not rb:
                repo_s = pull_s = job_s = "not read"
                rb_s = f"not read back: {e.get('not_read_back')}"
            else:
                repo, pull, job = rb.get("repository") or {}, rb.get("first_pull_request") or {}, rb.get("deploy_job") or {}
                repo_s = "not read" if not repo.get("read") else (f"created {repo.get('created_at')}" if repo.get("exists") else "does not exist")
                pull_s = "not read" if not pull.get("read") else (f"#{pull.get('number')}, merged {pull.get('merged_at')}" if pull.get("found") else "none")
                job_s = "not read" if not job.get("read") else (f"{job.get('conclusion')}, completed {job.get('completed_at')}" if job.get("found") else "does not exist")
                rb_s = "equal" if rb.get("equal") else ("not fully read" if rb.get("equal") is None else "; ".join(rb.get("differences") or []))
            lines.append(f"| {e['id']} | {'yes' if e['serves_time'] else 'no'} | {record_s} | {shown_s} | {repo_s} | {pull_s} | {job_s} | {rb_s} |")
        lines.append("")
    if result.get("unreadable"):
        lines += ["Not read:", ""] + [f"- {u}" for u in result["unreadable"]] + [""]
    if result["verdict"] == "UNSCORABLE":
        lines.append("UNSCORABLE is not a verdict on ledger row 8's F7.1. It is never RED and never GREEN.")
    else:
        lines.append("The verdict judges ledger row 8's F7.1 only. No time is shown here: a time is a result only with its clock record and the run that read it. Seats and the registry are not read.")
    return "\n".join(lines) + "\n"


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_result(args: argparse.Namespace, result: dict) -> None:
    write_json(args.out_dir / "result.json", result)
    text = summary_markdown(result)
    print(text)
    if args.summary:
        try:
            args.summary.parent.mkdir(parents=True, exist_ok=True)
            with args.summary.open("a", encoding="utf-8") as fh:
                fh.write(text)
        except OSError as exc:  # the result is written; a summary that cannot be appended changes nothing (M04 PR 3, Defect 3)
            print(f"the summary could not be appended: {exc!r}", file=sys.stderr)


def run(args: argparse.Namespace) -> int:
    unreadable: list[str] = []
    served = read_served(args.api)
    shown: list[dict] = []
    pages_read: list[dict] = []
    for page in args.page or default_pages():
        try:
            blocks = read_page(page)
        except Unscorable as exc:
            unreadable.append(str(exc))
            pages_read.append({"page": rel(page), "read": False, "blocks": None})
            continue
        shown += blocks
        pages_read.append({"page": rel(page), "read": True, "blocks": [b["block_id"] for b in blocks]})
    unrecorded_ids, checks = unrecorded(served)
    disagreed_ids, page_entries = disagreed(served, shown)
    page_equal: dict[str, bool] = {}
    for e in page_entries:
        page_equal[e["id"]] = page_equal.get(e["id"], True) and e["equal"]

    api = Api(os.environ.get(ENV["token"]) or None)
    entries, differing_ids = [], []
    for a in served:
        check = checks[a["id"]]
        entry: dict[str, Any] = {"id": a["id"], "name": a.get("name"), "repository": a.get("repository"), **check, "page_equal": page_equal.get(a["id"])}
        if not check["serves_time"]:
            entry["read_back"] = None
            entry["not_read_back"] = "the entry serves no time"
        elif not check["clock_record"]["has_record"]:
            entry["read_back"] = None
            entry["not_read_back"] = "no clock record"
        else:
            try:
                entry["read_back"] = read_back(a, api)
            except Exception as exc:  # noqa: BLE001  a read-back that raises is a read-back not made; the lists stand (M05 PR 3's rule)
                entry["read_back"] = {"equal": None, "differences": [], "not_read": [f"the read-back raised {type(exc).__name__}: {str(exc)[:160]}"]}
            for why in entry["read_back"]["not_read"]:
                unreadable.append(f"{a['id']}: {why}")
            if entry["read_back"]["differences"]:
                differing_ids.append(a["id"])
        entries.append(entry)

    result = {
        **provenance(),
        **judge(served, unrecorded_ids, disagreed_ids, differing_ids, unreadable),
        "served": entries,
        "pages": {"read": pages_read, "times_shown": [{"page": s["page"], "id": s["entry"]["id"]} for s in shown], "entries": page_entries},
        "api_reads": api.reads,
    }
    write_result(args, result)
    return {"GREEN": 0, "RED": 1}.get(result["verdict"], 2)


def unscorable(args: argparse.Namespace, exc: BaseException) -> int:
    refused = isinstance(exc, Unscorable)
    result = {
        **provenance(),
        "verdict": "UNSCORABLE",
        "reason": "F7.1 is not judged: " + ("the gate refused the inputs" if refused else "the gate raised"),
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
    parser.add_argument("--summary", type=Path, help="append a Markdown summary here (GITHUB_STEP_SUMMARY in CI)")
    parser.add_argument("--api", type=Path, default=ROOT / "pages" / "api" / "second-agent.json")
    parser.add_argument("--page", type=Path, action="append", help="a page to read for blocks; repeat. Default: index.html and every pages/*.html")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    try:
        return run(args)
    except Exception as exc:  # noqa: BLE001  every failure to judge is UNSCORABLE, written and exit 2; never the RED code
        return unscorable(args, exc)


if __name__ == "__main__":
    raise SystemExit(main())
