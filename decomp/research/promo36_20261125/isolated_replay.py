"""Independent original Splat reference and native object replay, prior to full-ROM staging."""
import argparse,json,hashlib,subprocess
from pathlib import Path
from decomp.consolidated_batch_promotion import exact,rels,stage,probe,jp55,glitch,cross
BATCH=Path(__file__).resolve().parent
ROOT=BATCH.parents[1]

def run(args,co,log):
    with log.open('w') as f:subprocess.run([str(x) for x in args],cwd=co,stdout=f,stderr=subprocess.STDOUT,check=True)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--region',required=True,choices=['usa','japan_0']);p.add_argument('--pristine',type=Path,required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args();r=a.region;co=a.pristine.resolve();w=a.work.resolve();w.mkdir();rom=stage.original(co,r);sha=lambda b:hashlib.sha256(b).hexdigest();assert sha((co/'tools/ido-5.3/cc').read_bytes())==stage.COMPILER_SHA
    rows=json.loads((BATCH/f'{r}-candidates.json').read_text());results=[]
    for f in rows:
        n=f['name'];off=f['rom_offset'];z=f['original_bytes'];owner=co/f'asm/{r}'/f['owner'];rec={'name':n,'offset':off,'vma':f['vma'],'size':z,'source_sha256':f['source_sha256'],'outcome':'NO_NEW_COMPILER_FINDING'}
        try:
            probe.get_original_splat_lines(owner,n,off,f['vma'],z,rom[off:off+z]);raw=owner.read_text();ms=list(jp55.BLOCK.finditer(raw));m=[m for m in ms if m['name']==n];assert len(m)==1;m=m[0];src=w/(n+'.ref.s');ref=w/(n+'.ref.o');header=raw[:ms[0].start()];header=header if '.include' in header else '.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n';src.write_text(header+raw[m.start():m.end()]+'\n');run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',ref,src],co,w/(n+'.as.log'))
            for key,file,h in [('positive','source','source_sha256'),('negative','negative_source','negative_sha256')]:
                ledger=ROOT/'COMPILER_QUIRKS.md';ledger.read_text();s=BATCH/f[file];assert sha(s.read_bytes())==f[h];obj=w/(n+'.'+key+'.o');run([co/'tools/ido-5.3/cc',*f['flags'],'-I'+str(s.parent),'-o',obj,s],co,w/(n+'.'+key+'.log'));rec[key+'_exact']=exact(obj,ref,f)
            rec['native_exact']=rec['positive_exact'];rec['negative_rejected']=not rec['negative_exact'];rec['relocation_count']=len(rels(ref));rec['ledger_sha256']=sha(ledger.read_bytes());assert rec['native_exact'] and rec['negative_rejected'];glitch.check_nontext(w/(n+'.positive.o'));rec['status']='ISOLATED_EXACT'
        except Exception as e:rec['status']='FAILED_NATIVE';rec['error']=str(e) or 'exact object/negative/nontext gate failed'
        results.append(rec);(w/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
    print(r,len([x for x in results if x['status']=='ISOLATED_EXACT']),len(results))
    return 0 if all(x['status']=='ISOLATED_EXACT' for x in results) else 1
if __name__=='__main__':raise SystemExit(main())
