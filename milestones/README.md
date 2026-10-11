# Ledger

One file. Rows are written on milestone open and the "Measured" cell is
filled at close. Each row is one claim, one planted failure, one measured
verdict (SPEC/00 §8). The claim text is SPEC/00 §8's, word for word.
Falsifiers, seeded commit and expected output are written when each
milestone opens, not before.

The adoption PR (#1, `milestones/adoption/rulings/adopt-spec00.md`) is
not counted against any milestone's cap of four (U9).

States: OPEN → GREEN | RED | UNMEASURED. GREEN: the CI-written verdict
in "Measured" equals the row's expected gate output, written at open.
RED: it does not. A milestone that closes without a measurement is RED
(M00 PR 4, Product).

## Rows

| # | M | Claim | Falsifiers | Seeded commit | Expected gate output | Measured | PRs used / cap | State |
|---|---|---|---|---|---|---|---|---|
| 0 | M00 | Goldens, traps and a naive baseline that fails them | F0.1 the baseline's answer to a `trap` golden equals that golden's `expected`: same `table_row`, same `clause_id`, every answer field equal. | `df860b7` on `m00-pr1`: `goldens/g-002.yaml` (trap) carries the baseline's own answer as its `expected`. | PR 2's gate runs the baseline over `goldens/` in CI, compares each observation with its golden and records the match per golden. On `df860b7`: RED, naming `g-002`. | RED, `traps_matched` `["g-002"]`, `written_by_ci` true, on `main` at `47788c0`: [run 38058191295](https://github.com/andaro74/pharmadelta/actions/runs/38058191295), artifact `m00-gate-47788c0a0b84854145e82e5fc70c9b22a87ab4ed`. Equals the expected output. | 4 / 4 | GREEN |
| 1 | M01 | The agent is created from the re-made template, seats filled, deployed | F1.1 `label-impact`'s first pull request is mergeable, or is merged and deployed, while one of its seven seats is not a login that administers the repository. | `eb9b201` on `first-agent` in `agentkeel-studio/label-impact`, [pull request #1](https://github.com/agentkeel-studio/label-impact/pull/1): `manifest.yaml` with `name: label-impact`, six seats `andaro74` and `rule-owner: null`; goldens `g-001` to `g-004`; `data/` as at `m00`; the tool, its schema and the prompt rewritten for labels. | agentkeel's `platform-check` on that pull request fails naming `rule-owner`. PR 2's reader in this repository reads that check, agentkeel's deploy runs and the registry for `label-impact`, in CI, and writes a `result.json` that is RED on F1.1 naming `rule-owner`. | RED on row 1 (falsifier F1.1), `finding` `control refused`, `seats_unassigned` `["rule-owner"]`, `written_by_ci` true, on PR 2 (#7) at merge ref `223de2d`: [run 38077129178](https://github.com/andaro74/pharmadelta/actions/runs/38077129178), artifact `m01-gate-223de2d13d518ce23327373cfff9775a49c24e0f`. The same reading on `main` at `8cdd851` after #7 merged: [run 38097865560](https://github.com/andaro74/pharmadelta/actions/runs/38097865560). Equals the expected output. | 4 / 4 | GREEN |
| 2 | M02 | Table and clauses are built from live FDA sources, versioned by effective date | F2.1 a clause in `data/clauses.json` carries an `effective_date` the eCFR versioner does not list for its section, or a `text` that is not the paragraph at that version; or a row in `data/table.json` carries a DailyMed-sourced field the SPL in force on its `label_read_on` does not hold. | `4379556` on `m02-pr1`: `data/clauses.json` carries `effective_date` on each of the nine clauses, the versioner's latest amendment date for the clause's section, read 2026-10-11; `314.98(a)` carries `2026-10-07`, the snapshot date (`ecfr_as_of`), which is not a version the versioner lists for 314.98. `data/table.json` is unchanged from `m00`. | PR 2's gate builds the clauses from the eCFR versioner and the rows from DailyMed, in CI, compares each with `data/`, and writes a `result.json` that is RED when any clause or row differs from the source at its version, naming each. On `4379556`: RED, `clauses_mismatched` `["314.98(a)"]`, `rows_mismatched` `[]`. The Measured cell cites the `main` run after PR 2 merges (M01 Unsure 23, ruled at M02 PR 1). | | 2 / 4 | OPEN |
| 3 | P | Per-agent guardrail rules and one approved public caller | | | | | measured in `andaro74/agentkeel`, not here | OPEN |
| 4 | M03 | A public API and the detail page call the deployed agent | | | | | 0 / 4 | OPEN |
| 5 | M04 | The side-by-side page runs the baseline live | | | | | 0 / 4 | OPEN |
| 6 | M05 | "Try to break it" is wired to agentkeel's planted failures | | | | | 0 / 4 | OPEN |
| 7 | M06 | Reviewer sign-off and a downloadable evidence package | | | | | 0 / 4 | OPEN |
| 8 | M07 | A second agent is created on a stopwatch | | | | | 0 / 4 | OPEN |

Row P is agentkeel's milestone. Its claim, falsifiers and measurement
live in `andaro74/agentkeel` under its own SPEC. This ledger records only
that it must close before M03 opens (SPEC/00 §8). M01 and M07 are built
in `agentkeel-studio`; their rows are measured here.
