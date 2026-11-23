"""Strict Japan-0 C-Right followup stage from the canonical JP2428 predecessor.
All original code/relocations and full ELF identities are checked independently.
Only private generated source/objects are edited; original ROM is read-only.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from . import japan_jp55_promotion as jp55
from . import japan_cright_promotion as cr
from . import japan_cright_dual_reference as crdual
from . import japan_noop_port as jp329
from . import japan_thirtyfour_c as jp34
from . import glitch_g2_promotion as glitch
from . import overlay_crossregion47 as cross
from . import usa_opening_new2_promotion as usa_abs
ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT/'research/jp_cright_followup_20261123'
MANIFEST=PACKAGE/'manifest.json'
MANIFEST_SHA='e9eb880a9f86c97287c7da9b4451d2c6e75f820810ea6be7925096fb1aa0c699'
STAGE=Path('build/japan_0/jp-cright-followup-stage.json')
ROM_SHA='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
BASE_C=2428
BASE_BYTES=130268
BASE_RELOCS=80745
BASE_RELOC_HASH=crdual.NORMALIZED_HASH

def sha(data):return hashlib.sha256(data).hexdigest()

def rows():
    if sha(MANIFEST.read_bytes())!=MANIFEST_SHA:raise ValueError('Pinned native-source manifest changed')
    data=json.loads(MANIFEST.read_text())
    if data['region']!='japan_0' or data['rom_sha1']!=ROM_SHA or data['canonical_parent']!='78e6303e2fe5f4e5f5a17bab50cb62fc792d241b':raise ValueError('Wrong original JP manifest provenance')
    out=[f for f in data['functions'] if f['eligible_for_strict_stage']]
    if len(out)!=4 or sum(f['size'] for f in out)!=316 or len({f['name'] for f in out})!=4:raise ValueError('Invalid target extents')
    for f in out:
        if f['native_relocation_count']!=f['original_raw_relocation_count'] or not f['isolated_linked_exact']:raise ValueError('Unproven native/relocation candidate')
        if sha((PACKAGE/f['source']).read_bytes())!=f['source_sha256'] or sha((PACKAGE/f['negative_source']).read_bytes())!=f['negative_sha256']:raise ValueError('Source or negative control drift')
        m=re.fullmatch(r'func_([0-9A-Fa-f]+)_([0-9A-Fa-f]+)',f['name'])
        if not m or (int(m[1],16),int(m[2],16))!=(f['vma'],f['rom_offset']):raise ValueError('Original function name/extent drift')
    return sorted(out,key=lambda x:x['rom_offset'])

def original(checkout):
    rom=(checkout/'config/japan_0/baserom.decompressed.z64').read_bytes()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=ROM_SHA:raise ValueError('Original expanded JP ROM not authenticated')
    for f in rows():
        start=f['rom_offset']
        if sha(rom[start:start+f['size']])!=f['original_code_sha256']:raise ValueError('Original function bytes mismatch '+f['name'])
    return rom

def plan(checkout):
    checkout=Path(checkout);rom=original(checkout)
    if (checkout/'build/japan_0/mnsg.z64').read_bytes()!=rom:
        raise ValueError('Canonical JP2428 prior ROM is not exact')
    prior=checkout/'build/japan_0/mnsg.elf'
    if len(cr.c_identities(prior))!=BASE_C or not (checkout/'build/japan_0/jpcross34-stage.json').is_file():
        raise ValueError('Current prior JP2428 accepted C source/ELF not independently staged')
    rel,n,h=glitch.all_semantic_relocations(prior)
    if n!=BASE_RELOCS or h!=BASE_RELOC_HASH or sum(cross._funcs(prior).values())!=7376 or sum(usa_abs.stable_globals(prior).values())!=26393:raise ValueError('JP2428 predecessor ELF/relocation/global proof drift')
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
    x=plan(checkout); co=x['checkout']; root=co/'src/jpcrightfollowup'
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
                path=f'asm/japan_0/jpcrightfollowup_{Path(owner).stem}_{idx:02}.s'
                parts.append(('asm',path,header+frag,current,start))
            else:
                between=raw[cursor:m.start()]
                if re.search(r'/\* [0-9A-Fa-f]{5,8} [0-9A-Fa-f]{8} [0-9A-Fa-f]{8} \*/',between):
                    raise ValueError('Unowned original MIPS instruction before '+rec['name'])
            path=f'src/jpcrightfollowup/{rec["name"]}.c'
            parts.append(('c',path,(PACKAGE/rec['source']).read_bytes(),start,end))
            entries.append({'name':rec['name'],'rom_offset':start,'vma':rec['vma'],'size':rec['size'],'source':path,'source_sha256':rec['source_sha256'],'original_code_sha256':rec['original_code_sha256'],'owner':owner,'relocations':rec['native_relocation_count']})
            current=end;cursor=m.end()
        if current<ending:
            frag=raw[cursor:]
            if jp55.word_span(frag)!=(current,ending):raise ValueError('Unowned tail ASM '+owner)
            path=f'asm/japan_0/jpcrightfollowup_{Path(owner).stem}_tail.s'
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
    if len(entries)!=4 or sum(e['size'] for e in entries)!=316:raise ValueError('Could not stage entire four batch')
    for kind,path,data,first,last in inputs:
        dest=co/path
        if dest.exists():raise ValueError('Refuse staging collision '+path)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data if isinstance(data,bytes) else data.encode())
        if kind=='asm':asmfrags.append({'path':path,'start':first,'end':last})
    x['ldpath'].write_text(ld)
    rec={'format':'goemon-jp-cright-followup-current-2428-stage-v1','baseline_c':BASE_C,'baseline_bytes':BASE_BYTES,'added_c':4,'added_bytes':316,'original_rom_sha1':ROM_SHA,'functions':entries,'assembly':asmfrags,'accepted_reloc_count':BASE_RELOCS,'accepted_reloc_sha256':BASE_RELOC_HASH}
    (co/STAGE).write_text(json.dumps(rec,indent=2)+'\n')
    return {'staged':len(entries),'asm_fragments':len(asmfrags),'owners':len(x['grouped'])}

def build(checkout,deps,runtime):
    checkout=Path(checkout);report=json.loads((checkout/STAGE).read_text());rom=original(checkout)
    if sha((checkout/'tools/ido-5.3/cc').read_bytes())!=json.loads(MANIFEST.read_text())['compiler_sha256']:raise ValueError('Wrong native IDO compiler')
    env=jp329.env_for(Path(deps).resolve(),Path(runtime).resolve())
    paths=[(f['source'],f['size']) for f in report['functions']]+[(f['path'],f['end']-f['start']) for f in report['assembly']]
    for f in report['functions']:
        if sha((checkout/f['source']).read_bytes())!=f['source_sha256']:raise ValueError('Native source changed before compile')
    targets=['build/japan_0/'+p+'.o' for p,_ in paths]
    subprocess.run(['make','-j4','VERSION=japan_0']+targets,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    fixes=[]
    for path,expected in paths:
        obj=checkout/f'build/japan_0/{path}.o';_,size,code,align=jp329.text_section(obj)
        if size<expected or size>((expected+15)&~15) or any(code[expected:]):raise ValueError('Original section extent/padding drift '+path)
        if size!=expected or align!=4:
            obj.write_bytes(jp34.pack_text_metadata(obj.read_bytes(),expected)[0]);fixes.append(path)
        _,newsize,_,newalign=jp329.text_section(obj)
        if (newsize,newalign)!=(expected,4):raise ValueError('Failed strict section metadata '+path)
    for f in report['functions']:
        obj=checkout/f'build/japan_0/{f["source"]}.o'
        syms=subprocess.check_output(['readelf','-Ws',str(obj)],text=True,env=env)
        found=[int(x.split()[2]) for x in syms.splitlines() if len(x.split())>=8 and x.split()[3]=='FUNC' and x.split()[7]==f['name'] and x.split()[6]!='UND']
        if found!=[f['size']]:raise ValueError('Original native FUNC size mismatch '+f['name'])
    subprocess.run(['mips-linux-gnu-ld','-T','.splat/japan_0/mnsg.ld','-Map','build/japan_0/mnsg.map','-T','.splat/japan_0/undefined_syms_auto.ld','-T','.splat/japan_0/undefined_funcs_auto.ld','--no-check-sections','--emit-relocs','-o','build/japan_0/mnsg.elf'],cwd=checkout,env=env,check=True)
    subprocess.run(['mips-linux-gnu-objcopy','-O','binary','--pad-to=0x2000000','--gap-fill=0x00','build/japan_0/mnsg.elf','build/japan_0/mnsg.z64'],cwd=checkout,env=env,check=True)
    actual=(checkout/'build/japan_0/mnsg.z64').read_bytes()
    if actual!=rom:raise ValueError('FAILED_ROM: first mismatch '+str(next((i for i,(a,b) in enumerate(zip(actual,rom)) if a!=b),None)))
    return {'status':'FULL_ROM_EXACT','sha1':ROM_SHA,'bytes':len(rom),'metadata_only_section_corrections':fixes}

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
    g0=usa_abs.stable_globals(old);g1=usa_abs.stable_globals(new)
    if g0!=g1 or sum(g0.values())!=26393:raise ValueError('Stable global symbol identity mismatch: '+repr(list((g0-g1).items())[:8])+' added '+repr(list((g1-g0).items())[:8]))
    c0=cr.c_identities(old);c1=cr.c_identities(new)
    expected={e['name'] for e in stage['functions']}
    if len(c0)!=BASE_C or len(c1)!=BASE_C+4 or c1-c0!=expected or c0-c1:
        raise ValueError('Canonical accepted C identities overlap/missing: '+str((len(c0),len(c1),sorted(c1-c0)[:5])))
    textmap=(co/'build/japan_0/mnsg.map').read_text()
    for e in stage['functions']:
        if e['name']+'.NON_MATCHING' in textmap or f'build/japan_0/{e["source"]}.o' not in textmap:
            raise ValueError('C source/original address not proven in link map '+e['name'])
        off=e['rom_offset'];n=e['size']
        if sha(rom[off:off+n])!=e['original_code_sha256']:
            raise ValueError('Original ROM function hash mismatch at promotion '+e['name'])
    result={'status':'PASSED_G2_LOCAL','region':'japan_0','before_C':BASE_C,'after_C':len(c1),'added_C':4,'added_bytes':316,'original_bytes_after':BASE_BYTES+316,'asm_remaining':7376-len(c1),'rom_bytes':33554432,'rom_sha1':ROM_SHA,'elf_identities_exact':7376,'semantic_relocations_exact':BASE_RELOCS,'semantic_relocations_sha256':h1,'stable_global_symbol_identities_exact':26393,'new_C_names':sorted(expected),'publication':'NOT_YET'}
    (co/'build/japan_0/jpcrightfollowup-G2.json').write_text(json.dumps(result,indent=2)+'\n')
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
