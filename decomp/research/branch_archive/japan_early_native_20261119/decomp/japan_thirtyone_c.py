"""Pinned Japanese rev-0 source stage and metadata-only linker-layout fixes.

No cartridge bytes enter the repository. Fail closed on source, layout or
relocation changes. Full 32/16 MiB equality remains an independent gate.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess

ROOT = Path(__file__).resolve().parent
PINNED_SHA1 = '6f8745fecc3a5e7d4918c7a73353eb0726116ded'
CONFIG = Path('config/japan_0/splat_thirtyone_c.local.yaml')
SOURCE_NAMES = ('jp_bit_array','jp_camera_13B70','jp_main_38620','jp_mode_flags',
    'jp_motion_12D60','jp_state_37D1C','jp_transition_37870','jp_warp_37920',
    'jp_warp_37B58','jp_warp_37C4C','jp_warp_37C84','jp_warp_37CB8',
    'jp_warp_37CE0','jp_warp_call_37900','jp_coord_37958',
    'jp_coord_37A24','jp_state_37AF4','jp_warp_37B8C','jp_state_37D5C','jp_compare_37EEC',
    'jp_wrapper_370B0','jp_wrapper_37178','jp_wrapper_3757C','jp_get_3769C',
    'jp_wrapper_383C4','jp_get_3847C','jp_set_3850C')
# Original code bytes. The IDO standalone section may have zero padding up
# to the next 16-byte boundary, and is never allowed to retain that padding.
REVIEWED = (
 ('jp_transition_37870', 'func_80036C70_37870',96),
 ('jp_warp_37920','func_80036D20_37920',56),
 ('jp_warp_37B58','func_80036F58_37B58',52),
 ('jp_warp_37C4C','func_8003704C_37C4C',56),
 ('jp_warp_37C84','func_80037084_37C84',52),
 ('jp_warp_37CB8','func_800370B8_37CB8',40),
 ('jp_warp_37CE0','func_800370E0_37CE0',60),
 ('jp_state_37D1C','func_8003711C_37D1C',64),
 ('jp_coord_37958','func_80036D58_37958',204),
 ('jp_coord_37A24','func_80036E24_37A24',208),
 ('jp_state_37AF4','func_80036EF4_37AF4',100),
 ('jp_warp_37B8C','func_80036F8C_37B8C',192),
 ('jp_state_37D5C','func_8003715C_37D5C',92),
 ('jp_compare_37EEC','func_800372EC_37EEC',52),
 ('jp_wrapper_370B0','func_800364B0_370B0',32),
 ('jp_wrapper_37178','func_80036578_37178',32),
 ('jp_wrapper_3757C','func_8003697C_3757C',32),
 ('jp_get_3769C','func_80036A9C_3769C',8),
 ('jp_wrapper_383C4','func_800377C4_383C4',36),
 ('jp_get_3847C','func_8003787C_3847C',20),
 ('jp_set_3850C','func_8003790C_3850C',20),
)
SEGMENTS = (
 ('    - [0x122F0, asm, main_122F0]',
  '    - [0x122F0, asm, main_122F0]\n    - [0x12D60, c, jp_motion_12D60]\n    - [0x12D80, asm, main_12D80]'),
 ('    - [0x140D0, asm, wave_uty]',
  '    - [0x13B70, c, jp_camera_13B70]\n    - [0x13B90, asm, main_13B90]\n    - [0x140D0, asm, wave_uty]'),
 ('    - [0x16E70, asm, main_16E70]',
  '    - [0x16DF0, c, jp_bit_array]\n    - [0x16E70, asm, main_16E70]'),
 ('    - [0x370B0, asm, main_370B0]', '\n'.join((
  '    - [0x370B0, c, jp_wrapper_370B0]',
  '    - [0x370D0, asm, main_370D0]',
  '    - [0x37178, c, jp_wrapper_37178]',
  '    - [0x37198, asm, main_37198]',
  '    - [0x3757C, c, jp_wrapper_3757C]',
  '    - [0x3759C, asm, main_3759C]',
  '    - [0x3769C, c, jp_get_3769C]',
  '    - [0x376A4, asm, main_376A4]'))),
 ('    - [0x37870, asm, main_37870]', '\n'.join((
  '    - [0x37870, c, jp_transition_37870]',
  '    - [0x378D0, c, jp_mode_flags]',
  '    - [0x37900, c, jp_warp_call_37900]',
  '    - [0x37920, c, jp_warp_37920]',
  '    - [0x37958, c, jp_coord_37958]',
  '    - [0x37A24, c, jp_coord_37A24]',
  '    - [0x37AF4, c, jp_state_37AF4]',
  '    - [0x37B58, c, jp_warp_37B58]',
  '    - [0x37B8C, c, jp_warp_37B8C]',
  '    - [0x37C4C, c, jp_warp_37C4C]',
  '    - [0x37C84, c, jp_warp_37C84]',
  '    - [0x37CB8, c, jp_warp_37CB8]',
  '    - [0x37CE0, c, jp_warp_37CE0]',
  '    - [0x37D1C, c, jp_state_37D1C]',
  '    - [0x37D5C, c, jp_state_37D5C]',
  '    - [0x37DB8, asm, main_37DB8]',
  '    - [0x37EEC, c, jp_compare_37EEC]',
  '    - [0x37F20, asm, main_37F20]'))),
 ('    - [0x38240, asm, main_38240]', '\n'.join((
  '    - [0x38240, asm, main_38240]',
  '    - [0x383C4, c, jp_wrapper_383C4]',
  '    - [0x383E8, asm, main_383E8]',
  '    - [0x3847C, c, jp_get_3847C]',
  '    - [0x38490, asm, main_38490]',
  '    - [0x3850C, c, jp_set_3850C]',
  '    - [0x38520, asm, main_38520]'))),
 ('    - [0x38620, asm, main_38620]',
  '    - [0x38620, c, jp_main_38620]'),
)


def render_config(original: str) -> str:
    if 'sha1: '+PINNED_SHA1 not in original:
        raise ValueError('Incorrect pinned Japanese expanded ROM')
    generated,count=re.subn(r'(?m)^([ \t]*-\s*\[\s*0x[\da-fA-F]+\s*,\s*)c(\s*,)',r'\1asm\2',original)
    if count!=189:
        raise ValueError(f'Unsupported Japanese Splat: expected 189 C units, got {count}')
    for old,new in SEGMENTS:
        if generated.count(old)!=1:
            raise ValueError('Missing unique Japanese subsegment: '+old)
        generated=generated.replace(old,new,1)
    if generated.count(', c,')!=27:
        raise ValueError('Wrong number of reviewed Japanese C translation units')
    return generated


def stage_config(checkout: Path) -> Path:
    original=(checkout/'config/japan_0/splat.yaml').read_text(encoding='utf-8')
    expected=render_config(original)
    dest=checkout/CONFIG
    if dest.exists() and dest.read_text(encoding='utf-8')!=expected:
        raise FileExistsError('Modified Splat stage; refusing to overwrite: '+str(dest))
    dest.write_text(expected,encoding='utf-8')
    return dest


def install_sources(checkout: Path, source_root: Path = ROOT) -> list[str]:
    installed=[]
    for stem in SOURCE_NAMES:
        source=source_root/'japan_matching'/(stem+'.c')
        expected=source.read_bytes()
        target=checkout/'src'/(stem+'.c')
        if target.exists():
            existing=target.read_bytes()
            if existing==expected:
                installed.append(str(target));continue
            # Only an unmodified Splat generated C stub can be replaced.
            src=existing.decode('utf-8')
            stubs=re.findall(r'#pragma GLOBAL_ASM\("([^"]+)"\)',src)
            if not stubs or '#include "common.h"' not in src or len(stubs)!=src.count('#pragma GLOBAL_ASM'):
                raise FileExistsError('Unrecognised existing Japanese source: '+str(target))
            if not all(f'asm/japan_0/nonmatchings/{stem}/' in s and s.endswith('.s') for s in stubs):
                raise FileExistsError('Unexpected original assembly file in generated stub: '+str(target))
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(expected)
        installed.append(str(target))
    return installed


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pack_text_metadata(data: bytes, actual_size: int) -> tuple[bytes,dict]:
    if data[:6]!=b'\x7fELF\x01\x02' or struct.unpack_from('>H',data,16)[0]!=1:
        raise ValueError('Expected relocatable ELF32 big-endian input')
    start=struct.unpack_from('>I',data,32)[0]
    width=struct.unpack_from('>H',data,46)[0]
    count=struct.unpack_from('>H',data,48)[0]
    if width!=40 or not count or start+width*count>len(data):
        raise ValueError('Bad ELF section header table')
    sections=[]
    for i in range(count):
        off=start+i*40
        kind,flags=struct.unpack_from('>II',data,off+4)
        payload_offset,payload_size=struct.unpack_from('>II',data,off+16)
        align=struct.unpack_from('>I',data,off+32)[0]
        info=struct.unpack_from('>I',data,off+28)[0]
        sections.append((off,kind,flags,payload_offset,payload_size,align,info))
    text=[(idx,entry) for idx,entry in enumerate(sections) if entry[1]==1 and entry[2]==6]
    if len(text)!=1:raise ValueError('Expected unique executable ELF .text section')
    idx,section=text[0]
    off,kind,flags,payload_off,original_size,align,_info=section
    required_size=(actual_size+15)&~15
    if original_size!=required_size or align!=16 or actual_size%4 or actual_size<=0:
        raise ValueError('Unexpected native section extent/alignment')
    if payload_off+original_size>len(data) or any(data[payload_off+actual_size:payload_off+original_size]):
        raise ValueError('Nonzero section padding would modify original instructions')
    reloc_count=0
    for roff,rkind,_flags,rpayload,rlength,_align,rinfo in sections:
        if rkind==4 and rinfo==idx:
            raise ValueError('RELA relocation format not reviewed')
        if rkind==9 and rinfo==idx:
            if rpayload+rlength>len(data) or rlength%8:
                raise ValueError('Invalid MIPS .text relocation entries')
            for j in range(rpayload,rpayload+rlength,8):
                displacement=struct.unpack_from('>I',data,j)[0]
                if displacement>=actual_size or displacement%4:
                    raise ValueError('Relocation points into padded / unreviewed code')
                reloc_count+=1
    patched=bytearray(data)
    struct.pack_into('>I',patched,off+20,actual_size)
    struct.pack_into('>I',patched,off+32,4)
    allowed=set(range(off+20,off+24))|set(range(off+32,off+36))
    changes=[i for i,(a,b) in enumerate(zip(data,patched)) if a!=b]
    if any(i not in allowed for i in changes):
        raise AssertionError('Unexpected original ELF bytes changed')
    return bytes(patched),dict(old_size=original_size,new_size=actual_size,old_align=16,new_align=4,
        zero_bytes_trimmed=original_size-actual_size,relocations_preserved=reloc_count,
        bytes_changed=len(changes),input_sha256=sha(data),output_sha256=sha(patched))


def prepare_layout(checkout: Path, objdump: str) -> dict:
    from .japan_relocation_policy import verify_text_relocations
    prepared=[]
    for stem,function,size in REVIEWED:
        object_path=checkout/'build/japan_0/src'/(stem+'.c.o')
        original=object_path.read_bytes()
        sym=subprocess.run([objdump,'-t',str(object_path)],capture_output=True,text=True,check=True).stdout
        symbol_re=r'(?m)^0{1,8}\s+g\s+F\s+\.text\s+'+f'{size:08x}'+r'\s+'+re.escape(function)+r'\s*$'
        if len(re.findall(symbol_re,sym))!=1:
            raise ValueError('Wrong original guest function symbol/size: '+function)
        reloc=subprocess.run([objdump,'-r','-j','.text',str(object_path)],capture_output=True,text=True,check=True).stdout
        count=verify_text_relocations('japan_matching/'+stem+'.c',reloc)
        packed,proof=pack_text_metadata(original,size)
        if count!=proof['relocations_preserved']:
            raise ValueError('Native relocations do not match ELF32 relocation table')
        if packed!=original:
            object_path.write_bytes(packed)
        prepared.append({'object':str(object_path.relative_to(checkout)),'function':function,'size':size,
                         'text_relocations':count,**proof})
    # These seven reviewed ASM slices end on non-16-byte boundaries.
    # Trim zero-only padding and preserve all native instruction/relocation records.
    reviewed_asm=(('main_370D0',0xA8,8),('main_37198',0x3E4,12),
                  ('main_376A4',0x1CC,4),('main_37DB8',0x134,12),
                  ('main_38240',0x184,12),('main_383E8',0x94,12),
                  ('main_38490',0x7C,4))
    for name,expected_size,expected_zero in reviewed_asm:
        suffix=checkout/'build/japan_0/asm/japan_0'/(name+'.s.o')
        packed,proof=pack_text_metadata(suffix.read_bytes(),expected_size)
        if proof['zero_bytes_trimmed']!=expected_zero:
            raise ValueError('Unexpected Japanese ASM padding in '+name)
        suffix.write_bytes(packed)
        prepared.append({'object':str(suffix.relative_to(checkout)),
                         'assembly_slice':True,**proof})
    ld=checkout/'.splat/japan_0/mnsg.ld'
    text=ld.read_text(encoding='utf-8')
    old='.main 0x80000450 : AT(main_ROM_START) SUBALIGN(16)'
    if text.count(old)!=1:raise ValueError('Missing unique original main linker subalign')
    updated=text.replace(old,'.main 0x80000450 : AT(main_ROM_START) SUBALIGN(4)',1)
    ld.write_text(updated,encoding='utf-8')
    return {'format':'japan-thirtyone-elf-metadata-layout-v1','objects':prepared,
            'linker_original_sha256':sha(text.encode()),'linker_staged_sha256':sha(updated.encode()),
            'main_subalign_changed_from':16,'main_subalign_changed_to':4}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('operation',choices=('stage','install','layout'))
    p.add_argument('checkout',type=Path)
    p.add_argument('--objdump',default='mips-linux-gnu-objdump')
    p.add_argument('--report',type=Path)
    args=p.parse_args(argv)
    root=args.checkout.resolve(strict=True)
    if args.operation=='stage':result=str(stage_config(root))
    elif args.operation=='install':result=install_sources(root)
    else:result=prepare_layout(root,args.objdump)
    if args.report:
        with args.report.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    else:print(json.dumps(result,indent=2))

if __name__=='__main__':main()
