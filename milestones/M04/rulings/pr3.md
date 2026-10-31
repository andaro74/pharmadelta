---
ruling: m04-pr3
seat:
  - Engineering
  - Threshold Owner
  - Security
  - Product
authorises:
  # Engineering: the repair of the gate's verdict path (Defects 1 to 3) and the two job-summary labels
  - src/m04/gate.py
  # Threshold Owner: the freeze check's unread path; no probe touched src/baseline/'s working tree
  - src/m04/gate.py
  # Security: the repair reads nothing new from the environment and writes nothing new of it; m04.yml is unchanged
  - src/m04/gate.py
  # Product: the ledger's PR count, the milestone's PR 3 detail and this file
  - milestones/README.md
  - milestones/M04/README.md
  - milestones/M04/rulings/pr3.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M04/README.md
  - milestones/M04/rulings/pr1.md
  - milestones/M04/rulings/pr2.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr3.md
  - milestones/M03/rulings/pr4.md
  - src/baseline/run.py
  - .github/workflows/m04.yml
  - .github/workflows/gate.yml
  - https://github.com/andaro74/pharmadelta/actions/runs/41233100816
  - https://github.com/andaro74/pharmadelta/actions/runs/41234548875
pr: https://github.com/andaro74/pharmadelta/pull/25
---

# Ruling: M04 PR 3 (repair)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR repairs. The cold review of #24 (`milestones/M04/README.md`,
"Cold review of #24") found three defects in the gate's verdict path,
each a failure after the served files were read that turned a RED into
UNSCORABLE where `rulings/pr2.md` 6 says RED comes first: a baseline
file that could not be read stopped the run before the agent column was
judged; git that could not be run raised out of the freeze check; a
summary that could not be appended overwrote a written RED. It found two
wrong labels in the job summary. `src/m04/gate.py` now records each of
the three as unread and judges the rest, and the labels say what
happened. Nothing under `pages/` changes; the plant stands and nothing
here lifts it. Nothing here decides the row: the `main` run after #24
merged, 41234548875, is the measurement, read first in this session, and
PR 4 fills the "Measured" cell from it.

## Rulings in this PR

1. **Engineering (Defects 1 to 3, the labels).** The repair is as the
   README's "The repair" states: `run` catches `Unscorable` from the
   baseline file and judges the agent column; `baseline_state` catches
   `OSError` and returns the freeze check unread; `write_result` appends
   the summary inside a `try`; `--summary ""` means none; "not resolved"
   and "page not read" in the summary. `result.json` gains `served_read`.
   The verdict on every input PR 2's construction run exercised is
   unchanged; the five made-up cases that read UNSCORABLE before read
   RED after, naming what the served files hold. The fields compared and
   the run record's fields are unchanged. No new dependency;
   `pyproject.toml` and `uv.lock` are unchanged.
2. **Threshold Owner.** Not one line of `src/baseline/` changes (P5);
   `git diff m00 --stat -- src/baseline/` is empty on this branch. No
   construction probe touched its working tree (PR 2 Unsure 18, ruled
   below): the git-absent probe removed git from `PATH`, and the
   missing-tag probe ran in a clone made with `--no-tags`. The freeze
   check that cannot be made reads `baseline_changed` null, never true
   and never false.
3. **Security.** The repair reads nothing new from the environment and
   writes nothing new of it: `served_read` is a boolean about the served
   file, `baseline.error` is git's stderr or the OS error's name and
   text, and the stderr line on a summary that could not be appended
   names the path given. `.github/workflows/m04.yml` is unchanged: no
   `secrets.`, no `vars.`, no `env:`.
4. **Product.** The `main` run after #24 merged, 41234548875 on
   `4d92676`, read RED, `answers_unrun` `["g-001"]`, `answers_disagreed`
   `[]`, `answers_differing` `[]`, `agent_disagreed` `[]`,
   `baseline_changed` false, `unreadable` `[]`, `written_by_ci` true,
   event push on `refs/heads/main`, the same as the PR run 41233100816
   on every field the row names. It is the run the Measured cell cites
   at PR 4, with the PR run named beside it (M01 Unsure 23).
