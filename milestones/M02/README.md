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
| Measured | |
| PRs used / cap | 1 / 4 |
| State | OPEN |

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

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant.

| # | Item | Seat |
|---|---|---|
| 1 | The eight effective dates were read from the versioner by an automated call on 2026-10-11, not by hand in a browser. P7 covers citations; an amendment date is the source's own field, read from the source. The Data Owner's hand confirmation (the eCFR page's "Timeline" for each section) is owed before a page shows a clause (M03). PR 2's gate re-reads the dates from the source in CI, which is the measurement. | Data Owner |
| 2 | `effective_date` is the section's latest amendment date, because the versioner versions sections, not paragraphs. The paragraph `201.57(c)(9)(i)` was last amended by 79 FR 72101 (Dec. 4, 2014) per its `source_note`, and its section's latest version is 2016-11-29. Confirm the section's date as the clause's version, or rule that a clause also carries its paragraph's own last-amended date from the `source_note` (a Federal Register citation, so P7 applies to it). | Data Owner, Tool Owner |
| 3 | The table's version. A row carries `dailymed_set_id` and `label_read_on` (SPEC/00 §9), not an SPL version number. DailyMed's history endpoint lists every version, but its XML API ignores the `version` parameter and serves the current version only; prior versions exist as HTML pages, which the build does not parse (read 2026-10-11, "The DailyMed read" above). Today the current version of each label predates `label_read_on`, so the risk is a revision between now and PR 2's run. **Ruled at PR 1** (`rulings/pr1.md` 7): accepted. No new row field in M02; the version stays set id plus read date, as §9 defines it. PR 2's build reads the history first; when a version was published after `label_read_on`, the source at the row's version cannot be read by machine and the result is UNSCORABLE naming the row and the page, never RED. The SPL version number and `effectiveTime` are recorded in the artifact beside each row, not in the row. | Data Owner, Tool Owner, Engineering |
| 4 | Which row fields the build derives from the source and which it carries from a hand file. Proposed: derived, the nine DailyMed fields listed under "Carried to PR 2"; carried, the six Data Owner fields. The gate compares the derived nine only. **Ruled at PR 1** (`rulings/pr1.md` 8): as proposed. | Data Owner |
| 5 | The Federal Register half of regdelta's ingestion (the poller) is not needed by the claim; M02 ports the eCFR reader and adds a DailyMed reader. Where the Federal Register feed lands (the "a rule changed" trigger for the public API) is a later row's. | Product |
| 6 | label-impact's `data/` is a copy as at `m00` and now differs from this repository's by the added field. When the agent takes the rebuilt data is not M02's: the deployed agent is called at M03, and a second agent is created at M07. | Product, Data Owner |
| 7 | The ruling file names this PR as #10, the next number on this repository. | Product |
| 8 | M00 Unsure 3 (`section_terms` read by an automated fetch on 2026-10-10, to be re-read by hand at M02's rebuild or M03). PR 2's build reads them by machine again. The hand re-read is still owed and is not done here. | Data Owner |
| 9 | M00 Unsure 7 (the extended-release metformin label's 08/2026 boxed-warning change, a candidate for M02's live build) is not taken into M02. The claim is the build of the seven rows and nine clauses the seed holds; a new row or golden is a Data Owner ruling in the milestone that needs it. | Data Owner |
| 10 | `ecfr_as_of` and `text_copied_on` are provenance: a rebuild changes them whenever the eCFR's as-of date or the run date moves, with the text unchanged. Proposed: the gate compares `text`, `lead_in`, `source_note` and `effective_date`, and records the provenance fields beside the result without comparing them. | Engineering, Data Owner |
