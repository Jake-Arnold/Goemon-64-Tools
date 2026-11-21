"""Fail-closed original-USA native-C insertion-wrapper promotion after USA 1962.

Must execute on the previous independently verified 1962-C candidate. Does
not patch original instructions or permit relocated semantic changes.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

from . import scheduler4_g2_promotion as previous
from . import verify as decomp_verify
from .inventory import summarize_inventory
from .japan_noop_port import env_for

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'research/scheduler5_20261121'
FIXTURE=BASE/'manifest.json'
ORIGINAL_SHA1='6ea0ed71032ce08fc2745f412d84936382197494'

def sha(data):return hashlib.sha256(data).hexdigest()

def fixture():
    d=json.loads(FIXTURE.read_text())
    f=d['functions'][0]
    assert len(d['functions'])==1
    assert (d['format'],d['region'],d['accepted_prior_count'],d['accepted_prior_bytes'],d['original_owner'])==('goemon-usa-scheduler5-after-1962-v1','usa',1962,84484,'asm/usa/35280_sched4_00.s')
    assert (f['name'],f['rom_offset'],f['vma'],f['size'],f['source'])==('func_80034B24_35724',0x35724,0x80034B24,52,'scheduler_insert52.c')
    assert sha((BASE/'sources'/f['source']).read_bytes())==f['source_sha256']
    assert d['expanded_sha1']==ORIGINAL_SHA1
    return d

def stage(checkout,prior):
    p=Path(checkout).resolve();prior=Path(prior).resolve();d=fixture();f=d['functions'][0]
    rom=previous.original_rom(p)
    assert (p/'build/usa/mnsg.z64').read_bytes()==rom
    assert sha(rom[f['rom_offset']:f['rom_offset']+f['size']])==f['original_code_sha256']
    proof=json.loads((p/'build/usa/scheduler4-proof.json').read_text())
    assert proof['status']=='PASSED_G2_LOCAL' and proof['accepted_after']==1962 and proof['semantic_relocations']==82103
    claim={e['name'] for e in decomp_verify.claimed_functions(decomp_verify.load_manifest(ROOT/'manifest.json'))}
    claim.update(('func_8001F8B0_204B0','func_8001F940_20540'))
    claim.update(e['name'] for e in previous.load_fixture()['functions'])
    assert f['name'] not in claim
    assert not prior.exists(), 'Predecessor backup must be new'
    (prior/'build/usa').mkdir(parents=True)
    for n in ('mnsg.z64','mnsg.elf'):shutil.copy2(p/'build/usa'/n,prior/'build/usa'/n)
    owner=p/d['original_owner']; t=owner.read_text()
    head=t[:t.index('nonmatching ')]
    expr=r'(?ms)^nonmatching '+re.escape(f['name'])+r', 0x34\s*.*?^endlabel '+re.escape(f['name'])+r'\s*'
    m=re.search(expr,t)
    assert m, 'Original function not in its verified original owner'
    offsets=[int(x,16) for x in re.findall(r'/\* ([0-9A-Fa-f]+) [0-9A-Fa-f]+ [0-9A-Fa-f]+ \*/',m.group())]
    assert len(offsets)==13 and offsets[0]==f['rom_offset'] and offsets[-1]==f['rom_offset']+48
    (p/'asm/usa/35280_sched5_00.s').write_text(t[:m.start()])
    (p/'asm/usa/35280_sched5_01.s').write_text(head+t[m.end():])
    shutil.copy2(BASE/'sources'/f['source'],p/'src'/f['source'])
    link=p/'.splat/usa/mnsg.ld';ld=link.read_text()
    marker='build/usa/asm/usa/35280_sched4_00.s.o(.text);'
    assert ld.count(marker)==1
    new='\n'.join('        '+piece for piece in ('build/usa/asm/usa/35280_sched5_00.s.o(.text);','build/usa/src/scheduler_insert52.c.o(.text);','build/usa/asm/usa/35280_sched5_01.s.o(.text);'))
    link.write_text(ld.replace(marker,new))
    return d

def build(checkout,deps,runtime):
    p=Path(checkout).resolve();f=fixture()['functions'][0]
    assert sha((p/'src'/f['source']).read_bytes())==f['source_sha256']
    env=env_for(Path(deps),Path(runtime))
    def run(args):subprocess.run(args,env=env,cwd=p,check=True,stdout=subprocess.DEVNULL)
    for n in ('35280_sched5_00.s','35280_sched5_01.s'):
        run(['mips-linux-gnu-as','-no-pad-sections','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(p/'build/usa/asm/usa'/(n+'.o')),f'asm/usa/{n}'])
    run(['make','-j4','VERSION=usa','build/usa/src/scheduler_insert52.c.o'])
    previous.shrink_zero_text_tail(p/'build/usa/src/scheduler_insert52.c.o',52)
    for n in ('mnsg.elf','mnsg.z64'):(p/'build/usa'/n).unlink(missing_ok=True)
    run(['make','-j4','VERSION=usa','build/usa/mnsg.z64'])
    rom=previous.original_rom(p)
    if (p/'build/usa/mnsg.z64').read_bytes()!=rom:raise ValueError('FAILED_ROM')
    return {'rom_exact':True,'original_bytes':len(rom),'source_original_bytes':52}

def verify(checkout,prior,original):
    p=Path(checkout).resolve();prior=Path(prior).resolve();original=Path(original).resolve()
    f=fixture()['functions'][0];rom=previous.original_rom(p)
    assert (p/'build/usa/mnsg.z64').read_bytes()==(prior/'build/usa/mnsg.z64').read_bytes()==rom
    a,b=prior/'build/usa/mnsg.elf',p/'build/usa/mnsg.elf'
    ids1,ids2=previous.funcs(a),previous.funcs(b)
    assert ids1==ids2 and sum(ids2.values())==7376
    r1,r2=previous.relocs(a),previous.relocs(b)
    assert r1==r2 and sum(r2.values())==82103
    table=subprocess.check_output(['mips-linux-gnu-objdump','-t',str(b)],text=True)
    assert f['name'] in table and f['name']+'.NON_MATCHING' not in table
    claims=[e['name'] for e in decomp_verify.claimed_functions(decomp_verify.load_manifest(ROOT/'manifest.json'))]
    claims+=['func_8001F8B0_204B0','func_8001F940_20540']
    claims += [e['name'] for e in previous.load_fixture()['functions']]
    claims.append(f['name'])
    orig=subprocess.check_output(['readelf','-Ws',str(original/'build/usa/mnsg.elf')],text=True)
    newer=subprocess.check_output(['readelf','-Ws',str(b)],text=True)
    inv=summarize_inventory(orig,newer,claims)
    assert inv['newly_matching_c']==1963 and inv['remaining_assembly_entries']==5400 and inv['extra_positive_alias_entries']==0
    result={'status':'PASSED_G2_LOCAL','region':'usa','accepted_before':1962,'accepted_after':1963,'instruction_bytes_added':52,'total_original_C_instruction_bytes':84536,'remaining_asm':5400,'rom_bytes':len(rom),'rom_sha1':ORIGINAL_SHA1,'elf_function_identities':7376,'semantic_relocations':82103,'original_function':f,'inventory':inv}
    (p/'build/usa/scheduler5-proof.json').write_text(json.dumps(result,indent=2)+'\n')
    return {k:v for k,v in result.items() if k not in ('inventory','original_function')}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=('stage','build','verify'))
    parser.add_argument('--checkout',type=Path,required=True)
    parser.add_argument('--prior',type=Path)
    parser.add_argument('--original',type=Path)
    parser.add_argument('--deps',type=Path)
    parser.add_argument('--runtime',type=Path)
    a=parser.parse_args()
    if a.action=='stage':r=stage(a.checkout,a.prior)
    elif a.action=='build':r=build(a.checkout,a.deps,a.runtime)
    else:r=verify(a.checkout,a.prior,a.original)
    print(json.dumps(r,indent=2))

if __name__=='__main__':main()
