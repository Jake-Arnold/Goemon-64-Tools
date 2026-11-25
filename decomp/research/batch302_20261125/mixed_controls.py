"""Independent original-assembly reference controls for the five mixed-unit candidates."""
from pathlib import Path
from decomp.consolidated_batch_promotion import exact,FLAGS,jp55,probe,stage
import json,subprocess,hashlib,argparse
P=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--checkout',type=Path,required=True);p.add_argument('--pristine',type=Path,required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args();co=a.checkout;base=a.pristine;w=a.work;w.mkdir(exist_ok=False);rom=stage.original(co,'usa');names={'func_8000A130_AD30','func_80023394_23F94','func_80023480_24080','func_800234D8_240D8','func_80023610_24210'};rows=[x for x in json.loads((P/'usa-candidates.json').read_text()) if x['name'] in names];res=[]
for f in rows:
 n=f['name'];z=f['original_bytes'];off=f['rom_offset'];owner=base/'asm/usa'/f['owner'];probe.get_original_splat_lines(owner,n,off,f['vma'],z,rom[off:off+z]);raw=owner.read_text();m=[m for m in jp55.BLOCK.finditer(raw) if m['name']==n];assert len(m)==1;m=m[0];asm=w/(n+'.s');ref=w/(n+'.ref.o');header='.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n';asm.write_text(header+raw[m.start():m.end()]+'\n');subprocess.run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(ref),str(asm)],cwd=co,check=True)
 results={}
 for kind,path in [('positive',f['source']),('negative',f['negative_source'])]:
  (stage.ROOT/'COMPILER_QUIRKS.md').read_bytes();obj=w/(n+'.'+kind+'.o');subprocess.run([str(co/'tools/ido-5.3/cc'),*FLAGS,'-o',str(obj),str((P/path).resolve())],cwd=co,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);results[kind]=exact(obj,ref,f)
 res.append({'name':n,'native_exact':results['positive'],'negative_rejected':not results['negative'],'outcome':'NO_NEW_COMPILER_FINDING','source_sha256':f['source_sha256'],'negative_sha256':f['negative_sha256']});print(res[-1])
(w/'summary.json').write_text(json.dumps(res,indent=2)+'\n');assert all(x['native_exact'] and x['negative_rejected'] for x in res)
