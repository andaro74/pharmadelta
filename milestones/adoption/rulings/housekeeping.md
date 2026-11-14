---
ruling: housekeeping
seat:
  - Product
  - Security
  - Engineering
authorises:
  # Product: SPEC/00's status line says what ADR-0001 did (ruling 1)
  - SPEC/00-overview.md
  # Security, Product: the M01 gate runs on a pull request only when the PR touches the reader or its workflow (ruling 2)
  - .github/workflows/m01.yml
  # Engineering: two f-strings with no placeholder (ruling 3)
  - src/m03/lift.py
  # Product: Unsure rows answered by #39, #40 and #41 marked where they stand (ruling 4)
  - milestones/M03/README.md
  - milestones/M04/README.md
  - milestones/M05/README.md
  - milestones/M06/README.md
  # Product: where the pages are; what the side-by-side page shows (ruling 5)
  - README.md
  - index.html
  - milestones/adoption/rulings/housekeeping.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/adoption/rulings/adopt-spec00.md
  - milestones/adoption/rulings/spec00-errata.md
  - milestones/M01/README.md
  - milestones/M01/rulings/main-run.md
  - milestones/adoption/rulings/m03-relift.md
  - milestones/adoption/rulings/trap-question.md
  - milestones/adoption/rulings/expected-answer.md
  - https://github.com/andaro74/pharmadelta/pull/1
  - https://github.com/andaro74/pharmadelta/actions/runs/43610021022
pr: https://github.com/andaro74/pharmadelta/pull/42
---

# Ruling: housekeeping before M07

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9). It carries no claim,
plants nothing and measures nothing. No row cell of the ledger, no
served file, no JSON block on a page, no gate's code and no agent call
is touched. The owner asked on 2026-11-14 for what was pending in this
repository to be fixed before M07 opens. The repository was read at
`136af05`: no open pull request, every gate on `main` GREEN or success.

## Rulings in this PR

1. **Product (SPEC/00's status line).** Line 3 read "Status: DRAFT, not
   adopted". ADR-0001 is `status: Accepted`, dated 2026-10-09, and the
   adoption pull request #1 merged 2026-10-09 14:20 UTC. The line now
   says so. No section of SPEC/00 changes; this is an erratum, as
   `spec00-errata.md` was.
2. **Security, Product (when the M01 gate runs).** `m01.yml` ran on
   every pull request and read PENDING, exit 3, a failed check, on #36
   to #41: the registry row is unread from here (M01 Unsure 12) and the
   deploy run of 2026-10-11 has scrolled out of the 100 runs the reader
   reads (M01 Unsure 15; `runs_total` 2500 on run 43610021022). Neither
   can change from this repository. `rulings/main-run.md` kept the
   trigger so that a PR that edits the reader is still read. The
   trigger now carries `paths`: `src/m01/**` and the workflow file.
   `workflow_dispatch` stays. Row 1's cell cites its `main` run and
   stands. The gate is not required and was never made so.
3. **Engineering (two f-strings).** `src/m03/lift.py` lines flagged
   F541: the `f` prefix removed, the strings unchanged. A rebuild of
   both pages from the artifacts of runs 43604067436 and 41250971500
   leaves `git status` empty on `pages/`.
4. **Product (Unsure rows marked).** M03's 35 (ruled by #40), M04's 33
   and 35 (ruled by #41), M05's 40 and M06's 42 (ruled by #39) each
   gain a "**Ruled**" note naming the ruling file and the PR. No row's
   earlier text is changed.
5. **Product (the README and the front page).** `README.md` names the
   ledger and the pages' URL, with the sentence that they show saved CI
   records and take no question. `index.html`'s side-by-side cell says
   the page shows the answer the test expects and whether each value
   equals it. No number, no answer.
6. **Product.** This PR is #42, the next number on this repository.

## Read and left as it is

- **Thirteen style findings** of `ruff check src/` in `src/ingest/`,
  `src/m01/reader.py`, `src/m03/gate.py`, `src/m05/lift.py`,
  `src/m06/gate.py` and `src/m06/page.py`. None is an error in what the
  code does. No workflow runs the linter. A gate's code is not edited
  for style after its milestone closed.
- **The evidence package** signed at `37352ef` holds the pages and the
  served answers as at its build, before #39 to #41. The sign-off's
  statement names the package's commit and is still true of it. A
  re-build needs the seat holder's own signing commit (M06 Unsure 36).
- **The artifacts the M06 gate compares** expire from 2027-01-08; after
  that the gate reads UNSCORABLE and the committed zip, its hash and
  the signing commit are the record (M06 Unsure 41).
- **Twenty-seven merged branches** on the remote. Deleting them is the
  owner's.
- **Unsure rows of closed milestones** with no note on the row. Each
  milestone's close ruled or carried its own by name in its
  `rulings/pr4.md`; they were not re-read one by one here.

## Flagged, not built here

- label-impact: the agent wrote prose after its JSON object on `g-002`,
  with an unchecked citation and a word SPEC/00 §11 bans (M04 Unsure
  34). label-impact's to read.
- agentkeel: the finding that a major upgrade whose only refusal is the
  agent's own field cannot be fixed from the agent's `main` (label-impact
  #2 to #4, 2026-10-20). No issue is open in `andaro74/agentkeel`; the
  owner files it there or drops it.
- The registry read for row 1 needs a credential this repository does
  not hold (M01 Unsure 12). The platform's and Security's.

## What a reader can falsify

- `git diff 136af05..<head> --stat` touches the ten files this
  ruling authorises and no other; nothing under `pages/`, `data/`,
  `goldens/` or `src/baseline/`.
- Rows 0 to 8 of `milestones/README.md` are byte-for-byte as at
  `136af05`.
- `gh api repos/andaro74/pharmadelta/pulls/1 --jq .merged_at` reads
  `2026-10-09T14:20:24Z`.
- A pull request that touches neither `src/m01/` nor `m01.yml` shows no
  `M01 gate` check; this one, which edits `m01.yml`, shows it once
  more, PENDING.
