# M04: The side-by-side page runs the baseline live

Row 5 of the ledger (`milestones/README.md`). The claim text is SPEC/00
§8's, word for word. Needs M03, which closed at tag `m03` on `9932776`
with row 4 GREEN. One claim, one planted failure, one measured verdict
(P3). Cap four PRs (ADR-0001 U9).

## Ledger row

Written at PR 1 open. The row in `milestones/README.md` is the ledger's;
this is the same row with the open detail.

| Field | Row 5 |
|---|---|
| Claim | The side-by-side page runs the baseline live |
| Falsifiers | F4.1 an ordinary-assistant answer the side-by-side page shows was not produced by a run of the frozen baseline (`src/baseline/` as at tag `m00`) made by this repository's CI: it carries no run record, or its `table_row`, `clause_id` or `answer_fields` differ from what that baseline writes for its question; or the page shows an ordinary-assistant answer the baseline file does not serve; or the page shows an agent answer that is not the entry the public API serves. |
| Seeded commit | `a896442` on `m04-pr1`: `pages/api/baseline.json`, the ordinary assistant's served answers, one entry, the question of golden `g-001` with an answer written by hand, its row `lisinopril.8.1` and its clause `201.57(c)(9)(i)` copied from `data/` at `595dd68`, `run` null, `scripted` true, a `PLANT` key beside them; `pages/side-by-side.html`, the side-by-side page, showing that answer in the ordinary-assistant column, labelled an illustration, with no run record, beside the deployed agent's entry copied from `pages/api/answers.json` with its call record. Nothing in the repository runs the baseline for a page. |
| Expected gate output | PR 2's gate, in CI, reads every ordinary-assistant answer the baseline file serves and the page shows and names each that carries no run record or that the page and the file do not agree on, and names each agent answer the page shows that the public API does not serve; then runs the frozen baseline in CI with the command `gate.yml` runs, `uv run python -m src.baseline.run`, over `goldens/`, compares each served answer with the run's observation of the same id (the served question must equal the golden's), and checks `src/baseline/` equals its state at tag `m00`. It writes a `result.json` that is RED when any served answer is unrun, disagreed or differing, any agent answer disagrees, or the baseline has changed, naming each; GREEN only when every served answer carries a run record, is shown as served and equals the run's observation, every agent answer shown is the API's, and `src/baseline/` equals `m00`; UNSCORABLE when nothing is RED and a served file could not be read or the baseline could not run. On `a896442`: RED, `answers_unrun` `["g-001"]`, `answers_disagreed` `[]`, `answers_differing` `[]`, `agent_disagreed` `[]`, `baseline_changed` false. The Measured cell cites the `main` run after PR 2 merges (M01 Unsure 23, ruled at M02 PR 1). |
| Measured | RED, `answers_unrun` `["g-001"]`, `answers_disagreed` `[]`, `answers_differing` `[]`, `agent_disagreed` `[]`, `baseline_changed` false, `unreadable` `[]`, `written_by_ci` true, on `main` at `4d92676`: [run 41234548875](https://github.com/andaro74/pharmadelta/actions/runs/41234548875), artifact `m04-gate-4d926760c985e973bdd5d35f1c76f0db47660808`. The PR run on #24 at merge ref `a724249`, [run 41233100816](https://github.com/andaro74/pharmadelta/actions/runs/41233100816), artifact `m04-gate-a7242498e5bd9fc47e714271df8ee604c04deca4`, read the same on every field the row names. Equals the expected output. |
| PRs used / cap | 4 / 4 |
| State | GREEN |

## The false state (P1, P2)

The claim says the side-by-side page runs the baseline live. It is
false when the page shows an ordinary-assistant answer that no run of
the baseline produced. That is what `a896442` commits.

`pages/api/baseline.json` is what the ordinary-assistant column serves:
a list of answers, one per question, in the shape of
`pages/api/answers.json` with `run` where that file has `agent` and
`call`. It holds one entry. The question is golden `g-001`'s. The
answer, `table_row` `lisinopril.8.1`, `clause_id` `201.57(c)(9)(i)`,
`impacted` true, `owed` `follow-rld`, `escalate` false, was written by
hand. The row and the clause beside it are copies of `data/table.json`
and `data/clauses.json` at `595dd68`. `run` is null: no run id, no
commit, no time, no artifact. `scripted` is true and a `PLANT` key says
what the entry is.

`pages/side-by-side.html` is the side-by-side page. It shows the
question once and two columns under it. The left column, "An ordinary
assistant", shows the hand-written answer with its row and its clause
under a banner that says it is an illustration and no run produced it
(P8, SPEC/00 §11). The right column, "The deployed agent", shows the
entry `pages/api/answers.json` serves for the same question: no row
found, the call record of CI run 41222218526, as `pages/detail.html`
shows it. The page embeds both entries in `<script
type="application/json">` blocks, `id="baseline-answer"` and
`id="agent-answer"`, so a reader reads the page's answers without an
HTML parser. The page says what the ordinary assistant is: the keyword
matcher in `src/baseline/`, no model, frozen at `m00` (M00
`rulings/pr2.md` 1). It shows no measured number; the numbers on it are
the row's, the clause's and the agent's call record's (M03 Unsure 7,
ruled).

Why this plant: a page that shows a right answer in the
ordinary-assistant column, with its row and its clause, and no run of
the baseline behind it, is the thing the claim rules out. It is also
what SPEC/00 §11 allowed before M04: an illustration. The hand-written
answer equals golden `g-001`'s `expected`, which is also what the
baseline wrote for `g-001` at `m00` (M00 README, run 38058191295). So a
gate that reruns the baseline and compares values reads no difference
on this plant. Only a gate that demands the run record goes RED. The
plant tests which one PR 2 builds, as M03's plant tested the call
record.

Lifting the plant is one change to the entry: `run` filled with the
record of the CI run of `src.baseline.run` that produced the answer,
the answer fields what that run wrote, `scripted` false, the `PLANT`
key removed; and the page rebuilt from it. Not one line of
`src/baseline/` changes (P5). Which PR carries the lift is decided
after PR 2 goes RED, not here.

## What "live" means at M04 (assumption, Unsure 1)

SPEC/00 §11 says the ordinary assistant is a real run of the frozen
baseline from M04. This milestone reads "live" as (a): a CI run of the
frozen baseline, in this repository, whose observation the page serves
with its run record, the shape M03 used for the agent (M03 Unsure 1,
ruled at `rulings/pr4.md` 7: the API is a read API). The other reading,
(b), a run at page view, needs a host that runs code at request time;
GitHub Pages runs none, and a run in the visitor's browser would be a
port of the baseline out of `src/baseline/`, a second copy of the
control that P5 freezes. The plant is false under either reading: no
run produced the answer. Proposed: (a). Product rules.

## Open detail (PR 1, 2026-10-31)

### What this PR holds

- Row 5 of the ledger: falsifier, seeded commit, expected gate output,
  PRs used 1 / 4.
- `pages/api/baseline.json` and `pages/side-by-side.html`, the plant.
- This file.
- `rulings/pr1.md`.

Nothing else. No code that runs the baseline for a page, no workflow,
no test (P2). No edit to `src/` (`src/baseline/` is frozen at `m00`,
P5), `goldens/`, `data/`, `pages/detail.html`, `pages/api/answers.json`,
`.github/workflows/`, SPEC/00, CLAUDE.md, the README, `.gitignore` or
anything under `milestones/M00/` to `milestones/M03/` or
`milestones/adoption/`.

### The repository, as read at open (construction, not evidence, P4)

Read 2026-10-31 on `main` at `9932776`.

| What | Read |
|---|---|
| `main` | `9932776`, the merge commit of #22; tag `m03` on it |
| `src/baseline/` | `answer.py` and `run.py`, unchanged since tag `m00` (`git diff m00 --stat -- src/baseline/` is empty) |
| the baseline on `g-001` | the M00 README records the CI run's observation: `lisinopril.8.1`, `201.57(c)(9)(i)`, `impacted` true, `owed` `follow-rld`, `escalate` false (run 38058191295). Not read again here; PR 2's CI run reads it |
| `pages/` | `detail.html` and `api/answers.json` only; no side-by-side page before this PR |
| the M03 gate's reads | `src/m03/gate.py` reads `pages/api/answers.json` and the `id="answer"` block of `pages/detail.html` by path (its `--api` and `--page` defaults); it globs nothing under `pages/`. The new page has no `id="answer"` block |
| `data/` | unchanged since `595dd68`; the row and the clause copied into the plant equal the table's and the file's |
| GitHub Pages | not enabled: `GET /repos/andaro74/pharmadelta/pages` answers 404 (Unsure 2) |

### What this PR does not hold

- No run of the baseline for a page. Grep `src.baseline` and
  `baseline.run` under `pages/` and `.github/`: the matches are
  `gate.yml`, the M00 gate, unchanged, and the `PLANT` key's prose in
  `pages/api/baseline.json`, copied into `pages/side-by-side.html`.
  The prose names the module; nothing under `pages/` runs it.
- No run record. The entry carries `run: null` until the PR that
  carries the lift, decided after PR 2 goes RED.
- No change to `src/baseline/`. `git diff m00 --stat -- src/baseline/`
  is empty on this branch.
- No change to `pages/detail.html` or `pages/api/answers.json`. The
  side-by-side page copies the API's entry; it does not change it.
- No workflow. `gate.yml`, `m01.yml`, `m02.yml`, `m03.yml` and
  `m03-lift.yml` are unchanged. The `M01 gate` reads PENDING, exit 3,
  on every pull request and is not required (M01 Unsure 14); it is left
  alone. The M03 gate runs on this PR and calls the agent; whatever it
  reads is a reading after the measurement and does not reopen row 4
  (M03 `rulings/pr4.md` 6, 22).
- No number on a page that is a result. The page's numbers are the
  row's strengths, dates and application numbers, the clause's
  citation and dates, and the agent's call record's time and id, the
  CI run's, linked (M03 Unsure 7, ruled at `rulings/pr4.md` 8).
- No brand name. No word of SPEC/00 §11's six.

### What a reader can falsify

- `git diff main --stat` on this PR touches `pages/api/baseline.json`,
  `pages/side-by-side.html`, `milestones/README.md`,
  `milestones/M04/README.md` and `milestones/M04/rulings/pr1.md` only.
- In `pages/api/baseline.json`, the one entry has `"run": null`,
  `"scripted": true` and a `PLANT` key. Its `row` equals the
  `lisinopril.8.1` object in `data/table.json` and its `clause`, less
  the `id` key, equals `data/clauses.json`'s `201.57(c)(9)(i)`, both at
  `595dd68`. Its `question` equals `goldens/g-001.yaml`'s and
  `pages/api/answers.json`'s.
- In `pages/side-by-side.html`, the JSON inside `<script
  type="application/json" id="baseline-answer">` parses to the same
  object as the baseline file's entry, and the JSON inside
  `id="agent-answer"` parses to the same object as
  `pages/api/answers.json`'s entry. The banner above the
  ordinary-assistant answer says it is an illustration.
- The page carries none of "validated", "compliant", "Part 11",
  "governed", "secure" or "proven", and no brand name (SPEC/00 §2,
  §11).
- The page has no `<script type="application/json" id="answer">`
  block, so `src/m03/gate.py`'s `PAGE_BLOCK` does not match it; the
  gate reads `pages/detail.html` by path in any case.
- Nothing in this PR runs the baseline for a page: the grep above
  finds `gate.yml` and the `PLANT` key's prose, nothing else.
- `git diff m00 --stat -- src/baseline/` on this branch is empty (P5).

### Carried to PR 2

PR 2 is the measure. It adds the gate that reads the plant and nothing
that lifts it.

- **The run.** The gate runs the frozen baseline in CI with the command
  `gate.yml` already runs, `uv run python -m src.baseline.run --out
  <file>`, over `goldens/`. It adds no runner and no argument to
  `src/baseline/` (P5). The observation with the served entry's `id` is
  the one compared; the served `question` must equal the golden's, else
  the entry is named differing.
- **The run record's fields, proposed.** `run_url` (a run of this
  repository's workflow), `artifact` (the CI artifact holding the
  observations file), `commit` (the commit the run checked out),
  `baseline_commit` (the last commit touching `src/baseline/`, at or
  before `m00`), `started_at` (the observations file's), `method`
  (`src/baseline/answer.py`'s docstring, "keyword matching"),
  `written_by_ci` true. The gate names an answer unrun when `run` is
  null, lacks a field, or `written_by_ci` is not true. Fixed at PR 2,
  not here (Unsure 5).
- **The verdict.** `answers_unrun`, `answers_disagreed`,
  `answers_differing`, `agent_disagreed`, `baseline_changed`,
  `unreadable`, `written_by_ci`, as the row's expected output says. RED
  on an unrun or disagreed answer is a read of the served files alone,
  before the baseline runs, as M03 Unsure 4 ruled for the call record.
- **The frozen check.** `git diff m00 --quiet -- src/baseline/` in the
  checkout; `baseline_changed` true when it differs (Unsure 7).
- **The artifact.** `m04-gate-<sha>`, holding `result.json` and the
  observations file, 90 days, as the other gates.
- **The agent column.** `agent_disagreed` names each agent entry the
  page shows that is not equal, as parsed JSON in canonical form, to
  the API's entry of that `id`. The M03 gate is not edited (Unsure 4).
- **No lift.** PR 2 serves nothing new. The lift's shape is M03's: a
  CI run writes the record as an artifact and a writer rebuilds the
  file and the page from it, deterministically, LF pinned.

### Rulings carried from earlier milestones

| # | Ruled |
|---|---|
| M01's 23 (ruled at M02 PR 1) | The Measured cell cites the run on `main` after PR 2 merges, with the PR run named beside it when it was the one read at the time. Row 5's expected gate output says so. |
| M00's 1 (ruled at M00 PR 2, `rulings/pr2.md` 1) | The baseline stays the keyword matcher and is frozen at `m00`. The M04 side-by-side page says what it is. The page does. |
| M00's 1, option C (noted at M00 PR 2, `rulings/pr2.md` 2) | A labelled live model panel beside the control is M04's to decide. Unsure 6 below. |
| M03's 7 (ruled at M03 PR 4, `rulings/pr4.md` 8) | The row's and the clause's data are not measured numbers; a call record's time and id are the CI run's, linked. Applied to the side-by-side page. |
| M03's 6 and 22 (ruled at M03 PR 4) | A reading of the M03 gate after the measurement never reopens row 4. The M03 gate's reading on this PR is recorded in the PR, not in a ledger cell. |

## Open detail (PR 2, 2026-10-31)

PR 2 is the measure. It adds the gate that reads the plant and nothing
that lifts it. `pages/api/baseline.json` serves one ordinary-assistant
answer with `run` null at the head this PR measures, and
`pages/side-by-side.html` shows it. M04 is measured here.

### What this PR holds

- `src/m04/gate.py`, the gate. Python 3.14; standard library plus
  PyYAML, which `src/baseline/run.py` already needs, so `pyproject.toml`
  and `uv.lock` are unchanged. It mirrors `src/m03/gate.py`: the same
  `read_served`, `read_page`, `canonical` and `disagreed`, the same
  provenance, the same `Unscorable` path. In order:
  1. Reads `pages/api/baseline.json` (the `answers` list), the JSON in
     the `<script type="application/json" id="baseline-answer">` and
     `id="agent-answer"` blocks of `pages/side-by-side.html` (one object
     or a list each), and `pages/api/answers.json` for the agent column.
  2. `answers_unrun`: every served answer whose `run` is null, is not an
     object, lacks a field of the run record or holds it empty, or whose
     `written_by_ci` is not true. A read of the served file; no run.
  3. `answers_disagreed`: every page baseline answer whose `id` the
     baseline file does not serve, or that is not equal to the file's
     entry of that `id` as parsed JSON in canonical form (sorted keys, no
     whitespace; M03 Unsure 15's reading).
  4. `agent_disagreed`: every page agent answer whose `id`
     `pages/api/answers.json` does not serve, or that is not equal to
     the API's entry of that `id`, canonical form (Unsure 4).
  5. `baseline_changed`: `git diff m00 --quiet -- src/baseline/` in the
     checkout; true on exit 1, false on exit 0, null with the error on
     any other exit or when the tag is not in the checkout (Unsure 7).
     The tag's commit and the last commit touching `src/baseline/` are
     recorded beside it.
  6. Reads the observations file `--observations` names, the one the
     workflow's baseline step wrote in the same job. The gate runs
     nothing itself.
  7. `answers_differing`: every served answer that carries a run record
     and whose `question` is not `goldens/<id>.yaml`'s, or whose
     `table_row`, `clause_id` or `answer_fields` is not what the run's
     observation of the same `id` holds, or for whose `id` the run holds
     no observation.
  8. Writes `result.json` and exits 0 GREEN, 1 RED, 2 UNSCORABLE.
- `.github/workflows/m04.yml`: on every pull request, every push to
  `main` and by hand. `actions/checkout` with `fetch-depth: 0` (the tag
  `m00` and the history of `src/baseline/`), `uv sync --locked`, the
  artifact directory, then the baseline step `gate.yml` runs, `uv run
  python -m src.baseline.run --out "$RUNNER_TEMP/m04-gate/observations.json"`,
  then the gate with `--observations` on that file, run whenever the
  baseline step ran, crashed or not, then the artifact `m04-gate-<sha>`
  holding `result.json` and `observations.json`, 90 days,
  `if-no-files-found: error`, uploaded on `if: always()`. The gate writes
  its table to the job summary. The job fails on anything but GREEN. No
  `secrets.`, no `vars.`, no `env` on any step. `gate.yml`, `m01.yml`,
  `m02.yml`, `m03.yml` and `m03-lift.yml` are unchanged.
- `result.json` records the commit, whether the tree was dirty, whether
  CI wrote it (`written_by_ci`), the run's URL, the run record's fields,
  the fields compared, the freeze check with the tag's commit and the
  last baseline commit (`baseline`), the observations file's provenance
  (`observations`: its `commit`, `started_at`, `method`, the ids), each
  served answer's record check, page equality, golden read, observation
  and comparison (`served`), the page's two columns (`page`) and the
  agent column against the API (`agent`), so the file says for itself
  whether it is evidence (P4).
- `rulings/pr2.md`, and "PRs used / cap" set to 2 / 4 here and in the
  ledger.

### The run record's fields (Unsure 5, ruled)

`run_url` (a run of this repository's `m04` workflow or the lift's),
`artifact` (the CI artifact holding the observations file the answer was
written from), `commit` (the commit the run checked out),
`baseline_commit` (the last commit touching `src/baseline/`, at or
before `m00`; `df860b7` on `main` today), `started_at` (the observations
file's, UTC), `method` (the observations file's: "keyword matching; see
src/baseline/answer.py"), `written_by_ci` (true). The gate names an
answer unrun when any is missing or empty or when `written_by_ci` is
not true. The lift writes them. From here `run_url` is readable through
GitHub's API and `artifact` for 90 days; `baseline_commit` is checkable
against the checkout's last baseline commit, which the gate records
under `baseline.baseline_commit` and does not judge (Unsure 13).

### The verdict

- **RED** when `answers_unrun`, `answers_disagreed`, `answers_differing`
  or `agent_disagreed` is non-empty, or `baseline_changed` is true. The
  first two and the fourth are reads of the served files and come before
  the observations file is read, so the plant reads RED whatever the
  baseline run's state that day (M03 Unsure 4's rule, applied here).
- **GREEN** only when every served answer carries a run record written
  by CI, is shown as served and equals the run's observation on its
  question, `table_row`, `clause_id` and the three answer fields; every
  agent answer shown is the API's entry; `src/baseline/` equals `m00`;
  and nothing is unread.
- **UNSCORABLE** when nothing is RED and: a served file could not be read
  or parsed, the baseline file serves no answer, a served answer is
  neither null nor an object, the tag `m00` is not in the checkout, the
  observations file was not written or could not be read (the baseline
  could not run), or a served answer with a run record was not compared.
  Never RED, never GREEN.
- Equality is against the gate's own run of the baseline in the same
  job, as M03's was against its own call (M03 `rulings/pr2.md` 4). The
  baseline has no model and no randomness, so the observation is the
  same on every run at the same `data/` and `goldens/` (Unsure 15).

### What this PR does not hold

- No lift. `git diff main -- pages/` is empty: `pages/api/baseline.json`
  carries `run: null`, `scripted: true` and the `PLANT` key as at
  `a896442`, and `pages/side-by-side.html` keeps its illustration banner.
- No change to `src/baseline/` (P5): `git diff m00 --stat --
  src/baseline/` is empty on this branch. The workflow runs it with
  `gate.yml`'s command and adds no argument to it.
- No change to `src/m03/`, `src/gate/`, `src/ingest/`, `src/m01/`,
  `gate.yml`, `m01.yml`, `m02.yml`, `m03.yml`, `m03-lift.yml`,
  `goldens/`, `data/`, `pyproject.toml`, `uv.lock`, SPEC/00, CLAUDE.md,
  the README, or anything under `milestones/M00/` to `milestones/M03/`
  or `milestones/adoption/`. The M03 gate is not edited (Unsure 4).
- No secret, no variable, no network. Grep `secrets.`, `vars.` and
  `env:` in `.github/workflows/m04.yml`: no match. Grep `https://`
  under `src/m04/`: no match; the run URL in `result.json` is built
  from the CI environment. The gate reads the checkout and the
  observations file.
- No design of a GitHub Pages deploy (Unsure 2, carried) and no live
  model panel (Unsure 6, carried).
- No "Measured" cell and no tag. Those are PR 4's.
- No number on a page: no page changes here. No word of SPEC/00 §11's
  six. No brand name.

### Construction run (not evidence, P4)

Run on 2026-10-31 on the branch before the first push, from the working
tree at `9628638` with the gate uncommitted, so `written_by_ci` is false
and the tree was dirty. In order:

| Reading | What was read |
|---|---|
| `uv run python -m src.baseline.run --out <scratch>/observations.json` | six observations, `g-001` to `g-006`; `g-001` `lisinopril.8.1`, `201.57(c)(9)(i)`, `impacted` true, `owed` `follow-rld`, `escalate` false, as the M00 README records run 38058191295 wrote; `commit` `9628638`, `dirty` true, `method` "keyword matching; see src/baseline/answer.py" |
| the gate on the real pages with that file | `RED`, `answers_unrun` `["g-001"]` (`run is null`), `answers_disagreed` `[]`, `answers_differing` `[]`, `agent_disagreed` `[]`, `baseline_changed` false (tag `m00` at `e94b76b`, `baseline_commit` `df860b7`, diff exit 0), `unreadable` `[]`, `written_by_ci` false; the page's baseline answer equal to the file's entry, the page's agent answer equal to the API's entry; g-001 not compared, "no run record"; golden read; exit 1 |
| the M00 scorer on the same observations file | `GREEN`, exit 0 |
| the M02 gate | `GREEN`, exit 0; eCFR title 21 up to date as of 2026-10-29 |
| twenty made-up pairs of files in the session's scratch directory, not committed | a lifted entry (run record complete, `written_by_ci` true, answer the observation's): `GREEN`, exit 0, "all equal". `written_by_ci` false: `RED`, `answers_unrun`. The record missing `artifact`: `RED`, `answers_unrun`. `run` a string: `RED`, `answers_unrun`. The page's `owed` changed on the plant: `RED`, `answers_unrun` and `answers_disagreed` `["g-001"]`. The page showing `g-999`: `answers_disagreed` `["g-999"]`. The page's agent `request_id` changed: `agent_disagreed` `["g-001"]`, on the plant and on the lifted entry alike. The lifted entry's `owed` changed: `RED`, `answers_differing`, "differs on ['answer_fields.owed']". Its `question` extended: `answers_differing`, "differs on ['question']". Its `answer` null: `answers_differing`, "the served answer is null and the run wrote an observation". `g-999` with a run record: `answers_differing`, "the run holds no observation of this id". The lifted entry with no `--observations`, or a missing file: `UNSCORABLE`, exit 2, `unreadable` names it. The plant with no observations file: `RED`, exit 1. The plant plus a run entry whose `answer` is the string "no answer": `RED`, `answers_unrun` `["g-001"]`, `unreadable` names g-002. That string entry alone: `UNSCORABLE`. Zero served answers: `UNSCORABLE`. The page without its `agent-answer` block, lifted: `UNSCORABLE`, `unreadable` names the block. The API file for the agent column malformed, on the plant: `RED`, `unreadable` names the API |
| the freeze arm | one comment line appended to `src/baseline/answer.py` in the working tree, the gate run, the line reverted with `git checkout --` in the same command: `RED`, "served answers g-001 carry no run record; src/baseline/ differs from tag m00", `baseline_changed` true, diff exit 1. After the revert `git diff m00 --stat -- src/baseline/` is empty and `git status` shows no change under `src/baseline/`. Never committed (Unsure 18) |

No defect was found by the twenty-one readings. The stub files and the
script live in the session's scratch directory and are not committed
(M01 Unsure 21's reading: no test file).

### Expected CI result on this PR

The ledger row says: RED, `answers_unrun` `["g-001"]`,
`answers_disagreed` `[]`, `answers_differing` `[]`, `agent_disagreed`
`[]`, `baseline_changed` false. The CI run on this PR is expected to
write that, with `written_by_ci` true, the run URL, `baseline.tag_commit`
`e94b76b` and `observations.read` true with six ids, and to fail the
`M04 gate` job (exit 1). The baseline's observation of g-001 is recorded
beside the unrun answer and decides nothing. On the same head the `M00
gate` is expected GREEN (the one required check), the `M02 gate` GREEN as
on `main`, the `M01 gate` PENDING, exit 3, not required (M01 Unsure 14),
and the `M03 gate` whatever shape the door gives that day: it signs in
as `pharmadelta` and calls the agent on every pull request, and its
reading is after the measurement and never reopens row 4 (M03
`rulings/pr4.md` 6, 22); it is recorded in the PR body, not in a ledger
cell. The CI run is the measurement; the construction run decides
nothing.

### Observed (CI run, 2026-10-31)

The first run on this PR,
[41233100816](https://github.com/andaro74/pharmadelta/actions/runs/41233100816),
wrote the artifact `m04-gate-a7242498e5bd9fc47e714271df8ee604c04deca4`
(the sha is the pull request's merge ref, as M00's to M03's were; the
branch head was `f54fca6`). It holds `result.json` and
`observations.json`, read with `gh run download` in this session:

| Field | Value |
|---|---|
| `verdict` | `RED`; `reason` "F4.1 holds: served answers g-001 carry no run record" |
| `answers_unrun` | `["g-001"]`: `served[0].run_record.why` "run is null" |
| `answers_disagreed` | `[]`: the page's baseline answer equals the file's entry as parsed JSON |
| `answers_differing` | `[]`: nothing compared, `not_compared` "no run record" |
| `agent_disagreed` | `[]`: the page's agent answer equals `pages/api/answers.json`'s entry |
| `baseline_changed` | `false`; `baseline.tag_commit` `e94b76b`, `baseline.baseline_commit` `df860b7`, `diff_exit` 0 (Unsure 14: the tag resolved under `fetch-depth: 0`) |
| `unreadable` | `[]` |
| `observations` | `read` true, six ids `g-001` to `g-006`, `commit` `a724249`, `dirty` false, `started_at` `2026-10-31T19:12:26+00:00`, `method` "keyword matching; see src/baseline/answer.py" |
| `served[0].observation` | `lisinopril.8.1`, `201.57(c)(9)(i)`, `impacted` true, `owed` `follow-rld`, `escalate` false: the baseline's observation of g-001, equal in value to the hand-written answer the plant serves, recorded beside the unrun answer; it decides nothing |
| `written_by_ci` | `true`; `commit` `a724249`, `dirty` false; `event` `pull_request`, `ref` `refs/pull/24/merge`; exit 1; the `M04 gate` job failed. On the same head `M00 gate` passed ([41233100811](https://github.com/andaro74/pharmadelta/actions/runs/41233100811)), `M02 gate` passed ([41233100772](https://github.com/andaro74/pharmadelta/actions/runs/41233100772)), `M01 gate` is not required and reads as it did on `main` ([41233100819](https://github.com/andaro74/pharmadelta/actions/runs/41233100819)) |

Equals the expected result above on every field the ledger row names.
The plant is named as ledger row 5 expects: the RED is the missing run
record and nothing else, as M03's was the missing call record.

The `M03 gate` on the same head,
[41233100879](https://github.com/andaro74/pharmadelta/actions/runs/41233100879),
artifact `m03-gate-a7242498e5bd9fc47e714271df8ee604c04deca4`, read
`GREEN`: `answers_uncalled` `[]`, `answers_disagreed` `[]`,
`answers_differing` `[]`; sign-in as `pharmadelta` 200, 506 ms; the
door 200, `request_id` `GH6QBin8vHcEPoA=` in `apigw-requestid`,
`stop_reason` `end_turn`, `parsed` null after two refused
`find_label_row` calls with `section` the number `8.1` (M03 Unsure 23,
label-impact's), then prose; `latency_ms` 5805, 9496 ms wall; 5591 in,
296 out; the result grepped for `execute-api` and `us-west-2_`: no
match. A reading after the measurement; it does not reopen row 4 (M03
`rulings/pr4.md` 6, 22) and is recorded here and in the PR, not in a
ledger cell.

### What a reader can falsify

- The artifact `m04-gate-<sha>` on this PR's run holds `result.json`
  with `verdict: RED`, `answers_unrun: ["g-001"]`, `answers_disagreed:
  []`, `answers_differing: []`, `agent_disagreed: []`,
  `baseline_changed: false`, `unreadable: []` and `written_by_ci: true`,
  and `observations.json` with six observations. Download it and read
  it.
- In that `result.json`, `baseline.tag_commit` is `e94b76b…`,
  `baseline.diff_exit` is 0, and `served[0].observation` is the
  baseline's observation of g-001, equal in value to the hand-written
  answer the plant serves; the RED is `served[0].run_record.why` "run is
  null", nothing else.
- `git diff main --stat` on this PR touches `src/m04/`,
  `.github/workflows/m04.yml`, `milestones/README.md`,
  `milestones/M04/README.md` and `milestones/M04/rulings/pr2.md` only.
  `git diff main -- pages/ src/baseline/ src/m03/ pyproject.toml
  uv.lock` is empty. `git diff m00 --stat -- src/baseline/` is empty.
- Grep `secrets.`, `vars.` and `env:` in `.github/workflows/m04.yml`:
  no match. The baseline step's command is `gate.yml`'s with the output
  path changed: diff the two `run:` lines.
- In `src/m04/gate.py`, `RUN_RECORD` holds the seven names above;
  `run_record_check({"run": None})["has_record"]` is false;
  `page_block("baseline-answer")` matches the page's first block and
  `page_block("answer")` matches nothing in it.

### After this PR goes RED

The plant is lifted by the one change named under "The false state":
`run` filled with the record of the CI run of `src.baseline.run` that
produced the answer, the answer fields what that run wrote, `scripted`
false, the `PLANT` key removed, and the page rebuilt from it by a writer
in `src/m04/` (Unsure 9). Which PR carries the lift is ruled on reading
this PR's CI run, as M03's was at PR 2 (`milestones/M03/README.md`,
"After this PR goes RED"). The lift needs a run made by this
repository's CI and its record written into `pages/api/baseline.json`;
M03's path (b), an artifact the writer rebuilds the pages from by hand,
fits, since the `m04` workflow's own artifact already holds
`observations.json` with the run's `commit` and `started_at`. Proposed:
the lift is carried by PR 4, as M00's to M03's were; PR 3, if the cold
review of #24 finds anything, repairs and does not lift; if it finds
nothing, PR 3 is skipped. Ruled in `rulings/pr2.md` on reading the run.

**Ruled at PR 2, on reading run 41233100816 (Product).** The lift is
carried by PR 4, as M00's to M03's were. PR 3, if the cold review of #24
finds anything, repairs and does not lift; if it finds nothing, PR 3 is
skipped. The Measured cell takes the `main` run after #24 merges (M01
Unsure 23, ruled at M02 PR 1), which reads as run 41233100816 did on the
four lists and the freeze check; the baseline is deterministic. The
lift's path is M03's (b): the `m04` workflow's own artifact holds
`observations.json` with the run's `commit` and `started_at`, and a
writer in `src/m04/` rebuilds the file and the page from it by hand,
with the artifact and the run named in the record (`rulings/pr2.md` 13).

## Repair (PR 3, 2026-10-31)

PR 3 is the repair: what the cold review of PR 2 (#24) found, and nothing
else. The plant stands: `pages/api/baseline.json` serves g-001 with `run`
null and `pages/side-by-side.html` shows it under its illustration
banner, as at `a896442`; `git diff main -- pages/` is empty. Nothing here
lifts, and nothing here decides the row: the `main` run after #24 merged
is the measurement, and PR 4 fills the "Measured" cell from it
(`rulings/pr2.md` 13). The review found three defects in the gate's
verdict path and two wrong labels in its job summary, so this is PR 3.

### The `main` run after #24 merged, read at PR 3

[Run 41234548875](https://github.com/andaro74/pharmadelta/actions/runs/41234548875)
on `main` at `4d92676` (push, 2026-10-31 19:30 UTC), the run the Measured
cell cites (M01 Unsure 23). Read first in this session with `gh run
download`, before any edit; artifact
`m04-gate-4d926760c985e973bdd5d35f1c76f0db47660808`, its `result.json`
and `observations.json`:

| Field | Value |
|---|---|
| `verdict` | `RED`; `reason` "F4.1 holds: served answers g-001 carry no run record" |
| `answers_unrun` | `["g-001"]`: `served[0].run_record.why` "run is null" |
| `answers_disagreed` | `[]`: the page's baseline answer equals the file's entry as parsed JSON |
| `answers_differing` | `[]`: nothing compared, `not_compared` "no run record" |
| `agent_disagreed` | `[]`: the page's agent answer equals `pages/api/answers.json`'s entry |
| `baseline_changed` | `false`; `baseline.tag_commit` `e94b76b`, `baseline.baseline_commit` `df860b7`, `diff_exit` 0 |
| `unreadable` | `[]` |
| `observations` | `read` true, six ids `g-001` to `g-006`, `commit` `4d92676`, `dirty` false, `started_at` `2026-10-31T19:30:43+00:00`, `method` "keyword matching; see src/baseline/answer.py"; `observations.json` in the artifact holds the same six |
| `served[0].observation` | `lisinopril.8.1`, `201.57(c)(9)(i)`, `impacted` true, `owed` `follow-rld`, `escalate` false; recorded beside the unrun answer, decides nothing |
| `written_by_ci` | `true`; `commit` `4d92676`, `dirty` false; `ci.event` `push`, `ci.ref` `refs/heads/main`; exit 1; the `M04 gate` job failed |

Equals ledger row 5's expected output on every field the row names, and
equals run 41233100816 on the four lists, `baseline_changed`,
`unreadable` and the observation of g-001. The plant is not changed.

### Cold review of #24

Read on `main` at `4d92676`, before any edit: `src/m04/gate.py` line by
line against "Open detail (PR 2)" and `rulings/pr2.md` 1 to 13;
`.github/workflows/m04.yml` against `gate.yml` and `m03.yml`;
`pages/api/baseline.json` and `pages/side-by-side.html` as the gate reads
them; `src/baseline/run.py` for what a golden does to the runner; the PR
run 41233100816 and the main run 41234548875 against the "Observed"
table. Nine findings. Three are defects in the verdict path and are
repaired here; two are wrong labels in the job summary and are repaired
beside them; four are readings, named under Unsure (PR 3).

1. **Defect 1, repaired.** `run()` read `pages/api/baseline.json` first
   and let its `Unscorable` raise to `main`'s handler, so a baseline file
   that could not be read or parsed, or served no `answers` list, wrote
   the whole run UNSCORABLE before the page's agent column was read
   against `pages/api/answers.json`. With the page showing an agent
   answer the API does not serve, that run read UNSCORABLE with no
   `agent_disagreed` list, where `rulings/pr2.md` 6 says RED comes first
   and UNSCORABLE is for when nothing is RED. Reproduced at construction
   (cases 22 and 24 below). Not reachable on the plant or on a lift that
   serves a readable file.
2. **Defect 2, repaired.** `baseline_state()` caught
   `CalledProcessError` from git and nothing else. When git cannot be
   run at all (not on `PATH`, not executable) `subprocess.run` raises
   `FileNotFoundError` after the served files were read, and the run
   wrote UNSCORABLE with no `answers_unrun` list: the plant's RED turned
   UNSCORABLE. The same family as M03 PR 3's Defect 1: a failure after
   the served files were read overturning a RED. Reproduced at
   construction with git removed from `PATH` (case 25). Not reachable in
   CI as the workflow stands: `actions/checkout` needs git.
3. **Defect 3, repaired.** `write_result` wrote `result.json`, then
   appended the summary to `--summary`. A summary path that cannot be
   opened for append (the empty string, which `Path` reads as the
   current directory; a directory; an unwritable file) raised after
   `result.json` was written RED, and `main`'s handler then overwrote it
   with UNSCORABLE, exit 2. Reproduced at construction (cases 27 and
   28). In CI `GITHUB_STEP_SUMMARY` is set and writable; the path is
   reached when the workflow's command is run with it empty.
4. **Label, repaired.** The summary printed the tag's commit as the first
   seven characters of its fallback text, "not in ", when the tag was
   not in the checkout. Reproduced in a clone made with `--no-tags`. It
   now prints "not resolved".
5. **Label, repaired.** The summary's "page equal" column printed "not
   shown" for every served answer when the page's `baseline-answer`
   block could not be read, the same word it prints for a served answer
   the page does not show. It now prints "page not read" (case 29).
6. **Reading, Unsure 19.** The freeze check trusts the tag `m00` in the
   checkout. `tag_commit` is recorded (`e94b76b` in both CI runs) and
   not judged against the ledger's `e94b76b`; a moved tag would pass.
7. **Reading, Unsure 20.** The gate does not check the observations
   file's `commit` equals the checkout's. The workflow writes the file
   in the same job; both commits are recorded (`observations.commit`,
   `commit`) and equal in both CI runs.
8. **Reading, Unsure 21.** `run_record_check` reads a field as empty
   when it is null or the empty string. A field holding `0`, `false`,
   `[]` or `{}` counts as present; `written_by_ci` false is caught by
   its own check.
9. **Reading, Unsure 22.** `read_golden_question` returns None for a
   golden with no `question` string, and `compare` then reads the served
   `question` against None, so a served entry with no `question` key
   would read equal on that field. Not reachable in the same job:
   `src/baseline/run.py` reads `golden["question"]` and lowercases it,
   so such a golden stops the baseline before any observation is
   written, and `compare` is reached only with an observation of that
   id.

Also read, no finding: `compare()` returns on every shape of served
answer (null, object, string), of `answer_fields` (object, string,
absent) and of observation (present, absent, malformed) and raises on
none; `read_page`'s pattern matches the page's two blocks and no
`id="answer"` block; `m04.yml`'s baseline step is `gate.yml`'s command
with the output path changed, its gate step runs on
`!cancelled() && steps.baseline.outcome != 'skipped'` as `gate.yml`'s
scorer does, so a baseline crash still runs the gate (the plant reads
RED; a lift reads UNSCORABLE naming the observations file), the artifact
uploads on `if: always()` with `if-no-files-found: error`, `permissions`
is `contents: read`, `fetch-depth: 0` resolved the tag in both runs, and
no `secrets.`, `vars.` or `env:` appears; the two CI results equal the
"Observed" table on every field it names.

### The repair

`src/m04/gate.py` only, 61 lines added and 18 removed; the docstring
says what changed.

- **Defect 1.** `run` catches `Unscorable` from the baseline file as it
  already did from the page and the API, records it under `unreadable`,
  and goes on: `answers_unrun` and `answers_disagreed` are `[]` with no
  served list to read, the agent column is judged, the freeze check and
  the observations file are read and recorded. `result.json` gains
  `served_read` (true when the baseline file was read) beside `served`.
  With nothing RED the run is UNSCORABLE naming the file, as before.
- **Defect 2.** `baseline_state` catches `OSError` on each of its three
  git calls and returns `changed` None with `error` saying git could not
  be run; `git_error` writes the reason for either exception. The run
  then reads as a missing tag does: unreadable, RED first.
- **Defect 3.** `write_result` appends the summary inside a `try`; on
  `OSError` it prints why on stderr and `result.json` stands as written.
  `--summary ""` now means no summary.
- **Labels.** "not resolved" for a tag commit the gate has none of;
  "page not read" when the page's baseline block was not read.

The verdict on every input PR 2's construction run exercised is
unchanged (below). The fields compared, the run record's fields and
`m04.yml` are unchanged. No new dependency.

### Construction readings (not evidence, P4)

Run 2026-10-31 on this branch from the working tree, `written_by_ci`
false, `dirty` true. The observations file was written by `uv run python
-m src.baseline.run --out <scratch>/observations.json` from the tree at
`4d92676` with the gate uncommitted: six observations, g-001's equal to
the main run's. Thirty made-up pairs of files in the session's scratch
directory, built by one script and run against the gate before and
after the repair, not committed (M01 Unsure 21's reading: no test file).
No probe touched `src/baseline/`'s working tree (PR 2 Unsure 18: once,
done); the git-absent probe ran the gate with git removed from `PATH`,
and the missing-tag probe ran it in a clone made with `--no-tags`.

| Reading | Before the repair | After |
|---|---|---|
| cases 1 to 21: PR 2's twenty pairs, rebuilt, and the real pages | the plant: `RED`, `answers_unrun` `["g-001"]`, exit 1. The lifted entry: `GREEN`, exit 0. `written_by_ci` false, `artifact` missing, `run` a string: `RED`, `answers_unrun`. Page `owed` changed: `answers_unrun` and `answers_disagreed` `["g-001"]`. Page g-999: `answers_disagreed` `["g-999"]`. Agent `request_id` changed, plant and lifted: `agent_disagreed` `["g-001"]`. Lifted `owed` changed, `question` extended, `answer` null, g-999 with a record: `answers_differing`, the four reasons PR 2 recorded. No `--observations`, file missing, lifted: `UNSCORABLE`. Plant with the file missing: `RED`. Plant plus a string answer: `RED`, `unreadable` names g-002. String entry alone, zero served, lifted without the agent block: `UNSCORABLE`. Agent API malformed on the plant: `RED` | the same verdict, the same lists and the same exit on all twenty-one; `served_read` true on each, false on "zero served answers", whose `result.json` now holds the lists and `unreadable` instead of the error |
| case 22: baseline file not JSON, page agent `request_id` changed | `UNSCORABLE`, exit 2, `Unscorable` from `read_served`, no lists | `RED`, exit 1, `agent_disagreed` `["g-001"]`, `unreadable` names the baseline file, `served_read` false |
| case 23: baseline file not JSON, agent column equal | `UNSCORABLE`, exit 2, no lists | `UNSCORABLE`, exit 2, the lists `[]`, `unreadable` names the file |
| case 24: baseline file with `answers` a string, agent `request_id` changed | `UNSCORABLE`, no lists | `RED`, `agent_disagreed` `["g-001"]` |
| case 25: the plant, git not on `PATH` | `UNSCORABLE`, exit 2, `FileNotFoundError`, no `answers_unrun` | `RED`, exit 1, `answers_unrun` `["g-001"]`, `baseline_changed` null, `baseline.error` "the tag m00 could not be resolved: git could not be run: FileNotFoundError", `unreadable` names the freeze check |
| case 26: the lifted entry, git not on `PATH` | `UNSCORABLE`, `FileNotFoundError` | `UNSCORABLE`, exit 2, g-001 equal, `unreadable` names the freeze check: nothing RED, as `rulings/pr2.md` 6 reads a missing tag |
| cases 27 and 28: the plant, `--summary ""` and `--summary <a directory>` | `result.json` first written `RED` then overwritten `UNSCORABLE`, `PermissionError`, exit 2 | `RED`, exit 1, `result.json` as written; case 28 prints on stderr that the summary could not be appended |
| case 29: the lifted entry, page without its `baseline-answer` block | `UNSCORABLE`; the summary's page column "not shown" | `UNSCORABLE`, the same lists; the column "page not read" |
| case 30: the plant plus g-002 with `answer_fields` a string | `RED`, `answers_unrun` `["g-001"]`, `unreadable` names g-002 | the same |
| the clone made with `--no-tags`, the real pages | `RED`, `answers_unrun` `["g-001"]`, `baseline_changed` null, `unreadable` "the tag m00 is not in the checkout"; the summary line "against tag `m00` (`not in `)" | the same verdict and lists; the summary line "against tag `m00` (`not resolved`)" |
| the real pages with the gate's default paths, `--summary` a scratch file | | `RED`, `answers_unrun` `["g-001"]`, the other lists `[]`, `baseline_changed` false (tag `e94b76b`, `baseline_commit` `df860b7`, diff exit 0), `unreadable` `[]`, `served_read` true, exit 1; the summary appended |
| the M00 scorer on the same observations file | | `GREEN`, exit 0 |
| the M02 gate | | `GREEN`, `clauses_mismatched` `[]`, `rows_mismatched` `[]`, exit 0 |

### What this PR does not hold

- No lift. `git diff main -- pages/` is empty: `run` null, `scripted`
  true, the `PLANT` key and the illustration banner stand.
- No change to the verdict on any input PR 2's construction run
  exercised, to the fields compared, to the run record's fields, or to
  `.github/workflows/m04.yml`.
- No change to `src/baseline/` (P5; `git diff m00 --stat --
  src/baseline/` is empty), `src/m03/`, `src/gate/`, `src/ingest/`,
  `gate.yml`, `m01.yml`, `m02.yml`, `m03.yml`, `m03-lift.yml`,
  `goldens/`, `data/`, `pyproject.toml`, `uv.lock`, SPEC/00, CLAUDE.md,
  the README, or anything under `milestones/M00/` to `milestones/M03/`
  or `milestones/adoption/`.
- No construction probe touched `src/baseline/`'s working tree.
- No secret, no variable, no network in `m04.yml` or the gate.
- No "Measured" cell and no tag. Those are PR 4's.
- No number on a page. No word of SPEC/00 §11's six. No brand name.

### Expected CI result on this PR

The plant stands, so the run on this PR is expected to read as
41234548875 did: `RED`, `answers_unrun` `["g-001"]`, `answers_disagreed`
`[]`, `answers_differing` `[]`, `agent_disagreed` `[]`,
`baseline_changed` false, `unreadable` `[]`, `written_by_ci` true, exit
1, the `M04 gate` job failed. New in the result: `served_read` true. On
the same head the `M00 gate` is expected GREEN, the `M02 gate` GREEN, the
`M01 gate` PENDING and not required, and the `M03 gate` whatever shape
the door gives that day, recorded here and not in a ledger cell (M03
`rulings/pr4.md` 6, 22).

### What a reader can falsify

- `git diff main --stat` on this PR touches `src/m04/gate.py`,
  `milestones/README.md`, `milestones/M04/README.md` and
  `milestones/M04/rulings/pr3.md` only. `git diff main -- pages/
  src/baseline/ .github/` is empty.
- In `src/m04/gate.py`, `baseline_state` catches `OSError`;
  `write_result` appends the summary inside a `try`; `run` catches
  `Unscorable` from `read_served(args.api)`; `summary_markdown` holds
  the strings "not resolved" and "page not read".
- The artifact on this PR's run holds `result.json` with `verdict: RED`,
  `answers_unrun: ["g-001"]`, the other three lists `[]`,
  `baseline_changed: false`, `unreadable: []`, `written_by_ci: true` and
  `served_read: true`.
- `git diff m00 --stat -- src/baseline/` on this branch is empty.

### Observed (CI run, 2026-10-31)

The first run on this PR,
[41235927800](https://github.com/andaro74/pharmadelta/actions/runs/41235927800),
wrote the artifact `m04-gate-4dbe2931e631d079d1c7f5706abd8874ca5ab931`
(the sha is the pull request's merge ref; the branch head was
`9737262`). It holds `result.json` and `observations.json`, read with
`gh run download` in this session:

| Field | Value |
|---|---|
| `verdict` | `RED`; `reason` "F4.1 holds: served answers g-001 carry no run record" |
| `answers_unrun` | `["g-001"]`: `served[0].run_record.why` "run is null" |
| `answers_disagreed` | `[]`: the page's baseline answer equals the file's entry as parsed JSON |
| `answers_differing` | `[]`: nothing compared, `not_compared` "no run record" |
| `agent_disagreed` | `[]`: the page's agent answer equals `pages/api/answers.json`'s entry |
| `baseline_changed` | `false`; `baseline.tag_commit` `e94b76b`, `baseline.baseline_commit` `df860b7`, `diff_exit` 0 |
| `unreadable` | `[]` |
| `served_read` | `true`: the field this PR adds, present |
| `observations` | `read` true, six ids `g-001` to `g-006`, `commit` `4dbe293`, `dirty` false, `started_at` `2026-10-31T19:48:36+00:00`, `method` "keyword matching; see src/baseline/answer.py" |
| `served[0].observation` | `lisinopril.8.1`, `201.57(c)(9)(i)`, `impacted` true, `owed` `follow-rld`, `escalate` false, as the two earlier runs wrote; decides nothing |
| `written_by_ci` | `true`; `commit` `4dbe293`, `dirty` false; `ci.event` `pull_request`, `ci.ref` `refs/pull/25/merge`; exit 1; the `M04 gate` job failed. On the same head `M00 gate` passed ([41235927743](https://github.com/andaro74/pharmadelta/actions/runs/41235927743)), `M02 gate` passed ([41235927824](https://github.com/andaro74/pharmadelta/actions/runs/41235927824)), `M01 gate` is not required and reads as it did on `main` ([41235927762](https://github.com/andaro74/pharmadelta/actions/runs/41235927762)) |

Equals the expected result above on every field. The plant is still
named as ledger row 5 expects, and the repair changed nothing on it: the
RED is the missing run record and nothing else.

The `M03 gate` on the same head,
[41235927809](https://github.com/andaro74/pharmadelta/actions/runs/41235927809),
artifact `m03-gate-4dbe2931e631d079d1c7f5706abd8874ca5ab931`, read
`GREEN`: `answers_uncalled` `[]`, `answers_disagreed` `[]`,
`answers_differing` `[]`; sign-in as `pharmadelta` 200; the door 200,
`request_id` `GH_jUhHtvHcEP5Q=`, `stop_reason` `end_turn`, `parsed` null
after two refused `find_label_row` calls with `section` the number `8.1`
(M03 Unsure 23, label-impact's), then prose; `latency_ms` 5841, 9908 ms
wall; 5591 in, 296 out; the result grepped for `execute-api` and
`us-west-2_`: no match. The same shape as run 41233100879 on #24. A
reading after the measurement; it does not reopen row 4 (M03
`rulings/pr4.md` 6, 22) and is recorded here and in the PR, not in a
ledger cell.

## Close (PR 4, 2026-10-31)

PR 4 closes the milestone at the cap, 4 / 4. It carries the lift, fills
the "Measured" cell from a CI-written result and writes the row's state,
rules or carries by name every open Unsure item of PR 1, PR 2 and PR 3,
and adds `rulings/pr4.md`. The tag `m04` goes on its merge commit after
the run on `main` is read. Nothing here decides the row: the `main` run
after #24 merged, 41234548875, is the measurement, and this PR reads it
again before writing the cell. The gate, `src/m04/gate.py` and
`m04.yml`, is not changed.

### Precondition, read at open

#25 merged at `36c453a` on 2026-10-31; `main` contains `5f03743` and
holds `src/m04/gate.py` as repaired at `9737262`. Tags `m00` `e94b76b`,
`m01` `c60599e`, `m02` `ab72b9d`, `m03` `9932776`, read with `git
rev-parse <tag>^{commit}`; no `m04` tag. The `main` run after #25
merged,
[41250971500](https://github.com/andaro74/pharmadelta/actions/runs/41250971500)
on `36c453a` (push, 2026-10-31 23:04 UTC), had completed. Downloaded
with `gh run download` before any edit; artifact
`m04-gate-36c453aa306377137a324e9a1f340af1fb3c7e09`, its `result.json`
and `observations.json`: `RED`, `answers_unrun` `["g-001"]`,
`answers_disagreed` `[]`, `answers_differing` `[]`, `agent_disagreed`
`[]`, `baseline_changed` false, `unreadable` `[]`, `served_read` true,
`written_by_ci` true, `ci.event` `push`, `ci.ref` `refs/heads/main`;
`observations` read, six ids, `commit` `36c453a`, `dirty` false,
`started_at` `2026-10-31T23:04:49+00:00`; the observation of g-001
`lisinopril.8.1`, `201.57(c)(9)(i)`, `impacted` true, `owed`
`follow-rld`, `escalate` false. The plant stood: `git diff a896442
36c453a -- pages/` was empty.

### The runs, read again at PR 4

All three downloaded with `gh run download` in this session before the
cell was written. Every field the ledger row names, side by side:

| Field | `main` run [41234548875](https://github.com/andaro74/pharmadelta/actions/runs/41234548875) (the Measured cell) | PR run [41233100816](https://github.com/andaro74/pharmadelta/actions/runs/41233100816) | `main` run [41250971500](https://github.com/andaro74/pharmadelta/actions/runs/41250971500) (the lift's record) |
|---|---|---|---|
| `commit` | `4d92676`, `main` after #24 merged, `event` `push`, `ref` `refs/heads/main` | `a724249`, merge ref of #24, `event` `pull_request` | `36c453a`, `main` after #25 merged, `event` `push`, `ref` `refs/heads/main` |
| artifact | `m04-gate-4d926760c985e973bdd5d35f1c76f0db47660808` | `m04-gate-a7242498e5bd9fc47e714271df8ee604c04deca4` | `m04-gate-36c453aa306377137a324e9a1f340af1fb3c7e09` |
| `verdict` | `RED` | `RED` | `RED` |
| `answers_unrun` | `["g-001"]`, "run is null" | `["g-001"]`, "run is null" | `["g-001"]`, "run is null" |
| `answers_disagreed` | `[]` | `[]` | `[]` |
| `answers_differing` | `[]` | `[]` | `[]` |
| `agent_disagreed` | `[]` | `[]` | `[]` |
| `baseline_changed` | `false`; tag `e94b76b`, `baseline_commit` `df860b7`, diff exit 0 | the same | the same |
| `unreadable` | `[]` | `[]` | `[]` |
| `served_read` | not in the result (PR 3 added it) | not in the result | `true` |
| `written_by_ci` | `true` | `true` | `true` |
| `observations.commit`, `started_at` | `4d92676`, `2026-10-31T19:30:43+00:00` | `a724249`, `2026-10-31T19:12:26+00:00` | `36c453a`, `2026-10-31T23:04:49+00:00` |
| the observation of g-001 (decides nothing) | `lisinopril.8.1`, `201.57(c)(9)(i)`, `impacted` true, `owed` `follow-rld`, `escalate` false | the same | the same |

All three equal row 5's expected gate output on every field it names.

### Measured

The cell cites the run on `main` after #24 merged, 41234548875 on
`4d92676` (M01 Unsure 23, ruled at M02 PR 1; `rulings/pr2.md` 13;
`rulings/pr3.md` 4), with the PR run 41233100816 named beside it as the
one read at the time. It is written in the ledger's words, as rows 0 to
4 are. The cell equals the expected gate output written at open, so
under the ledger's rule row 5 is GREEN and "PRs used / cap" is 4 / 4.
The lift's run (below) is recorded here, not in the cell: it is the
record the page carries and does not decide the row.

### The lift path (rulings/pr2.md 13, carried at PR 3)

M03's path (b), as ruled at PR 2 on reading run 41233100816: a CI run's
artifact and a writer in `src/m04/` that rebuilds the file and the page
from it by hand, with the artifact and the run named in the record. No
lift workflow: the `m04` workflow's own artifact already holds
`observations.json`, what `uv run python -m src.baseline.run` wrote in
CI, beside the gate's `result.json`, so the run that produces the
ordinary assistant's answer is the gate's own baseline step on `main`.
Every workflow keeps `permissions: contents: read`; `m04.yml` is
unchanged and reads no secret, no variable and no `env`.

- `src/m04/lift.py write --from <dir>` (M04's own module, Unsure 9):
  by hand, from the downloaded artifact. Reads `observations.json` (the
  observation of each golden, `commit`, `started_at`, `method`) and
  `result.json` beside it (`ci.run_url`, `ci.sha`, `written_by_ci`,
  `baseline.baseline_commit`), because the observations file alone
  names no run (Unsure 26). Refuses an artifact whose `result.json`
  says CI did not write it, whose two files name different commits,
  whose observations were written from a dirty tree, or that holds no
  observation of a served id. Rebuilds `pages/api/baseline.json` and
  `pages/side-by-side.html`: the served ids are the ones the file
  already serves; each `question` is its golden's (Unsure 28);
  `answer` is the run's observation, verbatim; `row` and `clause` are
  copied from `data/` at its last commit when the table holds the
  `table_row` and the clauses hold the `clause_id`, else null; `run`
  is the seven-field record (`rulings/pr2.md` 1), every value the
  artifact's and none this machine's; `scripted` false; no `PLANT`;
  under `lift` the run and the artifact. The page shows an answer only
  with its row and its clause (SPEC/00 §11); the agent column is the
  entry `pages/api/answers.json` serves, rendered from that file,
  unchanged. The rebuild is deterministic and writes LF on every
  platform (M03 Unsure 33).

Construction, not evidence (P4): `write` on the artifact of run
41250971500 wrote the two pages; a second `write` of the same artifact
into the scratch directory was byte-identical to them. `git ls-files
--eol` reads `i/lf w/lf` on both pages and on `lift.py`. The gate on
the rebuilt pages, with an observations file written by `uv run python
-m src.baseline.run` from the working tree at `36c453a` with the lift
uncommitted: `GREEN`, `answers_unrun` `[]`, `answers_disagreed` `[]`,
`answers_differing` `[]`, `agent_disagreed` `[]`, `baseline_changed`
false (tag `e94b76b`, `baseline_commit` `df860b7`, diff exit 0),
`unreadable` `[]`, `served_read` true, g-001 "equal", exit 0;
`written_by_ci` false, dirty tree. The M00 scorer on the same
observations file `GREEN`, exit 0. The M02 gate `GREEN`,
`clauses_mismatched` `[]`, `rows_mismatched` `[]`, exit 0. `git diff
m00 --stat -- src/baseline/` is empty; no probe touched the control's
working tree (PR 3 `rulings/pr3.md` 12). None of these readings
decides anything.

### The lift

The first commit of this PR: the one change "The false state" named,
written by `lift.py write` from the artifact of CI run 41250971500,
the `main` run after #25 merged (Unsure 27). In `pages/api/baseline.json`
the entry `g-001` now carries `run` with `run_url` that run, `artifact`
`m04-gate-36c453aa306377137a324e9a1f340af1fb3c7e09`, `commit`
`36c453a…`, `baseline_commit` `df860b7…`, `started_at`
`2026-10-31T23:04:49+00:00`, `method` "keyword matching; see
src/baseline/answer.py", `written_by_ci` true; the answer fields what
that run's observation holds (`lisinopril.8.1`, `201.57(c)(9)(i)`,
`impacted` true, `owed` `follow-rld`, `escalate` false, equal in value
to the hand-written answer the plant served, as the M00 README said the
baseline writes for g-001); `scripted` false; no `PLANT` key; the file
names `data_commit` `595dd68` and, under `lift`, the run and the
artifact it was written from. `pages/side-by-side.html` shows, in the
ordinary-assistant column, the answer with its row and its clause as
before, then the run record with `run_url` as a link, and the same
object in its `id="baseline-answer"` block; the illustration banner is
gone, because nothing scripted remains (P8); the header names the run
and the artifact. The agent column is the entry `pages/api/answers.json`
serves, in its `id="agent-answer"` block, unchanged: `git diff a896442
-- pages/side-by-side.html` touches no line of it. The page adds a
table of what the three answer fields mean (`milestones/M00/fields.md`,
the detail page's words) and the footer now names the run record beside
the call record (Unsure 31). `git diff a896442 -- pages/` touches the
two files and nothing else; `pages/detail.html` and
`pages/api/answers.json` are unchanged. No number on the page is new
but the run record's `started_at` and commits, which are the CI run's,
linked.

### What the gate on this PR can read

The gate compares against its own run of the baseline in the same job
(`rulings/pr2.md` 7), and the baseline has no model and no randomness,
so the run on this PR is expected `GREEN`: `answers_unrun` `[]`,
`answers_disagreed` `[]`, `answers_differing` `[]`, `agent_disagreed`
`[]`, `baseline_changed` false, `unreadable` `[]`, `served_read` true,
`written_by_ci` true, exit 0, the first pass of this gate. RED with
`answers_differing` `["g-001"]` would mean `data/` or `goldens/`
changed between the lift's run and the gate's, which this PR does not
do; UNSCORABLE would mean the baseline could not run or the tag did
not resolve. Any of the three is a reading after the measurement and
leaves the cell as it is. On the same head the `M00 gate` is expected
GREEN, the `M02 gate` GREEN, the `M01 gate` PENDING and not required,
and the `M03 gate` whatever shape the door gives that day (on `main` at
`36c453a`, run
[41250971475](https://github.com/andaro74/pharmadelta/actions/runs/41250971475)
read `RED`, `answers_differing` `["g-001"]`, the served null against a
`parsed` object with `table_row` null and `clause_id`
`21 CFR 201.57(c)(9)(i)`, `end_turn`, `request_id` `GIcTGjL5vHcESmg=`;
a reading after M03's measurement, M03 `rulings/pr4.md` 6, 22).

### Observed (CI runs, 2026-10-31)

The first run on this PR,
[41252104790](https://github.com/andaro74/pharmadelta/actions/runs/41252104790),
on the merge ref `5ac7e90` (branch head `0d6f696`, the close commit),
artifact `m04-gate-5ac7e906800d5407b4d8d270e5bf9c7b93d4d1f4`, its
`result.json` and `observations.json`, read with `gh run download` in
this session:

| Field | Value |
|---|---|
| `verdict` | `GREEN`; `reason` "F4.1 does not hold: every served answer carries a run record written by CI, is shown as served and equals the run's observation, every agent answer shown is the public API's, and src/baseline/ equals tag m00" |
| `answers_unrun` | `[]`: `served[0].run_record` "a run record written by CI, every field present" |
| `answers_disagreed` | `[]`: the page's baseline answer equals the file's entry as parsed JSON |
| `answers_differing` | `[]`: `comparison` "all equal" on `question` (the golden's), `table_row`, `clause_id` and the three answer fields |
| `agent_disagreed` | `[]`: the page's agent answer equals `pages/api/answers.json`'s entry |
| `baseline_changed` | `false`; `baseline.tag_commit` `e94b76b`, `baseline.baseline_commit` `df860b7`, `diff_exit` 0 |
| `unreadable` | `[]` |
| `served_read` | `true` |
| `observations` | `read` true, six ids `g-001` to `g-006`, `commit` `5ac7e90`, `dirty` false, `started_at` `2026-10-31T23:20:32+00:00`, `method` "keyword matching; see src/baseline/answer.py" |
| `written_by_ci` | `true`; `commit` `5ac7e90`, `dirty` false; `ci.event` `pull_request`, `ci.ref` `refs/pull/26/merge`; exit 0; the `M04 gate` job passed, the first pass of this gate. On the same head `M00 gate` passed ([41252104879](https://github.com/andaro74/pharmadelta/actions/runs/41252104879)), `M02 gate` passed ([41252104821](https://github.com/andaro74/pharmadelta/actions/runs/41252104821)), `M01 gate` is not required and reads as it does on `main` ([41252104888](https://github.com/andaro74/pharmadelta/actions/runs/41252104888)) |

Equals "What the gate on this PR can read" on every field. The served
answer is the record's run's observation, and the gate's own run in
this job wrote the same one. A reading after the measurement; the cell
above is the `main` run on the plant and is not changed by it.

The `M03 gate` on the same head,
[41252104785](https://github.com/andaro74/pharmadelta/actions/runs/41252104785),
artifact `m03-gate-5ac7e906800d5407b4d8d270e5bf9c7b93d4d1f4`, read
`GREEN`: `answers_uncalled` `[]`, `answers_disagreed` `[]`,
`answers_differing` `[]`; sign-in as `pharmadelta` 200; the door 200,
`request_id` `GIelcidGPHcEQ1w=`, `stop_reason` `tool_use`, `parsed` null
after three refused `find_label_row` calls with `section` the number
`8.1` (M03 Unsure 23, label-impact's); `latency_ms` 4827, 8521 ms wall;
5591 in, 279 out; the result grepped for `execute-api` and `us-west-2_`:
no match. The served null equals the run's null. A reading after M03's
measurement; it does not reopen row 4 (M03 `rulings/pr4.md` 6, 22) and
is recorded here and in the PR, not in a ledger cell. Runs on later
commits of this PR, if any, are named in the PR's comments.

### Rulings carried

| # | Ruled |
|---|---|
| PR 2's 13, PR 3's 14 | Product: the lift is carried by PR 4, this PR, by path (b); the Measured cell takes the `main` run after #24 merged. Done as ruled. |
| PR 2's 1 (Unsure 5) | Engineering: the lift writes the seven fields as fixed; the gate names the entry run. |
| PR 3's 12 (PR 2 Unsure 18) | Threshold Owner: no PR 4 probe touched `src/baseline/`'s working tree. Held. |

### What this PR does not hold

- No change to `src/m04/gate.py`, `.github/workflows/m04.yml` (no
  secret, no variable, no `env`, no `contents: write`), `gate.yml`,
  `m01.yml`, `m02.yml`, `m03.yml`, `m03-lift.yml`, `src/baseline/`
  (P5; `git diff m00 --stat -- src/baseline/` is empty), `src/m03/`,
  `src/gate/`, `src/ingest/`, `src/m01/`, `goldens/`, `data/`,
  `pyproject.toml`, `uv.lock`, SPEC/00, CLAUDE.md, the README, or
  anything under `milestones/M00/` to `milestones/M03/` or
  `milestones/adoption/`. No new dependency: `lift.py` imports the
  standard library, PyYAML and `src.m04.gate`.
- No edit to the expected gate output written at open, to
  `rulings/pr1.md`, `pr2.md` or `pr3.md`.
- No third column (Unsure 6). No GitHub Pages deploy (Unsure 2; 404
  again on 2026-10-31).
- No network in the lift. Grep `https://` under `src/m04/`: no match;
  the run URL in the record is the artifact's.
- No scripted content on a page: grep `PLANT`, `Illustration`,
  `class="scripted"` and `"scripted": true` under `pages/`: no match.
- No answer on a page without its row and its clause. No number on a
  page that is not the row's or the clause's own data or a CI run's
  record, linked. No word of SPEC/00 §11's six. No brand name.
- No change to label-impact or to agentkeel. No tag until this PR's
  run on `main` is read. No fifth PR.

### What a reader can falsify

- `git diff main --stat` on this PR touches `src/m04/lift.py`,
  `pages/api/baseline.json`, `pages/side-by-side.html`,
  `milestones/README.md`, `milestones/M04/README.md` and
  `milestones/M04/rulings/pr4.md` only. `git diff a896442 -- pages/`
  touches the two pages only, and `git diff a896442 main -- pages/`
  is empty.
- `gh run download 41250971500`, then `uv run python -m src.m04.lift
  write --from <dir>/m04-gate-36c453aa306377137a324e9a1f340af1fb3c7e09
  --api <a> --page <p>`: the two files written equal
  `pages/api/baseline.json` and `pages/side-by-side.html` at this PR's
  head byte for byte.
- In `pages/api/baseline.json`, `grep PLANT` matches nothing,
  `scripted` is false, `run` holds the seven fields with
  `written_by_ci` true, and `run.run_url` opens run 41250971500, whose
  artifact's `observations.json` holds the same `started_at`, `commit`
  and observation of g-001, and whose `result.json` holds the same
  `baseline.baseline_commit`.
- The `main` run's artifact
  `m04-gate-4d926760c985e973bdd5d35f1c76f0db47660808` holds
  `result.json` with `verdict: RED` and the lists in the cell. Download
  it and read it; the ledger's cell is that file.
- The artifact on this PR's run holds `verdict: GREEN`, every list
  `[]`, `baseline_changed: false`, `served_read: true` and
  `served[0].comparison.equal: true`.
- The page carries none of "validated", "compliant", "Part 11",
  "governed", "secure" or "proven", no brand name and no scripted
  banner; its `id="agent-answer"` block parses to the same object as
  `pages/api/answers.json`'s entry.
- `git ls-files --eol` reads `i/lf w/lf` on every file this PR
  changes.

### After this PR

Tag `m04` on the merge commit, as `m00` to `m03` were tagged, after
this PR's run on `main` is read with `gh run download`. That run's
verdict is recorded in the tag's message and in a comment on #26, not
in a commit: the milestone's four PRs are used and a fifth is a RED
close (Unsure 29). Whatever it reads, the cell stands. Row 5 is GREEN.
From the merge the ordinary assistant on the side-by-side page is a
real run of the frozen baseline, labelled so (SPEC/00 §11); until then
the page on `main` is the illustration.

Carried by name: Unsure 2 (GitHub Pages) to M05, with the constraint
PR 1 stated; Unsure 16 (the gate as a required check) with M02's and
M03's 16 to the owner's settings, outside any milestone; M03's 6 and
23 stay label-impact's (the door's reading on this PR's runs is named
in the PR, not in a cell).

## Unsure (PR 4)

Numbering continues from PR 3's. Each needs a seat's ruling. None
changes the measurement.

| # | Item | Seat |
|---|---|---|
| 25 | The ruling file names this PR as #26, the next number on this repository. **Ruled at PR 4** (`rulings/pr4.md` 18): #26. | Product |
| 26 | The writer builds the run record from two files of one artifact: `observations.json` for the answer, `commit`, `started_at` and `method`, and the gate's own `result.json` beside it for `run_url`, `written_by_ci` and `baseline_commit`, because the observations file names no run. It refuses when the two name different commits. The alternative, typing the run URL by hand, puts a hand-written value in the record. **Ruled at PR 4** (`rulings/pr4.md` 3): as built; every value in the record is the artifact's. | Engineering |
| 27 | The record names run 41250971500, the `main` run after #25 merged, as the session's instruction set; the Measured cell cites 41234548875, the `main` run after #24 merged. Two runs: the measurement on the plant and the run the page carries. The three runs wrote the same observation of g-001. **Ruled at PR 4** (`rulings/pr4.md` 5): as built; the cell and the record name different runs for different reasons. | Product |
| 28 | The served ids come from the `pages/api/baseline.json` the writer finds (g-001), and each `question` from its golden, since the artifact holds neither; `row` and `clause` from `data/` at its last commit. A reader's rebuild therefore reads the checkout for the ids, the questions and the data, and the artifact for the answer and the record. **Ruled at PR 4** (`rulings/pr4.md` 4): as built, as M03's writer read `data/`; the gate compares the served question with the golden's, so the golden is the question's source. | Engineering, Data Owner |
| 29 | This PR's run on `main` after it merges is read before the tag is placed, and its verdict is written in the tag's message and in a comment on #26, not in the README (M03 Unsure 31's shape). **Ruled at PR 4** (`rulings/pr4.md` 19): as stated. | Product |
| 30 | The pages were written on a Windows machine by the writer with LF pinned (M03 Unsure 33); `git ls-files --eol` reads `i/lf w/lf` and a second write is byte-identical. Recorded so a reader on another platform knows what to expect. **Ruled at PR 4** (`rulings/pr4.md` 3): recorded. | Engineering |
| 31 | The page's diff against the plant holds, beyond the one change named, a header paragraph naming the run and the artifact, a table of what the three answer fields mean, and the footer's wording. None is an answer, a number or a banner. Whether they are within "the one change". **Ruled at PR 4** (`rulings/pr4.md` 6): within it; each says where the answer came from or what a field means, and none changes what the gate reads. | Product |

## Unsure (PR 3)

Numbering continues from PR 2's. Each needs a seat's ruling. None blocks
the measurement, which is in.

| # | Item | Seat |
|---|---|---|
| 19 | The freeze check trusts the tag `m00` in the checkout and records its commit; it does not judge `tag_commit` against the ledger's `e94b76b`. A tag moved to another commit would read `baseline_changed` false against that commit. Both CI runs read `e94b76b`. Proposed: recorded, not judged; a reader checks the seven characters. The alternative pins the commit in the gate, a gate change for a repair slot that this PR did not make unruled. **Ruled at PR 4** (`rulings/pr4.md` 13): recorded, not judged; three CI runs read `e94b76b`. | Threshold Owner, Engineering |
| 20 | The gate does not check the observations file's `commit` equals the checkout's `commit`. The workflow writes the file in the same job from the same checkout, and both are recorded and equal in both CI runs. Proposed: recorded, not judged, as built. **Ruled at PR 4** (`rulings/pr4.md` 14): as built; the lift's writer refuses an artifact whose two files name different commits. | Engineering |
| 21 | `run_record_check` reads a field as empty when it is null or the empty string only; `0`, `false`, `[]` and `{}` count as present (`written_by_ci` false is caught by its own check). Proposed: as built; the lift writes strings and one boolean, and a reader reads the record. **Ruled at PR 4** (`rulings/pr4.md` 15): as built; the lift wrote six strings and `true`. | Engineering |
| 22 | A golden with no `question` string reads None from `read_golden_question`, and `compare` then reads the served `question` against None. Unreachable in one job (`src/baseline/run.py` stops on such a golden before any observation is written). Proposed: not changed; the baseline is frozen and the gate compares only with an observation. **Ruled at PR 4** (`rulings/pr4.md` 16): not changed. | Engineering, Data Owner |
| 23 | Defect 1's reading: a baseline file that cannot be read leaves the agent column judged, so a page agent answer the API does not serve reads RED beside an unreadable baseline file. Built from `rulings/pr2.md` 6's letter (RED first; UNSCORABLE when nothing is RED). The alternative reads an unreadable served file as "nothing can be judged". The seats confirm at PR 4. **Ruled at PR 4** (`rulings/pr4.md` 17): confirmed as built. | Product, Engineering |
| 24 | The ruling file names this PR as #25, the next number on this repository. **Ruled at PR 4** (`rulings/pr4.md` 18): #25. | Product |

## Unsure (PR 2)

Numbering continues from PR 1's. Each needs a seat's ruling. None blocks
the measurement.

| # | Item | Seat |
|---|---|---|
| 10 | The ruling file names this PR as #24, the next number on this repository. **Ruled at PR 2** (`rulings/pr2.md` 12): #24. | Product |
| 11 | A served baseline answer the page does not show is not named, as the M03 gate does not name a served answer the detail page does not show (M03 Unsure 25's reading). F4.1's third arm is "the page shows an answer the file does not serve", the other direction. With one served answer, shown, the two readings agree. | Product, Engineering |
| 12 | A served answer with a run record whose `id` has no golden under `goldens/`, or no observation in the run, reads differing, not UNSCORABLE: the baseline runs over `goldens/`, so nothing it writes could have produced that answer. The alternative reads it as "not read". Built: differing. | Product, Engineering |
| 13 | What the gate verifies of the run record from here: presence and non-emptiness of the seven fields and `written_by_ci` true, as M03's gate verified its call record (M03 `rulings/pr2.md` 7). `baseline_commit` is checkable against the checkout's last baseline commit, which the gate records under `baseline.baseline_commit` and does not judge; `run_url` and `artifact` need GitHub's API, which the gate does not read (no network). Whether the lift PR adds the `baseline_commit` check to the verdict. Proposed: recorded, not judged, at PR 2. **Carried at PR 3** (`rulings/pr3.md` 7). **Ruled at PR 4** (`rulings/pr4.md` 11): the lift does not add the check; the gate is unchanged; the record's `baseline_commit` is the artifact's `df860b7…`, equal to what the gate records. | Engineering, Threshold Owner |
| 14 | When the tag `m00` is not in the checkout, `baseline_changed` is null and the run reads UNSCORABLE unless something is RED, the reading "a reading could not be made". The alternative, RED, would name the checkout, not the control. Built: UNSCORABLE. `fetch-depth: 0` in the workflow fetches the tags; the CI run on this PR confirms. **Read at PR 2** (run 41233100816): the tag resolved to `e94b76b` on the merge ref, `baseline_changed` false. The reading on a missing tag stays proposed. | Threshold Owner, Engineering |
| 15 | Equality is against the gate's own run of the baseline in the same job, not against the run the record names (M03 `rulings/pr2.md` 4's reading). The baseline is deterministic at fixed `data/` and `goldens/`, so the two runs write the same observation unless `data/` or `goldens/` changed between them, which `answers_differing` then names. Built so. | Product, Data Owner, Threshold Owner |
| 16 | Whether `M04 gate` is made a required check on `main`, as M02's 16 and M03's 16 asked for theirs; both carried to the owner's settings, outside any milestone. Not changed here. **Carried at PR 4** (`rulings/pr4.md` 12): with M02's and M03's 16, the owner's setting. | Security, Product |
| 17 | The artifact `m04-gate-<sha>` holds `observations.json`, the same content `m00-gate-<sha>`'s artifact holds on the same head. A second copy, so the gate's artifact holds what the gate compared. Proposed: keep. | Engineering |
| 18 | The construction probe of the freeze arm appended one line to `src/baseline/answer.py` in the working tree and reverted it in the same command, never staged or committed; `git diff m00 --stat -- src/baseline/` is empty after. Whether a construction probe may touch the control's working tree at all under P5, which freezes the repository's `src/baseline/`. Proposed: allowed once, recorded; no further probe touches it. | Threshold Owner |

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant.

| # | Item | Seat |
|---|---|---|
| 1 | What "live" means: (a) a CI run of the frozen baseline whose observation the page serves with its run record, M03's shape for the agent; or (b) a run at page view, which GitHub Pages cannot do and which would port the baseline out of `src/baseline/` (P5). Proposed: (a). The plant is false under either. **Carried at PR 2** (`rulings/pr2.md` 11): the gate is built under (a); Product rules at PR 4. **Ruled at PR 4** (`rulings/pr4.md` 7): (a). | Product |
| 2 | M03's Unsure 2, carried here by name (`milestones/M03/rulings/pr4.md` 7). GitHub Pages is not enabled (404 on 2026-10-25 and 2026-10-31). Enabling it is a repository setting the owner makes by hand. Deploy-from-branch serves the branch root or `/docs` only, so `pages/` would need an Actions deploy workflow or a move; `docs/` holds the ADR. M04 is the first milestone that serves a page to a visitor, but row 5's claim is measurable with the page readable in the repository, as M03's was. Proposed: "public" means readable in the repository through PR 4; enabling Pages is ruled by name at PR 4 or carried to M05, and is not a PR of this cap. **Carried at PR 2** (`rulings/pr2.md` 11): still 404; "public" means readable in the repository through PR 4, as proposed. **Carried at PR 4** (`rulings/pr4.md` 8) to M05 by name; at M04 "public" means readable in the repository. | Product, Security |
| 3 | Where the ordinary assistant's served answers live: `pages/api/baseline.json`, beside the agent's `answers.json`, a second file the M03 gate does not read. Whether it is part of "the public API" of row 4 (which serves agent answers only) or a separate served file. Proposed: a separate served file, named in the row. **Ruled at PR 2** (`rulings/pr2.md` 3): a separate served file, named in the row; the M03 gate does not read it and row 4 is not touched. | Product, Tool Owner |
| 4 | The M03 gate and the new page. `src/m03/gate.py` reads `pages/detail.html` and `pages/api/answers.json` by path and globs nothing; F3.1's "the page" is the detail page. The side-by-side page's agent column copies the API's entry. Whether F3.1 reaches the new page. Proposed: it does not; M04's gate carries `agent_disagreed` for the new page; `m03.yml` and `gate.py` are not edited. **Ruled at PR 2** (`rulings/pr2.md` 4): F3.1 does not reach the new page; M04's gate carries `agent_disagreed`; `m03.yml` and `src/m03/gate.py` are not edited. | Product, Engineering |
| 5 | The run record's fields and what the gate verifies from here: `run_url` is readable through GitHub's API; `artifact` is readable for 90 days; `baseline_commit` is checkable against `m00` in the checkout. Proposed under "Carried to PR 2"; fixed at PR 2. **Ruled at PR 2** (`rulings/pr2.md` 1): fixed as the seven fields under "The run record's fields (Unsure 5, ruled)"; the gate names an answer unrun when any is missing or empty or `written_by_ci` is not true. | Engineering |
| 6 | Option C (M00 `rulings/pr2.md` 2): a labelled live model panel beside the control. Proposed: not at M04. The row's claim is the baseline; this repository holds no model credential; a third column would be scripted or would need a new secret, and either is another milestone's claim. **Carried at PR 2** (`rulings/pr2.md` 11): no third column at M04, as proposed; ruled by name at PR 4. **Ruled at PR 4** (`rulings/pr4.md` 9): no third column at M04. | Product, Threshold Owner |
| 7 | Whether the gate checks `src/baseline/` equals its state at `m00` and names `baseline_changed` (P5). Proposed: yes; "runs the baseline" means the control, and the check is one `git diff`. **Ruled at PR 2** (`rulings/pr2.md` 2): yes; `git diff m00 --quiet -- src/baseline/` in the checkout, `baseline_changed` true on exit 1, with the tag's commit recorded. | Threshold Owner, Engineering |
| 8 | The ruling file names this PR as #23, the next number on this repository. **Ruled at PR 2** (`rulings/pr2.md` 5): PR 1 was #23. | Product |
| 9 | The side-by-side page is written by hand at PR 1 and will be rebuilt by a writer at the lift, as M03's pages are by `src/m03/lift.py`. Whether the writer is M04's own module (`src/m04/`) or an extension of M03's. Proposed: M04's own, decided at the lift PR. **Carried at PR 2** (`rulings/pr2.md` 11): M04's own module, decided at the lift PR, as proposed. **Ruled at PR 4** (`rulings/pr4.md` 10): M04's own, `src/m04/lift.py`. | Engineering |
