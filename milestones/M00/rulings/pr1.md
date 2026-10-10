---
ruling: m00-pr1
seat:
  - Data Owner
  - Tool Owner
  - Engineering
  - Product
authorises:
  # Data Owner: the goldens, the seed table and clauses, U4, U5, U6, U7
  - goldens/**
  - data/table.json
  - data/clauses.json
  - milestones/M00/citations-checked.md
  - milestones/M00/labels.md
  - milestones/M00/fields.md
  # Tool Owner, with the Data Owner: the answer's shape (fields.md)
  # Engineering: the baseline and the toolchain
  - src/**
  - pyproject.toml
  - uv.lock
  - .python-version
  # Product: the ledger row and the milestone's open detail
  - milestones/README.md
  - milestones/M00/README.md
  - milestones/M00/rulings/pr1.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/citations-checked.md
  - milestones/M00/labels.md
  - milestones/M00/README.md
pr: https://github.com/andaro74/pharmadelta/pull/2
---

# Ruling: M00 PR 1 (plant)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR plants. Row 0 of the ledger is opened with its falsifier, its
seeded commit `df860b7` and its expected gate output. The false state is
committed: `goldens/g-002.yaml`, a `trap`, carries the baseline's own
answer as its `expected`, so the baseline passes a trap. Nothing in this
PR reads the plant: no scorer, no gate, no CI workflow, no test.

## Rulings in this PR

1. **Data Owner, U6 closed.** The five citations of SPEC/00 §10 exist on
   eCFR at the lettering given, checked by hand on 2026-10-09
   (`citations-checked.md`). Two of §10's notes are corrected there;
   the SPEC/00 edit is Product's (README, Unsure 5).
2. **Data Owner, U7 closed.** Scenario 3's paragraph is 21 CFR
   314.150(b)(10), read with 314.94(a)(8)(iv) and 314.97(a). `g-003`
   cites it.
3. **Data Owner, U4.** Three labels, all ANDA generics in the 201.56(d)
   format, originators checked on Drugs@FDA, none Pfizer (`labels.md`).
   The holder is Ardentia Generics, fictional, and every row says so.
4. **Data Owner and Tool Owner, U5.** The row's fields, the clause's
   fields and the answer's fields are as `fields.md`. The answer carries
   `impacted`, `owed` and `escalate`; `escalate` is U3's escalation
   field.
5. **Data Owner.** Nine clauses, each its own id, text copied verbatim
   from the eCFR XML as of 2026-10-07. The two 314.80(a) definitions
   carry a suffix.
6. **Data Owner.** The six goldens are SPEC/00 §7's six scenarios.
   `g-005` and `g-006` expect `BLOCKED` and live in this repository only
   until P. `g-002` is the plant; the Data Owner's answer to it is in
   the README and is not in the golden.
7. **Engineering.** The baseline is `src/baseline/answer.py`: keyword
   matching, no model, over the question and the agent's data. Python
   3.14 under `uv`, as agentkeel.
8. **Product.** Row 0 opens with one falsifier, F0.1, and one seeded
   commit. The gate is PR 2's. Which PR lifts the plant is decided
   after PR 2 goes RED.

## What a reader can falsify

Listed in `milestones/M00/README.md`, "What a reader can falsify".

## What this ruling does not settle

The eight items under Unsure in `milestones/M00/README.md`, each with
its seat. None blocks the plant; items 1 and 4 must be ruled before tag
`m00` and before M01 copies the goldens, respectively.
