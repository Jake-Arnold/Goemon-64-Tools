#!/usr/bin/env python3
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from decomp.consolidated_batch_promotion import exact, FLAGS, rels, text, probe, jp55, glitch

def sha(b): return hashlib.sha256(b).hexdigest()
def run(args,co,log):
 with log.open('w') as f: subprocess.run([str(a) for a in args],cwd=co,check=True,stdout=f,stderr=subprocess.STDOUT)
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--usa',type=Path,required=True);p.add_argument('--jp',type=Path,required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=False)
 kit=Path(__file__).resolve().parent;ledger=a.repo/'decomp/COMPILER_QUIRKS.md';out=[];refs={}
 for r,co,want in [('usa',a.usa,'6ea0ed71032ce08fc2745f412d84936382197494'),('japan_0',a.jp,'6f8745fecc3a5e7d4918c7a73353eb0726116ded')]:
  rom=(co/f'config/{r}/baserom.decompressed.z64').read_bytes();assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==want
  assert sha((co/'tools/ido-5.3/cc').read_bytes())=='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0';assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=co,text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
  refs[r]=(co,rom)
 for row in json.loads((kit/'manifest.json').read_text()):
  r,n,z=row['region'],row['name'],row['original_bytes'];co,rom=refs[r];v,off=map(lambda x:int(x,16),n.split('_')[1:]);folder=co/f'asm/{r}';owners=[x for x in folder.glob('*.s') if f'glabel {n}\n' in x.read_text()]; owners += list(folder.glob(f'nonmatchings/**/{n}.s')) if not owners else []
  assert len(owners)==1,(n,owners);owner=owners[0];code=rom[off:off+z];probe.get_original_splat_lines(owner,n,off,v,z,code);raw=owner.read_text();m=[m for m in jp55.BLOCK.finditer(raw) if m['name']==n];assert len(m)==1;m=m[0]
  asm=a.work/(n+'.ref.s');ref=a.work/(n+'.ref.o');asm.write_text('.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'+raw[m.start():m.end()]+'\n');run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',ref,asm],co,a.work/(n+'.as.log'))
  rec={**row,'rom_offset':off,'vma':v,'original_code_sha256':sha(code),'owner':str(owner.relative_to(co)),'flags':FLAGS,'compiler_sha256':sha((co/'tools/ido-5.3/cc').read_bytes()),'ledger_sha256':sha(ledger.read_bytes()),'attempts':[]}
  rel=rels(ref)
  if rec['relocation_count'] is None: rec['relocation_count']=len(rel)
  assert len(rel)==rec['relocation_count'],(n,rel)
  # Resolve original named symbols from the pinned symbol declarations or their original address names.
  names={name for _,_,name in rel};syms={}
  for path in list((co/f'config/{r}/symbol_addrs').rglob('*.txt'))+list((co/f'.splat/{r}').glob('undefined*.ld')):
   for k,x in re.findall(r'^\s*([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(0x[0-9a-fA-F]+)\s*;',path.read_text(),re.M):syms[k]=int(x,16)
  for name in names:
   if name not in syms:
    match=re.match(r'^(?:func|D)_([0-9a-fA-F]+)(?:_|$)',name)
    assert match,(n,name);syms[name]=int(match[1],16)
  ld=a.work/(n+'.ld');ld.write_text('\n'.join(f'{k} = 0x{syms[k]:X};' for k in sorted(names))+'\n'+f'SECTIONS {{ . = 0x{v:X}; .text : SUBALIGN(4) {{ *(.text) }} /DISCARD/ : {{ *(*) }} }}\n')
  def link(obj,k):
   elf=a.work/(n+'.'+k+'.elf');binfile=a.work/(n+'.'+k+'.bin');run(['mips-linux-gnu-ld','-EB','-m','elf32btsmip','-T',ld,'-o',elf,obj],co,a.work/(n+'.'+k+'.link.log'));run(['mips-linux-gnu-objcopy','-O','binary','-j','.text',elf,binfile],co,a.work/(n+'.'+k+'.copy.log'));b=binfile.read_bytes();return len(b)>=z and b[:z]==code and not any(b[z:])
  assert link(ref,'ref'),(n,'independent linked ASM differs from ROM')
  for kind in ['candidate','negative']:
   ledger.read_text();src=kit/row['source' if kind=='candidate' else 'negative_source'];obj=a.work/(n+'.'+kind+'.o');cmd=[str(co/'tools/ido-5.3/cc'),*FLAGS,'-o',str(obj),str(src)];run(cmd,co,a.work/(n+'.'+kind+'.compile.log'));matched=exact(obj,ref,rec);actual=text(obj);expected=text(ref);first=next((i for i in range(0,min(z,len(actual)),4) if actual[i:i+4]!=expected[i:i+4]),None)
   linked=None
   if kind=='candidate' and matched: linked=link(obj,kind)
   result=dict(variant=kind,source_sha256=sha(src.read_bytes()),source_git_blob_sha1=hashlib.sha1(b'blob '+str(len(src.read_bytes())).encode()+b'\0'+src.read_bytes()).hexdigest(),exact_raw=matched,linked_original_rom_exact=linked,first_raw_word_difference=first,named_relocations_exact=rels(obj)==rel,native_outcome='NO_NEW_COMPILER_FINDING',command=['tools/ido-5.3/cc',*FLAGS,'-o','<private-object>',str(src.relative_to(kit))]);rec['attempts'].append(result)
   if kind=='candidate' and matched:glitch.check_nontext(obj)
  out.append(rec);(a.work/'isolated-replay.json').write_text(json.dumps(out,indent=2)+'\n');print(r,n,z,[(x['variant'],x['exact_raw'],x['linked_original_rom_exact']) for x in rec['attempts']],flush=True)
 if not all(x['attempts'][0]['exact_raw'] and x['attempts'][0]['linked_original_rom_exact'] and not x['attempts'][1]['exact_raw'] for x in out):raise SystemExit('One or more isolated comparisons failed')
if __name__=='__main__':main()
