"""USA Mini selector original-address IDO C promotion after canonical USA2089.

Requires original table symbol ownership and all byte-for-byte original-ROM,
ELF identity, complete relocation, inventory and CI gates. No opcode patches.
"""
from __future__ import annotations

from collections import Counter
from contextlib import contextmanager
from pathlib import Path
import hashlib
import json
import re
import struct
import subprocess

from . import overlay_isolated233 as splice
from . import overlay_crossregion47 as cross
from .glitch_g2_promotion import all_semantic_relocations

ROOT=Path(__file__).resolve().parent
DIR=ROOT/'research/usa_mini_selector_20261123'
FORMAT='goemon-usa-mini-selector-post2089-v1'
FIXTURE_SHA256='173126a60ee34e3308d7e4ab5189296eb4200cb5baccee22a932f1868961f2fa'
PRIOR_SHA256='8447b1271718bede4dc63244b48057604d4b7af55fab9f35ab5acfd31a90e9ef'
ORIGINAL_SHA1='6ea0ed71032ce08fc2745f412d84936382197494'
NAME='func_801E1C90_59DBA0'
VMA=0x801E1C90
ROM_OFFSET=0x59DBA0
SIZE=384
RELOCS=(0x138,0x140)
TABLE_NAME='jtbl_8020B2E0_5C71F0'


def digest(raw):return hashlib.sha256(raw).hexdigest()


def fixture():
    raw=(DIR/'manifest.json').read_bytes()
    if digest(raw)!=FIXTURE_SHA256:raise ValueError('Mini selector fixture SHA256 drift')
    d=json.loads(raw)
    if (d.get('format'),d.get('region'),d.get('prior_count'),d.get('prior_bytes'),
        d.get('prior_manifest_sha256'),d.get('original_rom_sha1'),
        d.get('original_jump_table_vma'),d.get('original_table_count'),
        d.get('retargeted_relocation_offsets')) != (FORMAT,'usa',2089,94284,PRIOR_SHA256,
        ORIGINAL_SHA1,'0x8020B2E0',8,list(RELOCS)):
        raise ValueError('Mini selector unreviewed source/format/relocation fixture')
    fs=d.get('functions')
    if not isinstance(fs,list) or len(fs)!=1:raise ValueError('Mini selector must be one source')
    f=fs[0]
    if f.get('name')!=NAME or f.get('vma')!=VMA or f.get('rom_offset')!=ROM_OFFSET or f.get('size')!=SIZE or f.get('source')!='mini_selector' or f.get('original_asm')!='file_11':
        raise ValueError('Mini selector original ROM / ELF ownership invalid')
    if set(f)!={'name','rom_offset','vma','size','source','source_sha256','original_code_sha256','original_asm'}:
        raise ValueError('Mini selector fixture fields drift')
    if digest((DIR/'mini_selector.c').read_bytes())!=f['source_sha256']:
        raise ValueError('Mini selector native C source changed')
    if f['source_sha256']!='3dcbf3eac6764dcd36e4ec402d5b0cffe6ce181ef84f40a9736fa507a495541b':
        raise ValueError('Mini selector original C source hash changed')
    return d


def validate_predecessor(manifest,rom=None):
    from . import verify
    if manifest.get('overlay_mini_selector_stage') != {'format':FORMAT}:
        raise ValueError('Missing exact Mini selector canonical stage')
    prev={k:v for k,v in manifest.items() if k!='overlay_mini_selector_stage'}
    if digest((json.dumps(prev,indent=2)+'\n').encode())!=PRIOR_SHA256:
        raise ValueError('Mini selector canonical predecessor moved; rebase required')
    old=verify.claimed_functions(prev)
    if len(old)!=2089 or sum(x['size'] for x in old)!=94284:
        raise ValueError('Mini selector 2089-C predecessor count/size differs')
    for f in old:
        at=f['rom_offset'];size=f['size']
        if f['name']==NAME or (at<ROM_OFFSET+SIZE and at+size>ROM_OFFSET):
            raise ValueError('Mini selector already accepted/overlaps original C')
    d=fixture()
    if rom is not None:
        if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=ORIGINAL_SHA1:
            raise ValueError('Mini selector wrong original USA ROM')
        if digest(rom[ROM_OFFSET:ROM_OFFSET+SIZE])!=d['functions'][0]['original_code_sha256']:
            raise ValueError('Mini selector wrong authenticated instruction span')
    return d


