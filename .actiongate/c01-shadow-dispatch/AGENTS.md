# AGENTS.md — C01 Independent Shadow Dispatch

Scope: `.actiongate/c01-shadow-dispatch/**` for Issue #58.

## Mandatory read route

1. root `AGENTS.md`
2. Issue #58
3. Issue #26 and all current comments
4. Issue #24 and all current comments
5. PR #41 exact base `98c9545c0dd2bbfdabdaf27c8a992822a78b3840`
6. C01 contract `b63589e5a16e82fda1a9554227f2ebbb55398c8a`
7. execution-control subject `9f41038240837ea2dd9dcdb9befd13e6ba81a78e`
8. Draft PRs #34/#35/#36 exact current heads
9. `dispatch-registry.json`
10. applicable prompt or receipt contract

## Authority

This atom is a **dispatch compiler and verifier**. It may bind immutable public subjects, compile zero-placeholder read-only prompts, validate packet consistency, and record same-context Shadow findings.

It may not implement or repair the audited language subjects, act as the independent reviewer, emit an Issue #26 verdict, resolve semantic conflict, admit C01, start K01, merge, release, or claim hardware/MCP/security/legal truth.

## Hard laws

- `SAME_CONTEXT_READ_ONLY_SHADOW` is not independent.
- The Builder or any context that implemented/repaired the audited subjects cannot satisfy Issue #26.
- Mutable branch names are navigation only; exact commits, trees and blobs are evidence.
- The three language branches remain path-disjoint siblings.
- Missing falsifiers remain in the denominator.
- A dispatch packet or hosted checker PASS is not an independent review receipt.
- A valid Issue #26 receipt is not `C01_ADMITTED`; only Issue #24 may emit that verdict.
- No private URL, employer/customer detail, credential, stable device identifier or private reasoning.
- No writes outside this directory and the dedicated workflow path.

## Shadow blockers

```text
STALE_WORKER_HEAD_OR_TREE
RECEIPT_NOT_SUCCESSOR_BOUND
RECEIPT_OR_SHADOW_BLOB_DRIFT
WORKER_LEASE_OVERLAP
FALSE_INTER_WORKER_PARENT
DENOMINATOR_SHRINKAGE
REQUIRED_FALSIFIER_OMITTED
SAME_CONTEXT_PROMOTED_TO_INDEPENDENT
BUILDER_LISTED_AS_INDEPENDENT_REVIEWER
PRIVATE_ROUTE_OR_SECRET_IN_PUBLIC_PACKET
INDEPENDENT_PACKET_PROMOTED_TO_C01_ADMISSION
AUTOMATIC_MERGE_RELEASE_OR_K01_START
```

## Exit

The maximum terminal is `C01_INDEPENDENT_SHADOW_DISPATCH_READY_FOR_EXTERNAL_REVIEW`.
