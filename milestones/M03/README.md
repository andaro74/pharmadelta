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
| Measured | RED, `answers_uncalled` `["g-001"]`, `answers_disagreed` `[]`, `answers_differing` `[]`, `unreadable` `[]`, `written_by_ci` true, on `main` at `0b8d2ec`: [run 41171470951](https://github.com/andaro74/pharmadelta/actions/runs/41171470951), artifact `m03-gate-0b8d2ec7598b61c30f861a3f2114c2a13e89ad71`. The PR run on #20 at merge ref `f97f292`, [run 41126878288](https://github.com/andaro74/pharmadelta/actions/runs/41126878288), artifact `m03-gate-f97f292d7e9588807a5333835e1ae23fb759c683`, read the same on every field the row names. Equals the expected output. |
| PRs used / cap | 4 / 4 |
| State | GREEN |

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

## Open detail (PR 2, 2026-10-30)

PR 2 is the measure. It adds the gate that reads the plant and nothing
that lifts it. `pages/api/answers.json` serves one answer with `call`
null at the head this PR measures, and `pages/detail.html` shows it. M03
is measured here.

### What this PR holds

- `src/m03/gate.py`, the gate. Python 3.14, standard library only
  (`urllib`, `json`, `re`, `base64`); `pyproject.toml` and `uv.lock` are
  unchanged. In order:
  1. Reads `pages/api/answers.json` (the `answers` list) and the JSON in
     the `<script type="application/json" id="answer">` block of
     `pages/detail.html` (one object or a list).
  2. `answers_uncalled`: every served answer whose `call` is null, is not
     an object, lacks a field of the call record or holds it empty, or
     whose `subject` is not `pharmadelta`. A read of the served file; no
     door.
  3. `answers_disagreed`: every page answer whose `id` the API does not
     serve, or that is not equal to the API's entry of that `id` as
     parsed JSON in canonical form (sorted keys, no whitespace). The
     page's block and the API's entry are both pretty-printed at
     different depths, so "byte for byte" is read as "the same JSON
     value" (Unsure 15).
  4. Signs in (below) when the environment holds the secret and the
     three variables; else records `not attempted` and which were
     missing, by name.
  5. Asks the door every served answer's question, called or not, and
     records the reading under `door` (Unsure 11).
  6. `answers_differing`: every served answer that carries a call record
     and whose `table_row`, `clause_id` or `answer_fields` is not what
     the door's `parsed` holds on this run.
  7. Writes `result.json` and exits 0 GREEN, 1 RED, 2 UNSCORABLE.
- `.github/workflows/m03.yml`: on every pull request, every push to
  `main` and by hand. `uv sync --locked`, the artifact directory, the
  gate with the secret and the three variables in its `env`, then the
  artifact `m03-gate-<sha>` holding `result.json`, uploaded whenever the
  gate wrote a result. The gate writes its table to the job summary. The
  job fails on anything but GREEN. `gate.yml`, `m01.yml` and `m02.yml`
  are unchanged.
- `result.json` records the commit, whether the tree was dirty, whether
  CI wrote it (`written_by_ci`), the run's URL, the call record's fields,
  the fields compared, which of the secret and the variables the
  environment held (`env_set`, booleans), the sign-in's record, each
  served answer's record check, page equality, door reading and
  comparison, so the file says for itself whether it is evidence (P4).
- `rulings/pr2.md`, and "PRs used / cap" set to 2 / 4 here and in the
  ledger.

### The sign-in and the call, as built

Both are the platform's surfaces (agentkeel SPEC/10 §2, R2;
`docs/developer/quickstart.md` §5b; `src/agent/run.py`
`invoke_through_door`; `infra/construct/door.py`), used as the platform's
own deploy uses them and redesigned nowhere.

- **The sign-in.** `POST https://cognito-idp.us-west-2.amazonaws.com/`
  with `X-Amz-Target: AWSCognitoIdentityProviderService.InitiateAuth`,
  `Content-Type: application/x-amz-json-1.1` and the body `{"AuthFlow":
  "USER_PASSWORD_AUTH", "ClientId": <callers client>, "AuthParameters":
  {"USERNAME": "pharmadelta", "PASSWORD": <secret>}}`. No AWS credential,
  no client secret, no SigV4. The answer's `AuthenticationResult.AccessToken`
  is the token sent to the door: the door's authoriser admits a token
  whose `token_use` is `access`, whose `client_id` is the callers client
  and whose `username` is in the manifest's `callers`
  (`infra/construct/door.py`, `handler`), so the id token would be
  refused. A `ChallengeName` in the answer, an HTTP error or no token is
  recorded as a failed sign-in with Cognito's error type, and nothing is
  called. The token is held in memory for the run and written nowhere;
  the result records `signed_in`, `token_use` and `username` from its
  claims, read without verification (the door verifies), and nothing
  else of it (Unsure 18).
- **The call.** `POST` on `M03_DOOR_URL` with `Authorization: Bearer
  <access token>`, `Content-Type: application/json`, body `{"question":
  "..."}`, a 90-second timeout (Unsure 21). The URL must be https on a
  host under `.execute-api.us-west-2.amazonaws.com` with a path ending
  `/invocations`; anything else is refused before a request is made.
  Recorded per served answer: HTTP status, the request id and the header
  it came in (`apigw-requestid` first; Unsure 13), the response's header
  names, and from a 200 body `parsed`, `stop_reason`, `text`, `error`,
  `refused`, `latency_ms`, `guardrail_topics`, `tool_calls`, `usage`,
  `source` (label-impact `agent.py` `answer`). A body with `error` or
  `refused` (label-impact `server.py` sends 200 with `error` on a failed
  model call, 403 with `refused` on a chain refusal) is recorded and not
  compared (Unsure 22).
- **Never written**: the password, the URL, the pool id, the client id,
  the token. `env_set` holds four booleans. The sign-in record holds the
  pool id's region prefix (`us-west-2`) and nothing more of it.

### The verdict

- **RED** when `answers_uncalled`, `answers_disagreed` or
  `answers_differing` is non-empty. The first two are reads of the served
  files and come before the sign-in, so the plant reads RED whatever the
  pool's or the door's state that day (Unsure 4, ruled).
- **GREEN** only when every served answer carries a call record as
  `pharmadelta`, every page answer is an API entry, and every served
  answer that was compared equals the door's answer on this run, with
  nothing unread.
- **UNSCORABLE** when nothing is RED and: a served file could not be read
  or parsed, the API serves no answer (Unsure 14), the environment lacks
  the secret or a variable, the sign-in failed, or the door did not
  answer 200 with an observation for a called answer. Never RED, never
  GREEN.
- A pull request from a fork gets no secret: UNSCORABLE unless an answer
  is uncalled or disagreed (Unsure 19).

### The call record's fields (Unsure 10, ruled)

`subject` (`pharmadelta`), `issuer` (`self`), `door_host`, `request_id`,
`called_at` (UTC), `agent` (`label-impact`), `agent_commit`, `run_url`.
The gate names an answer uncalled when any is missing or empty or when
`subject` is not `pharmadelta`. The lift writes them; `door_host` is a
variable's value and is Unsure 12.

### What this PR does not hold

- No lift. `git diff main -- pages/` is empty: `pages/api/answers.json`
  carries `call: null`, `scripted: true` and the `PLANT` key as at
  `c7edf8f`.
- No value of the secret or a variable. Grep `execute-api`, `us-west-2_`
  and `amazonaws.com/` under `src/m03/` and `.github/workflows/m03.yml`:
  the matches are the host suffix the gate requires and the Cognito
  endpoint, never a URL, a pool id or a client id of this agent.
- No change to `pyproject.toml`, `uv.lock`, `gate.yml`, `m01.yml`,
  `m02.yml`, `data/`, `goldens/`, `src/baseline/` (P5), `src/gate/`,
  `src/ingest/`, `src/m01/`, SPEC/00, CLAUDE.md or anything under
  `milestones/M00/`, `M01/`, `M02/` or `adoption/`.
