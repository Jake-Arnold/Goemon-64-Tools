"""Fail-closed native USA27 recovery stage after 2014; original ASM retained on failure.

All source C is reconstructed from matching Japanese donors and independently
verified against the original USA ROM and original object relocations.
"""
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path
from . import overlay_isolated233 as splice
from . import scheduler4_g2_promotion as sched4
from . import usa_crossregion48_g2_promotion as prev
from . import verify as native_verify
from .inventory import summarize_inventory
from .japan_noop_port import env_for
import re
# Original Splat pragma-owned dialogue_window.c functions, distinct from standalone ASM.
# This extension is target-scoped and never rewrites original assembly or ROM bytes.
EMBEDDED_27={
    'func_8000C454_D054','func_8000C488_D088',
    'func_8000C4C8_D0C8','func_8000C4FC_D0FC',
    'func_8000C570_D170','func_8000C5A4_D1A4',
    'func_8000C60C_D20C','func_8000C640_D240',
    'func_8000C8D0_D4D0','func_8000D3B8_DFB8',
}

def embed_recovered_dialogue(checkout,fixture,root):
    items=[f for f in fixture['functions'] if f['name'] in EMBEDDED_27]
    path=Path(checkout)/'src/dialogue_window.c'
    code=path.read_text()
    field_header=(root/'jp_actor_fields.h').read_text()
    # The canonical source already declares D_80167C48 as DialogueWindow**.
    # Use its original declaration and a typed cast when accessing observed offsets.
    field_header=re.sub(r'^extern JPActorObserved \*D_80167C48_168848\[\];\n','',field_header,flags=re.M)
    assert 'extern JPActorObserved' not in field_header
    field_header=re.sub(r'^typedef unsigned (?:char|short|int|long long) u(?:8|16|32|64);\n','',field_header,flags=re.M)
    code=code.replace('#include "common.h"','#include "common.h"\n'+field_header,1)
    for f in items:
        pattern=r'(?m)^#pragma GLOBAL_ASM\("asm/usa/nonmatchings/[^"\n]*/'+re.escape(f['name'])+r'\.s"\)$'
        if len(re.findall(pattern,code))!=1:raise ValueError('Original embedded pragma missing '+f['name'])
        src=(root/(f['source']+'.c')).read_text()
        src=src.replace('#include "jp_actor_fields.h"\n','').replace('#include "jp_actor_observed.h"\n','')
        src=src.replace('JPActorObserved *p = D_80167C48_168848[idx];','JPActorObserved *p = (JPActorObserved *)D_80167C48_168848[idx];')
        code=re.sub(pattern,lambda _:'/* USA original-ID0 reconstruction for '+f['name']+' */\n'+src,code,count=1)
    path.write_text(code)

ROOT=Path(__file__).resolve().parent
DIR=ROOT/'research/usa_crossregion51_recovered27_20261122'
FMT='goemon-USA-crossregion51-recovered27-after-2014-v1'
SHA='6ea0ed71032ce08fc2745f412d84936382197494'
def digest(b):return hashlib.sha256(b).hexdigest()
def fixture():
 d=json.loads((DIR/'manifest.json').read_text())
 if (d['format'],d['region'],d['original_rom_sha1'],d['accepted_before'],d['accepted_bytes_before'])!=(FMT,'usa',SHA,2014,87900):raise ValueError('Unreviewed recovered27 manifest')
 fs=d['functions']
 if len(fs)!=27 or sum(f['size'] for f in fs)!=1904 or sum(len(f['original_symbolic_relocations']) for f in fs)!=77 or len({f['name'] for f in fs})!=27 or len({f['rom_offset'] for f in fs})!=27:raise ValueError('Bad recovered27 count / bytes / reloc')
 for f in fs:
  src=DIR/'sources'/(f['source']+'.c')
  if not src.is_file() or digest(src.read_bytes())!=f['source_sha256'] or int(f['name'].split('_')[-1],16)!=f['rom_offset']:raise ValueError('Invalid C provenance '+f['name'])
 return d

