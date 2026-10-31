"""The M03 gate: read what the public API serves and the detail page shows, ask the deployed agent through its door, judge F3.1.

Reads `pages/api/answers.json`, the public API's served answers, and the
`<script type="application/json" id="answer">` block of
`pages/detail.html`, the detail page's answer. Then, in order:

1. `answers_uncalled`: every served answer whose `call` is null, is not an
   object, lacks a field of the call record (`CALL_RECORD`), or whose
   `subject` is not `pharmadelta`. A read of the served file alone; no
   door is needed, so the plant reads RED whatever the door's state that
   day (M03 Unsure 4).
2. `answers_disagreed`: every page answer whose `id` the API does not
   serve, or that is not equal to the API's entry of that `id` as parsed
   JSON (canonical form: sorted keys, no whitespace).
3. The sign-in: Cognito `InitiateAuth`, `AuthFlow` `USER_PASSWORD_AUTH`,
   on the agent's identity pool with its callers client, `USERNAME`
   `pharmadelta`, `PASSWORD` the repository secret. No AWS credential, no
   client secret. The access token is held for the run and written
   nowhere; the result records that a token was issued and its
   `username` and `token_use` claims, nothing else of it.
4. The door: for every served answer, called or not, `POST` its question
   on the door's URL with `Authorization: Bearer <access token>` and the
   body `{"question": "..."}`, as agentkeel's `src/agent/run.py`
   `invoke_through_door` does. The body back is the runtime's
   observation; `parsed` holds `table_row`, `clause_id` and the answer
   fields when the model answered with a JSON object, else null. The
   reading is recorded beside the result under `door` (HTTP status, the
   request id the door returns in its response header, `stop_reason`,
   `parsed`, `text`, `error`, `latency_ms`, `guardrail_topics`, the tool
   calls made, `usage`), so the Measured cell carries what the agent said
   on the day. The URL, the pool id, the client id and the password are
   read from the environment and never written.
5. `answers_differing`: every served answer that carries a call record
   and whose `table_row`, `clause_id` or `answer_fields` is not what the
   door's `parsed` holds on this run (M03 Unsure 5: the run's own call).
   A served answer of null equals a `parsed` of null.

The verdict is ledger row 4's F3.1 and nothing else:

  RED         `answers_uncalled`, `answers_disagreed` or `answers_differing` is non-empty.
  GREEN       every served answer carries a call record as `pharmadelta`, every page answer is an
              API entry, and every served answer equals the door's answer on this run.
  UNSCORABLE  nothing is RED and: a served file could not be read or parsed, the API serves no
              answer, the environment lacks the secret or a variable, the sign-in failed, or the
              door answered anything but 200 for a called answer. Never RED, never GREEN.

Hosts: the sign-in goes to `cognito-idp.us-west-2.amazonaws.com` and the
call to the door's URL, which must be https on a host under
`execute-api.us-west-2.amazonaws.com` whose path ends `/invocations`;
anything else is refused before a request is made. Never SigV4, never the
runtime's ARN, never the door client's secret.

    uv run python -m src.m03.gate --out-dir <dir> [--summary <md>]

Writes `<dir>/result.json`. Exit 0 GREEN, 1 RED, 2 UNSCORABLE. The result
is evidence only when CI wrote it (P4), and it says whether it did.
"""

from __future__ import annotations

import argparse
import base64
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

ROOT = Path(__file__).resolve().parents[2]
REGION = "us-west-2"
SUBJECT = "pharmadelta"
AGENT = "label-impact"
COGNITO_HOST = f"cognito-idp.{REGION}.amazonaws.com"
DOOR_HOST_SUFFIX = f".execute-api.{REGION}.amazonaws.com"
# The call record's fields on a served answer (M03 README "Carried to PR 2"; fixed here, Unsure 10). The lift writes them.
CALL_RECORD = ("subject", "issuer", "door_host", "request_id", "called_at", "agent", "agent_commit", "run_url")
ANSWER_FIELDS = ("impacted", "owed", "escalate")
# The header the door returns its request id in: an HTTP API's `apigw-requestid`. Candidates are read in this order
# and the one found is recorded, so the CI run confirms the name (Unsure, PR 2).
REQUEST_ID_HEADERS = ("apigw-requestid", "x-amzn-requestid", "x-amz-apigw-id", "x-amzn-trace-id")
ENV = {
    "password": "M03_DOOR_PASSWORD",
    "url": "M03_DOOR_URL",
    "pool_id": "M03_DOOR_POOL_ID",
    "client_id": "M03_DOOR_CALLERS_CLIENT_ID",
}
FALSIFIER = (
    "F3.1 an answer the public API serves, or the detail page shows, was not produced by a call to the deployed "
    "agent through its door as the caller pharmadelta: it carries no call record, or its table_row, clause_id or "
    "answer_fields differ from what the agent answered on that call; or the page shows an answer the API does not serve"
)
PAGE_BLOCK = re.compile(r'<script\s+type="application/json"\s+id="answer"\s*>(.*?)</script>', re.DOTALL)


