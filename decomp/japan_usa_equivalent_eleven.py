"""Promote 11 USA-verified, byte-identical movement/math helpers to Japanese file_13.

Separate from JP-333 baseline; stage from the existing original 329-C ASM split
without copying any ROMs or generated objects into source control.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from . import japan_noop_port as jp329
from . import japan_character_switch_four as jp333
from . import japan_thirtynine_verify as jp39
from .japan_thirtyfour_c import pack_text_metadata

HERE=Path(__file__).resolve().parent
MANIFEST=HERE/'regions/japan_0_equiv11.json'
STAGE_NAME='build/japan_0/jp-usa-equiv11-stage.json'
ORIG_FRAG='asm/japan_0/jpport_602FA0_000.s'
SRC_ROOT=HERE/'research/jp_recomp_to_c/src'

def sha256(b:bytes)->str: return hashlib.sha256(b).hexdigest()

def manifest():
    m=json.loads(MANIFEST.read_text())
    if (m['format'],m['region'],m['baseline_matching_c'],m['added_matching_c'],m['added_instruction_bytes']) != ('goemon-japan-original-equivalent-11-v1','japan_0',333,11,728):
        raise ValueError('JP equivalent-11 manifest metadata drift')
    p=m['candidates'];seen=set();total=0
    if len(p)!=11:raise ValueError('Missing eleven original JP candidates')
    for c in p:
        name,off,sz,us=c['jp'],c['jp_rom'],c['sz'],c['usa']
        if name in seen or c['original_jp_instruction_sha256']!=c['hash'] or c['asm']!='602FA0.s':
            raise ValueError('Duplicated or mutated candidate record')
        if not re.fullmatch(r'func_[0-9A-F]{8}_[0-9A-F]{5,7}',name) or int(name.rsplit('_',1)[1],16)!=off:
            raise ValueError('Invalid original Japanese address')
        if not re.fullmatch(r'func_[0-9A-F]{8}_[0-9A-F]{5,7}',us):raise ValueError('Invalid USA original name')
        if sha256((SRC_ROOT/(us+'.c')).read_bytes())!=c['source_sha256']:
            raise ValueError('Previously USA-verified C source changed: '+us)
        seen.add(name);total+=sz
    if total!=728:raise ValueError('Wrong JP instruction-byte total')
    if {c['jp'] for c in p} & jp333.EXPECTED_NAMES:
        raise ValueError('Already accepted character switch double counted')
    return m

def c_source(c):
    src=(SRC_ROOT/(c['usa']+'.c')).read_text()
    if src.count(c['usa'])!=1:raise ValueError('Expected one original USA function name')
    return src.replace(c['usa'],c['jp'])

def full_c_list(checkout:Path):
    existing=jp333.full_c_list(checkout).split()
    return ' '.join(existing+[f"src/jp_equiv/{c['jp']}.c" for c in manifest()['candidates']])

def stage(checkout:Path,m:dict):
    rom=jp329.original_image(checkout)
    f=checkout/ORIG_FRAG;s=f.read_text()
    old=checkout/'build/japan_0/asm/japan_0/jpport_602FA0_000.s.o'
    _,obj_size,_,_=jp329.text_section(old)
    # Parent is the already-verified 329-stage split; its exact offsets are pinned in its stage JSON.
    st=json.loads((checkout/'build/japan_0/noop-port-stage.json').read_text())
    par=[x for x in st['parts'] if x['path']==ORIG_FRAG]
    if len(par)!=1 or (par[0]['start'],par[0]['end'])!=(0x602FA0,0x6075CC) or obj_size!=0x462C:
        raise ValueError('Prerequisite JP-329 source layout drift')
    expected=set(x['jp'] for x in m['candidates'])
    records={r['name']:r for r in jp329.BLOCK.finditer(s)}
    if not expected<=set(records):raise ValueError('JP original assembly function missing')
    header=s[:s.index('nonmatching ')]; cursor=0x602FA0;pos=0;parts=[]
    for c in sorted(m['candidates'],key=lambda x:x['jp_rom']):
        name,off,sz=c['jp'],c['jp_rom'],c['sz'];rec=records[name]
        if int(rec['size'],16)!=sz or sha256(rom[off:off+sz])!=c['hash']:
            raise ValueError('Original Japanese instructions mismatch: '+name)
        if off>cursor:
            frag=s[pos:rec.start()]
            target=f'asm/japan_0/jpeq13_{len(parts):03}.s';p=checkout/target
            if p.exists():raise ValueError('Stale ASM fragment')
            p.write_text(frag if pos==0 else header+frag)
            parts.append(dict(kind='asm',path=target,start=cursor,end=off))
        elif s[pos:rec.start()].strip():raise ValueError('Unreviewed ASM between original functions')
        target=f"src/jp_equiv/{name}.c";p=checkout/target;p.parent.mkdir(exist_ok=True,parents=True)
        if p.exists():raise ValueError('Stale C stage')
        generated=c_source(c);p.write_text(generated)
        parts.append(dict(kind='c',path=target,start=off,end=off+sz,name=name,source_sha256=sha256(generated.encode()),expected_code_sha256=c['hash']))
        pos=rec.end();cursor=off+sz
    if cursor<0x6075CC:
        target=f'asm/japan_0/jpeq13_{len(parts):03}.s'
        (checkout/target).write_text(header+s[pos:])
        parts.append(dict(kind='asm',path=target,start=cursor,end=0x6075CC))
    if parts[0]['start']!=0x602FA0 or parts[-1]['end']!=0x6075CC or any(a['end']!=b['start'] for a,b in zip(parts,parts[1:])):
        raise ValueError('Noncontiguous original JP code layout')
    ldpath=checkout/'.splat/japan_0/mnsg.ld';ld=ldpath.read_text()
    oldtext='        build/japan_0/asm/japan_0/jpport_602FA0_000.s.o(.text);'
    if ld.count(oldtext)!=1 or '.file_13 ' not in ld:raise ValueError('Parent original linker owner missing')
    ld=ld.replace(oldtext,'\n'.join(f"        build/japan_0/{x['path']}.o(.text);" for x in parts))
    for sec in ('data','rodata','bss'):
        old=f'build/japan_0/asm/japan_0/jpport_602FA0_000.s.o(.{sec})'
        if ld.count(old)!=1:raise ValueError('Missing original ASM nontext owner: '+sec)
        ld=ld.replace(old,f"build/japan_0/{parts[0]['path']}.o(.{sec})")
    ldpath.write_text(ld)
    doc={'format':'jp-us-equivalent-11-stage-v1','new_c':11,'new_bytes':728,'old_parent':ORIG_FRAG,'parts':parts}
    with (checkout/STAGE_NAME).open('x') as f:json.dump(doc,f,indent=2);f.write('\n')
    return doc

def build(checkout:Path,deps:Path,runtime:Path,m:dict,jobs:int=8):
    rom=jp329.original_image(checkout)
    doc=json.loads((checkout/STAGE_NAME).read_text())
    if doc['new_c']!=11 or doc['new_bytes']!=728:raise ValueError('Manifest drift')
    env=jp329.env_for(deps,runtime)
    objs=[f"build/japan_0/{p['path']}.o" for p in doc['parts']]
    common=['make',f'-j{jobs}','VERSION=japan_0','C_FILES='+full_c_list(checkout)]
    subprocess.run(common+objs,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    for p in doc['parts']:
        obj=checkout/f"build/japan_0/{p['path']}.o"
        _,size,code,align=jp329.text_section(obj);length=p['end']-p['start']
        if size not in (length,(length+15)&~15):raise ValueError('Wrong source object extent: '+p['path'])
        if p['kind']=='c':
            source=next(c for c in m['candidates'] if c['jp']==p['name'])
            if sha256((checkout/p['path']).read_bytes())!=p['source_sha256'] or (checkout/p['path']).read_text()!=c_source(source):raise ValueError('Generated C drift')
            # This batch has no external data/call relocations. Full linkage is additionally verified.
            if code[:length]!=rom[p['start']:p['end']] or sha256(code[:length])!=p['expected_code_sha256']:
                raise ValueError('Original IDO machine code mismatch: '+p['name'])
        if size!=length or align!=4:
            packed,_=pack_text_metadata(obj.read_bytes(),length);obj.write_bytes(packed)
        _,size,code,align=jp329.text_section(obj)
        if size!=length or align!=4:raise ValueError('Packed ELF section still mismatches source layout')
    subprocess.run(common+['build/japan_0/mnsg.z64'],cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    if (checkout/'build/japan_0/mnsg.z64').read_bytes()!=rom:raise ValueError('Full original 32MiB JP ROM mismatch')
    retail=checkout/'build/japan_0/mnsg.equiv344.retail.z64'
    subprocess.run([str(runtime/'python/bin/python3.12'),'tools/rommy.py','compress',
                    '--input','build/japan_0/mnsg.z64','--output',str(retail),
                    '--manifest','config/japan_0/rommy.yaml','--pad','--verify'],cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    if retail.read_bytes()!=jp39.read_image(checkout/'config/japan_0/baserom.z64',jp39.SHA_RETAIL,0x1000000):
        raise ValueError('Original Japanese retail ROM mismatch')
    return retail

def verify(checkout:Path,deps:Path,runtime:Path,retail:Path,m:dict):
    rom=jp329.original_image(checkout)
    if jp39.read_image(checkout/'build/japan_0/mnsg.z64',jp39.SHA_EXPANDED,0x2000000)!=rom:raise ValueError('Full 32MiB mismatch')
    if jp39.read_image(retail,jp39.SHA_RETAIL,0x1000000)!=jp39.read_image(checkout/'config/japan_0/baserom.z64',jp39.SHA_RETAIL,0x1000000):raise ValueError('Retail mismatch')
    env=jp329.env_for(deps,runtime);elf=checkout/'build/japan_0/mnsg.elf'
    raw=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-t',str(elf)],text=True,env=env)
    funcs={};marked=set();sections=set()
    for line in raw.splitlines():
        a=jp39.F_SYMBOL.fullmatch(line)
        if not a:continue
        addr,kind,sec,size,name=a.groups()
        if sec not in ('.main','.entry','.ipl3') and not re.fullmatch(r'\.file_\d+',sec):continue
        if kind=='F' and int(size,16)>0:
            if name in funcs:raise ValueError('Duplicate original ELF identity')
            funcs[name]=(sec,int(addr,16),int(size,16));sections.add(sec)
        elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
    orig=json.loads((HERE/'regions/japan_0.json').read_text())
    old={f['name'] for u in orig['units'] for f in u['functions']}
    previous={name for p in jp329.load_manifest()['parents'] for name,_ in p['c']}
    now={c['jp'] for c in m['candidates']}
    if len(old)!=39 or len(previous)!=290 or len(now)!=11 or old&now or previous&now or jp333.EXPECTED_NAMES&now:
        raise ValueError('JP accepted function ownership conflict')
    if set(funcs)-marked!=old|previous|jp333.EXPECTED_NAMES|now:
        raise ValueError('Unexpected original JP C/ASM ownership')
    for c in m['candidates']:
        name,off,sz=c['jp'],c['jp_rom'],c['sz']
        expected=(' .file_13',0) # Section checked without a code/ROM shortcut.
        if funcs.get(name)!=('.file_13',0x801D8520+off-0x602FA0,sz):
            raise ValueError('Original JP file_13 ELF name/VMA/size incorrect: '+name+' '+str(funcs.get(name)))
    if len(funcs)!=7376 or len(marked&funcs.keys())!=7032 or len(sections)!=73:
        raise ValueError('ELF function/section inventory mismatch')
    ident=sha256(('\n'.join(f'{n}|{s}|{v:08x}|{z:08x}' for n,(s,v,z) in sorted(funcs.items()))+'\n').encode())
    if ident!=orig['proven_original_elf_function_identities_sha256']:
        raise ValueError('Original ELF identity hash mismatch')
    raw=subprocess.check_output(['readelf','-r','-W',str(elf)],text=True,env=env)
    sec='';records=[]
    for line in raw.splitlines():
        a=re.search(r"^Relocation section '([^']+)'",line)
        if a:sec=a[1];continue
        a=re.match(r'^\s*([0-9a-fA-F]{8,16})\s+([0-9a-fA-F]{8})\s+(R_MIPS_[A-Z0-9_]+)\s+([0-9a-fA-F]{8,16})\s+(\S+)',line)
        if a:
            o,inf,k,v,n=a.groups();records.append((sec,int(o,16),k,int(v,16),n))
    rel=sha256(('\n'.join(f'{s}|{o:08x}|{k}|{v:08x}|{n}' for s,o,k,v,n in sorted(records))+'\n').encode())
    if len(records)!=80747 or rel!=orig['proven_original_semantic_relocations_sha256']:
        raise ValueError('Original ELF relocation count/hash mismatch')
    return {'status':'PASSED_G2','format':'goemon-jp-344-original-c-v1',
            'region':'japan_0','matching_c_functions':344,'matching_c_bytes':6416,
            'added_functions':11,'added_bytes':728,'remaining_assembly_functions':7032,
            'original_elf_functions':7376,'original_elf_function_sha256':ident,
            'original_semantic_relocations':80747,'semantic_relocations_sha256':rel,
            'expanded_rom_sha1':jp39.SHA_EXPANDED,'retail_rom_sha1':jp39.SHA_RETAIL,
            'function_names_offsets':{c['jp']:hex(c['jp_rom']) for c in m['candidates']},
            'emulator_gameplay':'NOT_RUN'}

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('action',choices=['stage','build','verify'])
    a.add_argument('--checkout',type=Path,required=True);a.add_argument('--deps',type=Path);a.add_argument('--runtime',type=Path);a.add_argument('--retail',type=Path);a.add_argument('--report',type=Path);a.add_argument('--jobs',type=int,default=8)
    q=a.parse_args();c=q.checkout.resolve(strict=True);m=manifest()
    if q.action=='stage':res=stage(c,m)
    else:
        if not q.deps or not q.runtime:raise ValueError('Native toolchain paths missing')
        if q.action=='build':res={'retail':str(build(c,q.deps,q.runtime,m,q.jobs))}
        else:
            if q.retail is None:raise ValueError('Missing retail image')
            res=verify(c,q.deps,q.runtime,q.retail,m)
    if q.report:
        with q.report.open('x') as f:json.dump(res,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in res.items() if k not in ('parts','function_names_offsets')},indent=2))
if __name__=='__main__':main()
