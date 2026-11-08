---
ruling: m06-pr2
seat:
  - Engineering
  - Security
  - Product
  - Tool Owner
  - Data Owner
  - Rule Owner
authorises:
  # Engineering: the gate and the workflow that runs it
  - src/m06/**
  - .github/workflows/m06.yml
  # Security: what the workflow reads and with what token, what it never writes, and the grep before upload
  - .github/workflows/m06.yml
  - src/m06/gate.py
  # Tool Owner: the records' fields and the package's form, fixed here
  - src/m06/gate.py
  # Product: the ledger's PR count and the milestone's PR 2 detail
  - milestones/README.md
  - milestones/M06/README.md
  - milestones/M06/rulings/pr2.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M03/rulings/pr2.md
  - milestones/M03/rulings/pr4.md
  - milestones/M05/README.md
  - milestones/M05/rulings/pr2.md
  - milestones/M05/rulings/pr3.md
  - milestones/M06/README.md
  - milestones/M06/rulings/pr1.md
  - src/m03/gate.py
  - src/m05/gate.py
  - .github/workflows/m05.yml
  - pages/api/sign-off.json
  - pages/sign-off.html
  - https://github.com/agentkeel-studio/label-impact/blob/956cd87/manifest.yaml
  - https://api.github.com/repos/andaro74/pharmadelta/commits/6cfc1eb14794217d87bff852e00b50589fc634d4
  - https://api.github.com/repos/andaro74/pharmadelta/actions/runs/41266122812/artifacts
pr: https://github.com/andaro74/pharmadelta/pull/34
---

# Ruling: M06 PR 2 (measure)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR measures. It adds the gate that reads the plant `6cfc1eb` and
judges it: `src/m06/gate.py` reads the sign-offs `pages/api/sign-off.json`
serves and the sign-offs `pages/sign-off.html` shows, names each shown as
signed that carries no signing record or no package record naming a file
in the repository, and each page sign-off the file does not serve; then,
for each sign-off that carries both records, reads back from GitHub's API
the commit that last changed the served file, label-impact's manifest at
the commit the reviewer record names, and the package's hash, zip and
entries against their sources, and writes `result.json` with one verdict;
`.github/workflows/m06.yml` runs it in CI with the workflow's own token
on a full-depth checkout, greps the result for a token's prefix, and
writes the result as the artifact `m06-gate-<sha>`. On `6cfc1eb`'s pages
the gate names `s-001`: `signature` is null and `package` is null, and
nothing is read from the network. The CI run on this PR is the
measurement (P4); the ledger's "Measured" cell is filled at close from
the `main` run after this PR merges (M01 Unsure 23, ruled at M02 PR 1).
Nothing in this PR lifts the plant, and nothing under `pages/` changes.

## Rulings in this PR

1. **Engineering.** The gate is the standard library and `pyyaml`, which
   `pyproject.toml` already lists; `pyproject.toml` and `uv.lock` are
   unchanged. Nothing is imported from `src/m03/`, `src/m04/` or
   `src/m05/`: no sign-in, no door call, no door URL check. The checkout
   is full depth because the gate asks git which commit last changed the
   served file; a shallow checkout reads `unreadable`, never a wrong
   commit (Unsure 22).
2. **Security; Unsure 8 as ruled.** The workflow reads GitHub's API with
   `GITHUB_TOKEN` in the gate step's `env` and nothing else:
   `permissions` is `contents: read` and `actions: read`, the second for
   this repository's artifacts. No secret and no variable of M03's is
   read; grep `secrets.` in the workflow: one match, `GITHUB_TOKEN`; grep
   `vars.`: none. The gate sends the token as a bearer to the API host
   only; the archive's 302 to the blob store is fetched by the gate
   itself without the token, and the redirect's URL is written nowhere.
   `result.json` holds one boolean for the token's presence. Before
   upload a step greps the result directory for `ghs_`, `ghp_` and
   `github_pat_` and fails the job on a match; the upload runs only when
   that step passed (Unsure 21). This repository takes no fork PRs, and a
   fork's token is read-only in any case.
3. **Security, Product; Unsure 1 as ruled.** A signature at M06 is (a):
   the reviewer's own commit that changes `pages/api/sign-off.json`, read
   back from GitHub's API as the commit that last changed the file. The
   gate requires its `author.login` to equal the login `label-impact`'s
   `manifest.yaml` holds for the seat at the commit the reviewer record
   names, `reviewer.login` and `signature.by`, and the function shown to
   be the seat's (SPEC/00 §5). `commit.verification.verified` is recorded
   as read and not required: commits on this repository are unsigned
   (`6cfc1eb`: `verified` false, reason `unsigned`), and requiring it
   would make every sign-off unreadable until the owner signs commits.
   `author.login` is GitHub's match of the commit's email to an account,
   and `committer.login` is recorded beside it; the limit is recorded
   under Unsure 19, not closed here. If Security later requires
   `verified`, the owner signs commits first and the gate changes
   outside this cap. The plant is unsigned under every reading.
4. **Tool Owner, Engineering; Unsure 5 as ruled.** The names are fixed:
   the files `pages/sign-off.html` and `pages/api/sign-off.json`, the
   served key `signoffs`, the entry fields `reviewer`, `statement`,
   `signed`, `signature`, `package`, the lists `signoffs_unsigned`,
   `signoffs_disagreed` and `signoffs_differing` with `unreadable` and
   `written_by_ci` beside them. The signature record is `over`, `by`,
   `method`, `read_from`. PR 1's proposed `read_back` is not in it: the
   signing commit is the commit that changes the file, so its own sha,
   login and time cannot be written into it; the read-back is the gate's,
   in `result.json`, and a page that shows it links the run (Unsure 18).
   The package record is `file`, `sha256`, `built_by` (`run_url`,
   `artifact`), `commit`, `entries`, `written_by_ci`; each entry is
   `path`, `sha256`, `source`, `run_url`, `artifact`, `name`, `commit`,
   `ledger_row`. The gate names a sign-off unsigned when any is missing
   or empty, a hash is not 64 hex digits, `written_by_ci` is not true, a
   run URL is not on github.com, or the file is not under `pages/` in
   the checkout. The lift writes them.
5. **Tool Owner, Product, Data Owner; Unsure 6 as ruled.** The package
   is one zip under `pages/evidence/`, named in `package.file`, fetched
   by its GitHub URL (PR 1 ruling 8), holding `manifest.json` equal to
   `package.entries` and each entry at its `path`. Entries come from
   three sources: this repository's CI artifacts, this repository at
   `package.commit`, and `label-impact`'s repository at the agent commit
   the served files name. The third source was not in PR 1's proposal
   and is read through the contents API, because label-impact is not in
   the checkout (Unsure 23). A zip in git is accepted: one file, one
   URL, one hash signed. Which files go in is fixed at the lift (Unsure
   16 carried); the gate accepts any entries whose sources it can read.
6. **Engineering, Product; Unsure 7 as ruled.** An artifact that has
   expired, or an archive or API that does not answer, is `unreadable`:
   named in the result, UNSCORABLE only when nothing is RED, and never a
   RED on its own. The expiry is recorded in the result as the listing
   gives it (`artifacts_read[].expires_at`), not in the record. The
   build artifact expires on the same terms (Unsure 20). After the
   expiries the committed zip and its hash in the signing commit are the
   only record; the gate then reads what it can and names the rest.
7. **Product; Unsure 4 as ruled.** The reviewer is the holder of
   `product`, shown as Regulatory Affairs. Any of the seven seats may add
   its own sign-off with its seat and login; the gate reads each against
   SPEC/00 §5's table (`SEAT_FUNCTION`) and the manifest. A seat not
   among the seven reads differing, so Pharmacovigilance and Legal
   cannot appear as a signature (SPEC/00 §5; CLAUDE.md; Unsure 25). One
   file holds every sign-off and is read against one last commit; with
   one person holding all seats the logins coincide (Unsure 27).
8. **Product, Engineering; Unsure 11 as ruled.** The M03, M04 and M05
   gates run on this PR, read their own pages by path and do not read
   the new files. Their readings are after their measurements (M03
   `rulings/pr4.md` 6, 22; M04 `rulings/pr4.md` 22; M05 `rulings/pr4.md`
   3) and are recorded in a PR comment and under "Observed", not in a
   ledger cell.
9. **Product; Unsure 12 as ruled.** #32 was the M05 count PR and #33
   this milestone's PR 1, as `milestones/adoption/rulings/m05-count.md`
   and `rulings/pr1.md` wrote. Neither `pr:` line changes.
10. **Product; Unsure 13 as ruled.** No page changes in this PR; the
    plant page's numbers stand as PR 1 read them (M03's 7).
11. **Product, Data Owner; Unsure 14 as ruled.** As built: the gate reads
    the manifest at the commit the reviewer record names and compares
    that login with `reviewer.login` and the commit's author. It does
    not read `main`'s manifest. A later change of the seat's login is
    read at the lift, when the record is written and the commit named.
12. **Product.** The construction run of 2026-11-08 UTC is recorded in
    the README as construction: the gate on the real pages with no
    token; fifty-two made-up pairs of files with every git and API read
    stubbed, exercising every arm; and the gate's own transport on real
    records with the owner's token in one process's environment, typed
    and printed nowhere. No defect was found. It decides nothing (P4).
13. **Product.** "PRs used / cap" is 2 / 4. Which PR carries the lift is
    ruled on reading this PR's CI run, as M03's, M04's and M05's were.
14. **Product; carried by name, not ruled.** Unsure 9 (the statement's
    wording; no page changes here; fixed before the signing commit), 10
    (one person reviews their own work; the sentence on the page is
    unchanged), 15 (a hand-run writer for the page in the signing commit;
    the gate reads page and file equal as parsed JSON whichever writer
    produced the page; the lift PR's) and 16 (the package's contents,
    the ordinary assistant's results among them; the lift PR's).
15. **Product.** This PR is #34, the next number on this repository
    after #33 (Unsure 17).
16. **Engineering, Product.** The verdict's shape is as PR 1's "Carried
    to PR 2" proposed: RED on any unsigned, disagreed or differing
    sign-off, the first two read from the served files before any
    network; GREEN only when every sign-off shown as signed carries both
    records, is read back as the seat holder's own commit over the
    package it signed with every entry equal to its source, and is shown
    as served, with nothing unread; UNSCORABLE when nothing is RED and a
    served file or a read-back could not be read. Exit 0, 1, 2. A file
    that serves no sign-off is UNSCORABLE (M03 Unsure 14's reading). A
    read-back that fails beside a RED leaves the RED standing (M05 PR 3's
    rule, built in from the start). A sign-off shown as not signed is
    named by no list (Unsure 24).

17. **Product, on reading run 42491031888.** The run wrote RED,
    `signoffs_unsigned` `["s-001"]`, `signoffs_disagreed` `[]`,
    `signoffs_differing` `[]`, `unreadable` `[]`, `written_by_ci` true,
    on the merge ref `8431885`; the plant is named as the row expects.
    `artifacts_read` is `[]` and `read_back` is null: the gate asked
    GitHub's API nothing for the plant, as M03 Unsure 4's rule asks. The
    grep step passed and the artifact was written; the downloaded result
    holds no token prefix and no door string. The lift is carried by PR
    4 by M03's path (b), the package built by a CI run and committed by
    hand, the signing commit the reviewer's own by hand (README, "After
    this PR goes RED"). PR 3, if the cold review of #34 finds anything,
    repairs and does not lift; if it finds nothing, PR 3 is skipped. The
    Measured cell takes the `main` run after #34 merges. Which files the
    package carries (Unsure 16) is fixed in the lift PR's first commit,
    before any page is written. The `M03 gate`, `M04 gate` and `M05 gate`
    on the same head read GREEN, readings after their measurements,
    recorded in the README and in a comment on #34.

## What a reader can falsify

Listed in `milestones/M06/README.md`, "What a reader can falsify" under
PR 2.

## What this ruling does not settle

The items under Unsure (PR 2) in `milestones/M06/README.md`, 17 to 27,
each with its seat (17 ruled above), and PR 1's 9, 10, 15 and 16, carried. What matters
most for the close: whether `committer.login` or `verified` should be
required (19), the one-file-one-commit limit when a second seat signs
(27), what the lift's CI run names its zip (26), and which files the
package carries (16).
