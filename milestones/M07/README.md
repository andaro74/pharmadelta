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
| PRs used / cap | 1 / 4 |
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
