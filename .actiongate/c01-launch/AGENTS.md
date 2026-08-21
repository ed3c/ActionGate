# AGENTS.md — C01 Worker Launch Preparation

Scope: `.actiongate/c01-launch/**` only.

## Read order

1. root `AGENTS.md`
2. `contracts/AGENTS.md`
3. frozen C01 `contracts/v1/PROFILE.md`, `DECISIONS.md`, schema and vectors
4. PR #38 exact execution-control subject
5. Issue #39
6. this file
7. `launch-registry.json`
8. the selected compiled prompt

## Authority

This atom compiles routing and launch prerequisites. It owns no language implementation, contract semantics, independent review verdict, convergence decision, K01 code, merge or release.

The current conversation is not eligible to act as a clean-room implementation Session because it contains private context. It may prepare public-safe packets only.

## Hard laws

- Launch packet != launched Session.
- Current-host runtime evidence is non-transferable.
- Human clean-room declarations may not be fabricated or inferred.
- Legal clearance is never produced by this checker.
- Kotlin, Swift and TypeScript remain sibling branches.
- Read PR #38 receipt contracts through an exact read-only sidecar/fetch; do not cherry-pick them into Worker branches.
- No unresolved placeholders.
- No private Google URLs, credentials, employer details or hidden reasoning.
- No source mutation outside this directory.
- Same-context Shadow does not satisfy Issue #26.
- Merge, release, security/legal acceptance and production remain Human-owned.

## Exit

The atom may publish `C01_WORKER_SESSION_LAUNCH_PACKETS_READY`. It must preserve all implementation and live lanes as not launched/not exercised.
