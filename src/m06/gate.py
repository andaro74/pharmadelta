"""The M06 gate: read what the sign-off page serves and shows, read the signing commit and the package back from GitHub, judge F6.1.

Reads `pages/api/sign-off.json`, the reviewer sign-offs pharmadelta serves,
and the `<script type="application/json" id="signoff-<id>">` blocks of
`pages/sign-off.html`, the sign-offs the page shows. Then, in order:

1. `signoffs_unsigned`: every served sign-off shown as signed (`signed`
   true) whose `signature` is null, is not an object, lacks a field of the
   signature record (`SIGNATURE_RECORD`) or holds it empty, or whose `over`
   is not a SHA-256; or whose `package` is null, is not an object, lacks a
   field of the package record (`PACKAGE_RECORD`, `BUILT_BY`, each entry
   `ENTRY_RECORD`) or holds it empty, whose `sha256` is not a SHA-256,
   whose `written_by_ci` is not true, or whose `file` is not a file under
   `pages/` in the checkout. A read of the served file alone; no network is
   needed, so the plant reads RED whatever GitHub's API says that day (M03
   Unsure 4's rule).
2. `signoffs_disagreed`: every page sign-off whose `id` the served file
   does not serve, whose block is not named for its `id`, or that is not
   equal to the file's entry of that `id` as parsed JSON (canonical form:
   sorted keys, no whitespace).
3. The read-back, for each signed sign-off that carries both records, and
   for no other:
   a. the commit that last changed `pages/api/sign-off.json`, from the
      checkout (`git log -1 --format=%H -- <file>`; the checkout must not
      be shallow), then `GET /repos/<repo>/commits/<sha>` on GitHub's API
      for `author.login`, `commit.author.date` and `commit.verification`;
   b. `label-impact`'s `manifest.yaml` at the commit the reviewer record
      names (`GET /repos/agentkeel-studio/label-impact/contents/manifest.yaml?ref=<commit>`),
      for `seats.<seat>`;
   c. the package file's SHA-256, the zip's `manifest.json` against the
      record's `entries`, each entry's bytes against its own SHA-256 and
      against its source: the artifact of the CI run it names, downloaded
      in this run (`GET /repos/<repo>/actions/runs/<id>/artifacts`, then
      the archive), the repository at the commit it names (`git show`), or
      label-impact's repository at the commit it names (the contents API);
   d. the package file against the artifact of the run that built it
      (`package.built_by`).
4. `signoffs_differing`: every such sign-off where the commit's
   `author.login` is not the login the manifest holds for the seat, or not
   `reviewer.login`, or not `signature.by`; or the function shown is not
   the one SPEC/00 §5 maps to the seat; or the package file's SHA-256 is
   not `signature.over` or not `package.sha256`; or the file is not a zip,
   its `manifest.json` is not the record's `entries`, an entry is missing,
   hashes differently or differs from its source; or the file differs from
   what the run that built it wrote. A read that could not be made (the
   checkout shallow, the API refusing, an artifact expired or not
   downloadable, a commit not in the checkout) is recorded under
   `unreadable` and decides nothing (Unsure 7).

The verdict is ledger row 7's F6.1 and nothing else:

  RED         `signoffs_unsigned`, `signoffs_disagreed` or `signoffs_differing` is non-empty.
  GREEN       every sign-off shown as signed carries a signature record and a package record,
              the signing commit is the seat holder's own, the package hashes to what was signed
              and every entry equals its source, every page sign-off is the file's entry; nothing
              unread.
  UNSCORABLE  nothing is RED and: a served file could not be read or parsed, the file serves no
              sign-off, or a read-back F6.1 needs could not be made. Never RED, never GREEN.

RED comes first. Nothing that fails after the served file was read turns a
RED into UNSCORABLE (M05 PR 3's repair, built in from the start): every
network and git read is guarded, recorded by its status or its exception's
type, and never raised. GitHub's `verification` is recorded as read and not
required (Unsure 1, ruled at PR 2); commits on this repository are unsigned.

Hosts: GitHub's API (`GITHUB_API_URL`, else `https://api.github.com`) with
the workflow's `GITHUB_TOKEN`, sent as a bearer on the API host only; an
artifact's redirect to the blob store is fetched without it, and the
redirect's URL is written nowhere. No door, no pool, no secret of M03's.
The token is read from the environment and never written.

    uv run python -m src.m06.gate --out-dir <dir> [--summary <md>]

Writes `<dir>/result.json`. Exit 0 GREEN, 1 RED, 2 UNSCORABLE. The result
is evidence only when CI wrote it (P4), and it says whether it did.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import traceback
import urllib.error
import urllib.request
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
REPO = "andaro74/pharmadelta"
AGENT_REPO = "agentkeel-studio/label-impact"
AGENT_MANIFEST = "manifest.yaml"
SERVED_FILE = "pages/api/sign-off.json"
PAGES_DIR = "pages"
# SPEC/00 §5: the function shown on the pages beside each agentkeel seat. A sign-off whose function is not its seat's reads differing.
SEAT_FUNCTION = {
    "product": "Regulatory Affairs",
    "rule-owner": "Medical Affairs",
    "data-owner": "Labeling Operations",
    "tool-owner": "Platform Engineering",
    "threshold-owner": "Quality",
    "security": "Security",
    "engineering": "Engineering",
}
# The records' fields on a served sign-off (M06 README "Carried to PR 2"; fixed here, Unsure 5). The lift writes them.
SIGNATURE_RECORD = ("over", "by", "method", "read_from")
PACKAGE_RECORD = ("file", "sha256", "built_by", "commit", "entries", "written_by_ci")
BUILT_BY = ("run_url", "artifact")
ENTRY_RECORD = ("path", "sha256", "source", "run_url", "artifact", "name", "commit", "ledger_row")
ENTRY_SOURCES = ("artifact", "repository", "agent")
PACKAGE_MANIFEST = "manifest.json"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
RUN_URL = re.compile(r"^https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/actions/runs/([0-9]+)$")
ENV = {"token": "GITHUB_TOKEN"}
MAX_DOWNLOAD = 64 * 1024 * 1024
FALSIFIER = (
    "F6.1 a sign-off the sign-off page shows as signed was not a seat holder's over a downloadable evidence package, "
    "as this repository's CI can read back: it carries no signing record, or the commit that last changed the served "
    "file was not authored by the login that holds the seat shown in label-impact's manifest.yaml, or the function "
    "shown is not that seat's (SPEC/00 §5); or it carries no package record, or the package file it names is not in "
    "the repository, or that file's SHA-256 differs from the one the signature names, or an entry of the package is "
    "not the CI-written result the run and artifact it names wrote; or the page shows a sign-off the served file does "
    "not serve"
)
PAGE_BLOCK = re.compile(r'<script\s+type="application/json"\s+id="signoff-([^"]*)"\s*>(.*?)</script>', re.DOTALL)


class Unscorable(Exception):
    """The inputs do not let F6.1 be judged. Not a verdict."""


def rel(path: Path) -> str:
    """The path as the repository names it, or as given when it lies outside the repository."""
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def api_base() -> str:
    return (os.environ.get("GITHUB_API_URL") or "https://api.github.com").rstrip("/")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ------------------------------------------------------------- provenance
def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout


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
        "what": "M06 gate: what the sign-off page serves and shows, read for a signature record and a package record, and for each signed sign-off the signing commit, the seat's login in label-impact's manifest and the package read back from GitHub and compared; the verdict is ledger row 7's F6.1",
        "milestone": "M06",
        "ledger_row": 7,
        "falsifier": FALSIFIER,
        "run_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": commit,
        "dirty": dirty,
        "written_by_ci": ci is not None,
        "ci": ci,
        "repository": REPO,
        "agent_repository": AGENT_REPO,
        "served_file": SERVED_FILE,
        "api": api_base(),
        "seat_function": SEAT_FUNCTION,
        "signature_record_fields": list(SIGNATURE_RECORD),
        "package_record_fields": list(PACKAGE_RECORD),
        "built_by_fields": list(BUILT_BY),
        "entry_record_fields": list(ENTRY_RECORD),
        "signature_reading": {
            "commit_from": f"git log -1 --format=%H -- {SERVED_FILE}, on a checkout that is not shallow",
            "login_from": "GET /repos/<repo>/commits/<sha>: author.login, commit.author.date, commit.verification",
            "seat_from": f"GET /repos/{AGENT_REPO}/contents/{AGENT_MANIFEST}?ref=<reviewer.seat_read_from.commit>: seats.<seat>",
            "verified_required": False,
            "note": "verification is recorded as read and not required at M06 (Unsure 1); the gate defines no signature, it reads one",
        },
        "env_set": {name: bool(os.environ.get(var)) for name, var in ENV.items()},
        "env_note": "whether the environment held the workflow's token; its value is never written",
    }


# ---------------------------------------------------------------- reading
def read_served(path: Path) -> list[dict]:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Unscorable(f"{rel(path)} could not be read as JSON: {exc}") from exc
    signoffs = doc.get("signoffs") if isinstance(doc, dict) else None
    if not isinstance(signoffs, list) or not all(isinstance(s, dict) and isinstance(s.get("id"), str) for s in signoffs):
        raise Unscorable(f"{rel(path)} does not hold a `signoffs` list of objects with an `id`")
    if not signoffs:
        raise Unscorable(f"{rel(path)} serves no sign-off; there is nothing to judge")
    ids = [s["id"] for s in signoffs]
    if len(set(ids)) != len(ids):
        raise Unscorable(f"{rel(path)} serves one id more than once: {ids}")
    return signoffs


def read_page(path: Path) -> list[dict]:
    """The page's sign-offs: the JSON in each `id="signoff-<id>"` block, one object each, with the block's own id beside it."""
    try:
        html = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise Unscorable(f"{rel(path)} could not be read: {exc}") from exc
    blocks = PAGE_BLOCK.findall(html)
    if not blocks:
        raise Unscorable(f'{rel(path)} has no <script type="application/json" id="signoff-<id>"> block')
    shown: list[dict] = []
    for block_id, block in blocks:
        try:
            obj = json.loads(block)
        except ValueError as exc:
            raise Unscorable(f"{rel(path)}: the block signoff-{block_id} is not JSON: {exc}") from exc
        if not isinstance(obj, dict) or not isinstance(obj.get("id"), str):
            raise Unscorable(f"{rel(path)}: the block signoff-{block_id} is not an object with an `id`")
        shown.append({"block_id": block_id, "entry": obj})
    return shown


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def missing_fields(record: dict, fields: tuple[str, ...]) -> list[str]:
    return [f for f in fields if f not in record or record[f] in (None, "")]


def signature_record_check(entry: dict) -> dict:
    """Whether the served `signature` is a signing record, and why not."""
    sig = entry.get("signature")
    if sig is None:
        return {"has_record": False, "why": "signature is null"}
    if not isinstance(sig, dict):
        return {"has_record": False, "why": f"signature is a {type(sig).__name__}, not an object"}
    missing = missing_fields(sig, SIGNATURE_RECORD)
    if missing:
        return {"has_record": False, "why": f"signature lacks {missing}", "missing": missing}
    if not isinstance(sig["over"], str) or not SHA256.match(sig["over"]):
        return {"has_record": False, "why": "signature.over is not a SHA-256 (64 hex digits)"}
    if not isinstance(sig["by"], str):
        return {"has_record": False, "why": f"signature.by is a {type(sig['by']).__name__}, not a login"}
    return {"has_record": True, "why": "a signing record naming the hash signed and the login expected, every field present"}


def package_file(entry: dict) -> Path | None:
    """The package file's path when the record names a file under `pages/` that is in the checkout, else None."""
    pkg = entry.get("package") if isinstance(entry.get("package"), dict) else {}
    name = pkg.get("file")
    if not isinstance(name, str) or not name:
        return None
    path = (ROOT / name).resolve()
    try:
        path.relative_to((ROOT / PAGES_DIR).resolve())
    except ValueError:
        return None
    return path if path.is_file() else None


