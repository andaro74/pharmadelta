---
ruling: pages-index
seat:
  - Product
  - Security
authorises:
  # Product: the front page, navigation only; no number, no answer, no scripted content
  - index.html
  # Product, Security: the record that GitHub Pages is enabled, closing Unsure 2 (M03, M04, M05, M06)
  - milestones/README.md
  - milestones/M06/README.md
  - milestones/adoption/rulings/pages-index.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M03/rulings/pr4.md
  - milestones/M04/rulings/pr4.md
  - milestones/M05/rulings/pr4.md
  - milestones/M06/rulings/pr1.md
  - milestones/M06/rulings/pr4.md
  - pages/detail.html
  - pages/side-by-side.html
  - pages/break-it.html
  - pages/sign-off.html
  - https://api.github.com/repos/andaro74/pharmadelta/pages
  - https://andaro74.github.io/pharmadelta/
pr: https://github.com/andaro74/pharmadelta/pull/37
---

# Ruling: the front page, and GitHub Pages enabled (Unsure 2)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as #1, #13 to #18, #31 and
#32 were. It changes no served file, no page under `pages/`, no gate,
no workflow and no data. It adds one file, `index.html` at the
repository root, and records a setting the owner changed by hand.

## Rulings in this PR

1. **Product, Security (Unsure 2 closed).** GitHub Pages was enabled by
   the owner on 2026-11-08 UTC, deploy from branch `main`, folder `/`,
   build type `legacy`. `GET /repos/andaro74/pharmadelta/pages` reads
   `status` `built`, `html_url` `https://andaro74.github.io/pharmadelta/`;
   the latest build is of `60494f4`, the M06 merge commit, at
   2026-11-08T23:57:53Z. Each of the four pages at
   `https://andaro74.github.io/pharmadelta/pages/<name>.html` answers
   200 and is byte-identical to the file on `main` (SHA-256 compared);
   the evidence zip at `pages/evidence/m06-evidence.zip` downloads with
   the SHA-256 the sign-off names. The item was carried by name from
   M03 (`rulings/pr4.md` 7) through M04, M05 (`rulings/pr4.md` 15) and
   M06 (`rulings/pr1.md` 8, `rulings/pr4.md` 24) as the owner's setting;
   it is closed here. No Measured cell depended on it: "public" meant
   readable in the repository at every measurement, and still does.
   Pages adds a second way to read the same bytes.
2. **Product (the front page).** `index.html` is navigation: the
   fictional-company statement every page carries, one sentence on the
   question the demo answers, a note that the pages show saved CI
   records and take no question, and links to the four pages, the
   ledger, SPEC/00, the evidence zip, the repository and the four served
   JSON files. It copies no number, shows no answer, names no brand,
   carries no scripted content and none of SPEC/00 §11's six words.
   Before it, the site root rendered the repository's README through
   Pages' Jekyll build; the README stays as it is for readers of the
   repository.
3. **Security (what Pages serves).** Pages serves `main` as it is, so
   everything on the site is already public in the repository. The
   build type is `legacy`, Jekyll: files and folders beginning with an
   underscore are not served, and none exist. No secret, no door host,
   no pool id and no token is in the tree (grepped at M06 PR 4; the
   gates grep their artifacts). Nothing is served that was not served
   by the repository before.
4. **Product (what this PR does not hold).** No live path: a visitor's
   own question still has nowhere to go, since the door needs a
   credential a browser cannot hold (M03 `rulings/pr4.md` 7), and a
   public caller is a platform item under agentkeel's SPEC, flagged and
   not designed here. No custom domain. No change to `pages/`, `src/`,
   `goldens/`, `data/` or any workflow.

## What a reader can falsify

- `git diff main --stat` on this PR touches `index.html`,
  `milestones/README.md`, `milestones/M06/README.md` and this file
  only.
- `https://andaro74.github.io/pharmadelta/` serves `index.html` once
  Pages rebuilds from the merge; each link on it resolves (200).
- `gh api repos/andaro74/pharmadelta/pages` reads `source.branch`
  `main`, `source.path` `/`, `status` `built`.
- `grep -c -i -E "validated|compliant|governed|secure|proven" index.html`
  reads 0.
