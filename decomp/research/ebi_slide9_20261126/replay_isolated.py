#!/usr/bin/env python3
"""Independently replay nine source-pinned Ebi Slide candidates, no canonical changes."""
from pathlib import Path
import argparse,hashlib,json,subprocess,re
from decomp.consolidated_batch_promotion import exact,FLAGS,stage,jp55,probe,text,rels,glitch
from decomp import promo65_promotion as prev

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--usa',type=Path,required=True);p.add_argument('--jp',type=Path,required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args();a.work.mkdir(exist_ok=True)
 specs=[('usa','func_801DF3D8_59B2E8',460,19,268,'NO_NEW_COMPILER_FINDING'),('usa','func_801DFE44_59BD54',300,12,268,'EXISTING_QUIRK_REPRODUCED'),('usa','func_801E3400_59F310',848,39,270,'EXISTING_QUIRK_REPRODUCED'),('usa','func_801CBAF8_587A08',240,10,272,'EXISTING_QUIRK_REPRODUCED'),('japan_0','func_801E46AC_5A067C',460,19,268,'NO_NEW_COMPILER_FINDING'),('japan_0','func_801E5108_5A10D8',300,12,268,'EXISTING_QUIRK_REPRODUCED'),('japan_0','func_801E905C_5A502C',220,6,270,'NO_NEW_COMPILER_FINDING'),('japan_0','func_801E8610_5A45E0',956,42,270,'EXISTING_QUIRK_REPRODUCED'),('japan_0','func_801D1228_58D1F8',236,10,272,'EXISTING_QUIRK_REPRODUCED')]
 sha=lambda b:hashlib.sha256(b).hexdigest();gsha=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();ledger=a.repo/'decomp/COMPILER_QUIRKS.md';out=[];refs={}
 for r,co in [('usa',a.usa),('japan_0',a.jp)]:
  rom=(co/f'config/{r}/baserom.decompressed.z64').read_bytes();assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==prev.REGIONS[r]['rom'];assert sha((co/'tools/ido-5.3/cc').read_bytes())==stage.COMPILER_SHA;assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=co,text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee';refs[r]=(co,rom)
 for r,n,z,count,pr,outcome in specs:
  co,rom=refs[r];v,off=map(lambda x:int(x,16),n.split('_')[1:]);owner_matches=[x for x in (co/f'asm/{r}').glob('*.s') if f'glabel {n}\n' in x.read_text()];assert len(owner_matches)==1,(n,owner_matches);owner=owner_matches[0];probe.get_original_splat_lines(owner,n,off,v,z,rom[off:off+z]);raw=owner.read_text();m=[m for m in jp55.BLOCK.finditer(raw) if m['name']==n];assert len(m)==1; m=m[0];asm=a.work/(n+'.ref.s');ref=a.work/(n+'.ref.o');asm.write_text('.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'+raw[m.start():m.end()]+'\n');subprocess.run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(ref),str(asm)],cwd=co,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  rec={'region':r,'name':n,'rom_offset':off,'vma':v,'original_bytes':z,'owner':owner.name,'code_sha256':sha(rom[off:off+z]),'relocation_count':count,'research_pr':pr,'compiler_quirk_outcome':outcome,'flags':FLAGS,'compiler_sha256':stage.COMPILER_SHA,'ledger_sha256':sha(ledger.read_bytes()),'attempts':[]}
  for kind in ['candidate','negative']:
   ledger.read_text();src=a.source/n/(kind+'.c');obj=a.work/(n+'.'+kind+'.o');log=a.work/(n+'.'+kind+'.log');cmd=[str(co/'tools/ido-5.3/cc'),*FLAGS,'-o',str(obj),str(src)];
   with log.open('w') as f:subprocess.run(cmd,cwd=co,check=True,stdout=f,stderr=subprocess.STDOUT)
   matched=exact(obj,ref,rec);actual=text(obj);expected=text(ref);first=next((i for i in range(0,min(z,len(actual)),4) if actual[i:i+4]!=expected[i:i+4]),None);rec['attempts'].append({'variant':kind,'source_sha256':sha(src.read_bytes()),'git_blob_sha1':gsha(src.read_bytes()),'exact':matched,'first_raw_word_difference':first,'raw_matching_words':sum(actual[i:i+4]==expected[i:i+4] for i in range(0,z,4)),'named_relocations_exact':rels(obj)==rels(ref),'native_outcome':outcome if kind=='candidate' and matched else 'NO_NEW_COMPILER_FINDING','command':['tools/ido-5.3/cc',*FLAGS,'-o','<private-object>',f'sources/{n}/{kind}.c']});assert matched==(kind=='candidate'),(n,kind,rec['attempts'][-1]);
   if kind=='candidate':glitch.check_nontext(obj)
  out.append(rec);(a.work/'isolated-replay.json').write_text(json.dumps(out,indent=2)+'\n');print(r,n,z,'positive exact; negative rejected',flush=True)
if __name__=='__main__':main()
