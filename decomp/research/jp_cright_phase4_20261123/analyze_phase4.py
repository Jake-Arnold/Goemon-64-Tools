#!/usr/bin/env python3
"""Conservative summary of a read-only Project64 Phase-4 C-Right JSONL trace.

A script finish('freeze_observed') only records a human report, not CPU freeze
or allocation corruption. Never publish raw JSONL game memory snapshots.
"""
import argparse
import collections
import json
from pathlib import Path

REQUIRED = {'start_state', 'finish'}
PC_CLEAR = '0x8021DBC0'
PC_SET_HELD = '0x802125C4'
PC_SET_BIT8 = '0x80212680'


def analyze(records):
    if not records:
        raise ValueError('Empty JSONL trace')
    mode = records[0].get('run')
    if mode not in ('held_followthrough','normal_followthrough'):
        raise ValueError('Unsupported Phase4 run mode')
    events = collections.Counter()
    observed_pc_reads = collections.Counter()
    flags = []
    p94 = []
    reject = 0
    for i, r in enumerate(records):
        if r.get('schema') != 'cright-phase4-v1' or r.get('run') != mode:
            raise ValueError(f'Wrong schema or mode at record {i}')
        if r.get('seq') != i:
            raise ValueError(f'Missing/duplicated seq at {i}')
        if not isinstance(r.get('elapsed_ms'), int) or r['elapsed_ms'] < 0:
            raise ValueError(f'Invalid elapsed_ms at {i}')
        if i and r['elapsed_ms'] < records[i-1]['elapsed_ms']:
            raise ValueError(f'Nonmonotonic timestamps at {i}')
        e = r.get('event')
        if not isinstance(e, str):
            raise ValueError('Missing event')
        events[e] += 1
        state = r.get('state', {})
        flags.append((i, state.get('stage_d1')))
        p94.append((i, state.get('stage_94_pointer'), state.get('stage_94_callback')))
        if e == 'overlay_signature_reject':
            reject += 1
        if e == 'stage_d1_read':
            observed_pc_reads[r.get('pc') or 'UNKNOWN_PC'] += 1
    if events['start_state'] != 1 or records[0]['event'] != 'start_state':
        raise ValueError('Start state missing/duplicate')
    if events['finish'] != 1 or records[-1]['event'] != 'finish':
        raise ValueError('Footer missing/duplicate')
    footer_reason = records[-1].get('extra', {}).get('reason')
    return {
        'status': 'OBSERVED_READ_ONLY_TRACE_WITH_MANUAL_OUTCOME',
        'run': mode,
        'record_count': len(records),
        'duration_ms': records[-1]['elapsed_ms'],
        'footer_reason': footer_reason,
        'freeze_proven_by_trace': False,
        'manual_freeze_reported': footer_reason == 'freeze_observed',
        'signature_rejections': reject,
        'event_counts': dict(sorted(events.items())),
        'stage_d1_read_pcs': dict(sorted(observed_pc_reads.items())),
        'observed_flag_values': sorted({f for _, f in flags if isinstance(f, int)}),
        'observed_p94_pointer_changed': len({x for _, x, _ in p94 if x is not None}) > 1,
        'p94_callback_changed': len({x for _, _, x in p94 if x is not None}) > 1,
        'stage_flag_reset_path_observed': bool(events['stage_d1_clear_instruction']),
        'stage_flag_held_set_path_observed': bool(events['stage_d1_set_held_instruction']),
        'stage_flag_bit8_set_path_observed': bool(events['stage_d1_set_bit8_instruction']),
        'reset_call_sites_seen': {k: events[k] for k in ('first_transition_reset_call','later_transition_reset_call')},
        'last_observed_event': records[-2].get('event') if len(records) > 1 else None,
        'last_observed_pc': records[-2].get('pc') if len(records) > 1 else None,
        'limits': [
          'CPU read-hook behavior must be independently verified inside actual Project64 3.x',
          'On-write hooks report pre-write state, not post-write values',
          'Last instrumented PC may differ from actual CPU PC at a freeze',
          'Manual freeze report does not independently prove a CPU stall or cause',
          'This is not a controlled normal-vs-held same-start-state comparison'
        ]
    }


def compare_pair(held, normal):
    if held[0].get('run')!='held_followthrough' or normal[0].get('run')!='normal_followthrough':
        raise ValueError('Expected held and normal runs in named positions')
    # Strict genuine matching-savestate comparator; does not ignore task-pointer changes.
    hs=held[0].get('state',{});ns=normal[0].get('state',{})
    keys=sorted(set(hs)|set(ns))
    # Controller input may differ after recording begins; only it is excluded.
    mismatch=[k for k in keys if k!='controller_buttons' and hs.get(k)!=ns.get(k)]
    return {'paired_start_state_equivalent_excluding_controller':not mismatch,
            'nonmatching_start_state_fields':mismatch,
            'held':analyze(held), 'normal':analyze(normal),
            'causal_inference_status':'CONTROLLED_START_OBSERVED_ONLY' if not mismatch else 'INCONCLUSIVE_DIFFERENT_START',
            'freeze_cause_proven':False}

def load(path):
    out = []
    with Path(path).open() as f:
        for i, line in enumerate(f, 1):
            if line.strip():
                try:
                    out.append(json.loads(line))
                except (ValueError, TypeError) as exc:
                    raise ValueError(f'Invalid JSONL at line {i}') from exc
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trace', type=Path, required=True)
    ap.add_argument('--out', type=Path, help='Sanitized aggregate JSON output')
    ap.add_argument('--normal', type=Path, help='Optional Phase4 normal-control JSONL, from the identical savestate')
    args = ap.parse_args()
    held=load(args.trace)
    result=compare_pair(held,load(args.normal)) if args.normal else analyze(held)
    text = json.dumps(result, indent=2) + '\n'
    if args.out:
        args.out.write_text(text)
    else:
        print(text, end='')

if __name__ == '__main__':
    main()