def eligibility(checkout):
 d=fixture();checkout=Path(checkout);rom=sched4.original_rom(checkout)
 if (checkout/'build/usa/mnsg.z64').read_bytes()!=rom:raise ValueError('USA2014 original image changed')
 proof=json.loads((checkout/'build/usa/cross48-proof.json').read_text())
 if (proof['status'],proof['accepted_after'],proof['original_elf_positive_functions'],proof['original_semantic_relocations'])!=('PASSED_G2_LOCAL',2014,7376,82103):raise ValueError('Prior 2014 proof missing')
 accepted={f['name'] for f in native_verify.claimed_functions(native_verify.load_manifest(ROOT/'manifest.json'))}
 from . import scheduler4_g2_promotion as s4, scheduler5_g2_promotion as s5, scheduler6_g2_promotion as s6,mini_ebisumaru_1_g2_promotion as mini
 accepted.update(f['name'] for f in s4.load_fixture()['functions']);accepted.update(f['name'] for f in s5.fixture()['functions']);accepted.update(f['name'] for f in s6.fixture()['functions'])
 accepted.update(f['name'] for f in mini.fixture()['functions']);accepted.update(f['name'] for f in prev.fixture()['functions'])
 accepted.update(('func_8001F8B0_204B0','func_8001F940_20540'))
 for f in d['functions']:
  if f['name'] in accepted or digest(rom[f['rom_offset']:f['rom_offset']+f['size']])!=f['original_code_sha256']:raise ValueError('Already accepted or ROM mismatch '+f['name'])
 return d,rom,accepted

def stage(checkout,prior):
 checkout=Path(checkout);prior=Path(prior);d,rom,accepted=eligibility(checkout)
 if prior.exists():raise ValueError('Use fresh predecessor backup')
 (prior/'build/usa').mkdir(parents=True)
 for n in ('mnsg.elf','mnsg.z64'):shutil.copy2(checkout/'build/usa'/n,prior/'build/usa'/n)
 for h in ('jp_actor_fields.h','jp_actor_observed.h','m2c_macros.h'):
  target=checkout/'src'/h
  if target.exists():raise ValueError('Existing source header collision '+h)
  shutil.copy2(DIR/'sources'/h,target)
 owners=splice.find_owners(checkout,d)
 plan=splice.stage_linker(checkout,rom,d,owners,DIR/'sources')
 (checkout/'build/usa/recovered27-stage.json').write_text(json.dumps(plan,indent=2)+'\n')
 return {'status':'STAGED_NOT_G2','functions':len(plan['functions']),'bytes':sum(f['size'] for f in plan['functions']),'owners':len(plan['parents']),'ASM_fragments':len(plan['assembly'])}

