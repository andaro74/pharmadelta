"""The M06 writer: the sign-off record from a CI build's artifact, and the sign-off page from the served file. Both by hand; neither is evidence (P4).

    uv run python -m src.m06.page record --from <dir>

Fills `pages/api/sign-off.json` from `<dir>/build.json`, the record of a
`m06-lift.yml` run downloaded with `gh run download`. Refuses a record
whose `written_by_ci` or `ok` is false, or whose zip is not committed
under `package.file` byte for byte (its SHA-256 must equal the record's,
and its `manifest.json` the record's `entries`). On each sign-off shown as
signed writes `signature` (`over` the zip's SHA-256, `by` the reviewer's
login, `method` the sentence fixed at PR 2, `read_from` the API path the
gate reads), `package` (`file`, `sha256`, `built_by`, `commit`, `entries`,
`written_by_ci`), `scripted` false, removes the `PLANT` key, and sets the
statement fixed at PR 4 (Unsure 9); writes `lift` at the top with the run
and the artifact. Nothing of the signing commit is written: it does not
exist yet, and the file cannot name the commit that changes it (Unsure
18).

    uv run python -m src.m06.page write

Rebuilds `pages/sign-off.html` from `pages/api/sign-off.json`. The page
shows each sign-off as the file holds it: the reviewer with the seat and
the login, the statement, the signature record, the package record with
the download link by the zip's GitHub URL at the commit that added it
(Unsure 37) and each entry with a link to its source, and the same object
in its `id="signoff-<id>"` block. It claims no read-back: who authored
the signing commit and when is read by the M06 gate on every CI run and
written in that run's result, which the page links (Unsure 18). It shows
no measured number: hashes, commits, run ids and row numbers are the
records' own. The banner says the sign-off is built in this repository's
website layer, is not an agentkeel seat or a platform control, and that
one person holds all seven seats (SPEC/00 §5); a sign-off that is still
scripted gets the scripted banner instead (P8). Deterministic, LF on
every platform (M03 Unsure 33): a reader runs it and compares. The two
files are what the M06 gate (`src/m06/gate.py`) reads; the gate decides,
not this writer.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

from src.m03.lift import esc, json_text, script_json
from src.m06.gate import (
    AGENT_REPO,
    BUILT_BY,
    ENTRY_RECORD,
    PACKAGE_MANIFEST,
    PACKAGE_RECORD,
    REPO,
    ROOT,
    SEAT_FUNCTION,
    SERVED_FILE,
    SIGNATURE_RECORD,
    canonical,
    git,
    package_record_check,
    sha256_hex,
    signature_record_check,
)

SIGNATURE_METHOD = "the last commit that changed pages/api/sign-off.json, read from GitHub's API"
SIGNATURE_READ_FROM = f"GET /repos/{REPO}/commits/<sha>"
STATEMENT = (
    "Reviewed: the evidence package named under `package` holds the CI-written results milestones/README.md cites in its "
    "Measured cells for rows 0, 1, 2, 4, 5 and 6, with the ledger, SPEC/00, the goldens and the four served files at the "
    "commit the package names and label-impact's manifest at the agent commits the served files name, as read on the day "
    "of the signature."
)
GATE_RUNS = f"https://github.com/{REPO}/actions/workflows/m06.yml"
SOURCE_MEANING = {
    "artifact": "a CI-written result: the file of that name in the artifact of the run linked, downloaded in the build run",
    "repository": "this repository's file at the build's commit",
    "agent": "label-impact's file at the agent commit the served files name, read through GitHub's contents API",
}


class Refused(Exception):
    """The inputs are not what the record or the page may be written from."""


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Refused(f"{path} could not be read as JSON: {exc}") from exc


def write_text(path: Path, text: str) -> None:
    # LF on every platform, as .gitattributes stores the files: a rebuild on Windows then equals the committed bytes (M03 Unsure 33).
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- record
def check_package(pkg: dict) -> bytes:
    """The committed zip's bytes, when they are what the build wrote: refused otherwise."""
    path = ROOT / pkg["file"]
    if not path.is_file():
        raise Refused(f"{pkg['file']} is not in the checkout; commit the zip from the artifact first")
    data = path.read_bytes()
    digest = sha256_hex(data)
    if digest != pkg["sha256"]:
        raise Refused(f"{pkg['file']} hashes to {digest}, not the build's {pkg['sha256']}")
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
        listed = json.loads(zf.read(PACKAGE_MANIFEST).decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise Refused(f"{pkg['file']}: {PACKAGE_MANIFEST} could not be read: {type(exc).__name__}") from exc
    if canonical(listed) != canonical(pkg["entries"]):
        raise Refused(f"{pkg['file']}: {PACKAGE_MANIFEST} is not the build's entries")
    for e in pkg["entries"]:
        if sha256_hex(zf.read(e["path"])) != e["sha256"]:
            raise Refused(f"{pkg['file']}: {e['path']} does not hash to its entry's sha256")
    return data


def record(args: argparse.Namespace) -> int:
    try:
        build = read_json(args.from_dir / "build.json")
        if not isinstance(build, dict) or build.get("written_by_ci") is not True:
            raise Refused(f"{args.from_dir / 'build.json'} was not written by CI; a local build is not a record (P4)")
        if build.get("ok") is not True:
            raise Refused(f"{args.from_dir / 'build.json'} holds no package: {build.get('why')}")
        ci, pkg_built = build.get("ci") or {}, build.get("package") or {}
        if not ci.get("run_url") or not ci.get("sha") or not pkg_built.get("sha256"):
            raise Refused(f"{args.from_dir / 'build.json'} names no run URL, no sha or no package hash")
        entries = build.get("entries")
        if not isinstance(entries, list) or not entries or any(tuple(e) != ENTRY_RECORD for e in entries):
            raise Refused(f"{args.from_dir / 'build.json'} holds no entries with the fields {list(ENTRY_RECORD)}")
        package = {
            "file": pkg_built["file"],
            "sha256": pkg_built["sha256"],
            "built_by": {"run_url": ci["run_url"], "artifact": build["artifact"]},
            "commit": pkg_built["commit"],
            "entries": entries,
            "written_by_ci": True,
        }
        assert tuple(package) == PACKAGE_RECORD and tuple(package["built_by"]) == BUILT_BY
        data = check_package(package)
        if sha256_hex(data) != package["sha256"]:
            raise Refused("the committed zip is not the build's")
        doc = read_json(args.api)
        signoffs = doc.get("signoffs") if isinstance(doc, dict) else None
        if not isinstance(signoffs, list) or not signoffs:
            raise Refused(f"{args.api} serves no sign-off")
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2

    for s in signoffs:
        if s.get("signed") is not True:
            continue
        reviewer = s.get("reviewer") or {}
        signature = {"over": package["sha256"], "by": reviewer.get("login"), "method": SIGNATURE_METHOD, "read_from": SIGNATURE_READ_FROM}
        assert tuple(signature) == SIGNATURE_RECORD
        s["statement"] = STATEMENT
        s["signature"] = signature
        s["package"] = package
        s["scripted"] = False
        s.pop("PLANT", None)
        if not signature_record_check(s)["has_record"] or not package_record_check(s)["has_record"]:
            print(f"refused: {s.get('id')} would not read as signed: {signature_record_check(s)['why']}; {package_record_check(s)['why']}", file=sys.stderr)
            return 2
    doc["lift"] = {
        "run_url": ci["run_url"],
        "artifact": build["artifact"],
        "written_from": f"build.json and {Path(package['file']).name} in that artifact; the zip is committed byte for byte under {package['file']}; "
        "`uv run python -m src.m06.page record --from <dir>` writes the records in this file and "
        "`uv run python -m src.m06.page write` rebuilds pages/sign-off.html from it",
    }
    write_text(args.api, json_text(doc) + "\n")
    for s in signoffs:
        print(f"{s['id']}: signed {json.dumps(s.get('signed'))}; signature over {str((s.get('signature') or {}).get('over'))[:12]}…; package {(s.get('package') or {}).get('file')} with {len((s.get('package') or {}).get('entries') or [])} entries; scripted {json.dumps(s.get('scripted'))}")
    print(f"wrote {args.api} from {args.from_dir / 'build.json'}; the signing commit is the seat holder's own, not this writer's")
    return 0


# ------------------------------------------------------------------ page
def code(value: Any) -> str:
    return f"<code>{esc(json.dumps(value) if value is None or isinstance(value, bool) else value)}</code>"


def link(url: str, text: str | None = None) -> str:
    return f'<a href="{esc(url)}">{esc(text if text is not None else url)}</a>'


def zip_commit(file: str) -> str:
    sha = git("log", "-1", "--format=%H", "--", file)
    if len(sha) != 40:
        raise Refused(f"{file} is not committed; the download link names the commit that added it (Unsure 37)")
    return sha


def source_link(e: dict) -> str:
    if e["source"] == "artifact":
        return f"{link(e['run_url'], 'the run')}, artifact {code(e['artifact'])}, file {code(e['name'])}"
    if e["source"] == "repository":
        return f"{link(f'https://github.com/{REPO}/blob/{e['commit']}/{e['name']}', e['name'])} at {code(e['commit'][:7])}"
    return f"{link(f'https://github.com/{AGENT_REPO}/blob/{e['commit']}/{e['name']}', e['name'])} of {esc(AGENT_REPO)} at {code(e['commit'][:7])}"


def render_signature(s: dict) -> list[str]:
    sig = s.get("signature")
    out = ["<h3>The signature</h3>"]
    if not isinstance(sig, dict):
        out += ['<div class="none" role="note">', f"  <p><strong>None.</strong> <code>signature</code> is {code(sig)}.</p>", "</div>"]
        return out
    out += [
        "<p>The signature is a commit: the one that last changed <code>api/sign-off.json</code>, made by the seat holder from their own",
        f"   terminal. The record names the hash signed and the login expected. Whether that commit's author is {code(sig.get('by'))}, when it",
        f"   was made and what GitHub says of its verification are read back by the M06 gate on every CI run ({link(GATE_RUNS, 'm06.yml runs')})",
        "   and written in that run's <code>result.json</code>; this page copies none of it, because the commit that writes this page cannot",
        "   name itself (M06 Unsure 18). The gate's run is the read-back; this page is the record.</p>",
        "<table>",
        "  <tbody>",
        f"    <tr><th scope=\"row\">signature.over</th><td>{code(sig.get('over'))}, the SHA-256 of the package file</td></tr>",
        f"    <tr><th scope=\"row\">signature.by</th><td>{code(sig.get('by'))}, the login the seat holder's commit must be authored by</td></tr>",
        f"    <tr><th scope=\"row\">signature.method</th><td>{esc(sig.get('method'))}</td></tr>",
        f"    <tr><th scope=\"row\">signature.read_from</th><td>{code(sig.get('read_from'))}</td></tr>",
        "  </tbody>",
        "</table>",
    ]
    return out


def render_package(s: dict) -> list[str]:
    pkg = s.get("package")
    out = ["<h3>The evidence package</h3>"]
    if not isinstance(pkg, dict):
        out += ['<div class="none" role="note">', f"  <p><strong>None.</strong> <code>package</code> is {code(pkg)}. Download the evidence package: nothing to download.</p>", "</div>"]
        return out
    sha = zip_commit(pkg["file"])
    view = f"https://github.com/{REPO}/blob/{sha}/{pkg['file']}"
    raw = f"https://github.com/{REPO}/raw/{sha}/{pkg['file']}"
    built = pkg.get("built_by") or {}
    entries = pkg.get("entries") or []
    out += [
        f"<p><strong>Download the evidence package:</strong> {link(view, Path(pkg['file']).name)} (the file view at the commit that added it,",
        f"   {code(sha[:7])}; {link(raw, 'the raw file')}). Its SHA-256 is {code(pkg.get('sha256'))}; compare after downloading. The zip holds",
        f"   <code>manifest.json</code>, the list of entries below, and each entry at its path. It was built by this repository's CI,",
        f"   {link(built.get('run_url') or '', built.get('run_url') or 'no run')}, as the artifact {code(built.get('artifact'))}, from this repository at",
        f"   {code(str(pkg.get('commit'))[:7])}, and committed byte for byte. The M06 gate compares the committed file with that artifact's and each",
        "   entry with its source on every CI run; what it read is in that run's result, linked above.</p>",
        "<table>",
        "  <thead><tr><th>Path in the zip</th><th>Source</th><th>Ledger row</th><th>SHA-256</th></tr></thead>",
        "  <tbody>",
    ]
    for e in entries:
        row = "" if e.get("ledger_row") is None else code(e["ledger_row"])
        out.append(f"    <tr><td><code>{esc(e['path'])}</code></td><td>{esc(e['source'])}: {source_link(e)}</td><td>{row}</td><td><code>{esc(e['sha256'])}</code></td></tr>")
    out += ["  </tbody>", "</table>"]
    out.append("<p>Sources: " + "; ".join(f"<code>{esc(k)}</code>, {esc(v)}" for k, v in SOURCE_MEANING.items()) + ". A ledger row is the row of "
               "<code>milestones/README.md</code> the entry is evidence for; the ledger inside the package is as at the build's commit, "
               "and row 7's own measurement is what this package is signed for, not what it holds.</p>")
    return out


def render_records(s: dict) -> list[str]:
    r = s.get("reviewer") or {}
    seat_from = r.get("seat_read_from") or {}
    sig, pkg = s.get("signature"), s.get("package")
    rows = [
        ("reviewer.function", code(r.get("function"))),
        ("reviewer.seat", code(r.get("seat"))),
        ("reviewer.login", f"{code(r.get('login'))}, read from {esc(seat_from.get('repository'))} {code(seat_from.get('path'))} at {code(seat_from.get('commit'))} ({code(seat_from.get('key'))})"),
        ("signed", f'<code class="chip chip-{"ok" if s.get("signed") is True else "warn"}">{esc(json.dumps(s.get("signed")) if s.get("signed") is None or isinstance(s.get("signed"), bool) else s.get("signed"))}</code>'),
        ("signature", code(None) if not isinstance(sig, dict) else f"over {code(str(sig.get('over'))[:12] + '…')}, by {code(sig.get('by'))}"),
        ("package", code(None) if not isinstance(pkg, dict) else f"{code(pkg.get('file'))}, {len(pkg.get('entries') or [])} entries, built by {link((pkg.get('built_by') or {}).get('run_url') or '')}"),
        ("scripted", code(s.get("scripted"))),
    ]
    out = ["<h3>Where this came from</h3>", "<table>", "  <tbody>"]
    out += [f"    <tr><th scope=\"row\">{esc(k)}</th><td>{v}</td></tr>" for k, v in rows]
    out += ["  </tbody>", "</table>"]
    return out


def render_signoff(s: dict) -> str:
    r = s.get("reviewer") or {}
    seat_from = r.get("seat_read_from") or {}
    expected = SEAT_FUNCTION.get(r.get("seat"))
    out = [f'<section class="signoff" id="{esc(s["id"])}">', f"<h2>Sign-off {code(s['id'])}</h2>", "<h3>The reviewer</h3>"]
    out.append(f"<p><strong>{esc(r.get('function'))}</strong>, the seat {code(r.get('seat'))}, held by {code(r.get('login'))} as "
               f"{esc(seat_from.get('repository'))}'s {code(seat_from.get('path'))} reads at {code(seat_from.get('commit'))} ({code(seat_from.get('key'))}). "
               + ("The function shown is the one SPEC/00 §5 maps to this seat." if expected == r.get("function") else f"SPEC/00 §5 maps this seat to {code(expected)}, not the function shown.") + "</p>")
    out += ["<h3>The statement</h3>", f"<blockquote><p>{esc(s.get('statement'))}</p></blockquote>"]
    out += ['<section class="record">', *render_signature(s), "</section>"]
    out += ['<section class="record">', *render_package(s), "</section>"]
    out += render_records(s)
    out += [
        "<h3>The same entry, as the file serves it</h3>",
        "<p>The object below is this sign-off's entry in <code>api/sign-off.json</code>, the same JSON value the file holds. A reader",
        "   of the page reads it from here.</p>",
        f'<script type="application/json" id="signoff-{esc(s["id"])}">',
        script_json(s),
        "</script>",
        f"<pre>{esc(json_text(s))}</pre>",
        "</section>",
    ]
    return "\n".join(out)


def render_page(doc: dict) -> str:
    signoffs = doc["signoffs"]
    lift = doc.get("lift") or {}
    scripted = any(s.get("scripted") is True for s in signoffs)
    parts = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>pharmadelta: reviewer sign-off</title>",
        '<link rel="stylesheet" href="assets/site.css">',
        "</head>",
        "<body>",
        "<header>",
        '  <p class="kicker"><strong>pharmadelta</strong> · reviewer sign-off</p>',
        '  <nav class="site-nav" aria-label="Pages">',
        '    <a href="../index.html">Front page</a>',
        '    <a href="detail.html">Detail</a>',
        '    <a href="side-by-side.html">Side by side</a>',
        '    <a href="break-it.html">Try to break it</a>',
        '    <a href="sign-off.html" aria-current="page">Sign-off</a>',
        '  </nav>',
        "  <p class=\"statement\">pharmadelta is an independent open-source demo and is not affiliated with any pharmaceutical company.",
        "     The company, Ardentia Generics, is fictional; its portfolio and every “our label” statement are invented.",
        "     The labels are real public-domain labels of old off-patent generics, read from DailyMed.</p>",
        "  <p>This page holds the reviewer sign-off and the evidence package: who reviewed the evidence behind this demo's",
        "     ledger (<code>milestones/README.md</code>), under which seat, and what they signed; and the package a reader",
        "     downloads to read the same evidence. The detail page <a href=\"detail.html\">detail.html</a>, the side-by-side page",
        "     <a href=\"side-by-side.html\">side-by-side.html</a> and the break page <a href=\"break-it.html\">break-it.html</a> show",
        "     the answers and the stops that evidence is about. This page copies <code>api/sign-off.json</code>.</p>",
    ]
    if lift.get("run_url"):
        parts += [
            f"  <p>The package was built by this repository's CI: {link(lift['run_url'])}, artifact {code(lift.get('artifact'))}; this file and this",
            "     page were written from that artifact and the committed zip by <code>src/m06/page.py</code>, and the signing commit is the seat",
            "     holder's own. Whether that commit is the seat holder's, and whether the package is what CI wrote with every entry equal to its",
            f"     source, is read back by the M06 gate on every CI run ({link(GATE_RUNS, 'm06.yml runs')}); this page claims neither.</p>",
        ]
    parts.append("</header>")
    parts.append("")
    if scripted:
        parts += [
            '<div class="scripted" role="note">',
            "  <p><strong>Scripted.</strong> A sign-off below is written by hand (SPEC/00 P8): its entry carries <code>scripted</code> true. Nothing",
            "     scripted is a signature, and a package it names is not evidence.</p>",
            "</div>",
        ]
    else:
        parts += [
            '<div class="layer" role="note">',
            "  <p><strong>Built in this repository's website layer.</strong> The sign-off is not an agentkeel seat and not a platform control, and the",
            "     platform does not read it (SPEC/00 §5). The agent is <code>label-impact</code>, a tenant of agentkeel; its seven seats are read from",
            "     its <code>manifest.yaml</code>. One person holds all seven seats on this project (agentkeel ruling R1, ADR-0001), so the reviewer",
            "     is the author of every pull request in this repository and reviews their own work; the sign-off's worth is that this repository's",
            "     CI can read it back, not that the reviewer is independent (M06 Unsure 10). Pharmacovigilance and Legal hold no seat and never",
            "     appear here as a signature (SPEC/00 §5).</p>",
            "</div>",
        ]
    parts += [
        "",
        "<h1>Reviewer sign-off</h1>",
        "<p>A sign-off is one seat holder's statement that an evidence package is the evidence the ledger cites, signed in a way",
        "   this repository's CI can read back: the seat holder's own commit that last changed <code>api/sign-off.json</code>, over the",
        "   SHA-256 of a package file in this repository. A package is a zip a reader downloads, holding CI-written results and the",
        "   files they are about, each named with the run that wrote it or the commit it is at.</p>",
        "",
    ]
    for s in signoffs:
        parts.append(render_signoff(s))
        parts.append("")
    parts += [
        "<footer>",
        "  <p>This demo produces the evidence a validation would need. It is not medical information: the agent assesses",
        "     regulatory impact on labeling and never answers a treatment question (SPEC/00 §2). The authority for what this demo",
        "     claims is <code>SPEC/00-overview.md</code>; what was measured is in <code>milestones/README.md</code>. No number on",
        "     this page is a measured result: the hashes, commits, run ids and row numbers are the records' own, the runs are",
        "     linked, and the seat count is SPEC/00 §5's. What CI read back of this sign-off is in the M06 gate's runs, linked above.</p>",
        "</footer>",
        "</body>",
        "</html>",
    ]
    return "\n".join(parts) + "\n"


