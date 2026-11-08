---
ruling: m05-count
seat:
  - Product
authorises:
  # Product: the count corrected in the README's re-lift section and its Unsure table (rulings 1, 2); this file (ruling 4)
  - milestones/M05/README.md
  - milestones/adoption/rulings/m05-count.md
evidence:
  - milestones/README.md
  - milestones/M05/README.md
  - milestones/M05/rulings/pr4.md
  - milestones/adoption/rulings/m05-relift.md
  - https://github.com/andaro74/pharmadelta/pull/31
  - https://github.com/andaro74/pharmadelta/actions/runs/41264751470
  - https://github.com/andaro74/pharmadelta/actions/runs/41265001644
  - https://github.com/andaro74/pharmadelta/actions/runs/41266122812
  - https://github.com/andaro74/pharmadelta/actions/runs/41267158120
  - https://github.com/andaro74/pharmadelta/actions/runs/41267294057
  - https://github.com/andaro74/pharmadelta/actions/runs/41268444478
  - https://github.com/andaro74/pharmadelta/actions/runs/41361477192
  - https://github.com/andaro74/pharmadelta/actions/runs/41362159234
  - https://github.com/andaro74/pharmadelta/actions/runs/41362407988
  - https://github.com/andaro74/pharmadelta/actions/runs/41364043231
  - https://github.com/andaro74/pharmadelta/actions/runs/42406643117
  - https://github.com/andaro74/pharmadelta/actions/runs/42410336643
  - https://github.com/andaro74/pharmadelta/actions/runs/42416341332
  - https://github.com/andaro74/pharmadelta/actions/runs/42416624187
  - https://github.com/andaro74/pharmadelta/actions/runs/42417261373
pr: https://github.com/andaro74/pharmadelta/pull/32
---

# Ruling: M05 call count

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as #1, #13 to #18 and #31
were. It carries no claim, plants nothing and measures nothing. It
corrects one number that `milestones/M05/README.md` states twice: how
many calls this repository's CI had made to the deployed agent as
`pharmadelta` when the re-lift run 42410336643 made its two. M05 closed
at 4 / 4 with row 6 GREEN and its finding, tagged `m05` on `71770aa`;
no cell, state or page changes here, and M06 does not open here.

## What was wrong

At #31 the README's section "The re-lift call" said eight CI runs of
two calls had read `end_turn` before the first stop, and that the
served run's calls were the nineteenth and twentieth as `pharmadelta`.
Its Unsure 47 said the same. Two gate runs were not counted: the run on
the second push of #28, 41265001644 (at `d9af4bd`), and the run on the
second push of #30, 41362407988 (at `8d66c21`). Each signed in as
`pharmadelta` and made two calls that read `end_turn`. The count was
low by four.

## The count, as read

Read on 2026-11-07 from every m05 gate and m05-lift artifact that
exists, fifteen runs, each downloaded with `gh run download` into a
fresh directory and read with `python -I`, and recorded in the second
comment on #31 (2026-11-07 21:48 UTC). This PR copies that reading; it
does not download again. A comment is a reading, not evidence (P4);
the artifacts it names are.

| Runs | What each read on both calls | Calls |
|---|---|---|
| gate 41264751470, 41265001644, 41266122812, 41267158120, 41267294057, 41268444478 (the six of row 6's finding) | `end_turn`, `guardrail_topics` `[]` | 1 to 12 |
| lift 41361477192 (PR 4) | `end_turn`, `[]` | 13, 14 |
| gate 41362159234, 41362407988 (PR 4, two pushes) | `end_turn`, `[]` | 15 to 18 |
| gate 41364043231 (`main` after #30) | `end_turn`, `[]` | 19, 20 |
| lift 42406643117 (first dispatch, not served) | `guardrail_intervened`, one rule each | 21, 22 |
| lift 42410336643 (second dispatch, served) | `guardrail_intervened`, one rule each | 23, 24 |
| gate 42416341332, 42416624187 (#31, two pushes) | `guardrail_intervened`, one rule each | 25 to 28 |
| gate 42417261373 (`main` after #31) | `guardrail_intervened`, one rule each | 29, 30 |

Thirty calls: twenty `end_turn` on ten runs, ten stopped on five. Row
6's finding, "six CI runs, twelve calls", counted the six gate runs of
the first row above and is right; the cell does not move.

## Rulings in this PR

1. **Product.** The paragraph under "The re-lift call" now says ten
   runs and twenty calls read `end_turn` before the first stop, names
   each run, and says the served run's calls were the twenty-third and
   twenty-fourth. Unsure 47 says the same and points at Unsure 48.
2. **Product.** Unsure 48 is added to the README's "Unsure (re-lift)"
   table: what was not counted, the reading it is corrected from, and
   that this PR carries the correction.
3. **Product.** The messages of `d9685e8` ("the first CI run from this
   repository to read so") and `1065863` ("nineteenth and twentieth"),
   and the first comment on #31, are not rewritten (Unsure 39's and
   47's shape). The README is the place a reader is sent to; the
   messages and the comment stand as written, with the README naming
   the error.
4. **Product.** This PR is #32, the next number on this repository. It
   is opened before M06 PR 1, which may not touch `milestones/M05/`,
   and shares no file with it.

## What a reader can falsify

- `git diff main --stat` on this PR touches `milestones/M05/README.md`
  and `milestones/adoption/rulings/m05-count.md` only.
- `grep -n "nineteenth and twentieth" milestones/M05/README.md` finds
  the phrase only inside Unsure 47's sentence naming it as the count
  #31 wrote; `grep -n "Eight CI runs"` finds nothing.
- Row 6 of `milestones/README.md` is byte-identical to `main`'s.
- Each run named in the table above exists under this repository's
  Actions and carries an `m05-gate-<sha>` or `m05-lift-<sha>`
  artifact; its `result.json` or `call.json` reads two calls with the
  `stop_reason` the table gives.
- `git ls-files --eol` reads `i/lf w/lf` on both files.

## What this ruling does not settle

Nothing of M06. Unsure 39, 47 and 48 are the same shape: a count or a
sentence written into a commit message or a comment that a later read
corrected. Whether a commit message should ever carry a count that a
README also carries is Product's, not ruled here.
