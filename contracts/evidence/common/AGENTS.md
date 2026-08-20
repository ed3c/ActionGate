# AGENTS.md — Common C01 Receipt Gate

Scope: `contracts/evidence/common/**` for Issue #30.

This gate validates receipt shape and semantic consistency. It does not execute Worker commands, certify code correctness, admit a candidate, merge a PR or widen evidence beyond local deterministic canonicalization.

Fixture receipts require `--fixture-mode`. Live convergence consumes only `evidence_kind=LIVE` receipts bound to exact immutable heads and trees. Missing controls remain in the denominator. Language-specific parser limitations use `NOT_REPRESENTABLE_WITH_REASON`; they do not disappear.

Do not add a dependency silently. The semantic checker uses the Python standard library. JSON-Schema shape validation remains a separate runtime lane.
