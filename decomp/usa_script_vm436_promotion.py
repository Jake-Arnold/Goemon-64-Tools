"""Fail-closed original-USA script VM 436B native C after canonical 2164 G2.

This stage is deliberately **after** all previously proven stages. Their
immutable historical 210/987/.../2164-C gates must still validate before the
new script-VM owner can be promoted. Native source and negative controls are
published in the already-reviewed research/usa_script_vm_436_20261123 folder.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import shutil

FORMAT = 'goemon-usa-script-vm436-post2164-v1'
ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
NAME = 'func_8003EBAC_3F7AC'
OFFSET = 0x3F7AC
VMA = 0x8003EBAC
SIZE = 436
ORIGINAL_VM_SOURCE_SHA256 = 'ef69896e2c6e77d9849d18700cd828a959bfa9fa269768fc40a0ad773a8dd422'
ORIGINAL_C_SOURCE_SHA256 = 'c1e4966ed0937947c05abdc672214d0d731cf84d43147a0acc50df3f54ab8baa'
MERGED_VM_SOURCE_SHA256 = '55475ae86cce1431fc2916b139e6f92a7ba6a5b0a776de483ed8eea2677343d8'
ASM_PRAGMA = '#ifndef GOEMON_DECOMP_HOST_TEST\n#pragma GLOBAL_ASM("asm/usa/nonmatchings/script_vm/func_8003EBAC_3F7AC.s")\n#endif'
SOURCE = Path(__file__).parent / 'research/usa_script_vm_436_20261123/source/func_8003EBAC_3F7AC.c'


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def validate_predecessor(manifest: dict, original: bytes | None = None) -> list[dict]:
    if manifest.get('usa_script_vm436_promotion') != {'format': FORMAT}:
        raise ValueError('Unreviewed USA VM 436 promotion stage')
    if manifest['decompressed_sha1'] != ROM_SHA1 or manifest['upstream_commit'] != '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee':
        raise ValueError('Changed original USA ROM/upstream provenance')
    from .verify import claimed_functions
    predecessor = {k:v for k,v in manifest.items() if k != 'usa_script_vm436_promotion'}
    prior = claimed_functions(predecessor)
    if (len(prior),sum(x['size'] for x in prior)) != (2164,99604):
        raise ValueError('Canonical 2,164-C predecessor moved')
    if NAME in {f['name'] for f in prior} or any(f['rom_offset'] < OFFSET+SIZE and OFFSET < f['rom_offset']+f['size'] for f in prior):
        raise ValueError('Original VM function already accepted or overlaps C')
    vm = [u for u in predecessor['units'] if u['source'] == 'script_vm.c']
    if len(vm)!=1 or len(vm[0]['functions'])!=56 or len(vm[0]['assembly_functions'])!=13 or vm[0]['assembly_functions'][7]!=NAME:
        raise ValueError('Historical script_vm C/ASM ownership drift')
    old_source=(Path(__file__).parent/'script_vm.c').read_bytes()
    if sha(old_source)!=ORIGINAL_VM_SOURCE_SHA256 or old_source.decode().count(ASM_PRAGMA)!=1:
        raise ValueError('Canonical original script_vm ASM/C source changed')
    source=SOURCE.read_bytes()
    if sha(source)!=ORIGINAL_C_SOURCE_SHA256:
        raise ValueError('Original native script_vm C lost its exact source hash')
    if original is not None:
        if len(original)!=33554432 or hashlib.sha1(original).hexdigest()!=ROM_SHA1:
            raise ValueError('Wrong original USA ROM supplied for VM promotion')
        # original instruction bytes verified in native G2 against this ROM
    return prior


def proposed_source() -> str:
    original=(Path(__file__).parent/'script_vm.c').read_text()
    researched=SOURCE.read_text()
    fn=researched[researched.index('void func_8003EBAC_3F7AC('):]
    fn=fn.replace('Gfx *','VmGfx *').replace('D_80077860_78460->field5C','((VmState *) D_80077860_78460)->field5C')
    header=('typedef struct { u32 w0, w1; } VmGfx;\n'
            'typedef struct { u8 pad[0x5C]; u8 field5C, field5D; } VmState;\n'
            'extern u8 D_80076148_76D48;\n'
            'extern u8 D_800777F0_783F0;\n'
            'extern VmGfx *D_8015C5CC_15D1CC;\n\n')
    if original.count(ASM_PRAGMA)!=1:
        raise ValueError('Missing original distinct script_vm ASM pragma')
    merged=original.replace(ASM_PRAGMA,'#ifndef GOEMON_DECOMP_HOST_TEST\n'+header+fn+'#endif')
    if sha(merged.encode())!=MERGED_VM_SOURCE_SHA256:
        raise ValueError('Unreviewed original IDO C source construction')
    return merged


def stage(checkout:Path,work:Path,prior_elf:Path) -> dict:
    checkout=Path(checkout); work=Path(work)
    vm=checkout/'src/script_vm.c'
    old=vm.read_bytes()
    if sha(old)!=ORIGINAL_VM_SOURCE_SHA256:
        raise ValueError('Staged original VM translation-unit source changed')
    source=proposed_source()
    elf=checkout/'build/usa/mnsg.elf'
    shutil.copyfile(elf,prior_elf)
    old_object=checkout/'build/usa/src/script_vm.c.o'
    old_layout=old_object.with_name(old_object.name+'.before-layout')
    if not old_layout.is_file() or not old_object.is_file():
        raise ValueError('Canonical VM ELF object and unmodified layout backup required')
    backup=work/'script_vm_2164_before_layout.o'
    if backup.exists():raise ValueError('Prior VM object backup already exists')
    old_layout.rename(backup)  # retain original object; do not discard evidence
    original_obj_sha=sha(old_object.read_bytes())
    old_object.unlink()  # force new IDO compilation
    vm.write_text(source,encoding='utf-8',newline='\n')
    return {'old_source_sha256':sha(old),'new_source_sha256':sha(source.encode()),
            'old_object_sha256':original_obj_sha,'original_layout_backup_sha256':sha(backup.read_bytes())}


def verify_native(baseline:Path,prior_elf:Path,candidate:Path,original:bytes,layout:dict) -> dict:
    from .overlay_crossregion47 import _funcs
    from .glitch_g2_promotion import all_semantic_relocations
    from .usa_opening_new2_promotion import stable_globals
    baseline=Path(baseline);candidate=Path(candidate);prior_elf=Path(prior_elf)
    rom=(candidate/'build/usa/mnsg.z64').read_bytes()
    if len(rom)!=33554432 or rom!=original or hashlib.sha1(rom).hexdigest()!=ROM_SHA1:
        raise ValueError('VM436 failed full 33,554,432-byte original USA ROM identity')
    oldfunc=_funcs(prior_elf);newfunc=_funcs(candidate/'build/usa/mnsg.elf')
    baseline_func=_funcs(baseline/'build/usa/mnsg.elf')
    if oldfunc!=newfunc or sum(oldfunc.values())!=sum(baseline_func.values())!=7376:
        raise ValueError('VM436 changed original 7,376 native ELF FUNC identities')
    # Published 2164 C has exactly one already-recorded original versus
    # mixed-build ELF extent exception. Preserve that exception *exactly*;
    # no other original ELF function name, address or size may change.
    expected_mixed_only={('func_8003F6E8_402E8',0x8003F6E8,56):1}
    expected_original_only={('func_8003F6E8_402E8',0x8003F6E8,48):1}
    if (oldfunc-baseline_func)!=expected_mixed_only or (baseline_func-oldfunc)!=expected_original_only:
        raise ValueError('VM436 changed or introduced an original ELF function extent exception')
    a,ac,ah=all_semantic_relocations(prior_elf)
    b,bc,bh=all_semantic_relocations(candidate/'build/usa/mnsg.elf')
    if not a==b or (ac,bc)!=(82103,82103) or ah!=bh or ah!='f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97':
        raise ValueError('VM436 changed accepted 82,103 original symbolic relocations')
    g0=stable_globals(prior_elf);g1=stable_globals(candidate/'build/usa/mnsg.elf')
    if g0!=g1 or sum(g1.values())!=26714:
        raise ValueError('VM436 changed original stable global symbol identities')
    if original[OFFSET:OFFSET+SIZE]!=rom[OFFSET:OFFSET+SIZE] or (NAME,VMA,SIZE) not in newfunc:
        raise ValueError('Original 436-byte function is not at original VMA / ELF extent')
    if NAME+'.NON_MATCHING' in (candidate/'build/usa/mnsg.map').read_text():
        raise ValueError('VM C still carries original nonmatching assembly marker')
    staged=(candidate/'src/script_vm.c').read_bytes()
    if sha(staged)!=MERGED_VM_SOURCE_SHA256 or ASM_PRAGMA.encode() in staged:
        raise ValueError('Native C source not compiled from pinned source')
    return {'status':'PASSED_G2_LOCAL','base_matching_C':2164,'accepted_c_after':2165,
            'added_matching_C':1,'added_instruction_bytes':SIZE,
            'accepted_original_bytes_after':100040,'remaining_assembly':5198,
            'full_rom_match':True,'original_rom_sha1':ROM_SHA1,
            'complete_original_ROM_bytes_exact':33554432,
            'original_positive_ELF_functions_exact':7376,
            'canonical_semantic_relocations_exact':82103,
            'canonical_semantic_relocation_sha256':bh,
            'stable_global_symbols_exact':sum(g1.values()),
            'original_function_rom_sha256':sha(original[OFFSET:OFFSET+SIZE]),
            'original_candidate_ELF_sha256':sha((candidate/'build/usa/mnsg.elf').read_bytes()),
            'canonical_predecessor_ELF_sha256':sha(prior_elf.read_bytes()),
            'compiled_original_source_sha256':MERGED_VM_SOURCE_SHA256,
            'source_original_C_sha256':ORIGINAL_C_SOURCE_SHA256,
            'layout':layout,'gameplay':'NOT_RUN'}
