---
ruling: m01-pr3
seat:
  - Engineering
  - Product
authorises:
  # Engineering: the reader's verdict, its docstrings and its reason strings
  - src/m01/**
  # Product: the ledger's PR count, the milestone's repair detail and this file
  - milestones/README.md
  - milestones/M01/README.md
  - milestones/M01/rulings/pr3.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/README.md
  - milestones/M01/README.md
  - milestones/M01/rulings/pr2.md
  - https://github.com/andaro74/pharmadelta/actions/runs/38077129178
  - https://github.com/andaro74/agentkeel/blob/m08/scripts/platform_check.py
  - https://github.com/andaro74/agentkeel/blob/m08/.github/workflows/deploy.yml
pr: https://github.com/andaro74/pharmadelta/pull/8
---

# Ruling: M01 PR 3 (repair)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR repairs. It holds what the cold review of PR 2 (#7) found, three
defects in `src/m01/reader.py` and ten inexact sentences, and nothing
else. The plant `eb9b201` stands: `rule-owner` is `null` in label-impact
and its first pull request is open. The CI run on this PR is expected
RED, `finding` `control refused`, naming `rule-owner`. Nothing here
decides the row; PR 2's run 38077129178 was the measurement, and PR 4
fills the "Measured" cell from it and carries the lift (`rulings/pr2.md`
11).

## Rulings in this PR

1. **Engineering (Defect 1).** GREEN's deploy leg is matched on the
   pull request's `merge_commit_sha`, the commit agentkeel deploys
   (`deployable` in `scripts/platform_check.py` at `m08` reads the
   default branch's head). The branch head is never a deploy's commit
   after a merge.
2. **Engineering (Defect 2).** The `finding` `control refused` is
   written only when a check run named `platform-check` from App
   5144253 on the head has a summary that refused the seats check.
   Without one, and with the pull request not read as mergeable, the
   finding is `unassigned, no refusal read`. `F1.1` keeps precedence:
   merged, or read as mergeable, with a seat unassigned.
3. **Engineering (Defect 3).** F1.1's "mergeable" is `mergeStateStatus`
   `CLEAN`, `UNSTABLE` or `HAS_HOOKS` when GraphQL was read, else
   `mergeable_state` `clean`, `unstable` or `has_hooks`. It is judged
   only when a token asked: a no-token REST reading showed `unstable`
   on a head the ruleset blocked, so with no token it is unread for
   F1.1 and the finding cannot be F1.1. The result's `mergeable_judged`
   names the source, the value and why.
4. **Engineering (prose in code).** The module docstring says: "not of
   a login's form"; a 404 on `manifest.yaml` is every seat unassigned,
   RED; a failure before `main` exits 1 with no file and the file is
   the verdict. `read_deploys` names the matrix leg
   `(<repository>, <repository_id>, <commit>, <name>, <rollout>)`.
   `judge_seats` says `admin_read` is `true` on an unassigned seat. The
   RED reason prints `unread` where `mergeStateStatus` was not read.
5. **Product (prose).** `milestones/M01/README.md` is repaired in
   place, sentence by sentence, as listed under "Repair (PR 3)", "Prose,
   repaired in place": the RED, GREEN and UNSCORABLE definitions; the
   `m01.yml` sentence on when the artifact is uploaded; "reads nothing
   from disk"; the `M00 gate` link, run 38077129122; and Unsure 11.
6. **Product (the ledger cell).** Row 1's expected gate output, "RED on
   F1.1 naming `rule-owner`", is not edited. It was written at open and
   the Measured cell is read against it. It reads: RED on the row whose
   falsifier is F1.1, with the `finding` field naming the arm. The
   reading is under Unsure 20 for confirmation at PR 4.
7. **Product.** Row 1's "PRs used / cap" is 3 / 4, here and in the
   ledger. `rulings/pr2.md` is not edited; its rulings 1 and 5 stand as
   the record of what PR 2 claimed, and the README's repair section says
   where they were inexact.
8. **Product.** The construction checks under "Repair (PR 3)" are not
   evidence (P4). The CI run on this PR is, and it is expected RED.

## What a reader can falsify

Listed in `milestones/M01/README.md`, "Repair (PR 3)": the nine
construction checks, which are not evidence (P4), and the expected CI
result on this PR, which is. `git diff main --stat` on this PR touches
`src/m01/reader.py`, `milestones/README.md`, `milestones/M01/README.md`
and `milestones/M01/rulings/pr3.md` only.

## What this ruling does not settle

The items under "Unsure (PR 3)" in `milestones/M01/README.md` (18 to
21), PR 2's Unsure 11 and 15, and PR 1's Unsure 1, 2, 5, 8 and 9, each
with its seat.
