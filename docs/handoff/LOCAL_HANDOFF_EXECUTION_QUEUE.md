# Local Handoff Execution Queue

The machine authority is `.actiongate/local-handoff-queue.json`. This document is its human-readable projection and cannot widen it.

Exactly one item is `ACTIVE`. A valid receipt may make several sibling items eligible, but the controller activates at most one item whose own entry conditions are satisfied. Queue order does not create Git ancestry and no item auto-executes.

## Execution boundary

Use a dedicated, empty, personal clean-room directory. Do not open employer repositories, confidential documents, private protocols, customer data or company credentials in an implementation Session.

No queue item grants `reset`, rebase, sync, push, merge, branch deletion, semantic-conflict resolution, dependency installation, SDK-license acceptance, release, production deployment or rollback unless its own Human authority explicitly admits that operation.

A prompt or launch packet remains `LAUNCH_REQUESTED`; it is not `SESSION_OBSERVED`.

## `LH-MAIN-001` — merged-main exact readback

**State:** `ACTIVE`

**Entry:** trusted clean host with Git, Python 3 and GitHub network; dedicated empty directory; no private/employer source in the same context.

The queue resolves `origin/main` only at execution time, then stores the exact SHA and tree in the receipt. Mutable `main` by itself is never completion evidence.

Required ancestor receipts:

```text
fee8c290061542bfb93e27ddcc33cce7fbf8c653  # C00 / PR #14
8810fe41f66ad1b4fe80db5f93bf9539e2a38899  # S01 / PR #15
76efa9297d147712bb9dfbb9e797d69ca9432a99  # D00 / PR #16
```

Commands:

```bash
git clone https://github.com/ed3c/ActionGate.git ActionGate
git -C ActionGate fetch origin --prune
git -C ActionGate switch --detach origin/main
git -C ActionGate rev-parse HEAD
git -C ActionGate rev-parse HEAD^{tree}
git -C ActionGate merge-base --is-ancestor fee8c290061542bfb93e27ddcc33cce7fbf8c653 HEAD
git -C ActionGate merge-base --is-ancestor 8810fe41f66ad1b4fe80db5f93bf9539e2a38899 HEAD
git -C ActionGate merge-base --is-ancestor 76efa9297d147712bb9dfbb9e797d69ca9432a99 HEAD
git -C ActionGate diff --check
python3 -m json.tool ActionGate/.actiongate/system-contract.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/task-dag.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/local-handoff-queue.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/source-claims.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/technology-candidates.json >/dev/null
```

Receipt:

```text
ActionGate/.actiongate/receipts/local/LH-MAIN-001.json
```

It binds the resolved SHA/tree, ancestor checks, JSON/Markdown presence, public/private leak review, clean-room separation and exact command exits. It does not record private locator values.

**Exit:** exact current main readback passes.

**Next candidates:** `LH-STACK-002` or `C01-SESSION-003`; at most one may become active.

## `LH-STACK-002` — Git Town and C01 branch graph

**State:** `BLOCKED_BY_PREDECESSOR`

**Entry:** `LH-MAIN-001` valid and the open C01 heads still match the Molecular Stack index, or an explicit state-delta packet supersedes them.

Checks:

```bash
git -C ActionGate fetch origin --prune
git -C ActionGate town --version
git -C ActionGate merge-base --is-ancestor 6cd18694878e6db3ee65034d8e86fe990ade02c0 origin/ag/C01-action-contracts
git -C ActionGate merge-base --is-ancestor origin/ag/C01-action-contracts origin/ag/C01-kotlin-vectors
git -C ActionGate merge-base --is-ancestor origin/ag/C01-action-contracts origin/ag/C01-swift-vectors
git -C ActionGate merge-base --is-ancestor origin/ag/C01-action-contracts origin/ag/C01-typescript-vectors
git -C ActionGate merge-base --is-ancestor origin/ag/C01-action-contracts origin/ag/C01-execution-preflight
```

`git town --version` may end as `BLOCKED_ABSENT_EXECUTABLE`. Tool absence does not invalidate the raw Git ancestry observations and does not authorize installation.

No sync, rebase, push, reset or merge runs.

## `C01-SESSION-003` — clean-room language Worker Session

**State:** `BLOCKED_BY_LAUNCH_PACKETS_AND_HUMAN_CLEANROOM`

**Entry:**

```text
Issue #39 publishes an exact zero-placeholder launch packet
+ selected PR #34/#35/#36 head and lease are current
+ the new Session re-probes its own runtime
+ Human clean-room declaration is present
```

The current private-context conversation cannot satisfy this gate. Start a separate implementation context containing public repository inputs only.

The Session may implement one language lease and return one worker-local receipt. It cannot close another language, independent Shadow, C01 convergence, hardware, MCP, legal, merge or release.

## `LH-ANDROID-004`

**State:** `BLOCKED_BY_IMPLEMENTATION`

Requires Issue #7 exact candidate, frozen connected-test task and a trusted physical Android device. Emulator evidence does not satisfy this lane.

```text
adb devices -l
./gradlew <ANDROID_CONNECTED_TEST_TASK>
```

The task value comes from the A02 exact handoff and is passed as argv, not guessed.

## `LH-IOS-005`

**State:** `BLOCKED_BY_IMPLEMENTATION`

Requires Issue #8 exact candidate, frozen scheme and physical destination binding. Simulator evidence does not satisfy this lane.

```text
xcodebuild -scheme <IOS_SCHEME> -destination <IOS_DESTINATION> test
```

Both values are resolved before process launch. The queue does not depend on shell expansion and does not publish the destination value by default.

## `LH-SECURITY-006`

**State:** `BLOCKED_BY_CANDIDATE`

Requires an immutable candidate SHA/tree, threat model, dependency-rights packet, SBOM and declared denominator. The reviewer is independent and read-only. Self-review cannot satisfy this item. Legal acceptance remains Human-owned.

## `LH-HUMAN-007`

**State:** `HUMAN_ADMIT_REQUIRED`

All policy-required technical, local, physical, rights and security receipts, unresolved blockers and rollback identity are presented together.

Only an explicit Human decision may authorize merge, release, production, rollback or public/private-boundary changes. Silence is not approval.

## Evidence ceiling

Queue correctness proves only that the handoff is typed and reviewable. It does not prove any command ran, a Session exists, Git Town is installed, a language implementation is correct, a physical device behaved correctly, independent security/legal review passed, or release/production was admitted.
