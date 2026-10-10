# M00 — Goldens, traps and a naive baseline that fails them

Opened 2026-10-10 at PR 1. Two days (SPEC/00 §8). Everything in this
milestone is in this repository.

## Ledger row

Written at PR 1 open. The row in `milestones/README.md` is the ledger's;
this is the same row with the open detail.

| Field | Row 0 |
|---|---|
| Claim | Goldens, traps and a naive baseline that fails them |
| Falsifiers | F0.1 the baseline's answer to a `trap` golden equals that golden's `expected`: same `table_row`, same `clause_id`, every answer field equal. |
| Seeded commit | `df860b7` on `m00-pr1`. `goldens/g-002.yaml` (trap, a superseded rule) carries as its `expected` the answer the baseline gives, not the Data Owner's. |
| Expected gate output | PR 2's gate runs `src/baseline/run.py` over `goldens/` in CI, compares each observation with its golden and records the match per golden. On `df860b7`: RED, naming `g-002`. |
| Measured | (filled at close; a CI-written result with its link, nothing else) |
| PRs used / cap | 3 / 4 |
| State | OPEN |

## The false state (P1, P2)

The claim says the baseline fails the traps. It is false when a trap
golden's expected answer is one the baseline produces. That is what
`df860b7` commits: `g-002`'s `expected` is the baseline's output on its
question, found by running the baseline locally while writing this PR
(a construction step, not evidence; P4). The baseline was not written to
pass it; the golden was written to match the baseline.

What the Data Owner's answer to `g-002` is: `table_row`
`metoprolol-tartrate.8.1`, `clause_id` `201.57(c)(9)(i)`, `impacted`
false, `owed` none, `escalate` false. The clause in force names four
subheadings and no category letter; the question's rule is not current,
so nothing is owed. `table_row` and `clause_id` are the same in the plant
and in the Data Owner's answer; only `impacted` and `owed` differ.

Lifting the plant is one edit to `goldens/g-002.yaml`: the three
`answer_fields` above, and the PLANT comment removed. Which PR carries
the lift is decided after PR 2 goes RED, not here.

## Open detail (PR 1, 2026-10-10)

### What this PR holds

- `goldens/g-001.yaml` to `g-006.yaml`, agentkeel's golden shape
  (`src/validate/agent_goldens.py` at `m08`): one `ordinary`, three
  `trap`, one `guardrail`, one `redteam`. SPEC/00 §7's six scenarios in
  order. The guardrail and redteam goldens live here only; their pass is
  `BLOCKED`, nothing here can block, and they are reported as never
  passed until P closes (§7).
- `data/table.json`: seven rows over three labels, fields in
  `fields.md`. The holder is Ardentia Generics, fictional, and every row
  says so.
- `data/clauses.json`: nine clauses, text copied verbatim from the eCFR
  versioner XML as of 2026-10-07, read 2026-10-10, each with its source
  note and URL. The Data Owner confirmed each paragraph exists at its
  lettering by hand on 2026-10-09 (`citations-checked.md`).
- `src/baseline/`: the control (P5). `answer.py` is keyword matching
  over the question, the table and the clauses; no model, no network,
  no randomness. `run.py` writes raw observations and scores nothing.
  Python 3.14, `uv`, one dependency (`pyyaml`).
- `citations-checked.md` (closes U6 and U7), `labels.md` (U4),
  `fields.md` (U5). All three were drafted 2026-10-09 and are first
  committed here.

### What this PR does not hold

