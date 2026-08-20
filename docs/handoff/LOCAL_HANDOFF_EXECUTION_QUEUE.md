# Local Handoff Execution Queue

Current queue subject: the ActionGate bootstrap/stack. Repository-only automation has reached real local/physical/Human boundaries.

Exactly one item is `ACTIVE`. After its valid receipt closes, the controller may activate exactly one eligible item from that item's `next_candidates`. A blocked sibling never becomes active merely because another sibling completed, and no item auto-executes. The machine authority is `.actiongate/local-handoff-queue.json`; this document is the human-readable projection and must not widen it.

## Execution boundary

Run `LH-001` and `LH-002` only from a dedicated, empty, personal clean-room working directory that contains no employer repository, confidential document, credential export, or unrelated source tree. The queue does not authorize destructive cleanup of an existing checkout.

No queue item authorizes `git reset`, rebase, sync, push, merge, branch deletion, semantic-conflict resolution, permission changes, release, production deployment, or rollback unless a later Human-owned item explicitly admits that operation.

A command template is not executable until every placeholder has an explicit non-shell binding. Environment-variable names may be recorded; secret or identity-bearing values must not be copied into public receipts.

## LH-001 — local clean checkout and bootstrap read-back

**State:** `ACTIVE`

**Entry:** Git, Python 3 and network access to GitHub are available on a trusted local host; the executor starts in a dedicated empty clean-room directory; no employer repository or confidential document is open in the same agent session.

**Expected subject:**

```text
origin/ag/C00-technical-control-plane
3b8f08f6fc179ea4a8166a24574a506269151586
```

**Commands:**

```bash
git clone https://github.com/ed3c/ActionGate.git ActionGate
git -C ActionGate fetch origin --prune
git -C ActionGate switch --detach origin/ag/C00-technical-control-plane
git -C ActionGate rev-parse HEAD
git -C ActionGate rev-parse HEAD^{tree}
git -C ActionGate diff --check
python3 -m json.tool ActionGate/.actiongate/system-contract.json >/dev/null
python3 -m json.tool ActionGate/.actiongate/task-dag.json >/dev/null
```

The executor writes an atom-local receipt at:

```text
ActionGate/.actiongate/receipts/local/LH-001.json
```

The receipt must bind:

```text
subject_sha == 3b8f08f6fc179ea4a8166a24574a506269151586
tree_sha
diff_check = PASS
system_contract_json = PASS
task_dag_json = PASS
clean_room_source_separation = PASS
```

Use Python or the host-native SHA-256 utility if a receipt digest is needed; do not assume GNU `sha256sum` exists on macOS.

**Exit:** the durable receipt binds the exact expected C00 subject/tree and every named check is `PASS`.

**Next candidates:** `LH-002` only.

## LH-002 — local branch/stack and Git Town capability receipt

**State:** `BLOCKED_BY_PREDECESSOR`

**Entry:** `LH-001` receipt valid; Draft PRs #14, #15 and #16 exist.

**Commands:**

```bash
git -C ActionGate fetch origin --prune
git -C ActionGate town --version
git -C ActionGate merge-base --is-ancestor origin/main origin/ag/C00-technical-control-plane
git -C ActionGate merge-base --is-ancestor origin/ag/C00-technical-control-plane origin/ag/S01-source-rights
git -C ActionGate merge-base --is-ancestor origin/ag/C00-technical-control-plane origin/ag/D00-prompts-handoff
```

The receipt is:

```text
ActionGate/.actiongate/receipts/local/LH-002.json
```

It records the Git Town version as `PASS` or `ABSENT`, each ancestry result independently, the exact remote refs observed, and an explicit assertion that no sync/push/merge/rebase/reset/branch-deletion/semantic-resolution operation ran.

`git town --version` failure records `BLOCKED_ABSENT_EXECUTABLE`; it does not convert the Git ancestry checks into a Git Town runtime `PASS`. No synchronization is required to prove the declared Draft topology.

**Exit:** stack ancestry is confirmed and Git Town capability is honestly `PASS` or `BLOCKED_ABSENT_EXECUTABLE`.

**Next candidates:** `LH-003`, `LH-004`, or `LH-005`, but the controller may activate only one whose entry contract is actually satisfied. This preserves true dependencies instead of forcing Android before iOS or vice versa.

## LH-003 — Android physical-device lane

**State:** `BLOCKED_BY_IMPLEMENTATION`

**Entry:** Issue #7 exact candidate SHA exists; the Android connected-test task is frozen by A02; a trusted personal Android device is connected.

**Command template:**

```text
adb devices -l
./gradlew <ANDROID_CONNECTED_TEST_TASK>
```

`<ANDROID_CONNECTED_TEST_TASK>` is taken from the exact A02 / Issue #7 handoff receipt before activation. It is not guessed by the queue and is passed as an argv value, not shell-expanded text.

Capture only the minimum redacted device/build class, hardware-key security level, test result, and Play Integrity evidence required by the test contract. Never capture private keys, tokens, account identifiers, or stable personal identifiers.

**Exit:** own-lane physical receipt admitted by Issue #13.

**Next candidates:** any still-eligible `LH-004`, `LH-005`, or `LH-006` entry. Completion of Android does not imply iOS/security/Human admission.

## LH-004 — iOS physical-device lane

**State:** `BLOCKED_BY_IMPLEMENTATION`

**Entry:** Issue #8 exact candidate SHA exists; the Xcode scheme is frozen by A03; the local physical destination binding exists.

**Command template:**

```text
xcodebuild -scheme <IOS_SCHEME> -destination <IOS_DESTINATION> test
```

Bindings before activation:

```text
<IOS_SCHEME>      <- exact A03 / Issue #8 handoff receipt
<IOS_DESTINATION> <- local ACTIONGATE_IOS_DESTINATION value
```

The executor substitutes these values before process launch and passes them as argv. It must not rely on a shell expanding `$ACTIONGATE_IOS_DESTINATION`, and the destination value is not copied into a public receipt unless the evidence contract explicitly permits a redacted form.

No simulator receipt satisfies this lane.

**Exit:** own-lane physical receipt admitted by Issue #13.

**Next candidates:** any still-eligible `LH-003`, `LH-005`, or `LH-006` entry.

## LH-005 — independent security and clean-room review

**State:** `BLOCKED_BY_CANDIDATE`

**Entry:** P7 emits one immutable candidate SHA/tree, SBOM, dependency-rights packet and threat model.

**Lane:** an independent read-only reviewer/security authority that did not implement the candidate.

**Exit:** a signed or hashed review receipt states `PASS`, `FAIL`, or typed blockers and binds the exact candidate. Technical self-review cannot satisfy independence. Employer-IP/legal acceptance remains a separate Human-owned lane.

**Next candidates:** remaining required physical lanes or `LH-006`, according to the release/admission policy. Security review does not silently waive missing physical evidence.

## LH-006 — Human merge/release admission

**State:** `HUMAN_ADMIT_REQUIRED`

**Entry:** all policy-required technical, local, physical, rights and security receipts are presented together with unresolved blockers and rollback identity.

**Authority:** repository owner and applicable organizational/legal/security authorities.

**Exit:** explicit decision for merge/release/production/rollback/public-private-boundary changes. Absence of a decision is not approval.

## Evidence ceiling

A validated queue proves only that continuation instructions are typed and reviewable. It does not prove that any command executed, that Git Town is installed, that a physical device behaved as expected, that a security/legal review passed, or that a Human admitted merge/release.
