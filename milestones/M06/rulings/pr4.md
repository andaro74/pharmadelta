---
ruling: m06-pr4
seat:
  - Product
  - Rule Owner
  - Security
  - Engineering
  - Tool Owner
  - Data Owner
  - Threshold Owner
authorises:
  # Security: the lift workflow holds GITHUB_TOKEN in one step's env and nothing else, contents: read and actions: read, the grep before the upload; the build fetches each redirect without the token and writes no URL
  - .github/workflows/m06-lift.yml
  - src/m06/build.py
  # Engineering: the lift path (rulings/pr2.md 17): the CI build, the artifact, the deterministic zip, the writer that rebuilds the page from the served file
  - .github/workflows/m06-lift.yml
  - src/m06/build.py
  - src/m06/page.py
  # Product, Threshold Owner, Data Owner: which files the package carries (Unsure 16), the zip committed byte for byte from the CI artifact
  - pages/evidence/m06-evidence.zip
  # Product, Rule Owner: the statement (Unsure 9); the signature is the seat holder's own commit 37352ef, which this file records and does not authorise: a ruling cannot sign
  - pages/api/sign-off.json
  - pages/sign-off.html
  # Product: the Measured cell, the row's state, 4 / 4, the close detail, the Unsure rulings and this file
  - milestones/README.md
  - milestones/M06/README.md
  - milestones/M06/rulings/pr4.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/M06/README.md
  - milestones/M06/rulings/pr1.md
  - milestones/M06/rulings/pr2.md
  - milestones/M06/rulings/pr3.md
  - milestones/M03/rulings/pr4.md
  - milestones/M05/rulings/pr4.md
  - src/m06/gate.py
  - .github/workflows/m06.yml
  - https://github.com/andaro74/pharmadelta/actions/runs/42495856254
  - https://github.com/andaro74/pharmadelta/actions/runs/42491031888
  - https://github.com/andaro74/pharmadelta/actions/runs/42502413422
  - https://github.com/andaro74/pharmadelta/actions/runs/42504215645
  - https://github.com/andaro74/pharmadelta/actions/runs/42503988551
  - https://github.com/andaro74/pharmadelta/actions/runs/42524408048
  - https://github.com/andaro74/pharmadelta/actions/runs/42524407941
  - https://api.github.com/repos/andaro74/pharmadelta/commits/37352ef713af56758316b565287195c3b339ecd2
  - https://github.com/agentkeel-studio/label-impact/blob/956cd87/manifest.yaml
  - https://github.com/agentkeel-studio/label-impact/blob/8cf0563/manifest.yaml
pr: https://github.com/andaro74/pharmadelta/pull/36
---

# Ruling: M06 PR 4 (close)

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which path.

This PR closes M06 at the cap, 4 / 4. It carries the lift by M03's path
(b) as `rulings/pr2.md` 17 ruled, fills the "Measured" cell from a
CI-written result and writes the row's state, rules or carries by name
every open Unsure item of PR 1 to PR 4, and is followed by the tag `m06`
on its merge commit after its run on `main` is read. It decides nothing
about the measurement: the `main` run after #34 merged, 42495856254, is
the measurement, read again at this PR with `gh run download` into a
fresh directory and `python -I` before the cell was written, with the PR
run 42491031888 beside it and the `main` run after #35 merged,
42502413422, read at open.

## Rulings in this PR

1. **Product, Threshold Owner, Data Owner (Unsure 16, ruled in the
   first commit, before any page was written).** The package carries
   the `result.json` of the run each Measured cell cites for rows 0, 1,
   2, 4, 5 and 6, both of row 1's runs (Unsure 35), with row 0's
   `observations.json`; `milestones/README.md`, `SPEC/00-overview.md`,
   the goldens and the four served files under `pages/api/` at the
   build run's commit `226ad89`; and label-impact's `manifest.yaml` at
   the two agent commits the served files name, `8cf0563` and
   `956cd87`. Twenty-two entries, each with the eight fields of
   `ENTRY_RECORD`, null where unused; `manifest.json` inside the zip
   equal to the record's `entries`. Not in it, as the README's table
   says: the M02 artifact's `sources/`, the M04 run's
   `observations.json`, `data/`, and any `m06-gate` result; the
   `sign-off.json` inside is the plant's, since a signature cannot be
   inside what it signs over (Unsure 34).
