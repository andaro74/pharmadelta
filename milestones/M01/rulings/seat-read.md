---
ruling: m01-seat-read
seat:
  - Security
  - Engineering
authorises:
  # Security: what the workflow may read, and with what token
  - .github/workflows/m01.yml
  # Engineering: the reader's token choice, and the README's record of it
  - src/m01/reader.py
  - milestones/M01/README.md
  - milestones/M01/rulings/seat-read.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/M01/README.md
  - milestones/M01/rulings/pr2.md
  - https://github.com/andaro74/pharmadelta/actions/runs/38190113017
  - https://docs.github.com/en/rest/collaborators/collaborators#get-repository-permissions-for-a-user
pr: https://github.com/andaro74/pharmadelta/pull/15
---

# Ruling: M01 seat read

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9), as #1, #13 and #14 were.
It carries no claim, plants nothing and measures nothing. M01 is closed
at tag `m01`; row 1 is GREEN on its measured RED and does not change.
The ledger is not touched. M03 does not open here.

## Why

Every run of the M01 gate on `main` since `8cdd851` (2026-10-11) has
read PENDING, exit 3, for two reasons: the six assigned seats'
collaborator permission is unread, because `GITHUB_TOKEN` gets 403 from
the permission endpoint on `agentkeel-studio/label-impact`; and the
registry row is unread, because this repository holds no AWS
credential. Run 38190113017 on `8073772` is the latest. Unsure 10 ruled
at PR 2 that when GREEN is wanted before M07, the fine-grained PAT is
the change. This PR makes that change. It removes the first reason
only. The run on `main` still reads PENDING on the second until M03
designs the registry read (Unsure 12).

## Rulings in this PR

1. **Security (Unsure 10).** The secret `M01_READ_TOKEN` was set on
   this repository on 2026-10-12 by the owner (`gh secret list` shows
   it). The steps it was made from name a fine-grained personal access
   token of `andaro74`, resource owner `agentkeel-studio`, repository
   access `agentkeel-studio/label-impact` only, permission Metadata read
   only, expiry 90 days. The token's settings are not readable from this
   repository; the owner confirms them at merge (PR body, Unsure 1), and
   the CI run on this PR shows what it reads. It reads what
   `GITHUB_TOKEN` already read, plus one endpoint: `GET
   /repos/agentkeel-studio/label-impact/collaborators/<login>/permission`.
   It writes nothing. `m01.yml` passes it to the reader step as
   `M01_READ_TOKEN` beside `GITHUB_TOKEN`; the header comment says so
   and no longer says no secret is read. A pull request from a fork
   gets no secret, and that run records the permission as unread, as
   every run did before. Rotation at expiry is the owner's; a lapsed
   token makes the read 401 and the result says so.
2. **Engineering (Unsure 10).** `token()` in `src/m01/reader.py` prefers
   `M01_READ_TOKEN` and names it, then `GITHUB_TOKEN`, then "no
   token", so each permission entry's `why` says which token answered.
   Two lines. No other reading, and no verdict rule, changes. The
   README's falsifier that `secrets.` matches nothing in `m01.yml` was
   true at PR 2 and is marked as since changed.
3. **Product.** This PR is #15, the next number on this repository.

## What a reader can falsify

- `git diff main --stat` touches four files: `.github/workflows/m01.yml`,
  `src/m01/reader.py`, `milestones/M01/README.md` and this file.
  `reader.py` is two added lines.
- `grep -n "secrets\." .github/workflows/m01.yml` matches one line,
  `M01_READ_TOKEN`.
- The M01 gate on this PR (same-repository branch, so the secret is
  present) writes each of the six `andaro74` seats as `permission`
  `admin` with `why` naming `M01_READ_TOKEN`, and a PENDING reason that
  names the registry only. Exit 3; the job fails, as it is not
  required (Unsure 14). Observed on the PR run at `21e19d8`, run
  [38192905362](https://github.com/andaro74/pharmadelta/actions/runs/38192905362):
  all seven seats "admin yes; GitHub answered 'admin' with
  M01_READ_TOKEN"; PENDING, "the registry row for label-impact is
  unread" and nothing else; M00 and M02 gates pass.
- The M01 gate on `main` after merge reads the same.
- The M00 and M02 gates are unchanged and pass.

## What this ruling does not settle

- The registry read (Unsure 12): designed at M03, once, as a read-only
  role in agentkeel assumed by OIDC, flagged there and not here. GREEN
  from this reader is not reachable until then.
- Whether the M01 gate keeps running on push to `main` now that row 1
  is measured (Unsure 14 made it not required). Product.
- The token's rotation record at expiry. Security.
