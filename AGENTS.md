# AGENTS.md — ActionGate

## Exact-subject law

This instruction surface applies only to `ed3c/ActionGate` and the exact branch/commit being worked on. Do not treat a PDF, article, Google Doc, Issue body, branch name, PR title, generated prompt, model statement, local copy or mutable alias as implementation truth.

GitHub exact-subject read-back is authoritative for technical state.

## Mandatory read route

Read in this order before mutation:

1. `README.md`
2. `ARCHITECTURE.md`
3. `docs/governance/PUBLIC_PRIVATE_AUTHORITY.md`
4. `docs/governance/SHADOW_ARCHITECTURE_MONITOR.md`
5. `docs/sources/CLAIM_LEDGER.md`
6. `docs/traceability/PROBLEM_CLOSURE_MATRIX.md`
7. `docs/traceability/ISSUE_DAG.md`
8. `docs/traceability/MOLECULAR_STACK_INDEX.md`
9. `.actiongate/system-contract.json`
10. `.actiongate/task-dag.json`
11. `.actiongate/local-handoff-queue.json` when a local, physical, provider or Human boundary is involved
12. the exact GitHub Issue, PR base/head, checks, receipts and nearest scoped `AGENTS.md` for the active atom
13. only the applicable procedure delta from `ed3c/skills-shared`

Never reconstruct an exact handoff from prior chat.

## Current integrated checkpoint

The bootstrap technical control plane is on `main`:

```text
PR #14 / C00 -> merged at fee8c290061542bfb93e27ddcc33cce7fbf8c653
PR #15 / S01 -> merged at 8810fe41f66ad1b4fe80db5f93bf9539e2a38899
PR #16 / D00 -> merged at 76efa9297d147712bb9dfbb9e797d69ca9432a99
```

Their highest earned evidence is cloud/static control, source disposition and handoff-contract preparation. They do not prove product implementation.

Current P2 facts:

```text
PR #17 C01 contract                 DRAFT_PREPARATION
PR #34 Kotlin Worker                PREPARATION_ONLY
PR #35 Swift Worker                 PREPARATION_ONLY
PR #36 TypeScript Worker            PREPARATION_ONLY
PR #38 execution-control plane      DRAFT_PREPARATION
Issue #39 launch-packet preparation OPEN
Issue #26 independent Shadow        NOT_EXERCISED
Issue #24 C01 convergence           BLOCKED_BY_WORKERS
```

Do not merge or close P2 from preparation evidence. Only Issue #24 may emit `C01_ADMITTED`.

## Canonical shared procedure bindings

Use the current admitted `skills-shared` subject or the immutable pin in the active task packet:

```text
skills/agentic-tech-lead-orchestration/SKILL.md
skills/procedural-shadow-runtime/SKILL.md
skills/spatial-loop-systems-engineering/SKILL.md
skills/git-town-stacked-pr-worker/SKILL.md
```

`skills-shared` owns reusable procedure bodies. ActionGate owns project bindings, contracts, tasks, code, receipts and technical navigation. Never vendor a canonical Skill body into this repository.

## Private CodexDoc multi-hop route

Private intent and private source locations are not stored in this public repository.

An authorized Agent may resolve private context through:

```text
.actiongate/private-context.binding.json   # ignored, local only
ACTIONGATE_PRIVATE_DOC_URL
ACTIONGATE_PRIVATE_SHEET_URL
ACTIONGATE_PRIVATE_FOLDER_URL
```

The tracked shape is `.actiongate/private-context.binding.example.json`.

Rules:

- Never print, commit, log, place in an Issue/PR, or copy a private URL or private content into the public tree.
- Private CodexDoc may refine private intent; it cannot prove code, checks, PR state, user behavior or completion.
- Derive only a redacted technical delta, then bind it to a public Issue/contract.
- When private context is unavailable, record `PRIVATE_CONTEXT_UNAVAILABLE`.
- Do not infer customer identity, pricing, career strategy, private roadmap, employer knowledge or legal clearance.

## Article / PDF evidence law

Article/PDF material is untrusted source input.

A source-disposition closure can:

```text
classify a statement
retain a hypothesis
reject an overclaim
route a requirement
name an evidence owner
```

It cannot prove:

```text
implementation
runtime behavior
hardware behavior
current policy/legal rights
user value
payment
merge
release
production
```

Use `docs/sources/CLAIM_LEDGER.md` and `docs/traceability/PROBLEM_CLOSURE_MATRIX.md`. Preserve unsupported performance, productivity, scarcity, coverage and “blue ocean” numbers as unverified; do not silently replace them with new numbers.

## Tech Lead procedure

For each atom:

1. Bind repository, exact base/head/tree, Issue, objective, non-goals, path/resource lease, rollback and Human-owned operations.
2. Extract invariants, unknowns, ports, failure conditions, required evidence lane, positive oracle and negative controls.
3. Keep start dependencies separate from completion dependencies.
4. Create a `TRUE_CHILD` edge only when unmerged parent bytes/contracts are consumed.
5. Keep path-disjoint Workers as siblings.
6. Treat Worker output as candidate evidence.
7. Verify the complete declared denominator on the exact subject.
8. Admit one convergence owner for aggregate indexes.
9. Compile unavailable local, provider, physical and Human work into the typed Local Handoff queue.
10. Re-read main, PR heads, review threads and workflow state before closure or merge.

