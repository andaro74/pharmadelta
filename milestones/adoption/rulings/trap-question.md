---
ruling: trap-question
seat:
  - Product
  - Data Owner
  - Engineering
  - Security
authorises:
  # Product: a second question, the trap g-002, served on both pages from CI records (rulings 1, 2); the front page's two cells (ruling 6)
  - pages/api/answers.json
  - pages/detail.html
  - pages/api/baseline.json
  - pages/side-by-side.html
  - index.html
  # Data Owner, Security: the agent's free text is on no page beside a shown answer (ruling 3)
  - src/m03/lift.py
  # Engineering: the lift asks a golden the API does not serve yet; the M04 writer appends an id (ruling 4)
  - src/m03/lift.py
  - src/m04/lift.py
  - .github/workflows/m03-lift.yml
  # Product: the record (ruling 7)
  - milestones/README.md
  - milestones/M04/README.md
  - milestones/adoption/rulings/trap-question.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M03/README.md
  - milestones/M04/README.md
  - milestones/M05/README.md
  - milestones/adoption/rulings/m03-relift.md
  - goldens/g-002.yaml
  - src/m03/lift.py
  - src/m04/lift.py
  - https://github.com/andaro74/pharmadelta/actions/runs/43604067436
  - https://github.com/andaro74/pharmadelta/actions/runs/43604067705
  - https://github.com/andaro74/pharmadelta/actions/runs/41250971500
  - https://github.com/andaro74/pharmadelta/actions/runs/38058191295
pr: https://github.com/andaro74/pharmadelta/pull/40
---

# Ruling: a second question on the side-by-side page, the trap g-002

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as #1, #13 to #18, #31,
#32 and #37 to #39 were. It carries no claim of this repository, plants
nothing and measures nothing. M03 and M04 are closed at 4 / 4, rows 4
and 5 GREEN; no cell and no state is touched. It answers M03's Unsure
35, asked for by the owner on 2026-11-14: after the M03 re-lift both
columns of the side-by-side page read the same on `g-001`. Three
commits over `e26b030`: the code (`4bfa4d8`), the pages (`6eb0235`) and
this record. M07 does not open here.

## Rulings in this PR

1. **Product (which trap).** `g-002`, scenario 2 of SPEC/00 §7, a
   superseded rule. It was fixed before any call to the agent, by one
   rule: it is the trap row 0's measurement names. The agent's answer
   was to be served whatever it was. `g-003` and `g-004` are not served
   (Unsure 32).
2. **Product (served from records on both sides).** The agent's entry
   is what `src.m03.lift write` writes from the artifact of CI run
   43604067436 (`workflow_dispatch` with `also` `g-002`, `ok` true,
   `written_by_ci` true): `metoprolol-tartrate.8.1`, `201.57(c)(9)(i)`,
   `impacted` false, `owed` `none`, `escalate` false, with its row, its
   clause and its call record. The ordinary assistant's entry is what
   `src.m04.lift write --also g-002` writes from the artifact of run
   41250971500, the run the file already named: the same row and
   clause, `impacted` true, `owed` `follow-rld`, `escalate` false. No
   hand-written entry was committed at any commit (P1, P8). The page
   shows two records and does not say which the golden expects (Unsure
   33).
3. **Data Owner, Security (the agent's free text).** The door's `text`
   on `g-002` carried prose after the JSON object: a word SPEC/00 §11
   bans on a page, and a citation of 21 CFR 201.56(e) not checked
   against the source (P7). `src/m03/lift.py` serves `door.text` only
   where no answer is shown with its row and its clause (M03 Unsure
   26); beside a shown answer it is null, for `g-001` too. The text
   stays in the run's artifact, as the guardrail's message does at M05
   (Unsure 22). The prose itself is label-impact's to read (Unsure 34).
4. **Engineering (how a new question is first served).**
   `src/m03/lift.py call --also <ids>` asks each id the served file
   does not hold with its golden's question; `m03-lift.yml` takes the
   dispatch input `also` as an environment value; `src/m04/lift.py
   write --also <ids>` appends an id. With no `--also` every rebuild is
   as before. No gate changes: both gates already read every served
   entry.
5. **Security (nothing of the door in a file).** Both artifacts, the
   four served files, the two pages, the commit messages and this file
   hold no door host, pool id or client id. The password was not typed
   in this session.
6. **Product (the front page).** `index.html`'s two table cells say two
   questions, one a trap about a rule no longer in force. No number, no
   answer.
7. **Product (the record).** `milestones/README.md`: every row cell
   unchanged; one paragraph under the rows. `milestones/M04/README.md`:
   the section "A second question: the trap g-002" with Unsure 32 to
   37. The gates' readings go in comments on #40; no tag.
8. **Product.** This PR is #40, the next number on this repository.

## What a reader can falsify

- `git diff e26b030..<head> --stat` touches the eleven files this
  ruling authorises and no other.
- Rows 0 to 8 of `milestones/README.md` are byte-for-byte as at
  `e26b030`.
- `gh run download 43604067436` and a `src.m03.lift write` from it,
  then `gh run download 41250971500` and a `src.m04.lift write` from
  it, leave `git status --short` empty on the head.
- `git log -1 --format=%h -- pages/api/sign-off.json` reads `37352ef`.

## What this ruling does not settle

- Unsure 32: whether `g-003` or `g-004` joins. Product.
- Unsure 33: whether the page states the golden's expected answer.
  Product, Data Owner.
- Unsure 34: the agent's prose after its object. label-impact's.
- Unsure 35: one sentence on the page saying the free text is not
  shown. Product, Security.
- Unsure 36: the gate's calls per run doubled. Threshold Owner.
- M07 (row 8), in its own session.
