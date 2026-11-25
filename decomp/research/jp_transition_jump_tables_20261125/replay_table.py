#!/usr/bin/env python3
"""Native text and jump-table comparison against independent original ASM."""
import argparse,collections,hashlib,json,pathlib,re,struct
import reference_helpers as m
P=pathlib.Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=P,required=True);p.add_argument('--upstream',type=P,required=True);p.add_argument('--out',type=P,required=True);p.add_argument('sources',type=P,nargs='+');a=p.parse_args();U=a.upstream.resolve();O=a.out.resolve();O.mkdir(parents=True,exist_ok=False)
assert m.run(['git','rev-parse','HEAD'],U).strip()==m.PIN
assert not m.run(['git','status','--porcelain','--untracked-files=no'],U).strip()
cc=U/'tools/ido-5.3/cc';assert m.digest(cc.read_bytes())==m.CC_SHA
rom=(U/'config/japan_0/baserom.decompressed.z64').read_bytes();assert m.digest(rom,'sha1')==m.ROM_SHA
assert m.digest((U/'config/japan_0/baserom.z64').read_bytes(),'sha1')==m.RETAIL_SHA
ledger=a.repo/'decomp/COMPILER_QUIRKS.md';ldhash=m.digest(ledger.read_bytes())
name=re.search(r'func_8000[0-9A-F]+_[0-9A-F]+',a.sources[0].stem)[0];vma,off=(int(x,16) for x in name.split('_')[1:]);size,table,toff,tsize={'func_800020D8_2CD8':(564,0x80080234,0x80e34,20),'func_80002EF4_3AF4':(412,0x80080278,0x80e78,24),'func_800024B8_30B8':(512,0x80080248,0x80e48,24),'func_800026B8_32B8':(544,0x80080260,0x80e60,24)}[name];table_name=f'jtbl_{table:X}_{toff:X}'
asm=(U/'asm/japan_0/nonmatchings/main_2BE0'/f'{name}.s').read_text();body=re.search(r'^glabel '+name+r'\n.*?^endlabel '+name+r'$',asm,re.M|re.S)[0];pool=(U/'asm/japan_0/data/main_2BE0.rodata.s').read_text();pool=re.search(r'^dlabel '+table_name+r'\n.*?^enddlabel '+table_name+r'$',pool,re.M|re.S)[0]
pre='.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text,"ax"\n'
def link(obj):
    sym=m.run(['readelf','-Ws',obj],U);defs={'g_system':0x800924B0,'g_system_ptr':0x80161DB8,'g_display_list_head_ptr':0x80161DBC};
    for s in re.findall(r'^\s*\d+:\s+[\da-f]+\s+(?:\d+|0x[\da-f]+)\s+\S+\s+\S+\s+\S+\s+UND[ \t]+(\S+)',sym,re.M):
        if s not in defs:
            mm=re.fullmatch(r'(?:func|D)_([\dA-Fa-f]+)(?:_[\dA-Fa-f]+)?',s);assert mm,s;defs[s]=int(mm[1],16)
    ld=obj.with_suffix('.ld');elf=obj.with_suffix('.elf');ld.write_text(f'SECTIONS {{ .text 0x{vma:X} : SUBALIGN(4) {{ *(.text) }} .rodata 0x{table:X} : SUBALIGN(4) {{ *(.rodata) }} /DISCARD/ : {{ *(.reginfo) *(.MIPS.abiflags) *(.pdr) *(.comment) *(.mdebug*) *(.options) }} }}\n'+''.join(f'{s} = 0x{v:X};\n' for s,v in defs.items()))
    m.run(['mips-linux-gnu-ld','-T',ld,'--emit-relocs','-o',elf,obj],U)
    result=[]
    for sec in ('text','rodata'):
        raw=obj.with_suffix('.'+sec+'.bin');m.run(['mips-linux-gnu-objcopy','-O','binary','-j','.'+sec,elf,raw],U);result.append(raw.read_bytes())
    sy=m.run(['readelf','-Ws',elf],U);ms=re.findall(r'^\s*\d+:\s+([\da-f]+)\s+(\d+)\s+FUNC\s+GLOBAL\s+DEFAULT\s+\d+\s+'+name+r'$',sy,re.M);assert len(ms)==1 and int(ms[0][0],16)==vma
    return result[0][:int(ms[0][1])],result[1]