2. **Product, Rule Owner (Unsure 9, ruled in the first commit).** The
   statement names what the package holds and no more: the CI-written
   results the ledger cites for rows 0, 1, 2, 4, 5 and 6, the ledger,
   SPEC/00, the goldens and the four served files at the commit the
   package names, label-impact's manifest at the agent commits the
   served files name, "as read on the day of the signature". It claims
   no validation, no compliance and no review of the agent's answers;
   it says the package holds what the ledger cites.
3. **Engineering, Security (the lift path, `rulings/pr2.md` 17).**
   M03's path (b), built: `.github/workflows/m06-lift.yml` runs
   `src/m06/build.py` in CI with `permissions` `contents: read` and
   `actions: read`, `GITHUB_TOKEN` in the build step's `env` and
   nothing else, no door secret and no variable of M03's; a grep of the
   JSON records for `ghs_`, `ghp_` and `github_pat_` before the upload,
   the artifact `m06-package-<sha>` for 90 days only when it passed.
   The build imports the gate's `Artifacts`, `api_json`,
   `read_agent_file`, `git`, `git_bytes`, `sha256_hex`, `ci_context`
   and `write_json` and copies none; refuses a checkout not at
   `GITHUB_SHA` or a dirty tree; downloads each cited artifact through
   the API with the 302 fetched without the token and the URL written
   nowhere; reads repository files with `git show <sha>:<path>`; reads
   the manifests through the contents API; checks every member for a
   token's prefix and the door's host or pool prefix; writes a
   deterministic zip and `build.json`, no zip when a source fails.
   `src/m06/page.py` rebuilds the page from the served file by hand in
   the signing commit, deterministic, LF pinned, and imports `esc`,
   `json_text` and `script_json` from `src/m03/lift.py` and the records'
   fields and checks from `src/m06/gate.py`. Two build runs at `226ad89`
   wrote the identical zip (42504215645 by dispatch, 42503988551 by
   push); the dispatch run is the one the record names. `src/m06/
   gate.py`, `m06.yml`, `src/m03/`, `src/m04/`, `src/m05/`,
   `src/baseline/`, `pyproject.toml` and `uv.lock` are unchanged.
4. **Product, Security (the signature; Unsure 1 and 15 as ruled, 19,
   40).** The signature is commit `37352ef`, the seat holder's own,
   made from their terminal and not by the session or by CI, changing
   `pages/api/sign-off.json` and `pages/sign-off.html` and nothing
   else. GitHub reads `author.login` and `committer.login` `andaro74`,
   the login that holds `product` in label-impact's manifest at
   `956cd87`, the commit the reviewer record names; the function shown,
   Regulatory Affairs, is that seat's (SPEC/00 §5). The commit is not
   GPG-signed (`verified` false, `unsigned`), recorded and not required
   at M06 as `rulings/pr2.md` 3 ruled (Unsure 40); if Security later
   requires it, the owner signs commits first and the gate changes
   outside this cap. This ruling records the signature and does not
   make it: a ruling file cannot sign. After `37352ef` nothing changes
   the served file; the close commit touches `milestones/` only.
5. **Product (Measured and state).** Row 7's "Measured" cell cites the
   `main` run after #34 merged, 42495856254 on `e175d77`, artifact
   `m06-gate-e175d772bd32ce9e148f79b868b72a2dcfa8b24f`: RED,
   `signoffs_unsigned` `["s-001"]`, `signoffs_disagreed` `[]`,
   `signoffs_differing` `[]`, `unreadable` `[]`, `written_by_ci` true.
   The PR run on #34 at merge ref `8431885`, 42491031888, is named
   beside it as the run read at the time; it read the same on every
   field the row names (M01 Unsure 23). Both were downloaded again in
   this session before the cell was written. The cell equals the
   expected gate output written at open, so row 7 is GREEN and "PRs
   used / cap" is 4 / 4. The cell then names the lift (the build run and
   its artifact, the zip's commit, the signing commit, the PR run that
   read the lifted state GREEN) as readings after the measurement, as
   rows 4 to 6 name theirs. No finding: the lift read as the close
   expected.
