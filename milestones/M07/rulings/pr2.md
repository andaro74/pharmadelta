---
ruling: m07-pr2
seat:
  - Engineering
  - Security
  - Product
  - Tool Owner
authorises:
  # Engineering: the gate and the workflow that runs it
  - src/m07/**
  - .github/workflows/m07.yml
  # Security: what the workflow reads and with what token, what it never writes, and the grep before upload
  - .github/workflows/m07.yml
  - src/m07/gate.py
  # Tool Owner: the clock record's fields, fixed here
  - src/m07/gate.py
  # Product: the ledger's PR count and the milestone's PR 2 detail
  - milestones/README.md
  - milestones/M07/README.md
  - milestones/M07/rulings/pr2.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M07/README.md
  - milestones/M07/rulings/pr1.md
  - milestones/M06/rulings/pr2.md
  - src/m06/gate.py
  - src/m01/reader.py
  - .github/workflows/m06.yml
  - pages/api/second-agent.json
  - https://api.github.com/repos/agentkeel-studio/label-impact
  - https://api.github.com/repos/andaro74/agentkeel/actions/jobs/114389865133
  - https://api.github.com/repos/andaro74/agentkeel/actions/runs/38112132210
pr: https://github.com/andaro74/pharmadelta/pull/48
---

# Ruling: M07 PR 2 (measure)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR measures. It adds the gate that reads the plant `c07fbe5` and
judges it: `src/m07/gate.py` reads the times
`pages/api/second-agent.json` serves and the times `index.html` and the
pages under `pages/` show, names each served time that carries no clock
record and each page time the file does not serve; then, for each time
with a clock record, reads back from GitHub's API the repository, its
first pull request and the deploy job the record names, and writes
`result.json` with one verdict. `.github/workflows/m07.yml` runs it in
CI with the workflow's own token, greps the result for a token's
prefix, and writes the artifact `m07-gate-<sha>`. On the plant the gate
names `a-002`: `clock` is null, and nothing is read from the network.
The CI run on this PR is the measurement (P4); the ledger's "Measured"
cell is filled at close from the `main` run after this PR merges (M01
Unsure 23, ruled at M02 PR 1). Nothing in this PR lifts the plant,
nothing under `pages/` changes, and no repository is created.

## Rulings in this PR

1. **Product; PR 1's Unsure 1, 2, 3, 5, 6, 7: not ruled.** The owner's
   start prompt for this PR listed the six and left each blank, with
   the instruction to use the session's proposal and record the item
   as still open. Done: each stands at its PR 1 proposal and is open
   (README, "The owner's rulings on PR 1's Unsure, as given"; Unsure
   28). This PR builds on 5 and 6 only.
2. **Engineering.** The gate is the standard library alone;
   `pyproject.toml` and `uv.lock` are unchanged. Nothing is imported
   from the earlier gates. The checkout is the default depth: the gate
   asks git for its own head and nothing else.
3. **Security; Unsure 5 as proposed, open.** The workflow reads
   GitHub's API with `GITHUB_TOKEN` in the gate step's `env`;
   `permissions` is `contents: read`. No secret and no variable. Public
   records only: the agent's repository, its pull requests, and
   agentkeel's job and run. No seat is read and the registry is not
   read. The gate follows no redirect. `result.json` holds one boolean
   for the token's presence; a step greps the result for `ghs_`, `ghp_`
   and `github_pat_` before upload and fails on a match.
4. **Tool Owner, Engineering.** The names are fixed: the served key
   `agents`, the entry fields `elapsed_seconds` and `clock`, the lists
   `times_unrecorded`, `times_disagreed` and `times_differing` with
   `unreadable` and `written_by_ci` beside them, the page block
   `second-agent-<id>`. The clock record is `repository`,
   `repository_id`, `template`, `created_at`, `pull_request`,
   `merge_commit`, `deploy_run`, `deploy_job`, `completed_at`,
   `conclusion`, `read_by` (`run_url`, `artifact`), as PR 1 proposed.
   The lift writes them.
5. **Engineering; Unsure 10 as built.** The deploy job is read by the
   job id the record names, not from a window of runs. A job id is one
   attempt's, so the record names one attempt's `completed_at`. Not
   exercised (Unsure 21).
6. **Engineering, Product; found here.** GitHub cuts a matrix job's
   name at 97 characters. The second agent's deploy job will carry
   about 36 of its merge commit's 40 digits, and no bare agent name.
   The gate reads the repository, its id and the commit by position and
   accepts a cut prefix of at least 20 digits. "Names the agent" in
   F7.1 is read as the repository's full name and id (Unsure 20).
7. **Product, Engineering; Unsure 6 as proposed, open.** A page shows a
   time by a `second-agent-<id>` block. The gate reads `index.html` and
   every `pages/*.html`, so the line may go on any of them. A page with
   no block shows no time: on the plant every page reads so, and
   `times_disagreed` is `[]`.
8. **Engineering, Product.** The verdict's shape is as the row says: RED
   on any unrecorded, disagreed or differing time, the first two read
   before any network; GREEN only when every served time carries a
   clock record equal to GitHub's records, the job concluded `success`,
   every page block is the file's entry and nothing was unread;
   UNSCORABLE when nothing is RED and a reading could not be made. Exit
   0, 1, 2. A read-back that fails beside a RED leaves the RED standing.
   A repository that answers 404 is a difference, not an unread
   (Unsure 19).
9. **Product.** The construction run of 2026-11-15 UTC is recorded in
   the README as construction: the gate on the real files with no
   token, eighty-four made-up cases with the API stubbed, and the
   gate's own transport on label-impact's real records. No defect was
   found. It decides nothing (P4). No time read there is written
   anywhere.
10. **Product.** "PRs used / cap" is 2 / 4. Which PR carries the lift is
    ruled on reading this PR's CI run.
11. **Product.** This PR is #48, the next number on this repository
    after #47 (Unsure 15).
12. **Security.** No host, account id, pool id, client id, ARN or token
    is written in any file of this PR. No repository was created and no
    step that starts the clock was taken; the session's only request
    about `agentkeel-studio/record-keep-desk` was a GET that answered
    404.

13. **Product, on reading run 43769375822.** The run wrote RED,
    `times_unrecorded` `["a-002"]`, `times_disagreed` `[]`,
    `times_differing` `[]`, `unreadable` `[]`, `written_by_ci` true, on
    the merge ref `c708fc2`; the plant is named as the row expects.
    `api_reads` is `[]` and `read_back` is null: the gate asked
    GitHub's API nothing for the plant. The grep step passed and the
    artifact was written. The second run, 43769500271 on merge ref
    `bc9687d`, read the same. The owner ruled: "PR 4 carries the lift".
    It does so by M03's path (b): a lift workflow started by hand after
    the stopwatch run, its artifact's entry committed (README, "After
    this PR goes RED"). PR 3, if the cold review of #48 finds anything,
    repairs and does not lift; if it finds nothing, PR 3 is skipped.
    The Measured cell takes the `main` run after #48 merges.

## What a reader can falsify

Listed in `milestones/M07/README.md`, "What a reader can falsify" under
PR 2.

## What this ruling does not settle

The items under Unsure (PR 2) in `milestones/M07/README.md`, 15 to 28,
each with its seat, and PR 1's fourteen. What matters most before the
stopwatch run: PR 1's 2, 3 and 7; that the second repository is public
(19); and that the agent's files go in its first pull request (23).
