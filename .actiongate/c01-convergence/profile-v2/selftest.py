#!/usr/bin/env python3
from __future__ import annotations
import copy
from pathlib import Path
import check_convergence as c
ROOT=Path(__file__).resolve().parent
reg=c.load(ROOT/"convergence-registry.json"); phase=c.load(ROOT/"phase-status.json"); contract=c.load(ROOT/"independent-review.contract.json")
def refuse(name,fn):
    try: fn()
    except c.Refusal: return
    raise AssertionError(name+" did not refuse")
def review(verdict="ELIGIBLE_FOR_C01_CONVERGENCE"):
    return {"schema":"actiongate-c01-independent-review-receipt/v2","template":False,"repository":"ed3c/ActionGate","issue":26,"dispatch_issue":60,"dispatch_pr":61,
      "dispatch_epoch":contract["dispatch_epoch"],
      "reviewer":{"context_id":"external-review-0001","kind":"OTHER_SEPARATE_READ_ONLY_SESSION","separate_context":True,"implemented_or_repaired_audited_subjects":False,"built_dispatch_packet":False,"same_context_as_builder":False,"read_only":True,"source_mutation_performed":False,"private_context_accessed":False},
      "audited_subjects":{"contract_epoch":contract["contract_epoch"],"common_evidence":contract["common_evidence"],**{k:{**v} for k,v in contract["workers"].items()}},
      "falsifiers":[{"id":x,"state":"PASS","evidence":"independent public evidence"} for x in contract["required_falsifiers"]],
      "findings":[],"dissent":[],"verdict":verdict,"evidence_ceiling":contract["evidence_ceiling"],"human_owned":["semantic conflict resolution","merge","release","production"]}
c.check(reg,phase,contract)
r=review(); assert c.validate_review(r,reg,contract)=="ELIGIBLE_FOR_C01_CONVERGENCE"
d=c.derive(r,reg,contract,"1"*40); assert d["decision"]=="C01_ADMITTED" and d["k01_completion_eligible"] and not d["k01_start_authorized"]
refuse("missing_independent_receipt",lambda:c.derive({},reg,contract,"1"*40))
r=review(); r["reviewer"]["same_context_as_builder"]=True; refuse("same_context_review",lambda:c.validate_review(r,reg,contract))
r=review(); r["dispatch_epoch"]="2"*40; refuse("review_subject_drift",lambda:c.validate_review(r,reg,contract))
r=review(); r["audited_subjects"]["contract_epoch"]="3"*40; refuse("wrong_contract_epoch",lambda:c.validate_review(r,reg,contract))
r=review(); r["audited_subjects"]["kotlin"]["current_head"]="4"*40; refuse("wrong_worker_head_or_tree",lambda:c.validate_review(r,reg,contract))
r=review(); r["falsifiers"].pop(); refuse("falsifier_denominator_shrinkage",lambda:c.validate_review(r,reg,contract))
r=review(); r["falsifiers"][0]["state"]="NOT_EXERCISED"; refuse("not_exercised_falsifier",lambda:c.validate_review(r,reg,contract))
d=c.derive(review("HOLD"),reg,contract,"1"*40); assert d["decision"]=="HOLD" and not d["c01_admitted"]
d=c.derive(review("REJECT"),reg,contract,"1"*40); assert d["decision"]=="REJECT" and not d["c01_admitted"]
r=review(); r["dissent"]=["https://"+"docs."+"google."+"com/private"]; refuse("private_locator_or_secret_shape",lambda:c.validate_review(r,reg,contract))
r=review(); r["evidence_ceiling"]="hardware MCP integration PASS"; refuse("hardware_or_mcp_claim_widening",lambda:c.validate_review(r,reg,contract))
p=copy.deepcopy(phase); p["k01_start_authorized"]=True; refuse("automatic_k01_start",lambda:c.check(reg,p,contract))
p=copy.deepcopy(phase); p["merge_authorized"]=True; refuse("automatic_merge_release_production",lambda:c.check(reg,p,contract))
rr=copy.deepcopy(reg); rr["stack"]["base_commit"]="5"*40; refuse("stale_dispatch_epoch",lambda:c.check(rr,phase,contract))
print("C01 convergence selftest: PASS 14/14")
