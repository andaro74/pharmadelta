---
ruling: m04-pr1
seat:
  - Product
  - Data Owner
  - Threshold Owner
  - Tool Owner
  - Security
authorises:
  # Data Owner: the illustration's answer, its row and its clause as copied; Tool Owner: the served shape
  - pages/api/baseline.json
  - pages/side-by-side.html
  # Product: the ledger row, the milestone's open detail, the carried rulings
  - milestones/README.md
  - milestones/M04/README.md
  - milestones/M04/rulings/pr1.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/README.md
  - milestones/M00/rulings/pr2.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr4.md
  - src/baseline/answer.py
  - src/baseline/run.py
  - src/m03/gate.py
  - .github/workflows/gate.yml
  - https://github.com/andaro74/pharmadelta/actions/runs/38058191295
  - https://github.com/andaro74/pharmadelta/actions/runs/41222218526
pr: https://github.com/andaro74/pharmadelta/pull/23
---

# Ruling: M04 PR 1 (plant)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR plants. Row 5 of the ledger is opened with its falsifier F4.1,
its seeded commit `a896442` and its expected gate output. The false
state is committed: `pages/api/baseline.json` serves one
ordinary-assistant answer that was written by hand, with `run` null,
and `pages/side-by-side.html` shows it, labelled an illustration,
beside the deployed agent's served entry. Nothing in this PR runs the
baseline for a page: no code, no workflow, no test.

## Rulings in this PR

1. **Product.** Row 5 opens with one falsifier, F4.1, and one seeded
   commit. The planted failure is the one served ordinary-assistant
   answer that no run of the baseline produced. The gate is PR 2's.
   Which PR lifts the plant is decided after PR 2 goes RED.
2. **Data Owner.** The illustration's answer fields are golden
   `g-001`'s `expected`, written by hand into the entry and not read
   from the golden by any code; its row and its clause are copies of
   `data/table.json` and `data/clauses.json` at `595dd68`, unchanged.
   No golden, no row and no clause changes (P6, P7). The page shows the
   row as the table holds it and the clause as the file holds it, each
   with its source.
3. **Threshold Owner.** The baseline is the control. Not one line of
   `src/baseline/` changes in this milestone (P5); `git diff m00
   --stat -- src/baseline/` is empty on this branch. The page says the
   ordinary assistant is a keyword matcher with no model (M00
   `rulings/pr2.md` 1). Whether PR 2's gate also checks the freeze is
   Unsure 7.
4. **Tool Owner.** The served shape of `pages/api/baseline.json` is
   `id`, `question`, `answer` (`table_row`, `clause_id`,
   `answer_fields`), `row`, `clause`, `run`, `scripted`: M03's shape
   with `run` where the agent's file has `agent` and `call`. The run
   record's fields are proposed in `milestones/M04/README.md` "Carried
   to PR 2" and are fixed at PR 2, not here.
5. **Security.** Nothing in this PR holds or reads a credential. The
   page copies the agent's call record as `pages/api/answers.json`
   serves it: `door_host` stays the hash (M03 Unsure 12). No door URL,
   pool id or client id appears.
6. **Product.** "Live" is read at M04 as a CI run of the frozen
   baseline whose observation the page serves with its run record
   (README, "What live means at M04"). Stated as the assumption the
   plant is built on, not ruled: Unsure 1 names the seat.
7. **Product, Security (M03 Unsure 2, carried).** GitHub Pages is not
   enabled (404 on 2026-10-31). Carried, not ruled: the README's
   Unsure 2 states the constraint (deploy-from-branch serves the root
   or `/docs` only) and proposes that "public" means readable in the
   repository through PR 4. The setting is the owner's to make by
   hand, outside any PR of this cap.
8. **Product, Engineering.** The M03 gate reads `pages/detail.html` and
   `pages/api/answers.json` by path and does not read the new page.
   Its reading on this PR is a reading after the measurement (M03
   `rulings/pr4.md` 6, 22) and is recorded in the PR body, not in the
   ledger. `m03.yml` and `src/m03/gate.py` are not edited.
9. **Product.** The reads of `main`, `src/baseline/`, `pages/`, the
   M03 gate and the Pages setting made on 2026-10-31 are recorded in
   the README as construction. They are reads while opening the row,
   not this repository's measurement (P4); PR 2's CI run is.
10. **Product, M01 Unsure 23.** A Measured cell cites the run on `main`
    after PR 2 merges, with the PR run named beside it when it was the
    one read at the time. Row 5's expected gate output says so.
11. **Product.** This PR is #23, the next number on this repository.

## What a reader can falsify

Listed in `milestones/M04/README.md`, "What a reader can falsify".

## What this ruling does not settle

The items under Unsure in `milestones/M04/README.md`, each with its
seat. None blocks the plant. What matters most for the close: what
"live" means (1), where the pages are served (2), whether the baseline
file is part of the public API (3), whether F3.1 reaches the new page
(4), the run record's fields (5), and whether the gate checks the
freeze (7).
