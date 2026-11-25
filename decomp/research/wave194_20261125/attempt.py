#!/usr/bin/env python3
"""Private native batch integration trial. Does not edit canonical manifests or publish.
Run after exact canonical predecessor is rebuilt; extends the existing stager only to preserve authenticated zero-prefix padding.
"""
import argparse,hashlib,json,os,shutil,subprocess,sys,traceback
from pathlib import Path
from decomp.consolidated_batch_promotion import exact, FLAGS, stage, cross, splice, opening, cright, glitch, inventory, jp55, probe
from decomp import native251_promotion as native, usa_short72_promotion as short72
from prefix_stage import stage_with_prefix
from finish import finish
ROOT=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def js(path,d):path.write_text(json.dumps(d,indent=2)+'\n')
def run(args,cwd,log):
 with log.open('w') as f: subprocess.run([str(x) for x in args],cwd=cwd,stdout=f,stderr=subprocess.STDOUT,check=True)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--region',choices=['usa','japan_0'],required=True);p.add_argument('--checkout',type=Path,required=True);p.add_argument('--pristine',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--uv',required=True);p.add_argument('--jobs',type=int,default=4);a=p.parse_args()
 r,co,base,w=a.region,a.checkout.resolve(),a.pristine.resolve(),a.work.resolve();w.mkdir();rows=json.loads(a.manifest.read_text());rows=[{**x,**{k:str((a.manifest.resolve().parent/x[k]).resolve()) for k in ('source','negative_source')}} for x in rows];bd=co/f'build/{r}';elf=bd/'mnsg.elf';prior=w/'prior.elf';rom=stage.original(co,r);d={'region':r,'requested':len(rows),'status':'RESEARCH_ONLY','stage':'preflight','native':[],'blocked':[],'errors':[]};report=w/'summary.json';js(report,d)
 try:
  expected={'usa':'2e3f1a026ace3822f9db944c92169a6fe7c6083b2b970841c76f3e11b6559151','japan_0':'ebe91bd0a279d5e4477303b6f462a0104a43cac3b1a08ac37e073e9f748b47d8'}[r]
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
  doc=stage_with_prefix(co,r,candidates=rows,namespace='wave194');d['blocked']=doc['blocked'];d['staged']=len(doc['functions']);d['fragments']=len(doc['fragments']);d['parents']=len(doc['parents']);js(report,d);print(r,'staged',d['staged'],'blocked',len(d['blocked']),flush=True)
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
  finish(r,co,base,w,a.uv,a.jobs,d,doc)
 except Exception as e:
  d['errors'].append({'stage':d['stage'],'error':str(e)});js(report,d);traceback.print_exc();raise
if __name__=='__main__':main()
