"""The M01 reader: read the plant in `agentkeel-studio/label-impact` and judge F1.1 (ledger row 1).

Reads, from GitHub's API, label-impact's first pull request at its head:
the manifest's seven seats, each seat's permission on the repository, the
check runs on the head with the App that posted each, the pull request's
`mergeable_state` and merge state; agentkeel's `deploy.yml` runs since the
repository was created, and which of their jobs name `label-impact`; and
the registry row for `label-impact`, which this repository has no
credential to read, so it is recorded as unread. Every reading is written
beside the verdict. Anything that cannot be read is written as unread,
with the error, never left out.

The verdict is ledger row 1's claim, "seats filled, deployed", read as
`milestones/M01/README.md` "Carried to PR 2" defines it:

- RED while any seat in `manifest.yaml` at the head is not a login that
  administers the repository: null, empty, not of a login's form, or read
  as a permission other than `admin`. Each such seat is named. A seat
  whose permission GitHub would not answer (404 as much as 403) is
  unread, not unassigned. No `manifest.yaml` at the head (404) is a fact
  about the commit: every seat unassigned, RED. The `finding` beside RED
  says what else was found: `F1.1` when the pull request is merged or is
  read as mergeable; `control refused` when a `platform-check` from
  agentkeel's App refused the head naming the seats check; otherwise
  `unassigned, no refusal read`. The ledger's expected output names the
  second.
  "Mergeable" is GitHub's `mergeable_state` `clean`, `unstable` or
  `has_hooks` (REST), or `mergeStateStatus` `CLEAN`, `UNSTABLE` or
  `HAS_HOOKS` (GraphQL): the states GitHub merges from. GraphQL decides
  when it was read, else REST. Both are judged only when a token asked:
  with no token REST showed `unstable` on a head the ruleset blocked
  (construction run, M01 PR 2), so a no-token read is recorded as unread
  for F1.1's purpose and cannot make the finding F1.1.
- GREEN only when every seat is assigned and read as `admin`, the pull
  request is merged, a `deploy-agent` job of agentkeel's `deploy.yml`
  naming `label-impact` and the merge commit (`merge_commit_sha`, main's
  head after the merge, which agentkeel deploys) concluded `success`, and
  the registry was read and holds `label-impact`. A seat whose permission
  could not be read, or an unread registry, does not make GREEN possible.
- PENDING when neither: no seat is read as unassigned, and GREEN's
  conditions are not all met. The result names what is missing.
- UNSCORABLE when the pull request, the repository, the manifest (any
  answer but 200 or 404) or the check runs could not be read, or anything
  raises inside `main`. Never RED, never GREEN. A failure before `main`
  runs (an import error) exits 1 with no result file; the file, not the
  exit code, is the verdict.

Only a CI-written result is evidence (P4); the result says whether CI
wrote it. Reads use `GITHUB_TOKEN` when set, else no token; which one is
recorded.

    uv run python -m src.m01.reader --out <result.json> [--summary <md>]

Exit status: 0 GREEN, 1 RED, 2 UNSCORABLE, 3 PENDING.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
API = os.environ.get("GITHUB_API_URL", "https://api.github.com")
AGENT_REPOSITORY = "agentkeel-studio/label-impact"
AGENT_NAME = "label-impact"
PULL_REQUEST = 1
PLATFORM_REPOSITORY = "andaro74/agentkeel"
PLATFORM_APP_ID = 5144253  # agentkeel-platform, the App the agent ruleset requires (infra/ruleset/agent.json at m08)
PLATFORM_CHECK = "platform-check"
# SPEC/00 §5's seven seats, as the manifest keys them.
SEATS = ("product", "rule-owner", "data-owner", "tool-owner", "threshold-owner", "security", "engineering")
LOGIN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}$")  # GitHub's form, as agentkeel reads it
REFUSED = re.compile(r"^- \*\*(.+?)\*\*: ", re.MULTILINE)  # one line per refused check in the App's summary
SHA = re.compile(r"\b[0-9a-f]{40}\b")
MAX_DEPLOY_RUNS = 100  # one page; more than this since the plant is recorded as truncated


class Unreadable(Exception):
    """A reading the verdict cannot do without could not be made. Not a verdict."""


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


# --- GitHub -----------------------------------------------------------------------------


def token() -> tuple[str | None, str]:
    if value := os.environ.get("GITHUB_TOKEN"):
        return value, "GITHUB_TOKEN"
    return None, "no token"


def gh(path: str, *, raw: bool = False) -> tuple[int, Any]:
    """(status, body) for GET. An HTTP error is returned, not raised; a network error raises."""
    request = urllib.request.Request(path if path.startswith("http") else f"{API}{path}")
    request.add_header("Accept", "application/vnd.github.raw" if raw else "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    value, _ = token()
    if value:
        request.add_header("Authorization", f"Bearer {value}")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read()
            return response.status, (body.decode("utf-8") if raw else (json.loads(body) if body else None))
    except urllib.error.HTTPError as exc:
        return exc.code, None


def must(path: str, what: str, *, raw: bool = False) -> Any:
    status, body = gh(path, raw=raw)
    if status != 200:
        raise Unreadable(f"{what}: GET {path} answered {status} with {token()[1]}")
    return body


# --- the pull request and its head ----------------------------------------------------------


def merge_state_graphql() -> dict[str, Any]:
    """GraphQL's `mergeStateStatus`, the field `gh pr view` shows. Needs a token; without one, or when GraphQL
    refuses the token, it is unread. Read beside REST's `mergeable_state` because the two can disagree for a
    caller without access to the repository's rulesets (construction run, M01 PR 2: REST said `unstable` with
    no token and `blocked` with an administrator's token, while GraphQL said `BLOCKED`)."""
    owner, name = AGENT_REPOSITORY.split("/")
    query = f'{{ repository(owner:"{owner}", name:"{name}") {{ pullRequest(number:{PULL_REQUEST}) {{ mergeStateStatus mergeable statusCheckRollup {{ state }} }} }} }}'
    value, which = token()
    if not value:
        return {"read": False, "why": "GraphQL needs a token; none set", "merge_state_status": None, "mergeable": None, "status_check_rollup": None}
    request = urllib.request.Request(f"{API}/graphql", data=json.dumps({"query": query}).encode("utf-8"), method="POST")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("Content-Type", "application/json")
    request.add_header("Authorization", f"Bearer {value}")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return {"read": False, "why": f"POST /graphql answered {exc.code} with {which}", "merge_state_status": None, "mergeable": None, "status_check_rollup": None}
    pr = ((body.get("data") or {}).get("repository") or {}).get("pullRequest") or {}
    if not pr:
        return {"read": False, "why": f"GraphQL returned no pull request with {which}: {json.dumps(body.get('errors'))}", "merge_state_status": None, "mergeable": None, "status_check_rollup": None}
    return {"read": True, "why": None, "merge_state_status": pr.get("mergeStateStatus"), "mergeable": pr.get("mergeable"),
            "status_check_rollup": (pr.get("statusCheckRollup") or {}).get("state")}  # fmt: skip


