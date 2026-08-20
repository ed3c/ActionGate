# Local Handoff Execution Queue

Current queue subject: the ActionGate bootstrap/stack. Repository-only automation has reached real local/physical/Human boundaries.

Exactly one item is `ACTIVE`. Successors remain blocked until the predecessor's durable exit receipt validates. The machine authority is `.actiongate/local-handoff-queue.json`; this document is the human-readable projection and must not widen it.

## Execution boundary

Run `LH-001` and `LH-002` only from a dedicated, empty, personal clean-room working directory that contains no employer repository, confidential document, credential export, or unrelated source tree. The queue does not authorize destructive cleanup of an existing checkout.

No queue item authorizes `git reset`, rebase, sync, push, merge, branch deletion, semantic-conflict resolution, permission changes, release, production deployment, or rollback unless a later Human-owned item explicitly admits that operation.

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

**Next:** `LH-002`.

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

**Next:** implementation-dependent physical lanes remain blocked until exact candidates exist.

## LH-003 — Android physical-device lane

**State:** `BLOCKED_BY_IMPLEMENTATION`

**Entry:** Issue #7 exact candidate SHA exists; `packages/sdk-android/` and its connected test task are implemented; a trusted personal Android device is connected.

**Commands:**

```bash
cd ActionGate
adb devices -l
./gradlew :packages:sdk-android:connectedCheck
```

The owning implementation atom freezes the exact Gradle task and receipt parser before this item becomes `ACTIVE`. Capture only the minimum redacted device/build class, hardware-key security level, test result, and Play Integrity evidence required by the test contract. Never capture private keys, tokens, account identifiers, or stable personal identifiers.

**Exit:** own-lane physical receipt admitted by Issue #13.

**Next:** `LH-005` only after every prerequisite named by its entry contract closes. `LH-004` may run independently when its own entry closes.

## LH-004 — iOS physical-device lane

**State:** `BLOCKED_BY_IMPLEMENTATION`

**Entry:** Issue #8 exact candidate SHA exists; `packages/sdk-ios/` and scheme are implemented; `ACTIONGATE_IOS_DESTINATION` is bound locally to an approved physical-device destination string.

**Command:**

```bash
cd ActionGate
xcodebuild -scheme ActionGateSDK -destination "$ACTIONGATE_IOS_DESTINATION" test
```

The exact scheme/destination and receipt parser are frozen by A03 before activation. No simulator receipt satisfies this lane.

**Exit:** own-lane physical receipt admitted by Issue #13.

## LH-005 — independent security and clean-room review

**State:** `BLOCKED_BY_CANDIDATE`

**Entry:** P7 emits one immutable candidate SHA/tree, SBOM, dependency-rights packet and threat model.

**Lane:** an independent read-only reviewer/security authority that did not implement the candidate.

**Exit:** a signed or hashed review receipt states `PASS`, `FAIL`, or typed blockers and binds the exact candidate. Technical self-review cannot satisfy independence. Employer-IP/legal acceptance remains a separate Human-owned lane.

## LH-006 — Human merge/release admission

**State:** `HUMAN_ADMIT_REQUIRED`

**Entry:** all required technical, local, physical, rights and security receipts are presented together with unresolved blockers and rollback identity.

**Authority:** repository owner and applicable organizational/legal/security authorities.

**Exit:** explicit decision for merge/release/production/rollback/public-private-boundary changes. Absence of a decision is not approval.

## Evidence ceiling

A validated queue proves only that continuation instructions are typed and reviewable. It does not prove that any command executed, that Git Town is installed, that a physical device behaved as expected, that a security/legal review passed, or that a Human admitted merge/release.
