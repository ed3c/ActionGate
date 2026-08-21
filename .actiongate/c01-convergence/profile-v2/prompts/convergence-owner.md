# Zero-context prompt — Issue #24 C01 convergence owner

ROLE: C01 semantic convergence owner.

Repository: ed3c/ActionGate.
Read root AGENTS.md, Issue #24, Issue #26, Issue #62, PR #61, and `.actiongate/c01-convergence/profile-v2/AGENTS.md` before acting.

Exact control epoch:

```text
PR #61 head/tree  2998b0a93d23ddfca0934250d82bdbd892f2c84b / e535e6fa031c84697d9b0b5cb96ee90a64286a08
contract          b63589e5a16e82fda1a9554227f2ebbb55398c8a
common evidence   9f41038240837ea2dd9dcdb9befd13e6ba81a78e
Kotlin            cf589a0990aaaa6422be9c649b52b44230d570f6 / 10a35f943aaee0b0035132100357a1adbacff7e1
Swift             039827061f54aa72e2b81365a4c904d25833f83e / 015cc3123b3b09ea0c087028aaea2ee052c51508
TypeScript        3ed9f0307df0937028bbf52fe8fbd2a6621acafe / 17532a35f42b07e350e7785a7be11038c9cf1ba0
```

INPUT: one external Issue #26 receipt conforming to `actiongate-c01-independent-review-receipt/v2`.

Procedure:

1. Confirm the receipt came from a separate read-only reviewer/session that did not build or repair the audited subjects or dispatch.
2. Re-read the current PR/Issue subjects. If any subject moved, emit `HOLD` and require rebind/review.
3. Run `check_convergence.py --review-receipt <receipt> --control-subject <exact #62 head> --emit-candidate <candidate.json>`.
4. Verify all 33 required falsifiers exist exactly once. `ELIGIBLE_FOR_C01_CONVERGENCE` requires 33/33 PASS.
5. Compare the three Worker exact heads/trees and contract/common evidence; no cherry-picking or denominator shrinkage.
6. Emit only `C01_ADMITTED`, `HOLD`, or `REJECT` on Issue #24 with the exact receipt digest and control subject.
7. `C01_ADMITTED` makes K01 completion *eligible*. It does not automatically start K01, merge any PR, prove mobile/MCP/security truth, or authorize release.
8. Preserve all dissent and evidence ceiling.

STOP on private context, stale subject, semantic conflict, incomplete independent receipt, false reviewer independence, or authority widening.
