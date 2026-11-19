"""Port three independently verified USA original-address C functions into Japanese main."""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
from . import japan_usa_main_two as jp429
from . import japan_usa_grouped_four as jp427
from . import japan_usa_equivalent_two_remaining as jp423
from . import japan_noop_port as jp329
from . import japan_thirtynine_verify as jp39
from .japan_thirtyfour_c import pack_text_metadata

HERE=Path(__file__).resolve().parent
MANIFEST=HERE/'regions/japan_0_main3.json'
STAGE=Path('build/japan_0/jp-main3-stage.json')

def digest(blob:bytes)->str:return hashlib.sha256(blob).hexdigest()

def manifest():
    m=json.loads(MANIFEST.read_text())
    keys=('format','region','upstream_commit','prior_c','prior_bytes','new_c','new_bytes','total_c','total_bytes','original_expanded_sha1','original_retail_sha1')
    expected=('goemon-japan-usa-main-3-v1','japan_0',jp39.PINNED,429,9980,3,428,432,10408,jp39.SHA_EXPANDED,jp39.SHA_RETAIL)
    if tuple(m[k] for k in keys)!=expected or jp429.manifest()['total_c']!=429:
        raise ValueError('Original JP main3 source or previous 429 C changed')
    if len(m['functions'])!=3:raise ValueError('Wrong original code count')
    seen=set();total=0
    for x in m['functions']:
        n=x['jp'];src=HERE.parent/x['source_path'];parent=x['current_asm_owner']
        if n in seen or x['sz'] not in (340,56,32) or x['jp_rom']!=int(n.rsplit('_',1)[1],16):
            raise ValueError('Duplicate/invalid original JP original main FUNC')
        if x['vma']!=int(n.split('_')[1],16) or x['section']!='main':raise ValueError('Original JP main ELF address changed')
        if x['source_path'] not in ('decomp/candidates/vm_comparator_exact.c','decomp/rotation_angles.c','decomp/fixed_loop.c'):
            raise ValueError('Unreviewed original USA C source')
        if digest(src.read_bytes())!=x['source_sha256']:raise ValueError('USA source SHA changed')
        if not re.fullmatch(r'asm/japan_0/(?:jpport_)?main_[A-F0-9_]+\.s',parent):
            raise ValueError('Unexpected JP main original linker owner')
        seen.add(n);total+=x['sz']
    if total!=428:raise ValueError('Original transferred code size drift')
    return m

def source_text(x):
    s=(HERE.parent/x['source_path']).read_text();n=x['usa']
    if x['source_path']=='decomp/candidates/vm_comparator_exact.c':
        if n!='func_8003D9B8_3E5B8':raise ValueError('Unreviewed source comparator')
        t=s
    else:
        mt=re.search(r'(?:void|float|s32)\s+'+re.escape(n)+r'\s*\(',s)
        if not mt:raise ValueError('Original USA definition absent '+n)
        start=mt.start();brace=s.index('{',start)
        if s.find(';',start)!=-1 and s.find(';',start)<brace:raise ValueError('Prototyped but not defined source')
        depth=1;end=brace+1
        while depth:
            if end>=len(s):raise ValueError('Original USA definition unclosed')
            if s[end]=='{':depth+=1
            elif s[end]=='}':depth-=1
            end+=1
        t='typedef unsigned short u16; typedef signed int s32;\n'+s[start:end]+'\n'
    if t.count(n)<1:raise ValueError('No C source symbol')
    return t.replace(n,x['jp']).rstrip()+'\n'

def owner_bounds(checkout:Path,path:str)->tuple[int,int]:
    previous=json.loads((checkout/'build/japan_0/noop-port-stage.json').read_text())['parts']
    entry=[x for x in previous if x['path']==path]
    if entry:
        if len(entry)!=1 or entry[0]['kind']!='asm':raise ValueError('Original split linker source is not ASM')
        start,end=entry[0]['start'],entry[0]['end']
    else:
        match=re.fullmatch(r'asm/japan_0/main_([A-F0-9]{4,7})\.s',path)
        if not match:raise ValueError('Unknown original main ASM owner '+path)
        start=int(match[1],16)
        end=start+jp329.text_section(checkout/f'build/japan_0/{path}.o')[1]
    _,sz,_,_=jp329.text_section(checkout/f'build/japan_0/{path}.o')
    if end-start!=sz:raise ValueError('Linked ASM owner text bytes changed')
    return start,end

