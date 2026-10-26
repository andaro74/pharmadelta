---
ruling: build-fixes
seat:
  - Engineering
  - Security
  - Data Owner
authorises:
  # Engineering: the gate and the reader
  - src/ingest/gate.py
  - src/ingest/dailymed.py
  # Security: sources/ on every exit (ruling 2)
  - src/ingest/gate.py
  # Data Owner: the label_revised rule and the carried-field check (rulings 3 and 4)
  - src/ingest/dailymed.py
  # the Unsure 23 mark and this file
  - milestones/M02/README.md
  - milestones/adoption/rulings/build-fixes.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M02/README.md
  - milestones/M02/rulings/pr2.md
  - milestones/M02/rulings/pr3.md
  - milestones/adoption/rulings/data-owner-cleanup.md
  - src/ingest/gate.py
  - src/ingest/dailymed.py
  - src/ingest/hand/table.json
  - data/table.json
  - https://github.com/andaro74/pharmadelta/actions/runs/38154731153
  - https://github.com/andaro74/pharmadelta/actions/runs/38189632015
  - https://www.accessdata.fda.gov/spl/stylesheet/spl-common.xsl
pr: https://github.com/andaro74/pharmadelta/pull/18
---

# Ruling: build fixes (M02 Unsure 23, 13 and 15)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as #1 and #13 to #17 were.
It carries no claim, plants nothing and measures nothing. It is not M03.
It repairs what M02 Unsure 23 owed to the next PR that edits `gate.py`,
and what `data-owner-cleanup.md` rulings 2 and 3 owed to the same PR.
Four edits, two files under `src/ingest/`, one mark in
`milestones/M02/README.md`, this file. Nothing under `data/`,
`src/ingest/hand/`, `src/baseline/` (P5), `goldens/`, the ledger or
`.github/workflows/` changes.

## Rulings in this PR

1. **Engineering (M02 Unsure 23, first item).** `gate.py`'s
   `fields_recorded_not_compared.rows` listed `section_terms` twice,
   once by name and once through `ROW_CARRIED` (M02 PR 3, cold review
   item 1). The list is now `ROW_CARRIED`, `dailymed_set_id`,
   `table_row`; `section_terms` appears once, through `ROW_CARRIED`.
   The comparison reads `ROW_FIELDS` and is not touched.
2. **Engineering, Security (M02 Unsure 23, second item).** When `main`'s
   top-level handler exited UNSCORABLE, `result.json` was written with
   the error and no `sources/` (M02 PR 3, cold review item 2). The
   handler now calls `write_sources` before `write_result`, inside its
   own try, and records the index under `sources` in the result, or the
   write error under `sources_error` with `sources` null. The fetch
   cache holds every body read before the failure, so they are in the
   artifact. The per-entry UNSCORABLE path already wrote them. The
   Security property, restated: every run that reaches `main` writes
   `result.json` and `sources/` with every response read, on every exit,
   GREEN, RED and UNSCORABLE alike, including the top-level handler; the
   workflow uploads the directory with `if: always()`, so the artifact
   holds what the run read whatever it exited. A failure before `main`
   (an import error) still writes nothing, as PR 2's README says.
3. **Engineering, Data Owner (M02 Unsure 15; `data-owner-cleanup.md`
   2).** The build carries the Data Owner's row fields (`ROW_CARRIED`:
   `holder`, `holder_fictional`, `rld_nda`, `label_read_on`,
   `section_terms`, `section_terms_read_on`, `requirement`) from
   `src/ingest/hand/table.json` and still does not read them from
   `data/` (ruled out, Unsure 15). Beside each row the result now
   records `carried`: per field `equal`, `committed` (`data/`) and
   `hand`; `equal` over the row; `diverging`, the field names that
   differ; `judged` false. `rows_carried_diverging` at the top of the
   result names each divergence as `row.field`, and the job summary
   carries a column. A divergence does not change the verdict: #14
   ruled it a Data Owner error (both files are edited in one PR), not a
   source mismatch, so it is named, not judged. Whether it should turn
   the verdict RED is under Unsure, for the Data Owner and Engineering.
   `provenance()` records the check under `fields_carried_checked`.