def entry_record_check(i: int, e: Any) -> str | None:
    """Why the i-th package entry is not an entry record, or None."""
    if not isinstance(e, dict):
        return f"entries[{i}] is a {type(e).__name__}, not an object"
    for f in ENTRY_RECORD:
        if f not in e:
            return f"entries[{i}] lacks {f!r}"
    if not isinstance(e["path"], str) or not e["path"]:
        return f"entries[{i}].path is not a path"
    if not isinstance(e["sha256"], str) or not SHA256.match(e["sha256"]):
        return f"entries[{i}].sha256 is not a SHA-256"
    if e["source"] not in ENTRY_SOURCES:
        return f"entries[{i}].source is {e['source']!r}, not one of {list(ENTRY_SOURCES)}"
    if e["source"] == "artifact" and not (isinstance(e["run_url"], str) and RUN_URL.match(e["run_url"]) and isinstance(e["artifact"], str) and e["artifact"] and isinstance(e["name"], str) and e["name"]):
        return f"entries[{i}] names an artifact source without a run URL on github.com, an artifact name and a file name"
    if e["source"] in ("repository", "agent") and not (isinstance(e["commit"], str) and e["commit"] and isinstance(e["name"], str) and e["name"]):
        return f"entries[{i}] names a {e['source']} source without a commit and a path"
    return None


