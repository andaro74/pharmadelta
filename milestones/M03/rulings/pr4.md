---
ruling: m03-pr4
seat:
  - Security
  - Engineering
  - Product
  - Tool Owner
  - Data Owner
  - Threshold Owner
authorises:
  # Security: door_host as a hash (Unsure 12); the lift workflow reads the same four names as the gate and writes none; contents: read on every workflow
  - .github/workflows/m03-lift.yml
  - src/m03/lift.py
  # Engineering: the lift path (Unsure 28): the CI call, the artifact, the deterministic rebuild of the pages
  - .github/workflows/m03-lift.yml
  - src/m03/lift.py
  # Product, Data Owner, Tool Owner: the lift, the two pages rebuilt from the CI record (Unsure 26)
  - pages/api/answers.json
  - pages/detail.html
  # Product: the Measured cell, the row's state, 4 / 4, the close detail, the Unsure rulings and this file
  - milestones/README.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr4.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/fields.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr1.md
  - milestones/M03/rulings/pr2.md
  - milestones/M03/rulings/pr3.md
  - milestones/M02/rulings/pr3.md
  - milestones/M01/rulings/pr4.md
  - https://github.com/andaro74/pharmadelta/actions/runs/41171470951
  - https://github.com/andaro74/pharmadelta/actions/runs/41126878288
  - https://github.com/andaro74/pharmadelta/actions/runs/41221327681
  - https://github.com/agentkeel-studio/label-impact/blob/8cf0563/manifest.yaml
pr: https://github.com/andaro74/pharmadelta/pull/22
---

# Ruling: M03 PR 4 (close)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR closes M03 at the cap, 4 / 4. It carries the lift, fills the
"Measured" cell from a CI-written result and writes the row's state,
rules or carries by name every open Unsure item of PR 1, PR 2 and PR 3,
and is followed by the tag `m03` on its merge commit after its run on
`main` is read. It decides nothing about the measurement: the `main` run
after #20 merged, 41171470951, is the measurement, read again at this PR
with `gh run download` before the cell was written.

## Rulings in this PR

1. **Security (Unsure 12, Unsure 27).** `door_host` in the call record
   is the SHA-256 of the door URL's host, lower-cased, written as
   `sha256:<64 hex>`, never the host. The gate as it stands names an
   answer uncalled when `door_host` is missing or empty (`rulings/pr2.md`
   7), so a hash fits it and "not written" would need a gate change the
   repair slot did not make (Unsure 27). What the hash gives: a reader
   who holds the variable `M03_DOOR_URL` confirms the record names the
   same host; a reader who does not learns nothing of the host from the
   page. What it does not give: the host is a short API Gateway id under
   a known suffix, so a brute-force search of the hash is possible for
   anyone who wants the id enough; the door still admits only a token of
   an admitted caller (agentkeel SPEC/10), so the host is not a credential
   and the hash is a courtesy, not a control. The gate is not changed.
2. **Engineering, Security (Unsure 28, the lift path).** Of the two
   candidates (`milestones/M03/README.md`, "Close (PR 4)", "The lift
   path"), the one built is the artifact path: `.github/workflows/m03-lift.yml`
   runs `src/m03/lift.py call` in CI, which signs in and asks the door
   each served question with the gate's own `sign_in` and `ask_door` and
   writes `call.json` (the call record, the door's reading, the answer
   verbatim) as the artifact `m03-lift-<sha>`; `lift.py write` rebuilds
   `pages/api/answers.json` and `pages/detail.html` from that artifact,
   by hand, deterministically, and the pull request commits them naming
   the run. Chosen over a workflow that commits to the branch with
   `GITHUB_TOKEN` because it leaves `permissions: contents: read` on
   every workflow of this repository and adds no token that can write a
   branch; the cost is one hand step, which a reader checks by running
   `write` on the downloaded artifact and comparing. The call is CI's as
   `pharmadelta`; `write` refuses a `call.json` whose `written_by_ci` is
   false (P4). The workflow reads the same secret and three variables
   as the gate, from one step's `env`, and writes none of them. It runs
   by hand and once on a push that adds or edits its own file on a
   branch other than `main`, because a `workflow_dispatch` needs the
   file on the default branch and the lift's call is made before this PR
   merges. `m03.yml`, `gate.yml`, `m01.yml`, `m02.yml`, `pyproject.toml`
   and `uv.lock` are unchanged.
3. **Product, Tool Owner, Data Owner (Unsure 26, Unsure 6).** The lift
   serves what its call returned, verbatim: `answer` is `table_row`,
   `clause_id` and the three answer fields of the door's `parsed`, or
   null when nothing parsed. `row` and `clause` are copied from `data/`
   only when the table holds the answer's `table_row` and the clauses
   hold its `clause_id`; else they are null and the page shows "no row
   found" with the question, the call record, the `parsed` object and
   the agent's text, verbatim and labelled as the agent's, and shows no
   answer: an answer is shown only with its row and its clause (SPEC/00
   §11). Row 4 closes on the call, as Unsure 6 asked; what the agent
   gave is on the page and in the cell's own words. The cause is
   label-impact's (Unsure 23) and nothing here changes there.