4. **Data Owner, Engineering (M02 Unsure 13; `data-owner-cleanup.md`
   3).** `dailymed.py`'s `label_revised` now follows the stylesheet's
   rule as ruling 3 quotes it: the top-level sections of the structured
   body only, in document order; the product data elements section
   (`48780-1`) excluded; every section after the first occurrence of the
   highest-numbered standard section present (`maxSection17`) excluded;
   values longer than seven characters kept; the latest, as `YYYY-MM`.
   Subsections are no longer walked. The function records, beside the
   row, every top-level section with its code, `effectiveTime` and why
   it was read or excluded (`section_effective_times`). The standard
   sections are `PLR_SECTIONS`: the stylesheet's own list, which
   `spl-common.xsl` line 41 reads from `plr-sections.xml` beside it
   (`<xsl:param name="standardSections"
   select="document('plr-sections.xml')/*"/>`). That file was read by
   fetch on 2026-10-25 (Finding, second session): its top-level
   `number` attributes are 0 (`34066-1`, boxed warning) and 1 to 17,
   with two codes numbered 17 (`34076-0` patient counseling
   information, `38056-8` supplemental patient material). The first
   session had hand-written the 17 codes 1 to 17 from memory; all 17
   equal the file's, and the two entries the file has beyond them were
   added. `maxStdSectionNumber` is the stylesheet's `max` over the
   `@number[. <= 17]` of the standard sections present, so the cut is
   at the highest number, not the last in document order; with two
   codes at 17 the `preceding-sibling` test cuts after the first of
   either, which `cut_at` reproduces by taking the first index of any
   section at that number. On the three labels the committed months
   are `2022-06`, `2023-07`, `2024-08` (`data/table.json`), which the
   old rule reproduced in run 38154731153; the new rule is read by the
   run this PR is owed (Observed, below).
5. **Product.** This PR is #18, the next number on this repository,
   outside any cap. M02 Unsure 23 is marked "Repaired at the build-fixes
   PR" in `milestones/M02/README.md` with items 1 and 2 of this file.
   Unsure 13 and 15 are not re-marked there: their rulings in
   `data-owner-cleanup.md` already name this PR as the one that carries
   the build edits, and this file is the record. Nothing in
   `milestones/README.md` changes.

## Expected CI result on this PR

The M02 gate writes `verdict: GREEN`, 9 of 9 clauses, 7 of 7 rows,
`rows_mismatched` `[]`, `rows_carried_diverging` `[]`, `label_revised`
equal on all three labels (`2022-06`, `2023-07`, `2024-08`), every row's
`carried.equal` true, `written_by_ci` true, and `sources/` with 21
responses as run 38156488922 wrote. The M00 gate passes. The M01 gate
reads PENDING, exit 3, not required, as on #13 to #17; not this PR's.
If `label_revised` reads another month on any label, or the verdict is
not GREEN, the data and the code are not patched: what the run read is
recorded under Finding and the PR stays a draft.

## Finding

Written 2026-10-25, before any run. This session had no approval
surface: every command that changes state or reads the network was
refused automatically, and the refusal said it would be for the rest of
the session. Refused, one attempt each unless noted: `git checkout -b
build-fixes` and `git switch -c build-fixes` (two attempts at the one
step, the command budget); `gh pr list`; `curl` of `spl-common.xsl`;
`WebFetch` of the same; `uv run python`; `python -I -m py_compile`.
Read-only `git status` and `git log`, and the file tools, were allowed.

So, at the end of the session:

- The four edits, the M02 README mark and this file are written into
  the working tree on `main` at `6f42712`, uncommitted. No branch
  `build-fixes` exists. Nothing is committed, pushed or opened. There is
  no PR #18 yet; the `pr` line above names the number the next session
  should get, not one that exists.
- No CI run was waited on, no artifact downloaded, no `result.json`
  read. Every number in this file comes from a file read in the
  repository or from the runs named in `milestones/M02/README.md` and
  `data-owner-cleanup.md`. No sentence here says a fix works.
