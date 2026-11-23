#!/usr/bin/env python3
"""Fail-closed original-Japan full-ROM / ELF / relocation test for 60B tail wrapper.

Private original ROM, generated Splat assembly, native compiler and ELF live only
inside the caller's scratch checkout. Never commit those files. This stage is
RESEARCH_ONLY until an accepted Japan-0 2370-C canonical integrated proof passes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from decomp import japan_asm_baseline as baseline  # noqa: E402
from decomp import overlay_crossregion47 as symbols  # noqa: E402
from decomp import glitch_g2_promotion as reloc  # noqa: E402

PIN = '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
ROM_SHA = '6f8745fecc3a5e7d4918c7a73353eb0726116ded'
RETAIL_SHA = '9843ee979b5f6c80f5eda85df0baed9ae7c4e73b'
IDO_SHA = '76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
SRC_SHA = '5ed38023f5cd59be0d2f3d5fa6f2ee1eec2ec9590e61f02be8bafe93821d7c62'
REF_RELOC_SHA = '82493bc7aa5eca079b1573a1f7999e99fb28384eed1efe8c4cf1777826dc2805'
NAME = 'func_80212C50_5CE1E0'
OFF = 0x5CE1E0
VMA = 0x80212C50
SIZE = 60
FUNCTION_PATH = Path('src/jp_cright_tail60.c')
SOURCE = Path(__file__).parent / 'source' / (NAME + '.c')
CONFIG = Path('config/japan_0/splat_tail60.local.yaml')
ASM_CONFIG = Path('config/japan_0/splat_asm_only.local.yaml')
SPLAT_INSERT = '    - [0x5CD620, asm]\n    - [0x5CE220, asm]'
SPLAT_REPLACEMENT = '    - [0x5CD620, asm]\n    - [0x5CE1E0, c, jp_cright_tail60]\n    - [0x5CE220, asm]'


def digest(path: Path, kind='sha256') -> str:
    h=hashlib.new(kind)
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def check_source() -> None:
    if digest(SOURCE)!=SRC_SHA:
        raise ValueError('Frozen matching-C source digest changed')


def check_checkout(p:Path) -> None:
    p=p.resolve(strict=True)
    sha=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
    if sha!=PIN: raise ValueError('Wrong original pinned mnsg revision '+sha)
    if digest(p/'config/japan_0/baserom.z64','sha1')!=RETAIL_SHA:
        raise ValueError('Wrong retail JP ROM')
    if digest(p/'config/japan_0/baserom.decompressed.z64','sha1')!=ROM_SHA:
        raise ValueError('Wrong expanded JP ROM')
    if digest(p/'tools/ido-5.3/cc')!=IDO_SHA:
        raise ValueError('Wrong native IDO5.3 compiler')


def render_candidate(original: str) -> str:
    asm=baseline.render_asm_config(original)
    if asm.count(SPLAT_INSERT)!=1: raise ValueError('Original overlay source boundary not unique')
    return asm.replace(SPLAT_INSERT,SPLAT_REPLACEMENT,1)


def stage(path:Path, *, candidate:bool) -> Path:
    path=path.resolve(strict=True)
    check_checkout(path)
    check_source()
    output=path/(CONFIG if candidate else ASM_CONFIG)
    if output.exists():raise FileExistsError('Refusing to overwrite Splat stage '+str(output))
    source=(path/'config/japan_0/splat.yaml').read_text(encoding='utf-8')
    prepared=render_candidate(source) if candidate else baseline.render_asm_config(source)
    output.write_text(prepared,encoding='utf-8')
    if candidate:
        dst=path/FUNCTION_PATH
        if dst.exists():raise FileExistsError('Refusing to replace original upstream C')
        dst.write_bytes(SOURCE.read_bytes())
    return output


def target_size(elf:Path) -> int:
    output=subprocess.check_output(['readelf','-Ws',str(elf)],text=True)
    rows=[r for r in output.splitlines() if re.search(r'\b'+re.escape(NAME)+r'$',r)]
    sizes=[int(parts[2]) for row in rows if len(parts:=(row.split()))>7 and parts[3]=='FUNC']
    if sizes!=[SIZE]: raise ValueError('Expected one 60B positive ELF FUNC identity, got '+str(sizes))
    return sizes[0]


def verify(original:Path,candidate:Path)->dict[str,object]:
    original=original.resolve(strict=True);candidate=candidate.resolve(strict=True)
    if original==candidate:raise ValueError('ASM baseline and C candidate must be independent scratch checkouts')
    check_source()
    for co in (original,candidate):
        check_checkout(co)
        rom=co/'build/japan_0/mnsg.z64'
        if rom.stat().st_size!=0x2000000 or digest(rom,'sha1')!=ROM_SHA:
            raise ValueError('Whole linked Japan ROM not exact '+str(co))
        if rom.read_bytes()!=(co/'config/japan_0/baserom.decompressed.z64').read_bytes():
            raise ValueError('Whole linked Japan ROM byte mismatch')
        target_size(co/'build/japan_0/mnsg.elf')
    # The generated build configs must be exact transformations of the pinned
    # upstream YAML. This prevents a second, unreviewed ASM edit or a different
    # function from masquerading as the single 60B source substitution.
    for co, path, is_candidate in (
            (original, ASM_CONFIG, False),
            (candidate, CONFIG, True)):
        source_yaml=(co/'config/japan_0/splat.yaml').read_text(encoding='utf-8')
        expected=render_candidate(source_yaml) if is_candidate else baseline.render_asm_config(source_yaml)
        if (co/path).read_text(encoding='utf-8')!=expected:
            raise ValueError('Staged Splat ownership differs from pinned source transformation')
    if digest(candidate/FUNCTION_PATH)!=SRC_SHA:
        raise ValueError('Staged native source does not equal frozen tested source')
    before=symbols._funcs(original/'build/japan_0/mnsg.elf')
    after=symbols._funcs(candidate/'build/japan_0/mnsg.elf')
    if before!=after or sum(before.values())!=7376:
        raise ValueError('ELF symbol identity mismatch')
    old,n0,h0=reloc.all_semantic_relocations(original/'build/japan_0/mnsg.elf')
    new,n1,h1=reloc.all_semantic_relocations(candidate/'build/japan_0/mnsg.elf')
    if old!=new or n0!=80810 or n1!=80810 or h0!=REF_RELOC_SHA or h1!=REF_RELOC_SHA:
        raise ValueError('Full ELF relocation difference outside original C function')
    words=(candidate/'build/japan_0/mnsg.z64').read_bytes()[OFF:OFF+SIZE]
    if words!=(original/'build/japan_0/mnsg.z64').read_bytes()[OFF:OFF+SIZE]:
        raise ValueError('Original native 15-instruction body mismatch')
    # Preserve and verify section ownership as an independent test.
    oldsym=subprocess.check_output(['readelf','-Ws',str(original/'build/japan_0/mnsg.elf')],text=True)
    newsym=subprocess.check_output(['readelf','-Ws',str(candidate/'build/japan_0/mnsg.elf')],text=True)
    if (NAME+'.NON_MATCHING' not in oldsym) or (NAME+'.NON_MATCHING' in newsym):
        raise ValueError('Expected exactly one ASM-to-C provenance/ownership conversion')
    return {'format':'goemon-jp-cright-tail60-original-asm-native-research-v1',
            'status':'FULL_ORIGINAL_ROM_EXACT_RESEARCH_ONLY',
            'region':'japan_0','target':NAME,'original_rom_offset':hex(OFF),
            'guest_vma':hex(VMA),'original_function_bytes':SIZE,
            'original_mips_instruction_words':SIZE//4,'exact_instruction_words':SIZE//4,
            'original_upstream_pin':PIN,'ido_compiler_sha256':IDO_SHA,
            'source_sha256':SRC_SHA,'expanded_rom_sha1':ROM_SHA,
            'entire_original_rom_bytes':0x2000000,'byte_differences':0,
            'positive_elf_function_identities':7376,'original_asm_relocations':n0,
            'native_c_relocations':n1,'relocations_multisets_exact':True,
            'relocation_fingerprint_sha256':REF_RELOC_SHA,
            'elf_symbol_asm_to_c':NAME,'accepted_jp2370_integration':'NOT_RUN',
            'strict_canonical_manifest_inventory':'NOT_RUN',
            'full_current_stable_decomp_ci':'NOT_RUN',
            'gameplay':'NOT_RUN'}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['stage-asm','stage-c','verify'])
    parser.add_argument('--checkout',type=Path)
    parser.add_argument('--original',type=Path)
    parser.add_argument('--candidate',type=Path)
    parser.add_argument('--report',type=Path)
    a=parser.parse_args()
    if a.command=='stage-asm':
        if a.checkout is None:parser.error('stage-asm requires --checkout')
        print(stage(a.checkout,candidate=False))
    elif a.command=='stage-c':
        if a.checkout is None:parser.error('stage-c requires --checkout')
        print(stage(a.checkout,candidate=True))
    else:
        if a.original is None or a.candidate is None:parser.error('verify requires --original and --candidate')
        result=verify(a.original,a.candidate)
        if a.report:
            if a.report.exists():raise FileExistsError('No overwriting existing proof')
            a.report.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))

if __name__=='__main__':main()
