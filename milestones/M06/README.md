# M06: Reviewer sign-off and a downloadable evidence package

Row 7 of the ledger (`milestones/README.md`). The claim text is SPEC/00
§8's, word for word. Needs M03, which closed at tag `m03` on `9932776`
with row 4 GREEN; M04 and M05 closed after it at tags `m04` on
`3905c10` and `m05` on `71770aa`, rows 5 and 6 GREEN. One claim, one
planted failure, one measured verdict (P3). Cap four PRs (ADR-0001 U9).

SPEC/00 §5: "M06's reviewer sign-off is built in the website layer of
this repository. It is not an agentkeel seat and not a platform
control, and the page says so."

## Ledger row

Written at PR 1 open. The row in `milestones/README.md` is the ledger's;
this is the same row with the open detail.

| Field | Row 7 |
|---|---|
| Claim | Reviewer sign-off and a downloadable evidence package |
| Falsifiers | F6.1 a sign-off the sign-off page shows as signed was not a seat holder's over a downloadable evidence package, as this repository's CI can read back: it carries no signing record, or the commit that last changed the served file was not authored by the login that holds the seat shown in `label-impact`'s `manifest.yaml`, or the function shown is not that seat's (SPEC/00 §5); or it carries no package record, or the package file it names is not in the repository, or that file's SHA-256 differs from the one the signature names, or an entry of the package is not the CI-written result the run and artifact it names wrote; or the page shows a sign-off the served file does not serve. |
| Seeded commit | `6cfc1eb` on `m06-pr1`: `pages/api/sign-off.json`, the reviewer sign-offs pharmadelta serves, one entry `s-001`: reviewer Regulatory Affairs, the seat `product`, held by `andaro74` as `label-impact`'s `manifest.yaml` reads at `956cd87`; a statement; `signed` true written by hand; `signature` null (no commit, no login read back, no time); `package` null (no file, no hash, no entries, no link); `scripted` true, a `PLANT` key beside them; `pages/sign-off.html`, the sign-off page, showing it as signed with nothing to download, labelled scripted, the same object embedded. No evidence package exists in the repository, and nothing in it builds one, hashes one or reads a signing commit. |
| Expected gate output | PR 2's gate, in CI, reads every sign-off the served file serves and the page shows and names each shown as signed that carries no signing record, or no package record, or names a package file that is not in the repository (`signoffs_unsigned`), and each that the page and the file do not agree on (`signoffs_disagreed`); then, for each signed sign-off, reads from GitHub's API the commit that last changed the served file and checks its author's login is the one holding the seat shown in `label-impact`'s `manifest.yaml` at the commit the reviewer record names and that the function shown is that seat's (SPEC/00 §5), hashes the package file and compares it with the hash the signature names, and compares each entry of the package with the artifact of the CI run it names, downloaded in that run; it names each that fails any of these (`signoffs_differing`). It writes a `result.json` that is RED when any sign-off is unsigned, disagreed or differing, naming each; GREEN only when every sign-off shown as signed carries a signing record by the seat holder and a package that hashes to what was signed with every entry equal to its CI artifact, and is shown as served; UNSCORABLE when nothing is RED and the served files, GitHub's API, the manifest or an artifact could not be read. On `6cfc1eb`: RED, `signoffs_unsigned` `["s-001"]`, `signoffs_disagreed` `[]`, `signoffs_differing` `[]`. The Measured cell cites the `main` run after PR 2 merges (M01 Unsure 23, ruled at M02 PR 1). |
| Measured | RED, `signoffs_unsigned` `["s-001"]`, `signoffs_disagreed` `[]`, `signoffs_differing` `[]`, `unreadable` `[]`, `written_by_ci` true, on `main` at `e175d77`: [run 42495856254](https://github.com/andaro74/pharmadelta/actions/runs/42495856254), artifact `m06-gate-e175d772bd32ce9e148f79b868b72a2dcfa8b24f`. The PR run on #34 at merge ref `8431885`, [run 42491031888](https://github.com/andaro74/pharmadelta/actions/runs/42491031888), artifact `m06-gate-8431885faa0353ebf43d56ea244df4bb98ca8c6b`, read the same on every field the row names. Equals the expected output. The lift (M03's path (b), `milestones/M06/rulings/pr2.md` 17): the package built by [run 42504215645](https://github.com/andaro74/pharmadelta/actions/runs/42504215645) as artifact `m06-package-226ad89ce575d89dfb90c9a5d93a8a5a9d1a31b9` and committed byte for byte at `3e56b07`; the seat holder's own signing commit `37352ef`; the run on PR #36 at merge ref `15fef71`, [run 42524408048](https://github.com/andaro74/pharmadelta/actions/runs/42524408048), artifact `m06-gate-15fef71e0c10aecf7a774d99ab3ea99c1f4da82c`, read GREEN, every list `[]`, `unreadable` `[]`, the signing commit's author `andaro74`, the seat's login `andaro74`, the hash equal, 22 of 22 entries equal to their sources; a reading after the measurement. |
| PRs used / cap | 4 / 4 |
| State | GREEN |

## The false state (P1, P2)

The claim says a reviewer signed off and an evidence package can be
downloaded. It is false when the page shows a sign-off that no seat
holder signed, over a package that does not exist. That is what
`6cfc1eb` commits.

`pages/api/sign-off.json` is what the sign-off page serves: a list of
sign-offs, in the shape of `pages/api/answers.json` with `reviewer`,
`signature` and `package` where that file has `agent`, `call` and
`door`. It holds one entry, `s-001`. The reviewer is Regulatory
Affairs, the function SPEC/00 §5 maps to the seat `product`; the seat
is held by `andaro74`, read from `agentkeel-studio/label-impact`'s
`manifest.yaml` at `956cd87` (`seats.product`) on 2026-11-08 UTC. The
statement is what a reviewer would sign. `signed` is true, written by
hand. `signature` is null: no commit, no login read back, no time.
`package` is null: no file, no hash, no entries, no link. `scripted` is
true and a `PLANT` key says what the entry is.

`pages/sign-off.html` is the sign-off page. It shows the reviewer with
the seat and the login, the statement, "None" under the signature and
"None" under the evidence package, with "Download the evidence package:
nothing to download", all under a banner that says the page is scripted,
nothing was signed and there is nothing to download (P8, SPEC/00 §11).
It says the sign-off is built in this repository's website layer, not
an agentkeel seat and not a platform control, that one person holds all
seven seats, and that Pharmacovigilance and Legal hold no seat and never
appear as a signature (SPEC/00 §5). It embeds the entry in a `<script
type="application/json" id="signoff-s-001">` block, so a reader reads
the page's sign-off without an HTML parser; the block was generated from
the file and equals its entry as parsed JSON. The page shows no answer,
no row and no clause: a sign-off is not an answer. It shows no measured
number: its numbers are the sign-off's id, SPEC/00's section numbers,
the seat count SPEC/00 §5 states, and the manifest's commit.

Why this plant: a page that shows a sign-off with a seat holder's name
on it and nothing signed is the thing the claim rules out, as a scripted
answer was M03's and a scripted block M05's. A gate that checks the page
shows a reviewer and the word "signed" passes the plant; a gate that
demands a signing commit by the seat holder and a package that hashes to
what was signed does not. The plant tests which one PR 2 builds. It also
plants the second half of the claim: there is no package file, so
"downloadable" is false too, and both halves are false in one entry
named in one list (P3).

Lifting the plant is: a package built by this repository's CI from CI
artifacts and written as an artifact, its file committed under `pages/`
with its SHA-256; then the seat holder's own commit that fills
`signature` with that hash and `package` with the record, sets
`scripted` false, removes the `PLANT` key and rebuilds the page. Which
PR carries the lift is decided after PR 2 goes RED, not here.

## What "sign-off" and "downloadable" mean at M06 (assumptions, Unsure 1, 2)

SPEC/00 says where the sign-off is built and what it is not. It does
not say what a signature is. This milestone reads it as (a): the
reviewer's own commit that changes `pages/api/sign-off.json`, read back
from GitHub's API as the commit that last changed the file, whose
`author.login` is the login holding the seat in `label-impact`'s
manifest. Every commit that changes the served file is a signing act
by its author; a change by anyone else, CI included, voids the sign-off
and the gate reads `signoffs_differing`. GitHub's `verification` of the
commit is recorded as read; commits on this repository are unsigned
today (`1065863`: `verified` false, reason `unsigned`), so whether the
gate must require it is Unsure 1. The other readings, (b) a signed tag
and (c) a platform control, are not taken: tags are not in a checkout
by default, and SPEC/00 §5 says the sign-off is not a platform control.
Proposed: (a). Security and Product rule.

"Downloadable" at M06 means a file in this public repository that a
reader fetches by its GitHub URL, raw or through the file view, named on
the page with its SHA-256. GitHub Pages is not enabled (404 on
2026-11-08 UTC); "public" has meant readable in the repository since
M03. Ruled at this PR (`rulings/pr1.md` 8): the milestone does not
depend on Pages, and the setting stays the owner's.

The reviewer is the holder of the seat `product`, shown as Regulatory
Affairs (SPEC/00 §5: "what the assessment covers and when it is
acceptable"). Other seats may sign later, each with its own seat and
login; Pharmacovigilance and Legal hold no seat and may be shown as
consulted, never as a signature (Unsure 4).

## Open detail (PR 1, 2026-11-08 UTC)

### What this PR holds

- Row 7 of the ledger: falsifier, seeded commit, expected gate output,
  PRs used 1 / 4.
- `pages/api/sign-off.json` and `pages/sign-off.html`, the plant.
- This file.
- `rulings/pr1.md`.

Nothing else. No package, no hash, no reading of a commit from GitHub's
API, no workflow, no gate, no test (P2). No edit to `src/`
(`src/baseline/` is frozen at `m00`, P5), `goldens/`, `data/`,
`pages/detail.html`, `pages/side-by-side.html`, `pages/break-it.html`,
`pages/api/answers.json`, `pages/api/baseline.json`,
`pages/api/break-it.json`, `.github/workflows/`, SPEC/00, CLAUDE.md,
the README, or anything under `milestones/M00/` to `milestones/M05/` or
`milestones/adoption/`.

### The repository, as read at open (construction, not evidence, P4)

Read 2026-11-08 UTC (2026-11-07 local) on `main` at `020bfac`.

| What | Read |
|---|---|
| `main` | `020bfac`, the merge commit of #31 (the M05 re-lift, outside any cap); tag `m05` on `71770aa`. Tags `m00` `e94b76b`, `m01` `c60599e`, `m02` `ab72b9d`, `m03` `9932776`, `m04` `3905c10`, `m05` `71770aa` (`git rev-parse <tag>^{commit}`); no `m06` tag |
| the ledger | row P GREEN; rows 0, 1, 4, 5, 6 GREEN, row 2 RED with its finding; row 7 OPEN at 0 / 4 before this PR |
| the `main` runs on `020bfac` | `gate` 42417261385, `m02` 42417261382, `m03` 42417261384, `m04` 42417261376 and `m05` 42417261373, all `push`, all success; artifacts `m00-gate-020bfac…`, `m02-gate-020bfac…`, `m03-gate-020bfac…`, `m04-gate-020bfac…`, `m05-gate-020bfac…`. Read in the second comment on #31; not downloaded here. Readings after their measurements |
| `pages/` | `detail.html`, `side-by-side.html`, `break-it.html`, `api/answers.json`, `api/baseline.json`, `api/break-it.json`; no sign-off page, no evidence package, no `pages/evidence/` before this PR. No page shows a seat before this PR (grep `seat` under `pages/`: no match) |
| the M03, M04 and M05 gates' reads | each reads its own files by path (`src/m03/gate.py`, `src/m04/gate.py`, `src/m05/gate.py`); none globs `pages/`. Grep `sign-off` and `signoff` under `src/` and `.github/`: no match |
| the M00 scorer | `src/gate/score.py` scores `g-005` and `g-006` as `matched` false with `why` "answered, not blocked; nothing here can block before P" on every `gate` run; `gate.yml` uploads `observations.json` and `result.json` as `m00-gate-<sha>`, 90 days. The baseline's report on scenarios 5 and 6 (SPEC/00 §7; M05 Unsure 12) |
| label-impact | `main` at `956cd87`; `manifest.yaml` (blob `4d6d126`) reads `platform_version: m10`, guardrail `4q5ebd7qov82` version `"1"`, seven seats each `andaro74`, `callers: [{subject: pharmadelta, issuer: self}]` |
| commits on this repository | unsigned: `1065863` reads `author.login` `andaro74`, `verification.verified` false, reason `unsigned`; the merge commit `020bfac` carries GitHub's own signature (`git log --format=%G?` reads `E`). `author.login` is GitHub's match of the commit's email to an account |
| the repository | `visibility` public, `default_branch` main, `has_pages` false |
| GitHub Pages | not enabled: `GET /repos/andaro74/pharmadelta/pages` answers 404 (Unsure 2); enabled by the owner after the close, 2026-11-08 UTC, `milestones/adoption/rulings/pages-index.md` |
| required checks on `main` | `M00 gate` the one required context, `strict` true; no rulesets (Unsure 3) |
| `src/baseline/` | unchanged since tag `m00` (`git diff m00 --stat -- src/baseline/` is empty) |
| the door's credential | the secret and the three variables set at M03 are on this repository; none is read by this PR |

### What this PR does not hold

- No package. No file under `pages/evidence/`, no zip, no manifest, no
  hash. `package` is null on the one entry until the PR that carries
  the lift.
- No signature. `signature` is null. The last commit that changed
  `pages/api/sign-off.json` on this branch is `6cfc1eb`, authored by
  the seat holder's login; the plant does not claim it as a signature,
  and PR 2's gate reads the record, not the author, when deciding
  `signoffs_unsigned`: a null record is unsigned whoever committed it.
- No reading of GitHub's API, of `label-impact`'s manifest or of an
  artifact by code. The manifest was read by hand at open and the
  reviewer's seat copied from it, as the goldens were copied at M05.
- No call to the door. Grep `M03_DOOR`, `InitiateAuth`, `Bearer`,
  `execute-api`, `us-west-2_` and `amazonaws.com/` under `pages/`: no
  match.
- No change to `src/`, `goldens/` or `data/`. `git diff m00 --stat --
  src/baseline/` is empty on this branch (P5).
- No change to the three other pages or the three other served files.
  The sign-off page links to the three pages; it does not change them.
- No workflow. `gate.yml`, `m01.yml`, `m02.yml`, `m03.yml`,
  `m03-lift.yml`, `m04.yml`, `m05.yml` and `m05-lift.yml` are
  unchanged. The M03, M04 and M05 gates run on this PR and read their
  own files by path; whatever they read is a reading after their
  measurements and reopens no row (M03 `rulings/pr4.md` 6, 22; M04
  `rulings/pr4.md` 22; M05 `rulings/pr4.md` 3).
- No answer on a page. The sign-off page shows no answer, no row and no
  clause; a sign-off is not an answer.
- No number on a page that is a result. The page's numbers are the
  sign-off's id, SPEC/00's section numbers, the seat count SPEC/00 §5
  states, and the manifest's commit (M03 `rulings/pr4.md` 7).
- No brand name. No word of SPEC/00 §11's six. No treatment answer. No
  function signing that has no seat behind it: Regulatory Affairs is
  the function SPEC/00 §5 maps to `product`, and the login is the
  manifest's.
- No edit under `milestones/M05/`. The M05 call count is corrected in
  #32, its own PR outside any cap (`milestones/adoption/rulings/m05-count.md`),
  which shares no file with this one.

### What a reader can falsify

- `git diff main --stat` on this PR touches `pages/api/sign-off.json`,
  `pages/sign-off.html`, `milestones/README.md`,
  `milestones/M06/README.md` and `milestones/M06/rulings/pr1.md` only.
- In `pages/api/sign-off.json`, the one entry has `"signed": true`,
  `"signature": null`, `"package": null`, `"scripted": true` and a
  `PLANT` key. Its `reviewer.login` equals `seats.product` in
  `agentkeel-studio/label-impact`'s `manifest.yaml` at `956cd87`, and
  its `reviewer.function` is the function SPEC/00 §5 maps to `product`.
- In `pages/sign-off.html`, the JSON inside `<script
  type="application/json" id="signoff-s-001">` parses to the same object
  as the file's `s-001` entry. The banner above it says the page is
  scripted, nothing was signed and there is nothing to download.
- The page says the sign-off is not an agentkeel seat and not a
  platform control, and that one person holds all seven seats.
- The page carries none of "validated", "compliant", "Part 11",
  "governed", "secure" or "proven", and no brand name (SPEC/00 §2, §11).
- The page has no `id="answer"`, `id="baseline-answer"`,
  `id="agent-answer"` or `id="scenario-g-…"` block, so no earlier gate's
  block pattern matches it; each reads its own page by path in any case.
- No file exists under `pages/evidence/` on this branch.
- `git diff m00 --stat -- src/baseline/` on this branch is empty (P5).
- `git ls-files --eol` reads `i/lf w/lf` on every file this PR adds.

### Carried to PR 2

PR 2 is the measure. It adds the gate that reads the plant and nothing
that lifts it. It reads GitHub's API with the workflow's own token and
nothing of the door.

- **The read.** The gate reads `pages/api/sign-off.json` and the
  `id="signoff-<id>"` blocks of `pages/sign-off.html`. It names every
  sign-off shown as signed whose `signature` is null or lacks a field,
  or whose `package` is null or names a file that is not in the
  checkout (`signoffs_unsigned`), and every page sign-off that is not
  equal, as parsed JSON, to the file's entry of that `id`, or that the
  file does not serve (`signoffs_disagreed`). RED on either is a read of
  the served files alone, before any network, as M03 Unsure 4 ruled for
  the call record.
- **The signing commit.** For each signed sign-off the gate reads the
  commit that last changed `pages/api/sign-off.json` (`git log -1
  --format=%H -- pages/api/sign-off.json` in the checkout, fetched with
  full depth) and `GET /repos/andaro74/pharmadelta/commits/<sha>` with
  `GITHUB_TOKEN`, takes `author.login`, `commit.author.date` and
  `commit.verification`, reads `label-impact`'s `manifest.yaml` at the
  commit the reviewer record names and compares `seats.<seat>` with the
  login and the function with SPEC/00 §5's table. A mismatch reads
  `signoffs_differing`. Whether `verification.verified` must be true is
  Unsure 1.
- **The package.** The gate hashes the package file named in the record
  and compares the SHA-256 with the one the signature names; then reads
  the package's own manifest of entries and, for each, downloads the
  artifact of the run it names (`GET
  /repos/andaro74/pharmadelta/actions/runs/<id>/artifacts`, then the
  archive) and compares the entry's bytes with the artifact's file of
  the same name. A difference reads `signoffs_differing`; an artifact
  that cannot be downloaded (expired after 90 days, or the token refused)
  reads `unreadable` (Unsure 7).
- **The records' fields, proposed.** `signature`: `over` (the package's
  SHA-256), `by` (the login expected), `method` (the sentence "the last
  commit that changed pages/api/sign-off.json, read from GitHub's API"),
  `read_back` (what the gate read: `commit`, `author_login`,
  `authored_at`, `verified`, `read_from`), written by the gate into
  `result.json` and copied to the record at the lift. `package`: `file`
  (the path under `pages/`), `sha256`, `built_by` (the run and the
  artifact that built it), `commit` (this repository's commit the
  package describes), `entries` (each with `path`, `sha256`, `run_url`,
  `artifact`, `ledger_row`), `written_by_ci` true. Fixed at PR 2 or at
  the lift, not here (Unsure 5).
- **The package's contents, proposed.** `milestones/README.md` at the
  package's commit; `SPEC/00-overview.md`; `goldens/`; the four served
  files under `pages/api/`; `label-impact`'s `manifest.yaml` at the
  agent commit the served files name; and the `result.json` of the run
  each ledger row's Measured cell cites (rows 0, 1, 2, 4, 5, 6), with
  the M00 run's `observations.json`; a `manifest.json` listing each
  entry with its SHA-256 and source. The M00 result carries the
  baseline's report on scenarios 5 and 6 (M05 Unsure 12, ruled at this
  PR: yes, from the artifact, with its link). The form, one zip plus
  its manifest, is Unsure 6.
- **The verdict.** `signoffs_unsigned`, `signoffs_disagreed`,
  `signoffs_differing`, `unreadable`, `written_by_ci`, as the row's
  expected output says. Exit 0 GREEN, 1 RED, 2 UNSCORABLE.
- **The artifact.** `m06-gate-<sha>`, holding `result.json`, 90 days,
  as the other gates. No door host is read, so no host grep is needed;
  the token is the workflow's and is written nowhere (Unsure 8).
- **No lift.** PR 2 serves nothing new. The lift's shape is M03's with
  one difference: the package is built by CI and written as an artifact,
  but the signing commit is the reviewer's own, made by hand, because a
  commit by CI is not a reviewer's signature (Unsure 1, 15).

### Platform items (flagged here, built in agentkeel, waited for)

Per CLAUDE.md "Platform changes": named, never designed here.

1. **None new.** SPEC/00 §5 puts the sign-off in this repository's
   website layer; it is not a platform control and asks nothing of
   agentkeel. If a later milestone wants the platform to read the
   sign-off, that is agentkeel's to design.
2. **The registry read** (M01 Unsure 12, M03 row P item 1): unchanged,
   not investigated here.

### Rulings carried from earlier milestones

| # | Ruled |
|---|---|
| M01's 23 (ruled at M02 PR 1) | The Measured cell cites the run on `main` after PR 2 merges, with the PR run named beside it when it was the one read at the time. Row 7's expected gate output says so. |
| M05's 2 (M04's and M03's 2; carried at M05 PR 4, `rulings/pr4.md` 15) | GitHub Pages is not enabled; "public" has meant readable in the repository. **Ruled at this PR** (`rulings/pr1.md` 8): the milestone does not depend on Pages; "downloadable" means a file in the repository fetched by its GitHub URL; the setting is the owner's and is carried to no further milestone by name. Unsure 2 below records the read. |
| M05's 3 (M04's 16, M03's 16, M02's 16; carried at M05 PR 4, `rulings/pr4.md` 16) | The M02 to M05 gates as required checks on `main` are the owner's setting. **Ruled at this PR** (`rulings/pr1.md` 9): no Measured cell depends on a required check, since each cites a run on `main`; `M00 gate` stays the one required check; whether `M06 gate` joins is recorded at PR 4 for the record only; carried to no further milestone by name. Unsure 3 below records the read. |
| M05's 12 (carried at M05 PR 4, `rulings/pr4.md` 14) | The baseline's report on scenarios 5 and 6 is the M00 scorer's artifact. **Ruled at this PR** (`rulings/pr1.md` 10): the evidence package carries the M00 gate's `result.json` of the run row 0's Measured cell cites, with its link, which scores `g-005` and `g-006` as answered, not blocked. |
| M03's 7 (ruled at M03 PR 4, `rulings/pr4.md` 8) | A golden's id, a row's and a clause's data and a CI record's time and id are not measured numbers. Applied to the sign-off page, which carries the sign-off's id, SPEC/00's section numbers, the seat count and the manifest's commit. |
| M03's 6 and 22, M04's 22, M05's 3 (ruled at their PR 4) | A reading of the M03, M04 or M05 gate after its measurement never reopens row 4, 5 or 6. Their readings on this PR are recorded in the PR, not in a ledger cell. |
| M03's 1 (ruled at M03 PR 4, `rulings/pr4.md` 7) | The public API is a read API: a served file of records. The sign-off page's served file is the same kind; the one record not written by CI is the signature, which is the reviewer's own commit (Unsure 1). |
| M05's 39, 47, 48 (`milestones/adoption/rulings/m05-count.md` 3) | A count in a commit message or a comment that a later read corrected is corrected in the README, not rewritten. This PR's messages carry no call count. |

