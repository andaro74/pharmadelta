# SPEC/00 — Overview: governed media ingestion to agentic package curation

Status: DRAFT (rev 2, pre-push: inference through AgentCore Gateway) ·
Owner: Product seat · Rulings R1–R13 recorded at open ·
N (review SLA) = 24 hours (R10) · To be adopted by ADR-0001 with
amendment 1 (rulings applied at adoption) · Platform: agentkeel at a
pinned tag (§13); this repo is a tenant of it, not a fork.

## 1. What this is

A pipeline that takes media from contributors, analyses it with Amazon
Bedrock Data Automation (BDA), decides **what BDA said that can be
trusted**, indexes only that as fact in an Amazon Bedrock Knowledge
Base, and lets a curator assemble a versioned extras package from one
prompt through a Strands agent on AgentCore — with every hallucination
control proved by a seeded error the gate must catch.

BDA produces the outputs. This repo governs **what happens to them**:
which outputs are evidence-bearing and which are generated; which
deterministic rule, entailment check or confidence band decides an
output's fate; what a reviewer decides and how that decision changes
the golden set and the rulebook; and what the agent may state as fact.

One sentence for the README: *BDA describes the media; extrasforge
proves which descriptions could only have reached the knowledge base by
passing a rule a seat owns, and that an agent cannot state a generated
description as fact.*

## 2. What it is not

- Not a media platform. Ingest, analysis, triage, index, query, package.
  Delivery to retailers is out of scope and stays out.
- Not a BDA benchmark. BDA's accuracy is measured only to size the
  controls around it; the repo does not tune BDA.
- Not a governed-agent platform. That is agentkeel. This repo consumes
  its `GovernedAgent` construct, seat model, envelope schema and gates
  at a pinned tag and adds nothing to them. One exception, stated: the
  model path is AgentCore Gateway inference targets (§9.7), not
  agentkeel's LLM-gateway alias; agentkeel adopts the same at its own
  upgrade milestone, never retrofitted here.
- Not a review UI product. The review queue is a DynamoDB table and a
  CLI; the viewer is one static page. A prettier tool is a follow-on.
- Not a rights or legal system. Rights and embargo rules are seeded
  fixtures on a fictional slate.

## 3. Threats — and the milestone that answers each

| Threat | Looks like | Answered by |
|---|---|---|
| Generated description taken as fact | a scene summary names an actor not in the film; the agent recommends the wrong clip | M03, M04, M06 |
| Impossible output indexed | a timestamp past the asset's duration; overlapping scenes; a poster OCR that names another title | M04 |
| Wrong-title upload | a *Harbour Lights* clip lands in the *Stone Orchard* prefix and is indexed under it | M04, M07 |
| Spoiler or embargo leak | a pre-release asset's description reaches the index with plot terms | M04, M05 |
| Cross-title leakage at query | a user assigned one title retrieves another's assets | M06 |
| Miscalibrated confidence | 0.7 means 60% correct on one field and 95% on another; the band is wrong | M03, M05 |
| Reviewer rubber-stamp | 100% confirm at 4 seconds per item; silence becomes consent past SLA | M05 |
| Model or blueprint drift | a BDA project or agent model change lowers the catch rate and nothing goes RED | M03, M07 |
| Poisoned upload | a clip whose on-screen text instructs the agent or the judge | M04, M06 |
| Direct model call | an agent role with `bedrock:InvokeModel`; a call naming a model outside the mapping | M06, M07 |
| Unattributed spend | every call through the gateway is billed to its role; a user over budget keeps calling | M06 |
| The one-human problem | the owner approves their own change | R1 — no gate depends on a human |

## 4. Principles (each is a rule the repo enforces on itself)

P1–P11 are agentkeel's, unchanged (a claim needs a false state; seed
first, build second; measure by PR 2; one claim, one gate, one envelope;
instruments never read their own claim; baseline first; regression bar,
not perfection; only business artifacts move the gates; the owner is
subject to the rules; cap four, no spare; only CI-written envelopes are
evidence). Two are added here.