def stage(checkout:Path,m:dict):
    rom=jp329.original_image(checkout)
    linker=checkout/'.splat/japan_0/mnsg.ld';ld=linker.read_text()
    groups=defaultdict(list)
    for x in m['functions']:
        off=x['jp_rom'];end=off+x['sz']
        if digest(rom[off:end])!=x['code_sha256']:raise ValueError('Original JP ROM differs '+x['jp'])
        groups[x['current_asm_owner']].append(x)
    parts=[]
    for ix,(owner,rows) in enumerate(sorted(groups.items())):
        first,end=owner_bounds(checkout,owner)
        asm=(checkout/owner).read_text();matches=list(jp329.BLOCK.finditer(asm))
        if not matches:raise ValueError('Original ASM function boundaries unavailable '+owner)
        byname={match['name']:match for match in matches}
        header=asm[:matches[0].start()]
        cursor=first;pos=0;pieces=[]
        for x in sorted(rows,key=lambda z:z['jp_rom']):
            n,off,sz=x['jp'],x['jp_rom'],x['sz'];r=byname.get(n)
            if not r or int(r['size'],16)!=sz or off<cursor or off+sz>end:raise ValueError('Original JP function linker extent mismatch '+n)
            if off>cursor:
                name=f'asm/japan_0/jp_main3_{ix:03}_{len(pieces):03}.s';fragment=asm[pos:r.start()]
                if not fragment.strip():raise ValueError('Empty ASM gap before C '+n)
                dest=checkout/name
                if dest.exists():raise ValueError('Stale generated original JP ASM fragment')
                dest.write_text(fragment if pos==0 else header+fragment)
                pieces.append({'kind':'asm','path':name,'start':cursor,'end':off})
            elif asm[pos:r.start()].strip() and not (pos==0 and asm[:r.start()]==header):
                raise ValueError('Interleaved unhandled ASM between original functions')
            name=f'src/jp_main3/{n}.c';dest=checkout/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():raise ValueError('Stale JP source C')
            ctext=source_text(x);dest.write_text(ctext)
            pieces.append({'kind':'c','path':name,'start':off,'end':off+sz,'name':n,'code_sha256':x['code_sha256'],'source_sha256':digest(ctext.encode())})
            cursor=off+sz;pos=r.end()
        if cursor<end:
            name=f'asm/japan_0/jp_main3_{ix:03}_{len(pieces):03}.s'
            dest=checkout/name
            if dest.exists():raise ValueError('Stale ASM tail')
            dest.write_text(asm[pos:] if pos==0 else header+asm[pos:])
            pieces.append({'kind':'asm','path':name,'start':cursor,'end':end})
        if pieces[0]['start']!=first or pieces[-1]['end']!=end or any(a['end']!=b['start'] for a,b in zip(pieces,pieces[1:])):
            raise ValueError('Original JP main text extent discontinuity')
        needle=f'        build/japan_0/{owner}.o(.text);'
        if ld.count(needle)!=1 or '.main 0x80000450' not in ld[:ld.index(needle)]:raise ValueError('Original main linker object ownership changed')
        ld=ld.replace(needle,'\n'.join(f"        build/japan_0/{p['path']}.o(.text);" for p in pieces))
        prefix=f'build/japan_0/{owner}.o('
        nontext=ld.count(prefix)
        if nontext not in (0,1,2,3):raise ValueError('Unexpected original nontext owner count')
        if nontext:
            if pieces[0]['kind']!='asm':raise ValueError('Nontext owner cannot be preserved')
            ld=ld.replace(prefix,f"build/japan_0/{pieces[0]['path']}.o(")
        parts+=pieces
    if len([p for p in parts if p['kind']=='c'])!=3:raise ValueError('Wrong number of new original C units')
    linker.write_text(ld)
    result={'format':'goemon-jp-usa-main3-stage-v1','added_functions':3,'added_bytes':428,'parts':parts}
    if (checkout/STAGE).exists():raise ValueError('Previous main3 source stage exists')
    (checkout/STAGE).write_text(json.dumps(result,indent=2)+'\n')
    return result

