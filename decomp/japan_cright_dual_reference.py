"""Three-way original-JP C-Right relocation proof, never a blanket waiver.

The original Splat assembler introduces symbolic relocations for a numeric
controller-structure offset. A second *independently assembled original-ASM*
reference expresses only those two first-check offset annotations as literals.

Every actual candidate relocation must equal that second original-ASM reference.
The unmodified published original reference must separately match its pinned
80,747 relocation fingerprint, and the entire difference between those two
independent original-ASM references must be exactly the two approved offset
annotations. The upstream native-code verifier is left unchanged.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import subprocess

from . import japan_cright_promotion as cr
from . import japan_cright_relocation_provenance as provenance
from . import glitch_g2_promotion as glitch
from . import overlay_crossregion47 as cross
from . import japan_noop_port as jp329

OWNER = 'asm/japan_0/jp1686_006_000.s'
BEFORE = 'lui        $t1, %hi(D_3B07A)'
AFTER = 'lui        $t1, 0x0004'
BEFORE_LO = 'lhu        $t1, %lo(D_3B07A)($t1)'
AFTER_LO = 'lhu        $t1, -0x4F86($t1)'
# These are Splat-generated undefined offsets, not explicit symbol addresses.
SYNTHETIC_PAIR = Counter({
    ('.rel.file_12',0x80212550,'R_MIPS_HI16',0x3B07A,'D_3B07A'):1,
    ('.rel.file_12',0x80212590,'R_MIPS_LO16',0x3B07A,'D_3B07A'):1,
})
BASELINE_HASH = 'e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20'
NORMALIZED_HASH = '43a133b21ac2b18d8e1d00f8c4e5718776b001a1f45c54e807dae12165e797c0'
REGION = 'japan_0'


def normalize_original_asm(original: str) -> str:
    """Normalize exactly two assembler expressions; preserve all other bytes.

    The exact original instruction annotations, register operands and remaining
    second symbolic HI/LO must be present. Generated source stays private.
    """
    if original.count(BEFORE)!=1 or original.count(BEFORE_LO)!=1:
        raise ValueError('Original first controller-offset instructions not unique')
    if original.count('%hi(D_3B07A)')!=2 or original.count('%lo(D_3B07A)')!=2:
        raise ValueError('Original C-Right offsets no longer have exactly two pairs')
    if '/* 5CDAE0 80212550 3C090004 */' not in original or \
       '/* 5CDB20 80212590 9529B07A */' not in original:
        raise ValueError('Original instruction VMA/ROM annotation changed')
    normalized=original.replace(BEFORE,AFTER,1).replace(BEFORE_LO,AFTER_LO,1)
    if normalized.count('%hi(D_3B07A)')!=1 or normalized.count('%lo(D_3B07A)')!=1:
        raise ValueError('Second input gate must retain its genuine symbolic pair')
    # Only exact whole-line operand rewrites may differ; no raw instruction bits
    # or other ASM source text may be altered.
    if normalized.replace(AFTER,BEFORE,1).replace(AFTER_LO,BEFORE_LO,1)!=original:
        raise ValueError("Literal normalization changed unrelated original ASM")
    return normalized


def check_relocation_triplet(original: Counter, normalized: Counter, candidate: Counter,
                             baseline_count: int, normalized_count: int, candidate_count: int,
                             baseline_hash: str, normalized_hash: str, candidate_hash: str):
    """No filtering, masking or metadata patching of original or candidate ELF."""
    if not all(isinstance(x,Counter) for x in (original,normalized,candidate)):
        raise TypeError('Expected three original ELF relocation multisets')
    if (baseline_count,normalized_count,candidate_count)!=(80747,80745,80745):
        raise ValueError('FAILED_RELOC: unexpected complete-ELF relocation counts')
    if (baseline_hash,normalized_hash,candidate_hash)!=(BASELINE_HASH,NORMALIZED_HASH,NORMALIZED_HASH):
        raise ValueError('FAILED_RELOC: complete-ELF relocation fingerprints changed')
    if sum(original.values())!=80747 or sum(normalized.values())!=80745 or sum(candidate.values())!=80745:
        raise ValueError('FAILED_RELOC: input relocation multiplicities inconsistent')
    if original-normalized != SYNTHETIC_PAIR or normalized-original or original-candidate!=SYNTHETIC_PAIR or candidate-original:
        raise ValueError('FAILED_RELOC: unrecognised original-to-literal or original-to-C delta')
    if normalized!=candidate:
        raise ValueError('FAILED_RELOC: matching C differs from normalized original-ASM reference')
    return dict(original_relocation_count=80747,independent_original_asm_relocation_count=80745,
                compiled_c_relocation_count=80745,real_relocations_exact_in_independent_reference=True,
                original_to_independent_missing=[list(x) for x in sorted(SYNTHETIC_PAIR)],
                original_reloc_sha256=BASELINE_HASH,independent_original_asm_reloc_sha256=NORMALIZED_HASH,
                candidate_reloc_sha256=NORMALIZED_HASH)


def check_original_source_provenance(original_checkout: Path, shadow_checkout: Path, candidate_checkout: Path):
    original=(original_checkout/OWNER).read_text()
    shadow=(shadow_checkout/OWNER).read_text()
    candidate=(candidate_checkout/OWNER).read_text()
    if original!=candidate or shadow!=normalize_original_asm(original):
        raise ValueError('FAILED_SOURCE: independent original-ASM reference has unexpected edits')
    autos=(original_checkout/'.splat/japan_0/undefined_syms_auto.ld').read_text()
    explicit_folder=original_checkout/'config/japan_0/symbol_addrs'
    explicit=[x.read_text(errors='replace') for x in sorted(explicit_folder.rglob('*')) if x.is_file()]
    provenance._check_splat_provenance(autos,explicit)
    if hashlib.sha256((candidate_checkout/cr.C_PATH).read_bytes()).hexdigest()!=cr.SRC_SHA:
        raise ValueError('FAILED_SOURCE: C-Right source changed')
    stage=json.loads((candidate_checkout/cr.STAGE).read_text())
    if stage.get('source_sha256')!=cr.SRC_SHA or stage.get('name')!=cr.TARGET:
        raise ValueError('FAILED_SOURCE: C-Right stage changed')
    return {'original_asm_sha256':hashlib.sha256(original.encode()).hexdigest(),
            'normalized_original_asm_sha256':hashlib.sha256(shadow.encode()).hexdigest(),
            'c_sha256':cr.SRC_SHA, 'symbol_provenance':'Splat undefined_syms_auto.ld only'}


def verify_three_way(original_checkout: Path, shadow_checkout: Path, candidate_checkout: Path):
    """Full original vs independent-ASM vs C linked ELF and 32 MiB ROM gate."""
    original_checkout=Path(original_checkout).resolve()
    shadow_checkout=Path(shadow_checkout).resolve()
    candidate_checkout=Path(candidate_checkout).resolve()
    authenticated=cr.original(candidate_checkout)
    for label,co in [('original',original_checkout),('normalized ASM',shadow_checkout),('matching C',candidate_checkout)]:
        if cr.original(co)!=authenticated:
            raise ValueError('FAILED_ROM: independent source ROM authentication differs '+label)
        if (co/'build/japan_0/mnsg.z64').read_bytes()!=authenticated:
            raise ValueError('FAILED_ROM: complete candidate differs '+label)
    prov=check_original_source_provenance(original_checkout,shadow_checkout,candidate_checkout)
    objects=[];relocs=[]
    for co in (original_checkout,shadow_checkout,candidate_checkout):
        elf=co/'build/japan_0/mnsg.elf'
        identities=cross._funcs(elf)
        obj,n,h=glitch.all_semantic_relocations(elf)
        objects.append(identities);relocs.append((obj,n,h))
    if objects[0]!=objects[1] or objects[1]!=objects[2] or sum(objects[0].values())!=7376:
        raise ValueError('FAILED_ELF: three-way function identities differ')
    native_reloc=check_relocation_triplet(relocs[0][0],relocs[1][0],relocs[2][0],
                        relocs[0][1],relocs[1][1],relocs[2][1],
                        relocs[0][2],relocs[1][2],relocs[2][2])
    origc=cr.c_identities(original_checkout/'build/japan_0/mnsg.elf')
    normc=cr.c_identities(shadow_checkout/'build/japan_0/mnsg.elf')
    candc=cr.c_identities(candidate_checkout/'build/japan_0/mnsg.elf')
    if (len(origc),len(normc),len(candc))!=(2369,2369,2370) or origc!=normc or \
         candc-origc!={cr.TARGET} or origc-candc:
        raise ValueError('FAILED_INVENTORY: unexpected original function ownership')
    obj=candidate_checkout/'build/japan_0/src/jpcright/stage_initializer.c.o'
    _addr,n,body,align=jp329.text_section(obj)
    if n!=cr.SIZE:
        raise ValueError('FAILED_NATIVE: IDO source-object function extent differs')
    # The relocatable IDO .o still contains unresolved HI16/LO16 immediates.
    # Compare the already linked complete image at the original ROM offset,
    # rather than incorrectly comparing unrelocated .o bytes to linked ROM.
    linked=(candidate_checkout/'build/japan_0/mnsg.z64').read_bytes()
    if hashlib.sha256(linked[cr.ROM_OFF:cr.ROM_OFF+cr.SIZE]).hexdigest()!=cr.CODE_SHA:
        raise ValueError('FAILED_NATIVE: original-address linked function differs')
    res={
        'format':'goemon-jpcright-dual-original-reference-G2-v1',
        'status':'PASSED_G2_DUAL_REFERENCE_LOCAL',
        'ordinary_raw_splat_relocations_exact':False,
        'normalizer_intent':'Use independently assembled authentic original ASM with two numeric offset spellings as semantic relocation reference',
        'normalizer_scope':'Exactly two original first-input synthetic D_3B07A HI16/LO16 records',
        'original_rom_sha1':cr.ROM_SHA, 'full_original_rom_bytes':len(authenticated),
        'elf_identities':7376, 'region':REGION,
        'accepted_functions_before':2369,'candidate_functions_after':2370,
        'original_C_bytes_before':126612,'candidate_C_bytes_after':127008,
        'original_asm_remaining':5006,'new_C_function':cr.TARGET,
        'function_rom_offset':f'{cr.ROM_OFF:#x}','function_vma':f'{cr.VMA:#x}',
        'function_bytes':cr.SIZE, 'function_sha256':cr.CODE_SHA,
        'provenance':prov,'relocation_proof':native_reloc,
        'gameplay':'NOT_RUN'
    }
    return res


def stage_independent_asm_reference(shadow_checkout: Path):
    """On a fresh private COPY of staged JP2370, restore original-ASM ownership.

    Never alter C or ELF relocations; only two exact assembler operand spellings
    in original Splat source and one existing linker ownership reference change.
    """
    co=Path(shadow_checkout).resolve()
    cr.original(co)
    stage=json.loads((co/cr.STAGE).read_text())
    if stage.get('name')!=cr.TARGET or stage.get('source_sha256')!=cr.SRC_SHA:
        raise ValueError('FAILED_STAGE: stage source differs from proven C')
    source=co/OWNER
    orig=source.read_text()
    expected_sha='f8a1c03f56d30ba28b281c9ce3c163a8fca94a82ec10083e68ba2b6aa8b26e90'
    if hashlib.sha256(orig.encode()).hexdigest()!=expected_sha:
        raise ValueError('FAILED_SOURCE: original generated ASM source hash drift')
    normal=normalize_original_asm(orig)
    linker=co/'.splat/japan_0/mnsg.ld'
    old=linker.read_text()
    prefix='        build/japan_0/'
    triple=(prefix+'asm/japan_0/jpcright_before.s.o(.text);\n'+
            prefix+'src/jpcright/stage_initializer.c.o(.text);\n'+
            prefix+'asm/japan_0/jpcright_after.s.o(.text);')
    if old.count(triple)!=1 or f'build/japan_0/{OWNER}.o(.text);' in old:
        raise ValueError('FAILED_LINK: original exact three-section ownership absent or duplicated')
    new=old.replace(triple,prefix+OWNER+'.o(.text);')
    # Do not mutate unrelated project files, assembler fragments or library.
    source.write_text(normal)
    linker.write_text(new)
    return {'original_asm_sha256':expected_sha,
            'normalized_asm_sha256':hashlib.sha256(normal.encode()).hexdigest(),
            'asm_owner':OWNER,'target':cr.TARGET}


def build_independent_asm_reference(shadow_checkout: Path, dependencies: Path, runtime: Path):
    """Use the complete accepted JP2369 C source list, but original ASM for target."""
    co=Path(shadow_checkout).resolve()
    cr.original(co)
    if (co/OWNER).read_text().count(BEFORE):
        raise ValueError('FAILED_SOURCE: shadow offset symbols not normalized')
    expected_sha='54e3ff201c3e9388bccd5bc8f9e71cdaacdca462b37b0fc7cc20528cc5e0fe5c'
    if hashlib.sha256((co/OWNER).read_bytes()).hexdigest()!=expected_sha:
        raise ValueError('FAILED_SOURCE: normalized original ASM changed')
    before=json.loads((co/'build/japan_0/glitch-g2-stage.json').read_text())
    vm=json.loads((co/'build/japan_0/vm-g2-stage.json').read_text())
    jp=json.loads((co/'build/japan_0/jp55-stage.json').read_text())
    if len(jp['functions'])!=55:raise ValueError('FAILED_BASE: missing JP55 native stage')
    sources=[e['source'] for e in before['new_functions']]+[e['source'] for e in vm['functions']]+[e['source'] for e in jp['functions']]
    args=glitch.makeargs(co,'japan_0',{'new_functions':[{'source':src} for src in sources]})
    env=jp329.env_for(Path(dependencies).resolve(),Path(runtime).resolve())
    obj=co/f'build/japan_0/{OWNER}.o'
    if obj.exists():obj.unlink()  # force real original-ASM reassembly
    for name in ('mnsg.elf','mnsg.z64'):
        path=co/'build/japan_0'/name
        if path.exists():path.unlink()
    subprocess.run(args+['build/japan_0/mnsg.z64'],cwd=co,env=env,check=True,stdout=subprocess.DEVNULL)
    rom=cr.original(co)
    if (co/'build/japan_0/mnsg.z64').read_bytes()!=rom:
        raise ValueError('FAILED_ROM: normalized original ASM reference differs')
    ids=cr.c_identities(co/'build/japan_0/mnsg.elf')
    if len(ids)!=2369 or cr.TARGET in ids:
        raise ValueError('FAILED_INVENTORY: independent reference incorrectly owns C-Right')
    _,num,h=glitch.all_semantic_relocations(co/'build/japan_0/mnsg.elf')
    if num!=80745 or h!=NORMALIZED_HASH:
        raise ValueError('FAILED_RELOC: independent original-ASM reference drift')
    return {'rom_sha1':cr.ROM_SHA,'elf_c_count':2369,'independent_asm_relocations':num,
            'independent_asm_relocations_sha256':h}


def main():
    import argparse
    ap=argparse.ArgumentParser(description='Strict three-way Japanese C-Right native proof')
    ap.add_argument('action',choices=['shadow-stage','shadow-build','verify'])
    ap.add_argument('--original',type=Path)
    ap.add_argument('--shadow',type=Path,required=True)
    ap.add_argument('--candidate',type=Path)
    ap.add_argument('--deps',type=Path)
    ap.add_argument('--runtime',type=Path)
    ap.add_argument('--report',type=Path)
    args=ap.parse_args()
    if args.action=='shadow-stage':result=stage_independent_asm_reference(args.shadow)
    elif args.action=='shadow-build':
        if args.deps is None or args.runtime is None:ap.error('shadow-build needs --deps and --runtime')
        result=build_independent_asm_reference(args.shadow,args.deps,args.runtime)
    else:
        if args.original is None or args.candidate is None:ap.error('verify needs --original and --candidate')
        result=verify_three_way(args.original,args.shadow,args.candidate)
    if args.report:
        if args.report.exists():raise FileExistsError('Proof report must not overwrite an existing file')
        args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
