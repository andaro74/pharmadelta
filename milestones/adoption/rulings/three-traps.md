---
ruling: three-traps
seat:
  - Product
  - Data Owner
  - Security
authorises:
  # Product: g-003 and g-004 served on both pages, each side from a CI record (rulings 1, 2)
  - pages/api/answers.json
  - pages/detail.html
  - pages/api/baseline.json
  - pages/side-by-side.html
  # Product: the front page and the README say four questions (ruling 4)
  - index.html
  - README.md
  # Product: the record (ruling 5)
  - milestones/README.md
  - milestones/M04/README.md
  - milestones/adoption/rulings/three-traps.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M04/README.md
  - milestones/adoption/rulings/trap-question.md
  - milestones/adoption/rulings/expected-answer.md
  - goldens/g-003.yaml
  - goldens/g-004.yaml
  - https://github.com/andaro74/pharmadelta/actions/runs/43621291917
  - https://github.com/andaro74/pharmadelta/actions/runs/41250971500
pr: https://github.com/andaro74/pharmadelta/pull/44
---

# Ruling: all three traps on the pages

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9). It carries no claim,
plants nothing and measures nothing. Rows 4 and 5 are GREEN and are not
touched. It rules Unsure 32 of `milestones/M04/README.md`, "A second
question": the owner asked on 2026-11-14 for all three traps the README
names to be on the pages. No code, gate or workflow changes: the path
is the one #40 built (`also` on the lift, `--also` on the M04 writer).

## Rulings in this PR

1. **Product (which questions).** `g-003` and `g-004`, the two `trap`
   goldens not yet served. With `g-002` they are every trap in
   `goldens/`. Nothing was chosen by the agent's answer: both ids were
   fixed before the call, and what the call returned is served.
2. **Product (served from records on both sides).** The agent's four
   entries are what `src.m03.lift write` writes from the artifact of CI
   run 43621291917 (`workflow_dispatch` on `three-traps` at `7437113`
   with `also` `g-003 g-004`, `ok` true, `written_by_ci` true, sign-in
   200, four calls 200 at `end_turn`, `guardrail_topics` `[]`,
   `agent_commit` `bd89989`). The ordinary assistant's four entries are
   what `src.m04.lift write --also "g-003 g-004"` writes from the
   artifact of run 41250971500. No hand-written entry at any commit.
3. **Data Owner, Security (the agent's free text).** On `g-002` and
   `g-004` the door's `text` carried prose after the JSON object; on
   `g-001` and `g-003` it did not. It is on no page, by the rule of
   `trap-question.md` 3. label-impact #10 holds the finding.
4. **Product (the words).** `index.html` and `README.md` say four
   questions, one ordinary and three traps. The README's shortcoming
   line says four answers are not a rate.
5. **Product (the record).** `milestones/README.md`: one paragraph
   under the rows; every row cell unchanged. `milestones/M04/README.md`:
   the section "All three traps", and a "Ruled" note on Unsure 32. The
   gates' readings go in comments on #44; no tag.
6. **Product.** This PR is #44, the next number on this repository.

## What a reader can falsify

- `git diff 7437113..<head> --stat` touches the nine files this ruling
  authorises and no other; nothing under `src/`, `.github/`,
  `goldens/` or `data/`.
- Rows 0 to 8 of `milestones/README.md` are byte-for-byte as at
  `7437113`.
- `gh run download 43621291917` and a `src.m03.lift write` from it,
  then `gh run download 41250971500` and a `src.m04.lift write` from
  it, leave `git status --short` empty on the head.
- `git log -1 --format=%h -- pages/api/sign-off.json` reads `37352ef`.

## What this ruling does not settle

- Whether the agent's answers are stable: one lift call and the gate's
  calls on this PR per question.
- The M03 gate now makes four calls per run under the agent's ceilings
  (M04 Unsure 36). Threshold Owner.
- The evidence package keeps the pages as at its build.
