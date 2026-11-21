"""USA N64 state and overlay image observer: read-only, evidence-tiered.

This module does NOT invent a guest frame counter, read a host PC, assume an
overlay request succeeded, or claim host polling is an atomic gameplay frame.
A debugger that pauses guest execution at a frame boundary may call
`capture_halted_frame` and supply its *actual* frame number and guest PC.

Only bounded N64 guest reads are performed. No process memory writes, no RAM
dumps, no unsafe warp/state modifications, and no original code bytes exported.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from typing import Any

FORMAT = 'goemon-usa-state-overlay-observations-v2'
FINGERPRINTS = Path(__file__).resolve().parent / 'research/usa_runtime_state_trace_20261121/overlay_fingerprints.json'
OVERLAY_VMA = 0x801CB460
OVERLAY_READ_LEN = 0x90
SYS_POINTER = 0x8015C5C8
SYS_EXPECTED = 0x8008CCC0
STATE_BASE = SYS_EXPECTED + 0x3ADD4  # 0x800C7A94
STATE_READ_LEN = 0x68
FLAG_9000 = SYS_EXPECTED + 0x3B07C # 0x800C7D3C
OVERLAY22_COUNTER = 0x801D7008
GATE_WORD = 0x800548D8
USA_ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'


def _u(buf: bytes, offset: int, length: int) -> int:
    return int.from_bytes(buf[offset:offset + length], 'big')


def load_fingerprints(path: Path = FINGERPRINTS) -> dict:
    db = json.loads(path.read_text(encoding='utf-8'))
    if db.get('format') != 'goemon-usa-overlay-text-fingerprints-v1' or db.get('identity_sha1') != USA_ROM_SHA1:
        raise ValueError('Unauthenticated USA overlay fingerprint database')
    records = db.get('records')
    if not isinstance(records, list) or len(records) != 8 or sorted(x['file_id'] for x in records) != [11, 13, 14, 15, 16, 20, 22, 23]:
        raise ValueError('Unexpected overlay group or file IDs')
    seen = set()
    for record in records:
        if record.get('guest_vma') != '0x801CB460' or record.get('window_offsets') != [0, 64, 128] or record.get('window_length') != 16:
            raise ValueError('Unrecognised overlay fingerprint geometry')
        windows = record.get('window_sha256')
        if not isinstance(windows, list) or len(windows) != 3 or any(len(x) != 64 or any(ch not in '0123456789abcdef' for ch in x) for x in windows):
            raise ValueError('Invalid fingerprint hashes')
        key = tuple(windows)
        if key in seen:
            raise ValueError('Ambiguous overlay fingerprints')
        seen.add(key)
    return db


def identify_image(guest_text: bytes, database: dict) -> dict:
    """Identify *bytes present*, not necessarily the currently executing file."""
    if len(guest_text) != OVERLAY_READ_LEN:
        raise OSError('Incomplete guest overlay signature window')
    for record in database['records']:
        offsets = record['window_offsets']
        length = record['window_length']
        found = [hashlib.sha256(guest_text[o:o+length]).hexdigest() for o in offsets]
        if found == record['window_sha256']:
            return {'image_file_id': record['file_id'], 'classification': 'exact_three_window_guest_code_image',
                    'active_resource_confirmed': False}
    return {'image_file_id': None, 'classification': 'unknown_or_unmapped_guest_code_image',
            'active_resource_confirmed': False}


def _read_checked(ram: Any, addr: int, size: int) -> bytes:
    raw = ram.read_guest(addr, size)
    if len(raw) != size:
        raise OSError(f'Incomplete guest RAM read at 0x{addr:08X}')
    return raw


def _raw_snapshot(ram: Any, fingerprints: dict) -> dict:
    ptr_before = _u(_read_checked(ram, SYS_POINTER, 4), 0, 4)
    if ptr_before != SYS_EXPECTED:
        raise ValueError(f'USA SYS pointer not validated: 0x{ptr_before:08X}')
    before = _read_checked(ram, STATE_BASE, STATE_READ_LEN)
    text_before = _read_checked(ram, OVERLAY_VMA, OVERLAY_READ_LEN)
    window_9000 = _u(_read_checked(ram, FLAG_9000, 2), 0, 2)
    image = identify_image(text_before, fingerprints)
    # Do not interpret file22-specific mutable state if code image is not file22.
    counter = _u(_read_checked(ram, OVERLAY22_COUNTER, 4), 0, 4) if image['image_file_id'] == 22 else None
    gate = _u(_read_checked(ram, GATE_WORD, 4), 0, 4)
    after = _read_checked(ram, STATE_BASE, STATE_READ_LEN)
    text_after = _read_checked(ram, OVERLAY_VMA, OVERLAY_READ_LEN)
    ptr_after = _u(_read_checked(ram, SYS_POINTER, 4), 0, 4)
    if (before != after or text_before != text_after or ptr_before != ptr_after):
        raise ValueError('Snapshot changed across guest reads; discard torn observation')
    return {'outer_state': before[0], 'stepw_end': before[1], 'secondary_state': before[2],
            'tertiary_state': before[3], 'vm_substate': before[0x3ADDE-0x3ADD4],
            'end_byte': before[0x3ADDF-0x3ADD4], 'map_id': _u(before, 0x3ADF2-0x3ADD4, 2),
            'room_group_selection': _u(before, 0x3ADF4-0x3ADD4, 2),
            'flag_9000_word': window_9000, 'file22_counter': counter,
            'gate_800548D8': gate, 'overlay': image}


def capture_poll(ram: Any, fingerprints: dict, *, elapsed_ms: int = 0) -> dict:
    """Read-only live *host poll*. Two stable reads != atomic guest frame."""
    values = _raw_snapshot(ram, fingerprints)
    return {'capture_kind': 'host_poll_non_atomic', 'guest_frame': None, 'guest_pc': None,
            'elapsed_ms': elapsed_ms, 'values': values,
            'limitation': 'Two stable reads check for torn data, but do not prove same-frame execution.'}


def capture_halted_frame(ram: Any, fingerprints: dict, *, frame: int, guest_pc: int,
                         proven_loader_file_id: int | None = None) -> dict:
    """Call only while an emulator/debugger has *actually halted* the guest.

    The caller, not this module, guarantees the frame boundary and authentic
    guest PC. The API deliberately does not claim source-level hook integration.
    A loader ID is accepted only from an independently instrumented, successful
    loader completion event for this very overlay region, not a guessed request.
    """
    if type(frame) is not int or frame < 0 or type(guest_pc) is not int or not 0x80000000 <= guest_pc < 0x80800000:
        raise ValueError('Frame index and guest PC must come from an actual halted guest')
    if proven_loader_file_id is not None and (type(proven_loader_file_id) is not int or proven_loader_file_id not in (11,13,14,15,16,20,22,23)):
        raise ValueError('Loader ID not in known overlay group')
    values = _raw_snapshot(ram, fingerprints)
    overlay = values['overlay']
    if overlay['image_file_id'] is not None:
        record = next(r for r in fingerprints['records'] if r['file_id'] == overlay['image_file_id'])
        code_size = int(record['rom_code_end'], 16) - int(record['rom_start'], 16)
        overlay['guest_pc_inside_fingerprinted_text'] = (OVERLAY_VMA <= guest_pc < OVERLAY_VMA + code_size)
        if overlay['guest_pc_inside_fingerprinted_text']:
            overlay['executing_code_image_file_id'] = overlay['image_file_id']
            overlay['execution_evidence'] = 'halted_guest_pc_inside_original_code_region_and_matching_code_image'
    if proven_loader_file_id is not None:
        if overlay['image_file_id'] != proven_loader_file_id:
            raise ValueError('Loader completion ID disagrees with guest overlay code image')
        overlay['active_resource_confirmed'] = True
        overlay['loader_provenance'] = 'caller_supplied_verified_loader_completion'
    return {'capture_kind': 'guest_halted_frame_callback', 'guest_frame': frame,
            'guest_pc': f'0x{guest_pc:08X}', 'values': values,
            'limitation': 'Atomicity and PC are guaranteed only by a genuinely halted emulator callback; this function cannot verify backend instrumentation.'}


def _edge(old: dict, new: dict) -> dict | None:
    x, y = old['values'], new['values']
    if x['outer_state'] == y['outer_state']:
        return None
    a,b=x['outer_state'],y['outer_state']
    observed = {'from': a, 'to': b,
                'earlier_overlay_image_file_id': x['overlay']['image_file_id'],
                'later_overlay_image_file_id': y['overlay']['image_file_id'],
                'from_secondary': x['secondary_state'], 'to_secondary': y['secondary_state'],
                'causal_attribution': 'NOT_PROVEN'}
    if (a,b)==(3,4) and x['overlay']['image_file_id']==22:
        observed['static_consistency'] = 'consistent_with_file22_overlay_state3_to4_path'
        observed['causal_attribution'] = 'NOT_PROVEN_NO_EXECUTED_PC_PROOF'
    return observed


def summarize(samples: list[dict], *, origin: str = 'read_only') -> dict:
    if len(samples) > 1_000_000:
        raise ValueError('Too many trace observations')
    events=[]
    previous=None
    for i, sample in enumerate(samples):
        if sample['capture_kind'] not in ('host_poll_non_atomic','guest_halted_frame_callback'):
            raise ValueError('Unknown capture type')
        if previous is not None:
            if previous['capture_kind'] == 'guest_halted_frame_callback' and sample['capture_kind'] == 'guest_halted_frame_callback':
                if sample['guest_frame'] <= previous['guest_frame']:
                    raise ValueError('Guest frames must be strictly increasing')
            transition=_edge(previous,sample)
            if transition:
                transition['observation_index']=i
                transition['sample_kind']=sample['capture_kind']
                events.append(transition)
            if previous['values']['map_id'] != sample['values']['map_id']:
                events.append({'observation_index': i,
                    'event': 'room_map_changed',
                    'elapsed_ms': sample.get('elapsed_ms'),
                    'from_map_id': previous['values']['map_id'],
                    'to_map_id': sample['values']['map_id'],
                    'from_room_group_selection': previous['values']['room_group_selection'],
                    'to_room_group_selection': sample['values']['room_group_selection'],
                    'outer_state_before': previous['values']['outer_state'],
                    'outer_state_after': sample['values']['outer_state'],
                    'earlier_overlay_image_file_id': previous['values']['overlay']['image_file_id'],
                    'later_overlay_image_file_id': sample['values']['overlay']['image_file_id'],
                    'limitation': 'Host polling may skip intermediate rooms or brief states; does not prove the writer.'})
            if previous['values']['overlay']['image_file_id'] != sample['values']['overlay']['image_file_id']:
                events.append({'observation_index':i,'event':'overlay_image_fingerprint_changed',
                    'from':previous['values']['overlay']['image_file_id'],
                    'to':sample['values']['overlay']['image_file_id'],
                    'limitation':'Image change does not identify the loader, instruction execution or resource lifecycle.'})
        previous=sample
    return {'format':FORMAT,'region':'USA','rom_identity':'user-supplied reference ROM fingerprints; running host ROM identity NOT authenticated',
            'origin':origin,'samples':len(samples),
            'sampling_evidence':'guest_frame_callback_requires_external_emulator_halt' if samples and all(x['capture_kind']=='guest_halted_frame_callback' for x in samples) else 'host_poll_not_same_frame',
            'observed_transitions':events,'observations':samples,
            'prohibitions':'No guest memory writes, no generated gameplay, no invented state labels, no raw RAM/code dumps.'}


def save_report(path: Path, report: dict):
    if path.exists():
        raise FileExistsError(f'Output already exists: {path}')
    if path.suffix != '.json':
        raise ValueError('Use a JSON output filename')
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as f:
        json.dump(report,f,indent=2,allow_nan=False)
        f.write('\n')


def record_pid(pid: int, fingerprints: dict, *, duration: float, interval: float,
               ram_base: int | None = None, endian: str = 'wordswapped') -> dict:
    """Use native Linux process_v_m_readv only; never open writable handles."""
    if duration <= 0 or duration > 1800 or interval < 0.005 or interval > 1:
        raise ValueError('Capture duration/interval outside safe bounds')
    from autosplitter.memory import Rdram, discover_rdram, HostProcess
    proc=HostProcess(pid, writable=False)
    try:
        if ram_base is None:
            ram_base, detected = discover_rdram(proc, endian)
            endian = detected
        ram=Rdram(proc, ram_base, endian)
        samples=[]
        failures=[]
        start=time.monotonic()
        until=start+duration
        while time.monotonic()<until:
            now=time.monotonic()
            try:
                samples.append(capture_poll(ram,fingerprints,elapsed_ms=round((now-start)*1000)))
            except (OSError,ValueError,RuntimeError) as e:
                if len(failures)<64:
                    failures.append({'elapsed_ms':round((now-start)*1000), 'reason':str(e)})
            time.sleep(interval)
        report=summarize(samples,origin='linux_process_read_only')
        report['requested_interval_ms']=round(interval*1000)
        report['capture_duration_ms']=round(duration*1000)
        report['rejected_samples']=failures
        report['rejected_count_capped']=len(failures)==64
        return report
    finally:
        proc.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pid',type=int,required=True,help='PID of an already running USA native recomp')
    parser.add_argument('--base',type=lambda x:int(x,0),help='Optional verified host RDRAM base')
    parser.add_argument('--endian',choices=['big','wordswapped'],default='wordswapped')
    parser.add_argument('--seconds',type=float,default=20.0)
    parser.add_argument('--interval-ms',type=float,default=20.0)
    parser.add_argument('--output',type=Path,required=True,help='New local JSON; never overwrites')
    args=parser.parse_args(argv)
    try:
        fingerprints=load_fingerprints()
        report=record_pid(args.pid,fingerprints,duration=args.seconds,interval=args.interval_ms/1000,
                          ram_base=args.base,endian=args.endian)
        save_report(args.output,report)
    except (OSError,ValueError,RuntimeError,PermissionError) as e:
        parser.exit(1,f'{e}\n')
    print(f'Recorded {report["samples"]} read-only non-atomic observations, {len(report["observed_transitions"])} changes; no in-game frame claims.')


if __name__=='__main__':main()
