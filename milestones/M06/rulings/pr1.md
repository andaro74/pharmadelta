---
ruling: m06-pr1
seat:
  - Product
  - Rule Owner
  - Data Owner
  - Tool Owner
  - Security
  - Threshold Owner
authorises:
  # Data Owner: the reviewer's seat and login as copied from label-impact's manifest; Rule Owner: the page answers nothing; Tool Owner: the served shape
  - pages/api/sign-off.json
  - pages/sign-off.html
  # Security: no credential, no door host, no token in either file; the function shown has a seat behind it
  - pages/sign-off.html
  # Product: the ledger row, the milestone's open detail, the carried rulings
  - milestones/README.md
  - milestones/M06/README.md
  - milestones/M06/rulings/pr1.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M03/rulings/pr4.md
  - milestones/M04/rulings/pr4.md
  - milestones/M05/README.md
  - milestones/M05/rulings/pr1.md
  - milestones/M05/rulings/pr4.md
  - milestones/adoption/rulings/m05-relift.md
  - milestones/adoption/rulings/m05-count.md
  - src/gate/score.py
  - src/m03/gate.py
  - src/m04/gate.py
  - src/m05/gate.py
  - .github/workflows/gate.yml
  - pages/api/answers.json
  - pages/api/break-it.json
  - https://github.com/agentkeel-studio/label-impact/blob/956cd87/manifest.yaml
  - https://api.github.com/repos/andaro74/pharmadelta/pages
  - https://api.github.com/repos/andaro74/pharmadelta/branches/main/protection
  - https://api.github.com/repos/andaro74/pharmadelta/commits/1065863
pr: https://github.com/andaro74/pharmadelta/pull/33
---

# Ruling: M06 PR 1 (plant)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR plants. Row 7 of the ledger is opened with its falsifier F6.1,
its seeded commit `6cfc1eb` and its expected gate output. The false
state is committed: `pages/api/sign-off.json` serves one sign-off as
signed, written by hand, with `signature` null and `package` null, and
`pages/sign-off.html` shows it so, labelled scripted, with nothing to
download. Nothing in this PR builds a package, hashes a file, reads a
commit from GitHub's API or reads the door: no code, no workflow, no
test.

## Rulings in this PR

1. **Product.** Row 7 opens with one falsifier, F6.1, and one seeded
   commit. The planted failure is one sign-off shown as signed that no
   seat holder signed, over a package that does not exist; both halves
   of the claim are false in one entry named in one list (P3). The gate
   is PR 2's. Which PR lifts the plant is decided after PR 2 goes RED.
2. **Data Owner.** The reviewer's seat `product` and login `andaro74`
   are copied from `agentkeel-studio/label-impact`'s `manifest.yaml` at
   `956cd87` (`seats.product`), read 2026-11-08 UTC, and the record
   names that commit. The function shown, Regulatory Affairs, is the one
   SPEC/00 §5 maps to `product`. No golden, row or clause is touched;
   the page cites no CFR paragraph (P7 has nothing to check).
3. **Rule Owner.** The page shows a reviewer, a statement, and "None"
   twice. It answers no question, shows no row and no clause, and names
   no rule of the agent's. No treatment answer appears anywhere (SPEC/00
   §2). The statement claims a reading, not a state, and carries none of
   SPEC/00 §11's six words (Unsure 9).
4. **Tool Owner.** The served shape of `pages/api/sign-off.json` is
   `id`, `reviewer` (`function`, `seat`, `login`, `seat_read_from`),
   `statement`, `signed`, `signature`, `package`, `scripted`: M03's
   shape with `reviewer`, `signature` and `package` where the agent's
   file has `agent`, `call` and `door`. The signature's and the
   package's fields are proposed in `milestones/M06/README.md` "Carried
   to PR 2" and are fixed at PR 2 or at the lift, not here (Unsure 5).
5. **Security.** Nothing in this PR holds or reads a credential or a
   token. Grep `M03_DOOR`, `InitiateAuth`, `Bearer`, `execute-api`,
   `us-west-2_` and `amazonaws.com/` under `pages/`: no match. The
   function shown signing has a seat behind it, the seat has a login,
   and the page says one person holds all seven seats (SPEC/00 §5;
   CLAUDE.md). Pharmacovigilance and Legal appear as holding no seat and
   not as a signature.