P12. **Deterministic before probabilistic.** Every check that can be
     made exact is a rule in `rules/`. A judge or a confidence band may
     only decide what no rule can. A PR that adds a judge check for
     something a rule could catch is returned.
P13. **Generated is never fact.** Every field indexed carries
     `provenance ∈ {extractive, referential, generated}` and
     `status ∈ {verified, unverified, quarantined}`. The agent's answer
     gate refuses to state an `unverified` or `generated` field as fact.
     A field with no provenance is a bug, not a style issue.

## 5. Seats

| Seat | Owns the truth about | Owned paths | May not |
|---|---|---|---|
| Product | what to build, when it's acceptable | `SPEC/**`, `milestones/**`, `CLAUDE.md`, `.claude/skills/**`, `docs/**`, `README.md`, `LICENSE`, `NOTICE` | define correctness; merge code |
| Rule Owner | what may be indexed and what the agent may state | `rules/**` (the rulebook, one YAML per rule with tests), `agents/*/rules/**`, guardrail id/version in manifest | edit goldens; move a band |
| Data Owner | what CORRECT means | `evals/goldens/**`, `data/**` (slate, title metadata, cast and character lists, spoiler terms, rights table, planted-error register), reviewer decisions that change a golden, corpus admission | weaken a golden to green a build |
| Tool Owner | tool and edge contracts | `tools/**`, `agents/*/tools/**` (three MCP servers' schemas), `may_call`, `may_be_called_by` | change a schema without a major bump |
| Threshold Owner | the bars, the bands and the model mapping | `thresholds.yaml` (triage bands per field, calibration method, catch-rate bar, cost cap, per-user budget), judge rubric, judge model id, agent model id + version + region, BDA project version pinned in manifest, `infra/gateway/inference-targets.yaml` (alias → provider model mapping) | move a band, a bar or a mapping without two keys |
| Security | what tooling and infra MAY DO | `.github/workflows/**`, `infra/**` (but for `infra/gateway/inference-targets.yaml`), KMS key policy, cosign identity, identity scoping (Cognito groups → title prefixes; KB metadata filter), gateway interceptors (`src/gateway/interceptors/**`), seats → groups in a manifest | define scope |
| Engineering | that it works | `src/**`, `scripts/**`, `tests/**`, `Makefile`, root config, `agents/<name>/**` but for the fields other seats own, `evals/history/**` (CI-written only), `evals/local/**` (gitignored, no gate) | self-approve any of the above |
| (the seat in its front matter) | its own routing | `.claude/agents/<name>.md` | rule; write to any seat-owned path |

Ownership notes:
- BDA blueprints (`agents/ingest/blueprints/*.json`) are split by field:
  enum and `unknown` handling is Rule Owner; which fields exist and
  which are `generated` is Data Owner; the project id and version is
  Threshold Owner. A diff names the seat of every field it changes.
- Reviewer decisions (`data/decisions/`) are written by the review CLI
  from the queue, never by hand. A decision that changes a golden is a
  Data Owner ruling; the CLI writes the ruling stub.
- Every file on `main` has a seat. A file no seat owns is deleted.

**Ruling R1 (one human).** Every seat is one person. No gate depends on
a human approval. Mechanical gates, exhaustively: `validate`,
`signature`, `ruling-cited`, `two-key`, `regression`, `cost-cap`,
`docs-current`, `cold-review-ruling` — all as agentkeel §5 defines them,
consumed at the pinned tag — plus one this repo adds from M04:
- `cost-cap` (this repo's reading) — from M06 reads the interceptor
  ledger (`spend` table, per identity, per model), not Bedrock per-call
  metrics: a call through an inference target is billed to the gateway
  role, so per-request attribution exists only where the request
  interceptor wrote it (§9.7). Before M06 it reads agentkeel's.
- `catch-rate` — RED when the planted-error catch rate on the fixture
  set drops below `thresholds.yaml: catch_rate_min`, or when any planted
  error that was ever caught is no longer caught (regression bar on
  plants, P7). Read on `scope: pipeline` results only; the naive control
  is reported, never gated.

### 5.1 Subagents and specialists (`.claude/agents/`)

Seven seat subagents, written at M00 PR 1, same names and duties as
agentkeel's (`product-spec-reviewer` first, run against this SPEC before
the rest of PR 1). Reports are drafts, never rulings.

**Specialists (called by a seat; never rule; added by need, R8)**

| Specialist | Called by | Added at | Does |
|---|---|---|---|
| `bda-output-reviewer` | Data Owner | M02 | reads a raw BDA output against the asset; drafts the extractive/generated split per field; proposes goldens; never labels a golden as passing |
| `rule-drafter` | Rule Owner | M04 | turns a reviewer decision with reason code into a candidate rule with its positive and negative test; the seat's PR carries it |
| `security-reviewer` | Security | M00 (seat subagent) | as agentkeel |
| `red-teamer` | Rule Owner | M06 | on-screen-text and transcript injections aimed at the agent and the judge; each with an expected block |
| `docs-writer` | Product | M03 | explainers in the plain register |

Reviewer agents run in CI as advisory checks (§9.5). They post
findings. They hold no key. This is P8 applied to people: a seat
decides; an agent reports.

## 6. Artifacts

- **Manifest** (`agents/search-media/manifest.yaml`, from M06):
  `model_alias` (never a provider model id), guardrail id + version
  (contextual grounding on), judge model id, seats → groups, `may_call`
  (three MCP servers), endpoint allowlist, ceilings, `platform_version`
  (agentkeel tag). **Inference-target config**
  (`infra/gateway/inference-targets.yaml`, Threshold Owner, from M06):
  the gateway's inference targets in Provider form — one entry per
  alias with provider, model id + version + region, guardrail id, and
  `weights` (PoC: a single 100% mapping; canary deferred). A swap is a
  diff to this file and nothing else. **Ingest manifest** (`agents/ingest/manifest.yaml`, from M01):
  BDA project id + version, blueprint ids + versions, output bucket,
  ledger table, KB id.
- **Job ledger** (DynamoDB from M01; `data/ledger/` fixtures at M00):
  one item per asset per run: `asset_id, title_id, run_id, state ∈
  {submitted, analysed, validated, indexed, quarantined, reviewed},
  bda_project_version, rule_results[], bands{}, decision_ref`.
- **Rulebook** (`rules/*.yaml`): `id` (immutable), `family ∈
  {schema, referential, temporal, cross_output, business}`, `field`,
  `severity ∈ {fail, warn}`, `owner`, `rationale`, `planted_error`
  (the register id it was written to catch), `tests` (positive and
  negative fixtures). A rule is retired, never renamed.
- **Planted-error register** (`data/plants/register.yaml`, Data
  Owner): `id` (`e-NNN`), `kind ∈ {wrong_person, invented_character,
  timestamp_past_duration, overlap, wrong_title_card, spoiler_term,
  wrong_language, runaway_summary, wrong_title_prefix, injection}`,
  `asset_id`, `field`, `truth`, `planted`, `catching_layer_expected ∈
  {rule, entailment, confidence, review}`, `added`, `retired`.
- **Golden** (`evals/goldens/v1/g-NNN.yaml`): `id` (immutable, R11),
  `kind ∈ {ingest, query, leak, guardrail, redteam}`, `asset_id` or
  `question`, `expected` (ingest: per-field `status` and `value`; query:
  `asset_ids[]`, `cited_timestamps[]`; leak: `BLOCKED`; guardrail:
  `BLOCKED|MASKED`; redteam: `BLOCKED`), `seat`, `added`, `retired`.
- **Envelope**: agentkeel's `verdict.schema.json` at the pinned tag,
  extended by ADR at M04 with `scope ∈ {control, pipeline, agent}`,
  `plants_expected`, `plants_fired`, `catch_rate`, `catch_by_layer{}`,
  `calibration{field: ece}`, and `checks` keyed by falsifier id.
- **Decision** (`data/decisions/d-NNNN.yaml`, written by the review
  CLI): `queue_item, asset_id, field, proposed, decision ∈ {confirm,
  correct, reject_rerun, escalate}, value, reason_code, reviewer_seat,
  ts, golden_change` (null or a golden id).
- **Ledger**, **feasibility note**, **ruling**, **ADR**: as agentkeel.

## 7. The claims

| # | Claim | M | State |
|---|---|---|---|
| 0 | Every later catch rate is a delta against a frozen naive ingest measured on the same fixtures | M00 | OPEN |
| 1 | Every upload reaches one terminal ledger state, exactly once, under a project-scoped identity | M01 | OPEN |
| 2 | Every BDA output type for every modality is on record, split into extractive and generated fields | M02 | OPEN |
| 3 | Confidence bands are calibrated per field on the golden set; a blueprint change that moves calibration goes RED | M03 | OPEN |
| 4 | Ten planted errors: the rulebook catches its share, the entailment check its share, nothing reaches the index unverified | M04 | OPEN |
| 5 | A reviewer decision changes the index, the golden set and the rulebook; a rubber-stamp and an aged item are both detected | M05 | OPEN |
| 6 | One prompt returns a cited package; a cross-title query returns nothing; a generated field is never stated as fact; no agent reaches a model except through the gateway | M06 | OPEN |
| 7 | A blueprint or model swap that lowers the catch rate goes RED before it indexes; a swap is a mapping diff, never a code or workflow edit; a wrong-title upload is caught by the title-card rule | M07 | OPEN |

States: OPEN → GREEN | RED | UNMEASURED | UNSCHEDULED (two-key) | RETIRED.
A milestone that closes without a measurement is RED.

## 8. Milestones

Cap four PRs each. PR 1 always: SPEC/NN, `milestones/MNN/feasibility.md`,
ledger row on open, seeded false state planted, explainer draft. Every PR
ends with a ruling file at `milestones/MNN/rulings/<slug>.md`; a PR
touching the milestone's build paths cites `SPEC/00-overview.md#8-MNN`.
Measurement lands by PR 2. Eight milestones, at most 32 PRs. **Cut
list for the interview deadline (R12): M00–M04 and M06 are the set;
M05 may close on the CLI alone; M07 may close as a written drill with
one measured swap.**

### M00 — Naive control and ledger
Build: `src/baseline/` — the naive pipeline as the control: takes a raw
BDA output fixture, writes every field to a flat JSON index with no
provenance, no rule, no band; answers a query golden by keyword match
over that index and returns the top asset with no citation. Frozen by
ADR-0002 at the close PR. Reads nothing from `rules/` or
`thresholds.yaml`. Model ids for every role (agent under test, swap
candidate, judge candidates) pinned by the Threshold Owner at the top of
`milestones/M00/README.md`; the naive control calls no model.
`scripts/seed_slate.py` writing `data/slate.json` (§9), `data/titles/`
(per-title metadata, cast, characters, runtimes, rights, embargo),
`data/spoiler_terms.json`. **BDA fixtures:** one real clip per modality
(video, audio, image, document) run through BDA by hand under the
developer's credentials, raw outputs committed under
`tests/fixtures/bda/` exactly as returned, with the request parameters
and the BDA project version in `tests/fixtures/bda/README.md`. Ten
planted errors (`e-001`…`e-010`, §9.4) applied to copies of those
fixtures by `scripts/plant_errors.py`, each its own commit, the register
naming the commit. Golden set v1: 20 goldens — 12 ingest (one per planted
error, two clean), 5 query, 3 leak. `verdict.schema.json` consumed from
agentkeel at the pinned tag; `verdict.build`, `verdict.gate` (with the
plant rule as one line at PR 2); the ledger; `replay_history`. `Makefile`
with all five targets: at PR 1 `evals-local` and `validate` run
(`validate` checks golden, rule and ruling front matter and that every
`planted_error` id in a rule exists in the register) and `evals`,
`plants`, `ledger` exit 1 with "not until M00 PR 2". The seven seat
subagents, `product-spec-reviewer` first. `cold-review-ruling` required
from PR 2 (R9). This SPEC/00 and R1–R12, recorded by ADR-0001. ADR-0002
(control frozen) at the close PR, at tag `m00`. Skills at the close PR.
Rulings cited: PR 1 cites `SPEC/00-overview.md#8-M00` for
`evals/goldens/`, `src/baseline/`, `scripts/`, `data/` and
`tests/fixtures/`, naming the seat per path in the PR body.
Seeded: the naive control indexes all ten planted errors as fact and
answers the query goldens from them; a run without a control card is
rejected by `verdict.build`.
Expected on the control: control card written; per ingest golden,
`indexed_as_fact` true for every planted field (10/10 plants pass through
— that is the number every later milestone is a delta against); query
goldens answered with `cites` false on all 5; leak goldens 0/3 BLOCKED
and `never_passed`, `plants_expected = 0` under the plant rule. Every
result is `scope: control`, so `regressed` is 0 by construction and
`checks.F0_2` and `checks.F0_3` decide the verdict.
Falsifiers: F0.2 an envelope validates without a control card ref. F0.3
a PR merges without a ruling file after PR 2.
Finding F0.1 (not a falsifier): a planted error that the naive control
happens not to index (a malformed fixture the flat writer drops). Record
it; do not fix the plant in this milestone.
Done when: `make evals` writes an envelope with the control card and the
row 0 measured value (`plants_through 10/10; cites 0/5; leak 0/3
never_passed`) in `milestones/README.md`.

### M01 — Ingest and ledger
Build: S3 prefix per title; Cognito groups → prefix policy (Security);
EventBridge → `start_analysis` Lambda → BDA async job → DynamoDB ledger
(`submitted`); completion → `record_analysis` Lambda → raw outputs to
the insights bucket → ledger (`analysed`). Idempotency key on
`asset_id + content_hash`. Ingest manifest with the BDA project pinned.
Runs on the four M00 fixture clips only. Adds `platform-architect`.
Seeded: the same clip uploaded twice; an upload from a group with no
prefix grant; a completion event for a job the ledger never saw.
Falsifiers: F1.1 a duplicate produces two runs. F1.2 the ungranted
upload lands. F1.3 the orphan completion writes a ledger item. F1.4 any
asset ends in a non-terminal state after N.

### M02 — Every modality on record
Build: the full stand-in library (§9.2) through BDA standard outputs
(video, audio, image, document) and the three custom blueprints
(`extra_asset`, `poster`, `script_scene`); `data/bda_coverage.yaml`
(Data Owner): every output type BDA returned, per modality, and each
field's `provenance`; the viewer (one static page from the insights
bucket: scenes and timestamps, transcript spans, OCR, bounding boxes,
diarization). Adds `bda-output-reviewer`.
Seeded: a modality with one output type deleted from the coverage file;
a field labelled `extractive` that BDA documents as generated.
Falsifiers: F2.1 `validate` passes with an output type on disk absent
from the coverage file. F2.2 a generated field carries `extractive`.
F2.3 the viewer shows a timestamp the output does not contain.

