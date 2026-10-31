---
ruling: m04-pr4
seat:
  - Product
  - Engineering
  - Threshold Owner
  - Data Owner
  - Tool Owner
  - Security
authorises:
  # Engineering: the lift path (Unsure 26, 28, 30): the writer that rebuilds the pages from the m04 workflow's own artifact
  - src/m04/lift.py
  # Product, Data Owner, Tool Owner: the lift, the two pages rebuilt from the CI record
  - pages/api/baseline.json
  - pages/side-by-side.html
  # Threshold Owner: not one line of src/baseline/ changes; the record's baseline_commit is the artifact's
  - pages/api/baseline.json
  # Security: the lift reads no secret, no variable and no network; no workflow changes
  - src/m04/lift.py
  # Product: the Measured cell, the row's state, 4 / 4, the close detail, the Unsure rulings and this file
  - milestones/README.md
  - milestones/M04/README.md
  - milestones/M04/rulings/pr4.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/fields.md
  - milestones/M00/README.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr4.md
  - milestones/M04/README.md
  - milestones/M04/rulings/pr1.md
  - milestones/M04/rulings/pr2.md
  - milestones/M04/rulings/pr3.md
  - src/m04/gate.py
  - src/baseline/run.py
  - .github/workflows/m04.yml
  - https://github.com/andaro74/pharmadelta/actions/runs/41234548875
  - https://github.com/andaro74/pharmadelta/actions/runs/41233100816
  - https://github.com/andaro74/pharmadelta/actions/runs/41250971500
pr: https://github.com/andaro74/pharmadelta/pull/26
---

# Ruling: M04 PR 4 (close)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR closes M04 at the cap, 4 / 4. It carries the lift, fills the
"Measured" cell from a CI-written result and writes the row's state,
rules or carries by name every open Unsure item of PR 1, PR 2 and PR 3,
and is followed by the tag `m04` on its merge commit after its run on
`main` is read. It decides nothing about the measurement: the `main` run
after #24 merged, 41234548875, is the measurement, read again at this PR
with `gh run download` before the cell was written, with the PR run
41233100816 and the `main` run after #25 merged, 41250971500, beside it.

## Rulings in this PR

1. **Product (Measured and state).** Row 5's "Measured" cell cites the
   `main` run after #24 merged, 41234548875 on `4d92676`, artifact
   `m04-gate-4d926760c985e973bdd5d35f1c76f0db47660808`: RED,
   `answers_unrun` `["g-001"]`, `answers_disagreed` `[]`,
   `answers_differing` `[]`, `agent_disagreed` `[]`, `baseline_changed`
   false, `unreadable` `[]`, `written_by_ci` true. The PR run on #24 at
   merge ref `a724249`, 41233100816, is named beside it as the run read
   at the time; it read the same on every field the row names (M01
   Unsure 23). The `main` run after #25 merged, 41250971500, read the
   same again. All three were downloaded in this session before the
   cell was written. The cell equals the expected gate output written
   at open, so row 5 is GREEN and "PRs used / cap" is 4 / 4. The lift's
   run is recorded in the README and not in the cell.
2. **Product (the lift, as ruled).** `rulings/pr2.md` 13 and
   `rulings/pr3.md` 14 carried the lift to PR 4 by M03's path (b). This
   PR carries it: `pages/api/baseline.json` and
   `pages/side-by-side.html` in the first commit of this PR, the one
   change "The false state" named, written by `lift.py write` from the
   artifact of CI run 41250971500. `run` holds the seven fields, the
   answer is the run's observation, `scripted` is false, the `PLANT`
   key and the illustration banner are gone; the agent column is
   unchanged. `git diff a896442 -- pages/` touches the two files and
   nothing else.