@contextmanager
def source_context():
    old=splice.EMBEDDED.copy()
    try:
        splice.EMBEDDED.clear()
        yield
    finally:
        splice.EMBEDDED.clear();splice.EMBEDDED.update(old)


def sections(b):
    if b[:6]!=b'\x7fELF\x01\x02':raise ValueError('Mini selector C output not MIPS ELF32 big endian')
    shoff=struct.unpack_from('>I',b,32)[0];shent=struct.unpack_from('>H',b,46)[0]
    shnum=struct.unpack_from('>H',b,48)[0];shstrndx=struct.unpack_from('>H',b,50)[0]
    if not shent or shstrndx>=shnum:raise ValueError('Malformed MIPS ELF section header')
    idx=shoff+shent*shstrndx
    strbase=struct.unpack_from('>I',b,idx+16)[0]
    d={}
    for i in range(shnum):
        at=shoff+shent*i
        off=struct.unpack_from('>I',b,at)[0]
        name=b[strbase+off:b.index(0,strbase+off)].decode()
        d[name]=(struct.unpack_from('>I',b,at+16)[0],struct.unpack_from('>I',b,at+20)[0],struct.unpack_from('>I',b,at+36)[0])
    return d


def patch_jumptable_symbol(obj):
    """Retarget two ELF relocation symbols only; native MIPS .text unchanged."""
    obj=Path(obj)
    raw=obj.read_bytes()
    d=sections(raw)
    textoff,textlen,_=d['.text']
    before_text=raw[textoff:textoff+textlen]
    original=obj.with_suffix('.source.o')
    if original.exists():raise ValueError('Prior selector original object collision')
    obj.rename(original)
    subprocess.run(['mips-linux-gnu-objcopy','--add-symbol',TABLE_NAME+'=.text:0,global',str(original),str(obj)],check=True)
    buf=bytearray(obj.read_bytes());d=sections(buf)
    textoff,textlen,_=d['.text']
    if buf[textoff:textoff+textlen]!=before_text:
        raise ValueError('Selector native compiler instructions changed by symbolic adapter')
    symoff,symsize,syment=d['.symtab']
    if syment!=16 or symsize//16!=9:raise ValueError('Original IDO symbol table layout drift')
    symbol8=symoff+8*16
    if struct.unpack_from('>H',buf,symbol8+14)[0]!=1 or struct.unpack_from('>I',buf,symbol8+4)[0]!=0:
        raise ValueError('Original table symbol must be zero-offset defined before retarget')
    struct.pack_into('>H',buf,symbol8+14,0)
    reloff,relsize,relent=d['.rel.text']
    if relent!=8:raise ValueError('Selector native relocation size changed')
    changed=[]
    for j in range(relsize//relent):
        at=reloff+j*8
        off,info=struct.unpack_from('>II',buf,at)
        if off in RELOCS:
            expected_type=5 if off==0x138 else 6
            if info>>8!=2 or info&255!=expected_type:
                raise ValueError('Selector relocation offset/type/target changed')
            struct.pack_into('>I',buf,at+4,(8<<8)|(info&255))
            changed.append(off)
    if changed!=list(RELOCS):raise ValueError('Selector missing HI16/LO16 original-table retargets')
    obj.write_bytes(buf)
    final=obj.read_bytes();sec=sections(final);a,n,_=sec['.text']
    if final[a:a+n]!=before_text:raise ValueError('Selector ELF symbolic-only patch modified native instructions')
    return {'retargeted_offsets':[hex(x) for x in changed], 'table_symbol':TABLE_NAME,
            'native_compiled_instruction_bytes_unchanged':True}


def verify_combined(baseline,prior_elf,candidate,rom,plan):
    with source_context():
        proof=splice.verify_link(baseline,prior_elf,candidate,rom,plan)
    before,nprev,sha=all_semantic_relocations(prior_elf)
    after,nnew,newsha=all_semantic_relocations(Path(candidate)/'build/usa/mnsg.elf')
    if nprev!=82103 or nnew!=nprev or before!=after:
        raise ValueError('Mini selector changed complete original 82,103 semantic relocations')
    return {'status':'PASSED_G2_LOCAL','new_c':1,'new_original_bytes':384,
            'total_c':2090,'total_original_C_bytes':94668,'remaining_ASM':5273,
            'rom_sha1':proof['sha1'],'rom_bytes':proof['rom_bytes'],
            'original_ELF_identities':proof['positive_elf_function_entries'],
            'complete_relocations':nprev,'complete_relocation_sha256':sha,
            'all_semantic_relocations_equal':True,'retained_ASM':proof['retained_ASM_fragments']}
