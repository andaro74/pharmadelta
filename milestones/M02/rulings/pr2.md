---
ruling: m02-pr2
seat:
  - Engineering
  - Security
  - Data Owner
  - Product
authorises:
  # Engineering: the build, the gate and the workflow that runs them
  - src/ingest/**
  - .github/workflows/m02.yml
  # Security: what the workflow reads (two public hosts, no token, no secret), and the fetch allowlist
  - .github/workflows/m02.yml
  - src/ingest/fetch.py
  # Data Owner: the hand files, the fields carried and the derivation rules proposed
  - src/ingest/hand/clauses.json
  - src/ingest/hand/table.json
  # Product: the ledger's PR count and the milestone's PR 2 detail
  - milestones/README.md
  - milestones/M02/README.md
  - milestones/M02/rulings/pr2.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/fields.md
  - milestones/M02/README.md
  - milestones/M02/rulings/pr1.md
  - https://www.ecfr.gov/api/versioner/v1/titles.json
  - https://www.ecfr.gov/api/versioner/v1/versions/title-21.json?section=314.98
  - https://www.ecfr.gov/api/versioner/v1/full/2016-12-23/title-21.xml?part=314&section=314.98
  - https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/f39ee08d-73db-71b9-e053-2995a90a877c/history.json
  - https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/f39ee08d-73db-71b9-e053-2995a90a877c.xml
  - https://github.com/andaro74/pharmadelta/actions/runs/38153322315
pr: https://github.com/andaro74/pharmadelta/pull/11
---

# Ruling: M02 PR 2 (measure)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR measures. It adds the build that reads the plant `4379556` and
the gate that judges it: `src/ingest/` builds the nine clauses from the
eCFR versioner at each clause's committed `effective_date` and the seven
rows from DailyMed at each row's `label_read_on`, compares the build
with `data/`, and writes `result.json` with one verdict;
`.github/workflows/m02.yml` runs it in CI and writes the result, the
built files and every source response as the artifact `m02-gate-<sha>`.
On `4379556`'s data the gate names `314.98(a)`: its `effective_date`
`2026-10-07` is not a version the versioner lists for 314.98. The CI run
on this PR is the measurement (P4); the ledger's "Measured" cell is
filled at PR 4 from the `main` run after this PR merges (ruling 4).
Nothing in this PR lifts the plant, and nothing under `data/` changes.

## Rulings in this PR

1. **Engineering.** The eCFR half of regdelta's ingestion is ported
   under `src/ingest/` with its scope changed to 21 CFR 201 and 314
   (SPEC/00 §8): `valid_version_dates`, `latest_version_date` and the
   DIV8 reading of `parse_ecfr_xml` from `src/ingestion/processor.py`,
   the host allowlist, redirect check and size cap from
   `src/shared/fetch.py`. regdelta's rule that a snapshot date is not an
   effective date is kept: the build reads at the committed date and
   never resolves "latest" or today. The paragraph locator and the
   DailyMed reader are new. Standard library only; no dependency added.
2. **Security.** The workflow reads `www.ecfr.gov` and
   `dailymed.nlm.nih.gov` over https with no token and no secret of this
   repository; `fetch.py` refuses any other scheme or hostname on the
   first request and on every redirect, and caps each body at 8 MiB.
   Every response read is written into the artifact so the measurement
   can be re-read without the source.
3. **Data Owner, Unsure 4 as ruled.** The build carries the six Data
   Owner fields of a row and the four of a clause from
   `src/ingest/hand/`, copied from `data/` at `0382d21`, with two
   reading flags per clause (`lead_in`, `append_subparagraphs`) that say
   what the Data Owner's clause is. It derives eight DailyMed fields by
   the rules in `milestones/M02/README.md`, "What the build reads".
   `section_terms`, the ninth, is a reading and not a structure; it is
   carried and recorded, not compared. That departs from ruling 8's
   "compares the nine" and is Unsure 11, for the Data Owner and the
   Tool Owner.
4. **Data Owner.** The comparison is string equality as the source
   prints it. Two seed rows differ from the SPL on `section_title` by
   case; the gate names them and is not changed to pass the seed. Which
   is wrong, the seed or the reading of "as printed", is Unsure 12.
5. **Product.** The expected CI result on this PR is RED naming
   `314.98(a)` with `rows_mismatched` `["metformin.6",
   "metoprolol-tartrate.5"]` beside it. The plant is named as the ledger
   row expects; the two rows are a RED on the seed, the case PR 1's
   README foresaw, and not a reason to edit the expected output. What
   the Measured cell can equal is decided by Unsure 11 and 12 and is
   recorded at PR 4, not here.
6. **Product.** The construction run of 2026-10-11 is recorded in the
   README as construction. It decides nothing (P4).
7. **Product.** "PRs used / cap" is 2 / 4. Which PR carries the lift is
   ruled on reading this PR's CI run, as M01's was.
8. **Product, on reading run 38153322315.** The run wrote RED,
   `clauses_mismatched` `["314.98(a)"]`, `rows_mismatched`
   `["metformin.6", "metoprolol-tartrate.5"]`, `written_by_ci` true;
   the plant is named as the row expects. The lift is carried by PR 4.
   PR 3, if the cold review of #11 finds anything, repairs and does not
   lift; if it finds nothing, PR 3 is skipped. The Measured cell takes
   the `main` run after #11 merges; whether it equals the expected
   output is Unsure 11 and 12's, and the cell says what it reads.
9. **Data Owner, Tool Owner; Unsure 11.** `section_terms` is a reading,
   not a structure. It is carried from the hand file and recorded, not
   compared; the gate compares eight DailyMed fields. Ruling 3's
   departure from ruling 8 stands. The hand re-read (Unsure 8) stays
   owed. Ruled on the session's recommendation, 2026-10-11.
10. **Data Owner, Product; Unsure 12.** The seed is wrong on two
    `section_title` cells; the SPL prints the headings in capitals and
    `fields.md` says "as printed". The cells are corrected in
    `data/table.json` in the PR that lifts the plant (PR 4). The gate
    is not changed. The Measured cell cites the `main` run after #11
    merges as it reads, naming the plant and the two rows; that is not
    the expected output written at open, and under the ledger's rule
    row 2 reads RED, with the finding beside it. Product writes the
    state at PR 4. Ruled on the session's recommendation, 2026-10-11.

## What a reader can falsify

Listed in `milestones/M02/README.md`, "What a reader can falsify" under
PR 2.

## What this ruling does not settle

The items under Unsure (PR 2) in `milestones/M02/README.md`, 11 to 21,
each with its seat, and PR 1's 1, 2, 5, 6, 8, 9 and 10, still open.