def read_pull_request() -> dict[str, Any]:
    """GitHub's own reading of the pull request. `mergeable_state` is computed lazily; ask up to three times."""
    pull: dict[str, Any] = {}
    for attempt in range(3):
        pull = must(f"/repos/{AGENT_REPOSITORY}/pulls/{PULL_REQUEST}", "the pull request")
        if pull.get("mergeable_state") != "unknown":
            break
        time.sleep(2 * (attempt + 1))
    return {
        "repository": AGENT_REPOSITORY,
        "number": PULL_REQUEST,
        "url": pull.get("html_url"),
        "state": pull.get("state"),
        "head_sha": pull["head"]["sha"],
        "head_ref": pull["head"].get("ref"),
        "merged": bool(pull.get("merged")),
        "merged_at": pull.get("merged_at"),
        "merge_commit_sha": pull.get("merge_commit_sha") if pull.get("merged") else None,
        # `mergeable` says only that the branch has no conflict; `mergeable_state` is what the ruleset
        # decides, and `clean` is F1.1's "mergeable" (milestones/M01/README.md, "Observed at open").
        "mergeable": pull.get("mergeable"),
        "mergeable_state": pull.get("mergeable_state"),
        "graphql": merge_state_graphql(),
        "read_at": now(),
    }


def read_seats(head: str) -> dict[str, Any]:
    """The seven seats as the commit holds them. No manifest is a fact about the commit: every seat unassigned."""
    status, text = gh(f"/repos/{AGENT_REPOSITORY}/contents/manifest.yaml?ref={head}", raw=True)
    if status == 404:
        return {"manifest": None, "seats": {slug: None for slug in SEATS}, "read_at": now()}
    if status != 200:
        raise Unreadable(f"manifest.yaml at {head}: {status} with {token()[1]}")
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise Unreadable(f"manifest.yaml at {head} is not YAML ({type(exc).__name__})") from exc
    seats = doc.get("seats") if isinstance(doc, dict) else None
    seats = seats if isinstance(seats, dict) else {}
    return {"manifest": "manifest.yaml", "seats": {slug: seats.get(slug) for slug in SEATS}, "read_at": now()}


