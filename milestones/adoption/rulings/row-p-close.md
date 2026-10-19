---
ruling: row-p-close
seat:
  - Product
authorises:
  # Product: row P's cells and state, and the paragraph beneath the rows
  - milestones/README.md
  - milestones/adoption/rulings/row-p-close.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - https://github.com/andaro74/agentkeel/blob/m10/milestones/README.md
  - https://github.com/andaro74/agentkeel/blob/m10/SPEC/09-per-agent-rules.md
  - https://github.com/andaro74/agentkeel/blob/m10/SPEC/10-public-caller.md
  - https://github.com/andaro74/agentkeel/actions/runs/38400685274
  - https://github.com/andaro74/agentkeel/actions/runs/39143365127
  - https://github.com/andaro74/agentkeel/releases/tag/m09
  - https://github.com/andaro74/agentkeel/releases/tag/m10
pr: https://github.com/andaro74/pharmadelta/pull/17
---

# Ruling: row P closes

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as #1 and #13 to #16 were.
It carries no claim of this repository, plants nothing and measures
nothing here. It fills row P's cells from agentkeel's ledger and sets
the row's state, which SPEC/00 §8 makes the condition for M03. M03 does
not open here; it opens in its own session at its PR 1.

## What row P is

SPEC/00 §8 row P: "Per-agent guardrail rules and one approved public
caller", repository agentkeel, "its own SPEC; not designed here". The
ledger's paragraph beneath the rows says this ledger records only that
it must close before M03 opens. agentkeel built it as two milestones:

| agentkeel row | Claim, in short | Tag | Closed |
|---|---|---|---|
| 9, M09 | an agent is guarded by its own rules on top of a platform baseline, and each rule fires on a question planted for it | `m09` on `833ab2b` | 2026-10-13 |
| 10, M10 | a caller outside the platform reaches an agent only through a door the platform controls, under an identity the manifest admits, with the pinned guardrail on every answer and the caller named in the record; no identity or not admitted is refused and recorded within N | `m10` on `20ac721` | 2026-10-19 UTC |

agentkeel's SPEC/10 §11 R6 ruled the public caller M10, its own claim,
so row P needed both tags. Both exist.

## Rulings in this PR

1. **Product (the cells).** Row P's Falsifiers, Seeded commit and
   Expected gate output cells name agentkeel's, by section and commit,
   and do not restate them: they were written at agentkeel's opens,
   under its SPEC, and this repository never designs them (SPEC/00 §2,
   CLAUDE.md "Platform changes"). The Measured cell copies the two
   rows' CI-written verdict lines from agentkeel's ledger at `m10`, each
   with its envelope, its run and its tag. Nothing is re-measured here.
2. **Product (the state).** GREEN. The ledger's rule reads GREEN when
   the CI-written verdict in Measured equals the row's expected output
   written at open. Row P's expected output was written at agentkeel's
   opens (SPEC/09 §7, SPEC/10 §7), its rows read GREEN at 4 / 4 each,
   and the verdicts are CI-written (P4) in agentkeel's Actions. The
   "PRs used / cap" cell keeps "measured in agentkeel, not here". No
   fourth state word is added for a row measured elsewhere; if Product
   wants one, that is a ledger rule change in its own PR (Unsure 1).
3. **Product (what this opens).** SPEC/00 §8 row 03 "Needs: P closed"
   is met. M03 opens in a new session with its PR 1, under the shape in
   CLAUDE.md. This PR does not write M03's row, claim or false state.
4. **Product.** This PR is #17, the next number on this repository.

## What a reader can falsify

- `git diff main --stat` touches two files: `milestones/README.md` and
  this file. The ledger diff is one row and one paragraph.
- agentkeel's ledger at tag `m10` (the evidence link) holds rows 9 and
  10 with the quoted verdict lines, both `4 / 4`, both GREEN.
- `gh api repos/andaro74/agentkeel/tags` lists `m09` at `833ab2b` and
  `m10` at `20ac721`.
- Runs 38400685274 and 39143365127 exist in agentkeel's Actions and
  are the runs the two rows name.
- Every other row of this ledger is byte-for-byte as before.

## What this ruling does not settle

- **The deployed agent is not yet callable from outside.**
  `agentkeel-studio/label-impact` is at `platform_version 36c97ddaee93`,
  the template's version of 2026-10-10: no `callers` field, no `rules/`,
  guardrail version 5. agentkeel's platform check now refuses a manifest
  with no `callers`, and its upgrade planner reads label-impact as
  current because the template itself is still at `36c97ddaee93`, so no
  upgrade pull request has arrived. Before M03 can measure a call, the
  template is re-made at `m10` (agentkeel, M07's surface), label-impact
  takes the upgrade and adds one caller for this repository (Tool
  Owner, one key, in label-impact), the deploy builds the door, and the
  owner sets the first credential by hand. Row P's close does not do
  any of that; M03 PR 1 names it under row P's heading and waits.
- **label-impact's data is the `m00` copy** (M02 Unsure 6). This
  repository's table has moved since (two `section_title` cells, one
  `section_terms` heading). Data Owner, in label-impact, before M03's
  pages show the agent's answer beside its row.
- **The registry read** the M01 reader lacks (M01 Unsure 12): designed
  at M03 as a read-only role in agentkeel assumed by OIDC. M01's gate
  on `main` runs only by hand until then (`rulings/main-run.md`).
- **The M01 reader's deploy window has closed** (M01 Unsure 15, ruled
  at PR 2 as a known limit). The M01 gate on this PR, run 39191730478,
  reads PENDING on two reasons: "no deploy-agent job of agentkeel's
  deploy.yml naming label-impact at the merge commit concluded success"
  and the registry row unread. The reader reads the latest 100 deploy
  runs; agentkeel deploys every ten minutes, and label-impact's deploy
  of 2026-10-11 has scrolled out. Unsure 15 says a deploy that scrolled
  out is unread until read another way, the registry row. Not a defect
  of this PR, which touches no reader; it is the second thing the M03
  registry read restores. Engineering.
- The two build edits owed with M02 Unsure 23
  (`milestones/adoption/rulings/data-owner-cleanup.md`).
