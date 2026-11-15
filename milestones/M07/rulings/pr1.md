---
ruling: m07-pr1
seat:
  - Product
  - Rule Owner
  - Data Owner
  - Security
authorises:
  # Product: the served file's entry (the name, the job, the hand-typed time), the ledger row, the open detail and the attention plan
  - pages/api/second-agent.json
  - milestones/README.md
  - milestones/M07/README.md
  - milestones/M07/rulings/pr1.md
  # Rule Owner: the served file says the agent gives no legal or financial advice and answers no treatment question
  # Data Owner: no golden, row, clause or citation is written or touched
  # Security: no host, account id, pool id, client id, ARN or token in any file
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M01/README.md
  - milestones/M01/rulings/pr1.md
  - milestones/M01/rulings/pr4.md
  - milestones/M06/rulings/pr1.md
  - src/m01/reader.py
  - .github/workflows/m01.yml
  - https://github.com/agentkeel-studio/agent-template/tree/be4e07f0e1d59825ec06d97f5f3fd8ea55e31cf6
  - https://github.com/andaro74/agentkeel/blob/79c7715/agents/refagent/manifest.yaml
  - https://github.com/andaro74/agentkeel/blob/79c7715/SPEC/06-developer-template.md
  - https://github.com/andaro74/agentkeel/blob/79c7715/docs/developer/quickstart.md
  - https://github.com/andaro74/agentkeel/blob/79c7715/milestones/maintenance/README.md
  - https://github.com/andaro74/agentkeel/issues/60
pr: https://github.com/andaro74/pharmadelta/pull/47
---

# Ruling: M07 PR 1 (plant)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR plants. Row 8 of the ledger is opened with its falsifier F7.1,
its seeded commit `c07fbe5` and its expected gate output. The false
state is committed: `pages/api/second-agent.json` serves a time for the
second agent, `3600` seconds typed by hand, with `clock` null, for a
repository that does not exist. Nothing in this PR reads a clock,
creates a repository or writes an agent: no code, no workflow, no test.

## Rulings in this PR

1. **Product.** Row 8 opens with one falsifier, F7.1, and one seeded
   commit. The planted failure is one time with no clock record, named
   in one list (P3). The gate is PR 2's. Which PR carries the lift is
   decided after PR 2 goes RED.
2. **Product (the second agent).** Its name is `record-keep-desk`. Its
   job: a document type is due for disposal; may it be destroyed yet,
   and who signs, citing one row of a fictional bank's retention table
   and one clause of the bank's own retention policy. Chosen by the
   owner on 2026-11-14 (local) from the options the session put. It is
   fictional and small, and has nothing to do with treatment advice.
3. **Product (the clock).** It starts at the second repository's
   `created_at` and stops when the platform has deployed the agent: the
   `completed_at` of agentkeel's `deploy-agent` job for the merge
   commit, conclusion `success`. Both are GitHub's records. From the
   owner's start prompt. It is narrower than agentkeel SPEC/06's stop,
   and the README says so.
4. **Product (where the false time lives).** The owner's decision was
   "a time for the second agent written by hand, with no CI record
   behind it". SPEC/00 §11 forbids an unmeasured number on a page, and
   the owner said to follow the spec where it contradicts. The time is
   planted in the served file alone, labelled, and on no HTML page. The
   reading "a served file is not a page" is Unsure 1.
5. **Product (where the measured time appears).** The ledger's Measured
   cell and one line on the site, each linked to the CI run that wrote
   it. Written at the lift, not here. Which page is Unsure 6.
6. **Product (the attention plan).** `milestones/M07/README.md` carries
   it, with the rules for the stopwatch run. The clock starts only on
   the owner's "go"; the session never creates the repository on its
   own.
7. **Rule Owner.** The served file says the second agent states what
   the bank's policy requires and gives no legal or financial advice.
   No treatment answer appears anywhere (SPEC/00 §2). None of SPEC/00
   §11's six words is used of anything. What rules the agent runs under
   is Unsure 9.
8. **Data Owner.** No golden, row or clause is written, here or in any
   other repository. The second agent cites no CFR paragraph and no
   Federal Register notice, so P7 has nothing to check. Its data is
   ruled in its own repository during the run (Unsure 12).
9. **Security.** No host, account id, pool id, client id, ARN or token
   is written in the four files. The platform items (the App's
   installation on selected repositories; issue #60; a first deploy
   after the platform's maintenance) are flagged in the README and
   designed nowhere here.

## What a reader can falsify

Listed in `milestones/M07/README.md`, "What a reader can falsify".

## What this ruling does not settle

The fourteen items under Unsure in `milestones/M07/README.md`, each
with its seat. None blocks the plant. Items 2, 3 and 7 must be ruled
before the stopwatch run. Nothing in PR 2 or later.
