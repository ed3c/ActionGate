#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parent
REG=ROOT/"dispatch-registry.json"; TPL=ROOT/"independent-review-receipt.template.json"
PROMPTS=(ROOT/"prompts/independent-shadow.md",ROOT/"prompts/convergence.md")
PHASE=ROOT/"phase-status.json"
REG_SHA="ade7fddfc1dbe78e7fb5ce477f318248f6bc8cc03dc93f840342b54834615c0d"
OLD_HEADS={"511b26ad10389e0d0076f463f59f3a9c0e8a1b6e","48bc9cf00105f40d5444542ddcdad85106f3c1d5","6a99c61150d00be56c7eddf70eb9e3f423cfb7fa"}
PROFILE={"registered_domain_allowlist","unknown_domain_rejected","embedded_nul_domain_rejected","raw_ascii_key_profile","raw_fraction_rejected","raw_exponent_rejected","raw_positive_unsafe_integer_rejected","raw_negative_unsafe_integer_rejected","raw_safe_integer_boundaries","raw_negative_zero_accepted"}
ALL_STATES={"PASS","FAIL","NOT_EXERCISED"}
PRIVATE=("docs"+".google.com","drive"+".google.com","-----"+"BEGIN","ghp"+"_","github"+"_pat_","Bearer"+" ","employer-internal")
PLACEHOLDER=re.compile(r"<[A-Z0-9_ -]+>")

class Refusal(ValueError): pass

def load(p:Path)->Any: return json.loads(p.read_text("utf-8"))
def strings(v:Any):
    if isinstance(v,str): yield v
    elif isinstance(v,list):
        for x in v: yield from strings(x)
    elif isinstance(v,dict):
        for k,x in v.items(): yield k; yield from strings(x)
def safe(v:Any,label:str):
    for s in strings(v):
        if any(x.lower() in s.lower() for x in PRIVATE): raise Refusal(label+": private-or-secret-shaped content")
def subject(w:dict)->dict:
    return {k:w[k] for k in ("current_head","current_tree","source_candidate","source_tree","receipt_subject","receipt_tree","receipt_blob","shadow_blob")}
def expected_subjects(r:dict)->dict:
    return {"contract_epoch":r["contract_epoch"]["commit"],"common_evidence":r["common_evidence"]["commit"],**{w["language"]:subject(w) for w in r["workers"]}}

def check_registry(r:dict, exact:bool=True):
    if exact and hashlib.sha256(REG.read_bytes()).hexdigest()!=REG_SHA: raise Refusal("registry byte digest drift")
    if r.get("schema")!="actiongate-c01-profile-shadow-dispatch/v2" or r.get("issue")!=60: raise Refusal("registry identity")
    if r.get("stack",{}).get("relation")!="TRUE_CHILD_SUPERSEDING_DISPATCH_EPOCH": raise Refusal("false stack relation")
    if r.get("superseded_dispatch",{}).get("may_be_used_for_review") is not False: raise Refusal("stale dispatch not quarantined")
    c=r.get("current_context",{})
    if c.get("independent_reviewer_eligible") is not False or c.get("may_emit_issue_26_verdict") is not False or c.get("may_emit_c01_admitted") is not False: raise Refusal("builder authority widened")
    if r.get("worker_relation")!="PATH_DISJOINT_SIBLINGS_NO_INTER_WORKER_GIT_PARENT": raise Refusal("false worker serialization")
    ws=r.get("workers",[])
    if len(ws)!=3 or {w.get("language") for w in ws}!={"kotlin","swift","typescript"}: raise Refusal("worker set")
    if len({w.get("lease") for w in ws})!=3: raise Refusal("lease overlap")
    for w in ws:
        for k in ("current_head","current_tree","source_candidate","source_tree","receipt_subject","receipt_tree","receipt_blob","shadow_blob"):
            if not re.fullmatch(r"[0-9a-f]{40}",str(w.get(k,""))): raise Refusal(w["language"]+":"+k)
        if w["current_head"] in OLD_HEADS: raise Refusal("stale Issue #49 head reused")
        if w["current_head"]==w["source_candidate"]: raise Refusal("missing successor layers")
    if r.get("common_receipt_denominator")!={"positive":3,"negative":7,"required":10}: raise Refusal("denominator")
    fs=r.get("required_falsifiers",[])
    if len(fs)!=33 or len(set(fs))!=33 or not PROFILE.issubset(set(fs)): raise Refusal("falsifier denominator")
    if r.get("review",{}).get("issue")!=26 or r.get("review",{}).get("external_separate_context_required") is not True: raise Refusal("review gate")
    if r.get("convergence",{}).get("state")!="BLOCKED_BY_INDEPENDENT_REVIEW_RECEIPT": raise Refusal("convergence gate")
    if r.get("local_handoff",{}).get("active_item")!="C01-PROFILE-SHADOW-002": raise Refusal("handoff active item")
    safe(r,"registry")

