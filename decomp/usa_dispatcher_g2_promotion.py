"""Fail-closed original-USA IDO C promotion of 0x80002040 after accepted USA1965.

Original ROM, assembly, linked objects and program binaries remain local.
The 'stage' operation does not claim promotion; only 'verify' can produce proof.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from . import verify as verifier
from .inventory import summarize_inventory
from .scheduler4_g2_promotion import funcs, relocs, shrink_zero_text_tail
from .japan_noop_port import env_for

BASE=Path(__file__).resolve().parent
RESEARCH=BASE/'research/usa_dispatcher_2c40_20261121'
MANIFEST=RESEARCH/'manifest.json'
SOURCE=RESEARCH/'sources/usa_state_dispatch.c'
ROM_SHA1='6ea0ed71032ce08fc2745f412d84936382197494'
TITLE='goemon-usa-dispatcher-2c40-after-1965-v1'
FILENAME='game_state_dispatch_2c40.c'
ASM='asm/usa/2C40_w132_00.s'
LINK_MARKER='build/usa/asm/usa/2C40_w132_00.s.o(.text);'
C_MARKER='build/usa/src/'+FILENAME+'.o(.text);'

def sha(data):return hashlib.sha256(data).hexdigest()

def fixture():
    m=json.loads(MANIFEST.read_text())
    if set(m)!={'format','region','original_rom_sha1','accepted_prior_count','accepted_prior_original_C_bytes','owner','function','expected_rom_bytes','expected_elf_functions','expected_relocations'}:
        raise ValueError('Unsupported dispatcher manifest fields')
    if (m['format'],m['region'],m['original_rom_sha1'],m['accepted_prior_count'],m['accepted_prior_original_C_bytes'],m['owner'],m['expected_rom_bytes'],m['expected_elf_functions'],m['expected_relocations'])!=(TITLE,'usa',ROM_SHA1,1965,84648,ASM,33554432,7376,82103):
        raise ValueError('Wrong original-USA dispatcher acceptance baseline')
    e=m['function']
    if set(e)!={'name','rom_offset','vma','size','source','source_sha256','original_code_sha256'}:raise ValueError('Unsupported dispatcher function fields')
    if (e['name'],e['rom_offset'],e['vma'],e['size'],e['source'])!=('func_80002040_2C40',0x2c40,0x80002040,120,'usa_state_dispatch.c'):
        raise ValueError('Wrong original-address function')
    if sha(SOURCE.read_bytes())!=e['source_sha256']:raise ValueError('Dispatcher C source hash changed')
    return m

def original_rom(checkout):
    file=Path(checkout)/'config/usa/baserom.decompressed.z64'
    raw=file.read_bytes()
    if len(raw)!=33554432 or hashlib.sha1(raw).hexdigest()!=ROM_SHA1:raise ValueError('Wrong original USA decompressed ROM')
    return raw

def expected_predecessor(checkout,entry):
    checkout=Path(checkout)
    rom=original_rom(checkout)
    if (checkout/'build/usa/mnsg.z64').read_bytes()!=rom:raise ValueError('Not the original-USA byte-identical baseline')
    proof=json.loads((checkout/'build/usa/scheduler6-proof.json').read_text())
    if proof['accepted_after']!=1965 or proof['total_original_C_instruction_bytes']!=84648 or proof['rom_sha1']!=ROM_SHA1 or proof['semantic_relocations']!=82103:
        raise ValueError('Not the already accepted USA1965 linked predecessor')
    if sha(rom[entry['rom_offset']:entry['rom_offset']+entry['size']])!=entry['original_code_sha256']:
        raise ValueError('Wrong original function bytes')
    symbols=subprocess.check_output(['readelf','-Ws',str(checkout/'build/usa/mnsg.elf')],text=True)
    if entry['name']+'.NON_MATCHING' not in symbols:
        raise ValueError('Original function is no longer ASM; another promotion may have occurred')
    return rom

def stage(checkout,prior):
    m=fixture();e=m['function'];checkout=Path(checkout).resolve();prior=Path(prior).resolve()
    expected_predecessor(checkout,e)
    if prior.exists():raise ValueError('Refusing to overwrite existing predecessor')
    (prior/'build/usa').mkdir(parents=True)
    for name in ('mnsg.elf','mnsg.z64'):
        shutil.copy2(checkout/'build/usa'/name,prior/'build/usa'/name)
    path=checkout/ASM
    text=path.read_text()
    pattern=r'(?m)^nonmatching '+re.escape(e['name'])+r', 0x78\s*.*?^endlabel '+re.escape(e['name'])+r'(?=\s|$)'
    spans=list(re.finditer(pattern,text,re.S|re.M))
    if len(spans)!=1:raise ValueError('Original assembly ownership changed')
    insn=re.findall(r'/\* ([0-9A-Fa-f]+) [0-9A-Fa-f]+ [0-9A-Fa-f]+ \*/',spans[0].group())
    if len(insn)!=30 or int(insn[0],16)!=0x2c40 or int(insn[-1],16)!=0x2cb4:
        raise ValueError('Original function extent changed')
    path.write_text(text[:spans[0].start()]+text[spans[0].end():])
    linker=checkout/'.splat/usa/mnsg.ld'
    ld=linker.read_text()
    if ld.count(LINK_MARKER)!=1 or '.main 0x80000450 : AT(main_ROM_START) SUBALIGN(4)' not in ld:
        raise ValueError('Unexpected original linker ownership')
    linker.write_text(ld.replace(LINK_MARKER,C_MARKER+'\n        '+LINK_MARKER))
    shutil.copy2(SOURCE,checkout/'src'/FILENAME)
    result={'format':TITLE,'original_address':'0x80002040','original_rom_offset':'0x2C40','original_bytes':120,
            'source_sha256':e['source_sha256'],'original_instruction_sha256':e['original_code_sha256'],
            'prior_elf_sha256':sha((prior/'build/usa/mnsg.elf').read_bytes()),'accepted_prior_count':1965,'accepted_candidate_count':1966}
    (checkout/'build/usa/dispatcher-stage.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

def build(checkout,deps,runtime):
    checkout=Path(checkout).resolve();m=fixture();e=m['function']
    metadata=json.loads((checkout/'build/usa/dispatcher-stage.json').read_text())
    if metadata['source_sha256']!=e['source_sha256'] or sha((checkout/'src'/FILENAME).read_bytes())!=e['source_sha256']:
        raise ValueError('Staged dispatcher C source has changed')
    env=env_for(Path(deps).resolve(),Path(runtime).resolve())
    def run(cmd):
        return subprocess.run(cmd,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    orig=checkout/ASM;obj=checkout/'build/usa/asm/usa/2C40_w132_00.s.o'
    run(['mips-linux-gnu-as','-no-pad-sections','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(obj),str(orig.relative_to(checkout))])
    run(['make','-j4','VERSION=usa',f'build/usa/src/{FILENAME}.o'])
    shrink_zero_text_tail(checkout/'build/usa/src'/(FILENAME+'.o'),120)
    for name in ('mnsg.elf','mnsg.z64'):(checkout/'build/usa'/name).unlink(missing_ok=True)
    run(['make','-j4','VERSION=usa','build/usa/mnsg.z64'])
    rom=original_rom(checkout)
    if (checkout/'build/usa/mnsg.z64').read_bytes()!=rom:
        raise ValueError('FAILED_ROM: candidate diverges from original-USA ROM')
    return {'rom_bytes':33554432,'rom_sha1':ROM_SHA1,'original_C_bytes_added':120}

def verify(checkout,prior,original):
    checkout=Path(checkout).resolve();prior=Path(prior).resolve();original=Path(original).resolve()
    m=fixture();e=m['function']
    rom=original_rom(checkout)
    if (checkout/'build/usa/mnsg.z64').read_bytes()!=rom or (prior/'build/usa/mnsg.z64').read_bytes()!=rom:
        raise ValueError('Prior or candidate original-ROM equality failed')
    old=prior/'build/usa/mnsg.elf';new=checkout/'build/usa/mnsg.elf'
    before=funcs(old);after=funcs(new)
    if before!=after or sum(after.values())!=7376:
        raise ValueError('Original ELF function identity or size drift')
    preloc=relocs(old);postloc=relocs(new)
    if preloc!=postloc or sum(postloc.values())!=82103:
        raise ValueError('Original semantic relocation multiset drift')
    if sha(rom[0x2c40:0x2cb8])!=e['original_code_sha256']:
        raise ValueError('Original function code hash differs')
    original_text=subprocess.check_output(['readelf','-Ws',str(original/'build/usa/mnsg.elf')],text=True)
    candidate_text=subprocess.check_output(['readelf','-Ws',str(new)],text=True)
    original_claims=[f['name'] for f in verifier.claimed_functions(verifier.load_manifest(BASE/'manifest.json'))]
    additionally=['func_8001F8B0_204B0','func_8001F940_20540',
        'func_80034DD8_359D8','func_80034E08_35A08','func_80034E38_35A38','func_80034E68_35A68',
        'func_80034B24_35724','func_80034C4C_3584C','func_80034C84_35884',e['name']]
    claims=original_claims+additionally
    if len(claims)!=1966 or len(set(claims))!=1966:raise ValueError('Stale or duplicated canonical stage claims')
    summary=summarize_inventory(original_text,candidate_text,claims)
    if (summary['newly_matching_c'],summary['remaining_assembly_entries'],summary['extra_positive_alias_entries'])!=(1966,5397,0):
        raise ValueError('Strict function inventory rejected the promotion')
    proof={'format':TITLE,'status':'PASSED_G2_LOCAL','region':'usa',
           'accepted_before':1965,'new_C_functions':1,'original_instruction_bytes_added':120,
           'accepted_after':1966,'total_original_C_instruction_bytes':84768,'remaining_assembly_entries':5397,
           'original_rom_bytes':33554432,'original_rom_sha1':ROM_SHA1,'original_elf_function_identities':7376,
           'semantic_relocation_records':82103,'all_relocations_equal':True,
           'source_sha256':e['source_sha256'],'original_code_sha256':e['original_code_sha256'],
           'inventory':summary}
    (checkout/'build/usa/dispatcher-g2-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
    return proof

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=('stage','build','verify'));p.add_argument('--checkout',type=Path,required=True)
    p.add_argument('--prior',type=Path);p.add_argument('--original',type=Path);p.add_argument('--deps',type=Path);p.add_argument('--runtime',type=Path)
    a=p.parse_args()
    if a.action=='stage':
        if not a.prior:p.error('stage needs --prior')
        r=stage(a.checkout,a.prior)
    elif a.action=='build':
        if not a.deps or not a.runtime:p.error('build needs --deps and --runtime')
        r=build(a.checkout,a.deps,a.runtime)
    else:
        if not a.prior or not a.original:p.error('verify needs --prior and --original')
        r=verify(a.checkout,a.prior,a.original)
    print(json.dumps({k:v for k,v in r.items() if k!='inventory'},indent=2))
if __name__=='__main__':main()
