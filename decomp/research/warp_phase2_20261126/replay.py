#!/usr/bin/env python3
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path

META={
'usa':[
('func_802150E4_5D05B4',128,'5C8770','D_8023A124_5F55F4','func_80221B48_5DD018','func_80221C0C_5DD0DC','func_80219E70_5D5340','func_802150A0_5D0570','func_8003521C_35E1C'),
('func_80215164_5D0634',120,'5C8770','D_8023A128_5F55F8','func_80221B48_5DD018','func_80221C0C_5DD0DC','func_80219E70_5D5340','func_802150A0_5D0570','func_8003521C_35E1C'),
('func_802157C4_5D0C94',108,'5C8770','D_8023A238_5F5708','func_80216DF8_5D22C8',None,None,'func_80215830_5D0D00','func_8003521C_35E1C')],
'japan_0':[
('func_80219E74_5D5404',128,'5D52F0','D_8023EE34_5FA3C4','func_802268B8_5E1E48','func_8022697C_5E1F0C','func_8021EBE0_5DA170','func_80219E30_5D53C0','func_80034E8C_35A8C'),
('func_80219EF4_5D5484',120,'5D52F0','D_8023EE38_5FA3C8','func_802268B8_5E1E48','func_8022697C_5E1F0C','func_8021EBE0_5DA170','func_80219E30_5D53C0','func_80034E8C_35A8C'),
('func_8021A554_5D5AE4',108,'5D5500','D_8023EF48_5FA4D8','func_8021BB68_5D70F8',None,None,'func_8021A5C0_5D5B50','func_80034E8C_35A8C')]}
ROM={'usa':('df8083a54296b8c151917c5333e1c85f014a2a66','6ea0ed71032ce08fc2745f412d84936382197494'),'japan_0':('9843ee979b5f6c80f5eda85df0baed9ae7c4e73b','6f8745fecc3a5e7d4918c7a73353eb0726116ded')}
COMPILER='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
def sha(b):return hashlib.sha256(b).hexdigest()
def run(args,cwd):return subprocess.run([str(a) for a in args],cwd=cwd,check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True).stdout

