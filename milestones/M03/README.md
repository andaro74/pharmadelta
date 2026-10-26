# M03 — A public API and the detail page call the deployed agent

Opened 2026-10-25 at PR 1. Three days (SPEC/00 §8). Needs row P closed:
met at #17 (`6f42712`, `milestones/adoption/rulings/row-p-close.md`), row
P GREEN. Everything in this milestone is measured in this repository. The
agent it calls is `agentkeel-studio/label-impact` at `8cf0563`, deployed
on agentkeel `m10`, and is not changed by this milestone.

## Ledger row

Written at PR 1 open. The row in `milestones/README.md` is the ledger's;
this is the same row with the open detail.

| Field | Row 4 |
|---|---|
| Claim | A public API and the detail page call the deployed agent |
| Falsifiers | F3.1 an answer the public API serves, or the detail page shows, was not produced by a call to the deployed agent through its door as the caller `pharmadelta`: it carries no call record, or its `table_row`, `clause_id` or `answer_fields` differ from what the agent answered on that call; or the page shows an answer the API does not serve. |
| Seeded commit | `c7edf8f` on `m03-pr1`: `pages/api/answers.json`, the public API's served answers, one entry, the question of golden `g-001` with an answer written by hand, its row `lisinopril.8.1` and its clause `201.57(c)(9)(i)` copied from `data/` at `b9f84e3`, `agent` null, `call` null, `scripted` true, a `PLANT` key beside them; `pages/detail.html`, the detail page, showing that answer with its row and its clause, labelled scripted, the same object embedded. Nothing in the repository signs in to the door or calls the agent. |
| Expected gate output | PR 2's gate, in CI, reads every answer the API serves and the page shows and names each that carries no call record or that the page and the API do not agree on; then signs in to label-impact's identity pool as `pharmadelta` with the repository secret, asks the deployed agent each called answer's question through the door, and compares the served answer with the door's. It writes a `result.json` that is RED when any served answer is uncalled, disagreed or differing, naming each; GREEN only when every served answer carries a call record, is shown as served and equals the door's answer; UNSCORABLE when nothing is RED and the served files, the pool or the door could not be read. On `c7edf8f`: RED, `answers_uncalled` `["g-001"]`, `answers_disagreed` `[]`, `answers_differing` `[]`. The Measured cell cites the `main` run after PR 2 merges (M01 Unsure 23, ruled at M02 PR 1). |
| Measured | |
| PRs used / cap | 1 / 4 |
| State | OPEN |

## The false state (P1, P2)

The claim says the public API and the detail page call the deployed
agent. It is false when either serves an answer that no call to the
agent produced. That is what `c7edf8f` commits.

`pages/api/answers.json` is what the public API serves: a list of
answers, one per question. It holds one entry. The question is golden
`g-001`'s. The answer, `table_row` `lisinopril.8.1`, `clause_id`
`201.57(c)(9)(i)`, `impacted` true, `owed` `follow-rld`, `escalate`
false, was written by hand. The row and the clause beside it are
copies of `data/table.json` and `data/clauses.json` at `b9f84e3`.
`agent` is null and `call` is null: no door, no request id, no time, no
CI run. `scripted` is true and a `PLANT` key says what the entry is.

`pages/detail.html` is the detail page (LabelKeel, SPEC/00 §11's
placeholder name). It shows that answer with its row and its clause,
under a banner that says the answer is scripted and no call produced it
(P8), and embeds the same object in a `<script type="application/json"
id="answer">` block so a reader reads the page's answer without an HTML
parser. The page shows no measured number; the numbers on it are the
row's and the clause's own data (Unsure 7).

Why this plant: a page that shows a right answer with its row and its
clause, and did not ask the agent, is the thing the claim rules out. It
is also what every page of this demo is before this milestone: the
baseline is a keyword matcher and the agent has only been asked its own
goldens by the platform's deploy. A gate that checks the page shows a
row and a clause passes the plant; a gate that checks the answer came
from a call does not. The plant tests which one PR 2 builds.

Lifting the plant is one change to the entry: `agent` and `call` filled
with the record of the call that produced the answer, made by this
repository's CI as `pharmadelta`, the answer fields what that call
returned, `scripted` false, the `PLANT` key removed; and the page
rebuilt from it. Which PR carries the lift is decided after PR 2 goes
RED, not here.

## What the public API is at M03 (assumption, Unsure 1)