6. **Threshold Owner.** Not one line of `src/baseline/` changes in this
   milestone (P5); `git diff m00 --stat -- src/baseline/` is empty on
   this branch. No probe touched the control's working tree.
7. **Product, Security.** A signature is read at M06 as (a): the
   reviewer's own commit that changes the served file, read back from
   GitHub's API as the commit that last changed it, its `author.login`
   the seat's login (README, "What sign-off and downloadable mean at
   M06"). Stated as the assumption the plant and the expected gate
   output are built on; whether `verification.verified` must also be
   true is Unsure 1, Security's. Commits here are unsigned today.
8. **Product, Security (M05 Unsure 2, M04's and M03's 2, ruled).**
   GitHub Pages is not enabled (404 on 2026-11-08 UTC; `has_pages`
   false). Ruled: "downloadable" at M06 means a file in this public
   repository that a reader fetches by its GitHub URL, raw or through the
   file view, named on the page with its SHA-256; "public" means readable
   in the repository, as since M03. The milestone does not depend on
   Pages. Enabling it, from which branch and directory, is the owner's
   setting outside every milestone; it is carried to no further milestone
   by name and stays in the owner's settings. M07 is built in
   agentkeel-studio and has no page here.
9. **Security, Product (M05 Unsure 3, M04's 16, M03's 16, M02's 16,
   ruled).** `M00 gate` is the one required check on `main`, `strict`
   true, no rulesets (read 2026-11-08 UTC). Ruled: no Measured cell
   depends on a required check, since each cites a run on `main` after
   the merge (M01 Unsure 23), so the M02 to M05 gates stay as they are
   and the ledger loses nothing. Whether `M06 gate` joins the list is
   recorded at PR 4 for the record only. The setting is the owner's,
   outside every milestone, and is carried to no further milestone by
   name.
10. **Product (M05 Unsure 12, ruled).** The evidence package carries
    the M00 gate's `result.json` of the run row 0's Measured cell cites
    (38058191295, artifact `m00-gate-47788c0…`), with its link, and that
    file's per-golden scores say `g-005` and `g-006` were answered, not
    blocked: the baseline's report on scenarios 5 and 6 that SPEC/00 §7
    asks for. It is a file in the package, not a number on the page; if
    a page ever shows it, from the package with the run's link. The
    rest of the package's contents are proposed in the README and fixed
    at PR 2 or at the lift (Unsure 6).
11. **Product.** The M05 call count (`milestones/M05/README.md` "The
    re-lift call" and Unsure 47, low by four at #31) is corrected in
    #32, its own PR outside any cap, opened before this one
    (`milestones/adoption/rulings/m05-count.md`). It is not folded into
    this PR, which touches nothing under `milestones/M05/`; the two
    share no file and merge in either order.
12. **Product, Engineering.** The M03, M04 and M05 gates read their own
    files by path and none globs `pages/` or reads the new files. Their
    readings on this PR are readings after their measurements (M03
    `rulings/pr4.md` 6, 22; M04 `rulings/pr4.md` 22; M05 `rulings/pr4.md`
    3) and are recorded in the PR body or a comment, not in the ledger.
    No gate, workflow or module is edited.
13. **Product.** The reads of `main`, the tags, the `main` runs on
    `020bfac`, `pages/`, the three gates, the M00 scorer, label-impact's
    manifest, the commit verification, the repository's visibility, the
    Pages setting and the required checks made on 2026-11-08 UTC are
    recorded in the README as construction. They are reads while
    opening the row, not this repository's measurement (P4); PR 2's CI
    run is.
14. **Product, M01 Unsure 23.** A Measured cell cites the run on `main`
    after PR 2 merges, with the PR run named beside it when it was the
    one read at the time. Row 7's expected gate output says so.
15. **Product.** This PR is #33, the next number after #32 (Unsure 12).

## What a reader can falsify

Listed in `milestones/M06/README.md`, "What a reader can falsify".

## What this ruling does not settle

The items under Unsure in `milestones/M06/README.md`, each with its
seat. None blocks the plant. What matters most for the close: what a
signature is and whether GitHub's verification is required (1), which
seat reviews (4), the names fixed at PR 2 (5), the package's form and
contents (6), what the gate reads when an artifact has expired (7), and
whether a hand-run writer may produce the page in the signing commit
(15).
