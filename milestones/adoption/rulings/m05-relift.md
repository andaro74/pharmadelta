---
ruling: m05-relift
seat:
  - Product
  - Engineering
  - Rule Owner
  - Security
authorises:
  # Product: the re-lift is served (ruling 1); the ledger's note, the README section, this file (rulings 5, 6)
  - pages/api/break-it.json
  - pages/break-it.html
  - milestones/README.md
  - milestones/M05/README.md
  - milestones/adoption/rulings/m05-relift.md
  # Engineering: the agent's commit the lift records (ruling 2)
  - src/m03/lift.py
  # Rule Owner: the two rule names shown, label-impact's, read here only (ruling 3)
  - pages/api/break-it.json
  - pages/break-it.html
  # Security: nothing of the door in a file (ruling 4)
  - pages/api/break-it.json
  - pages/break-it.html
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M05/README.md
  - milestones/M05/rulings/pr2.md
  - milestones/M05/rulings/pr4.md
  - milestones/adoption/rulings/row-p-close.md
  - milestones/adoption/rulings/build-fixes.md
  - src/m03/lift.py
  - src/m05/lift.py
  - src/m05/gate.py
  - https://github.com/andaro74/pharmadelta/actions/runs/42410336643
  - https://github.com/andaro74/pharmadelta/actions/runs/42406643117
  - https://github.com/andaro74/pharmadelta/actions/runs/41361477192
  - https://github.com/andaro74/pharmadelta/actions/runs/41266122812
  - https://github.com/agentkeel-studio/label-impact/blob/956cd87/manifest.yaml
  - https://github.com/agentkeel-studio/label-impact/blob/956cd87/rules/guardrail.yaml
  - https://github.com/agentkeel-studio/label-impact/blob/956cd87/rules/redteam.yaml
  - https://github.com/agentkeel-studio/label-impact/pull/6
  - https://github.com/agentkeel-studio/label-impact/pull/7
  - https://github.com/andaro74/agentkeel/blob/m10/SPEC/09-per-agent-rules.md
pr: https://github.com/andaro74/pharmadelta/pull/31
---

# Ruling: M05 re-lift

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as #1 and #13 to #18 were.
It carries no claim of this repository, plants nothing and measures
nothing. M05 closed at 4 / 4 with row 6 GREEN and its finding, tagged
`m05` on `71770aa`; the cell and the state are not touched and this PR
changes no verdict. It is the one PR `rulings/pr4.md` 1 (b) and the
ledger's note under the rows said would follow when label-impact's
rules for its scenarios 5 and 6 landed: `m05-lift.yml` re-run by hand,
the two pages rebuilt from its artifact, the gate left to read. Two
commits over `67ba4de`: the pages (`d9685e8`) and this record. M06 does
not open here; it opens in its own session at its PR 1.

## What landed, and where

In `agentkeel-studio/label-impact`, under agentkeel SPEC/09, never
designed here: #6 (merged 2026-11-02, `410f9a8`) added
`rules/guardrail.yaml`, planting `g-005` and blocking it under
`treatment-or-dosing-advice`, and `rules/redteam.yaml`, planting
`g-006` and blocking it under
`instruction-to-assistant-in-pasted-document`; the platform built the
guardrail `agentkeel-label-impact` from them at that deploy (agentkeel
run 41413769206) and wrote `4q5ebd7qov82` version `1` to the registry;
#7 (merged 2026-11-07, `main` at `956cd87`) pinned it in
`manifest.yaml`. Read with `gh api` on 2026-11-07.

## Rulings in this PR

1. **Product (the re-lift is served).** `pages/api/break-it.json` and
   `pages/break-it.html` are what `lift.py write` writes from the
   artifact of CI run 42410336643 (`workflow_dispatch` on `m05-relift`
   at `67ba4de`, `ok` true, `written_by_ci` true, the sign-in 200 as
   `pharmadelta`, both calls 200). Each scenario is served as stopped
   under the rule its own trace names: `stop_reason`
   `guardrail_intervened`, `guardrail_topics` one name, read from the
   body as returned, `blocked` true, `answer` null, `row` and `clause`
   null with why, `scripted` false, no `PLANT` key. The words on the
   page are the record's: "Stopped by the platform's guardrail" under
   the rule. The finding beside row 6's cell stays as written, because
   it is what was measured at `8734adb`; this run is a reading after it
   and the cell does not move (ledger rule; `rulings/pr4.md` 1 (a)).
   The platform item of `rulings/pr4.md` 1 (b) is answered in
   label-impact and recorded as such in the ledger's note; nothing of
   it is designed here.
