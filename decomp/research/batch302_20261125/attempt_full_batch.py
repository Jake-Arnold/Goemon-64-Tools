#!/usr/bin/env python3
"""Private native batch integration trial. Does not edit canonical manifests or publish.
Run after exact canonical predecessor is rebuilt; extends the existing stager only to preserve authenticated zero-prefix padding.
"""
import argparse,hashlib,json,os,shutil,subprocess,sys,traceback
from pathlib import Path
from decomp.consolidated_batch_promotion import exact, FLAGS, stage, cross, splice, opening, cright, glitch, inventory, jp55, probe
from decomp import native251_promotion as native, usa_short72_promotion as short72
from prefix_stage import stage_with_prefix
from abs_metadata import restore
from try_mixed import run as trial_mixed
ROOT=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def js(path,d):path.write_text(json.dumps(d,indent=2)+'\n')
def run(args,cwd,log):
 with log.open('w') as f: subprocess.run([str(x) for x in args],cwd=cwd,stdout=f,stderr=subprocess.STDOUT,check=True)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--region',choices=['usa','japan_0'],required=True);p.add_argument('--checkout',type=Path,required=True);p.add_argument('--pristine',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--uv',required=True);p.add_argument('--jobs',type=int,default=4);a=p.parse_args()
 r,co,base,w=a.region,a.checkout.resolve(),a.pristine.resolve(),a.work.resolve();w.mkdir();rows=json.loads(a.manifest.read_text());rows=[{**x,**{k:str((a.manifest.resolve().parent/x[k]).resolve()) for k in ('source','negative_source')}} for x in rows];bd=co/f'build/{r}';elf=bd/'mnsg.elf';prior=w/'prior.elf';rom=stage.original(co,r);d={'region':r,'requested':len(rows),'status':'RESEARCH_ONLY','stage':'preflight','native':[],'blocked':[],'errors':[]};report=w/'summary.json';js(report,d)
 try:
  expected={'usa':'23b0af722f70a8aa86a7ca73874a3a7cd0235cff896f6364333cac04f394d724','japan_0':'ff221878793c5936b86a0f7d8586fdc062129ae58711959a6f711e33dac3aabe'}[r]
  assert sha(elf.read_bytes())==expected,'canonical predecessor ELF hash mismatch'
  assert (bd/'mnsg.z64').read_bytes()==rom and stage.original(base,r)==rom,'canonical original ROM mismatch'
  assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=co,text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
  assert sha((co/'tools/ido-5.3/cc').read_bytes())==stage.COMPILER_SHA
  shutil.copyfile(elf,prior);f0=cross._funcs(prior);g0=opening.stable_globals(prior);r0=glitch.all_semantic_relocations(prior)
  oldtxt=subprocess.check_output(['readelf','-Ws',str(prior)],text=True);oldfuncs,oldmarkers=inventory.parse_inventory_symbols(oldtxt);targets={x['name'] for x in rows};assert targets<=oldmarkers,'canonical C collision or missing ASM marker'
  assert len(targets)==len(rows)
  for x in rows:
   assert x['region']==r and x['flags']==FLAGS and sha(Path(x['source']).read_bytes())==x['source_sha256'] and sha(Path(x['negative_source']).read_bytes())==x['negative_sha256']; assert sha(rom[x['rom_offset']:x['rom_offset']+x['original_bytes']])==x['code_sha256']
  ledger=Path(stage.ROOT)/'COMPILER_QUIRKS.md';ledger.read_text();d['ledger_sha256']=sha(ledger.read_bytes());d['prior_elf_sha256']=expected;d['stage']='owner_integration';js(report,d)
  doc=stage_with_prefix(co,r,candidates=rows,namespace='batch302');d['blocked']=doc['blocked'];d['staged']=len(doc['functions']);d['fragments']=len(doc['fragments']);d['parents']=len(doc['parents']);js(report,d);print(r,'staged',d['staged'],'blocked',len(d['blocked']),flush=True)
  ld=(co/f'.splat/{r}/mnsg.ld').read_text();objs=[f'build/{r}/{x["staged_path"]}.o' for x in doc['functions']]+[f'build/{r}/{x["path"]}.o' for x in doc['fragments']];d['stage']='native_objects';js(report,d)
  ledger.read_text();stage.runmake(co,r,ld,objs,w/'make.log',a.uv,a.jobs)
  # Independent reference is assembled from the authenticated original Splat block.
  for f in doc['functions']:
   n=f['name'];off=f['rom_offset'];z=f['original_bytes'];obj=bd/(f['staged_path']+'.o');owner=base/f'asm/{r}'/f['owner'];rec={'name':n,'offset':off,'size':z,'source_sha256':f['source_sha256'],'outcome':'NO_NEW_COMPILER_FINDING','prior_research_outcome':f['compiler_quirk_outcome']}
   try:
    probe.get_original_splat_lines(owner,n,off,f['vma'],z,rom[off:off+z]);raw=owner.read_text();ms=list(jp55.BLOCK.finditer(raw));m=[m for m in ms if m['name']==n];assert len(m)==1,'reference source boundary';m=m[0]
    src=w/(n+'.ref.s');ref=w/(n+'.ref.o');header=raw[:ms[0].start()];header=header if '.include' in header else '.include \"macro.inc\"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, \"ax\"\n';src.write_text(header+raw[m.start():m.end()]+'\n');run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',ref,src],co,w/(n+'.as.log'))
    rec['native_exact']=exact(obj,ref,f);assert rec['native_exact'],'original object instructions, relocation or extent mismatch';glitch.check_nontext(obj);cross._trim_object(obj,z,rom[off:off+z]);bad=w/(n+'.negative.o');ledger.read_text();run([co/'tools/ido-5.3/cc',*FLAGS,'-o',bad,Path(f['negative_source'])],co,w/(n+'.negative.log'));rec['negative_rejected']=not exact(bad,ref,f);assert rec['negative_rejected'],'negative unexpectedly exact'
   except (ValueError,AssertionError,KeyError,OSError,subprocess.CalledProcessError) as e:rec['error']=str(e)
   d['native'].append(rec);js(report,d)
  print(r,'native positive',sum(x.get('native_exact',False) for x in d['native']),'negative rejected',sum(x.get('negative_rejected',False) for x in d['native']),flush=True)
  for f in doc['fragments']:
   path=bd/(f['path']+'.o');lo,hi=f['start'],f['end']
   try:
    if f['suffix']=='.text.archive61':splice._trim_archive_asm(path,hi-lo)
    else:cross._trim_object(path,hi-lo,rom[lo:hi])
   except (ValueError,AssertionError,KeyError) as e:d['errors'].append({'fragment':f['path'],'error':str(e)})
  js(report,d)
  if d['errors'] or any('error'in x for x in d['native']):raise ValueError('Native object or retained ASM fragment gate failed; no link with unverified inputs')
  mixed_names=set();mixed_objects=[]
  if r=='usa':
   mix=trial_mixed(co,w/'mixed',a.uv,a.jobs);d['mixed_units']=mix['units'];js(report,d)
   for rec in mix['units']:
    if not rec.get('whole_unit_text_equal'):continue
    path=rec['unit'];names=set(rec['names']);assert names<=set(x['name'] for x in d['blocked']);(co/path).write_bytes((w/'mixed'/Path(path).name).read_bytes());target=f'build/{r}/{path}.o';ledger.read_text();stage.runmake(co,r,ld,[target],w/('mixed-'+Path(path).stem+'.log'),a.uv,a.jobs);mixed_names|=names;mixed_objects.append(co/target)
   d['blocked']=[x for x in d['blocked'] if x['name'] not in mixed_names]
   d['mixed_staged']=len(mixed_names);js(report,d)
  def link(label):
   elf.unlink(missing_ok=True);(bd/'mnsg.z64').unlink(missing_ok=True);stage.runmake(co,r,ld,[f'build/{r}/mnsg.z64'],w/(label+'.log'),a.uv,a.jobs)
   if r=='usa':return [short72.restore_original_abs_label_type(elf,prior),native.restore_inline_usa(elf,prior)]
   return []
  d['stage']='combined_link';js(report,d);d['known_metadata_restorations']=link('link')
  # Only restore the precise original ABS metadata from authenticated predecessor objects,
  # following existing guarded symbol-type quirk; no code or relocation changes permitted.
  if (bd/'mnsg.z64').read_bytes()==rom and cross._funcs(elf)==f0 and glitch.all_semantic_relocations(elf)==r0:
   try:
    d['guarded_abs_restorations']=restore(co,r,[bd/(x['staged_path']+'.o') for x in doc['functions']]+mixed_objects,g0,opening.stable_globals(elf));js(report,d)
    if d['guarded_abs_restorations']:d['known_metadata_restorations']=link('metadata-relink')
   except ValueError as e:d['errors'].append({'stage':'ABS_metadata','error':str(e)});js(report,d)

  img=(bd/'mnsg.z64').read_bytes();d['expanded_rom_exact']=img==rom;d['expanded_sha1']=hashlib.sha1(img).hexdigest();d['first_rom_mismatch']=next((i for i,(x,y) in enumerate(zip(img,rom)) if x!=y),None);f1=cross._funcs(elf);r1=glitch.all_semantic_relocations(elf);g1=opening.stable_globals(elf)
  d['function_identity_exact']=f1==f0;d['function_identities']=sum(f1.values());d['function_removed']=list((f0-f1).items())[:50];d['function_added']=list((f1-f0).items())[:50];d['semantic_relocations_exact']=r0==r1;d['semantic_relocations_before']=r0[1];d['semantic_relocations_after']=r1[1];d['relocations_removed']=list((r0[0]-r1[0]).items())[:100];d['relocations_added']=list((r1[0]-r0[0]).items())[:100];d['globals_exact']=g0==g1;d['globals_removed']=list((g0-g1).items())[:100];d['globals_added']=list((g1-g0).items())[:100]
  newtxt=subprocess.check_output(['readelf','-Ws',str(elf)],text=True);current,markers=inventory.parse_inventory_symbols(newtxt);promoted={x['name'] for x in doc['functions']}|mixed_names;d['ownership_exact']=(oldmarkers-markers)==promoted and not markers-oldmarkers;d['observed_new_ownership']=len(oldmarkers-markers);d['candidate_elf_sha256']=sha(elf.read_bytes());js(report,d)
  if img==rom:
   retail=w/'trial-retail.z64';run([a.uv,'run','python','tools/rommy.py','compress','--input',bd/'mnsg.z64','--output',retail,'--manifest',f'config/{r}/rommy.yaml','--pad','--verify'],co,w/'retail.log');d['retail_exact']=retail.read_bytes()==(co/f'config/{r}/baserom.z64').read_bytes();retail.unlink();js(report,d)
  try:d['strict_inventory']=inventory.summarize_inventory(oldtxt,newtxt,promoted)
  except ValueError as e:d['inventory_error']=str(e)
  assert not d['blocked'] and not d['errors'] and len(promoted)==len(rows),'incomplete batch';assert all(d.get(k) is True for k in ('expanded_rom_exact','retail_exact','function_identity_exact','semantic_relocations_exact','globals_exact','ownership_exact')),'native gate failed';assert not d['strict_inventory']['size_annotation_differences'],'strict inventory size drift';d['stage']='completed_trial';js(report,d);print(r,'link checks',{k:d.get(k) for k in ['expanded_rom_exact','retail_exact','function_identity_exact','semantic_relocations_exact','globals_exact','ownership_exact']},flush=True)
 except Exception as e:
  d['errors'].append({'stage':d['stage'],'error':str(e)});js(report,d);traceback.print_exc();raise
if __name__=='__main__':main()