def read_owner() -> dict[str, Any]:
    repo = must(f"/repos/{AGENT_REPOSITORY}", "the repository")
    owner = repo.get("owner") or {}
    return {"id": repo.get("id"), "created_at": repo.get("created_at"), "owner": owner.get("login"), "owner_type": owner.get("type")}


_permission_cache: dict[str, dict[str, Any]] = {}


def read_permission(login: str, owner: dict[str, Any]) -> dict[str, Any]:
    """What GitHub says `login` holds on the repository, as agentkeel's seat validator asks it (src/validate/seats.py at m08).

    A person who owns a personal repository holds it; an organisation's own login never does. Anyone else is
    asked of the collaborator permission endpoint, which answers only a token with access to the repository.
    Any answer but 200 is recorded as unread with its status: this reader does not know whether 404 means
    "not a collaborator" or "this token cannot see collaborators", so it says neither."""
    if login in _permission_cache:
        return _permission_cache[login]
    if owner.get("owner_type") == "User" and str(owner.get("owner", "")).lower() == login.lower():
        found = {"read": True, "permission": "admin", "why": f"owner of {AGENT_REPOSITORY}"}
    elif str(owner.get("owner", "")).lower() == login.lower():
        found = {"read": True, "permission": None, "why": f"{login} is the organisation that owns {AGENT_REPOSITORY}, not a person"}
    else:
        status, body = gh(f"/repos/{AGENT_REPOSITORY}/collaborators/{login}/permission")
        if status == 200 and isinstance(body, dict):
            held = body.get("permission")
            found = {"read": True, "permission": held, "why": f"GitHub answered {held!r} with {token()[1]}"}
        else:
            found = {"read": False, "permission": None, "why": f"GET collaborators/{login}/permission answered {status} with {token()[1]}: unread"}
    _permission_cache[login] = found
    return found


def judge_seats(seats: dict[str, Any], owner: dict[str, Any]) -> list[dict[str, Any]]:
    judged = []
    # `admin_read` is True whenever nothing is unread: on a null, empty or malformed seat no read was needed, and on
    # a seat read as not admin the read was made. It is False only on an assigned seat GitHub did not answer for.
    for slug in SEATS:
        value = seats.get(slug)
        if not isinstance(value, str) or not value.strip():
            judged.append({"seat": slug, "login": value, "assigned": False, "admin": None, "admin_read": True, "why": f"seat {slug} is {value!r}: unassigned"})
            continue
        login = value.strip()
        if not LOGIN.match(login):
            judged.append({"seat": slug, "login": login, "assigned": False, "admin": None, "admin_read": True, "why": f"{login!r} is not a GitHub login"})
            continue
        found = read_permission(login, owner)
        if not found["read"]:
            judged.append({"seat": slug, "login": login, "assigned": True, "admin": None, "admin_read": False, "why": found["why"]})
        elif found["permission"] == "admin":
            judged.append({"seat": slug, "login": login, "assigned": True, "admin": True, "admin_read": True, "why": found["why"]})
        else:
            judged.append({"seat": slug, "login": login, "assigned": False, "admin": False, "admin_read": True, "why": f"{found['why']}: not admin"})
    return judged