def main():
 if not __debug__:raise RuntimeError("assertions required")
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--usa',type=Path,required=True);p.add_argument('--jp',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--sources',type=Path,default=Path(__file__).parent/'sources');a=p.parse_args();a.work.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(a.repo))
 from decomp.consolidated_batch_promotion import FLAGS, rels, text, probe, jp55
 from decomp import usa_opening_new2_promotion as opening
 # Helpers used for raw function extent and symbol identity. The independent linked original must match ROM.
 ledger=a.repo/'decomp/COMPILER_QUIRKS.md';report=[]
 for region,co in [('usa',a.usa),('japan_0',a.jp)]:
  rom=(co/f'config/{region}/baserom.decompressed.z64').read_bytes();assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM[region][1]
  assert hashlib.sha1((co/f'config/{region}/baserom.z64').read_bytes()).hexdigest()==ROM[region][0]
  assert sha((co/'tools/ido-5.3/cc').read_bytes())==COMPILER and run(['git','rev-parse','HEAD'],co).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
  for n,z,owner,constant,*_ in META[region]:
   srcs=sorted((a.sources/n).glob('*.c'))
   if not srcs:continue
   v,off=map(lambda x:int(x,16),n.split('_')[1:]);folder=a.work/n;folder.mkdir(exist_ok=True);own=co/f'asm/{region}/{owner}.s';raw=own.read_text();code=rom[off:off+z];probe.get_original_splat_lines(own,n,off,v,z,code)
   matches=[m for m in jp55.BLOCK.finditer(raw) if m['name']==n];assert len(matches)==1;m=matches[0]
   asm=folder/'original.s';ref=folder/'original.o';asm.write_text('.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'+raw[m.start():m.end()]+'\n');run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',ref,asm],co)
   rr=rels(ref);names={name for _,_,name in rr};syms={}
   for path in list((co/f'config/{region}/symbol_addrs').rglob('*.txt'))+list((co/f'.splat/{region}').glob('undefined*.ld')):
    for k,x in re.findall(r'^\s*([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(0x[0-9a-fA-F]+)\s*;',path.read_text(),re.M):syms[k]=int(x,16)
   for name in names:
    if name not in syms:
     match=re.match(r'^(?:func|D)_([0-9a-fA-F]+)(?:_|$)',name);assert match,(n,name);syms[name]=int(match[1],16)
   cv,cf=map(lambda x:int(x,16),constant.split('_')[1:]);ld=folder/'original.ld';ld.write_text('\n'.join(f'{k} = 0x{syms[k]:X};' for k in sorted(names))+'\n'+f'SECTIONS {{ . = 0x{v:X}; .text : SUBALIGN(4) {{ *(.text) }} .rodata 0x{cv:X} : SUBALIGN(4) {{ *(.rodata) }} /DISCARD/ : {{ *(*) }} }}\n')
   def link(obj,label):
    elf=folder/(label+'.elf');binary=folder/(label+'.bin');run(['mips-linux-gnu-ld','-EB','-m','elf32btsmip','-T',ld,'-o',elf,obj],co);run(['mips-linux-gnu-objcopy','-O','binary','-j','.text',elf,binary],co);return binary.read_bytes(),elf
   orig,elf=link(ref,'original');assert orig[:z]==code and not any(orig[z:]);assert probe.check_size(run(['readelf','-Ws',elf],co),n,z)[0]
   rt=text(ref)
   for src in srcs:
    ledger_bytes=ledger.read_bytes();assert b'NO_NEW_COMPILER_FINDING' in ledger_bytes
    obj=folder/(src.stem+'.o');cmd=[str(co/'tools/ido-5.3/cc'),*FLAGS,'-o',str(obj),str(src.resolve())]
    row=dict(region=region,name=n,owner=owner,rom_offset=off,vma=v,original_bytes=z,source=str(src.relative_to(a.sources)),source_sha256=sha(src.read_bytes()),compiler_sha256=COMPILER,ledger_sha256=sha(ledger_bytes),flags=FLAGS,original_code_sha256=sha(code),original_named_relocations=len(rr))
    try:
     run(cmd,co);ct=text(obj);cr=rels(obj);raw=[i for i in range(0,min(z,len(ct)),4) if rt[i:i+4]!=ct[i:i+4]];lb,le=link(obj,src.stem);diff=[i for i in range(0,min(z,len(lb)),4) if code[i:i+4]!=lb[i:i+4]];sz=probe.check_size(run(['readelf','-Ws',le],co),n,z)[0];pool=False
     # Pool contents are verified independently if present. Literal-pool name changes remain a mismatch.
     sec=opening.elf_sections(obj.read_bytes()).get('.rodata')
     if sec and sec['size']:
      ob=obj.read_bytes();pool=ob[sec['offset']:sec['offset']+sec['size']];row['literal_pool_bytes']=len(pool);row['literal_pool_first_word_exact']=pool[:4]==rom[cf:cf+4];row['literal_pool_padding_zero']=not any(pool[4:]);
     row.update(function_extent_exact=sz,linked_words_equal=z//4-len(diff)-max(0,(z-len(lb))//4),first_linked_difference=diff[0] if diff else None,linked_text_exact=sz and lb[:z]==code and not any(lb[z:]),named_relocations_exact=cr==rr,generated_named_relocations=len(cr),raw_text_exact=ct[:z]==rt[:z] and not any(ct[z:]),first_raw_difference=raw[0] if raw else None,classification='NO_NEW_COMPILER_FINDING')
     if row['linked_text_exact'] and not row['named_relocations_exact'] and row.get('literal_pool_first_word_exact'):row['classification']='EXISTING_QUIRK_REPRODUCED'
     row['first_mismatch_category']='none' if row['linked_text_exact'] and row['named_relocations_exact'] else ('relocation' if row['linked_text_exact'] else 'scheduling/register' if sz else 'extent')
    except subprocess.CalledProcessError as e:row.update(error=e.stdout[-500:],classification='EXISTING_QUIRK_NOT_APPLICABLE')
    report.append(row);print(n,src.stem,row.get('linked_words_equal'),row.get('first_linked_difference'),row.get('named_relocations_exact'),row.get('error',''),flush=True)
 (a.work/'evidence.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
