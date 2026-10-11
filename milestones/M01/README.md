# M01 — The agent is created from the re-made template, seats filled, deployed

Opened 2026-10-10 at PR 1. Two days (SPEC/00 §8). The agent is built in
`agentkeel-studio/label-impact`; the row is measured here.

## Ledger row

Written at PR 1 open. The row in `milestones/README.md` is the ledger's;
this is the same row with the open detail.

| Field | Row 1 |
|---|---|
| Claim | The agent is created from the re-made template, seats filled, deployed |
| Falsifiers | F1.1 label-impact's first pull request is mergeable, or is merged and deployed, while one of its seven seats is not a login that administers the repository. |
| Seeded commit | `eb9b201` on `first-agent` in `agentkeel-studio/label-impact`, [pull request #1](https://github.com/agentkeel-studio/label-impact/pull/1): `manifest.yaml` with `name: label-impact`, six seats `andaro74` and `rule-owner: null`; goldens `g-001` to `g-004`; `data/` as at pharmadelta `m00`; the tool, its schema and the prompt rewritten for labels. |
| Expected gate output | agentkeel's `platform-check` on that pull request fails, naming `rule-owner`. PR 2's reader in this repository reads that check, agentkeel's deploy runs and the registry for `label-impact`, in CI, and writes a `result.json` that is RED on F1.1 naming `rule-owner`. |
| Measured | |
| PRs used / cap | 3 / 4 |
| State | OPEN |

## The false state (P1, P2)

The claim says the seats are filled. It is false when a seat is not
filled and the first pull request can merge, or merges and the platform
deploys the agent anyway. That is what the seeded commit commits: one
seat, `rule-owner`, is `null`; the other six are `andaro74`. Everything
else in the commit is what the lifted agent would carry.

Why `rule-owner`: it is the one seat that decides nothing today (SPEC/00
§5; the guardrail is the platform's until P), so a platform that let it
stay empty would be the easiest to excuse. The plant tests whether the
control reads every seat or only the ones that matter.

What the control is: agentkeel's platform check, `src/validate/agent.py`
at `m08`, which runs `seats.check` over the pull request's head with
`AGENTKEEL_SEAT_REPOSITORY` set to `agentkeel-studio/label-impact`. On a
null seat its message is
`manifest.yaml: seat rule-owner is None: unassigned (SPEC/06 section 2)`,
and the check is posted failed by the platform's App, which the
repository's ruleset requires before a merge (`infra/ruleset/agent.json`).
That the check posts on this pull request and names this seat is the
record PR 2 reads. It is agentkeel's control firing on this plant; it is
not this repository's measurement.

Lifting the plant is one edit to `manifest.yaml` in label-impact:
`rule-owner: andaro74`. Which PR carries the lift is decided after PR 2
goes RED, not here.

## Open detail (PR 1, 2026-10-10)

### What this PR holds, here

- Row 1 of the ledger: falsifier, seeded commit, expected gate output,
  PRs used 1 / 4.
- This file.
- `rulings/pr1.md`.

Nothing else. No reader, no workflow, no test (P2). No edit to
`src/baseline/` (frozen at `m00`, P5), `src/gate/`, `goldens/`, `data/`,
SPEC/00, CLAUDE.md, the README or anything under `milestones/M00/`.

### What the seeded commit holds, in label-impact

The repository is created by the organisation's owner from
`agentkeel-studio/agent-template` (quickstart §0); the owner is the user,
`andaro74`. Recorded at creation:

| Record | Value |
|---|---|
| Repository | `agentkeel-studio/label-impact`, public |
| `created_at` | `2026-10-10T16:54:39Z` (GitHub's; starts agentkeel's clock, SPEC/06 §1; M01 is not timed). Repository id 1413442450 |
| Initial commit | `2d4e43e`, tree `a333557`, the template head's tree |
| App access | The platform App (`agentkeel-platform`, 5144253, installation 166731821) is installed on **selected** repositories, not all. The first ruleset POST was refused, `Invalid integration ids`, until the owner added `label-impact` to the installation by hand. Unsure 8 |
| Ruleset | `infra/ruleset/agent.post.json` at `m08` applied by the owner at `2026-10-10T16:57:28Z`; GitHub's id 24846330; read back equal to `infra/ruleset/agent.json` in `name`, `target`, `enforcement`, `conditions`, `rules` and `bypass_actors` |
| Template head | `66ca2e4ba3e76136549e7d2a0dfdd423acba5fc5`, made from agentkeel `36c97dd` (`.template-source.json`) |

On branch `first-agent`, one commit `eb9b201`
(`eb9b2019a02e127267e7339bbab4b25121158077`),
[pull request #1](https://github.com/agentkeel-studio/label-impact/pull/1)
opened `2026-10-10T17:01:49Z`, left open and not merged:

- `manifest.yaml`: `name: label-impact`; `guardrail` and `model` as the
  template ships them (quickstart §2); `seats`: `product`, `data-owner`,
  `tool-owner`, `threshold-owner`, `security`, `engineering` set to
  `andaro74`, **`rule-owner: null`**, the plant. Everything else as the
  template ships it, including `platform_version: 36c97ddaee93`.
- `goldens/g-001.yaml` to `g-004.yaml`: copied from this repository at
  `m00`, unchanged. `g-005` (guardrail) and `g-006` (redteam) stay here
  until P (SPEC/00 §7); an agent's goldens are ordinary or trap only.
- `data/table.json`, `data/clauses.json`: copied from this repository at
  `m00`, unchanged. The fields are `milestones/M00/fields.md`'s.
- `tools/find_label_row.json`, `prompt.txt`, `agent.py`: the template's
  tool, schema and prompt are written for refagent's rights table (title,
  territory, platform, date) and its clause ids (`ML-2.1` and the like).
  They are rewritten for labels: the tool takes a label and a section,
  returns the one row of `data/table.json` with that `table_row` and the
  clauses that row can be read under, and decides nothing; the prompt
  names the three labels and the answer's three fields (`impacted`,
  `owed`, `escalate`). Contract in `rulings/pr1.md`; built there, by
  Engineering, under the Tool Owner's contract.
- `server.py`, `__init__.py`, `README.md`, `.template-source.json`: as
  the template ships them.

### Observed at open

Written after the pull request was opened. This is agentkeel's record,
not this repository's measurement (P4); PR 2's CI-written result is.

Before the platform check posted, read at `2026-10-10T17:02Z` with
`gh pr view 1`: `mergeable` `MERGEABLE`, `mergeStateStatus` `BLOCKED`, no
check run on `eb9b201`. GitHub's `mergeable` says only that the branch
has no conflict; `mergeStateStatus` (`mergeable_state` in the REST form)
is what the ruleset decides, and `BLOCKED` is the required check not yet
posted. F1.1's "mergeable" is `mergeable_state` `clean`, as agentkeel's
observer reads it (SPEC/06 §4), never the `mergeable` field.

The platform check, posted by agentkeel's scheduled
[run 38070849620](https://github.com/andaro74/agentkeel/actions/runs/38070849620)
(started `17:13:24Z`) as check run
[114267967935](https://github.com/agentkeel-studio/label-impact/runs/114267967935)
on `eb9b201`, completed `2026-10-10T17:14:24Z`:

| Field | Value |
|---|---|
| `name` | `platform-check` |
| `app.id` | 5144253 |
| `conclusion` | `failure` |
| `output.title` | `1 refused` |
| `output.summary` | `seats assigned, each a login that administers the repository: agents/label-impact/manifest.yaml: seat rule-owner is None: unassigned (SPEC/06 section 2)` |
| `output.text` | `Posted by agentkeel's platform check from its main (SPEC/06 section 6).` |

Read after it posted: `mergeStateStatus` still `BLOCKED`. The check named
the planted seat and nothing else: name, guardrail, image files, manifest
schema, edges, lifecycle and the four goldens all passed, so the only
thing between this pull request and a merge is `rule-owner`. That is the
record the expected gate output names. PR 2 reads it in CI and writes the
result; nothing here is the measurement.

### What this PR does not hold

- No reader of the platform check, the deploy runs or the registry. That
  is PR 2's, and it is carried below.
- No lift. `rule-owner` stays `null` in label-impact until the PR that
  carries the lift, decided after PR 2 goes RED.
- No merge in label-impact. The first pull request stays open.
- No number that is not a CI-written result with a link.

### What a reader can falsify

- `manifest.yaml` at `eb9b201` carries `rule-owner: null` and six seats
  `andaro74`. Open the commit on GitHub.
- The four goldens, `data/table.json` and `data/clauses.json` at `eb9b201`
  are byte-equal to this repository's at `m00`:
  `git diff m00 -- goldens/g-001.yaml` and so on against the clone.
- `g-005` and `g-006` are not in label-impact.
- The pull request's `platform-check` is posted by agentkeel's App
  (`integration_id` 5144253), not by a workflow in label-impact, which
  has none: the repository's `.github/` does not exist.
- The template's head at creation is `66ca2e4`: the repository's first
  commit is that commit's tree, and `.template-source.json` names
  `36c97dd`.
- Nothing in this repository reads label-impact. Grep `label-impact`
  under `src/` and `.github/`: no match.

### Carried to PR 2

- The reader: a script in this repository that, in CI, reads the
  platform check on label-impact's first pull request (GitHub's checks
  API: conclusion, App id, output text), the pull request's
  `mergeable_state` and merge state, agentkeel's `deploy.yml` runs that
  name `label-impact`, and the registry row for `label-impact`; and
  writes a `result.json` with one verdict, read as the ledger's expected
  gate output reads it. RED while any seat in `manifest.yaml` at the
  first pull request's head is not a login that administers the
  repository, naming each such seat: the claim "seats filled" is false,
  and on `eb9b201` that is `rule-owner`. GREEN only when every seat is
  assigned, the pull request is merged, the platform's deploy run for
  that merge succeeded and the registry holds `label-impact`. Beside the
  verdict it records the control: the check's conclusion, App id and
  output, the `mergeable_state`, the deploy runs and the registry read.
  A pull request found with `mergeable_state` `clean`, or merged, while
  a seat is unassigned is RED with F1.1 as the finding, named as such;
  the plant is expected to produce the other RED, the check refusing it,
  and that reading is the one the ledger cell names. `written_by_ci` and
  the run URL as M00's. (Corrected before the merge of PR 1: the first
  draft said GREEN when the check refused the pull request, which
  disagreed with the ledger's cell.)
- What token the reader needs, and whether it needs one (Unsure 3).
- Whether the registry is read through AWS or through Grafana panel 1,
  and with what credential (Unsure 3).

## Open detail (PR 2, 2026-10-10)

PR 2 is the measure. It adds the reader that reads the plant and nothing
that lifts it. `rule-owner` stays `null` at `eb9b201`; label-impact's
first pull request stays open. M01 is measured here (SPEC/00 §3).

### What this PR holds

- `src/m01/reader.py`: the reader. In CI it reads, from GitHub's REST
  API with this repository's `GITHUB_TOKEN`: label-impact's first pull
  request (state, head, `merged`, `mergeable`, `mergeable_state`), and
  beside it GraphQL's `mergeStateStatus`, the field `gh pr view` shows;
  `manifest.yaml` at the head, the seven seats of SPEC/00 §5; for each
  seat that is a string, what GitHub says the login holds on the
  repository, asked as agentkeel's seat validator asks it
  (`src/validate/seats.py` at `m08`: the owner, then the collaborator
  permission endpoint); every check run on the head with its App id,
  conclusion and output, and the check names its own summary says it
  refused; the ruleset's required checks; agentkeel's `deploy.yml` runs
  since the repository was created, with the jobs in each that name
  `label-impact`; and the registry, which it records as unread because
  this repository holds no credential for it. It writes `result.json`
  with every reading beside one verdict:
  - **RED** while any seat at the head is not a login that administers
    the repository: `null`, empty, not of a login's form, or read as a
    permission other than `admin`. Each is named in `seats_unassigned`.
    A login the permission endpoint answers 404 for is unread, not
    unassigned: the reader cannot tell "not a collaborator" from "this
    token cannot see collaborators". No `manifest.yaml` at the head
    (404) is every seat unassigned, RED, not UNSCORABLE. The `finding`
    is `F1.1` when the pull request is also merged or read as mergeable;
    `control refused` when a `platform-check` from App 5144253 refused
    the head naming the seats check, the reading the ledger's expected
    output names; otherwise `unassigned, no refusal read`. (Repair, PR 3:
    at PR 2 the second finding was written on every RED where the pull
    request was not mergeable, whether or not a check had refused it.)
    "Read as mergeable" is `mergeStateStatus` `CLEAN`, `UNSTABLE` or
    `HAS_HOOKS` when GraphQL was read, else `mergeable_state` `clean`,
    `unstable` or `has_hooks`: the states GitHub merges from. Either is
    judged only when a token asked; `mergeable_judged` records the
    source. (Repair, PR 3: at PR 2 `clean`/`CLEAN` alone was judged
    mergeable.)
  - **GREEN** only when every seat is assigned and read as `admin`, the
    pull request is merged, a `deploy-agent` job of agentkeel's
    `deploy.yml` naming `label-impact` and the merge commit
    (`merge_commit_sha`: main's head after the merge, which agentkeel
    deploys) concluded `success`, and the registry was read and holds
    `label-impact`. (Repair, PR 3: at PR 2 the leg was matched on the
    branch head, which agentkeel never deploys after a merge.)
  - **PENDING** when neither: no seat is read as unassigned and GREEN is
    not shown. `green_blocked_by` names what is missing. A seat whose
    permission is unread, or an unread registry, lands here, never in
    GREEN.
  - **UNSCORABLE** when the pull request, the repository, the manifest
    (any answer but 200 or 404) or the check runs could not be read, or
    anything raises inside `main`. Never RED, never GREEN. The error is
    written in the result. A failure before `main` runs, an import error,
    exits 1 with no file; the file, not the exit code, is the verdict
    (Unsure 19).

  Exit 0 GREEN, 1 RED, 2 UNSCORABLE, 3 PENDING. Anything else that is
  unread is written as unread with the status GitHub gave and which
  token asked, never left out and never read as a pass. A seat's
  `admin_read` is `true` when the judgement needed no permission read,
  so an unassigned seat carries `admin_read: true` and `admin: null`;
  it is `false` only on an assigned seat whose permission GitHub did
  not answer.
- `.github/workflows/m01.yml`: on every pull request, every push to
  `main` and by hand. `uv sync --locked`, the artifact directory, the
  reader, then the artifact `m01-gate-<sha>` holding `result.json`,
  uploaded whenever the reader wrote one, which is whenever `main` ran;
  an import error before `main` exits 1 with no file, and the upload
  then fails on `if-no-files-found: error` (Unsure 19). The reader writes
  the per-reading table to the job summary. The job fails on anything
  but GREEN. The workflow reads two public repositories with
  `GITHUB_TOKEN` and no secret of this repository. `gate.yml` is
  unchanged.
- `result.json` records the commit, whether the tree was dirty, whether
  CI wrote it (`written_by_ci`), the run's URL and which token read, so
  the file says for itself whether it is evidence (P4).
- `rulings/pr2.md`, and "PRs used / cap" set to 2 / 4 here and in the
  ledger.

### What this PR does not hold

- No lift. No commit to label-impact, no merge there. `rule-owner` is
  `null` at the head the reader reads.
- No edit to `src/baseline/` (P5), `src/gate/score.py`, `goldens/`,
  `data/`, SPEC/00, CLAUDE.md, the README or `milestones/M00/`.
- No credential. The seat-permission read and the registry read each
  need one this repository does not hold; both are under Unsure (PR 2)
  with the seat whose ruling settles them.
- No test of the reader. Its reading is checked against "Observed at
  open" above, against the construction run below, and against the CI
  run on this PR.
- No "Measured" cell. That is PR 4's, from the CI run's link.
- No branch protection. Whether `M01 gate` is required on `main` is a
  repository setting; see Unsure (PR 2).

### Construction run (not evidence, P4)

Run once on 2026-10-10 on the branch before the first push, with no
token, so the reads are what an unauthenticated caller gets. CI's
`GITHUB_TOKEN` is authenticated but has no access to the organisation,
so its reads may differ; the CI run on this PR says how.

| Reading | What the reader wrote |
|---|---|
| pull request | `#1` at `eb9b201`, state `open`, `merged` false, `mergeable` true, `mergeable_state` **`unstable`**; GraphQL unread (needs a token; the reason string at PR 2 printed it as `None`, repaired at PR 3 to `unread`) |
| seats | `rule-owner` is `None`: unassigned. The six `andaro74` seats: assigned, permission **unread**, `GET collaborators/andaro74/permission` answered 401 with no token |
| check runs on the head | one: `platform-check`, App 5144253 (`agentkeel-platform`), conclusion `failure`, title `1 refused`, refused `["seats assigned, each a login that administers the repository"]` |
| required checks | ruleset 24846330: `platform-check` from integration 5144253, read with no token |
| agentkeel deploy runs | 8 since `2026-10-10T16:54:39Z`, every one `sign-agent` and `deploy-agent` skipped, 0 jobs naming `label-impact` |
| registry | unread: no credential |
| verdict | RED, `finding` `control refused`, `seats_unassigned` `["rule-owner"]`, exit 1 |

Two readings differ by who asks, found in this run and recorded for the
CI run to settle:

- REST's `mergeable_state` was `unstable` with no token and `blocked`
  with an administrator's token; GraphQL's `mergeStateStatus` was
  `BLOCKED` with the administrator's token. GitHub shows a caller without
  access to the rulesets a state that does not account for them. Neither
  word is `clean`, so the verdict is the same either way; the reader
  records both forms and which token asked, and judges "mergeable" on
  `clean` or `CLEAN` only (Unsure 11).
- The collaborator permission endpoint answers only a token with access
  to the repository. With none the six assigned seats are recorded as
  "permission unread", so the reader as built cannot go GREEN from this
  repository's CI until a token is ruled (Unsure 10). That is the right
  reading for PR 2, where RED is expected, and it is said here rather
  than hidden.

### Expected CI result on this PR

The ledger row says: RED, naming `rule-owner`. The reader reads
`manifest.yaml` at `eb9b201`, finds `rule-owner` `None`, and writes
`verdict: RED`, `seats_unassigned: ["rule-owner"]`, `finding: "control
refused"`, with the platform check's refusal beside it, `written_by_ci`
true and the run URL. The CI run on this PR is the measurement; the
construction run above decides nothing.

### Observed (CI run, 2026-10-10)

The first run on this PR,
[38077129178](https://github.com/andaro74/pharmadelta/actions/runs/38077129178),
wrote the artifact `m01-gate-223de2d13d518ce23327373cfff9775a49c24e0f`
(the sha is the pull request's merge ref, as M00's artifacts were). It
holds:

| Field | Value |
|---|---|
| `verdict` | `RED` |
| `finding` | `control refused` |
| `seats_unassigned` | `["rule-owner"]` |
| `seats_admin_unread` | the six `andaro74` seats: `GET collaborators/andaro74/permission` answered 403 with `GITHUB_TOKEN` |
| `pull_request` | head `eb9b201`, `open`, `merged` false, `mergeable_state` `blocked`, GraphQL `mergeStateStatus` `BLOCKED`, `statusCheckRollup` `FAILURE` |
| `control.check_runs` | one: id 114267967935, `platform-check`, App 5144253, `failure`, refused `["seats assigned, each a login that administers the repository"]` |
| `control.required_checks` | ruleset 24846330: `platform-check` from integration 5144253 |
| `deploys` | 9 runs since `2026-10-10T16:54:39Z`, all read, none naming `label-impact`, not truncated |
| `registry` | unread, no credential |
| `written_by_ci` | `true`; exit 1; the `M01 gate` job failed; `M00 gate` on the same head passed: [run 38077129122](https://github.com/andaro74/pharmadelta/actions/runs/38077129122) |

Equals the expected result above. Two reads differ from the
construction run, by token: REST `mergeable_state` is `blocked` with
`GITHUB_TOKEN` where it was `unstable` with none, and the permission
endpoint answers 403 where it answered 401. Neither changes the verdict.

### What a reader can falsify

- The artifact `m01-gate-<sha>` on this PR's run holds a `result.json`
  with `verdict: RED`, `seats_unassigned: ["rule-owner"]` and
  `written_by_ci: true`. Download it and read it.
- The `control.check_runs` entry in it equals "Observed at open" above:
  id 114267967935, App 5144253, conclusion `failure`, title `1 refused`.
- `src/m01/reader.py` reads no file of this repository's content: every
  reading of label-impact and agentkeel comes from GitHub's API at run
  time. It runs `git rev-parse HEAD` and `git status --porcelain` for the
  result's `commit` and `dirty`, and writes the result and the summary.
  Grep `open(` under `src/m01/`: two `urllib.request.urlopen` calls to
  the API and one `args.summary.open` in append mode; `read_text` does
  not occur; `subprocess.run` occurs once, in `git`. (Repair, PR 3: the
  sentence said "reads nothing from disk".)
- The verdict is formed from the seats, the merge state, the deploys and
  the registry only; the check runs are recorded and named in the
  reason, and do not decide RED. Read `judge` in `src/m01/reader.py`.
- No path under `src/m01/` or in `m01.yml` names a secret: grep
  `secrets.` in `.github/workflows/m01.yml`, no match.
- Nothing in this PR changes label-impact. The pull request's head is
  still `eb9b201` and `rule-owner` is still `null` there.
- `git diff main --stat` on this PR touches `src/m01/`,
  `.github/workflows/m01.yml`, `milestones/README.md`,
  `milestones/M01/README.md` and `milestones/M01/rulings/pr2.md` only.

### After this PR goes RED

The plant is lifted by the one edit named under "The false state":
`rule-owner: andaro74` in label-impact's `manifest.yaml`.

**Ruled at PR 2, on reading run 38077129178 (Product).** The lift is
carried by PR 4, as M00's was (`milestones/M00/rulings/pr4.md`). PR 3,
if the cold review of #7 finds anything, repairs and does not lift; if
it finds nothing, PR 3 is skipped. The Measured cell takes run
38077129178: RED naming `rule-owner`, which equals the row's expected
output. PR 4 records the lift commit, the platform check that passes
it, the merge and agentkeel's `deploy-agent` job for the merged head,
each with its link. PR 4 does not claim GREEN from this reader: with
Unsure 10 and 12 ruled as they are, the reader reads PENDING after the
lift, naming the unread seat permissions and the unread registry.

## Repair (PR 3, 2026-10-10)

PR 3 is the repair: what the cold review of PR 2 (#7) found, and nothing
else. The plant stands; `rule-owner` is `null` at `eb9b201` and
label-impact's first pull request is open. The review found three
defects in the reader and ten inexact sentences. Nothing here decides
the row: PR 2's run 38077129178 was the measurement, and PR 4 fills the
"Measured" cell from it.

### Defect 1: the deploy leg was matched on the branch head

GREEN asked for a `deploy-agent` job naming `label-impact` at the pull
request's head sha. agentkeel deploys main's head: `deployable` in
`scripts/platform_check.py` at `m08` reads `branch["commit"]["sha"]`,
which after a merge is the merge commit, never the branch head. The
reader read `merge_commit_sha` into the result and did not use it, so
GREEN was unreachable on a merged pull request whatever the deploy did.

Fix in `src/m01/reader.py`, `judge`: the leg's commit is matched on
`merge_commit_sha`. Input that showed it: a merged pull request with a
`deploy-agent` leg at the merge commit read PENDING before, GREEN after
(construction check D1 below).

### Defect 2: "control refused" was written with no refusal read

The `finding` `control refused` was written on every RED where the pull
request was not found mergeable, whether or not any check run had
refused anything. A head with the null seat and no `platform-check` yet
posted would have carried the finding the ledger's expected output
names.

Fix in `judge`: `control refused` needs a check run named
`platform-check` from App 5144253 whose summary refused the seats
check, as the reader already parsed it. Without one the finding is
`unassigned, no refusal read`: the claim is false on the manifest alone
and no control is on record. F1.1 keeps precedence over both. The third
name is Product's to confirm (Unsure 18).

### Defect 3: "mergeable" was `clean` only

F1.1's "mergeable" was judged on `mergeable_state` `clean` or
`mergeStateStatus` `CLEAN`. GitHub merges from `unstable` (a failing
status that is not required) and `has_hooks` too, so a pull request in
either state with the null seat would have read `control refused`
instead of F1.1.

Fix in `judge_mergeable`, new: the sets are `clean`, `unstable`,
`has_hooks` and `CLEAN`, `UNSTABLE`, `HAS_HOOKS`. GraphQL decides when it
was read, else REST, and `mergeable_judged` in the result names the
source and the value. One consequence, handled in the same fix: the
construction run at PR 2 with no token read REST `unstable` on this
head while the ruleset blocked it, so the widened set would have read
F1.1 from a no-token run. "Mergeable" is therefore judged only when a
token asked; with none it is unread for F1.1's purpose, recorded as
such, and the finding cannot be F1.1. Unsure 11 is updated in place.

### Prose, repaired in place

Each sentence is rewritten where it stands, as M00's Q4 and Q6 were.

| Where | Said | Now says |
|---|---|---|
| Ledger row 1 and this file, expected gate output | "RED on F1.1 naming `rule-owner`" | Not edited: written at open, and the Measured cell is read against it. It reads: RED on row 1, whose falsifier is F1.1; the `finding` field names the arm, `control refused` on the plant. Unsure 20. |
| "What this PR holds", RED | "not a login" | "not of a login's form"; a login the permission endpoint answers 404 for is unread, not unassigned |
| "What this PR holds", RED | `control refused` otherwise | `control refused` only on a refusal read; else `unassigned, no refusal read` (Defect 2) |
| "What this PR holds", RED | `clean`/`CLEAN` | the three states GitHub merges from, token only (Defect 3) |
| "What this PR holds", GREEN | "the merged head" | "the merge commit" (Defect 1) |
| "What this PR holds", UNSCORABLE | "the manifest ... could not be read" | a 404 on `manifest.yaml` is every seat unassigned, RED; UNSCORABLE is any other answer but 200 |
| "What this PR holds", exit codes | nothing on `admin_read` | an unassigned seat carries `admin_read: true`, `admin: null`: nothing was unread |
| "What this PR holds", `m01.yml` | "uploaded whenever the job reached the reader step" | uploaded whenever `main` ran; an import error exits 1 with no file (Unsure 19) |
| "Construction run", pull request | "GraphQL unread" | the reason string printed `mergeStateStatus None`; now `unread` |
| "What a reader can falsify" | "reads nothing from disk" | reads no file of this repository's content; runs `git rev-parse` and `git status` for provenance |
| "Observed (CI run)" | "`M00 gate` on the same PR passed" | with the link, run 38077129122 |
| `reader.py`, `read_deploys` | leg name `(<name>, <repository>, <commit>)` | `(<repository>, <repository_id>, <commit>, <name>, <rollout>)`, the matrix row's key order; the reader finds the name and the sha by content, so the code was right and the sentence was not |

### Construction checks (not evidence, P4)

Run on this branch on 2026-10-10. The live plant: with the owner's
token and with none, in the scratch directory, not committed. The
synthetic cases: `judge` called on hand-made inputs the live plant
cannot produce, with no API call.

| Input | Before PR 3 | After PR 3 |
|---|---|---|
| live, owner's token | RED, `control refused`, `["rule-owner"]`; `mergeStateStatus BLOCKED` | the same; `mergeable_judged` source `graphql`, value `BLOCKED` |
| live, no token | RED, `control refused`; reason printed `mergeStateStatus None` | RED, `control refused`; `mergeable_judged` unread, "no token asked"; reason prints `unread` |
| D1: merged, `deploy-agent` leg at the merge commit, every seat admin, registry row | PENDING | GREEN |
| D1: merged, leg at the branch head only | GREEN | PENDING |
| D2: `rule-owner` null, `BLOCKED`, no check run on the head | RED, `control refused` | RED, `unassigned, no refusal read` |
| D2: the same with the App's refusal | RED, `control refused` | RED, `control refused` |
| D3: `rule-owner` null, `mergeStateStatus UNSTABLE` | RED, `control refused` | RED, `F1.1`, source `graphql` |
| D3: `HAS_HOOKS` | RED, `control refused` | RED, `F1.1`, source `graphql` |
| D3: GraphQL unread, REST `unstable`, token set | RED, `control refused` | RED, `F1.1`, source `rest` |

### What this PR does not hold

- No lift. `rule-owner` stays `null` at `eb9b201`; nothing is committed
  to label-impact. The lift is PR 4's, ruled at PR 2.
- No edit to `rulings/pr2.md`. A ruling is a record of what was ruled;
  its ruling 1 ("the artifact is written whenever the reader step
  started") and ruling 5 ("the pull request is not mergeable") stand
  as the record of what PR 2 claimed, and this section says where they
  were inexact.
- No edit to `src/baseline/` (P5), `src/gate/`, `goldens/`, `data/`,
  SPEC/00, CLAUDE.md, the README or `milestones/M00/`.
- No "Measured" cell. That is PR 4's, from run 38077129178.
- No token and no registry read (ruled at PR 2, Unsure 10 and 12).
- No edit to `.github/workflows/m01.yml`: the review found nothing in
  it. The `ruff` format and one `UP031` finding on `reader.py` predate
  this PR and CI does not run `ruff`; not the review's and not repaired.
- No test file. The synthetic checks above were run from the scratch
  directory and are not committed (Unsure 21).

### Expected CI result on this PR

RED, `finding` `control refused`, `seats_unassigned` `["rule-owner"]`,
`mergeable_judged` source `graphql` value `BLOCKED`, `written_by_ci`
true. The plant is not lifted, so RED is the correct reading, and the
`M01 gate` job fails. `M01 gate` is not required on `main` (Unsure 14,
ruled), so this PR merges on `M00 gate` alone, with nothing merged over
a check.

### Observed (CI run, 2026-10-10)

The first run on this PR,
[38098770569](https://github.com/andaro74/pharmadelta/actions/runs/38098770569),
on commit `835643e` (the artifact's sha is the pull request's merge
ref, as PR 2's was), wrote the artifact
`m01-gate-dab1b72c36e7718c01cbd11c4c18e6e9777c5195`. It holds:

| Field | Value |
|---|---|
| `verdict` | `RED` |
| `finding` | `control refused` |
| `seats_unassigned` | `["rule-owner"]` |
| `seats_admin_unread` | the six `andaro74` seats: `GET collaborators/andaro74/permission` answered 403 with `GITHUB_TOKEN` |
| `mergeable_judged` | `read` true, `mergeable` false, source `graphql`, value `BLOCKED`, "mergeStateStatus 'BLOCKED' with GITHUB_TOKEN" |
| `pull_request` | head `eb9b201`, `open`, `merged` false, `mergeable_state` `blocked`, GraphQL `mergeStateStatus` `BLOCKED` |
| `control.check_runs` | one: id 114267967935, `platform-check`, App 5144253, `failure`, refused `["seats assigned, each a login that administers the repository"]` |
| `deploys` | 37 runs since `2026-10-10T16:54:39Z`, all read, none naming `label-impact`, not truncated |
| `registry` | unread, no credential |
| `written_by_ci` | `true`; exit 1; the `M01 gate` job failed; `M00 gate` on the same head passed: [run 38098770600](https://github.com/andaro74/pharmadelta/actions/runs/38098770600) |

Equals the expected result above. The reason string now reads
`mergeStateStatus BLOCKED`, where PR 2's would have read `'BLOCKED'`
and a no-token run's `None`. Every other reading equals PR 2's run
38077129178 except the deploy count, which grew from 9 to 37 as
agentkeel's schedule ran (Unsure 15: still within one page).

## Unsure (PR 3)

Each needs a seat's ruling. None changes the measurement.

| # | Item | Seat |
|---|---|---|
| 18 | The third finding's name, `unassigned, no refusal read`, is Engineering's choice at PR 3. It means: a seat is unassigned, the pull request is not read as mergeable, and no `platform-check` from the App is on record refusing the seats check. Confirm the name or give another; the two the ledger knows, `F1.1` and `control refused`, are unchanged. | Product |
| 19 | An import error in the reader (a missing dependency, a syntax error) exits 1, the RED code, before `main` runs, and writes no `result.json`; the upload then fails on `if-no-files-found: error`, so no artifact exists. The file is the verdict and the exit code is not, so no RED can be read from it; but the job's red mark looks like RED. Proposed: leave it; a missing artifact is "no result", and the ledger reads artifacts only. Or: a wrapper step that writes UNSCORABLE when the reader exits with no file. | Engineering |
| 20 | The ledger's expected gate output says "RED on F1.1 naming `rule-owner`" and the result's `finding` is `control refused`. The cell was written at open and is not edited here. Reading: "RED on F1.1" is RED on the row whose falsifier is F1.1, and `finding` names which arm; the plant's arm is the refusal. Confirm that reading, or rule that PR 4's Measured cell must say so in its own words. | Product |
| 21 | The synthetic checks of `judge` are not committed. Committing them would be a test of the reader, which PR 2 said it does not hold; the next milestone that changes `judge` should decide whether `judge` gets a test file under `src/m01/`. | Engineering |

## Unsure (PR 2)

Each needs a seat's ruling. PR 1's items 1, 2, 5, 8 and 9 stand as
written; this PR touches none of them. Items 3 and 4 are addressed below.

| # | Item | Seat |
|---|---|---|
| 10 | **The token.** This repository's `GITHUB_TOKEN` reads, on the two public repositories, the pull request, the commit's contents, the check runs, the rulesets and the Actions runs and jobs: all read with no token in the construction run, so an authenticated token reads them too, with a higher rate limit. It cannot read a seat's collaborator permission on `agentkeel-studio/label-impact`: that endpoint answers only a token with access to the repository (401 with none; the CI run says what `GITHUB_TOKEN` gets). So the reader records the six assigned seats' permission as unread, and GREEN is not reachable from this CI as it stands. Settles PR 1's Unsure 3 for the GitHub half. Proposed: a fine-grained PAT of the owner with Metadata read on the organisation's repositories, or a token minted by agentkeel's observer App, set as a repository secret named by Security and passed to the reader step as `GITHUB_TOKEN`; who sets it and under which seat's record. Not done in this PR. **Ruled at PR 2** (`rulings/pr2.md` 6): not needed to close M01; the seat read matters only for GREEN. Ruled again when a milestone needs GREEN from this reader, M07 at the latest; if earlier, the fine-grained PAT, as the smaller change. | Security, Engineering |
| 11 | **Merge state by token.** REST `mergeable_state` read `unstable` with no token and `blocked` with the owner's; GraphQL `mergeStateStatus` read `BLOCKED` with the owner's and is unread with none. The reader records both and judges "mergeable" on `clean`/`CLEAN` only. Whether a caller without access could ever be shown `clean` while the ruleset blocks the merge is not known; if it could, F1.1's reading from this CI would need the token of item 10. **Repaired at PR 3:** `unstable` and `has_hooks` are now mergeable (Defect 3), so the no-token reading above would read F1.1 on a head the ruleset blocks. The reader therefore judges F1.1's "mergeable" only when a token asked, GraphQL deciding when read, else REST, and records the source in `mergeable_judged`; with no token it is unread for F1.1. Why REST without a token shows `unstable` is still not known. | Engineering |
| 12 | **The registry.** Recorded as unread. GREEN is impossible while it is. Read it through AWS (a read-only role this repository assumes by OIDC, in the agent account: an agentkeel change, flagged not designed here) or through Grafana panel 1 (a Grafana token as a secret here, the pattern of agentkeel's `evals.yml`), or leave it unread until M03 needs the deployed agent. Settles PR 1's Unsure 3 for the AWS half only by naming the options. **Ruled at PR 2** (`rulings/pr2.md` 7): unread through M01. The read is designed at M03, once, as a read-only role in agentkeel assumed by OIDC, flagged there and not here. | Security, Product |
| 13 | **PENDING.** The reader has a fourth verdict for "not RED, not GREEN, readable": every seat assigned but the pull request not merged, or merged but not deployed, or the registry unread. The ledger knows RED, GREEN and UNSCORABLE. Proposed: PENDING is an exit 3, fails the job, and is never written to a Measured cell; the cell takes RED or GREEN only. **Ruled at PR 2** (`rulings/pr2.md` 8): as proposed. | Product |
| 14 | **Required check.** Whether `M01 gate` is made a required check on `main` after this PR merges, as `M00 gate` was (M00 Unsure 12). While the plant stands the job is RED on every run, so PR 3 and PR 4 cannot merge on their own run; M00 Unsure 17's pattern was an administrator merging over the check, on record, with the lift in PR 4. The same choice is owed here, after this run is read. **Ruled at PR 2** (`rulings/pr2.md` 9): `M01 gate` is not made required on `main`. After the lift the reader reads PENDING until items 10 and 12 are read, and a required check would block every later PR for that reason alone. No PR of M01 is merged over a check. | Security, Product |
| 15 | **Deploy runs grow.** agentkeel's `deploy.yml` runs every ten minutes; the reader reads up to 100 runs since the repository was created, one jobs call each, and records `truncated` when more exist. Within a day the window closes over the plant's early runs; a deploy that scrolled out of it is unread and blocks GREEN until read another way (the registry row, item 12, names the deploying run). | Engineering |
| 16 | **PR 1's Unsure 4.** The platform check's output on the pull request is now read by the reader: it refused the seats check only, and passed the goldens, so `g-004`'s `escalate` field and `314.80(c)(1)(i)` clause survived agentkeel's golden validation at `eb9b201`. Proposed: ruled, by that record. **Ruled at PR 2** (`rulings/pr2.md` 10): closed, by that record; PR 1's Unsure 4 is settled. | Data Owner, Tool Owner |
| 17 | The ruling file names this PR as #7, the next number on this repository. Confirmed: #7. | Product |

## Unsure (PR 1)

Each needs a seat's ruling. None blocks the plant.

| # | Item | Seat |
|---|---|---|
| 1 | The template was not re-made at `m08`. Its head `66ca2e4` was made from agentkeel `36c97dd`, which is `m07~1`, 78 commits before `m08`. Between the two, nothing under `agents/refagent/`, `scripts/make_template.py`, `infra/ruleset/` or `src/validate/` changed; `docs/developer/template-README.md` changed by two lines, and `platform_version` would read `m08` instead of `36c97ddaee93`. Product chose to create from the template as it stands (2026-10-10, option 1 of two). SPEC/00 §3's sentence "from a template re-made at `m08`" is then not literally met; a one-line edit to §3 is owed under Product. | Product |
| 2 | How label-impact's own pull requests count against the cap: this repository's four, or label-impact's own. Proposed: the cap of four is this repository's; label-impact's pull requests are the seeded commit and the lift and are counted in this file, not in the ledger's cell. | Product |
| 3 | Whether PR 2's reader reads GitHub's checks API and agentkeel's deploy runs with the user's token in this repository's CI, and what secret that needs. The checks on a public repository's pull request and the runs of a public repository's workflow are readable without a token, within GitHub's rate limit for unauthenticated calls; `GITHUB_TOKEN` of this repository reads them too. The registry is a DynamoDB table in the agent account, read with an AWS credential this repository does not hold. | Security, Engineering |
| 4 | Whether the `m00` goldens' `escalate` field and `g-004`'s `314.80(c)(1)(i)` clause survive agentkeel's golden validation unchanged. Read against `src/validate/agent_goldens.py` at `m08`: the validator asks the seven top-level fields, `kind` in {ordinary, trap}, `expected` with exactly `table_row`, `clause_id` and a non-empty `answer_fields`, and that the row and clause exist in the agent's own `data/`. It does not read the answer fields' names or values. `314.80(c)(1)(i)` is a key of `data/clauses.json`. The platform check's output on the pull request is the record. | Data Owner, Tool Owner |
| 5 | Whether U3's trap (`g-004`) is measured on the deployed agent at M01 as ADR-0001 says, given the guardrail is the platform's. The deploy asks the agent its goldens after a merge and records the answer; at M06 a failing golden blocks nothing (quickstart §5). Nothing merges in this PR, so nothing is asked at PR 1. | Data Owner |
| 6 | The template's `agent.py` reads its file fallback from `BUNDLE.parents[1] / "data" / "rights_table.json"`, a path above an agent repository's root. The rewrite points it at `data/table.json` beside `agent.py`. The deployed runtime reads DynamoDB and never takes the fallback. | Engineering |
| 7 | The ruling file names this PR as #6, the next number on this repository. | Product |
| 8 | The platform App's installation on `agentkeel-studio` covers selected repositories, not all. agentkeel SPEC/06 §6 and quickstart §0 say the App is installed on all the organisation's repositories, and the owner's creation steps do not include adding the new repository to the installation. Without it, the ruleset POST is refused (`Invalid integration ids`) and no platform check can post. On this project the owner added `label-impact` by hand between creation and the ruleset. Sharper: agentkeel's scheduled check [run 38069629989](https://github.com/andaro74/agentkeel/actions/runs/38069629989) at `16:55:31Z`, one minute after creation, found `label-impact` at `2d4e43e`, evaluated it, and its `post` job raised `HTTP Error 404` on `/repos/agentkeel-studio/label-impact/installation` and exited, so that run posted no check on any repository. A repository created outside the installation stops the platform check for the whole organisation until it is added. The step belongs in agentkeel's quickstart §0, or the installation is set to all repositories, and the posting job should skip a repository it cannot mint for rather than exit; all three are agentkeel's, flagged here, not designed here. | Security |
| 9 | M00 PR 1's Unsure 4, `g-001`'s `owed: follow-rld`, was to be confirmed or changed before M01 copied the goldens (`milestones/M00/rulings/pr1.md`, "What this ruling does not settle"). It was not ruled. The golden moved as it stands, byte for byte, so the copy can be read against `m00`; a change is a Data Owner ruling in label-impact, and a retired id is never reused (quickstart §5). | Data Owner |
