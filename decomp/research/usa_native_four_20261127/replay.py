#!/usr/bin/env python3
"""Private original-ROM isolated replay; no whole-ROM promotion or output ROM.
Requires live repository source, clean pinned upstream USA extraction + pristine ELF,
and original MIPS binutils and SGI IDO 5.3 on PATH. No private bytes published.
"""
import argparse,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()
def run(cmd,**kw):return subprocess.check_output([str(x) for x in cmd],stderr=subprocess.STDOUT,**kw)
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--upstream',type=Path,required=True);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args()
    root=a.repo.resolve();co=a.upstream.resolve();here=Path(__file__).resolve().parent;sys.path.insert(0,str(root))
    from decomp.consolidated_batch_promotion import exact,glitch,jp55,probe,rels,text
    from decomp.verify import claimed_functions,load_manifest
    rom=(co/'config/usa/baserom.decompressed.z64').read_bytes();retail=(co/'config/usa/baserom.z64').read_bytes();elf=co/'build/usa/mnsg.elf';cc=co/'tools/ido-5.3/cc';ledger=root/'decomp/COMPILER_QUIRKS.md'
    require(run(['git','rev-parse','HEAD'],cwd=co,text=True).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee','upstream pin');require(not run(['git','status','--porcelain','--untracked-files=no'],cwd=co,text=True).strip(),'upstream tracked files modified')
    require(len(rom)==33554432 and hashlib.sha1(rom).hexdigest()=='6ea0ed71032ce08fc2745f412d84936382197494','expanded ROM');require(len(retail)==16777216 and hashlib.sha1(retail).hexdigest()=='df8083a54296b8c151917c5333e1c85f014a2a66','retail ROM');require((co/'build/usa/mnsg.z64').read_bytes()==rom,'pristine rebuild');require(sha(elf.read_bytes())=='83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038','pristine ELF');require(sha(cc.read_bytes())=='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0','compiler pin')
    accepted=claimed_functions(load_manifest(root/'decomp/manifest.json'));symbols={};funcs={}
    for line in run(['readelf','-Ws',elf],text=True).splitlines():
        m=re.match(r'^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+(\w+)\s+\w+\s+\w+\s+(\S+)\s+(\S+)',line)
        if m and m[4]!='UND':
            v=int(m[1],16);sz=int(m[2]);n=m[5];symbols.setdefault(n,set()).add(v)
            if m[3]=='FUNC' and sz:funcs.setdefault(n,set()).add((v,sz))
    evidence=[]
    for f in json.loads((here/'manifest.json').read_text()):
        n=f['name'];v=f['vma'];off=f['rom_offset'];z=f['original_bytes'];original=rom[off:off+z]
        require(sha(original)==f['code_sha256'],'ROM code hash '+n);require(funcs.get(n)=={(v,z)},'pristine FUNC identity '+n);require(not any(x['name']==n or x['rom_offset']<off+z and off<x['rom_offset']+x['size'] for x in accepted),'canonical overlap '+n)
        source=here/f['source'];negative=here/f['negative'];require(sha(source.read_bytes())==f['source_sha256'] and sha(negative.read_bytes())==f['negative_sha256'],'source hash '+n)
        for h,hs in f['headers'].items():require(sha((source.parent/h).read_bytes())==hs,'header hash '+n)
        owner=co/'asm/usa'/f['owner'];probe.get_original_splat_lines(owner,n,off,v,z,original);raw=owner.read_text();ms=list(jp55.BLOCK.finditer(raw));match=[m for m in ms if m['name']==n];require(len(match)==1,'owner '+n)
        with tempfile.TemporaryDirectory(prefix='goemon-native-replay-') as tmp:
            d=Path(tmp);asm=d/'original.s';ref=d/'original.o';pos=d/'candidate.o';neg=d/'negative.o';asm.write_text(raw[:ms[0].start()]+match[0][0]+'\n')
            run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',ref,asm],cwd=co)
            for src,obj in ((source,pos),(negative,neg)):
                ledger.read_text();run([cc,*f['flags'],'-I'+str(source.parent),'-o',obj,src],cwd=co)
            require(exact(pos,ref,f),'native object mismatch '+n);glitch.check_nontext(pos);require(not exact(neg,ref,f),'negative unexpectedly exact '+n)
            # Define external symbols only from the independently verified pristine ELF.
            ext=sorted({sym for _,_,sym in rels(ref) if sym!=n});defs=[]
            for sym in ext:
                require(len(symbols.get(sym,set()))==1,'ambiguous/missing original symbol '+sym);defs.append('--defsym='+sym+'=0x%X'%next(iter(symbols[sym])))
            link=d/'link.ld';link.write_text('SECTIONS { . = 0x%X; .text : SUBALIGN(4) { *(.text) } /DISCARD/ : { *(*) } }\n'%v)
            linked=[]
            for obj in (ref,pos):
                le=d/(obj.stem+'.elf');run(['mips-linux-gnu-ld','-EB','-melf32btsmip','--no-warn-mismatch','-T',link,'-e',n,*defs,'-o',le,obj],cwd=co)
                body=text(le);require(body[:z]==original and not any(body[z:]),'original-address linked bytes '+n)
                symtab=run(['readelf','-Ws',le],text=True);require(re.search(r'^\s*\d+:\s+%08x\s+%d\s+FUNC\s+\w+\s+\w+\s+\S+\s+%s\s*$'%(v,z,re.escape(n)),symtab,re.M|re.I),'linked FUNC identity '+n)
                linked.append(sha(body[:z]))
            evidence.append(dict(name=n,rom_offset=off,vma=v,bytes=z,relocations=f['relocation_count'],candidate_source_sha256=f['source_sha256'],negative_source_sha256=f['negative_sha256'],compiler_flags=f['flags'],compiler_outcome=f['compiler_outcome'],original_address_reference_sha256=linked[0],original_address_candidate_sha256=linked[1],native_object_exact=True,negative_rejected=True,original_address_exact=True,original_func_identity=True,nontext_empty=True))
        print(n,'PASS',z,f['relocation_count'],flush=True)
    report=dict(status='RESEARCH_ONLY',base_commit='35a93f259cc00cde13eaa591008323df1278c24f',region='usa',native_matches=len(evidence),native_bytes=sum(x['bytes'] for x in evidence),named_relocations=sum(x['relocations'] for x in evidence),pristine_expanded_sha1=hashlib.sha1(rom).hexdigest(),pristine_elf_sha256=sha(elf.read_bytes()),ido_sha256=sha(cc.read_bytes()),compiler_ledger_sha256=sha(ledger.read_bytes()),whole_candidate_unit='NOT_RUN',canonical_G2='NOT_RUN',strict_candidate_inventory='NOT_RUN',canonical_promotion_integrity='NOT_RUN',functions=evidence)
    a.report.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
