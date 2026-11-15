# M07: A second agent is created on a stopwatch

Row 8 of the ledger (`milestones/README.md`), the last open row. The
claim text is SPEC/00 §8's, word for word. Needs M01, which closed at
tag `m01` on `c60599e` with row 1 GREEN. One to two days (SPEC/00 §8).
One claim, one planted failure, one measured verdict (P3). Cap four PRs
(ADR-0001 U9). The second agent is built in `agentkeel-studio` from the
same template as the first; the row is measured here (SPEC/00 §3).

M07 repeats M01 with a clock running. M01 created `label-impact` and
did not time it. M07 creates a second agent and serves one number: how
long it took, read by CI from GitHub's records.

## Ledger row

Written at PR 1 open. The row in `milestones/README.md` is the ledger's;
this is the same row with the open detail.

| Field | Row 8 |
|---|---|
| Claim | A second agent is created on a stopwatch |
| Falsifiers | F7.1 a time this repository serves for its second agent was not read by this repository's CI from GitHub's own records of the agent's creation and deploy: it carries no clock record; or the repository the record names does not exist or was not created from `agentkeel-studio/agent-template`; or the record's start is not that repository's `created_at`; or its stop is not the `completed_at` of a `deploy-agent` job of agentkeel's `deploy.yml` that names the agent and the merge commit of its first pull request and concluded `success`; or `elapsed_seconds` is not the stop less the start; or a page shows a time for the second agent that the served file does not serve. |
| Seeded commit | `c07fbe5` on `m07-pr1`: `pages/api/second-agent.json`, the time pharmadelta serves for its second agent, one entry `a-002`: name `record-keep-desk`, its job, repository `agentkeel-studio/record-keep-desk` with `repository_exists` false (GitHub answered 404 on 2026-11-15 UTC), `elapsed_seconds` `3600` typed by hand, `clock` null (no `created_at`, no deploy job, no run), `scripted` true, a `PLANT` key beside them. No page shows the number. No second repository exists, nothing was created or deployed, and nothing in this repository reads a clock. |
| Expected gate output | PR 2's gate, in CI, reads every time the served file serves and names each that carries no clock record (`times_unrecorded`), and each time a page shows for the second agent that the file does not serve or serves differently (`times_disagreed`); then, for each time with a clock record, reads from GitHub's API the repository the record names (its `created_at` and its template), its first pull request's merge commit, and the `deploy-agent` job the record names by run and job id, and names each whose record differs from what GitHub answers or whose `elapsed_seconds` is not the stop less the start (`times_differing`). It writes a `result.json` that is RED when any time is unrecorded, disagreed or differing, naming each; GREEN only when every served time carries a clock record that equals GitHub's records, is shown as served, and the job concluded `success`; UNSCORABLE when nothing is RED and the served file, a page or GitHub's API could not be read. On `c07fbe5`: RED, `times_unrecorded` `["a-002"]`, `times_disagreed` `[]`, `times_differing` `[]`. The Measured cell cites the `main` run after PR 2 merges (M01 Unsure 23, ruled at M02 PR 1). |
| Measured | |
| PRs used / cap | 3 / 4 |
| State | OPEN |

## The false state (P1, P2)

The claim says a second agent was created and that a stopwatch timed
it. It is false when the repository serves a time for that agent that
no clock produced. That is what `c07fbe5` commits.

`pages/api/second-agent.json` is what the site will serve about the
second agent: a list of agents, in the shape of the other served files,
with `clock` where `pages/api/answers.json` has `call`. It holds one
entry, `a-002`. The name is `record-keep-desk` and the job is Product's
(ruling 2). `repository` names where it will be built and
`repository_exists` is false: `GET /repos/agentkeel-studio/record-keep-desk`
answered 404 on 2026-11-15 UTC. `elapsed_seconds` is `3600`, a round
number typed by hand. `clock` is null: no `created_at`, no deploy job,
no run that read either. `scripted` is true and a `PLANT` key says what
the entry is.

No HTML page shows the number. Product asked for the false state to be
"a time written by hand"; SPEC/00 §11 says a number on a page comes
from a CI-written result and links to it, and CLAUDE.md says never
otherwise. So the hand-typed time is planted in the served file alone,
labelled, and the one line on the site is written at the lift from the
CI record (ruling 4; Unsure 1). The number appears in the ledger's
seeded-commit cell and in this file as the plant's value, named as
typed by hand each time.

Why this plant: a time with a name beside it and nothing behind it is
the thing the claim rules out, as a scripted answer was M03's and a
hand-set `signed` was M06's. A gate that checks the file holds a number
passes the plant. A gate that demands the two GitHub records and
recomputes the difference does not. The plant tests which one PR 2
builds. Both halves of the claim are false in one entry named in one
list (P3): no agent was created, and no clock ran.

Lifting the plant is the stopwatch run, then a lift in CI: the second
repository created from the template, its first pull request merged
under the platform's check, the platform's deploy; then a workflow of
this repository that reads the two records from GitHub's API and writes
the entry with its `clock`, `scripted` false and no `PLANT` key, and the
one line on the site. Which PR carries the lift is decided after PR 2
goes RED, not here.

## The clock (Product, ruling 3)

| | Record | Whose |
|---|---|---|
| Start | `created_at` of `agentkeel-studio/record-keep-desk` | GitHub's, written when the owner creates the repository from the template |
| Stop | `completed_at` of the `deploy-agent` job of agentkeel's `deploy.yml` whose name carries `record-keep-desk` and the merge commit of the agent's first pull request, conclusion `success` | GitHub's, written when the platform's job ends |

Neither is a time a person types. This repository's CI reads both and
subtracts.

The stop is narrower than agentkeel's own clock. agentkeel SPEC/06 §1
stops at the last of four records: merged, deployed, answered, listed
in the registry. M07 stops at deployed. The `deploy-agent` job asks the
agent its goldens before it ends, so "answered" falls inside it; the
registry row is unread from this repository (M01 Unsure 12). agentkeel's
one timed run (its M07, 2026-10-03, 3,615 s by its own quickstart) was a
second developer with write access and no admin, to the last of four
records. M07's time here is the owner's, with an assistant writing the
files, to the deploy. The two numbers do not compare one to one, and
the line on the site says whose time it is (Unsure 4).

A repository's `created_at` cannot be reset. A run cannot be restarted;
a second try is a new repository with a new name, and the first try
stays on record (agentkeel SPEC/06, finding 4; Unsure 7).

## The second agent (Product, ruling 2)

`record-keep-desk`. For a fictional bank with no name: a document type
is due for disposal; may it be destroyed yet, and who signs? Every
answer cites one row of the bank's retention table (document type by
years kept) and one clause of the bank's own retention policy. The trap
Product named: a document past its years but under a legal-hold flag in
the row.

- It is a table-and-clause agent, the only kind the template makes
  (SPEC/00 §6): one tool that returns a row and decides nothing.
