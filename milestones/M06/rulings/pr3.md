---
ruling: m06-pr3
seat:
  - Engineering
  - Security
  - Product
  - Tool Owner
authorises:
  # Engineering: the repair of the gate's verdict path (Defects 1, 2), the label (Defect 3) and the commit check (Hardening 5)
  - src/m06/gate.py
  # Security: the redirect leg records an exception by type alone, no leg returns headers, a Location is resolved once and kept nowhere (Defect 4); m06.yml is unchanged
  - src/m06/gate.py
  # Tool Owner: the records' fields are unchanged; `package.commit` stays as fixed at PR 2 (Unsure 29)
  - src/m06/gate.py
  # Product: the ledger's PR count, the milestone's PR 3 detail and this file
  - milestones/README.md
  - milestones/M06/README.md
  - milestones/M06/rulings/pr3.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M06/README.md
  - milestones/M06/rulings/pr1.md
  - milestones/M06/rulings/pr2.md
  - milestones/M05/README.md
  - milestones/M05/rulings/pr3.md
  - milestones/M04/rulings/pr3.md
  - milestones/M03/rulings/pr4.md
  - .github/workflows/m06.yml
  - pages/api/sign-off.json
  - pages/sign-off.html
  - https://github.com/andaro74/pharmadelta/actions/runs/42491031888
  - https://github.com/andaro74/pharmadelta/actions/runs/42491298504
  - https://github.com/andaro74/pharmadelta/actions/runs/42495856254
  - https://api.github.com/repos/andaro74/pharmadelta/actions/runs/42495856254/artifacts
pr: https://github.com/andaro74/pharmadelta/pull/35
---

# Ruling: M06 PR 3 (repair)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR repairs. The cold review of #34 (`milestones/M06/README.md`,
"Cold review of #34") found four defects and one hardening in
`src/m06/gate.py` and nothing in `.github/workflows/m06.yml`. Two are in
the verdict path: a zip member or the package file that could not be
read raised out of `read_back` and dropped the differences found before
it, so a differing sign-off read UNSCORABLE; and a page that is not UTF-8
raised past the served file's read, so the plant itself read UNSCORABLE
with no lists. One is a label: the summary's "package hash" column read
"equal" when nothing was hashed. One is what `result.json` could hold:
on the redirect leg, urllib's own message for a `Location` it refuses
quotes that URL, the blob store's signed redirect, and the gate wrote the
message. The hardening pins a `repository` entry's `commit` to hex
digits, as the agent source already was. `src/m06/gate.py` now guards
every zip and file read, keeps the lists when the read-back raises,
records the page's failure under `unreadable` with the lists standing,
returns no headers and records the redirect leg's failure by type, and
labels an unhashed file "not read". Nothing under `pages/` changes; the
plant stands and nothing here lifts it. Nothing here decides the row: the
`main` run after #34 merged, 42495856254, is the measurement, read first
in this session, and PR 4 fills the "Measured" cell from it.

## Rulings in this PR

1. **Engineering (Defects 1, 2, 3; Hardening 5).** The repair is as the
   README's "The repair" states: `zip_member` for every member read, the
   package file's `read_bytes` guarded, `read_back` a wrapper that keeps
   `differences` and `not_read` when `_read_back` raises, `read_page`
   catching `ValueError` beside `OSError`, the summary's hash column
   "not read" when the read-back holds no hash, `read_repository_file`
   requiring 7 to 40 hex digits. The lists' names, the records' fields,
   `SEAT_FUNCTION`, the verdict's shape, the exit codes and the artifact's
   name are unchanged. `import urllib.parse` is the one new import.
   `pyproject.toml` and `uv.lock` are unchanged.
2. **Security (Defect 4).** `http_get` returns no headers on any leg. A
   `Location` is resolved once with `urllib.parse.urljoin` against the
   request's URL and passed to the redirect leg, which sends no
   `Authorization` header; it is kept in no variable that outlives the
   call and written nowhere. On the redirect leg an exception is recorded
   by its type alone, so a URL urllib quotes in its message reaches
   neither `result.json`, the step summary nor the log. On the API leg
   the type and a short message stay: the API URL holds no token and no
   redirect. `m06.yml` is unchanged: the token stays in the gate step's
   `env` alone and the grep step stays as the second fence. No run has
   taken the redirect leg in CI; the local server reading is construction
   (P4).
3. **Engineering, Security; the rule.** M05 PR 3's rule, stated at PR 2
   as built in, now holds for every read after the served file: network,
   git, zip and file. A read that raises is a read not made, recorded
   under `unreadable`, and the lists stand; RED comes first. `run()`
   keeps a last fence around `read_back` for what the wrapper does not
   foresee; that fence can now drop nothing, since the lists live outside
   the call.
4. **Security; Unsure 19 as ruled.** The signer is the commit's
   `author.login`, as PR 2 built; `committer.login` is recorded beside it
   and not required. A squash merge would make the committer `web-flow`
   and leave the author; a merge commit leaves both the author's. GitHub's
   `verification.verified` is recorded and not required at M06 (Unsure 1,
   ruled at PR 2). If Security later requires either, the owner signs
   commits first and the gate changes outside this cap. Closed at M06.
