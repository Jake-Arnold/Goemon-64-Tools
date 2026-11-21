#!/usr/bin/env python3
"""Fail-closed, original-ROM-authenticated IDO 5.3 native C stack diagnostics.

No original ROM, assembly, proprietary compiler or objects are distributed.
C variants with unused volatile local arrays are *diagnostic only*, not
accepted decompilation: matching the frame size doesn't match original code.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess

PIN='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
USA_SHA1='6ea0ed71032ce08fc2745f412d84936382197494'
FUN_SHA256='eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9'
START=0x69ECE4
SIZE=1808
FLAGS=['-c','-G','0','-non_shared','-Xfullwarn','-Xcpluscomm',
       '-Wab,-r4300_mul','-woff','649,838,712',
       '-D_LANGUAGE_C','-D_FINALROM','-DF3DEX_GBI','-D__sgi',
       '-DNDEBUG','-O2','-mips2']


def text_from_elf32_be(path):
    b=path.read_bytes()
    if b[:6]!=b'\x7fELF\x01\x02':raise ValueError('Expected original IDO ELF32 BE')
    shoff=struct.unpack_from('>I',b,0x20)[0]
    ent=struct.unpack_from('>H',b,0x2e)[0]
    num=struct.unpack_from('>H',b,0x30)[0]
    stridx=struct.unpack_from('>H',b,0x32)[0]
    if ent<40 or stridx>=num or shoff+num*ent>len(b):raise ValueError('Corrupt IDO ELF section table')
    strbase=struct.unpack_from('>I',b,shoff+stridx*ent+16)[0]
    for i in range(num):
        hdr=shoff+i*ent
        stroff=struct.unpack_from('>I',b,hdr)[0]
        if strbase+stroff>=len(b):raise ValueError('Invalid ELF name offset')
        name=b[strbase+stroff:b.index(0,strbase+stroff)]
        if name==b'.text':
            p,n=struct.unpack_from('>II',b,hdr+16)
            if p+n>len(b):raise ValueError('Invalid ELF text extent')
            return b[p:p+n]
    raise ValueError('No .text section in IDO object')


def stack_ops(data):
    counter=Counter()
    for k in range(0,len(data)-3,4):
        word=int.from_bytes(data[k:k+4],'big')
        op=word>>26
        base=(word>>21)&31
        if base!=29 or op not in (0x23,0x2b):continue
        imm=word&0xffff
        if imm&0x8000:imm-=0x10000
        counter[(imm,'load' if op==0x23 else 'store')]+=1
    return [{'offset':f'0x{k:X}',
             'loads':counter.get((k,'load'),0),'stores':counter.get((k,'store'),0)}
            for k in sorted({a for a,b in counter})]


def construct_probes(base):
    anchor='    s32 sp138;\n'
    if base.count(anchor)!=1:raise ValueError('Source anchor changed')
    single=base.replace(anchor, '    volatile s32 reserved_stack[20]; /* frame-size diagnostic, NOT original source */\n'+anchor,1)
    multi=base
    replacements=[
        ('    s32 sp138;\n','    s32 sp138;\n    volatile s32 reserved_below_row[13]; /* unused source-diagnostic */\n'),
        ('    s32 sp100;\n','    s32 sp100;\n    volatile s32 reserved_below_tile[3];\n'),
        ('    u16 *spE0;\n','    u16 *spE0;\n    volatile s32 reserved_below_pointers[2];\n'),
        ('    s32 sp34;\n','    s32 sp34;\n    volatile s32 reserved_below_pixel[1];\n')]
    for before,after in replacements:
        if multi.count(before)!=1:raise ValueError(f'Source anchor changed {before!r}')
        multi=multi.replace(before,after,1)
    return {'existing_m2c_baseline':base,
            'unused_storage_20_ints':single,
            'observed_gap_distribution_13_3_2_1':multi}


def analyze(original,generated):
    n=min(len(original),len(generated))//4
    matched=sum(original[i*4:i*4+4]==generated[i*4:i*4+4] for i in range(n))
    prefix=0
    while prefix<n and original[prefix*4:prefix*4+4]==generated[prefix*4:prefix*4+4]:prefix+=1
    frame_word=int.from_bytes(generated[:4],'big')
    if frame_word&0xffff0000!=0x27bd0000:raise ValueError('Not addiu $sp,$sp,IMM prologue')
    frame=-struct.unpack('>h',generated[2:4])[0]
    return {
      'original_function_bytes':len(original),'candidate_object_text_bytes':len(generated),
      'candidate_prologue_frame_bytes':frame,
      'first_consecutive_original_instruction_words_equal':prefix,
      'first_raw_mismatch_original_rom':f'0x{START+4*prefix:08X}' if prefix<n else None,
      'raw_original_words_equal':matched,'raw_original_positions_compared':n,
      'original_code_equal':len(original)==len(generated) and generated==original,
      'candidate_stack_word_accesses':stack_ops(generated),
      'relocation_resolution':'NOT_PERFORMED: raw ELF object .text vs linked original ROM',
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--checkout',type=Path,required=True)
    ap.add_argument('--deps',type=Path,required=True)
    ap.add_argument('--runtime',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    root=args.checkout.resolve()
    out=args.output.resolve()
    if out.exists():raise SystemExit(f'Refusing existing output directory: {out}')
    pin=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    if pin!=PIN:raise SystemExit(f'Wrong upstream original pin: {pin}')
    rom=(root/'config/usa/baserom.decompressed.z64').read_bytes()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=USA_SHA1:
        raise SystemExit('Wrong original USA decompressed ROM')
    original=rom[START:START+SIZE]
    if hashlib.sha256(original).hexdigest()!=FUN_SHA256:
        raise SystemExit('Wrong original large file22 function')
    compiled=(root/'tools/ido-5.3/cc')
    if not compiled.is_file():raise SystemExit('Pinned native IDO compiler unavailable')
    source=Path(__file__).resolve().parent/'file22_ido_trial.c'
    variants=construct_probes(source.read_text())
    env=os.environ.copy()
    env['PATH']=str(args.deps.resolve()/'bin')+os.pathsep+env.get('PATH','')
    env['LD_LIBRARY_PATH']=str(args.runtime.resolve()/'lib')+os.pathsep+env.get('LD_LIBRARY_PATH','')
    out.mkdir(parents=True)
    reports={}
    for name,text in variants.items():
        src=out/(name+'.c')
        obj=out/(name+'.o')
        src.write_text(text)
        proc=subprocess.run([str(compiled),*FLAGS,'-o',str(obj),str(src)],
            env=env,cwd=root,capture_output=True,text=True)
        (out/(name+'.compiler.log')).write_text(proc.stdout+'\n'+proc.stderr)
        if proc.returncode:raise RuntimeError(f'IDO failed {name}: {proc.returncode}')
        report=analyze(original,text_from_elf32_be(obj))
        report.update({'C_source_sha256':hashlib.sha256(text.encode()).hexdigest(),
                       'diagnostic_only':True,'no_original_C_promotion':True})
        reports[name]=report
    result={'status':'FAILED_NATIVE_RESEARCH_ONLY',
      'source_pin':pin,'original_USA_decompressed_sha1':USA_SHA1,
      'original_file22_function_sha256':FUN_SHA256,
      'original_stack_frame_bytes':320,
      'original_stack_word_accesses':stack_ops(original),
      'probes':reports,'any_native_exact':any(x['original_code_equal'] for x in reports.values()),
      'full_32MiB_G2':'NOT_RUN','accepted_C_delta':0}
    (out/'native_stack_study.json').write_text(json.dumps(result,indent=2)+'\n')
    for name,item in reports.items():
        print(f"{name:38s} frame={item['candidate_prologue_frame_bytes']} "
              f"prefix={item['first_consecutive_original_instruction_words_equal']} "
              f"raw={item['raw_original_words_equal']}/{item['raw_original_positions_compared']} "
              f"text={item['candidate_object_text_bytes']}/{len(original)} "
              f"first={item['first_raw_mismatch_original_rom']}")
    print('FAIL_CLOSED: all source variants are diagnostic only; no native C match or accepted promotion')
if __name__=='__main__':main()
