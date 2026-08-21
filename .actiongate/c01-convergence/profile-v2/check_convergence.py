#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REG=ROOT/"convergence-registry.json"; PHASE=ROOT/"phase-status.json"; CONTRACT=ROOT/"independent-review.contract.json"
class Refusal(RuntimeError): pass
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def private(v):
    s=json.dumps(v,ensure_ascii=False)
    return any(x in s for x in ("docs.google.com","drive.google.com","ACTIONGATE_PRIVATE_","BEGIN PRIVATE KEY","BEGIN OPENSSH PRIVATE KEY","ghp_","github_pat_"))
EXPECTED={
"kotlin":{"current_head":"cf589a0990aaaa6422be9c649b52b44230d570f6","current_tree":"10a35f943aaee0b0035132100357a1adbacff7e1","source_candidate":"0247eb1fc7201b51aded66f2c2311aa42f9ca83c","source_tree":"15a27f2d9dbaacdfbea57dc1cd37e4af284b09dc","receipt_subject":"9420a4cdb4c7119ff56d921688a65d62ff92cf39","receipt_tree":"c4d5b2fcd70b29b993d149e7120d149c82272592","receipt_blob":"73e38ebfadf4512d1fbff63ba3d6b428ee5c46a7","shadow_blob":"0dec1c52b2e197c24deac9d0ac2ab9c2e69c78a2"},
"swift":{"current_head":"039827061f54aa72e2b81365a4c904d25833f83e","current_tree":"015cc3123b3b09ea0c087028aaea2ee052c51508","source_candidate":"2f089d45056fd783f57f3458dc739f33a49304c7","source_tree":"684275693783c379b134bd499a7dcddeb1f0b34c","receipt_subject":"acd6ef93dc2f17340c86d5e45fa7a56496a53d52","receipt_tree":"921a8fd1d7584991c0321bd3dadf6959b24a480c","receipt_blob":"31384670f22a0ff9558a0257ec6bb916056d1942","shadow_blob":"4345e5354d49338613b5e71419dc639a7803b89a"},
"typescript":{"current_head":"3ed9f0307df0937028bbf52fe8fbd2a6621acafe","current_tree":"17532a35f42b07e350e7785a7be11038c9cf1ba0","source_candidate":"dbdcfdcd8f100c3135730bc828700ffc8239994e","source_tree":"39a40aab9f13fdcae04d3164669667aa7322029c","receipt_subject":"9f4f19468fda8c32cab376484ed75855bb577277","receipt_tree":"75e8d5fd360a2f15af6a27b62aa02b765b7392a1","receipt_blob":"4b16df1f702cc4e91dcef8c873cdf8df67cdd2b6","shadow_blob":"d398b39159e8aa4b1347315911330136c95b1504"}}
def check(reg,phase,contract):
    if (reg.get("schema"),reg.get("repository"),reg.get("issue"))!=("actiongate-c01-convergence-control/v1","ed3c/ActionGate",62): raise Refusal("registry identity")
    st=reg.get("stack",{})
    if (st.get("base_pr"),st.get("base_commit"),st.get("base_tree"),st.get("relation"))!=(61,"2998b0a93d23ddfca0934250d82bdbd892f2c84b","e535e6fa031c84697d9b0b5cb96ee90a64286a08","TRUE_CHILD_OF_PROFILE_V2_DISPATCH"): raise Refusal("stale dispatch epoch")
    d=reg.get("dispatch",{})
    if (d.get("dispatch_candidate"),d.get("dispatch_candidate_tree"))!=("23ee1763bea2703f732482952b6312d751faf8cb","bd34215ad036be41b5a2333b9b36b076bcddabc6"): raise Refusal("dispatch candidate drift")
    if reg.get("contract_epoch")!="b63589e5a16e82fda1a9554227f2ebbb55398c8a" or reg.get("common_evidence")!="9f41038240837ea2dd9dcdb9befd13e6ba81a78e": raise Refusal("contract drift")
    if reg.get("workers")!=EXPECTED: raise Refusal("worker subjects drift")
    fs=reg.get("required_falsifiers",[])
    if len(fs)!=33 or len(set(fs))!=33: raise Refusal("falsifier denominator shrinkage")
    if reg.get("independent_review",{}).get("receipt_present") is not False: raise Refusal("fabricated review presence")
    a=reg.get("authority",{})
    for k in ("this_atom_may_fabricate_review","this_atom_may_emit_final_issue24_verdict","automatic_k01_start","automatic_merge","automatic_release","automatic_production"):
        if a.get(k) is not False: raise Refusal("authority widening "+k)
    if phase.get("state")!="BLOCKED_BY_INDEPENDENT_RECEIPT" or phase.get("independent_review")!="NOT_EXERCISED": raise Refusal("false phase")
    for k in ("c01_admitted","k01_completion_eligible","k01_start_authorized","merge_authorized","release_authorized","production_authorized"):
        if phase.get(k) is not False: raise Refusal("false authority "+k)
    if contract.get("dispatch_epoch")!=d["dispatch_candidate"] or contract.get("contract_epoch")!=reg["contract_epoch"] or contract.get("common_evidence")!=reg["common_evidence"] or contract.get("workers")!=EXPECTED or contract.get("required_falsifiers")!=fs: raise Refusal("review contract drift")
    if private(reg) or private(phase) or private(contract): raise Refusal("private/secret shape")
