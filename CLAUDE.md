# CLAUDE.md — pharmadelta

A labeling rule changed; which of our labels does it touch, and what do
we owe? Every answer cites one row of the label table and one clause of
FDA regulation. The agent is a tenant of agentkeel. This repository holds
what surrounds it.

SPEC/00-overview.md is the authority. If this file, the README or a chat
summary disagrees with it, SPEC/00 wins and the other gets a PR.

## How a session starts

1. Read `milestones/README.md` (the ledger) and the open milestone's
   `milestones/MNN/README.md`.
2. State back, in two sentences: the claim, and the commit or input that
   makes it false. If you cannot, stop and say so. Do not touch code.
3. Say which PR of the milestone this session is (1–4) and what that PR
   is allowed to contain (below).
4. One milestone per session. A session that drifts to the next
   milestone ends.

## The PR shape (cap four, no spare; ADR-0001 U9)

- **PR 1 — plant.** The milestone's row opened in the ledger and in
  `milestones/MNN/README.md`, the false state committed. Nothing that
  makes it pass.
- **PR 2 — measure.** The gate that reads the plant. The plant must go
  RED here. This PR is the measurement; later PRs do not decide the row.
- **PR 3 — repair.** What the cold review of PR 2 found. If it found
  nothing, PR 3 is skipped and the milestone closes at PR 3.
- **PR 4 — close.** Ledger "Measured" cell, `git tag mNN`.
- A milestone may close in three PRs; never in five. A fifth PR is a RED
  close with the finding as the result. Do not propose a cap raise.
- The adoption PR (#1) counts against no cap.

Every PR ends with a ruling file at `milestones/MNN/rulings/<slug>.md`
(front matter: `ruling`, `seat`, `authorises`, `evidence`, `pr`). You
write the diff; you do not merge.

## Never (SPEC/00 §2, §4, §11)

- Never write a claim whose false state is not already in the repo (P1).
- Never build the code that catches a failure before the failure is
  committed (P2).
- Never put more than one claim, one planted failure or one measured
  verdict in a milestone (P3).
- Never treat a local run as evidence. Only CI-written results are (P4).
- Never improve `src/baseline/` after tag `m00`. It is the control (P5).
- Never let a golden state the fact its own row holds (P6).
- Never put a CFR or Federal Register citation in a golden, the table,
  the clauses or a page before it is checked against the source (P7).
- Never leave scripted content on a page unlabelled (P8).
- Never use the six words SPEC/00 §11 bans about a control that has not
  fired on its planted case. Write: *it produces the evidence a
  validation would need.*
- Never answer a treatment question. The agent assesses regulatory
  impact on labeling, nothing else.
- Never name a Pfizer brand or the brand name of any marketed product.
  The company and its portfolio are fictional and say so.
- Never show an answer on a page without its row and its clause.
- Never call the "ordinary assistant" a real run before M04. Before M04
  it is labelled an illustration.
- Never put a number on a page that is not a CI-written result with a
  link to it.
- Never show a function signing that has no seat behind it.

## Three repositories (SPEC/00 §3)

| Repository | Holds | Authority for |
|---|---|---|
| `andaro74/pharmadelta` (this one) | SPEC, ledger, the demo's golden set, the frozen baseline, ingestion, the public API and pages | what the demo claims and what was measured |
| `agentkeel-studio/label-impact` (created at M01, not before) | the agent: manifest, code, prompt, tools, table, clauses, goldens | the deployed agent and its own tests |
| `andaro74/agentkeel` | the platform: checks, signing, deploy, guardrail, registry, audit | everything a tenant cannot change |

## Platform changes

Per-agent guardrail rules, a public caller and anything else a tenant
cannot change are agentkeel features. They are built there, under its
own SPEC. This repository flags them in the PR body and in the ledger
(row P) and waits. It never designs them.

## Toolchain

Code arrives at M00, not before. It is Python 3.14, managed with `uv`:
`pyproject.toml` with `requires-python = ">=3.14"`, `uv.lock` and a
`.python-version` of `3.14`, matching agentkeel. None of those files
exist before M00 PR 1.

## Writing

Plain. Short sentences. Numbers over adjectives. Name the shortcoming.

## When unsure

Say so in the PR body under **Unsure**, name the seat whose ruling would
settle it, and stop. An unstated assumption that later proves wrong costs
a milestone; a stated one costs a sentence.