def write(args: argparse.Namespace) -> int:
    try:
        doc = read_json(args.api)
        signoffs = doc.get("signoffs") if isinstance(doc, dict) else None
        if not isinstance(signoffs, list) or not signoffs or not all(isinstance(s, dict) and isinstance(s.get("id"), str) for s in signoffs):
            raise Refused(f"{args.api} holds no `signoffs` list of objects with an `id`")
        html = render_page(doc)
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    write_text(args.page, html)
    for s in signoffs:
        print(f"{s['id']}: signed {json.dumps(s.get('signed'))}; signature {'record' if isinstance(s.get('signature'), dict) else 'null'}; package {'record' if isinstance(s.get('package'), dict) else 'null'}; scripted {json.dumps(s.get('scripted'))}")
    print(f"wrote {args.page} from {args.api}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_record = sub.add_parser("record", help="by hand: fill the records in pages/api/sign-off.json from a build run's artifact")
    p_record.add_argument("--from", dest="from_dir", required=True, type=Path, help="the directory holding build.json")
    p_record.add_argument("--api", type=Path, default=ROOT / SERVED_FILE)
    p_write = sub.add_parser("write", help="by hand: rebuild pages/sign-off.html from pages/api/sign-off.json")
    p_write.add_argument("--api", type=Path, default=ROOT / SERVED_FILE)
    p_write.add_argument("--page", type=Path, default=ROOT / "pages" / "sign-off.html")
    args = parser.parse_args()
    return record(args) if args.command == "record" else write(args)


if __name__ == "__main__":
    raise SystemExit(main())