SPEC/00 §3 gives this repository "the public API and pages" and says
nothing more about the API. This milestone reads it as a read API: a
public JSON file of answers, each produced by a call this repository's
CI made to the deployed agent as `pharmadelta`, each carrying the record
of its call, served beside the pages. A live path, where a visitor's
question is forwarded to the agent on request, needs a host that runs
code and holds the caller's credential; this repository has no cloud
account and GitHub Pages runs no code. A public proxy would also let
anyone spend the agent's daily budget (`daily_usd` 10 in its manifest).
So the live path is not M03's, and is named under Unsure for Product
and Security. If Product rules a live path is the claim, the plant is
unchanged: it is still an answer no call produced.

## Open detail (PR 1, 2026-10-25)

### What this PR holds

- Row 4 of the ledger: falsifier, seeded commit, expected gate output,
  PRs used 1 / 4.
- `pages/api/answers.json` and `pages/detail.html`, the plant.
- This file.
- `rulings/pr1.md`.

Nothing else. No code that signs in or calls, no workflow, no test
(P2). No edit to `src/` (`src/baseline/` is frozen at `m00`, P5),
`goldens/`, `data/`, SPEC/00, CLAUDE.md, the README, `.gitignore` or
anything under `milestones/M00/`, `milestones/M01/`, `milestones/M02/`
or `milestones/adoption/`.

### The deployed agent, as read at open (construction, not evidence, P4)

Read 2026-10-25 from the clones at `~/code/label-impact` and
`~/code/agentkeel` and from agentkeel's Actions with `gh`. Each is a
read of the platform's own record while opening the row; PR 2's CI run
is this repository's measurement.