### M03 — Calibration
Build: golden set v2 — 50 hand-labelled assets (Data Owner, the human is
the SME; labels are the truth, BDA is the measured); per-field
reliability: predicted confidence against observed accuracy, expected
calibration error on the envelope; `thresholds.yaml` bands per field
set from the curves (Threshold Owner) with review capacity as a stated
input; entailment check (summary vs transcript + OCR) scored against the
labels. Adds `docs-writer`.
Seeded: a blueprint revision that raises a field's confidence without
raising its accuracy; a band set at 0.7 on a field whose curve says 0.85.
Falsifiers: F3.1 the revision is GREEN. F3.2 a band below its curve's
point passes `validate`. F3.3 the entailment check scores above its bar
on a summary the labels say is wrong.

### M04 — Rulebook and triage
Build: `rules/` with the five families (§9.3), tests per rule including
its `planted_error`; `validate` requires every rule to name a register
id and every register id to be named by a rule, an entailment case or a
review case; three-band triage in `src/triage/` (verified / queue /
quarantine, re-run with the strict blueprint); `catch-rate` gate; index
writer that refuses a field with no provenance. Adds `rule-drafter`.
Seeded: the ten planted errors from M00, now with the controls in the
tree so they are plants, not never-passed goldens; an eleventh with no
rule and no entailment case (`e-011`, must reach the queue, never the
index).
Falsifiers: F4.1 any planted error is indexed as `verified`. F4.2 the
gate is GREEN with `plants_fired < plants_expected`. F4.3 a rule with no
test merges. F4.4 `e-011` is indexed instead of queued. F4.5 a judge
check is added for something a rule in the tree already catches (P12).