6. **Product, Engineering (the PR run; Unsure 30, 41).** Run
   42524408048 on merge ref `15fef71` read GREEN, every list `[]`,
   `unreadable` `[]`, `read_back` with `author_login` `andaro74`, the
   manifest's login `andaro74`, the hash equal, 22 of 22 entries equal,
   `built_by` equal, eight artifacts listed and downloaded 200, exit 0.
   The read-back paths ran in CI for the first time on this run; every
   read answered. It is the first GREEN of this gate and a reading
   after the measurement; it is recorded in the README and in the cell's
   last sentence and decides nothing. The artifacts it compares expire
   from 2027-01-08; after that a run reads `unreadable` and the
   committed zip, its hash and the signing commit are the record
   (Unsure 7 and 20 as ruled). No re-build is planned.
7. **Product, Tool Owner, Engineering (Unsure 18 as ruled).** The
   signature record has no `read_back` field and the page makes no
   read-back claim: it shows the record as the file holds it (`over`,
   `by`, `method`, `read_from`) and links the `m06.yml` workflow's runs,
   where the read-back is written by CI with its run's link. Who signed
   and when, as read back, is in `result.json` of each run and nowhere
   on the page. Built so; closed at M06.
8. **Engineering, Product (Unsure 20 as ruled).** The build artifact
   expires 2027-02-06T17:17:32Z. Recorded in the gate's `artifacts_read`
   on every run; after it the gate reads `built_by` as `unreadable` and
   the hash in the signing commit stands as the record. As Unsure 7.
9. **Engineering (Unsure 23 as ruled).** The `agent` source reads files
   under 1 MB through the contents API; the two manifests read are 1128
   and 1419 bytes, both 200 on the build and on the gate's run. Closed
   at M06.
10. **Product (Unsure 24 as ruled).** A served sign-off shown as not
    signed is named by no list, as built; not exercised by the lift,
    whose one sign-off is shown as signed. Closed at M06.
11. **Product, Rule Owner (Unsure 25 as ruled).** `SEAT_FUNCTION` is
    SPEC/00 §5's table; on the lift `product` read as Regulatory
    Affairs, equal. Pharmacovigilance and Legal hold no seat and cannot
    sign; the page shows neither as a signature. If §5 changes the gate
    changes with it, outside this cap.
12. **Tool Owner, Engineering (Unsure 29 as ruled).** `package.commit`
    is the build run's full sha, `226ad89ce575d89dfb90c9a5d93a8a5a9d1a31b9`,
    and every `repository` entry's `commit` equals it; the gate reads
    each entry's own commit and requires nothing of `package.commit`
    beyond presence, as PR 3 proposed. Recorded; closed at M06.
13. **Security, Engineering (Unsure 31 as ruled).** No entry path and
    no artifact name holds a token's prefix; the grep step passed on
    both build runs and on every gate run. Closed at M06.
14. **Product (Unsure 32 as ruled).** The lifted page shows every served
    sign-off, which is one; the gate reads one direction and is not
    changed. Closed at M06.
15. **Product (Unsure 10 as ruled).** One person reviews their own work:
    R1 holds, one login in every seat. The sign-off is the seat holder's
    record that the package holds what the ledger cites, read back by
    CI; it is not an independent review and the page does not call it
    one. The banner says one person holds all seven seats. A limit of
    the project, recorded; closed at M06.
16. **Product, Tool Owner (Unsure 15 as ruled).** The page is rebuilt by
    a hand-run writer in the signing commit, not by CI, because the
    commit that changes the served file must be the reviewer's. The gate
    reads page and file equal as parsed JSON whichever writer produced
    the page; `page write` on the head reproduces the page byte for
    byte. Built so.
17. **Engineering, Security (Unsure 33 as ruled).** `m06-lift.yml` runs
    on `workflow_dispatch` and once on a push of its own file on a
    branch other than `main`, as `m03-lift.yml` and `m05-lift.yml` do.
    The dispatch on the branch was accepted before the file was on
    `main`, so the push trigger was not needed; it cost one run that
    wrote the identical zip. It stays for the shape the two earlier
    lifts have; a later lift may drop it, outside this cap.
18. **Product (Unsure 34, 35 as ruled).** The package carries the plant's
    `pages/api/sign-off.json` and the ledger with row 7's cell empty, as
    at `226ad89`: a signature cannot be inside what it signs over, and
    the statement names what the package holds. Row 1's two runs are
    both in; rows 2, 4, 5 and 6 take the `main` run's artifact alone,
    the cell's source. Closed at M06.
19. **Tool Owner, Product (Unsure 36 as ruled).** One basename for the
    milestone, `m06-evidence.zip`; the record carries `package.commit`
    and the hash. A re-build replaces the file and needs a new signing
    commit; none is planned. Closed at M06.
