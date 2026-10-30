---
ruling: m03-pr2
seat:
  - Engineering
  - Security
  - Product
  - Data Owner
  - Threshold Owner
  - Tool Owner
authorises:
  # Engineering: the gate and the workflow that runs it
  - src/m03/**
  - .github/workflows/m03.yml
  # Security: what the workflow reads (Cognito's InitiateAuth and the door, with the caller's password from a secret), what it holds and what it never writes
  - .github/workflows/m03.yml
  - src/m03/gate.py
  # Product: the ledger's PR count and the milestone's PR 2 detail
  - milestones/README.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr2.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/fields.md
  - milestones/M02/README.md
  - milestones/M02/rulings/pr2.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr1.md
  - https://github.com/andaro74/agentkeel/blob/m10/SPEC/10-public-caller.md
  - https://github.com/andaro74/agentkeel/blob/m10/docs/developer/quickstart.md
  - https://github.com/andaro74/agentkeel/blob/m10/src/agent/run.py
  - https://github.com/andaro74/agentkeel/blob/m10/infra/construct/door.py
  - https://github.com/agentkeel-studio/label-impact/blob/8cf0563/agent.py
  - https://github.com/agentkeel-studio/label-impact/blob/8cf0563/server.py
pr: https://github.com/andaro74/pharmadelta/pull/20
---

# Ruling: M03 PR 2 (measure)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR measures. It adds the gate that reads the plant `c7edf8f` and
judges it: `src/m03/gate.py` reads the answers `pages/api/answers.json`
serves and the answer `pages/detail.html` shows, names each served
answer that carries no call record as `pharmadelta` and each page answer
the API does not serve, signs in to label-impact's identity pool as
`pharmadelta` with the repository secret, asks the deployed agent each
served answer's question through its door, compares each called answer
with the door's `parsed`, and writes `result.json` with one verdict;
`.github/workflows/m03.yml` runs it in CI and writes the result as the
artifact `m03-gate-<sha>`. On `c7edf8f`'s pages the gate names `g-001`:
its `call` is null. The CI run on this PR is the measurement (P4); the
ledger's "Measured" cell is filled at close from the `main` run after
this PR merges (M01 Unsure 23, ruled at M02 PR 1). Nothing in this PR
lifts the plant, and nothing under `pages/` changes.

## Rulings in this PR

1. **Engineering.** The gate is standard library only; `pyproject.toml`
   and `uv.lock` are unchanged. The sign-in and the call are the
   platform's surfaces, used as agentkeel's `invoke_through_door` and
   its door's authoriser define them (SPEC/10 §2, R2): `InitiateAuth`
   with `USER_PASSWORD_AUTH` on the callers client, the access token as
   bearer, `POST {"question"}` on the door's URL. Nothing is redesigned.
   The door's URL must be https on a host under
   `.execute-api.us-west-2.amazonaws.com` with a path ending
   `/invocations`, or the gate refuses it before any request.
2. **Security; Unsure 3 as ruled.** The workflow reads Cognito's
   endpoint in `us-west-2` and the door's URL, with the caller's
   password from the secret `M03_DOOR_PASSWORD` and the door's URL, pool
   id and callers client id from the variables `M03_DOOR_URL`,
   `M03_DOOR_POOL_ID` and `M03_DOOR_CALLERS_CLIENT_ID`, the names PR 1
   proposed and the owner set. The gate reads them from its environment
   and writes none of them: `result.json` holds four booleans for their
   presence, the pool id's region prefix, and two claims of the token
   (Unsure 18). No AWS credential, no SigV4, no runtime ARN, no door
   client secret. A pull request from a fork gets no secret (Unsure 19).
3. **Engineering, Product; Unsure 4 as ruled.** The verdict's shape is
   as PR 1 proposed: RED on any uncalled, disagreed or differing served
   answer, the first two read from the served files before any sign-in;
   GREEN only when every served answer carries a call record, every page
   answer is an API entry and every compared answer equals the door's;
   UNSCORABLE when nothing is RED and a served file, the environment,
   the sign-in or the door could not be read. Exit 0, 1, 2. An API that
   serves no answer is UNSCORABLE (Unsure 14).
4. **Product, Data Owner, Threshold Owner; Unsure 5 as ruled.** Equality
   is against the run's own call: `table_row`, `clause_id` and the three
   `answer_fields` of the door's `parsed`, flat or under `answer_fields`,
   against the served `answer`. A served answer of null equals a `parsed`
   of null. The call that produced a served answer is matched only by
   its `request_id` in the security account, which this repository
   cannot read.
5. **Product; Unsure 8 as ruled.** PR 1 was #19.
6. **Threshold Owner, Security; Unsure 9 as ruled.** The gate runs on
   every pull request, every push to `main` and by hand, and asks the
   door every served answer's question, called or not, so the Measured
   cell carries what the agent said on the day (Unsure 11). One call per
   served answer per run, under the agent's own ceilings and
   `daily_usd`; the spend is the agent's.
7. **Engineering, Security; Unsure 10 as ruled.** The call record's
   fields are fixed: `subject`, `issuer`, `door_host`, `request_id`,
   `called_at`, `agent`, `agent_commit`, `run_url`. The gate names an
   answer uncalled when any is missing or empty or `subject` is not
   `pharmadelta`. `run_url` is readable from here; `request_id` is not;
   `door_host` is a variable's value and is Unsure 12.
8. **Product.** The construction run of 2026-10-30 is recorded in the
   README as construction: no sign-in was possible outside Actions, one
   no-token call read the door's headers (Unsure 20), seven made-up
   pairs of files exercised the arms, and one defect found by them was
   fixed before the first push. It decides nothing (P4).
9. **Product.** "PRs used / cap" is 2 / 4. Which PR carries the lift is
   ruled on reading this PR's CI run, as M02's was.
10. **Product, on reading run 41126878288.** The run wrote RED,
    `answers_uncalled` `["g-001"]`, `answers_disagreed` `[]`,
    `answers_differing` `[]`, `written_by_ci` true, on the merge ref
    `f97f292`; the plant is named as the row expects. The sign-in
    succeeded and the door answered 200 with request id
    `GE2QwjpovHcESyQ=` in `apigw-requestid` (Unsure 13, confirmed),
    `stop_reason` `tool_use`, `parsed` null: the agent's tool refused
    `section` `8.1` sent as a number, three times (Unsure 23, carried to
    label-impact). The lift is carried by PR 4. PR 3, if the cold review
    of #20 finds anything, repairs and does not lift; if it finds
    nothing, PR 3 is skipped. The Measured cell takes the `main` run
    after #20 merges.

## What a reader can falsify

Listed in `milestones/M03/README.md`, "What a reader can falsify" under
PR 2.

## What this ruling does not settle

The items under Unsure (PR 2) in `milestones/M03/README.md`, 11 to 23,
each with its seat (13 ruled above), and PR 1's 1, 2, 6 and 7, still open. What matters
most for the close: what the public API is (1), where it is served (2),
the deployed agent's answer record (6) and its cause (23), and how the
lift's call record gets from a CI run into a commit ("After this PR goes
RED").
