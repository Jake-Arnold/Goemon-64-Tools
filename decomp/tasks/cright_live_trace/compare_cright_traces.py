"""Compare two actual Project64 narrow read-only traces, fail closed on missing evidence.

Does not read ROMs, savestates, or process memory. Never manufactures live observations.
"""
from __future__ import annotations

import argparse
import collections
from difflib import SequenceMatcher
import json
from pathlib import Path
import sys

SCHEMA = 'goemon-cright-live-trace-v1'
STAGE_PTRS = ['p90','p94','p98','p9c','pa0','pa4','pa8','pac']


def load(path: Path, label: str, *, allow_mock: bool=False) -> list[dict]:
    if not path.is_file():
        raise ValueError(f'Cannot read {label} trace: {path}')
    data = []
    for lineno, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        if not line.strip():
            continue
        try:
            x=json.loads(line)
        except json.JSONDecodeError as ex:
            raise ValueError(f'{label}:{lineno} invalid JSON: {ex}') from ex
        if x.get('schema')!=SCHEMA or x.get('run')!=label:
            raise ValueError(f'{label}:{lineno} wrong trace schema or run label')
        if data and x.get('seq')!=data[-1]['seq']+1:
            raise ValueError(f'{label}:{lineno} missing/out-of-order record')
        if not data and x.get('seq')!=0:
            raise ValueError(f'{label}:{lineno} missing initial record')
        data.append(x)
    if not data or data[0].get('kind')!='header':
        raise ValueError(f'{label} missing recorder header')
    if data[0].get('test_only_mock') and not allow_mock:
        raise ValueError(f'{label} is synthetic mock data, not an actual Project64 trace')
    if data[0].get('expected_original_expanded_rom_sha1')!='6f8745fecc3a5e7d4918c7a73353eb0726116ded':
        raise ValueError(f'{label} wrong Japanese ROM reference')
    return data


def is_aliased(row):
    stage=row.get('stage') or {}
    p90=stage.get('p90')
    return bool(p90 and p90 != '0x00000000' and all(stage.get(p)==p90 for p in STAGE_PTRS))


def summarize(rows):
    execs=[e for e in rows if e.get('kind')=='exec']
    counts=collections.Counter(e.get('event') for e in execs)
    gates=[x for x in execs if x.get('event')=='cright_gate']
    held_gates=[x for x in gates if (int(x.get('regs',{}).get('t2') or '0', 16)&1)]
    free_gates=[x for x in gates if not (int(x.get('regs',{}).get('t2') or '0', 16)&1)]
    allocator_events=[x for x in execs if x.get('event')=='allocator_call']
    last_gated_held=False
    observed=[]
    resolver_by_sp={}
    for x in execs:
        ev=x.get('event')
        if ev=='stage_reset_entry':
            last_gated_held=False
        if ev=='cright_gate':
            last_gated_held=bool(int(x.get('regs',{}).get('t2') or '0', 16)&1)
        elif ev=='resolver_call':
            regs=x.get('regs',{})
            resolver_by_sp[regs.get('sp')]={'category':regs.get('a1'),'actor':regs.get('a0'),'result':None}
        elif ev=='resolver_result':
            sp=x.get('regs',{}).get('sp')
            if sp in resolver_by_sp:
                resolver_by_sp[sp]['result']=x.get('regs',{}).get('v0')
        elif ev=='allocator_call':
            regs=x.get('regs',{})
            stage=x.get('stage') or {}
            parent=regs.get('a0')
            slot=stage.get('p90')
            paired=resolver_by_sp.pop(regs.get('sp'),None)
            alias_state=is_aliased(x)
            parent_is_alias=bool(alias_state and parent==slot)
            observed.append({'seq':x['seq'],'pc':x.get('pc'),'parent':parent,
                'parent_equals_stage_root':bool(parent==slot and slot and slot!='0x00000000'),
                'all_eight_slots_aliased':alias_state,
                'alias_allocator_argument_observed':parent_is_alias,
                'last_gate_held':last_gated_held,
                'input_bit_0001_set':bool(int(stage.get('buttons') or '0',16)&1),
                'resolver_category':paired.get('category') if paired else None,
                'resolver_result_equals_allocator_arg':(paired.get('result') is not None and paired.get('result')==parent) if paired else None})
    direct=[e for e in observed if e['alias_allocator_argument_observed']]
    matched=[e for e in direct if e.get('resolver_result_equals_allocator_arg') is True]
    completed=rows[-1].get('kind')=='footer'
    has_trace=bool(execs)
    if not has_trace:
        status='BLOCKED_NO_GUEST_EXECUTION'
    elif direct and any(x['last_gate_held'] for x in direct):
        status='OBSERVED_HELD_ALIAS_ALLOCATOR_ARGUMENT'
    elif direct:
        status='OBSERVED_ALIAS_ARGUMENT_HELD_GATE_UNCONFIRMED'
    elif not held_gates and rows[0]['run']=='held':
        status='INCONCLUSIVE_NO_HELD_GATE'
    elif allocator_events:
        status='INCONCLUSIVE_ALLOCATOR_NO_EIGHT_SLOT_ALIAS'
    else:
        status='INCONCLUSIVE_NO_ALLOCATOR_CALL'
    return {'run':rows[0]['run'],'status':status,'complete_file':completed,
        'event_count':len(execs),'event_counts':dict(sorted(counts.items())),
        'held_gate_count':len(held_gates),'normal_gate_count':len(free_gates),
        'stage_init_count':counts['stage_init_entry'],
        'allocator_boundary_count':len(allocator_events),
        'allocator_with_all_eight_slots_aliased':len(direct),
        'allocator_with_paired_resolver_result':len(matched),
        'allocator_observations':observed[:500],
        'rejected_overlay_events':sum(x.get('kind')=='overlay-rejected' for x in rows),
        'guard_fail_events':sum(x.get('kind')=='guard-fail' for x in rows),
        'sig_at_start':rows[0].get('main_signature_at_script_start'),
        'gate_sequences':[x['seq'] for x in gates[:30]],
        'notice':('Original Japanese per-event opcode signature checks are performed by the recorder; '
                  'matching signatures do not prove live savestate equality.')}


