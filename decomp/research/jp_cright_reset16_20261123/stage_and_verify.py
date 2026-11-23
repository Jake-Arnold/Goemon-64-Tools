#!/usr/bin/env python3
"""Fail-closed original-JP reset16 C research: pure staging and native proof.

Only modifies a PRIVATE scratch copy of the user-owned pinned Japanese build.
Does NOT change/patch original ROM instructions or ELF relocation records.
An IDO/asm-processor quirk adds four unowned zero bytes to one ASM FUNC size;
size-metadata-only correction is allowed with exact source and ELF checks.
"""
from __future__ import annotations
import argparse,hashlib,json,re,struct,subprocess,shutil,sys
from pathlib import Path

ROM_SHA='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
C_SHA='d59c3bfbd24ae69e442f47ee0bc95ac7571dd4b0e1e1e9dd93b93409435e2b5d'
MIX_SHA='9b18b98e732c2ec2d5a3f356833a72835cca54d0d188e1bded385eb058b89d7b'
NATIVE_OBJ_SHA='d586274c332ea1c3c9b8b0400e1b9ea1c1d7d5eb95999e482310e34b9a8902ad'
PACK_OBJ_SHA='d4829d4b13885a486041e9c6e9bfafa8705e6c479b97275c278d825a3cf160f0'
CODE_SHA='2b5316356ac165deed76b9e3a59026a2060b0267acf26cbf62014560510f00a1'
REL_SHA='43a133b21ac2b18d8e1d00f8c4e5718776b001a1f45c54e807dae12165e797c0'
ROM_OFF=0x4D70
NAMES=[('func_80004170_4D70',0x3C),('func_800041AC_4DAC',0x30),
       ('func_800041DC_4DDC',0x48),('func_80004224_4E24',0x48),
       ('func_8000426C_4E6C',0x5D0)]
ORIG='asm/japan_0/main_4D70.s'
STAGED='src/jpcright_resetmixed.c'
ASM_SUB='asm/japan_0/nonmatchings/jpcright_resetmixed'
STAGE='build/japan_0/cright-reset16-stage.json'
ROM='config/japan_0/baserom.decompressed.z64'

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def original(co:Path)->bytes:
    x=(co/ROM).read_bytes()
    if len(x)!=33554432 or hashlib.sha1(x).hexdigest()!=ROM_SHA or sha(x[ROM_OFF:ROM_OFF+60])!=CODE_SHA:
        raise ValueError('FAILED_INPUT: wrong authenticated Japanese ROM/function')
    return x

def read_source()->bytes:
    p=Path(__file__).resolve().parent/'source/func_80004170_4D70.c'
    s=p.read_bytes()
    if sha(s)!=C_SHA:raise ValueError('Unreviewed C body')
    return s

