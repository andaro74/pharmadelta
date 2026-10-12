---
ruling: spec00-errata
seat:
  - Product
  - Data Owner
authorises:
  - SPEC/00-overview.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/citations-checked.md
  - milestones/M00/rulings/pr1.md
  - milestones/M01/rulings/pr1.md
  - milestones/M02/rulings/pr1.md
  - milestones/M02/README.md
  - https://github.com/andaro74/pharmadelta/actions/runs/38166729564
  - https://github.com/agentkeel-studio/label-impact
pr: https://github.com/andaro74/pharmadelta/pull/13
---

# Ruling: SPEC/00 errata

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as the adoption PR was. It
carries no claim, plants nothing, reads nothing. Three one-line edits to
`SPEC/00-overview.md`, owed since M00 PR 1 (Unsure 5) and M01 PR 1
(Unsure 1), named at M02 PR 1 ruling 5 as a PR of their own. The ledger
is not touched. M02 is closed at tag `m02` (`ab72b9d`); M03 does not
open here.

## Rulings in this PR

1. **Product, M01 Unsure 1.** §3 said the agent repository is created
   "from a template re-made at `m08`". It was not. `label-impact` was
   created 2026-10-10 from the template at `66ca2e4`, made from
   agentkeel `36c97dd` (`m07~1`), by Product's choice (M01 PR 1 ruling
   2). §3 now says what was done. The paragraph is otherwise unchanged.
2. **Product, with Data Owner; M00 Unsure 5a.** §10's note on 21 CFR
   314.70(c)(6)(iii)(A) said "written for the holder of an approved
   NDA". `milestones/M00/citations-checked.md` row 2 corrected it on
   2026-10-09: the subject is "the applicant", which 314.3 defines to
   include an ANDA applicant, and 314.97(a) sends the ANDA holder to
   314.70. §10's note now says that, in those words. No citation is
   added that `citations-checked.md` did not check (P7).
3. **Product, M00 Unsure 5b.** §10 said ecfr.gov refused the automated
   read and that U6 was still open. The versioner API answers when the
   request accepts gzip (M02 PR 2, construction item 2), and the M02
   gate reads it in CI: run 38166729564 on `main` at `ab72b9d`, GREEN.
   §10 now says so and links the run. U6 is not closed by that run. U6
   asked for a hand check; it was done 2026-10-09 and closed at M00 PR
   1 (`milestones/M00/rulings/pr1.md` 1). §12's U6 row is left as it
   stands, as U7's was when it closed.

## What this ruling does not settle

- §8's row 01 "Needs" column still reads "the template re-made at
  `m08`". It is a milestone row's wording, not §3's sentence, and is not
  in this PR. Owed under Product if a reader finds it misleading.
- CLAUDE.md §3 says only "created at M01, not before" and does not
  disagree with the edited §3. No CLAUDE.md PR is owed.
- Everything carried from M02: Unsure 15 (the hand files and the
  `metoprolol-tartrate.8.1` section_terms heading, with 13 and 14), 23
  (two `gate.py` findings), 6 (label-impact's data), and 16 to 20.