- It cites no real regulation. The clauses are the fictional bank's own
  policy, invented and labelled so. P7 has no CFR or Federal Register
  citation to check, by design: a source check would run on the clock.
- It answers no treatment question and has nothing to do with drug
  labeling. It gives no legal or financial advice: it says what the
  bank's policy requires, never what a person should do (Unsure 9).
- It names no real bank and no brand.
- Its table, clauses, goldens, tool and prompt do not exist. They are
  written in its own repository, after that repository is created
  (Unsure 2). None is written here, in this PR or any other.

## Attention plan

For the owner, who is not at the keyboard the whole time. Three levels:
AWAY (the session works alone), CHECK-IN (answer a question or merge; a
few minutes; no hurry), PRESENT (stay and act without a break).

| Stage | What the owner does by hand | Level | How long, and based on what | Must be true first |
|---|---|---|---|---|
| PR 1, plant | Names the agent, says "go"; later merges with a merge commit | CHECK-IN, AWAY while the session writes, CHECK-IN to merge | 5 min; about 40 min of the session's work (guess); 2 min to merge | The name, the job and "go" (given 2026-11-14 local) |
| PR 2, the gate (new session) | Reads the RED run, rules which PR carries the lift, merges | AWAY, then CHECK-IN | About 60 min of the session's work (guess); the CI run 1 to 2 min (guess); 5 min for the owner | PR 1 merged. No new secret if the gate reads only public records (Unsure 5) |
| PR 3, repair, if the cold review of PR 2 finds anything | Merges | AWAY, then CHECK-IN | 30 to 60 min of the session's work (guess); 2 min for the owner | PR 2 merged. Skipped if the review finds nothing |
| The stopwatch run | Creates the repository from the template; adds it to the platform App's installation; merges the agent's pull request when the check passes | PRESENT | Keep 2 hours free. Estimate 45 to 75 min, from the records below | PR 2 merged, and PR 3 if there is one; Unsure 2, 3 and 7 ruled; the go / no-go checklist answered "go" |
| PR 4, close | Merges; places tag `m07` with two commands | AWAY, then CHECK-IN | About 45 min of the session's work (guess); 5 min for the owner | The run done; the `deploy-agent` job concluded `success` |

Product's list put the stopwatch run before PR 3. This plan puts PR 3
first, so the lift is read by a repaired gate. Product's to change.

What the stopwatch estimate rests on:

| Record | Time | Source |
|---|---|---|
| M01, repository created to the first platform check posted | 19 min 45 s, waiting on the schedule | `milestones/M01/README.md`: `16:54:39Z` to `17:14:24Z` |
| M01, lift pushed to `deploy-agent` concluded | 19 min 42 s, with the check started by hand twice and the deploy once | the same file: `04:24:47Z` to `04:44:29Z` |
| M01, the `deploy-agent` job alone | 6 min 37 s | the same file: `04:37:52Z` to `04:44:29Z` |
| agentkeel's own timed run | 3,615 s | agentkeel `docs/developer/quickstart.md` |
| Writing the agent's files on the clock | 15 to 30 min | a guess |

Rules for the run, from the owner's start prompt:

- The clock starts only on the owner's "go". The session never creates
  the repository, and never takes a step that starts the clock, on its
  own.
- Before the PRESENT stretch the session stops and gives a go / no-go
  checklist: every hand step in order, one action each, what to click
  and what to expect; everything needed in hand first; the exact moment
  the clock starts and stops; what an interruption does to the
  measurement; how long to keep free. Nothing starts until the owner
  answers "go". On "wait" the session stops and says how to resume.
- Each time control goes back to the owner the message starts
  "NEEDS YOU: AWAY / CHECK-IN / PRESENT, about N minutes".
- Anything unplanned that needs the owner during the stretch is said at
  once, with whether the clock is still running, and recorded under
  Unsure.

The checklist will re-read, on the day: that the template's guardrail
pin equals the platform's, that the template still ships `callers`, and
that agentkeel's check and deploy schedules ran in the last hour.

## The platform, as read at open (construction, not evidence, P4)

Read 2026-11-15 UTC (2026-11-14 local). Nothing here is designed in
this repository; what needs the platform is flagged.

| What | Read |
|---|---|
| The template | `agentkeel-studio/agent-template` at `be4e07f`, made from agentkeel `20ac721` (tag `m10`). `manifest.yaml` ships `callers: []`, guardrail version `'6'`, `platform_version: m10`, seven seats null |
| The platform's pin | agentkeel `main` at `79c7715`, `agents/refagent/manifest.yaml`: guardrail version `"6"`, the same id as the template's. `main` is 18 commits past `m10`; the files changed are the README, `docs/assets/`, `evals/history/`, `infra/bootstrap/`, `milestones/maintenance/` and one test. Nothing under `src/validate/`, `scripts/` or `.github/workflows/` |
| agentkeel issue #60 | Open. A major upgrade that adds a field the agent's seat must fill, and moves the guardrail pin, cannot be fixed from the agent's `main`. It needs an upgrade. A repository created from the template today is at the platform's version with the platform's pin and `callers` present, so it meets none. **As read, #60 does not affect creating the second agent.** If the platform's version or pin moves before the run, it does, and the run waits on the platform |
| The platform App's installation | `agentkeel-platform` on `agentkeel-studio`: `repository_selection` `selected`. A new repository is not covered until the owner adds it by hand; until then the platform check posts on no repository in the organisation (M01 Unsure 8, still true). A hand step inside the run. agentkeel's quickstart §0 now names it. Platform item, flagged |
| How the platform finds an agent | `scripts/platform_check.py`: every repository in the organisation that is not archived and not the template. A new agent needs no change in agentkeel |
| The schedules | `platform-check.yml` every 5 minutes, `deploy.yml` every 10; both `active`; the last six runs of each, to `2026-11-15T00:10Z`, concluded `success`. Both take `workflow_dispatch` |
| agentkeel's state | Building stopped at `m10` (`milestones/maintenance/README.md`). Four agents were retired and their stacks deleted on 2026-11-06 and 2026-11-07; `agentkeel-refagent` and `agentkeel-label-impact` stand. The last first-time deploy of a new agent was `festival-desk`, 2026-10-12 and 13. That a first deploy still works after the maintenance changes is not read; the run reads it |
| Its findings that touch a new agent | Maintenance finding 2: the upgrade moves an own-rules agent's pin to refagent's. It bears on an agent with a `rules/` folder; proposed here that `record-keep-desk` has none (Unsure 9) |
| `agentkeel-studio/record-keep-desk` | Does not exist: 404 |
| The organisation's repositories | `agent-template`, `owner-check`, `window-check`, `drill-agent`, `label-impact`, `festival-desk`. "Second" is pharmadelta's second; the platform has deployed others |

## Open detail (PR 1, 2026-11-15 UTC)

### What this PR holds