5. **Security; Unsure 21 as ruled.** The grep step's prefixes stay
   `ghs_`, `ghp_` and `github_pat_`. The workflow's token is an Actions
   token, `ghs_`; the step is a second fence behind a code path that
   writes the token nowhere, and after Defect 4's repair writes no
   redirect URL either. The prefixes `gho_`, `ghu_` and `ghr_` are
   tokens no step of this workflow holds and are not added. A match can
   only be a token or a package entry's path (Unsure 31). Closed at M06.
6. **Engineering; Unsure 22 as ruled.** `fetch-depth: 0` stays. On a
   pull request the checkout is the merge ref; `git log -1 --
   pages/api/sign-off.json` names the branch commit that last changed the
   file when the merge is clean, and the merge commit, authored by the
   merger, when it is not. On `main` after a merge commit it names the
   branch commit. With one person holding every seat the merger is the
   seat holder in either case; a conflict merge by another login would
   read `signoffs_differing`, which is the finding and not a repair.
   Recorded; closed at M06.
7. **Engineering; Unsure 26 as ruled.** The lift's CI run names the zip
   inside its artifact by the basename it is committed under
   (`Path(package.file).name`), and the gate finds it so. Fixed for the
   lift; the lift PR's first commit names the file.
8. **Product, Tool Owner; Unsure 27 as ruled.** One served file, one
   last commit, accepted as the limit of reading (a) at M06. Every
   sign-off in `pages/api/sign-off.json` is read against the commit that
   last changed the file; a second seat's sign-off by a second login
   would make the first read `signoffs_differing`, and that is the
   finding, not a repair. With one person holding all seven seats (R1)
   the logins coincide. Per-sign-off files are not built at M06; a later
   milestone that wants more than one signer designs them.
9. **Product; Unsure 28.** This PR is #35, the next number on this
   repository after #34.
10. **Product.** "PRs used / cap" is 3 / 4 here and in the ledger. PR 4
    carries the lift by M03's path (b) as `rulings/pr2.md` 17 ruled, the
    "Measured" cell from run 42495856254, the rulings carried below, and
    the tag `m06`. A fifth PR is a RED close (ADR-0001 U9).
11. **Product; carried by name to PR 4, not ruled.** Unsure 9 (the
    statement's wording), 10 (one person reviews their own work), 15 (a
    hand-run writer for the page in the signing commit), 16 (which files
    the package carries), 18 (no `read_back` field in the signature
    record; the page shows the read-back from the CI result with the
    run's link), 20 (the build artifact's expiry), 23 (the `agent` source
    reads files under 1 MB), 24 (a sign-off shown as not signed is named
    by no list), 25 (`SEAT_FUNCTION` is SPEC/00 §5's table); and PR 3's
    29 (`package.commit` read back by nothing), 30 (the read-back paths'
    first CI exercise is the lift's), 31 (a path holding a token's
    prefix), 32 (`signoffs_disagreed` reads one direction).
12. **Product; on reading run 42495856254.** The `main` run after #34
    merged wrote RED, `signoffs_unsigned` `["s-001"]`,
    `signoffs_disagreed` `[]`, `signoffs_differing` `[]`, `unreadable`
    `[]`, `written_by_ci` true, `artifacts_read` `[]`, `read_back` null,
    on `main` at `e175d77`, exit 1; the grep step passed and the artifact
    `m06-gate-e175d772bd32ce9e148f79b868b72a2dcfa8b24f` was written. It
    equals the PR runs on every field the row names. It is the Measured
    cell's source for PR 4 (M01 Unsure 23, ruled at M02 PR 1).

## What a reader can falsify

- `git diff main --stat` on this PR touches `src/m06/gate.py`,
  `milestones/README.md`, `milestones/M06/README.md` and
  `milestones/M06/rulings/pr3.md` only. `git diff main -- pages/
  .github/ src/m03/ src/m04/ src/m05/ src/baseline/ pyproject.toml
  uv.lock` is empty.
- In `src/m06/gate.py`: `zip_member` exists and is called three times;
  `read_back` calls `_read_back` inside a `try`; `read_page` catches
  `(OSError, ValueError)`; `http_get` returns no `headers` key and calls
  `urllib.parse.urljoin`; `read_repository_file` matches
  `[0-9a-f]{7,40}`; the summary's hash column has a "not read" arm.
- The artifact `m06-gate-<sha>` on this PR's run holds `result.json`
  with `verdict: RED`, `signoffs_unsigned: ["s-001"]`, the other lists
  `[]`, `read_back` null and `artifacts_read: []`, as #34's runs did.
- The artifact of run 42495856254 reads as the table under "The `main`
  run after #34" says. Download it and read it.

## What this ruling does not settle

The items carried under ruling 11, each with its seat in
`milestones/M06/README.md`. What matters most for the close: which files
the package carries (16), the statement's wording before the signing
commit (9), and whether the lift's page shows the read-back from the CI
result with its link (18).