def read_check_runs(head: str) -> list[dict[str, Any]]:
    """Every check run on the head, with the App that posted it and the checks its own summary says it refused."""
    runs = must(f"/repos/{AGENT_REPOSITORY}/commits/{head}/check-runs?per_page=100", "the check runs on the head").get("check_runs") or []
    out = []
    for run in runs:
        output = run.get("output") or {}
        summary = output.get("summary")
        refused = [] if run.get("conclusion") == "success" else (REFUSED.findall(summary) if isinstance(summary, str) else None)
        out.append({
            "id": run.get("id"), "name": run.get("name"), "url": run.get("html_url"),
            "app_id": (run.get("app") or {}).get("id"), "app_slug": (run.get("app") or {}).get("slug"),
            "status": run.get("status"), "conclusion": run.get("conclusion"), "completed_at": run.get("completed_at"),
            "output": {"title": output.get("title"), "summary": summary, "text": output.get("text")},
            "refused": refused,
        })  # fmt: skip
    return out


def read_required_checks() -> dict[str, Any]:
    """The live rulesets' required checks, each with the App it must come from; unread when GitHub refuses the list."""
    try:
        status, listed = gh(f"/repos/{AGENT_REPOSITORY}/rulesets?includes_parents=false&per_page=100")
        if status != 200:
            return {"read": False, "why": f"GET rulesets answered {status} with {token()[1]}", "checks": None}
        checks = []
        for one in listed or []:
            status, ruleset = gh(f"/repos/{AGENT_REPOSITORY}/rulesets/{one['id']}")
            if status != 200:
                return {"read": False, "why": f"GET rulesets/{one['id']} answered {status} with {token()[1]}", "checks": None}
            for rule in ruleset.get("rules") or []:
                if rule.get("type") == "required_status_checks":
                    checks += [{"ruleset_id": one["id"], "context": c.get("context"), "integration_id": c.get("integration_id")}
                               for c in (rule.get("parameters") or {}).get("required_status_checks") or []]  # fmt: skip
        return {"read": True, "why": None, "checks": checks}
    except (urllib.error.URLError, KeyError, TimeoutError, OSError) as exc:
        return {"read": False, "why": f"{type(exc).__name__}: {exc}", "checks": None}


# --- agentkeel's deploys and the registry ----------------------------------------------------


def read_deploys(since: str | None) -> dict[str, Any]:
    """agentkeel's deploy.yml runs since the agent repository was created, and the jobs in each that name the agent.

    deploy.yml's `sign-agent` and `deploy-agent` are matrix jobs with no `name` of their own, so GitHub names each
    leg from the matrix row in its key order, `<job> (<repository>, <repository_id>, <commit>, <name>, <rollout>)`
    (`deployable` in scripts/platform_check.py at m08). A leg for this agent carries `label-impact` and the
    40-hex commit it deployed; both are found by content, not by position."""
    query = {"per_page": MAX_DEPLOY_RUNS, "exclude_pull_requests": "true"}
    if since:
        query["created"] = f">={since}"
    try:
        page = must(f"/repos/{PLATFORM_REPOSITORY}/actions/workflows/deploy.yml/runs?{urllib.parse.urlencode(query)}", "agentkeel's deploy runs")
    except (Unreadable, urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"read": False, "why": f"{type(exc).__name__}: {exc}", "since": since, "runs": None, "runs_total": None, "truncated": None, "naming_agent": []}
    runs_total = page.get("total_count")
    runs = []
    naming = []
    for run in page.get("workflow_runs") or []:
        status, jobs = gh(f"/repos/{PLATFORM_REPOSITORY}/actions/runs/{run['id']}/jobs?per_page=100")
        legs = []
        job_conclusions: dict[str, Any] = {}
        if status == 200:
            for job in (jobs or {}).get("jobs") or []:
                base = str(job.get("name", "")).split(" (")[0]
                job_conclusions.setdefault(base, job.get("conclusion"))
                if AGENT_NAME in str(job.get("name", "")):
                    sha = SHA.search(str(job.get("name", "")))
                    legs.append({"job": base, "name": job.get("name"), "conclusion": job.get("conclusion"), "commit": sha.group(0) if sha else None, "url": job.get("html_url")})
        entry = {"id": run["id"], "url": run.get("html_url"), "event": run.get("event"), "created_at": run.get("created_at"),
                 "status": run.get("status"), "conclusion": run.get("conclusion"), "head_sha": run.get("head_sha"),
                 "jobs_read": status == 200, "jobs": job_conclusions, "naming_agent": legs}  # fmt: skip
        runs.append(entry)
        naming += [{"run_id": run["id"], **leg} for leg in legs]
    return {"read": True, "why": None, "since": since, "runs_total": runs_total, "runs_read": len(runs),
            "truncated": bool(runs_total is not None and runs_total > len(runs)), "runs": runs, "naming_agent": naming, "read_at": now()}  # fmt: skip


