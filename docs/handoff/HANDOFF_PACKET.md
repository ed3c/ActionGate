# Handoff Packet Contract

A stage handoff is executable technical state, not prose.

```yaml
schema: actiongate-handoff-packet/v1
repository: ed3c/ActionGate
issue: 0
stage: P0
atom: C00
base_ref: main
subject_sha: 0000000000000000000000000000000000000000
subject_tree: ABSENT
branch: example
pr: ABSENT
lease:
  paths: []
  resources: []
private_context:
  state: PRIVATE_CONTEXT_UNAVAILABLE
  private_urls_echoed: false
inputs:
  receipts: []
outputs:
  changed_paths: []
  artifacts: []
verification:
  commands: []
  receipt: ABSENT
  evidence_lane: cloud/static
  evidence_state: ABSENT
shadow:
  observer_kind: SAME_CONTEXT_READ_ONLY_SHADOW
  independence_claimed: false
  deltas: []
  dissent: []
blockers: []
next_entry_condition: exact condition
human_owned_operations: []
```

Rules:

- Exact SHA/tree and durable artifact locators are required when available.
- Private URLs, secrets, hidden reasoning and machine-local credentials are forbidden.
- A chat transcript or Issue status alone is not a verification receipt.
- The next stage may start only when its start edge is readable and leases are free; completion requires own-lane prerequisite receipts.