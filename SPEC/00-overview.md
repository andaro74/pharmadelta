# SPEC/00 — Overview: pharmadelta, a labeling impact demo on agentkeel

Status: DRAFT, not adopted · Owner: Product seat · Drafted 2026-10-09 from
the handoff brief of 2026-10-08 and a read of `andaro74/agentkeel` at tag
`m08` (`0ba6d1d`), `agentkeel-studio/window-check` and this repository at
`77330e8`. The code was read, not run. Adoption is by ADR-0001 in the
adoption pull request, which also rules on every item in §12.

This file is the authority. If `CLAUDE.md`, the README or a chat summary
disagrees with it, this file wins and the other gets a pull request.

## 1. What this is

A demo that answers one question for a fictional generics company: **a
labeling rule changed; which of our labels does it touch, and what do we
owe?** Every answer cites one row of the company's label table and one
clause of FDA regulation.

The agent that answers is a tenant of agentkeel
(`github.com/andaro74/agentkeel`). It is created from agentkeel's
template, its seats are filled, and agentkeel checks, signs and deploys
it. This repository holds what surrounds the agent: the tests for the
demo, the naive baseline it is compared with, the code that builds its
table from FDA sources, and the public pages.

One sentence for the README: *pharmadelta shows what changed in FDA drug
labeling and which labels it touches, with a citation on every claim, from
an agent whose rules, tests and thresholds each have a named owner.*

Two audiences. Executives see the same question answered by an ordinary
assistant and by the governed agent. Architects and auditors see the
evidence behind each answer.

## 2. What it is not

- Not a validated system. No page, README or commit says "validated",
  "compliant" or "Part 11 compliant". The wording is: *it produces the
  evidence a validation would need.*
- Not medical information. The agent assesses regulatory impact on
  labeling. It never answers a treatment question.
- Not a statement about any marketed product. The company and the status
  of its portfolio are fictional. The labels are real public-domain labels
  of old off-patent generics. No Pfizer brand, and no brand name of any
  marketed product, appears anywhere.
- Not a platform. Guardrail rules per agent and a public caller are
  agentkeel features. They are built in agentkeel, under its own SPEC and
  its own Claude project. This repository flags them and waits.
- Not affiliated. The README carries: "pharmadelta is an independent
  open-source demo and is not affiliated with any pharmaceutical company."

## 3. Three repositories

| Repository | Holds | Authority for |
|---|---|---|
| `andaro74/pharmadelta` (this one) | SPEC, ledger, the demo's golden set, the frozen baseline, ingestion, the public API and pages | what the demo claims and what was measured |
| `agentkeel-studio/label-impact` (created at M01, not before) | the agent: `manifest.yaml`, `agent.py`, `prompt.txt`, `tools/`, `data/table.json`, `data/clauses.json`, `goldens/` | the deployed agent and its own tests |
| `andaro74/agentkeel` | the platform: checks, signing, deploy, guardrail, registry, audit | everything a tenant cannot change |

The agent repository's creation time starts agentkeel's
time-to-governed-agent clock (agentkeel SPEC/06). So it is created at M01,
from a template re-made at `m08`. The template in use today was made from
an older commit (`window-check` records `39031e7`, `platform_version: m06`).

## 4. Principles

Taken from agentkeel SPEC/00 §4 and kept here without change of meaning.

P1. **A claim needs a false state.** A milestone opens by naming the
    commit or input that makes its claim false.
P2. **Plant first, build second.** The failure is committed before the
    code that catches it.
P3. **One claim, one planted failure, one measured verdict** per
    milestone.
P4. **Only CI-written results are evidence.** A local run is not.
P5. **Baseline first, and frozen.** `src/baseline/` is the control. After
    tag `m00` it is never improved. Every number is a delta against it.
P6. **The tests never supply the answer.** A golden does not state the
    fact its own row holds.
P7. **Sources before claims.** A CFR or Federal Register citation is
    checked against the source before it enters a golden, the table, the
    clauses or a page (§10).
P8. **Sample data says so.** Anything scripted on a page is labelled.

## 5. Seats

agentkeel gives every agent seven seats. Each is a GitHub login that
administers the agent repository. On this project one person holds all
seven (agentkeel ruling R1), and every page that shows a seat says so.

The pages show a pharma function beside each seat. This is the proposed
mapping.

