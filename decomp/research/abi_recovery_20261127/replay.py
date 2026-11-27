import json,sys,hashlib,subprocess,time,re,tempfile,collections,os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
W=Path(__file__).resolve().parent; R=Path(os.environ['GOEMON_REPO']).resolve();sys.path.insert(0,str(R))
from scripts import harvest_zero_token as h
from decomp.consolidated_batch_promotion import FLAGS,exact,glitch,jp55,probe,rels,text
from decomp.probe import Elf32,linker_script
P=Path(os.environ['GOEMON_UPSTREAM']).resolve();ledger=R/'decomp/COMPILER_QUIRKS.md';sha=lambda b:hashlib.sha256(b).hexdigest();CC=P/'tools/ido-5.3/cc'
def run(t):
 n=t['name'];z=t['original_bytes'];off=t['rom_offset'];region=t.get('region','usa');o=P/'asm'/region/t['owner'];out={k:v for k,v in t.items() if k not in ('attempts','variants')};out.update(status='NOT_RUN',attempts=[])
 rom=(P/'config'/region/'baserom.decompressed.z64').read_bytes();orig=rom[off:off+z];baseline=Elf32((P/'build'/region/'mnsg.elf').read_bytes());globalmap=baseline.globals();
 with tempfile.TemporaryDirectory(prefix='linked_') as td:
  w=Path(td);(w/'m2c_types.h').write_bytes((W/'m2c_types.h').read_bytes());raw=o.read_text();ms=list(jp55.BLOCK.finditer(raw));m=next(m for m in ms if m['name']==n);blk=raw[m.start():m.end()]+'\n';probe.get_original_splat_lines(o,n,off,t['vma'],z,orig);a=w/'r.s';a.write_text(raw[:ms[0].start()]+blk);ref=w/'r.o';subprocess.run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(ref),str(a)],cwd=P,check=True,capture_output=True);reference=text(ref);meta={**t,'relocation_count':len(rels(ref))}
  def link(obj,tag):
   im=Elf32(obj.read_bytes());linker=w/(tag+'.ld');linker.write_text(linker_script(n,t['vma'],im.undefined(),globalmap));elf=w/(tag+'.elf');p=subprocess.run(['mips-linux-gnu-ld','-T',str(linker),'-o',str(elf),str(obj)],cwd=P,capture_output=True,text=True);assert p.returncode==0,p.stderr;im=Elf32(elf.read_bytes());fn=im.function(n);return fn.value==t['vma'] and im.code(fn)==orig,sha(im.code(fn)),sha(elf.read_bytes())
  rok,rhash,relf=link(ref,'ref');assert rok,'independent reference does not equal ROM';out.update(reference_linked_rom_match=True,reference_code_sha256=rhash,reference_elf_sha256=relf)
  def test(src,label,flags,negative=False):
   l=ledger.read_bytes();c=w/'candidate.c';obj=w/'candidate.o';c.write_text(src);obj.unlink(missing_ok=True);p=subprocess.run([str(CC),*flags,'-I'+str(w),'-o',str(obj),str(c)],cwd=P,capture_output=True,text=True,timeout=20);rec={'label':label,'source':src,'source_sha256':sha(src.encode()),'ledger_sha256':sha(l),'flags':flags,'returncode':p.returncode,'negative':negative,'outcome':'NO_NEW_COMPILER_FINDING'};out['attempts'].append(rec)
   if p.returncode or not obj.exists():rec.update(category='compile_failure',diagnostic=p.stderr);return False,999
   b=text(obj);diff=[i for i in range(0,z,4) if reference[i:i+4]!=b[i:i+4]];d=len(diff)+sum(1 for i in range(z,len(b),4) if any(b[i:i+4]));ok=exact(obj,ref,meta)
   try:glitch.check_nontext(obj)
   except Exception:ok=False
   rec.update(exact_object=ok,diff_words=d,first_mismatch={'offset':diff[0],'ref_sha256':sha(reference[diff[0]:diff[0]+4]),'candidate_sha256':sha(b[diff[0]:diff[0]+4]),'category':'instruction_or_scheduling'} if diff else (None if ok else {'category':'extent_relocation_or_section'}))
   if ok:
    lm,ch,eh=link(obj,'candidate');rec.update(linked_rom_match=lm,linked_code_sha256=ch,linked_elf_sha256=eh);ok=lm
   return ok,d
  positive=None;seen=set();flags=None
  for v in t['variants']:
   key=(sha(v['source'].encode()),tuple(v.get('flags',FLAGS)))
   if key in seen:continue
   seen.add(key);flags=v.get('flags',FLAGS);ok,d=test(v['source'],v['label'],flags)
   if ok:positive=v['source'];break
  if positive:
   negs=[t['negative_c']] if 'negative_c' in t else h._make_negative(positive,n)[:3]
   for neg in negs:
    ok,_=test(neg,'altered_source_control',flags,True)
    if not ok and out['attempts'][-1]['returncode']==0:
     out.update(status='LINKED_EXACT',candidate_c=positive,negative_c=neg,code_sha256=sha(orig),relocation_count=meta['relocation_count'],flags=flags);return out
   out['status']='NEGATIVE_CONTROL_FAILED';return out
  out['status']='MISMATCH';return out

def safe(t):
 try:return run(t)
 except Exception as e:return {'name':t['name'],'status':'ERROR','error':str(e),'attempts':[]}
if __name__=='__main__':
 ts=json.loads(Path(sys.argv[1]).read_text());dest=Path(sys.argv[2]);stats=collections.Counter();st=time.monotonic()
 with dest.open('w') as f,ProcessPoolExecutor(max_workers=int(os.environ.get('GOEMON_JOBS','4'))) as pool:
  for i,res in enumerate(pool.map(safe,ts,chunksize=1),1):
   stats[res['status']]+=1;f.write(json.dumps(res)+'\n');f.flush()
   if res['status']=='LINKED_EXACT':print('LINKED_EXACT',res['name'],res['original_bytes'],flush=True)
   if i%20==0:print(i,dict(stats),round(time.monotonic()-st,1),flush=True)
 print('DONE',dict(stats),flush=True)