def package_record_check(entry: dict) -> dict:
    """Whether the served `package` is a package record naming a file in the repository, and why not."""
    pkg = entry.get("package")
    if pkg is None:
        return {"has_record": False, "why": "package is null"}
    if not isinstance(pkg, dict):
        return {"has_record": False, "why": f"package is a {type(pkg).__name__}, not an object"}
    missing = missing_fields(pkg, PACKAGE_RECORD)
    if missing:
        return {"has_record": False, "why": f"package lacks {missing}", "missing": missing}
    if not isinstance(pkg["sha256"], str) or not SHA256.match(pkg["sha256"]):
        return {"has_record": False, "why": "package.sha256 is not a SHA-256 (64 hex digits)"}
    if pkg.get("written_by_ci") is not True:
        return {"has_record": False, "why": f"package.written_by_ci is {pkg.get('written_by_ci')!r}, not true"}
    built = pkg["built_by"]
    if not isinstance(built, dict) or missing_fields(built, BUILT_BY):
        return {"has_record": False, "why": f"package.built_by is not an object with {list(BUILT_BY)}"}
    if not isinstance(built["run_url"], str) or not RUN_URL.match(built["run_url"]):
        return {"has_record": False, "why": "package.built_by.run_url is not a run URL on github.com"}
    if not isinstance(pkg["entries"], list) or not pkg["entries"]:
        return {"has_record": False, "why": "package.entries is not a non-empty list"}
    for i, e in enumerate(pkg["entries"]):
        why = entry_record_check(i, e)
        if why:
            return {"has_record": False, "why": why}
    if not isinstance(pkg["file"], str) or not pkg["file"]:
        return {"has_record": False, "why": "package.file is not a path"}
    if package_file(entry) is None:
        return {"has_record": False, "why": f"package.file {pkg['file']!r} is not a file under {PAGES_DIR}/ in the checkout"}
    return {"has_record": True, "why": f"a package record naming {pkg['file']!r}, in the checkout, with {len(pkg['entries'])} entries, every field present"}


def unsigned(served: list[dict]) -> tuple[list[str], dict[str, dict]]:
    """Every served sign-off shown as signed that has no signing record or no package record naming a file in the repository."""
    checks: dict[str, dict] = {}
    for s in served:
        shown_signed = s.get("signed") is True
        sig = signature_record_check(s)
        pkg = package_record_check(s)
        signed = sig["has_record"] and pkg["has_record"]
        checks[s["id"]] = {"shown_signed": shown_signed, "signature_record": sig, "package_record": pkg, "signed": signed}
    return [i for i, c in checks.items() if c["shown_signed"] and not c["signed"]], checks


