---
ruling: data-owner-cleanup
seat:
  - Data Owner
  - Engineering
  - Product
authorises:
  # Data Owner: one cell, the same in both files
  - data/table.json
  - src/ingest/hand/table.json
  # Data Owner, Engineering: the Unsure marks; Product: this file
  - milestones/M02/README.md
  - milestones/adoption/rulings/data-owner-cleanup.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/fields.md
  - milestones/M02/README.md
  - milestones/M02/rulings/pr2.md
  - milestones/M02/rulings/pr3.md
  - milestones/adoption/rulings/spec00-errata.md
  - src/ingest/gate.py
  - src/ingest/dailymed.py
  - https://github.com/andaro74/pharmadelta/actions/runs/38154731153
  - https://github.com/andaro74/pharmadelta/actions/runs/38189632015
  - https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f8d16c85-50e2-4d99-afae-6fb902734e42
  - https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f39ee08d-73db-71b9-e053-2995a90a877c
  - https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=24837d82-0f3f-4482-9af0-31e5f675c30f
  - https://www.accessdata.fda.gov/spl/stylesheet/spl-common.xsl
pr: https://github.com/andaro74/pharmadelta/pull/14
---

# Ruling: Data Owner clean-up

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as the adoption PR and
the SPEC/00 errata PR were. It carries no claim, plants nothing and
measures nothing. It settles M02 Unsure 15, corrects the one
`section_terms` cell that M02 PR 3 found and left (Unsure 25), and
records Unsure 13 and 14. M02 is closed at tag `m02` (`ab72b9d`). Row P
is still open. M03 does not open here. The ledger is not touched.

## Rulings in this PR

1. **Data Owner (M02 Unsure 25 and PR 1's 8; the cell).**
   `metoprolol-tartrate.8.1`'s `section_terms` now reads "Risk Summary;
   Clinical consideration; Data" in `data/table.json` and in
   `src/ingest/hand/table.json`. It read "Risk Summary; Clinical
   Considerations; Data", the regulation's wording (201.57(c)(9)(i)
   names the subheading "Clinical Considerations"). The field is what
   the label prints today (`fields.md`), and the label prints "Clinical
   consideration": read by the Data Owner in a browser on 2026-10-11
   (Unsure 25), and read again on 2026-10-11 by a fetch of the page for
   this PR, which lists under 8.1, in order, "Risk Summary", "Clinical
   consideration", "Disease-associated maternal and/or embryo/fetal
   risk", "Fetal/Neonatal adverse reactions", "Data", "Human Data",
   "Animal Data". The cell keeps the three subheadings, as the seed's
   reading of 8.1 does on both 8.1 rows. `section_terms_read_on` stays
   2026-10-10, as Unsure 25 ruled. No other cell changes.