def check_template(t:dict,r:dict):
    if t.get("schema")!="actiongate-c01-independent-review-receipt/v2" or t.get("template") is not True or t.get("issue")!=26 or t.get("dispatch_issue")!=60: raise Refusal("template identity")
    if t.get("reviewer",{}).get("separate_context") is not False or t.get("verdict")!="HOLD": raise Refusal("template fabricates authority")
    fs=t.get("falsifiers",[])
    if {x.get("id") for x in fs}!=set(r["required_falsifiers"]) or any(x.get("state")!="NOT_EXERCISED" for x in fs): raise Refusal("template falsifiers")
    if t.get("audited_subjects")!=expected_subjects(r): raise Refusal("template subjects")
    safe(t,"template")

def check_prompts(r:dict):
    for p in PROMPTS:
        s=p.read_text("utf-8")
        if PLACEHOLDER.search(s): raise Refusal(p.name+": placeholder")
        for x in ("Issue #60","Issue #26","Issue #24","SAME_CONTEXT_READ_ONLY_SHADOW_IS_NOT_INDEPENDENT",r["contract_epoch"]["commit"],r["common_evidence"]["commit"],*(w["current_head"] for w in r["workers"])):
            if x not in s: raise Refusal(p.name+": missing "+x)
        safe(s,p.name)

def check_phase(p:dict):
    if p.get("schema")!="actiongate-c01-profile-shadow-phase/v2" or p.get("issue")!=60: raise Refusal("phase identity")
    if p.get("independent_review")!="NOT_EXERCISED" or p.get("c01_admitted") is not False or p.get("k01_started") is not False: raise Refusal("phase authority")
    safe(p,"phase")

def validate_review_receipt(d:dict,r:dict):
    if d.get("schema")!="actiongate-c01-independent-review-receipt/v2" or d.get("template") is not False or d.get("issue")!=26 or d.get("dispatch_issue")!=60: raise Refusal("review identity")
    pr=r.get("stack",{}).get("dispatch_pr",0); epoch=r.get("dispatch_candidate",{}).get("commit")
    if pr and d.get("dispatch_pr")!=pr: raise Refusal("dispatch PR")
    if epoch and d.get("dispatch_epoch")!=epoch: raise Refusal("dispatch epoch")
    q=d.get("reviewer",{})
    required={"separate_context":True,"implemented_or_repaired_audited_subjects":False,"built_dispatch_packet":False,"same_context_as_builder":False,"read_only":True,"source_mutation_performed":False,"private_context_accessed":False}
    if any(q.get(k) is not v for k,v in required.items()): raise Refusal("reviewer independence")
    if len(str(q.get("context_id","")))<8: raise Refusal("reviewer context")
    if d.get("audited_subjects")!=expected_subjects(r): raise Refusal("review subjects")
    fs=d.get("falsifiers",[])
    if len(fs)!=len(r["required_falsifiers"]) or {x.get("id") for x in fs}!=set(r["required_falsifiers"]): raise Refusal("review denominator")
    if any(x.get("state") not in ALL_STATES or not x.get("evidence") for x in fs): raise Refusal("review falsifier evidence")
    verdict=d.get("verdict")
    if verdict not in {"ELIGIBLE_FOR_C01_CONVERGENCE","HOLD","REJECT"}: raise Refusal("review verdict")
    if verdict=="ELIGIBLE_FOR_C01_CONVERGENCE" and any(x["state"]!="PASS" for x in fs): raise Refusal("eligible requires all PASS")
    if d.get("evidence_ceiling")!="independent read-only C01 contract and language review only" or "merge" not in d.get("human_owned",[]): raise Refusal("review authority")
    safe(d,"review")

def run(review:Path|None=None):
    r=load(REG); check_registry(r); check_template(load(TPL),r); check_prompts(r); check_phase(load(PHASE))
    if review: validate_review_receipt(load(review),r)

def main()->int:
    a=argparse.ArgumentParser(); a.add_argument("--review-receipt",type=Path); x=a.parse_args()
    try: run(x.review_receipt)
    except (OSError,json.JSONDecodeError,Refusal,KeyError,TypeError) as e:
        print("C01_PROFILE_SHADOW_DISPATCH: FAIL: "+str(e),file=sys.stderr); return 2
    print("C01_PROFILE_SHADOW_DISPATCH: PASS")
    print("INDEPENDENT_REVIEW: NOT_EXERCISED" if x.review_receipt is None else "INDEPENDENT_REVIEW_RECEIPT: VALID")
    print("C01_CONVERGENCE: BLOCKED_BY_INDEPENDENT_REVIEW_RECEIPT"); return 0
if __name__=="__main__": raise SystemExit(main())
