---
ruling: m05-pr3
seat:
  - Engineering
  - Security
  - Product
authorises:
  # Engineering: the repair of the gate's verdict path (Defect 1) and the two labels
  - src/m05/gate.py
  # Security: the repair reads nothing new from the environment and writes nothing new of it; the door URL's parse failure is written by type alone; m05.yml is unchanged
  - src/m05/gate.py
  # Product: the ledger's PR count, the milestone's PR 3 detail and this file
  - milestones/README.md
  - milestones/M05/README.md
  - milestones/M05/rulings/pr3.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M05/README.md
  - milestones/M05/rulings/pr1.md
  - milestones/M05/rulings/pr2.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr3.md
  - milestones/M04/README.md
  - milestones/M04/rulings/pr3.md
  - src/m03/gate.py
  - .github/workflows/m05.yml
  - https://github.com/andaro74/pharmadelta/actions/runs/41264751470
  - https://github.com/andaro74/pharmadelta/actions/runs/41265001644
  - https://github.com/andaro74/pharmadelta/actions/runs/41266122812
pr: https://github.com/andaro74/pharmadelta/pull/29
---

# Ruling: M05 PR 3 (repair)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR repairs. The cold review of #28 (`milestones/M05/README.md`,
"Cold review of #28") found one defect in the gate's verdict path: a
failure of the sign-in or of a door call that M03's `sign_in` and
`ask_door` do not catch themselves (`http.client`'s exceptions, which are
not `OSError`; a Cognito body that is not an object), or a door URL
`urlsplit` cannot parse, raised out of `run()` after the served files
were read, and `main`'s handler wrote the run UNSCORABLE with no
`scenarios_untraced` list, where `rulings/pr2.md` 7 says RED comes
first; on the URL path the handler also wrote a fragment of the URL
variable into `result.json`. It found two wrong labels. `src/m05/gate.py`
now makes the sign-in and each door call inside a guard that records a
failure the helper did not catch as a reading not made, records a URL
that cannot be parsed by the exception's type alone, and the labels say
what happened. Nothing under `pages/` changes; the plant stands and
nothing here lifts it. Nothing here decides the row: the `main` run
after #28 merged, 41266122812, is the measurement, read first in this
session, and PR 4 fills the "Measured" cell from it.

## Rulings in this PR

1. **Engineering (Defect 1, the labels).** The repair is as the README's
   "The repair" states: `sign_in_guarded` and `ask_door_guarded` wrap
   M03's functions and return the helper's own failure shape on any
   exception it did not catch; `run` catches any exception other than
   `Unscorable` from `check_url`; "page not read", "the door did not
   answer (...)" and "no answer" in the stop reading and the summary.
   The verdict on every input PR 2's construction run exercised is
   unchanged; the four stubbed pairs on the plant that read UNSCORABLE
   before read RED naming the plant after, and the two lifted pairs that
   read UNSCORABLE by an exception before read UNSCORABLE with the lists
   and the reading recorded after. The fields compared, the trace
   record's fields and `m05.yml` are unchanged. `src/m03/` is not
   edited. No new dependency; `pyproject.toml` and `uv.lock` are
   unchanged.
2. **Security.** The repair reads nothing new from the environment and
   writes nothing new of it. A caught failure is recorded as the
   exception's type and its text cut at 200 or 300 characters, the shape
   M03's own `except` clauses record for `URLError`; the classes seen
   carry the server's status line, byte counts or a type name, never
   the password, the token, the pool id or the client id (Unsure 27). A
   door URL that cannot be parsed is written by the exception's type
   alone, because `urlsplit`'s message quotes the host it refused: the
   one path that wrote a fragment of the URL variable before this PR
   (case D) writes none after. The grep step and the upload condition
   of `.github/workflows/m05.yml` are unchanged and ran as designed on
   all three RED runs.
3. **Product.** The `main` run after #28 merged, 41266122812 on
   `8734adb`, read RED, `scenarios_untraced` `["g-005", "g-006"]`,
   `scenarios_disagreed` `[]`, `scenarios_differing` `[]`, `unreadable`
   `[]`, `written_by_ci` true, event push on `refs/heads/main`, the same
   as the PR runs 41264751470 and 41265001644 on every field the row
   names. It is the run the Measured cell cites at PR 4, with the PR run
   41264751470 named beside it (M01 Unsure 23). The door's readings on
   it are as on #28: `end_turn`, `guardrail_topics` `[]`, g-005 parsed
   no row, g-006 parsed `metformin.bw` and `314.150(b)(10)`; the
   platform's guardrail stopped neither question. They decide nothing on
   the plant (Unsure 16, 18).
4. **Product, Engineering (Unsure 26, proposed, not ruled).** A lone
   surrogate in the door's body would make the result's write raise
   after the lists were computed. Not reachable from the door as built;
   recorded, not repaired. The seats confirm at PR 4 or rule it a
   repair.
5. **Engineering (PR 2 Unsure 20, ruled).** The trace's `request_id`
   must equal the call's; a mismatch reads untraced. As built, read at
   PR 2's construction, unchanged here.
6. **Security (PR 2 Unsure 21, read).** The grep step ran and passed
   with the gate step failed on all three RED runs (41264751470,
   41265001644, 41266122812) and the upload ran after it each time; a
   match would fail the job before the upload. Whether the same step is
   owed to `m03.yml` and `m04.yml` is outside this cap, carried.
7. **Product, Rule Owner (PR 2 Unsure 17, 19, 22 and PR 1's 1, 2, 3, 5,
   7, 8, 9, 12, 13, carried by name, not ruled).** Not changed here. 17
   (a scenario shown as not blocked is named by no list) and 1 ("wired")
   are Product's at PR 4; 19 (membership, not "only") is Rule Owner's at
   PR 4 with the lift, read at construction (case N); 22 (the door's
   text recorded whole) is carried with the main run's text read and
   copied nowhere; 2 (GitHub Pages), 3 (required checks), 5, 7, 8, 9, 12
   and 13 as PR 2 carried them. Unsure 16 and 18 stay read, not ruled:
   no trace is designed here and what the lift serves is Product's at
   PR 4.
8. **Product.** "PRs used / cap" is 3 / 4 in the ledger and the
   milestone README. PR 4 is the close: the lift by M03's path (b), the
   Measured cell from run 41266122812, the row's state, the rulings on
   the open Unsure items, the tag `m05` after its run on `main` is
   read. A fifth PR is a RED close.
9. **Product (Unsure 29).** This PR is #29.

## What this ruling does not settle

Unsure 23 to 28 (`milestones/M05/README.md`, "Unsure (PR 3)"), each
with its seat; PR 2's 16, 17, 18, 19 and 22; PR 1's 1, 2, 3, 5, 7, 8, 9,
12 and 13, carried. What matters most for the close: what the lift
serves when the door stopped neither question (18: the two calls as not
blocked, a RED close with the finding, or a wait on per-agent rules for
label-impact), which is Product's to decide before PR 4 opens; what
"wired" means (1); and whether a denied topic's name is "the rule that
fired" (16), a platform item.
