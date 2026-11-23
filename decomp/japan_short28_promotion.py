"""Japanese 28 individually native-exact short functions: fail-closed original-ROM G2.

This stages only canonical ASM-owned functions. It never modifies machine code,
ROM bytes, assembler relocations or accepted C. Full original Japanese ROM,
ELF function identity and complete semantic relocation equality are required.
"""
from __future__ import annotations
import hashlib, json, re, subprocess
from pathlib import Path
from . import japan_jp55_promotion as jp55
from . import japan_cright_promotion as cr
from . import japan_cright_dual_reference as crdual
from . import japan_noop_port as jp329
from . import japan_thirtyfour_c as jp34
from . import glitch_g2_promotion as glitch
from . import overlay_crossregion47 as cross

ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT/'research/jp_short28_20261123'
MANIFEST=PACKAGE/'manifest.json'
MANIFEST_SHA='b4e73af93456761b44b433bef40ac7d75c878f4eea2acd6a289e5fe8597c2ce5'
STAGE=Path('build/japan_0/jp-short28-stage.json')
ROM_SHA='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
BASE_C=2370
BASE_BYTES=127008
BASE_RELOCS=80745
BASE_RELOC_HASH=crdual.NORMALIZED_HASH

def sha(data):return hashlib.sha256(data).hexdigest()

def rows():
    if sha(MANIFEST.read_bytes())!=MANIFEST_SHA:raise ValueError('JP28 manifest content not pinned')
    obj=json.loads(MANIFEST.read_text())
    if (obj.get('format')!='goemon-jp-short28-original-exact-v1' or obj.get('region')!='japan_0'
        or obj.get('upstream_commit')!='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
        or obj.get('original_rom_sha1')!=ROM_SHA or obj.get('prior_c')!=BASE_C
        or obj.get('prior_bytes')!=BASE_BYTES or obj.get('prior_asm')!=5006):
        raise ValueError('Not original canonical Japanese 2370-C provenance')
    functions=obj['functions']; seen=set(); ranges=[]
    if len(functions)!=28 or sum(x['size'] for x in functions)!=1980 or sum(x['native_relocation_count'] for x in functions)!=124:
        raise ValueError('JP28 count/size/native relocation fingerprint drift')
    for f in functions:
        n=f['name']; s=f['size'];start=f['rom_offset']
        if n in seen or not 8<=s<100 or s%4 or start%4 or f['compiler_quirk_outcome']!='NO_NEW_COMPILER_FINDING':
            raise ValueError('Duplicate/nonshort/unclassified JP candidate '+n)
        m=re.fullmatch(r'func_([0-9A-Fa-f]+)_([0-9A-Fa-f]+)',n)
        if m is None or (int(m[1],16),int(m[2],16))!=(f['vma'],start):
            raise ValueError('Original VMA/ROM function name drift '+n)
        src=PACKAGE/f['source']
        if not src.is_file() or sha(src.read_bytes())!=f['source_sha256'] or sha((PACKAGE/f['negative_source']).read_bytes())!=f['negative_sha256']:
            raise ValueError('Native-tested C source not authentic '+n)
        seen.add(n); ranges.append((start,start+s))
    if any(a[1]>b[0] for a,b in zip(sorted(ranges),sorted(ranges)[1:])):
        raise ValueError('Overlapping original C candidates')
    return sorted(functions,key=lambda x:x['rom_offset'])

def original(checkout):
    rom=(checkout/'config/japan_0/baserom.decompressed.z64').read_bytes()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=ROM_SHA:raise ValueError('Original expanded JP ROM not authenticated')
    for f in rows():
        start=f['rom_offset']
        if sha(rom[start:start+f['size']])!=f['original_code_sha256']:
            raise ValueError('Original function bytes mismatch '+f['name'])
    return rom

