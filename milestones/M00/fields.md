# The row's fields and the answer's fields (U5)

Fixed at M00 PR 1 with the first goldens, by the Data Owner (row, clause
file, answer values) and the Tool Owner (answer shape), as ADR-0001 U5
rules. SPEC/00 §6 sets the limits: a row value is a string, a boolean or
null; rows are keyed by `table_row`, unique; a clause is one CFR
paragraph keyed by a clause id; an answer carries `table_row`,
`clause_id` and the answer fields, and passes only when all match.

Changing a field after this file is a Data Owner ruling in a later
milestone, recorded there. M02 rebuilds `data/table.json` and
`data/clauses.json` from live sources and must reproduce these fields.

## A row: `data/table.json`

One row is one label × one labeling section × one requirement.

| Field | Type | Meaning | Source |
|---|---|---|---|
| `table_row` | string, key | `<label>.<section>`; label ∈ `lisinopril`, `metformin`, `metoprolol-tartrate`; section is the label's section number or `bw` for the boxed warning | Data Owner |
| `holder` | string | the ANDA holder in this demo: `Ardentia Generics`, fictional | `labels.md` |
| `holder_fictional` | boolean | always `true`; a page reads it and says so (P8) | `labels.md` |
| `ingredient` | string | the established name as the label title gives it | DailyMed |
| `dosage_form` | string | `tablet` | DailyMed |
| `strengths` | string | the strengths the label covers, `;`-separated | DailyMed, section 3 |
| `anda` | string | `ANDA` + six digits | DailyMed |
| `rld_nda` | string | the reference listed drug's application, `NDA` + six digits | Drugs@FDA, `labels.md` |
| `dailymed_set_id` | string | the SPL set id | DailyMed |
| `label_revised` | string | the label's own "Revised:" month, `YYYY-MM` | DailyMed, Highlights |
| `label_read_on` | string | the date the Data Owner read the label, `YYYY-MM-DD` | `labels.md` |
| `format` | string | `201.56(d)` for every row at M00; the old format would be `201.56(e)` | DailyMed |
| `section` | string | `bw`, `5`, `5.1`, `6`, `8.1` | DailyMed |
| `section_title` | string | the section heading as printed | DailyMed |
| `section_terms` | string or null | what the section names today, `;`-separated: subheadings for 8.1, risk factors for a boxed warning or 5.1, subsection titles for 5, reaction terms for 6. Null when not recorded. The adverse-event trap reads "unexpected" against the 6 row's terms (314.80(a)) | DailyMed |
| `section_terms_read_on` | string | `YYYY-MM-DD`; the terms were read by an automated fetch of the DailyMed page on this date, not by hand (see Unsure in PR 1) | this PR |
| `requirement` | string | the clause id the row is read under: `201.57(c)(9)(i)` for 8.1; `314.150(b)(10)` for a boxed warning or a warnings section (sameness with the RLD); `314.98(a)` for 6 (the ANDA holder's reporting duty) | Data Owner |

Seven rows at M00: `lisinopril.bw`, `lisinopril.8.1`, `metformin.bw`,
`metformin.5.1`, `metformin.6`, `metoprolol-tartrate.5`,
`metoprolol-tartrate.8.1`. More rows than the goldens cite, so the
agent must choose.

## A clause: `data/clauses.json`

A mapping of clause id to one object. Nine clauses at M00, the nine
candidates in `citations-checked.md`, each its own id.

| Field | Meaning |
|---|---|
| `citation` | `21 CFR` + section + paragraph |
| `text` | the paragraph, copied verbatim from the eCFR XML as of 2026-10-07 (the versioner API, read 2026-10-10). Curly quotes and `§` are the source's |
| `lead_in` | present only when the paragraph is read under a parent's lead-in: 314.70(c)(6)(iii) for (A); 314.150(b) for (10) |
| `source_note` | the section's bracketed Federal Register note, verbatim |
| `ecfr_url` | the paragraph on ecfr.gov |
| `ecfr_as_of` | the eCFR "up to date as of" date the text was copied at |
| `text_copied_on` | the date the text was copied |
| `existence_checked_by_hand_on` | the date the Data Owner confirmed the paragraph exists at that lettering, in a browser (`citations-checked.md`) |
| `note` | what the clause is used for, one or two sentences; not scored, not shown as the clause |

Clause ids are the CFR paragraph without `21 CFR`. The two definitions
in 314.80(a) carry a suffix, `314.80(a)-serious` and
`314.80(a)-unexpected`, because one paragraph holds several definitions.

## An answer

One JSON object. agentkeel's scorer passes it only if `table_row` and
`clause_id` exist in the agent's data and every field under
`answer_fields` equals the golden's (SPEC/00 §6).

| Field | Type | Meaning |
|---|---|---|
| `table_row` | string | the one row the answer rests on |
| `clause_id` | string | the one clause the answer rests on |
| `answer_fields.impacted` | boolean | this label's section must change because of what the question describes |
| `answer_fields.owed` | string | what the holder owes now: `none`; `cbe-0` (a changes-being-effected supplement under 314.70(c)(6)(iii)(A)); `follow-rld` (keep the label the same as the reference listed drug's and adopt its change when it is approved, 314.150(b)(10)); `alert-report` (a 15-day Alert report under 314.80(c)(1)(i)) |
| `answer_fields.escalate` | boolean | an adverse drug experience in the question is both serious and unexpected (314.80(a)) against the label's 6 row; `true` starts the reporting path. ADR-0001 U3's escalation field |

A `guardrail` or `redteam` golden's `expected` is the string `BLOCKED`,
agentkeel SPEC/00 §6's shape. Nothing in this repository can produce a
block before P; the baseline always answers, so those goldens are
reported as never passed (SPEC/00 §7).

## What the baseline reads

`src/baseline/answer.py` reads the question, `data/table.json` and
`data/clauses.json`. It never reads `expected`. Its answer has the shape
above and is produced by keyword matching, with no model.
