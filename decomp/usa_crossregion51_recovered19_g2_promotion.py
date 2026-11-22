"""Native USA nineteen original-address C functions after independently verified USA2046.

Nineteen floating-point ratio/range setters. Fail-closed original G2.
"""
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,re
from pathlib import Path
from . import overlay_isolated233 as splice
from . import scheduler4_g2_promotion as sched4
from . import usa_crossregion51_extra5_g2_promotion as prev
from . import verify as native_verify
from .inventory import summarize_inventory
from .japan_noop_port import env_for
ROOT=Path(__file__).resolve().parent
DIR=ROOT/'research/usa_crossregion51_recovered19_20261122'
FMT='goemon-USA-crossregion51-recovered19-after-2046-v1'
SHA='6ea0ed71032ce08fc2745f412d84936382197494'
def digest(b):return hashlib.sha256(b).hexdigest()
def fixture():
 d=json.loads((DIR/'manifest.json').read_text());fs=d['functions']
 if (d['format'],d['region'],d['original_rom_sha1'],d['accepted_before'],d['accepted_bytes_before'])!=(FMT,'usa',SHA,2046,90168):raise ValueError('Bad recovered19 manifest')
 if len(fs)!=19 or sum(f['size'] for f in fs)!=1596 or sum(len(f['original_symbolic_relocations']) for f in fs)!=0 or len({f['name'] for f in fs})!=19 or len({f['rom_offset'] for f in fs})!=19:raise ValueError('Wrong 19 count')
 for f in fs:
  src=DIR/'sources'/(f['source']+'.c')
  if not src.exists() or digest(src.read_bytes())!=f['source_sha256'] or int(f['name'].split('_')[-1],16)!=f['rom_offset']:raise ValueError('Source changed '+f['name'])
 return d

def eligibility(checkout):
 d=fixture();checkout=Path(checkout);rom=sched4.original_rom(checkout)
 if (checkout/'build/usa/mnsg.z64').read_bytes()!=rom:raise ValueError('Prior ROM not exact')
 proof=json.loads((checkout/'build/usa/extra5-proof.json').read_text())
 if (proof['status'],proof['accepted_after'],proof['original_elf_positive_functions'],proof['original_semantic_relocations'])!=('PASSED_G2_LOCAL',2046,7376,82103):raise ValueError('No verified 2046 predecessor')
 accepted={f['name'] for f in native_verify.claimed_functions(native_verify.load_manifest(ROOT/'manifest.json'))}
 from . import scheduler4_g2_promotion as s4,scheduler5_g2_promotion as s5,scheduler6_g2_promotion as s6,mini_ebisumaru_1_g2_promotion as mini,usa_crossregion48_g2_promotion as cross48,usa_crossregion51_recovered27_g2_promotion as prev27
 for mod,method in [(s4,'load_fixture'),(s5,'fixture'),(s6,'fixture'),(mini,'fixture'),(cross48,'fixture'),(prev,'fixture'),(prev27,'fixture')]:
  accepted.update(f['name'] for f in getattr(mod,method)()['functions'])
 accepted.update(['func_8001F8B0_204B0','func_8001F940_20540'])
 for f in d['functions']:
  if f['name'] in accepted or digest(rom[f['rom_offset']:f['rom_offset']+f['size']])!=f['original_code_sha256']:raise ValueError('Already accepted or ROM mismatch '+f['name'])
 return d,rom

def stage(checkout,prior):
 checkout=Path(checkout);prior=Path(prior);d,rom=eligibility(checkout)
 if prior.exists():raise ValueError('Fresh predecessor backup required')
 (prior/'build/usa').mkdir(parents=True)
 for n in ('mnsg.elf','mnsg.z64'):shutil.copy2(checkout/'build/usa'/n,prior/'build/usa'/n)
 owners=splice.find_owners(checkout,d)
 plan=splice.stage_linker(checkout,rom,d,owners,DIR/'sources')
 (checkout/'build/usa/recovered19-stage.json').write_text(json.dumps(plan,indent=2)+'\n')
 return {'status':'STAGED','functions':len(plan['functions']),'C_bytes':1596,'owners':len(plan['parents']),'remaining_ASM_fragments':len(plan['assembly'])}