def plan(checkout):
    checkout=Path(checkout);rom=original(checkout)
    if (checkout/'build/japan_0/mnsg.z64').read_bytes()!=rom:
        raise ValueError('Canonical JP2370 prior ROM is not exact')
    prior=checkout/'build/japan_0/mnsg.elf'
    if len(cr.c_identities(prior))!=BASE_C or not (checkout/'build/japan_0/jpcright-stage.json').is_file():
        raise ValueError('Current prior JP2370 accepted C source/ELF not independently staged')
    ldpath=checkout/'.splat/japan_0/mnsg.ld';ld=ldpath.read_text()
    allrows=rows(); targets={r['name'] for r in allrows}
    maps,cache=jp55.parse_owner(checkout,ld,targets)
    if set(maps)!=targets:
        raise ValueError('Previously accepted or missing active ASM owners: '+repr(sorted(targets-set(maps))))
    grouped={};planned=[]
    for f in allrows:
        own,m=maps[f['name']]
        if int(m['size'],16)!=f['size'] or jp55.word_span(cache[own][0][m.start():m.end()])!=(f['rom_offset'],f['rom_offset']+f['size']):
            raise ValueError('Original ASM extent/size drift '+f['name'])
        grouped.setdefault(own,[]).append(f)
        planned.append({'name':f['name'],'owner':own,'rom_offset':f['rom_offset'],'size':f['size']})
    return {'checkout':checkout,'rom':rom,'ld':ld,'ldpath':ldpath,'maps':maps,'cache':cache,'grouped':grouped,'entries':planned}

def stage(checkout):
    x=plan(checkout); co=x['checkout']; root=co/'src/jpshort28'
    if root.exists() or (co/STAGE).exists():raise ValueError('Already staged or collision')
    ld=x['ld']; inputs=[]; entries=[]; asmfrags=[]
    for owner, targetrows in sorted(x['grouped'].items()):
        targetrows.sort(key=lambda r:r['rom_offset'])
        raw,matches=x['cache'][owner]
        oldobj=co/f'build/japan_0/{owner}.o'
        glitch.check_nontext(oldobj)
        _,objlen,code,align=jp329.text_section(oldobj)
        first=jp55.word_span(raw[matches[0].start():matches[0].end()])[0]
        last=jp55.word_span(raw[matches[-1].start():matches[-1].end()])[1]
        ending=first+objlen
        if ending<last:raise ValueError('ASM last function beyond original ELF text extent '+owner)
        if ending!=last:
            tail=raw[matches[-1].end():]
            if jp55.word_span(tail)!=(last,ending) or x['rom'][last:ending]!=bytes(ending-last) or code[-(ending-last):]!=bytes(ending-last):
                raise ValueError('Unexpected original trailing text/padding '+owner)
        current=first;cursor=matches[0].start();header=raw[:cursor]; byname={m['name']:m for m in matches}
        parts=[]
        for idx,rec in enumerate(targetrows):
            m=byname[rec['name']];start=rec['rom_offset'];end=start+rec['size']
            if start<current or m.start()<cursor:raise ValueError('Original owner span overlap')
            if start>current:
                frag=raw[cursor:m.start()]
                if jp55.word_span(frag)!=(current,start):raise ValueError('Unexplained ASM gap '+rec['name'])
                path=f'asm/japan_0/jpshort28_{Path(owner).stem}_{idx:02}.s'
                parts.append(('asm',path,header+frag,current,start))
            else:
                between=raw[cursor:m.start()]
                if re.search(r'/\* [0-9A-Fa-f]{5,8} [0-9A-Fa-f]{8} [0-9A-Fa-f]{8} \*/',between):
                    raise ValueError('Unowned original MIPS instruction before '+rec['name'])
            path=f'src/jpshort28/{rec["name"]}.c'
            parts.append(('c',path,(PACKAGE/rec['source']).read_bytes(),start,end))
            entries.append({'name':rec['name'],'rom_offset':start,'vma':rec['vma'],'size':rec['size'],'source':path,'source_sha256':rec['source_sha256'],'original_code_sha256':rec['original_code_sha256'],'owner':owner,'relocations':rec['native_relocation_count']})
            current=end;cursor=m.end()
        if current<ending:
            frag=raw[cursor:]
            if jp55.word_span(frag)!=(current,ending):raise ValueError('Unowned tail ASM '+owner)
            path=f'asm/japan_0/jpshort28_{Path(owner).stem}_tail.s'
            parts.append(('asm',path,header+frag,current,ending))
        prefix=f'build/japan_0/{owner}.o'
        needle=prefix+'(.text);'
        if ld.count(needle)!=1:raise ValueError('Active original ASM object not unique '+owner)
        replacement='\n'.join('        build/japan_0/'+p+'.o(.text);' for kind,p,_,_,_ in parts)
        ld=ld.replace(needle,replacement,1)
        for sect in ('.data','.rodata','.bss','.sdata','.sbss'):
            k=prefix+f'({sect});'
            if ld.count(k)>1:raise ValueError('Non-text owner double linked '+owner)
            ld=ld.replace(k,'')
        if prefix+'(' in ld:raise ValueError('Unexpected ASM owner sections after split '+owner)
        inputs+=parts
    if len(entries)!=28 or sum(e['size'] for e in entries)!=1980:raise ValueError('Could not stage entire 28 batch')
    for kind,path,data,first,last in inputs:
        dest=co/path
        if dest.exists():raise ValueError('Refuse staging collision '+path)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data if isinstance(data,bytes) else data.encode())
        if kind=='asm':asmfrags.append({'path':path,'start':first,'end':last})
    x['ldpath'].write_text(ld)
    rec={'format':'goemon-jp-short28-current-2370-stage-v1','baseline_c':BASE_C,'baseline_bytes':BASE_BYTES,'added_c':28,'added_bytes':1980,'original_rom_sha1':ROM_SHA,'functions':entries,'assembly':asmfrags,'accepted_reloc_count':BASE_RELOCS,'accepted_reloc_sha256':BASE_RELOC_HASH}
    (co/STAGE).write_text(json.dumps(rec,indent=2)+'\n')
    return {'staged':len(entries),'asm_fragments':len(asmfrags),'owners':len(x['grouped'])}