| What | Read |
|---|---|
| label-impact head | `8cf0563`, [pull request #5](https://github.com/agentkeel-studio/label-impact/pull/5) merged 2026-10-21 |
| manifest | `platform_version: m10`; guardrail `1088aw3ujhyd` version `"6"`; `callers: [{subject: pharmadelta, issuer: self}]`; `may_call: []`, `may_be_called_by: []`; every seat `andaro74`; `ceilings` concurrency 2, rps_per_edge 1; `daily_usd` 10 |
| data | `data/table.json` and `data/clauses.json` in label-impact equal this repository's at `b9f84e3`, compared as parsed JSON (M02 Unsure 6, carried items below) |
| deploy | agentkeel [run 39547397318](https://github.com/andaro74/agentkeel/actions/runs/39547397318), `deploy-agent` for `label-impact` at `8cf0563`, success, 2026-10-21. Its "The door the stack built" step read the stack's outputs `DoorUrl`, `DoorPoolId`, `DoorClientId`, `DoorTokenEndpoint` and `DoorScope`; the door is an API Gateway HTTP API in `us-west-2` whose URL ends `/invocations` (agentkeel SPEC/10 §2, R2's hybrid door) |
| the goldens through the door | the same run asked label-impact's four goldens through the door as `platform` and wrote `answer.json: RED`. The step's log reads `g-001 ordinary tool_use None`, `g-002 trap end_turn {table_row: None, clause_id: '21 CFR 201.57(c)(9)(i)', impacted: False, owed: 'none', escalate: False}`, `g-003 trap tool_use None`, `g-004 trap end_turn {table_row: None, clause_id: '314.80(c)(1)(i)', impacted: False, owed: 'alert-report', escalate: True}`. The first deploy, [run 38112132210](https://github.com/andaro74/agentkeel/actions/runs/38112132210) at `5e370ca` on 2026-10-11, straight at the runtime, read the same but `g-001 ordinary end_turn None`. CI-written by agentkeel, so evidence of what the agent answered; not this repository's measurement. Carried items below |
| the caller's credential | set by hand by the owner in the pool (agentkeel M10 README item 4's path, `admin-set-user-password`); lives nowhere in git; at M03 a repository secret, never a file |
| this repository's Pages | not enabled: `GET /repos/andaro74/pharmadelta/pages` answers 404 (Unsure 2) |

### What this PR does not hold

- No sign-in and no call. Grep `cognito`, `initiate`, `Bearer`,
  `execute-api` and `secrets.` under `src/`, `pages/` and `.github/`:
  no match.
- No credential, no door URL, no pool id, no client id. The page and
  the API name the agent by its repository and nothing of the door.
- No lift. The entry carries `call: null` until the PR that carries the
  lift, decided after PR 2 goes RED.
- No change to label-impact or to agentkeel. Platform items are flagged
  under "Row P" below and waited for.
- No workflow. `gate.yml`, `m01.yml` and `m02.yml` are unchanged. The
  `M01 gate` reads PENDING, exit 3, on every pull request and is not
  required (M01 Unsure 14); it is left alone.
- No number on a page that is a result. The page's numbers are the
  row's strengths, dates and application numbers and the clause's
  citation and dates, as `data/` holds them (Unsure 7).

### What a reader can falsify

- `git diff main --stat` on this PR touches `pages/api/answers.json`,
  `pages/detail.html`, `milestones/README.md`,
  `milestones/M03/README.md` and `milestones/M03/rulings/pr1.md` only.
- In `pages/api/answers.json`, the one entry has `"agent": null`,
  `"call": null`, `"scripted": true` and a `PLANT` key. Its `row`
  equals the `lisinopril.8.1` object in `data/table.json` and its
  `clause`, less the `id` key, equals `data/clauses.json`'s
  `201.57(c)(9)(i)`, both at `b9f84e3`. Its `question` equals
  `goldens/g-001.yaml`'s.
- In `pages/detail.html`, the JSON inside `<script
  type="application/json" id="answer">` parses to the same object as
  the API's entry. The banner above the answer says it is scripted.
- The page carries none of "validated", "compliant", "Part 11",
  "governed", "secure" or "proven", and no brand name (SPEC/00 §2,
  §11).
- Nothing in this PR reads the door: the greps above find nothing.
- `.gitignore` line 170 ignores `/site`, which is why the pages live
  under `pages/`; `git check-ignore pages/detail.html` answers nothing.

### Carried to PR 2

PR 2 is the measure. It adds the gate that reads the plant and nothing
that lifts it. The sign-in and the call are platform surfaces (agentkeel
SPEC/10 §2, `docs/developer/quickstart.md` §5b); PR 2 uses them as the
platform's own deploy does and redesigns nothing.

- **The sign-in.** Cognito `InitiateAuth`, `AuthFlow`
  `USER_PASSWORD_AUTH`, on the agent's identity pool with its callers
  client (no client secret: the construct makes it with
  `ALLOW_USER_PASSWORD_AUTH`, agentkeel `infra/construct/governed_agent.py`),
  `USERNAME` `pharmadelta`, `PASSWORD` the repository secret. It needs no
  AWS credential. The answer is an access token, masked, held for the
  run and written nowhere.
- **The call.** `POST` on the door's URL with `Authorization: Bearer
  <access token>`, `Content-Type: application/json` and the body
  `{"question": "..."}`, as agentkeel's `src/agent/run.py`
  `invoke_through_door` does. The door's authoriser admits the callers
  client's token whose `username` is in the manifest's `callers`; the
  proxy exchanges to the door's own token and invokes the runtime. The
  body that comes back is the runtime's observation (label-impact
  `server.py`, `agent.answer`): `text`, `parsed`, `stop_reason`,
  `guardrail_topics`, `usage`, `latency_ms`, `tool_calls`, `source`;
  `parsed` holds `table_row`, `clause_id` and the answer fields when
  the model answered with a JSON object, else null. The request id is
  the one the door returns in its response header (`apigw-requestid`
  for an HTTP API; confirmed at PR 2's construction run), which is the
  `request_id` the door's access log carries, so a record in the
  security account can be matched to it. Never: SigV4, an IAM
  credential, the runtime's ARN, the door client's secret. A call
  straight at the runtime is M10's bypass arm and is refused.
- **What the owner sets before PR 2 runs** (none of it in a file): the
  secret `M03_DOOR_PASSWORD`, the caller's password; the repository
  variables `M03_DOOR_URL` (the stack output `DoorUrl`),
  `M03_DOOR_POOL_ID` (`DoorPoolId`) and `M03_DOOR_CALLERS_CLIENT_ID`
  (the pool's `callers` app client, read in the Cognito console: no
  stack output names it, row P item 2); the region is `us-west-2`.
  Names proposed, Security's to rule (Unsure 3).
- **The gate.** `src/m03/gate.py` and `.github/workflows/m03.yml`, on
  every pull request, every push to `main` and by hand. In order: read
  `pages/api/answers.json` and the `id="answer"` block of
  `pages/detail.html`; name every served answer whose `call` is null
  or lacks a field of the record (`answers_uncalled`), and every page
  answer that is not byte for byte an API entry (`answers_disagreed`);
  sign in; for each served answer that carries a call, ask its
  question through the door and compare `table_row`, `clause_id` and
  `answer_fields` with the door's `parsed` (`answers_differing`, the
  served value and the door's beside each); record the door's reading
  for every served answer, called or not, beside the result (`door`:
  signed in, HTTP status, request id, `stop_reason`, `parsed`), so the
  Measured cell carries what the agent said on the day. Write
  `result.json` with `verdict`, the three lists, `door`, `commit`,
  `dirty`, `written_by_ci` and the run URL, and upload it as
  `m03-gate-<sha>`. The job fails on anything but GREEN.
- **The verdict.** RED when `answers_uncalled`, `answers_disagreed` or
  `answers_differing` is non-empty. GREEN only when every served answer
  carries a call record, is shown as served and equals the door's
  answer on this run. UNSCORABLE when nothing is RED and the served
  files could not be read, the sign-in failed, or the door answered
  anything but 200 for a called answer; never RED, never GREEN. The
  first arm, uncalled, is a read of the served files and needs no
  door, so the plant reads RED whatever the door's state that day
  (Unsure 4). Exit 0 GREEN, 1 RED, 2 UNSCORABLE.
- **The expected RED.** On `c7edf8f`: RED, `answers_uncalled`
  `["g-001"]`, `answers_disagreed` `[]`, `answers_differing` `[]`. The
  one served answer carries no call, so nothing is compared. The door's
  reading is recorded beside it and decides nothing on the plant.
- **The call record's fields** on a served answer, proposed (Unsure
  10): `subject` `pharmadelta`, `issuer` `self`, `door_host`, `request_id`,
  `called_at` (UTC), `agent` `label-impact`, `agent_commit`, `run_url`
  (the CI run of this repository that made the call; the link SPEC/00
  §11 asks for beside anything a page shows). PR 2 fixes the names; the
  lift writes them.
- **Equality** is the three answer fields as `parsed` holds them
  (Unsure 5). A called answer whose call returned no `parsed` object is
  served as "no answer" with its question and its call record, and the
  page shows that; a page never shows an answer without its row.
- **What a pull request from a fork gets.** No secret, so the sign-in
  fails and the run reads UNSCORABLE unless an answer is uncalled.
- **Cost.** One call per served answer per run, under the agent's own
  ceilings and `daily_usd` (Unsure 9).

### Row P (platform items, flagged here, built in agentkeel, waited for)

Per CLAUDE.md "Platform changes": named, never designed here.

1. **The registry read for the M01 reader** (M01 Unsure 12, ruled at M01
   PR 2 to be designed at M03): a read-only role in agentkeel, assumed by
   this repository's CI by OIDC, that reads the registry row for
   `label-impact`. Until it exists the `M01 gate` reads PENDING, exit 3,
   on every pull request, and is not required (M01 Unsure 14). Left
   alone in this milestone; not investigated.
2. **The callers client id as a stack output.** The deploy reads
   `DoorUrl`, `DoorPoolId`, `DoorClientId` (the door's own client),
   `DoorTokenEndpoint` and `DoorScope`; no output names the pool's
   `callers` client, which is what an outside caller signs in with. The
   owner reads it in the Cognito console. An output would spare that.
3. **The caller's credential path.** The first password is set by hand
   (`admin-set-user-password`); rotation and revocation of a caller's
   credential are the platform's.
4. **The door's proxy timeout.** The proxy invokes the runtime with a
   28-second timeout (`infra/construct/door.py`, `PROXY_SOURCE`) and an
   HTTP API's integration limit is 30 seconds; an agent call with three
   model rounds can take longer. Read at PR 2's construction run; if a
   call through the door times out where the deploy's did not, that is
   the platform's limit, not this repository's.

### Carried items (owed elsewhere; named so they are not lost)

- **To agentkeel (Engineering, Tool Owner).** A major platform upgrade
  whose only refusal is the agent's own field cannot be fixed from the
  agent's `main`, because the pin rule reads the platform's current
  pin: the upgrade pull request is refused for the missing field and a
  pull request adding the field from `main` is refused for the pin, so
  the two refusals lock each other. Found 2026-10-20 on label-impact
  #2 and #3, resolved by #4 built on the upgrade branch. Owed to
  agentkeel as a finding; not designed here.
- **To label-impact (Engineering, Tool Owner, Data Owner there).** The
  deployed agent's answer record read RED at both deploys (the table
  above): `g-001` ended in `tool_use` with no parsed answer through the
  door (`end_turn` with none on 2026-10-11), `g-003` the same, and the
  two traps answered with `table_row` null. The agent's goldens are its
  own tests (SPEC/00 §3) and this repository changes nothing there.
  What it means here: a call that returns no `parsed` object gives the
  page no row to show, so the lift may serve "no answer" with its call
  record, and row 4 may close GREEN on the call while the page shows the
  agent gave nothing. Named at open so it is not found at PR 4
  (Unsure 6).
- **M02 Unsure 6, for M03's purpose.** label-impact's `data/` equals
  this repository's at `b9f84e3` (compared 2026-10-25, the table above).
  A later rebuild into `data/` reopens it.
- **#18's open Unsure items** (`milestones/adoption/rulings/build-fixes.md`)
  are the build's, not M03's.

### Rulings carried from earlier milestones

| # | Ruled |
|---|---|
| M01's 23 (ruled at M02 PR 1) | The Measured cell cites the run on `main` after PR 2 merges, with the PR run named beside it when it was the one read at the time. Row 4's expected gate output says so. |
| M01's 12 (ruled at M01 PR 2) | The registry read is designed at M03 as a read-only role in agentkeel assumed by OIDC, flagged there and not here. Row P item 1 above is that flag. Nothing in this PR designs it. |

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant.

| # | Item | Seat |
|---|---|---|
| 1 | What "a public API" is at M03: a read API, a public JSON file of answers each produced by a CI call as `pharmadelta` with its record (this file's assumption), or a live path that forwards a visitor's question on request, which needs a host that runs code and holds the credential, and exposes the agent's daily budget to anyone. Proposed: the read API at M03; a live path is a later row's or a platform item. | Product, Security |
| 2 | Where the pages and the API are served. GitHub Pages is not enabled on this repository (404, 2026-10-25); enabling it, and from which branch and directory, is a repository setting. Until it is, "public" means readable in the repository. `/site` is ignored by `.gitignore` line 170, so the directory is `pages/`. | Product, Security |
| 3 | The secret and the variables PR 2 reads: `M03_DOOR_PASSWORD` as the one secret; the door URL, the pool id and the callers client id as repository variables (none is a secret; the URL is public and the ids are not credentials); who sets them and under whose record. Names proposed under "Carried to PR 2". | Security |
| 4 | The verdict's shape: RED on an uncalled served answer needs no door read, so the plant's RED does not depend on the pool or the door that day; UNSCORABLE only when nothing is RED and a read failed. M02's gate read UNSCORABLE whenever a source could not be read; this differs, because F3.1's first arm is a read of the served files alone. | Product, Engineering |
| 5 | What "equals the door's answer" compares: `table_row`, `clause_id` and `answer_fields` of the door's `parsed` object on the gate's run. The agent runs at temperature 0, but the deploys show it does not always parse to an answer; a served answer whose call returned none is shown as "no answer" with its call record. Whether the comparison is against the run's own call (proposed) or against the call that produced the served answer, which only the security account's records could confirm. | Product, Data Owner, Threshold Owner |
| 6 | The deployed agent's answer record is RED at both deploys and `g-001` gave no parsed answer through the door (carried items). Whether M03 proceeds to PR 2 with the agent as it stands, and what row 4's cell says if the lift serves a call record with no answer. Not this repository's to fix. | Engineering, Tool Owner (label-impact); Product |
| 7 | Numbers on the page: the row's strengths, dates and application numbers and the clause's citation, dates and source note are the row's and the clause's own data, each with its source, not a measured result. Whether SPEC/00 §11's "a number on a page comes from a CI-written result" reaches a row's data. | Product |
| 8 | The ruling file names this PR as #19, the next number on this repository. | Product |
| 9 | Cost and ceilings: one call per served answer per gate run on every pull request and push to `main`, under the agent's `concurrency` 2, `rps_per_edge` 1 and `daily_usd` 10; the spend is the agent's, not this repository's. Whether the gate runs on every pull request or on `main` and by hand only. | Threshold Owner, Security |
| 10 | The call record's fields on a served answer and which the gate can verify from here: `run_url` is a run of this repository's workflow, readable through GitHub's API; the `request_id` can be matched to the door's access log only in the security account, which agentkeel's observer reads, not this repository. | Engineering, Security |
