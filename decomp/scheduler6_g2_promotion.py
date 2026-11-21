"""Fail-closed 56-byte pair of original USA task-insertion-mode wrappers.

Requires native-combined G2 of the preceding 1963-stage; no ASM edits permitted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

from . import scheduler5_g2_promotion as preceding
from . import scheduler4_g2_promotion as sched4
from . import verify as decomp_verify
from .inventory import summarize_inventory
from .japan_noop_port import env_for

ROOT=Path(__file__).resolve().parent
DIR=ROOT/'research/scheduler6_20261121'
FMT='goemon-usa-scheduler6-after-1963-v1'
SHA1=sched4.SHA1

def sha(data):return hashlib.sha256(data).hexdigest()

def fixture():
    d=json.loads((DIR/'manifest.json').read_text())
    assert d['format']==FMT and d['region']=='usa' and d['expanded_sha1']==SHA1
    assert (d['accepted_prior_count'],d['accepted_prior_bytes'],d['original_owner'])==(1963,84536,'asm/usa/35280_sched5_01.s')
    assert len(d['functions'])==2
    for i,f in enumerate(d['functions']):
        assert (f['name'],f['rom_offset'],f['vma'],f['size'],f['source'])==(
            ('func_80034C4C_3584C','func_80034C84_35884')[i],(0x3584C,0x35884)[i],(0x80034C4C,0x80034C84)[i],56,f'sched_insert56_mode{i+1}.c')
        assert sha((DIR/'sources'/f['source']).read_bytes())==f['source_sha256']
    return d

def accepted_claims():
    names=[x['name'] for x in decomp_verify.claimed_functions(decomp_verify.load_manifest(ROOT/'manifest.json'))]
    names+=['func_8001F8B0_204B0','func_8001F940_20540']
    names+=[x['name'] for x in sched4.load_fixture()['functions']]
    names+=[x['name'] for x in preceding.fixture()['functions']]
    return names

def stage(checkout,prior):
    checkout=Path(checkout).resolve();prior=Path(prior).resolve();d=fixture();rom=sched4.original_rom(checkout)
    assert (checkout/'build/usa/mnsg.z64').read_bytes()==rom
    assert not prior.exists()
    proof=json.loads((checkout/'build/usa/scheduler5-proof.json').read_text())
    assert proof['status']=='PASSED_G2_LOCAL' and proof['accepted_after']==1963 and proof['semantic_relocations']==82103
    claims=set(accepted_claims())
    for f in d['functions']:
        assert f['name'] not in claims
        assert sha(rom[f['rom_offset']:f['rom_offset']+56])==f['original_code_sha256']
    (prior/'build/usa').mkdir(parents=True)
    for n in ('mnsg.elf','mnsg.z64'):shutil.copy2(checkout/'build/usa'/n,prior/'build/usa'/n)
    owner=checkout/d['original_owner'];text=owner.read_text();head=text[:text.index('nonmatching ')]
    parts=[];start=0;frags=[]
    for i,f in enumerate(d['functions']):
        match=re.search(r'(?ms)^nonmatching '+f['name']+r', 0x38\s*.*?^endlabel '+f['name']+r'\s*',text)
        assert match and match.start()>=start
        addresses=[int(x,16) for x in re.findall(r'/\* ([0-9A-Fa-f]+) [0-9A-Fa-f]+ [0-9A-Fa-f]+ \*/',match.group())]
        assert len(addresses)==14 and addresses[0]==f['rom_offset'] and addresses[-1]==f['rom_offset']+52
        frag=f'35280_sched6_{i:02}.s';frags.append(frag)
        (checkout/'asm/usa'/frag).write_text((text[start:match.start()] if i==0 else head+text[start:match.start()]))
        parts.extend((f'build/usa/asm/usa/{frag}.o(.text);',f'build/usa/src/{f["source"]}.o(.text);'))
        shutil.copy2(DIR/'sources'/f['source'],checkout/'src'/f['source'])
        start=match.end()
    frag=f'35280_sched6_{len(d["functions"]):02}.s';frags.append(frag)
    (checkout/'asm/usa'/frag).write_text(head+text[start:])
    parts.append(f'build/usa/asm/usa/{frag}.o(.text);')
    linker=checkout/'.splat/usa/mnsg.ld';ld=linker.read_text()
    marker='build/usa/asm/usa/35280_sched5_01.s.o(.text);';assert ld.count(marker)==1
    linker.write_text(ld.replace(marker,'\n'.join('        '+x for x in parts)))
    return {'staged':len(d['functions']),'asm_fragments':frags}

def build(checkout,deps,runtime):
    checkout=Path(checkout).resolve();d=fixture();env=env_for(Path(deps),Path(runtime))
    def run(args):subprocess.run(args,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    for i in range(3):
        n=f'35280_sched6_{i:02}.s'
        run(['mips-linux-gnu-as','-no-pad-sections','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(checkout/'build/usa/asm/usa'/(n+'.o')),f'asm/usa/{n}'])
    for f in d['functions']:
        assert sha((checkout/'src'/f['source']).read_bytes())==f['source_sha256']
        run(['make','-j4','VERSION=usa','build/usa/src/'+f['source']+'.o'])
        sched4.shrink_zero_text_tail(checkout/'build/usa/src'/(f['source']+'.o'),56)
    for n in ('mnsg.elf','mnsg.z64'):(checkout/'build/usa'/n).unlink(missing_ok=True)
    run(['make','-j4','VERSION=usa','build/usa/mnsg.z64'])
    rom=sched4.original_rom(checkout)
    if (checkout/'build/usa/mnsg.z64').read_bytes()!=rom:raise ValueError('FAILED_ROM: not original 32 MiB')
    return {'rom_exact':True,'original_rom_bytes':len(rom),'new_C_bytes':112}

def verify(checkout,prior,original):
    checkout=Path(checkout).resolve();prior=Path(prior).resolve();original=Path(original).resolve()
    f=fixture()['functions'];rom=sched4.original_rom(checkout)
    assert (checkout/'build/usa/mnsg.z64').read_bytes()==(prior/'build/usa/mnsg.z64').read_bytes()==rom
    a=prior/'build/usa/mnsg.elf';b=checkout/'build/usa/mnsg.elf'
    id1,id2=sched4.funcs(a),sched4.funcs(b);assert id1==id2 and sum(id2.values())==7376
    r1,r2=sched4.relocs(a),sched4.relocs(b);assert r1==r2 and sum(r2.values())==82103
    symbols=subprocess.check_output(['mips-linux-gnu-objdump','-t',str(b)],text=True)
    for entry in f:assert entry['name'] in symbols and entry['name']+'.NON_MATCHING' not in symbols
    claims=accepted_claims()+[x['name'] for x in f]
    orig=subprocess.check_output(['readelf','-Ws',str(original/'build/usa/mnsg.elf')],text=True)
    new=subprocess.check_output(['readelf','-Ws',str(b)],text=True)
    inv=summarize_inventory(orig,new,claims)
    assert inv['newly_matching_c']==1965 and inv['remaining_assembly_entries']==5398 and inv['extra_positive_alias_entries']==0
    result={'status':'PASSED_G2_LOCAL','region':'usa','accepted_before':1963,'accepted_after':1965,'new_C_functions':2,'new_original_instruction_bytes':112,'total_original_C_instruction_bytes':84648,'remaining_asm':5398,'rom_bytes':len(rom),'rom_sha1':SHA1,'elf_function_identities':7376,'semantic_relocations':82103,'functions':f,'inventory':inv}
    (checkout/'build/usa/scheduler6-proof.json').write_text(json.dumps(result,indent=2)+'\n')
    return {k:v for k,v in result.items() if k not in ('inventory','functions')}

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['stage','build','verify']);p.add_argument('--checkout',type=Path,required=True);p.add_argument('--prior',type=Path);p.add_argument('--original',type=Path);p.add_argument('--deps',type=Path);p.add_argument('--runtime',type=Path)
    a=p.parse_args();r=stage(a.checkout,a.prior) if a.action=='stage' else build(a.checkout,a.deps,a.runtime) if a.action=='build' else verify(a.checkout,a.prior,a.original)
    print(json.dumps(r,indent=2))
if __name__=='__main__':main()