- Row 8 of the ledger: falsifier, seeded commit, expected gate output,
  PRs used 1 / 4.
- `pages/api/second-agent.json`, the plant.
- This file, with the attention plan.
- `rulings/pr1.md`.

Nothing else. No gate, no workflow, no reader, no test (P2). No second
repository, no agent file, no deploy. No edit to `index.html`, any
file under `pages/` but the new one, `src/` (`src/baseline/` is frozen
at `m00`, P5), `goldens/`, `data/`, `.github/workflows/`, SPEC/00,
CLAUDE.md, the README, `docs/`, or anything under `milestones/M00/` to
`milestones/M06/` or `milestones/adoption/`.

### This repository, as read at open (construction, not evidence, P4)

| What | Read |
|---|---|
| `main` | `c2d45c3`, the merge commit of #46. PRs #39 to #46 were outside any cap; their rulings are in `milestones/adoption/rulings/`. No open pull request |
| The ledger | rows 0, 1, 4, 5, 6, 7 and P GREEN; row 2 RED with its finding; row 8 OPEN at 0 / 4 before this PR |
| The served files | `pages/api/answers.json`, `baseline.json`, `break-it.json`, `sign-off.json`. The four gates that read them (`src/m03/` to `src/m06/`) read their own files by path; grep `second-agent` and `record-keep` under `src/`, `.github/`, `pages/` and `index.html` before this PR: no match |
| `m01.yml` | runs on a pull request only when `src/m01/**` or the workflow changes; not on this PR |
| The evidence package | signed before PRs #39 to #46. Rebuilt and signed again after M07 closes, not during it |
| The README | its comparison table says row 8 is not yet measured. Updated when M07 closes, not here |

### What this PR does not hold

- No gate. That is PR 2's, and it is carried below.
- No lift and no stopwatch run. The repository is not created.
- No number on a page.
- No design of anything the platform owns.

### What a reader can falsify

- `pages/api/second-agent.json` at `c07fbe5` carries `elapsed_seconds`
  `3600`, `clock` null, `scripted` true and a `PLANT` key. Open the
  commit.
- `agentkeel-studio/record-keep-desk` does not exist: open the URL.
- No HTML file in this repository names the second agent or shows its
  time: grep `record-keep` and `second-agent` in `index.html` and
  `pages/*.html`, no match.
- Nothing in this repository reads the file: grep the same two words
  under `src/` and `.github/`, no match.
- `git diff main --stat` on this PR touches `pages/api/second-agent.json`,
  `milestones/README.md`, `milestones/M07/README.md` and
  `milestones/M07/rulings/pr1.md` only.
- The template's pin and the platform's pin are both version 6: read
  `manifest.yaml` in `agentkeel-studio/agent-template` at `be4e07f` and
  `agents/refagent/manifest.yaml` in `andaro74/agentkeel` at `79c7715`.

### Expected CI on this PR

No M07 gate exists, so nothing judges row 8. The gates that run on a
pull request (`gate`, `m02` to `m06`) read their own files, none of
which this PR changes; each is expected to read as it does on `main`.
The run links go in the PR body once read. A local run is not evidence
(P4) and none was made.

### Carried to PR 2

- The gate: `src/m07/gate.py` and `.github/workflows/m07.yml`, reading
  the served file and the pages, then GitHub's API for each clock
  record, and writing `result.json` as the artifact `m07-gate-<sha>` as
  the row's expected output says. RED on `c07fbe5`, naming `a-002` under
  `times_unrecorded`.
- It reads the deploy job by the run id and job id the clock record
  names, not from a window of recent runs: agentkeel's deploy runs every
  ten minutes, and M01's reader lost sight of a run within a day (M01
  Unsure 15; Unsure 10 here).
- Which page the gate reads for the line (Unsure 6), and whether it
  reads seats (Unsure 5).
- What the clock record's fields are. Proposed: `repository`,
  `repository_id`, `template`, `created_at`, `pull_request`,
  `merge_commit`, `deploy_run`, `deploy_job`, `completed_at`,
  `conclusion`, and the run and artifact of the lift that read them.

## Open detail (PR 2, 2026-11-15 UTC)

PR 2 is the measure. It adds the gate that reads the plant and nothing
that lifts it. `pages/api/second-agent.json` serves one time, `3600`
seconds typed by hand, with `clock` null at the head this PR measures.
M07 is measured here.

### The owner's rulings on PR 1's Unsure, as given

The start prompt for this PR listed Unsure 1, 2, 3, 5, 6 and 7 for
Product and left all six blank. Each stands at its PR 1 proposal and
stays open. PR 2 builds on two of them:

| # | Proposal used | Built on here |
|---|---|---|
| 1 | a served JSON file is not a page | no; the served file is not edited |
| 2 | nothing is drafted before `created_at` | no; before the run |
| 3 | the check and the deploy may be started by hand, each recorded | no; before the run |
| 5 | the gate reads public records only, with `GITHUB_TOKEN`, no secret | yes |
| 6 | the one line goes on `index.html` | yes; the gate reads `index.html` and every `pages/*.html`, so a ruling for another page changes no code |
| 7 | the first attempt stays the measurement | no; before the run |

If 5 is ruled the other way, the gate gains a seat read and the
workflow a secret, in PR 3. Items 2, 3 and 7 must still be ruled before
the stopwatch run.

### What this PR holds

- `src/m07/gate.py`, the gate. Python 3.14, the standard library only;
  `pyproject.toml` and `uv.lock` are unchanged. Nothing is imported from
  `src/m01/` to `src/m06/`. In order:
  1. Reads `pages/api/second-agent.json` (the `agents` list) and the
     JSON in each `<script type="application/json"
     id="second-agent-<id>">` block of `index.html` and every
     `pages/*.html`.
  2. `times_unrecorded`: every served entry that serves a time
     (`elapsed_seconds` is not null) whose `clock` is null, is not an
     object, lacks a field of the clock record (below), holds it empty,
     or holds it in the wrong form. A read of the served file; no
     network.
  3. `times_disagreed`: every page block whose `id` the file does not
     serve, whose block is not named `second-agent-<its id>`, or that is
     not equal to the file's entry of that `id` as parsed JSON in
     canonical form. A page with no block shows no time.
  4. For each time that carries a clock record, and for no other, the
     read-back from GitHub's API ("The read-back, as built").
  5. `times_differing`: every such time with a difference. A read that
     could not be made is `unreadable` and decides nothing.
  6. Writes `result.json` and exits 0 GREEN, 1 RED, 2 UNSCORABLE.
- `.github/workflows/m07.yml`: on every pull request, every push to
  `main` and by hand. A default checkout (the gate asks git nothing but
  its own head), `uv sync --locked`, the artifact directory, the gate
  with `GITHUB_TOKEN` in its `env` and nothing else; a step that greps
  the result directory for a token's prefix and fails on a match; then
  the artifact `m07-gate-<sha>` holding `result.json`, 90 days, uploaded
  only when the grep step passed. `permissions` is `contents: read`. The
  job fails on anything but GREEN. The other ten workflows are
  unchanged.