class Unscorable(Exception):
    """The inputs do not let F3.1 be judged. Not a verdict."""


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
        "what": "M03 gate: what the public API serves and the detail page shows, read and compared with what the deployed agent answers through its door as pharmadelta; the verdict is ledger row 4's F3.1",
        "milestone": "M03",
        "ledger_row": 4,
        "falsifier": FALSIFIER,
        "run_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": commit,
        "dirty": dirty,
        "written_by_ci": ci is not None,
        "ci": ci,
        "agent": AGENT,
        "subject": SUBJECT,
        "region": REGION,
        "call_record_fields": list(CALL_RECORD),
        "fields_compared": ["table_row", "clause_id", *(f"answer_fields.{f}" for f in ANSWER_FIELDS)],
        "env_set": {name: bool(os.environ.get(var)) for name, var in ENV.items()},
        "env_note": "which of the secret and the three variables the environment held; their values are never written",
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


def read_page(path: Path) -> list[dict]:
    """The page's answers: the JSON in its `id="answer"` block, one object or a list of them."""
    try:
        html = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise Unscorable(f"{rel(path)} could not be read: {exc}") from exc
    blocks = PAGE_BLOCK.findall(html)
    if not blocks:
        raise Unscorable(f'{rel(path)} has no <script type="application/json" id="answer"> block')
    shown: list[dict] = []
    for block in blocks:
        try:
            obj = json.loads(block)
        except ValueError as exc:
            raise Unscorable(f"{rel(path)}: the answer block is not JSON: {exc}") from exc
        items = obj if isinstance(obj, list) else [obj]
        if not all(isinstance(i, dict) and isinstance(i.get("id"), str) for i in items):
            raise Unscorable(f"{rel(path)}: the answer block is not an object, or a list of objects, with an `id`")
        shown.extend(items)
    return shown


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def call_record_check(entry: dict) -> dict:
    call = entry.get("call")
    if call is None:
        return {"has_record": False, "why": "call is null"}
    if not isinstance(call, dict):
        return {"has_record": False, "why": f"call is a {type(call).__name__}, not an object"}
    missing = [f for f in CALL_RECORD if f not in call or call[f] in (None, "")]
    if missing:
        return {"has_record": False, "why": f"call lacks {missing}", "missing": missing}
    if call.get("subject") != SUBJECT:
        return {"has_record": False, "why": f"call.subject is {call.get('subject')!r}, not {SUBJECT!r}"}
    return {"has_record": True, "why": "a call record as pharmadelta, every field present"}


def uncalled(served: list[dict]) -> tuple[list[str], dict[str, dict]]:
    checks = {a["id"]: call_record_check(a) for a in served}
    return [i for i, c in checks.items() if not c["has_record"]], checks


def disagreed(served: list[dict], shown: list[dict]) -> tuple[list[str], list[dict]]:
    by_id = {a["id"]: a for a in served}
    entries = []
    for page in shown:
        api = by_id.get(page["id"])
        if api is None:
            entries.append({"id": page["id"], "equal": False, "why": "the API serves no answer with this id"})
        elif canonical(api) != canonical(page):
            keys = sorted(k for k in set(api) | set(page) if canonical(api.get(k)) != canonical(page.get(k)))
            entries.append({"id": page["id"], "equal": False, "why": f"differs from the API's entry on {keys}", "keys": keys})
        else:
            entries.append({"id": page["id"], "equal": True, "why": "equal to the API's entry as parsed JSON"})
    return [e["id"] for e in entries if not e["equal"]], entries


# ---------------------------------------------------------------- the door
def check_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https":
        raise Unscorable("the door URL is not https")
    if not (parts.hostname or "").endswith(DOOR_HOST_SUFFIX):
        raise Unscorable(f"the door URL's host is not under {DOOR_HOST_SUFFIX}")
    if not parts.path.endswith("/invocations"):
        raise Unscorable("the door URL's path does not end /invocations")
    return url