## Open detail (PR 2, 2026-11-08 UTC)

PR 2 is the measure. It adds the gate that reads the plant and nothing
that lifts it. `pages/api/sign-off.json` serves one sign-off shown as
signed with `signature` null and `package` null at the head this PR
measures, and `pages/sign-off.html` shows it. M06 is measured here.

### What this PR holds

- `src/m06/gate.py`, the gate. Python 3.14; the standard library and
  `pyyaml`, which `pyproject.toml` already lists for the ingest;
  `pyproject.toml` and `uv.lock` are unchanged. Nothing is imported from
  `src/m03/` or `src/m05/`: no sign-in, no door, no secret of M03's. In
  order:
  1. Reads `pages/api/sign-off.json` (the `signoffs` list) and the JSON
     in each `<script type="application/json" id="signoff-<id>">` block
     of `pages/sign-off.html`, one object per block, with the block's own
     id beside it.
  2. `signoffs_unsigned`: every served sign-off shown as signed (`signed`
     true) whose `signature` is null, is not an object, lacks a field of
     the signature record (below) or holds it empty, or whose `over` is
     not a SHA-256; or whose `package` is null, is not an object, lacks a
     field of the package record or of an entry, whose `sha256` is not a
     SHA-256, whose `written_by_ci` is not true, whose `built_by.run_url`
     is not a run on github.com, or whose `file` is not a file under
     `pages/` in the checkout. A read of the served file; no network.
  3. `signoffs_disagreed`: every page sign-off whose `id` the file does
     not serve, whose block is not named `signoff-<its id>`, or that is
     not equal to the file's entry of that `id` as parsed JSON in
     canonical form (sorted keys, no whitespace; M03 Unsure 15's reading).
  4. For each sign-off that carries both records, and for no other, the
     read-back: the commit that last changed the served file, from git;
     that commit from GitHub's API; `label-impact`'s manifest at the
     commit the reviewer record names; the package file's hash, its zip,
     its entries against their sources; the file against the artifact of
     the run that built it ("The read-back, as built").
  5. `signoffs_differing`: every such sign-off with a difference. A read
     that could not be made is `unreadable` and decides nothing.
  6. Writes `result.json` and exits 0 GREEN, 1 RED, 2 UNSCORABLE.
- `.github/workflows/m06.yml`: on every pull request, every push to
  `main` and by hand, as `m05.yml`. `actions/checkout@v7` with
  `fetch-depth: 0`, the first full-depth checkout in this repository,
  because the gate asks git which commit last changed the served file
  and a shallow checkout answers with its own head. `uv sync --locked`,
  the artifact directory, the gate with `GITHUB_TOKEN` in its `env` and
  nothing else; then a step that greps the result directory for a
  token's prefix (`ghs_`, `ghp_`, `github_pat_`) and fails on a match;
  then the artifact `m06-gate-<sha>` holding `result.json`, 90 days,
  uploaded only when the grep step passed. `permissions` is `contents:
  read` and `actions: read`, the second for this repository's artifacts.
  The job fails on anything but GREEN. `gate.yml`, `m01.yml`, `m02.yml`,
  `m03.yml`, `m03-lift.yml`, `m04.yml`, `m05.yml` and `m05-lift.yml` are
  unchanged.
- `result.json` records `verdict`, `signoffs_unsigned`,
  `signoffs_disagreed`, `signoffs_differing`, `unreadable`, `commit`,
  `dirty`, `written_by_ci`, `ci`, the API base, SPEC/00 §5's seat table
  as the gate holds it (`seat_function`), the four records' fields, how
  the signature is read (`signature_reading`, with `verified_required`
  false), whether the environment held the token (`env_set`, a boolean),
  per served sign-off its record checks, page equality and read-back
  (`served`), the page's blocks (`page`) and every artifact listing and
  download made (`artifacts_read`: run, artifact, statuses, `expired`,
  `expires_at`, the files), so the file says for itself whether it is
  evidence (P4). No token, no redirect URL.
- `rulings/pr2.md`, and "PRs used / cap" set to 2 / 4 here and in the
  ledger.

### The read-back, as built

For a sign-off that carries both records. Nothing here runs on the
plant.

| Read | From | Decides |
|---|---|---|
| the function shown | `reviewer.function` against SPEC/00 §5's table, held in the gate as `SEAT_FUNCTION` | differing when it is not the seat's, or the seat is not one of the seven |
| the signing commit | `git rev-parse --is-shallow-repository`, then `git log -1 --format=%H -- pages/api/sign-off.json` | unreadable when the checkout is shallow or git names no commit |
| the commit's record | `GET /repos/andaro74/pharmadelta/commits/<sha>`: `author.login`, `committer.login`, `commit.author.date`, `commit.verification` | differing when `author.login` is null, or is not `reviewer.login`, or not `signature.by`; unreadable when the API does not answer 200 with an object |
| the seat's login | `GET /repos/agentkeel-studio/label-impact/contents/manifest.yaml?ref=<reviewer.seat_read_from.commit>`, base64, YAML, `seats.<seat>` | differing when it is not `reviewer.login`, or not the commit's `author.login`; unreadable when the API does not answer or the file is not YAML with `seats` |
| the package file | SHA-256 of the bytes under `package.file` | differing when it is not `signature.over` or not `package.sha256` |
| the package's zip | `zipfile`; its `manifest.json` as parsed JSON against `package.entries` | differing when the file is not a zip, holds no `manifest.json`, or the two are not equal in canonical form |
| each entry | the member at `path`, hashed; then its source: `artifact` (the run's artifact listing, the archive, the file `name` in it), `repository` (`git show <commit>:<name>`), or `agent` (the contents API on label-impact at `<commit>`) | differing when the member is missing, hashes to other than `sha256`, or is not byte-equal to its source; unreadable when the artifact has expired, the archive or the API did not answer, or the commit is not in the checkout |
| the build | `package.built_by`: the run's artifact, the file in it named as the package file | differing when the bytes are not the package file's; unreadable when it cannot be downloaded |
| `verification.verified` | the commit's record | recorded; not required (Unsure 1, ruled) |

An artifact is listed and downloaded once per run and read from memory
after that. The archive's request answers 302 to a blob store; the gate
does not let `urllib` follow it, fetches the `Location` itself without
the token, and writes that URL nowhere. Bodies are capped at 64 MB. The
artifact's `expired` and `expires_at` are recorded as listed.

### The records' fields (Unsure 5, ruled)

Fixed here; the lift writes them. A field present and empty is missing.

- `signature`: `over` (the package file's SHA-256, 64 hex digits), `by`
  (the login expected: the seat holder's), `method` (the sentence "the
  last commit that changed pages/api/sign-off.json, read from GitHub's
  API"), `read_from` (the API path the gate reads, `GET
  /repos/andaro74/pharmadelta/commits/<sha>`). PR 1 proposed a fifth
  field, `read_back`, holding what the gate read of the signing commit.
  It is not in the record: the signing commit is the commit that changes
  this file, so its own sha, login and time cannot be written into it.
  The read-back is in the gate's `result.json`, CI-written; a page that
  shows it shows it from that result with the run's link (SPEC/00 §11;
  Unsure 18).
- `package`: `file` (a path under `pages/`), `sha256`, `built_by`
  (`run_url`, `artifact`: the CI run and artifact that wrote the file),
  `commit` (this repository's commit the package describes), `entries`
  (a non-empty list), `written_by_ci` (true).
- each entry: `path` (in the zip), `sha256`, `source` (`artifact`,
  `repository` or `agent`), `run_url` and `artifact` and `name` (for an
  artifact source: the run on github.com, the artifact's name, the file
  in it), `commit` and `name` (for a repository source: this repository's
  commit and path; for an agent source: label-impact's commit and path),
  `ledger_row` (the row the entry is evidence for, or null). Every key
  present on every entry; null where the source does not use it.

### The package's form (Unsure 6, ruled)

One zip under `pages/evidence/`, named in `package.file`, fetched by its
GitHub URL (PR 1 ruling 8). Inside, `manifest.json` equal to
`package.entries`, and each entry at its `path`. Three sources: this
repository's CI artifacts (the `result.json` each Measured cell cites,
the M00 run's `observations.json`), this repository at `package.commit`
(the ledger, SPEC/00, the goldens, the four served files), and
`label-impact`'s repository at the agent commit the served files name
(`manifest.yaml`). The third source needed a read the proposal did not
name: label-impact is not in the checkout, so the gate reads it through
the contents API, which returns content for files under 1 MB (Unsure
23). A zip in git is accepted: it is one file, downloadable by one URL,
and its hash is what is signed; the M02 artifact is 142 KB and the rest
under 4 KB. Which files go in is the lift's (Unsure 16 carried); the
gate accepts any entries whose sources it can read.

### The verdict

- **RED** when `signoffs_unsigned`, `signoffs_disagreed` or
  `signoffs_differing` is non-empty. The first two are reads of the
  served files and come before any network, so the plant reads RED
  whatever GitHub's API says that day (M03 Unsure 4's rule).
- **GREEN** only when every sign-off shown as signed carries both
  records, the commit that last changed the served file is the seat
  holder's own by `author.login` and the manifest, the function shown is
  the seat's, the package hashes to what was signed and every entry
  equals its source, the file is what its build wrote, every page
  sign-off is the file's entry, and nothing was unread.
- **UNSCORABLE** when nothing is RED and: a served file could not be
  read or parsed, the file serves no sign-off or one id twice, or a
  read-back could not be made (the checkout shallow, the API not
  answering, the manifest not YAML, an artifact expired or not
  downloadable, a commit not in the checkout, the read-back raising).
  Never RED, never GREEN.
- A read-back that cannot be made on a sign-off that also differs
  leaves the RED standing: `unreadable` is recorded beside it (M05 PR 3's
  rule, built in).
- A sign-off shown as not signed (`signed` not true) is named by no
  list, whatever its records (M05 Unsure 17's reading; Unsure 24).

### What this PR does not hold

- No lift. `git diff 6cfc1eb main -- pages/` and `git diff main --
  pages/` are empty: the one entry carries `signature` null, `package`
  null, `scripted` true and the `PLANT` key as at `6cfc1eb`, and the page
  keeps its scripted banner. No file under `pages/evidence/`.
- No edit to `src/m03/`, `src/m04/` or `src/m05/`: the gate imports
  nothing from them. No change to `src/baseline/` (P5; `git diff m00
  --stat -- src/baseline/` is empty), `src/gate/`, `src/ingest/`,
  `src/m01/`, `goldens/`, `data/`, `pyproject.toml`, `uv.lock`, the
  other eight workflows, SPEC/00, CLAUDE.md, the README, or anything
  under `milestones/M00/` to `milestones/M05/` or `milestones/adoption/`.
- No secret and no variable. Grep `secrets.` in
  `.github/workflows/m06.yml`: one match, `secrets.GITHUB_TOKEN`, in the
  gate step's `env`. Grep `vars.`: no match. Grep `M03_DOOR`,
  `InitiateAuth`, `Bearer`, `execute-api`, `us-west-2_` and
  `amazonaws.com/` under `src/m06/` and the workflow: one match, the
  word `Bearer` in the gate's own `Authorization` header to GitHub's API.
  Grep `https://` under `src/m06/`: the API base `https://api.github.com`
  and the run URL pattern `https://github.com/`, nothing else.
- No design of a signature. The gate reads GitHub's record of a commit
  and label-impact's manifest as they are; it defines no field of
  either.
- No change to label-impact or to agentkeel. No platform item is new.
- No "Measured" cell and no tag. Those are PR 4's.
- No number on a page: no page changes here. No word of SPEC/00 §11's
  six. No brand name. No treatment answer: the gate shows nothing and
  asks no agent anything.

### Construction run (not evidence, P4)

Run on 2026-11-08 UTC on the branch before the first push, from the
working tree, so `written_by_ci` is false and the tree was dirty.
Readings, in order:

| Reading | What was read |
|---|---|
| the gate on the real pages with no token | `RED`, `signoffs_unsigned` `["s-001"]` (`signature is null`, `package is null`), `signoffs_disagreed` `[]`, `signoffs_differing` `[]`, `unreadable` `[]`; the one page sign-off equal to the file's entry; `read_back` null, `not_read_back` "no signing record"; `artifacts_read` `[]`; `env_set` false; exit 1. `result.json` grepped for `ghs_`, `ghp_`, `github_pat_`, `execute-api` and `us-west-2_`: no match |
| fifty-two made-up pairs of files in the session's scratch directory, every git and API read stubbed, a made-up zip of four entries (two from artifacts, one from this repository, one from label-impact), not committed | the plant: `RED`, unsigned `s-001`, nothing read back. A lifted entry with every read equal: `GREEN`, exit 0, `verified` false recorded. The commit by another login, or matched to no login; the manifest holding another login for the seat; the function not the seat's; a seat not of the seven; the signature over another hash; the record's hash differing; the file altered; an entry differing from its artifact, from this repository, from label-impact; the file not what its build wrote; the build artifact lacking the file; an entry missing from the zip; `manifest.json` not the entries; the file not a zip: each `RED`, `signoffs_differing` `["s-001"]`, with the difference named. An artifact expired; the archive answering 403; the commit's API answering 403; the manifest 404; label-impact's file 404; the checkout shallow; a repository file not in the checkout; the read-back raising; the page without a block on a lifted entry: each `UNSCORABLE`, exit 2, `unreadable` naming it, the lists empty. An expired artifact beside a commit by another login: `RED`, differing, `unreadable` beside it. The page's `signed` flipped: `signoffs_disagreed` `["s-001"]`. The page showing `s-999`: disagreed `["s-999"]`. The block misnamed: disagreed. The page without a block on the plant: `RED`, unsigned, `unreadable` names the page. A signature lacking `method`, `over` not a hash, the signature a string; the package file missing, or under `src/`; `written_by_ci` false; `entries` empty; an entry lacking `name` or with source `web`; `built_by.run_url` off github.com; the package lacking `commit`: each `RED`, `signoffs_unsigned` `["s-001"]`, nothing read back. A sign-off shown as not signed, alone: `GREEN`; beside the plant: unsigned `["s-001"]` only. Zero served, the file not JSON, one id twice: `UNSCORABLE` by the refusal path. The block pattern on the real pages: `s-001` on `sign-off.html`; nothing on `break-it.html`, `detail.html`, `side-by-side.html` |
| the gate's own transport, with the owner's `gh auth token` in the environment of one process, on real records; the token typed nowhere and printed nowhere | `read_commit` on `6cfc1eb`: 200, `author.login` `andaro74`, `committer.login` `andaro74`, `2026-11-08T02:57:19Z`, `verified` false, reason `unsigned`; the same without a token: 200. `read_manifest_seat` on label-impact at `956cd87`: 200, blob `4d6d126…`, `seats.product` `andaro74`, seven seats. `Artifacts.get` on run 41266122812, artifact `m05-gate-8734adb…`: listing 200, `expired` false, `expires_at` 2027-01-30, archive 200 through the 302 with the token withheld, one file `result.json`, 3781 bytes zipped, `verdict` `RED` inside. `read_last_commit`: `6cfc1eb…` from a full checkout. `git show 6cfc1eb:pages/api/sign-off.json`: read. The recorded reads hold no token |

No defect was found by the fifty-four readings. The stub files and the
script live in the session's scratch directory and are not committed
(M01 Unsure 21's reading: no test file).

### Expected CI result on this PR

The ledger row says: RED, `signoffs_unsigned` `["s-001"]`,
`signoffs_disagreed` `[]`, `signoffs_differing` `[]`. The CI run on this
PR is expected to write that, with `unreadable` `[]`, `written_by_ci`
true, `env_set` true, `artifacts_read` `[]`, no read-back made, and the
run URL, and to fail the `M06 gate` job (exit 1). On the same head
`M00 gate` and `M02 gate` are expected GREEN, `M01 gate` PENDING, exit
3, not required (M01 Unsure 14), and `M03 gate`, `M04 gate` and
`M05 gate` whatever they read on `main` at `6a3840b` (all passed there:
runs 42442496159, 42442496213, 42442496230): readings after their
measurements, named in a PR comment, not in a cell (PR 1, Unsure 11).
The CI run is the measurement; the construction run decides nothing.

### Observed (CI run, 2026-11-08 UTC)

The first run on this PR,
[42491031888](https://github.com/andaro74/pharmadelta/actions/runs/42491031888),
wrote the artifact `m06-gate-8431885faa0353ebf43d56ea244df4bb98ca8c6b`
(the sha is the pull request's merge ref, as M00's to M05's were; the
branch head was `18d9103`). It holds `result.json`, read with `gh run
download` into a fresh directory and `python -I` in this session:

| Field | Value |
|---|---|
| `verdict` | `RED`; `reason` "F6.1 holds: sign-offs s-001 are shown as signed with no signing record or no package record naming a file in the repository" |
| `signoffs_unsigned` | `["s-001"]`: `signature is null`, `package is null` |
| `signoffs_disagreed` | `[]`: the one page sign-off equals the file's entry as parsed JSON, in the block named for its id |
| `signoffs_differing` | `[]`: nothing read back, `read_back` null, `not_read_back` "no signing record" |
| `unreadable` | `[]` |
| `env_set` | `{"token": true}`; no value of it in the file. The workflow's grep step (`ghs_`, `ghp_`, `github_pat_`) passed before the upload; the downloaded file grepped again here for those and for `execute-api`, `us-west-2_`, `amazonaws.com/`: no match |
| `artifacts_read` | `[]`: no listing, no download; GitHub's API was not asked anything for the plant |
| `signature_reading.verified_required` | `false` |
| `written_by_ci` | `true`; `commit` `8431885`, `dirty` false; `event` `pull_request`, `ref` `refs/pull/34/merge`; `run_at` `2026-11-08T14:41:31+00:00`; exit 1; the `M06 gate` job failed at the gate step, the grep step and the upload step succeeded. The artifact is 1727 bytes zipped, `result.json` 4068 bytes, `expires_at` 2027-02-06. On the same head `M00 gate` passed ([42491031843](https://github.com/andaro74/pharmadelta/actions/runs/42491031843)), `M02 gate` passed ([42491031811](https://github.com/andaro74/pharmadelta/actions/runs/42491031811)), `M01 gate` failed, not required ([42491031845](https://github.com/andaro74/pharmadelta/actions/runs/42491031845)) |

Equals the expected result above on every field the ledger row names.
The plant is named as ledger row 7 expects: the RED is the missing
signing record and the missing package record, nothing else. No network
read was made, so what GitHub's API, the manifest or an artifact would
have said that day decided nothing (M03 Unsure 4's rule).

The `M03 gate` on the same head,
[42491031831](https://github.com/andaro74/pharmadelta/actions/runs/42491031831),
artifact `m03-gate-8431885faa0353ebf43d56ea244df4bb98ca8c6b`, read
`GREEN`: `answers_uncalled` `[]`, `answers_disagreed` `[]`,
`answers_differing` `[]`, `unreadable` `[]`; sign-in 200; the door 200,
`stop_reason` `end_turn`, `parsed` null. The `M04 gate`,
[42491031860](https://github.com/andaro74/pharmadelta/actions/runs/42491031860),
artifact `m04-gate-8431885faa0353ebf43d56ea244df4bb98ca8c6b`, read
`GREEN`: `answers_unrun` `[]`, `answers_disagreed` `[]`,
`answers_differing` `[]`, `agent_disagreed` `[]`, `baseline_changed`
false, `unreadable` `[]`. The `M05 gate`,
[42491031806](https://github.com/andaro74/pharmadelta/actions/runs/42491031806),
artifact `m05-gate-8431885faa0353ebf43d56ea244df4bb98ca8c6b`, read
`GREEN`: `scenarios_untraced` `[]`, `scenarios_disagreed` `[]`,
`scenarios_differing` `[]`, `unreadable` `[]`; sign-in 200; the door
stopped g-005 under `treatment-or-dosing-advice` and g-006 under
`instruction-to-assistant-in-pasted-document`, `stop_reason`
`guardrail_intervened` on both, as the re-lifted break page serves. All
three are readings after their measurements; none reopens row 4, 5 or 6
(M03 `rulings/pr4.md` 6, 22; M04 `rulings/pr4.md` 22; M05
`rulings/pr4.md` 3). Recorded here and in a comment on #34, not in a
ledger cell. The push that adds this section runs every gate again; the
second `M06 gate` run is read into the same comment.

### What a reader can falsify

- The artifact `m06-gate-<sha>` on this PR's run holds `result.json`
  with `verdict: RED`, `signoffs_unsigned: ["s-001"]`,
  `signoffs_disagreed: []`, `signoffs_differing: []`, `unreadable: []`
  and `written_by_ci: true`. Download it and read it.
- In that `result.json`, `env_set` is one boolean; `served[0].read_back`
  is null and `artifacts_read` is `[]`: nothing was fetched for the
  plant. Grep it for `ghs_`, `ghp_` and `github_pat_`: no match (the
  workflow's grep step passed, or there would be no artifact).
- `git diff main --stat` on this PR touches `src/m06/`,
  `.github/workflows/m06.yml`, `milestones/README.md`,
  `milestones/M06/README.md` and `milestones/M06/rulings/pr2.md` only.
  `git diff main -- pages/ src/m03/ src/m04/ src/m05/ src/baseline/
  pyproject.toml uv.lock` is empty.
- Grep `secrets.` in `.github/workflows/m06.yml`: one match,
  `GITHUB_TOKEN`. Grep `fetch-depth: 0`: one match. Grep `actions: read`:
  one match. Grep `from src.m0` in `src/m06/gate.py`: no match.
- In `src/m06/gate.py`, `SIGNATURE_RECORD`, `PACKAGE_RECORD`,
  `BUILT_BY` and `ENTRY_RECORD` hold the names above; `SEAT_FUNCTION` is
  SPEC/00 §5's table, seven rows; `signature_record_check({"signature":
  None})["has_record"]` is false; `PAGE_BLOCK` matches the one block of
  `pages/sign-off.html` and nothing in the three other pages.

### After this PR goes RED

The plant is lifted by the one change named under "The false state": a
package built by this repository's CI from the sources above and written
as an artifact, its zip committed under `pages/evidence/`; then the seat
holder's own commit that fills `signature` and `package` with the records
above, sets `scripted` false, removes the `PLANT` key and rebuilds the
page from the file. Which PR carries the lift is ruled on reading this
PR's CI run, as M03's, M04's and M05's were at PR 2. Proposed: PR 4, by
M03's path (b) with one difference: the package is written by a CI run
with `permissions: contents: read` and committed by hand, and the
signing commit is the reviewer's own, by hand, because a commit by CI is
not a reviewer's signature (Unsure 1, 15). PR 3, if the cold review of
this PR finds anything, repairs and does not lift; if it finds nothing,
PR 3 is skipped. Ruled in `rulings/pr2.md` on reading the run.

**Ruled at PR 2, on reading run 42491031888 (Product).** The lift is
carried by PR 4, as M00's to M05's were, by M03's path (b) with one
difference: a CI run with `permissions: contents: read` builds the
package from the sources under "The package's form" and writes it as an
artifact; the zip is committed under `pages/evidence/` by hand with its
hash; then the seat holder's own commit, by hand, fills `signature` and
`package`, sets `scripted` false, removes the `PLANT` key and rebuilds
the page from the file, so the commit that last changed the served file
is the reviewer's (Unsure 1, 15). PR 3, if the cold review of #34 finds
anything, repairs and does not lift; if it finds nothing, PR 3 is
skipped. The Measured cell takes the `main` run after #34 merges (M01
Unsure 23, ruled at M02 PR 1), which reads as run 42491031888 did on the
three lists: the plant makes no network read. Which files the package
carries is Unsure 16, fixed in the lift PR's first commit before any
page is written (`rulings/pr2.md` 17).

## Open detail (PR 3, 2026-11-08 UTC)

PR 3 is the repair. It holds what the cold review of #34 found in
`src/m06/gate.py`, and nothing that lifts the plant: `pages/` is
unchanged, `pages/api/sign-off.json` still serves `s-001` with
`signature` null and `package` null, and the gate on this PR must read
RED with the same lists as #34's runs. Nothing here decides the row: the
`main` run after #34 merged is the measurement, read first in this
session, and PR 4 fills the "Measured" cell from it.

### The `main` run after #34 (the Measured cell's source, M01 Unsure 23)

Run [42495856254](https://github.com/andaro74/pharmadelta/actions/runs/42495856254),
`push` on `main` at `e175d77` (the merge commit of #34), conclusion
failure, wrote the artifact
`m06-gate-e175d772bd32ce9e148f79b868b72a2dcfa8b24f` (1726 bytes zipped,
`result.json` 4058 bytes, `expires_at` 2027-02-06T15:38:48Z). Read with
`gh run download` into a fresh directory and `python -I` in this session:

| Field | Value |
|---|---|
| `verdict` | `RED`; `reason` "F6.1 holds: sign-offs s-001 are shown as signed with no signing record or no package record naming a file in the repository" |
| `signoffs_unsigned` | `["s-001"]`: `signature is null`, `package is null` |
| `signoffs_disagreed` | `[]`: the one page sign-off equals the file's entry as parsed JSON, in the block named for its id |
| `signoffs_differing` | `[]`: `read_back` null, `not_read_back` "no signing record" |
| `unreadable` | `[]` |
| `written_by_ci` | `true`; `commit` `e175d772bd32ce9e148f79b868b72a2dcfa8b24f`, `dirty` false; `event` `push`, `ref` `refs/heads/main`, `run_attempt` 1; `run_at` `2026-11-08T15:38:56+00:00` |
| `env_set` | `{"token": true}`; `artifacts_read` `[]`; `signature_reading.verified_required` false |
| the job | the gate step failed (exit 1), the grep step passed ("no match"), the upload step passed. The downloaded file grepped here for `ghs_`, `ghp_`, `github_pat_`, `execute-api`, `us-west-2_` and `amazonaws.com/`: no match |

Equals the PR runs 42491031888 (merge ref `8431885`) and 42491298504 on
every field the ledger row names. The Measured cell at PR 4 cites this
run and this artifact, with the PR run named beside it.

### Cold review of #34

`src/m06/gate.py` and `.github/workflows/m06.yml` read as a reader who
did not write them, against F6.1 and the row's expected output, in this
order: the three record checks and whether a field the lift must write
can be missing without reading unsigned; `read_back`'s `differences` and
`not_read` lists and whether anything after the served file was read can
raise instead of being recorded (M05 PR 3's rule); `http_get`'s redirect
handling; `read_last_commit` on a pull request's merge ref;
`package_file`'s path check; the `Artifacts` cache and the 64 MB cap; the
summary table on a lifted entry; the grep step's patterns; every field of
`result.json` that could hold a token or a redirect URL. Each candidate
was confirmed with made-up inputs in the session's scratch directory
before it was called a defect (construction, not evidence, P4; nothing
committed). Four defects and one hardening.

**Defect 1 (the verdict path).** `read_back` could raise after it had
recorded a difference. Four reads inside it were not guarded: the zip's
`manifest.json` (`zf.read`), each entry's member (`zf.read`), the build
artifact's member (`Artifacts.file`) and the package file's bytes
(`path.read_bytes`). A member with a bad CRC raises
`zipfile.BadZipFile`; an unsupported compression `NotImplementedError`;
an encrypted member `RuntimeError`; a corrupt stream `zlib.error`. The
exception left `read_back`, and `run()`'s handler replaced the whole
read-back with a record whose `differences` is `[]`, so a difference
found before the raise (the seat not one of the seven, the function not
the seat's, the author's login not the seat holder's, the hash not what
was signed) was dropped: the sign-off left `signoffs_differing`, and the
verdict was UNSCORABLE where `rulings/pr2.md` 16 says RED comes first.
Confirmed: a lifted entry with the seat `legal` and a package whose
member `a.json` has a bad CRC, the API unroutable: `UNSCORABLE`,
`signoffs_differing` `[]`, `unreadable` naming the raise, exit 2.

**Defect 2 (the verdict path).** `read_page` caught `OSError` only. A
page that is not UTF-8 raised `UnicodeDecodeError` (a `ValueError`) past
`run()`'s `except Unscorable` into `main`'s handler: UNSCORABLE with no
lists, exit 2, on the plant itself, after the served file had been read.
`read_served` catches `ValueError`; the page's reader did not. The page
holds "§", so a save in cp1252 is enough. Confirmed: the real served file
and `pages/sign-off.html` re-encoded in cp1252: `UNSCORABLE`,
`error.type` `UnicodeDecodeError`, no `signoffs_unsigned`.

**Defect 3 (a label).** The step summary's "package hash" column read
"equal" when the read-back record held no `package_file` (the record
`run()` writes on a raise): `None == None == None`. `result.json` was
right; the summary was not. Confirmed on Defect 1's stub: the row read
`equal` under "package hash" with nothing hashed.

**Defect 4 (what `result.json` could hold).** `http_get` wrote
`str(exc)[:120]` for every exception on every leg. On the redirect leg,
the blob store's, urllib's own messages quote the URL they refuse: a
relative `Location` raises `ValueError: unknown url type: '<url>'` and
one with a control character `http.client.InvalidURL: ... '<url>'`, and
that URL is the signed redirect. The message reached
`artifacts_read[].why`, `unreadable`, `result.json`, the step summary and
the job log, and the grep step's three prefixes do not match it. The same
function also returned the response's headers on every leg, `Location`
among them on a 3xx; no caller read them. A relative `Location` was not
resolved against the request's URL, so it read `unreadable`. GitHub's
redirect is absolute and well formed, and no run has taken this path: it
is what the file could hold, which Unsure 8 and 21 asked. Confirmed:
`urllib.request.Request("/blob/path?sig=…")` raises
`ValueError("unknown url type: '/blob/path?sig=…'")`, the text the old
leg wrote.

**Hardening 5.** `read_repository_file` ran `git show <commit>:<name>`
with any non-empty `commit` the entry named: a branch name is a moving
target the record calls a commit, and a string beginning `-` reaches git
as an option. `read_agent_file` already required 7 to 40 hex digits. No
served entry exists, so no verdict could have turned on it.

Read and found nothing: the three record checks name a sign-off unsigned
when any field of `SIGNATURE_RECORD`, `PACKAGE_RECORD`, `BUILT_BY` or
`ENTRY_RECORD` is absent, null or empty, a hash is not 64 hex digits,
`written_by_ci` is not true, a run URL is off github.com, a source is
not one of three, or the file is not under `pages/` in the checkout
(absolute paths, `..` and a symlink out of `pages/` resolve outside and
read None); `package.commit` is checked present and read back by nothing
(Unsure 29). `read_last_commit` on a merge ref reads as Unsure 22
records. The `Artifacts` cache lists and downloads once per run and
artifact, records `expired` and `expires_at` as listed, and a body over
64 MB is a `ValueError` recorded by type. The grep step's prefixes are
Unsure 21's; a GitHub login cannot hold `_` and a hex digest cannot hold
`ghs_`, so a match can only be a token or a package entry's path (Unsure
31). `env_set` is one boolean. `m06.yml` is unchanged by this PR.

### The repair

`src/m06/gate.py` only. In order:

- `read_page` catches `(OSError, ValueError)` and raises `Unscorable`,
  as `read_served` does; `run()` records it under `unreadable` and the
  lists stand (Defect 2).
- `zip_member(zf, member)` reads one member and returns its bytes or why
  it could not be read, by the exception's type and message. The zip's
  `manifest.json`, each entry's member and the build artifact's member go
  through it; a member that cannot be read is `not_read` for that entry
  (`equal` null), never a raise (Defect 1).
- The package file's `read_bytes` is guarded: a file that was in the
  checkout when the record was checked and cannot be read now is a read
  not made, recorded under `not_read`, and the hash, zip and build
  comparisons that need its bytes are skipped (Defect 1).
- `read_back` is now a wrapper around `_read_back`: the `differences`
  and `not_read` lists are created outside the call, so a raise inside
  it is appended to `not_read` and the differences found before it stand.
  `run()` keeps its own `except` as a last fence (Defect 1).
- `http_get` returns no headers on any leg; a `Location` is resolved with
  `urllib.parse.urljoin` against the request's URL before the redirect
  leg; on the redirect leg (`follow` false) an exception is recorded by
  its type alone. The API leg keeps the type and a short message, since
  the API URL holds no token and no redirect (Defect 4).
- `read_repository_file` requires 7 to 40 hex digits for `commit`, as
  `read_agent_file` does, and reads `unreadable` otherwise (Hardening 5).
- The summary's "package hash" column reads "not read" when the
  read-back holds no hash (Defect 3).
- The module docstring says what is guarded.

No change to the lists' names, the records' fields, `SEAT_FUNCTION`, the
verdict's shape, the exit codes, the workflow or the artifact's name.
`import urllib.parse` is the one new import; it is the standard library.
`pyproject.toml` and `uv.lock` are unchanged.

### What this PR does not hold

- No lift. `git diff main -- pages/` is empty; no file under
  `pages/evidence/`; `signature` null, `package` null, `scripted` true
  and the `PLANT` key stand at `6cfc1eb`'s values.
- No change to `.github/workflows/m06.yml` or any other workflow, to
  `src/m03/`, `src/m04/`, `src/m05/`, `src/baseline/` (P5; `git diff m00
  --stat -- src/baseline/` is empty), `src/gate/`, `src/ingest/`,
  `src/m01/`, `goldens/`, `data/`, SPEC/00, CLAUDE.md, the README, or
  anything under `milestones/M00/` to `milestones/M05/` or
  `milestones/adoption/`.
- No secret, no variable, no door string. Grep `M03_DOOR`,
  `InitiateAuth`, `execute-api`, `us-west-2_` and `amazonaws.com/` under
  `src/m06/`: no match; `Bearer` once, the gate's own header to GitHub's
  API, as at PR 2.
- No "Measured" cell and no tag. Those are PR 4's.
- No page change, so no number on a page. No word of SPEC/00 §11's six.
  No brand name. No treatment answer.

### Construction readings on this PR (not evidence, P4)

Run on 2026-11-08 UTC from the working tree, before the push. The stub
files and scripts live in the session's scratch directory and are not
committed (M01 Unsure 21's reading).

| Reading | Before the repair | After the repair |
|---|---|---|
| the gate on the real pages, no token | `RED`, `signoffs_unsigned` `["s-001"]`, the other lists `[]`, `read_back` null, `artifacts_read` `[]`, exit 1 | the same: `RED`, `["s-001"]`, `[]`, `[]`, `[]`, `read_back` null, `artifacts_read` `[]`, `env_set` `{"token": false}`, exit 1; grepped for `ghs_`, `ghp_`, `github_pat_`, `execute-api`, `us-west-2_`, `amazonaws`: no match |
| the real served file, the page re-encoded cp1252 (Defect 2) | `UNSCORABLE`, `error.type` `UnicodeDecodeError`, no lists, exit 2 | `RED`, `signoffs_unsigned` `["s-001"]`, `unreadable` naming the page and `UnicodeDecodeError`, `page.read` false, exit 1 |
| a lifted entry, seat `legal`, a zip member with a bad CRC, the API unroutable (Defects 1, 3) | `UNSCORABLE`, `signoffs_differing` `[]`, `unreadable` `["s-001: the read-back raised BadZipFile: Bad CRC-32 for file 'a.json'"]`, exit 2; the summary's hash column `equal` | `RED`, `signoffs_differing` `["s-001"]`, two differences (the seat not of the seven; `manifest.json` not the entries), `unreadable` four items beside it (git, the manifest's API, the member's bad CRC, the build's API), the entry `equal` null with its `why`, exit 1 |
| the summary on a read-back record with no hash (Defect 3) | "package hash" `equal` | "package hash" `not read` |
| `http_get` against a local server answering 302 three ways, a made-up `ghs_` string as the token (Defect 4) | a relative `Location` raised `ValueError` whose text quotes the URL | relative `Location`: 200 through `urljoin`; `Location` with a control character: `error` `InvalidURL` alone; absolute `Location`: 200; the target saw no `Authorization` header on any leg; no returned field holds `sig=`, the URL or `ghs_` |

### Expected CI result on this PR

The ledger row says: RED, `signoffs_unsigned` `["s-001"]`,
`signoffs_disagreed` `[]`, `signoffs_differing` `[]`. The CI run on this
PR is expected to write that, with `unreadable` `[]`, `written_by_ci`
true, `env_set` `{"token": true}`, `artifacts_read` `[]`, `read_back`
null, and to fail the `M06 gate` job (exit 1), as runs 42491031888,
42491298504 and 42495856254 did. The repaired paths run on the plant for
no input: the plant carries no record, so nothing is read back and no
redirect is followed. On the same head `M00 gate` and `M02 gate` are
expected GREEN, `M01 gate` PENDING, exit 3, not required (M01 Unsure 14),
and `M03 gate`, `M04 gate` and `M05 gate` whatever they read: readings
after their measurements, named in a PR comment, not in a cell (Unsure
11, ruled at PR 2).

### Observed (CI run on this PR, 2026-11-08 UTC)

The first run on this PR,
[42500055895](https://github.com/andaro74/pharmadelta/actions/runs/42500055895),
on the merge ref `6844f9f` (the branch head was `47d9c3c`), wrote the
artifact `m06-gate-6844f9f922e3403010f0cc447499ebb9da6b2cd6` (1729 bytes
zipped, `result.json` 4069 bytes, `expires_at` 2027-02-06T16:28:26Z),
read with `gh run download` into a fresh directory and `python -I` in
this session:

| Field | Value |
|---|---|
| `verdict` | `RED`; `reason` "F6.1 holds: sign-offs s-001 are shown as signed with no signing record or no package record naming a file in the repository" |
| `signoffs_unsigned` | `["s-001"]`: `signature is null`, `package is null` |
| `signoffs_disagreed` | `[]`: the one page sign-off equals the file's entry as parsed JSON, in the block named for its id |
| `signoffs_differing` | `[]`: `read_back` null, `not_read_back` "no signing record" |
| `unreadable` | `[]`; `page.read` true |
| `env_set` | `{"token": true}`; `artifacts_read` `[]`: no listing, no download, no redirect leg |
| `written_by_ci` | `true`; `commit` `6844f9f`, `dirty` false; `event` `pull_request`, `ref` `refs/pull/35/merge`; `run_at` `2026-11-08T16:28:35+00:00`; exit 1; the gate step failed, the grep step and the upload step passed. The downloaded file grepped here for `ghs_`, `ghp_`, `github_pat_`, `execute-api`, `us-west-2_` and `amazonaws.com/`: no match |

Equals the expected result above and runs 42491031888, 42491298504 and
42495856254 on every field the ledger row names. The repair changed no
reading on the plant. On the same head `M00 gate` passed
([42500055880](https://github.com/andaro74/pharmadelta/actions/runs/42500055880)),
`M02 gate` passed
([42500055875](https://github.com/andaro74/pharmadelta/actions/runs/42500055875)),
`M01 gate` failed, not required
([42500055836](https://github.com/andaro74/pharmadelta/actions/runs/42500055836)).
The `M03 gate`
([42500055839](https://github.com/andaro74/pharmadelta/actions/runs/42500055839)),
`M04 gate`
([42500055922](https://github.com/andaro74/pharmadelta/actions/runs/42500055922))
and `M05 gate`
([42500055924](https://github.com/andaro74/pharmadelta/actions/runs/42500055924))
read `GREEN` with every list `[]`, readings after their measurements,
named in a comment on #35 and not in a cell (Unsure 11, ruled at PR 2).
The push that adds this section runs every gate again; the second
`M06 gate` run is read into the same comment.

## Close (PR 4, 2026-11-08 UTC)

PR 4 closes the milestone at the cap, 4 / 4. It carries the lift by
M03's path (b), as `rulings/pr2.md` 17 ruled: a CI run builds the
evidence package and writes it as an artifact; the zip is committed
under `pages/evidence/` by hand, byte for byte; then the seat holder's
own commit, made from their terminal and not by the session or by CI,
fills `signature` and `package` in `pages/api/sign-off.json`, sets
`scripted` false, removes the `PLANT` key and rebuilds the page from
the file. It fills the "Measured" cell from a CI-written result, writes
the row's state, rules or carries by name every open Unsure item of PR
1 to PR 3, adds `rulings/pr4.md`, and is followed by the tag `m06` on
its merge commit after the run on `main` is read. Nothing here decides
the row: the `main` run after #34 merged, 42495856254, is the
measurement, read again at this PR before the cell is written. The
gate, `src/m06/gate.py` and `m06.yml`, is not changed.

### Precondition, read at open

#35 merged at `194a6ab` on 2026-11-08 UTC; `main` holds `47d9c3c` and
`d198b6f` and `src/m06/gate.py` as repaired. Tags `m00` `e94b76b`,
`m01` `c60599e`, `m02` `ab72b9d`, `m03` `9932776`, `m04` `3905c10`,
`m05` `71770aa`; no `m06` tag. Row 7 OPEN at 3 / 4. The `main` run
after #35 merged,
[42502413422](https://github.com/andaro74/pharmadelta/actions/runs/42502413422)
on `194a6ab` (push), had completed: downloaded with `gh run download`
into a fresh directory before any edit and read with `python -I`,
artifact `m06-gate-194a6ab0581560f44d0ce9d3f1e4963d0a24b6b3` (1722
bytes zipped, `result.json` 4058 bytes, `expires_at`
2027-02-06T16:56:26Z): `RED`, `signoffs_unsigned` `["s-001"]`,
`signoffs_disagreed` `[]`, `signoffs_differing` `[]`, `unreadable` `[]`,
`written_by_ci` true, `read_back` null, `artifacts_read` `[]`, `env_set`
`{"token": true}`, `run_at` `2026-11-08T16:56:34+00:00`; grepped for
`ghs_`, `ghp_`, `github_pat_`, `execute-api`, `us-west-2_` and
`amazonaws.com/`: no match. The same as runs 42491031888, 42495856254
and 42500055895 on every field the row names; a reading after the
measurement. The plant stood: `git diff 6cfc1eb main -- pages/` was
empty. The Measured cell's source, run 42495856254, and the PR run
42491031888 were downloaded again the same way and read the same (the
table under "Measured", below). The artifacts the cells of rows 0, 1,
2, 4, 5 and 6 cite were listed through the API: none expired, the
earliest expiry 2027-01-08T14:04:46Z (row 0's). `main`'s required
checks: `M00 gate` alone, `strict` true (Unsure 3).

### Unsure 16, ruled before the lift (Product, Threshold Owner, Data Owner)

Ruled in the first commit of this PR, before any page was written
(`rulings/pr2.md` 17; `rulings/pr4.md` 1). The package carries, each
entry at its `path` in the zip with every field of the gate's
`ENTRY_RECORD`, null where unused:

| Source | Entries | `commit` / `run_url` | `ledger_row` |
|---|---|---|---|
| `artifact` | `artifacts/<artifact>/result.json` of the CI run each "Measured" cell cites: row 0 [38058191295](https://github.com/andaro74/pharmadelta/actions/runs/38058191295) (`m00-gate-47788c0…`), with that run's `observations.json`, the baseline's report on scenarios 5 and 6 (M05 Unsure 12); row 1 [38077129178](https://github.com/andaro74/pharmadelta/actions/runs/38077129178) (`m01-gate-223de2d…`, the artifact the cell names) and [38097865560](https://github.com/andaro74/pharmadelta/actions/runs/38097865560) (`m01-gate-8cdd851…`, the `main` run the cell names beside it); row 2 [38154731153](https://github.com/andaro74/pharmadelta/actions/runs/38154731153) (`m02-gate-e8c3690…`); row 4 [41171470951](https://github.com/andaro74/pharmadelta/actions/runs/41171470951) (`m03-gate-0b8d2ec…`); row 5 [41234548875](https://github.com/andaro74/pharmadelta/actions/runs/41234548875) (`m04-gate-4d92676…`); row 6 [41266122812](https://github.com/andaro74/pharmadelta/actions/runs/41266122812) (`m05-gate-8734adb…`). Nine files. Each downloaded in the build run through the API as the gate downloads it | the run; `commit` null | 0, 0, 1, 1, 2, 4, 5, 6 |
| `repository` | `repository/milestones/README.md`, `repository/SPEC/00-overview.md`, `repository/goldens/g-001.yaml` to `g-006.yaml`, `repository/pages/api/answers.json`, `baseline.json`, `break-it.json`, `sign-off.json`: twelve files, read from the checkout with `git show <sha>:<path>` | the build run's commit, 40 hex digits, the same as `package.commit` (Unsure 29) | null |
| `agent` | `agent/label-impact/<sha>/manifest.yaml` at each agent commit the served files name: `8cf0563` (`answers.json`, `agent.commit`) and `956cd87` (`break-it.json`, `agent.commit`; `sign-off.json`, `reviewer.seat_read_from.commit`), the short sha each file names resolved to the full one through `GET /repos/agentkeel-studio/label-impact/commits/<sha>`, the file read through the contents API as the gate reads it (Unsure 23) | the agent's commit, 40 hex digits | null |

Plus `manifest.json`, the entries as a list, equal to `package.entries`.
Twenty-two entries, twenty-three members with `manifest.json`. The ordinary assistant's results are in: the M00
run's `observations.json` and `result.json` (the baseline over the
goldens, scored), the M04 run's `result.json` (the baseline run the
side-by-side page's record names, compared), and `baseline.json`, the
served file (Unsure 16's question: yes). Every number in the package is
a CI-written result or a copy of data. Not in: the M02 artifact's
`sources/` (the eCFR and DailyMed responses, 140 KB; the cell cites the
`result.json`, and the sources stay in the artifact until it expires),
the M04 run's `observations.json` (its `result.json` carries the
comparison; the observations are the baseline's own run, which the M00
entry already shows on the same goldens), `data/` (copied into the
served files' `row` and `clause` where an answer is shown;
`data/table.json` and `data/clauses.json` are what the M02 gate
compares, and its `result.json` is in), and any `m06-gate` result (row
7's own measurement is what this package is signed for, not what it
holds). The served files are as at the build's commit, which precedes
the signing commit by construction: `sign-off.json` inside the package
is the plant's entry with `signature` null, and the ledger inside it has
row 7's "Measured" cell empty. A signature cannot be inside the package
it signs over; the package is what was reviewed, and the signature and
the cell are written after it (Unsure 34).

The zip is `pages/evidence/m06-evidence.zip` (`package.file`), the
basename `m06-evidence.zip` inside the artifact `m06-package-<sha>`
(Unsure 26, 36). It is deterministic: entries sorted by path, one fixed
timestamp, deflated at one level, so a reader with the same sources
writes the same bytes. The build writes no zip when any source could
not be read or any member holds a token's prefix or the door's host or
pool prefix; `build.json` beside it says why.

### Unsure 9, ruled before the lift (Product, Rule Owner)

The statement PR 1 proposed named "the evidence milestones/README.md
cites for its rows". The package carries row 7's own evidence for no
row, and the cells of rows 0, 1, 2, 4, 5 and 6 only; the statement
names them. Fixed, in the first commit, before the signing commit:

> Reviewed: the evidence package named under `package` holds the
> CI-written results milestones/README.md cites in its Measured cells
> for rows 0, 1, 2, 4, 5 and 6, with the ledger, SPEC/00, the goldens
> and the four served files at the commit the package names and
> label-impact's manifest at the agent commits the served files name,
> as read on the day of the signature.

It claims a reading, not a state; it carries none of SPEC/00 §11's six
words; it answers no question (`rulings/pr4.md` 2).

### The lift path (rulings/pr2.md 17)

M03's path (b), with the difference PR 2 ruled: the package is written
by a CI run with no write permission and committed by hand, and the
signing commit is the reviewer's own, by hand, because a commit by CI is
not a reviewer's signature (Unsure 1, 15).

- `.github/workflows/m06-lift.yml`: `permissions` `contents: read` and
  `actions: read`. One job: `actions/checkout@v7`, `uv sync --locked`,
  the artifact directory, then `uv run python -m src.m06.build` with
  `GITHUB_TOKEN` in that step's `env` and nothing else (no secret and no
  variable of M03's; grep `secrets.`: one match, `GITHUB_TOKEN`; grep
  `vars.`: none); then a step that greps the JSON records for a token's
  prefix (`ghs_`, `ghp_`, `github_pat_`) and fails on a match; then the
  artifact `m06-package-<sha>` holding the zip and `build.json`, 90
  days, uploaded only when the grep passed. Runs by hand
  (`workflow_dispatch`) and once on a push that adds or edits its own
  file on a branch other than `main`, because a dispatch needs the file
  on the default branch and the package is built before it is there,
  M03 Unsure 32's shape as `m03-lift.yml` and `m05-lift.yml` (Unsure
  33).
- `src/m06/build.py`: imports the gate's `Artifacts`, `api_json`,
  `read_agent_file`, `git`, `git_bytes`, `sha256_hex`, `ci_context`
  and `write_json` and copies none of them, so the build reads each
  source by the same code the gate reads it back with. Refuses to build
  when the checkout's `HEAD` is not the run's `GITHUB_SHA` or the tree
  is dirty: the package describes one commit. Downloads each cited
  artifact (the listing, then the archive through its 302 without the
  token), reads the repository files with `git show <sha>:<path>` and
  the goldens by `git ls-tree` at that sha, resolves the agent commits
  the served files name and reads the manifest at each, checks every
  member against the forbidden patterns, writes the zip and
  `build.json` (provenance, `ok`, `why`, `package` with `sha256`,
  `bytes`, `commit`, `built_by`, `written_by_ci`, the `entries`,
  `artifacts_read` with each `expires_at`, `agent_commits` as resolved,
  `env_set` one boolean). Exit 0 when the zip was written, 2 otherwise.
  Outside CI it writes `written_by_ci` false, and that zip is not
  committed (P4).
- `src/m06/page.py`: by hand, in the signing commit. Rebuilds
  `pages/sign-off.html` from `pages/api/sign-off.json`,
  deterministically, LF pinned (M03 Unsure 33), the records shown as
  the file holds them, the download link by the zip's GitHub URL at the
  commit that added it, no read-back claim and no measured number
  (Unsure 15, 18, 37). The gate reads page and file equal as parsed
  JSON whichever writer produced the page.
- The signing commit: the seat holder's own, run from their terminal.
  `pages/api/sign-off.json` with `signature` (`over` the zip's SHA-256,
  `by` `andaro74`, `method` the sentence fixed at PR 2, `read_from` the
  API path), `package` (`file`, `sha256`, `built_by`, `commit`,
  `entries` equal to the zip's `manifest.json`, `written_by_ci` true),
  `scripted` false, no `PLANT` key, the statement as fixed above, and
  the page rebuilt from it. After it nothing changes the served file:
  the commit that last changed it stays the reviewer's.

### The build (CI runs 42504215645 and 42503988551, not the Measured cell)

The first commit of this PR, `226ad89`, was pushed on 2026-11-08 UTC.
The push ran `m06-lift.yml` once, as its `push` trigger says
([42503988551](https://github.com/andaro74/pharmadelta/actions/runs/42503988551),
17:14:50Z, success). Then `gh workflow run m06-lift.yml --ref m06-pr4`
was tried for Unsure 33 and accepted: GitHub ran the dispatch on the
branch before the file was on `main`
([42504215645](https://github.com/andaro74/pharmadelta/actions/runs/42504215645),
`workflow_dispatch`, 17:17:31Z, success). Both ran at `226ad89`. Both
artifacts were downloaded with `gh run download` into fresh directories
and read with `python -I`; the two zips are byte-identical
(`cmp` equal, one SHA-256). The dispatch run is the one the record
names, since the close asked for a dispatch; the push run is named
here beside it.

| Field | Run 42504215645 (`package.built_by`) |
|---|---|
| artifact | `m06-package-226ad89ce575d89dfb90c9a5d93a8a5a9d1a31b9`, id 13626414153, 53226 bytes zipped, `expires_at` 2027-02-06T17:17:32Z (the push run's: id 13627035673, 53221 bytes zipped, `expires_at` 2027-02-06T17:14:50Z) |
| `build.json` | `ok` true, `written_by_ci` true, `commit` `226ad89ce575d89dfb90c9a5d93a8a5a9d1a31b9`, `dirty` false, `event` `workflow_dispatch`, `ref` `refs/heads/m06-pr4`, `run_at` `2026-11-08T17:17:41+00:00`, `env_set` `{"token": true}`, `failures` `[]`; 18248 bytes. Grepped for `ghs_`, `ghp_`, `github_pat_`, `execute-api`, `us-west-2_`, `blob.core` and `sig=`: no match |
| `m06-evidence.zip` | 51837 bytes, SHA-256 `2a3e3760f8fea4961624915108d8ece6e5a14d30d7057e7ca38f979798a1699e`, equal to `build.json`'s `package.sha256`; 23 members: `manifest.json` and 22 entries; `manifest.json` equal to `build.json`'s `entries` as canonical JSON; every entry's bytes hash to its `sha256`; every entry carries the eight fields of `ENTRY_RECORD` in order; every `repository` entry's `commit` is `226ad89…`, the run's sha |
| `artifacts_read` | seven artifacts, each listed 200 and downloaded 200, none expired: `m00-gate-47788c0…` (expires 2027-01-08T14:04:46Z), `m01-gate-223de2d…` (2027-01-08T18:46:23Z), `m01-gate-8cdd851…` (2027-01-09T00:16:26Z), `m02-gate-e8c3690…` (2027-01-09T16:15:55Z), `m03-gate-0b8d2ec…` (2027-01-29T05:09:45Z), `m04-gate-4d92676…` (2027-01-29T19:30:36Z), `m05-gate-8734adb…` (2027-01-30T02:39:54Z); the nine files taken hash as the same artifacts did when downloaded by hand at open |
| `agent_commits` | `8cf0563` → `8cf056345196aa28be30d05ee1e1b8bd0690d67c` (named by `answers.json`), `956cd87` → `956cd875c8e8200da2183ad401597cc559540b24` (named by `break-it.json` and `sign-off.json`), both 200 |
| the job | every step succeeded; the grep step read "no match"; the upload wrote the two files |

Construction, not evidence (P4): the build run from a clean worktree at
`226ad89` on this machine, with the owner's token in one process's
environment, wrote a zip whose 23 members are byte-identical to the CI
zip's and whose archive bytes are not: Windows Python's `zlib` is
zlib-ng and Ubuntu's is zlib, and the two deflate the same bytes
differently. The zip is deterministic given one zlib; the committed
bytes are the artifact's, never a local build's, and a reader who
rebuilds compares members and hashes, not archive bytes (Unsure 38).

### The zip, committed

The second commit of this PR adds `pages/evidence/m06-evidence.zip`,
the file of the dispatch run's artifact copied byte for byte: SHA-256
`2a3e3760f8fea4961624915108d8ece6e5a14d30d7057e7ca38f979798a1699e`,
51837 bytes, checked after `git add` against the blob git stores (`git
show :pages/evidence/m06-evidence.zip | sha256sum`), which `.gitattributes`
leaves unconverted (`git ls-files --eol` reads `-text`). Nothing else
under `pages/` changes in that commit; `pages/api/sign-off.json` still
serves the plant.

### The signing commit (`37352ef`)

The fourth commit of this PR is the seat holder's own, made from their
terminal on 2026-11-08 at 21:13:49Z and not by the session or by CI,
with the two files `src/m06/page.py` had written in the working tree:
`pages/api/sign-off.json` and `pages/sign-off.html`, nothing else
(`git show --stat 37352ef`: two files). GitHub's API reads the commit
with `author.login` `andaro74` and `committer.login` `andaro74`,
`verification.verified` false, reason `unsigned`, one parent `8b95193`
(Unsure 40). In the served file: `signature` `over`
`2a3e3760f8fea4961624915108d8ece6e5a14d30d7057e7ca38f979798a1699e`,
`by` `andaro74`, `method` the sentence fixed at PR 2, `read_from` `GET
/repos/andaro74/pharmadelta/commits/<sha>`; `package` `file`
`pages/evidence/m06-evidence.zip`, `sha256` the same hash, `built_by`
run 42504215645 and artifact `m06-package-226ad89…`, `commit`
`226ad89ce575d89dfb90c9a5d93a8a5a9d1a31b9`, `entries` the 22 records
equal to the zip's `manifest.json`, `written_by_ci` true; `scripted`
false; no `PLANT` key; the statement as fixed above; `lift` naming the
run and the artifact. The page is the writer's output from that file:
the reviewer, the statement, the signature record with no read-back
claim, the package record with the download link by the zip's GitHub
URL at `3e56b07` and each entry linked to its source, the same object in
its `id="signoff-s-001"` block, the banner saying the sign-off is built
in this repository's website layer, not an agentkeel seat or a platform
control, and that one person holds all seven seats. No number on the
page is anything but a hash, a size or a count read from the file. It
produces the evidence a validation would need. Since this commit nothing
has changed the served file: `git log -1 --format=%H --
pages/api/sign-off.json` reads `37352ef…` at the close commit.

### Observed (CI run on this PR, 2026-11-08 UTC; not the Measured cell)

PR #36 opened at 21:16Z on head `37352ef`. Its `M06 gate` run,
[42524408048](https://github.com/andaro74/pharmadelta/actions/runs/42524408048) (`pull_request`, merge ref `15fef71`), was
downloaded with `gh run download` into a fresh directory and read with
`python -I`: artifact `m06-gate-15fef71e0c10aecf7a774d99ab3ea99c1f4da82c`
(id 13634712284, 5079 bytes zipped, `result.json` 24912 bytes,
`expires_at` 2027-02-06T21:16:59Z). Grepped for `ghs_`, `ghp_`,
`github_pat_`, `execute-api`, `us-west-2_` and `amazonaws.com/`: no
match.

| Field | Read |
|---|---|
| `verdict` | `GREEN`; the gate step, the grep step and the upload succeeded; exit 0 |
| `signoffs_unsigned`, `signoffs_disagreed`, `signoffs_differing`, `unreadable` | `[]`, `[]`, `[]`, `[]` |
| `written_by_ci`, `env_set` | true, `{"token": true}` |
| `run_at`, `commit` | `2026-11-08T21:17:14+00:00`, `15fef71e0c10aecf7a774d99ab3ea99c1f4da82c` |
| `served[0]` | `s-001`, `shown_signed` true, `signature_record.has_record` true, `package_record.has_record` true ("22 entries, every field present"), `signed` true, `page_equal` true |
| `read_back.function` | seat `product`, shown `Regulatory Affairs`, expected `Regulatory Affairs`, equal |
| `read_back.last_commit` | `37352ef713af56758316b565287195c3b339ecd2` from `git log -1 --format=%H -- pages/api/sign-off.json` (the branch commit, not the merge ref: Unsure 22) |
| `read_back.commit` | 200, `author_login` `andaro74`, `committer_login` `andaro74`, `authored_at` `2026-11-08T21:13:49Z`, `verified` false (`unsigned`), one parent `8b95193…` |
| `read_back.manifest` | 200 at `ref=956cd87`, blob `4d6d126…`, seat `product` → login `andaro74`; all seven seats `andaro74` |
| `read_back.package_file` | 51837 bytes, `sha256` equal to `signed_over` and to `recorded`, `2a3e3760…1699e` |
| `read_back.package_zip` | `is_zip` true, 23 files |
| `read_back.entries` | 22, every `in_package` true, every `sha256_equal` true, every `source_read.read` true (two `agent` entries 200, twelve `repository` entries by `git show`, eight `artifact` entries found in their downloaded artifacts), every `equal` true |
| `read_back.built_by` | run 42504215645, artifact `m06-package-226ad89…`, file `m06-evidence.zip`, read, found, equal |
| `read_back.differences`, `read_back.not_read`, `read_back.equal` | `[]`, `[]`, true |
| `artifacts_read` | eight: the seven gate artifacts of rows 0, 1 (two), 2, 4, 5, 6 and the build artifact, each listed 200 and downloaded 200, none expired; the earliest `expires_at` 2027-01-08T14:04:46Z (row 0), the build artifact's 2027-02-06T17:17:32Z |

Every field the close expected. The read-back paths (`read_last_commit`,
`read_commit`, `read_manifest_seat`, the artifact listing and download
with the workflow's token, the redirect leg) ran in CI for the first
time on this run (Unsure 30, 41). This is a reading after the
measurement and decides nothing about the row; the cell cites run
42495856254.

### The other gates on this PR's head (not a cell)

Read the same way, recorded here and in a comment on #36, not in any
cell (M03 `rulings/pr4.md` 6, 22; M04 `rulings/pr4.md` 22; M05
`rulings/pr4.md` 3; M06 Unsure 11, ruled).

| Gate | Run | Read |
|---|---|---|
| `M00 gate` | [42524407962](https://github.com/andaro74/pharmadelta/actions/runs/42524407962) | the job succeeded |
| `M01 gate` | [42524407973](https://github.com/andaro74/pharmadelta/actions/runs/42524407973) | `PENDING`, exit 3, as on every run since M01 PR 4: no deploy run of agentkeel's naming label-impact among the 100 read, the registry unread; not required |
| `M02 gate` | [42524408109](https://github.com/andaro74/pharmadelta/actions/runs/42524408109) | the job succeeded |
| `M03 gate` | [42524407941](https://github.com/andaro74/pharmadelta/actions/runs/42524407941) | `RED`, `answers_uncalled` `[]`, `answers_disagreed` `[]`, `answers_differing` `["g-001"]`, `unreadable` `[]`; sign-in 200; the door 200, `stop_reason` `end_turn`, `guardrail_topics` `[]`, the same two `find_label_row` tool errors on section `8.1` as every call since M03 (M03 Unsure 23), and this time a `parsed` object with `table_row` null, a clause and `impacted` false, where the served answer is null: "one side has an answer and the other has none". The `main` run after #35, [42502413323](https://github.com/andaro74/pharmadelta/actions/runs/42502413323), read `parsed` null on the same tool errors and GREEN. Nothing in this PR touches `pages/api/answers.json`, the agent or its door; the door's answer to g-001 varies between calls. A reading after row 4's measurement; row 4's cell stands (Unsure 42) |
| `M04 gate` | [42524408003](https://github.com/andaro74/pharmadelta/actions/runs/42524408003) | `GREEN`: `answers_unrun` `[]`, `answers_disagreed` `[]`, `answers_differing` `[]`, `agent_disagreed` `[]`, `baseline_changed` false, `unreadable` `[]` |
| `M05 gate` | [42524407953](https://github.com/andaro74/pharmadelta/actions/runs/42524407953) | `GREEN`: `scenarios_untraced` `[]`, `scenarios_disagreed` `[]`, `scenarios_differing` `[]`, `unreadable` `[]`; the door stopped g-005 under `treatment-or-dosing-advice` and g-006 under `instruction-to-assistant-in-pasted-document`, `stop_reason` `guardrail_intervened` on both |

### The two runs, read again at PR 4

Before the cell was written, the Measured cell's source and the PR run
beside it were downloaded again with `gh run download` into fresh
directories and read with `python -I`; both grepped for a token's prefix
and the door's strings: no match.

| Field | Run 42495856254 (`main`, after #34) | Run 42491031888 (PR #34) |
|---|---|---|
| artifact | `m06-gate-e175d772bd32ce9e148f79b868b72a2dcfa8b24f`, id 13622994136, 1726 bytes zipped, `result.json` 4058 bytes, `expires_at` 2027-02-06T15:38:48Z | `m06-gate-8431885faa0353ebf43d56ea244df4bb98ca8c6b`, id 13621551969, 1727 bytes zipped, `result.json` 4069 bytes, `expires_at` 2027-02-06T14:41:21Z |
| `verdict` | `RED` | `RED` |
| `signoffs_unsigned` | `["s-001"]` | `["s-001"]` |
| `signoffs_disagreed`, `signoffs_differing`, `unreadable` | `[]`, `[]`, `[]` | `[]`, `[]`, `[]` |
| `written_by_ci`, `env_set` | true, `{"token": true}` | true, `{"token": true}` |
| `read_back`, `artifacts_read` | null, `[]` | null, `[]` |
| `commit`, `ref`, `event`, `run_at` | `e175d77…`, `refs/heads/main`, `push`, `2026-11-08T15:38:56+00:00` | `8431885…`, `refs/pull/34/merge`, `pull_request`, `2026-11-08T14:41:31+00:00` |

### Measured

The cell cites the run on `main` after #34 merged, 42495856254 on
`e175d77` (M01 Unsure 23, ruled at M02 PR 1; `rulings/pr2.md` 17;
`rulings/pr3.md` 12), with the PR run 42491031888 named beside it as the
one read at the time. It is written in the ledger's words, as rows 0 to
6 are. The cell equals the expected gate output written at open, so
under the ledger's rule row 7 is GREEN and "PRs used / cap" is 4 / 4.
The cell then names the lift as rows 4 to 6 name theirs: the build run
and its artifact, the zip's commit, the signing commit, and the PR run
that read the lifted state GREEN, each a reading after the measurement
that decides nothing. No finding: the lift read as the close expected.
The M03 gate's reading on this head is row 4's matter and is recorded
above and under Unsure 42, not in row 7's cell.

### What the gate on this PR can read after the close commit

The close commit changes `milestones/README.md`,
`milestones/M06/README.md` and `milestones/M06/rulings/pr4.md` and
nothing under `pages/`, so the commit that last changed
`pages/api/sign-off.json` stays `37352ef`, the reviewer's. The `M06
gate` run on the new head is expected to read as 42524408048 did:
GREEN, every list `[]`, the same read-back, when GitHub's API and the
eight artifacts answer; `UNSCORABLE` with the lists `[]` when one does
not (Unsure 30). Either is a reading after the measurement, recorded in
a comment on #36 and not here. The `M03 gate` may read RED or GREEN
again on g-001 as the door answers (Unsure 42); the `M00`, `M02`, `M04`
and `M05` gates are expected as above and the `M01 gate` PENDING, none
required.

### Rulings carried

Ruled or carried by name in `rulings/pr4.md`: PR 1's 2, 3, 9, 10, 15,
16; PR 2's 18, 20, 23, 24, 25; PR 3's 29, 30, 31, 32; PR 4's 33 to 42.
Unsure 3: `M06 gate` is not made a required check in this PR; `M00
gate` stays the one required context, `strict` true, no rulesets (read
2026-11-08 UTC at the close); recorded for the record, the owner's
setting, carried to no milestone. Unsure 2: GitHub Pages stays not
enabled; "downloadable" is the zip's GitHub URL on the page (PR 1's
ruling). Label-impact's own items stay its: the tool that refuses
section `8.1` as a number (M03 Unsure 23) and the two break rules (M05's
platform item, answered at label-impact `410f9a8` and read as stopping
both on every run since).

### What this PR does not hold

- No change to `src/m06/gate.py`, `.github/workflows/m06.yml`,
  `src/m03/`, `src/m04/`, `src/m05/`, `src/baseline/` (P5), `goldens/`,
  `pyproject.toml` or `uv.lock`.
- No change to `pages/api/sign-off.json` or `pages/sign-off.html` after
  `37352ef`; no change to any other served file or page.
- No required-check change, no Pages setting, no tag: the tag `m06` is
  placed by the owner on the merge commit after the `main` run is read.
- No door host, pool id, client id, door text or token in any file,
  artifact, page or comment; the build's and the gate's artifacts were
  grepped before they were cited.
- No number on the page that is not read from the served file; no
  read-back claim on the page (Unsure 18); no signature by a function
  without a seat; no word of SPEC/00 §11's six about the sign-off.
- No design of a platform control: the sign-off is this repository's
  website layer and says so.

### What a reader can falsify

- `git diff 194a6ab..<head> --stat` touches `.github/workflows/m06-lift.yml`,
  `src/m06/build.py`, `src/m06/page.py`, `pages/evidence/m06-evidence.zip`,
  `pages/api/sign-off.json`, `pages/sign-off.html`,
  `milestones/README.md`, `milestones/M06/README.md` and
  `milestones/M06/rulings/pr4.md` only; `git diff 194a6ab..<head> --
  src/m06/gate.py .github/workflows/m06.yml src/m03 src/m04 src/m05
  src/baseline goldens pyproject.toml uv.lock` is empty.
- `git log -1 --format='%H %an %ae' -- pages/api/sign-off.json` on the
  head reads `37352ef… andaro74 andaro74@gmail.com`; `gh api
  repos/andaro74/pharmadelta/commits/37352ef` reads `author.login`
  `andaro74` and two files.
- `sha256sum pages/evidence/m06-evidence.zip` reads `2a3e3760…1699e`;
  `python -I -c "import zipfile,json; z=zipfile.ZipFile('pages/evidence/m06-evidence.zip'); print(len(z.namelist()))"`
  reads 23; the zip's `manifest.json` equals `package.entries` in the
  served file as canonical JSON; each member's SHA-256 is its entry's.
- The artifact of run 42504215645 holds a `m06-evidence.zip` with the
  same SHA-256, and its `build.json` reads `written_by_ci` true at
  `226ad89…`.
- The artifact of run 42524408048 reads as the table under "Observed"
  says; the artifact of run 42495856254 reads as the table under "The
  two runs" says. Download them and read them.
- `uv run python -m src.m06.page write` on the head leaves
  `pages/sign-off.html` unchanged (`git status --short` empty).
- `gh api repos/andaro74/pharmadelta/branches/main/protection/required_status_checks`
  reads `M00 gate` alone, `strict` true.

### After this PR

The owner merges #36 with a merge commit, not a squash (Unsure 19: a
squash would make the committer `web-flow`). The `main` run of `m06.yml`
on the merge commit is downloaded with `gh run download` and read with
`python -I`, and recorded in a comment on #36; it is expected GREEN and
decides nothing (the cell is written). Then `git tag m06 <merge commit>`
and `git push origin m06` by the owner. M06 is closed at 4 / 4. A fifth
PR on this milestone is a RED close with its finding as the result and
is not proposed. What is owed outside the cap: nothing in this
repository; label-impact's tool refusing `8.1` as a number (M03 Unsure
23) stays label-impact's, and the owner's settings (Pages, required
checks) stay the owner's.

## Unsure (PR 4)

Numbering continues from PR 3's. Each needs a seat's ruling. None blocks
the close, whose measurement is run 42495856254.

| # | Item | Seat |
|---|---|---|
| 33 | `m06-lift.yml` runs on `workflow_dispatch` and once on a push that adds or edits its own file on a branch other than `main`, as `m03-lift.yml` and `m05-lift.yml` do (M03 Unsure 32). The close was asked for a dispatch-only workflow; a dispatch of a workflow file that is not on the default branch is refused by GitHub, so the first build is the push's. Whether a dispatch on this branch is accepted before the file is on `main` is tried at the push and recorded. **Read at the push:** accepted; run 42504215645 is the dispatch's, made before the file was on `main`, and the push's run 42503988551 wrote the same zip. The push trigger was not needed for the dispatch and stays as `m03-lift.yml` and `m05-lift.yml` have it; it cost one run. Ruled at `rulings/pr4.md`. | Engineering, Security |
| 34 | The package carries `pages/api/sign-off.json` and `milestones/README.md` as at the build's commit: the plant's entry with `signature` null, and row 7's cell empty. A signature cannot be inside the package it signs over. Recorded; the statement names what the package holds. | Product |
| 35 | Row 1's cell cites two runs; both `result.json` files are in the package (the PR run's artifact the cell names, and the `main` run's beside it). Rows 2, 4, 5 and 6 name a PR run beside the `main` run too, as "read the same"; only the `main` run's artifact, the cell's source, is taken for those. Row 1 is the one row whose named artifact is the PR run's. | Product |
| 36 | The zip's basename is `m06-evidence.zip`, one name for the milestone; a later re-build (as M05's re-lift) would replace the file and the signature would have to be made again. A name carrying the build's sha was not chosen: the record carries `package.commit` and the hash. | Tool Owner, Product |
| 37 | The download link on the page is the zip's GitHub URL at the commit that added it (the file view and the raw file), pinned by sha, with the SHA-256 beside it; `main`'s URL would move. The page writer reads that commit with `git log -1 -- <file>`. | Product, Security |
| 38 | The zip's archive bytes depend on the zlib that deflates them: the CI zip and a local build at the same commit hold byte-identical members and differ as archives (zlib-ng on Windows, zlib on Ubuntu). The record's hash is the CI artifact's, the committed bytes are the artifact's, and the gate compares the committed file with the artifact's file; a local rebuild compares members and hashes. Whether the build should store members uncompressed, so that any zlib gives one archive, is a change outside this cap. | Engineering, Tool Owner |
| 39 | The ruling file names this PR as #36, the next number on this repository after #35. **Read at open:** #36. | Product |
| 40 | The signing commit `37352ef` is not GPG-signed (`verification.verified` false, reason `unsigned`), as every commit on this repository; `author.login` is GitHub's match of the commit's email to the account `andaro74`. Recorded as read and not required at M06 (Unsure 1 and 19, ruled). If Security later requires it, the owner signs commits first and the gate changes outside this cap. | Security |
| 41 | The gate's read-back paths ran in CI for the first time on run 42524408048 (Unsure 30): every read answered 200. The eight artifacts the gate compares expire from 2027-01-08T14:04:46Z (row 0's) to 2027-02-06T17:17:32Z (the build's) (Unsure 7, 20); after the first expiry a run reads `unreadable` on that entry and `UNSCORABLE` when nothing is RED, and the committed zip, its hash and the signing commit are the record. No re-build is planned; one would need a new signature (Unsure 36). | Engineering, Product |
| 42 | On this PR's head the `M03 gate` read `RED`, `answers_differing` `["g-001"]`: the door answered g-001 with a `parsed` object (`table_row` null, a clause, `impacted` false) after the same two tool errors every call has shown since M03 (the tool refuses section `8.1` as a number, M03 Unsure 23), where the served answer is null; the `main` run after #35 read `parsed` null on the same errors and GREEN. The door's answer to g-001 varies between calls. Nothing in this PR touches `pages/api/answers.json`, the agent or its door; row 4's cell cites its `main` run and stands. Recorded in the comment on #36 and here, in no cell. Whether row 4's served answer should be re-lifted when label-impact fixes the tool is a PR outside any cap, as M05's re-lift was. | Product, Rule Owner, Tool Owner |

## Unsure (PR 3)

Numbering continues from PR 2's. Each needs a seat's ruling. None blocks
the measurement, which is the `main` run above.

| # | Item | Seat |
|---|---|---|
| 28 | The ruling file names this PR as #35, the next number on this repository after #34. | Product |
| 29 | `package.commit` (this repository's commit the package describes) is checked present and non-empty, and read back by nothing: each `repository` entry carries its own `commit`, and the gate reads that. Whether the gate should require every `repository` entry's `commit` to equal `package.commit`, or record `package.commit` in the read-back. Proposed: recorded in the read-back at the lift if the lift's record uses it; not required at M06. | Tool Owner, Engineering |
| 30 | The read-back paths (`read_last_commit` on a full checkout, `read_commit`, `read_manifest_seat`, the artifact listing and download with `GITHUB_TOKEN` under `actions: read`, the redirect leg) have run in CI on no run yet: the plant makes no network read. Their first CI exercise is the lift's. A failure there reads `unreadable`, never a wrong verdict; the construction readings at PR 2 ran them with the owner's token, not the workflow's. | Engineering |
| 31 | The grep step matches a package entry's `path` or an artifact's name as it matches a token: a path holding `ghs_` would fail the step and lose the artifact, a false positive. The lift names the paths; none proposed holds a prefix. Recorded for the lift. | Security, Engineering |
| 32 | `signoffs_disagreed` reads one direction, as the row's words do ("the page shows a sign-off the served file does not serve"): a served sign-off the page does not show is named by no list while the page shows at least one block (a page with no block is `unreadable`). Whether the lift's page must show every served sign-off is Product's; the gate does not require it. | Product |

## Unsure (PR 2)

Numbering continues from PR 1's. Each needs a seat's ruling. None blocks
the measurement.

| # | Item | Seat |
|---|---|---|
| 17 | The ruling file names this PR as #34, the next number on this repository after #33. | Product |
| 18 | The signature record has no `read_back` field (PR 1 proposed one): the signing commit's own sha, login and time cannot be in the file that commit changes. The read-back is in the gate's `result.json`. If the lifted page shows who signed and when, it shows it from a CI result with the run's link, as SPEC/00 §11 asks of a number; the record itself carries `by` (expected) and the hash. Built so. | Tool Owner, Engineering |
| 19 | The gate reads `author.login`, not `committer.login`, and records both. Merges here are merge commits, so the commit that last changed the served file is the branch commit and both logins are the author's; a squash merge would keep the author and make the committer `web-flow`. `author.login` is GitHub's match of the commit's email to an account, which anyone can set in `git config`; `verified` is recorded and not required (Unsure 1, ruled). Whether the gate should also require `committer.login` equal to the author's. Proposed: not at M06; recorded. | Security |
| 20 | The build artifact (`package.built_by`) expires 90 days after its run, like the entries' artifacts (Unsure 7). After that the gate cannot read whether the package file is what CI wrote, and reads `unreadable`; the committed zip and its hash in the signing commit are then the only record. Proposed: as Unsure 7, recorded with the expiry in `artifacts_read`. | Engineering, Product |
| 21 | The grep step before upload matches `ghs_`, `ghp_` and `github_pat_`, the prefixes of an Actions token, a classic token and a fine-grained token. Hex digests and logins cannot contain them. The token is written by no code path; the step is a second fence. Whether the prefix list is complete is Security's. | Security |
| 22 | `fetch-depth: 0` is the first full-depth checkout in this repository's workflows. On a pull request the checkout is the merge ref; `git log -1 -- pages/api/sign-off.json` names the branch commit that last changed the file, not the merge commit, because a clean merge changes no file. A conflict merge would name the merge commit, authored by the merger. Recorded. | Engineering |
| 23 | The entry source `agent` reads `label-impact`'s repository through the contents API, which returns `content` only for files under 1 MB; `manifest.yaml` is under 2 KB. A larger file reads `unreadable`. The source was added at PR 2 because PR 1's proposed package carries that manifest and label-impact is not in the checkout. | Engineering |
| 24 | A served sign-off shown as not signed (`signed` not true) is named by no list, whatever its records: the row's words name "each shown as signed" (M05 Unsure 17's reading). Built so; construction reading: alone, GREEN. | Product |
| 25 | `SEAT_FUNCTION` is SPEC/00 §5's table copied into the gate. A seat not among the seven reads differing; a function other than the seat's reads differing. If §5 changes, the gate changes with it. Pharmacovigilance and Legal cannot be a signature by this check (SPEC/00 §5; CLAUDE.md). | Product, Rule Owner |
| 26 | The gate finds the package file in the build artifact by its basename (`Path(package.file).name`). The lift's CI run must name the zip inside its artifact as it is committed. Recorded for the lift. | Engineering |
| 27 | One served file, one last commit. Every sign-off in `pages/api/sign-off.json` is read against the same commit, the one that last changed the file. A second sign-off added later by a second login would make the first read differing, since the last commit would not be the first signer's. With one person holding all seven seats (R1) every login coincides and this does not arise; it is a limit of reading (a) with one file, recorded. Per-sign-off files are not built here. | Product, Tool Owner |

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant.

| # | Item | Seat |
|---|---|---|
| 1 | What a signature is: (a) the reviewer's own commit that changes `pages/api/sign-off.json`, read back from GitHub's API as the commit that last changed the file, `author.login` the seat's login; (b) a signed tag; (c) a platform control, which SPEC/00 §5 rules out. Proposed: (a). Under (a), whether the gate must also read `commit.verification.verified` true: commits on this repository are unsigned today, and `author.login` is GitHub's match of the commit's email to an account, which anyone can set in `git config`. Proposed: `verified` is recorded as read and not required at M06; if Security wants it required, the owner signs commits first and the gate changes at PR 2. The plant is false under every reading. **Ruled at PR 2** (`rulings/pr2.md` 3): (a), as built; `verified` is recorded as read and not required; the commit's `author.login` must be the seat's login in the manifest at the commit the record names, `reviewer.login` and `signature.by`; the plant is unsigned under every reading. Unsure 19 records the author, committer and email-match limits. | Security, Product |
| 2 | M05's Unsure 2, carried here by name (`milestones/M05/rulings/pr4.md` 15). GitHub Pages is not enabled (404 on 2026-11-08 UTC; `has_pages` false). **Ruled at this PR** (`rulings/pr1.md` 8): "downloadable" means a file in this public repository fetched by its GitHub URL; "public" means readable in the repository, as since M03; the milestone does not depend on Pages; enabling it is the owner's setting and is carried to no further milestone by name. **Closed after the close** (`milestones/adoption/rulings/pages-index.md` 1): Pages enabled 2026-11-08 UTC from `main` root; the pages served are byte-identical to the files. | Product, Security |
| 3 | M05's Unsure 3, carried here by name (`milestones/M05/rulings/pr4.md` 16). `M00 gate` is the one required check, `strict` true, no rulesets (read 2026-11-08 UTC). **Ruled at this PR** (`rulings/pr1.md` 9): no Measured cell depends on a required check; the M02 to M05 gates stay as they are; whether `M06 gate` joins is recorded at PR 4 for the record; the setting is the owner's and is carried to no further milestone by name. | Security, Product |
| 4 | Which seat reviews. Proposed: `product`, shown as Regulatory Affairs (SPEC/00 §5). Whether other seats may add their own sign-offs, each with its seat and login, is open; Pharmacovigilance and Legal hold no seat and may be shown as consulted, never as a signature (SPEC/00 §5; CLAUDE.md). **Ruled at PR 2** (`rulings/pr2.md` 7): `product`, shown as Regulatory Affairs; any of the seven seats may add a sign-off with its own seat and login, and the gate reads each against SPEC/00 §5's table; a seat not of the seven reads differing, so Pharmacovigilance and Legal cannot sign (Unsure 25, 27). | Product |
| 5 | Names proposed here and fixed at PR 2: the files `pages/sign-off.html` and `pages/api/sign-off.json`; the served key `signoffs`; the entry fields `reviewer`, `statement`, `signed`, `signature`, `package`; the records' fields under "Carried to PR 2"; the gate's lists `signoffs_unsigned`, `signoffs_disagreed`, `signoffs_differing`. **Ruled at PR 2** (`rulings/pr2.md` 4): fixed as built, with the records' fields under "The records' fields"; `read_back` dropped from the signature record (Unsure 18); `unreadable` and `written_by_ci` beside the three lists. | Tool Owner, Engineering |
| 6 | The package's form and contents: one zip under `pages/evidence/` plus a `manifest.json` of entries, each with its SHA-256 and the run and artifact it came from, holding the files listed under "Carried to PR 2". Whether a zip in git is acceptable (the M02 artifact is 142 KB; the rest are under 3 KB each) or the package should be one JSON file. Proposed: the zip; fixed at PR 2 or at the lift. **Ruled at PR 2** (`rulings/pr2.md` 5): the zip under `pages/evidence/`, `manifest.json` inside equal to the record's `entries`, three sources (artifact, repository, agent); a zip in git accepted; which files go in is fixed at the lift (16). | Tool Owner, Product, Data Owner |
| 7 | CI artifacts expire after 90 days. The runs the Measured cells cite are from 2026-10-10 (row 0), 2026-10-10 (row 1), 2026-10-11 (row 2), 2026-10-31 (rows 4, 5) and 2026-11-01 (row 6); the first expire about 2027-01-08. After that the gate cannot compare a package entry with its artifact and reads `unreadable`; the package is then the only copy. Proposed: the gate compares what it can download and names the rest under `unreadable`, which is UNSCORABLE only when nothing is RED; the package records each artifact's expiry date. **Ruled at PR 2** (`rulings/pr2.md` 6): as proposed; the expiry is recorded in the gate's result (`artifacts_read[].expires_at`), not in the record; the build artifact expires too (Unsure 20). | Engineering, Product |
| 8 | The gate reads GitHub's API with `GITHUB_TOKEN` (`contents: read`, `actions: read`) and downloads artifacts of this repository. No secret of the door is read. Whether `actions: read` on a pull request from a fork is a concern: this repository takes no fork PRs. **Ruled at PR 2** (`rulings/pr2.md` 2): `GITHUB_TOKEN` in the gate step's `env`, `contents: read` and `actions: read`, no door secret or variable; the token is withheld from the blob store's redirect and grepped for before upload (Unsure 21); this repository takes no fork PRs, and a fork's token is read-only in any case. | Security, Engineering |
| 9 | The statement's wording: "Reviewed: the evidence package named under `package` is the evidence milestones/README.md cites for its rows at the commit the package names, as read on the day of the signature." It avoids SPEC/00 §11's six words and claims a reading, not a state. Proposed: as written; fixed before the signing commit. **Carried at PR 2** (`rulings/pr2.md` 14): the statement is unchanged here, since no page changes; fixed before the signing commit. | Product, Rule Owner |
| 10 | One person holds all seven seats (R1) and authors every PR, so the reviewer reviews their own work and the page says so. Whether the page needs more than that sentence, such as a second reviewer who holds no seat, which SPEC/00 §5 forbids as a signature. Proposed: the sentence is enough; the sign-off's worth is that CI can read it back, not that the reviewer is independent. **Carried at PR 2** (`rulings/pr2.md` 14): unchanged; the gate reads one login for every seat, as the manifest holds. | Product, Security |
| 11 | The M03, M04 and M05 gates run on this PR, read their own files by path and do not read the new files. Their readings are after their measurements and are named in the PR body or a comment, not in a cell. Proposed: recorded. **Ruled at PR 2** (`rulings/pr2.md` 8): recorded in a comment on the PR and under "Observed". | Product, Engineering |
| 12 | The ruling file names this PR as #33, the next number after #32 (the M05 count PR, opened first). If #32 is not opened first, the number is wrong by one and is corrected at PR 2. **Ruled at PR 2** (`rulings/pr2.md` 9): #32 was the count PR and #33 this milestone's PR 1, as the two ruling files wrote; neither `pr:` line changes. | Product |
| 13 | Numbers on the plant page: `s-001`, SPEC/00's section numbers, "seven" seats (SPEC/00 §5's) and the manifest's commit `956cd87`. None is a measured result (M03's 7). **Ruled at PR 2** (`rulings/pr2.md` 10): no page changes here; the numbers stand as read at PR 1. | Product |
| 14 | The reviewer's seat is copied from `label-impact`'s manifest at `956cd87` by hand. If the manifest changes the seat's login before the lift, the record names the commit it read and the gate reads the manifest at that commit; a stale read is a `signoffs_differing` finding, not a repair here. **Ruled at PR 2** (`rulings/pr2.md` 11): as built, the gate reads the manifest at the commit the record names and compares that login with the commit's author; it does not read `main`'s manifest. A change of the seat's login is read at the lift, when the record is written. | Product, Data Owner |
| 15 | The lift's writer rebuilds the page from the served file, as M03's and M05's do; but the signing commit is the reviewer's own, made by hand, so the page in that commit is written by a hand-run writer. The page's content is a copy of records, not evidence; the evidence is the artifacts the package names and the gate's run (P4). Whether a hand-run writer is acceptable for the page in the signing commit. Proposed: yes, with the gate reading page and file equal as parsed JSON. **Carried at PR 2** (`rulings/pr2.md` 14): to the lift PR; the gate reads page and file equal as parsed JSON whichever writer produced the page. | Engineering, Product |
| 16 | Whether the package carries the ordinary assistant's results (the baseline's observations, M04's served file) beside the agent's. Proposed: yes, as listed; every number in the package is a CI-written result or a copy of data. **Carried at PR 2** (`rulings/pr2.md` 14): to the lift PR; the gate accepts any entries whose sources it can read. | Product, Threshold Owner |
