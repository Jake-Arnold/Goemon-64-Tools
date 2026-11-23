#!/usr/bin/env python3
"""Reproduce native SGI IDO 5.3 isolated matches from private ROM and Splat ASM.

Requires original decompressed 32 MiB USA/JP ROMs and pristine per-region Splat
assembly. Never claims whole-unit/ELF baseline or complete-ROM G2 promotion.
Do not put original ROM/ASM/linked objects into a publication repository.
"""
import argparse, hashlib, json, re, subprocess, struct, os
from pathlib import Path

RELOC_RE = re.compile(r'^\s*([0-9a-fA-F]{8})\s+[0-9a-fA-F]+\s+(R_MIPS_\w+)\s+[0-9a-fA-F]+\s+([^\s]+)', re.M)
FUNC_RE = re.compile(r'^\s*\d+:\s+[0-9A-Fa-f]+\s+(\d+)\s+FUNC\s+\w+\s+\w+\s+\S+\s+(\S+)\s*$', re.M)

def sha256(data):return hashlib.sha256(data).hexdigest()

def get_original_splat_lines(source, name, expected_offset, expected_vma, size, code):
    text=source.read_text()
    rg=r'^nonmatching '+re.escape(name)+r',\s*0x([0-9A-Fa-f]+)\s*\n\s*glabel '+re.escape(name)+r'\s*\n(.*?)^endlabel '+re.escape(name)
    found=re.findall(rg,text,re.M|re.S)
    if len(found)!=1:raise AssertionError('missing/nonunique original ASM owner '+name)
    sz,body=found[0]
    if int(sz,16)!=size:raise AssertionError('Splat extent disagreement '+name)
    raw=[(int(o,16),int(v,16),int(w,16),t.strip()) for o,v,w,t in
         re.findall(r'/\* ([0-9A-Fa-f]+) ([0-9A-Fa-f]+) ([0-9A-Fa-f]{8}) \*/\s*([^\n]+)',body)]
    if len(raw)!=size//4:raise AssertionError('instruction count '+name)
    for i,(off,vma,word,_) in enumerate(raw):
        if off!=expected_offset+i*4 or vma!=(expected_vma+i*4)&0xFFFFFFFF:
            raise AssertionError('Splat ROM/VMA addressing '+name)
        if code[i*4:i*4+4]!=word.to_bytes(4,'big'):
            raise AssertionError('Splat word not authenticated to original ROM '+name)
    return [item[3] for item in raw]

def original_relocs(lines):
    expected=[]
    for i,line in enumerate(lines):
        t='R_MIPS_HI16' if '%hi(' in line else 'R_MIPS_LO16' if '%lo(' in line else ('R_MIPS_26' if re.search(r'\bjal\s+\w',line) else None)
        if t:
            m=(re.search(r'%hi\(([^)]+)\)',line) or re.search(r'%lo\(([^)]+)\)',line) or re.search(r'\bjal\s+(\S+)',line))
            if m is None:raise AssertionError('cannot resolve original relocation')
            expected.append((4*i,t,m.group(1)))
    return sorted(expected)

def native_compile(cc,objcopy,readelf,source,out,env,name):
    # The caller must read compiler quirks ledger immediately before each native compile.
    obj=out/(name+'.o');binfile=out/(name+'.bin')
    p=subprocess.run([str(cc),'-c','-G','0','-non_shared','-O2','-mips2','-o',str(obj),str(source)],capture_output=True,text=True,env=env)
    if p.returncode:
        raise RuntimeError('IDO compile rejected '+name+': '+(p.stderr+p.stdout)[-240:])
    subprocess.run([str(objcopy),'-O','binary','-j','.text',str(obj),str(binfile)],capture_output=True,check=True,env=env)
    reloc=subprocess.run([str(readelf),'-rW',str(obj)],capture_output=True,text=True,check=True).stdout
    symbols=subprocess.run([str(readelf),'-sW',str(obj)],capture_output=True,text=True,check=True).stdout
    return binfile.read_bytes(), reloc, symbols

def check_size(symbols,name,size):
    sizes=[int(k) for k,n in FUNC_RE.findall(symbols) if n==name]
    if sizes!=[size]:return False,sizes
    # One positive-sized function symbol in this translation unit, exactly the target.
    others=[(n,int(k)) for k,n in FUNC_RE.findall(symbols) if int(k)>0 and n!=name]
    return not others,others

def check_exact(source_bytes,code,relocation_output,original_lines,size):
    actual=sorted((int(addr,16),typ,name) for addr,typ,name in RELOC_RE.findall(relocation_output) if int(addr,16)<size)
    expected=original_relocs(original_lines)
    if actual!=expected:return False,'RELOC_MISMATCH',0,actual,expected
    if len(source_bytes)<size:return False,'SHORT_TEXT',len(source_bytes),actual,expected
    mask={pos:(0xfc000000 if typ=='R_MIPS_26' else 0xffff0000) for pos,typ,name in actual}
    for offset in range(0,size,4):
        word=int.from_bytes(source_bytes[offset:offset+4],'big');orig=int.from_bytes(code[offset:offset+4],'big')
        # The Splat source refers to unmodified symbol operands, never symbol+offset.
        # Reject hidden relocation addends even when the reloc opcode matches.
        if offset in mask and (word & (0xffffffff ^ mask[offset])) != 0:
            return False,'NONZERO_RELOC_ADDEND',offset,actual,expected
        if (word & mask.get(offset,0xffffffff)) != (orig & mask.get(offset,0xffffffff)):
            return False,'WORD_DIFF',offset,actual,expected
    if any(source_bytes[size:]):return False,'NONZERO_TEXT_PADDING',size,actual,expected
    return True,'EXACT',None,actual,expected