def jwt_claims(token: str) -> dict:
    """The payload of a JWT, unverified: the door verifies the token, this reads two claims to record."""
    try:
        payload = token.split(".")[1]
        return json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    except Exception:  # noqa: BLE001  a token that does not read as a JWT is still sent; the door decides
        return {}


def sign_in(pool_id: str, client_id: str, password: str) -> tuple[str | None, dict]:
    """Cognito InitiateAuth with USER_PASSWORD_AUTH on the callers client. Returns the access token (never written) and the record."""
    body = json.dumps({
        "AuthFlow": "USER_PASSWORD_AUTH",
        "ClientId": client_id,
        "AuthParameters": {"USERNAME": SUBJECT, "PASSWORD": password},
    }).encode("utf-8")
    request = urllib.request.Request(
        f"https://{COGNITO_HOST}/", data=body, method="POST",
        headers={
            "Content-Type": "application/x-amz-json-1.1",
            "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
        },
    )
    record: dict[str, Any] = {"flow": "USER_PASSWORD_AUTH", "username": SUBJECT, "host": COGNITO_HOST, "pool_id_prefix": pool_id.split("_")[0]}
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            answer = json.loads(response.read())
            record["status"] = response.status
    except urllib.error.HTTPError as exc:
        err = {}
        try:
            err = json.loads(exc.read())
        except Exception:  # noqa: BLE001  the error body is Cognito's; its type is recorded when it reads
            pass
        record.update(signed_in=False, status=exc.code, error=err.get("__type"), message=str(err.get("message", ""))[:200])
        return None, record
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        record.update(signed_in=False, status=None, error=type(exc).__name__, message=str(exc)[:200])
        return None, record
    finally:
        record["latency_ms"] = round((time.perf_counter() - started) * 1000)
    if "ChallengeName" in answer:
        record.update(signed_in=False, error="challenge", challenge=answer["ChallengeName"], message="the pool asked for a challenge instead of issuing a token")
        return None, record
    token = (answer.get("AuthenticationResult") or {}).get("AccessToken")
    if not token:
        record.update(signed_in=False, error="no access token", message=f"keys answered: {sorted(answer)}")
        return None, record
    claims = jwt_claims(token)
    record.update(signed_in=True, token_use=claims.get("token_use"), token_username=claims.get("username"),
                  expires_in=(answer.get("AuthenticationResult") or {}).get("ExpiresIn"))  # fmt: skip
    return token, record


