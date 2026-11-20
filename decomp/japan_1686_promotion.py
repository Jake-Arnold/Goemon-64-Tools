"""Fail-closed Japanese C-Right research batch staging and original-ROM validation.

Research-to-production integration. Never accepts isolated exactness alone.
Original ROM, toolchain and generated assembly remain outside the repository.
"""
from __future__ import annotations
import csv, hashlib, json, os, re, shutil, subprocess, sys
from collections import defaultdict
from pathlib import Path
from . import japan_noop_port as jp329
from . import japan_thirtynine_verify as jp39
from . import japan_usa_main_three as jp432
from .japan_thirtyfour_c import pack_text_metadata

HERE = Path(__file__).resolve().parent
BATCH = Path(os.environ.get('GOEMON_JP1688_BATCH', HERE / 'research/jp1686_promotion'))
STAGE = Path('build/japan_0/jp1686-stage.json')
OMIT = {'func_08001228_6B3168','func_080012AC_6B51AC'}
EXPECTED_SHA = '6f8745fecc3a5e7d4918c7a73353eb0726116ded'
EXPECTED_RELOC_COUNT = 80747
EXPECTED_ELF_FUNCS = 7376
EXPECTED_C = 432 + 1686

def digest(blob:bytes)->str:return hashlib.sha256(blob).hexdigest()

def candidates():
    with (BATCH/'candidates.csv').open(newline='') as stream: allrows=list(csv.DictReader(stream))
    if len(allrows)!=1688:raise ValueError('Wrong frozen input count')
    ret=[]
    for row in allrows:
        f=row['function']
        if f in OMIT:continue
        row['off']=int(row['rom_offset'],0)
        row['end']=row['off']+int(row['size_bytes'])
        row['vma']=int(row['guest_vma'],0)
        src=BATCH/row['source_file']
        if not src.is_file() or digest(src.read_bytes())!=row['source_sha256']:
            raise ValueError('Frozen source hash mismatch '+f)
        ret.append(row)
    if len(ret)!=1686 or len(set(x['off'] for x in ret))!=1686:raise ValueError('Duplicate or omitted candidate')
    return ret

def code_sources(rows):
    grouped=defaultdict(list)
    for row in rows:grouped[row['source_file']].append(row)
    for source,items in grouped.items():
        items.sort(key=lambda x:x['off'])
        if any(a['end']!=b['off'] for a,b in zip(items,items[1:])):raise ValueError('Non-contiguous compiled C unit '+source)
    if len(grouped)!=1663:raise ValueError(f'Wrong unique source count: {len(grouped)}')
    return grouped

def original(checkout):
    rom=(checkout/'config/japan_0/baserom.decompressed.z64').read_bytes()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=EXPECTED_SHA:raise ValueError('Incorrect Japanese expanded ROM')
    return rom

def parse_active(checkout, ldtext):
    owners=re.findall(r'(?m)^\s*build/japan_0/(asm/japan_0/[^\s()]+\.s)\.o\(\.text\);',ldtext)
    owners=list(dict.fromkeys(owners))
    maps={};used={}
    for path in owners:
        raw=(checkout/path).read_text()
        matches=list(jp329.BLOCK.finditer(raw))
        if not matches:continue
        names={m['name']:m for m in matches}
        for name in names:
            if name in maps:raise ValueError('Duplicate original ASM function name '+name)
            maps[name]=(path, names[name])
        used[path]=matches
    return maps,used

