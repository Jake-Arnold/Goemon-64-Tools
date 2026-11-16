#!/usr/bin/env python3
"""Fail-closed research gate for 143 original-USA file_11 matching-C functions.

This deliberately does *not* modify the decomp production manifest or certify
its separate main/other-overlay 160 matching-C functions. It builds into a new
private scratch checkout and compares all original ROM bytes and file11 relocs.

Run with the pinned portable Python 3.12/Splat runtime and MIPS binutils:
 python verify_file11_143.py --upstream /path/to/pinned/mnsg-japan \
   --workdir /tmp/goemon-file11-143-fresh \
   --splat-script /path/to/goemon-dependencies/.venv/bin/splat \
   --report /tmp/goemon-file11-143-fresh-proof.json

The upstream checkout must already have an exact pristine USA baseline build.
No ROM, original assembly, toolchain or compiled output belongs in Git.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys

HERE=Path(__file__).resolve().parent
FIXTURE=HERE/'file11_143_source_fixture.json'
ROM_SHA1='6ea0ed71032ce08fc2745f412d84936382197494'
ELF_SHA256='83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038'
ASM_SHA256='e936f86295b8d8795369fd6db6a42da5b13184b9856058878066b9448e4a5f8b'
PREFIX='goemon-file11-143-exact-staging-candidate-v1'
START=0x587370
END=0x5B8500


def sha(data:bytes,algo='sha256')->str:
    return hashlib.new(algo,data).hexdigest()


def run(command, *, cwd=None, env=None)->str:
    result=subprocess.run(list(map(str,command)),cwd=cwd,env=env,text=True,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"Command failed {command[0]} ({result.returncode}):\n{result.stdout[-14000:]}")
    return result.stdout


def read_symbols(path:Path)->dict[str,tuple[int,int]]:
    rows={}
    for line in run(['readelf','-Ws',path]).splitlines():
        match=re.search(r'\s([0-9a-fA-F]{8})\s+(\d+) FUNC\s+GLOBAL\s+DEFAULT\s+\d+\s+(func_[0-9A-Fa-f]+_[0-9A-Fa-f]+)\s*$',line)
        if match:
            vma,size,name=int(match[1],16),int(match[2]),match[3]
            if name in rows and rows[name]!=(vma,size):
                raise ValueError(f'Conflicting original FUNC symbols: {name}')
            rows[name]=(vma,size)
    return rows


def read_relocations(path:Path):
    output=run(['readelf','-Wr',path])
    hit=re.search(r"Relocation section '\.rel\.file_11'[^\n]* contains (\d+) entries:\n(.*?)(?=\nRelocation section '|\Z)",output,re.S)
    if not hit:
        raise ValueError('Missing .rel.file_11')
    out=[]
    for line in hit[2].splitlines():
        fields=line.split()
        if len(fields)>4 and fields[2].startswith('R_MIPS_'):
            out.append((int(fields[0],16),fields[2],int(fields[3],16)))
    if len(out)!=int(hit[1]):raise ValueError('Relocation parse/count failure')
    return out


def checked_fixture(original_rom:bytes,original_elf:Path,original_asm:Path):
    f=json.loads(FIXTURE.read_text())
    if (f.get('format')!=PREFIX or f.get('upstream_commit')!='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
         or f.get('original_rom_sha1')!=ROM_SHA1 or f.get('original_elf_sha256')!=ELF_SHA256
         or f.get('original_asm_sha256')!=ASM_SHA256 or f.get('file11_relocations')!=8825
         or f.get('rom_length')!=0x2000000 or f.get('overlay_text_start')!=START
         or f.get('overlay_text_end')!=END or f.get('production_promotion_count')!=0):
        raise ValueError('Unexpected promotion candidate identity/contract')
    if len(original_rom)!=0x2000000 or sha(original_rom,'sha1')!=ROM_SHA1:
        raise ValueError('Wrong original 32 MiB USA ROM')
    if sha(original_elf.read_bytes())!=ELF_SHA256:raise ValueError('Wrong pristine baseline ELF')
    if sha(original_asm.read_bytes())!=ASM_SHA256:raise ValueError('Wrong original 906-function Splat assembly')
    symbols=read_symbols(original_elf)
    chunks=f['chunks'];expect_start=START;seen=set();all_functions=[]
    for c in chunks:
        start,end=c['rom_start'],c['rom_end'];kind=c['kind']
        if (start!=expect_start or end<=start or end>END or start%4 or end%4
              or c['size']!=end-start or kind not in ('c','asm')
              or sha(original_rom[start:end])!=c['original_sha256']):
            raise ValueError(f'Invalid or overlapping original-ROM chunk: {c.get("name")}')
        if kind=='c':
            source=c.get('source');name=c.get('name')
            if (not isinstance(source,str) or not isinstance(name,str)
                  or any(x in source for x in ('GLOBAL_ASM','#include'))
                  or sha(source.encode())!=c['source_sha256']):
                raise ValueError('Unreviewed C source data')
            off=start
            for fn in c['functions']:
                if (fn['off']!=off or fn['name'] in seen or fn['size']<=0
                      or fn['vma']!=0x801CB460+off-START
                      or symbols.get(fn['name'])!=(fn['vma'],fn['size'])
                      or fn['name'] not in source):
                    raise ValueError('Wrong function identity, offset or source')
                seen.add(fn['name']);all_functions.append(fn)
                off+=fn['size']
            if off!=end:raise ValueError('Function group has missing assembly')
        else:
            if c.get('name') is not None:raise ValueError('Unexpected ASM ownership')
        expect_start=end
    if expect_start!=END or len(all_functions)!=143 or sum(c['size'] for c in chunks if c['kind']=='c')!=3908:
        raise ValueError('Incorrect original contiguous overlay coverage')
    if (sum(1 for x in chunks if x['kind']=='c')!=44
        or f['total_represented_functions']!=143 or f['new_covered_functions_beyond_existing_50']!=93
        or f['original_file11_stage_c_functions']!=50 or f['wave1_research_functions_covered']!=77
        or f['wave45_additional_functions_beyond_wave1']!=16):
        raise ValueError('Unexpected discovered vs already-promoted function count')
    return f,all_functions


def trim_text_object(data:bytes,original_size:int)->bytes:
    raw=bytearray(data)
    if len(raw)<52 or raw[:4]!=b'\x7fELF' or raw[4]!=1 or raw[5]!=2 or struct.unpack_from('>H',raw,18)[0]!=8:
        raise ValueError('Expected ELF32 big-endian MIPS object')
    shoff,=struct.unpack_from('>I',raw,32)
    ents,number,str_idx=struct.unpack_from('>HHH',raw,46)
    if ents<40 or number==0 or str_idx>=number or shoff+number*ents>len(raw):
        raise ValueError('Invalid ELF section headers')
    header=lambda n:shoff+n*ents
    soff,ssz=struct.unpack_from('>II',raw,header(str_idx)+16)
    if soff+ssz>len(raw):raise ValueError('Section string table exceeds file')
    sections={}
    for i in range(number):
        h=header(i);n,=struct.unpack_from('>I',raw,h)
        if n>=ssz:raise ValueError('Bad section name')
        k=raw[soff+n:raw.index(0,soff+n,soff+ssz)].decode('ascii')
        sections[k]=h
    if '.text' not in sections:raise ValueError('Missing .text section')
    t=sections['.text'];start,size=struct.unpack_from('>II',raw,t+16)
    if size<original_size or size-original_size>12 or start+size>len(raw) or original_size%4:
        raise ValueError('Compiler object .text size differs outside allowable final padding')
    if any(raw[start+original_size:start+size]):raise ValueError('Nonzero code tail cannot be trimmed')
    if '.rel.text' in sections:
        r=sections['.rel.text'];rtype,=struct.unpack_from('>I',raw,r+4)
        roff,rlength=struct.unpack_from('>II',raw,r+16)
        if rtype!=9 or rlength%8 or roff+rlength>len(raw):raise ValueError('Bad relocation section')
        for at in range(roff,roff+rlength,8):
            loc,=struct.unpack_from('>I',raw,at)
            if loc>=original_size:raise ValueError('Trim would discard a relocation')
    struct.pack_into('>I',raw,t+20,original_size)
    struct.pack_into('>I',raw,t+32,4)
    return bytes(raw)


def stage_config(checkout:Path,f:dict):
    cfg=checkout/'config/usa/splat.yaml'
    txt=cfg.read_text()
    i=txt.index('  - name: file_11');j=txt.index('  - name: file_12',i)
    blk=txt[i:j]
    old='    - [0x587370, asm]\n    - [0x5B8500, data]'
    if blk.count(old)!=1 or blk.count('subalign: 16')!=1:
        raise ValueError('Pinned upstream file_11 SPLAT config no longer pristine')
    line=lambda c:f'    - [0x{c["rom_start"]:X}, {c["kind"]}'+(f', {c["name"]}' if c['kind']=='c' else '')+']'
    repl='\n'.join(map(line,f['chunks']))+'\n    - [0x5B8500, data]'
    cfg.write_text(txt[:i]+blk.replace(old,repl)+txt[j:])
    for c in f['chunks']:
        if c['kind']=='c':
            dest=checkout/'src'/(c['name']+'.c')
            if dest.exists():raise ValueError('Candidate source file name collision')
            dest.write_text(c['source'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream',required=True,type=Path)
    parser.add_argument('--workdir',required=True,type=Path)
    parser.add_argument('--splat-script',required=True,type=Path)
    parser.add_argument('--report',required=True,type=Path)
    parser.add_argument('--jobs',type=int,default=8)
    a=parser.parse_args()
    if a.workdir.exists() or a.report.exists():
        parser.error('Refusing to overwrite an existing scratch checkout or proof report')
    if not 1<=a.jobs<=32:parser.error('jobs must be 1..32')
    upstream=a.upstream.resolve()
    git_head=run(['git','rev-parse','HEAD'],cwd=upstream).strip()
    if git_head!='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee':
        raise ValueError('Wrong source revision: '+git_head)
    original_rom=(upstream/'config/usa/baserom.decompressed.z64').read_bytes()
    base_elf=upstream/'build/usa/mnsg.elf'
    f,functions=checked_fixture(original_rom,base_elf,upstream/'asm/usa/587370.s')
    if (upstream/'build/usa/mnsg.z64').read_bytes()!=original_rom:
        raise ValueError('Pristine upstream is not itself an exact baseline ROM build')
    original_relocs=read_relocations(base_elf)
    if len(original_relocs)!=8825:raise ValueError('Original relocation count differs')
    # Copy private source/built baseline, never rewrite the user's checked out tree.
    shutil.copytree(upstream,a.workdir,ignore=shutil.ignore_patterns('.git','*.encoded.c','*.encoded.s'))
    stage_config(a.workdir,f)
    env=os.environ.copy()
    run([sys.executable,a.splat_script,'split','config/usa/splat.yaml'],cwd=a.workdir,env=env)
    targets=[('build/usa/src/'+c['name']+'.c.o') if c['kind']=='c'
             else ('build/usa/asm/usa/'+f'{c["rom_start"]:X}'+'.s.o') for c in f['chunks']]
    run(['make','-j'+str(a.jobs),'VERSION=usa',*targets],cwd=a.workdir,env=env)
    changes=[]
    for c,target in zip(f['chunks'],targets):
        path=a.workdir/target
        raw=path.read_bytes()
        trimmed=trim_text_object(raw,c['size'])
        if sha(trimmed)!=c['trimmed_obj_sha256']:
            raise ValueError('Native compiled object diverged: '+target)
        changes.append((path,trimmed))
    # Validate everything before modifying even scratch overlay objects.
    linker=a.workdir/'.splat/usa/mnsg.ld'
    script=linker.read_text()
    old='.file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(16)'
    if script.count(old)!=1:raise ValueError('File_11 linker alignment differs')
    for path,content in changes:path.write_bytes(content)
    linker.write_text(script.replace(old,old.replace('SUBALIGN(16)','SUBALIGN(4)')))
    for suffix in ('.elf','.z64'):
        p=a.workdir/'build/usa'/('mnsg'+suffix)
        if p.exists():p.unlink()
    run(['make','-j'+str(a.jobs),'VERSION=usa','build/usa/mnsg.z64'],cwd=a.workdir,env=env)
    candidate=a.workdir/'build/usa/mnsg.z64'
    if candidate.read_bytes()!=original_rom or sha(candidate.read_bytes(),'sha1')!=ROM_SHA1:
        raise ValueError('Full 33,554,432-byte USA ROM mismatch')
    candidate_elf=a.workdir/'build/usa/mnsg.elf'
    relocs=read_relocations(candidate_elf)
    if len(relocs)!=8825 or Counter(relocs)!=Counter(original_relocs):
        raise ValueError('Relocation identity multiset mismatch')
    actual_symbols=read_symbols(candidate_elf)
    for fn in functions:
        if actual_symbols.get(fn['name'])!=(fn['vma'],fn['size']):
            raise ValueError('Linked function original address/size mismatch: '+fn['name'])
    report={'format':'goemon-file11-143-full-rom-reproduction-v1','original_usa_rom_sha1':ROM_SHA1,
            'original_elf_sha256':ELF_SHA256,'pinned_original_asm_sha256':ASM_SHA256,
            'file11_c_functions_original_address_exact':len(functions),
            'file11_original_C_instruction_bytes':3908,'additional_beyond_production_50':93,
            'file11_relocation_records_original':len(original_relocs),
            'file11_relocation_records_candidate':len(relocs),
            'semantic_relocations_match':True,'whole_rom_bytes_compared':len(original_rom),
            'whole_rom_byte_exact':True,'combined_210_plus_207_production_g2_ran':False,
            'production_promotion_claims':0,'scope':'pristine_USA_source_plus_file11_only'}
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 143 original-address C functions / 3,908 bytes; 32 MiB USA ROM exact; 8,825 relocation identities exact')
    print('Research proof only; not the current 210+207 central production G2 promotion')

if __name__=='__main__':main()