def ask_door(url: str, token: str, question: str) -> dict:
    """One call through the door, as `invoke_through_door` makes it. Returns the reading; the token is sent and never written."""
    request = urllib.request.Request(
        url, data=json.dumps({"question": question}).encode("utf-8"), method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    reading: dict[str, Any] = {"asked": True}
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            raw, status, headers = response.read(), response.status, response.headers
    except urllib.error.HTTPError as exc:
        raw, status, headers = exc.read(), exc.code, exc.headers
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        reading.update(status=None, error=f"{type(exc).__name__}: {exc}"[:300], parsed=None, stop_reason=None)
        reading["wall_ms"] = round((time.perf_counter() - started) * 1000)
        return reading
    reading["wall_ms"] = round((time.perf_counter() - started) * 1000)
    reading["status"] = status
    header = next((h for h in REQUEST_ID_HEADERS if headers.get(h)), None)
    reading["request_id_header"] = header
    reading["request_id"] = headers.get(header) if header else None
    reading["response_header_names"] = sorted({k.lower() for k in headers.keys()})
    try:
        body = json.loads(raw)
    except ValueError:
        reading.update(body_text=raw.decode("utf-8", errors="replace")[:500], parsed=None, stop_reason=None, error="the body is not JSON")
        return reading
    if not isinstance(body, dict):
        reading.update(body_text=str(body)[:500], parsed=None, stop_reason=None, error="the body is not a JSON object")
        return reading
    if status != 200:
        reading.update(body=body, parsed=None, stop_reason=None, error=f"the door answered {status}")
        return reading
    reading.update(
        parsed=body.get("parsed"),
        stop_reason=body.get("stop_reason"),
        text=body.get("text"),
        error=body.get("error"),
        refused=body.get("refused"),
        latency_ms=body.get("latency_ms"),
        guardrail_topics=body.get("guardrail_topics"),
        tool_calls=body.get("tool_calls"),
        usage=body.get("usage"),
        source=body.get("source"),
        body_keys=sorted(body),
    )
    return reading


def door_answer(parsed: Any) -> dict | None:
    """The door's `parsed` as the served `answer` is shaped: `table_row`, `clause_id`, `answer_fields`. None when nothing parsed."""
    if not isinstance(parsed, dict):
        return None
    fields = parsed.get("answer_fields") if isinstance(parsed.get("answer_fields"), dict) else parsed
    return {
        "table_row": parsed.get("table_row"),
        "clause_id": parsed.get("clause_id"),
        "answer_fields": {f: fields.get(f) for f in ANSWER_FIELDS},
    }


def compare(served_answer: Any, door_parsed: Any) -> dict:
    door = door_answer(door_parsed)
    if served_answer is None and door is None:
        return {"equal": True, "why": "the served answer is null and the door parsed no answer", "fields": {}}
    if served_answer is None or door is None:
        return {"equal": False, "why": "one side has an answer and the other has none", "fields": {}, "served": served_answer, "door": door}
    fields = {}
    for name in ("table_row", "clause_id"):
        s, d = served_answer.get(name), door.get(name)
        fields[name] = {"equal": s == d, "served": s, "door": d}
    for f in ANSWER_FIELDS:
        s, d = (served_answer.get("answer_fields") or {}).get(f), door["answer_fields"].get(f)
        fields[f"answer_fields.{f}"] = {"equal": s == d, "served": s, "door": d}
    unequal = [k for k, v in fields.items() if not v["equal"]]
    return {"equal": not unequal, "why": "all equal" if not unequal else f"differs on {unequal}", "fields": fields, "unequal": unequal}


# ------------------------------------------------------------------- gate
def judge(served: list[dict], uncalled_ids: list[str], disagreed_ids: list[str], differing_ids: list[str], unreadable: list[str]) -> dict:
    if uncalled_ids or disagreed_ids or differing_ids:
        verdict, parts = "RED", []
        if uncalled_ids:
            parts.append(f"served answers {', '.join(uncalled_ids)} carry no call record")
        if disagreed_ids:
            parts.append(f"page answers {', '.join(disagreed_ids)} are not what the API serves")
        if differing_ids:
            parts.append(f"served answers {', '.join(differing_ids)} differ from the door's answer")
        reason = "F3.1 holds: " + "; ".join(parts)
    elif unreadable:
        verdict = "UNSCORABLE"
        reason = "nothing is RED and a reading F3.1 needs could not be made: " + "; ".join(unreadable)
    else:
        verdict = "GREEN"
        reason = "F3.1 does not hold: every served answer carries a call record as pharmadelta, every page answer is an API entry, and every served answer equals the door's answer on this run"
    return {
        "verdict": verdict,
        "reason": reason,
        "answers_uncalled": uncalled_ids,
        "answers_disagreed": disagreed_ids,
        "answers_differing": differing_ids,
        "unreadable": unreadable,
        "counts": {"served": len(served), "uncalled": len(uncalled_ids), "disagreed": len(disagreed_ids), "differing": len(differing_ids)},
    }


def summary_markdown(result: dict) -> str:
    lines = [f"## M03 gate: {result['verdict']}", "", result["reason"] + ".", ""]
    lines.append(f"Commit `{result.get('commit') or 'unknown'}`" + (" (dirty tree)" if result.get("dirty") else "") + f", written by CI: `{result['written_by_ci']}`.")
    lines.append("")
    if "error" in result:
        lines += [f"`{result['error']['type']}: {result['error']['message']}`", ""]
    if result.get("sign_in"):
        s = result["sign_in"]
        lines += [f"Sign-in as `{s.get('username')}`: signed in `{s.get('signed_in')}`" + (f", status `{s.get('status')}`" if s.get("status") is not None else "") + (f", `{s.get('error')}`" if s.get("error") else "") + ".", ""]
    if result.get("served"):
        lines += ["| served | call record | page equal | door status | request id header | stop_reason | parsed | compared |", "|---|---|---|---|---|---|---|---|"]
        for e in result["served"]:
            d = e.get("door") or {}
            parsed = d.get("parsed")
            parsed_s = "null" if parsed is None else ("object" if isinstance(parsed, dict) else type(parsed).__name__)
            cmp = e.get("comparison")
            cmp_s = "not compared (uncalled)" if cmp is None else ("equal" if cmp["equal"] else cmp["why"])
            page = e.get("page_equal")
            lines.append(f"| {e['id']} | {'yes' if e['call_record']['has_record'] else 'no: ' + e['call_record']['why']} | {'not shown' if page is None else ('yes' if page else 'no')} | {d.get('status') if d.get('asked') else 'not asked'} | {d.get('request_id_header') or 'none'} | {d.get('stop_reason') or ''} | {parsed_s} | {cmp_s} |")
        lines.append("")
    if result.get("unreadable"):
        lines += ["Not read:", ""] + [f"- {u}" for u in result["unreadable"]] + [""]
    if result["verdict"] == "UNSCORABLE":
        lines.append("UNSCORABLE is not a verdict on ledger row 4's F3.1. It is never RED and never GREEN.")
    else:
        lines.append("The verdict judges ledger row 4's F3.1 only. The door's reading on an uncalled answer is recorded and decides nothing.")
    return "\n".join(lines) + "\n"


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
    unreadable: list[str] = []
    served = read_served(args.api)
    try:
        shown: list[dict] | None = read_page(args.page)
    except Unscorable as exc:
        shown, unreadable = None, [str(exc)]
    uncalled_ids, checks = uncalled(served)
    disagreed_ids, page_entries = disagreed(served, shown) if shown is not None else ([], [])
    page_equal = {e["id"]: e["equal"] for e in page_entries}

    env = {name: os.environ.get(var) or None for name, var in ENV.items()}
    missing = [ENV[name] for name, value in env.items() if not value]
    token, sign_in_record = None, {"username": SUBJECT, "signed_in": False, "error": "not attempted", "message": f"the environment lacks {missing}"}
    if not missing:
        try:
            check_url(env["url"])
        except Unscorable as exc:
            sign_in_record = {"username": SUBJECT, "signed_in": False, "error": "door URL refused", "message": str(exc)}
            unreadable.append(f"the door: {exc}")
        else:
            token, sign_in_record = sign_in(env["pool_id"], env["client_id"], env["password"])
            if token is None:
                unreadable.append(f"the sign-in failed: {sign_in_record.get('error')} ({sign_in_record.get('message')})")
    else:
        unreadable.append(f"the environment lacks {missing}: no sign-in, no call")

    entries, differing_ids = [], []
    for a in served:
        entry: dict[str, Any] = {"id": a["id"], "call_record": checks[a["id"]], "page_equal": page_equal.get(a["id"]), "served_answer": a.get("answer")}
        if token is not None and isinstance(a.get("question"), str):
            entry["door"] = ask_door(env["url"], token, a["question"])
        else:
            entry["door"] = {"asked": False, "why": "no token" if token is None else "the served answer has no question string"}
        door = entry["door"]
        if checks[a["id"]]["has_record"]:
            if door.get("asked") and door.get("status") == 200 and not door.get("error") and not door.get("refused"):
                entry["comparison"] = compare(a.get("answer"), door.get("parsed"))
                if not entry["comparison"]["equal"]:
                    differing_ids.append(a["id"])
            else:
                entry["comparison"] = None
                unreadable.append(f"{a['id']}: a called answer that was not compared: " + (f"the door answered {door.get('status')} ({door.get('error') or door.get('refused')})" if door.get("asked") else f"not asked ({door.get('why')})"))
        else:
            entry["comparison"] = None
        entries.append(entry)

    result = {
        **provenance(),
        **judge(served, uncalled_ids, disagreed_ids, differing_ids, unreadable),
        "sign_in": sign_in_record,
        "served": entries,
        "page": {"read": shown is not None, "answers_shown": [p["id"] for p in shown] if shown else [], "entries": page_entries},
        "door": [{"id": e["id"], **e["door"]} for e in entries],
    }
    write_result(args, result)
    return {"GREEN": 0, "RED": 1}.get(result["verdict"], 2)


def unscorable(args: argparse.Namespace, exc: BaseException) -> int:
    refused = isinstance(exc, Unscorable)
    result = {
        **provenance(),
        "verdict": "UNSCORABLE",
        "reason": "F3.1 is not judged: " + ("the gate refused the inputs" if refused else "the gate raised"),
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
    parser.add_argument("--api", type=Path, default=ROOT / "pages" / "api" / "answers.json")
    parser.add_argument("--page", type=Path, default=ROOT / "pages" / "detail.html")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    try:
        return run(args)
    except Exception as exc:  # noqa: BLE001  every failure to judge is UNSCORABLE, written and exit 2; never the RED code
        return unscorable(args, exc)


if __name__ == "__main__":
    raise SystemExit(main())
