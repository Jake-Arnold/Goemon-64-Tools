"""Original-USA source equivalent for two JP main-executable memory routines."""
from __future__ import annotations
from pathlib import Path
from collections import defaultdict
import argparse
import hashlib
import json
import re
import subprocess
from . import japan_usa_grouped_four as jp427
from . import japan_usa_equivalent_two_remaining as jp423
from . import japan_noop_port as jp329
from . import japan_thirtynine_verify as jp39
from .japan_thirtyfour_c import pack_text_metadata

HERE=Path(__file__).resolve().parent
MANIFEST=HERE/'regions/japan_0_main2.json'
STAGE=Path('build/japan_0/jp-main2-stage.json')

def digest(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def manifest():
    m=json.loads(MANIFEST.read_text())
    keys=('format','region','upstream_commit','previous_c','previous_bytes','added_c','added_bytes','total_c','total_bytes','original_jp_expanded_sha1','original_jp_retail_sha1')
    expected=('goemon-japan-usa-main-2-v1','japan_0',jp39.PINNED,427,9892,2,88,429,9980,jp39.SHA_EXPANDED,jp39.SHA_RETAIL)
    if tuple(m[k] for k in keys)!=expected:raise ValueError('Original JP main2 source manifest drift')
    if len(m['candidates'])!=2 or jp427.manifest()['total_c']!=427:raise ValueError('Base accepted C functions changed')
    seen=set();size=0
    for x in m['candidates']:
        n=x['jp'];s=x['sz']
        if n in seen or s not in (40,48) or int(n.rsplit('_',1)[1],16)!=x['jp_rom']:
            raise ValueError('Duplicate JP main original function '+n)
        if x['section']!='main' or x['original_parent']!='asm/japan_0/main_44F0.s':
            raise ValueError('Original JP main segment ownership changed')
        if x['source_path']!='decomp/system_memory.c':raise ValueError('Unreviewed source path')
        if digest((HERE.parent/x['source_path']).read_bytes())!=x['source_sha256']:
            raise ValueError('Original USA C source is no longer accepted fixture')
        if int(n.split('_')[1],16)!=x['vma']:raise ValueError('Original JP VMA mismatch')
        seen.add(n);size+=s
    if len(seen)!=2 or size!=88:raise ValueError('JP C amount drift')
    return m

def source_text(x):
    s=(HERE.parent/x['source_path']).read_text();us=x['usa']
    name='void '+us+'('
    start=s.index(name)
    if s.find(';',start)<s.find('{',start):start=s.index(name,start+1)
    brace=s.index('{',start);depth=1;pos=brace+1
    while depth:
        if pos>=len(s):raise ValueError('Unterminated original USA C')
        if s[pos]=='{':depth+=1
        elif s[pos]=='}':depth-=1
        pos+=1
    t=s[start:pos]
    if t.count(us)!=1:raise ValueError('Expected one original USA C definition')
    return 'typedef unsigned char u8; typedef int s32;\n'+t.replace(us,x['jp'])+'\n'

def stage(checkout:Path,m:dict):
    rom=jp329.original_image(checkout)
    owner='asm/japan_0/main_44F0.s'
    original=(checkout/owner).read_text()
    matches=list(jp329.BLOCK.finditer(original))
    if not matches:raise ValueError('No original JP main ASM function signatures')
    definitions={r['name']:r for r in matches}
    first=0x44F0
    _,width,_,_=jp329.text_section(checkout/f'build/japan_0/{owner}.o')
    end=first+width
    if end!=0x4D70:raise ValueError('Original main_44F0 section bounds changed')
    cs=sorted(m['candidates'],key=lambda x:x['jp_rom'])
    header=original[:matches[0].start()]
    cursor=first;pos=0;parts=[]
    for x in cs:
        n=x['jp'];o=x['jp_rom'];z=x['sz'];r=definitions.get(n)
        if r is None or int(r['size'],16)!=z or o<cursor or o+z>end:
            raise ValueError('Original JP main symbol extent mismatch '+n)
        if digest(rom[o:o+z])!=x['code_sha256']:raise ValueError('Original JP MIPS code hash changed '+n)
        if o>cursor:
            f=f'asm/japan_0/jpmain2_{len(parts):03}.s'
            frag=original[pos:r.start()]
            if not frag.strip():raise ValueError('Unexpected empty original main ASM gap')
            dest=checkout/f
            if dest.exists():raise ValueError('Stale original ASM fragment')
            dest.write_text(frag if pos==0 else header+frag)
            parts.append({'kind':'asm','path':f,'start':cursor,'end':o})
        else:
            if original[pos:r.start()].strip() and not (pos==0 and original[:r.start()]==header):
                raise ValueError('Unaccounted ASM tokens')
        name=f'src/jp_main2/{n}.c';dest=checkout/name
        dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists():raise ValueError('Stale original C source')
        code=source_text(x);dest.write_text(code)
        parts.append({'kind':'c','path':name,'start':o,'end':o+z,'name':n,'source_sha256':digest(code.encode()),'code_sha256':x['code_sha256']})
        cursor=o+z;pos=r.end()
    if cursor<end:
        p=f'asm/japan_0/jpmain2_{len(parts):03}.s'
        (checkout/p).write_text(original[pos:] if pos==0 else header+original[pos:])
        parts.append({'kind':'asm','path':p,'start':cursor,'end':end})
    if parts[0]['start']!=first or parts[-1]['end']!=end or any(a['end']!=b['start'] for a,b in zip(parts,parts[1:])):
        raise ValueError('Changed original ASM/C section extents')
    ldp=checkout/'.splat/japan_0/mnsg.ld';ld=ldp.read_text()
    needle=f'        build/japan_0/{owner}.o(.text);'
    if ld.count(needle)!=1:raise ValueError('Original main section owner missing')
    if '.main 0x80000450' not in ld[:ld.index(needle)]:raise ValueError('Original main linker placement changed')
    ld=ld.replace(needle,'\n'.join(f"        build/japan_0/{p['path']}.o(.text);" for p in parts))
    orig=f'build/japan_0/{owner}.o('
    if ld.count(orig)!=1 or parts[0]['kind']!='asm':raise ValueError('Original main nontext owner unexpected')
    ld=ld.replace(orig,f"build/japan_0/{parts[0]['path']}.o(")
    ldp.write_text(ld)
    result={'format':'goemon-japan-usa-main2-stage-v1','added_c':2,'added_bytes':88,'parts':parts}
    if (checkout/STAGE).exists():raise ValueError('Prior staged JP main2 object')
    (checkout/STAGE).write_text(json.dumps(result,indent=2)+'\n')
    return result

def full_c_list(checkout:Path,m:dict)->str:
    return jp427.full_c_list(checkout,jp427.manifest())+' '+' '.join(f"src/jp_main2/{x['jp']}.c" for x in m['candidates'])

def build(checkout:Path,deps:Path,runtime:Path,m:dict,jobs:int=4):
    rom=jp329.original_image(checkout)
    st=json.loads((checkout/STAGE).read_text())
    if st['added_c']!=2 or st['added_bytes']!=88:raise ValueError('JP main2 stage metadata changed')
    env=jp329.env_for(deps,runtime)
    common=['make',f'-j{jobs}','VERSION=japan_0','C_FILES='+full_c_list(checkout,m)]
    objects=[f"build/japan_0/{p['path']}.o" for p in st['parts']]
    subprocess.run(common+objects,env=env,cwd=checkout,stdout=subprocess.DEVNULL,check=True)
    cmap={x['jp']:x for x in m['candidates']}
    for p in st['parts']:
        target=checkout/f"build/japan_0/{p['path']}.o"
        _,sz,code,align=jp329.text_section(target);expected=p['end']-p['start']
        if sz not in (expected,(expected+15)&~15) or align not in (4,16):raise ValueError('Original main2 object extent differs '+p['path'])
        if p['kind']=='c':
            x=cmap[p['name']];source=(checkout/p['path']).read_bytes()
            if digest(source)!=p['source_sha256'] or source.decode()!=source_text(x):raise ValueError('Original JP C source mutation '+p['name'])
            if code[:expected]!=rom[p['start']:p['end']]:raise ValueError('Original JP MIPS instructions mismatch '+p['name'])
            reloc=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-r','-j','.text',str(target)],env=env,text=True)
            if 'R_MIPS_' in reloc:raise ValueError('Unexpected original main C relocation '+p['name'])
        if sz!=expected or align!=4:target.write_bytes(pack_text_metadata(target.read_bytes(),expected)[0])
        _,checksz,checkcode,checkalign=jp329.text_section(target)
        if checksz!=expected or checkalign!=4 or (p['kind']=='c' and checkcode!=rom[p['start']:p['end']]):
            raise ValueError('Original JP main C ELF object was repacked incorrectly')
    subprocess.run(common+['build/japan_0/mnsg.z64'],cwd=checkout,env=env,stdout=subprocess.DEVNULL,check=True)
    if (checkout/'build/japan_0/mnsg.z64').read_bytes()!=rom:raise ValueError('Japanese 32MiB expanded ROM differs')
    retail=checkout/'build/japan_0/mnsg.equiv429.retail.z64'
    subprocess.run([str(runtime/'python/bin/python3.12'),'tools/rommy.py','compress','--input','build/japan_0/mnsg.z64','--output',str(retail),'--manifest','config/japan_0/rommy.yaml','--pad','--verify'],cwd=checkout,env=env,stdout=subprocess.DEVNULL,check=True)
    if retail.read_bytes()!=jp39.read_image(checkout/'config/japan_0/baserom.z64',jp39.SHA_RETAIL,0x1000000):raise ValueError('Japanese retail ROM differs')
    return retail

def verify(checkout:Path,deps:Path,runtime:Path,retail:Path,m:dict):
    rom=jp329.original_image(checkout)
    if jp39.read_image(checkout/'build/japan_0/mnsg.z64',jp39.SHA_EXPANDED,0x2000000)!=rom:raise ValueError('Expanded image changed')
    if jp39.read_image(retail,jp39.SHA_RETAIL,0x1000000)!=jp39.read_image(checkout/'config/japan_0/baserom.z64',jp39.SHA_RETAIL,0x1000000):raise ValueError('Retail image changed')
    env=jp329.env_for(deps,runtime);elf=checkout/'build/japan_0/mnsg.elf'
    original=json.loads((HERE/'regions/japan_0.json').read_text())
    text=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-t',str(elf)],text=True,env=env)
    funcs={};marked=set();secs=set()
    for line in text.splitlines():
        result=jp39.F_SYMBOL.fullmatch(line)
        if not result:continue
        a,kind,sec,size,name=result.groups()
        if sec not in ('.main','.entry','.ipl3') and re.fullmatch(r'\.file_\d+',sec) is None:continue
        if kind=='F' and int(size,16)>0:
            if name in funcs:raise ValueError('Duplicate original JP ELF FUNC')
            funcs[name]=(sec,int(a,16),int(size,16));secs.add(sec)
        elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
    # The original JP source manifest retains the exact list of all accepted C functions.
    from . import japan_character_switch_four as jp333
    from . import japan_usa_equivalent_eleven as jp344
    from . import japan_usa_equivalent_36 as jp380
    from . import japan_usa_equivalent_four_more as jp384
    from . import japan_usa_equivalent_thirtyseven_more as jp421
    accepted={f['name'] for u in original['units'] for f in u['functions']}
    accepted|={n for p in jp329.load_manifest()['parents'] for n,_ in p['c']}
    accepted|=jp333.EXPECTED_NAMES
    for module in (jp344,jp380,jp384,jp421,jp423):accepted|={x['jp'] for x in module.manifest()['candidates']}
    accepted|={x['jp'] for x in jp427.manifest()['candidates']}
    if len(accepted)!=427:raise ValueError('Previous JP 427 matching C set differs')
    expected=accepted|{x['jp'] for x in m['candidates']}
    if len(expected)!=429 or set(funcs)-marked!=expected or len(funcs)!=7376 or len(marked&funcs.keys())!=6947 or len(secs)!=73:
        raise ValueError('Original JP ELF inventory changed in main2 integration')
    for x in m['candidates']:
        if funcs.get(x['jp'])!=('.main',x['vma'],x['sz']):raise ValueError('Original JP main ELF function location differs '+x['jp'])
    fn_hash=digest(('\n'.join(f'{n}|{s}|{v:08x}|{z:08x}' for n,(s,v,z) in sorted(funcs.items()))+'\n').encode())
    if fn_hash!=original['proven_original_elf_function_identities_sha256']:raise ValueError('Original JP ELF identity digest differs')
    out=subprocess.check_output(['readelf','-r','-W',str(elf)],text=True,env=env)
    sec='';rels=[]
    for line in out.splitlines():
        match=re.search(r"^Relocation section '([^']+)'",line)
        if match:sec=match[1];continue
        m2=re.match(r'^\s*([0-9a-fA-F]{8,16})\s+([0-9a-fA-F]{8})\s+(R_MIPS_[A-Z0-9_]+)\s+([0-9a-fA-F]{8,16})\s+(\S+)',line)
        if m2:
            off,info,kind,val,name=m2.groups();rels.append((sec,int(off,16),kind,int(val,16),name))
    rel_hash=digest(('\n'.join(f'{s}|{o:08x}|{k}|{v:08x}|{n}' for s,o,k,v,n in sorted(rels))+'\n').encode())
    if len(rels)!=80747 or rel_hash!=original['proven_original_semantic_relocations_sha256']:raise ValueError('Original JP semantic relocations changed')
    return {'status':'PASSED_G2','region':'japan_0','previous_c':427,'new_matching_c':2,'new_bytes':88,'matching_c_functions':429,'matching_c_bytes':9980,'remaining_assembly_entries':6947,'original_elf_function_count':7376,'original_elf_identity_sha256':fn_hash,'semantic_relocations_count':80747,'semantic_relocations_sha256':rel_hash,'expanded_rom_sha1':jp39.SHA_EXPANDED,'retail_rom_sha1':jp39.SHA_RETAIL,'new_functions':[{'name':x['jp'],'rom_offset':f"0x{x['jp_rom']:X}",'size':x['sz']} for x in m['candidates']],'emulator_gameplay':'NOT_RUN'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['stage','build','verify'])
    parser.add_argument('--checkout',type=Path,required=True)
    parser.add_argument('--deps',type=Path)
    parser.add_argument('--runtime',type=Path)
    parser.add_argument('--retail',type=Path)
    parser.add_argument('--report',type=Path)
    parser.add_argument('--jobs',type=int,default=4)
    args=parser.parse_args()
    m=manifest();checkout=args.checkout.resolve(strict=True)
    if args.action=='stage':result=stage(checkout,m)
    else:
        if not args.deps or not args.runtime:parser.error('Missing original native toolchain inputs')
        if args.action=='build':result={'retail':str(build(checkout,args.deps,args.runtime,m,args.jobs))}
        else:
            if not args.retail:parser.error('Retained retail ROM required')
            result=verify(checkout,args.deps,args.runtime,args.retail,m)
    if args.report:
        with args.report.open('x') as out:json.dump(result,out,indent=2);out.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('parts','new_functions')},indent=2))
if __name__=='__main__':main()
