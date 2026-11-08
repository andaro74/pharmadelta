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
| Measured | |
| PRs used / cap | 1 / 4 |
| State | OPEN |

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
| GitHub Pages | not enabled: `GET /repos/andaro74/pharmadelta/pages` answers 404 (Unsure 2) |
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

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant.

| # | Item | Seat |
|---|---|---|
| 1 | What a signature is: (a) the reviewer's own commit that changes `pages/api/sign-off.json`, read back from GitHub's API as the commit that last changed the file, `author.login` the seat's login; (b) a signed tag; (c) a platform control, which SPEC/00 §5 rules out. Proposed: (a). Under (a), whether the gate must also read `commit.verification.verified` true: commits on this repository are unsigned today, and `author.login` is GitHub's match of the commit's email to an account, which anyone can set in `git config`. Proposed: `verified` is recorded as read and not required at M06; if Security wants it required, the owner signs commits first and the gate changes at PR 2. The plant is false under every reading. | Security, Product |
| 2 | M05's Unsure 2, carried here by name (`milestones/M05/rulings/pr4.md` 15). GitHub Pages is not enabled (404 on 2026-11-08 UTC; `has_pages` false). **Ruled at this PR** (`rulings/pr1.md` 8): "downloadable" means a file in this public repository fetched by its GitHub URL; "public" means readable in the repository, as since M03; the milestone does not depend on Pages; enabling it is the owner's setting and is carried to no further milestone by name. | Product, Security |
| 3 | M05's Unsure 3, carried here by name (`milestones/M05/rulings/pr4.md` 16). `M00 gate` is the one required check, `strict` true, no rulesets (read 2026-11-08 UTC). **Ruled at this PR** (`rulings/pr1.md` 9): no Measured cell depends on a required check; the M02 to M05 gates stay as they are; whether `M06 gate` joins is recorded at PR 4 for the record; the setting is the owner's and is carried to no further milestone by name. | Security, Product |
| 4 | Which seat reviews. Proposed: `product`, shown as Regulatory Affairs (SPEC/00 §5). Whether other seats may add their own sign-offs, each with its seat and login, is open; Pharmacovigilance and Legal hold no seat and may be shown as consulted, never as a signature (SPEC/00 §5; CLAUDE.md). | Product |
| 5 | Names proposed here and fixed at PR 2: the files `pages/sign-off.html` and `pages/api/sign-off.json`; the served key `signoffs`; the entry fields `reviewer`, `statement`, `signed`, `signature`, `package`; the records' fields under "Carried to PR 2"; the gate's lists `signoffs_unsigned`, `signoffs_disagreed`, `signoffs_differing`. | Tool Owner, Engineering |
| 6 | The package's form and contents: one zip under `pages/evidence/` plus a `manifest.json` of entries, each with its SHA-256 and the run and artifact it came from, holding the files listed under "Carried to PR 2". Whether a zip in git is acceptable (the M02 artifact is 142 KB; the rest are under 3 KB each) or the package should be one JSON file. Proposed: the zip; fixed at PR 2 or at the lift. | Tool Owner, Product, Data Owner |
| 7 | CI artifacts expire after 90 days. The runs the Measured cells cite are from 2026-10-10 (row 0), 2026-10-10 (row 1), 2026-10-11 (row 2), 2026-10-31 (rows 4, 5) and 2026-11-01 (row 6); the first expire about 2027-01-08. After that the gate cannot compare a package entry with its artifact and reads `unreadable`; the package is then the only copy. Proposed: the gate compares what it can download and names the rest under `unreadable`, which is UNSCORABLE only when nothing is RED; the package records each artifact's expiry date. | Engineering, Product |
| 8 | The gate reads GitHub's API with `GITHUB_TOKEN` (`contents: read`, `actions: read`) and downloads artifacts of this repository. No secret of the door is read. Whether `actions: read` on a pull request from a fork is a concern: this repository takes no fork PRs. | Security, Engineering |
| 9 | The statement's wording: "Reviewed: the evidence package named under `package` is the evidence milestones/README.md cites for its rows at the commit the package names, as read on the day of the signature." It avoids SPEC/00 §11's six words and claims a reading, not a state. Proposed: as written; fixed before the signing commit. | Product, Rule Owner |
| 10 | One person holds all seven seats (R1) and authors every PR, so the reviewer reviews their own work and the page says so. Whether the page needs more than that sentence, such as a second reviewer who holds no seat, which SPEC/00 §5 forbids as a signature. Proposed: the sentence is enough; the sign-off's worth is that CI can read it back, not that the reviewer is independent. | Product, Security |
| 11 | The M03, M04 and M05 gates run on this PR, read their own files by path and do not read the new files. Their readings are after their measurements and are named in the PR body or a comment, not in a cell. Proposed: recorded. | Product, Engineering |
| 12 | The ruling file names this PR as #33, the next number after #32 (the M05 count PR, opened first). If #32 is not opened first, the number is wrong by one and is corrected at PR 2. | Product |
| 13 | Numbers on the plant page: `s-001`, SPEC/00's section numbers, "seven" seats (SPEC/00 §5's) and the manifest's commit `956cd87`. None is a measured result (M03's 7). | Product |
| 14 | The reviewer's seat is copied from `label-impact`'s manifest at `956cd87` by hand. If the manifest changes the seat's login before the lift, the record names the commit it read and the gate reads the manifest at that commit; a stale read is a `signoffs_differing` finding, not a repair here. | Product, Data Owner |
| 15 | The lift's writer rebuilds the page from the served file, as M03's and M05's do; but the signing commit is the reviewer's own, made by hand, so the page in that commit is written by a hand-run writer. The page's content is a copy of records, not evidence; the evidence is the artifacts the package names and the gate's run (P4). Whether a hand-run writer is acceptable for the page in the signing commit. Proposed: yes, with the gate reading page and file equal as parsed JSON. | Engineering, Product |
| 16 | Whether the package carries the ordinary assistant's results (the baseline's observations, M04's served file) beside the agent's. Proposed: yes, as listed; every number in the package is a CI-written result or a copy of data. | Product, Threshold Owner |