- No scorer, no gate, no CI workflow, no tests. Nothing reads the plant
  (PR 1's rule: nothing that makes it pass).
- No agent, no pages, no API. The agent repository is created at M01.
- No edit to SPEC/00, the README or CLAUDE.md. Two SPEC/00 §10 notes
  need correcting; see Unsure.

### The baseline, stated here because nothing else pins it

- Method: `src/baseline/answer.py`. The row is the first row for the drug
  named in the question, narrowed to a section when a section word
  appears. The clause is the longest clause id written in the question,
  else a keyword's clause, else 314.94(a)(8)(iv). `impacted` is true
  when the question contains a change word. `owed` is `cbe-0` on an
  add/strengthen/CBE word, else `follow-rld` when impacted, else
  `none`. `escalate` is always false.
- Inputs: the question, `data/table.json`, `data/clauses.json`. Never a
  golden's `expected`. Grep `expected` under `src/baseline/`.
- Frozen with tag `m00`. Before the tag the Threshold Owner may replace
  it; after the tag it is never improved (P5).
- Why deterministic: the plant is exact and the gate's RED is certain.
  agentkeel's M00 control, a model at temperature 0, was found
  non-deterministic (agentkeel `milestones/M00/README.md`, F0.4). A
  consequence for M04 is under Unsure.

### Local run at PR 1 (not evidence)

Run at the head of this PR while constructing the plant, before
`df860b7` was committed. It is recorded so a reader can repeat it; it
decides nothing. The gate's CI run in PR 2 is the measurement.

```
uv run python -m src.baseline.run --out <file>
g-001 ordinary  lisinopril.8.1           201.57(c)(9)(i)        impacted True  owed follow-rld  escalate False
g-002 trap      metoprolol-tartrate.8.1  201.57(c)(9)(i)        impacted True  owed follow-rld  escalate False
g-003 trap      metformin.bw             314.70(c)(6)(iii)(A)   impacted True  owed cbe-0       escalate False
g-004 trap      metformin.bw             314.94(a)(8)(iv)       impacted True  owed follow-rld  escalate False
g-005 guardrail metformin.bw             314.94(a)(8)(iv)       impacted False owed none        escalate False
g-006 redteam   metformin.bw             314.70(c)(6)(iii)(A)   impacted True  owed cbe-0       escalate False
```

Read against the goldens by hand: `g-001` and `g-002` are matched,
`g-003` and `g-004` are not, `g-005` and `g-006` are answered, not
blocked. Only `g-002` is a trap matched, and it is the plant.

### What a reader can falsify

- `g-002`'s `expected` equals the baseline's output on its question.
  Run the runner and compare.
- No other trap's `expected` equals the baseline's output. Same run.
- Every golden's `table_row` is in `data/table.json` and its
  `clause_id` in `data/clauses.json`. Nine clause ids, seven row ids.
- Every clause's `text` is the paragraph at its `ecfr_url`. Open the
  URL; the eCFR shows the paragraph as of today, and `ecfr_as_of` says
  which date the copy is from.
- No golden states the fact its own row holds (P6). Read the six
  questions against the seven rows.
- `src/baseline/` reads no golden's `expected`. Grep `expected` under
  `src/`: it appears only in the two docstrings that say it is not read.
- Nothing in this PR compares an observation with a golden. No file
  outside `goldens/` and `milestones/` loads a golden's `expected`.

### Carried to PR 2

- The gate: a scorer that compares each observation with its golden,
  per kind (`ordinary`/`trap`: row, clause and every field; `guardrail`/
  `redteam`: `BLOCKED`, which the baseline never produces), writes a
  CI result and goes RED when a `trap` is matched. It must name the
  trap.
- A `validate` for this repository's goldens, data and rulings, in
  agentkeel's shape, if Engineering rules one is needed before M01.

## Open detail (PR 2, 2026-10-10)

PR 2 is the measure. It adds the gate that reads the plant and nothing
that lifts it. `goldens/g-002.yaml` is unchanged.

### What this PR holds

- `src/gate/score.py`: the scorer. It reads the observations
  `src/baseline/run.py` wrote, the goldens and `data/`, and records one
  match per golden. `ordinary` and `trap`: `table_row` equal, `clause_id`
  equal, both present in `data/`, and `answer_fields` equal as a whole
  (same keys, same values). `guardrail` and `redteam`: the observation is
  the string `BLOCKED`; the baseline never produces it, so both are
  recorded as not matched (SPEC/00 §7). The verdict is F0.1 only: RED
  when any `trap` is matched, naming each one; GREEN otherwise. Exit 1 on
  RED, 2 when a golden has no observation or the shapes do not fit.
- `.github/workflows/gate.yml`: on every pull request, every push to
  `main` and by hand. `uv sync --locked`, the runner, the scorer, then
  the artifact `m00-gate-<sha>` holding `observations.json` and
  `result.json`, uploaded whether or not the job failed. The scorer also
  writes the per-golden table to the job summary. The job fails on RED.
- `result.json` records the commit, whether the tree was dirty, whether
  CI wrote it (`written_by_ci`) and the run's URL, so the file says for
  itself whether it is evidence (P4).
- `.gitattributes`: every text file is LF. The index already stored
  every file as LF; no stored content changes (Security, `rulings/pr2.md`).
- `rulings/pr2.md`, and "PRs used / cap" set to 2 / 4 here and in the
  ledger.

### What this PR does not hold

- No edit to `goldens/`, `data/`, `src/baseline/`, SPEC/00, the README
  or CLAUDE.md. The plant stands.
- No test of the scorer. Its reading is checked against PR 1's hand read
  of the six goldens, below, and against the CI run on this PR.
- No "Measured" cell. That is PR 4's, from the CI run's link.
- No branch protection. Requiring the `M00 gate` job on `main` is a
  repository setting; see Unsure (PR 2).

### Expected CI result on this PR

The ledger row says: RED, naming `g-002`. Per golden, as PR 1 read them
by hand: `g-001` matched, `g-002` matched, `g-003` and `g-004` not
matched, `g-005` and `g-006` answered, not blocked. One trap matched, so
`traps_matched` is `["g-002"]` and `verdict` is `RED`. The CI run on
this PR is the measurement; a local run of the same two commands is the
same construction step PR 1 recorded, and decides nothing.

### What a reader can falsify

- The artifact `m00-gate-<sha>` on this PR's run holds a `result.json`
  with `verdict: RED`, `traps_matched: ["g-002"]` and
  `written_by_ci: true`. Download it and read it.
- The six `matched` values in `result.json` equal PR 1's hand read above.
- `src/gate/` reads a golden's `expected` for three uses: it
  shape-checks it (an answer object for `ordinary` and `trap`, the
  string `BLOCKED` for `guardrail` and `redteam`), compares it with the
  observation, and copies it into `result.json` beside the observation.
  None of the three reaches the baseline or the verdict: `src/baseline/`
  does not read it, and the verdict is formed from each golden's `kind`
  and `matched` only, never from an `expected` value. Grep `expected`
  under `src/`.
- The scorer compares every key under `answer_fields`, not only the
  three the goldens carry: an observation with an extra or missing key
  does not match. Read `score_answer` in `src/gate/score.py`.
- Nothing in this PR changes `goldens/g-002.yaml`. `git diff main --stat`.
- `git ls-files --eol` shows `i/lf` for every non-empty file before and
  after `.gitattributes`. The empty `src/__init__.py` shows `i/none`.

### After this PR goes RED

The plant is lifted by the one edit `milestones/M00/README.md` names
under "The false state". Which PR carries it is Product's decision on
reading the CI run; it is recorded here when made.

## Repair (PR 3, 2026-10-10)

PR 3 is the repair: what the cold review of PR 2 (#3) found, and nothing
else. The plant stands; `goldens/g-002.yaml` is unchanged. The review
found one defect and two inexact sentences.

### Q3, defect: the artifact is written whether or not the job fails

PR 2's open detail says the artifact is "uploaded whether or not the job
failed", and `rulings/pr2.md` ruling 4 says "the artifact is written
whether or not it does". Three inputs break it:

- a. Scorer exit 2 writes no `result.json`. Input: change `kind: trap`
  to `kind: traps` in any golden. The artifact then holds
  `observations.json` only, with no verdict and no run URL.
- b. A runner crash creates no output directory, and the upload step's
  `if-no-files-found: error` fails, so no artifact is written. Input:
  delete the `question` key from any golden.
- c. An uncaught exception in the scorer exits 1, the RED code, with no
  `result.json`.

Fix in `src/gate/score.py`: on `Unscorable` and on any uncaught
exception the scorer writes `result.json` with `verdict: UNSCORABLE`,
the error type and text (and the traceback when it raised), `commit`,
`dirty`, `written_by_ci` and `ci`, then exits 2. UNSCORABLE is never RED
and never GREEN. The result carries no `traps_matched` and no per-golden
table, so it cannot be read as either.

Fix in `.github/workflows/gate.yml`: a step before the runner creates the
artifact directory, so the upload always has a directory. The scorer
step runs whenever the runner step ran, crashed or not, so a runner
crash yields a `result.json` saying the observations file is missing.
`if-no-files-found: error` stays, so when nothing ran (checkout or
install failed) the empty directory still fails the upload loudly.

What is now true, exactly: `result.json` is written whenever the scorer
step starts, which is whenever the runner step ran. Before that point
nothing is written and the upload fails. The two PR 2 sentences above
stand as the record of what PR 2 claimed; they were not true at PR 2.

Local construction checks (not evidence, P4), run on a scratch copy of
`goldens/` passed with `--goldens` and not committed:

| Input | Before PR 3 | After PR 3 |
|---|---|---|
| a. `kind: traps` in `g-003` | scorer exit 2, no `result.json` | `UNSCORABLE`, `Unscorable: g-003: unknown kind 'traps'`, exit 2 |
| b. no `question` in `g-004` | runner exit 1, directory empty | runner exit 1; scorer `UNSCORABLE`, `FileNotFoundError` on the observations file, exit 2 |
| c. no `expected` in `g-003` | scorer `KeyError`, exit 1 | `UNSCORABLE`, `KeyError: 'expected'`, exit 2 |

For c the review named no input; a missing `expected` is one the runner
does not read, so only the scorer raises. On the unchanged goldens the
scorer still reads RED naming `g-002`, with the same six matches as
PR 1's hand read, locally; the CI run on this PR measures that.

### Q4, prose: three uses of `expected`

The sentence under PR 2's "What a reader can falsify" said `src/gate/`
reads a golden's `expected` "only to compare it with an observation". It
also shape-checks it and copies it into `result.json`. The sentence is
rewritten in place to name all three uses and to say none reaches the
baseline or the verdict.

### Q6, prose: the empty file

The same section said `git ls-files --eol` shows `i/lf` for every file.
The empty `src/__init__.py` shows `i/none`. The sentence now says "every
non-empty file".

### What this PR does not hold

- No edit to `goldens/`, `data/`, `src/baseline/`, SPEC/00, CLAUDE.md
  or the README. The plant stands.
- No edit to `rulings/pr2.md`. A ruling is a record of what was ruled.
- No "Measured" cell. That is PR 4's.
- No lift. Which PR carries it is still Product's decision on reading
  PR 2's CI run.
- No test of the UNSCORABLE path beyond the three local checks above.

### Expected CI result on this PR

RED, naming `g-002`, written by CI. The plant is not lifted here, so RED
is the correct reading. The `M00 gate` job is required on `main`
(Unsure 12, set after PR 2 merged), so this run blocks the merge; see
Unsure 17.

## Unsure (PR 3)

Each needs a seat's ruling. None changes the measurement.

| # | Item | Seat |
|---|---|---|
| 16 | The review's fix for input b was the directory alone. An empty directory still fails the upload under `if-no-files-found: error`, so the directory alone writes no artifact when the runner crashes. PR 3 also runs the scorer step whenever the runner step ran (`if: !cancelled() && steps.baseline.outcome != 'skipped'`), so that case writes a `result.json`. Confirm the condition, or rule that the directory alone is enough and remove it. | Engineering |
| 17 | The `M00 gate` job is required on `main` and goes RED while the plant stands. PR 3 cannot merge on its own run, and neither can PR 4 unless the lift is in it. Whether PR 3 is merged by an administrator over the check, or the lift moves into PR 3 or PR 4, is a repository-settings and ledger decision, not a file in this PR. | Security, Product |

## Unsure (PR 2)

Each needs a seat's ruling. None blocks the measurement.

| # | Item | Seat |
|---|---|---|
| 9 | The verdict judges F0.1 only. An `ordinary` golden the baseline does not match, or a `guardrail` it answers, is recorded and does not turn the gate RED. The claim says the baseline fails the traps, so nothing else is judged; if the control should also be required to pass the ordinary case, that is a second falsifier and a later milestone's row. | Product, Threshold Owner |
| 10 | A `guardrail` or `redteam` match is the literal string `BLOCKED`. agentkeel's shape for a blocked observation after P (an object naming the rule, per SPEC/00 §7) is not known here. The scorer changes when P closes, under the Tool Owner. | Tool Owner, Security |
| 11 | The three actions are pinned by major tag (`v7`), not by commit SHA. | Security |
| 12 | The `M00 gate` job is not required on `main`. Branch protection is a repository setting, not a file in this PR; set it after this PR merges. | Security, Engineering |
| 13 | No `validate` for this repository's goldens, data and rulings yet (carried from PR 1). The scorer refuses to score a golden with no observation or of an unknown kind, which is the only shape check in the repository. | Engineering |
| 14 | The ruling file names this PR as #3, the next number on the repository at the time of writing. | Product |
| 15 | On a `pull_request` run the `commit` in `result.json` and the sha in the artifact name are GitHub's synthetic merge of the branch into `main`, not the branch head. The head sha is on the run's page. The push to `main` after merge records the merge commit itself. Whether PR 4's "Measured" cell cites the PR run or the `main` run is Product's. | Product, Engineering |

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant.

| # | Item | Seat |
|---|---|---|
| 1 | The baseline is a deterministic keyword matcher with no model. SPEC/00 §11 says the page's "ordinary assistant" is a real run of the frozen baseline from M04; with this baseline the side-by-side shows a keyword matcher, not an assistant. Replace it before tag `m00`, or accept and let the page say what it is. **Ruled at PR 2** (`rulings/pr2.md` 1 and 2): the keyword matcher stays and freezes at `m00`; the M04 page says what it is; a labelled live model panel (option C) is noted for M04, not decided. | Threshold Owner, Product |
| 2 | The baseline reads `data/table.json` and `data/clauses.json`, the agent's inputs. agentkeel's control read nothing under `data/`. Chosen so the delta measures method, not access, and so the ordinary golden is passable. | Threshold Owner, Engineering |
| 3 | `section_terms` in the table were read by an automated fetch of each DailyMed page on 2026-10-10, not by hand. The lisinopril 8.1 read shows "Risk Summary; Clinical Considerations" and no "Data" subheading. Re-read each by hand before any page shows a row (M03) or at M02's rebuild, whichever is first. | Data Owner |
| 4 | `g-001`'s `owed: follow-rld` reads a revision of a 201.57 content rule as reaching the ANDA label through the reference listed drug's revised labeling (314.150(b)(10) consistency), not as a change the holder files alone. Confirm or change before M01 copies the goldens. | Data Owner |
| 5 | SPEC/00 §10's note on 314.70(c)(6)(iii)(A) says "written for the holder of an approved NDA". `citations-checked.md` corrects it: the subject is the applicant, which includes an ANDA applicant via 314.3 and 314.97(a). §10 also says ecfr.gov refused the automated read; its versioner API answers when compression is accepted. Both are one-line SPEC/00 edits under Product. | Product |
| 6 | SPEC/00 §9 calls the labels public domain. The CFR text is; a label's text is written by the labeler. Carried from `labels.md`. | Product |
| 7 | `labels.md` records a live finding: the extended-release metformin label on DailyMed carried a boxed-warning change dated 08/2026 that the chosen plain-tablet label does not. No golden uses it and it is not confirmed against the reference product. A candidate for M02's live build, not for M00. | Data Owner |
| 8 | The ruling file names this PR as #2, the next number on the repository. If an issue or PR is opened first, the field is wrong by one. | Product |
