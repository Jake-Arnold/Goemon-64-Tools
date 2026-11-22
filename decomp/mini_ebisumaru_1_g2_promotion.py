"""Native original-USA Mini Ebisumaru movement callback staged after independently verified USA1965.

Requires previous exact ROM, all ELF/relocation identities, full inventory.
Does not alter original ASM instructions or permit unverified accepted counts.
"""
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,re
from pathlib import Path
from . import overlay_isolated233 as splice
from . import scheduler4_g2_promotion as sched4
from . import scheduler6_g2_promotion as sched6
from . import verify as native_verify
from .inventory import summarize_inventory
from .japan_noop_port import env_for

ROOT=Path(__file__).resolve().parent
DIR=ROOT/'research/mini_ebisumaru_1_g2_20261122'
SHA='6ea0ed71032ce08fc2745f412d84936382197494'
FMT='goemon-USA-mini-ebisumaru-1-after-1965-v1'
EXPECTED=(('func_801E20A0_59DFB0',0x59DFB0,0x801E20A0,224),)

def digest(b):return hashlib.sha256(b).hexdigest()

def fixture():
 d=json.loads((DIR/'manifest.json').read_text())
 if (d['format'],d['rom_sha1'],d['accepted_before'],d['accepted_instruction_bytes_before'])!=(FMT,SHA,1965,84648):raise ValueError('Unreviewed USA mini1 manifest')
 fs=d['functions']
 if sorted((x['name'],x['rom_offset'],x['vma'],x['size']) for x in fs)!=list(EXPECTED):raise ValueError('Mini1 original function identities differ')
 for f in fs:
  p=DIR/'sources'/(f['source']+'.c')
  if not p.exists() or digest(p.read_bytes())!=f['source_sha256']:raise ValueError('Mini1 source hash mismatch')
 return d

def eligibility(checkout):
 p=Path(checkout);d=fixture();rom=sched4.original_rom(p)
 if (p/'build/usa/mnsg.z64').read_bytes()!=rom:raise ValueError('Predecessor USA ROM is not exact')
 proof=json.loads((p/'build/usa/scheduler6-proof.json').read_text())
 if proof['status']!='PASSED_G2_LOCAL' or (proof['accepted_after'],proof['semantic_relocations'])!=(1965,82103):raise ValueError('Missing verified USA1965 predecessor')
 accepted={f['name'] for f in native_verify.claimed_functions(native_verify.load_manifest(ROOT/'manifest.json'))}
 accepted.update(('func_8001F8B0_204B0','func_8001F940_20540'))
 accepted.update(f['name'] for f in sched4.load_fixture()['functions'])
 from . import scheduler5_g2_promotion as s5
 accepted.update(f['name'] for f in s5.fixture()['functions']);accepted.update(f['name'] for f in sched6.fixture()['functions'])
 for f in d['functions']:
  if f['name'] in accepted or digest(rom[f['rom_offset']:f['rom_offset']+f['size']])!=f['original_code_sha256']:
   raise ValueError('Mini1 duplicate accepted C / original ROM changed '+f['name'])
 return d,rom

def stage(checkout,prior):
 checkout=Path(checkout);prior=Path(prior);d,rom=eligibility(checkout)
 if prior.exists():raise ValueError('Nonempty previous stage backup')
 (prior/'build/usa').mkdir(parents=True)
 for n in ('mnsg.elf','mnsg.z64'):shutil.copy2(checkout/'build/usa'/n,prior/'build/usa'/n)
 owners=splice.find_owners(checkout,d)
 # No manual ASM/data rewrite; splice only verified original nonmatching blocks.
 plan=splice.stage_linker(checkout,rom,d,owners,DIR/'sources')
 (checkout/'build/usa/mini-ebisu1-stage.json').write_text(json.dumps(plan,indent=2)+'\n')
 return {'status':'STAGED_NOT_G2','objects':len(plan['functions']),'assembly_fragments':len(plan['assembly']),'parents':len(plan['parents'])}

