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
for name in ('func_80002D84_3984','func_80002E10_3A10'):
    ap='asm/japan_0/nonmatchings/main_2BE0/'+name+'.s'
    old=f'#pragma GLOBAL_ASM("{ap}")'; assert candidate.count(old)==1
    candidate=candidate.replace(old,(W/'src'/(name+'_named_word.c')).read_text())
for tag,src in [('reference',orig),('candidate',candidate)]:
    ledger.read_text()
    f=O/(tag+'.c'); f.write_text(src)
    helpers.run([U/'tools/asm-processor/asm-processor','--input-enc=utf-8','--output-enc=Shift_JIS',U/'tools/ido-5.3/cc','--','mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','--',*helpers.FLAGS,'-I'+str(W/'src'),'-o',O/(tag+'.o'),f],U)
def run(*a):return s.check_output(list(map(str,a)),text=True,cwd=U)
syms={}
for p in list((U/'config/japan_0/symbol_addrs').glob('*.txt'))+list((U/'.splat/japan_0').glob('undefined*ld')):
 for n,v in re.findall(r'^\s*(\w+)\s*=\s*(0x[0-9a-fA-F]+)',p.read_text(),re.M):syms[n]=int(v,16)
rom=(U/'config/japan_0/baserom.decompressed.z64').read_bytes()[0x2be0:0x44f0]
results={}
for tag in ['reference','candidate']:
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
a,b=[results[x] for x in ['reference','candidate']]
print('relocation difference',a[1]-b[1],b[1]-a[1]);assert a[0]==b[0];assert a[1]==b[1];assert len(b[0])==38
report={'status':'RESEARCH_ONLY','text_bytes':len(rom),'original_text_sha256':hashlib.sha256(rom).hexdigest(),'all_text_exact':True,'all_38_function_identities_exact':True,'reference_relocations':sum(a[1].values()),'candidate_relocations':sum(b[1].values()),'reference_relocation_multiset_exact':True,'scope':'Two new C functions plus 36 original ASM siblings; original inferred text owner only, not current canonical mixed source layout, data/rodata or full ROM.'};(O/'owner_summary.json').write_text(json.dumps(report,indent=2)+'\n')
