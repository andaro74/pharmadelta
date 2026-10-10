---
ruling: m00-pr4
seat:
  - Data Owner
  - Product
  - Security
  - Engineering
authorises:
  # Data Owner: the lift, one golden
  - goldens/g-002.yaml
  # Product: the Measured cell, the state definitions, the close detail and this file
  - milestones/README.md
  - milestones/M00/README.md
  - milestones/M00/rulings/pr4.md
  # Security: the administrator merge of #4 over the required check; a repository action, not a file
  # Engineering: the scorer step condition stays (Unsure 16); no file changes
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/README.md
  - milestones/M00/rulings/pr2.md
  - milestones/M00/rulings/pr3.md
  - https://github.com/andaro74/pharmadelta/actions/runs/38058191295
  - https://github.com/andaro74/pharmadelta/actions/runs/38060295880
pr: https://github.com/andaro74/pharmadelta/pull/5
---

# Ruling: M00 PR 4 (close)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR closes M00 at the cap, 4 / 4. It lifts the plant, fills the
"Measured" cell from a CI-written result, rules the two items PR 3 left
open, and is followed by the tag `m00` on its merge commit. It decides
nothing about the measurement; PR 2's run on `main` is the measurement.

## Rulings in this PR

1. **Data Owner and Product (the lift).** `goldens/g-002.yaml` carries
   the Data Owner's answer: `impacted` false, `owed` none, `escalate`
   false, with the PLANT comment removed. This is the one edit
   `milestones/M00/README.md` named under "The false state". The lift is
   in PR 4 because PR 3 was open with the plant standing when the
   decision was due and a fifth PR is a RED close.
2. **Product (Measured and state).** Row 0's "Measured" cell cites the
   run on `main` after PR 2 merged, 38058191295: RED, `traps_matched`
   `["g-002"]`, `written_by_ci` true, commit `47788c0`. It equals the
   expected gate output written at open. The ledger now defines the
   states: GREEN when the CI-written verdict equals the row's expected
   gate output; RED when it does not or there is no measurement. Row 0
   is GREEN. The cell cites the `main` run, not the PR run, because the
   `main` run's commit is a commit in this repository (Unsure 15).
3. **Security (Unsure 17).** PR 3 (#4) is merged over the required
   `M00 gate` check by an administrator. Its run, 38060295880, was RED
   naming `g-002` by design, and is linked in the M00 README. The check
   is not disabled. This PR merges under the check on its own GREEN run.
4. **Engineering (Unsure 16).** The scorer step's condition in
   `.github/workflows/gate.yml` stays. Without it, a runner crash leaves
   an empty directory and the upload fails, so no result would be written
   for the input the review named.
5. **Product.** Row 0's "PRs used / cap" is 4 / 4 and its state is
   GREEN. After this PR merges, the tag `m00` is placed on the merge
   commit and `src/baseline/` is never improved (P5). The Unsure items
   not ruled at M00 carry to the milestone that touches them.

## What a reader can falsify

Listed in `milestones/M00/README.md`, "Close (PR 4)": the lift is one
edit to one golden; the Measured cell's link opens a CI-written
`result.json` with the values the cell states; the run on this PR is
GREEN after the lift.

## What this ruling does not settle

PR 1's Unsure 2 to 8 and PR 2's Unsure 9 to 11 and 13, each with its
seat. Nothing in M01 or later.