def preflight(checkout:Path,rom:bytes,rows:list[dict],maps:dict,allmatches:dict,ldtext:str):
    missing=[r['function'] for r in rows if r['function'] not in maps]
    if missing:raise ValueError(f'Missing {len(missing)} original active ASM functions: '+str(missing[:10]))
    groups=code_sources(rows)
    byowner=defaultdict(list)
    for source,items in groups.items():
        own={maps[r['function']][0] for r in items}
        if len(own)!=1:raise ValueError('One C unit crosses original ASM objects: '+source)
        owner=next(iter(own))
        byowner[owner].append((source,items))
    for owner,parts in byowner.items():
        text=(checkout/owner).read_text()
        matches=allmatches[owner]
        start=int(matches[0]['name'].rsplit('_',1)[1],16)
        obj=checkout/f'build/japan_0/{owner}.o'
        _o,size,code,align=jp329.text_section(obj)
        # ASM relocations are unresolved before final link; compare full linked ROM later.
        if size%4:raise ValueError('Original MIPS ASM extent not word aligned')
        cursor=start
        for m in matches:
            f=m['name'];off=int(f.rsplit('_',1)[1],16)
            if off<cursor:raise ValueError(f'Overlapping original ASM function {owner} at {f} after {cursor:x}')
            cursor=off+int(m['size'],16)
        if cursor>start+size:raise ValueError('Original ASM extends beyond section extent '+owner)
        for source,items in parts:
            for r in items:
                m=maps[r['function']][1]
                if int(m['size'],16)!=r['end']-r['off'] or digest(rom[r['off']:r['end']])!=r['original_code_sha256']:
                    raise ValueError('Original candidate extent/code anchor mismatch '+r['function'])
        needle=f'        build/japan_0/{owner}.o(.text);'
        if ldtext.count(needle)!=1:raise ValueError('ASM linked owner ambiguity '+owner)
    return groups,byowner

def stage(checkout:Path)->dict:
    rom=original(checkout);rows=candidates()
    linker=checkout/'.splat/japan_0/mnsg.ld';ld=linker.read_text()
    maps,allmatches=parse_active(checkout,ld)
    sources,byowner=preflight(checkout,rom,rows,maps,allmatches,ld)
    staged_root=checkout/'src/jp1686'
    if staged_root.exists() or (checkout/STAGE).exists():raise ValueError('Stale Japanese 1686 generated stage')
    shutil.copytree(BATCH/'sources',staged_root/'sources')
    pieces=[];source_placements={};affected_sections=set();nontext_only=[]
    for index,(owner,unitlist) in enumerate(sorted(byowner.items())):
        raw=(checkout/owner).read_text()
        matches=allmatches[owner]
        byname={m['name']:m for m in matches}
        header=raw[:matches[0].start()]
        first=int(matches[0]['name'].rsplit('_',1)[1],16)
        end=first+jp329.text_section(checkout/f'build/japan_0/{owner}.o')[1]
        cursor=first;pos=0;unitpieces=[]
        for source,items in sorted(unitlist,key=lambda pair:pair[1][0]['off']):
            start=items[0]['off'];stop=items[-1]['end']
            f=items[0]['function'];last=items[-1]['function']
            a,b=byname[f],byname[last]
            if start<cursor or stop>end:raise ValueError('Overlapping or out-of-owner source '+source)
            for i in range(len(items)-1):
                if byname[items[i]['function']].end()>byname[items[i+1]['function']].start():raise ValueError('Overlapping original blocks')
            if start>cursor:
                name=f'asm/japan_0/jp1686_{index:03}_{len(unitpieces):03}.s'
                fragment=raw[pos:a.start()]
                if not fragment.strip():raise ValueError('Empty ASM gap '+owner)
                dest=checkout/name
                if dest.exists():raise ValueError('Generated ASM already exists')
                dest.write_text(fragment if pos==0 else header+fragment)
                unitpieces.append({'kind':'asm','path':name,'start':cursor,'end':start})
            elif raw[pos:a.start()].strip() and not (pos==0 and raw[:a.start()]==header):
                raise ValueError('Unowned ASM bytes between source units '+owner)
            path='src/jp1686/'+source
            unitpieces.append({'kind':'c','path':path,'start':start,'end':stop,'functions':[it['function'] for it in items],
                              'source_sha256':digest((checkout/path).read_bytes()),'code_sha256':digest(rom[start:stop])})
            source_placements[source]=owner
            cursor=stop;pos=b.end()
        if cursor<end:
            name=f'asm/japan_0/jp1686_{index:03}_{len(unitpieces):03}.s'
            dest=checkout/name
            if dest.exists():raise ValueError('Stale ASM tail '+name)
            dest.write_text(raw[pos:] if pos==0 else header+raw[pos:])
            unitpieces.append({'kind':'asm','path':name,'start':cursor,'end':end})
        if not unitpieces or unitpieces[0]['start']!=first or unitpieces[-1]['end']!=end or any(a['end']!=b['start'] for a,b in zip(unitpieces,unitpieces[1:])):raise ValueError('Linker source fragment gap '+owner)
        needle=f'        build/japan_0/{owner}.o(.text);'
        # Identify enclosing ELF section for original overlay.
        pre=ld[:ld.index(needle)]
        secs=list(re.finditer(r'(?m)^    \.(main|file_\d+|entry)\b',pre))
        if not secs:raise ValueError('Original linker section absent '+owner)
        sec=secs[-1].group(1)
        if sec.startswith('file_'):affected_sections.add(sec)
        ld=ld.replace(needle,'\n'.join(f"        build/japan_0/{p['path']}.o(.text);" for p in unitpieces))
        original_prefix=f'build/japan_0/{owner}.o('
        count=ld.count(original_prefix)
        if count:
            asmfirst=next((p for p in unitpieces if p['kind']=='asm'),None)
            if asmfirst is None:
                # Preserve original data/rodata/bss directives without original .text definitions.
                nontext=f'asm/japan_0/jp1686_{index:03}_nontext.s'
                cleaned=jp329.BLOCK.sub('',raw)
                (checkout/nontext).write_text(cleaned)
                nontext_only.append(nontext)
                ld=ld.replace(original_prefix,f'build/japan_0/{nontext}.o(')
            else:
                ld=ld.replace(original_prefix,f"build/japan_0/{asmfirst['path']}.o(")
        pieces+=unitpieces
    # All overlay sections must preserve the original 4-byte function placements.
    for sec in sorted(affected_sections):
        pattern=r'(?m)^(    \.'+re.escape(sec)+r'\b[^\n]+)SUBALIGN\(16\)'
        ld,n=re.subn(pattern,r'\1SUBALIGN(4)',ld)
        if n not in (0,1):raise ValueError('Unexpected overlay linker alignment '+sec)
    linker.write_text(ld)
    result={'format':'goemon-jp1686-staged-v1','original_sha1':EXPECTED_SHA,'candidate_count':len(rows),
            'source_units':len(sources),'owner_count':len(byowner),'section_alignment_updates':sorted(affected_sections),
            'original_elf_expected':EXPECTED_ELF_FUNCS,'original_relocation_count_expected':EXPECTED_RELOC_COUNT,
            'excluded_relocation_sensitive':sorted(OMIT),'nontext_only_objects':nontext_only,'parts':pieces}
    (checkout/STAGE).write_text(json.dumps(result,indent=2)+'\n')
    return result

