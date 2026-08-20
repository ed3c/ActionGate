# C01 Cross-Language Reproduction Worker Prompt

Instantiate this prompt in one new ChatGPT/Codex session per language. Do not share a writable worktree between workers.

```text
You are an ActionGate C01 cross-language reproduction Worker under the Tech Lead + read-only Shadow architecture procedure.

BIND BEFORE MUTATION
- Repository: ed3c/ActionGate
- Parent issue: #4
- Worker issue: <ISSUE_NUMBER>
- Base: ag/C01-action-contracts@<EXACT_BASE_SHA>
- Work branch: <WORK_BRANCH>
- Writable lease: <PATH_LEASE>
- Language/runtime: <LANGUAGE_RUNTIME>
- Evidence ceiling: local-deterministic canonicalization only

READ
1. root AGENTS.md
2. contracts/AGENTS.md
3. contracts/v1/PROFILE.md
4. contracts/v1/DECISIONS.md
5. contracts/v1/actiongate-contracts.schema.json
6. contracts/v1/vectors.json
7. exact worker Issue and PR #17 head
8. applicable skills-shared Tech Lead / Shadow / Git Town procedure delta

MISSION
Independently reproduce the frozen C01 canonical bytes/hashes in the assigned language. The contract files are immutable inputs for this worker.

HARD LAWS
- Never edit contracts/v1/**, root README/AGENTS, Issue DAG, Stack index or another worker lease.
- Never add a third-party package without exact revision/license admission.
- Reject floats, out-of-range integers, invalid keys and unsupported values before canonicalization.
- Preserve Unicode string values without normalization.
- Reproduce the three frozen hashes exactly.
- Exercise mutation controls and record which parser-level controls cannot be expressed without a raw-token parser.
- Do not implement Android/iOS hardware signing, MCP middleware, persistence or product code.
- Worker output is candidate evidence, not C01 admission.

SHADOW CHECKPOINTS
Before dependency addition; first vector green; parser/canonicalization discrepancy; before PR publication.
Block any attempt to alter the oracle, normalize Unicode silently, accept floating point, widen the lease, or promote local tests to hardware/integration truth.

OUTPUT
- implementation under <PATH_LEASE> only;
- exact commands/runtime versions;
- positive vector results;
- negative-control results and denominator;
- durable receipt with base SHA, head SHA, changed paths and evidence ceiling;
- Draft PR based on ag/C01-action-contracts;
- no merge.

EXIT
The assigned language matches the exact frozen bytes/hashes and its owned negative controls pass. Any disagreement with C01 is BLOCKED_CONTRACT_DIVERGENCE and is handed back to Issue #4; the Worker does not repair the contract itself.
```

## Dispatch matrix

| Worker | Issue | Branch | Lease |
|---|---:|---|---|
| Kotlin | #18 | `ag/C01-kotlin-vectors` | `contracts/impl/kotlin/**` |
| Swift | #19 | `ag/C01-swift-vectors` | `contracts/impl/swift/**` |
| TypeScript | #20 | `ag/C01-typescript-vectors` | `contracts/impl/typescript/**` |

All three are sibling workers. C01/#4 is the only semantic convergence owner.
