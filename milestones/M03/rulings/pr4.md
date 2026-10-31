---
ruling: m03-pr4
seat:
  - Security
  - Engineering
  - Product
  - Tool Owner
  - Data Owner
  - Threshold Owner
authorises:
  # Security: door_host as a hash (Unsure 12); the lift workflow reads the same four names as the gate and writes none; contents: read on every workflow
  - .github/workflows/m03-lift.yml
  - src/m03/lift.py
  # Engineering: the lift path (Unsure 28): the CI call, the artifact, the deterministic rebuild of the pages
  - .github/workflows/m03-lift.yml
  - src/m03/lift.py
  # Product, Data Owner, Tool Owner: the lift, the two pages rebuilt from the CI record (Unsure 26)
  - pages/api/answers.json
  - pages/detail.html
  # Product: the Measured cell, the row's state, 4 / 4, the close detail, the Unsure rulings and this file
  - milestones/README.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr4.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M00/fields.md
  - milestones/M03/README.md
  - milestones/M03/rulings/pr1.md
  - milestones/M03/rulings/pr2.md
  - milestones/M03/rulings/pr3.md
  - milestones/M02/rulings/pr3.md
  - milestones/M01/rulings/pr4.md
  - https://github.com/andaro74/pharmadelta/actions/runs/41171470951
  - https://github.com/andaro74/pharmadelta/actions/runs/41126878288
  - https://github.com/andaro74/pharmadelta/actions/runs/41221327681
  - https://github.com/agentkeel-studio/label-impact/blob/8cf0563/manifest.yaml
pr: https://github.com/andaro74/pharmadelta/pull/22
---

# Ruling: M03 PR 4 (close)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR closes M03 at the cap, 4 / 4. It carries the lift, fills the
"Measured" cell from a CI-written result and writes the row's state,
rules or carries by name every open Unsure item of PR 1, PR 2 and PR 3,
and is followed by the tag `m03` on its merge commit after its run on
`main` is read. It decides nothing about the measurement: the `main` run
after #20 merged, 41171470951, is the measurement, read again at this PR
with `gh run download` before the cell was written.

## Rulings in this PR

1. **Security (Unsure 12, Unsure 27).** `door_host` in the call record
   is the SHA-256 of the door URL's host, lower-cased, written as
   `sha256:<64 hex>`, never the host. The gate as it stands names an
   answer uncalled when `door_host` is missing or empty (`rulings/pr2.md`
   7), so a hash fits it and "not written" would need a gate change the
   repair slot did not make (Unsure 27). What the hash gives: a reader
   who holds the variable `M03_DOOR_URL` confirms the record names the
   same host; a reader who does not learns nothing of the host from the
   page. What it does not give: the host is a short API Gateway id under
   a known suffix, so a brute-force search of the hash is possible for
   anyone who wants the id enough; the door still admits only a token of
   an admitted caller (agentkeel SPEC/10), so the host is not a credential
   and the hash is a courtesy, not a control. The gate is not changed.