def native_build(checkout:Path,deps:Path,runtime:Path,jobs:int=8)->dict:
    data=json.loads((checkout/STAGE).read_text())
    if data['candidate_count']!=1686:raise ValueError('Staged candidate count modified')
    rom=original(checkout);env=jp329.env_for(deps,runtime)
    # Reuse the completely verified JP432 C source input list.
    base=jp432.jp429.full_c_list(checkout,jp432.jp429.manifest())
    base+=' '+' '.join('src/jp_main3/'+r['jp']+'.c' for r in jp432.manifest()['functions'])
    new=sorted({p['path'] for p in data['parts'] if p['kind']=='c'})
    # Make preprocesses IDO inputs into build/.../*.encoded.c; mirror source headers there.
    for hdr in (checkout/'src/jp1686').rglob('*.h'):
        rel=hdr.relative_to(checkout/'src/jp1686')
        target=checkout/'build/japan_0/src/jp1686'/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(hdr,target)
    # Original research pass50 had a compatibility header adjacent to c_sources,
    # while the standalone IDO compiler invoked in the game Makefile reads its
    # generated encoded input from build/ instead of the source directory.
    pass50=checkout/'src/jp1686/sources/pass50/m2c_types.h'
    if pass50.is_file():
        for dest in (checkout/'src/jp1686/sources/pass50/c_sources/m2c_types.h',
                     checkout/'build/japan_0/src/jp1686/sources/pass50/c_sources/m2c_types.h'):
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(pass50,dest)
    args=['make',f'-j{jobs}','VERSION=japan_0','C_FILES='+base+' '+' '.join(new)]
    objects=['build/japan_0/'+p['path']+'.o' for p in data['parts']] + ['build/japan_0/'+p+'.o' for p in data.get('nontext_only_objects',[])]
    subprocess.run(args+objects,env=env,cwd=checkout,check=True,stdout=subprocess.DEVNULL)
    checked=0;relocated=[];packed=[]
    for p in data['parts']:
        target=checkout/('build/japan_0/'+p['path']+'.o')
        _off,size,code,align=jp329.text_section(target)
        expected=p['end']-p['start']
        if size not in (expected,(expected+15)&~15) or align not in (4,16):raise ValueError('Wrong object text size/align: '+p['path']+f' actual {size}/{align}, expected {expected}')
        # Native object code may have unapplied MIPS relocations; link/ROM verification is authoritative.
        if p['kind']=='c':
            if digest((checkout/p['path']).read_bytes())!=p['source_sha256']:raise ValueError('C code modified: '+p['path'])
            rel=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-r','-j','.text',str(target)],env=env,text=True)
            if 'R_MIPS_' in rel:relocated.append({'path':p['path'],'relocations':rel.count('R_MIPS_')})
            checked+=len(p['functions'])
        if size!=expected or align!=4:
            target.write_bytes(pack_text_metadata(target.read_bytes(),expected)[0]);packed.append(p['path'])
        _,n,contents,a=jp329.text_section(target)
        if n!=expected or a!=4:raise ValueError('Original MIPS object extent invalid after packing '+p['path'])
    if checked!=1686:raise ValueError('Not all native functions compiled')
    subprocess.run(args+['build/japan_0/mnsg.z64'],env=env,cwd=checkout,check=True,stdout=subprocess.DEVNULL)
    output=checkout/'build/japan_0/mnsg.z64'
    actual=output.read_bytes()
    if actual!=rom:
        first=next((i for i,(x,y) in enumerate(zip(actual,rom)) if x!=y),None)
        raise ValueError(f'Japanese combined ROM failed: actual size {len(actual)}, expected 33554432, first mismatch {first}')
    retail=checkout/'build/japan_0/mnsg.jp1686.retail.z64'
    subprocess.run([str(runtime/'python/bin/python3.12'),'tools/rommy.py','compress','--input','build/japan_0/mnsg.z64','--output',str(retail),'--manifest','config/japan_0/rommy.yaml','--pad','--verify'],cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    if hashlib.sha1(retail.read_bytes()).hexdigest()!=jp39.SHA_RETAIL:raise ValueError('Retail ROM SHA mismatch')
    result={'native_functions':checked,'source_units':len(new),'packed_objects':len(packed),'source_relocations':relocated,
            'expanded_sha1':hashlib.sha1(actual).hexdigest(),'retail_sha1':jp39.SHA_RETAIL}
    path=checkout/'build/japan_0/jp1686-native-proof.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    return result

def full_verify(checkout:Path,deps:Path,runtime:Path)->dict:
    data=json.loads((checkout/STAGE).read_text())
    rom=original(checkout)
    actual=(checkout/'build/japan_0/mnsg.z64').read_bytes()
    if actual!=rom:raise ValueError('Full-ROM equality gate failed')
    elf=checkout/'build/japan_0/mnsg.elf';env=jp329.env_for(deps,runtime)
    sym=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-t',str(elf)],text=True,env=env)
    funcs={};marked=set();sections=set()
    for line in sym.splitlines():
        q=jp39.F_SYMBOL.fullmatch(line)
        if not q:continue
        adr,kind,sec,size,name=q.groups()
        if sec not in ('.main','.entry','.ipl3') and not re.fullmatch(r'\.file_\d+',sec):continue
        if kind=='F' and int(size,16)>0:
            if name in funcs:raise ValueError('Duplicate ELF original function identity')
            funcs[name]=(sec,int(adr,16),int(size,16));sections.add(sec)
        elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
    if len(funcs)!=7376 or len(sections)!=73:raise ValueError('Original positive ELF funcs / sections differ')
    base=jp432.manifest()
    accepted={f['name'] for x in json.loads((HERE/'regions/japan_0.json').read_text())['units'] for f in x['functions']}
    from . import japan_character_switch_four as jp333
    from . import japan_usa_equivalent_eleven as jp344
    from . import japan_usa_equivalent_36 as jp380
    from . import japan_usa_equivalent_four_more as jp384
    from . import japan_usa_equivalent_thirtyseven_more as jp421
    from . import japan_usa_equivalent_two_remaining as jp423
    from . import japan_usa_grouped_four as jp427
    from . import japan_usa_main_two as jp429
    accepted|={n for x in jp329.load_manifest()['parents'] for n,_ in x['c']}
    accepted|=jp333.EXPECTED_NAMES
    for mod in (jp344,jp380,jp384,jp421,jp423,jp427,jp429,jp432):
        j=mod.manifest();accepted|={x['jp'] for x in j.get('candidates',j.get('functions',[]))}
    if len(accepted)!=432:raise ValueError(f'Original canonical identity drift: {len(accepted)}')
    inc={x['function'] for x in candidates()}
    if accepted&inc:raise ValueError('Canonical duplicate')
    expected=accepted|inc
    if set(funcs)-marked!=expected or len(expected)!=2118:raise ValueError(f'Combined matching-C identity mismatch {len(set(funcs)-marked)} != {len(expected)}')
    for row in candidates():
        n=row['function']
        if funcs.get(n)!=(funcs[n][0],row['vma'],row['end']-row['off']):raise ValueError('Original VMA or ELF extent mismatch '+n)
    func_hash=digest(('\n'.join(f'{n}|{sec}|{v:08x}|{sz:08x}' for n,(sec,v,sz) in sorted(funcs.items()))+'\n').encode())
    region=json.loads((HERE/'regions/japan_0.json').read_text())
    if func_hash!=region['proven_original_elf_function_identities_sha256']:raise ValueError('Original ELF FUNC hash differs')
    out=subprocess.check_output(['readelf','-r','-W',str(elf)],text=True,env=env)
    sec='';records=[]
    for line in out.splitlines():
        g=re.search(r"^Relocation section '([^']+)'",line)
        if g:sec=g[1];continue
        q=re.match(r'^\s*([0-9a-fA-F]{8,16})\s+([0-9a-fA-F]{8})\s+(R_MIPS_[A-Z0-9_]+)\s+([0-9a-fA-F]{8,16})\s+(\S+)',line)
        if q:
            off,inf,kind,val,name=q.groups();records.append((sec,int(off,16),kind,int(val,16),name))
    reloc_hash=digest(('\n'.join(f'{s}|{o:08x}|{k}|{v:08x}|{n}' for s,o,k,v,n in sorted(records))+'\n').encode())
    if len(records)!=80747 or reloc_hash!=region['proven_original_semantic_relocations_sha256']:
        raise ValueError(f'Original semantic relocations differ: {len(records)}/{80747}, hash {reloc_hash}')
    return {'status':'PASSED_G2_LOCAL','region':'japan_0','original_elf_count':len(funcs),'original_elf_identity_sha256':func_hash,
            'matched_c_functions':len(expected),'new_c_functions':len(inc),'matched_c_instruction_bytes':10408+sum(int(x['size_bytes']) for x in candidates()),
            'assembly_remaining':7376-len(expected),'semantic_relocation_count':len(records),'semantic_relocation_sha256':reloc_hash,
            'expanded_rom_sha1':EXPECTED_SHA,'retail_sha1':jp39.SHA_RETAIL,'gameplay':'NOT_RUN'}

def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['stage','build','verify']);parser.add_argument('--checkout',required=True,type=Path)
    parser.add_argument('--deps',type=Path);parser.add_argument('--runtime',type=Path);parser.add_argument('--jobs',type=int,default=8)
    args=parser.parse_args();checkout=args.checkout.resolve(strict=True)
    if args.action=='stage':result=stage(checkout)
    else:
        if args.deps is None or args.runtime is None:parser.error('Need deps and runtime paths')
        if args.action=='build':result=native_build(checkout,args.deps,args.runtime,args.jobs)
        else:result=full_verify(checkout,args.deps,args.runtime)
    print(json.dumps({k:v for k,v in result.items() if k!='parts'},indent=2)[:13000])
if __name__=='__main__':main()