3. **Engineering, Security (Unsure 26, 30, the lift path).** No lift
   workflow: the `m04` workflow's own artifact holds `observations.json`
   and `result.json` from one job, and `src/m04/lift.py write` rebuilds
   the pages from both, by hand, deterministically, LF pinned. The run
   record's values are the artifact's: `commit`, `started_at` and
   `method` from `observations.json`; `run_url`, `artifact` (from
   `ci.sha`), `written_by_ci` and `baseline_commit` from the gate's
   `result.json`. Nothing is typed by hand and nothing is read from this
   machine but `data/` and `goldens/` at the checkout. `write` refuses
   an artifact whose `result.json` says CI did not write it, whose two
   files name different commits, whose observations were written from a
   dirty tree, or that holds no observation of a served id (P4). The
   lift reads no secret, no variable and no network; every workflow
   keeps `permissions: contents: read`, and `m04.yml` is unchanged. A
   second write of the same artifact was byte-identical to the
   committed pages; `git ls-files --eol` reads `i/lf w/lf` on each.
4. **Engineering, Data Owner (Unsure 28).** As built: the served ids are
   the ones `pages/api/baseline.json` already serves, each `question` is
   its golden's, and `row` and `clause` are copied from `data/` at its
   last commit (`595dd68`) when the table holds the `table_row` and the
   clauses hold the `clause_id`, as M03's writer copied them. The gate
   compares the served question with the golden's, so the golden is the
   question's source; the baseline ran over `goldens/`, so the
   observation is the golden's answer. No golden, no row and no clause
   changes (P6, P7).
5. **Product (Unsure 27).** The cell and the record name different runs
   for different reasons. The cell is the measurement on the plant, the
   `main` run after PR 2 merged (M01 Unsure 23). The record is the run
   the page carries, the latest `main` run with the gate as repaired at
   PR 3, so the record and the gate that reads it are the same code.
   The three runs wrote the same observation of g-001; the baseline is
   deterministic (`rulings/pr3.md` 9).
