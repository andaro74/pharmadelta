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
| PRs used / cap | 1 / 4 |
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
  writes a `result.json` with a verdict on F1.1 only: RED when the pull
  request is mergeable or merged while a seat is unassigned, GREEN when
  the check refused it naming the seat and nothing merged or deployed.
  The verdict names the seat. `written_by_ci` and the run URL as M00's.
- What token the reader needs, and whether it needs one (Unsure 3).
- Whether the registry is read through AWS or through Grafana panel 1,
  and with what credential (Unsure 3).

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
