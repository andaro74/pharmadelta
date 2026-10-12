---
ruling: m01-main-run
seat:
  - Product
  - Security
authorises:
  # Product: when the M01 gate runs, now that row 1 is measured
  - .github/workflows/m01.yml
  - milestones/M01/README.md
  - milestones/M01/rulings/main-run.md
  # Security: the trigger change reads nothing new and removes a run; no token or permission changes
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M01/README.md
  - milestones/M01/rulings/pr2.md
  - milestones/M01/rulings/seat-read.md
  - https://github.com/andaro74/pharmadelta/actions/runs/38097865560
  - https://github.com/andaro74/pharmadelta/actions/runs/38193151353
pr: https://github.com/andaro74/pharmadelta/pull/16
---

# Ruling: M01 gate, the run on main

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as #1 and #13 to #15 were.
It carries no claim, plants nothing and measures nothing. M01 is closed
at tag `m01`; row 1 is GREEN on its measured RED and does not change.
The ledger is not touched. M03 does not open here.

## Why

`m01.yml` ran on every push to `main`. Row 1's Measured cell cites the
`main` run at `8cdd851`, 38097865560, read 2026-10-11 after #7 merged.
Every push run since the lift has read PENDING, exit 3, and the job
has shown as failed on every `main` commit: the latest, 38193151353 on
`3efa949`, reads "no seat is read as unassigned, and GREEN is not
shown: the registry row for label-impact is unread", the one reason
left after #15. That reason does not change with any commit in this
repository until M03 designs the registry read (Unsure 12). A run that
cannot read differently from the last one judges nothing new. The red
check on `main` was read twice as a defect of a PR that did not cause
it (#14, #15).

## Rulings in this PR

1. **Product (Unsure 14).** The `push` trigger is removed from
   `m01.yml`. The workflow keeps `pull_request`, so a PR that edits the
   reader runs it against its branch, and `workflow_dispatch`, so
   `gh workflow run m01.yml --ref main` reads `main` on demand. The
   header comment says so. `M01 gate` stays not required, as PR 2 ruled.
   Row 1's cell and its runs stand; a run that no longer happens is not
   a measurement withdrawn.
2. **Security.** The change reads nothing new. `M01_READ_TOKEN` and
   `GITHUB_TOKEN` are passed as #15 left them, to fewer runs. No
   permission changes.
3. **Product.** This PR is #16, the next number on this repository.

## What a reader can falsify

- `git diff main --stat` touches three files: `.github/workflows/m01.yml`,
  `milestones/M01/README.md` and this file. The workflow diff removes
  two lines under `on:` and adds a comment.
- `gh run list --workflow m01.yml --branch main` lists no run created
  after this PR's merge commit unless dispatched by hand.
- The M01 gate on this PR runs (it is a pull request) and reads PENDING
  on the registry only, as 38193151353 did. The job fails; not
  required. M00 and M02 gates pass.
- After merge, `gh workflow run m01.yml --ref main` creates one run that
  reads the same.

## What this ruling does not settle

- The registry read (Unsure 12), M03.
- Whether the push run is restored when the registry read lands, so
  `main` is judged GREEN on every commit. Product, at M03.
