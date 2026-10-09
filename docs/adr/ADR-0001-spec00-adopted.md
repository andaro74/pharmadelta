---
adr: ADR-0001
title: SPEC/00 adopted; rulings U1–U10 recorded
status: Accepted
date: 2026-10-09
seat: Product
authorises:
  - Product        # §5 seat mapping, §6 agent name, §8 PR shape and cap, U8, U10
amendments: 0
---

# ADR-0001 — SPEC/00 adopted

## Context

SPEC/00-overview.md was drafted on 2026-10-09 from the handoff brief of
2026-10-08 and a read of `andaro74/agentkeel` at tag `m08`. Its §12 lists
ten items it could not settle and names the seat for each. One person,
Hector Flores, holds all seven seats on this project (agentkeel ruling
R1). He ruled on all ten on 2026-10-09. This ADR records the adoption of
SPEC/00 as the authority and the ten rulings, each under its seat.

## Decision

SPEC/00-overview.md is adopted as the authority for this repository, as
committed on the `adoption` branch. CLAUDE.md is the working summary;
where they disagree SPEC/00 wins and CLAUDE.md gets a pull request.

Rulings on SPEC/00 §12. Eight are closed. Two are open and name the
milestone that must close them.

| # | Seat | Ruling |
|---|---|---|
| U1 | Product | The seat mapping in §5 stands. Pharmacovigilance and Legal hold no seat. A page may show them as consulted, never as a signature. |
| U2 | Product | The first agent is named `label-impact`. |
| U3 | Data Owner, with Rule Owner | The buried adverse event is a `trap` golden. Its answer carries an escalation field and cites the 314.80 or 314.98 clause. It is measured at M01 without the guardrail. |
| U4 | Data Owner | The five to ten labels are chosen at M00 open. No Pfizer originator brand, checked per product. |
| U5 | Data Owner, Tool Owner | The row's fields and the answer's fields are fixed at M00 with the first goldens. |
| U6 | Data Owner | **OPEN.** The five citations in §10 were checked against Cornell LII only. The check against eCFR is owed, by hand, before M00 PR 1. M00 closes it. |
| U7 | Data Owner | **OPEN.** The paragraph for scenario 3 is not verified. It is checked at M00 before any golden cites it. M00 closes it. |
| U8 | Product | Accepted. `main` started at `77330e8` with GitHub's README, LICENSE and `.gitignore`. The adoption pull request is #1 and is the first ruling. |
| U9 | Product | Cap four pull requests per milestone: PR 1 plant, PR 2 measure, PR 3 repair, PR 4 close, as agentkeel. The adoption pull request counts against no cap. |
| U10 | Product | A trademark search is owed before any commercial use, not before the demo. |

U1 to U10 get no ruling files of their own. This ADR is their record. The
adoption itself is ruled in `milestones/adoption/rulings/adopt-spec00.md`.

## Consequences

- §5's mapping is what the pages show. Three functions are added
  (Labeling Operations, Platform Engineering, Engineering) and two are
  shown as consulted (Pharmacovigilance, Legal).
- The agent repository is `agentkeel-studio/label-impact`, created at
  M01, not before.
- Scenario 4 is measurable from M01 (§7). Scenarios 5 and 6 still wait
  for P.
- M00 PR 1 cannot open until U6 is closed. No M00 golden may cite
  scenario 3's paragraph until U7 is closed. Both closures are recorded
  in `milestones/M00/`.
- The ledger (`milestones/README.md`) carries nine rows, M00 to M07 and
  P, each with a cap of four, and the adoption pull request is counted
  against none of them.
- This ADR has used none of its two amendments.