- No change to label-impact or to agentkeel. The `M01 gate` still reads
  PENDING, exit 3, and is not required; left alone.
- No SigV4, no IAM credential, no runtime ARN, no door client secret: grep
  `sigv4`, `AWS4`, `boto`, `arn:aws`, `client_secret`, case folded, under
  `src/m03/` and the workflow: two matches, the sentence "Never SigV4,
  never the runtime's ARN, never the door client's secret" in the gate's
  docstring and in the workflow's comment.

### Construction run (not evidence, P4)

Run on 2026-10-30 on the branch before the first push, from the working
tree, so `written_by_ci` is false and the tree was dirty. The caller's
password is a repository secret and cannot be read outside Actions, so
no construction run signed in; the door's own reading of the question
is made first by the CI run on this PR. Four readings, in order:

| Reading | What was read |
|---|---|
| the gate with no environment | `RED`, `answers_uncalled` `["g-001"]` (`call is null`), `answers_disagreed` `[]`, `answers_differing` `[]`; the page's one answer equal to the API's entry; sign-in `not attempted`, the four names missing; door not asked; exit 1 |
| the gate with the three variables in the shell's environment (read with `gh variable get` into shell variables, never printed) and no password | the same verdict and lists; `env_set` `url`, `pool_id`, `client_id` true, `password` false; sign-in `not attempted`; door not asked. `result.json` grepped for `execute-api` and `us-west-2_`: no match |
| one `POST` on the door with no token, `{"question": "probe: no token"}` (the call M10's run file names `none`) | `401`, body `{"message":"Unauthorized"}`, response headers `apigw-requestid` (16 characters), `connection`, `content-length`, `content-type`, `date`. The request id header is confirmed as `apigw-requestid`, the name the gate reads first. This call is a refused call with no identity and leaves a record in the security account's access log, as SPEC/10 §2 says it must; that record is agentkeel's to read, not this repository's (Unsure 20) |
| seven made-up pairs of files in the session's scratch directory, not committed | a called answer with the page equal and no environment: `UNSCORABLE`, exit 2. The page's `owed` changed: `RED`, `answers_disagreed` `["g-001"]`. The page showing `g-999`: `RED`, `answers_disagreed` `["g-999"]`. A call record missing `run_url`: `RED`, `answers_uncalled`. A record with `subject` `platform`: `RED`, `answers_uncalled`. Zero served answers: `UNSCORABLE`. The page without its block while the plant is uncalled: `RED`. `compare()` on g-001's served answer: a flat `parsed` of the same values equal; the same values under `answer_fields` equal; the deploy's g-002 shape differs on `table_row`, `clause_id`, `impacted`, `owed`; null against an answer differs; null against null equal |

One defect was found by the seventh pair and fixed before the first
push: a page path outside the repository made `Path.relative_to` raise,
and the uncalled plant then read `UNSCORABLE` instead of `RED`. The gate
now names a file as the repository names it, or as given.

### Expected CI result on this PR

The ledger row says: RED, `answers_uncalled` `["g-001"]`,
`answers_disagreed` `[]`, `answers_differing` `[]`. The CI run on this
PR is expected to write that, with `written_by_ci` true and the run URL,
and to fail the job (exit 1). Beside it, for the first time from this
repository, the door's reading of g-001's question as `pharmadelta`: the
sign-in's record, the HTTP status, the request id, `stop_reason` and
`parsed`. That reading decides nothing on the plant. At both of
agentkeel's deploys g-001 ended in `tool_use` with no parsed answer
(PR 1, "The deployed agent, as read at open"), so a `parsed` of null is
the likely reading and is recorded as what the agent said that day. The
CI run is the measurement; the construction run decides nothing.

### Observed (CI run, 2026-10-30)

The first run on this PR,
[41126878288](https://github.com/andaro74/pharmadelta/actions/runs/41126878288),
wrote the artifact `m03-gate-f97f292d7e9588807a5333835e1ae23fb759c683`
(the sha is the pull request's merge ref, as M00's, M01's and M02's
were; the branch head was `ab0b981`). It holds `result.json`:

| Field | Value |
|---|---|
| `verdict` | `RED` |
| `answers_uncalled` | `["g-001"]`: `call is null` |
| `answers_disagreed` | `[]`: the page's one answer equals the API's entry |
| `answers_differing` | `[]`: nothing compared, the one served answer carries no call |
| `unreadable` | `[]` |
| `env_set` | all four true; no value of any in the file (grepped for `execute-api` and `us-west-2_`: no match) |
| `sign_in` | `signed_in` true, status 200, `token_use` `access`, `token_username` `pharmadelta`, `expires_in` 3600, 622 ms |
| `door[0]` for g-001's question | status 200; `request_id` `GE2QwjpovHcESyQ=` in the header `apigw-requestid` (Unsure 13, confirmed on an admitted call); response headers `apigw-requestid`, `connection`, `content-length`, `content-type`, `date`; `stop_reason` `tool_use`; `parsed` null; `text` empty; `error` null; `refused` null; `guardrail_topics` `[]`; `source` `dynamodb`; `latency_ms` 5969 (the runtime's), 10086 ms wall; `usage` 5591 in, 279 out |
| `door[0].tool_calls` | three calls of `find_label_row`, each `{"label": "lisinopril", "section": 8.1}` with `section` a number, each `status` `error`: `8.1 is not one of ['bw', '5', '5.1', '6', '8.1']`. The model asked the right row three times and the tool refused the number where it holds strings; the run ended at the tool-call ceiling with no answer |
| `written_by_ci` | `true`; `commit` `f97f292`, `dirty` false; exit 1; the `M03 gate` job failed. `M00 gate` and `M02 gate` on the same head passed ([41126878150](https://github.com/andaro74/pharmadelta/actions/runs/41126878150), [41126878245](https://github.com/andaro74/pharmadelta/actions/runs/41126878245)). `M01 gate` is not required and reads as it did on `main` |

Equals the expected result above on every field the ledger row names.
The plant is named as ledger row 4 expects. The door's reading is
recorded beside it and decides nothing.

What the door's reading says, for the seat that owns it (Unsure 23;
carried to label-impact, not fixed here): the deployed agent gave no
answer to g-001 because its tool refused the model's argument. The
model sent `section` as the number `8.1`; `find_label_row` in
label-impact's `agent.py` compares it with the strings `'bw'`, `'5'`,
`'5.1'`, `'6'`, `'8.1'` and names it not one of them, three times, and
the run stopped at `tool_use` with empty text. That is the same reading
agentkeel's deploys recorded (`g-001 ordinary tool_use None`), now with
the cause. It is label-impact's (SPEC/00 §3, the agent's own tests);
this repository changes nothing there. For M03 it means the lift, as the
agent stands, serves g-001 as "no answer" with its call record (PR 1,
"Equality"), and the page shows that.

### What a reader can falsify

- The artifact `m03-gate-<sha>` on this PR's run holds `result.json`
  with `verdict: RED`, `answers_uncalled: ["g-001"]`,
  `answers_disagreed: []`, `answers_differing: []` and `written_by_ci:
  true`. Download it and read it.
- In that `result.json`, `env_set` is four booleans; grep it for
  `execute-api` and `us-west-2_`: no match. `sign_in` holds no token.
- `door[0]` holds `status`, `request_id`, `request_id_header`,
  `stop_reason` and `parsed` for g-001's question, or `asked: false` with
  why.
- `git diff main --stat` on this PR touches `src/m03/`,
  `.github/workflows/m03.yml`, `milestones/README.md`,
  `milestones/M03/README.md` and `milestones/M03/rulings/pr2.md` only.
  `git diff main -- pages/ pyproject.toml uv.lock` is empty.
- Grep `secrets.` and `vars.` in `.github/workflows/m03.yml`: four
  matches, the four names, in the gate step's `env` only.
- The gate reads two hosts: grep `https://` under `src/m03/`, the one
  literal is the Cognito endpoint; the door's URL comes from the
  environment and `check_url` refuses any host not under
  `.execute-api.us-west-2.amazonaws.com`.

### After this PR goes RED

The plant is lifted by the one change named under "The false state":
`agent` and `call` filled with the record of the call that produced the
answer, the answer fields what that call returned, `scripted` false, the
`PLANT` key removed, and the page rebuilt from it. Which PR carries the
lift is ruled on reading this PR's CI run, as M02's was at PR 2
(`milestones/M02/README.md`, "After this PR goes RED"). The lift needs a
call made by this repository's CI as `pharmadelta` and its record
written into `pages/api/answers.json`; how that record gets from a CI
run into a commit is the lift PR's to say, not this one's.

**Ruled at PR 2, on reading run 41126878288 (Product).** The lift is
carried by PR 4, as M00's, M01's and M02's were. PR 3, if the cold review
of #20 finds anything, repairs and does not lift; if it finds nothing,
PR 3 is skipped. The Measured cell takes the `main` run after #20 merges
(M01 Unsure 23, ruled at M02 PR 1), which reads as run 41126878288 did
on the three lists, whatever the door answers that day. As the agent
stands, the lift serves g-001 as "no answer" with its call record
(Unsure 6, 23), and what row 4's cell then says is Product's at PR 4.

## Repair (PR 3, 2026-10-31)

PR 3 is the repair: what the cold review of PR 2 (#20) found, and nothing
else. The plant stands: `pages/api/answers.json` serves g-001 with `call`
null and `pages/detail.html` shows it, as at `c7edf8f`; `git diff main --
pages/` is empty. Nothing here lifts, and nothing here decides the row:
the `main` run after #20 merged is the measurement, and PR 4 fills the
"Measured" cell from it. `rulings/pr2.md` 10 said: PR 3, if the cold
review finds anything, repairs and does not lift. It found one defect in
the gate's verdict path, so this is PR 3.

### The `main` run after #20 merged, read at PR 3

[Run 41171470951](https://github.com/andaro74/pharmadelta/actions/runs/41171470951)
on `main` at `0b8d2ec` (push, 2026-10-31 05:09 UTC), the run the Measured
cell cites (M01 Unsure 23). Read first in this session with `gh run
download`; artifact `m03-gate-0b8d2ec7598b61c30f861a3f2114c2a13e89ad71`,
its `result.json`:

| Field | Value |
|---|---|
| `verdict` | `RED` |
| `answers_uncalled` | `["g-001"]`: `call is null` |
| `answers_disagreed` | `[]`: the page's one answer equals the API's entry |
| `answers_differing` | `[]`: nothing compared |
| `unreadable` | `[]` |
| `env_set` | all four true; grepped for `execute-api` and `us-west-2_`: no match |
| `sign_in` | `signed_in` true, status 200, `token_use` `access`, `token_username` `pharmadelta`, `expires_in` 3600, 691 ms |
| `door[0]` for g-001's question | status 200; `request_id` `GF-1ZhzEvHcEMbQ=` in `apigw-requestid`; `stop_reason` `end_turn`; `parsed` `{"table_row": null, "clause_id": "21 CFR 201.57(c)(9)(i)", "impacted": false, "owed": "none", "escalate": false}`; `error` null; `refused` null; `guardrail_topics` `[]`; `source` `dynamodb`; `latency_ms` 7058, 10845 ms wall; `usage` 5591 in, 412 out |
| `door[0].tool_calls` | two calls of `find_label_row`, each `{"label": "lisinopril", "section": 8.1}`, each refused: `8.1 is not one of ['bw', '5', '5.1', '6', '8.1']`. The model then stopped calling and wrote an answer whose text says it met a tool error, must not invent a row, and answers "not found" |
| `written_by_ci` | `true`; `commit` `0b8d2ec`, `dirty` false; `event` `push`, `ref` `refs/heads/main`; exit 1; the job failed |

The same as run 41126878288 on the three lists, `unreadable`,
`written_by_ci` and the sign-in. Equals ledger row 4's expected output
on every field the row names. The door's reading differs from the PR
run's: there the model called the tool three times and ended at
`tool_use` with `parsed` null; here it called twice, gave up and ended at
`end_turn` with a parsed object whose `table_row` is null and whose
`clause_id` carries a `21 CFR ` prefix that `data/clauses.json`'s id does
not. The cause is the same (Unsure 23); what it does to the lift is
Unsure 26.

### Cold review of #20

Read on `main` at `0b8d2ec`, before any edit: `src/m03/gate.py` line by
line against "Open detail (PR 2)" and `rulings/pr2.md` 1 to 7,
`.github/workflows/m03.yml`, `pages/api/answers.json`,
`pages/detail.html`, and the two CI results (41126878288 and
41171470951) against the "Observed" tables. Four findings. One is a
defect in the verdict path and is repaired here; one is a wrong label in
the job summary and is repaired beside it; two are readings, named under
Unsure.

1. **Defect 1, repaired.** `compare()` calls `.get` on the served
   `answer` and on its `answer_fields`. A served answer that carries a
   call record and whose `answer` is neither null nor an object (or whose
   `answer_fields` is not an object) raises `AttributeError` once the
   door has answered 200, and `main`'s handler then writes the whole run
   `UNSCORABLE`, exit 2, with no `answers_uncalled` list. On a file that
   also serves the uncalled plant, that run reads UNSCORABLE where ruling
   3 (Unsure 4) says RED comes first and UNSCORABLE only when nothing is
   RED. Reproduced at construction (below) with the sign-in and the door
   stubbed. The same family as the `Path.relative_to` defect PR 2 fixed
   before its first push. Not reachable on the plant (nothing is
   compared) or on the lift as PR 1 describes it (null or an object).
2. **Label, repaired.** The job summary's "compared" column printed "not
   compared (uncalled)" for every served answer that was not compared,
   including a called one the door was not asked or did not answer 200
   for. It now prints why: "no call record", the shape, or the door's
   status.
3. **Reading, Unsure 25.** Ledger row 4's expected output says GREEN
   "only when every served answer carries a call record, is shown as
   served and equals the door's answer". The gate names a page answer
   the API does not serve, or that differs from the API's entry, and
   does not name a served answer the page does not show, as PR 1's "The
   gate" and F3.1's third arm define it. With one served answer, shown,
   the two readings agree.
4. **Reading, Unsure 27.** The gate names an answer uncalled when
   `door_host` is missing or empty (ruling 7). If Security rules Unsure
   12 as "not written", no lift can pass the gate as it stands; that
   change is this PR's slot or none, and this PR does not make it
   unruled.

Also read, no finding: `check_url` refuses any host not under
`.execute-api.us-west-2.amazonaws.com` before a request; `sign_in` returns
on every error path before `answer` is read; `ask_door` records the
status and the body on a non-200 and never the token; no exception
message on any path carries a value of the secret or the variables
(`HTTPError` and `URLError` print no URL; `Request` is built only after
`check_url`); the workflow reads the four names in the gate step's `env`
only, uploads on `if: always()` with `if-no-files-found: error`, and
`permissions` is `contents: read`. `pyproject.toml`, `uv.lock`,
`gate.yml`, `m01.yml`, `m02.yml` are unchanged by #20.

### Defect 1: the repair

`src/m03/gate.py`, three places and the docstring:

- `served_answer_check(answer)`: None for null or an object whose
  `answer_fields` is null, absent or an object; else why it cannot be
  compared. Exactly the shapes that raised; a served answer PR 2
  compared is compared the same way.
- In `run`, each served answer's shape is checked before the comparison
  and recorded as `answer_shape`. A malformed answer is recorded under
  `unreadable` by id, is not compared, and `not_compared` says why. The
  order is: no call record, then shape, then the door's status, then
  `compare`. RED on an uncalled, disagreed or differing answer still
  comes first; a malformed served answer makes the run UNSCORABLE only
  when nothing is RED, the same reading as "a served file could not be
  read" (ruling 3), at the entry (Unsure 24).
- `compare` no longer raises on any input: a non-object served answer
  reads "cannot be compared", `answer_fields` is read only when it is an
  object. `run` does not reach it with those shapes; this is so a reader
  of `compare` alone finds no path that raises.
- The summary's "compared" column prints `not_compared`.

The verdict on every input PR 2's construction run exercised is
unchanged (below).

### Construction readings (not evidence, P4)

Run 2026-10-31 on this branch from the working tree, `written_by_ci`
false. No sign-in: the password is a repository secret. Readings:

| Reading | Before the repair | After |
|---|---|---|
| the real pages, no environment | `RED`, `answers_uncalled` `["g-001"]`, exit 1 | the same; the summary's compared column reads "not compared: no call record" |
| pair a: the plant plus a called `g-002` whose `answer` is the string `"no answer"`, the sign-in and the door stubbed to answer as run 41171470951 did | `UNSCORABLE`, exit 2, `AttributeError: 'str' object has no attribute 'get'`, no `answers_uncalled` | `RED`, `answers_uncalled` `["g-001"]`, `unreadable` `["g-002: the served answer is a str, not null or an object, and cannot be compared"]`, g-002 not compared, exit 1 |
| pair b: as a, with `answer_fields` the string `"none"` | `UNSCORABLE`, exit 2, the same error | `RED`, `answers_uncalled` `["g-001"]`, `unreadable` names g-002's `answer_fields`, exit 1 |
| `compare()` alone | `compare(plant's served answer, the main run's parsed)`: differs on `table_row`, `clause_id`, `impacted`, `owed`; `compare(None, that parsed)`: one side has an answer; `compare("no answer", …)` raises | the first two the same; the third reads "not null or an object and cannot be compared"; an object with string `answer_fields` differs on all five |

The stub files and the script live in the session's scratch directory
and are not committed (M01 Unsure 21's reading: no test file).

### What this PR does not hold

- No lift. `git diff main -- pages/` is empty.
- No change to the verdict on any input PR 2 compared, to the fields
  compared, to the call record's fields, to the sign-in, to the call, to
  what is written of the environment, or to `.github/workflows/m03.yml`.
- No change to `pyproject.toml`, `uv.lock`, `gate.yml`, `m01.yml`,
  `m02.yml`, `data/`, `goldens/`, `src/baseline/` (P5), SPEC/00,
  CLAUDE.md, or anything under `milestones/M00/`, `M01/`, `M02/` or
  `adoption/`. The `M01 gate` still reads PENDING and is not required.
- No change to label-impact or to agentkeel.
- No "Measured" cell and no tag. Those are PR 4's.

### Expected CI result on this PR

The plant stands, so the run on this PR is expected to read as 41171470951
did: `RED`, `answers_uncalled` `["g-001"]`, `answers_disagreed` `[]`,
`answers_differing` `[]`, `unreadable` `[]`, `written_by_ci` true, the
job failed. New in the result: `answer_shape` "null or an object; can be
compared" and `not_compared` "no call record" on g-001. The door's
reading beside it is whatever the agent says that day and decides
nothing. It is one more call as `pharmadelta` (ruling 6).

### What a reader can falsify

- `git diff main --stat` on this PR touches `src/m03/gate.py`,
  `milestones/README.md`, `milestones/M03/README.md` and
  `milestones/M03/rulings/pr3.md` only.
- In `src/m03/gate.py`, `served_answer_check` returns None for `None`
  and for `{"answer_fields": {}}`, and a string for `"x"` and for
  `{"answer_fields": "x"}`; `compare("x", None)` returns a dict and does
  not raise.
- The artifact on this PR's run holds `result.json` with `verdict: RED`,
  `answers_uncalled: ["g-001"]`, `unreadable: []`, `written_by_ci: true`,
  and `served[0].answer_shape` and `served[0].not_compared` present.
- Grep `secrets.` and `vars.` in `.github/workflows/m03.yml`: unchanged,
  four matches in the gate step's `env`.

### Observed (CI run, 2026-10-31)

The first run on this PR,
[41216016582](https://github.com/andaro74/pharmadelta/actions/runs/41216016582),
wrote the artifact `m03-gate-f82422576e2f3d96935abee98e32f2f41f6d3001`
(the sha is the pull request's merge ref; the branch head was `2c15639`).
Its `result.json`:

| Field | Value |
|---|---|
| `verdict` | `RED` |
| `answers_uncalled` | `["g-001"]`: `call is null` |
| `answers_disagreed` | `[]`: the page's one answer equals the API's entry |
| `answers_differing` | `[]`: nothing compared |
| `unreadable` | `[]` |
| `served[0]` | `answer_shape` "null or an object; can be compared"; `not_compared` "no call record"; `comparison` null; `page_equal` true. The two fields this PR adds, present |
| `env_set` | all four true; grepped for `execute-api` and `us-west-2_`: no match |
| `sign_in` | `signed_in` true, status 200, `token_use` `access`, `token_username` `pharmadelta`, `expires_in` 3600, 570 ms |
| `door[0]` for g-001's question | status 200; `request_id` `GHbUBguyvHcEMoQ=` in `apigw-requestid`; `stop_reason` `end_turn`; `parsed` null; `error` null; `refused` null; `guardrail_topics` `[]`; `source` `dynamodb`; `latency_ms` 6120, 9949 ms wall; `usage` 5591 in, 296 out |
| `door[0].tool_calls` | two calls of `find_label_row`, `{"label": "lisinopril", "section": 8.1}`, each refused as before. The model then stopped and wrote prose: it met a tool error, will not fabricate a row or clause, asks for the question to be resubmitted. No JSON object in the text, so `parsed` is null |
| `written_by_ci` | `true`; `commit` `f824225`, `dirty` false; `event` `pull_request`, `ref` `refs/pull/21/merge`; exit 1; the `M03 gate` job failed. `M00 gate` and `M02 gate` on the same head passed ([41216016830](https://github.com/andaro74/pharmadelta/actions/runs/41216016830), [41216016645](https://github.com/andaro74/pharmadelta/actions/runs/41216016645)). `M01 gate` is not required and reads as it did on `main` |

Equals the expected result above on every field. The plant is still named
as ledger row 4 expects, and the repair changed nothing on it. The
door's reading is a third shape in three CI runs: `tool_use` with
`parsed` null (41126878288), `end_turn` with an object whose `table_row`
is null (41171470951), `end_turn` with prose and `parsed` null (this
run). Same two refusals each time. Recorded for Unsure 26; decides
nothing.

## Close (PR 4, 2026-10-31)

PR 4 closes the milestone at the cap, 4 / 4. It carries the lift, fills
the "Measured" cell from a CI-written result and writes the row's state,
rules or carries by name every open Unsure item of PR 1, PR 2 and PR 3,
and adds `rulings/pr4.md`. The tag `m03` goes on its merge commit after
the run on `main` is read. Nothing here decides the row: the `main` run
after #20 merged is the measurement, and this PR reads it again before
writing the cell. The gate, `src/m03/gate.py` and `m03.yml`, is not
changed.

### Precondition, read at open

#21 merged at `51dfa3a` on 2026-10-31. `main` holds `src/m03/gate.py`
with `served_answer_check` and `milestones/M03/rulings/pr3.md`. The
`main` run after #21 merged,
[41221327681](https://github.com/andaro74/pharmadelta/actions/runs/41221327681)
on `51dfa3a`, read with `gh run download`: `RED`, `answers_uncalled`
`["g-001"]`, `answers_disagreed` `[]`, `answers_differing` `[]`,
`unreadable` `[]`, `written_by_ci` true; the door's reading `end_turn`
with a parsed object whose `table_row` is null, two refused tool calls,
as run 41171470951 read. The plant stood: `git diff c7edf8f main --
pages/` was empty.

### The two runs, read again at PR 4

Both downloaded with `gh run download` in this session before the cell
was written. Every field the ledger row names, side by side:

| Field | `main` run [41171470951](https://github.com/andaro74/pharmadelta/actions/runs/41171470951) | PR run [41126878288](https://github.com/andaro74/pharmadelta/actions/runs/41126878288) |
|---|---|---|
| `commit` | `0b8d2ec`, `main` after #20 merged, `event` `push` | `f97f292`, merge ref of #20, `event` `pull_request` |
| artifact | `m03-gate-0b8d2ec7598b61c30f861a3f2114c2a13e89ad71` | `m03-gate-f97f292d7e9588807a5333835e1ae23fb759c683` |
| `verdict` | `RED` | `RED` |
| `answers_uncalled` | `["g-001"]` | `["g-001"]` |
| `answers_disagreed` | `[]` | `[]` |
| `answers_differing` | `[]` | `[]` |
| `unreadable` | `[]` | `[]` |
| `written_by_ci` | `true` | `true` |
| the door's reading (decides nothing) | `end_turn`, `parsed` an object with `table_row` null | `tool_use`, `parsed` null |

Both equal row 4's expected gate output on every field it names.

### Measured

The cell cites the run on `main` after #20 merged, 41171470951 on
`0b8d2ec` (M01 Unsure 23, ruled at M02 PR 1; `rulings/pr2.md` 10;
`rulings/pr3.md` 4), with the PR run 41126878288 named beside it as the
one read at the time. It is written in the ledger's words, as rows 0 to
2 are. The cell equals the expected gate output written at open, so
under the ledger's rule row 4 is GREEN and "PRs used / cap" is 4 / 4.
The lift's own runs (below) are recorded here, not in the cell: they say
what the agent answered on the day and do not decide the row.

### Unsure 12, ruled before the lift (Security)

`door_host` is the SHA-256 of the door URL's host, lower-cased, written
`sha256:<64 hex>`. The host is never written. A hash fits the gate as it
stands, which names an answer uncalled when the field is empty (ruling
pr2.md 7); "not written" would need a gate change this PR does not make
(Unsure 27). The ruling and its limit (the host is a short id under a
known suffix, so the hash can be searched by anyone who wants the id;
the door admits only an admitted caller's token, so the host is not a
credential) are `rulings/pr4.md` 1. Ruled in the first commit of this
PR, `e5f79ef`, before any page was written.

### The lift path (Unsure 28)

Two candidates were weighed:

- (a) A `workflow_dispatch` job signs in, calls the door, writes the two
  pages and commits them to the PR branch with `GITHUB_TOKEN`. One step
  from call to commit, no hand in between. Needs `contents: write` on
  that workflow, a token that can push to a branch, and a bot commit on
  the branch.
- (b) The job writes the call record and the door's body as an artifact;
  the pages are rebuilt from that artifact by hand into the PR, with the
  artifact's run named in the record. Every workflow keeps `contents:
  read`. One hand step, which a reader repeats.

Built: (b), the smaller change (`rulings/pr4.md` 2). Either way the call
is CI's as `pharmadelta`; a local call is not a record (P4).

- `.github/workflows/m03-lift.yml`: `permissions: contents: read`. One
  job: `uv sync --locked`, then `uv run python -m src.m03.lift call`
  with the secret `M03_DOOR_PASSWORD` and the variables `M03_DOOR_URL`,
  `M03_DOOR_POOL_ID`, `M03_DOOR_CALLERS_CLIENT_ID` in that step's `env`,
  the same four names as `m03.yml`; then the artifact `m03-lift-<sha>`
  holding `call.json`, uploaded on `if: always()`. It runs by hand
  (`workflow_dispatch`) and once on a push that adds or edits its own
  file on a branch other than `main`, because a dispatch needs the file
  on the default branch and the lift's call is made before this PR
  merges (Unsure 32).
- `src/m03/lift.py call`: reads the questions `pages/api/answers.json`
  serves, signs in and asks the door with the gate's own `sign_in` and
  `ask_door` (imported, not copied), and writes `call.json`: provenance
  (`commit`, `written_by_ci`, `ci`, `env_set` as four booleans), the
  sign-in's record, and per served answer the call record (`subject`
  `pharmadelta`, `issuer` `self`, `door_host` the hash, `request_id`
  from `apigw-requestid`, `called_at` UTC, `agent` `label-impact`,
  `agent_commit` `8cf0563`, `run_url`), the door's full reading, and
  `answer`: `table_row`, `clause_id` and the three answer fields of the
  door's `parsed`, or null when nothing parsed. Exit 0 when every call
  answered 200 with an observation and every record is complete; else 2
  and `call.json` says why. Nothing of the URL, the pool id, the client
  id, the password or the token is written.
- `src/m03/lift.py write --from <dir>`: by hand, from the downloaded
  artifact. Refuses a `call.json` whose `written_by_ci` is false or
  whose `ok` is false. Rebuilds `pages/api/answers.json` and
  `pages/detail.html`: `answer` verbatim from the call; `row` and
  `clause` copied from `data/` at its last commit only when the table
  holds the `table_row` and the clauses hold the `clause_id`, else null;
  `agent` and `call` the record; `door` the status, header, `stop_reason`,
  `parsed` and `text`; `scripted` false; no `PLANT`. The page shows an
  answer only with its row and its clause; otherwise "no row found" with
  the question, the call record, the `parsed` object and the agent's
  text, verbatim and labelled as the agent's (Unsure 26, `rulings/pr4.md`
  3). The page embeds the same object in its `id="answer"` block. The
  rebuild is deterministic and writes LF.

Construction, not evidence (P4): before the first push, `call` with no
environment wrote `ok` false, `written_by_ci` false, exit 2, and `write`
refused it. Three stub `call.json` files in the session's scratch
directory, `written_by_ci` set true by hand, in the three shapes the door
has given (an object with `table_row` null; null; an object naming
`lisinopril.8.1` and `201.57(c)(9)(i)`), rendered three pages: the gate
with no environment read each as called, page equal, `answers_uncalled`
`[]`, UNSCORABLE for the missing sign-in; `compare()` read the first
equal to run 41171470951's `parsed` and the second equal to run
41126878288's; a `</script>` planted in a stub's text came out as `<\/`
in the block. Two writes of the same stub were byte-identical. Not
committed.

### The lift call (CI run 41222218526, not the Measured cell)

The push of `e5f79ef` added `m03-lift.yml` and ran it:
[41222218526](https://github.com/andaro74/pharmadelta/actions/runs/41222218526),
artifact `m03-lift-e5f79ef8f33fe7b2d63f3bc9b08e31fcea584695`, its
`call.json`:

| Field | Value |
|---|---|
| `ok` | `true`: "every call answered 200 with an observation and every record is complete" |
| `written_by_ci` | `true`; `commit` `e5f79ef`, `dirty` false; `event` `push`, `ref` `refs/heads/m03-pr4` |
| `env_set` | all four true; the file grepped for `execute-api` and `us-west-2_`: no match |
| `sign_in` | `signed_in` true, status 200, `token_use` `access`, `token_username` `pharmadelta`, `expires_in` 3600, 574 ms |
| `calls[0].call` | `subject` `pharmadelta`, `issuer` `self`, `door_host` `sha256:21585a9a…d68139`, `request_id` `GHmo8jHQPHcEMNA=`, `called_at` `2026-10-31T16:58:32+00:00`, `agent` `label-impact`, `agent_commit` `8cf0563`, `run_url` the run above; `record_missing` `[]` |
| `calls[0].door` | status 200, request id in `apigw-requestid`; `stop_reason` `tool_use`; `parsed` null; `text` empty; `error` null; `refused` null; three calls of `find_label_row` with `section` the number `8.1`, each refused `8.1 is not one of ['bw', '5', '5.1', '6', '8.1']`; `latency_ms` 4819, 8879 ms wall; `usage` 5591 in, 279 out |
| `calls[0].answer` | `null` |

The same shape as the PR 2 run (41126878288). The agent gave no answer;
the record is complete. The lift serves g-001 as "no answer" with this
record (PR 1 "Equality"; Unsure 6, 23, 26).

### The lift

Commit `8aae03d`: the one change "The false state" named, written by
`lift.py write` from that artifact. In `pages/api/answers.json` the entry
`g-001` now carries `answer` null, `row` null, `clause` null, `agent`
(`label-impact`, `agentkeel-studio/label-impact`, `8cf0563`, agentkeel
m10), `call` the record above, `door` (200, `apigw-requestid`,
`tool_use`, `parsed` null, `text` empty), `scripted` false, and no
`PLANT` key; the file names `data_commit` `595dd68` and, under `lift`,
the run and the artifact it was written from. `pages/detail.html` shows
the question, "No row found" with why, the call record with `run_url`
as a link, and the same object in its `id="answer"` block; no scripted
banner, because nothing scripted remains (P8); no answer, because an
answer is shown only with its row and its clause. `git diff c7edf8f --
pages/` is the whole of both files. The `row` and `clause` copied at
`c7edf8f` are gone with the hand-written answer: the agent returned no
row, so none is copied in.

`8aae03d`'s message says the writer pins LF. Its diff did not hold that
change: the edit to `lift.py` had failed in the session without being
noticed, and the commit went ahead with the pages, which git stored LF
under `.gitattributes`. `6dd2fc2` holds the pin and says so (Unsure 33).
The committed pages are byte-identical to a rebuild from the artifact
with the pinned writer.

### What the gate on this PR can read

The gate compares against its own call (`rulings/pr2.md` 4), so the
run on this PR reads GREEN when the door parses nothing that day (null
equals null), RED with `answers_differing` `["g-001"]` when it parses an
object, and UNSCORABLE when the sign-in or the door fails. Any of the
three is a reading after the measurement and leaves the cell as it is.

### Observed (CI runs, 2026-10-31)

The first run on this PR,
[41222318273](https://github.com/andaro74/pharmadelta/actions/runs/41222318273),
on the merge ref `f09637c` (branch head `8aae03d`), artifact
`m03-gate-f09637ceb5b933a132adde13e981a75291922576`, its `result.json`:

| Field | Value |
|---|---|
| `verdict` | `GREEN`; `reason` "F3.1 does not hold: every served answer carries a call record as pharmadelta, every page answer is an API entry, and every served answer equals the door's answer on this run" |
| `answers_uncalled` | `[]`: `served[0].call_record` "a call record as pharmadelta, every field present" |
| `answers_disagreed` | `[]`: the page's one answer equals the API's entry |
| `answers_differing` | `[]`: `comparison` equal, "the served answer is null and the door parsed no answer" |
| `unreadable` | `[]` |
| `env_set` | all four true; grepped for `execute-api` and `us-west-2_`: no match |
| `sign_in` | `signed_in` true, status 200, `token_use` `access`, `token_username` `pharmadelta`, 278 ms |
| `door[0]` | status 200; `request_id` `GHm1jifhPHcEPDA=` in `apigw-requestid`; `stop_reason` `end_turn`; `parsed` null; two refused tool calls as before, then prose with no JSON object: the agent says it met a tool error, names the row it believes the table holds, and will not return an unverified row; `latency_ms` 6733, 7457 ms wall; `usage` 5591 in, 283 out |
| `written_by_ci` | `true`; `commit` `f09637c`, `dirty` false; exit 0; the `M03 gate` job passed, the first pass of this gate. `M00 gate` and `M02 gate` on the same head passed ([41222318310](https://github.com/andaro74/pharmadelta/actions/runs/41222318310), [41222318270](https://github.com/andaro74/pharmadelta/actions/runs/41222318270)). `M01 gate` is not required and reads as it does on `main` |

The second run, on `6dd2fc2` (the LF pin),
[41222395263](https://github.com/andaro74/pharmadelta/actions/runs/41222395263)
on the merge ref `63f4f31`: the same on every field above; `request_id`
`GHm9iiHXPHcEPRA=`, `end_turn`, `parsed` null, two refused tool calls,
497 ms sign-in, `latency_ms` 6104. The run on the close commit is named
under "After this PR" when read.

Both are readings after the measurement. GREEN here says: on those two
calls the agent again parsed nothing, so the served "no answer" equals
the door's. It does not say the agent answers the question; it does
not. The cell above is the `main` run on the plant and is not changed by
these runs. Four shapes in seven CI calls now: `tool_use` null
(41126878288, 41222218526), `end_turn` with an object whose `table_row`
is null (41171470951, 41221327681), `end_turn` prose and null
(41216016582, 41222318273, 41222395263). Same refusal every time
(Unsure 23, label-impact's).

### Rulings carried

| # | Ruled |
|---|---|
| PR 2's 10, PR 3's 5 | Product: the lift is carried by PR 4, this PR; the Measured cell takes the `main` run after #20 merged. Done as ruled. |
| PR 2's 7 (Unsure 10) | Engineering, Security: the lift writes the eight fields as fixed; the gate names the entry called. |
| PR 3's 2 (Unsure 24) | Product, Engineering: confirmed at PR 4 (`rulings/pr4.md` 20). |

### What this PR does not hold

- No change to `src/m03/gate.py`, `.github/workflows/m03.yml`,
  `gate.yml`, `m01.yml`, `m02.yml`, `pyproject.toml`, `uv.lock`, `data/`,
  `goldens/`, `src/baseline/` (P5), `src/gate/`, `src/ingest/`,
  `src/m01/`, SPEC/00, CLAUDE.md, the README, or anything under
  `milestones/M00/`, `M01/`, `M02/` or `adoption/`. No new dependency.
- No edit to the expected gate output written at open, to `rulings/pr1.md`,
  `pr2.md` or `pr3.md`.
- No value of the secret or a variable. Grep `execute-api`, `us-west-2_`
  and `amazonaws.com/` under `src/m03/`, `pages/` and
  `.github/workflows/`: the gate's host suffix and the Cognito endpoint
  as at #20, and nothing under `pages/`.
- No workflow with `contents: write`. Grep `permissions` under
  `.github/workflows/`: every file reads `contents: read`.
- No answer on a page without its row and its clause. The page shows
  none.
- No number on a page that is a result: the call record's time and id
  are the CI run's, linked; nothing else is new.
- No change to label-impact or to agentkeel. No tag until this PR's run
  on `main` is read.
- No fifth PR.

### What a reader can falsify

- `git diff main --stat` on this PR touches `.github/workflows/m03-lift.yml`,
  `src/m03/lift.py`, `pages/api/answers.json`, `pages/detail.html`,
  `milestones/README.md`, `milestones/M03/README.md` and
  `milestones/M03/rulings/pr4.md` only.
- `gh run download 41222218526`, then `uv run python -m src.m03.lift
  write --from <dir> --api <a> --page <p>`: the two files written equal
  `pages/api/answers.json` and `pages/detail.html` at this PR's head byte
  for byte.
- In `pages/api/answers.json`, `grep PLANT` matches nothing, `scripted`
  is false, `call` holds the eight fields with `subject` `pharmadelta`,
  and `call.run_url` opens run 41222218526, whose artifact's `call.json`
  holds the same `request_id` and `called_at`.
- `sha256sum` of the host of the variable `M03_DOOR_URL`, lower-cased,
  no newline, equals `call.door_host` less its `sha256:` prefix. Only a
  reader who holds the variable can do this; the page gives no host.
- The `main` run's artifact `m03-gate-0b8d2ec7598b61c30f861a3f2114c2a13e89ad71`
  holds `result.json` with `verdict: RED` and the three lists in the
  cell. Download it and read it; the ledger's cell is that file.
- The artifact on this PR's first run holds `verdict: GREEN`,
  `answers_uncalled: []`, `comparison.equal: true` on `g-001`.
- Grep `secrets.` and `vars.` in `.github/workflows/m03-lift.yml`: four
  matches, the four names, in one step's `env`.
- The page carries none of "validated", "compliant", "Part 11",
  "governed", "secure" or "proven", no brand name, and no scripted
  banner.

### After this PR

Tag `m03` on the merge commit, as `m00`, `m01` and `m02` were tagged,
after this PR's run on `main` is read with `gh run download`. That run's
verdict is recorded in the tag's message and in a comment on #22, not in
a commit: the milestone's four PRs are used and a fifth is a RED close
(Unsure 31). Whatever it reads, the cell stands. Row 4 is GREEN. The
milestone is closed, not reopened, by what the agent answers later.

Carried by name: Unsure 2 (GitHub Pages) to M04, the first milestone
that serves a page to a visitor; Unsure 6 and 23 (the agent's tool
refuses `section` as a number; the answer record RED at every deploy)
to label-impact, with the four shapes above; Unsure 16 (the gate as a
required check) with M02's 16 to the owner's settings, outside any
milestone; the deadlock finding and the refused construction call
(Unsure 20) to agentkeel, as PR 1's carried items say. Row 4's cell
closes on the call, not on the answer, as Unsure 6 asked at open: the
page says the agent gave no row.

## Unsure (PR 4)

Numbering continues from PR 3's. Each needs a seat's ruling. None
changes the measurement.

| # | Item | Seat |
|---|---|---|
| 30 | The ruling file names this PR as #22, the next number on this repository. **Ruled at PR 4** (`rulings/pr4.md` 13): #22. | Product |
| 31 | This PR's run on `main` after it merges is read before the tag is placed, and its verdict is written in the tag's message and in a comment on #22, not in the README: a commit after the merge would be a fifth PR, and a direct push to `main` is not the PR shape. The Measured cell is not touched by it. **Ruled at PR 4** (`rulings/pr4.md` 22): as stated. | Product |
| 32 | `m03-lift.yml` runs by hand and once on a push that adds or edits its own file on a branch other than `main`, because `workflow_dispatch` needs the file on the default branch and the lift's call had to be made on this branch. After this PR merges the push trigger still fires on a branch edit of the file, one call as `pharmadelta` per such push, under the agent's ceilings. Its artifact is kept 90 days, as the gates' are; after that the record survives as the page's copy and the run's log and summary. **Ruled at PR 4** (`rulings/pr4.md` 23): as built; the retention is the artifact's, the record is the page's. | Engineering, Security, Threshold Owner |
| 33 | The pages were written by hand on a Windows machine from the downloaded artifact. The first write produced CRLF files, which git stored LF under `.gitattributes`; `8aae03d`'s message claims the writer pins LF and its diff does not hold it; `6dd2fc2` holds the pin. The committed bytes equal a rebuild with the pinned writer. **Ruled at PR 4** (`rulings/pr4.md` 24): recorded; the pages stand; the message is not rewritten. | Engineering |

## Unsure (PR 3)

Numbering continues from PR 2's. Each needs a seat's ruling. None blocks
the measurement, which is in.

| # | Item | Seat |
|---|---|---|
| 24 | A served answer that is neither null nor an object, or whose `answer_fields` is not an object, is read as "could not be read" at the entry: not compared, named under `unreadable`, UNSCORABLE only when nothing is RED. The alternative, naming it under `answers_differing` (a served answer with no `table_row` differs from any door answer), would make a malformed served file RED. Proposed and built: unreadable, because F3.1 compares fields the entry does not have. **Ruled at PR 4** (`rulings/pr4.md` 20): confirmed as built. | Product, Engineering |
| 25 | Ledger row 4's "is shown as served" against the gate's reading: the gate names page answers the API does not serve or that differ from the API's entry (F3.1's third arm, PR 1 "The gate"), and does not name a served answer the page does not show. Confirm the row's words mean the gate's reading, or rule that every served answer must be shown, which is a gate change for the repair slot. **Ruled at PR 4** (`rulings/pr4.md` 21): the row's words mean the gate's reading; the gate is not changed. | Product |
| 26 | The door's answer to g-001 differs between the two CI runs: run 41126878288 ended at `tool_use` with `parsed` null after three refused tool calls; run 41171470951 ended at `end_turn` with `parsed` `{"table_row": null, "clause_id": "21 CFR 201.57(c)(9)(i)", "impacted": false, "owed": "none", "escalate": false}` after two. Under ruling 4 the comparison is against the run's own call, so after the lift a served answer equals the door's only on a run whose call returns the same shape; the Measured cell is read from the `main` run after PR 4 merges and may name g-001 under `answers_differing` by the day. Also: the parsed object's `table_row` is null and its `clause_id` carries a `21 CFR ` prefix `data/clauses.json`'s ids do not, so an answer the lift serves from such a call has no row to show and a clause id the table does not hold; CLAUDE.md says a page never shows an answer without its row and its clause. PR 1's "Equality" covered `parsed` null ("no answer" with the call record), not this shape. Proposed for PR 4: the lift serves what its call returned, verbatim, with `table_row` null shown as "no row found" beside the question and the call record and no row or clause copied in; the cell says what the `main` run read. The cause is label-impact's (Unsure 23). **Ruled at PR 4** (`rulings/pr4.md` 3): as proposed; the lift served g-001 as "no answer" with its record, the call having parsed nothing; both PR runs read GREEN against a null of their own. | Product, Tool Owner, Data Owner |
| 27 | `door_host` (Unsure 12, Security, open): the gate names an answer uncalled when `door_host` is missing or empty (ruling 7). A ruling of "not written" needs a gate change, and this PR is the milestone's repair slot. Security is asked to rule Unsure 12 before PR 4 opens: the host, a hash of it (fits the gate as it stands), or "not written" (does not). This PR changes nothing on it unruled. **Ruled at PR 4** (`rulings/pr4.md` 1): a hash, before the lift. | Security |
| 28 | How the lift's call record gets from a CI run into a commit is still undecided ("After this PR goes RED"). PR 4 proposes the smallest path and states it under Unsure for Engineering and Security before building it. Named here so PR 4's body has the item. **Ruled at PR 4** (`rulings/pr4.md` 2): the artifact path, built. | Engineering, Security |
| 29 | The ruling file names this PR as #21, the next number on this repository. **Ruled at PR 4** (`rulings/pr4.md` 13): #21. | Product |

## Unsure (PR 2)

Numbering continues from PR 1's. Each needs a seat's ruling. None blocks
the measurement.

| # | Item | Seat |
|---|---|---|
| 11 | The uncalled answer's question is asked through the door and its reading recorded, though it decides nothing on the plant: one call per served answer per run whatever its record, so the Measured cell carries what the agent said on the day (PR 1, "The gate"). The alternative, asking only called answers, spends nothing on the plant and records nothing of the agent at PR 2. **Ruled at PR 4** (`rulings/pr4.md` 9): as built; the readings on the plant gave the shapes Unsure 26 records. | Threshold Owner, Product |
| 12 | `door_host` in the call record is the door URL's host, a repository variable's value; writing it into `pages/api/answers.json` at the lift commits that value, which this PR's gate takes care never to write. Whether the lift writes the host, a hash of it, or names the agent and the request id only. **Ruled at PR 4** (`rulings/pr4.md` 1): the SHA-256 of the host, never the host. | Security |
| 13 | The request id header: `apigw-requestid`, confirmed on a refused call at construction (401). The CI run on this PR reads it on an admitted call; the gate records the header name it found and every header name the door returned. **Ruled at PR 2** (`rulings/pr2.md` 10): `apigw-requestid` on the admitted call too, `GE2QwjpovHcESyQ=`, the only request-id header the door returned. | Engineering |
| 14 | An API that serves no answer reads UNSCORABLE, not GREEN: "every served answer carries a call record" is true of none, and the claim says the API serves answers. **Ruled at PR 4** (`rulings/pr4.md` 10): confirmed. | Product |
| 15 | "Byte for byte" (PR 1, "The gate") is read as equality of the parsed JSON values in canonical form, because the page's block and the API's entry are pretty-printed at different depths. A whitespace-only difference passes; a value difference does not. **Ruled at PR 4** (`rulings/pr4.md` 11): confirmed. | Engineering, Tool Owner |
| 16 | Whether `M03 gate` is made a required check on `main`, as M02's Unsure 16 asked for its gate. Not changed here. **Carried at PR 4** (`rulings/pr4.md` 12): not changed; with M02's 16, the owner's setting, outside any milestone. | Security, Product |
| 17 | The ruling file names this PR as #20, the next number on this repository. **Ruled at PR 4** (`rulings/pr4.md` 13): #20. | Product |
| 18 | The result records two claims of the access token, `token_use` and `username`, read from its payload without verification, and the pool id's region prefix. Whether recording any claim of the token, or any part of the pool id, is allowed; the token itself is never written. **Ruled at PR 4** (`rulings/pr4.md` 14): allowed as built. | Security |
| 19 | A pull request from a fork gets no secret and reads UNSCORABLE unless an answer is uncalled or disagreed, and its job fails either way. Whether that is the wanted reading for an outside contribution. **Ruled at PR 4** (`rulings/pr4.md` 15): the wanted reading. | Security, Product |
| 20 | Construction touched the door once, with no token, to read its headers. The call left a refused record with no identity in the security account's log. Whether a construction run may call the door at all, and whether the refused record is owed a note in agentkeel. **Ruled at PR 4** (`rulings/pr4.md` 16): the one call stands; no construction call touches the door from here on; the refused record is named to agentkeel in the carried items. | Security |
| 21 | The door call's timeout is 90 seconds here; the proxy invokes the runtime with 28 and the HTTP API's integration limit is 30 (row P item 4). A call that outlives the proxy reads as the door's status (a 5xx), not as a client timeout. **Ruled at PR 4** (`rulings/pr4.md` 17): as built. | Engineering |
| 22 | label-impact's runtime answers 200 with `{"error": ...}` on a failed model call and 403 with `{"refused": ...}` on a chain refusal (`server.py`). The gate records either and does not compare, so a called answer whose call failed that way reads UNSCORABLE, not differing. **Ruled at PR 4** (`rulings/pr4.md` 18): confirmed. | Tool Owner, Engineering |
| 23 | The deployed agent answers g-001 with no `parsed` object because its tool refuses the model's argument: `find_label_row` was called three times with `section` as the number `8.1` and answered `8.1 is not one of ['bw', '5', '5.1', '6', '8.1']` each time (Observed, `door[0].tool_calls`). The cause of the RED answer record at both deploys (PR 1, carried items). label-impact's to repair, in its own repository; nothing here changes. What row 4's cell says if the lift serves a call record with no answer is Unsure 6's. **Read again at PR 3** (run 41171470951): the same refusal twice, then the model stopped and answered `table_row` null with a `21 CFR `-prefixed `clause_id`; the shape varies by run (Unsure 26). Still label-impact's. **Carried at PR 4** (`rulings/pr4.md` 19) to label-impact by name, with the four shapes; row 4 closes on the call. | Tool Owner, Engineering (label-impact); Product |

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant.

| # | Item | Seat |
|---|---|---|
| 1 | What "a public API" is at M03: a read API, a public JSON file of answers each produced by a CI call as `pharmadelta` with its record (this file's assumption), or a live path that forwards a visitor's question on request, which needs a host that runs code and holds the credential, and exposes the agent's daily budget to anyone. Proposed: the read API at M03; a live path is a later row's or a platform item. **Ruled at PR 4** (`rulings/pr4.md` 7): the read API is the claim at M03; a live path is a later row's or a platform item. | Product, Security |
| 2 | Where the pages and the API are served. GitHub Pages is not enabled on this repository (404, 2026-10-25); enabling it, and from which branch and directory, is a repository setting. Until it is, "public" means readable in the repository. `/site` is ignored by `.gitignore` line 170, so the directory is `pages/`. **Carried at PR 4** (`rulings/pr4.md` 7) to M04 by name; at M03 "public" means readable in the repository. | Product, Security |
| 3 | The secret and the variables PR 2 reads: `M03_DOOR_PASSWORD` as the one secret; the door URL, the pool id and the callers client id as repository variables (none is a secret; the URL is public and the ids are not credentials); who sets them and under whose record. Names proposed under "Carried to PR 2". **Ruled at PR 2** (`rulings/pr2.md` 2): the names as proposed. The owner set the secret `M03_DOOR_PASSWORD` and the variables `M03_DOOR_URL`, `M03_DOOR_POOL_ID` and `M03_DOOR_CALLERS_CLIENT_ID` in this repository's settings before PR 2 (names read with `gh secret list` and `gh variable list` on 2026-10-30; values never read into a file). The workflow reads them from its environment and the gate writes none of them; `env_set` records only which were present. | Security |
| 4 | The verdict's shape: RED on an uncalled served answer needs no door read, so the plant's RED does not depend on the pool or the door that day; UNSCORABLE only when nothing is RED and a read failed. M02's gate read UNSCORABLE whenever a source could not be read; this differs, because F3.1's first arm is a read of the served files alone. **Ruled at PR 2** (`rulings/pr2.md` 3): as proposed and as built. RED on an uncalled or disagreed answer is a read of the served files alone, before any sign-in; UNSCORABLE only when nothing is RED and a reading failed. The construction run read RED with no door. | Product, Engineering |
| 5 | What "equals the door's answer" compares: `table_row`, `clause_id` and `answer_fields` of the door's `parsed` object on the gate's run. The agent runs at temperature 0, but the deploys show it does not always parse to an answer; a served answer whose call returned none is shown as "no answer" with its call record. Whether the comparison is against the run's own call (proposed) or against the call that produced the served answer, which only the security account's records could confirm. **Ruled at PR 2** (`rulings/pr2.md` 4): the comparison is against the run's own call, on `table_row`, `clause_id` and the three `answer_fields` as the door's `parsed` holds them, flat (the deploys' shape) or under an `answer_fields` key. A served answer of null equals a `parsed` of null. The originating call is matched only by its `request_id` in the security account, which this repository cannot read (Unsure 10). | Product, Data Owner, Threshold Owner |
| 6 | The deployed agent's answer record is RED at both deploys and `g-001` gave no parsed answer through the door (carried items). Whether M03 proceeds to PR 2 with the agent as it stands, and what row 4's cell says if the lift serves a call record with no answer. Not this repository's to fix. **Ruled at PR 4** (`rulings/pr4.md` 3): row 4 closes on the call; the page says the agent gave no row; the fix is label-impact's. | Engineering, Tool Owner (label-impact); Product |
| 7 | Numbers on the page: the row's strengths, dates and application numbers and the clause's citation, dates and source note are the row's and the clause's own data, each with its source, not a measured result. Whether SPEC/00 §11's "a number on a page comes from a CI-written result" reaches a row's data. **Ruled at PR 4** (`rulings/pr4.md` 8): the row's and the clause's data are not measured numbers; the call record's time and id are the CI run's, linked. | Product |
| 8 | The ruling file names this PR as #19, the next number on this repository. **Ruled at PR 2** (`rulings/pr2.md` 5): PR 1 was #19. | Product |
| 9 | Cost and ceilings: one call per served answer per gate run on every pull request and push to `main`, under the agent's `concurrency` 2, `rps_per_edge` 1 and `daily_usd` 10; the spend is the agent's, not this repository's. Whether the gate runs on every pull request or on `main` and by hand only. **Ruled at PR 2** (`rulings/pr2.md` 6): the gate runs on every pull request, every push to `main` and by hand, one call per served answer per run, called or not (Unsure 11), under the agent's ceilings; the spend is the agent's. Narrowing the triggers is a one-line change for PR 3 if the Threshold Owner asks. | Threshold Owner, Security |
| 10 | The call record's fields on a served answer and which the gate can verify from here: `run_url` is a run of this repository's workflow, readable through GitHub's API; the `request_id` can be matched to the door's access log only in the security account, which agentkeel's observer reads, not this repository. **Ruled at PR 2** (`rulings/pr2.md` 7): the fields are fixed as `subject`, `issuer`, `door_host`, `request_id`, `called_at`, `agent`, `agent_commit`, `run_url`; the gate names an answer uncalled when any is missing or empty or `subject` is not `pharmadelta`. From here `run_url` is readable through GitHub's API and `request_id` is not; `door_host` is Unsure 12. | Engineering, Security |
