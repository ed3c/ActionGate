# Local Handoff Execution Queue

Current queue subject: the ActionGate bootstrap/stack. Repository-only automation has reached real local/physical/Human boundaries.

Exactly one item is `ACTIVE`. Successors remain blocked until the predecessor's durable exit receipt validates.

## LH-001 — local clean checkout and bootstrap read-back

**State:** `ACTIVE`

**Entry:** Git, Python 3 and network access to GitHub are available on a trusted local host; no employer repository or confidential document is open in the same agent session.

**Commands:**

```bash
mkdir -p "$HOME/actiongate-handoff"
cd "$HOME/actiongate-handoff"
[ -d ActionGate/.git ] || git clone https://github.com/ed3c/ActionGate.git ActionGate
cd ActionGate
git fetch origin --prune
git checkout ag/C00-technical-control-plane
git reset --hard origin/ag/C00-technical-control-plane
git rev-parse HEAD
git diff --check
python3 -m json.tool .actiongate/system-contract.json >/dev/null
python3 -m json.tool .actiongate/task-dag.json >/dev/null
mkdir -p .actiongate/receipts/local
{
  printf 'subject_sha='; git rev-parse HEAD
  printf 'tree_sha='; git rev-parse HEAD^{tree}
  printf 'diff_check=PASS\njson_parse=PASS\n'
} > .actiongate/receipts/local/LH-001.txt
sha256sum .actiongate/receipts/local/LH-001.txt > .actiongate/receipts/local/LH-001.txt.sha256
```

**Exit:** receipt contains the exact expected C00 head/tree and both checks PASS.

**Next:** LH-002.

## LH-002 — local branch/stack and Git Town capability receipt

**State:** `BLOCKED_BY_PREDECESSOR`

**Entry:** LH-001 receipt valid; Draft PRs #14, #15 and #16 exist.

**Commands:**

```bash
cd "$HOME/actiongate-handoff/ActionGate"
git fetch origin --prune
git town --version > .actiongate/receipts/local/LH-002.txt 2>&1
git merge-base --is-ancestor origin/main origin/ag/C00-technical-control-plane
git merge-base --is-ancestor origin/ag/C00-technical-control-plane origin/ag/S01-source-rights
git merge-base --is-ancestor origin/ag/C00-technical-control-plane origin/ag/D00-prompts-handoff
{
  printf 'main_to_C00=PASS\n'
  printf 'C00_to_S01=PASS\n'
  printf 'C00_to_D00=PASS\n'
} >> .actiongate/receipts/local/LH-002.txt
sha256sum .actiongate/receipts/local/LH-002.txt > .actiongate/receipts/local/LH-002.txt.sha256
```

`git town --version` failure records `BLOCKED_ABSENT_EXECUTABLE`; it does not convert the Git ancestry checks into a Git Town runtime PASS. No sync/push/merge is authorized by this item.

**Exit:** stack ancestry is confirmed and Git Town capability is honestly `PASS` or `BLOCKED_ABSENT_EXECUTABLE`.

**Next:** LH-003 when an exact implementation candidate exists.

## LH-003 — Android physical-device lane

**State:** `BLOCKED_BY_IMPLEMENTATION`

**Entry:** Issue #7 exact candidate SHA exists; `packages/sdk-android/` and its connected test task are implemented; a trusted personal Android device is connected.

**Commands:**

```bash
cd "$HOME/actiongate-handoff/ActionGate"
adb devices -l
./gradlew :packages:sdk-android:connectedCheck
```

The owning implementation atom must define the exact Gradle path before this item becomes ACTIVE. Capture device/build fingerprint, key security level, test result and redacted Play Integrity evidence in an atom-defined receipt. Never capture private keys, tokens or stable personal identifiers.

**Exit:** own-lane physical receipt admitted by Issue #13.

**Next:** LH-004 may run independently when its entry condition closes.

## LH-004 — iOS physical-device lane

**State:** `BLOCKED_BY_IMPLEMENTATION`

**Entry:** Issue #8 exact candidate SHA exists; `packages/sdk-ios/` and scheme are implemented; `ACTIONGATE_IOS_DESTINATION` is bound to an approved physical-device destination string.

**Command:**

```bash
cd "$HOME/actiongate-handoff/ActionGate"
xcodebuild -scheme ActionGateSDK -destination "$ACTIONGATE_IOS_DESTINATION" test
```

The exact scheme/destination and receipt parser are frozen by A03 before activation. No simulator receipt satisfies this lane.

**Exit:** own-lane physical receipt admitted by Issue #13.

## LH-005 — independent security and clean-room review

**State:** `BLOCKED_BY_CANDIDATE`

**Entry:** P7 emits an immutable candidate SHA/tree, SBOM and threat model.

**Lane:** independent read-only reviewer/security authority that did not implement the candidate.

**Exit:** signed/hashed review receipt states PASS/FAIL/blockers. Technical self-review cannot satisfy independence. Legal/employer-IP acceptance remains Human-owned.

## LH-006 — Human merge/release admission

**State:** `HUMAN_ADMIT_REQUIRED`

**Entry:** required technical, local, physical, rights and security receipts are presented with unresolved blockers.

**Authority:** repository owner and applicable organizational/legal/security authorities.

**Exit:** explicit decision for merge/release/rollback; absence of a decision is not approval.