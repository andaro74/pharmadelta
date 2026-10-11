---
ruling: m02-pr3
seat:
  - Data Owner
  - Product
  - Engineering
  - Security
authorises:
  # Data Owner: the lift, and the two section_title cells Unsure 12 ruled
  - data/clauses.json
  - data/table.json
  # Product: the Measured cell and the row's state, the close detail, the Unsure rulings and this file
  - milestones/README.md
  - milestones/M02/README.md
  - milestones/M02/rulings/pr3.md
  # Engineering, Security: the two cold-review findings are recorded, not repaired; no file changes
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/fields.md
  - milestones/M02/README.md
  - milestones/M02/rulings/pr1.md
  - milestones/M02/rulings/pr2.md
  - https://github.com/andaro74/pharmadelta/actions/runs/38154731153
  - https://github.com/andaro74/pharmadelta/actions/runs/38153322315
  - https://www.ecfr.gov/api/versioner/v1/versions/title-21.json?section=314.98
  - https://www.ecfr.gov/api/versioner/v1/full/2016-12-23/title-21.xml?part=314&section=314.98
  - https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/f39ee08d-73db-71b9-e053-2995a90a877c.xml
  - https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/24837d82-0f3f-4482-9af0-31e5f675c30f.xml
pr: https://github.com/andaro74/pharmadelta/pull/12
---

# Ruling: M02 PR 3 (close)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR closes M02 at 3 / 4. The cold review of #11 found nothing that
changes a verdict or a compared field, so the repair slot is skipped and
the milestone's third PR is the close. It carries the lift, corrects the
two `section_title` cells Unsure 12 ruled, fills the "Measured" cell
from a CI-written result and writes the row's state, and is followed by
the tag `m02` on its merge commit. It decides nothing about the
measurement; the `main` run after #11 merged, 38154731153, is the
measurement.

## Rulings in this PR

1. **Product (Unsure 22).** The close is the milestone's third PR. Its
   ruling file is `pr3.md` and "PRs used / cap" is 3 / 4, one ruling
   file per PR used. `rulings/pr2.md` 8 and 10 named the close "PR 4":
   that is the close slot of CLAUDE.md's PR shape, which this PR fills.
   Those rulings are not reopened.
2. **Data Owner (the lift).** `data/clauses.json`: `314.98(a)`'s
   `effective_date` is `2016-12-23`, the one version the versioner lists
   for 314.98, and the `PLANT` key is removed. This is the one edit
   `milestones/M02/README.md` named under "The false state" and nothing
   more. The close carries it as ruled at PR 2 (`rulings/pr2.md` 8).
3. **Data Owner (Unsure 12, as ruled at PR 2).** `data/table.json`:
   `metformin.6`'s `section_title` is `ADVERSE REACTIONS` and
   `metoprolol-tartrate.5`'s is `WARNINGS AND PRECAUTIONS`, the headings
   as the SPLs print them (`fields.md`: "as printed") and as run
   38154731153 read them. `src/ingest/hand/table.json` is not touched;
   `section_title` is derived, not carried. The gate is not changed.
4. **Product (Measured and state; Unsure 24).** Row 2's "Measured" cell
   cites the run on `main` after #11 merged, 38154731153 on `e8c3690`,
   artifact `m02-gate-e8c3690d3877f8603620f3cb56c9104e530ec824`: RED,
   `clauses_mismatched` `["314.98(a)"]`, `rows_mismatched`
   `["metformin.6", "metoprolol-tartrate.5"]`, `unreadable` `[]`,
   `written_by_ci` true. The PR run on #11, 38153322315, is named beside
   it as the run read at the time; it read the same. The expected gate
   output written at open names the plant only, so the cell does not
   equal it and row 2 is RED under the ledger's rule, with the finding
   beside it: the hand-built seed was not fully reproduced from the
   source; the build was. The expected output is not edited and no case
   is folded in the gate. From here on, a `main` run that reads
   UNSCORABLE is not a measurement: the cell is owed another run, and
   the README says so rather than citing it.
5. **Engineering, Security (Unsure 23).** The cold review of #11 found
   two things in `src/ingest/gate.py`: `fields_recorded_not_compared.rows`
   lists `section_terms` twice, and the top-level UNSCORABLE path writes
   `result.json` without `sources/`, so PR 2's ruling 2 ("every response
   read is written into the artifact") does not hold on that path.
   Neither touches the comparison or the verdict; the measurement stands
   as read. No repair PR in this milestone. Both are repaired in the next
   PR that edits `gate.py`, and the Security property is restated there.
6. **Data Owner (Unsure 25; PR 1's 1 and 8).** The hand confirmations
   are asked of the Data Owner at this PR, to be done in a browser: the
   eight effective dates against each section's "Timeline" on ecfr.gov,
   and `section_terms` re-read on the three DailyMed pages. Nothing in
   this PR does them by machine or calls them done. If the Data Owner
   gives dates before this PR merges, they are recorded under Unsure 25
   in the README; otherwise both stay owed before M03 shows a clause.
7. **Product (Unsure 26).** This PR is #12, the next number on this
   repository.

## What a reader can falsify

Listed in `milestones/M02/README.md`, "What a reader can falsify" under
"Close (PR 3)".

## What this ruling does not settle

Unsure 13 to 20 (PR 2) and PR 1's 2, 5, 6, 9 and 10, each with its
seat, carry to the milestone that touches them. Unsure 16 (whether
`M02 gate` is made required on `main`) is a repository setting and is
not changed here. M01 Unsure 1 and M00 Unsure 5 are owed a PR of their
own outside any cap (`milestones/adoption/rulings/spec00-errata.md`).
