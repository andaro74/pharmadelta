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
| Measured | |
| PRs used / cap | 1 / 4 |
| State | OPEN |

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

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant.

| # | Item | Seat |
|---|---|---|
| 1 | What "live" means: (a) a CI run of the frozen baseline whose observation the page serves with its run record, M03's shape for the agent; or (b) a run at page view, which GitHub Pages cannot do and which would port the baseline out of `src/baseline/` (P5). Proposed: (a). The plant is false under either. | Product |
| 2 | M03's Unsure 2, carried here by name (`milestones/M03/rulings/pr4.md` 7). GitHub Pages is not enabled (404 on 2026-10-25 and 2026-10-31). Enabling it is a repository setting the owner makes by hand. Deploy-from-branch serves the branch root or `/docs` only, so `pages/` would need an Actions deploy workflow or a move; `docs/` holds the ADR. M04 is the first milestone that serves a page to a visitor, but row 5's claim is measurable with the page readable in the repository, as M03's was. Proposed: "public" means readable in the repository through PR 4; enabling Pages is ruled by name at PR 4 or carried to M05, and is not a PR of this cap. | Product, Security |
| 3 | Where the ordinary assistant's served answers live: `pages/api/baseline.json`, beside the agent's `answers.json`, a second file the M03 gate does not read. Whether it is part of "the public API" of row 4 (which serves agent answers only) or a separate served file. Proposed: a separate served file, named in the row. | Product, Tool Owner |
| 4 | The M03 gate and the new page. `src/m03/gate.py` reads `pages/detail.html` and `pages/api/answers.json` by path and globs nothing; F3.1's "the page" is the detail page. The side-by-side page's agent column copies the API's entry. Whether F3.1 reaches the new page. Proposed: it does not; M04's gate carries `agent_disagreed` for the new page; `m03.yml` and `gate.py` are not edited. | Product, Engineering |
| 5 | The run record's fields and what the gate verifies from here: `run_url` is readable through GitHub's API; `artifact` is readable for 90 days; `baseline_commit` is checkable against `m00` in the checkout. Proposed under "Carried to PR 2"; fixed at PR 2. | Engineering |
| 6 | Option C (M00 `rulings/pr2.md` 2): a labelled live model panel beside the control. Proposed: not at M04. The row's claim is the baseline; this repository holds no model credential; a third column would be scripted or would need a new secret, and either is another milestone's claim. | Product, Threshold Owner |
| 7 | Whether the gate checks `src/baseline/` equals its state at `m00` and names `baseline_changed` (P5). Proposed: yes; "runs the baseline" means the control, and the check is one `git diff`. | Threshold Owner, Engineering |
| 8 | The ruling file names this PR as #23, the next number on this repository. | Product |
| 9 | The side-by-side page is written by hand at PR 1 and will be rebuilt by a writer at the lift, as M03's pages are by `src/m03/lift.py`. Whether the writer is M04's own module (`src/m04/`) or an extension of M03's. Proposed: M04's own, decided at the lift PR. | Engineering |