def read_registry() -> dict[str, Any]:
    """The registry is DynamoDB table `agentkeel-registry` in agentkeel's agent account. This repository holds no
    credential for it (milestones/M01/README.md Unsure 3), so the row is unread. Unread never makes GREEN possible."""
    return {"read": False, "table": "agentkeel-registry", "row": None, "read_at": now(),
            "why": "no AWS credential in this repository; read through AWS or Grafana is ruled under Unsure (Security, Product)"}  # fmt: skip


# --- the verdict -----------------------------------------------------------------------------


MERGEABLE_REST = ("clean", "unstable", "has_hooks")  # the `mergeable_state` values GitHub merges from
MERGEABLE_GRAPHQL = ("CLEAN", "UNSTABLE", "HAS_HOOKS")  # the same, as `mergeStateStatus` spells them


def judge_mergeable(pull: dict[str, Any]) -> dict[str, Any]:
    """F1.1's "mergeable", read from one source and said which. GraphQL decides when it was read, else REST.

    Only a token's reading decides: with no token REST showed `unstable` on a head the ruleset blocked
    (construction run, M01 PR 2, Unsure 11), so a no-token reading is unread for F1.1's purpose."""
    graphql = pull["graphql"]
    if token()[0] is None:
        return {"read": False, "mergeable": None, "source": None, "value": pull["mergeable_state"],
                "why": "no token asked; REST's mergeable_state without a token does not account for the ruleset"}  # fmt: skip
    if graphql.get("read"):
        value = graphql.get("merge_state_status")
        return {"read": True, "mergeable": value in MERGEABLE_GRAPHQL, "source": "graphql", "value": value, "why": f"mergeStateStatus {value!r} with {token()[1]}"}
    value = pull["mergeable_state"]
    return {"read": True, "mergeable": value in MERGEABLE_REST, "source": "rest", "value": value,
            "why": f"mergeable_state {value!r} with {token()[1]}; GraphQL unread: {graphql.get('why')}"}  # fmt: skip