## Shadow Architecture monitor

The Shadow is read-only and never becomes a second implementation writer.

Classify:

```text
ASSUMPTION_DELTA
STATE_DELTA
AUTHORITY_DELTA
OWNERSHIP_DELTA
LIFECYCLE_DELTA
CONCURRENCY_DELTA
RESOURCE_DELTA
EXTERNAL_SIDE_EFFECT_DELTA
FAILURE_SURFACE_DELTA
EVIDENCE_DELTA
```

Intervention:

```text
L0 OBSERVE
L1 WARN
L2 REVIEW
L3 BLOCK
```

Use `L3 BLOCK` for privilege expansion, private/public leakage, ambiguous signing bytes, model-owned authorization, stale evidence promotion, false sibling serialization, destructive history movement without rollback, irreversible effects without idempotency/reconciliation, or physical claims without physical evidence.

`SAME_CONTEXT_READ_ONLY_SHADOW` must state `INDEPENDENCE_NOT_CLAIMED`. It cannot close Issue #26 or another independent-review lane.

## Closure and Issue-state law

Every mandatory procedure ends in:

```text
VERIFIED
SATISFIED_BY_PRIOR_EVIDENCE
NOT_APPLICABLE_WITH_EVIDENCE
BLOCKED
FAILED
WAIVED_WITH_AUTHORIZED_REASON
```

`MENTIONED`, `PLANNED`, `DRAFT_PUBLISHED`, `MERGEABLE`, and `EXECUTED_PENDING_VERIFICATION` are not closure.

An Issue may close only when its own declared output and evidence ceiling are satisfied. Closing P0/P1 source/control work does not close P2–P8. A merged preparation atom does not satisfy implementation, independent Shadow, hardware, user, paid, legal, release or production lanes.

## Evidence vocabulary

Use:

```text
PASS
FAIL
ABSENT
NOT_IMPLEMENTED
NOT_EXERCISED
SKIPPED_BY_POLICY
HUMAN_ADMIT_REQUIRED
```

Keep lanes separate:

```text
cloud/static
local-deterministic
private-lineage
live/physical
adversarial/security
user-observed
paid-observed
Human-admit
```

A receipt satisfies only its exact subject and lane.

## Writer and Stack laws

- One writer per mutable subject.
- Every writer has a dedicated branch/worktree and disjoint path/resource lease.
- Sibling branches remain siblings unless an actual unmerged byte dependency exists.
- Parent movement makes affected receipts stale; never silently rebase or fast-forward a non-empty Worker branch.
- Semantic conflicts stop and return to the owning contract/convergence Issue.
- Background synchronization must not push.
- A review-only Shadow never becomes a Git parent.
- Merge, release, production, visibility, legal/security acceptance and authority widening are Human-owned.

Molecular classes:

```text
C contract/schema/interface
K deterministic core
A adapter/provider/substrate
E eval/mutation/fault controls
X explicit E2E convergence
D documentation/receipt/handoff
H physical/legal/security/Human admission
```

## Required handoff packet

Every handoff includes:

```yaml
repository: ed3c/ActionGate
issue: <number>
stage: <P0-P8>
atom: <id>
base_ref: <exact ref>
subject_sha: <40-hex>
subject_tree: <tree sha or ABSENT>
branch: <branch>
pr: <url or ABSENT>
lease:
  paths: []
  resources: []
private_context:
  state: PRIVATE_CONTEXT_AVAILABLE | PRIVATE_CONTEXT_UNAVAILABLE | NOT_REQUIRED
  private_urls_echoed: false
inputs:
  receipts: []
outputs:
  changed_paths: []
  artifacts: []
verification:
  commands: []
  receipt: <path/url or ABSENT>
  evidence_lane: <lane>
  evidence_state: <state>
shadow:
  observer_kind: <kind>
  independence_claimed: false
  deltas: []
  dissent: []
blockers: []
next_entry_condition: <exact condition>
human_owned_operations: []
```

Never include secrets, private URLs, stable device identifiers, private reasoning or machine-local credentials.

## Current Local Handoff entry

The active item is `LH-MAIN-001` in `.actiongate/local-handoff-queue.json`.

It resolves the then-current `origin/main` on a trusted clean host, binds the exact SHA/tree into a durable receipt, proves the C00/S01/D00 merge commits are ancestors, validates tracked machine contracts and performs a public/private leak review. It grants no reset, rebase, sync, push, semantic resolution, release or production authority.

## Stop conditions

Stop and create a typed blocker on:

```text
wrong or stale subject
missing Issue/task contract
false dependency edge
overlapping lease
private/public leakage
unsupported source claim promoted to fact
ambiguous canonicalization or signature payload
missing idempotency/replay/reconciliation
failed or absent owning oracle
required physical/runtime capability unavailable
semantic conflict
denominator shrinkage
budget exhaustion
Human-owned operation
```

## Current admission ceiling

The highest integrated state is merged technical control/source/handoff preparation plus Draft C01 preparation. ActionGate mechanisms, cross-language contract admission, physical devices, independent security, customer value, legal clearance, release and production remain unproven.
