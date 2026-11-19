"""Fail-closed original-address USA C -> Japanese two-function final exact-source transfer following 421 C.

This stage follows the independently verified JP 344-C build. It neither copies
ROM bytes into source code nor relaxes the ELF/relocation/whole-ROM gates.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from pathlib import Path
import hashlib
import json
import re
import subprocess

from . import japan_noop_port as jp329
from . import japan_character_switch_four as jp333
from . import japan_usa_equivalent_eleven as jp344
from . import japan_usa_equivalent_36 as jp380
from . import japan_usa_equivalent_four_more as jp384
from . import japan_usa_equivalent_thirtyseven_more as jp421
from . import japan_thirtynine_verify as jp39
from .japan_thirtyfour_c import pack_text_metadata

HERE = Path(__file__).resolve().parent
MANIFEST = HERE/'regions/japan_0_equiv2_remaining.json'
STAGE = 'build/japan_0/jp-equiv2-stage.json'
# Research C source paths are constrained in the manifest


def digest(b:bytes)->str: return hashlib.sha256(b).hexdigest()


def manifest() -> dict:
    m=json.loads(MANIFEST.read_text())
    keys=('format','region','base_functions','base_bytes','added_functions','added_bytes','total_functions','total_bytes','upstream_commit','original_jp_expanded_sha1','original_jp_retail_sha1')
    expected=('goemon-japan-usa-exact-source-overlay2-v1','japan_0',421,9608,2,68,423,9676,jp39.PINNED,jp39.SHA_EXPANDED,jp39.SHA_RETAIL)
    if tuple(m[k] for k in keys)!=expected:raise ValueError('Unreviewed source batch metadata')
    accepted={f['name'] for u in json.loads((HERE/'regions/japan_0.json').read_text())['units'] for f in u['functions']}
    accepted|={n for p in jp329.load_manifest()['parents'] for n,_ in p['c']}
    accepted|=jp333.EXPECTED_NAMES
    accepted|={x['jp'] for x in jp344.manifest()['candidates']}
    accepted|={x['jp'] for x in jp380.manifest()['candidates']}
    accepted|={x['jp'] for x in jp384.manifest()['candidates']}
    accepted|={x['jp'] for x in jp421.manifest()['candidates']}
    if len(accepted)!=421:raise ValueError('Wrong previous JP C identities')
    seen=set();total=0
    for x in m['candidates']:
        n=x['jp'];o=x['jp_rom'];s=x['sz'];path=HERE.parent/x['source_path']
        if n in seen or n in accepted or int(n.rsplit('_',1)[1],16)!=o or not(8<=s<=512 and s%4==0):
            raise ValueError('Duplicate or invalid function '+n)
        if not re.fullmatch(r'func_[A-Fa-f0-9]{8}_[A-Fa-f0-9]{5,7}',n):raise ValueError('Invalid JP symbol')
        if not x['source_path'].startswith('decomp/research/') or not path.resolve().is_relative_to(HERE.parent.resolve()):
            raise ValueError('Unreviewed USA provenance path')
        if path.name!=x['usa']+'.c' or digest(path.read_bytes())!=x['source_sha256']:
            raise ValueError('USA C source hash mismatch '+n)
        if not re.fullmatch(r'file_\d+', x['section']) or x['original_parent']!='6B7D80.s':
            raise ValueError('Unexpected original Japanese code owner '+n)
        if x['vma']!=int(n.split('_')[1],16):raise ValueError('Original guest VMA mismatch')
        seen.add(n);total+=s
    if len(seen)!=2 or total!=68:raise ValueError('Candidate count drift')
    return m


def c_source(x):
    name=x['usa'];s=(HERE.parent/x['source_path']).read_text()
    if s.count(name)!=1:raise ValueError('USA C source contains unexpected function names')
    return s.replace(name,x['jp'])+'\n'


def full_c_list(checkout:Path,m:dict):
    return jp421.full_c_list(checkout,jp421.manifest())+' '+' '.join(f"src/jp_equiv2/{x['jp']}.c" for x in m['candidates'])


def _owner(x,checkpoint,checkout):
    owner=x['current_owner'];start=x['owner_start'];end=x['owner_end'];off=x['jp_rom']
    if not owner.startswith('asm/japan_0/') or not (start<=off and off+x['sz']<=end):
        raise ValueError('Current original Japanese source ownership invalid')
    obj=checkout/f'build/japan_0/{owner}.o'
    _,size,_,_=jp329.text_section(obj)
    if size!=end-start:
        raise ValueError('Current original ASM text owner width mismatch: '+owner)
    return owner,start,end


def stage(checkout:Path,m:dict):
    rom=jp329.original_image(checkout)
    prior=json.loads((checkout/'build/japan_0/noop-port-stage.json').read_text())
    # Only originals explicitly owned by previous JP-329 split are reused.
    checkpoint={'parts':prior['parts'],'parents':{p['asm'] for p in jp329.load_manifest()['parents']}}
    groups=defaultdict(list);bounds={}
    for x in m['candidates']:
        off=x['jp_rom'];end=off+x['sz']
        if digest(rom[off:end])!=x['code_sha256']:
            raise ValueError('Original JP instruction bytes not identical to accepted USA: '+x['jp'])
        path,start,stop=_owner(x,checkpoint,checkout)
        groups[path].append(x)
        if path in bounds and bounds[path]!=(start,stop):raise ValueError('Conflicting ASM source owner extents')
        bounds[path]=(start,stop)
    ldpath=checkout/'.splat/japan_0/mnsg.ld';ld=ldpath.read_text()
    stageparts=[]
    for seq,(owner,candidates) in enumerate(sorted(groups.items())):
        candidates.sort(key=lambda x:x['jp_rom'])
        start,end=bounds[owner]
        asm=(checkout/owner).read_text()
        matches=list(jp329.BLOCK.finditer(asm))
        if not matches:raise ValueError('No original disassembled functions in '+owner)
        records={r['name']:r for r in matches}
        header=asm[:matches[0].start()]
        cursor=start;pos=0;pieces=[]
        for cand in candidates:
            n,off,sz=cand['jp'],cand['jp_rom'],cand['sz']
            r=records.get(n)
            if r is None or int(r['size'],16)!=sz or off<cursor:
                raise ValueError('Disassembly record or original extent mismatch '+n)
            if off>cursor:
                path=f'asm/japan_0/jpeq2_{seq:03}_{len(pieces):03}.s'
                fragment=asm[pos:r.start()]
                if not fragment.strip():raise ValueError('Unexpected empty original ASM gap')
                text=fragment if pos==0 else header+fragment
                dest=checkout/path
                if dest.exists():raise ValueError('Stale generated source, refuse overwrite '+path)
                dest.write_text(text)
                pieces.append(dict(kind='asm',path=path,start=cursor,end=off))
            elif asm[pos:r.start()].strip() and not (pos==0 and asm[:r.start()]==header):
                raise ValueError('Unaccounted source tokens between adjacent functions: '+owner+' '+n+' '+repr(asm[pos:r.start()][:400]))
            path=f"src/jp_equiv2/{n}.c";dest=checkout/path;dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():raise ValueError('Stale generated C source '+path)
            text=c_source(cand);dest.write_text(text)
            pieces.append(dict(kind='c',path=path,start=off,end=off+sz,name=n,source_sha256=digest(text.encode()),code_sha256=cand['code_sha256']))
            cursor=off+sz;pos=r.end()
        if cursor<end:
            path=f'asm/japan_0/jpeq2_{seq:03}_{len(pieces):03}.s'
            dest=checkout/path
            if dest.exists():raise ValueError('Stale generated ASM '+path)
            dest.write_text((asm[pos:] if pos==0 else header+asm[pos:]))
            pieces.append(dict(kind='asm',path=path,start=cursor,end=end))
        if not pieces or pieces[0]['start']!=start or pieces[-1]['end']!=end or any(a['end']!=b['start'] for a,b in zip(pieces,pieces[1:])):
            raise ValueError('ASM and C source extents not continuous '+owner)
        needle=f'        build/japan_0/{owner}.o(.text);'
        if ld.count(needle)!=1:raise ValueError('Expected exactly one original linker owner: '+owner)
        n=list(re.finditer(r'(?m)^    \.file_(\d+) ',ld[:ld.index(needle)]))[-1].group(1)
        if not any(x['section']==f'file_{n}' for x in candidates):
            raise ValueError('Source region is not original JP overlay file_'+n)
        if re.search(r'(?m)^    \.file_'+n+r' [^\n]+SUBALIGN\(16\)',ld):
            ld,nchanged=re.subn(r'(?m)^(    \.file_'+n+r' [^\n]+)SUBALIGN\(16\)',r'\1SUBALIGN(4)',ld)
            if nchanged!=1:raise ValueError('Overlay section alignment update failure')
        ld=ld.replace(needle,'\n'.join(f"        build/japan_0/{p['path']}.o(.text);" for p in pieces))
        # The first ASM chunk retains non-text section ownership and symbols.
        original_prefix=f'build/japan_0/{owner}.o('
        nontext_count=ld.count(original_prefix)
        if nontext_count not in (0,3):
            raise ValueError('Unexpected ASM nontext ownership '+owner)
        if nontext_count:
            if pieces[0]['kind']!='asm':
                raise ValueError('Cannot reassign original nontext ownership to C: '+owner)
            ld=ld.replace(original_prefix,f"build/japan_0/{pieces[0]['path']}.o(")
        stageparts.extend(pieces)
    if len([p for p in stageparts if p['kind']=='c'])!=2:raise ValueError('Staged C count mismatch')
    ldpath.write_text(ld)
    doc={'format':'goemon-jp-usa-overlay2-stage-v1','added_functions':2,'added_bytes':68,'source_objects':len(groups),'parts':stageparts}
    path=checkout/STAGE
    if path.exists():raise ValueError('Stage already exists')
    path.write_text(json.dumps(doc,indent=2)+'\n')
    return doc


def build(checkout:Path,deps:Path,runtime:Path,m:dict,jobs:int=4):
    rom=jp329.original_image(checkout)
    doc=json.loads((checkout/STAGE).read_text())
    if doc['added_functions']!=2 or doc['added_bytes']!=68:raise ValueError('Stage manifest mismatch')
    env=jp329.env_for(deps,runtime)
    common=['make',f'-j{jobs}','VERSION=japan_0','C_FILES='+full_c_list(checkout,m)]
    objects=[f"build/japan_0/{p['path']}.o" for p in doc['parts']]
    subprocess.run(common+objects,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    byname={x['jp']:x for x in m['candidates']}
    for p in doc['parts']:
        target=checkout/f"build/japan_0/{p['path']}.o"
        _,size,code,align=jp329.text_section(target)
        length=p['end']-p['start']
        if size not in (length,(length+15)&~15) or align not in (4,16):raise ValueError('IDO/MIPS object extent/align mismatch '+p['path'])
        if p['kind']=='c':
            c=byname[p['name']]
            src=(checkout/p['path']).read_bytes()
            if digest(src)!=p['source_sha256'] or src.decode()!=c_source(c):
                raise ValueError('Compiled C source modified after staging')
            if code[:length]!=rom[p['start']:p['end']] or digest(code[:length])!=p['code_sha256']:
                raise ValueError('Original IDO machine-code differs from original JP: '+p['name'])
            rel=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-r','-j','.text',str(target)],text=True,env=env)
            if 'R_MIPS_' in rel:raise ValueError('Unreviewed C relocation '+p['name'])
        if size!=length or align!=4:
            updated,proof=pack_text_metadata(target.read_bytes(),length)
            target.write_bytes(updated)
        _,sz,compiled,alignment=jp329.text_section(target)
        if sz!=length or alignment!=4 or (p['kind']=='c' and compiled!=rom[p['start']:p['end']]):
            raise ValueError('Packed source object identity invalid: '+p['path'])
    subprocess.run(common+['build/japan_0/mnsg.z64'],cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    if (checkout/'build/japan_0/mnsg.z64').read_bytes()!=rom:
        raise ValueError('Complete Japanese 32MiB ROM does not match original')
    retail=checkout/'build/japan_0/mnsg.equiv423.retail.z64'
    subprocess.run([str(runtime/'python/bin/python3.12'),'tools/rommy.py','compress','--input','build/japan_0/mnsg.z64','--output',str(retail),'--manifest','config/japan_0/rommy.yaml','--pad','--verify'],cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    if retail.read_bytes()!=jp39.read_image(checkout/'config/japan_0/baserom.z64',jp39.SHA_RETAIL,0x1000000):
        raise ValueError('Japanese retail ROM changed')
    return retail


def verify(checkout:Path,deps:Path,runtime:Path,retail:Path,m:dict):
    rom=jp329.original_image(checkout)
    if jp39.read_image(checkout/'build/japan_0/mnsg.z64',jp39.SHA_EXPANDED,0x2000000)!=rom:raise ValueError('Expanded ROM differs')
    if jp39.read_image(retail,jp39.SHA_RETAIL,0x1000000)!=jp39.read_image(checkout/'config/japan_0/baserom.z64',jp39.SHA_RETAIL,0x1000000):raise ValueError('Retail ROM differs')
    env=jp329.env_for(deps,runtime)
    original=json.loads((HERE/'regions/japan_0.json').read_text())
    elf=checkout/'build/japan_0/mnsg.elf'
    sym=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-t',str(elf)],text=True,env=env)
    funcs={};marked=set();sections=set()
    for line in sym.splitlines():
        mat=jp39.F_SYMBOL.fullmatch(line)
        if not mat:continue
        a,kind,sec,size,name=mat.groups()
        if sec not in ('.main','.entry','.ipl3') and re.fullmatch(r'\.file_\d+',sec) is None:continue
        if kind=='F' and int(size,16)>0:
            if name in funcs:raise ValueError('Repeated original ELF function identity')
            funcs[name]=(sec,int(a,16),int(size,16));sections.add(sec)
        elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
    base={f['name'] for u in original['units'] for f in u['functions']}
    noop={n for p in jp329.load_manifest()['parents'] for n,_ in p['c']}
    switch=jp333.EXPECTED_NAMES
    prev11={x['jp'] for x in jp344.manifest()['candidates']}
    prev36={x['jp'] for x in jp380.manifest()['candidates']}
    prev4={x['jp'] for x in jp384.manifest()['candidates']}
    prev37={x['jp'] for x in jp421.manifest()['candidates']}
    now={x['jp'] for x in m['candidates']}
    expected=base|noop|switch|prev11|prev36|prev4|prev37|now
    if len(expected)!=423 or len(set(funcs)-marked)!=423 or set(funcs)-marked!=expected:
        raise ValueError('Combined JP 423-C function ownership differs')
    offsets={x['jp']:x for x in m['candidates']}
    for n,x in offsets.items():
        region=x['section'];source_name=x['original_parent']
        # Original guest VMA is pinned independently of the relocated overlay.
        if funcs.get(n)!=(f'.{region}',x['vma'],x['sz']):
            raise ValueError('Original JP ELF function VMA or section differs: '+n+' '+str(funcs.get(n)))
    if len(funcs)!=7376 or len(marked&funcs.keys())!=6953 or len(sections)!=73:raise ValueError('ELF inventory mismatch')
    ident=digest(('\n'.join(f'{n}|{s}|{v:08x}|{z:08x}' for n,(s,v,z) in sorted(funcs.items()))+'\n').encode())
    if ident!=original['proven_original_elf_function_identities_sha256']:raise ValueError('Original ELF identity digest differs')
    out=subprocess.check_output(['readelf','-r','-W',str(elf)],text=True,env=env)
    sec='';records=[]
    for line in out.splitlines():
        g=re.search(r"^Relocation section '([^']+)'",line)
        if g:sec=g[1];continue
        q=re.match(r'^\s*([0-9a-fA-F]{8,16})\s+([0-9a-fA-F]{8})\s+(R_MIPS_[A-Z0-9_]+)\s+([0-9a-fA-F]{8,16})\s+(\S+)',line)
        if q:
            off,inf,kind,val,name=q.groups();records.append((sec,int(off,16),kind,int(val,16),name))
    rel=digest(('\n'.join(f'{s}|{o:08x}|{k}|{v:08x}|{n}' for s,o,k,v,n in sorted(records))+'\n').encode())
    if len(records)!=80747 or rel!=original['proven_original_semantic_relocations_sha256']:
        raise ValueError('Original JP relocation tuple digest mismatch')
    return {'status':'PASSED_G2','region':'japan_0','baseline_c':421,'added_c':2,'added_instruction_bytes':68,'matching_c_functions':423,'matching_c_bytes':9676,'remaining_assembly_entries':6953,'original_elf_function_count':7376,'original_elf_identity_sha256':ident,'semantic_relocations_count':len(records),'semantic_relocations_sha256':rel,'expanded_rom_sha1':jp39.SHA_EXPANDED,'retail_rom_sha1':jp39.SHA_RETAIL,'original_overlay_functions':[{'name':x['jp'],'rom_offset':f"0x{x['jp_rom']:X}",'size':x['sz']} for x in m['candidates']],'emulator_gameplay':'NOT_RUN'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['stage','build','verify'])
    parser.add_argument('--checkout',type=Path,required=True)
    parser.add_argument('--deps',type=Path)
    parser.add_argument('--runtime',type=Path)
    parser.add_argument('--retail',type=Path)
    parser.add_argument('--jobs',type=int,default=4)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    m=manifest();checkout=args.checkout.resolve(strict=True)
    if args.action=='stage':result=stage(checkout,m)
    else:
        if not args.deps or not args.runtime:parser.error('Missing native toolchain inputs')
        if args.action=='build':result={'retail':str(build(checkout,args.deps,args.runtime,m,args.jobs))}
        else:
            if not args.retail:parser.error('Missing retail ROM output')
            result=verify(checkout,args.deps,args.runtime,args.retail,m)
    if args.report:
        with args.report.open('x') as file:json.dump(result,file,indent=2);file.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('parts','original_overlay_functions')},indent=2))

if __name__=='__main__':main()
