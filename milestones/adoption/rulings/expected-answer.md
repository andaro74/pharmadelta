---
ruling: expected-answer
seat:
  - Product
  - Data Owner
  - Engineering
  - Security
authorises:
  # Product, Data Owner: the golden's expected answer shown beside each question, and the two phrases (rulings 1, 2)
  - pages/detail.html
  - pages/side-by-side.html
  # Engineering: the two writers (ruling 3)
  - src/m03/lift.py
  - src/m04/lift.py
  # Product, Security: the sentence on the agent's free text (ruling 4)
  - pages/detail.html
  - pages/side-by-side.html
  # Product: the record (ruling 5)
  - milestones/M04/README.md
  - milestones/adoption/rulings/expected-answer.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M04/README.md
  - milestones/adoption/rulings/trap-question.md
  - goldens/g-001.yaml
  - goldens/g-002.yaml
  - pages/api/answers.json
  - pages/api/baseline.json
  - https://github.com/andaro74/pharmadelta/actions/runs/43604067436
  - https://github.com/andaro74/pharmadelta/actions/runs/41250971500
pr: https://github.com/andaro74/pharmadelta/pull/41
---

# Ruling: the expected answer on the page

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9). It carries no claim,
plants nothing and measures nothing. Rows 4 and 5 are not touched; no
served file changes; no call to the agent was made. It rules Unsure 33
and 35 of `milestones/M04/README.md`, "A second question", asked for by
the owner on 2026-11-14. Two commits over `d5b7957`: the writers and
the pages, and this record.

## Rulings in this PR

1. **Product, Data Owner (Unsure 33: the expected answer is shown).**
   Each question that has a golden shows the golden's `expected`, named
   as the Data Owner seat's, with the golden linked at the commit that
   last changed it. It is a copy of the test's answer; the block says
   no run wrote it. P6 is about what a golden may state, not about what
   a page may copy from one.
2. **Product (the two phrases).** Beside each value of a shown answer:
   "equals expected" or "differs from expected". The page compares two
   values it prints and says that this is not a measured result. It
   does not say "right", "wrong", "correct" or "passed": the baseline's
   score is row 0's, and the agent's score against its goldens is
   agentkeel's. No reason for the expected answer is written (P7).
3. **Engineering (the writers).** `expected_answer`, `expected_mark`
   and `render_expected` in `src/m03/lift.py`, used by both writers.
   The served files and the JSON blocks on the pages do not change, so
   no gate reads anything new. A rebuild reads `goldens/` and its git
   history, as it reads `data/`.
4. **Product, Security (Unsure 35: the sentence).** Under the agent's
   record on both pages: text the agent wrote beside its answer is in
   the run's artifact and is not shown.
5. **Product (the record).** `milestones/M04/README.md`: the section
   "The expected answer on the page" with Unsure 38 to 40. The ledger
   is not edited: no served record changed. The gates' readings go in
   comments on #41; no tag.
6. **Product.** This PR is #41, the next number on this repository.

## What a reader can falsify

- `git diff d5b7957..<head> --stat` touches the six files this ruling
  authorises and no other.
- Each value in a block equals the `expected` of its golden file.
- The three JSON blocks on the two pages are byte-equal to `d5b7957`.
- A rebuild from the artifacts of runs 43604067436 and 41250971500
  leaves `git status --short` empty on the head.

## What this ruling does not settle

- Unsure 38: whether a gate reads the marks in CI. Proposed no.
- Unsure 39: the evidence package keeps the pages as at its build.
- Unsure 32 of "A second question": whether `g-003` or `g-004` joins.
- M07 (row 8), in its own session.
