---
ruling: m07-pr3
seat:
  - Engineering
  - Security
  - Product
authorises:
  # Engineering: the two repairs to the gate
  - src/m07/gate.py
  # Security: nothing new is read or written; no token and no redirect URL reaches the result
  - src/m07/gate.py
  # Product: the ledger's PR count, the main run's reading and the milestone's PR 3 detail
  - milestones/README.md
  - milestones/M07/README.md
  - milestones/M07/rulings/pr3.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M07/README.md
  - milestones/M07/rulings/pr1.md
  - milestones/M07/rulings/pr2.md
  - src/m07/gate.py
  - .github/workflows/m07.yml
  - https://github.com/andaro74/pharmadelta/actions/runs/43770733652
  - https://api.github.com/repos/andaro74/agentkeel/actions/jobs/114389865133
  - https://api.github.com/repos/andaro74/agentkeel/actions/jobs/115060689514
  - https://api.github.com/repos/andaro74/agentkeel/actions/runs/42967373936/jobs
  - https://github.com/andaro74/agentkeel/blob/main/.github/workflows/deploy.yml
pr: https://github.com/andaro74/pharmadelta/pull/49
---

# Ruling: M07 PR 3 (repair)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR repairs. A session that did not write the gate read it cold at
`3292219` and found two defects. Both are repaired in
`src/m07/gate.py`. Nothing is lifted: `pages/api/second-agent.json` and
every page are unchanged, and the gate reads the plant as it did.

## Rulings in this PR

1. **Product, on reading run 43770733652.** The `main` run after #48
   merged, at `3292219`, wrote RED, `times_unrecorded` `["a-002"]`,
   `times_disagreed` `[]`, `times_differing` `[]`, `unreadable` `[]`,
   `written_by_ci` true, `api_reads` `[]`. It equals row 8's expected
   output and is the Measured cell's source. The cell is filled at PR 4.
2. **Engineering; D1.** A summary that cannot be rendered or printed no
   longer changes a verdict already written: `write_result` writes
   `result.json` first and guards what follows. The three difference
   messages use `...` in place of `…`.
3. **Engineering; D2.** A job name that GitHub cut just after a value's
   comma is read without that comma. The commit is then read whole.
4. **Product, by the owner's start prompt.** Limits are recorded under
   Unsure with their seat and not repaired: Unsure 30 to 38 and 40. The
   owner said "go" to the repair of D1 and D2 as proposed.
5. **Security.** The repair reads nothing new and writes nothing new.
   The review found no path by which the token or a redirect URL reaches
   `result.json`. The workflow is unchanged. No host, account id, pool
   id, client id, ARN or token is written in any file of this PR. No
   repository was created and no step that starts the clock was taken;
   the session's only request about `agentkeel-studio/record-keep-desk`
   was a GET that answered 404.
6. **Product; Unsure 2, 3, 7, 17, 19, 20, 23: not ruled.** The start
   prompt listed the seven and left each blank. Each stands at its
   proposal and is open (Unsure 39). 2, 3 and 7 must be ruled before the
   stopwatch run.
7. **Product.** The construction readings are recorded in the README as
   construction and decide nothing (P4). "PRs used / cap" is 3 / 4. PR 4
   carries the lift, the Measured cell and the tag (`rulings/pr2.md`
   13).
8. **Product.** This PR is #49, the next number on this repository
   after #48 (Unsure 29).

## What a reader can falsify

Listed in `milestones/M07/README.md`, "What a reader can falsify" under
PR 3.

## What this ruling does not settle

The items under Unsure (PR 3) in `milestones/M07/README.md`, 29 to 40,
and those still open from PR 1 and PR 2. Before the stopwatch run: PR
1's 2, 3 and 7; that the second repository is public (19); that the
agent's files go in its first pull request (23); what a failed first
deploy does to the reading (38); and whether the read-back is exercised
in CI by a dry run first (36).