def build(checkout,deps,runtime):
 checkout=Path(checkout);d=fixture();rom=sched4.original_rom(checkout);env=env_for(Path(deps),Path(runtime));plan=json.loads((checkout/'build/usa/recovered19-stage.json').read_text())
 if plan['functions']!=d['functions']:raise ValueError('Plan differs from validated manifest')
 def run(cmd):subprocess.run(cmd,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
 run(['make','-j4','VERSION=usa',*splice.object_targets(plan)])
 packed=splice.pack_objects(checkout,rom,plan)
 if len(packed['C_objects'])!=19:raise ValueError('Missing C objects')
 (checkout/'build/usa/recovered19-objects.json').write_text(json.dumps(packed,indent=2)+'\n')
 for n in ('mnsg.elf','mnsg.z64'):(checkout/'build/usa'/n).unlink(missing_ok=True)
 run(['make','-j4','VERSION=usa','build/usa/mnsg.z64'])
 got=(checkout/'build/usa/mnsg.z64').read_bytes()
 if got!=rom:raise ValueError('FAILED_ROM: '+str(next((i for i,(a,b) in enumerate(zip(got,rom)) if a!=b),None)))
 return {'status':'ROM_EXACT','ROM_bytes':len(got),'SHA1':SHA}

def verify(checkout,prior,original):
 checkout=Path(checkout);prior=Path(prior);original=Path(original);d=fixture();rom=sched4.original_rom(checkout)
 plan=json.loads((checkout/'build/usa/recovered19-stage.json').read_text())
 proof=splice.verify_link(original,prior/'build/usa/mnsg.elf',checkout,rom,plan)
 from . import scheduler4_g2_promotion as s4,scheduler5_g2_promotion as s5,scheduler6_g2_promotion as s6,mini_ebisumaru_1_g2_promotion as mini,usa_crossregion48_g2_promotion as cross48,usa_crossregion51_recovered27_g2_promotion as prev27
 claim=[f['name'] for f in native_verify.claimed_functions(native_verify.load_manifest(ROOT/'manifest.json'))]
 claim+=['func_8001F8B0_204B0','func_8001F940_20540']
 for mod,method in [(s4,'load_fixture'),(s5,'fixture'),(s6,'fixture'),(mini,'fixture'),(cross48,'fixture'),(prev,'fixture'),(prev27,'fixture')]:claim += [f['name'] for f in getattr(mod,method)()['functions']]
 claim += [f['name'] for f in d['functions']]
 old=subprocess.check_output(['readelf','-Ws',str(original/'build/usa/mnsg.elf')],text=True)
 new=subprocess.check_output(['readelf','-Ws',str(checkout/'build/usa/mnsg.elf')],text=True)
 inv=summarize_inventory(old,new,claim)
 if inv['newly_matching_c']!=2065 or inv['remaining_assembly_entries']!=5298 or inv['extra_positive_alias_entries']:
  raise ValueError('Strict inventory diverged '+repr(inv))
 result={'status':'PASSED_G2_LOCAL','region':'usa','accepted_before':2046,'accepted_after':2065,'new_original_C_bytes':1596,'total_original_C_bytes':91764,'remaining_asm':5298,'original_ROM_sha1':SHA,'original_ROM_bytes':33554432,'original_elf_positive_functions':7376,'original_semantic_relocations':82103,'source_relocations_in_batch':0,'new_functions':d['functions'],'link_proof':proof,'inventory':inv}
 (checkout/'build/usa/recovered19-proof.json').write_text(json.dumps(result,indent=2)+'\n')
 return {k:v for k,v in result.items() if k not in ('new_functions','link_proof','inventory')}

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('stage','build','verify'));p.add_argument('--checkout',type=Path,required=True);p.add_argument('--prior',type=Path);p.add_argument('--original',type=Path);p.add_argument('--deps',type=Path);p.add_argument('--runtime',type=Path);a=p.parse_args()
 result=stage(a.checkout,a.prior) if a.action=='stage' else build(a.checkout,a.deps,a.runtime) if a.action=='build' else verify(a.checkout,a.prior,a.original)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
