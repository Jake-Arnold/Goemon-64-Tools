#!/usr/bin/env python3
"""Reproduce isolated native evidence; not a canonical Goemon promotion."""
import argparse, collections, hashlib, json, pathlib, re, subprocess
P = pathlib.Path
HERE = P(__file__).resolve().parent
UPSTREAM = '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
ROM_SHA = '6ea0ed71032ce08fc2745f412d84936382197494'
CC_SHA = '76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
FLAGS = '-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Iinclude -Ilibultra/include -Ilibultra/include/PR -Isrc -I. -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2'.split()
TARGET = {'454c': ('func_8000394C_454C', 0x454c, 0x8000394c, 116), '3cf0': ('func_800030F0_3CF0', 0x3cf0, 0x800030f0, 568)}
VARIANTS = ['454c','454c_negative','454c_symbol','454c_symbol_volatile','3cf0','3cf0_selector','3cf0_loop','3cf0_selector_int','3cf0_selector_minus']
def digest(data, algorithm='sha256'): return hashlib.new(algorithm,data).hexdigest()
def run(cmd, cwd):
    return subprocess.run([str(x) for x in cmd],cwd=cwd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True).stdout
def reloc(obj, cwd):
    s=run(['readelf','-Wr',obj],cwd).split("Relocation section '.rel.text'")[1].split('Relocation section')[0]
    return collections.Counter((int(a,16),b,c) for a,b,c in re.findall(r'^([\da-f]+)\s+[\da-f]+\s+(R_MIPS_\w+)\s+[\da-f]+\s+(\S+)',s,re.M))
def link(obj, key, out, cwd):
    elf=out/(obj.stem+'.elf'); raw=out/(obj.stem+'.bin')
    run(['mips-linux-gnu-ld','-T',HERE/(key+'.ld'),'--emit-relocs','-o',elf,obj],cwd)
    run(['mips-linux-gnu-objcopy','-O','binary','-j','.text',elf,raw],cwd)
    name,_,vma,_=TARGET[key]; sym=run(['readelf','-Ws',elf],cwd)
    matches=[(int(a,16),int(b)) for a,b in re.findall(r'^\s*\d+:\s+([\da-fA-F]+)\s+(\d+)\s+FUNC\s+GLOBAL\s+DEFAULT\s+\d+\s+'+re.escape(name)+r'$',sym,re.M)]
    assert len(matches)==1 and matches[0][0]==vma, (name,matches)
    return raw.read_bytes()[:matches[0][1]],matches[0][1]
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--upstream',required=True,type=P);p.add_argument('--ledger',required=True,type=P);p.add_argument('--out',required=True,type=P);a=p.parse_args();cwd=a.upstream.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    assert run(['git','rev-parse','HEAD'],cwd).strip()==UPSTREAM
    assert not run(['git','status','--porcelain','--untracked-files=no'],cwd).strip(), 'Tracked upstream is dirty'
    cc=cwd/'tools/ido-5.3/cc';assert digest(cc.read_bytes())==CC_SHA
    rom=(cwd/'config/usa/baserom.decompressed.z64').read_bytes();assert len(rom)==33554432 and digest(rom,'sha1')==ROM_SHA
    retail=(cwd/'config/usa/baserom.z64').read_bytes();assert len(retail)==16777216 and digest(retail,'sha1')=='df8083a54296b8c151917c5333e1c85f014a2a66'
    asm=(cwd/'asm/usa/2C40.s').read_text();prologue='\n'.join(asm.splitlines()[:7])+'\n';refs={};reference_bytes={}
    for key,(name,offset,_,size) in TARGET.items():
        body=re.search(r'^glabel '+name+r'\n.*?^endlabel '+name+r'$',asm,re.M|re.S).group(0)
        for kind in (['named','numeric'] if key=='454c' else ['named']):
            src=out/(key+'-original-'+kind+'.s');obj=src.with_suffix('.o');text=body
            if kind=='numeric':
                assert text.count('%hi(D_3ADD6)')==2 and text.count('%lo(D_3ADD6)')==2
                text=text.replace('%hi(D_3ADD6)','4').replace('%lo(D_3ADD6)','-21034')
            src.write_text(prologue+text+'\n');run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',obj,src],cwd)
            b,n=link(obj,key,out,cwd);assert n==size and b==rom[offset:offset+size]
            refs[key,kind]=reloc(obj,cwd);reference_bytes[key,kind]=obj
    evidence=[]
    for variant in VARIANTS:
        # Mandatory preflight: consult and read live/pinned compiler ledger before each attempt.
        ledger=a.ledger.read_bytes();assert b'EXISTING_QUIRK_REPRODUCED' in ledger and b'controller-offset expression' in ledger
        key=variant.split('_')[0];name,offset,_,size=TARGET[key];src=HERE/(variant+'.c');obj=out/(variant+'.o')
        run([cc,*FLAGS,'-o',obj,src],cwd);actual,n=link(obj,key,out,cwd);original=rom[offset:offset+size]
        first=next((i for i in range(0,size,4) if original[i:i+4]!=actual[i:i+4]),None)
        r=reloc(obj,cwd);named=refs[key,'named'];record={'variant':variant,'source_sha256':digest(src.read_bytes()),'ledger_sha256':digest(ledger),'extent':n,'expected_extent':size,'aligned_words_equal':sum(original[i:i+4]==actual[i:i+4] for i in range(0,size,4)),'original_words':size//4,'first_mismatch_offset':first,'linked_bytes_exact':n==size and actual==original,'original_named_relocs':sum(named.values()),'native_text_relocs':sum(r.values()),'named_relocs_equal':named==r,'named_relocs_intersection':sum((named&r).values())}
        if key=='454c':record['numeric_original_relocs_equal']=refs[key,'numeric']==r
        evidence.append(record)
    positive=next(r for r in evidence if r['variant']=='454c');assert positive['linked_bytes_exact'] and positive['numeric_original_relocs_equal'] and not positive['named_relocs_equal']
    assert not next(r for r in evidence if r['variant']=='454c_negative')['linked_bytes_exact']
    assert not any(r['linked_bytes_exact'] for r in evidence if r['variant'].startswith('3cf0'))
    report={'status':'RESEARCH_ONLY','upstream':UPSTREAM,'rom_sha1':ROM_SHA,'cc_sha256':CC_SHA,'flags':FLAGS,'variants':evidence,'full_canonical_G2':'NOT_RUN','full_canonical_CI':'NOT_RUN'}
    (out/'evidence.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