| agentkeel seat | Decides, for this agent | Function shown on the pages |
|---|---|---|
| `product` | what the assessment covers and when it is acceptable | Regulatory Affairs |
| `rule-owner` | what the agent may say and do: no treatment answers, no off-label answers, what happens to an adverse event | Medical Affairs |
| `data-owner` | what CORRECT means: the label table, the clauses, the goldens | Labeling Operations |
| `tool-owner` | the tool's contract | Platform Engineering |
| `threshold-owner` | the bars and the model pin | Quality |
| `security` | what tooling and infrastructure may do | Security |
| `engineering` | that it works | Engineering |

What this changes in the two mockups, which show six functions
(Regulatory, Medical Affairs, Pharmacovigilance, Legal, Security,
Quality):

- **Pharmacovigilance and Legal hold no seat.** agentkeel has one
  `rule-owner`, and three functions would want it. A page must not show a
  function signing that has no seat behind it. They may appear as
  "consulted", never as a signature.
- **Labeling Operations, Platform Engineering and Engineering are added.**
- **`rule-owner` decides nothing today.** Every tenant pins the platform's
  guardrail, and a `rules/` folder in the agent repository is not read
  (agentkeel `docs/developer/template-README.md`). Until agentkeel's next
  milestone (§8, P) the Medical Affairs seat is a name on a manifest.

M06's reviewer sign-off is built in the website layer of this repository.
It is not an agentkeel seat and not a platform control, and the page says
so.

## 6. The agent: `label-impact`

A table-and-clause agent, the only kind agentkeel's template makes today.
No knowledge base, no judge, no human review step, no calls between agents
(agentkeel `docs/developer/quickstart.md`).

- **One tool.** It returns one row of the table and the clauses that row
  can be read under. It decides nothing. The model decides, from the row.
- **A row** is one label × one labeling section × one requirement. The
  table is `data/table.json`, a list of rows keyed by `table_row`.
- **A clause** is the text of one CFR paragraph, in `data/clauses.json`,
  keyed by a clause id.
- **An answer** is one JSON object carrying `table_row`, `clause_id` and
  the answer fields. agentkeel's scorer passes it only if the row and the
  clause exist in the agent's data and every field matches the golden.

Limits read from agentkeel's code that shape the table:

| Limit | Where | Consequence |
|---|---|---|
| A row value is a string, a boolean or null | `scripts/load_rights_table.py`, `agent.rights_rows` | no numbers, no lists, no nested fields in a row; a date is a string |
| Rows are keyed by `table_row`, unique | `src/validate/agent_goldens.py`; DynamoDB partition key | settles the brief's "table loading" risk: the loader keys on `table_row` and the table is named `agentkeel-<name>-rights` |
| An agent's goldens are `ordinary` or `trap` only | `src/validate/agent_goldens.py` | see §7 |
| Agent name 3 to 31 characters, lower-case, fictional | `src/validate/agent.py` | `label-impact` fits |
| Row fields and clause ids are the agent's own | agentkeel SPEC/07 §2 | the quickstart's "keep the row fields until M07" sentence is out of date; the tool, its schema and the prompt are rewritten for labels |

The row's fields are fixed at M00 by the Data Owner with the first
goldens, not here.

## 7. The six scenarios, and where each can be measured

The agent repository accepts two kinds of golden. The platform's
guardrail is built from the film agent's rules. So today three of the six
scenarios can be measured on the deployed agent and three cannot.

| # | Scenario | Kind | Measurable on the deployed agent |
|---|---|---|---|
| 1 | An ordinary impact question | `ordinary` | from M01 |
| 2 | A superseded rule | `trap` | from M01 |
| 3 | A rule that does not apply to a generics company | `trap` | from M01 |
| 4 | A buried adverse event | `trap`, proposed (§12, U3) | from M01 if ruled a trap; otherwise after P |
| 5 | An off-label question | `guardrail` | after P |
| 6 | A prompt injection in a pasted document | `redteam` | after P |

Until P closes, scenarios 5 and 6 live in this repository's golden set
only. They are run against the baseline, they are reported as never
passed, and no page calls them blocked. A scenario counts as blocked only
when the platform's guardrail stops it and the trace names the rule.

## 8. Milestones

Each row is one claim, one planted failure, one measured verdict. The
falsifiers and seeded commits are written when each milestone opens.

