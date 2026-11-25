import argparse, pathlib, subprocess, json, hashlib, sys, re
from decomp.consolidated_batch_promotion import stage, cross, opening, glitch, inventory
from decomp import native251_promotion as native, usa_short72_promotion as short72
P=pathlib.Path
from decomp.research.wave194_20261125.abs_metadata import restore

from collections import Counter
from inline_metadata import restore_inline, EXPECTED
sha=lambda b:hashlib.sha256(b).hexdigest()
def finish(r,co,base,w,uv,jobs,d,doc):
 bd=co/f'build/{r}';elf=bd/'mnsg.elf';prior=w/'prior.elf';rom=stage.original(co,r);ldpath=co/f'.splat/{r}/mnsg.ld';ld=ldpath.read_text();aliases=[];ldpath.write_text(ld);d['preserved_original_labels']=aliases;d['errors']=[];save=lambda:(w/'summary.json').write_text(json.dumps(d,indent=2)+'\n')
 f0=cross._funcs(prior);g0=opening.stable_globals(prior);r0=glitch.all_semantic_relocations(prior);oldtxt=subprocess.check_output(['readelf','-Ws',str(prior)],text=True);oldfuncs,oldmarkers=inventory.parse_inventory_symbols(oldtxt)
 def link(label):
  elf.unlink(missing_ok=True);(bd/'mnsg.z64').unlink(missing_ok=True);stage.runmake(co,r,ld,[f'build/{r}/mnsg.z64'],w/(label+'.log'),uv,jobs)
  if r=='usa':return [short72.restore_original_abs_label_type(elf,prior),native.restore_inline_usa(elf,prior),*restore_inline(elf,base/'build/usa/mnsg.elf',prior)]
  return []
 d['stage']='combined_link';save();d['known_metadata_restorations']=link('link-retry');save()
 rfirst=glitch.all_semantic_relocations(elf)
 rel_ok=rfirst==r0
 if (bd/'mnsg.z64').read_bytes()==rom and cross._funcs(elf)==f0 and rel_ok:
  d['guarded_abs_restorations']=restore(co,r,[bd/(x['staged_path']+'.o') for x in doc['functions']],g0,opening.stable_globals(elf));save()
  if d['guarded_abs_restorations']:d['known_metadata_restorations']=link('metadata-relink')
 img=(bd/'mnsg.z64').read_bytes();d['expanded_rom_exact']=img==rom;d['expanded_sha1']=hashlib.sha1(img).hexdigest();d['first_rom_mismatch']=next((i for i,(x,y) in enumerate(zip(img,rom)) if x!=y),None);f1=cross._funcs(elf);r1=glitch.all_semantic_relocations(elf);g1=opening.stable_globals(elf)
 d['function_identity_exact']=f1==f0;d['function_identities']=sum(f1.values());d['function_removed']=list((f0-f1).items())[:50];d['function_added']=list((f1-f0).items())[:50];d['semantic_relocations_exact']=r0==r1;d['semantic_relocations_before']=r0[1];d['semantic_relocations_after']=r1[1];d['semantic_relocation_sha256']=r1[2];d['relocations_removed']=list((r0[0]-r1[0]).items())[:100];d['relocations_added']=list((r1[0]-r0[0]).items())[:100];d['globals_exact']=g0==g1;d['globals_removed']=list((g0-g1).items())[:100];d['globals_added']=list((g1-g0).items())[:100];d['stable_globals']=sum(g1.values())
 newtxt=subprocess.check_output(['readelf','-Ws',str(elf)],text=True);current,markers=inventory.parse_inventory_symbols(newtxt);promoted={x['name'] for x in doc['functions']};d['ownership_exact']=(oldmarkers-markers)==promoted and not markers-oldmarkers;d['observed_new_ownership']=len(oldmarkers-markers);d['candidate_elf_sha256']=sha(elf.read_bytes());save();print(r, {k:d[k] for k in ('expanded_rom_exact','function_identity_exact','semantic_relocations_exact','globals_exact','ownership_exact')},flush=True)
 if aliases:
  for a in aliases:
   n=a['name'];before=[x.split()[1:] for x in oldtxt.splitlines() if x.split() and x.split()[-1]==n];after=[x.split()[1:] for x in newtxt.splitlines() if x.split() and x.split()[-1]==n];assert before==after and len(before)==1, (before,after);a['identity_exact']=True
 if img==rom:
  retail=w/'trial-retail.z64';withlog=w/'retail.log'
  with withlog.open('w') as f:subprocess.run([uv,'run','python','tools/rommy.py','compress','--input',str(bd/'mnsg.z64'),'--output',str(retail),'--manifest',f'config/{r}/rommy.yaml','--pad','--verify'],cwd=co,stdout=f,stderr=subprocess.STDOUT,check=True)
  d['retail_exact']=retail.read_bytes()==(co/f'config/{r}/baserom.z64').read_bytes();d['retail_sha1']=hashlib.sha1(retail.read_bytes()).hexdigest();retail.unlink();save()
 d['strict_inventory']=inventory.summarize_inventory(oldtxt,newtxt,promoted);save();assert not d['blocked'] and not d['errors'] and len(promoted)==d['requested'];assert all(d.get(k) is True for k in ('expanded_rom_exact','retail_exact','function_identity_exact','globals_exact','ownership_exact'));assert d['semantic_relocations_exact'];assert not d['strict_inventory']['size_annotation_differences'];d['stage']='completed_trial';d['status']='PASSED_G2_LOCAL';save();print(r,'PASS',flush=True)
