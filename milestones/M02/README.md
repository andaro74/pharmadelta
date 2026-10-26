# M02 — Table and clauses are built from live FDA sources, versioned by effective date

Opened 2026-10-11 at PR 1. Three days (SPEC/00 §8). Everything in this
milestone is in this repository. It needs regdelta's ingestion with its
scope changed to 21 CFR 201 and 314 (SPEC/00 §8); a clone is at
`~/code/regdelta`.

## Ledger row

Written at PR 1 open. The row in `milestones/README.md` is the ledger's;
this is the same row with the open detail.

| Field | Row 2 |
|---|---|
| Claim | Table and clauses are built from live FDA sources, versioned by effective date |
| Falsifiers | F2.1 a clause in `data/clauses.json` carries an `effective_date` the eCFR versioner does not list for its section, or a `text` that is not the paragraph at that version; or a row in `data/table.json` carries a DailyMed-sourced field the SPL in force on its `label_read_on` does not hold. |
| Seeded commit | `4379556` on `m02-pr1`: `data/clauses.json` carries `effective_date` on each of the nine clauses, the versioner's latest amendment date for the clause's section, read 2026-10-11; `314.98(a)` carries `2026-10-07`, the snapshot date (`ecfr_as_of`), which is not a version the versioner lists for 314.98. `data/table.json` is unchanged from `m00`. |
| Expected gate output | PR 2's gate builds the clauses from the eCFR versioner and the rows from DailyMed, in CI, compares each with `data/`, and writes a `result.json` that is RED when any clause or row differs from the source at its version, naming each. On `4379556`: RED, `clauses_mismatched` `["314.98(a)"]`, `rows_mismatched` `[]`. The Measured cell cites the `main` run after PR 2 merges (M01 Unsure 23, ruled here). |
| Measured | RED, `clauses_mismatched` `["314.98(a)"]`, `rows_mismatched` `["metformin.6", "metoprolol-tartrate.5"]`, `unreadable` `[]`, `written_by_ci` true, on `main` at `e8c3690`: [run 38154731153](https://github.com/andaro74/pharmadelta/actions/runs/38154731153), artifact `m02-gate-e8c3690d3877f8603620f3cb56c9104e530ec824`. The PR run on #11 at merge ref `c6ef241`, [run 38153322315](https://github.com/andaro74/pharmadelta/actions/runs/38153322315), read the same on every compared field. Names the plant as the row expects, and two rows the expected output does not: the seed's `section_title` on those rows was title-cased where the SPL prints capitals (M02 Unsure 12, ruled: the seed was wrong; corrected at PR 3). Does not equal the expected output. Finding: the hand-built seed was not fully reproduced from the source; the build was. |
| PRs used / cap | 3 / 4 |
| State | RED |

## The false state (P1, P2)

The claim says each clause is versioned by its effective date. It is
false when a clause carries, as its effective date, a date that is not
a version of its section at the source. That is what `4379556` commits:
`314.98(a)` carries `effective_date` `2026-10-07`. That date is the
eCFR "up to date as of" date the seed text was copied at (`ecfr_as_of`,
every clause). It is a snapshot date. The versioner lists one version of
314.98, with amendment date `2016-12-23`, and no version dated
2026-10-07.

Why this plant: writing the snapshot date as the effective date is the
mistake a hand-built seed makes. The seed at `m00` carried only the
snapshot date and no effective date at all. regdelta's domain rule says
the two are never conflated ("a snapshot date is not an effective
date", `src/ingestion/processor.py` in the clone). A gate that only
checks the field is present passes the plant; a gate that checks the
date against the source's version list does not. The plant tests which
one PR 2 builds.

The other eight clauses carry the date the versioner gives for their
section. The clause texts, the table and the goldens are not touched.

Lifting the plant is one edit to `data/clauses.json`: `314.98(a)`'s
`effective_date` to `2016-12-23`, and the `PLANT` key removed. Which PR
carries the lift is decided after PR 2 goes RED, not here.

## Open detail (PR 1, 2026-10-11)

### What this PR holds

- Row 2 of the ledger: falsifier, seeded commit, expected gate output,
  PRs used 1 / 4.
- `data/clauses.json`: one field added to each of the nine clauses,
  `effective_date`, after `ecfr_as_of`. Nothing else in the file
  changes; the diff is ten added lines. The plant is one of them, with a
  `PLANT` key beside it that says what it is.
- This file.
- `rulings/pr1.md`.

Nothing else. No ingestion code, no workflow, no test (P2). No edit to
`src/baseline/` (frozen at `m00`, P5), `src/gate/`, `src/m01/`,
`goldens/`, `data/table.json`, SPEC/00, CLAUDE.md, the README or
anything under `milestones/M00/` or `milestones/M01/`.

### The field added (Data Owner, `rulings/pr1.md` 2)

`milestones/M00/fields.md` says a field change after M00 is a Data
Owner ruling in a later milestone, recorded there. This is it.

| Field | Meaning |
|---|---|
| `effective_date` | `YYYY-MM-DD`. The date the version of the clause's **section** that the `text` is read from took effect: the eCFR versioner's `amendment_date` for the latest `content_versions[]` entry of that section. It is the section's date, not the paragraph's. A paragraph's own last amendment may be older; `source_note` says when. It is never the snapshot date (`ecfr_as_of`), which says when the copy was taken. |

The seed's `text` was copied from the eCFR XML as of 2026-10-07
(`fields.md`). The versioner serves that XML at a version date, and the
version in force on 2026-10-07 is the latest one for each section, so
the `effective_date` written here is the version the seed text is from.
PR 2's gate reads the paragraph at that date from the source and says
whether the seed text equals it.

### The versioner read (construction, not evidence, P4)

Read on 2026-10-11 with seven calls to
`https://www.ecfr.gov/api/versioner/v1/versions/title-21.json?section=<section>`
and one to `titles.json`. Title 21 answered "up to date as of
2026-10-07, latest amended on 2026-10-06". The responses are in the
session's scratch directory and are not committed; PR 2 reads them
again, in CI.

| Section | `content_versions[]` amendment dates (substantive) | Clause ids |
|---|---|---|
| 201.57 | 2016-11-29 | `201.57(c)(9)(i)` |
| 314.70 | 2016-12-23 | `314.70(c)(6)(iii)(A)` |
| 314.80 | 2016-12-23 | `314.80(c)(1)(i)`, `314.80(a)-serious`, `314.80(a)-unexpected` |
| 314.94 | 2016-12-23, 2017-01-11 | `314.94(a)(8)(iv)` |
| 314.97 | 2016-12-23 | `314.97(a)` |
| 314.98 | 2016-12-23 | `314.98(a)`, the plant: written as `2026-10-07` |
| 314.150 | 2016-12-23 | `314.150(b)(10)` |

201.57, 314.70 and 314.80 also list a 2023-03-30 entry with
`substantive: false` and the same amendment date; it is an issue of the
same text, not a version. 314.94 has two versions; the later,
2017-01-11, is written.

### The DailyMed read (construction, not evidence, P4)

Read on 2026-10-11, after PR 1 was opened, to settle Unsure 3. Three
calls to `/dailymed/services/v2/spls/<setid>/history.json`, four to
`/spls/<setid>.xml?version=<n>` and one to `lookup.cfm?setid=<setid>&version=5`.
The responses are in the session's scratch directory and are not
committed; PR 2 reads them again, in CI.

| Label | Versions listed | Current version, published | `effectiveTime` of the current XML |
|---|---|---|---|
| lisinopril | 5 | 5, 2022-11-18 | not read |
| metformin | 5 (versions 1, 2, 3, 5, 6) | 6, 2025-12-05 | not read |
| metoprolol tartrate | 10 | 10, 2024-11-06 | `20240822`, which is the row's `label_revised` `2024-08` |

The XML endpoint ignored `version`: asked for 1, 5, 8 and 9 of
metoprolol it answered `versionNumber` 10 every time. The web lookup
with `version=5` answered the version 5 page ("Revised: 6/2019"), as
HTML. Every current version was published before `label_read_on`
(2026-10-09), so today the current version is the version in force on
the read date for all three labels.

### What this PR does not hold

- No reader of the source. Nothing in this repository calls ecfr.gov
  or DailyMed. Grep `ecfr.gov` and `dailymed` under `src/` and
  `.github/`: no match.
- No lift. `314.98(a)` carries `2026-10-07` until the PR that carries
  the lift, decided after PR 2 goes RED.
- No edit to `data/table.json`. The rows are as at `m00`, with
  `dailymed_set_id` and `label_read_on` as their version (SPEC/00 §9).
- No change to label-impact. Its `data/` is a copy as at `m00` and is
  not touched by this milestone (Unsure 6).
- No number that is not a CI-written result with a link.

### What a reader can falsify

- `git diff m01 -- data/clauses.json` is ten added lines: nine
  `effective_date` lines and one `PLANT` line. No other file under
  `data/`, `goldens/` or `src/` differs from `m01`.
- `314.98(a)` carries `effective_date` `2026-10-07`, which equals its
  `ecfr_as_of`. The other eight carry a date that differs from their
  `ecfr_as_of`.
- The versioner lists no version of 314.98 dated 2026-10-07. Open
  `https://www.ecfr.gov/api/versioner/v1/versions/title-21.json?section=314.98`:
  one entry, `amendment_date` `2016-12-23`.
- Each of the other eight dates is the latest `amendment_date` the same
  endpoint lists for the clause's section. Open the seven URLs in the
  table above.
- The frozen baseline and the M00 scorer read clause ids only
  (`for cid in clauses` in `src/baseline/answer.py`, `set(clauses)` in
  `src/gate/score.py`), so the added field changes no M00 reading. The
  `M00 gate` run on this PR is the record; a local run before the plant
  commit read GREEN, `traps_matched` `[]`, and decides nothing.
- Nothing in this PR compares `data/` with a source.
  `git diff main --stat` on this PR touches `data/clauses.json`,
  `milestones/README.md`, `milestones/M02/README.md` and
  `milestones/M02/rulings/pr1.md` only.

### Carried to PR 2

- **The build, clauses.** A port of the eCFR half of regdelta's
  ingestion (`src/ingestion/processor.py`: `valid_version_dates`,
  `latest_version_date`, `parse_ecfr_xml`; `src/shared/fetch.py`'s host
  allowlist), scope 21 CFR 201 and 314, under `src/ingest/`. For each
  clause id in `data/clauses.json`: read the versioner's
  `content_versions[]` for the section; fetch
  `/full/<date>/title-21.xml?part=<part>&section=<section>` at the
  clause's `effective_date`; find the paragraph at the clause's
  lettering; write `text`, `lead_in`, `source_note`, `effective_date`,
  `ecfr_as_of` (from `titles.json`) and `text_copied_on` (the run
  date). Where it reads the plant: a clause whose `effective_date` is
  not in the section's version list cannot be fetched at that date, and
  is named.
- **The build, rows.** For each `dailymed_set_id` in `data/table.json`:
  read DailyMed's history for the set id. If no version was published
  after the row's `label_read_on`, the current SPL XML is the version in
  force on the read date; fetch it and derive the DailyMed-sourced
  fields: `ingredient`, `dosage_form`, `strengths`, `anda`,
  `label_revised`, `format`, `section`, `section_title`,
  `section_terms`. If a version was published after `label_read_on`,
  the source at the row's version cannot be read by machine (the XML
  API serves the current version only; Unsure 3, ruled): the row is
  named with the page URL and the result is UNSCORABLE, never RED. The
  SPL version number and `effectiveTime` are written in the artifact
  beside the row, not into the row. The Data Owner's fields (`holder`,
  `holder_fictional`, `rld_nda`, `label_read_on`,
  `section_terms_read_on`, `requirement`) are carried from a hand file
  the build reads, not derived (Unsure 4, ruled).
