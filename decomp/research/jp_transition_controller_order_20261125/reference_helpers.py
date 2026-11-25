#!/usr/bin/env python3
"""Isolated native JP transition block research; no canonical promotion."""
import argparse, collections, hashlib, json, pathlib, re, subprocess
P=pathlib.Path
HERE=P(__file__).resolve().parent
PIN='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
ROM_SHA='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
RETAIL_SHA='9843ee979b5f6c80f5eda85df0baed9ae7c4e73b'
CC_SHA='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
LEDGER_BLOB='10313aba367418d71cd6c332086d2d6a9bf83e39'
FLAGS='-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Iinclude -Ilibultra/include -Ilibultra/include/PR -Isrc -I. -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2'.split()
ACCEPTED={'func_8000324C_3E4C','func_8000327C_3E7C','func_80003760_4360','func_800037A4_43A4'}
def digest(b,alg='sha256'):return hashlib.new(alg,b).hexdigest()
def run(args,cwd):return subprocess.run([str(x) for x in args],cwd=cwd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True).stdout
def rels(o,up):
    s=run(['readelf','-Wr',o],up)
    if "Relocation section '.rel.text'" not in s:return collections.Counter()
    s=s.split("Relocation section '.rel.text'")[1].split('Relocation section')[0]
    return collections.Counter((int(x,16),t,n) for x,t,n in re.findall(r'^([\da-f]+)\s+[\da-f]+\s+(R_MIPS_\w+)\s+[\da-f]+\s+(\S+)',s,re.M))
