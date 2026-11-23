#!/usr/bin/env python3
"""Read-only, ROM-free reconciliation of *recorded* Goemon decomp research.

Do not treat names mentioned in evidence as new C candidates. Historical
isolated/native success is not canonical acceptance, and task status can be stale.
"""
from __future__ import annotations
import collections
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

MAIN_RE = re.compile(r'^func_[0-9A-Fa-f]{8}_[0-9A-Fa-f]+$')


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def blob_sha(path: Path) -> str:
    h = hashlib.sha1()
    data = path.read_bytes()
    h.update(b'blob ' + str(len(data)).encode() + b'\0' + data)
    return h.hexdigest()


def names_from(value):
    if isinstance(value, str):
        if MAIN_RE.fullmatch(value):
            return [value]
        return []
    if isinstance(value, dict):
        output = []
        for k in ('name','function','symbol','target','function_name'):
            if k in value:
                output += names_from(value[k])
        return output
    if isinstance(value, list):
        return [name for item in value for name in names_from(item)]
    return []


def main(root: Path, out: Path):
    d = root/'decomp'
    combined=read_json(d/'results/combined.json')
    inventory=read_json(d/'results/inventory.json')
    registry=read_json(d/'data/candidate_registry.json')
    jman=read_json(d/'regions/japan_0.json')
    tasks=read_json(d/'history/TASKS_100.json')['tasks']
    branches=read_json(d/'data/branch_snapshot_20261117.json')
    usa={x['name'] for x in combined['comparison']['functions'] if x['matched']}
    japan={f['name'] for u in jman['units'] for f in u['functions']}
    assert len(usa)>=864 and len(japan)>=39
    assert inventory['summary']['newly_matching_c']==len(usa)
    assert registry['accepted_baseline']['usa_functions']<=len(usa) and registry['accepted_baseline']['japan_0_functions']==len(japan)
    ledger_records=[]
    for p in sorted((d/'plans/execution').glob('*.json')):
        data=read_json(p)
        if not isinstance(data,dict): continue
        primary=[]
        for key in ('original_function','target_function','function','target','original','functions'):
            primary.extend(names_from(data.get(key)))
        # "scope", "decision", "implementation" can mention other functions,
        # which are not assumed to be this task's target.
        primary=sorted(set(primary))
        status=data.get('status')
        if status is None and isinstance(data.get('decision'),dict):
            status=data['decision'].get('status',data['decision'].get('classification','UNSPECIFIED'))
        if not isinstance(status,str): status='UNSPECIFIED'
        ledger_records.append({
            'source':str(p.relative_to(root)),
            'blob_sha1':blob_sha(p),
            'task_id':data.get('task_id'),
            'date':data.get('date'),
            'historical_status':status,
            'explicit_target_names':primary,
            'explicit_targets_currently_accepted_usa':sorted(set(primary)&usa),
            'explicit_targets_currently_accepted_japan':sorted(set(primary)&japan),
            'explicit_targets_not_in_accepted_c':sorted(set(primary)-usa-japan),
            'retest_status':'HISTORICAL_EVIDENCE_REVIEWED_NOT_RECOMPILED',
        })
    task_list=[]
    for t in tasks:
        assert t['id'].startswith('G64-')
        task_list.append({'task_id':t['id'],'title':t.get('title'),'historical_status':t.get('status'),
                          'evidence_sources':[e['source'] for e in ledger_records if e['task_id']==t['id']]})
    report_records=[]
    for p in sorted((d/'results').glob('*.json')):
        if p.name.startswith(('combined','inventory')):continue
        obj=read_json(p)
        if not isinstance(obj,dict):continue
        report_records.append({
            'path':str(p.relative_to(root)),
            'blob_sha1':blob_sha(p),
            'format':obj.get('format'),
            'historical_status':obj.get('status','UNSPECIFIED'),
            'historical_as_of':obj.get('date',obj.get('date_utc',obj.get('started_utc'))),
        })
    residual=read_json(d/'results/vm_residual_inventory.json')
    has_residuals=residual.get('residual_functions',[])
    if isinstance(has_residuals,dict):has_residuals=list(has_residuals.values())
    residual_names=[]
    for entry in has_residuals:
        if isinstance(entry,dict):
            for key in ('name','function'):
                residual_names+=names_from(entry.get(key))
    # The live source manifest is the authority for the 13 unresolved script VM
    # functions; don't infer from an older research ledger.
    man=read_json(d/'manifest.json')
    script_vm=next(x for x in man['units'] if x['source']=='script_vm.c')
    live_vm_asm=script_vm['assembly_functions']
    if man.get('usa_script_vm436_promotion') is not None:
        # Final stage is applied after the immutable historical VM unit.
        from decomp.usa_script_vm436_promotion import NAME, validate_predecessor
        validate_predecessor(man)
        assert NAME in live_vm_asm and NAME in usa
        assert NAME not in combined['retained_assembly_functions']
        live_vm_asm=[name for name in live_vm_asm if name!=NAME]
    assert len(live_vm_asm)<=13
    assert not set(live_vm_asm)&usa
    old_registry=read_json(d/'data/candidate_registry_782_pending_20261117.json')
    assert len(old_registry['candidates'])==87
    assert all(c['name'] in (usa if c['region']=='usa' else japan) for c in old_registry['candidates'])
    status_summary=dict(sorted(collections.Counter(e['historical_status'] for e in ledger_records).items()))
    pr_preview=[{'number':x.get('number'),'title':x.get('title'),'url':x.get('url')}
                for x in branches.get('open_prs',[])]
    output={
        'format':'goemon-historical-research-reconciliation-v1',
        'as_of_utc':'2026-11-17',
        'scope':'Audits checked-in local decomp history, not every ASM entry or every remote branch tip',
        'canonical_tree_source':'authenticated local 864-USA/39-JP source aligned with live decomp manifests',
        'canonical_production':{
            'usa_matching_c':len(usa),'usa_matching_bytes':combined['comparison']['matched_function_bytes'],
            'usa_original_rom_exact':combined['comparison']['full_rom_match'],
            'usa_original_rom_sha1':combined['comparison']['candidate_sha1'],
            'usa_asm_remaining':inventory['summary']['remaining_assembly_entries'],
            'japan_matching_c':len(japan),
            'current_unpromoted_registry':len(registry['candidates']),
        },
        'reconciliation':{
            'old_registry_entries':87,
            'old_registry_now_accepted':sum(c['name'] in (usa if c['region']=='usa' else japan) for c in old_registry['candidates']),
            'historic_task_records':len(task_list),
            'historical_execution_ledgers':len(ledger_records),
            'historical_execution_statuses':status_summary,
            'research_result_files_indexed':len(report_records),
            'historical_branch_snapshot_entries':len(branches.get('branches',[])),
            'historical_open_pr_snapshot_entries':len(pr_preview),
            'live_script_vm_asm_names':live_vm_asm,
            'vm_residual_ledger_names':sorted(set(residual_names)),
        },
        'task_catalog':task_list,
        'execution_evidence':ledger_records,
        'archived_research_reports':report_records,
        'historic_branch_refs':[{'name':x['name'],'snapshot_head':x['head']}
                               for x in branches.get('branches',[])],
        'historic_pr_snapshot':pr_preview,
        'integration_boundaries':[
          'The 87 old registry candidates are all accepted. Their old isolated statuses are obsolete.',
          'Historical G64 PASSED_G2 labels do not independently establish current production ownership.',
          'A mentioned function name is not necessarily the historical task target.',
          'The task ledger describes investigations, not a verified exhaustive listing of 6,499 ASM entries.',
          'The currently enumerated script-VM assembly functions remain unpromoted despite earlier semantic models.',
          'Older branch and PR references are historical pointers, not authenticated current branch contents.',
          'Recompiling the thousands of remaining ASM entries or all historic variants was not performed by this metadata audit.',
        ],
    }
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS',**output['reconciliation'],'report_bytes':out.stat().st_size}))

if __name__=='__main__':
    main(Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(),Path(sys.argv[2] if len(sys.argv)>2 else '/tmp/goemon-historical-audit.json'))