2. **Data Owner, Engineering (M02 Unsure 15).** Neither of the two
   moves offered. The hand files stay at `src/ingest/hand/`: they are
   the build's input and sit beside the build. The build does not read
   the carried fields from `data/`: that would make the built file equal
   the committed one by construction, which is why it does not today.
   The rule from here on: an edit to a carried field (on a row,
   `holder`, `holder_fictional`, `rld_nda`, `label_read_on`,
   `section_terms`, `section_terms_read_on`, `requirement`; on a clause,
   the Data Owner's fields the hand file holds) is made in `data/` and
   in the hand file in the same PR, and the PR body says so. This PR
   does that for one cell. The gate today writes the hand file's values
   into the built table and compares the derived fields only, so a
   divergence between the two files is not named in a result. Naming it
   (committed beside carried, as the `section_terms` entry already
   records) is a `gate.py` edit. It is owed to the next PR that edits
   `gate.py`, with Unsure 23, under Engineering, with the Security
   property restated there. Until then the rule is the Data Owner's,
   and "What a reader can falsify" below gives the check.
3. **Data Owner (M02 Unsure 13).** `label_revised`. Unsure 13 asked for
   one of two things: the three pages by hand, or the stylesheet in a
   browser. This PR read both by fetch on 2026-10-11, not in a browser,
   and says so. FDA's stylesheet answered a plain fetch (HTTP 200); it
   refused the build's automated read at M02 PR 2. The rule it holds,
   `spl-common.xsl`, template `effectiveDateHighlights`: when the
   document has an `effectiveTime`, take `effectiveTime/@value` of each
   top-level section of the structured body, excluding sections whose
   code is `48780-1` and every section after the highest-numbered
   standard section up to 17 (`maxSection17`); keep values longer than
   seven characters; sort descending; print the first as `M/YYYY` after
   "Revised: " (template `recent-effectiveDate`; `displayMonth` true,
   `displayDay` false, `displayYear` true, delimiter `/`). The select,
   verbatim:
   `/v3:document/v3:component/v3:structuredBody/v3:component[not(preceding-sibling::v3:component/v3:section/v3:code/@code = $maxSection17/@code) and not(v3:section/v3:code/@code = '48780-1')]/v3:section/v3:effectiveTime/@value`.
   The three pages print "Revised: 6/2022", "Revised: 7/2023",
   "Revised: 8/2024". The build (`dailymed.py`, `label_revised`) wrote
   `2022-06`, `2023-07`, `2024-08` in CI (run 38154731153), equal to the
   pages and to the committed cells. The build's rule is not the
   stylesheet's: it walks every section and its subsections, and it
   does not stop after section 17; the stylesheet reads top-level
   sections only and stops. On these three labels the two rules give
   the same month. A label whose Medication Guide, patient information
   or package label section carries a later `effectiveTime` than its
   content of labeling, or whose latest date sits on a subsection only,
   would differ. Ruling: the field's source is the stylesheet's rule as
   quoted; `fields.md`'s definition ("the label's own Revised: month")
   stands. The build's rule is recorded as equal on these three labels,
   not as the rule. Aligning it is a build edit, owed to the next PR
   that edits `gate.py` or `dailymed.py`, with Unsure 23 and ruling 2.
4. **Data Owner (M02 Unsure 14).** `ingredient`. The three pages' main
   headings print "Label: LISINOPRIL tablet", "Label: METFORMIN
   HYDROCHLORIDE- metformin hydrochloride tablet tablet" and "Label:
   METOPROLOL TARTRATE- metoprolol tablet", as DailyMed prints them. The
   Ingredients and Appearance table of each prints the active
   ingredient as "LISINOPRIL (UNII: E7199S1YWR)", "METFORMIN
   HYDROCHLORIDE (UNII: 786Z46389E)" and "METOPROLOL TARTRATE (UNII:
   W5S57Y3A5L)", each with its active moiety in parentheses
   ("LISINOPRIL ANHYDROUS", "METFORMIN", "METOPROLOL") and its basis of
   strength. The committed `ingredient` on all seven rows equals the
   active ingredient's substance name, lowercased, and the CI run
   matched it on all seven. `genericMedicine/name` reads "Metformin
   Hydrochloride Tablet" and "METOPROLOL" on two of three (M02 PR 2,
   construction item 6). Ruling: the source is the substance name
   (`ingredientSubstance/name` of each product's active ingredient).
   Not the active moiety, not the generic medicine name. `fields.md`'s
   wording, "the established name as the label title gives it", is
   M00's and is not edited; on these three the title's established name
   and the substance name are the same words. A label where they
   differ is a new ruling.
5. **Product.** This PR is #14, the next number on this repository.
   Nothing in `milestones/README.md` changes. Row P is still open and
   must close before M03 opens.

## What a reader can falsify

- `git diff main --stat` touches four files: `data/table.json`,
  `src/ingest/hand/table.json`, `milestones/M02/README.md` and this
  file. The first two are one changed line each, the same line.
- The two files agree on every carried field of every row:

  ```
  python -I -c "import json;d={r['table_row']:r for r in json.load(open('data/table.json'))};h={r['table_row']:r for r in json.load(open('src/ingest/hand/table.json'))};k=('holder','holder_fictional','rld_nda','label_read_on','section_terms','section_terms_read_on','requirement');print([(i,f) for i in h for f in k if d[i][f]!=h[i][f]])"
  ```

  prints `[]`.
- The M02 gate on this PR writes `verdict: GREEN`, 9 of 9 clauses and
  7 of 7 rows, and its `metoprolol-tartrate.8.1` entry's
  `section_terms.committed` reads the new value with `compared` false.
  Observed on the PR run at `595dd68`,
  [38189632015](https://github.com/andaro74/pharmadelta/actions/runs/38189632015),
  artifact `m02-gate-e20e9be161435e48436ed31bb79b6c71133635fc`:
  `verdict` `GREEN`, `written_by_ci` true, `clauses_mismatched` `[]`,
  `rows_mismatched` `[]`; the entry's `committed` reads "Risk Summary;
  Clinical consideration; Data" and its `headings_read` lists "Risk
  Summary", "Clinical consideration", "Disease-associated maternal
  and/or embryo/fetal risk", "Fetal/Neonatal adverse reactions",
  "Data", "Human Data", "Animal Data", the same list the page fetch
  read (ruling 1). The M01 gate on the same PR exits 3 (registry
  unread, no AWS credential), as on #13; it is not required and not
  this PR's.
- `spl-common.xsl` at the URL above holds the template and the select
  quoted in ruling 3.
- The three DailyMed pages print the "Revised:" lines and the active
  ingredient names quoted in rulings 3 and 4.
- `grep -rn "Clinical Considerations" data/ src/ingest/hand/` matches
  three lines: `lisinopril.8.1`'s cell in both files, which the
  lisinopril page prints that way (Unsure 25), and 201.57(c)(9)(i)'s
  `text` in `data/clauses.json`, the regulation's own wording. No
  `metoprolol-tartrate.8.1` line.

## What this ruling does not settle

- Two build edits, both owed to the next PR that edits `gate.py` or
  `dailymed.py`, with Unsure 23: naming a divergence between `data/`
  and the hand file (ruling 2); aligning `label_revised` to the
  stylesheet's rule (ruling 3). Engineering, Security.
- `fields.md`'s wording for `ingredient` (ruling 4) and for
  `section_terms_read_on`, which calls the date an automated read while
  one cell now holds the hand's reading. M00's file; Data Owner, in the
  milestone that touches it.
- The two fetch reads of this PR (the three pages, the stylesheet)
  repeated in a browser by the Data Owner. Four URLs. No rule requires
  it; the PR body lists them.
- label-impact's `data/` copy (M02 Unsure 6), Unsure 16 to 20, and
  M02 PR 1's 2, 5, 9 and 10, each carried with its seat.
