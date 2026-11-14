---
ruling: readme-overview
seat:
  - Product
authorises:
  # Product: the overview's three pictures placed in the README (rulings 1 to 3)
  - README.md
  - milestones/adoption/rulings/readme-overview.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/adoption/rulings/readme.md
  - milestones/adoption/rulings/exec-overview.md
  - docs/assets/workflow-today-and-with.svg
  - docs/assets/workflow-one-rule-change.svg
  - docs/assets/workflow-who-owns-what.svg
  - pages/overview.html
pr: https://github.com/andaro74/pharmadelta/pull/46
---

# Ruling: the overview's pictures in the README

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9). It carries no claim,
plants nothing and measures nothing. It changes `README.md` and adds
this file. No picture is redrawn: the three files are those
`exec-overview.md` authorised, read at `4d9898c`. The owner asked on
2026-11-14 for a reader to see, as soon as the repository opens, what
the demo solves for the business.

## Rulings in this PR

1. **Product (what comes first).** After the header image and the five
   lines SPEC/00 fixes or the earlier rulings placed, the first section
   is "What it solves for the business": the three things someone has to
   work out, then the two-lane picture. The second is "One rule change,
   start to finish": the six-step picture. The section that was "The
   problem" keeps its sentences under the new heading.
2. **Product (the illustration is labelled in the README too).** Under
   the two-lane picture the README says the left lane is an
   illustration written by hand, that nobody measured a manual process,
   and that it claims no time, no cost and no error rate (P8), as the
   picture and the overview page do. Under the six-step picture it
   links the CI run and the side-by-side page: the answer drawn has its
   row and its clause in the picture (SPEC/00 §11).
3. **Product (the seats).** The seven-seats picture sits in "Why an
   agent on a platform", after the table. Its alt text says one person
   holds all seven seats, as the picture does.
4. **Product.** Each picture has the alt text the overview page gives
   it. None of SPEC/00 §11's six words is added. No number is added.
   The "New here?" line now says the pictures below are also on the
   overview page.
5. **Product.** This PR is #46, the next number on this repository.

## What a reader can falsify

- `git diff 4d9898c..<head> --stat` touches `README.md` and this file
  only.
- The three image paths in the new sections are files on `main`.
- `grep -i -w -E "validated|compliant|governed|secure|proven" README.md`
  prints nothing.

## What this ruling does not settle

- The README is longer: six pictures. Whether the architecture diagram
  or the screenshot should move to a linked page is Product's.
- The pictures go stale as `exec-overview.md` says (its Unsure 2, 3).
