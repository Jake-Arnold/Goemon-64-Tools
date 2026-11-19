"""Region JP original-address character-switch C integration after the 329-C gate.

Four USA/JP native-exact switch routines are staged into the original JP file_11
linker translation unit. Requires a private pinned ROM and offline IDO toolchain.
Never outputs or checks in any game image, assembly, ELF or compiler binaries.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from . import japan_noop_port as jp329
from .japan_thirtyfour_c import pack_text_metadata
from . import japan_thirtynine_verify as original

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'research/character_switch_native_candidates.c'
SOURCE_SHA256='8d41e320f201666b8b062960b32e49a764b75e8806605f39bbf6ebaa33e714e0'
STAGE_NAME='build/japan_0/jp-switch-four-stage.json'
RECORDS=(
    ('func_801E2888_59E858',0x59E858,0x28,'SELECT_WRAPPER'),
    ('func_801E28B0_59E880',0x59E880,0x0C,'SELECT_READER'),
    ('func_801E2970_59E940',0x59E940,0x94,'SELECT_SYNC'),
    ('func_801E2A04_59E9D4',0x59E9D4,0x84,'SELECT_ALT'),
)
EXPECTED_NAMES={x[0] for x in RECORDS}
ORIGINAL_PARENT='59DA50.s'
ORIGINAL_SIZE=0x1010
EXPECTED_SHA256={
    'func_801E2888_59E858':'ac19e4b67f7d32974f4462beb03d85979df8247b9b16e74c09c8fd3faf61a771',
    'func_801E28B0_59E880':'b48732223e740fed84b92fbee5fa9a3fb0197fb627625e29f574bc94a423c1a5',
    'func_801E2970_59E940':'9e87cb88a5fd60f120b9f65207da9863eded7bb1ddf6c890d57e2e73eef93363',
    'func_801E2A04_59E9D4':'5cd9a9acbc741485da9d7d416f0187a5c15bf79de2a378d41edcbd47bda6d4be',
}

def sha256(b:bytes)->str: return hashlib.sha256(b).hexdigest()

def source_text(name:str,selection:str)->str:
    return f'#define REGION_JAPAN 1\n#define {selection} 1\n#include "src/jp_switch/jp_switch_verified_shared.h"\n'

def full_c_list(checkout:Path)->str:
    stage=json.loads((checkout/'build/japan_0/noop-port-stage.json').read_text())
    if stage['new_c']!=290 or len([x for x in stage['parts'] if x['kind']=='c'])!=290:
        raise ValueError('Missing authenticated 329-C prerequisite')
    existing=jp329.c_files(stage).split()
    return ' '.join(existing+[f'src/jp_switch/{n}.c' for n,_,_,_ in RECORDS])

def stage(checkout:Path)->dict:
    rom=jp329.original_image(checkout)
    original_s=checkout/'asm/japan_0'/ORIGINAL_PARENT
    if not original_s.is_file():raise ValueError('Missing original JP parent assembly')
    original_text=original_s.read_text()
    blocks={m['name']:m for m in jp329.BLOCK.finditer(original_text)}
    header=original_text[:original_text.index('nonmatching ')]
    _,sz,asm_bytes,_=jp329.text_section(checkout/'build/japan_0/asm/japan_0/59DA50.s.o')
    if sz!=ORIGINAL_SIZE:
        raise ValueError('Original parent section/ROM not exact')
    stage_dir=checkout/'src/jp_switch';stage_dir.mkdir(exist_ok=True,parents=True)
    shared=stage_dir/'jp_switch_verified_shared.h'
    if shared.exists():raise ValueError('Stale switch header; requires fresh staging')
    if sha256(SOURCE.read_bytes())!=SOURCE_SHA256:raise ValueError('Pinned original USA/JP source changed')
    shared.write_bytes(SOURCE.read_bytes())
    # Exact copy of previously isolated native-C research source: all four forms.
    if sha256(shared.read_bytes())!=sha256(SOURCE.read_bytes()):raise ValueError('Research C source changed')
    parts=[];cursor=0x59DA50;pos=0
    for name,off,length,selection in RECORDS:
        m=blocks.get(name)
        if not m or int(m['size'],16)!=length or off!=int(name.rsplit('_',1)[1],16):
            raise ValueError('Incorrect original-JP function boundary: '+name)
        if sha256(rom[off:off+length])!=EXPECTED_SHA256[name]:
            raise ValueError('Original JP function instructions changed: '+name)
        if off>cursor:
            fragment=original_text[pos:m.start()]
            target=f'asm/japan_0/jp_switch_part_{len(parts):02d}.s'
            path=checkout/target
            if path.exists():raise ValueError('Stale split ASM fragment')
            path.write_text((fragment if pos==0 else header+fragment))
            parts.append({'kind':'asm','path':target,'start':cursor,'end':off})
        elif original_text[pos:m.start()].strip():
            raise ValueError('Unexpected code between switch functions')
        target=f'src/jp_switch/{name}.c';src=source_text(name,selection)
        if (checkout/target).exists():raise ValueError('Stale C source')
        (checkout/target).write_text(src)
        parts.append({'kind':'c','path':target,'name':name,'start':off,'end':off+length,
                      'source_sha256':sha256(src.encode()),'original_code_sha256':EXPECTED_SHA256[name]})
        pos=m.end();cursor=off+length
    end=0x59DA50+ORIGINAL_SIZE
    if cursor<end:
        target=f'asm/japan_0/jp_switch_part_{len(parts):02d}.s'
        (checkout/target).write_text(header+original_text[pos:])
        parts.append({'kind':'asm','path':target,'start':cursor,'end':end})
    if parts[0]['start']!=0x59DA50 or parts[-1]['end']!=end or any(a['end']!=b['start'] for a,b in zip(parts,parts[1:])):
        raise ValueError('Noncontiguous original JP parent section')
    linker=checkout/'.splat/japan_0/mnsg.ld';ld=linker.read_text()
    needle='        build/japan_0/asm/japan_0/59DA50.s.o(.text);'
    if ld.count(needle)!=1:raise ValueError('Missing original parent text owner')
    # Keep the original nontext section ownership with the first ASM fragment.
    for sec in ('data','rodata','bss'):
        if ld.count(f'build/japan_0/asm/japan_0/59DA50.s.o(.{sec})')!=1:
            raise ValueError('Original JP nontext owner drift: '+sec)
    repl='\n'.join(f"        build/japan_0/{p['path']}.o(.text);" for p in parts)
    ld=ld.replace(needle,repl).replace('build/japan_0/asm/japan_0/59DA50.s.o(',
          f"build/japan_0/{parts[0]['path']}.o(")
    # Existing JP-329 stage already pins file_11 SUBALIGN(4).
    if '.file_11 0x801D0B90 : AT(file_11_ROM_START) SUBALIGN(4)' not in ld:
        raise ValueError('Original file_11 linker alignment changed')
    linker.write_text(ld)
    payload={'format':'jp-switch-four-original-v1','new_c':4,'new_bytes':332,
             'parent':ORIGINAL_PARENT,'parent_size':ORIGINAL_SIZE,'parent_original_sha256':sha256(rom[0x59DA50:0x59DA50+ORIGINAL_SIZE]),
             'shared_sha256':sha256(shared.read_bytes()),'parts':parts}
    stagefile=checkout/STAGE_NAME
    with stagefile.open('x') as f:json.dump(payload,f,indent=2);f.write('\n')
    return payload

def run_build(checkout:Path,deps:Path,runtime:Path,jobs:int=6):
    rom=jp329.original_image(checkout)
    data=json.loads((checkout/STAGE_NAME).read_text())
    if data['new_c']!=4 or data['new_bytes']!=332:raise ValueError('Bad stage metadata')
    if sha256(SOURCE.read_bytes())!=SOURCE_SHA256 or (checkout/'src/jp_switch/jp_switch_verified_shared.h').read_bytes()!=SOURCE.read_bytes():
        raise ValueError('Source header not original reviewed C')
    env=jp329.env_for(deps,runtime)
    parts=data['parts']; objs=[f"build/japan_0/{p['path']}.o" for p in parts]
    common=['make',f'-j{jobs}','VERSION=japan_0','C_FILES='+full_c_list(checkout)]
    subprocess.run(common+objs,cwd=checkout,env=env,check=True)
    for p in parts:
        obj=checkout/f"build/japan_0/{p['path']}.o"
        _,size,code,align=jp329.text_section(obj)
        length=p['end']-p['start']
        if size not in (length,(length+15)&~15):raise ValueError('Unexpected new C/ASM object size: '+p['path'])
        if p['kind']=='c':
            # External relocations are unresolved in the original IDO object.
            # Whole-ROM and ELF relocation gates below prove resolved code.
            if (checkout/p['path']).read_text()!=source_text(p['name'],next(x[3] for x in RECORDS if x[0]==p['name'])):
                raise ValueError('Unreviewed switch C source')
        if size!=length or align!=4:
            packed,proof=pack_text_metadata(obj.read_bytes(),length)
            obj.write_bytes(packed)
        _,s,code,a=jp329.text_section(obj)
        if s!=length or a!=4:
            raise ValueError('Final code/assembly not original after packing: '+p['path'])
    subprocess.run(common+['build/japan_0/mnsg.z64'],cwd=checkout,env=env,check=True)
    out=(checkout/'build/japan_0/mnsg.z64').read_bytes()
    if out!=rom:raise ValueError('Full 32MiB JP ROM differs from original')
    retail=checkout/'build/japan_0/mnsg.switch333.retail.z64'
    subprocess.run([str(runtime/'python/bin/python3.12'),'tools/rommy.py','compress',
                    '--input','build/japan_0/mnsg.z64','--output',str(retail),
                    '--manifest','config/japan_0/rommy.yaml','--pad','--verify'],cwd=checkout,env=env,check=True)
    if retail.read_bytes()!=original.read_image(checkout/'config/japan_0/baserom.z64',original.SHA_RETAIL,0x1000000):
        raise ValueError('Retail 16MiB JP ROM differs from original')
    return retail

def verify(checkout:Path,deps:Path,runtime:Path,retail:Path):
    data=json.loads((checkout/STAGE_NAME).read_text());rom=jp329.original_image(checkout)
    if data['new_c']!=4 or data['new_bytes']!=332 or data['parent_original_sha256']!=sha256(rom[0x59DA50:0x59EA60]):
        raise ValueError('Missing or modified original JP switch provenance')
    built=original.read_image(checkout/'build/japan_0/mnsg.z64',original.SHA_EXPANDED,0x2000000)
    if original.read_image(retail,original.SHA_RETAIL,0x1000000)!=original.read_image(checkout/'config/japan_0/baserom.z64',original.SHA_RETAIL,0x1000000):
        raise ValueError('Retail ROM bytes differ')
    if built!=rom:raise ValueError('Expanded ROM differs')
    env=jp329.env_for(deps,runtime)
    elf=checkout/'build/japan_0/mnsg.elf'
    out=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-t',str(elf)],text=True,env=env)
    funcs={};marked=set();sections=set()
    for line in out.splitlines():
        m=original.F_SYMBOL.fullmatch(line)
        if not m:continue
        addr,kind,sec,size,name=m.groups()
        if sec not in ('.main','.entry','.ipl3') and not re.fullmatch(r'\.file_\d+',sec):continue
        if kind=='F' and int(size,16)>0:
            if name in funcs:raise ValueError('Duplicate ELF function name: '+name)
            funcs[name]=(sec,int(addr,16),int(size,16));sections.add(sec)
        elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
    base=json.loads((HERE/'regions/japan_0.json').read_text())
    prior={f['name'] for u in base['units'] for f in u['functions']}
    prior329={n for par in jp329.load_manifest()['parents'] for n,_ in par['c']}
    if len(prior)!=39 or len(prior329)!=290 or len(EXPECTED_NAMES)!=4:raise ValueError('Baseline C coverage drift')
    if set(funcs)-marked!=prior|prior329|EXPECTED_NAMES:
        raise ValueError('Unmarked function inventory drift')
    for n,off,size,_ in RECORDS:
        if funcs.get(n)!=('.file_11',0x801D0B90+off-0x58CB60,size):
            # file_11 VRAM offset differs by overlay ROM start 58CB60.
            raise ValueError('New original ELF switch identity drift: '+n+': '+str(funcs.get(n)))
    if len(funcs)!=7376 or len(marked&funcs.keys())!=7043 or len(sections)!=73:
        raise ValueError('Original ELF positive functions/sections drift')
    ident=sha256(('\n'.join(f'{n}|{s}|{v:08x}|{z:08x}' for n,(s,v,z) in sorted(funcs.items()))+'\n').encode())
    if ident!=base['proven_original_elf_function_identities_sha256']:
        raise ValueError('Original ELF function identity hash changed')
    r=subprocess.check_output(['readelf','-r','-W',str(elf)],text=True,env=env)
    sec='';normalized=[]
    for line in r.splitlines():
        g=re.search(r"^Relocation section '([^']+)'",line)
        if g:sec=g[1];continue
        m=re.match(r'^\s*([0-9a-fA-F]{8,16})\s+([0-9a-fA-F]{8})\s+(R_MIPS_[A-Z0-9_]+)\s+([0-9a-fA-F]{8,16})\s+(\S+)',line)
        if m:
            offset,info,kind,value,name=m.groups()
            normalized.append((sec,int(offset,16),kind,int(value,16),name))
    rel=sha256(('\n'.join(f'{s}|{o:08x}|{k}|{v:08x}|{n}' for s,o,k,v,n in sorted(normalized))+'\n').encode())
    if len(normalized)!=80747 or rel!=base['proven_original_semantic_relocations_sha256']:
        raise ValueError('Original JP semantic relocations changed')
    return {'status':'PASSED_G2','region':'japan_0','matching_c_functions':333,'matching_c_bytes':5688,
            'new_c_functions':4,'new_c_bytes':332,'remaining_assembly_functions':7043,
            'original_elf_function_count':7376,'elf_identity_sha256':ident,
            'semantic_relocations_count':80747,'semantic_relocations_sha256':rel,
            'retail_rom_sha1':original.SHA_RETAIL,'expanded_rom_sha1':original.SHA_EXPANDED,
            'function_rom_offsets':{n:hex(off) for n,off,_,_ in RECORDS},'emulator_gameplay':'NOT_RUN'}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('action',choices=['stage','build','verify']);a.add_argument('--checkout',type=Path,required=True)
    a.add_argument('--deps',type=Path);a.add_argument('--runtime',type=Path)
    a.add_argument('--jobs',type=int,default=6);a.add_argument('--retail',type=Path)
    a.add_argument('--report',type=Path)
    q=a.parse_args();c=q.checkout.resolve(strict=True)
    if q.action=='stage': ans=stage(c)
    else:
        if not q.deps or not q.runtime:raise ValueError('Missing tools')
        if q.action=='build':ans={'retail':str(run_build(c,q.deps,q.runtime,q.jobs))}
        else:
            if not q.retail:raise ValueError('Missing retail image')
            ans=verify(c,q.deps,q.runtime,q.retail)
    if q.report:
        with q.report.open('x') as f:json.dump(ans,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in ans.items() if k not in ('parts',)},indent=2))

if __name__=='__main__':main()
