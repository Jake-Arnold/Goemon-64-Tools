#!/usr/bin/env python3
"""Original-USA file22 MIPS opcode-shape alignment against an IDO object.

This is deliberately a WEAK alignment diagnostic: ignore register operands,
branch targets, and relocations (which are validated in the compiler probe).
The result is NOT an exact MIPS match or a proof of register equivalence.
Source-only, requires the user's authenticated original USA decompressed ROM.
"""
from __future__ import annotations
import argparse, collections, difflib, hashlib, json, struct
from pathlib import Path
from reproduce_compiled_ido import compiled_guest_text, code_stats, FUN_SHA256
from trace_original_file22_mips import ROM_SHA1

ROM_START=0x69ECE4
LENGTH=1808
VMA=0x801CC0C4
PHASES=[
 ('entry',0x801CC0C4,0x801CC128),
 ('outer_clipping',0x801CC128,0x801CC1AC),
 ('inner_clipping',0x801CC1AC,0x801CC234),
 ('tile_lookup',0x801CC234,0x801CC414),
 ('mode_selection',0x801CC414,0x801CC444),
 ('texture_mode_0',0x801CC444,0x801CC528),
 ('texture_mode_1',0x801CC528,0x801CC620),
 ('texture_mode_2',0x801CC620,0x801CC70C),
 ('texture_rectangle',0x801CC70C,0x801CC780),
 ('inner_tail',0x801CC780,0x801CC790),
 ('outer_tail',0x801CC790,0x801CC7D4),
]

def shape(word):
    op=word>>26
    rt=(word>>16)&31
    funct=word&63
    shamt=(word>>6)&31
    immediate=word&65535
    if op==0:
        if funct in (0,2,3):return ('SHIFT',funct,shamt)
        if funct in (0x1A,0x1B,0x18,0x19,0xD,0x8,0x9,0x10,0x12):return ('SPECIAL',funct)
        return ('R',funct)
    if op==1:return ('REGIMM',rt)
    if op in (2,3,4,5,6,7,20,21,22,23):return ('BRANCH',op)
    if op in (0x20,0x21,0x23,0x24,0x25,0x28,0x29,0x2B):return ('MEM',op,immediate)
    if op in (8,9,10,11,12,13,14,15):return ('IMM',op,immediate)
    return ('OTHER',op)

def align(original,compiled):
    base=[shape(w) for (w,) in struct.iter_unpack('>I',original)]
    candidate=[shape(w) for (w,) in struct.iter_unpack('>I',compiled)]
    matcher=difflib.SequenceMatcher(a=base,b=candidate,autojunk=False)
    blocks=matcher.get_matching_blocks()
    paired={a+k:b+k for a,b,n in blocks for k in range(n)}
    phases=[]
    for name,start,end in PHASES:
        first=(start-VMA)//4
        last=(end-VMA)//4
        phases.append({'name':name,'original_start':hex(start),'original_end_exclusive':hex(end),
            'original_instructions':last-first,
            'ordered_opcode_shape_matches':sum(i in paired for i in range(first,last))})
    total=sum(n for a,b,n in blocks)
    return {'original_instructions':len(base),'candidate_instructions':len(candidate),
        'ordered_opcode_shape_matches':total,'ordered_opcode_shape_fraction':round(total/len(base),6),
        'register_operands_ignored':True,'branch_targets_ignored':True,
        'phase_breakdown':phases}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--usa',required=True,type=Path)
    p.add_argument('--object',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    if a.output.exists():raise FileExistsError('Use new output file')
    rom=a.usa.read_bytes()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=ROM_SHA1:raise ValueError('Wrong original USA image')
    original=rom[ROM_START:ROM_START+LENGTH]
    if hashlib.sha256(original).hexdigest()!=FUN_SHA256:raise ValueError('Wrong original target function')
    compiled=compiled_guest_text(a.object)
    results=align(original,compiled)
    stats=code_stats(original,compiled)
    results['candidate_text_bytes']=len(compiled)
    results['original_text_bytes']=len(original)
    results['native_exact']=compiled==original
    results['candidate_stack_frame']=stats['candidate_frame_bytes']
    results['matching_consecutive_entry_words']=stats['matching_consecutive_entry_words']
    results['matching_raw_word_positions']=stats['matching_raw_word_positions']
    results['original_F300_lui']=stats['original_lui_F300']
    results['candidate_F300_lui']=stats['candidate_lui_F300']
    results['original_E700_lui']=stats['original_lui_E700']
    results['candidate_E700_lui']=stats['candidate_lui_E700']
    a.output.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k!='phase_breakdown'},indent=2))
if __name__=='__main__':main()