def compare(normal: list[dict], held: list[dict]):
    a=summarize(normal);b=summarize(held)
    names_a=[r['event'] for r in normal if r.get('kind')=='exec']
    names_b=[r['event'] for r in held if r.get('kind')=='exec']
    edits=[]
    for mode,i,j,k,l in SequenceMatcher(None,names_a[:5000],names_b[:5000],autojunk=False).get_opcodes():
        if mode=='equal':continue
        edits.append({'kind':mode,'normal_range':[i,j],'held_range':[k,l],
            'normal_events':names_a[i:min(j,i+5)],'held_events':names_b[k:min(l,k+5)]})
        if len(edits)>=15:break
    interpretation='INCONCLUSIVE'
    if any(x['alias_allocator_argument_observed'] and x['last_gate_held'] for x in b['allocator_observations']):
        interpretation='HELD_ALIAS_PASSED_TO_ALLOCATOR_OBSERVED'
    elif b['allocator_with_all_eight_slots_aliased']:
        interpretation='ALIAS_ARGUMENT_OBSERVED_HELD_GATE_UNCONFIRMED'
    elif not b['event_count']:
        interpretation='NO_LIVE_HELD_EXECUTION'
    elif not b['held_gate_count']:
        interpretation='NO_HELD_C_RIGHT_GATE_CAPTURED'
    report={'schema':'goemon-cright-comparison-v1','status':interpretation,
        'normal':a,'held':b,'first_sequence_differences':edits,
        'limits':['Exact same savestate was not independently authenticated.',
                  'An aliased allocator argument alone does not prove a malformed task or map corruption.',
                  'No allocator hit during an incomplete trace cannot rule out a later hit.',
                  'No task graph mutation or gameplay outcome is asserted without execution beyond the boundary.']}
    return report


def markdown(report):
    a,b=report['normal'],report['held']
    lines=['# Japanese C-Right — read-only Project64 trace comparison','',f'**Outcome:** `{report["status"]}`','',
         '| Metric | Normal | C-Right held/released |','|---|---:|---:|']
    for field,title in [
        ('event_count','Executed instrumented instructions'),
        ('stage_init_count','Stage initializer entries'),
        ('held_gate_count','C-Right-held gate visits'),
        ('normal_gate_count','Released/unheld gate visits'),
        ('allocator_boundary_count','Actor allocator-boundary hits'),
        ('allocator_with_all_eight_slots_aliased','Allocator hits with eight stage slots aliased'),
        ('allocator_with_paired_resolver_result','Aliased allocator hits with matched resolver result'),
        ('rejected_overlay_events','Rejected overlay-signature events')]:
        lines.append(f'| {title} | {a[field]} | {b[field]} |')
    lines.extend(['','## Strongest evidence',''])
    if b['allocator_with_all_eight_slots_aliased']:
        for obs in b['allocator_observations']:
            if obs['alias_allocator_argument_observed']:
                lines.append('- Held-trial record seq '+str(obs['seq'])+' passed `'+str(obs['parent'])+'` as allocator `$a0` while all eight slots were aliased. Paired resolver category: '+str(obs['resolver_category'])+'.')
                break
    else:
        lines.append('- No allocator boundary was recorded with all eight stage slots aliased in the provided held-trial trace.')
    lines.extend(['','## Interpretation limits',''])
    lines.extend('- '+s for s in report['limits'])
    if not a['complete_file'] or not b['complete_file']:
        lines.extend(['','**Warning:** At least one trace does not have a clean footer; partial file.'])
    return '\n'.join(lines)+'\n'


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--normal',type=Path,required=True)
    p.add_argument('--held',type=Path,required=True)
    p.add_argument('--report',type=Path,help='Output JSON report')
    p.add_argument('--markdown',type=Path,help='Output Markdown report')
    p.add_argument('--allow-mock',action='store_true',help='Allow mock fixtures for local testing only')
    args=p.parse_args()
    try:
        report=compare(load(args.normal,'normal',allow_mock=args.allow_mock),load(args.held,'held',allow_mock=args.allow_mock))
    except ValueError as err:
        p.error(str(err))
    if args.report:args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if args.markdown:args.markdown.write_text(markdown(report),encoding='utf-8')
    print(markdown(report))
    return 0 if report['normal']['event_count'] and report['held']['event_count'] else 2

if __name__=='__main__':
    sys.exit(main())