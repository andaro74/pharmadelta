---
ruling: m05-pr1
seat:
  - Product
  - Rule Owner
  - Data Owner
  - Tool Owner
  - Security
  - Threshold Owner
authorises:
  # Data Owner: the two questions as copied from the goldens; Rule Owner: the page shows them and answers neither; Tool Owner: the served shape
  - pages/api/break-it.json
  - pages/break-it.html
  # Security: no credential, no door host, no pool id in either file
  - pages/break-it.html
  # Product: the ledger row, the milestone's open detail, the carried rulings
  - milestones/README.md
  - milestones/M05/README.md
  - milestones/M05/rulings/pr1.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - goldens/g-005.yaml
  - goldens/g-006.yaml
  - milestones/M03/README.md
  - milestones/M03/rulings/pr4.md
  - milestones/M04/README.md
  - milestones/M04/rulings/pr1.md
  - milestones/M04/rulings/pr4.md
  - milestones/adoption/rulings/row-p-close.md
  - src/m03/gate.py
  - src/m04/gate.py
  - pages/api/answers.json
pr: https://github.com/andaro74/pharmadelta/pull/27
---

# Ruling: M05 PR 1 (plant)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR plants. Row 6 of the ledger is opened with its falsifier F5.1,
its seeded commit `b26a697` and its expected gate output. The false
state is committed: `pages/api/break-it.json` serves scenarios 5 and 6
as blocked, written by hand, with `call` null and `guardrail` null, and
`pages/break-it.html` shows them so, labelled scripted. Nothing in this
PR calls the door, reads a guardrail trace or reads agentkeel's
registry: no code, no workflow, no test.

## Rulings in this PR

1. **Product.** Row 6 opens with one falsifier, F5.1, and one seeded
   commit. The planted failure is the two scenarios shown as blocked
   that the platform's guardrail did not stop. The gate is PR 2's.
   Which PR lifts the plant is decided after PR 2 goes RED.
2. **Data Owner.** The two questions are `goldens/g-005.yaml`'s and
   `goldens/g-006.yaml`'s, copied verbatim at `3b014f1` with each
   golden's `kind` and `expected`. No golden changes; neither states a
   fact of a row (P6). The citation inside `g-006`'s pasted document is
   the question's own text and was checked at SPEC/00 §10 (P7); the page
   names the bracketed note as the injection and adopts nothing from
   it. `row` and `clause` are null on both entries and `why_none` says
   why: a block is not an answer, so there is no row and no clause to
   show (Unsure 9).
3. **Rule Owner.** The page shows an off-label treatment question and a
   prompt injection, says each was blocked, and answers neither. No
   treatment answer appears anywhere (SPEC/00 §2). The agent's rules are
   the platform's and are not read, named or changed here; what the
   trace names when a rule fires is the platform's to say (Unsure 4).
4. **Tool Owner.** The served shape of `pages/api/break-it.json` is
   `id`, `scenario`, `scenario_name`, `kind`, `question`, `expected`,
   `blocked`, `answer`, `row`, `clause`, `why_none`, `agent`, `call`,
   `guardrail`, `scripted`: M03's shape with `blocked` and `guardrail`
   where the agent's file has `answer` and `door`. The call record's
   fields are M03's (`milestones/M03/rulings/pr2.md`); the trace record's
   fields are proposed in `milestones/M05/README.md` "Carried to PR 2"
   and are fixed at PR 2 or at the lift, not here (Unsure 6).
5. **Security.** Nothing in this PR holds or reads a credential. Grep
   `M03_DOOR`, `InitiateAuth`, `Bearer`, `execute-api` and `us-west-2_`
   under `pages/`: no match. No door URL, pool id or client id appears.
   The secret and the three variables set at M03 are not read.
6. **Threshold Owner.** Not one line of `src/baseline/` changes in this
   milestone (P5); `git diff m00 --stat -- src/baseline/` is empty on
   this branch. No probe touched the control's working tree.
7. **Product.** "Wired" is read at M05 as (a): each scenario sent
   through the door by this repository's CI, stopped by the platform's
   guardrail, served with the call record and the trace naming the
   rule (README, "What wired means at M05"). Stated as the assumption
   the plant is built on, not ruled: Unsure 1 names the seat.
8. **Product, Security (M04 Unsure 2, M03's 2, carried).** GitHub Pages
   is not enabled (404 on 2026-10-31). Carried, not ruled: the README's
   Unsure 2 states the constraint and proposes that "public" means
   readable in the repository through PR 4, as at M03 and M04. The
   setting is the owner's to make by hand, outside any PR of this cap.
9. **Security, Product (M04 Unsure 16, M02's and M03's 16, carried).**
   The M02, M03 and M04 gates as required checks on `main` are the
   owner's setting, outside any milestone. Carried by name: the
   README's Unsure 3. Not changed here; `M00 gate` stays the one
   required check.
10. **Product, Engineering.** The M03 gate reads `pages/detail.html` and
    `pages/api/answers.json` by path, the M04 gate reads
    `pages/side-by-side.html`, `pages/api/baseline.json` and
    `pages/api/answers.json` by path, and neither globs `pages/` or
    reads the new files. Their readings on this PR are readings after
    their measurements (M03 `rulings/pr4.md` 6, 22; M04 `rulings/pr4.md`
    22) and are recorded in the PR body or a comment, not in the
    ledger. No gate, workflow or module is edited.
11. **Product.** The reads of `main`, the tags, the goldens, `pages/`,
    the two gates, the door's body as M03 read it, label-impact's
    manifest and the Pages setting made on 2026-10-31 are recorded in
    the README as construction. They are reads while opening the row,
    not this repository's measurement (P4); PR 2's CI run is.
12. **Product, M01 Unsure 23.** A Measured cell cites the run on `main`
    after PR 2 merges, with the PR run named beside it when it was the
    one read at the time. Row 6's expected gate output says so.
13. **Product.** This PR is #27, the next number on this repository.

## What a reader can falsify

Listed in `milestones/M05/README.md`, "What a reader can falsify".

## What this ruling does not settle

The items under Unsure in `milestones/M05/README.md`, each with its
seat. None blocks the plant. What matters most for the close: what
"wired" means (1), which field of the door's body is the trace and
whether it names the rule (4, a platform item), what "agentkeel's
planted failures" reaches (5), the names fixed at PR 2 (6), and what
the row reads when the door answers instead of stopping (13).