- **The gate.** In CI, on every pull request and push to `main`: build
  both, compare each clause and row with `data/`, and write
  `result.json` with one verdict. RED when any clause's
  `effective_date` is not a version the versioner lists for its
  section, or its `text` is not the paragraph at that version, or any
  row's DailyMed-sourced field differs from the SPL at its version;
  `clauses_mismatched` and `rows_mismatched` name each, with the
  source's value beside the committed one. GREEN only when every clause
  and row equals the build. UNSCORABLE when a source could not be read
  at the entry's version, never RED and never GREEN (M00 PR 3's shape;
  a label revised after its `label_read_on` lands here, Unsure 3). `written_by_ci` and the
  run URL as M00's. The built files are written into the artifact
  beside the result, so a reader can diff them; they are not written
  into `data/` by the gate.
- **Provenance fields.** `ecfr_as_of` and `text_copied_on` change on
  every rebuild whether or not the text does (Unsure 10); the
  comparison proposed excludes them.
- **The expected RED.** On `4379556`: RED, `clauses_mismatched`
  `["314.98(a)"]`, `rows_mismatched` `[]`. The other eight clauses must
  reproduce the seed text byte for byte (SPEC/00 §9: "M02 replaces it
  and must reproduce it"), and the seven rows must reproduce from the
  SPL. If they do not, the result names more than the plant and the
  Measured cell will not equal this output; that is a true RED on the
  seed, not a reason to edit the expected output. A label revised after
  its read date is not that case: it reads UNSCORABLE (Unsure 3,
  ruled), and the measurement is then owed another run.

### Rulings carried from M01

| # | Ruled |
|---|---|
| M01's 23 | Product (`rulings/pr1.md` 4): a Measured cell cites the run on `main` after PR 2 merges, because its commit is a commit in this repository (M00 Unsure 15). When the run read at the time was the PR run, it is named beside the `main` run. Row 2's expected gate output says so. One rule from here on. |
| M01's 1 | Product (`rulings/pr1.md` 5): SPEC/00 §3's "re-made at `m08`" is owed a one-line edit. It rides in a PR of its own, outside any milestone's cap, together with the two one-line §10 edits M00's Unsure 5 owes; proposed ruling file `milestones/adoption/rulings/spec00-errata.md`. This session does not open it (one milestone per session), so after this PR it is still owed, with its PR named. It is not folded into M02's cap. |

## Open detail (PR 2, 2026-10-11)

PR 2 is the measure. It adds the build and the gate that read the plant
and nothing that lifts it. `314.98(a)` carries `effective_date`
`2026-10-07` at the head this PR measures. M02 is measured here.

### What this PR holds

- `src/ingest/`, the build. Python 3.14, standard library only;
  `pyproject.toml` and `uv.lock` are unchanged.
  - `fetch.py`: a port of regdelta's `src/shared/fetch.py`. Two hosts
    are allowed, `www.ecfr.gov` and `dailymed.nlm.nih.gov`, https only,
    the allowlist re-checked on every redirect hop, the body capped at
    8 MiB. Added for the eCFR: every request accepts gzip, because the
    `/full/` endpoint answers 406 without it (construction, below), and
    the body is inflated here. A 5xx, a 429 or a network error is tried
    three times; any other status is final. Each URL is read once per
    run, and every body read is written into the artifact under
    `sources/` with an index of file to URL.
  - `ecfr.py`: the eCFR half of regdelta's `src/ingestion/processor.py`,
    scoped to 21 CFR 201 and 314 (`cfr_section` refuses any other part).
    Ported: `valid_version_dates` (the versioner's `content_versions[]`
    to ISO dates, skip-and-report), `latest_version_date` (kept for
    reference; the build never resolves "latest" or today, it reads at
    the clause's committed `effective_date`), and the DIV8 reading of
    `parse_ecfr_xml` (HEAD, the flat P elements, the CITA note as
    `source_note`). New: the paragraph locator. eCFR's P elements are
    flat and each starts with its own lettering, so the section's
    hierarchy is rebuilt by walking them with six levels, (a) (1) (i)
    (A) (*1*) (*i*), a marker after an italic heading continuing the
    lettering ("(a) *Changes to an approved NDA.* (1)(i) ..."), and an
    unlettered P belonging to the paragraph above it (the definitions in
    314.80(a)). A marker that can be placed two ways, or none, stops the
    read of that section; the clause is then unread, not RED.
  - `dailymed.py`: the history of a set id (`history.json`, every
    version with its published date), the current SPL XML, and the
    derivation of eight fields from it (the table below).
  - `gate.py`: builds both files from `data/`'s ids and the hand files,
    compares each entry with `data/`, writes `result.json`, the built
    `clauses.json` and `table.json` in `data/`'s shape, and `sources/`.
  - `hand/clauses.json`, `hand/table.json`: the Data Owner's fields the
    build carries rather than derives, copied from `data/` at `0382d21`
    (Unsure 4, ruled: `holder`, `holder_fictional`, `rld_nda`,
    `label_read_on`, `section_terms_read_on`, `requirement`; for a
    clause `citation`, `ecfr_url`, `existence_checked_by_hand_on`,
    `note`), the row's `dailymed_set_id` and `section` (its version and
    its selector, SPEC/00 §9), `section_terms` (Unsure 11), and two
    reading flags per clause that say what the Data Owner's clause is:
    `lead_in` (the parent paragraph is carried: 314.70(c)(6)(iii) for
    (A), 314.150(b) for (10)) and `append_subparagraphs` (314.150(b)(10)
    carries its (i) and (ii); 201.57(c)(9)(i) does not carry its (A) to
    (D), as `fields.md` and the clause's `note` say).
- `.github/workflows/m02.yml`: on every pull request, every push to
  `main` and by hand. `uv sync --locked`, the artifact directory, the
  gate, then the artifact `m02-gate-<sha>` holding `result.json`, the
  built files and `sources/`, uploaded whenever the gate wrote a result,
  which is whenever `main` ran; an import error before `main` exits 1
  with no file and the upload fails on `if-no-files-found: error`. The
  gate writes its tables to the job summary. The job fails on anything
  but GREEN. The workflow reads two public hosts with no token and no
  secret of this repository. `gate.yml` and `m01.yml` are unchanged.
- `result.json` records the commit, whether the tree was dirty, whether
  CI wrote it (`written_by_ci`), the run's URL, which fields were
  compared and which were recorded only, so the file says for itself
  whether it is evidence (P4).
- `rulings/pr2.md`, and "PRs used / cap" set to 2 / 4 here and in the
  ledger.

### What the build reads, per entry

A clause, at its committed `effective_date`:

| Step | Source | What is taken |
|---|---|---|
| 1 | `titles.json` | title 21's `up_to_date_as_of`, written as `ecfr_as_of`; recorded, not compared (Unsure 10) |
| 2 | `versions/title-21.json?section=<section>` | `content_versions[].date`, the dates the versioner lists for the clause's section. A committed `effective_date` not among them is named in `clauses_mismatched` with the listed dates beside it, and nothing is fetched at it: it is not a version of the section |
| 3 | `full/<effective_date>/title-21.xml?part=<part>&section=<section>` | the section at that version: the paragraph at the clause id's lettering as `text` (with its sub-paragraphs appended where the hand file says so), the parent paragraph as `lead_in` where the hand file says so, the CITA note as `source_note`. A definition id (`314.80(a)-serious`) takes the unlettered paragraph under (a) whose text begins with the suffix |

Compared: `text`, `lead_in`, `source_note`, `effective_date`. Recorded:
`ecfr_as_of`, `text_copied_on` (the run date, UTC), the Data Owner's
fields, and `PLANT`, which the build does not write.

A row, at its committed `label_read_on`:

| Step | Source | What is taken |
|---|---|---|
| 1 | `spls/<setid>/history.json` | every version and its published date. A version published after `label_read_on` means the SPL at the row's version cannot be read by machine (the XML endpoint serves the current version only, ruling 7): the row is named with its page URL and the result is UNSCORABLE |
| 2 | `spls/<setid>.xml` | the current SPL. Its `setId` must be the row's and its `versionNumber` the history's current, else the row is unread. `spl_version` and `effectiveTime` are written beside the row in the result, not into the row |

The eight derived fields and their rules (`fields.md` names the field;
the rule is PR 2's reading of its "Source" column, Unsure 13 and 14):

| Field | Rule |
|---|---|
| `ingredient` | the active ingredient's substance name on the SPL's products, lowercased. Not `genericMedicine/name`: metformin's reads "Metformin Hydrochloride Tablet" and metoprolol's "METOPROLOL" (construction, below) |
| `dosage_form` | the products' `formCode` display name, lowercased |
| `strengths` | each product's active quantity, `<value> <unit>`, unique, ascending, `; `-joined |
| `anda` | the products' approval id |
| `label_revised` | the latest `effectiveTime` over the label's sections, outside the product data elements section, as `YYYY-MM`. Two of the three SPLs carry no "Revised:" text; on all three the month DailyMed prints in the Highlights equals this (construction, below) |
| `format` | `201.56(d)` when the SPL carries Highlights (any `<highlight>` element); else `201.56(e)` |
| `section` | the row's section code, when the SPL has it: `bw` is a section coded LOINC 34066-1, `N` or `N.N` a section whose title begins with that number |
| `section_title` | that section's title without its number. A boxed warning whose title is the generic "BOXED WARNING" takes its first non-empty paragraph |

The products must agree on ingredient, dosage form and approval id;
where they do not, the field is null with the disagreement beside it.
The comparison is string equality, with no case folding (Unsure 12).

`section_terms` is not derived and not compared (Unsure 11). The
result records beside each row what the section carries as headings by
structure: its subsection titles and its short styled paragraphs.

### The verdict

- **RED** when any clause's `effective_date` is not a version the
  versioner lists for its section, or its `text`, `lead_in` or
  `source_note` is not what the section carries at that version (a
  paragraph missing at the clause's lettering is this case: the
  committed text is not the paragraph at that version); or any row's
  derived field differs from the SPL at its version. `clauses_mismatched`
  and `rows_mismatched` name each; every compared field carries the
  committed value and the source's beside it.
- **GREEN** only when every compared field of every clause and row
  equals the build.
- **UNSCORABLE** when a source could not be read at an entry's version:
  a network or HTTP failure after the retries, a label with a version
  published after its read date, an SPL served at another version or
  set id, a section whose lettering the reader could not rebuild, the
  titles endpoint unread, or anything raised inside `main`. Never RED,
  never GREEN (M00 PR 3's shape). The entries read before the unread
  one keep their comparison in the result; the verdict is still
  UNSCORABLE. The error is written in the result.

Exit 0 GREEN, 1 RED, 2 UNSCORABLE.

### What this PR does not hold

- No lift. `314.98(a)` carries `2026-10-07` at the head the gate reads.
- No edit to `data/`, `goldens/`, `src/baseline/` (P5), `src/gate/`,
  `src/m01/`, SPEC/00, CLAUDE.md, the README, `milestones/M00/` or
  `milestones/M01/`. No new dependency.
- No write into `data/`. The built files go in the artifact. Who takes
  a rebuild into `data/` is not this PR's (Unsure 19).
- No hand confirmation of the dates (Unsure 1) or the section terms
  (Unsure 8). Both are still owed.
- No comparison of `section_terms` (Unsure 11) and no case folding of
  `section_title` (Unsure 12).
- No test of the build. Its reading is checked against the construction
  run below and against the CI run on this PR.
- No "Measured" cell. That is PR 4's, from the `main` run after this
  PR merges (ruling 4).
- No branch protection. Whether `M02 gate` is required on `main` is a
  repository setting (Unsure 16).

### Construction run (not evidence, P4)

Run once on 2026-10-11 on the branch before the first push, from the
working tree, so `written_by_ci` is false and the tree was dirty. It
read 20 responses: `titles.json`, seven version lists, seven section
XMLs (the three 314.80 clauses share one), three histories and three
SPLs. Nothing was fetched at the plant's date. The responses are in the
session's scratch directory, not the repository.

| Reading | What the gate wrote |
|---|---|
| eCFR title 21 | `up_to_date_as_of` `2026-10-07`, `latest_amended_on` `2026-10-06`; `meta.date` `2026-10-08`, `import_in_progress` true (Unsure 18) |
| versions | each section lists the dates PR 1 recorded; 314.98 lists `2016-12-23` only |
| the eight clauses | `text`, `lead_in` where carried, `source_note`: all equal to `data/`, byte for byte, with the sub-paragraphs (i) and (ii) appended to 314.150(b)(10) and the parent paragraphs read for 314.70(c)(6)(iii)(A) and 314.150(b)(10) |
| `314.98(a)` | `version_listed` false; `effective_date` committed `2026-10-07`, the source lists `['2016-12-23']`; `text` and `source_note` not read, no version at that date. Named in `clauses_mismatched` |
| DailyMed histories | lisinopril: 5 versions, current 5 published 2022-11-18. metformin: 5 versions listed (1, 2, 3, 5, 6), current 6 published 2025-12-05. metoprolol tartrate: 10 versions, current 10 published 2024-11-06. None published after `label_read_on` 2026-10-09 |
| SPLs served | lisinopril version 5, `effectiveTime` 20220630; metformin 6, 20251204; metoprolol tartrate 10, 20240822 |
| the seven rows | `ingredient`, `dosage_form`, `strengths`, `anda`, `label_revised`, `format`, `section`: all equal on all seven. `section_title`: equal on five; `metformin.6` committed `Adverse Reactions`, source `ADVERSE REACTIONS`; `metoprolol-tartrate.5` committed `Warnings and Precautions`, source `WARNINGS AND PRECAUTIONS` |
| verdict | RED, `clauses_mismatched` `["314.98(a)"]`, `rows_mismatched` `["metformin.6", "metoprolol-tartrate.5"]`, `unreadable` `[]`, exit 1 |

Six things the sources showed while this was built, each recorded for
the seat that owns it:

1. The eCFR `/full/<date>/` endpoint answers the plant's date. Asked
   for 314.98 at 2026-10-07 it answered 200 with the section's current
   text; asked at 2015-01-01, before the section's version, it answered
   404. So the source does not refuse a snapshot date, and the version
   check is the list check, as ruled: the build does not fetch at a date
   the versioner does not list (Unsure 17).
2. The same endpoint answers 406 ("requires response compression")
   unless the request accepts gzip. regdelta's Lambda runtime sent that
   header; the port sends it explicitly.
3. Two rows' `section_title` is title-cased in the seed where the SPL
   prints capitals. `fields.md` defines the field as "the section
   heading as printed"; the gate compares what the SPL prints (Unsure 12).
4. `section_terms` cannot be reproduced by machine. For a boxed warning,
   5.1 or 6 the seed holds a paraphrase ("fetal toxicity; discontinue
   when pregnancy is detected; drugs that act directly on the
   renin-angiotensin system"); for 8.1 the seed holds "Clinical
   Considerations" where the metoprolol SPL's underlined paragraph reads
   "Clinical consideration". The field is a reading, which is what M00
   Unsure 3 and this milestone's Unsure 8 already say (Unsure 11).
5. The SPL XML of lisinopril and metformin carries no "Revised:" text;
   metoprolol's does, "Revised: 08/2024". The DailyMed page prints
   6/2022, 7/2023 and 8/2024. The latest section `effectiveTime` outside
   the product data elements section is 20220630, 20230727 and 20240822:
   the same months. The document `effectiveTime` is not (metformin's is
   20251204). FDA's SPL stylesheet, which would say the rule, refused
   the automated read (an abuse-detection page), so the rule is observed
   on three labels, not read from the stylesheet (Unsure 13).
6. `genericMedicine/name` is not the established name on two of three
   SPLs (item above); the active substance name on the products is, on
   all three (Unsure 14).

### Expected CI result on this PR

The ledger row says: RED, `clauses_mismatched` `["314.98(a)"]`,
`rows_mismatched` `[]`. The construction run says the gate as built
also names two rows on `section_title`, so the CI run on this PR is
expected to write `verdict: RED`, `clauses_mismatched` `["314.98(a)"]`
and `rows_mismatched` `["metformin.6", "metoprolol-tartrate.5"]`,
`written_by_ci` true and the run URL. The plant is named as the row
expects. The two rows are a RED on the seed, the case PR 1's "The
expected RED" foresaw: not a reason to edit the expected output, and
not a reason to fold case in the gate (Unsure 12). The CI run is the
measurement; the construction run decides nothing.

### Observed (CI run, 2026-10-11)

The first run on this PR,
[38153322315](https://github.com/andaro74/pharmadelta/actions/runs/38153322315),
wrote the artifact `m02-gate-c6ef2418b43d295e3a7755652faebc75ec665fd8`
(the sha is the pull request's merge ref, as M00's and M01's were). It
holds `result.json`, `clauses.json`, `table.json` and `sources/` with
20 responses and `index.json`. `result.json`:

| Field | Value |
|---|---|
| `verdict` | `RED` |
| `clauses_mismatched` | `["314.98(a)"]`: `effective_date` committed `2026-10-07`, the versioner lists `["2016-12-23"]`; `text` and `source_note` not read, no version at that date |
| `rows_mismatched` | `["metformin.6", "metoprolol-tartrate.5"]`, each on `section_title` only: committed `Adverse Reactions` and `Warnings and Precautions`, source `ADVERSE REACTIONS` and `WARNINGS AND PRECAUTIONS` |
| `unreadable` | `[]` |
| `counts` | clauses 8 of 9 matched; rows 5 of 7 matched |
| the eight clauses | `text`, `lead_in`, `source_note`, `effective_date` all equal |
| rows read | lisinopril SPL version 5, `effectiveTime` 20220630, current published 2022-11-18; metformin 6, 20251204, 2025-12-05; metoprolol tartrate 10, 20240822, 2024-11-06; none published after `label_read_on` |
| `ecfr` | `up_to_date_as_of` `2026-10-07`; `meta.date` `2026-10-08`, `import_in_progress` true |
| `written_by_ci` | `true`; `commit` `c6ef241`, `dirty` false; exit 1; the `M02 gate` job failed. `M00 gate` on the same head passed: [run 38153322301](https://github.com/andaro74/pharmadelta/actions/runs/38153322301). `M01 gate` is not required and reads as it did on `main` |

Equals the expected result above, and equals the construction run on
every compared field. The plant is named as ledger row 2 expects; the
two rows are named beside it.

### What a reader can falsify

- The artifact `m02-gate-<sha>` on this PR's run holds `result.json`
  with `verdict: RED`, `clauses_mismatched: ["314.98(a)"]` and
  `written_by_ci: true`; `clauses.json` and `table.json`, the build;
  and `sources/` with every response read and `index.json`. Download
  it and read it.
- In the built `clauses.json`, the eight clauses equal `data/`'s except
  `text_copied_on`; `314.98(a)` has `text`, `source_note` and
  `effective_date` null and no `PLANT` key.
- In the built `table.json`, every row equals `data/`'s except the two
  `section_title` cells named above. `section_terms` is carried, not
  derived: compare `src/ingest/hand/table.json` with `data/table.json`
  on the Data Owner's fields; they are equal.
- The build reads two hosts: grep `https://` under `src/ingest/`, every
  URL built for a fetch is on `www.ecfr.gov` or `dailymed.nlm.nih.gov`;
  the one other match, `github.com`, is the User-Agent string in
  `fetch.py` and is never fetched; `check_url` there refuses any other
  hostname. Grep `secrets.` in `.github/workflows/m02.yml`: no match.
- The build never resolves "current" or today as a version: grep
  `latest_version_date` under `src/ingest/`, it is defined and not
  called; grep `/current/`, no match outside `ecfr_url` carried from the
  hand file.
- `git diff main --stat` on this PR touches `src/ingest/`,
  `.github/workflows/m02.yml`, `milestones/README.md`,
  `milestones/M02/README.md` and `milestones/M02/rulings/pr2.md` only.

### After this PR goes RED

The plant is lifted by the one edit named under "The false state":
`314.98(a)`'s `effective_date` to `2016-12-23` and the `PLANT` key
removed. Which PR carries the lift is ruled on reading this PR's CI
run, as M01's was at PR 2 (`milestones/M01/README.md`, "After this PR
goes RED"). The two `section_title` cells are the Data Owner's (Unsure
12); whether they are corrected in `data/table.json` with the lift, and
what the Measured cell then says, is ruled there.

**Ruled at PR 2, on reading run 38153322315 (Product).** The lift is
carried by PR 4, as M00's and M01's were. PR 3, if the cold review of
#11 finds anything, repairs and does not lift; if it finds nothing, PR 3
is skipped. The Measured cell takes the `main` run after #11 merges
(ruling 4), which reads as run 38153322315 did unless a source moves.
Whether that run equals the row's expected output is decided by Unsure
11 and 12, not here: as the gate stands, it names two rows the expected
output does not, and the cell says so.

## Close (PR 3, 2026-10-11)

PR 3 closes the milestone at 3 / 4. The cold review of #11 found nothing
that changes a verdict or a compared field (below), so the repair slot of
the PR shape is skipped and this, the milestone's third PR, is the close
(CLAUDE.md: "the milestone closes at PR 3"). `rulings/pr2.md` 8 and 10
call the close "PR 4": that is the close slot of the shape, which this
PR fills. One ruling file per PR used, so the file is `rulings/pr3.md`
(Product, Unsure 22). This PR holds the lift, the two `section_title`
cells Unsure 12 ruled, the "Measured" cell and the row's state, and
`rulings/pr3.md`. The tag `m02` goes on its merge commit. Nothing here
decides the row: the `main` run after #11 merged is the measurement.

### Cold review of #11

Read before this PR was opened: the four modules and the two hand files
under `src/ingest/`, `.github/workflows/m02.yml`, and the `main` run's
artifact against what "Open detail (PR 2)" says the gate does. Two
findings, neither in the path that judged the plant or the rows:

1. `result.json`'s `fields_recorded_not_compared.rows` lists
   `section_terms` twice: once by name and once through the carried
   fields (`ROW_CARRIED` in `gate.py` holds it too). A duplicate in the
   record of what was not compared. The comparison reads `ROW_FIELDS`
   and is right.
2. When the gate exits UNSCORABLE from its top-level handler (the
   titles endpoint unread, a hand entry missing, anything raised inside
   `run`), it writes `result.json` with the error and no `sources/`. The
   responses read before the failure are not in the artifact, so
   `rulings/pr2.md` 2, "every response read is written into the
   artifact", does not hold on that path. The per-entry UNSCORABLE path
   (a label revised after its read date, a section the reader could not
   letter) is not this case: it continues and writes every source. Run
   38154731153 wrote all 20 it read.

Ruled (Engineering, Security; Unsure 23): neither is a defect in the
measurement, which stands as read; both are repaired in the next PR that
edits `gate.py`, not in a PR of this milestone. A seat that disagrees
overrules before this PR merges; the repair is then PR 3 and the close
PR 4, inside the cap.

### The lift

The one edit "The false state" named, in `data/clauses.json`:
`314.98(a)`'s `effective_date` is `2016-12-23`, the one version the
versioner lists for 314.98, and the `PLANT` key is gone. `git diff m01
-- data/clauses.json` is now nine added lines, one `effective_date` per
clause. Product ruled at PR 2 that the close carries it
(`rulings/pr2.md` 8).

### The two cells (Unsure 12, ruled at PR 2)

In `data/table.json`, `metformin.6`'s `section_title` is now `ADVERSE
REACTIONS` and `metoprolol-tartrate.5`'s is `WARNINGS AND PRECAUTIONS`:
what the SPLs print, and what run 38154731153 read. `fields.md` defines
the field as the heading "as printed"; the seed had title-cased two of
seven. `src/ingest/hand/table.json` is not touched: `section_title` is
derived by the build, not carried, so the hand file does not hold it and
Unsure 15 is not this case. Nothing else under `data/` changes.

### Measured

The cell cites the run on `main` after #11 merged,
[38154731153](https://github.com/andaro74/pharmadelta/actions/runs/38154731153)
on `e8c3690`, artifact `m02-gate-e8c3690d3877f8603620f3cb56c9104e530ec824`
(`rulings/pr1.md` 4; M01 Unsure 23). The PR run on #11 at merge ref
`c6ef241`, [38153322315](https://github.com/andaro74/pharmadelta/actions/runs/38153322315),
read the same on every compared field; it is named beside the `main` run
as the one read at the time. The `main` run's `result.json`:

| Field | Value |
|---|---|
| `verdict` | `RED` |
| `clauses_mismatched` | `["314.98(a)"]`: `effective_date` committed `2026-10-07`, the versioner lists `["2016-12-23"]`; `text` and `source_note` not read, no version at that date |
| `rows_mismatched` | `["metformin.6", "metoprolol-tartrate.5"]`, each on `section_title` only: committed `Adverse Reactions` and `Warnings and Precautions`, source `ADVERSE REACTIONS` and `WARNINGS AND PRECAUTIONS` |
| `unreadable` | `[]` |
| `counts` | clauses 8 of 9 matched; rows 5 of 7 matched |
| the eight clauses | `text`, `lead_in`, `source_note`, `effective_date` all equal |
| rows read | lisinopril SPL version 5, `effectiveTime` 20220630, current published 2022-11-18; metformin 6, 20251204, 2025-12-05; metoprolol tartrate 10, 20240822, 2024-11-06; none published after `label_read_on` |
| `ecfr` | `up_to_date_as_of` `2026-10-07`; `meta.date` `2026-10-08`, `import_in_progress` true |
| `written_by_ci` | `true`; `commit` `e8c3690`, `dirty` false; `ci.run_url` the run above; the `M02 gate` job failed, exit 1. `M00 gate` on the same head passed: [run 38154731111](https://github.com/andaro74/pharmadelta/actions/runs/38154731111) |

The expected gate output written at open says `rows_mismatched` `[]`.
The run names two rows beside the plant. The cell does not equal the
expected output, so under the ledger's rule row 2 is RED. The finding
beside it: the hand-built seed was not fully reproduced from the source;
the build was. The plant was named as the row expects. The two rows are
the seed's error on `section_title`, which Unsure 12 ruled and this PR
corrects. The gate is not changed and the expected output is not edited
(Product, `rulings/pr2.md` 10). What the claim says of the build holds
on every field the gate compares; what it says of the seed did not, on
two cells of one field, and the row says so.

A `main` run that reads UNSCORABLE (a label revised after its read date,
the titles endpoint unread, an import in progress ruled unread) is not a
measurement: the cell is then owed another run and the README says so
rather than citing it (Product, Unsure 24). Run 38154731153 read RED, so
the rule is stated here and not applied.

### Construction run after the lift (not evidence, P4)

Run once on 2026-10-11 from the working tree with the lift and the two
cells applied, before the branch was pushed; `written_by_ci` false,
`dirty` true. Its output is in the session's scratch directory, not the
repository. It read 21 responses: the 20 the `main` run read, plus
`full/2016-12-23/title-21.xml?part=314&section=314.98`, which the plant
had kept from being fetched. Verdict GREEN, 9 of 9 clauses and 7 of 7
rows, `unreadable` `[]`, exit 0. `314.98(a)`: `version_listed` true,
`text` and `source_note` equal to the seed byte for byte at 2016-12-23.
The eCFR still answered `up_to_date_as_of` `2026-10-07` with
`import_in_progress` true (Unsure 18). DailyMed's current versions were
unchanged: lisinopril 5, metformin 6, metoprolol tartrate 10, none
published after `label_read_on`. This run decides nothing. It says what
the CI run on this PR should read if no source moves.

### Expected CI result on this PR

GREEN: `clauses_mismatched` `[]`, `rows_mismatched` `[]`, `unreadable`
`[]`, `written_by_ci` true, 9 of 9 clauses and 7 of 7 rows, exit 0, and
the `M02 gate` job passes for the first time. `M00 gate`, the required
check, passes as it did on `main`. `M01 gate` reads PENDING and fails,
not required, as on `main`. A source that moves between now and the run
(a label revised, the eCFR import) reads UNSCORABLE, never RED or GREEN;
that would change nothing in the cell above. This run is a reading after
the measurement, not the Measured cell.

### Observed (CI run, 2026-10-11)

The first run on this PR,
[38156488922](https://github.com/andaro74/pharmadelta/actions/runs/38156488922),
wrote the artifact `m02-gate-2b1da30ba21dcab522543cdc22762df4ee2fc5ea`
(the sha is the pull request's merge ref, as every PR run's has been). It
holds `result.json`, `clauses.json`, `table.json` and `sources/` with 21
responses and `index.json`. `result.json`:

| Field | Value |
|---|---|
| `verdict` | `GREEN`; `reason` "F2.1 does not hold" |
| `clauses_mismatched` | `[]` |
| `rows_mismatched` | `[]` |
| `unreadable` | `[]` |
| `counts` | clauses 9 of 9 matched; rows 7 of 7 matched |
| `314.98(a)` | `effective_date` `2016-12-23`, `version_listed` true; `text` and `source_note` read at `full/2016-12-23/title-21.xml?part=314&section=314.98` and equal to `data/` |
| the two cells | `metformin.6` `section_title` source `ADVERSE REACTIONS`, `metoprolol-tartrate.5` source `WARNINGS AND PRECAUTIONS`, both equal to `data/` |
| rows read | lisinopril SPL version 5, `effectiveTime` 20220630; metformin 6, 20251204; metoprolol tartrate 10, 20240822; current versions and published dates as the `main` run read them; none published after `label_read_on` |
| `ecfr` | `up_to_date_as_of` `2026-10-07`; `meta.date` `2026-10-08`, `import_in_progress` true (Unsure 18) |
| `written_by_ci` | `true`; `commit` `2b1da30`, `dirty` false; `ci.run_url` the run above; exit 0; the `M02 gate` job passed, the first pass of this gate. `M00 gate` on the same head passed: [run 38156488930](https://github.com/andaro74/pharmadelta/actions/runs/38156488930). `M01 gate`, [run 38156488890](https://github.com/andaro74/pharmadelta/actions/runs/38156488890), is not required and reads as it does on `main` |

Equals the expected result above and the construction run on every
compared field. The built `clauses.json` differs from `data/` on
`text_copied_on` only (`2026-10-11` against `2026-10-10`; recorded, not
compared, Unsure 10); the built `table.json` equals `data/` on every
field. This run is a reading after the measurement. The cell above is
the `main` run on the plant, and is not changed by it.

### Rulings carried

| # | Ruled |
|---|---|
| PR 2's 8 | Product: the lift is carried by the close, this PR. |
| PR 2's 10 | Data Owner, Product: the two cells are corrected here; the cell cites the `main` run as it read; row 2 is RED with the finding beside it. |
| PR 1's 1, 8 | Data Owner: the hand confirmations (the eight dates against each section's "Timeline" on ecfr.gov; `section_terms` re-read in a browser) were done by the Data Owner in a browser on 2026-10-11, twenty steps, one URL each, recorded under Unsure 25. Nine dates confirmed; one `section_terms` heading differs on `metoprolol-tartrate.8.1`, owed a correction with the hand file (Unsure 15). Not done by machine. |

### What this PR does not hold

- No edit to `src/` (the hand files included), `goldens/`,
  `src/baseline/` (P5), `src/gate/`, `src/m01/`, `.github/workflows/`,
  SPEC/00, CLAUDE.md, the README, `milestones/M00/`, `milestones/M01/`,
  `rulings/pr1.md` or `rulings/pr2.md`. No new dependency.
- No change to the gate: no case folding, no `section_terms`
  comparison, no repair of the two cold-review findings.
- No edit to the expected gate output written at open.
- No hand confirmation done by machine and called a hand check. The two
  done at this PR were done in a browser (Unsure 25).
- No edit to `section_terms` or `section_terms_read_on`: the one heading
  the hand re-read found is owed with the hand file (Unsure 15, 25).
- No branch protection change (Unsure 16).
- No new claim. M03 waits on row P (SPEC/00 §8).

### What a reader can falsify

- `git diff m01 -- data/clauses.json` is nine added lines, each an
  `effective_date`. `grep -r PLANT data/` matches nothing.
- `git diff m01 -- data/table.json` is two changed lines, both
  `section_title`, the values above.
- The `main` run's artifact `m02-gate-e8c3690d3877f8603620f3cb56c9104e530ec824`
  holds `result.json` with `verdict: RED` and the two lists in the table
  above, `written_by_ci: true`, and 20 files under `sources/`. Download
  it and read it; the ledger's cell is that file.
- The CI run on this PR writes `verdict: GREEN`. Its built
  `clauses.json` and `table.json` equal `data/`'s on every compared
  field; `text_copied_on` differs (recorded, not compared, Unsure 10).
- `git diff main --stat` on this PR touches `data/clauses.json`,
  `data/table.json`, `milestones/README.md`, `milestones/M02/README.md`
  and `milestones/M02/rulings/pr3.md` only.

### After this PR

Tag `m02` on the merge commit, as `m00` and `m01` were tagged. Row 2
reads RED in the ledger with its finding; the milestone is closed, not
reopened. Open and carried to the milestone that touches them: Unsure 13
to 20, and PR 1's 2, 5, 6, 9 and 10. Unsure 23's repair goes to the next
PR that edits `gate.py`. M01 Unsure 1 and M00 Unsure 5 are still owed
three one-line SPEC/00 edits in a PR of their own
(`milestones/adoption/rulings/spec00-errata.md`), outside any cap. Row P
must close before M03 opens.

## Unsure (PR 3)

Numbering continues from PR 2's. Each needs a seat's ruling. None
changes the measurement.

| # | Item | Seat |
|---|---|---|
| 22 | The close is the milestone's third PR, so its ruling file is `pr3.md` and "PRs used / cap" is 3 / 4, one file per PR used; `rulings/pr2.md` 8 and 10 say "PR 4", meaning the close slot of the shape. M00 and M01 each used four PRs, so there was no precedent. **Ruled at PR 3** (`rulings/pr3.md` 1): as written. | Product |
| 23 | The cold review of #11 found two things in `gate.py` that do not change a verdict or a compared field: `section_terms` listed twice in `fields_recorded_not_compared.rows`; no `sources/` written when the gate exits UNSCORABLE from its top-level handler, so ruling 2 of PR 2 does not hold on that path. **Ruled at PR 3** (`rulings/pr3.md` 5): not a repair PR of this milestone; repaired in the next PR that edits `gate.py`, with the Security property restated there. **Repaired at the build-fixes PR** (`milestones/adoption/rulings/build-fixes.md` 1 and 2; the run that reads the repair is cited there, under its Finding until observed). | Engineering, Security |
| 24 | A `main` run that reads UNSCORABLE is not a measurement; the Measured cell is owed another run and the README says so rather than citing it. The `main` run after #11 read RED, so the rule did not apply. **Ruled at PR 3** (`rulings/pr3.md` 4): stated as the rule for every cell from here on. | Product |
| 25 | PR 1's Unsure 1 (the eight effective dates against each section's "Timeline" on ecfr.gov) and Unsure 8 (`section_terms` re-read by hand) are owed to the Data Owner in a browser. Asked at this PR. Not done by machine. **Done at PR 3** (`rulings/pr3.md` 6), by the Data Owner in a browser on 2026-10-11. Unsure 1: the "Timeline" of 201.57, 314.70, 314.80, 314.97, 314.98 and 314.150 on ecfr.gov reads "No changes found for this content after 1/03/2017" (the eCFR's point-in-time record begins that day, so it shows no 2016 date and no later change); 314.94's shows 1/11/2017 as its latest. The versioner's `versions/title-21.json?section=<section>`, opened in the browser, reads `amendment_date` 2016-11-29 for 201.57 and 2016-12-23 for 314.70, 314.80, 314.97, 314.98 (one entry; none dated 2026-10-07) and 314.150. All nine committed `effective_date`s confirmed. Unsure 8: six rows' `section_terms` read on the DailyMed pages as the seed holds them (lisinopril bw and 8.1, metformin bw, 5.1 and 6, metoprolol tartrate 5). `metoprolol-tartrate.8.1` differs on one heading: the page prints "Clinical consideration" where the seed holds "Clinical Considerations", the build's reading (construction item 4). That cell is the Data Owner's to correct, in `data/table.json` and the hand file together, in the PR that settles Unsure 15; it is not edited here. `section_terms_read_on` in `data/` stays 2026-10-10, the machine read; the hand date is this row's. **Corrected at the clean-up PR** (`milestones/adoption/rulings/data-owner-cleanup.md` 1): the cell reads "Risk Summary; Clinical consideration; Data" in both files. | Data Owner |
| 26 | The ruling file names this PR as #12, the next number on this repository. | Product |

## Unsure (PR 2)

Numbering continues from PR 1's. Each needs a seat's ruling. None blocks
the measurement; 11 and 12 decide what the Measured cell can equal.

| # | Item | Seat |
|---|---|---|
| 11 | `section_terms` is not derived by the build and not compared by the gate. Ruling 8 said the gate compares nine DailyMed fields; the build found the ninth is a reading, not a structure the SPL carries (construction, item 4), so a machine cannot reproduce it and a comparison would name every row for a reason that is not the build's. The gate compares eight and records beside each row the headings the section carries by structure. Confirm, or rule that `section_terms` is compared as a hand-derived field, in which case the gate names all seven rows and row 2 is RED on the seed. The hand re-read (Unsure 8) is owed either way. **Ruled at PR 2** (`rulings/pr2.md` 9): as built. `section_terms` is a Data Owner reading, carried and recorded, not compared. The hand re-read stays owed. | Data Owner, Tool Owner |
| 12 | `section_title` is compared as the SPL prints it, without case folding. Two seed rows are title-cased where the SPL prints capitals (construction, item 3), so the CI run names them and the Measured cell will not equal the expected output, which names the plant only. The gate is not changed to pass the seed. Rule which of the two is wrong: the seed, corrected in `data/table.json` by the Data Owner in the PR that lifts the plant, with the consequence for the Measured cell stated there; or the comparison, if "as printed" means the words and not the case, in which case PR 3 repairs the gate to fold case and says so. **Ruled at PR 2** (`rulings/pr2.md` 10): the seed is wrong. The two cells are corrected to what the SPL prints, in `data/table.json`, in the PR that lifts the plant (PR 4). The gate is not changed. The Measured cell at PR 4 cites the `main` run after #11 merges as it reads, naming the plant and the two rows; that does not equal the expected output written at open, and the ledger's rule then reads row 2 RED. The state is Product's to write at PR 4, with the finding beside it. | Data Owner, Product |
| 13 | `label_revised` is the latest section `effectiveTime` outside the product data elements section, a rule observed on three labels against the month DailyMed prints (construction, item 5). FDA's stylesheet, which would state the rule, refused the automated read. Confirm by hand against the three pages, or read the stylesheet in a browser and record the rule it holds. **Ruled at the clean-up PR** (`milestones/adoption/rulings/data-owner-cleanup.md` 3): the stylesheet (`spl-common.xsl`, template `effectiveDateHighlights`) was read on 2026-10-11 by fetch, not in a browser. Its rule: the latest `effectiveTime` over the top-level sections of the structured body, excluding `48780-1` and every section after the highest-numbered standard section up to 17, printed `M/YYYY`. The three pages print 6/2022, 7/2023, 8/2024, equal to the build's `2022-06`, `2023-07`, `2024-08`. The build's rule differs in two places (it walks subsections; it does not stop after section 17); equal on these three labels, not the same rule. Alignment is owed to the next PR that edits the build, with Unsure 23. | Data Owner |
| 14 | `ingredient` is the active ingredient's substance name on the SPL's products, lowercased, not `genericMedicine/name` (construction, item 6). `fields.md` says "the established name as the label title gives it"; the title reads "METFORMIN HYDROCHLORIDE tablets" and the substance name "METFORMIN HYDROCHLORIDE". Confirm the substance name as the field's source. **Ruled at the clean-up PR** (`milestones/adoption/rulings/data-owner-cleanup.md` 4): the substance name is the source. The three pages' Ingredients and Appearance tables print `LISINOPRIL`, `METFORMIN HYDROCHLORIDE`, `METOPROLOL TARTRATE` as the active ingredient (read 2026-10-11 by fetch), and the committed `ingredient` is each, lowercased, on all seven rows. `fields.md`'s wording is not edited. | Data Owner |
| 15 | The hand files live at `src/ingest/hand/` and duplicate the Data Owner's fields of `data/`. An edit to those fields in `data/` must be made in the hand file too, or the gate's carried fields and the committed ones part. Whether the hand files move beside `data/`, or the build reads the carried fields from `data/` itself (which would make them trivially equal and is why they are not read from there now), is a ruling. **Ruled at the clean-up PR** (`milestones/adoption/rulings/data-owner-cleanup.md` 2): neither. The hand files stay at `src/ingest/hand/`; the build does not read the carried fields from `data/`. An edit to a carried field is made in both files in one PR, as this one does for `metoprolol-tartrate.8.1`. The gate does not name a divergence between the two today; naming it is owed to the next PR that edits `gate.py`, with Unsure 23. | Data Owner, Engineering |
| 16 | Whether `M02 gate` is made a required check on `main`, as M00's Unsure 12 and M01's Unsure 14 asked for theirs. Not changed here. | Security, Product |
| 17 | The eCFR `/full/<date>/` endpoint answers a date the versioner does not list with the text in force on that date (construction, item 1). The build does not fetch at such a date, so the plant's `text` is "not read", not "differs". A reader might expect the text compared anyway. The reading here follows regdelta's rule that a snapshot date is not an effective date. | Tool Owner |
| 18 | `titles.json` answered `up_to_date_as_of` `2026-10-07` with `meta.date` `2026-10-08` and `import_in_progress` true. `ecfr_as_of` is written from `up_to_date_as_of` and the meta is recorded beside it. Whether a run during an import should be unread is not ruled. | Engineering |
| 19 | The built files are written into the artifact, never into `data/`. Who takes a rebuild into `data/`, and when (the lift PR, a later milestone), is not this PR's. | Product, Data Owner |
| 20 | Unsure 2 (the section's date as the clause's version) is not touched: the build checks the committed date against the section's version list and reads the section at that date. | Data Owner, Tool Owner |
| 21 | The ruling file names this PR as #11, the next number on this repository. | Product |

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant.

| # | Item | Seat |
|---|---|---|
| 1 | The eight effective dates were read from the versioner by an automated call on 2026-10-11, not by hand in a browser. P7 covers citations; an amendment date is the source's own field, read from the source. The Data Owner's hand confirmation (the eCFR page's "Timeline" for each section) is owed before a page shows a clause (M03). PR 2's gate re-reads the dates from the source in CI, which is the measurement. **Done at PR 3** (Unsure 25): Unsure 1: the "Timeline" of 201.57, 314.70, 314.80, 314.97, 314.98 and 314.150 on ecfr.gov reads "No changes found for this content after 1/03/2017" (the eCFR's point-in-time record begins that day, so it shows no 2016 date and no later change); 314.94's shows 1/11/2017 as its latest. The versioner's `versions/title-21.json?section=<section>`, opened in the browser, reads `amendment_date` 2016-11-29 for 201.57 and 2016-12-23 for 314.70, 314.80, 314.97, 314.98 (one entry; none dated 2026-10-07) and 314.150. All nine committed `effective_date`s confirmed. | Data Owner |
| 2 | `effective_date` is the section's latest amendment date, because the versioner versions sections, not paragraphs. The paragraph `201.57(c)(9)(i)` was last amended by 79 FR 72101 (Dec. 4, 2014) per its `source_note`, and its section's latest version is 2016-11-29. Confirm the section's date as the clause's version, or rule that a clause also carries its paragraph's own last-amended date from the `source_note` (a Federal Register citation, so P7 applies to it). | Data Owner, Tool Owner |
| 3 | The table's version. A row carries `dailymed_set_id` and `label_read_on` (SPEC/00 §9), not an SPL version number. DailyMed's history endpoint lists every version, but its XML API ignores the `version` parameter and serves the current version only; prior versions exist as HTML pages, which the build does not parse (read 2026-10-11, "The DailyMed read" above). Today the current version of each label predates `label_read_on`, so the risk is a revision between now and PR 2's run. **Ruled at PR 1** (`rulings/pr1.md` 7): accepted. No new row field in M02; the version stays set id plus read date, as §9 defines it. PR 2's build reads the history first; when a version was published after `label_read_on`, the source at the row's version cannot be read by machine and the result is UNSCORABLE naming the row and the page, never RED. The SPL version number and `effectiveTime` are recorded in the artifact beside each row, not in the row. | Data Owner, Tool Owner, Engineering |
| 4 | Which row fields the build derives from the source and which it carries from a hand file. Proposed: derived, the nine DailyMed fields listed under "Carried to PR 2"; carried, the six Data Owner fields. The gate compares the derived nine only. **Ruled at PR 1** (`rulings/pr1.md` 8): as proposed. | Data Owner |
| 5 | The Federal Register half of regdelta's ingestion (the poller) is not needed by the claim; M02 ports the eCFR reader and adds a DailyMed reader. Where the Federal Register feed lands (the "a rule changed" trigger for the public API) is a later row's. | Product |
| 6 | label-impact's `data/` is a copy as at `m00` and now differs from this repository's by the added field. When the agent takes the rebuilt data is not M02's: the deployed agent is called at M03, and a second agent is created at M07. | Product, Data Owner |
| 7 | The ruling file names this PR as #10, the next number on this repository. | Product |
| 8 | M00 Unsure 3 (`section_terms` read by an automated fetch on 2026-10-10, to be re-read by hand at M02's rebuild or M03). PR 2's build reads them by machine again. **Done at PR 3** (Unsure 25): Unsure 8: six rows' `section_terms` read on the DailyMed pages as the seed holds them (lisinopril bw and 8.1, metformin bw, 5.1 and 6, metoprolol tartrate 5). `metoprolol-tartrate.8.1` differs on one heading: the page prints "Clinical consideration" where the seed holds "Clinical Considerations", the build's reading (construction item 4). That cell is the Data Owner's to correct, in `data/table.json` and the hand file together, in the PR that settles Unsure 15; it is not edited here. `section_terms_read_on` in `data/` stays 2026-10-10, the machine read; the hand date is this row's. **Corrected at the clean-up PR** (`milestones/adoption/rulings/data-owner-cleanup.md` 1). | Data Owner |
| 9 | M00 Unsure 7 (the extended-release metformin label's 08/2026 boxed-warning change, a candidate for M02's live build) is not taken into M02. The claim is the build of the seven rows and nine clauses the seed holds; a new row or golden is a Data Owner ruling in the milestone that needs it. | Data Owner |
| 10 | `ecfr_as_of` and `text_copied_on` are provenance: a rebuild changes them whenever the eCFR's as-of date or the run date moves, with the text unchanged. Proposed: the gate compares `text`, `lead_in`, `source_note` and `effective_date`, and records the provenance fields beside the result without comparing them. | Engineering, Data Owner |
