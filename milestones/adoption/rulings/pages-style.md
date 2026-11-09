---
ruling: pages-style
seat:
  - Product
  - Security
  - Engineering
authorises:
  # Product: the look; one stylesheet for the five pages
  - pages/assets/site.css
  # Product, Engineering: the writers' head, nav row and classes; the agent commit read from the call record
  - src/m03/lift.py
  - src/m04/lift.py
  - src/m05/lift.py
  - src/m06/page.py
  # Product: the four pages rebuilt by their writers, and the front page
  - pages/detail.html
  - pages/side-by-side.html
  - pages/break-it.html
  - pages/sign-off.html
  - index.html
  - milestones/adoption/rulings/pages-style.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/adoption/rulings/pages-index.md
  - milestones/M06/rulings/pr4.md
  - pages/api/answers.json
  - pages/api/baseline.json
  - pages/api/break-it.json
  - pages/api/sign-off.json
  - https://github.com/andaro74/pharmadelta/actions/runs/41222218526
  - https://github.com/andaro74/pharmadelta/actions/runs/41250971500
  - https://github.com/andaro74/pharmadelta/actions/runs/42410336643
pr: https://github.com/andaro74/pharmadelta/pull/38
---

# Ruling: one stylesheet for the five pages

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as #1, #13 to #18, #31,
#32 and #37 were. It changes how the five pages look and not one word
of what they say. No served JSON, no gate, no workflow, no data, no
golden and no ledger cell changes.

## Rulings in this PR

1. **Product (what the stylesheet is).** `pages/assets/site.css` is one
   file, 268 lines, linked from `index.html` and the four pages under
   `pages/`. Self-hosted: no `@import`, no web font, no image, no
   script, no CDN. System font stack. Every colour is a custom property
   on `:root`, redefined once under `prefers-color-scheme: dark`; no
   colour literal appears outside those two blocks. The look is an
   evidence record: a header band carrying the fictional-company
   statement, a nav row naming the five pages with the current one
   marked (`aria-current="page"`), each record (an answer, a scenario, a
   sign-off, its signature, its package) as a card with its title, and
   the states the pages already print (No row found; Stopped by the
   platform's guardrail; `blocked` and `signed` values) as chips. The
   `.scripted` banner (P8) is the loudest element on any page that
   shows it: a 4px border, the largest text, the only upper-case block.
   The `.layer` banner on the sign-off page and the front page keeps a
   2px border and a filled background. Links to runs, rows, clauses and
   sources stay underlined text. Readable at 390px: a 16px gutter, no
   horizontal page scroll; a table with a header row keeps a 36rem
   minimum width and scrolls inside its card; hashes and tokens are
   monospace and wrap. Focus is a 3px outline. The lowest contrast of
   any foreground on its background is 6.55:1 in light and 7.13:1 in
   dark, both above WCAG AA's 4.5:1, computed from the tokens.
2. **Product, Security (what did not change).** The visible text of
   each page equals the text before this PR apart from the five nav
   words, checked by stripping tags on both and comparing; the six JSON
   blocks the gates read (`id="answer"`, `id="baseline-answer"`,
   `id="agent-answer"`, `id="scenario-g-005"`, `id="scenario-g-006"`,
   `id="signoff-s-001"`) are byte-equal; every link target is the same
   and in the same order, plus the five nav links; the count of SPEC/00
   §11's six words is 0 on each page before and after. Nothing under
   `pages/api/` changed: the four writers were re-run from the
   artifacts the served files name (runs 41222218526, 41250971500,
   42410336643, and `pages/api/sign-off.json` as it is) and wrote the
   same JSON bytes; the last commit on `pages/api/sign-off.json` stays
   `37352ef`, which the M06 gate reads as the signing commit. No gate,
   no workflow, `src/baseline/` (P5), `goldens/`, `data/`,
   `pyproject.toml`, `uv.lock` and the evidence zip are untouched. No
   number was added to a page, no answer, no brand, no treatment
   content, no door host, pool id, client id or token.
3. **Engineering (the M03 writer's agent commit).** At the M05 re-lift
   (`67ba4de`) `src/m03/lift.py`'s constant `AGENT_COMMIT` moved from
   `8cf0563` to `956cd87`, but `build_entries` stamped the constant into
   each entry's `agent.commit` instead of the call record's own
   `agent_commit`. Re-run today on the artifact of run 41222218526, the
   writer would have changed `pages/api/answers.json` and the
   `id="answer"` block to a commit the call never saw. This PR makes
   `agent.commit` the call record's `agent_commit`, as the artifact
   holds it: the rebuild then reproduces the committed page and file
   byte for byte, and a future lift records the commit its own call was
   made at. One line of record-building code, named here because the
   brief for this PR excluded such edits; the alternative was a page
   edited by hand or a served file changed, both forbidden.
4. **Product (the pages now differ from the package's entries).** The
   evidence package `pages/evidence/m06-evidence.zip` holds the four
   pages as they were at `226ad89`. After this PR the live pages differ
   from those entries in bytes. That is expected: the M06 gate compares
   each entry with its source at the commit the entry names, not with
   the live tree, so the package stays what was signed and the gate's
   reading does not change. The package is not rebuilt and the sign-off
   is not re-signed: what was reviewed was the evidence at that commit.
5. **Security (nothing new served).** Pages serves `main` as it is. The
   stylesheet is one more static file in the tree, fetched from the same
   origin; no page requests anything from another host. The scratch
   renders used to look at the pages were made with a local browser
   from the working tree and are not committed.
6. **Product (what this PR does not hold).** No JavaScript, no new page,
   no new sentence, no change to the ledger's cells or its paragraphs.
   A local run of each gate was made for construction only and read
   UNSCORABLE with every named list empty (no door secret, no
   observations file, no artifact token locally); it is not evidence
   (P4). The PR's CI runs are the reading.

## What a reader can falsify

- `git diff main --stat` on this PR touches `pages/assets/site.css`,
  the four writers, the four pages, `index.html` and this file only.
- `git log -1 --format=%h -- pages/api/sign-off.json` reads `37352ef`
  on the PR head; `git diff main -- pages/api/` is empty.
- Download the three artifacts the served files name, run each
  writer's `write` command and `uv run python -m src.m06.page write`;
  `git status` shows no change.
- Strip tags from each page on `main` and on the PR head; the texts
  are equal apart from "Front page Detail Side by side Try to break it
  Sign-off".
- `grep -c -i -E "validated|compliant|governed|secure|proven"` reads 0
  on each of the five pages.
- `grep -c -E "#[0-9a-fA-F]{3,6}" pages/assets/site.css` counts only
  lines inside the two `:root` blocks.
- `grep -E "@import|https?://|url\(" pages/assets/site.css` finds
  nothing.