def link(obj,name,vma,out,up):
    elf=obj.with_suffix('.elf');raw=obj.with_suffix('.bin');ld=obj.with_suffix('.ld')
    sym=run(['readelf','-Ws',obj],up)
    undefined=re.findall(r'^\s*\d+:\s+[\da-f]+\s+\d+\s+\S+\s+\S+\s+\S+\s+UND[ \t]+(\S+)',sym,re.M)
    definitions={'g_system':0x800924B0,'g_system_ptr':0x80161DB8,'g_display_list_head_ptr':0x80161DBC,'osViSetSpecialFeatures':0x8003FB60}
    for s in undefined:
        if s in definitions:continue
        m=re.fullmatch(r'(?:func|D)_([\dA-Fa-f]{8})(?:_[\dA-Fa-f]+)?',s)
        if m:definitions[s]=int(m[1],16);continue
        m=re.fullmatch(r'D_([\dA-Fa-f]+)',s)
        if m:definitions[s]=int(m[1],16);continue
        raise ValueError(s)
    ld.write_text(f'SECTIONS {{ .text 0x{vma:X} : SUBALIGN(4) {{ *(.text) }} /DISCARD/ : {{ *(.reginfo) *(.MIPS.abiflags) *(.pdr) *(.comment) *(.mdebug*) }} }}\n'+''.join(f'{s} = 0x{v:X};\n' for s,v in definitions.items()))
    run(['mips-linux-gnu-ld','-T',ld,'--emit-relocs','-o',elf,obj],up)
    run(['mips-linux-gnu-objcopy','-O','binary','-j','.text',elf,raw],up)
    sy=run(['readelf','-Ws',elf],up)
    m=re.findall(r'^\s*\d+:\s+([\da-f]+)\s+(\d+)\s+FUNC\s+GLOBAL\s+DEFAULT\s+\d+\s+'+name+r'$',sy,re.M)
    assert len(m)==1 and int(m[0][0],16)==vma,(name,m)
    size=int(m[0][1]);return raw.read_bytes()[:size]
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--upstream',type=P,required=True);a.add_argument('--out',type=P,required=True);a.add_argument('--ledger',type=P,required=True);a.add_argument('--source',type=P,action='append');args=a.parse_args()
    up=args.upstream.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    assert run(['git','rev-parse','HEAD'],up).strip()==PIN
    # Splat creates source stubs but may not modify tracked upstream files.
    assert not run(['git','status','--porcelain','--untracked-files=no'],up).strip()
    cc=up/'tools/ido-5.3/cc';assert digest(cc.read_bytes())==CC_SHA
    rom=(up/'config/japan_0/baserom.decompressed.z64').read_bytes();assert len(rom)==33554432 and digest(rom,'sha1')==ROM_SHA
    retail=(up/'config/japan_0/baserom.z64').read_bytes();assert len(retail)==16777216 and digest(retail,'sha1')==RETAIL_SHA
    folder=up/'asm/japan_0/nonmatchings/main_2BE0'
    rows=[]
    for src in args.source or sorted((HERE/'source').glob('func_*.c')):
        src=src.resolve();name=re.search(r'func_8000[0-9A-F]+_[0-9A-F]+',src.stem)[0];vma,off=(int(x,16) for x in name.split('_')[1:]);asm=(folder/(name+'.s')).read_text();size=int(re.search(r'nonmatching '+name+r', (0x[\da-fA-F]+)',asm)[1],16);orig=rom[off:off+size];assert name not in ACCEPTED
        body=re.search(r'^glabel '+name+r'\n.*?^endlabel '+name+r'$',asm,re.M|re.S)[0]
        pre='.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'
        refs={};refb={}
        for kind in (('named','numeric','numeric_alias') if name=='func_80003870_4470' else ('named','numeric')):
            text=body
            if kind in ('numeric','numeric_alias'):
                text=re.sub(r'%hi\(D_([0-9A-F]+)\)',lambda m:str((int(m[1],16)+0x8000)>>16) if len(m[1])<8 else m[0],text)
                text=re.sub(r'%lo\(D_([0-9A-F]+)\)',lambda m:str((int(m[1],16)+0x8000)%65536-0x8000) if len(m[1])<8 else m[0],text)
            if kind=='numeric_alias':
                assert text.count('%hi(g_system + 0x30000)')==1 and text.count('%lo(g_system + 0x30000)')==1
                text=text.replace('g_system + 0x30000','D_800C24B0')
            refsrc=out/(name+'_'+kind+'.s');refsrc.write_text(pre+text+'\n');refobj=refsrc.with_suffix('.o')
            run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',refobj,refsrc],up)
            actual=link(refobj,name,vma,out,up);assert actual==orig,(name,kind)
            refs[kind]=rels(refobj,up)
        if args.ledger:
            led=args.ledger.read_bytes();assert digest(b'blob '+str(len(led)).encode()+b'\0'+led,'sha1')==LEDGER_BLOB
        # Explicitly review compiler ledger for source-line grouping, prototype/ABI,
        # redundant masks, offset provenance, loop scheduling, and metadata padding.
        obj=out/(src.stem+'.o');run([cc,*FLAGS,'-o',obj,src],up);actual=link(obj,name,vma,out,up);rr=rels(obj,up)
        n=min(len(actual),len(orig));first=next((i for i in range(0,n,4) if actual[i:i+4]!=orig[i:i+4]),None)
        if first is None and len(actual)!=len(orig):first=n
        row={'name':name,'variant':src.stem,'rom_offset':hex(off),'vma':hex(vma),'size':size,'generated_size':len(actual),'matching_words':sum(actual[i:i+4]==orig[i:i+4] for i in range(0,n,4)),'total_words':size//4,'first_mismatch':first,'first_mismatch_class':('NONE' if first is None else ('ABI_OR_REGISTER_SCHEDULING' if first<0x10 else 'BRANCH_OR_ADDRESSING_SCHEDULING')),'exact':actual==orig,'source_sha256':digest(src.read_bytes()),'original_sha256':digest(orig),'linked_sha256':digest(actual),'named_relocs':sum(refs['named'].values()),'numeric_relocs':sum(refs['numeric'].values()),'native_relocs':sum(rr.values()),'named_relocs_equal':rr==refs['named'],'numeric_relocs_equal':rr==refs['numeric'],'numeric_alias_relocs_equal':rr==refs.get('numeric_alias',None),'compiler_ledger_git_blob':LEDGER_BLOB,'compiler_outcome':'EXISTING_QUIRK_REPRODUCED' if actual==orig and (rr==refs['numeric'] or rr==refs.get('numeric_alias')) and rr!=refs['named'] else 'NO_NEW_COMPILER_FINDING'}
        rows.append(row);print(name,src.stem,len(actual),row['matching_words'],size//4,first,row['numeric_relocs_equal'],flush=True)
    (out/'report.json').write_text(json.dumps({'region':'japan_0','status':'RESEARCH_ONLY','upstream':PIN,'expanded_sha1':ROM_SHA,'retail_sha1':RETAIL_SHA,'cc_sha256':CC_SHA,'flags':FLAGS,'rows':rows,'full_canonical_G2':'NOT_RUN','full_canonical_CI':'NOT_RUN'},indent=2)+'\n')
if __name__=='__main__':main()