def judge(pull: dict[str, Any], seats: list[dict[str, Any]], checks: list[dict[str, Any]], deploys: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    unassigned = [s["seat"] for s in seats if not s["assigned"]]
    admin_unread = [s["seat"] for s in seats if s["assigned"] and not s["admin_read"]]
    platform_checks = [c for c in checks if c["name"] == PLATFORM_CHECK and c["app_id"] == PLATFORM_APP_ID]
    refused_seats = any(c["refused"] and any("seats" in r for r in c["refused"]) for c in platform_checks)
    mergeable = judge_mergeable(pull)
    found_mergeable = pull["merged"] or bool(mergeable["mergeable"])
    # agentkeel deploys main's head, which after the merge is the merge commit, not the branch head
    # (`deployable` in scripts/platform_check.py at m08 reads branch["commit"]["sha"]).
    merge_head = pull["merge_commit_sha"] if pull["merged"] else None
    deployed = [leg for leg in deploys.get("naming_agent") or [] if leg["job"] == "deploy-agent" and leg["conclusion"] == "success" and leg["commit"] == merge_head] if merge_head else []
    in_registry = bool(registry.get("read") and registry.get("row"))
    merge_words = f"mergeable_state {pull['mergeable_state']!r}, mergeStateStatus {pull['graphql'].get('merge_state_status') or 'unread'}"
    not_mergeable = f"not mergeable ({merge_words})" if mergeable["read"] else f"not read as mergeable ({mergeable['why']}; {merge_words})"

    if unassigned:
        seats_words = f"seat(s) {', '.join(unassigned)} are not a login that administers the repository"
        if found_mergeable:
            finding = "F1.1"
            reason = f"F1.1 holds: the pull request is {'merged' if pull['merged'] else 'mergeable (' + mergeable['why'] + ')'} while {seats_words}"
        elif refused_seats:
            finding = "control refused"
            reason = f"the claim 'seats filled' is false: {seats_words}; the pull request is {not_mergeable} and the platform check refused the head naming the seats"
        else:
            finding = "unassigned, no refusal read"
            reason = f"the claim 'seats filled' is false: {seats_words}; the pull request is {not_mergeable} and no platform check from the App refused the head for the seats"
        return {"verdict": "RED", "finding": finding, "reason": reason, "seats_unassigned": unassigned, "seats_admin_unread": admin_unread,
                "mergeable_judged": mergeable, "green_blocked_by": None}  # fmt: skip

    blocked = []
    if admin_unread:
        blocked.append(f"seat(s) {', '.join(admin_unread)}: permission unread, so 'administers the repository' is not shown")
    if not pull["merged"]:
        blocked.append(f"the pull request is not merged (state {pull['state']!r}, mergeable_state {pull['mergeable_state']!r})")
    if not deployed:
        blocked.append("no deploy-agent job of agentkeel's deploy.yml naming label-impact at the merge commit concluded success"
                       + ("" if deploys.get("read") else " (deploy runs unread)"))
    if not in_registry:
        blocked.append("the registry row for label-impact is unread" if not registry.get("read") else "the registry does not hold label-impact")
    if blocked:
        return {"verdict": "PENDING", "finding": None, "reason": "no seat is read as unassigned, and GREEN is not shown: " + "; ".join(blocked),
                "seats_unassigned": [], "seats_admin_unread": admin_unread, "mergeable_judged": mergeable, "green_blocked_by": blocked}  # fmt: skip
    return {"verdict": "GREEN", "finding": None, "reason": "every seat is a login read as admin, the pull request is merged, its deploy succeeded and the registry holds label-impact",
            "seats_unassigned": [], "seats_admin_unread": [], "mergeable_judged": mergeable, "green_blocked_by": []}  # fmt: skip


def summary_markdown(result: dict[str, Any]) -> str:
    lines = [f"## M01 reader: {result['verdict']}", "", result["reason"] + ".", "",
             f"Commit `{result.get('commit') or 'unknown'}`" + (" (dirty tree)" if result.get("dirty") else "")
             + f", written by CI: `{result['written_by_ci']}`, token: `{result.get('token')}`.", ""]  # fmt: skip
    if result["verdict"] == "UNSCORABLE":
        err = result["error"]
        lines += [f"`{err['type']}: {err['message']}`", "", "UNSCORABLE is not a verdict on ledger row 1. It is never RED and never GREEN."]
        return "\n".join(lines) + "\n"
    pull = result["pull_request"]
    lines += ["| reading | value |", "|---|---|",
              f"| pull request | [{pull['repository']}#{pull['number']}]({pull['url']}) at `{pull['head_sha'][:7]}`, state `{pull['state']}`, merged `{pull['merged']}`, mergeable_state `{pull['mergeable_state']}`, mergeStateStatus `{pull['graphql'].get('merge_state_status') or 'unread'}` |"]  # fmt: skip
    for s in result["seats"]:
        lines.append(f"| seat `{s['seat']}` | `{s['login']!r}`: {'assigned' if s['assigned'] else 'unassigned'}; admin {('yes' if s['admin'] else 'no') if s['admin_read'] and s['assigned'] else ('unread' if s['assigned'] else 'n/a')}; {s['why']} |")
    for c in result["control"]["check_runs"]:
        lines.append(f"| check `{c['name']}` | app {c['app_id']} (`{c['app_slug']}`), conclusion `{c['conclusion']}`, title `{c['output']['title']}`, refused {c['refused']} |")
    rc = result["control"]["required_checks"]
    lines.append(f"| required checks | {rc['checks'] if rc['read'] else 'unread: ' + str(rc['why'])} |")
    d = result["deploys"]
    lines.append(f"| agentkeel deploy runs | {('%s read since %s, %s naming label-impact%s' % (d['runs_read'], d['since'], len(d['naming_agent']), ', truncated' if d['truncated'] else '')) if d['read'] else 'unread: ' + str(d['why'])} |")
    r = result["registry"]
    lines.append(f"| registry | {'row ' + json.dumps(r['row']) if r['read'] else 'unread: ' + str(r['why'])} |")
    lines += ["", "The verdict judges ledger row 1 only, as `milestones/M01/README.md` \"Carried to PR 2\" defines it. Unread is recorded, never read as a pass."]
    return "\n".join(lines) + "\n"


# --- provenance, writing, main ------------------------------------------------------------


def ci_context() -> dict[str, Any] | None:
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return None
    server, repo, run_id = (os.environ.get(k) for k in ("GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_RUN_ID"))
    return {"run_url": f"{server}/{repo}/actions/runs/{run_id}" if server and repo and run_id else None, "run_id": run_id,
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"), "workflow": os.environ.get("GITHUB_WORKFLOW"), "job": os.environ.get("GITHUB_JOB"),
            "event": os.environ.get("GITHUB_EVENT_NAME"), "ref": os.environ.get("GITHUB_REF"), "sha": os.environ.get("GITHUB_SHA")}  # fmt: skip


def provenance() -> dict[str, Any]:
    ci = ci_context()
    try:
        commit: str | None = git("rev-parse", "HEAD")
        dirty: bool | None = bool(git("status", "--porcelain"))
    except Exception:  # noqa: BLE001  the commit is still recorded from CI's environment when git cannot answer
        commit, dirty = (ci or {}).get("sha"), None
    return {
        "what": "M01 reader: label-impact's first pull request at its head, agentkeel's deploys and the registry; the verdict is ledger row 1's",
        "milestone": "M01", "ledger_row": 1,
        "falsifier": "F1.1 label-impact's first pull request is mergeable, or is merged and deployed, while one of its seven seats is not a login that administers the repository",
        "read_at": now(), "commit": commit, "dirty": dirty, "written_by_ci": ci is not None, "ci": ci, "token": token()[1],
    }  # fmt: skip


def write_result(args: argparse.Namespace, result: dict[str, Any]) -> None:
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    text = summary_markdown(result)
    print(text)
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        with args.summary.open("a", encoding="utf-8") as fh:
            fh.write(text)


EXIT = {"GREEN": 0, "RED": 1, "UNSCORABLE": 2, "PENDING": 3}


def run(args: argparse.Namespace) -> int:
    pull = read_pull_request()
    owner = read_owner()
    head = pull["head_sha"]
    manifest = read_seats(head)
    seats = judge_seats(manifest["seats"], owner)
    checks = read_check_runs(head)
    required = read_required_checks()
    deploys = read_deploys(owner.get("created_at"))
    registry = read_registry()
    verdict = judge(pull, seats, checks, deploys, registry)
    result = {
        **provenance(), **verdict,
        "pull_request": pull, "repository": owner, "manifest": manifest["manifest"], "seats": seats,
        "control": {"platform_app_id": PLATFORM_APP_ID, "check_runs": checks, "required_checks": required},
        "deploys": deploys, "registry": registry,
    }  # fmt: skip
    write_result(args, result)
    return EXIT[result["verdict"]]


def unscorable(args: argparse.Namespace, exc: BaseException) -> int:
    refused = isinstance(exc, Unreadable)
    result = {**provenance(), "verdict": "UNSCORABLE", "finding": None,
              "reason": "a reading the verdict needs could not be made, so row 1 is not judged: " + ("unread" if refused else "the reader raised"),
              "error": {"type": type(exc).__name__, "message": str(exc), "traceback": None if refused else traceback.format_exc()}}  # fmt: skip
    print(f"UNSCORABLE: {type(exc).__name__}: {exc}", file=sys.stderr)
    if not refused:
        traceback.print_exc()
    try:
        write_result(args, result)
    except Exception as write_exc:  # noqa: BLE001  the exit code stays 2 even when the result cannot be written
        print(f"UNSCORABLE: could not write {args.out}: {write_exc!r}", file=sys.stderr)
    return EXIT["UNSCORABLE"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, type=Path, help="where to write the result JSON")
    parser.add_argument("--summary", type=Path, help="append a Markdown summary here (GITHUB_STEP_SUMMARY in CI)")
    args = parser.parse_args()
    try:
        return run(args)
    except Exception as exc:  # noqa: BLE001  every failure to read is UNSCORABLE, written and exit 2; never the RED code
        return unscorable(args, exc)


if __name__ == "__main__":
    raise SystemExit(main())