def rels(obj,sec):
    s=m.run(['readelf','-Wr',obj],U);mark=f"Relocation section '.rel.{sec}'";s=s.split(mark)[1].split('Relocation section')[0] if mark in s else ''
    return collections.Counter((int(o,16),t,n) for o,t,n in re.findall(r'^([\da-f]+)\s+[\da-f]+\s+(R_MIPS_\w+)\s+[\da-f]+\s+(\S+)',s,re.M))
refs={}
for kind in ('named','numeric'):
    text=body
    if kind=='numeric':text=re.sub(r'%(hi|lo)\(D_([0-9A-F]{1,7})\)',lambda x:str((int(x[2],16)+0x8000)>>16 if x[1]=='hi' else (int(x[2],16)+0x8000)%65536-0x8000),text)
    ref=O/(kind+'.s');ref.write_text(pre+text+'\n.section .rodata,"a"\n'+pool+'\n');obj=ref.with_suffix('.o');m.run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',obj,ref],U);tx,ro=link(obj);assert tx==rom[off:off+size];assert ro[:tsize]==rom[toff:toff+tsize];refs[kind]=(rels(obj,'text'),rels(obj,'rodata'))
# Only compiler-local table identity may differ. Both linked text table address and
# linked table destinations must be exact; raw tuples also retained for audit.
for src in a.sources:
    assert src.stem.startswith(name+'_')
    ledger.read_text();assert m.digest(ledger.read_bytes())==ldhash
    obj=O/(src.stem+'.o');m.run([cc,*m.FLAGS,'-o',obj,src.resolve()],U);tx,ro=link(obj);rr=rels(obj,'text');rt=rels(obj,'rodata');ref=refs['numeric'][0];norm=collections.Counter((o,t,'.rodata' if n==table_name else n) for o,t,n in ref.elements());# local table references compare at identical addresses
    normrt=collections.Counter((o,t,'.text' if n.startswith('.L8000') else n) for o,t,n in refs['numeric'][1].elements())
    dif=[i for i in range(0,min(len(tx),size),4) if tx[i:i+4]!=rom[off+i:off+i+4]];first=dif[0] if dif else (size if len(tx)!=size else None)
    row=dict(region='japan_0',target=name,rom_offset=hex(off),vma=hex(vma),size=size,generated_size=len(tx),source_sha256=m.digest(src.read_bytes()),original_sha256=m.digest(rom[off:off+size]),linked_sha256=m.digest(tx),matching_words=min(len(tx),size)//4-len(dif),total_words=size//4,first_mismatch=first,first_original_word=rom[off+first:off+first+4].hex() if first is not None else None,first_generated_word=tx[first:first+4].hex() if first is not None else None,text_exact=tx==rom[off:off+size],table_offset=hex(toff),table_extent=tsize,native_pool_extent=len(ro),table_exact=ro[:tsize]==rom[toff:toff+tsize],pool_tail_zero=not any(ro[tsize:]),table_sha256=m.digest(ro[:tsize]),original_table_sha256=m.digest(rom[toff:toff+tsize]),named_text_relocs=sum(refs['named'][0].values()),numeric_text_relocs=sum(ref.values()),native_text_relocs=sum(rr.values()),text_relocation_type_offset_identity_equal=norm==rr,semantic_text_relocs_equal=norm==rr and tx==rom[off:off+size],table_relocation_type_offset_identity_equal=normrt==rt,semantic_table_relocs_equal=normrt==rt and ro[:tsize]==rom[toff:toff+tsize],reference_table_relocs=sum(normrt.values()),native_table_relocs=sum(rt.values()),raw_reference_table_relocs=list(refs['numeric'][1].elements()),raw_native_table_relocs=list(rt.elements()),reference_only_text=list((norm-rr).elements()),native_only_text=list((rr-norm).elements()),flags=m.FLAGS,ledger_sha256=ldhash,compiler_sha256=m.CC_SHA,compiler_outcome='NO_NEW_COMPILER_FINDING',first_mismatch_class='NONE' if first is None else ('BRANCH_DISPLACEMENT' if first==32 else 'REGISTER_ALLOCATION_OR_SCHEDULING'))
    (O/(src.stem+'.json')).write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row),flush=True)
