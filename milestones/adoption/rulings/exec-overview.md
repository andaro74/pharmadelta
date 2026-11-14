---
ruling: exec-overview
seat:
  - Product
  - Data Owner
  - Security
authorises:
  # Product: the executive overview page and its three pictures (rulings 1 to 4)
  - pages/overview.html
  - docs/assets/workflow-one-rule-change.svg
  - docs/assets/workflow-today-and-with.svg
  - docs/assets/workflow-who-owns-what.svg
  # Product: the walkthrough (ruling 5)
  - docs/demo-walkthrough.md
  # Product: the front page's header image, "Start here" and the nav link; the figure rule; the README's line (ruling 6)
  - index.html
  - pages/assets/site.css
  - README.md
  - milestones/adoption/rulings/exec-overview.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/adoption/rulings/three-traps.md
  - milestones/adoption/rulings/readme.md
  - goldens/g-002.yaml
  - goldens/g-003.yaml
  - goldens/g-004.yaml
  - milestones/M00/fields.md
  - pages/api/answers.json
  - pages/api/baseline.json
  - https://github.com/andaro74/pharmadelta/actions/runs/43621291917
pr: https://github.com/andaro74/pharmadelta/pull/45
---

# Ruling: the executive overview

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9). It carries no claim,
plants nothing and measures nothing. No ledger row, served file, page
writer, gate or workflow is touched, and no call to the agent was made.
The owner asked on 2026-11-14 for workflows a pharma executive can
read: what the problem is and how the demo answers it. It is built on
top of `three-traps` (#44) and merges after it.

## Rulings in this PR

1. **Product (a sixth page, written by hand).** `pages/overview.html`
   is static. No writer builds it and no gate reads it. It says so in
   its first note: it measures nothing and shows no result of its own.
   It carries the fictional-company statement, the nav row, "what it is
   not" and the footer the other pages carry.
2. **Product, Data Owner (picture 1: one rule change).** The one answer
   drawn is `g-002`'s, as `pages/api/answers.json` serves it from CI
   run 43621291917: row `metoprolol-tartrate.8.1`, clause
   `201.57(c)(9)(i)`, `impacted` false, `owed` `none`, `escalate`
   false. It is drawn with its row and its clause (SPEC/00 §11), and
   the caption links the run and the side-by-side page. "No" and
   "Nothing" are those three values in plain words. "Equals the answer
   the test expects" is `rulings/expected-answer.md` 2's phrase. That
   the question's version of the rule "is no longer the rule" is the
   golden's own first line, the Data Owner's at M00. The three trap
   descriptions under the picture say what each golden's first line and
   `milestones/M00/fields.md` say, in plain words; no citation is added
   (P7).
3. **Product (picture 2: by hand and with pharmadelta).** The left lane
   is an illustration of a manual process. It is labelled three times:
   in the picture's lane header, in the picture's footer, and in a
   `.scripted` banner above it on the page (P8). It states no time, no
   cost and no error rate; nothing measured a manual process. The right
   lane states only what the ledger holds: the clauses and their dates
   (row 2), the seats (row 1), the gates that ask again (rows 4 to 6),
   the signed evidence (row 7), and SPEC/00 §11's rule that an answer
   is shown only with its row and its clause.
4. **Product (picture 3: who owns what).** The seven functions and what
   each seat decides are SPEC/00 §5's table. Pharmacovigilance and
   Legal are drawn as consulted, with no seat and no signature. The
   picture and the caption say one person holds all seven seats.
5. **Product (the walkthrough).** `docs/demo-walkthrough.md`: seven
   stops, each a page to open and what to notice. Each thing it says a
   reader will see is on that page at this commit. It ends with what a
   reader did not see: a live question, a rate, a validation.
6. **Product (the front page and the README).** `index.html` shows the
   repository's header image, a "Start here" table of two links and an
   "Overview" nav link. `pages/assets/site.css` gains one rule for
   figures. `README.md` gains one line. The four pages the writers
   build keep their five-link nav: adding a sixth means editing four
   writers and rebuilding four pages, the sign-off page among them, and
   is not done here (Unsure 1).
7. **Security (the rules on images and pages).** None of SPEC/00 §11's
   six words is in a picture, the page or the walkthrough. No number is
   a measured result: the run id and the ledger's row numbers are the
   records' own. Each picture says the company is fictional and that it
   is not medical information. No host, account id or identifier.
8. **Product.** This PR is #45, the next number on this repository
   after #44.

## What a reader can falsify

- `git diff <three-traps head>..<head> --stat` touches the nine files
  this ruling authorises and no other; nothing under `src/`,
  `.github/`, `pages/api/`, `goldens/` or `data/`.
- The five values in picture 1 equal `g-002`'s entry in
  `pages/api/answers.json`.
- Each of the seven cards in picture 3 says what SPEC/00 §5's row for
  that seat says.
- `grep -i -w -E "validated|compliant|governed|secure|proven"` over the
  nine files prints nothing.

## What this ruling does not settle

- Unsure 1: the four built pages do not link the overview in their nav.
  A reader reaches it from the front page. Adding the link is a PR that
  touches four writers.
- Unsure 2: picture 1 goes stale if a later lift serves a different
  answer on `g-002`. No gate reads the picture. It is re-drawn by hand
  then.
- Unsure 3: whether picture 2's left lane is a fair illustration of a
  manual process. It was written without a source. Product's, with
  someone who has done the job.