- `result.json` records `verdict`, `times_unrecorded`,
  `times_disagreed`, `times_differing`, `unreadable`, `commit`, `dirty`,
  `written_by_ci`, `ci`, the API base, the clock record's fields, how
  the clock is read (`clock_reading`, with `seats_read` false and
  `registry_read` false), whether the environment held the token
  (`env_set`, a boolean), per served entry its record check, page
  equality and read-back (`served`), each page read and its blocks
  (`pages`) and every API read by path and status (`api_reads`). No
  token.
- `rulings/pr2.md`, and "PRs used / cap" set to 2 / 4 here and in the
  ledger.

### The clock record's fields (fixed here; the lift writes them)

A field present and empty is missing.

| Field | Form the gate requires | Read back against |
|---|---|---|
| `repository` | `owner/name` | the entry's `repository`; `full_name` of `GET /repos/<repository>` |
| `repository_id` | a positive whole number | the repository's `id`; the second value in the job's name |
| `template` | `owner/name` | `agentkeel-studio/agent-template`, and the repository's `template_repository.full_name` |
| `created_at` | a time with an offset | the repository's `created_at`, as an instant |
| `pull_request` | a positive whole number | the `number` of the repository's first pull request by creation time |
| `merge_commit` | 40 hex digits | that pull request's `merge_commit_sha`, when it is merged; the third value in the job's name |
| `deploy_run` | a positive whole number | the job's `run_id`; the run's `path`, which must be `.github/workflows/deploy.yml` |
| `deploy_job` | a positive whole number | `GET /repos/andaro74/agentkeel/actions/jobs/<deploy_job>` |
| `completed_at` | a time with an offset | the job's `completed_at`, as an instant |
| `conclusion` | a word | `success`, and the job's `conclusion` |
| `read_by` | `run_url`, a run of this repository on github.com; `artifact`, a name | nothing; form only (Unsure 22) |

`elapsed_seconds`, on the entry, must be a whole number equal to
`completed_at` less `created_at`, both in the record and as GitHub
answers.

### The read-back, as built

Nothing here runs on the plant. Four GETs per time.

| Read | Decides |
|---|---|
| `GET /repos/<clock.repository>` | differing when GitHub answers 404 (the repository does not exist, or is not public: Unsure 19), names it otherwise, holds another id, was created from another template or none, or its `created_at` is not the record's; unreadable on any other status |
| `GET /repos/<clock.repository>/pulls?state=all&sort=created&direction=asc&per_page=1` | differing when there is no pull request, the first is not the record's number, is not merged, or its merge commit is not the record's (Unsure 23); not asked of a repository that answered 404 |
| `GET /repos/andaro74/agentkeel/actions/jobs/<clock.deploy_job>` | differing when the job does not exist, belongs to another run, is not a `deploy-agent` job, its name does not carry the repository, its id and the merge commit, it did not conclude `success`, or its `completed_at` is not the record's |
| `GET /repos/andaro74/agentkeel/actions/runs/<clock.deploy_run>` | differing when the run does not exist or is not a run of `deploy.yml` |

The gate follows no redirect, so the token goes to the API host alone;
a 301 reads `unreadable`.

**The job's name is cut (found here).** `deploy-agent` is a matrix job,
so GitHub names each leg from the matrix row: `deploy-agent
(<repository>, <repository_id>, <commit>, <name>, <rollout>)`. GitHub
cuts the name at 97 characters and adds `...`. On label-impact's deploy
job 114389865133 the name ends right after the 40-digit commit; the
agent's bare name, the fourth value, is not in it. `agentkeel-studio/record-keep-desk`
is four characters longer, so with a ten-digit repository id its job
name will hold 36 of the commit's 40 digits. The gate reads the three
leading values by position: the repository and its id whole; the commit
whole when 40 digits are there, else as a prefix of the record's merge
commit, at least 20 digits, and only when the cut ended the name inside
it. It records which (`name_read.commit_whole`). F7.1's "names the
agent" is read as: names the agent's repository and its id (Unsure 20).

**Unsure 10, as built.** The record names the job by id. A job id is
one attempt's: a re-run makes a new job with a new id under the same
run id. So the record names one attempt and that attempt's
`completed_at`. This is GitHub's documented behaviour; it has not been
exercised here (Unsure 21).

### The verdict

- **RED** when `times_unrecorded`, `times_disagreed` or
  `times_differing` is non-empty. The first two are reads of the served
  file and the pages and come before any network, so the plant reads RED
  whatever GitHub's API says that day (M03 Unsure 4's rule).
- **GREEN** only when every served time carries a clock record, every
  read-back equals it, the job concluded `success`, every page block is
  the file's entry, and nothing was unread.
- **UNSCORABLE** when nothing is RED and: the served file could not be
  read or parsed, it serves no entry or one id twice, a page could not
  be read or holds a block that is not JSON, or a read-back could not be
  made. Never RED, never GREEN.
- A read-back that cannot be made on a time that also differs leaves
  the RED standing, with `unreadable` beside it (M05 PR 3's rule, built
  in).
- An entry that serves no time (`elapsed_seconds` null or absent) is
  named by no list (Unsure 18). A served time that no page shows is
  named by no list (Unsure 17).

### What this PR does not hold

- No lift. `git diff c07fbe5 -- pages/` and `git diff main -- pages/
  index.html` are empty.
- No second repository and no step that starts the clock. The session
  asked GitHub whether `agentkeel-studio/record-keep-desk` exists (a
  GET; 404) and created nothing.
- No edit under `src/m01/` to `src/m06/`, `src/baseline/` (P5),
  `src/gate/`, `src/ingest/`, `goldens/`, `data/`, `pyproject.toml`,
  `uv.lock`, the other workflows, SPEC/00, CLAUDE.md, the README or any
  other milestone's files.
- No secret and no variable. Grep `secrets.` in
  `.github/workflows/m07.yml`: one match, `secrets.GITHUB_TOKEN`. Grep
  `vars.`: none. Grep `https://` under `src/m07/`: the API base and the
  run URL pattern on github.com, nothing else.
- No seat read and no registry read (Unsure 5; M01 Unsure 12).
- No "Measured" cell and no tag. Those are PR 4's.
- No number on a page: no page changes. The step summary shows no time.
  No word of SPEC/00 §11's six. No design of anything the platform owns.

### Construction run (not evidence, P4)

Run on 2026-11-15 UTC from the working tree before the first push, so
`written_by_ci` is false and the tree was dirty.