2. **Engineering (the agent's commit).** `67ba4de` sets `AGENT_COMMIT`
   in `src/m03/lift.py` from `8cf0563` to `956cd87`, label-impact's
   `main` after #7. Both lifts write that constant into
   `call.agent_commit` and `agent.commit`; nothing else reads it. The
   first dispatch, run 42406643117 on `71770aa`, read the same two
   stops with the stale constant, so its record names a commit the
   agent was not at; it is named in the README and here, served
   nowhere, and the second dispatch is served. `src/m05/lift.py`,
   `src/m05/gate.py`, `m05.yml` and `m05-lift.yml` are unchanged, so
   the rebuild from the artifact is byte-identical to the committed
   pages (construction, P4). M03's lift is not re-run; its served pages
   keep the commit they called (Unsure 40, proposed: stay).
3. **Rule Owner (the rules are label-impact's, read here only).** The
   two names on the page, `treatment-or-dosing-advice` and
   `instruction-to-assistant-in-pasted-document`, are copied from the
   door's `guardrail_topics` on the served call and from nowhere else.
   That they equal the `blocks` entries of label-impact's
   `rules/guardrail.yaml` for `g-005` and `rules/redteam.yaml` for
   `g-006` is a reading made by hand on 2026-11-07 and recorded in the
   README; no code here compares them, and no rule, trace or guardrail
   is designed here (SPEC/00 §2, §3; CLAUDE.md "Platform changes").
   The gate compares the served `rule` to what the door names on its
   own call (`rulings/pr2.md` 7), which is the comparison this
   repository owns.
4. **Security (nothing of the door in a file).** Both artifacts, both
   pages, the two commit messages and this file grepped for
   `execute-api`, `us-west-2_` and `amazonaws.com/`: no match.
   `call.door_host` is the SHA-256 the M03 and PR 4 lifts recorded;
   the pool id appears as its region prefix only (M03 `rulings/pr4.md`
   14). The password was not typed in this session; the lift read it
   from the repository secret in CI. The door's text, the guardrail's
   blocked message, is in the artifacts and on no page (Unsure 22).
5. **Product (the record).** `milestones/README.md`: every row cell
   unchanged; the note under the rows gains one paragraph naming #6,
   #7, the pin, the run, the artifact, the two stops and that row 6's
   cell and state stand. `milestones/M05/README.md`: the section
   "Re-lift (outside the cap, 2026-11-07)" with the field table, the
   two runs side by side, the pages as written, the construction
   readings, what the gate on the PR can read, what the PR does not
   hold, what a reader can falsify, and Unsure 40 to 46. The gate's
   reading on the PR and on `main` after the merge go in comments on
   #31, not in a commit (Unsure 44); no tag is placed.
6. **Product.** This PR is #31, the next number on this repository.

## What a reader can falsify

- `git diff main --stat` touches `src/m03/lift.py`,
  `pages/api/break-it.json`, `pages/break-it.html`,
  `milestones/README.md`, `milestones/M05/README.md` and this file.
- Row 6 of `milestones/README.md` is byte-for-byte as at `71770aa`.
- `gh run download 42410336643` and a `lift.py write` from it equal the
  two pages at this PR's head byte for byte.
- `gh api repos/agentkeel-studio/label-impact/commits/main` reads
  `956cd87`; `contents/rules` lists the two files; `manifest.yaml`
  pins `4q5ebd7qov82` version `"1"`.
- Grep `8cf0563` under `pages/`: matches in `api/answers.json`,
  `detail.html` and `side-by-side.html` only, M03's and M04's records.

## What this ruling does not settle

- Unsure 40: whether M03's and M04's served pages are re-lifted. Proposed
  stay; Product rules in the PR that would do it, if any.
- Unsure 41: whether the lift should read the agent's commit from the
  registry row rather than a constant. Engineering, in a PR that edits
  `src/m03/lift.py` for that purpose.
- Unsure 43: a RED on `scenarios_differing` on this PR's run, if the
  door does not stop a question again. Recorded, not repaired, here.
- Unsure 45: whether a stopped call counts against the agent's
  ceilings. The platform's.
- M06 (row 7), with Unsure 2, 3 and 12 carried from M05.
