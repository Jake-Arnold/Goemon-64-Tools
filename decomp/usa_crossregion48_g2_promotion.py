"""Fail-closed 48 unique USA cross-region original native C stage after USA1966 Mini Ebisumaru.

Every new function/relocation must match the original; changes to arbitrary game
assets/instructions or to the prior ELF symbol identity are forbidden. This is
NOT automatic promotion: completion requires full ROM, ELF, all relocations,
strict inventory and full local CI, and subsequent audited publication.
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess
from pathlib import Path
from . import overlay_isolated233 as splice
from . import scheduler4_g2_promotion as sched4
from . import mini_ebisumaru_1_g2_promotion as mini
from . import verify as native_verify
from .inventory import summarize_inventory
from .japan_noop_port import env_for

ROOT=Path(__file__).resolve().parent
DIR=ROOT/'research/usa_crossregion48_g2_20261122'
FMT='goemon-USA-crossregion48-after-1966-v1'
SHA='6ea0ed71032ce08fc2745f412d84936382197494'

def digest(raw):return hashlib.sha256(raw).hexdigest()

def fixture():
 d=json.loads((DIR/'manifest.json').read_text())
 if (d['format'],d['region'],d['original_rom_sha1'],d['accepted_before'],d['accepted_bytes_before'])!=(FMT,'usa',SHA,1966,84872):
  raise ValueError('Wrong USA cross48 fixture')
 fs=d['functions']
 if len(fs)!=48 or sum(f['size'] for f in fs)!=3028 or len({f['name'] for f in fs})!=48 or len({f['rom_offset'] for f in fs})!=48:
  raise ValueError('Cross48 duplicate names/ROM extents or count/bytes changed')
 if sum(len(f['original_symbolic_relocations']) for f in fs)!=130:raise ValueError('Cross48 isolated relocation count changed')
 for f in fs:
  p=DIR/'sources'/(f['source']+'.c')
  if not p.is_file() or digest(p.read_bytes())!=f['source_sha256'] or int(f['name'].split('_')[-1],16)!=f['rom_offset']:
   raise ValueError('Cross48 C source identity/hash mismatch: '+f['name'])
 return d

def eligibility(checkout):
 checkout=Path(checkout);d=fixture();rom=sched4.original_rom(checkout)
 if (checkout/'build/usa/mnsg.z64').read_bytes()!=rom:raise ValueError('USA1966 original ROM not byte-identical')
 proof=json.loads((checkout/'build/usa/mini-ebisu1-proof.json').read_text())
 if (proof['status'],proof['accepted_after'],proof['original_elf_functions'],proof['semantic_relocations'])!=('PASSED_G2_LOCAL',1966,7376,82103):
  raise ValueError('Missing actual USA1966 Mini1 combined native G2 proof')
 previous={f['name'] for f in native_verify.claimed_functions(native_verify.load_manifest(ROOT/'manifest.json'))}
 previous.update(f['name'] for f in mini.fixture()['functions'])
 previous.update(('func_8001F8B0_204B0','func_8001F940_20540'))
 from . import scheduler5_g2_promotion as s5,scheduler6_g2_promotion as s6
 from . import scheduler4_g2_promotion as s4
 previous.update(f['name'] for f in s4.load_fixture()['functions'])
 previous.update(f['name'] for f in s5.fixture()['functions'])
 previous.update(f['name'] for f in s6.fixture()['functions'])
 for f in d['functions']:
  if f['name'] in previous or digest(rom[f['rom_offset']:f['rom_offset']+f['size']])!=f['original_code_sha256']:
   raise ValueError('Cross48 function already accepted or original ROM changed: '+f['name'])
 return d,rom

def stage(checkout,prior):
 checkout=Path(checkout);prior=Path(prior);d,rom=eligibility(checkout)
 if prior.exists():raise ValueError('Not a fresh cross48 predecessor ELF backup')
 (prior/'build/usa').mkdir(parents=True)
 for n in ('mnsg.elf','mnsg.z64'):shutil.copy2(checkout/'build/usa'/n,prior/'build/usa'/n)
 owners=splice.find_owners(checkout,d)
 plan=splice.stage_linker(checkout,rom,d,owners,DIR/'sources')
 (checkout/'build/usa/cross48-stage.json').write_text(json.dumps(plan,indent=2)+'\n')
 return {'status':'STAGED_NOT_G2','functions':len(plan['functions']),'original_code_bytes':sum(f['size'] for f in plan['functions']),'replaced_ASM_owners':len(plan['parents']),'retained_ASM_fragments':len(plan['assembly'])}

def build(checkout,deps,runtime):
 checkout=Path(checkout);env=env_for(Path(deps),Path(runtime));d=fixture();rom=sched4.original_rom(checkout)
 plan=json.loads((checkout/'build/usa/cross48-stage.json').read_text())
 if plan['functions']!=d['functions']:raise ValueError('Cross48 plan changed')
 def run(args):subprocess.run(args,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
 run(['make','-j4','VERSION=usa',*splice.object_targets(plan)])
 packed=splice.pack_objects(checkout,rom,plan)
 if len(packed['C_objects'])!=48:raise ValueError('Cross48 C object count differs')
 packed.update(functions=48,embedded=0,instruction_bytes=3028)
 (checkout/'build/usa/cross48-objects.json').write_text(json.dumps(packed,indent=2)+'\n')
 for n in ('mnsg.elf','mnsg.z64'):(checkout/'build/usa'/n).unlink(missing_ok=True)
 run(['make','-j4','VERSION=usa','build/usa/mnsg.z64'])
 got=(checkout/'build/usa/mnsg.z64').read_bytes()
 if len(got)!=33554432 or got!=rom:
  off=next((i for i,(a,b) in enumerate(zip(got,rom)) if a!=b),None)
  raise ValueError(f'FAILED_ROM: cross48 32 MiB failed, first differing byte={off}, sha1={hashlib.sha1(got).hexdigest()}')
 return {'status':'ROM_EQUAL_PENDING_ELF_RELOCS','rom_sha1':SHA,'new_original_bytes':3028}

def verify(checkout,prior,original):
 checkout=Path(checkout);prior=Path(prior);original=Path(original);d=fixture();plan=json.loads((checkout/'build/usa/cross48-stage.json').read_text());rom=sched4.original_rom(checkout)
 proof=splice.verify_link(original,prior/'build/usa/mnsg.elf',checkout,rom,plan)
 proof.update(count=48,bytes=3028,C_units=48)
 old=subprocess.check_output(['readelf','-Ws',str(original/'build/usa/mnsg.elf')],text=True)
 new=subprocess.check_output(['readelf','-Ws',str(checkout/'build/usa/mnsg.elf')],text=True)
 claims=[f['name'] for f in native_verify.claimed_functions(native_verify.load_manifest(ROOT/'manifest.json'))]
 claims+=['func_8001F8B0_204B0','func_8001F940_20540']
 from . import scheduler5_g2_promotion as s5,scheduler6_g2_promotion as s6
 from . import scheduler4_g2_promotion as s4
 claims += [f['name'] for f in s4.load_fixture()['functions']]+[f['name'] for f in s5.fixture()['functions']]+[f['name'] for f in s6.fixture()['functions']]
 claims += [f['name'] for f in mini.fixture()['functions']]+[f['name'] for f in d['functions']]
 inv=summarize_inventory(old,new,claims)
 if inv['newly_matching_c']!=2014 or inv['remaining_assembly_entries']!=5349 or inv['extra_positive_alias_entries']:
  raise ValueError('Cross48 full inventory failed '+str(inv))
 result={'status':'PASSED_G2_LOCAL','region':'usa','accepted_before':1966,'accepted_after':2014,'new_original_C_bytes':3028,'total_original_C_bytes':87900,'remaining_asm':5349,'original_ROM_sha1':SHA,'original_ROM_bytes':len(rom),'original_elf_positive_functions':7376,'original_semantic_relocations':82103,'source_relocations_in_batch':130,'new_functions':d['functions'],'link_proof':proof,'inventory':inv}
 (checkout/'build/usa/cross48-proof.json').write_text(json.dumps(result,indent=2)+'\n')
 return {k:v for k,v in result.items() if k not in ('new_functions','link_proof','inventory')}

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('stage','build','verify'));p.add_argument('--checkout',type=Path,required=True);p.add_argument('--prior',type=Path);p.add_argument('--original',type=Path);p.add_argument('--deps',type=Path);p.add_argument('--runtime',type=Path);a=p.parse_args()
 result=stage(a.checkout,a.prior) if a.action=='stage' else build(a.checkout,a.deps,a.runtime) if a.action=='build' else verify(a.checkout,a.prior,a.original)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
