---
ruling: m00-pr3
seat:
  - Engineering
  - Product
authorises:
  # Engineering: the scorer's UNSCORABLE result and the workflow's directory and step condition
  - src/gate/**
  - .github/workflows/gate.yml
  # Product: the ledger's PR count, the milestone's repair detail and this file
  - milestones/README.md
  - milestones/M00/README.md
  - milestones/M00/rulings/pr3.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/README.md
  - milestones/M00/rulings/pr2.md
pr: https://github.com/andaro74/pharmadelta/pull/4
---

# Ruling: M00 PR 3 (repair)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR repairs. It holds what the cold review of PR 2 (#3) found, one
defect (Q3) and two inexact sentences (Q4, Q6), and nothing else. The
plant `df860b7` stands: `goldens/g-002.yaml` is unchanged, and the CI
run on this PR is expected RED naming `g-002`. Nothing here decides the
row; PR 2's run was the measurement and PR 4 fills the "Measured" cell.

## Rulings in this PR

1. **Engineering (Q3).** `src/gate/score.py` writes `result.json` on
   every failure to score: on `Unscorable` and on any uncaught exception
   it writes `verdict: UNSCORABLE` with the error type and text, the
   traceback when it raised, `commit`, `dirty`, `written_by_ci` and
   `ci`, then exits 2. UNSCORABLE is never RED and never GREEN; the
   result carries no `traps_matched` and no per-golden table. Exit 1 is
   RED and nothing else.
2. **Engineering (Q3).** `.github/workflows/gate.yml` creates the
   artifact directory in a step before the runner, and runs the scorer
   step whenever the runner step ran, crashed or not. The upload keeps
   `if-no-files-found: error`, so an empty directory still fails
   loudly. What is true after this PR: `result.json` is written whenever
   the scorer step starts, which is whenever the runner step ran; before
   that point nothing is written. The step condition is under Unsure 16.
3. **Product (Q4).** The sentence in `milestones/M00/README.md` under
   PR 2's "What a reader can falsify" names the three uses `src/gate/`
   makes of a golden's `expected`: shape check, comparison, and the copy
   into `result.json`, and says none reaches the baseline or the
   verdict.
4. **Product (Q6).** The same section says `git ls-files --eol` shows
   `i/lf` for every non-empty file; the empty `src/__init__.py` shows
   `i/none`.
5. **Product.** Row 0's "PRs used / cap" is 3 / 4. `rulings/pr2.md` is
   not edited; its ruling 4 stands as the record of what PR 2 claimed,
   and the repair section in the M00 README says it was not true at
   PR 2. Which PR lifts the plant is still Product's decision on reading
   PR 2's CI run.

## What a reader can falsify

Listed in `milestones/M00/README.md`, "Repair (PR 3)": the three local
construction checks, which are not evidence (P4), and the expected CI
result on this PR, which is.

## What this ruling does not settle

The items under "Unsure (PR 3)" in `milestones/M00/README.md`, and
PR 1's and PR 2's open Unsure items, each with its seat.
