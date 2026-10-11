---
ruling: m01-pr4
seat:
  - Product
  - Engineering
  - Security
authorises:
  # Product: the Measured cell, the close detail, the Unsure rulings and this file
  - milestones/README.md
  - milestones/M01/README.md
  - milestones/M01/rulings/pr4.md
  # Engineering: one comment above the reader step (Unsure 22)
  - .github/workflows/m01.yml
  # Product with Engineering: the lift, one line of manifest.yaml in agentkeel-studio/label-impact (built there)
  # Security: the merge of label-impact's first pull request under its required check; a repository action, not a file
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/rulings/pr4.md
  - milestones/M01/README.md
  - milestones/M01/rulings/pr2.md
  - milestones/M01/rulings/pr3.md
  - https://github.com/andaro74/pharmadelta/actions/runs/38077129178
  - https://github.com/andaro74/pharmadelta/actions/runs/38097865560
  - https://github.com/agentkeel-studio/label-impact/pull/1
  - https://github.com/agentkeel-studio/label-impact/commit/e26f8826715cec69e6a364c556b26926f13894bd
pr: https://github.com/andaro74/pharmadelta/pull/9
---

# Ruling: M01 PR 4 (close)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path, here and in
`agentkeel-studio/label-impact`.

This PR closes M01 at the cap, 4 / 4. It carries the lift in
label-impact, fills the "Measured" cell from a CI-written result, rules
the five items PR 3 left open and one of PR 1's, repairs one comment in
`m01.yml`, and is followed by the tag `m01` on its merge commit. It
decides nothing about the measurement; PR 2's run 38077129178 is the
measurement.

## Rulings in this PR

1. **Product, with Engineering (the lift).** `manifest.yaml` in
   label-impact carries `rule-owner: andaro74` at `e26f882` on
   `first-agent`, the PLANT comment removed. This is the one edit
   `milestones/M01/README.md` named under "The false state" and nothing
   more. PR 4 carries it as ruled at PR 2 (`rulings/pr2.md` 11).
2. **Product (Measured and state).** Row 1's "Measured" cell cites run
   38077129178 on #7, the run Product ruled on reading it: RED, `finding`
   `control refused`, `seats_unassigned` `["rule-owner"]`,
   `written_by_ci` true. It names beside it the run on `main` at
   `8cdd851`, 38097865560, which carries the same reading. The cell
   equals the expected gate output written at open, so row 1 is GREEN
   and "PRs used / cap" is 4 / 4. Which run a cell cites from M02 on is
   Unsure 23.
3. **Product (Unsure 20).** "RED on F1.1 naming `rule-owner`" in the
   expected gate output is RED on the row whose falsifier is F1.1; the
   result's `finding` names which arm fired, and on this plant that is
   `control refused`. The Measured cell says so in its own words. The
   expected output is not edited: it was written at open.
4. **Product (Unsure 18).** The third finding's name,
   `unassigned, no refusal read`, stands.
5. **Engineering (Unsure 19 and 21).** An import error in the reader
   leaves no artifact and that is "no result": the ledger reads
   artifacts only. No wrapper step. The synthetic checks of `judge` get
   no test file in M01; the next milestone that changes `judge` decides.
6. **Engineering (Unsure 22).** The comment above the reader step in
   `.github/workflows/m01.yml` reads "whenever its `main` runs" and
   names the import-error case. Nothing else in the workflow changes.
7. **Product (PR 1's Unsure 2).** The cap of four is this repository's.
   label-impact's pull request #1 carried the seeded commit and the lift
   and is counted in `milestones/M01/README.md`, not in the ledger's
   cell.
8. **Security (the merge in label-impact).** label-impact's first pull
   request merges under its ruleset's required `platform-check`, posted
   by agentkeel's App on `e26f882`, by the repository's owner. Nothing
   is merged over a check, there or here (`rulings/pr2.md` 9).
9. **Product.** The CI run on this PR reads PENDING, as
   `milestones/M01/README.md` "Expected CI result on this PR" says, and
   PENDING is never written to a cell (`rulings/pr2.md` 8). This PR
   merges on `M00 gate`. After it merges the tag `m01` is placed on the
   merge commit.

## What a reader can falsify

Listed in `milestones/M01/README.md`, "Close (PR 4)": the lift is one
line of one file in label-impact, open the commit; the Measured cell's
two links open CI-written `result.json` files with the values the cell
states; the run on this PR is PENDING with `green_blocked_by` naming the
unread permissions and the unread registry; `git diff main --stat` on
this PR touches `.github/workflows/m01.yml`, `milestones/README.md`,
`milestones/M01/README.md` and `milestones/M01/rulings/pr4.md` only.

## What this ruling does not settle

Unsure 23 in `milestones/M01/README.md`, PR 2's Unsure 11 and 15, and
PR 1's Unsure 1, 5, 8 and 9, each with its seat. GREEN from the reader
needs Unsure 10 and 12 read, which is not M01's. Nothing in M02 or later.