def render_fragments(original_source:str)->tuple[bytes,list[tuple[str,str]]]:
    # Splat original ASM has one header plus precisely these five sequential
    # ROM-owned functions. Do not embed the source ASM in any release package.
    ms=list(re.finditer(r'(?m)^nonmatching (func_[A-Za-z0-9_]+), 0x([0-9A-Fa-f]+)\s*$',original_source))
    if [(m[1],int(m[2],16)) for m in ms]!=NAMES:
        raise ValueError('Original five-function owner/order/length changed')
    if not original_source.startswith('.include "macro.inc"'):
        raise ValueError('Unexpected assembler owner header')
    entries=[]
    for index,m in enumerate(ms):
        start=m.start();end=ms[index+1].start() if index+1<len(ms) else len(original_source)
        name=m[1];span=original_source[start:end]
        if span.count('glabel '+name)!=1 or span.count('endlabel '+name)!=1:
            raise ValueError('Unreviewed original asm block '+name)
        # Original function comments contain each original ROM offset and
        # MIPS instruction; count without copying code into the release.
        instr=re.findall(r'(?m)^\s*/\*\s*([0-9A-Fa-f]+)\s+([0-9A-Fa-f]+)\s+[0-9A-Fa-f]{8}\s*\*/',span)
        expected_words=NAMES[index][1]//4
        # The final original unit carries one unowned linker-pad NOP after
        # its 1488-byte FUNC endlabel; exact original ROM address 0x543C.
        if index==len(NAMES)-1:
            if (len(instr)!=expected_words+1 or instr[-1]!=('543C','8000483C')
                    or 'endlabel '+name not in span
                    or not re.search(r'/\* 543C 8000483C 00000000 \*/\s+nop\s*$',span)):
                raise ValueError('Original final 4-byte zero padding changed')
        elif len(instr)!=expected_words:
            raise ValueError('ASM instruction count does not match original function '+name)
        expected_rom=ROM_OFF+sum(length for _,length in NAMES[:index])
        expected_guest=0x80000400+expected_rom-0x1000
        if int(instr[0][0],16)!=expected_rom or int(instr[0][1],16)!=expected_guest:
            raise ValueError('Unexpected ASM function address '+name)
        if not all(int(instr[i+1][0],16)==int(instr[i][0],16)+4 and
                   int(instr[i+1][1],16)==int(instr[i][1],16)+4 for i in range(len(instr)-1)):
            raise ValueError('Noncontiguous original MIPS words/guest VMAs')
        entries.append((name,span))
    c=read_source()+b'\n'+''.join(f'#pragma GLOBAL_ASM("{ASM_SUB}/{n}.s")\n' for n,_ in entries[1:]).encode()
    if sha(c)!=MIX_SHA:raise ValueError('Generated C/ASM pragma source changed')
    return c,entries[1:]

def stage(co:Path):
    co=co.resolve();rom=original(co)
    if (co/'build/japan_0/mnsg.z64').read_bytes()!=rom:
        raise ValueError('Must stage on exact accepted Japanese ROM build')
    if (co/STAGE).exists() or (co/STAGED).exists() or (co/ASM_SUB).exists():
        raise FileExistsError('Scratch stage already exists; no overwrite')
    src=(co/ORIG).read_text()
    compiled,fragments=render_fragments(src)
    ld=co/'.splat/japan_0/mnsg.ld';text=ld.read_text()
    expected_main_prefix='.main 0x80000450 : AT(main_ROM_START) SUBALIGN('
    # The accepted JP2370 baseline already uses the reviewed SUBALIGN(4)
    # in japan_thirtyfour_c. The pristine original-ASM layout uses 16.
    # Both are allowed ONLY when the baseline ROM is already exact; this
    # staged conversion never changes the linker subalignment.
    if sum(text.count(expected_main_prefix+str(a)+')') for a in (4,16))!=1:
        raise ValueError('Unreviewed original main linker alignment')
    # Original main source owns no dynamic data payload; the standalone
    # main_4D70.data.s.o is a distinct owner and remains untouched.
    for sec in ('.text','.rodata','.bss'):
        old=f'build/japan_0/asm/japan_0/main_4D70.s.o({sec});'
        if text.count(old)!=1:raise ValueError('Ambiguous original owner '+sec)
        text=text.replace(old,f'build/japan_0/src/jpcright_resetmixed.c.o({sec});',1)
    if 'build/japan_0/asm/japan_0/main_4D70.s.o(' in text:
        raise ValueError('Unreviewed original object has additional link sections')
    path=co/ASM_SUB;path.mkdir(parents=True)
    for name,fragment in fragments:(path/(name+'.s')).write_text(fragment)
    (co/STAGED).write_bytes(compiled)
    ld.write_text(text)
    output={'status':'STAGED_ONLY','target':NAMES[0][0],'source_sha256':C_SHA,
            'mixed_source_sha256':MIX_SHA,'old_asm_source_sha256':sha(src.encode()),
            'original_ROM_sha1':ROM_SHA,'separate_asm_fragments':len(fragments),
            'original_asm_symbols':[name for name,_ in NAMES],'linker_sha256':sha(text.encode())}
    (co/STAGE).write_text(json.dumps(output,indent=2)+'\n')
    return output

