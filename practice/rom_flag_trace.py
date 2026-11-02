"""Read-only flag-reference index for the verified decompressed US ROM.

Reports aligned GEV opcode-pattern candidates, not an exhaustive script CFG or
native-code analysis. No ROM, dialogue text, RAM dump or game assets are bundled.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
import hashlib
import json
from pathlib import Path
import struct

US_RETAIL_SHA1 = 'df8083a54296b8c151917c5333e1c85f014a2a66'
US_DECOMPRESSED_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
FLAG_BASE = 0x8015C608
FLAG_BYTES = 0x64
OPERATIONS = {0x8020:'set',0x8021:'clear',0x8022:'branch_if_set'}


def flag_location(flag_id):
    if type(flag_id) is not int or not 0<=flag_id<FLAG_BYTES*8:
        raise ValueError('Flag ID must be inside the primary 100-byte event field')
    return FLAG_BASE+(flag_id>>3),1<<(flag_id&7)


def file_ranges(data):
    """Return one-based file IDs and decompressed offsets; final entry is an end marker."""
    signature=b'Nisitenma-Ichigo'
    offset=data.find(signature)
    if offset<0:raise ValueError('ROM file table signature missing')
    if data.find(signature,offset+1)>=0:raise ValueError('Ambiguous ROM file table signature')
    position=offset+len(signature);entries=[]
    while position+4<=len(data):
        value=struct.unpack_from('>I',data,position)[0];position+=4
        if value==0:break
        if value&0x80000000:raise ValueError('Compressed file entry; decompress the ROM first')
        if value>len(data) or (entries and value<entries[-1]):
            raise ValueError('Invalid file-table offsets')
        entries.append(value)
    else:raise ValueError('Unterminated file table')
    if len(entries)<2:raise ValueError('File table has no file ranges')
    return [(i+1,start,end) for i,(start,end) in enumerate(zip(entries,entries[1:])) if end>start]


def scan_candidates(data,ranges,flag_ids=None):
    """Pattern candidates only; native writes and unrecognized encodings are excluded."""
    wanted=None if flag_ids is None else set(flag_ids)
    if wanted is not None:
        for flag_id in wanted:flag_location(flag_id)
    starts=[start for _,start,_ in ranges]
    if starts!=sorted(starts):raise ValueError('File ranges must be sorted')
    hits=[]
    for position in range(0,len(data)-7,4):
        op,flag_id=struct.unpack_from('>II',data,position)
        if op not in OPERATIONS or flag_id>=FLAG_BYTES*8 or (wanted is not None and flag_id not in wanted):
            continue
        index=bisect_right(starts,position)-1
        if index<0:continue
        file_id,start,end=ranges[index]
        size=12 if op==0x8022 else 8
        if position+size>end:continue
        address,mask=flag_location(flag_id)
        hit=dict(file_id=file_id,file_offset=f'0x{position-start:X}',
                 rom_offset=f'0x{position:X}',flag_id=f'0x{flag_id:03X}',
                 address=f'0x{address:08X}',mask=f'0x{mask:02X}',
                 operation=OPERATIONS[op],status='opcode_pattern_candidate')
        if op==0x8022:
            target=struct.unpack_from('>I',data,position+8)[0]
            # These three mapped scenario files use segmented 0x08 local targets.
            # Other prefixes may be valid elsewhere, but are not silently resolved.
            local=target&0xffffff
            hit['branch_target']=f'0x{target:08X}'
            hit['local_branch_rom_offset']=(f'0x{start+local:X}'
                if target>>24==8 and local<end-start else None)
        hits.append(hit)
    return hits


def analyze_rom(data,flag_ids=None):
    digest=hashlib.sha1(data).hexdigest()
    if digest!=US_DECOMPRESSED_SHA1:
        if digest==US_RETAIL_SHA1:raise ValueError('Verified retail ROM is compressed; supply its decompressed research copy')
        raise ValueError('Unsupported ROM SHA-1; this analyzer requires the verified decompressed US ROM')
    ranges=file_ranges(data)
    references=scan_candidates(data,ranges,flag_ids)
    return dict(format='goemon-rom-flag-references-v1',rom_sha1=digest,
        identity='verified_decompressed_us',file_ranges=len(ranges),references=references,
        flags_with_references=len({h['flag_id'] for h in references}),
        limitations=['Aligned opcode patterns can include data false positives; manually trace before naming a flag.',
                     'No native instruction dataflow, actor placement analysis or complete script control-flow graph.',
                     'No evidence of runtime behavior or verification of the ROM loaded by a running host.'])


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom',type=Path,required=True,help='Local verified decompressed US ROM')
    parser.add_argument('--flag-id',type=lambda value:int(value,0),action='append',help='Optional repeatable numeric event flag ID')
    parser.add_argument('--output',type=Path,required=True,help='Local JSON report; use ignored practice/diagnostics/')
    args=parser.parse_args(argv)
    try:
        if args.output.resolve()==args.rom.resolve():raise ValueError('Report path must differ from the ROM')
        report=analyze_rom(args.rom.read_bytes(),args.flag_id)
        # Exclusive creation prevents accidental replacement of research files.
        with args.output.open('x',encoding='utf-8') as stream:
            json.dump(report,stream,indent=2);stream.write('\n')
    except (OSError,ValueError) as exc:parser.exit(1,f'{exc}\n')
    print(f'{len(report["references"])} reference candidates across {report["flags_with_references"]} flags; saved {args.output}')


if __name__=='__main__':main()