def disagreed(served: list[dict], shown: list[dict]) -> tuple[list[str], list[dict]]:
    by_id = {s["id"]: s for s in served}
    entries = []
    for item in shown:
        page, block_id = item["entry"], item["block_id"]
        api = by_id.get(page["id"])
        if api is None:
            entries.append({"id": page["id"], "block": block_id, "equal": False, "why": "the file serves no sign-off with this id"})
        elif block_id != page["id"]:
            entries.append({"id": page["id"], "block": block_id, "equal": False, "why": f"shown in the block signoff-{block_id}, not signoff-{page['id']}"})
        elif canonical(api) != canonical(page):
            keys = sorted(k for k in set(api) | set(page) if canonical(api.get(k)) != canonical(page.get(k)))
            entries.append({"id": page["id"], "block": block_id, "equal": False, "why": f"differs from the file's entry on {keys}", "keys": keys})
        else:
            entries.append({"id": page["id"], "block": block_id, "equal": True, "why": "equal to the file's entry as parsed JSON"})
    return [e["id"] for e in entries if not e["equal"]], entries


# --------------------------------------------------------------- transport
class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Redirects are not followed by urllib here: the bearer token must not travel to the blob store (`http_get` fetches the target itself, without it)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, D102
        return None


def read_capped(resp: Any) -> bytes:
    data = resp.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        raise ValueError(f"the body is larger than {MAX_DOWNLOAD} bytes")
    return data