5. **Product, Engineering (PR 2 Unsure 11, ruled).** The gate names a
   page baseline answer the file does not serve or that differs from the
   file's entry, and does not name a served answer the page does not
   show, as M03's gate did not (M03 Unsure 25, ruled at M03 PR 4). The
   row's words "is shown as served" mean the gate's reading. With one
   served answer, shown, the readings agree; the gate is not changed.
6. **Product, Engineering (PR 2 Unsure 12, ruled).** A served answer
   with a run record whose `id` has no golden or no observation in the
   run reads `answers_differing`, not UNSCORABLE: the baseline runs
   over `goldens/`, so nothing it wrote could have produced that
   answer. Built so and read so at construction (case 13).
7. **Engineering, Threshold Owner (PR 2 Unsure 13, carried).**
   `baseline_commit` in the run record is recorded against the
   checkout's last baseline commit and not judged, at PR 2 and here.
   Whether the lift adds it to the verdict is PR 4's to propose with the
   lift, and is not a repair.
8. **Threshold Owner, Engineering (PR 2 Unsure 14, ruled).** When the
   tag `m00` is not in the checkout, or git cannot be run, the freeze
   check reads null and the run is UNSCORABLE unless something is RED:
   "a reading could not be made", never a verdict on the control. Read
   at PR 2 in CI with the tag present (`e94b76b`), at PR 3 at
   construction with the tag absent (the clone) and with git absent
   (case 25): RED first on the plant, UNSCORABLE on the lifted entry.
9. **Product, Data Owner, Threshold Owner (PR 2 Unsure 15, ruled).**
   Equality is against the gate's own run of the baseline in the same
   job. The baseline has no model and no randomness; the PR run and the
   main run wrote the same six observations at the same `data/` and
   `goldens/`, g-001's equal in value to the plant's hand-written
   answer. A change to `data/` or `goldens/` between a lift's run and a
   later gate run reads `answers_differing` and names the id.
10. **Security, Product (PR 2 Unsure 16, carried).** Whether `M04 gate`
    is made a required check on `main` is the owner's settings, outside
    any milestone, as M02's 16 and M03's 16 were carried. Not changed
    here.
11. **Engineering (PR 2 Unsure 17, ruled).** The artifact
    `m04-gate-<sha>` keeps `observations.json` beside `result.json`: the
    gate's artifact holds what the gate compared. A second copy of what
    `m00-gate-<sha>` holds on the same head, 90 days each.
12. **Threshold Owner (PR 2 Unsure 18, ruled).** The construction probe
    of the freeze arm at PR 2 touched `src/baseline/answer.py` in the
    working tree once and reverted it in the same command, never staged
    or committed. Allowed once, recorded. No later probe touches the
    control's working tree; PR 3's probes did not, and PR 4's will not.
13. **Product (PR 1 Unsure 1, 2, 6, 9, carried).** Carried by name, not
    ruled: the gate is built under reading (a) of "live"; GitHub Pages
    is still not enabled and "public" means readable in the repository
    through PR 4; no third column at M04; the page writer is M04's own
    module in `src/m04/`, built at the lift. Product rules 1, 2 and 6
    at PR 4; 9 is decided by the lift.
14. **Product.** "PRs used / cap" is 3 / 4 in the ledger and the
    milestone README. PR 4 is the close: the lift by M03's path (b), the
    Measured cell from run 41234548875, the row's state, the rulings on
    the open Unsure items, the tag `m04` after its run on `main` is
    read. A fifth PR is a RED close.
15. **Product (Unsure 24).** This PR is #25.

## What this ruling does not settle

Unsure 19 to 23 (`milestones/M04/README.md`, "Unsure (PR 3)"), each
with its seat; PR 2's 13 and 16, carried; PR 1's 1, 2, 6 and 9, carried.
What matters most for the close: what "live" means (1), where the pages
are served (2), whether the lift judges `baseline_commit` (13), and
Defect 1's reading of an unreadable served file beside a judged agent
column (23).