| Reading | What was read |
|---|---|
| the gate on the real files with no token | `RED`, `times_unrecorded` `["a-002"]` (`clock is null`), `times_disagreed` `[]`, `times_differing` `[]`, `unreadable` `[]`; six pages read, no block on any; `read_back` null; `api_reads` `[]`; exit 1. `result.json` grepped for `ghs_`, `ghp_`, `github_pat_`, `execute-api` and `amazonaws`: no match |
| eighty-four made-up pairs of files in the session's scratch directory, every API read stubbed, not committed | the plant: `RED`, unrecorded, no API read. A lifted entry with every read equal: `GREEN`, with no page block and with a block equal to the entry. Fifteen malformed clock records (a string, a field missing or empty, a repository not `owner/name`, an id a string or `true` or zero, a time with no offset or a word, a short commit, `read_by` malformed, off github.com or another repository's run): each `RED`, unrecorded, no API read. Fourteen differences on the record's side (the entry's repository, the template, the conclusion, `elapsed_seconds` off by one, a float, a word or `true`, the start, the stop, a stop before the start, the id, the pull request, the merge commit, the run) and twenty-three on GitHub's side (the repository 404, renamed, with no template or another, another `created_at`; no pull request, the first not merged, not the record's number, another merge commit; the job 404, of another run, a `sign-agent` job, naming another repository, id or commit, with no values, cut below twenty digits, a short commit in an uncut name, `failure`, not completed, another `completed_at`; the run 404 or of `platform-check.yml`): each `RED`, differing. An uncut name with the whole commit: `GREEN`. Eight unread answers (403, 301, 500, 502, a body that is not an object, a `created_at` that is not a time, the API raising): each `UNSCORABLE`, exit 2. An unread answer beside a difference: `RED`, with `unreadable`. A page showing another time, an id the file lacks, a misnamed block, one wrong page of two: `RED`, disagreed. A page missing beside the plant: `RED`, unrecorded, `unreadable` names the page; beside a lifted entry, a page missing, not UTF-8, or with a block that is not JSON or not an object: `UNSCORABLE`. An entry with no time, alone: `GREEN`; beside the plant: unrecorded `["a-002"]` only. Zero served, not JSON, `agents` not a list, one id twice, an entry with no id: `UNSCORABLE` by the refusal path |
| the gate's own transport on real records: label-impact written as if it were a lifted entry (its repository, id, `created_at`, pull request #1, merge commit `5e370ca`, agentkeel run 38112132210, job 114389865133), once with the owner's `gh auth token` in one process's environment, typed and printed nowhere, and once with no token | `GREEN` both times; four GETs, each 200; the job's name read with the commit whole. With a later deploy job of label-impact (130347979449, commit `bd89989`): `RED`, differing, "the job's name carries the commit bd899896ff7f…, not the merge commit". With the repository named `agentkeel-studio/record-keep-desk`: `RED`, differing, "the repository the record names does not exist". No time read here is written anywhere: label-impact was not timed (M01) |

No defect was found by the eighty-nine readings. The script and its
files live in the session's scratch directory and are not committed (M01
Unsure 21's reading: no test file).

### Expected CI result on this PR

The ledger row says: RED, `times_unrecorded` `["a-002"]`,
`times_disagreed` `[]`, `times_differing` `[]`. The CI run on this PR is
expected to write that, with `unreadable` `[]`, `written_by_ci` true,
`env_set` true, `api_reads` `[]`, no read-back made, and to fail the
`M07 gate` job (exit 1). The other gates that run on a pull request
read their own files, none of which this PR changes. The CI run is the
measurement; the construction run decides nothing.

### Observed (CI run, 2026-11-15 UTC)