def validate_review(r,reg,contract):
    if r.get("schema")!="actiongate-c01-independent-review-receipt/v2" or r.get("template") is not False: raise Refusal("not evidence")
    if (r.get("repository"),r.get("issue"),r.get("dispatch_issue"),r.get("dispatch_pr"),r.get("dispatch_epoch"))!=("ed3c/ActionGate",26,60,61,contract["dispatch_epoch"]): raise Refusal("review subject drift")
    rr=r.get("reviewer",{})
    for k,v in contract["required_reviewer_state"].items():
        if rr.get(k)!=v: raise Refusal("review independence "+k)
    if rr.get("kind") not in ("EXTERNAL_CODEX_REPLAY","EXTERNAL_HUMAN_REVIEWER","OTHER_SEPARATE_READ_ONLY_SESSION"): raise Refusal("reviewer kind")
    if not isinstance(rr.get("context_id"),str) or len(rr["context_id"])<8 or rr["context_id"]=="UNSET000": raise Refusal("review context")
    a=r.get("audited_subjects",{})
    if a.get("contract_epoch")!=contract["contract_epoch"] or a.get("common_evidence")!=contract["common_evidence"]: raise Refusal("audited contract drift")
    for lang,w in EXPECTED.items():
        if a.get(lang)!=w: raise Refusal(lang+" audited subject drift")
    fs=r.get("falsifiers",[]); by={x.get("id"):x for x in fs}
    if len(fs)!=33 or len(by)!=33 or set(by)!=set(contract["required_falsifiers"]): raise Refusal("review denominator")
    if any(x.get("state") not in ("PASS","FAIL","NOT_EXERCISED") or not x.get("evidence") for x in fs): raise Refusal("bad falsifier")
    v=r.get("verdict")
    if v not in contract["allowed_verdicts"]: raise Refusal("bad verdict")
    if v=="ELIGIBLE_FOR_C01_CONVERGENCE" and any(x["state"]!="PASS" for x in fs): raise Refusal("eligible with incomplete evidence")
    if r.get("evidence_ceiling")!=contract["evidence_ceiling"] or "merge" not in r.get("human_owned",[]): raise Refusal("evidence/authority widening")
    if private(r): raise Refusal("private/secret shape")
    return v
def derive(r,reg,contract,subject):
    if not isinstance(subject,str) or len(subject)!=40 or any(ch not in "0123456789abcdef" for ch in subject) or subject=="0"*40: raise Refusal("control subject must be exact non-zero SHA")
    v=validate_review(r,reg,contract); decision={"ELIGIBLE_FOR_C01_CONVERGENCE":"C01_ADMITTED","HOLD":"HOLD","REJECT":"REJECT"}[v]; ok=decision=="C01_ADMITTED"
    return {"schema":"actiongate-c01-convergence-decision/v1","repository":"ed3c/ActionGate","issue":24,"control_issue":62,"control_subject":subject,
      "independent_review_digest":hashlib.sha256(json.dumps(r,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest(),
      "contract_epoch":reg["contract_epoch"],"worker_subjects":{k:{"head":v["current_head"],"tree":v["current_tree"]} for k,v in EXPECTED.items()},
      "decision":decision,"c01_admitted":ok,"k01_completion_eligible":ok,"k01_start_authorized":False,"merge_authorized":False,"release_authorized":False,"production_authorized":False,
      "dissent":r.get("dissent",[]),"evidence_ceiling":"C01 contract/canonicalization admission only; no hardware, MCP, integration, security/legal, merge, release or production proof",
      "human_owned":["semantic conflict resolution","merge","release","production","security/legal acceptance"]}
def main():
    p=argparse.ArgumentParser(); p.add_argument("--review-receipt"); p.add_argument("--control-subject"); p.add_argument("--emit-candidate"); x=p.parse_args()
    reg,phase,contract=load(REG),load(PHASE),load(CONTRACT); check(reg,phase,contract)
    if not x.review_receipt:
        print("C01 convergence structural control: PASS"); print("Independent review: NOT_EXERCISED; admission remains BLOCKED"); return
    cand=derive(load(x.review_receipt),reg,contract,x.control_subject)
    if x.emit_candidate: Path(x.emit_candidate).write_text(json.dumps(cand,indent=2)+"\n",encoding="utf-8")
    print("C01 convergence review receipt: PASS -> "+cand["decision"])
if __name__=="__main__": main()