def build(checkout,deps,runtime):
    checkout=Path(checkout);report=json.loads((checkout/STAGE).read_text());rom=original(checkout)
    pre=json.loads((checkout/'build/japan_0/glitch-g2-stage.json').read_text())
    vm=json.loads((checkout/'build/japan_0/vm-g2-stage.json').read_text())
    jp55_stage=json.loads((checkout/'build/japan_0/jp55-stage.json').read_text())
    cright=json.loads((checkout/'build/japan_0/jpcright-stage.json').read_text())
    if len(jp55_stage['functions'])!=55 or cright['name']!=cr.TARGET:raise ValueError('Wrong latest accepted JP stages')
    sources=[r['source'] for r in pre['new_functions']+vm['functions']+jp55_stage['functions']+report['functions']]+[cright['source']]
    args=glitch.makeargs(checkout,'japan_0',{'new_functions':[{'source':s} for s in sources]})
    targets=['build/japan_0/'+r['source']+'.o' for r in report['functions']]
    targets+=['build/japan_0/'+r['path']+'.o' for r in report['assembly']]
    env=jp329.env_for(Path(deps).resolve(),Path(runtime).resolve())
    subprocess.run(args+targets,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    fixes=[]
    for c in report['functions']:
        path=c['source'];expected=c['size'];start=c['rom_offset']
        if sha((checkout/path).read_bytes())!=c['source_sha256']:raise ValueError('Source changed before MIPS native compile')
        obj=checkout/f'build/japan_0/{path}.o'
        _,size,code,align=jp329.text_section(obj)
        if size<expected or size>(expected+15)&~15 or any(code[expected:]):raise ValueError('Original C extent/zero padding mismatch '+path)
        if size!=expected or align!=4:
            obj.write_bytes(jp34.pack_text_metadata(obj.read_bytes(),expected)[0]);fixes.append(path)
        _,newsize,_,newalign=jp329.text_section(obj)
        if (newsize,newalign)!=(expected,4):raise ValueError('Failed strict C section metadata '+path)
        if start%4:raise ValueError('Original C VMA/ROM unaligned')
    for c in report['assembly']:
        path=c['path'];expected=c['end']-c['start']
        obj=checkout/f'build/japan_0/{path}.o';_,size,code,align=jp329.text_section(obj)
        if size<expected or size>(expected+15)&~15 or any(code[expected:]):raise ValueError('Original ASM fragment extent/padding drift '+path)
        if size!=expected or align!=4:
            obj.write_bytes(jp34.pack_text_metadata(obj.read_bytes(),expected)[0]);fixes.append(path)
        _,newsize,_,newalign=jp329.text_section(obj)
        if (newsize,newalign)!=(expected,4):raise ValueError('Failed ASM section metadata '+path)
    for f in ('mnsg.elf','mnsg.z64'):
        p=checkout/'build/japan_0'/f
        if p.exists():p.unlink()
    subprocess.run(args+['build/japan_0/mnsg.z64'],cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    actual=(checkout/'build/japan_0/mnsg.z64').read_bytes()
    diff=next((i for i,(a,b) in enumerate(zip(actual,rom)) if a!=b),None)
    result={'result':'FULL_ROM_EXACT' if actual==rom else 'FAILED_ROM','expected_sha1':ROM_SHA,'actual_sha1':hashlib.sha1(actual).hexdigest(),'size':len(actual),'first_mismatch':diff,'metadata_only_pad_corrections':fixes}
    (checkout/'build/japan_0/jpshort28-build.json').write_text(json.dumps(result,indent=2)+'\n')
    if actual!=rom:raise ValueError('FAILED_ROM: first mismatch '+str(diff))
    return result

def verify(checkout,base):
    co=Path(checkout);base=Path(base);rom=original(co);stage=json.loads((co/STAGE).read_text())
    if (co/'build/japan_0/mnsg.z64').read_bytes()!=rom or (base/'build/japan_0/mnsg.z64').read_bytes()!=rom:
        raise ValueError('Complete Japanese ROM differs')
    old=base/'build/japan_0/mnsg.elf';new=co/'build/japan_0/mnsg.elf'
    a=cross._funcs(old);b=cross._funcs(new)
    if a!=b or sum(a.values())!=7376:raise ValueError('One of 7,376 original ELF FUNC identities differs')
    r0,n0,h0=glitch.all_semantic_relocations(old)
    r1,n1,h1=glitch.all_semantic_relocations(new)
    if n0!=BASE_RELOCS or n1!=BASE_RELOCS or h0!=BASE_RELOC_HASH or h1!=h0 or r0!=r1:
        raise ValueError('Original JP canonical semantic relocation multiset differs: old/new '+str((n0,n1,h0,h1))+' removed '+repr(list((r0-r1).items())[:5])+' added '+repr(list((r1-r0).items())[:5]))
    c0=cr.c_identities(old);c1=cr.c_identities(new)
    expected={e['name'] for e in stage['functions']}
    if len(c0)!=BASE_C or len(c1)!=BASE_C+28 or c1-c0!=expected or c0-c1:
        raise ValueError('Canonical accepted C identities overlap/missing: '+str((len(c0),len(c1),sorted(c1-c0)[:5])))
    textmap=(co/'build/japan_0/mnsg.map').read_text()
    for e in stage['functions']:
        if e['name']+'.NON_MATCHING' in textmap or f'build/japan_0/{e["source"]}.o' not in textmap:
            raise ValueError('C source/original address not proven in link map '+e['name'])
        off=e['rom_offset'];n=e['size']
        if sha(rom[off:off+n])!=e['original_code_sha256']:
            raise ValueError('Original ROM function hash mismatch at promotion '+e['name'])
    result={'status':'PASSED_G2_LOCAL','region':'japan_0','before_C':BASE_C,'after_C':len(c1),'added_C':28,'added_bytes':1980,'original_bytes_after':BASE_BYTES+1980,'asm_remaining':7376-len(c1),'rom_bytes':33554432,'rom_sha1':ROM_SHA,'elf_identities_exact':7376,'semantic_relocations_exact':BASE_RELOCS,'semantic_relocations_sha256':h1,'new_C_names':sorted(expected),'publication':'NOT_YET'}
    (co/'build/japan_0/jpshort28-G2.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['plan','stage','build','verify'])
    p.add_argument('--checkout',type=Path,required=True)
    p.add_argument('--deps',type=Path)
    p.add_argument('--runtime',type=Path)
    p.add_argument('--base',type=Path)
    a=p.parse_args()
    if a.action=='plan':
        x=plan(a.checkout);result={'replaceable':len(x['entries']),'owners':len(x['grouped'])}
    elif a.action=='stage':result=stage(a.checkout)
    elif a.action=='build':result=build(a.checkout,a.deps,a.runtime)
    else:result=verify(a.checkout,a.base)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
