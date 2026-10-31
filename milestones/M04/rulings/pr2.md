---
ruling: m04-pr2
seat:
  - Engineering
  - Threshold Owner
  - Product
  - Tool Owner
  - Data Owner
  - Security
authorises:
  # Engineering: the gate and the workflow that runs it
  - src/m04/**
  - .github/workflows/m04.yml
  # Threshold Owner: the freeze check against tag m00 and the construction probe of it
  - src/m04/gate.py
  # Security: the workflow reads no secret, no variable and no network beyond the checkout
  - .github/workflows/m04.yml
  # Product: the ledger's PR count and the milestone's PR 2 detail
  - milestones/README.md
  - milestones/M04/README.md
  - milestones/M04/rulings/pr2.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/README.md
  - milestones/M00/rulings/pr2.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr2.md
  - milestones/M03/rulings/pr4.md
  - milestones/M04/README.md
  - milestones/M04/rulings/pr1.md
  - src/baseline/answer.py
  - src/baseline/run.py
  - src/m03/gate.py
  - .github/workflows/gate.yml
  - .github/workflows/m03.yml
  - https://github.com/andaro74/pharmadelta/actions/runs/38058191295
pr: https://github.com/andaro74/pharmadelta/pull/24
---

# Ruling: M04 PR 2 (measure)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR measures. It adds the gate that reads the plant `a896442` and
judges it: `src/m04/gate.py` reads the answers `pages/api/baseline.json`
serves and the two columns `pages/side-by-side.html` shows, names each
served ordinary-assistant answer that carries no run record written by
CI, each page baseline answer the file does not serve and each page
agent answer the public API does not serve, checks `src/baseline/`
against tag `m00`, compares each served answer that carries a run record
with the observation a run of the frozen baseline wrote in the same job,
and writes `result.json` with one verdict; `.github/workflows/m04.yml`
runs the baseline with `gate.yml`'s command and the gate in CI and
writes both as the artifact `m04-gate-<sha>`. On `a896442`'s pages the
gate names `g-001`: its `run` is null. The CI run on this PR is the
measurement (P4); the ledger's "Measured" cell is filled at close from
the `main` run after this PR merges (M01 Unsure 23, ruled at M02 PR 1).
Nothing in this PR lifts the plant, nothing under `pages/` changes, and
not one line of `src/baseline/` changes (P5).

## Rulings in this PR

1. **Engineering; Unsure 5 as ruled.** The run record's fields are
   fixed: `run_url`, `artifact`, `commit`, `baseline_commit`,
   `started_at`, `method`, `written_by_ci`. The gate names an answer
   unrun when any is missing or empty or when `written_by_ci` is not
   true. The lift writes them. From here `run_url` is readable through
   GitHub's API and `artifact` for 90 days; `baseline_commit` is
   recorded against the checkout's last baseline commit and not judged
   (Unsure 13).
2. **Threshold Owner, Engineering; Unsure 7 as ruled.** The gate checks
   the freeze: `git diff m00 --quiet -- src/baseline/` in the checkout,
   `baseline_changed` true on exit 1 and false on exit 0, the tag's
   commit and the last commit touching `src/baseline/` recorded beside
   it. The workflow checks out with `fetch-depth: 0` so the tag
   resolves. A missing tag reads null and UNSCORABLE unless something
   is RED (Unsure 14). "Runs the baseline" means the control, and the
   control is what `m00` holds.
3. **Product, Tool Owner; Unsure 3 as ruled.** `pages/api/baseline.json`
   is a separate served file, named in row 5, in the shape of
   `pages/api/answers.json` with `run` where that file has `agent` and
   `call`. It is not part of row 4's public API, which serves the
   agent's answers only; the M03 gate does not read it and row 4 is not
   touched.
4. **Product, Engineering; Unsure 4 as ruled.** F3.1's "the page" is
   the detail page. The M03 gate reads `pages/detail.html` and
   `pages/api/answers.json` by path and does not reach the side-by-side
   page. M04's gate carries `agent_disagreed`: each agent answer the
   side-by-side page shows that is not the API's entry of that `id`,
   canonical JSON. `m03.yml` and `src/m03/gate.py` are not edited.
5. **Product; Unsure 8 as ruled.** PR 1 was #23.
6. **Engineering, Product.** The verdict's shape is as PR 1's "Carried
   to PR 2" proposed: RED on any unrun, disagreed, differing or
   agent-disagreed answer or a changed baseline, the first, second and
   fourth read from the served files before the observations file;
   GREEN only when every served answer carries a run record written by
   CI, is shown as served and equals the run's observation, every agent
   answer shown is the API's, and `src/baseline/` equals `m00`;
   UNSCORABLE when nothing is RED and a served file, the tag or the
   observations file could not be read, or a served answer with a
   record was not compared. Exit 0, 1, 2. A file that serves no answer
   is UNSCORABLE (M03 Unsure 14's reading).
7. **Product, Data Owner, Threshold Owner.** Equality is against the
   gate's own run of the baseline in the same job, on `question` (the
   golden's), `table_row`, `clause_id` and the three `answer_fields`
   (Unsure 15). The baseline has no model and no randomness. An `id`
   with no golden or no observation reads differing (Unsure 12).
8. **Security.** The workflow reads no secret, no variable and nothing
   over the network beyond `actions/checkout` and `uv sync`. No `env`
   on any step. `result.json` records the CI environment's run URL,
   ids and ref, as the other gates do, and nothing else of the
   environment.
9. **Threshold Owner.** Not one line of `src/baseline/` changes in this
   PR (P5); `git diff m00 --stat -- src/baseline/` is empty on this
   branch. The workflow's baseline step is `gate.yml`'s command with
   the output path changed and adds no argument. The construction probe
   of the freeze arm touched the working tree once and reverted it in
   the same command, never staged or committed (Unsure 18); no further
   probe touches it.
10. **Product.** The construction run of 2026-10-31 is recorded in the
    README as construction: the baseline run, the gate on the real
    pages, the M00 scorer and the M02 gate, twenty made-up pairs of
    files and the freeze probe. No defect was found. It decides nothing
    (P4).
11. **Product.** "PRs used / cap" is 2 / 4. Unsure 1, 2, 6 and 9 are
    carried by name, not ruled: the gate is built under reading (a) of
    "live"; GitHub Pages is still not enabled and "public" means
    readable in the repository through PR 4; no third column at M04;
    the page writer is M04's own module, decided at the lift PR. Which
    PR carries the lift is ruled on reading this PR's CI run, as M03's
    was.
12. **Product.** This PR is #24, the next number on this repository
    (Unsure 10).

## What a reader can falsify

Listed in `milestones/M04/README.md`, "What a reader can falsify" under
PR 2.

## What this ruling does not settle

The items under Unsure (PR 2) in `milestones/M04/README.md`, 10 to 18,
each with its seat (10 ruled above), and PR 1's 1, 2, 6 and 9, carried.
What matters most for the close: what "live" means (1), where the pages
are served (2), whether the lift judges `baseline_commit` (13), and how
the lift's run record gets from a CI run into a commit ("After this PR
goes RED").
