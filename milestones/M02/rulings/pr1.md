---
ruling: m02-pr1
seat:
  - Product
  - Data Owner
  - Tool Owner
  - Engineering
authorises:
  # Data Owner: the field added to each clause, and the plant
  - data/clauses.json
  # Product: the ledger row, the milestone's open detail, two carried rulings
  - milestones/README.md
  - milestones/M02/README.md
  - milestones/M02/rulings/pr1.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/fields.md
  - milestones/M01/README.md
  - milestones/M02/README.md
  - https://www.ecfr.gov/api/versioner/v1/versions/title-21.json?section=314.98
  - https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/24837d82-0f3f-4482-9af0-31e5f675c30f/history.json
pr: https://github.com/andaro74/pharmadelta/pull/10
---

# Ruling: M02 PR 1 (plant)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR plants. Row 2 of the ledger is opened with its falsifier F2.1,
its seeded commit `4379556` and its expected gate output. The false
state is committed: `data/clauses.json` carries `effective_date` on
each clause, and `314.98(a)`'s is `2026-10-07`, the snapshot date,
which the eCFR versioner does not list as a version of 314.98. Nothing
in this PR reads it: no ingestion code, no workflow, no test.

## Rulings in this PR

1. **Product.** Row 2 opens with one falsifier, F2.1, and one seeded
   commit. The planted failure is the one clause whose effective date
   is the snapshot date. The build and the gate are PR 2's. Which PR
   lifts the plant is decided after PR 2 goes RED.
2. **Data Owner.** Each clause carries one new field, `effective_date`:
   the eCFR versioner's latest amendment date for the clause's section,
   the version the seed text is from. Defined in `milestones/M02/README.md`
   under "The field added", as `milestones/M00/fields.md` requires of a
   field change after M00. The eight dates not planted were read from
   the versioner on 2026-10-11; the hand confirmation is owed (README,
   Unsure 1).
3. **Data Owner.** No clause text, no row, no golden changes. The
   plant is a date, not a citation: `21 CFR 314.98(a)` is the checked
   paragraph it was at `m00` (P7). The `PLANT` key beside it says what
   it is and is removed with the lift.
4. **Product, M01 Unsure 23.** A Measured cell cites the run on `main`
   after PR 2 merges, because its commit is a commit in this repository
   (M00 Unsure 15). When the run read at the time was the PR run, it is
   named beside the `main` run. Row 2's expected gate output says so.
   One rule from here on.
5. **Product, M01 Unsure 1.** SPEC/00 §3's "re-made at `m08`" rides in
   a PR of its own, outside any milestone's cap, with the two §10
   one-line edits M00's Unsure 5 owes. This session does not open it.
   It is owed, named, and not folded into M02's cap.
6. **Product.** The versioner read of 2026-10-11 is recorded in the
   README as construction. It is a read of the source while building
   the plant, not this repository's measurement (P4); PR 2's CI run is.
7. **Data Owner, Tool Owner, Engineering; Unsure 3.** A row's version
   stays its set id and read date (SPEC/00 §9); no field is added to a
   row in M02. DailyMed's XML API serves the current version only
   (read 2026-10-11, README "The DailyMed read"). PR 2's build reads
   the history first; a version published after the row's
   `label_read_on` means the source at that version cannot be read by
   machine, and the result is UNSCORABLE naming the row and its page,
   never RED. The SPL version number and `effectiveTime` go in the
   artifact beside the row. Ruled on the session's recommendation,
   2026-10-11, after the three read-only checks it names.
8. **Data Owner; Unsure 4.** The build derives nine fields from
   DailyMed and carries six from a hand file; the gate compares the
   nine. As proposed in the README.

## What a reader can falsify

Listed in `milestones/M02/README.md`, "What a reader can falsify".

## What this ruling does not settle

The items under Unsure in `milestones/M02/README.md` not marked ruled,
each with its seat. None blocks the plant. Items 3 and 4 are ruled
above; what remains open is the hand confirmation of the dates and the
section terms (1, 8), the meaning of a clause's date (2), the Federal
Register feed (5), when label-impact takes the rebuilt data (6), the
PR number (7), the metformin finding (9) and the provenance fields (10).
