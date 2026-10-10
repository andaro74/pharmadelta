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
| PRs used / cap | 1 / 4 |
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

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant.

| # | Item | Seat |
|---|---|---|
| 1 | The baseline is a deterministic keyword matcher with no model. SPEC/00 §11 says the page's "ordinary assistant" is a real run of the frozen baseline from M04; with this baseline the side-by-side shows a keyword matcher, not an assistant. Replace it before tag `m00`, or accept and let the page say what it is. | Threshold Owner, Product |
| 2 | The baseline reads `data/table.json` and `data/clauses.json`, the agent's inputs. agentkeel's control read nothing under `data/`. Chosen so the delta measures method, not access, and so the ordinary golden is passable. | Threshold Owner, Engineering |
| 3 | `section_terms` in the table were read by an automated fetch of each DailyMed page on 2026-10-10, not by hand. The lisinopril 8.1 read shows "Risk Summary; Clinical Considerations" and no "Data" subheading. Re-read each by hand before any page shows a row (M03) or at M02's rebuild, whichever is first. | Data Owner |
| 4 | `g-001`'s `owed: follow-rld` reads a revision of a 201.57 content rule as reaching the ANDA label through the reference listed drug's revised labeling (314.150(b)(10) consistency), not as a change the holder files alone. Confirm or change before M01 copies the goldens. | Data Owner |
| 5 | SPEC/00 §10's note on 314.70(c)(6)(iii)(A) says "written for the holder of an approved NDA". `citations-checked.md` corrects it: the subject is the applicant, which includes an ANDA applicant via 314.3 and 314.97(a). §10 also says ecfr.gov refused the automated read; its versioner API answers when compression is accepted. Both are one-line SPEC/00 edits under Product. | Product |
| 6 | SPEC/00 §9 calls the labels public domain. The CFR text is; a label's text is written by the labeler. Carried from `labels.md`. | Product |
| 7 | `labels.md` records a live finding: the extended-release metformin label on DailyMed carried a boxed-warning change dated 08/2026 that the chosen plain-tablet label does not. No golden uses it and it is not confirmed against the reference product. A candidate for M02's live build, not for M00. | Data Owner |
| 8 | The ruling file names this PR as #2, the next number on the repository. If an issue or PR is opened first, the field is wrong by one. | Product |
