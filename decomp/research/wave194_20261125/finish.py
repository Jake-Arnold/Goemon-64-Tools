import argparse, pathlib, subprocess, json, hashlib, sys, re
from decomp.consolidated_batch_promotion import stage, cross, opening, glitch, inventory
from decomp import native251_promotion as native, usa_short72_promotion as short72
P=pathlib.Path
from abs_metadata import restore
from alias_proof import link_references, DELTA
from collections import Counter
sha=lambda b:hashlib.sha256(b).hexdigest()
def preserve_alias(co,r,prior,base,doc,ld):
 if r!='japan_0':return ld,[]
 name='func_080040B8_6C8278';label='.L08004178_6C8338';addr=0x08004178;off=0xC0
 f=next(x for x in doc['functions'] if x['name']==name)
 assert f['vma']+off==addr and f['rom_offset']+off==0x6C8338 and off<f['original_bytes']
 syms=subprocess.check_output(['readelf','-Ws',str(prior)],text=True);m=[x.split() for x in syms.splitlines() if x.split() and x.split()[-1]==label];assert len(m)==1 and m[0][1:6]==['08004178','0','NOTYPE','GLOBAL','DEFAULT'] and m[0][6].isdigit()
 original=(base/'asm/japan_0'/f['owner']).read_text();active=(co/f['active_owner']).read_text();assert re.search(r'(?m)^\s*'+re.escape(label)+r':\s*$',original) and re.search(r'(?m)^\s*\.globl '+re.escape(label)+r'\s*$',active) and re.search(r'(?m)^\s*'+re.escape(label)+r':\s*$',active)
 needle=f'build/{r}/{f["staged_path"]}.o(.text);';assert ld.count(needle)==1 and (label not in ld or ld.count(label+' = . + 0xC0;')==1)
 if label not in ld:ld=ld.replace(needle,label+' = . + 0xC0;\n        '+needle,1)
 return ld,[dict(name=label,owner=name,original_address=addr,offset=off,source='authenticated original Splat global interior label',compiler_outcome='NO_NEW_COMPILER_FINDING')]
def finish(r,co,base,w,uv,jobs,d,doc):
 bd=co/f'build/{r}';elf=bd/'mnsg.elf';prior=w/'prior.elf';rom=stage.original(co,r);ldpath=co/f'.splat/{r}/mnsg.ld';ld=ldpath.read_text();ld,aliases=preserve_alias(co,r,prior,base,doc,ld);ldpath.write_text(ld);d['preserved_original_labels']=aliases;d['errors']=[];save=lambda:(w/'summary.json').write_text(json.dumps(d,indent=2)+'\n')
 f0=cross._funcs(prior);g0=opening.stable_globals(prior);r0=glitch.all_semantic_relocations(prior);oldtxt=subprocess.check_output(['readelf','-Ws',str(prior)],text=True);oldfuncs,oldmarkers=inventory.parse_inventory_symbols(oldtxt)
 def link(label):
  elf.unlink(missing_ok=True);(bd/'mnsg.z64').unlink(missing_ok=True);stage.runmake(co,r,ld,[f'build/{r}/mnsg.z64'],w/(label+'.log'),uv,jobs)
  if r=='usa':return [short72.restore_original_abs_label_type(elf,prior),native.restore_inline_usa(elf,prior)]
  return []
 d['stage']='combined_link';save();d['known_metadata_restorations']=link('link-retry');save()
 rfirst=glitch.all_semantic_relocations(elf)
 rel_ok=rfirst==r0 or (r=='japan_0' and r0[0]-rfirst[0]==Counter({DELTA:1}) and not rfirst[0]-r0[0])
 if (bd/'mnsg.z64').read_bytes()==rom and cross._funcs(elf)==f0 and rel_ok:
  d['guarded_abs_restorations']=restore(co,r,[bd/(x['staged_path']+'.o') for x in doc['functions']],g0,opening.stable_globals(elf));save()
  if d['guarded_abs_restorations']:d['known_metadata_restorations']=link('metadata-relink')
 img=(bd/'mnsg.z64').read_bytes();d['expanded_rom_exact']=img==rom;d['expanded_sha1']=hashlib.sha1(img).hexdigest();d['first_rom_mismatch']=next((i for i,(x,y) in enumerate(zip(img,rom)) if x!=y),None);f1=cross._funcs(elf);r1=glitch.all_semantic_relocations(elf);g1=opening.stable_globals(elf)
 d['function_identity_exact']=f1==f0;d['function_identities']=sum(f1.values());d['function_removed']=list((f0-f1).items())[:50];d['function_added']=list((f1-f0).items())[:50];d['semantic_relocations_exact']=r0==r1;d['semantic_relocations_before']=r0[1];d['semantic_relocations_after']=r1[1];d['semantic_relocation_sha256']=r1[2];d['relocations_removed']=list((r0[0]-r1[0]).items())[:100];d['relocations_added']=list((r1[0]-r0[0]).items())[:100];d['globals_exact']=g0==g1;d['globals_removed']=list((g0-g1).items())[:100];d['globals_added']=list((g1-g0).items())[:100];d['stable_globals']=sum(g1.values())
 newtxt=subprocess.check_output(['readelf','-Ws',str(elf)],text=True);current,markers=inventory.parse_inventory_symbols(newtxt);promoted={x['name'] for x in doc['functions']};d['ownership_exact']=(oldmarkers-markers)==promoted and not markers-oldmarkers;d['observed_new_ownership']=len(oldmarkers-markers);d['candidate_elf_sha256']=sha(elf.read_bytes());save();print(r, {k:d[k] for k in ('expanded_rom_exact','function_identity_exact','semantic_relocations_exact','globals_exact','ownership_exact')},flush=True)
 if aliases:
  for a in aliases:
   n=a['name'];before=[x.split()[1:] for x in oldtxt.splitlines() if x.split() and x.split()[-1]==n];after=[x.split()[1:] for x in newtxt.splitlines() if x.split() and x.split()[-1]==n];assert before==after and len(before)==1, (before,after);a['identity_exact']=True
 if r=='japan_0':
  assert img==rom and f1==f0 and g1==g0 and r0[0]-r1[0]==Counter({DELTA:1}) and not r1[0]-r0[0]
  d['independent_original_reference']=link_references(co,base,w,doc,prior,elf,ld,rom);save()
 if img==rom:
  retail=w/'trial-retail.z64';withlog=w/'retail.log'
  with withlog.open('w') as f:subprocess.run([uv,'run','python','tools/rommy.py','compress','--input',str(bd/'mnsg.z64'),'--output',str(retail),'--manifest',f'config/{r}/rommy.yaml','--pad','--verify'],cwd=co,stdout=f,stderr=subprocess.STDOUT,check=True)
  d['retail_exact']=retail.read_bytes()==(co/f'config/{r}/baserom.z64').read_bytes();d['retail_sha1']=hashlib.sha1(retail.read_bytes()).hexdigest();retail.unlink();save()
 d['strict_inventory']=inventory.summarize_inventory(oldtxt,newtxt,promoted);save();assert not d['blocked'] and not d['errors'] and len(promoted)==d['requested'];assert all(d.get(k) is True for k in ('expanded_rom_exact','retail_exact','function_identity_exact','globals_exact','ownership_exact'));assert d['semantic_relocations_exact'] or (r=='japan_0' and d['independent_original_reference']['status']=='PASS');assert not d['strict_inventory']['size_annotation_differences'];d['stage']='completed_trial';d['status']='PASSED_G2_LOCAL';save();print(r,'PASS',flush=True)
