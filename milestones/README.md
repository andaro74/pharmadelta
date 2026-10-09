# Ledger

One file. Rows are written on milestone open and the "Measured" cell is
filled at close. Each row is one claim, one planted failure, one measured
verdict (SPEC/00 §8). The claim text is SPEC/00 §8's, word for word.
Falsifiers, seeded commit and expected output are written when each
milestone opens, not before.

The adoption PR (#1, `milestones/adoption/rulings/adopt-spec00.md`) is
not counted against any milestone's cap of four (U9).

States: OPEN → GREEN | RED | UNMEASURED. A milestone that closes without
a measurement is RED.

## Rows

| # | M | Claim | Falsifiers | Seeded commit | Expected gate output | Measured | PRs used / cap | State |
|---|---|---|---|---|---|---|---|---|
| 0 | M00 | Goldens, traps and a naive baseline that fails them | | | | | 0 / 4 | OPEN |
| 1 | M01 | The agent is created from the re-made template, seats filled, deployed | | | | | 0 / 4 | OPEN |
| 2 | M02 | Table and clauses are built from live FDA sources, versioned by effective date | | | | | 0 / 4 | OPEN |
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