6. **Product (Unsure 31).** The page's additions beyond the one change
   are within it: a header paragraph naming the run and the artifact
   the page was rebuilt from, a table of what the three answer fields
   mean (the detail page's words, `milestones/M00/fields.md`), and the
   footer naming the run record beside the call record. Each says where
   an answer came from or what a field means; none is an answer, a
   measured number or a banner, and none changes what the gate reads.
7. **Product (PR 1's Unsure 1).** "Live" at M04 is (a): a CI run of the
   frozen baseline, in this repository, whose observation the page
   serves with its run record, the shape M03 used for the agent. That is
   what row 5 measured and what the lift serves. (b), a run at page view,
   needs a host that runs code at request time, which GitHub Pages is
   not, or a copy of the control outside `src/baseline/`, which P5 does
   not allow. Not designed here.
8. **Product, Security (PR 1's Unsure 2, M03's 2).** GitHub Pages is
   not enabled on this repository (404 again on 2026-10-31). At M04
   "public" means readable in the repository, as at M03. Enabling Pages,
   from which branch and directory, is the owner's setting, not a PR of
   this cap; carried by name to M05 with the constraint PR 1 stated
   (deploy-from-branch serves the root or `/docs` only).
9. **Product, Threshold Owner (PR 1's Unsure 6).** No third column at
   M04. The row's claim is the baseline; this repository holds no model
   credential; a labelled live model panel would be scripted or would
   need a new secret, and either is another milestone's claim. Option C
   of M00 `rulings/pr2.md` 2 stays open for a later row.
10. **Engineering (PR 1's Unsure 9).** The page writer is M04's own
    module, `src/m04/lift.py`, decided by the lift. It imports
    `src.m04.gate` for the run record's field names, the answer fields
    and `git`, and nothing from `src/m03/`, which is not edited.
11. **Engineering, Threshold Owner (PR 2's Unsure 13).** The lift does
    not add a `baseline_commit` check to the verdict: the gate is PR 2's
    and PR 3's and is not changed here. The record's `baseline_commit`
    is the artifact's, `df860b7f67d44947bf1c6c53b4c38f0322c32ce5`, the
    value the gate recorded under `baseline.baseline_commit` in all
    three runs, and the last commit touching `src/baseline/` on `main`.
    A reader checks the two against each other.
12. **Security, Product (PR 2's Unsure 16).** `M04 gate` is not made a
    required check in this PR, as `M02 gate` and `M03 gate` were not. It
    is the owner's setting, outside any milestone; carried by name with
    M02's and M03's 16. `M00 gate` stays the one required check.
13. **Threshold Owner, Engineering (PR 3's Unsure 19).** Recorded, not
    judged: the freeze check trusts the tag `m00` in the checkout and
    records its commit; three CI runs read `e94b76b`. A reader checks
    the seven characters against the ledger. The gate is not changed.
14. **Engineering (PR 3's Unsure 20).** As built: the gate records the
    observations file's `commit` and the checkout's and judges neither
    against the other; they were equal in all three runs. The lift's
    writer refuses an artifact whose `observations.json` and
    `result.json` name different commits, a check at the lift and not
    in the gate.
15. **Engineering (PR 3's Unsure 21).** As built: `run_record_check`
    reads null and the empty string as missing. The lift wrote six
    strings and the boolean `true`.
16. **Engineering, Data Owner (PR 3's Unsure 22).** Not changed: a
    golden with no `question` string stops the baseline before any
    observation is written, and the gate compares only with an
    observation. The lift's writer refuses such a golden too.
17. **Product, Engineering (PR 3's Unsure 23).** Confirmed as built at
    PR 3: a baseline file that cannot be read leaves the agent column
    judged, so a page agent answer the API does not serve reads RED
    beside the unreadable file. RED comes first; UNSCORABLE is for when
    nothing is RED (`rulings/pr2.md` 6).
18. **Product (PR 3's Unsure 24, Unsure 25).** PR 3 was #25; this PR is
    #26.
19. **Product (Unsure 29).** After this PR merges, its run on `main` is
    read with `gh run download` before the tag is placed. Its verdict is
    written in the tag `m04`'s message and in a comment on #26, not in
    the README: a commit after the merge would be a fifth PR, and a push
    to `main` is not the PR shape. The cell stands whatever it reads.
20. **Threshold Owner.** Not one line of `src/baseline/` changes in this
    PR (P5); `git diff m00 --stat -- src/baseline/` is empty on this
    branch. No construction probe touched the control's working tree
    (`rulings/pr3.md` 12). The observations file the local gate read was
    written by `uv run python -m src.baseline.run` with no argument
    added.
21. **Product.** The construction readings of 2026-10-31 (the writer
    twice, the gate on the rebuilt pages, the M00 scorer, the M02 gate)
    are recorded in the README as construction. They decide nothing
    (P4); the CI run on this PR is the reading, and it is a reading
    after the measurement.
22. **Product, on reading run 41252104790.** The gate on this PR read
    GREEN on the merge ref `5ac7e90`: every list `[]`,
    `baseline_changed` false, `unreadable` `[]`, `served_read` true,
    `written_by_ci` true, `comparison` "all equal" on g-001; the first
    pass of this gate. The `M03 gate` on the same head read GREEN with
    `parsed` null against the served null. Both are readings after the
    measurement: neither touches the cell, and the milestone is not
    reopened by what a later run reads.

## What a reader can falsify

Listed in `milestones/M04/README.md`, "Close (PR 4)", "What a reader
can falsify": rebuild the pages from the artifact of run 41250971500
and compare; open the `main` run's artifact
`m04-gate-4d926760c985e973bdd5d35f1c76f0db47660808` and read the cell
from it; grep the pages for a `PLANT` key, a scripted banner or a banned
word; `git diff main --stat` on this PR touches six files.

## What this ruling does not settle

Nothing of M04 is left open: every Unsure item of PR 1 to PR 4 is ruled
above or carried by name (Unsure 2 to M05; 16 to the owner's settings
with M02's and M03's 16; M03's 6 and 23 stay label-impact's). The tag
`m04` is placed after this PR's run on `main` is read (ruling 19).
Nothing in M05 or later.