| M | Claim | Days | Repository | Needs |
|---|---|---|---|---|
| 00 | Goldens, traps and a naive baseline that fails them | 2 | pharmadelta | a hand-built seed table and clauses, citations checked |
| 01 | The agent is created from the re-made template, seats filled, deployed | 2 | agentkeel-studio | the template re-made at `m08` |
| 02 | Table and clauses are built from live FDA sources, versioned by effective date | 3 | pharmadelta | regdelta's ingestion, scope changed to 21 CFR 201 and 314 |
| P | Per-agent guardrail rules and one approved public caller | 3 to 4 | agentkeel | its own SPEC; not designed here |
| 03 | A public API and the detail page call the deployed agent | 3 | pharmadelta | P closed |
| 04 | The side-by-side page runs the baseline live | 2 | pharmadelta | M03 |
| 05 | "Try to break it" is wired to agentkeel's planted failures | 2 | pharmadelta | M03 |
| 06 | Reviewer sign-off and a downloadable evidence package | 3 | pharmadelta | M03 |
| 07 | A second agent is created on a stopwatch | 1 to 2 | agentkeel-studio | M01 |

Sum of the rows: M00 to M04 is 12 days, plus 3 to 4 for P, which must
close before M03. All nine rows are 21 to 23 days.

## 9. Data

- **Regulations.** 21 CFR Parts 201 and 314, the Federal Register and FDA
  guidance. US government works, public domain.
- **Labels.** Five to ten real labels from DailyMed for old off-patent
  generics that were never Pfizer brands. Each is recorded by its DailyMed
  set id and the date it was read.
- **The company.** Fictional. Its name, its portfolio status and every
  "our label" statement are invented and labelled as such.
- **M00 uses a seed.** M00's goldens must cite rows and clauses that
  exist, and the live build is M02. So M00 carries a small table and
  clause file written by hand, each line checked against its source. M02
  replaces it and must reproduce it.

## 10. Citations checked

Checked on 2026-10-09 against Cornell LII's text of the CFR. ecfr.gov
refused the automated read, so the eCFR check the brief asks for is still
open (§12, U6). All five citations in the mockups exist and are about
what the mockups use them for.

| Citation | What it is | Note |
|---|---|---|
| 21 CFR 201.57(c)(9)(i) | Use in specific populations, 8.1 Pregnancy | applies to labels in the 201.56(d) format |
| 21 CFR 314.70(c)(6)(iii)(A) | Changes being effected: add or strengthen a contraindication, warning, precaution or adverse reaction | written for the holder of an approved NDA; how far it reaches an ANDA holder is the point of scenario 3 and needs its own check |
| 21 CFR 314.94(a)(8)(iv) | ANDA labeling: side-by-side comparison; proposed labeling the same as the reference listed drug's, with listed exceptions | |
| 21 CFR 314.80(c)(1)(i) | Postmarketing 15-day "Alert reports" | serious and unexpected, within 15 calendar days |
| 21 CFR 314.98 | Postmarketing reports for an approved ANDA | (a) sends the ANDA holder to 314.80 |

## 11. Rules for pages and prose

- Never "validated", "compliant", "Part 11 compliant", "governed",
  "secure" or "proven" about a control that has not fired on its planted
  case.
- Every answer on a page shows its row and its clause.
- The "ordinary assistant" is a real run of the frozen baseline from M04.
  Before M04 it is labelled an illustration.
- A number on a page comes from a CI-written result and links to it.
- LabelKeel is a placeholder name for the detail page.

## 12. Unsure — each needs a ruling at adoption

| # | Item | Seat | Proposed |
|---|---|---|---|
| U1 | The seat mapping in §5, and Pharmacovigilance and Legal without a seat | Product | as §5 |
| U2 | The first agent's name | Product | `label-impact` |
| U3 | The buried adverse event as a `trap` whose answer carries an escalation field and cites the 314.80 or 314.98 clause, so it is measured at M01 without the guardrail | Data Owner, with Rule Owner | yes; the alternative waits for P |
| U4 | Which five to ten labels | Data Owner | chosen at M00 open; no Pfizer originator brand, checked per product |
| U5 | The row's fields and the answer's fields | Data Owner, Tool Owner | fixed at M00 with the first goldens |
| U6 | The five citations against eCFR itself, by hand | Data Owner | before M00 PR 1 |
| U7 | Scenario 3's rule: which paragraph says a generics company may not make the change on its own | Data Owner | checked at M00; not yet verified |
| U8 | The repository was not created empty. `77330e8` holds GitHub's README, LICENSE and `.gitignore`, so history does not start with a ruling | Product | accept; the adoption pull request is #1 |
| U9 | The PR cap and the PR shape (agentkeel: cap four; plant, measure, repair, close) | Product | same as agentkeel |
| U10 | A trademark search on the name | Product | before any commercial use; not needed for the demo |
