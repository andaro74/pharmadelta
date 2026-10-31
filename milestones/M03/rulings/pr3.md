---
ruling: m03-pr3
seat:
  - Engineering
  - Security
  - Product
authorises:
  # Engineering: the repair of the gate's verdict path (Defect 1) and the job summary's label
  - src/m03/gate.py
  # Security: the repair writes nothing new of the environment; the sign-in, the call and what is recorded of them are unchanged
  - src/m03/gate.py
  # Product: the ledger's PR count, the milestone's PR 3 detail and this file
  - milestones/README.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr3.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr1.md
  - milestones/M03/rulings/pr2.md
  - milestones/M02/README.md
  - milestones/M02/rulings/pr3.md
  - milestones/M01/README.md
  - https://github.com/andaro74/pharmadelta/actions/runs/41126878288
  - https://github.com/andaro74/pharmadelta/actions/runs/41171470951
pr: https://github.com/andaro74/pharmadelta/pull/21
---

# Ruling: M03 PR 3 (repair)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR repairs. The cold review of #20 (`milestones/M03/README.md`,
"Cold review of #20") found one defect in the gate's verdict path: a
served answer carrying a call record whose `answer` is neither null nor
an object made `compare()` raise once the door answered 200, and the run
then read UNSCORABLE with no `answers_uncalled` list, where ruling 3 of
`rulings/pr2.md` says RED comes first. `src/m03/gate.py` now checks each
served answer's shape before comparing, records a malformed one under
`unreadable` and does not compare it, and `compare` raises on no input.
The job summary's "compared" column, which printed "not compared
(uncalled)" for every answer not compared, now says why. Nothing under
`pages/` changes; the plant stands and nothing here lifts it. Nothing
here decides the row: the `main` run after #20 merged, 41171470951, is
the measurement, read first in this session, and PR 4 fills the
"Measured" cell from it.

## Rulings in this PR

1. **Engineering (Defect 1).** The repair is as the README's "Defect 1:
   the repair" states: `served_answer_check`, the shape check in `run`
   before the comparison, `compare` made total, the summary label. The
   verdict on every input PR 2's construction run exercised is
   unchanged; the two stubbed pairs that read UNSCORABLE before read RED
   naming the plant after. No new dependency; `pyproject.toml` and
   `uv.lock` are unchanged.
2. **Product, Engineering (Unsure 24, proposed, not ruled).** A
   malformed served answer is read as "could not be read" at the entry:
   UNSCORABLE only when nothing is RED, never RED by itself. Built so;
   the seats confirm or rule it `answers_differing` at PR 4.
3. **Security.** The repair reads nothing new from the environment and
   writes nothing new of it. `result.json` gains `answer_shape` and
   `not_compared` per served answer, both sentences about the served
   file or the door's status, never a value of the secret or a variable.
   The sign-in, the call, `check_url`, `env_set` and the two token claims
   recorded (Unsure 18) are as #20 left them. `.github/workflows/m03.yml`
   is unchanged.
4. **Product.** The `main` run after #20 merged, 41171470951 on
   `0b8d2ec`, read RED, `answers_uncalled` `["g-001"]`,
   `answers_disagreed` `[]`, `answers_differing` `[]`, `written_by_ci`
   true, the same as the PR run 41126878288 on the three lists. It is the
   run the Measured cell cites at PR 4, with the PR run named beside it
   (M01 Unsure 23). Its door reading (end_turn, a parsed object with
   `table_row` null) differs from the PR run's (tool_use, null) and is
   recorded in the README; it decides nothing on the plant.
5. **Product.** "PRs used / cap" is 3 / 4 in the ledger and the
   milestone README. PR 4 is the close: the lift, the Measured cell, the
   row's state, the rulings on the open Unsure items, the tag `m03` after
   its run on `main` is read. A fifth PR is a RED close.
6. **Product (Unsure 29).** This PR is #21.

## What this ruling does not settle

Unsure 25 to 28 (`milestones/M03/README.md`, "Unsure (PR 3)"), each with
its seat; PR 2's 11, 12, 14 to 23; PR 1's 1, 2, 6 and 7. Security is
asked to rule Unsure 12 (`door_host`) before PR 4 opens, because a
ruling of "not written" needs a gate change this PR did not make
(Unsure 27). What the lift serves when the door's `parsed` has
`table_row` null (Unsure 26) and how the call record gets from a CI run
into a commit (Unsure 28) are PR 4's to propose and the seats' to rule.
