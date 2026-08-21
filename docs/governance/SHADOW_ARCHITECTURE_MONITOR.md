# Shadow Architecture Monitor

## Mode

Default: `MONITOR`.

The Builder may explore and implement reversible work. The Shadow Architect remains read-only, observes material design deltas, requests falsifiers, and blocks only unsafe or evidence-laundering transitions.

## Sync points

Run a Shadow checkpoint at:

```text
architecture choice
first vertical slice
persistence introduced
async/concurrency introduced
external integration introduced
first green
before PR/publication
CI/runtime failure with design impact
before physical/Human admission
```

## Delta ledger

| Field | Meaning |
|---|---|
| `delta_id` | stable identifier |
| `checkpoint` | sync point |
| `class` | assumption/state/authority/ownership/lifecycle/concurrency/resource/side-effect/failure/evidence |
| `became_possible` | newly reachable behavior |
| `invariant` | what must remain true |
| `falsifier` | cheapest test/probe that could prove it false |
| `evidence_required` | lane and exact subject |
| `intervention` | L0-L3 |
| `disposition` | terminal procedure disposition |

## Baseline delta set

| ID | Class | Risk | Required falsifier | Current state |
|---|---|---|---|---|
| `SH-001` | authority | planner accidentally treated as authorizer | direct protected-tool bypass test | `NOT_IMPLEMENTED` |
| `SH-002` | state | “stateless MCP” erases nonce/grant/device state | restart + replay test | `NOT_IMPLEMENTED` |
| `SH-003` | identity | signature not bound to exact canonical parameters/audience | parameter/audience mutation vectors | `NOT_IMPLEMENTED` |
| `SH-004` | concurrency | duplicate requests execute side effect twice | concurrent idempotency fault test | `NOT_IMPLEMENTED` |
| `SH-005` | lifecycle | key/challenge/grant invalidation states omitted | rotation/cancel/expiry tests | `NOT_IMPLEMENTED` |
| `SH-006` | evidence | emulator/static proof promoted to StrongBox/Secure Enclave fact | physical-device receipt gate | `NOT_EXERCISED` |
| `SH-007` | privacy | private CodexDoc URL/content leaks to public GitHub | full-tree/Issue/PR leak scan | `NOT_EXERCISED` |
| `SH-008` | rights | license inferred by reputation or latest branch | exact revision LICENSE/NOTICE read-back | `NOT_EXERCISED` |
| `SH-009` | source | PDF/article proposal promoted to measured fact | primary-source or reproducible probe | `NOT_EXERCISED` |
| `SH-010` | failure | crash after side effect creates unknown completion | reconciliation/fault-injection test | `NOT_IMPLEMENTED` |

## Baseline receipt

```yaml
subject: ed3c/ActionGate@bootstrap
observer_kind: SAME_CONTEXT_READ_ONLY_SHADOW
independence: NOT_CLAIMED
implementation_ownership: NONE
evidence_lane: cloud/static
highest_state: READ_ONLY_RECON
architecture_verdict: BLOCKED_BEFORE_IMPLEMENTATION_CLAIMS
```

This baseline proves only that the initial risks and obligations were recorded. It is not independent Shadow evidence and does not close any implementation or physical state.

## Escalation

A missing hard oracle escalates:

```text
existing harness
-> deterministic assertion
-> bounded runtime probe
-> trace/external observer
-> model judge only for non-hard scoring
-> exact-subject evidence
```

A model statement never substitutes for a hard assertion.