The first run on this PR,
[43769375822](https://github.com/andaro74/pharmadelta/actions/runs/43769375822),
wrote the artifact `m07-gate-c708fc2413185f005f66dcf86b402f3ee0609070`
(the sha is the pull request's merge ref; the branch head was
`8ca4f15`). It holds `result.json`, read with `gh run download` into a
fresh directory and `python -I` in this session:

| Field | Value |
|---|---|
| `verdict` | `RED`; `reason` "F7.1 holds: times a-002 are served with no clock record" |
| `times_unrecorded` | `["a-002"]`: `clock is null` |
| `times_disagreed` | `[]`: six pages read (`index.html` and the five under `pages/`), no `second-agent-` block on any |
| `times_differing` | `[]`: nothing read back, `read_back` null, `not_read_back` "no clock record" |
| `unreadable` | `[]` |
| `api_reads` | `[]`: GitHub's API was asked nothing for the plant |
| `env_set` | `{"token": true}`; no value of it in the file. The workflow's grep step passed before the upload; the downloaded file grepped again here for `ghs_`, `ghp_`, `github_pat_`, `execute-api` and `amazonaws`: no match |
| `written_by_ci` | `true`; `commit` `c708fc2`, `dirty` false; `event` `pull_request`, `ref` `refs/pull/48/merge`; `run_at` `2026-11-15T22:27:26+00:00`; exit 1; the `M07 gate` job failed at the gate step, the grep step and the upload step succeeded. `result.json` is 4345 bytes, the artifact 1689 bytes, `expires_at` 2027-02-13 |

Equals the expected result on every field the ledger row names. The
plant is named as row 8 expects: the RED is the missing clock record,
nothing else. No network read was made, so what GitHub's API would have
said that day decided nothing.

On the same head `M00 gate`
([43769375770](https://github.com/andaro74/pharmadelta/actions/runs/43769375770)),
`M02 gate`
([43769375838](https://github.com/andaro74/pharmadelta/actions/runs/43769375838)),
`M03 gate`
([43769375763](https://github.com/andaro74/pharmadelta/actions/runs/43769375763)),
`M04 gate`
([43769375812](https://github.com/andaro74/pharmadelta/actions/runs/43769375812)),
`M05 gate`
([43769375885](https://github.com/andaro74/pharmadelta/actions/runs/43769375885))
and `M06 gate`
([43769375856](https://github.com/andaro74/pharmadelta/actions/runs/43769375856))
passed; `m01.yml` did not run (its paths did not change). Those six are
readings after their measurements and reopen no row. The push that adds
this section runs every gate again; the second `M07 gate` run is read
into a comment on #48.

### What a reader can falsify

- The artifact `m07-gate-<sha>` on this PR's run holds `result.json`
  with `verdict: RED`, `times_unrecorded: ["a-002"]`, `times_disagreed:
  []`, `times_differing: []`, `unreadable: []` and `written_by_ci:
  true`. Download it and read it.
- In that file `served[0].read_back` is null and `api_reads` is `[]`:
  GitHub's API was asked nothing for the plant.
- `git diff main --stat` on this PR touches `src/m07/`,
  `.github/workflows/m07.yml`, `milestones/README.md`,
  `milestones/M07/README.md` and `milestones/M07/rulings/pr2.md` only.
- `agentkeel-studio/record-keep-desk` still answers 404: open the URL.
- The job name's cut: `GET
  /repos/andaro74/agentkeel/actions/jobs/114389865133`, `name`, 100
  characters ending `...`.
- Grep `from src.m0` in `src/m07/gate.py`: no match. Grep `secrets.` in
  the workflow: one match.

### After this PR goes RED

The plant is lifted as "The false state" says: the stopwatch run, then a
workflow of this repository that reads the four records above from
GitHub's API and writes the entry with its `clock`, `scripted` false and
no `PLANT` key, and the one line on the site with its block. Which PR
carries the lift is ruled on reading this PR's CI run, as M03's to
M06's were. Proposed: PR 4, by M03's path (b), a lift workflow run by
hand whose artifact is committed. PR 3, if the cold review of this PR
finds anything, repairs and does not lift; if it finds nothing, PR 3 is
skipped.

**Ruled at PR 2, on reading run 43769375822 (Product).** The owner's
words: "PR 4 carries the lift". The lift is carried by PR 4, as M03's
to M06's were, by M03's path (b): after the stopwatch run, a workflow
of this repository, started by hand, reads the four records from
GitHub's API and writes the entry with its `clock` as an artifact; the
artifact's entry is committed to `pages/api/second-agent.json` with
`scripted` false and no `PLANT` key, and the one line with its block is
written on the site. PR 3, if the cold review of #48 finds anything,
repairs and does not lift; if it finds nothing, PR 3 is skipped. The
Measured cell takes the `main` run after #48 merges (M01 Unsure 23,
ruled at M02 PR 1), which is expected to read as run 43769375822 did on
the three lists: the plant makes no network read (`rulings/pr2.md` 13).

### The `main` run after #48 merged (read 2026-11-15 UTC)

#48 merged at `3292219`. The push ran the gate on `main`:
[run 43770733652](https://github.com/andaro74/pharmadelta/actions/runs/43770733652),
artifact `m07-gate-329221941fb3b9eb2c1e21b1b92e8c23ea1541dc`. Its
`result.json` was read with `gh run download` into a fresh directory and
`python -I`:

| Field | Value |
|---|---|
| `verdict` | `RED`; `reason` "F7.1 holds: times a-002 are served with no clock record" |
| `times_unrecorded` | `["a-002"]`: `clock is null` |
| `times_disagreed` | `[]`: six pages read, no `second-agent-` block on any |
| `times_differing` | `[]`: `read_back` null, `not_read_back` "no clock record" |
| `unreadable` | `[]` |
| `api_reads` | `[]` |
| `env_set` | `{"token": true}`; the file grepped for `ghs_`, `ghp_`, `github_pat_`, `execute-api` and `amazonaws`: no match |
| `written_by_ci` | `true`; `commit` `3292219`, `dirty` false; `event` `push`, `ref` `refs/heads/main`; `run_at` `2026-11-15T22:42:06+00:00`; the `M07 gate` job failed at the gate step, the grep step and the upload step succeeded. `result.json` is 4334 bytes, the artifact 1690 bytes, `expires_at` 2027-02-13 |

Equals row 8's expected output on every field the row names, and reads
as run 43769375822 did. This run is the Measured cell's source. The cell
is filled at PR 4, not here.

## Open detail (PR 3, 2026-11-15 UTC)

PR 3 is the repair. A session that did not write the gate read
`src/m07/gate.py` and `.github/workflows/m07.yml` at `3292219` cold,
against row 8's words, and found two defects. This PR repairs both and
nothing else. It does not lift: `pages/api/second-agent.json` and every
page are unchanged, and the gate still reads the plant RED.

### What the review found

Construction readings only (P4): stubs in the session's scratch
directory, and public records of the platform. None is committed.

**Defects, repaired here.**

| # | Where (at `3292219`) | The input that showed it | What it would have cost |
|---|---|---|---|
| D1 | `write_result`, `main` | `result.json` was written, then the summary rendered and printed. A print that raised reached `main`, which wrote UNSCORABLE over the verdict already written. Shown: a lifted entry with a wrong merge commit and a stdout that encodes ASCII only read exit 2, UNSCORABLE, `UnicodeEncodeError`; the same entry with a UTF-8 stdout read RED. The character was `…`, in three difference messages, none of which has printed in CI. | A real difference at the lift could have read UNSCORABLE where it is RED, in PR 4, with no PR left. CI's stdout is expected to be UTF-8; that was not read in CI, so the defect was latent |
| D2 | `parse_job_name` | GitHub cuts a job's name at 97 characters and trims nothing (`sign-agent`'s name on run 42967373936 ends `, ...`). When the cut lands between the commit's comma and the space after it, the third value read as 40 hex digits and a comma, and the gate named a true time differing. That is a full repository name of 28 characters with a ten-digit id. | Nothing for `record-keep-desk` (33 characters; 36 digits of the commit kept). A second try under an 11-character name (Unsure 7) would have read RED for a reason that is not F7.1's |

**The repair.**

- D1: `write_result` writes `result.json` first; rendering and printing
  the summary are each guarded and cannot raise. The three messages use
  `...` in place of `…`.
- D2: the last value of a cut name loses a trailing comma, which is the
  separator's.

**Limits, recorded and not repaired** (Unsure 30 to 38).

**Nothing found** on: a token or a redirect URL reaching `result.json`
(no path writes either; a redirect is recorded as its status alone); a
clause of F7.1 the gate does not read; a clause read more strictly than
the words; the workflow.

### The cut name, read on real records

| Job | Name | Read |
|---|---|---|
| label-impact, 114389865133 | 100 characters, ends right after the 40-digit commit | the commit whole |
| festival-desk, 115060689514 | 100 characters, 39 digits of the commit, then `...` | a prefix of 39 digits |
| `record-keep-desk`, made up, ten-digit id | 36 digits | a prefix of 36 digits |
| the same, eleven-digit id | 35 digits | a prefix of 35 digits |
| a 28-character full name, made up | 40 digits, a comma, `...` | differing before this PR; the commit whole after |

### Construction run on the repaired gate (not evidence, P4)

| Reading | Before | After |
|---|---|---|
| the gate on the real files, no token | RED, unrecorded `["a-002"]` | the same; other lists `[]`, `api_reads` `[]`, exit 1 |
| a wrong merge commit, stdout ASCII only | UNSCORABLE, exit 2 | RED, differing `["a-002"]`, exit 1 |
| a wrong merge commit, stdout UTF-8 | RED, differing | the same |
| the cut after the comma | differing | no difference |
| label-impact's real records in the lifted shape, no token | GREEN | GREEN |

### What this PR does not hold

- No lift. `git diff main -- pages/ index.html` is empty.
- No second repository and no step that starts the clock.
  `agentkeel-studio/record-keep-desk` answered 404 to a GET in this
  session.
- No change to the workflow, to any other gate, to `src/baseline/`
  (P5), `goldens/`, `data/`, `pyproject.toml` or `uv.lock`.
- No "Measured" cell and no tag. No number on a page.
- No repair of a limit. No design of anything the platform owns.

### Expected CI result on this PR

As row 8 says, and as the `main` run read: RED, `times_unrecorded`
`["a-002"]`, `times_disagreed` `[]`, `times_differing` `[]`, with
`unreadable` `[]`, `written_by_ci` true and `api_reads` `[]`. The
`M07 gate` job fails (exit 1). The Measured source stays run
43770733652; this run is a reading after it.

### Observed (CI run, 2026-11-15 UTC)

The first run on this PR,
[43774347102](https://github.com/andaro74/pharmadelta/actions/runs/43774347102),
wrote the artifact `m07-gate-4e5542203a3f63d23b11b8ccc2c738e70b293a7f`
(the sha is the pull request's merge ref; the branch head was
`b14b74a`). Its `result.json`, read with `gh run download` into a fresh
directory and `python -I`:

| Field | Value |
|---|---|
| `verdict` | `RED`; `reason` "F7.1 holds: times a-002 are served with no clock record" |
| `times_unrecorded` | `["a-002"]` |
| `times_disagreed` | `[]`: six pages read, no block on any |
| `times_differing` | `[]`: `read_back` null, `not_read_back` "no clock record" |
| `unreadable` | `[]`; `api_reads` `[]` |
| `written_by_ci` | `true`; `commit` `4e55422`, `dirty` false; `event` `pull_request`, `ref` `refs/pull/49/merge`; `run_at` `2026-11-15T23:21:23+00:00`; `env_set` `{"token": true}`, no token prefix in the file; the job failed at the gate step, the grep step and the upload succeeded |

Equals the expected result on every field the ledger row names. The
repaired gate reads the plant as the gate on `main` did. The repaired
paths (a difference message, a cut job name) did not run: the plant
makes no read-back. Their first CI exercise is the lift's (Unsure 36).

On the same head `M00 gate`, `M02 gate`, `M03 gate`, `M04 gate`,
`M05 gate` and `M06 gate` passed (runs 43774347057, 43774347052,
43774347024, 43774347030, 43774347043, 43774347020); `m01.yml` did not
run. Those are readings after their measurements and reopen no row. The
push that adds this section runs every gate again; that second `M07
gate` run is read into a comment on #49.

### What a reader can falsify

- `git diff main --stat` on this PR touches `src/m07/gate.py`,
  `milestones/README.md`, `milestones/M07/README.md` and
  `milestones/M07/rulings/pr3.md` only.
- Grep `…` in `src/m07/gate.py`: no match.
- The artifact of this PR's `m07` run holds `result.json` with
  `verdict: RED` and `times_unrecorded: ["a-002"]`.
- festival-desk's job name: `GET
  /repos/andaro74/agentkeel/actions/jobs/115060689514`, `name`.

## Unsure (PR 3)

Numbering continues from PR 2's. Each needs a seat's ruling. None blocks
the repair. Item 38 bears on the stopwatch run's checklist.

| # | Item | Seat |
|---|---|---|
| 29 | The ruling file names this PR as #49, the next number on this repository after #48. | Product |
| 30 | **The agent is not bound to the entry (extends 20).** The gate never reads the entry's `name`. label-impact's real records, served as `a-002` with the name `record-keep-desk`, read GREEN: any repository made from the template and deployed passes as "the second agent". The lift writes the repository the owner creates; the gate cannot tell it from the first. | Product, Engineering |
| 31 | **The run's branch is not read.** A run of `deploy.yml` from a branch of agentkeel other than `main` would count as "agentkeel's `deploy.yml`". Only a login with write access there can make one. label-impact's run reads `head_branch` `main`. | Security, Engineering |
| 32 | **Which successful job (extends 21).** The gate accepts any `deploy-agent` job that names the repository and the commit and concluded `success`, as F7.1's "a job" says. It does not read whether that job deployed or skipped at "Already deployed". The platform drops a deployed commit in `find-agents` and queues runs in one group, so a second successful job for one commit needs a re-run. The lift writes the job that deployed. | Engineering |
| 33 | **How a page block is found (extends 16).** Only `type` before `id`, both in double quotes. A block written the other way round is not seen, and a page's prose is not compared with its block; both read GREEN. The lift writes the block in the form the gate reads. | Product, Engineering |
| 34 | **A time under another key (extends 18).** An entry with `elapsed_seconds` null and the time under another name reads GREEN. | Product |
| 35 | The plant beside an entry with no `id`, or beside one id served twice, reads UNSCORABLE, not RED: the gate refuses the file before it reads any entry. | Engineering |
| 36 | **A 404 on the job or the run is a difference (extends 26).** If this repository's `GITHUB_TOKEN` could not see a job of `andaro74/agentkeel`, a true time would read RED. M01's reader read agentkeel's runs and job lists in CI under the same `permissions`; `GET .../actions/jobs/<id>` has run in CI on no run. A dry run by hand on a branch that is never merged would settle it before the stopwatch run; proposed, not ruled, not done. | Security, Engineering |
| 37 | The step summary ends "No time is shown here". It shows the repository's `created_at` and the job's `completed_at`, and a difference message can name `elapsed_seconds`. Wording; a CI summary is not a page (follows 27). | Product |
| 38 | **A first deploy that fails.** festival-desk's `deploy-agent` job failed on every scheduled run from at least `21:47Z` to `23:57Z` on 2026-10-12. If `record-keep-desk`'s first deploy fails and the fix is a second pull request, the deployed commit is not the first pull request's merge commit and the time reads differing, as F7.1's words say. For the checklist, with 7, 13 and 23. | Product, Security |
| 39 | Unsure 2, 3, 7, 17, 19, 20 and 23 were left blank in this PR's start prompt and stand at their proposals, open. 2, 3 and 7 before the stopwatch run. | Product |
| 40 | D2 as repaired covers a cut after the commit's comma. A cut inside the repository's name or its id (a full name of more than 70 characters) still reads differing. Not reachable by a name the owner would choose. | Engineering |

## Unsure (PR 2)

Numbering continues from PR 1's. Each needs a seat's ruling. None blocks
the measurement. Items 19 and 23 bear on the stopwatch run's checklist.

| # | Item | Seat |
|---|---|---|
| 15 | The ruling file names this PR as #48, the next number on this repository after #47. | Product |
| 16 | **How a page shows a time.** By a `<script type="application/json" id="second-agent-<id>">` block holding the file's entry, on `index.html` or any `pages/*.html`. A time typed into a page's prose with no block is not seen by the gate, the same limit as the M03 to M06 gates. The lift writes the line and its block together. | Product, Engineering |
| 17 | **One direction.** The row says GREEN needs every served time "shown as served". Read here as: what a page shows equals what the file serves. A served time that no page shows is named by no list. Whether GREEN must require the line to exist is Product's; the lift places it either way. | Product |
| 18 | An entry whose `elapsed_seconds` is null or absent serves no time and is named by no list, whatever its `clock` (M06 Unsure 24's reading). | Product |
| 19 | **The second repository must be public.** The gate reads with this repository's `GITHUB_TOKEN`, which sees public repositories only. A private repository answers 404, and the gate names its time differing, "does not exist, or is not public". One line for the stopwatch run's checklist: choose Public when creating from the template. | Security, Product |
| 20 | **The job's name is cut at 97 characters.** For `record-keep-desk` the name will hold about 36 of the commit's 40 digits, fewer if the repository id is longer. The gate accepts a cut prefix of at least 20 digits. The name never holds the agent's bare name; "names the agent" is read as the repository's full name and id. GitHub's API gives the matrix values nowhere else on the job's record. | Engineering, Product |
| 21 | Unsure 10 as built: the record names one attempt by its job id. That a re-run makes a new job id is GitHub's documented behaviour, not exercised here. If the deploy job is re-run during the stopwatch run, the lift writes the first attempt that concluded `success`. Proposed. | Engineering |
| 22 | `read_by`, the lift's run and artifact, is checked for form and not read back: the gate reads GitHub's four records itself. Whether it should also download the lift's artifact and compare. Proposed: no. | Engineering |
| 23 | **"First pull request"** is the earliest by creation time, whatever its number. If it is closed unmerged and a second one is merged and deployed, the time reads differing, as F7.1's words say. For the checklist: the agent's files go in one pull request and that one is merged. | Product |
| 24 | The gate does not read `scripted` or `PLANT`. A lifted entry that still said `scripted` true would read GREEN if its records were equal. The lift removes both. | Product |
| 25 | The template is read from `template_repository.full_name`. If the template repository is later renamed or deleted, GitHub's answer changes and the time would read differing. Recorded. | Engineering |
| 26 | The read-back has run in CI on no run: the plant makes no network read. Its first CI exercise is the lift's. That this repository's `GITHUB_TOKEN` can read a job of `andaro74/agentkeel` rests on M01's reader, which read that repository's runs and jobs with it, and on the construction reading with no token. | Engineering |
| 27 | `result.json` records the plant's `elapsed_seconds` as read, in `served[].elapsed_seconds`. A CI artifact is not a page, and the step summary shows no time. Follows Unsure 1. | Product |
| 28 | PR 1's Unsure 1, 2, 3, 5, 6 and 7 were left blank in this PR's start prompt and stand at their proposals, open. 2, 3 and 7 before the stopwatch run. The order of PR 3 and the run in the attention plan is still Product's to change. | Product |

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant. Items 2, 3 and 7
must be ruled before the stopwatch run.

| # | Item | Seat |
|---|---|---|
| 1 | **A served JSON file and SPEC/00 §11.** §11 and CLAUDE.md forbid a number on a page that is not a CI-written result. The plant's `3600` is in `pages/api/second-agent.json`, which GitHub Pages serves, and in no HTML page. Read here as: a served file is not a page, as `pages/api/sign-off.json` carried a hand-set `signed` at M06. The number is labelled as typed by hand wherever it is written. Confirm the reading, or rule that the plant must carry no number (for instance `elapsed_seconds` as the word "about an hour"). | Product |
| 2 | **What may be prepared before the clock.** agentkeel SPEC/06 §1: nothing is prepared before `created_at` beyond the account set-up. Proposed the same: before the run only the name, the job, this file and the checklist exist; the table, clauses, goldens, tool and prompt are written after `created_at`. The other reading, files drafted beforehand and pasted in, gives a smaller number that times the platform alone. Which one decides what the number means. | Product |
| 3 | **Starting the check and the deploy by hand.** Both workflows run on a schedule and take `workflow_dispatch`. At M01 the owner started the check twice and the deploy once; agentkeel's own timed run did the same when GitHub skipped the schedule for 28 minutes. Proposed: allowed, each recorded in the close detail with its run link, and said on the site line's record. Who dispatches, the owner or the session with `gh` on the owner's "go", is the owner's to say in the checklist. | Product, Security |
| 4 | **Whose time it is.** The owner creates and merges; an assistant session writes the agent's files; one person holds all seven seats. It is not a second developer with write access alone, which is what agentkeel timed. Proposed: the site line and the Measured cell say so in those words. | Product |
| 5 | **Seats.** F7.1 does not read the second agent's seats. The platform's check refuses a null seat and the deploy needs a passing check, so a deployed agent's seats were filled as the platform reads them; that is the platform's record, not this gate's reading. `M01_READ_TOKEN` covers `label-impact` only; reading the new repository's seat permissions would need the owner to extend it after the repository exists, a hand step inside or after the run. Proposed: the M07 gate reads public records only, with `GITHUB_TOKEN`, and no secret. | Security, Engineering |
| 6 | **Where the one line goes.** Product said: the ledger's Measured cell and one line on the site, each linked to the CI run that wrote it. Proposed: `index.html`, under "The record". The gate must read that page for the `times_disagreed` arm. | Product |
| 7 | **A second try.** If the run is abandoned or fails, a new repository with a new name is a new attempt. Proposed, as agentkeel's finding 4: the first attempt's time is the measurement; a later attempt is recorded beside it and never replaces it. A run that never reaches a successful deploy is an attempt with no stop, and the row is read from it. | Product |
| 8 | **A bank's agent on a labeling demo.** SPEC/00 §1 and §9 describe one fictional generics company. The second agent belongs to a fictional bank, by Product's choice, to show the platform is not tied to labeling. SPEC/00 §8 says only "a second agent", so nothing is contradicted; §3's table of three repositories will be one short once the repository exists. Proposed: an errata PR to §3 after M07 closes, outside any cap, and the site line says the second agent is a fictional bank's. | Product |
| 9 | **What the second agent may say.** It says what the bank's policy requires and gives no legal or financial advice; the prompt says so. Proposed: no `rules/` folder, so it runs under the platform's baseline guardrail alone. Rules of its own would need a second pull request and a registry read by the owner (agentkeel quickstart §5a), both on the clock, and meet maintenance finding 2 at the next upgrade. | Rule Owner |
| 10 | **The deploy run by id.** The gate reads the run and job the clock record names. Whether a job's `completed_at` can change after the fact (a re-run of the job makes a new attempt) and how the gate reads attempts is PR 2's to settle. | Engineering |
| 11 | **The bank has no name.** A made-up bank name could match a real one, and no search was made. Proposed: it stays "a fictional bank" everywhere. | Product |
| 12 | **The data.** The retention table, the policy clauses and the goldens are the Data Owner's, ruled in the agent's repository during the run. A golden does not state the fact its own row holds (P6). At least one ordinary and one trap, the platform's minimum. | Data Owner |
| 13 | **First deploy after the platform's maintenance.** Not read (table above). If the first deploy of a new agent fails for a platform reason during the run, the clock keeps running, it is said at once, and the fix is agentkeel's, flagged and not designed here. | Security |
| 14 | The ruling file names this PR as #47, the next number on this repository. | Product |
