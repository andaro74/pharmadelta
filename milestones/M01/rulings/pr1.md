---
ruling: m01-pr1
seat:
  - Product
  - Data Owner
  - Tool Owner
  - Engineering
authorises:
  # Product: the ledger row and the milestone's open detail
  - milestones/README.md
  - milestones/M01/README.md
  - milestones/M01/rulings/pr1.md
  # Data Owner: which goldens and data move to label-impact (built there)
  # Tool Owner, with Engineering: the rewritten tool's contract (built there)
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/fields.md
  - milestones/M01/README.md
  - https://github.com/agentkeel-studio/label-impact/pull/1
pr: https://github.com/andaro74/pharmadelta/pull/6
---

# Ruling: M01 PR 1 (plant)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path, here and in
`agentkeel-studio/label-impact`.

This PR plants. Row 1 of the ledger is opened with its falsifier F1.1,
its seeded commit `eb9b201` in label-impact and its expected gate output.
The false state is committed there: `manifest.yaml` carries
`rule-owner: null` while six seats are `andaro74`, and the first pull
request is open. Nothing in this repository reads it: no reader, no
workflow, no test.

## Rulings in this PR

1. **Product.** Row 1 opens with one falsifier, F1.1, and one seeded
   commit. The planted failure is the one null seat. The reader is
   PR 2's. Which PR lifts the plant is decided after PR 2 goes RED.
2. **Product.** The template is used as it stands, head `66ca2e4`, made
   from agentkeel `36c97dd` (`m07~1`), not re-made at `m08`. The agent
   files are the same at both commits; the README and `platform_version`
   are not. SPEC/00 §3's sentence is owed a one-line edit (README,
   Unsure 1). Ruled 2026-10-10 on the two options the session put.
3. **Data Owner.** Goldens `g-001` to `g-004`, `data/table.json` and
   `data/clauses.json` move to label-impact byte for byte as at `m00`.
   `g-005` and `g-006` stay here until P (SPEC/00 §7). The fields are
   `milestones/M00/fields.md`'s. M00 PR 1's Unsure 4 (`g-001`'s
   `follow-rld`) was to be ruled before M01 copied the goldens and was
   not; the golden moves as it stands and the item carries (README,
   Unsure 9).
4. **Tool Owner.** The tool's contract, `tools/find_label_row.json` in
   label-impact: input `label` (one of the three labels) and `section`
   (one of `bw`, `5`, `5.1`, `6`, `8.1`); output `found`, `row` (the
   seventeen fields of `fields.md`, or null), `clause_candidates` (the
   row's `requirement` first, then the clauses its section is read
   with, every one a key of `data/clauses.json`) and `source`
   (`dynamodb` or `data/table.json`). Strict both ways. The tool returns
   the row and decides nothing; the three answer fields are the model's.
5. **Engineering.** `agent.py` in label-impact keeps refagent's loop,
   `rights_rows` and `answer` by name (so `server.py` is the template's,
   unchanged), replaces `check_availability` with `find_label_row`, and
   reads its file fallback from `data/table.json` beside it. The prompt
   names the three labels, the seven rows, the five sections and the
   three answer fields, and says the agent assesses labeling impact and
   nothing else. Guardrail and model as the template ships them.
6. **Product.** The platform check's refusal on pull request #1, once
   posted, is recorded in the README as what was observed at open. It is
   agentkeel's control firing on this plant, not this repository's
   measurement; it produces the evidence a validation would need.

## What a reader can falsify

Listed in `milestones/M01/README.md`, "What a reader can falsify".

## What this ruling does not settle

The items under Unsure in `milestones/M01/README.md`, each with its
seat. None blocks the plant. Item 8 (the App's repository access) is
agentkeel's and is flagged, not designed, here.
