"""Japanese 30 original-region native C source-unit promotion: fail-closed original-ROM G2.

This stages only canonical ASM-owned functions. It never modifies machine code,
ROM bytes, assembler relocations or accepted C. Full original Japanese ROM,
ELF function identity and complete semantic relocation equality are required.
"""
from __future__ import annotations
import hashlib, json, re, subprocess, struct
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
PACKAGE=ROOT/'research/crossregion_native34_full_20261123'
MANIFEST=PACKAGE/'manifest.json'
MANIFEST_SHA='acae8d60db1d069c00d4e1a917210ffb1f16a6ce2a4c85a98f5c77017cd347ac'
STAGE=Path('build/japan_0/jpcross34-stage.json')
ROM_SHA='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
BASE_C=2398
BASE_BYTES=128988
BASE_RELOCS=80745
BASE_RELOC_HASH=crdual.NORMALIZED_HASH
RETAIN_ASM_ABS_RELOCS={'osAiGetLength','__osSpGetStatus','__osSpSetStatus'}
CANONICAL_VARIANTS={'func_801D9074_603AF4': '840a5231a6cd6ed93e03b987eea9f41b26884f52c89f36b0839c536791faf48b', 'func_802125D8_67BCC8': 'dc449b78560ffc217d804510ead18d8ced0d8b2fc337f9cded7aca35a5559054', 'func_802014A0_5BD470': 'db20c0375408bb34f4baf789582683c90404b2adfe880d6c9133d2f092941975', 'func_802014D0_5BD4A0': '51a53fbeda2ef2a822786cbcd3b646987758a158205b4ba41278d3fb3229c3d4', 'osAiGetLength': '109f2db2e9c495c826c3d4bf8b8135b602821ca527a23433a7363b4a831e047d', '__osSpGetStatus': '2c1edf05f4e780dfa94824715489b8e5e9b1c43728b1c65c786258a3f1f0c231', '__osSpSetStatus': 'b6ce632fce18a27ae88f37ed93356e5a565537c15ccce66775ad6354a2c525f4'}

def sha(data):return hashlib.sha256(data).hexdigest()

