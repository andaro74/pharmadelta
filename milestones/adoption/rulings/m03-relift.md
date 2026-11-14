---
ruling: m03-relift
seat:
  - Product
  - Engineering
  - Tool Owner
  - Security
authorises:
  # Product: the re-lift is served (ruling 1); the side-by-side page copies it (ruling 2); the record (ruling 6)
  - pages/api/answers.json
  - pages/detail.html
  - pages/side-by-side.html
  - milestones/README.md
  - milestones/M03/README.md
  - milestones/adoption/rulings/m03-relift.md
  # Engineering: the agent's commit the lift records; the M05 writer reads it from the call record (ruling 3)
  - src/m03/lift.py
  - src/m05/lift.py
  # Tool Owner: the fix is label-impact's, read here only (ruling 4)
  - pages/api/answers.json
  # Security: nothing of the door in a file (ruling 5)
  - pages/api/answers.json
  - pages/detail.html
  - pages/side-by-side.html
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr4.md
  - milestones/M06/README.md
  - milestones/M06/rulings/pr4.md
  - milestones/adoption/rulings/m05-relift.md
  - milestones/adoption/rulings/pages-style.md
  - src/m03/lift.py
  - src/m04/lift.py
  - src/m05/lift.py
  - https://github.com/andaro74/pharmadelta/actions/runs/43602104535
  - https://github.com/andaro74/pharmadelta/actions/runs/41250971500
  - https://github.com/andaro74/pharmadelta/actions/runs/42410336643
  - https://github.com/andaro74/pharmadelta/actions/runs/41222218526
  - https://github.com/andaro74/agentkeel/actions/runs/42967373936
  - https://github.com/agentkeel-studio/label-impact/pull/8
  - https://github.com/agentkeel-studio/label-impact/pull/9
  - https://github.com/agentkeel-studio/label-impact/blob/bd89989/manifest.yaml
pr: https://github.com/andaro74/pharmadelta/pull/39
---

# Ruling: M03 re-lift

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as #1, #13 to #18, #31,
#32, #37 and #38 were. It carries no claim of this repository, plants
nothing and measures nothing. M03 closed at 4 / 4 with row 4 GREEN,
tagged `m03` on `9932776`; the cell and the state are not touched and
this PR changes no verdict. It is the PR M06's Unsure 42 named: when
label-impact fixed its tool, `m03-lift.yml` re-run by hand, the pages
rebuilt from its artifact, the gates left to read. Three commits over
`cd2c462`: the code (`4e5d5ba`), the pages (`e35146a`) and this record.
M07 does not open here.

## What landed, and where

In `agentkeel-studio/label-impact`, never designed here: #8 (merged
2026-11-11, `d899d68`) made `find_label_row` read the section as text;
#9 (merged 2026-11-11, `main` at `bd89989`) changed the prompt.
agentkeel run 42967373936 (2026-11-11 05:41 UTC) signed and deployed
the agent at `bd89989`. Its `data/` equals this repository's at
`595dd68` by git blob hash. Read with `gh` on 2026-11-14.

## Rulings in this PR

1. **Product (the re-lift is served).** `pages/api/answers.json` and
   `pages/detail.html` are what `src.m03.lift write` writes from the
   artifact of CI run 43602104535 (`workflow_dispatch` on `m03-relift`
   at `4e5d5ba`, `ok` true, `written_by_ci` true, the sign-in 200 as
   `pharmadelta`, the call 200). `g-001` is served with the call's
   answer verbatim: `table_row` `lisinopril.8.1`, `clause_id`
   `201.57(c)(9)(i)`, `impacted` true, `owed` `follow-rld`, `escalate`
   false; its row and its clause copied from `data/` at `595dd68`;
   `scripted` false. The page shows the answer with its row and its
   clause (SPEC/00 §11). Row 4's cell is what was measured at `0b8d2ec`
   and does not move (ledger rule; M03 `rulings/pr4.md` 6, 22).
2. **Product (the side-by-side page).** `pages/side-by-side.html` is
   what `src.m04.lift write` writes from the artifact of run
   41250971500, the run `pages/api/baseline.json` already names. Its
   right column copies the new entry, as F4.1's last clause requires;
   its left column and `pages/api/baseline.json` are unchanged. Both
   columns now read the same on `g-001`, an `ordinary` golden; whether
   the page serves a second question is Unsure 35, not settled here.
3. **Engineering (the agent's commit).** `AGENT_COMMIT` in
   `src/m03/lift.py` moves from `956cd87` to `bd89989`. `src/m05/lift.py`
   writes `agent.commit` from the call record's `agent_commit`, as
   `src/m03/lift.py` has since `df5a56f`, so the constant's move does
   not change a rebuild of the break page: a rebuild from the artifact
   of run 42410336643 leaves both break files unchanged (construction,
   P4). No gate and no workflow changes.
4. **Tool Owner (the fix is label-impact's, read here only).** That the
   tool now accepts the section and the answer equals
   `goldens/g-001.yaml`'s `expected` is a reading made by hand on
   2026-11-14 from the artifact. No code here compares the answer with
   a golden; the gate compares the served answer with the door's on its
   own call (M03 `rulings/pr2.md`), which is the comparison this
   repository owns. One call does not show the answer is stable
   (Unsure 34).
5. **Security (nothing of the door in a file).** The artifact, the
   three served files, the commit messages and this file grepped for
   `execute-api`, `us-west-2_` and `amazonaws.com/`: no match.
   `call.door_host` is the SHA-256 the M03 lift recorded. The password
   was not typed in this session; the lift read it from the repository
   secret in CI.
6. **Product (the record).** `milestones/README.md`: every row cell
   unchanged; the note under the rows gains one paragraph.
   `milestones/M03/README.md`: the section "Re-lift (outside the cap,
   2026-11-14)" with Unsure 34 to 37. The evidence package and the
   sign-off are not touched; the package keeps the entry as at its
   build (Unsure 36, proposed: stay). The gates' readings go in
   comments on #39; no tag is placed.
7. **Product.** This PR is #39, the next number on this repository.

## What a reader can falsify

- `git diff cd2c462..<head> --stat` touches the eight files this ruling
  authorises and no other.
- Row 4 of `milestones/README.md` is byte-for-byte as at `cd2c462`.
- `gh run download 43602104535` and a `src.m03.lift write` from it,
  then `gh run download 41250971500` and a `src.m04.lift write` from
  it, leave `git status --short` empty on the head.
- `gh api repos/agentkeel-studio/label-impact/commits/main` reads
  `bd89989`.
- `git log -1 --format=%h -- pages/api/sign-off.json` reads `37352ef`.

## What this ruling does not settle

- Unsure 34: whether the door's answer to `g-001` is stable.
- Unsure 35: a second question on the side-by-side page. Product.
- Unsure 36: whether the evidence package is re-built and re-signed.
  Proposed stay.
- M07 (row 8), in its own session.