def run():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('usa-rom','jp-rom','usa-splat','jp-splat','ido','objcopy','readelf','ledger','output'):
        p.add_argument('--'+key,required=True,type=Path)
    p.add_argument('--no-negative-controls',action='store_true')
    args=p.parse_args();here=Path(__file__).resolve().parent
    manifest=json.loads((here/'manifest.json').read_text())
    if len(manifest['candidates'])!=manifest['research_isolated_count'] or len(manifest['candidates'])!=101:raise AssertionError('expected exactly 101 unique originals')
    images={reg:path.read_bytes() for reg,path in [('usa',args.usa_rom),('japan_0',args.jp_rom)]}
    for reg,blob in images.items():
        if len(blob)!=33554432 or hashlib.sha1(blob).hexdigest()!=manifest['original_sha1'][reg]:
            raise AssertionError('original decompressed '+reg+' ROM invalid')
    if sha256(args.ido.read_bytes())!=manifest['ido_cc_sha256']:raise AssertionError('not pinned original IDO cc')
    roots={'usa':args.usa_splat,'japan_0':args.jp_splat}
    if args.output.exists():raise RuntimeError('refuse existing output path')
    args.output.mkdir(parents=True)
    env=os.environ.copy()
    results=[]
    for i,e in enumerate(manifest['candidates']):
        reg=e['region'];name=e['name'];offset=e['rom_offset'];size=e['original_bytes']
        orig=images[reg][offset:offset+size]
        if sha256(orig)!=e['code_sha256']:raise AssertionError('ROM code hash mismatch '+name)
        asm=(roots[reg]/e['owner'])
        lines=get_original_splat_lines(asm,name,offset,e['vma'],size,orig)
        src=here/e['source']
        if sha256(src.read_bytes())!=e['source_sha256']:raise AssertionError('C source hash mismatch '+name)
        # Mandatory IDO quirks preflight before every native attempt
        ledger=args.ledger.read_bytes()
        if b'NO_NEW_COMPILER_FINDING' not in ledger:raise AssertionError('ledger missing classification')
        folder=args.output/(f'{i:03d}');folder.mkdir()
        body,relo,sym=native_compile(args.ido,args.objcopy,args.readelf,src,folder,env,'positive')
        good,reason,diff,actual,expected=check_exact(body,orig,relo,lines,size)
        symok,syminfo=check_size(sym,name,size)
        r={'region':reg,'name':name,'original_bytes':size,'rom_offset':hex(offset),'vma':hex(e['vma']),
           'source_sha256':e['source_sha256'],'positive_match':bool(good),'positive_status':reason,'first_difference':diff,
           'positive_text_size':len(body),'original_elf_symbol_size':size,'function_elf_size_match':symok,
           'native_reloc_count':len(actual),'native_relocation_names_match':actual==expected,
           'original_sha256':e['code_sha256'],'quirk_ledger_sha256':sha256(ledger),
           'compiler_quirk_outcome':e['compiler_quirk_outcome'],'negative_mutation':e['negative_control_change']}
        if not good or not symok:
            print('FAILED POSITIVE',i,name,reason,syminfo,flush=True)
            raise AssertionError('source has not matched original '+name)
        if not args.no_negative_controls:
            neg=here/e['negative_source']
            if sha256(neg.read_bytes())!=e['negative_sha256']:raise AssertionError('negative source changed '+name)
            ledger=args.ledger.read_bytes()
            nbody,nrelo,nsym=native_compile(args.ido,args.objcopy,args.readelf,neg,folder,env,'negative')
            ngood,nreason,ndiff,nactual,nexpected=check_exact(nbody,orig,nrelo,lines,size)
            r.update(negative_distinct=not ngood,negative_reason=nreason,negative_first_difference=ndiff,
                     negative_source_sha256=e['negative_sha256'])
            if ngood:raise AssertionError('negative control did not diverge '+name)
        results.append(r)
        if i%20==19:
            print('VALIDATED',i+1,'of',len(manifest['candidates']),'positive and negative native probes',flush=True)
    out={'base_sha':manifest['stable_decomp_sha'],'status':'ISOLATED_NATIVE_RESEARCH_ONLY',
         'total_verified':len(results),'total_original_bytes':sum(x['original_bytes'] for x in results),
         'negative_controls':sum(x.get('negative_distinct',False) for x in results),
         'complete_rom':'NOT_RUN','full_unit':'NOT_RUN','canonical_promoted_delta':0,'entries':results}
    (args.output/'native_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',out['total_verified'],'original native bodies + ELF FUNC extents; negatives',out['negative_controls'],flush=True)

if __name__=='__main__':run()