def http_get(url: str, token: str | None, accept: str = "application/vnd.github+json", follow: bool = True) -> dict:
    """One GET. Returns status, headers and body, or the exception's type; the token and any redirect URL are in no field."""
    headers = {"Accept": accept, "User-Agent": "pharmadelta-m06-gate", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(urllib.request.Request(url, headers=headers), timeout=60) as resp:
            return {"status": resp.status, "headers": dict(resp.headers), "body": read_capped(resp), "error": None, "redirected": False}
    except urllib.error.HTTPError as exc:
        location = exc.headers.get("Location") if exc.headers else None
        if exc.code in (301, 302, 303, 307, 308) and follow and location:
            got = http_get(location, token=None, accept="*/*", follow=False)
            got["redirected"] = True
            return got
        try:
            body = exc.read()
        except Exception:  # noqa: BLE001
            body = b""
        return {"status": exc.code, "headers": dict(exc.headers or {}), "body": body, "error": f"HTTP {exc.code}", "redirected": False}
    except Exception as exc:  # noqa: BLE001  URLError, timeout, ValueError on a capped body, http.client's own: the type and a short message, never the URL
        return {"status": None, "headers": {}, "body": b"", "error": f"{type(exc).__name__}: {str(exc)[:120]}", "redirected": False}


def api_json(path: str, token: str | None) -> dict:
    """GET an API path (relative to the API base) as JSON. `read` is false with `why` when it could not be."""
    url = f"{api_base()}{path}"
    got = http_get(url, token)
    out: dict[str, Any] = {"path": path, "status": got["status"], "read": False, "json": None}
    if got["error"] or got["status"] != 200:
        out["why"] = f"GET {path} answered {got['status']} ({got['error']})"
        return out
    try:
        out["json"] = json.loads(got["body"].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        out["why"] = f"GET {path} did not answer JSON: {type(exc).__name__}"
        return out
    out["read"] = True
    return out


# ---------------------------------------------------------------- read-back
def read_last_commit(served_file: str) -> dict:
    """The commit that last changed the served file, from a checkout that is not shallow."""
    try:
        if git("rev-parse", "--is-shallow-repository") == "true":
            return {"read": False, "why": "the checkout is shallow; the commit that last changed the served file cannot be known"}
        sha = git("log", "-1", "--format=%H", "--", served_file)
    except Exception as exc:  # noqa: BLE001  git absent, not a repository, the path unknown
        return {"read": False, "why": f"git could not answer: {type(exc).__name__}"}
    if not re.fullmatch(r"[0-9a-f]{40}", sha or ""):
        return {"read": False, "why": f"git log names no commit for {served_file}"}
    return {"read": True, "sha": sha, "read_from": f"git log -1 --format=%H -- {served_file}"}


def read_commit(repo: str, sha: str, token: str | None) -> dict:
    """GitHub's record of one commit: the author's login, the authored time, the verification."""
    got = api_json(f"/repos/{repo}/commits/{sha}", token)
    if not got["read"]:
        return {"read": False, "why": got["why"], "status": got["status"]}
    doc = got["json"]
    if not isinstance(doc, dict) or not isinstance(doc.get("commit"), dict):
        return {"read": False, "why": "the commit's record is not an object with `commit`", "status": got["status"]}
    author = doc.get("author") if isinstance(doc.get("author"), dict) else {}
    committer = doc.get("committer") if isinstance(doc.get("committer"), dict) else {}
    c = doc["commit"]
    ver = c.get("verification") if isinstance(c.get("verification"), dict) else {}
    return {
        "read": True,
        "status": got["status"],
        "read_from": got["path"],
        "sha": doc.get("sha"),
        "author_login": author.get("login"),
        "committer_login": committer.get("login"),
        "authored_at": (c.get("author") or {}).get("date") if isinstance(c.get("author"), dict) else None,
        "committed_at": (c.get("committer") or {}).get("date") if isinstance(c.get("committer"), dict) else None,
        "verified": ver.get("verified"),
        "verification_reason": ver.get("reason"),
        "parents": [p.get("sha") for p in doc.get("parents", []) if isinstance(p, dict)],
    }


def read_manifest_seat(agent_repo: str, commit: str, seat: str, token: str | None) -> dict:
    """`seats.<seat>` of label-impact's manifest at one commit."""
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{7,40}", commit):
        return {"read": False, "why": f"the reviewer record names no commit of the manifest to read ({commit!r})"}
    got = api_json(f"/repos/{agent_repo}/contents/{AGENT_MANIFEST}?ref={commit}", token)
    if not got["read"]:
        return {"read": False, "why": got["why"], "status": got["status"]}
    doc = got["json"]
    try:
        text = base64.b64decode(doc["content"]).decode("utf-8")
        manifest = yaml.safe_load(text)
    except Exception as exc:  # noqa: BLE001  not base64, not UTF-8, not YAML
        return {"read": False, "why": f"the manifest could not be decoded: {type(exc).__name__}", "status": got["status"]}
    seats = manifest.get("seats") if isinstance(manifest, dict) else None
    if not isinstance(seats, dict):
        return {"read": False, "why": "the manifest holds no `seats` mapping", "status": got["status"]}
    return {
        "read": True,
        "status": got["status"],
        "read_from": got["path"],
        "blob_sha": doc.get("sha"),
        "seat": seat,
        "login": seats.get(seat),
        "seats": {k: v for k, v in seats.items() if isinstance(k, str)},
    }


class Artifacts:
    """Artifacts of this repository's runs, downloaded once each in this run and read as zips."""

    def __init__(self, repo: str, token: str | None) -> None:
        self.repo, self.token = repo, token
        self.cache: dict[tuple[str, str], dict] = {}
        self.reads: list[dict] = []

    def get(self, run_url: str, name: str) -> dict:
        key = (run_url, name)
        if key not in self.cache:
            self.cache[key] = self._fetch(run_url, name)
            self.reads.append({k: v for k, v in self.cache[key].items() if k != "zip"})
        return self.cache[key]

    def _fetch(self, run_url: str, name: str) -> dict:
        m = RUN_URL.match(run_url or "")
        if not m:
            return {"read": False, "why": f"not a run URL on github.com: {run_url!r}", "run_url": run_url, "artifact": name}
        repo, run_id = m.group(1), m.group(2)
        if repo != self.repo:
            return {"read": False, "why": f"the run is {repo}'s, not {self.repo}'s", "run_url": run_url, "artifact": name}
        listing = api_json(f"/repos/{repo}/actions/runs/{run_id}/artifacts?per_page=100", self.token)
        base = {"run_url": run_url, "run_id": run_id, "artifact": name, "list_status": listing["status"]}
        if not listing["read"]:
            return {**base, "read": False, "why": listing["why"]}
        items = (listing["json"] or {}).get("artifacts") if isinstance(listing["json"], dict) else None
        found = next((a for a in items or [] if isinstance(a, dict) and a.get("name") == name), None)
        if found is None:
            return {**base, "read": False, "why": f"run {run_id} has no artifact named {name!r}", "artifacts_listed": [a.get("name") for a in items or [] if isinstance(a, dict)]}
        base.update({"artifact_id": found.get("id"), "expired": found.get("expired"), "expires_at": found.get("expires_at"), "size_in_bytes": found.get("size_in_bytes")})
        if found.get("expired"):
            return {**base, "read": False, "why": f"artifact {name!r} of run {run_id} expired at {found.get('expires_at')}"}
        got = http_get(f"{api_base()}/repos/{repo}/actions/artifacts/{found.get('id')}/zip", self.token)
        base["download_status"] = got["status"]
        if got["error"] or got["status"] != 200:
            return {**base, "read": False, "why": f"the archive of artifact {name!r} of run {run_id} answered {got['status']} ({got['error']})"}
        try:
            zf = zipfile.ZipFile(io.BytesIO(got["body"]))
            names = zf.namelist()
        except zipfile.BadZipFile:
            return {**base, "read": False, "why": f"the archive of artifact {name!r} of run {run_id} is not a zip"}
        return {**base, "read": True, "zip": zf, "files": names, "bytes": len(got["body"])}

    def file(self, run_url: str, name: str, member: str) -> dict:
        art = self.get(run_url, name)
        if not art["read"]:
            return {"read": False, "why": art["why"]}
        if member not in art["files"]:
            return {"read": True, "found": False, "why": f"artifact {name!r} holds no file {member!r} (it holds {art['files']})"}
        return {"read": True, "found": True, "bytes": art["zip"].read(member)}


def read_repository_file(commit: str, name: str) -> dict:
    """A file of this repository at one commit, from the checkout."""
    try:
        data = git_bytes("show", f"{commit}:{name}")
    except subprocess.CalledProcessError as exc:
        err = (exc.stderr or b"").decode("utf-8", "replace").strip()
        return {"read": False, "why": f"git show {commit}:{name} failed: {err[:160] or 'no message'}"}
    except Exception as exc:  # noqa: BLE001
        return {"read": False, "why": f"git could not answer: {type(exc).__name__}"}
    return {"read": True, "bytes": data}


def read_agent_file(agent_repo: str, commit: str, name: str, token: str | None) -> dict:
    """A file of label-impact's repository at one commit, from GitHub's contents API (the agent's repository is not in the checkout)."""
    if not re.fullmatch(r"[0-9a-f]{7,40}", commit or ""):
        return {"read": False, "why": f"the entry names no commit of the agent's repository ({commit!r})"}
    got = api_json(f"/repos/{agent_repo}/contents/{name}?ref={commit}", token)
    if not got["read"]:
        return {"read": False, "why": got["why"], "status": got["status"]}
    doc = got["json"]
    try:
        if doc.get("encoding") != "base64":
            raise ValueError(f"encoding {doc.get('encoding')!r}")
        data = base64.b64decode(doc["content"])
    except Exception as exc:  # noqa: BLE001  a directory, a file over 1 MB (no content), not base64
        return {"read": False, "why": f"{agent_repo} {name} at {commit}: no content to decode ({type(exc).__name__})", "status": got["status"]}
    return {"read": True, "bytes": data, "status": got["status"], "read_from": got["path"], "blob_sha": doc.get("sha")}


def read_back(entry: dict, artifacts: Artifacts, token: str | None) -> dict:
    """Everything F6.1 asks GitHub and the checkout about one signed sign-off; what differs and what could not be read."""
    sig, pkg, reviewer = entry["signature"], entry["package"], entry.get("reviewer") if isinstance(entry.get("reviewer"), dict) else {}
    seat, login, function = reviewer.get("seat"), reviewer.get("login"), reviewer.get("function")
    seat_from = reviewer.get("seat_read_from") if isinstance(reviewer.get("seat_read_from"), dict) else {}
    differences: list[str] = []
    not_read: list[str] = []
    out: dict[str, Any] = {}

    # The function shown is the seat's (SPEC/00 §5): a read of the record and the table, no network.
    expected_function = SEAT_FUNCTION.get(seat) if isinstance(seat, str) else None
    out["function"] = {"seat": seat, "shown": function, "expected": expected_function, "equal": expected_function is not None and function == expected_function}
    if expected_function is None:
        differences.append(f"the seat {seat!r} is not one of SPEC/00 §5's seven")
    elif function != expected_function:
        differences.append(f"the function shown {function!r} is not the seat's ({expected_function!r})")

    # The signing commit.
    last = read_last_commit(SERVED_FILE)
    out["last_commit"] = last
    if not last["read"]:
        not_read.append(last["why"])
        out["commit"] = {"read": False, "why": "no commit to read"}
    else:
        commit = read_commit(REPO, last["sha"], token)
        out["commit"] = commit
        if not commit["read"]:
            not_read.append(f"the signing commit {last['sha'][:7]}: {commit['why']}")
        else:
            if commit["author_login"] is None:
                differences.append(f"GitHub matched the author of {last['sha'][:7]} to no login")
            if commit["author_login"] != login:
                differences.append(f"the commit's author.login {commit['author_login']!r} is not reviewer.login {login!r}")
            if commit["author_login"] != sig["by"]:
                differences.append(f"the commit's author.login {commit['author_login']!r} is not signature.by {sig['by']!r}")

    # The seat in label-impact's manifest at the commit the reviewer record names.
    manifest = read_manifest_seat(AGENT_REPO, seat_from.get("commit"), seat, token) if isinstance(seat, str) else {"read": False, "why": "the reviewer record names no seat"}
    out["manifest"] = manifest
    if not manifest["read"]:
        not_read.append(f"label-impact's manifest at {seat_from.get('commit')!r}: {manifest['why']}")
    else:
        if manifest["login"] != login:
            differences.append(f"the manifest holds {manifest['login']!r} for the seat {seat!r}, not reviewer.login {login!r}")
        if out["commit"].get("read") and manifest["login"] != out["commit"]["author_login"]:
            differences.append(f"the commit's author.login {out['commit']['author_login']!r} is not the seat holder {manifest['login']!r}")

    # The package file, its hash, its zip, its entries.
    path = package_file(entry)
    data = path.read_bytes() if path else b""
    digest = sha256_hex(data)
    out["package_file"] = {"file": pkg["file"], "bytes": len(data), "sha256": digest, "signed_over": sig["over"], "recorded": pkg["sha256"]}
    if digest != sig["over"]:
        differences.append(f"the package file hashes to {digest[:12]}…, not what the signature names ({sig['over'][:12]}…)")
    if digest != pkg["sha256"]:
        differences.append(f"the package file hashes to {digest[:12]}…, not what its record says ({pkg['sha256'][:12]}…)")
    entries_out: list[dict] = []
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
        members = zf.namelist()
        out["package_zip"] = {"is_zip": True, "files": members}
    except zipfile.BadZipFile:
        zf, members = None, []
        out["package_zip"] = {"is_zip": False}
        differences.append("the package file is not a zip")
    if zf is not None:
        if PACKAGE_MANIFEST not in members:
            differences.append(f"the package holds no {PACKAGE_MANIFEST}")
            out["package_zip"]["manifest_equal"] = False
        else:
            try:
                listed = json.loads(zf.read(PACKAGE_MANIFEST).decode("utf-8"))
                equal = canonical(listed) == canonical(pkg["entries"])
            except (UnicodeDecodeError, ValueError):
                equal = False
            out["package_zip"]["manifest_equal"] = equal
            if not equal:
                differences.append(f"the package's {PACKAGE_MANIFEST} is not the record's entries")
        for e in pkg["entries"]:
            rec: dict[str, Any] = {"path": e["path"], "source": e["source"], "ledger_row": e["ledger_row"]}
            if e["path"] not in members:
                rec.update({"in_package": False, "equal": False, "why": "not in the package"})
                differences.append(f"entry {e['path']!r} is not in the package")
                entries_out.append(rec)
                continue
            got = zf.read(e["path"])
            rec.update({"in_package": True, "bytes": len(got), "sha256": sha256_hex(got), "sha256_equal": sha256_hex(got) == e["sha256"]})
            if not rec["sha256_equal"]:
                differences.append(f"entry {e['path']!r} hashes to {rec['sha256'][:12]}…, not {e['sha256'][:12]}…")
            if e["source"] == "artifact":
                src = artifacts.file(e["run_url"], e["artifact"], e["name"])
                rec["source_read"] = {k: v for k, v in src.items() if k != "bytes"}
                if not src["read"]:
                    rec["equal"] = None
                    not_read.append(f"entry {e['path']!r}: {src['why']}")
                elif not src["found"]:
                    rec["equal"] = False
                    differences.append(f"entry {e['path']!r}: {src['why']}")
                else:
                    rec["equal"] = src["bytes"] == got
                    if not rec["equal"]:
                        differences.append(f"entry {e['path']!r} is not the file {e['name']!r} of artifact {e['artifact']!r} of its run")
            else:
                src = read_repository_file(e["commit"], e["name"]) if e["source"] == "repository" else read_agent_file(AGENT_REPO, e["commit"], e["name"], token)
                rec["source_read"] = {k: v for k, v in src.items() if k != "bytes"}
                where = e["commit"] if e["source"] == "repository" else f"{AGENT_REPO} at {e['commit']}"
                if not src["read"]:
                    rec["equal"] = None
                    not_read.append(f"entry {e['path']!r}: {src['why']}")
                else:
                    rec["equal"] = src["bytes"] == got
                    if not rec["equal"]:
                        differences.append(f"entry {e['path']!r} is not {e['name']!r} at {where}")
            entries_out.append(rec)
    out["entries"] = entries_out

    # The package against the artifact of the run that built it.
    built = pkg["built_by"]
    member = Path(pkg["file"]).name
    src = artifacts.file(built["run_url"], built["artifact"], member)
    out["built_by"] = {"run_url": built["run_url"], "artifact": built["artifact"], "file": member, **{k: v for k, v in src.items() if k != "bytes"}}
    if not src["read"]:
        out["built_by"]["equal"] = None
        not_read.append(f"the package's build: {src['why']}")
    elif not src["found"]:
        out["built_by"]["equal"] = False
        differences.append(f"the package's build: {src['why']}")
    else:
        out["built_by"]["equal"] = src["bytes"] == data
        if not out["built_by"]["equal"]:
            differences.append(f"the package file is not the {member!r} that artifact {built['artifact']!r} of its run wrote")

    out["differences"], out["not_read"] = differences, not_read
    out["equal"] = None if (not differences and not_read) else not differences
    return out


# ------------------------------------------------------------------- gate
def judge(served: list[dict], unsigned_ids: list[str], disagreed_ids: list[str], differing_ids: list[str], unreadable: list[str]) -> dict:
    if unsigned_ids or disagreed_ids or differing_ids:
        verdict, parts = "RED", []
        if unsigned_ids:
            parts.append(f"sign-offs {', '.join(unsigned_ids)} are shown as signed with no signing record or no package record naming a file in the repository")
        if disagreed_ids:
            parts.append(f"page sign-offs {', '.join(disagreed_ids)} are not what the file serves")
        if differing_ids:
            parts.append(f"sign-offs {', '.join(differing_ids)} were not read back as the seat holder's own commit over the package it signed")
        reason = "F6.1 holds: " + "; ".join(parts)
    elif unreadable:
        verdict = "UNSCORABLE"
        reason = "nothing is RED and a reading F6.1 needs could not be made: " + "; ".join(unreadable)
    else:
        verdict = "GREEN"
        reason = "F6.1 does not hold: every sign-off shown as signed carries a signing record and a package record, the commit that last changed the served file is the seat holder's own, the function shown is the seat's, the package hashes to what was signed and every entry equals its source, and every page sign-off is the file's entry"
    return {
        "verdict": verdict,
        "reason": reason,
        "signoffs_unsigned": unsigned_ids,
        "signoffs_disagreed": disagreed_ids,
        "signoffs_differing": differing_ids,
        "unreadable": unreadable,
        "counts": {"served": len(served), "unsigned": len(unsigned_ids), "disagreed": len(disagreed_ids), "differing": len(differing_ids)},
    }


def summary_markdown(result: dict) -> str:
    lines = [f"## M06 gate: {result['verdict']}", "", result["reason"] + ".", ""]
    lines.append(f"Commit `{result.get('commit') or 'unknown'}`" + (" (dirty tree)" if result.get("dirty") else "") + f", written by CI: `{result['written_by_ci']}`.")
    lines.append("")
    if "error" in result:
        lines += [f"`{result['error']['type']}: {result['error']['message']}`", ""]
    if result.get("served"):
        page_read = (result.get("page") or {}).get("read", True)
        lines += ["| served | shown signed | signature record | package record | page equal | signing commit | author login | seat holder | package hash | entries | read back |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for e in result["served"]:
            rb = e.get("read_back") or {}
            page = e.get("page_equal")
            sig_s = "yes" if e["signature_record"]["has_record"] else "no: " + e["signature_record"]["why"]
            pkg_s = "yes" if e["package_record"]["has_record"] else "no: " + e["package_record"]["why"]
            page_s = "page not read" if not page_read else ("not shown" if page is None else ("yes" if page else "no"))
            if not rb:
                commit_s = login_s = holder_s = hash_s = entries_s = "not read"
                rb_s = f"not read back: {e.get('not_read_back')}"
            else:
                last, commit, manifest, pf = rb.get("last_commit") or {}, rb.get("commit") or {}, rb.get("manifest") or {}, rb.get("package_file") or {}
                commit_s = (last.get("sha") or "")[:7] if last.get("read") else "not read"
                login_s = (commit.get("author_login") or "none") if commit.get("read") else "not read"
                holder_s = (manifest.get("login") or "none") if manifest.get("read") else "not read"
                hash_s = "equal" if pf.get("sha256") == pf.get("signed_over") == pf.get("recorded") else "differs"
                ents = rb.get("entries") or []
                entries_s = f"{sum(1 for x in ents if x.get('equal') is True)} of {len(ents)} equal"
                rb_s = "equal" if rb.get("equal") else ("not fully read" if rb.get("equal") is None else "; ".join(rb.get("differences") or []))
            lines.append(f"| {e['id']} | {'yes' if e['shown_signed'] else 'no'} | {sig_s} | {pkg_s} | {page_s} | {commit_s} | {login_s} | {holder_s} | {hash_s} | {entries_s} | {rb_s} |")
        lines.append("")
    if result.get("unreadable"):
        lines += ["Not read:", ""] + [f"- {u}" for u in result["unreadable"]] + [""]
    if result["verdict"] == "UNSCORABLE":
        lines.append("UNSCORABLE is not a verdict on ledger row 7's F6.1. It is never RED and never GREEN.")
    else:
        lines.append("The verdict judges ledger row 7's F6.1 only. A sign-off shown as not signed is named by no list; GitHub's verification is recorded and not required (Unsure 1).")
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
    try:
        shown: list[dict] | None = read_page(args.page)
    except Unscorable as exc:
        shown, unreadable = None, [str(exc)]
    unsigned_ids, checks = unsigned(served)
    disagreed_ids, page_entries = disagreed(served, shown) if shown is not None else ([], [])
    page_equal = {e["id"]: e["equal"] for e in page_entries}

    token = os.environ.get(ENV["token"]) or None
    artifacts = Artifacts(REPO, token)
    entries, differing_ids = [], []
    for s in served:
        check = checks[s["id"]]
        entry: dict[str, Any] = {"id": s["id"], **check, "page_equal": page_equal.get(s["id"])}
        if not check["signed"]:
            entry["read_back"] = None
            entry["not_read_back"] = "no signing record" if not check["signature_record"]["has_record"] else "no package record naming a file in the repository"
        else:
            try:
                entry["read_back"] = read_back(s, artifacts, token)
            except Exception as exc:  # noqa: BLE001  a read-back that raises is a read-back not made; the lists stand (M05 PR 3's rule)
                entry["read_back"] = {"equal": None, "differences": [], "not_read": [f"the read-back raised {type(exc).__name__}: {str(exc)[:160]}"]}
            for why in entry["read_back"]["not_read"]:
                unreadable.append(f"{s['id']}: {why}")
            if entry["read_back"]["differences"]:
                differing_ids.append(s["id"])
        entries.append(entry)

    result = {
        **provenance(),
        **judge(served, unsigned_ids, disagreed_ids, differing_ids, unreadable),
        "served": entries,
        "page": {"read": shown is not None, "signoffs_shown": [p["entry"]["id"] for p in shown] if shown else [], "entries": page_entries},
        "artifacts_read": artifacts.reads,
    }
    write_result(args, result)
    return {"GREEN": 0, "RED": 1}.get(result["verdict"], 2)


def unscorable(args: argparse.Namespace, exc: BaseException) -> int:
    refused = isinstance(exc, Unscorable)
    result = {
        **provenance(),
        "verdict": "UNSCORABLE",
        "reason": "F6.1 is not judged: " + ("the gate refused the inputs" if refused else "the gate raised"),
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
    parser.add_argument("--api", type=Path, default=ROOT / "pages" / "api" / "sign-off.json")
    parser.add_argument("--page", type=Path, default=ROOT / "pages" / "sign-off.html")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    try:
        return run(args)
    except Exception as exc:  # noqa: BLE001  every failure to judge is UNSCORABLE, written and exit 2; never the RED code
        return unscorable(args, exc)


if __name__ == "__main__":
    raise SystemExit(main())