def repair(co:Path):
    co=co.resolve();x=json.loads((co/STAGE).read_text())
    if x['mixed_source_sha256']!=sha((co/STAGED).read_bytes()) or x['source_sha256']!=C_SHA:
        raise ValueError('Staged source changed')
    p=co/'build/japan_0/src/jpcright_resetmixed.c.o'
    orig=p.read_bytes()
    if sha(orig)!=NATIVE_OBJ_SHA:raise ValueError('Original native toolchain/mixed object drift')
    data=bytearray(orig)
    if data[:6]!=b'\x7fELF\x01\x02' or struct.unpack_from('>H',data,16)[0]!=1:
        raise ValueError('Expected big endian relocatable ELF32')
    shoff=struct.unpack_from('>I',data,32)[0];entsz=struct.unpack_from('>H',data,46)[0];n=struct.unpack_from('>H',data,48)[0]
    if entsz!=40 or shoff+n*entsz>len(data):raise ValueError('Malformed native ELF sections')
    ss=[]
    for i in range(n):
        o=shoff+i*40
        ss.append({'type':struct.unpack_from('>I',data,o+4)[0],
                   'flags':struct.unpack_from('>I',data,o+8)[0],
                   'off':struct.unpack_from('>I',data,o+16)[0],
                   'size':struct.unpack_from('>I',data,o+20)[0],
                   'link':struct.unpack_from('>I',data,o+24)[0],
                   'entsize':struct.unpack_from('>I',data,o+36)[0]})
    ts=[s for s in ss if s['type']==1 and s['flags']==6]
    syms=[s for s in ss if s['type']==2]
    if len(ts)!=1 or len(syms)!=1:raise ValueError('Nonunique original .text or .symtab')
    t=ts[0];s=syms[0]
    if t['size']!=0x6D0 or s['entsize']!=16 or data[t['off']+0x6CC:t['off']+0x6D0]!=b'\0'*4:
        raise ValueError('Last four bytes are not original zero padding')
    strings=ss[s['link']]; names=bytes(data[strings['off']:strings['off']+strings['size']]);found=[];proof=[]
    for off in range(s['off'],s['off']+s['size'],16):
        nameoff,val,length=struct.unpack_from('>III',data,off)
        stop=names.find(b'\0',nameoff)
        if stop<0:raise ValueError('Invalid ELF symbol string')
        name=names[nameoff:stop].decode('ascii','replace')
        if name==NAMES[-1][0]:
            if (val,length,data[off+12]&15)!=(0xFC,1492,2):
                raise ValueError('Unreviewed final FUNC metadata')
            struct.pack_into('>I',data,off+8,1488);found.append(off)
        elif name==NAMES[-1][0]+'.NON_MATCHING':
            if (val,length,data[off+12]&15)!=(0xFC,1488,1):raise ValueError('Bad original ASM owner marker')
            proof.append(off)
    if len(found)!=1 or len(proof)!=1:raise ValueError('Missing final ASM symbol/marker')
    changed=[i for i,(a,b) in enumerate(zip(orig,data)) if a!=b]
    if not all(found[0]+8<=i<found[0]+12 for i in changed):
        raise ValueError('Attempted to modify native code or relocations')
    if sha(data)!=PACK_OBJ_SHA:raise ValueError('Unreviewed generated ELF metadata')
    p.write_bytes(data)
    return {'status':'STAGED_ELF_SIZE_ONLY','symbol':NAMES[-1][0],
            'original_FUNC_size':1492,'verified_size':1488,'zero_padding_bytes':4,
            'metadata_byte_offsets_changed':changed,'object_sha256':sha(data)}

