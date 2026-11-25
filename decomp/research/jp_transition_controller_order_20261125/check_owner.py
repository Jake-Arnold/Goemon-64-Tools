from pathlib import Path
import argparse,re,subprocess as s,collections,hashlib,json
import reference_helpers as helpers
W=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--upstream',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args();U=args.upstream.resolve();O=args.out.resolve();O.mkdir(parents=True,exist_ok=False)
assert helpers.run(['git','rev-parse','HEAD'],U).strip()==helpers.PIN
assert not helpers.run(['git','status','--porcelain','--untracked-files=no'],U).strip()
assert helpers.digest((U/'tools/ido-5.3/cc').read_bytes())==helpers.CC_SHA
assert helpers.digest((U/'config/japan_0/baserom.decompressed.z64').read_bytes(),'sha1')==helpers.ROM_SHA
assert helpers.digest((U/'config/japan_0/baserom.z64').read_bytes(),'sha1')==helpers.RETAIL_SHA
ledger=args.repo.resolve()/'decomp/COMPILER_QUIRKS.md'; print('ledger',helpers.digest(ledger.read_bytes()))
orig=(U/'src/main_2BE0.c').read_text()
candidate=orig
shadow=orig
for name in ('func_800028D8_34D8','func_80002C1C_381C'):
    ap='asm/japan_0/nonmatchings/main_2BE0/'+name+'.s'
    old=f'#pragma GLOBAL_ASM("{ap}")'; assert candidate.count(old)==1
    candidate=candidate.replace(old,(W/'src'/(name+'_named.c')).read_text())
    source=(U/ap).read_text()
    source=re.sub(r'%(hi|lo)\(D_([0-9A-F]{1,7})\)',lambda x:str((int(x[2],16)+0x8000)>>16 if x[1]=='hi' else (int(x[2],16)+0x8000)%65536-0x8000),source)
    numeric=O/(name+'_numeric.s'); numeric.write_text(source)
    shadow=shadow.replace(old,f'#pragma GLOBAL_ASM("{numeric}")')
for tag,src in [('reference',orig),('shadow',shadow),('candidate',candidate)]:
    ledger.read_text()
    f=O/(tag+'.c'); f.write_text(src)
    helpers.run([U/'tools/asm-processor/asm-processor','--input-enc=utf-8','--output-enc=Shift_JIS',U/'tools/ido-5.3/cc','--','mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','--',*helpers.FLAGS,'-I'+str(W/'src'),'-o',O/(tag+'.o'),f],U)
def run(*a):return s.check_output(list(map(str,a)),text=True,cwd=U)
syms={}
for p in list((U/'config/japan_0/symbol_addrs').glob('*.txt'))+list((U/'.splat/japan_0').glob('undefined*ld')):
 for n,v in re.findall(r'^\s*(\w+)\s*=\s*(0x[0-9a-fA-F]+)',p.read_text(),re.M):syms[n]=int(v,16)
rom=(U/'config/japan_0/baserom.decompressed.z64').read_bytes()[0x2be0:0x44f0]
results={}
for tag in ['reference','shadow','candidate']:
 obj=O/(tag+'.o');elf=O/(tag+'.elf');raw=O/(tag+'.bin'); ld=O/(tag+'.ld'); st=run('readelf','-Ws',obj)
 undefined=re.findall(r'^\s*\d+:\s+[\da-f]+\s+(?:\d+|0x[\da-f]+)\s+\S+\s+\S+\s+\S+\s+UND[ \t]+(\S+)',st,re.M)
 defs={}
 for n in undefined:
  if n in syms:defs[n]=syms[n];continue
  m=re.fullmatch(r'(?:func|D|jtbl)_([\dA-Fa-f]+)(?:_[\dA-Fa-f]+)?',n)
  if not m:raise ValueError(n)
  defs[n]=int(m[1],16)
 ld.write_text('SECTIONS { .text 0x80001FE0 : SUBALIGN(4) { *(.text) } /DISCARD/ : { *(.reginfo) *(.MIPS.abiflags) *(.pdr) *(.comment) *(.mdebug*) *(.options) } }\n'+''.join(f'{n} = 0x{v:X};\n' for n,v in defs.items()))
 run('mips-linux-gnu-ld','-T',ld,'--emit-relocs','-o',elf,obj); run('mips-linux-gnu-objcopy','-O','binary','-j','.text',elf,raw)
 funcs=sorted((n,int(v,16),int(z)) for v,z,n in re.findall(r'^\s*\d+:\s+([\da-f]+)\s+(\d+)\s+FUNC\s+GLOBAL\s+DEFAULT\s+\d+\s+(\S+)',run('readelf','-Ws',elf),re.M) if int(z)>0)
 rel=run('readelf','-Wr',obj).split("Relocation section '.rel.text'")[1].split('Relocation section')[0]
 rels=collections.Counter((int(o,16),t,n) for o,t,n in re.findall(r'^([\da-f]+)\s+[\da-f]+\s+(R_MIPS_\w+)\s+[\da-f]+\s+(\S+)',rel,re.M))
 text=raw.read_bytes();print(tag,'bytes',len(text),'exact',text==rom,'functions',len(funcs),'relocs',sum(rels.values()));assert text==rom
 results[tag]=(funcs,rels)
a,b,c=[results[x] for x in ['reference','shadow','candidate']]
removed=a[1]-b[1]; added=b[1]-a[1]
assert not added and removed and all(re.fullmatch(r'D_[0-9A-F]{1,7}',n) for _,_,n in removed)
assert a[0]==b[0]==c[0] and len(c[0])==38
assert b[1]==c[1],(b[1]-c[1],c[1]-b[1])
report={'status':'RESEARCH_ONLY','text_bytes':len(rom),'original_text_sha256':hashlib.sha256(rom).hexdigest(),'all_text_exact':True,'all_38_function_identities_exact':True,'named_reference_relocations':sum(a[1].values()),'numeric_shadow_relocations':sum(b[1].values()),'candidate_relocations':sum(c[1].values()),'removed_synthetic_reference_tuples':list(sorted(removed.elements())),'reference_relocation_multiset_exact':True,'scope':'Two newly exact C functions plus 36 original ASM siblings; independent original numeric shadow for these two functions only; not canonical mixed source layout or full ROM.'};(O/'owner_summary.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
