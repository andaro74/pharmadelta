---
ruling: m01-pr2
seat:
  - Engineering
  - Security
  - Product
authorises:
  # Engineering: the reader and the workflow that runs it
  - src/m01/**
  - .github/workflows/m01.yml
  # Security: what the workflow may read, and with what token
  - .github/workflows/m01.yml
  # Product: the ledger's PR count and the milestone's PR 2 detail
  - milestones/README.md
  - milestones/M01/README.md
  - milestones/M01/rulings/pr2.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M01/README.md
  - milestones/M01/rulings/pr1.md
  - https://github.com/agentkeel-studio/label-impact/pull/1
  - https://github.com/agentkeel-studio/label-impact/runs/114267967935
pr: https://github.com/andaro74/pharmadelta/pull/7
---

# Ruling: M01 PR 2 (measure)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR measures. It adds the reader that reads the plant `eb9b201` in
`agentkeel-studio/label-impact`: `src/m01/reader.py` reads the first
pull request at its head, the seats, the check runs, agentkeel's deploy
runs and the registry from GitHub's API, and
`.github/workflows/m01.yml` runs it in CI and writes the result as the
artifact `m01-gate-<sha>`. On `eb9b201` the reader goes RED naming
`rule-owner`. The CI run on this PR is the measurement (P4); the ledger's
"Measured" cell is filled at PR 4 with that run's link and nothing else.
Nothing in this PR lifts the plant, and nothing in label-impact changes.

## Rulings in this PR

1. **Engineering.** The reader is `src/m01/reader.py`. It judges ledger
   row 1 as `milestones/M01/README.md` "Carried to PR 2" defines it. RED
   while any of the seven seats at the head is not a login that
   administers the repository, each named; the finding is F1.1 when the
   pull request is also found `clean` or merged, else "control refused".
   GREEN only when every seat is read as `admin`, the pull request is
   merged, its `deploy-agent` job succeeded and the registry holds
   `label-impact`. PENDING when neither, naming what is missing.
   UNSCORABLE when the pull request, the manifest or the check runs
   cannot be read, never RED or GREEN. Every reading is written beside
   the verdict; anything unread is written as unread with the status and
   the token, and is never read as a pass. The job fails on anything but
   GREEN; the artifact is written whenever the reader step started.
2. **Security.** The workflow reads two public repositories,
   `agentkeel-studio/label-impact` and `andaro74/agentkeel`, through
   GitHub's REST and GraphQL APIs with this repository's `GITHUB_TOKEN`
   and `contents: read`. It reads no secret of this repository and
   holds no credential for the organisation or for AWS. A seat's
   collaborator permission and the registry are therefore unread; which
   token or role reads them is ruled later (README, Unsure 10 and 12),
   not assumed here.
3. **Security.** The seat-permission read, when a token is ruled, asks
   the same two endpoints agentkeel's `src/validate/seats.py` asks, and
   nothing wider: the repository's owner, and one login's permission.
4. **Product.** Row 1's "PRs used / cap" is 2 / 4. Which PR lifts the
   plant is decided when the CI run on this PR is read, and is recorded
   in `milestones/M01/README.md`, not here.
5. **Product.** The expected CI result on this PR is RED naming
   `rule-owner`, with `finding` "control refused": agentkeel's platform
   check refused the head for the one null seat, and the pull request
   is not mergeable. That reading, written by CI, is what the ledger's
   expected output names. PR 1's Unsure 4 is answered by the same
   record: the check refused the seats only and passed the goldens.

Added on reading run 38077129178, before this PR left draft:

6. **Security, Engineering (Unsure 10).** No token beyond `GITHUB_TOKEN`
   is set for M01. The seat-permission read matters only for GREEN, which
   M01 does not need to close: the Measured cell takes the RED run on
   the plant. Ruled again when a milestone needs GREEN from this reader.
7. **Security, Product (Unsure 12).** The registry stays unread through
   M01. The read is designed at M03 as a read-only role in agentkeel
   assumed by OIDC, flagged there.
8. **Product (Unsure 13).** PENDING stands: exit 3, fails the job, never
   written to a Measured cell. The cell takes RED or GREEN only.
9. **Security, Product (Unsure 14).** `M01 gate` is not made a required
   check on `main`. No PR of M01 is merged over a check.
10. **Data Owner, Tool Owner (Unsure 16).** PR 1's Unsure 4 is closed by
    the platform check's record at `eb9b201`: the goldens passed.
11. **Product.** The lift is carried by PR 4. PR 3 repairs what the cold
    review of #7 finds, or is skipped. Recorded in
    `milestones/M01/README.md`, "After this PR goes RED".

## What a reader can falsify

Listed in `milestones/M01/README.md`, "Open detail (PR 2)".

## What this ruling does not settle

Unsure 11 and 15 in `milestones/M01/README.md`, and PR 1's Unsure 1, 2,
5, 8 and 9, each with its seat. GREEN from this reader needs Unsure 10
and 12 read, which is not M01's.
