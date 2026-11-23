#!/usr/bin/env python3
"""Read-only native script-VM probes; no canonical promotion or relocation edits."""
import argparse, hashlib, json, os, re, subprocess, sys
from pathlib import Path
from collections import Counter

p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--binutils',type=Path,required=True);p.add_argument('--lib',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
a.repo=a.repo.resolve();a.baseline=a.baseline.resolve();a.out=a.out.resolve();a.out.mkdir(exist_ok=False,parents=True)
sys.path.insert(0,str(a.repo));from decomp.probe import Elf32,compare_code
sha=lambda b:hashlib.sha256(b).hexdigest()
rom=(a.baseline/'config/usa/baserom.decompressed.z64').read_bytes()
assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()=='6ea0ed71032ce08fc2745f412d84936382197494'
assert (a.baseline/'build/usa/mnsg.z64').read_bytes()==rom
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.baseline,text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
assert not subprocess.check_output(['git','diff','--name-only'],cwd=a.baseline,text=True).strip()
cc=a.baseline/'tools/ido-5.3/cc';assert sha(cc.read_bytes())=='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
ledger=a.repo/'decomp/COMPILER_QUIRKS.md';assert ledger.is_file()
flags='-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Iinclude -Ilibultra/include -Ilibultra/include/PR -Isrc -I. -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2'.split()
env=os.environ.copy();env['LD_LIBRARY_PATH']=str(a.lib.resolve())+':'+env.get('LD_LIBRARY_PATH','')
ld=str(a.binutils.resolve()/'mips-linux-gnu-ld')
orig=Elf32((a.baseline/'build/usa/asm/usa/3DBA0.s.o').read_bytes());baseline=Elf32((a.baseline/'build/usa/mnsg.elf').read_bytes());g=baseline.globals()
def relocs(e,f):
    return Counter((r.offset-f.value,r.relocation_type,r.symbol.name or e.names[r.symbol.section]) for r in e.relocations(f.section) if f.value<=r.offset<f.value+f.size)
def run(cmd,log):
    with log.open('w') as o:subprocess.run(cmd,cwd=a.baseline,env=env,check=True,stdout=o,stderr=subprocess.STDOUT)
rows=[]
for path in sorted((Path(__file__).parent/'sources').glob('*.c')):
    # Re-read ledger before each native attempt; existing line grouping, mask and named-vs-literal scheduling observations apply.
    ledger.read_text()
    name='func_8003E234_3EE34' if path.name.startswith(('440','func_8003E234')) else 'func_8003F37C_3FF7C'
    vma,off,size=(0x8003E234,0x3EE34,440) if name.endswith('3EE34') else (0x8003F37C,0x3FF7C,192)
    expected=rom[off:off+size];of=orig.function(name);assert of.size==size and baseline.function(name).value==vma
    o=a.out/(path.stem+'.o');elf=a.out/(path.stem+'.elf');script=a.out/(path.stem+'.ld')
    run([str(cc),*flags,str(path.resolve()),'-o',str(o)],a.out/(path.stem+'.compile.log'))
    e=Elf32(o.read_bytes());f=e.function(name);r0=relocs(orig,of);r1=relocs(e,f)
    defs=[]
    for n in sorted(e.undefined()):
        assert n in g and re.fullmatch(r'[A-Za-z_.$][A-Za-z0-9_.$]*',n);defs.append(f'{n} = 0x{g[n]:08x};')
    ro='';pool=None
    if '.rodata' in e.names:
        data=e.payload(e.names.index('.rodata'))
        if data:
            assert name.endswith('3FF7C') and data[:4]==rom[0x7DD08:0x7DD0C] and not any(data[4:]);ro='.rodata 0x8007D108 : SUBALIGN(4) { *(.rodata) }';pool=sha(data[:4])
    script.write_text(f'ENTRY({name})\nSECTIONS {{ .text 0x{vma:08X} : SUBALIGN(4) {{ *(.text) }} {ro} /DISCARD/ : {{ *(*) }} }}\n'+'\n'.join(defs)+'\n')
    run([ld,'-T',str(script),'--emit-relocs','-o',str(elf),str(o)],a.out/(path.stem+'.link.log'))
    linked=Elf32(elf.read_bytes());lf=linked.function(name);assert lf.value==vma
    cmp=compare_code(expected,linked.code(lf))
    expected_pass=path.name=='func_8003E234_3EE34.c';same=cmp['word_differences']==0 and r0==r1 and lf.size==size
    assert same==expected_pass,(path.name,cmp,r0-r1,r1-r0)
    if path.name=='literal.c':assert cmp['word_differences']==0 and r0!=r1
    first=cmp['first_mismatch_offset'];delta=(r0-r1)+(r1-r0)
    outcome='EXISTING_QUIRK_REPRODUCED' if path.name in ('440_no_mask.c','440_split_line.c','func_8003E234_3EE34.c','literal.c','F37C.c') else 'EXISTING_QUIRK_NOT_APPLICABLE'
    rows.append(dict(source=path.name,source_sha256=sha(path.read_bytes()),function=name,region='usa',rom_offset=hex(off),vma=hex(vma),original_bytes=size,compiled_func_size=lf.size,word_differences=cmp['word_differences'],first_instruction_mismatch_offset=first,expected_code_sha256=cmp['expected_sha256'],candidate_code_sha256=cmp['actual_sha256'],named_relocations_original=sum(r0.values()),named_relocations_candidate=sum(r1.values()),named_relocation_exact=r0==r1,removed_relocations=[list(k) for k in sorted((r0-r1).elements())],added_relocations=[list(k) for k in sorted((r1-r0).elements())],first_relocation_mismatch_offset=min((k[0] for k in delta),default=None),native_pool_sha256=pool,compiler_quirk_outcome=outcome,status='ISOLATED_EXACT' if same else 'RESEARCH_ONLY'))
result={'format':'goemon-script-vm-followup-native-probe-v1','base_sha':'78e6303e2fe5f4e5f5a17bab50cb62fc792d241b','upstream':'7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee','compiler_sha256':sha(cc.read_bytes()),'compiler_flags':flags,'ledger_sha256':sha(ledger.read_bytes()),'baseline_rom_sha1':hashlib.sha1(rom).hexdigest(),'baseline_rom_bytes':len(rom),'native_invocations':len(rows),'rows':rows,'canonical_promotion':'NOT_RUN','gameplay':'NOT_RUN'}
(a.out/'evidence.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps([{k:r[k] for k in ('source','compiled_func_size','word_differences','first_instruction_mismatch_offset','named_relocation_exact','first_relocation_mismatch_offset','status')} for r in rows],indent=2))