def preserve_original_abs_notyp_symbol(path,name):
    """Restore original ABS NOTYPE, one ELF st_info byte only; never patch code/relocs.

    Reproduces the *existing* independently proven USA file18 IDO OBJECT vs
    original NOTYPE linker-symbol quirk in the Japanese source units.
    """
    path=Path(path);before=path.read_bytes();buf=bytearray(before)
    sec=usa_abs.elf_sections(before)
    if not {'.symtab','.strtab','.text','.rel.text'}<=set(sec):raise ValueError('Cannot inspect native C object for original symbol type')
    tab=sec['.symtab'];strings=sec['.strtab']
    if tab['entsize']!=16 or tab['size']%16:raise ValueError('Unexpected SGI IDO ELF symtab')
    found=[]
    for i in range(tab['size']//16):
        at=tab['offset']+16*i
        offset=struct.unpack_from('>I',buf,at)[0]
        start=strings['offset']+offset
        curr=buf[start:buf.index(0,start)].decode('ascii')
        if curr!=name:continue
        info=buf[at+12]
        if info not in (0x10,0x11) or (struct.unpack_from('>II',buf,at+4))!=(0,0) or struct.unpack_from('>H',buf,at+14)[0]!=0:
            raise ValueError('Unexpected original ABS/undefined C symbol type '+name)
        found.append((at+12,info))
    if len(found)!=1:raise ValueError('Missing/multiple original ABS symbol '+name)
    at,info=found[0]
    if info==0x11:buf[at]=0x10
    differences=[i for i,(a,b) in enumerate(zip(before,buf)) if a!=b]
    if len(differences)!=(1 if info==0x11 else 0) or (differences and differences[0]!=at):raise ValueError('More than one prohibited ELF metadata edit')
    for part in ('.text','.rel.text'):
        entry=sec[part];i=entry['offset'];j=i+entry['size']
        if before[i:j]!=buf[i:j]:raise ValueError('Native code/reloc patch forbidden')
    path.write_bytes(buf)
    return {'symbol':name,'source_undefined_Stt_OBJECT':info==0x11,'original_undefined_Stt_NOTYPE':True,'st_info_bytes_changed':len(differences),'original_code_and_relocations_unchanged':True,'source_object_sha256':sha(before),'original_provenance_object_sha256':sha(buf),'compiler_outcome':'EXISTING_QUIRK_REPRODUCED'}

def rows():
    if sha(MANIFEST.read_bytes()) != MANIFEST_SHA:
        raise ValueError('Crossregion34 pinned source manifest changed')
    obj=json.loads(MANIFEST.read_text())
    if (obj.get('function_count')!=34 or obj.get('canonical_base_sha')!='838e9f87c3a860973e9d168b58fcf88bd456bfb4'
            or obj.get('status')!='RESEARCH_ONLY_ISOLATED_NATIVE_34_POSITIVE_AND_NEGATIVE'):
        raise ValueError('Unrecognized native34 research provenance')
    out=[]; seen=set(); ranges=[]
    for f in obj['functions']:
        if f['region']!='japan_0' or f['name'] in RETAIN_ASM_ABS_RELOCS:continue
        n=f['name']; start=int(f['original_rom_offset'],16);size=f['original_instruction_bytes'];vma=int(f['original_vma'],16)
        if n in seen or start%4 or size%4 or not 8<=size<=100 or f['compiler_quirk_outcome']!='NO_NEW_COMPILER_FINDING' or f['native_original_repro'] not in ('ISOLATED_COMPILER_CODE_EXACT','ISOLATED_LINKED_EXACT'):
            raise ValueError('Unverified native record '+n)
        m=re.fullmatch(r'func_([A-Fa-f0-9]+)_([A-Fa-f0-9]+)',n)
        if m and (int(m[1],16),int(m[2],16))!=(vma,start):raise ValueError('Named original offset mismatch '+n)
        source=PACKAGE/f['candidate_source_path']; neg=PACKAGE/f['negative_source_path']
        if not source.is_file() or sha(source.read_bytes())!=f['candidate_source_sha256'] or not neg.is_file() or sha(neg.read_bytes())!=f['negative_source_sha256']:
            raise ValueError('Native-tested C source/negative control changed '+n)
        out.append(dict(name=n,rom_offset=start,vma=vma,size=size,source=f['candidate_source_path'],source_sha256=f['candidate_source_sha256'],original_code_sha256=f['original_code_sha256'],native_relocation_count=0,compiler_quirk_outcome=f['compiler_quirk_outcome']))
        seen.add(n);ranges.append((start,start+size))
    if len(out)!=30 or sum(x['size'] for x in out)!=1280 or len(seen)!=30 or any(a[1]>b[0] for a,b in zip(sorted(ranges),sorted(ranges)[1:])):
        raise ValueError('JP33 research count or overlap mismatch')
    return sorted(out,key=lambda x:x['rom_offset'])

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
        raise ValueError('Canonical JP2398 prior ROM is not exact')
    prior=checkout/'build/japan_0/mnsg.elf'
    if len(cr.c_identities(prior))!=BASE_C or not (checkout/'build/japan_0/jp-short28-stage.json').is_file():
        raise ValueError('Current prior JP2398 accepted C source/ELF not independently staged')
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
    x=plan(checkout); co=x['checkout']; root=co/'src/jpcross34'
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
                path=f'asm/japan_0/jpcross34_{Path(owner).stem}_{idx:02}.s'
                parts.append(('asm',path,header+frag,current,start))
            else:
                between=raw[cursor:m.start()]
                if re.search(r'/\* [0-9A-Fa-f]{5,8} [0-9A-Fa-f]{8} [0-9A-Fa-f]{8} \*/',between):
                    raise ValueError('Unowned original MIPS instruction before '+rec['name'])
            path=f'src/jpcross34/{rec["name"]}.c'
            content=(PACKAGE/rec['source']).read_bytes()
            candidate_variant=CANONICAL_VARIANTS.get(rec['name'])
            if candidate_variant:
                content=(PACKAGE/f'canonical_variants/{rec["name"]}.c').read_bytes()
                if sha(content)!=candidate_variant: raise ValueError('Native-tested canonical linkage source changed '+rec['name'])
            parts.append(('c',path,content,start,end))
            ent={'name':rec['name'],'rom_offset':start,'vma':rec['vma'],'size':rec['size'],'source':path,'source_sha256':sha(content),'source_research_sha256':rec['source_sha256'],'original_code_sha256':rec['original_code_sha256'],'owner':owner,'relocations':None}
            if candidate_variant:ent['canonical_variant_source']=f'canonical_variants/{rec["name"]}.c'
            entries.append(ent)
            current=end;cursor=m.end()
        if current<ending:
            frag=raw[cursor:]
            if jp55.word_span(frag)!=(current,ending):raise ValueError('Unowned tail ASM '+owner)
            path=f'asm/japan_0/jpcross34_{Path(owner).stem}_tail.s'
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
    if len(entries)!=30 or sum(e['size'] for e in entries)!=1280:raise ValueError('Could not stage entire 30 native-exact relocation-supported targets')
    for kind,path,data,first,last in inputs:
        dest=co/path
        if dest.exists():raise ValueError('Refuse staging collision '+path)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data if isinstance(data,bytes) else data.encode())
        if kind=='asm':asmfrags.append({'path':path,'start':first,'end':last})
    x['ldpath'].write_text(ld)
    rec={'format':'goemon-jp-crossregion30-after2398-stage-v1','baseline_c':BASE_C,'baseline_bytes':BASE_BYTES,'added_c':30,'added_bytes':1280,'original_rom_sha1':ROM_SHA,'functions':entries,'assembly':asmfrags,'accepted_reloc_count':BASE_RELOCS,'accepted_reloc_sha256':BASE_RELOC_HASH,'retained_asm_native_relocation_blockers':[{'name':f['name'],'rom_offset':int(f['original_rom_offset'],16),'size':f['original_instruction_bytes'],'reason':'native-original-ID0 instruction exact but either missing original ABS symbol relocations or extra ADDIU when correct symbol used'} for f in json.loads(MANIFEST.read_text())['functions'] if f['region']=='japan_0' and f['name'] in RETAIN_ASM_ABS_RELOCS]}
    (co/STAGE).write_text(json.dumps(rec,indent=2)+'\n')
    return {'staged':len(entries),'asm_fragments':len(asmfrags),'owners':len(x['grouped'])}

