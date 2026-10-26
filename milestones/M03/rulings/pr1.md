---
ruling: m03-pr1
seat:
  - Product
  - Data Owner
  - Tool Owner
  - Security
authorises:
  # Data Owner: the scripted answer, its row and its clause as copied; Tool Owner: the served shape
  - pages/api/answers.json
  - pages/detail.html
  # Product: the ledger row, the milestone's open detail, the carried rulings
  - milestones/README.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr1.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/fields.md
  - milestones/M02/README.md
  - milestones/adoption/rulings/row-p-close.md
  - milestones/M03/README.md
  - https://github.com/andaro74/agentkeel/blob/m10/SPEC/10-public-caller.md
  - https://github.com/andaro74/agentkeel/blob/m10/docs/developer/quickstart.md
  - https://github.com/agentkeel-studio/label-impact/blob/8cf0563/manifest.yaml
  - https://github.com/andaro74/agentkeel/actions/runs/39547397318
  - https://github.com/andaro74/agentkeel/actions/runs/38112132210
pr: https://github.com/andaro74/pharmadelta/pull/19
---

# Ruling: M03 PR 1 (plant)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR plants. Row 4 of the ledger is opened with its falsifier F3.1,
its seeded commit `c7edf8f` and its expected gate output. The false
state is committed: `pages/api/answers.json` serves one answer that was
written by hand, with `agent` null and `call` null, and
`pages/detail.html` shows it, labelled scripted. Nothing in this PR
signs in to the door or calls the agent: no code, no workflow, no test.

## Rulings in this PR

1. **Product.** Row 4 opens with one falsifier, F3.1, and one seeded
   commit. The planted failure is the one served answer that no call
   produced. The gate is PR 2's. Which PR lifts the plant is decided
   after PR 2 goes RED.
2. **Data Owner.** The scripted answer's fields are golden `g-001`'s
   `expected`, written by hand into the entry and not read from the
   golden by any code; its row and its clause are copies of
   `data/table.json` and `data/clauses.json` at `b9f84e3`, unchanged. No
   golden, no row and no clause changes (P6, P7). The page shows the
   row as the table holds it and the clause as the file holds it, each
   with its source.
3. **Tool Owner.** The served answer's shape is `id`, `question`,
   `answer` (`table_row`, `clause_id`, `answer_fields`), `row`,
   `clause`, `agent`, `call`, `scripted`. The call record's fields are
   proposed in `milestones/M03/README.md` "Carried to PR 2" and are
   fixed at PR 2, not here.
4. **Security.** Nothing in this PR holds or reads a credential, a door
   URL, a pool id or a client id. The caller's password is a repository
   secret at M03, never a file (SPEC/10 §2: set by hand, outside any
   repository). The names of the secret and the variables are proposed
   under Unsure 3 and ruled at PR 2.
5. **Product.** The reads of label-impact's clone, its manifest and
   agentkeel's deploy runs made on 2026-10-25 are recorded in the
   README as construction. They are reads of the platform's record
   while opening the row, not this repository's measurement (P4); PR
   2's CI run is.
6. **Product, M01 Unsure 23.** A Measured cell cites the run on `main`
   after PR 2 merges, with the PR run named beside it when it was the
   one read at the time. Row 4's expected gate output says so.
7. **Product.** "A public API" is read at M03 as a read API of answers
   produced by CI calls, each with its record (README, "What the public
   API is at M03"). Stated as the assumption the plant is built on, not
   ruled: Unsure 1 names the seats.
8. **Product.** The platform items under the README's "Row P" heading
   are flagged and waited for. None is designed in this repository.
9. **Product.** This PR is #19, the next number on this repository.

## What a reader can falsify

Listed in `milestones/M03/README.md`, "What a reader can falsify".

## What this ruling does not settle

The items under Unsure in `milestones/M03/README.md`, each with its
seat. None blocks the plant. What matters most for the close: what the
public API is (1), where it is served (2), the secret and the variables
(3), the verdict's shape (4), what equality compares (5), and the
deployed agent's answer record reading RED at both deploys (6), which
is label-impact's to repair and may make row 4's cell say the agent was
called and gave no answer.
