import argparse,pathlib as P,sys,hashlib,re,collections,subprocess,json,os
import reference_helpers as m
W=P.Path(__file__).resolve().parent
a=argparse.ArgumentParser();a.add_argument('--repo',type=P.Path,required=True);a.add_argument('--upstream',type=P.Path,required=True);a.add_argument('--out',type=P.Path,required=True);a.add_argument('sources',nargs='*',type=P.Path);args=a.parse_args();R=args.repo.resolve();U=args.upstream.resolve();O=args.out.resolve();O.mkdir(parents=True,exist_ok=False)
assert m.run(['git','rev-parse','HEAD'],U).strip()==m.PIN
assert not m.run(['git','status','--porcelain','--untracked-files=no'],U).strip()
cc=U/'tools/ido-5.3/cc';assert m.digest(cc.read_bytes())==m.CC_SHA
rom=(U/'config/japan_0/baserom.decompressed.z64').read_bytes();assert m.digest(rom,'sha1')==m.ROM_SHA
assert m.digest((U/'config/japan_0/baserom.z64').read_bytes(),'sha1')==m.RETAIL_SHA
ledger=R/'decomp/COMPILER_QUIRKS.md';ldhash=m.digest(ledger.read_bytes()); print('ledger',ldhash,flush=True)
for s in args.sources or sorted((W/'src').glob('func_*.c')):
 src=P.Path(s).resolve(); name=re.search(r'func_8000[0-9A-F]+_[0-9A-F]+',src.stem)[0];vma,off=(int(x,16) for x in name.split('_')[1:]);asm=(U/'asm/japan_0/nonmatchings/main_2BE0'/(name+'.s')).read_text();size=int(re.search(r'nonmatching '+name+r', (0x[\da-fA-F]+)',asm)[1],16);orig=rom[off:off+size]
 body=re.search(r'^glabel '+name+r'\n.*?^endlabel '+name+r'$',asm,re.M|re.S)[0]; body=re.sub(r'%(hi|lo)\(D_([0-9A-F]{1,7})\)',lambda x:str((int(x[2],16)+0x8000)>>16 if x[1]=='hi' else (int(x[2],16)+0x8000)%65536-0x8000),body)
 refsrc=O/(name+'_ref.s');refsrc.write_text('.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'+body+'\n');refobj=refsrc.with_suffix('.o');m.run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',refobj,refsrc],U);assert m.link(refobj,name,vma,O,U)==orig
 ledger.read_text(); assert m.digest(ledger.read_bytes())==ldhash
 obj=O/(src.stem+'.o');m.run([cc,*m.FLAGS,'-o',obj,src],U);actual=m.link(obj,name,vma,O,U);rr=m.rels(obj,U);ref=m.rels(refobj,U)
 n=min(len(actual),size);diff=[i for i in range(0,n,4) if actual[i:i+4]!=orig[i:i+4]];first=diff[0] if diff else (n if n!=size or n!=len(actual) else None)
 row=dict(name=name,variant=src.stem,size=size,generated_size=len(actual),matching_words=n//4-len(diff),total_words=size//4,first_mismatch=first,matching_relocations=sum((rr&ref).values()),reference_relocations=sum(ref.values()),native_relocations=sum(rr.values()),exact=actual==orig,source_sha256=m.digest(src.read_bytes()),linked_sha256=m.digest(actual),original_sha256=m.digest(orig),flags=m.FLAGS,ledger_sha256=ldhash,compiler_outcome=('EXISTING_QUIRK_REPRODUCED' if src.stem.endswith('_control') and m.digest(actual)=='7f3231dfb73690360a39db09eaed41700551356a3307b6d41a44867e1c6ae814' else 'EXISTING_QUIRK_REPRODUCED' if src.stem.endswith('4408_explicit_mask') and m.digest(actual)=='67fea1eefd32fe88df53257c9b0d86f8704a93a267cf359cde3e86724f4e5d9c' else 'NO_NEW_COMPILER_FINDING'))
 (O/(src.stem+'.json')).write_text(json.dumps(row,indent=2)+'\n');print(row,flush=True)