def build(checkout,deps,runtime):
    checkout=Path(checkout);report=json.loads((checkout/STAGE).read_text());rom=original(checkout)
    pre=json.loads((checkout/'build/japan_0/glitch-g2-stage.json').read_text())
    vm=json.loads((checkout/'build/japan_0/vm-g2-stage.json').read_text())
    jp55_stage=json.loads((checkout/'build/japan_0/jp55-stage.json').read_text())
    cright=json.loads((checkout/'build/japan_0/jpcright-stage.json').read_text())
    jp28stage=json.loads((checkout/'build/japan_0/jp-short28-stage.json').read_text())
    if len(jp55_stage['functions'])!=55 or len(jp28stage['functions'])!=28 or cright['name']!=cr.TARGET:raise ValueError('Wrong latest accepted JP stages')
    sources=[r['source'] for r in pre['new_functions']+vm['functions']+jp55_stage['functions']+jp28stage['functions']+report['functions']]+[cright['source']]
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
    # Same original linker-symbol metadata-only fix as the verified USA file18
    # D_CF8F8 IDO 5.3 quirk; three JP sources affected. Check exact STT_OBJECT
    # state and preserve all original .text and .rel.text bytes.
    abs_fixes=[]
    for name,symbol in [('func_802014A0_5BD470','D_CF8F0'),('func_802014D0_5BD4A0','D_CF8F0'),('func_802125D8_67BCC8','D_CF8F8')]:
        obj=checkout/f'build/japan_0/src/jpcross34/{name}.c.o'
        abs_fixes.append({'function':name,**preserve_original_abs_notyp_symbol(obj,symbol)})
    (checkout/'build/japan_0/jpcross34-absolute-global-identity.json').write_text(json.dumps(abs_fixes,indent=2)+'\n')
    for f in ('mnsg.elf','mnsg.z64'):
        p=checkout/'build/japan_0'/f
        if p.exists():p.unlink()
    subprocess.run(args+['build/japan_0/mnsg.z64'],cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    actual=(checkout/'build/japan_0/mnsg.z64').read_bytes()
    diff=next((i for i,(a,b) in enumerate(zip(actual,rom)) if a!=b),None)
    result={'result':'FULL_ROM_EXACT' if actual==rom else 'FAILED_ROM','expected_sha1':ROM_SHA,'actual_sha1':hashlib.sha1(actual).hexdigest(),'size':len(actual),'first_mismatch':diff,'metadata_only_pad_corrections':fixes,'original_ABS_symbol_type_corrections':abs_fixes}
    (checkout/'build/japan_0/jpcross34-build.json').write_text(json.dumps(result,indent=2)+'\n')
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
    globals_before=usa_abs.stable_globals(old)
    globals_after=usa_abs.stable_globals(new)
    if globals_before!=globals_after:
        raise ValueError('Original 26,393 stable global symbol name/address/type identities differ: removed '+repr(list((globals_before-globals_after).items())[:4])+' added '+repr(list((globals_after-globals_before).items())[:4]))
    if sum(globals_before.values())!=26393:raise ValueError('Original regional stable-global baseline changed')
    c0=cr.c_identities(old);c1=cr.c_identities(new)
    expected={e['name'] for e in stage['functions']}
    if len(c0)!=BASE_C or len(c1)!=BASE_C+30 or c1-c0!=expected or c0-c1:
        raise ValueError('Canonical accepted C identities overlap/missing: '+str((len(c0),len(c1),sorted(c1-c0)[:5])))
    textmap=(co/'build/japan_0/mnsg.map').read_text()
    for e in stage['functions']:
        if e['name']+'.NON_MATCHING' in textmap or f'build/japan_0/{e["source"]}.o' not in textmap:
            raise ValueError('C source/original address not proven in link map '+e['name'])
        off=e['rom_offset'];n=e['size']
        if sha(rom[off:off+n])!=e['original_code_sha256']:
            raise ValueError('Original ROM function hash mismatch at promotion '+e['name'])
    result={'status':'PASSED_G2_LOCAL','region':'japan_0','before_C':BASE_C,'after_C':len(c1),'added_C':30,'added_bytes':1280,'original_bytes_after':BASE_BYTES+1280,'asm_remaining':7376-len(c1),'rom_bytes':33554432,'rom_sha1':ROM_SHA,'elf_identities_exact':7376,'semantic_relocations_exact':BASE_RELOCS,'semantic_relocations_sha256':h1,'stable_global_symbol_identities_exact':26393,'new_C_names':sorted(expected),'publication':'NOT_YET'}
    (co/'build/japan_0/jpcross34-G2.json').write_text(json.dumps(result,indent=2)+'\n')
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
