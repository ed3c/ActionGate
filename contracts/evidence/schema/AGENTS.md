# AGENTS.md — C01 Schema Evidence

Scope: `contracts/evidence/schema/**` for Issue #23.

This lane may read but never edit `contracts/v1/**`. It validates JSON Schema shape behavior against exact immutable C01 blobs. Semantic freshness, canonicalization, signature verification, authorization, replay, hardware and integration remain outside this lane.

Required output is an exact-subject receipt. A validator package is runtime evidence, not an admitted product dependency. Record version, license evidence and license digest. Do not download or install a replacement silently.