def full_c_list(checkout:Path,m:dict)->str:
    return jp429.full_c_list(checkout,jp429.manifest())+' '+' '.join(f"src/jp_main3/{x['jp']}.c" for x in m['functions'])

def build(checkout:Path,deps:Path,runtime:Path,m:dict,jobs:int=4):
    original=jp329.original_image(checkout)
    stage=json.loads((checkout/STAGE).read_text())
    if stage['added_functions']!=3 or stage['added_bytes']!=428:raise ValueError('Stage manifest changed')
    env=jp329.env_for(deps,runtime)
    common=['make',f'-j{jobs}','VERSION=japan_0','C_FILES='+full_c_list(checkout,m)]
    objects=[f"build/japan_0/{p['path']}.o" for p in stage['parts']]
    subprocess.run(common+objects,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    byname={x['jp']:x for x in m['functions']}
    for p in stage['parts']:
        target=checkout/f"build/japan_0/{p['path']}.o"
        _,size,code,align=jp329.text_section(target);expected=p['end']-p['start']
        if size not in (expected,(expected+15)&~15) or align not in (4,16):raise ValueError('Original ABI code extent/alignment mismatch '+p['path'])
        if p['kind']=='c':
            cand=byname[p['name']];source=(checkout/p['path']).read_bytes()
            if digest(source)!=p['source_sha256'] or source.decode()!=source_text(cand):raise ValueError('Original JP C candidate source changed')
            if code[:expected]!=original[p['start']:p['end']]:raise ValueError('Original JP instruction bytes differ '+p['name'])
            rel=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-r','-j','.text',str(target)],text=True,env=env)
            if 'R_MIPS_' in rel:raise ValueError('Unexpected C native code relocation '+p['name'])
        if size!=expected or align!=4:target.write_bytes(pack_text_metadata(target.read_bytes(),expected)[0])
        _,sz,compiled,al=jp329.text_section(target)
        if sz!=expected or al!=4 or (p['kind']=='c' and compiled!=original[p['start']:p['end']]):raise ValueError('Packed original JP C/ASM ELF code differs '+p['path'])
    subprocess.run(common+['build/japan_0/mnsg.z64'],cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    if (checkout/'build/japan_0/mnsg.z64').read_bytes()!=original:raise ValueError('Complete Japanese ROM not original (32 MiB)')
    retail=checkout/'build/japan_0/mnsg.equiv432.retail.z64'
    subprocess.run([str(runtime/'python/bin/python3.12'),'tools/rommy.py','compress','--input','build/japan_0/mnsg.z64','--output',str(retail),'--manifest','config/japan_0/rommy.yaml','--pad','--verify'],env=env,cwd=checkout,check=True,stdout=subprocess.DEVNULL)
    if retail.read_bytes()!=jp39.read_image(checkout/'config/japan_0/baserom.z64',jp39.SHA_RETAIL,0x1000000):raise ValueError('Original Japanese retail bytes changed')
    return retail

def verify(checkout:Path,deps:Path,runtime:Path,retail:Path,m:dict):
    original=jp329.original_image(checkout)
    if jp39.read_image(checkout/'build/japan_0/mnsg.z64',jp39.SHA_EXPANDED,0x2000000)!=original:raise ValueError('Expanded JP ROM mismatch')
    if jp39.read_image(retail,jp39.SHA_RETAIL,0x1000000)!=jp39.read_image(checkout/'config/japan_0/baserom.z64',jp39.SHA_RETAIL,0x1000000):raise ValueError('Retail JP ROM mismatch')
    env=jp329.env_for(deps,runtime);elf=checkout/'build/japan_0/mnsg.elf'
    prior=json.loads((HERE/'regions/japan_0.json').read_text())
    sym=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-t',str(elf)],text=True,env=env)
    funcs={};marked=set();sections=set()
    for line in sym.splitlines():
        q=jp39.F_SYMBOL.fullmatch(line)
        if not q:continue
        address,kind,sec,size,name=q.groups()
        if sec not in ('.main','.entry','.ipl3') and not re.fullmatch(r'\.file_\d+',sec):continue
        if kind=='F' and int(size,16)>0:
            if name in funcs:raise ValueError('Original duplicate MIPS ELF FUNC')
            funcs[name]=(sec,int(address,16),int(size,16));sections.add(sec)
        elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
    from . import japan_character_switch_four as jp333
    from . import japan_usa_equivalent_eleven as jp344
    from . import japan_usa_equivalent_36 as jp380
    from . import japan_usa_equivalent_four_more as jp384
    from . import japan_usa_equivalent_thirtyseven_more as jp421
    base={f['name'] for u in prior['units'] for f in u['functions']}
    base|={n for p in jp329.load_manifest()['parents'] for n,_ in p['c']}
    base|=jp333.EXPECTED_NAMES
    for mod in (jp344,jp380,jp384,jp421,jp423,jp427,jp429):
        units=mod.manifest().get('candidates',mod.manifest().get('functions',[]))
        base|={x['jp'] for x in units}
    if len(base)!=429:raise ValueError('Prior 429 accepted C identities changed')
    expected=base|{x['jp'] for x in m['functions']}
    if len(expected)!=432 or set(funcs)-marked!=expected or len(funcs)!=7376 or len(marked&funcs.keys())!=6944 or len(sections)!=73:
        raise ValueError('Combined original JP 432-C function identity failure')
    for x in m['functions']:
        if funcs.get(x['jp'])!=('.main',x['vma'],x['sz']):raise ValueError('Original JP ELF main function VMA differs '+x['jp'])
    func_hash=digest(('\n'.join(f'{n}|{sec}|{v:08x}|{sz:08x}' for n,(sec,v,sz) in sorted(funcs.items()))+'\n').encode())
    if func_hash!=prior['proven_original_elf_function_identities_sha256']:raise ValueError('Original ELF FUNC digest changed')
    out=subprocess.check_output(['readelf','-r','-W',str(elf)],text=True,env=env)
    sec='';records=[]
    for line in out.splitlines():
        g=re.search(r"^Relocation section '([^']+)'",line)
        if g:sec=g[1];continue
        q=re.match(r'^\s*([0-9a-fA-F]{8,16})\s+([0-9a-fA-F]{8})\s+(R_MIPS_[A-Z0-9_]+)\s+([0-9a-fA-F]{8,16})\s+(\S+)',line)
        if q:
            off,inf,kind,val,name=q.groups();records.append((sec,int(off,16),kind,int(val,16),name))
    reloc_hash=digest(('\n'.join(f'{s}|{o:08x}|{k}|{v:08x}|{n}' for s,o,k,v,n in sorted(records))+'\n').encode())
    if len(records)!=80747 or reloc_hash!=prior['proven_original_semantic_relocations_sha256']:
        raise ValueError('Original JP semantic relocation digest changed')
    return {'status':'PASSED_G2','region':'japan_0','previous_c':429,'added_functions':3,'added_instruction_bytes':428,'matching_c_functions':432,'matching_c_bytes':10408,'remaining_assembly_entries':6944,'original_elf_function_count':7376,'original_elf_identity_sha256':func_hash,'semantic_relocations_count':80747,'semantic_relocations_sha256':reloc_hash,'expanded_rom_sha1':jp39.SHA_EXPANDED,'retail_rom_sha1':jp39.SHA_RETAIL,'original_functions':[{'name':x['jp'],'offset':hex(x['jp_rom']),'size':x['sz']} for x in m['functions']],'emulator_gameplay':'NOT_RUN'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('stage','build','verify'))
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
        if not args.deps or not args.runtime:parser.error('Missing native compiler inputs')
        if args.action=='build':result={'retail':str(build(checkout,args.deps,args.runtime,m,args.jobs))}
        else:
            if not args.retail:parser.error('Missing original retail image')
            result=verify(checkout,args.deps,args.runtime,args.retail,m)
    if args.report:
        with args.report.open('x') as out:json.dump(result,out,indent=2);out.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('parts','original_functions')},indent=2))
if __name__=='__main__':main()
