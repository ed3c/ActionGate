# AGENTS.md — ActionGate

## Exact subject

This instruction surface applies only to `ed3c/ActionGate` and the exact branch/commit being worked on. Do not treat another repository, a local copy, a PDF, a Google Doc, an Issue description, or a model statement as implementation truth for this repository.

## Mandatory read route

Read in this order before mutation:

1. `README.md`
2. `ARCHITECTURE.md`
3. `docs/governance/PUBLIC_PRIVATE_AUTHORITY.md`
4. `docs/governance/SHADOW_ARCHITECTURE_MONITOR.md`
5. `docs/traceability/ISSUE_DAG.md`
6. `docs/traceability/MOLECULAR_STACK_INDEX.md`
7. `.actiongate/system-contract.json`
8. `.actiongate/task-dag.json`
9. the exact GitHub Issue and parent PR/branch for the active atom
10. only the applicable canonical procedures in `ed3c/skills-shared`

Do not load every Skill body. Compute the applicable procedure delta.

## Canonical shared procedure bindings

Resolve from the current default branch of `ed3c/skills-shared`, or from a version pinned by the active task packet:

```text
skills/agentic-tech-lead-orchestration/SKILL.md
skills/procedural-shadow-runtime/SKILL.md
skills/spatial-loop-systems-engineering/SKILL.md
skills/git-town-stacked-pr-worker/SKILL.md
```

`skills-shared` owns reusable procedure bodies. ActionGate owns only project bindings, contracts, tasks, code, receipts, and technical navigation. Do not vendor or fork canonical Skill bodies into this repository.

## Private CodexDoc multi-hop route

Private intent and private source URLs are not stored in this public repository.

An authorized Agent may resolve private context through either:

```text
.actiongate/private-context.binding.json   # ignored, local only
ACTIONGATE_PRIVATE_DOC_URL                 # environment / connected source
ACTIONGATE_PRIVATE_SHEET_URL
ACTIONGATE_PRIVATE_FOLDER_URL
```

The tracked shape is `.actiongate/private-context.binding.example.json`.

Rules:

- Never print, commit, log, place in an Issue/PR, or copy a private URL or private content into the public tree.
- Private CodexDoc may refine private intent and strategic constraints; it cannot prove code, tests, PR state, or completion.
- GitHub exact-subject read-back wins for technical implementation state.
- When private context is unavailable, record `PRIVATE_CONTEXT_UNAVAILABLE`; continue only with public technical work whose acceptance criteria are complete.
- Do not infer business strategy, customer identity, employer-confidential knowledge, legal clearance, or roadmap from public technical files.

## Public-only content law

Public repository text must be technical. Exclude:

```text
business strategy
pricing or go-to-market material
career/job-search material
customer or design-partner identity
private roadmap or prioritization rationale
private source URLs
employer-confidential architecture/code/know-how
unsupported market or productivity claims
```

Allowed public material includes technical requirements, protocols, schemas, threat models, implementation decisions, tests, evidence states, rights metadata, dependency constraints, and reproducible technical results.

## Tech Lead procedure

For each active atom:

1. Bind exact repository, branch/head, Issue, objective, non-goals, path/resource lease, and Human-owned operations.
2. Extract invariants, unknowns, interfaces, failure conditions, required evidence lane, negative controls, and rollback.
3. Create dependency edges only when a child consumes unmerged parent contract/bytes/state.
4. Admit parallel workers only with disjoint leases.
5. Treat worker output as candidate evidence.
6. Verify on the exact subject with independent assertions.
7. Converge aggregate indexes through exactly one owner.
8. Compile unresolved physical/local/Human work into a typed Local Handoff Execution Queue.

## Shadow Architecture monitor

The Shadow is read-only and never becomes a second implementation writer.

At every material checkpoint, classify deltas:

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

Intervention levels:

```text
L0 OBSERVE
L1 WARN
L2 REVIEW
L3 BLOCK
```

Use `L3 BLOCK` for privilege expansion, irreversible side effects without idempotency/reconciliation, private/public leakage, ambiguous action signing, model-owned authorization, stale evidence promotion, destructive migration without rollback, or physical claims without physical evidence.

Every applicable mandatory procedure ends in one terminal disposition:

```text
VERIFIED
SATISFIED_BY_PRIOR_EVIDENCE
NOT_APPLICABLE_WITH_EVIDENCE
BLOCKED
FAILED
WAIVED_WITH_AUTHORIZED_REASON
```

`MENTIONED`, `PLANNED`, and `EXECUTED_PENDING_VERIFICATION` do not close work.

## Evidence vocabulary

Use only:

```text
PASS
FAIL
ABSENT
NOT_IMPLEMENTED
NOT_EXERCISED
SKIPPED_BY_POLICY
HUMAN_ADMIT_REQUIRED
```

Keep evidence lanes separate:

```text
cloud/static
local-deterministic
private-lineage
live/physical
adversarial/security
Human-admit
```

A receipt satisfies only its own exact subject and lane.

## Writer and Stack laws

- One writer per active mutation subject.
- Every writer has a dedicated branch/worktree and disjoint path/resource lease.
- Sibling adapters remain siblings unless they consume unmerged parent bytes/contracts.
- Sync, rebase, branch movement, or conflict resolution invalidates stale exact-head receipts.
- Semantic conflicts stop; never auto-resolve them.
- Background synchronization must not push.
- Merge, release, production promotion, repository visibility, and authority widening are Human-owned.

Molecular atom classes:

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

Every stage/atom handoff must include:

```yaml
repository: ed3c/ActionGate
issue: <number>
stage: <P0-P8>
atom: <C/K/A/E/X/D/H id>
base_ref: <exact ref>
subject_sha: <40-hex>
subject_tree: <tree sha if available>
branch: <branch>
pr: <url or ABSENT>
lease:
  paths: []
  resources: []
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
  deltas: []
  dissent: []
blockers: []
next_entry_condition: <exact condition>
human_owned_operations: []
```

Do not include secrets, private URLs, hidden reasoning, or machine-local credentials.

## Stop conditions

Stop and issue a typed blocker on:

```text
wrong or stale subject
missing exact Issue/task contract
false dependency edge
overlapping lease
private/public leakage
unsupported external claim promoted to fact
ambiguous canonicalization or signature payload
missing idempotency/replay/reconciliation for protected side effect
failed or absent owning oracle
required physical capability unavailable
semantic conflict
budget exhaustion
Human-owned operation
```

## Current admission ceiling

At repository bootstrap, the maximum admissible state is documentation/schema preparation. Product implementation, physical-device behavior, independent security acceptance, customer value, release, and production remain unproven.