- The code was not executed, not even compiled. The first execution is
  the CI run on the PR. An import or syntax error there exits 1 before
  `main`, with no `result.json` (PR 2's README); that would be a
  finding on this file's rulings 1 to 4, not on the data.
- The stylesheet was not read. `PLR_SECTIONS` is hand-written from
  memory of the SPL Implementation Guide's section list (Unsure 2).

What the next session owes, in order: `git switch -c build-fixes` with
these changes in hand (never a checkout of `main` with them); commit;
push; open #18 as a draft; wait for the M02 gate run; download its
artifact; read `result.json`; write what it read under "Observed" here,
with the run id and the artifact name; un-draft if it reads as
"Expected" says, else leave the draft and the Finding. If the number
is not 18, correct the `pr` line and ruling 5.

**Second session, 2026-10-25, attended.** The refusals above were the
launcher's: it ran the first session with a permission mode that admits
file edits and denies every other command, with no one to answer. Not
a rule of this project. The attended session that followed read the
four edits as a cold review and found them as rulings 1 to 4 describe,
compiled both files, fetched `spl-common.xsl` and `plr-sections.xml`
and confirmed `PLR_SECTIONS` against the latter (ruling 4; Unsure 2 and
3 answered), added the file's two entries the first session lacked
(number 0, and the second code at 17), then branched, committed, pushed
and opened the PR. A local run of the gate was made for the session's
own reading of whether the code crashes; it is not evidence (P4) and no
number from it is in this file. The CI run is under "Observed".

## Observed

The M02 gate on this PR at `9aa8480`, run
[40249943382](https://github.com/andaro74/pharmadelta/actions/runs/40249943382),
artifact `m02-gate-a9b305278715e45adc158e3abdd22ad1f39291a8`, read on
2026-10-25 from the downloaded `result.json`:

| Field | Value |
|---|---|
| `verdict` | `GREEN` |
| `written_by_ci` | true |
| `clauses_mismatched`, `rows_mismatched`, `unreadable` | `[]`, `[]`, `[]` |
| `rows_carried_diverging` | `[]`; every row's `carried.equal` true |
| `counts` | clauses 9 of 9 matched; rows 7 of 7 matched |
| `label_revised`, source against committed | `2022-06` on both lisinopril rows, `2023-07` on the three metformin rows, `2024-08` on both metoprolol tartrate rows; equal on all seven |
| `sources/` | 21 entries, as run 38156488922 wrote |

Equal to "Expected CI result on this PR" on every line. The M00 gate
passed (run 40249943284). The M01 gate read PENDING, exit 3 (run
40249943261), not required, not this PR's. On metoprolol tartrate the
new rule's record shows the three package-label panels (`51945-4`)
excluded as "after the highest-numbered standard section (34076-0)" and
the product data section excluded by code; the month is unchanged
because every section of that label carries the same date.

## What a reader can falsify

- `git diff main --stat` on the PR touches four files: `src/ingest/gate.py`,
  `src/ingest/dailymed.py`, `milestones/M02/README.md` and this file.
  Nothing under `data/`, `src/ingest/hand/`, `src/baseline/`, `goldens/`
  or `.github/workflows/`.
- In `gate.py`, `"section_terms"` occurs once in
  `fields_recorded_not_compared` (through `ROW_CARRIED`); `unscorable`
  calls `write_sources` before `write_result`; `build_row` writes
  `entry["carried"]` and `judge` writes `rows_carried_diverging`.
- In `dailymed.py`, `label_revised` reads `label.sections` only, never
  `.children`; `PLR_SECTIONS` holds 19 entries, numbers 0 and 1 to 17
  with two codes at 17, equal to the top-level `number` attributes of
  https://www.accessdata.fda.gov/spl/stylesheet/plr-sections.xml.
- The two files agree on every carried field of every row today
  (`data-owner-cleanup.md`, "What a reader can falsify", the one-line
  check prints `[]`), so the run should name no divergence.
- The run on the PR, once observed, is the only evidence of what the
  edits do (P4).

## What this ruling does not settle

Each item needs a seat's ruling. None changes a measurement; M02 is
closed at `m02`.

| # | Item | Seat |
|---|---|---|
| 1 | Should a divergence between `data/` and the hand file on a carried field turn the verdict RED? Today it is named in `rows_carried_diverging` and beside the row, and does not change the verdict, because #14 ruled it a Data Owner error and not a source mismatch (F2.1 is about the source). The smaller change was taken. | Data Owner, Engineering |
| 2 | `PLR_SECTIONS`, the 17 LOINC section codes, was hand-written without reading the stylesheet (Finding). Confirm each code against `spl-common.xsl`'s `maxSection17` list, in a browser, and against the SPL Implementation Guide. One wrong code moves the cut and can change `label_revised` on a label whose later sections carry a later date. **Answered in the second session** (ruling 4): the list is `plr-sections.xml`, read by fetch on 2026-10-25; the 17 codes equal it; two entries added (number 0; `38056-8` at 17). A browser read by the Data Owner is one URL and is not required by any rule. | Data Owner |
| 3 | The reading of `maxSection17`: the build takes the highest-numbered standard section present and cuts after its first occurrence in document order, on the quoted select's `preceding-sibling` test. Whether the stylesheet picks the highest number or the last standard section in document order was not read. Equal when the sections are in PLR order, as the three labels are expected to be. **Answered in the second session** (ruling 4): `maxStdSectionNumber` is `max` over `@number[. <= 17]` of the standard sections present (`spl-common.xsl` lines 66 to 71), the highest number; the build's reading stands. | Data Owner, Engineering |
| 4 | A top-level UNSCORABLE that read nothing writes an empty `sources/` with an empty `index.json`. Taken as "every response read", none. | Security |
| 5 | This PR is named #18 without reading the repository's PR list (`gh` refused). **Answered in the second session**: opened as #18. | Product |
| 6 | The result gains three keys (`rows_carried_diverging`, `carried` per row, `fields_carried_checked`) and the summary a column; `section_effective_times` changes shape (top-level sections with `why`, not every section). No SPEC rule names the result's shape; M02's README describes the old one and is not edited beyond Unsure 23. | Engineering, Product |
| 7 | The session's command budget was spent on branch creation (two refusals), so the PR is not open and the run is not observed. Whether a session with no approval surface should edit the working tree at all, or stop at the first refusal, is a rule for Product. The edits are uncommitted and reversible. | Product |