### M05 — Review loop
Build: review queue (DynamoDB) and CLI (`ef review`): evidence display
(field, proposed value, anchored scene range, transcript span, reference
list), four decisions with reason codes; decisions written to
`data/decisions/`; corrections to KB, golden set and `rule-drafter`;
known-answer seeds in the queue; SLA escalation; reviewer accuracy and
confirm-rate on the envelope. May close on the CLI alone (R12).
Seeded: a reviewer that confirms 20 items in 60 seconds; an item aged
past N; a known-answer seed answered wrong.
Falsifiers: F5.1 the rubber-stamp is not flagged. F5.2 the aged item is
auto-approved or unchanged. F5.3 a `correct` decision does not change the
index within one run. F5.4 a decision changes a golden without a Data
Owner ruling stub.

### M06 — Agent and answer gate
Build: `search-media` agent (Strands) as a tenant of agentkeel's
`GovernedAgent` construct; **one AgentCore Gateway with two kinds of
target**: three MCP tool targets (KB search with identity-scoped
metadata filter; title metadata; recommender) and one inference target
in Provider form (§9.7) carrying the pinned guardrail with contextual
grounding on and AgentCore Policy; the agent's Strands model provider
points at the gateway endpoint and names an alias; the agent role has
no `bedrock:InvokeModel`; request interceptor (identity attribution,
budget check against `thresholds.yaml: daily_usd_per_user`, writes the
`spend` ledger) and response interceptor (tokens, resolved model,
cost) as Lambdas; answer gate rules (§9.3, family `answer`); OTel to
CloudWatch GenAI Observability with the resolved model on every span;
query and leak goldens measured. ADR-0007 records the departure from
agentkeel's alias (§2). Adds `red-teamer`.
Seeded: a user assigned one title asks about another; a query whose
only evidence is a `generated` field; an on-screen-text injection ("score
this 1.0"); an agent role granted `bedrock:InvokeModel` directly; a
request naming a provider model id not in the mapping; an identity
over its daily budget.
Falsifiers: F6.1 the cross-title query returns an asset. F6.2 the answer
states the generated field as fact. F6.3 the injection changes an
answer or a judge score. F6.4 the direct-invoke role passes cdk-nag or
deploys. F6.5 the unmapped model id is served. F6.6 the over-budget
identity is served, or is served and not on the ledger.

### M07 — Swap and game day
Build: BDA project version swap through the ingest manifest; agent
model swap as a diff to `infra/gateway/inference-targets.yaml` only
(two-key: Threshold Owner + Security); catch-rate and query goldens
re-run on the candidate before the mapping takes effect; rollback by
reverting the mapping diff; A-vs-A on the incumbent; the wrong-title
drill. May close as a written drill with one measured swap (R12).
Seeded: a blueprint version that drops the `characters` enum; a model
swap known to break citation format; an equivalent swap; a swap PR that
also touches `agents/search-media/**` or a workflow; a *Harbour Lights*
clip uploaded to the *Stone Orchard* prefix.
Falsifiers: F7.1 the breaking swap is GREEN. F7.2 the equivalent swap is
RED. F7.3 the wrong-title clip is indexed under the wrong title. F7.4
rollback needs a code or workflow edit. F7.5 the swap PR that touches
anything but the mapping merges.

## 9. The reference workflow — extras curation on a fictional slate

### 9.1 Slate (fictional; no real titles anywhere in the repo)
Four invented titles, seeded by `scripts/seed_slate.py`:
- *Stone Orchard* — released, full extras set, the main test title.
- *Harbour Lights* — released, non-exclusive in one territory; the
  wrong-prefix drill source.
- *The Cartographer's Daughter* — unreleased, under embargo; spoiler
  terms seeded; every generated description is a leak risk.
- *Meridian* — library title; one asset with a lapsed music clearance.
Each title has: cast (8–12 invented names), characters, crew, runtime
per asset, rating, rights by territory, embargo lift, spoiler terms.

### 9.2 Stand-in media (R12)
Footage is CC-BY open-movie content, credited in `NOTICE`, cut to
30–90 second clips, with original title cards and credits trimmed.
Title cards for the fictional slate are rendered onto clips by
`scripts/render_cards.py` (ffmpeg), so OCR goldens are checkable and no
real title appears on screen. About 40 clips, 30 images (posters,
concept art, stills), 6 documents (scripts, one-sheets, cast lists), 4
audio tracks (invented commentary, recorded by the developer). The
library is built at M02; M00 and M01 use four fixture clips.

### 9.3 Rulebook families (Rule Owner, M04; `answer` family at M06)
- `schema` — blueprint output validates; enums honoured; `unknown` not
  a placeholder string; summary length within bounds.
- `referential` — every person in `data/titles/<id>/cast.json`; every
  character in `characters.json`; title, year, rating match metadata.
- `temporal` — scene ranges within ffprobe duration; non-overlapping;
  ordered; coverage within tolerance; bounding boxes within frame.
- `cross_output` — OCR title card matches title; summary entities ⊆
  entity list; transcript language equals declared; runaway summary.
- `business` — embargoed title: no spoiler term in any generated field;
  rights: asset not tagged for a territory its row excludes; duplicate
  by perceptual hash.
- `answer` (M06) — every recommended `asset_id` exists; every cited
  timestamp exists in that asset; every named entity resolves; no asset
  outside the caller's title grant; no `generated` field stated as fact.

### 9.4 Planted-error register v1 (Data Owner, M00)
`e-001` wrong actor in a scene summary · `e-002` invented character ·
`e-003` scene end past duration · `e-004` overlapping scenes · `e-005`
poster OCR names another slate title · `e-006` spoiler term in an
embargoed title's description · `e-007` transcript language ≠ declared ·
`e-008` runaway 900-word summary · `e-009` audio speaker label not in
crew · `e-010` blueprint field filled with "N/A" where `unknown` is
required. Expected catching layer per plant is recorded at open; the
M04 measurement compares.

### 9.5 Reviewer agents in CI (advisory; from M04)
`security-lint` (diff to `rules/`, `infra/`, workflows against the
Security checklist), `rule-test-runner` (every rule has its tests and
its register id), `spoiler-term-scan` (any generated fixture or golden
against `data/spoiler_terms.json`). Findings are PR comments. None is a
required check; none holds a key.

### 9.6 Size and non-goals
Under 400 lines of agent code, one runtime agent, three tools, one
edge. No package assembler agent (named follow-on). No second reviewer
role. No canary routing (agentkeel §12). Bedrock spend under $60 for
BDA, under $40 for the agent and judge.

### 9.7 The model path (M06)
The agent never holds a model credential. Its Strands model provider
calls the AgentCore Gateway endpoint with the agent's workload identity
(AgentCore Identity) and a `model_alias`. The gateway's inference
target (Provider form, so the mapping is explicit config) resolves the
alias to a provider model, applies the pinned Bedrock Guardrail and
AgentCore Policy, and calls the provider with the gateway's own
credentials. Because the provider sees the gateway's role as the
caller, per-request attribution is not native: the request interceptor
writes identity, alias and resolved model to the `spend` ledger before
the call and refuses over-budget identities; the response interceptor
writes tokens and cost after. `cost-cap` reads that ledger. Tool calls
take the same gateway's MCP targets; the two paths share one endpoint
and one policy but are separate targets with separate seats
(Tool Owner for MCP schemas; Threshold Owner for the mapping; Security
for the interceptors). Canary weights are deferred (§12).

## 10. Documentation and recordings
As agentkeel §10: one explainer page and one ≤ 8-minute unedited video
per milestone; `docs/platform/controls.md` gains one row per control at
the milestone that measured it; `docs-current` is the one check. The
executive lane is three explainers: M02 (what BDA sees), M04 (what was
caught and by what), M06 (one prompt to a cited package, and the leak
that returned nothing).

## 11. Rulings recorded in this SPEC
- **R1–R11** — agentkeel's, adopted unchanged (§5 and agentkeel §11).
- **R10 (this repo's N)** — N is the review SLA, 24 hours. An item past
  N escalates; it never auto-approves.
- **R13 — one model path.** Every model call from every agent in this
  repo goes through the AgentCore Gateway inference target. An agent
  manifest carries a `model_alias`, never a provider model id; a
  provider model id appears in `infra/gateway/inference-targets.yaml`
  and nowhere else. cdk-nag and `validate` (from M06) enforce both.
- **R12 — fictional slate, stand-in footage, interview cut list.** No
  real title, cast, contract or studio workflow detail in the repo;
  footage is CC-BY open-movie content with title cards trimmed and
  fictional cards rendered on. The milestone set for the interview
  deadline is M00–M04 and M06; M05 may close on the CLI, M07 as a
  written drill with one measured swap. A milestone cut this way is
  closed GREEN only on what it measured, and its explainer says so.

## 12. Deferred (named so they are not assumed)
- Package assembler agent (rights quotas, territory packaging).
- Review UI beyond the CLI; second-reviewer separation of duties
  enforced by the queue (stated as a rule, enforced by R1's one human
  only as routing).
- KB multimodal parsing via BDA as an alternative ingest path (shown as
  a comparison in the M02 explainer, not built).
- Canary weights on the inference target (mapping carries `weights`;
  PoC is a single 100% entry); DSAR deletion; multi-region — agentkeel
  §12.
- Per-team budgets and a budget UI; the PoC enforces a per-identity
  daily cap in the request interceptor only.

## 13. Third-party tools and their single job
| Tool | Job | Not its job |
|---|---|---|
| agentkeel (pinned tag) | construct, seats, gates, envelope, LLM gateway alias | this repo's rules or goldens |
| Amazon Bedrock Data Automation | media analysis; blueprints | deciding what is fact |
| Bedrock Knowledge Bases | index and retrieval with metadata filters | storing unverified fields as fact |
| AgentCore Runtime, Identity | agent hosting, workload identity | model routing |
| AgentCore Gateway | MCP tool targets; inference target (single model endpoint, alias → provider mapping); guardrail and policy on every call | per-request cost attribution without interceptors; the eval gate |
| Gateway interceptors (Lambda) | identity attribution, budget refusal, spend ledger | model choice |
| Bedrock Guardrails | contextual grounding at the answer; denied topics | ingestion checks |
| ffprobe / ffmpeg | duration truth; card rendering | analysis |
| CloudWatch GenAI Observability + ADOT | traces and metrics | the verdict |
| GitHub Actions | gates, CI reviewer agents | policy source of truth |

## 14. Cost
BDA calls confined to the four M00 fixtures (by hand), M02's library
build (once), M03's golden labelling run (once) and M07's swap (once).
Model calls confined to `make evals` and M06. Target under $100 total
on top of agentkeel's own spend. From M06 the interceptor ledger is the
source for this number; the M06 explainer reports spend from it.

## 15. Done when
Rows 0–7 in `milestones/README.md` have a measured value; at least six
are GREEN; every RED or cut row carries a ruling file; every PR since M00
PR 1 has one; `docs-current` is green; the M04 explainer states the
catch rate by layer against the M00 control's 10/10 pass-through; the
M06 explainer states the leak result and that no agent role holds
`bedrock:InvokeModel`; and `git tag m06` exists on `main`.