def build(checkout,deps,runtime):
 checkout=Path(checkout);env=env_for(Path(deps),Path(runtime));d,rom=fixture(),sched4.original_rom(checkout)
 plan=json.loads((checkout/'build/usa/mini-ebisu1-stage.json').read_text())
 if plan['functions']!=d['functions']:raise ValueError('Stale Mini1 stage')
 def run(command):subprocess.run(command,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
 # Compile exact selected IDO source and all original ASM leftovers.
 targets=splice.object_targets(plan)
 run(['make','-j4','VERSION=usa',*targets])
 packed=splice.pack_objects(checkout,rom,plan)
 # The reusable 233-stage helper labels its output with its historical count.
 # Normalize it only after verifying the actual new function identities.
 if len(plan['functions'])!=1 or len(packed['C_objects'])!=1:raise ValueError('Mini1 packing count mismatch')
 packed['functions']=1;packed['embedded']=0;packed['instruction_bytes']=224
 for n in ('mnsg.elf','mnsg.z64'):(checkout/'build/usa'/n).unlink(missing_ok=True)
 run(['make','-j4','VERSION=usa','build/usa/mnsg.z64'])
 built=(checkout/'build/usa/mnsg.z64').read_bytes()
 if built!=rom:
  off=next((i for i,(x,y) in enumerate(zip(built,rom)) if x!=y),None)
  raise ValueError('FAILED_ROM: Mini1 first differing byte '+str(off)+' SHA1 '+hashlib.sha1(built).hexdigest())
 (checkout/'build/usa/mini-ebisu1-objects.json').write_text(json.dumps(packed,indent=2)+'\n')
 return {'status':'ROM_EQUAL_PENDING_ELF_AUDIT','rom_sha1':SHA,'new_bytes':sum(f['size'] for f in d['functions'])}

def verify(checkout,prior,original):
 checkout=Path(checkout);prior=Path(prior);original=Path(original);d=fixture();plan=json.loads((checkout/'build/usa/mini-ebisu1-stage.json').read_text());rom=sched4.original_rom(checkout)
 proof=splice.verify_link(original,prior/'build/usa/mnsg.elf',checkout,rom,plan)
 if len(plan['functions'])!=1 or sum(f['size'] for f in plan['functions'])!=224:raise ValueError('Mini1 verified identity changed')
 proof['count']=1;proof['bytes']=224;proof['C_units']=1
 old=subprocess.check_output(['readelf','-Ws',str(original/'build/usa/mnsg.elf')],text=True)
 new=subprocess.check_output(['readelf','-Ws',str(checkout/'build/usa/mnsg.elf')],text=True)
 claims=[x['name'] for x in native_verify.claimed_functions(native_verify.load_manifest(ROOT/'manifest.json'))]
 claims+=['func_8001F8B0_204B0','func_8001F940_20540'];claims+=[x['name'] for x in sched4.load_fixture()['functions']]
 from . import scheduler5_g2_promotion as s5
 claims+=[x['name'] for x in s5.fixture()['functions']]+[x['name'] for x in sched6.fixture()['functions']]+[x['name'] for x in d['functions']]
 inv=summarize_inventory(old,new,claims)
 if inv['newly_matching_c']!=1966 or inv['remaining_assembly_entries']!=5397 or inv['extra_positive_alias_entries']:
  raise ValueError('Mini1 original strict inventory mismatch '+str(inv))
 result={'status':'PASSED_G2_LOCAL','region':'usa','accepted_before':1965,'accepted_after':1966,'added_original_bytes':224,'total_C_original_instruction_bytes':84872,'remaining_asm':5397,'rom_sha1':SHA,'rom_bytes':len(rom),'original_elf_functions':7376,'semantic_relocations':82103,'new_functions':d['functions'],'link_proof':proof,'inventory':inv}
 (checkout/'build/usa/mini-ebisu1-proof.json').write_text(json.dumps(result,indent=2)+'\n')
 return {k:v for k,v in result.items() if k not in ('inventory','new_functions','link_proof')}

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('stage','build','verify'));p.add_argument('--checkout',type=Path,required=True);p.add_argument('--prior',type=Path);p.add_argument('--original',type=Path);p.add_argument('--deps',type=Path);p.add_argument('--runtime',type=Path);args=p.parse_args()
 result=stage(args.checkout,args.prior) if args.action=='stage' else build(args.checkout,args.deps,args.runtime) if args.action=='build' else verify(args.checkout,args.prior,args.original)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