def build(checkout,deps,runtime):
 checkout=Path(checkout);env=env_for(Path(deps),Path(runtime));d=fixture();rom=sched4.original_rom(checkout)
 plan=json.loads((checkout/'build/usa/recovered27-stage.json').read_text())
 if plan['functions']!=d['functions']:raise ValueError('Plan changed')
 def run(cmd):subprocess.run(cmd,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
 run(['make','-j4','VERSION=usa',*splice.object_targets(plan)])
 packed=splice.pack_objects(checkout,rom,plan)
 if len(packed['C_objects'])!=17:raise ValueError('Wrong standalone C object count')
 packed.update(functions=27,embedded=10,instruction_bytes=1904)
 (checkout/'build/usa/recovered27-objects.json').write_text(json.dumps(packed,indent=2)+'\n')
 for n in ('mnsg.elf','mnsg.z64'):(checkout/'build/usa'/n).unlink(missing_ok=True)
 run(['make','-j4','VERSION=usa','build/usa/mnsg.z64'])
 got=(checkout/'build/usa/mnsg.z64').read_bytes()
 if len(got)!=33554432 or got!=rom:
  off=next((i for i,(a,b) in enumerate(zip(got,rom)) if a!=b),None)
  raise ValueError(f'FAILED_ROM: {off=} {hashlib.sha1(got).hexdigest()}')
 return {'status':'ROM_EQUAL_PENDING_ELF_RELOC','sha1':SHA,'new_bytes':1904}

def verify(checkout,prior,original):
 checkout=Path(checkout);prior=Path(prior);original=Path(original);d=fixture();plan=json.loads((checkout/'build/usa/recovered27-stage.json').read_text());rom=sched4.original_rom(checkout)
 # One pre-existing canonical ELF symbol-size annotation (D3B8) was
 # 72 bytes instead of the 64-byte original. This source corrects it.
 # All 7376 identities are compared with that *single* original-ROM
 # correction; no other identity or relocation differences are accepted.
 from .overlay_crossregion47 import _funcs as symbols, _relocations as relocations
 from collections import Counter
 before=symbols(prior/'build/usa/mnsg.elf')
 after=symbols(checkout/'build/usa/mnsg.elf')
 ori=symbols(original/'build/usa/mnsg.elf')
 key_old=('func_8000D3B8_DFB8',0x8000D3B8,72)
 key_original=('func_8000D3B8_DFB8',0x8000D3B8,64)
 assert sum(ori.values())==sum(before.values())==sum(after.values())==7376
 assert ori[key_original]==after[key_original]==1 and before[key_old]==1
 expected=Counter(before)
 expected[key_old]-=1
 if not expected[key_old]:del expected[key_old]
 expected[key_original]+=1
 if expected!=after:raise ValueError('ELF identity drift besides original-size correction')
 oldrel=relocations(prior/'build/usa/mnsg.elf')
 newrel=relocations(checkout/'build/usa/mnsg.elf')
 if set(oldrel)!=set(newrel) or any(Counter(oldrel[k])!=Counter(newrel[k]) for k in oldrel):
     raise ValueError('Semantic relocations changed')
 linkmap=(checkout/'build/usa/mnsg.map').read_text()
 for f in d['functions']:
     expected_owner=('build/usa/src/'+f['source']+'.c.o' if f['name'] not in EMBEDDED_27
                     else 'build/usa/src/dialogue_window.c.o')
     if ((f['name'],f['vma'],f['size']) not in after or expected_owner not in linkmap or
         f['name']+'.NON_MATCHING' in linkmap or
         (checkout/'build/usa/mnsg.z64').read_bytes()[f['rom_offset']:f['rom_offset']+f['size']]!=rom[f['rom_offset']:f['rom_offset']+f['size']]):
         raise ValueError('New C source not established at original address '+f['name'])
 proof={'status':'PASS','count':27,'bytes':1904,'rom_bytes':len(rom),'sha1':SHA,
        'positive_elf_function_entries':7376,'semantic_relocation_counts':{k:len(v) for k,v in newrel.items()},
        'embedded':len(EMBEDDED_27),'original_size_annotation_correction':{'name':key_original[0],'old_size':72,'original_size':64}}
 from . import scheduler4_g2_promotion as s4,scheduler5_g2_promotion as s5,scheduler6_g2_promotion as s6,mini_ebisumaru_1_g2_promotion as mini
 claims=[f['name'] for f in native_verify.claimed_functions(native_verify.load_manifest(ROOT/'manifest.json'))]
 claims+=['func_8001F8B0_204B0','func_8001F940_20540']
 claims += [f['name'] for f in s4.load_fixture()['functions']]+[f['name'] for f in s5.fixture()['functions']]+[f['name'] for f in s6.fixture()['functions']]
 claims += [f['name'] for f in mini.fixture()['functions']]+[f['name'] for f in prev.fixture()['functions']]+[f['name'] for f in d['functions']]
 old=subprocess.check_output(['readelf','-Ws',str(original/'build/usa/mnsg.elf')],text=True)
 new=subprocess.check_output(['readelf','-Ws',str(checkout/'build/usa/mnsg.elf')],text=True)
 inv=summarize_inventory(old,new,claims)
 if inv['newly_matching_c']!=2041 or inv['remaining_assembly_entries']!=5322 or inv['extra_positive_alias_entries']:
  raise ValueError('Strict inventory fail: '+repr(inv))
 result={'status':'PASSED_G2_LOCAL','region':'usa','accepted_before':2014,'accepted_after':2041,'new_original_C_bytes':1904,'total_original_C_bytes':89804,'remaining_asm':5322,'original_ROM_sha1':SHA,'original_ROM_bytes':33554432,'original_elf_positive_functions':7376,'original_semantic_relocations':82103,'source_relocations_in_batch':77,'new_functions':d['functions'],'link_proof':proof,'inventory':inv}
 (checkout/'build/usa/recovered27-proof.json').write_text(json.dumps(result,indent=2)+'\n')
 return {k:v for k,v in result.items() if k not in ('new_functions','link_proof','inventory')}

# Scope predecessor adapter state to one stage/build/verify invocation.
# Do not alter unrelated tests or native233's production registry on import.
from contextlib import contextmanager
@contextmanager
def scoped_embedded():
 old_map=splice.EMBEDDED.copy()
 old_embed=splice.embed_original
 try:
  splice.EMBEDDED.update({n:'dialogue_window.c' for n in EMBEDDED_27})
  splice.embed_original=embed_recovered_dialogue
  yield
 finally:
  splice.EMBEDDED.clear();splice.EMBEDDED.update(old_map)
  splice.embed_original=old_embed

_original_stage=stage
_original_build=build
_original_verify=verify
def stage(*args):
 with scoped_embedded():return _original_stage(*args)
def build(*args):
 with scoped_embedded():return _original_build(*args)
def verify(*args):
 with scoped_embedded():return _original_verify(*args)

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('stage','build','verify'));p.add_argument('--checkout',type=Path,required=True);p.add_argument('--prior',type=Path);p.add_argument('--original',type=Path);p.add_argument('--deps',type=Path);p.add_argument('--runtime',type=Path);a=p.parse_args()
 result=stage(a.checkout,a.prior) if a.action=='stage' else build(a.checkout,a.deps,a.runtime) if a.action=='build' else verify(a.checkout,a.prior,a.original)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
