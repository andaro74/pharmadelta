---
ruling: m00-pr2
seat:
  - Threshold Owner
  - Product
  - Security
  - Engineering
authorises:
  # Engineering: the gate and the workflow that runs it
  - src/gate/**
  - .github/workflows/gate.yml
  # Security: line endings
  - .gitattributes
  # Product: the ledger's PR count and the milestone's PR 2 detail
  - milestones/README.md
  - milestones/M00/README.md
  - milestones/M00/rulings/pr2.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/README.md
  - milestones/M00/rulings/pr1.md
pr: https://github.com/andaro74/pharmadelta/pull/3
---

# Ruling: M00 PR 2 (measure)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR measures. It adds the gate that reads the plant `df860b7`:
`src/gate/score.py` compares each baseline observation with its golden,
and `.github/workflows/gate.yml` runs the baseline and the scorer in CI
and writes both outputs as the artifact `m00-gate-<sha>`. On `df860b7`'s
goldens the gate goes RED naming `g-002`. The CI run on this PR is the
measurement (P4); the ledger's "Measured" cell is filled at PR 4 with
that run's link and nothing else. Nothing in this PR lifts the plant.

## Rulings in this PR

1. **Threshold Owner (PR 1 Unsure 1).** The baseline stays the keyword
   matcher in `src/baseline/answer.py`, with no model. It freezes at tag
   `m00` and is never improved after (P5). The M04 side-by-side page
   must say what it is: a keyword matcher, not an assistant.
2. **Product (PR 1 Unsure 1).** Option C, a labelled live model panel
   beside the control on the M04 page, is noted for M04. It is not
   decided now; M04's open detail decides it.
3. **Security.** PR 2 may add `.gitattributes` setting LF line endings
   for every text file. The index already stores every file as LF, so
   the rule changes no stored content. The check that every PR carries
   a ruling file is deferred to a milestone that can plant its own
   failure (P2, P3); M00's one plant is `g-002`.
4. **Engineering.** The gate is `src/gate/score.py`. For an `ordinary`
   or `trap` golden a match is: `table_row` equal, `clause_id` equal,
   both present in `data/`, and `answer_fields` equal as a whole, same
   keys and same values (SPEC/00 §6, `fields.md`). For a `guardrail` or
   `redteam` golden a match is the string `BLOCKED`, which the baseline
   never produces, so both are recorded as not matched (§7). The verdict
   is F0.1 and nothing else: RED when any `trap` is matched, naming each
   one; GREEN otherwise. Every other match is recorded, not judged. The
   job fails on RED and the artifact is written whether or not it does.
5. **Product.** Row 0's "PRs used / cap" is 2 / 4. Which PR lifts the
   plant is decided when the CI run on this PR is read, and is recorded
   in `milestones/M00/README.md`, not here.

## What a reader can falsify

Listed in `milestones/M00/README.md`, "Open detail (PR 2)".

## What this ruling does not settle

The items under "Unsure (PR 2)" in `milestones/M00/README.md`, and
PR 1's Unsure 2 to 8, each with its seat.
