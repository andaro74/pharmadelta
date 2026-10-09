---
ruling: adopt-spec00
seat: Product
authorises:
  - SPEC/00-overview.md
  - CLAUDE.md
  - README.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - milestones/adoption/rulings/adopt-spec00.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
pr: https://github.com/andaro74/pharmadelta/pull/1
---

# Ruling: adopt SPEC/00

SPEC/00-overview.md is adopted as the authority of this repository, as
committed on the `adoption` branch. The ten rulings on its §12 are
recorded in `docs/adr/ADR-0001-spec00-adopted.md`, two of them open (U6,
U7) for M00 to close.

This PR carries its ruling in-PR. No check enforces a ruling file yet;
that arrives with the first gates. This PR is counted against no
milestone's cap of four (U9).
