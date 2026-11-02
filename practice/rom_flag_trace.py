"""Read-only flag-reference index for the verified decompressed US ROM.

Reports GEV opcode patterns and optional bounded native JALR patterns, not an
exhaustive CFG/dataflow analysis. No ROM, dialogue text or game assets are bundled.
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
FLAG_HELPERS = {0x80024038:'set',0x80024088:'clear',0x800240DC:'test'}


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


def scan_indirect_calls(data,ranges,file_ids):
    """Conservative LUI/ADDIU/JALR patterns with a literal flag in the delay slot.

    Stops at control flow or target-register clobbering. Does not follow spilled
    pointers, nonliteral arguments, alternate constructions or prove reachability.
    File ranges may contain data, so matches still require manual review.
    """
    hits=[]
    def destination(word):
        op=word>>26
        if op==0:return (word>>11)&31
        if op in (*range(8,16),*range(32,40),48,52,55):return (word>>16)&31
        return None
    def control(word):
        return word>>26 in (1,2,3,4,5,6,7,20,21,22,23) or (word>>26==0 and word&63 in (8,9,12,13))
    for file_id,start,end in ranges:
        if file_id not in file_ids:continue
        for pos in range((start+3)&~3,end-3,4):
            word=struct.unpack_from('>I',data,pos)[0]
            if word>>26!=15 or word&0xffff!=0x8002:continue
            register=(word>>16)&31
            if register==0:continue
            target=None
            for step in range(pos+4,min(end-7,pos+48),4):
                item=struct.unpack_from('>I',data,step)[0]
                op=item>>26;rs=(item>>21)&31;rt=(item>>16)&31
                if op==0 and item&63==9 and rs==register and (item>>11)&31==31:
                    argument=struct.unpack_from('>I',data,step+4)[0]
                    if target in FLAG_HELPERS and argument>>26 in (9,13) and (argument>>21)&31==0 and (argument>>16)&31==4:
                        flag_id=argument&0xffff
                        if flag_id<FLAG_BYTES*8:
                            address,mask=flag_location(flag_id)
                            hits.append(dict(file_id=file_id,file_offset=f'0x{step-start:X}',
                                rom_offset=f'0x{step:X}',callee=f'0x{target:08X}',
                                operation=FLAG_HELPERS[target],flag_id=f'0x{flag_id:03X}',
                                address=f'0x{address:08X}',mask=f'0x{mask:02X}',
                                status='native_indirect_call_pattern_candidate'))
                    break
                if control(item):break
                if op==9 and rs==register and rt==register and target is None:
                    immediate=item&0xffff
                    target=(0x80020000+(immediate if immediate<0x8000 else immediate-0x10000))&0xffffffff
                elif destination(item)==register:break
                # Unknown/coproc formats are outside this small pattern matcher.
                elif op not in (0,*range(8,16),*range(32,44),46,48,52,55):break
    return hits


def analyze_rom(data,flag_ids=None,native_file_ids=()):
    digest=hashlib.sha1(data).hexdigest()
    if digest!=US_DECOMPRESSED_SHA1:
        if digest==US_RETAIL_SHA1:raise ValueError('Verified retail ROM is compressed; supply its decompressed research copy')
        raise ValueError('Unsupported ROM SHA-1; this analyzer requires the verified decompressed US ROM')
    ranges=file_ranges(data)
    references=scan_candidates(data,ranges,flag_ids)
    native=scan_indirect_calls(data,ranges,set(native_file_ids))
    if flag_ids is not None:native=[h for h in native if int(h['flag_id'],16) in set(flag_ids)]
    return dict(format='goemon-rom-flag-references-v1',rom_sha1=digest,
        identity='verified_decompressed_us',file_ranges=len(ranges),references=references,
        flags_with_references=len({h['flag_id'] for h in references}),native_references=native,
        limitations=['Aligned opcode patterns can include data false positives; manually trace before naming a flag.',
                     'Optional native scans recognize only bounded literal JALR patterns; no complete dataflow, placement analysis or script CFG.',
                     'No evidence of runtime behavior or verification of the ROM loaded by a running host.'])


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom',type=Path,required=True,help='Local verified decompressed US ROM')
    parser.add_argument('--flag-id',type=lambda value:int(value,0),action='append',help='Optional repeatable numeric event flag ID')
    parser.add_argument('--native-file-id',type=lambda value:int(value,0),action='append',default=[],help='Optional repeatable file ID for conservative native JALR patterns')
    parser.add_argument('--output',type=Path,required=True,help='Local JSON report; use ignored practice/diagnostics/')
    args=parser.parse_args(argv)
    try:
        if args.output.resolve()==args.rom.resolve():raise ValueError('Report path must differ from the ROM')
        report=analyze_rom(args.rom.read_bytes(),args.flag_id,args.native_file_id)
        # Exclusive creation prevents accidental replacement of research files.
        with args.output.open('x',encoding='utf-8') as stream:
            json.dump(report,stream,indent=2);stream.write('\n')
    except (OSError,ValueError) as exc:parser.exit(1,f'{exc}\n')
    print(f'{len(report["references"])} script / {len(report["native_references"])} native reference candidates; saved {args.output}')


if __name__=='__main__':main()