20. **Product, Security (Unsure 37 as ruled).** The download link is the
    zip's GitHub URL pinned at `3e56b07`, the commit that added it, the
    file view and the raw file, with the SHA-256 beside it; `main`'s URL
    would move. Closed at M06.
21. **Engineering, Tool Owner (Unsure 38, recorded).** The zip's archive
    bytes depend on the zlib that deflates them; members are identical
    across builds and archives are not. The committed bytes are the CI
    artifact's; the gate compares the committed file with the artifact's
    file, and a reader who rebuilds compares members and hashes. Storing
    members uncompressed is a build change for a later lift, outside
    this cap; not done here.
22. **Product (Unsure 39).** This PR is #36, the next number on this
    repository after #35.
23. **Security, Product (Unsure 3; M05's 3, M04's 16, M03's 16, M02's
    16).** `M06 gate` is not made a required check in this PR, as the
    M02 to M05 gates were not. `M00 gate` stays the one required
    context, `strict` true, no rulesets, read at the close. No Measured
    cell depends on a required check. The setting is the owner's and is
    carried to no milestone by name; it rests with the owner's settings.
24. **Product, Security (Unsure 2; M05's 2).** GitHub Pages stays not
    enabled; "downloadable" at M06 is the zip's GitHub URL, as
    `rulings/pr1.md` 8 ruled, and the page shows it. Enabling Pages
    rests with the owner's settings and is carried to no milestone by
    name.
25. **Product, Rule Owner, Tool Owner (Unsure 42, recorded).** On this
    PR's head the `M03 gate` read RED on g-001: the door answered with
    a `parsed` object where the served answer is null, after the same
    two tool errors every call has shown since M03 (label-impact's tool
    refuses section `8.1` as a number, M03 Unsure 23); the `main` run
    after #35 read `parsed` null on the same errors and GREEN. The
    door's answer to g-001 varies between calls. Nothing in this PR
    touches `pages/api/answers.json`, the agent or its door; row 4's
    cell cites its `main` run and stands; the reading is recorded in the
    README and in a comment on #36 and in no cell (M03 `rulings/pr4.md`
    6, 22). Whether row 4's served answer is re-lifted when label-impact
    fixes the tool is a PR outside any cap, as M05's re-lift was;
    label-impact's item stays label-impact's.
26. **Product (the cap).** "PRs used / cap" is 4 / 4. After the merge
    the `main` run is read with `gh run download` and `python -I` and
    recorded in a comment on #36, then the owner places `git tag m06
    <merge commit>` and pushes it. A fifth PR on this milestone is a RED
    close with its finding as the result (ADR-0001 U9) and is not
    proposed. The next milestone opens in a new session.

## What a reader can falsify

- `git diff 194a6ab..<head> --stat` touches `.github/workflows/m06-lift.yml`,
  `src/m06/build.py`, `src/m06/page.py`, `pages/evidence/m06-evidence.zip`,
  `pages/api/sign-off.json`, `pages/sign-off.html`,
  `milestones/README.md`, `milestones/M06/README.md` and this file
  only.
- `git log -1 --format='%H %an' -- pages/api/sign-off.json` reads
  `37352ef… andaro74`; `gh api repos/andaro74/pharmadelta/commits/37352ef`
  reads `author.login` `andaro74`.
- `sha256sum pages/evidence/m06-evidence.zip` reads
  `2a3e3760f8fea4961624915108d8ece6e5a14d30d7057e7ca38f979798a1699e`,
  the value of `signature.over`, `package.sha256` and `build.json`'s
  `package.sha256` in the artifact of run 42504215645.
- The artifact of run 42524408048 holds `result.json` with `verdict`
  `GREEN`, every list `[]`, `read_back.commit.author_login` `andaro74`,
  `read_back.equal` true. The artifact of run 42495856254 holds
  `result.json` with `verdict` `RED` and `signoffs_unsigned`
  `["s-001"]`. Download them and read them.
- `uv run python -m src.m06.page write` on the head changes nothing.

## What this ruling does not settle

Label-impact's tool refusing section `8.1` as a number (M03 Unsure 23)
and whether row 4's answer is re-lifted after it is fixed (ruling 25);
GPG-signed commits, if Security wants them (ruling 4); storing the zip's
members uncompressed (ruling 21); the owner's settings (rulings 23, 24).
Each is outside this cap and named with its seat.