2. **Engineering, Security (Unsure 28, the lift path).** Of the two
   candidates (`milestones/M03/README.md`, "Close (PR 4)", "The lift
   path"), the one built is the artifact path: `.github/workflows/m03-lift.yml`
   runs `src/m03/lift.py call` in CI, which signs in and asks the door
   each served question with the gate's own `sign_in` and `ask_door` and
   writes `call.json` (the call record, the door's reading, the answer
   verbatim) as the artifact `m03-lift-<sha>`; `lift.py write` rebuilds
   `pages/api/answers.json` and `pages/detail.html` from that artifact,
   by hand, deterministically, and the pull request commits them naming
   the run. Chosen over a workflow that commits to the branch with
   `GITHUB_TOKEN` because it leaves `permissions: contents: read` on
   every workflow of this repository and adds no token that can write a
   branch; the cost is one hand step, which a reader checks by running
   `write` on the downloaded artifact and comparing. The call is CI's as
   `pharmadelta`; `write` refuses a `call.json` whose `written_by_ci` is
   false (P4). The workflow reads the same secret and three variables
   as the gate, from one step's `env`, and writes none of them. It runs
   by hand and once on a push that adds or edits its own file on a
   branch other than `main`, because a `workflow_dispatch` needs the
   file on the default branch and the lift's call is made before this PR
   merges. `m03.yml`, `gate.yml`, `m01.yml`, `m02.yml`, `pyproject.toml`
   and `uv.lock` are unchanged.
3. **Product, Tool Owner, Data Owner (Unsure 26, Unsure 6).** The lift
   serves what its call returned, verbatim: `answer` is `table_row`,
   `clause_id` and the three answer fields of the door's `parsed`, or
   null when nothing parsed. `row` and `clause` are copied from `data/`
   only when the table holds the answer's `table_row` and the clauses
   hold its `clause_id`; else they are null and the page shows "no row
   found" with the question, the call record, the `parsed` object and
   the agent's text, verbatim and labelled as the agent's, and shows no
   answer: an answer is shown only with its row and its clause (SPEC/00
   §11). Row 4 closes on the call, as Unsure 6 asked; what the agent
   gave is on the page and in the cell's own words. The cause is
   label-impact's (Unsure 23) and nothing here changes there.
4. **Product (Measured and state).** Row 4's "Measured" cell cites the
   `main` run after #20 merged, 41171470951 on `0b8d2ec`, artifact
   `m03-gate-0b8d2ec7598b61c30f861a3f2114c2a13e89ad71`: RED,
   `answers_uncalled` `["g-001"]`, `answers_disagreed` `[]`,
   `answers_differing` `[]`, `unreadable` `[]`, `written_by_ci` true.
   The PR run on #20 at merge ref `f97f292`, 41126878288, is named
   beside it as the run read at the time; it read the same on every
   field the row names (M01 Unsure 23). Both were downloaded again in
   this session before the cell was written. The cell equals the
   expected gate output written at open, so row 4 is GREEN and "PRs used
   / cap" is 4 / 4. The lift's runs are recorded in the README and not
   in the cell.
5. **Product (the lift, as ruled).** `rulings/pr2.md` 10 and
   `rulings/pr3.md` 5 carried the lift to PR 4. This PR carries it:
   `pages/api/answers.json` and `pages/detail.html` at `8aae03d`, the
   one change "The false state" named, written by `lift.py write` from
   the artifact of CI run 41222218526. `git diff c7edf8f -- pages/` is
   the whole of both files, because the hand-written answer and the row
   and clause copied for it are gone with it; nothing else changes.
6. **Product, on reading runs 41222318273 and 41222395263.** The gate
   on this PR read GREEN twice: every served answer carries a call
   record as `pharmadelta`, the page's answer equals the API's, and the
   served null equals a `parsed` null of the run's own call. The first
   GREEN of this gate. It is a reading after the measurement: it says
   the agent gave no answer on those calls, as on the lift's; it does
   not say the agent answers the question, and it does not touch the
   cell. A later run that parses an object reads RED on
   `answers_differing` and is recorded as what the agent said that day
   (ruling 3); the milestone is not reopened by it.
7. **Product, Security (PR 1's Unsure 1 and 2).** At M03 "a public API"
   is the read API: a public JSON file of answers, each produced by a CI
   call as `pharmadelta` with its record, served beside the page. That
   is the claim row 4 measured. A live path that forwards a visitor's
   question is a later row's or a platform item, and is not designed
   here. GitHub Pages is not enabled on this repository (404 again on
   2026-10-31), so "public" at M03 means readable in the repository.
   Enabling Pages, from which branch and directory, is carried by name
   to M04, the first milestone that serves a page to a visitor.
8. **Product (PR 1's Unsure 7).** SPEC/00 §11's "a number on a page
   comes from a CI-written result and links to it" reaches measured
   numbers. A row's and a clause's data (strengths, dates, application
   numbers, a citation) are the data's own, each with its source in
   `data/`, and are not measured results. The call record's `called_at`
   and `request_id` are the CI run's and the page links the run. The
   page says so in its footer.
9. **Threshold Owner, Product (Unsure 11).** As built: the gate asks the
   door every served answer's question, called or not, one call per
   served answer per run. On the plant it gave the readings Unsure 26
   records and cost the agent one call per run.
10. **Product (Unsure 14).** Confirmed: an API that serves no answer
    reads UNSCORABLE, never GREEN.
11. **Engineering, Tool Owner (Unsure 15).** Confirmed: "byte for byte"
    is equality of the parsed JSON values in canonical form. The lift's
    page embeds the same value the API serves, pretty-printed; the gate
    read them equal.
12. **Security, Product (Unsure 16).** `M03 gate` is not made a required
    check in this PR, as `M02 gate` was not. It is a repository setting,
    the owner's, outside any milestone; carried by name with M02's
    Unsure 16. `M00 gate` stays the one required check.
13. **Product (Unsure 17, 29, 30).** PR 2 was #20, PR 3 was #21, this PR
    is #22.
14. **Security (Unsure 18).** Allowed as built: the result records
    `token_use` and `username` from the token's payload, unverified,
    and the pool id's region prefix. They identify the caller and the
    region and nothing of the token's signature; the token is never
    written. The lift's `call.json` records the same and nothing more.
15. **Security, Product (Unsure 19).** The wanted reading: a pull request
    from a fork gets no secret, cannot call the agent, and its gate
    reads UNSCORABLE unless an answer is uncalled or disagreed; never
    GREEN. The job fails either way.
16. **Security (Unsure 20).** The one construction call with no token
    stands as recorded; it was made to read the door's headers and left
    a refused record with no identity in the security account's log,
    named to agentkeel under PR 1's carried items. No construction run
    touches the door from here on: every call since is CI's as
    `pharmadelta`, including the lift's.
17. **Engineering (Unsure 21).** As built: the door call's timeout is 90
    seconds, the proxy's 28; a call that outlives the proxy reads as the
    door's status, never as a client timeout. Seven CI calls answered in
    7 to 11 seconds wall.
18. **Tool Owner, Engineering (Unsure 22).** Confirmed: a 200 with
    `error` or a 403 with `refused` is recorded and not compared, and a
    called answer whose call failed that way reads UNSCORABLE, not
    differing. The lift's `call` exits 2 on either and `write` refuses
    the record.
19. **Tool Owner, Engineering (label-impact); Product (Unsure 23, 6).**
    Carried by name to label-impact: `find_label_row` refuses `section`
    sent as the number `8.1` on every call read from here, seven in CI,
    and the agent's answer to g-001 takes four shapes (`milestones/M03/README.md`,
    "Observed (CI runs, 2026-10-31)"). The agent's goldens are its own
    tests (SPEC/00 §3); nothing here changes there. For row 4: the cell
    closes on the call, the page says the agent gave no row, and that is
    what this milestone measured.
20. **Product, Engineering (Unsure 24).** Confirmed as built at PR 3: a
    served answer that is neither null nor an object is unreadable at
    the entry, never RED by itself.
21. **Product (Unsure 25).** The row's "is shown as served" means the
    gate's reading: a page answer the API does not serve, or that
    differs from the API's entry, is named; a served answer the page does
    not show is not. The gate is not changed. With one served answer,
    shown, the two readings agree.
22. **Product (Unsure 31).** After this PR merges, its run on `main` is
    read with `gh run download` before the tag is placed. Its verdict is
    written in the tag `m03`'s message and in a comment on #22, not in
    the README: a commit after the merge would be a fifth PR, and a push
    to `main` is not the PR shape. The cell stands whatever it reads.
23. **Engineering, Security, Threshold Owner (Unsure 32).** As built:
    `m03-lift.yml` runs by hand and once on a push that adds or edits its
    own file on a branch other than `main`. One call as `pharmadelta`
    per such push, under the agent's ceilings. The artifact is kept 90
    days, as the gates' are; the record is the page's copy, the run's
    log and its summary after that.
24. **Engineering (Unsure 33).** `8aae03d`'s message claims an LF pin
    its diff does not hold; `6dd2fc2` holds the pin and says so. The
    committed pages are LF and equal a rebuild from the artifact with the
    pinned writer, byte for byte. The message is not rewritten.

## What a reader can falsify

Listed in `milestones/M03/README.md`, "Close (PR 4)", "What a reader
can falsify": rebuild the pages from the artifact of run 41222218526
and compare; open the `main` run's artifact and read the cell from it;
grep the pages and the workflows for a host, a pool id, a client id, a
`PLANT` key, a scripted banner or a banned word; `git diff main --stat`
on this PR touches seven files.

## What this ruling does not settle

Nothing of M03 is left open: every Unsure item of PR 1 to PR 4 is ruled
above or carried by name (Unsure 2 to M04; 6 and 23 to label-impact; 16
to the owner's settings with M02's 16; the deadlock finding and Unsure
20's refused record to agentkeel). The tag `m03` is placed after this
PR's run on `main` is read (ruling 22). Nothing in M04 or later.