def verify(baseline:Path,candidate:Path):
    baseline=baseline.resolve();candidate=candidate.resolve()
    if baseline==candidate:raise ValueError('Baseline and candidate must be independent checkouts')
    rom=original(baseline)
    if original(candidate)!=rom:raise ValueError('Original ROM inputs differ')
    if (baseline/'build/japan_0/mnsg.z64').read_bytes()!=rom or (candidate/'build/japan_0/mnsg.z64').read_bytes()!=rom:
        raise ValueError('FAILED_ROM: complete integrated original ROM mismatch')
    stage=json.loads((candidate/STAGE).read_text())
    if stage['mixed_source_sha256']!=MIX_SHA or sha((candidate/STAGED).read_bytes())!=MIX_SHA:
        raise ValueError('FAILED_SOURCE: staged mixed source changed')
    if sha((candidate/'build/japan_0/src/jpcright_resetmixed.c.o').read_bytes())!=PACK_OBJ_SHA:
        raise ValueError('FAILED_NATIVE: native stage object changed')
    from decomp import overlay_crossregion47 as cross
    from decomp import glitch_g2_promotion as glitch
    from decomp import japan_cright_promotion as cr
    elf=lambda co:co/'build/japan_0/mnsg.elf'
    sym0=cross._funcs(elf(baseline));sym1=cross._funcs(elf(candidate))
    if sym0!=sym1 or sum(sym1.values())!=7376:raise ValueError('FAILED_ELF: lost original FUNC identities')
    rel0,n0,h0=glitch.all_semantic_relocations(elf(baseline))
    rel1,n1,h1=glitch.all_semantic_relocations(elf(candidate))
    if n0!=80745 or n1!=80745 or h0!=REL_SHA or h1!=REL_SHA or rel0!=rel1:
        raise ValueError('FAILED_RELOC: changed complete ELF relocations')
    c0=cr.c_identities(elf(baseline));c1=cr.c_identities(elf(candidate))
    if (len(c0),len(c1))!=(2370,2371) or c1-c0!={NAMES[0][0]} or c0-c1:
        raise ValueError('FAILED_INVENTORY: unexpected C ownership change')
    result={'status':'PASSED_COMBINED_2371_RESEARCH_ONLY','region':'japan_0','target':NAMES[0][0],
            'original_C_count':len(c0),'candidate_C_count':len(c1),
            'candidate_C_bytes':127068,'candidate_ASM_remaining':5005,
            'full_ROM_bytes':len(rom),'ROM_sha1':ROM_SHA,
            'positive_ELF_functions':7376,'ELF_function_identities_exact':True,
            'baseline_relocations':n0,'candidate_relocations':n1,
            'full_reloc_multiset_exact':True,'reloc_sha256':h0,
            'C_source_sha256':C_SHA,'mixed_source_sha256':MIX_SHA,
            'original_function_ROM_offset':ROM_OFF,'original_function_bytes':60,
            'native_source_code_sha256':CODE_SHA,
            'ordinary_original_Splat_80747_pair':'historical CRight dual reference, not newly waived',
            'stable_canonical_manifest':'NOT_UPDATED','current_stable_CI':'NOT_RUN'}
    return result

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('operation',choices=['stage','repair','verify'])
    p.add_argument('--checkout',type=Path)
    p.add_argument('--baseline',type=Path)
    p.add_argument('--candidate',type=Path)
    p.add_argument('--report',type=Path)
    a=p.parse_args(argv)
    if a.operation in {'stage','repair'}:
        if not a.checkout:p.error('--checkout required')
        result=stage(a.checkout) if a.operation=='stage' else repair(a.checkout)
    else:
        if not a.baseline or not a.candidate:p.error('--baseline and --candidate required')
        result=verify(a.baseline,a.candidate)
    if a.report:
        if a.report.exists():raise FileExistsError('No overwrites of original proof reports')
        a.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
