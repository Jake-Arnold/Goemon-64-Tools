"""Reproducible USA-derived no-op C port to Japanese rev-0 (39 + 290 functions).

This only stages human-readable C, a local linker layout and reproducible
original-address proof. Requires the ROM and IDO tools privately at build time.
Do not commit generated assembly, object files, linker scripts or ROMs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess

from . import japan_thirtynine_verify as baseline
from .japan_thirtyfour_c import pack_text_metadata

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / 'regions/japan_0_noop_port_290.json'
BASE_MANIFEST = HERE / 'regions/japan_0.json'
BASE_BUILD = HERE / 'build_japan_thirtynine_c.sh'
BLOCK = re.compile(r'(?ms)^nonmatching (?P<name>func_[0-9A-Fa-f]+_[0-9A-Fa-f]+), 0x(?P<size>[0-9A-Fa-f]+)\s*\n.*?^endlabel (?P=name)[^\n]*\n')
FORM = {
    'P': {'size': 12, 'kind': 'two_pointer_unused', 'arguments': 'void *a0, void *a1',
          'code_sha256': '691e766163b1b8288cf1e76b4dc9eb7dde764cde7f749bf5aef916d919300f2b'},
    'Z': {'size': 8, 'kind': 'zero_arg_noop', 'arguments': 'void',
          'code_sha256': '78aa5094d5ec7291c79f799c009d04f06c2f20187988e3dcc8d35ee5efdbb378'},
}
EXPECTED_RELOCS = 80747
EXPECTED_FUNCTIONS = 7376


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def load_manifest(path: Path = MANIFEST) -> dict:
    m = json.loads(path.read_text())
    assert m['format'] == 'goemon-japan-usa-verified-noop-port-v1'
    assert m['region'] == 'japan_0' and m['upstream_commit'] == baseline.PINNED
    assert (m['baseline_c_functions'], m['baseline_c_bytes']) == (39, 2092)
    assert (m['new_c_functions'], m['new_c_bytes']) == (290, 3264)
    assert (m['total_c_functions'], m['total_c_bytes']) == (329, 5356)
    assert (m['original_retail_sha1'], m['original_expanded_sha1']) == (baseline.SHA_RETAIL, baseline.SHA_EXPANDED)
    assert m['original_semantic_relocation_count'] == EXPECTED_RELOCS
    base = json.loads(BASE_MANIFEST.read_text())
    assert m['original_elf_func_sha256'] == base['proven_original_elf_function_identities_sha256']
    assert m['original_semantic_relocations_sha256'] == base['proven_original_semantic_relocations_sha256']
    seen_names, seen_files, entries = set(), set(), []
    for parent in m['parents']:
        name = parent['asm']
        assert re.fullmatch(r'(?:main_)?[0-9A-F]{5,7}\.s', name), name
        assert name not in seen_files
        seen_files.add(name)
        first = int(name[:-2].removeprefix('main_'), 16)
        assert first == parent['start'] and parent['size'] > 0 and parent['size'] % 16 == 0
        prior_end = first
        for entry in parent['c']:
            assert len(entry) == 2
            func, form = entry
            assert form in FORM
            match = re.fullmatch(r'func_([0-9A-F]{8})_([0-9A-F]{5,7})', func)
            assert match, func
            off, sz = int(match[2], 16), FORM[form]['size']
            assert prior_end <= off and off + sz <= first + parent['size'], func
            assert func not in seen_names
            seen_names.add(func)
            entries.append((func, off, int(match[1], 16), sz, form, name))
            prior_end = off + sz
    assert len(entries) == m['new_c_functions']
    assert sum(t[3] for t in entries) == m['new_c_bytes']
    assert len(m['parents']) == 81
    assert sum(t[4] == 'P' for t in entries) == 236
    assert sum(t[4] == 'Z' for t in entries) == 54
    base_names = {f['name'] for u in base['units'] for f in u['functions']}
    assert not (seen_names & base_names)
    return m


def source_text(name: str, form: str) -> str:
    info = FORM[form]
    return (f"/* Original JP stub; USA verified C form: {info['kind']}. */\n"
            f"void {name}({info['arguments']}) {{}}\n")


def text_section(obj: Path) -> tuple[int, int, bytes, int]:
    data = obj.read_bytes()
    if data[:6] != b'\x7fELF\x01\x02':
        raise ValueError('Expected original big-endian 32-bit ELF: '+str(obj))
    off = struct.unpack_from('>I', data, 32)[0]
    shsize, shnum = struct.unpack_from('>HH', data, 46)
    if shsize != 40:
        raise ValueError('Unexpected ELF section header width')
    found = []
    for i in range(shnum):
        p = off + i*40
        if struct.unpack_from('>II', data, p+4) == (1, 6):
            o,n = struct.unpack_from('>II', data, p+16)
            align = struct.unpack_from('>I', data, p+32)[0]
            found.append((o,n,data[o:o+n],align))
    if len(found) != 1:
        raise ValueError(f'Expected one executable text section in {obj}; found {len(found)}')
    return found[0]


def original_image(checkout: Path) -> bytes:
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True).strip() != baseline.PINNED:
        raise ValueError('Wrong pinned upstream source commit')
    if subprocess.run(['git','diff','--quiet'],cwd=checkout,check=False).returncode:
        raise ValueError('Upstream tracked source changes not permitted')
    return baseline.read_image(checkout/'config/japan_0/baserom.decompressed.z64',baseline.SHA_EXPANDED,0x2000000)


def stage(checkout: Path, m: dict, stage_path: Path) -> dict:
    checkout=checkout.resolve(strict=True)
    rom=original_image(checkout)
    ld=checkout/'.splat/japan_0/mnsg.ld'
    script=ld.read_text()
    if script.count('.main 0x80000450 : AT(main_ROM_START) SUBALIGN(4)') != 1:
        raise ValueError('39-C prerequisite has not installed original JP main alignment')
    cparts=[];parts=[]
    for parent in m['parents']:
        filename=parent['asm'];stem=filename[:-2]
        orig=checkout/'asm/japan_0'/filename
        original=orig.read_text()
        header=original[:original.index('nonmatching ')]
        base=parent['start'];size=parent['size']
        original_obj=checkout/'build/japan_0/asm/japan_0'/f'{filename}.o'
        _,obj_size,body,_=text_section(original_obj)
        if obj_size != size:
            raise ValueError('Original JP assembly section extent drift: '+filename)
        # Explicitly prove the selected original assembly records and their ABI.
        all_records={x.group('name'):x for x in BLOCK.finditer(original)}
        elig=[]
        for name,form in parent['c']:
            match=all_records.get(name)
            if match is None:raise ValueError('Missing original JP function: '+name)
            off=int(name.rsplit('_',1)[1],16);length=int(match.group('size'),16)
            if length!=FORM[form]['size'] or digest(rom[off:off+length])!=FORM[form]['code_sha256']:
                raise ValueError('JP function instruction signature or extent mismatch: '+name)
            elig.append((off,name,match,form))
        if elig != sorted(elig,key=lambda x:x[0]):
            raise ValueError('JP function order invalid: '+filename)
        # Verify that no original JP function sharing either exact template was omitted.
        native_eligible={x.group('name') for x in all_records.values() if
            (length:=int(x.group('size'),16)) in (8,12) and
            digest(rom[int(x.group('name').rsplit('_',1)[1],16):int(x.group('name').rsplit('_',1)[1],16)+length]) in
            {f['code_sha256'] for f in FORM.values()}}
        if native_eligible != {x[1] for x in elig}:
            raise ValueError('Missing or added JP portable stubs: '+filename)
        created=[];cur=base;pos=0
        for off,name,match,form in elig:
            if off>cur:
                fragment=original[pos:match.start()]
                if '/* ' not in fragment:raise ValueError('Missing original assembly fragment')
                path=f'asm/japan_0/jpport_{stem}_{len(created):03d}.s'
                target=checkout/path
                if target.exists():raise ValueError('Not a fresh staged checkout: '+str(target))
                target.write_text((fragment if pos==0 else header+fragment))
                created.append({'kind':'asm','path':path,'start':cur,'end':off})
            else:
                skip=original[pos:match.start()].strip()
                if skip and not skip.startswith('.include'):
                    raise ValueError('Unexpected assembly content before C: '+name)
            path=f'src/jp_ported/jpport_{name}.c'
            target=checkout/path
            target.parent.mkdir(exist_ok=True,parents=True)
            if target.exists():raise ValueError('Not a fresh C target: '+str(target))
            src=source_text(name,form)
            target.write_text(src)
            length=FORM[form]['size']
            created.append({'kind':'c','path':path,'start':off,'end':off+length,'name':name,'form':form,
                            'source_sha256':digest(src.encode())})
            pos=match.end();cur=off+length
        if cur<base+size:
            fragment=original[pos:]
            if '/* ' not in fragment:raise ValueError('Missing final assembly fragment')
            path=f'asm/japan_0/jpport_{stem}_{len(created):03d}.s'
            target=checkout/path
            if target.exists():raise ValueError('Not a fresh staged checkout: '+str(target))
            target.write_text(header+fragment)
            created.append({'kind':'asm','path':path,'start':cur,'end':base+size})
        if created[0]['start']!=base or created[-1]['end']!=base+size or any(a['end']!=b['start'] for a,b in zip(created,created[1:])):
            raise ValueError('Noncontiguous staged source: '+filename)
        needle=f'        build/japan_0/asm/japan_0/{filename}.o(.text);'
        if script.count(needle)!=1:raise ValueError('Original linker ownership lost: '+filename)
        if not filename.startswith('main_'):
            n=list(re.finditer(r'(?m)^    \.file_(\d+) ',script[:script.index(needle)]))[-1].group(1)
            line=re.compile(r'(\.file_'+n+r' [^\n]+)SUBALIGN\(16\)')
            if re.search(r'\.file_'+n+r' [^\n]+SUBALIGN\(4\)',script) is None:
                script,count=line.subn(r'\1SUBALIGN(4)',script)
                if count!=1:raise ValueError('Could not pin per-overlay text alignment: '+n)
        replacement='\n'.join(f"        build/japan_0/{p['path']}.o(.text);" for p in created)
        script=script.replace(needle,replacement)
        prefix=f'build/japan_0/asm/japan_0/{filename}.o('
        occurrences=script.count(prefix)
        if filename.startswith('main_'):
            if occurrences>3:raise ValueError('Unexpected main linker section references')
        elif occurrences!=3:raise ValueError('Unexpected overlay data/rodata/bss references')
        script=script.replace(prefix,f"build/japan_0/{created[0]['path']}.o(")
        parts.extend(created)
        cparts.extend(p for p in created if p['kind']=='c')
    if len(cparts)!=290 or sum(p['end']-p['start'] for p in cparts)!=3264:
        raise ValueError('Incomplete JP stub transfer')
    ld.write_text(script)
    stage_data={'format':'goemon-japan-noop-local-stage-v1','region':'japan_0',
                'new_c':len(cparts),'new_bytes':3264,'parts':parts}
    stage_path.parent.mkdir(parents=True,exist_ok=True)
    if stage_path.exists():raise ValueError('Stage proof exists; require fresh staging')
    stage_path.write_text(json.dumps(stage_data,indent=2)+'\n')
    return stage_data


def c_files(stage_data:dict) -> str:
    wrapper=BASE_BUILD.read_text()
    match=re.search(r"(?m)^C_FILES='([^']+)'",wrapper)
    if not match:raise ValueError('Original 39-C prerequisite C_FILES list changed')
    base_c=match.group(1).split()
    if len(base_c)!=35:raise ValueError('Original 39-C prerequisite is not 35 C units')
    return ' '.join(base_c+[p['path'] for p in stage_data['parts'] if p['kind']=='c'])


def env_for(deps:Path,runtime:Path) -> dict:
    env=os.environ.copy()
    env.update(PYTHONHOME=str(runtime/'python'),
               PYTHONPATH=str(deps/'.venv/lib/python3.12/site-packages'),
               LD_LIBRARY_PATH=str(runtime/'lib')+(':'+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else ''),
               PATH=str(deps/'bin')+':'+env['PATH'])
    return env


def build(checkout:Path,m:dict,stage_path:Path,deps:Path,runtime:Path,jobs:int=8) -> dict:
    checkout=checkout.resolve(strict=True)
    rom=original_image(checkout)
    stage_data=json.loads(stage_path.read_text())
    if stage_data['new_c']!=290 or stage_data['new_bytes']!=3264:raise ValueError('Untrusted stage metadata')
    env=env_for(deps,runtime)
    objects=[f"build/japan_0/{p['path']}.o" for p in stage_data['parts']]
    common=['make',f'-j{jobs}','VERSION=japan_0','C_FILES='+c_files(stage_data)]
    subprocess.run([*common,*objects],cwd=checkout,env=env,check=True)
    packed=[]
    for p in stage_data['parts']:
        obj=checkout/f"build/japan_0/{p['path']}.o"
        expected_size=p['end']-p['start']
        _,size,code,alignment=text_section(obj)
        if size not in (expected_size,(expected_size+15)&~15):
            raise ValueError('Unexpected original object text extent: '+str(obj))
        if p['kind']=='c':
            if code[:expected_size] != rom[p['start']:p['end']]:
                raise ValueError('Candidate C machine instructions differ: '+p['name'])
            if digest(code[:expected_size])!=FORM[p['form']]['code_sha256']:
                raise ValueError('Candidate native IDO source signature differs: '+p['name'])
            out=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-r','-j','.text',str(obj)],env=env,text=True)
            if 'R_MIPS' in out:raise ValueError('Unexpected C .text relocation: '+p['name'])
            source=(checkout/p['path']).read_bytes()
            if digest(source)!=p['source_sha256'] or source!=source_text(p['name'],p['form']).encode():
                raise ValueError('Unexpected original C source content: '+p['name'])
        if alignment==4 and size==expected_size:
            preserved='already_exact'
        else:
            updated,proof=pack_text_metadata(obj.read_bytes(),expected_size)
            obj.write_bytes(updated)
            preserved=proof['relocations_preserved']
        _,actual_sz,packed_code,actual_align=text_section(obj)
        if actual_sz!=expected_size or actual_align!=4 or (p['kind']=='c' and packed_code!=rom[p['start']:p['end']]):
            raise ValueError('Staged native C or assembly section alignment/size drift: '+p['path'])
        packed.append({'path':p['path'],'size':actual_sz,'relocations_preserved':preserved})
    subprocess.run([*common,'build/japan_0/mnsg.z64'],cwd=checkout,env=env,check=True)
    result=(checkout/'build/japan_0/mnsg.z64').read_bytes()
    if result!=rom or sha1(result)!=baseline.SHA_EXPANDED:
        raise ValueError('Full expanded JP ROM does not match original')
    retail=checkout/'build/japan_0/mnsg.noop-port-329.retail.z64'
    subprocess.run([str(runtime/'python/bin/python3.12'),'tools/rommy.py','compress',
        '--input','build/japan_0/mnsg.z64','--output',str(retail),'--manifest','config/japan_0/rommy.yaml',
        '--pad','--verify'],cwd=checkout,env=env,check=True)
    if retail.read_bytes()!=baseline.read_image(checkout/'config/japan_0/baserom.z64',baseline.SHA_RETAIL,0x1000000):
        raise ValueError('Full rebuilt JP retail ROM does not match original')
    return {'packed':len(packed),'candidate_c':290,'expanded_rom_sha1':sha1(result),
            'retail_rom_sha1':sha1(retail.read_bytes()),'retail':str(retail)}


def verify(checkout:Path,m:dict,stage_path:Path,retail:Path,deps:Path,runtime:Path,readelf:str='readelf') -> dict:
    checkout=checkout.resolve(strict=True)
    original=original_image(checkout)
    built=baseline.read_image(checkout/'build/japan_0/mnsg.z64',baseline.SHA_EXPANDED,0x2000000)
    original16=baseline.read_image(checkout/'config/japan_0/baserom.z64',baseline.SHA_RETAIL,0x1000000)
    built16=baseline.read_image(retail,baseline.SHA_RETAIL,0x1000000)
    if original!=built or original16!=built16 or retail.resolve()==(checkout/'config/japan_0/baserom.z64').resolve():
        raise ValueError('JP retail and expanded ROM gate failed')
    stage_data=json.loads(stage_path.read_text())
    if stage_data['new_c']!=290 or stage_data['new_bytes']!=3264 or len(stage_data['parts'])!=561:
        raise ValueError('Unreviewed stage manifest')
    expected_records={name:(int(name.split('_')[1],16),FORM[form]['size'],form) for parent in m['parents'] for name,form in parent['c']}
    env=env_for(deps,runtime)
    observed={}
    for part in stage_data['parts']:
        length=part['end']-part['start']
        obj=checkout/f"build/japan_0/{part['path']}.o"
        _,sz,code,align=text_section(obj)
        if sz!=length or align!=4 or (part['kind']=='c' and code!=original[part['start']:part['end']]):
            raise ValueError('Original JP C code or assembly fragment section extent/alignment drift: '+str(obj))
        if part['kind']=='c':
            name=part['name'];form=part['form']
            if name in observed or name not in expected_records:raise ValueError('Unexpected C: '+name)
            off=int(name.split('_')[-1],16)
            if (off,length,form)!=(part['start'],FORM[form]['size'],form):raise ValueError('Function metadata mismatch: '+name)
            source=(checkout/part['path']).read_bytes()
            if source!=source_text(name,form).encode() or digest(source)!=part['source_sha256'] or digest(code)!=FORM[form]['code_sha256']:
                raise ValueError('Source or compiled original instruction mismatch: '+name)
            sym=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-t',str(obj)],text=True,env=env)
            ident=re.compile(r'^\s*[0-9A-Fa-f]{8}\s+g\s+F\s+\.text\s+([0-9A-Fa-f]+)\s+'+re.escape(name)+r'\s*$',re.M)
            match=ident.search(sym)
            if not match or int(match.group(1),16)!=length:
                raise ValueError('C original function object symbol mismatch: '+name)
            observed[name]=expected_records[name]
    if observed!=expected_records:raise ValueError('Missing source/object ownership: '+str(sorted(expected_records.keys()-observed.keys())[:5]))
    elf=checkout/'build/japan_0/mnsg.elf'
    out=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-t',str(elf)],text=True,env=env)
    funcs={};marked=set();sections=set()
    for line in out.splitlines():
        match=baseline.F_SYMBOL.fullmatch(line)
        if not match:continue
        addr,kind,sec,size,name=match.groups()
        if sec not in ('.main','.entry','.ipl3') and not re.fullmatch(r'\.file_\d+',sec):continue
        if kind=='F' and int(size,16)>0:
            if name in funcs:raise ValueError('Duplicate positive function identity: '+name)
            funcs[name]=(sec,int(addr,16),int(size,16));sections.add(sec)
        elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
    base=json.loads(BASE_MANIFEST.read_text())
    previously={f['name']:(f['vram'],f['size']) for unit in base['units'] for f in unit['functions']}
    if len(previously)!=39 or sum(sz for _,sz in previously.values())!=2092:
        raise ValueError('Invalid baseline C records')
    for name,(vram,size) in previously.items():
        if funcs.get(name)!=('.main',vram,size):raise ValueError('Previously accepted JP C drift: '+name)
    for name,(vram,size,form) in expected_records.items():
        expected_sec='.main' if any(name in [x[0] for x in p['c']] and p['asm'].startswith('main_') for p in m['parents']) else None
        result=funcs.get(name)
        if result is None or result[1:]!=(vram,size) or (expected_sec and result[0]!=expected_sec) or (not expected_sec and not result[0].startswith('.file_')):
            raise ValueError('Ported JP C ELF address/section drift: '+name)
    unmarked=set(funcs)-marked
    if unmarked!=(set(previously)|set(expected_records)):
        raise ValueError('Unexpected C/ASM ownership in final ELF: '+str(sorted(unmarked^(set(previously)|set(expected_records)))[:10]))
    if len(funcs)!=EXPECTED_FUNCTIONS or len(marked&funcs.keys())!=EXPECTED_FUNCTIONS-329 or len(sections)!=73:
        raise ValueError('Original 7,376 positive-sized ELF functions or 73 sections changed')
    ident_hash=digest(('\n'.join(f'{name}|{sec}|{vma:08x}|{size:08x}' for name,(sec,vma,size) in sorted(funcs.items()))+'\n').encode())
    if ident_hash!=m['original_elf_func_sha256']:
        raise ValueError('All-original function identity hash changed')
    r=subprocess.check_output([readelf,'-r','-W',str(elf)],text=True,env=env)
    sec='';normalized=[]
    for line in r.splitlines():
        group=re.search(r"^Relocation section '([^']+)'",line)
        if group:sec=group[1];continue
        match=re.match(r'^\s*([0-9a-fA-F]{8,16})\s+([0-9a-fA-F]{8})\s+(R_MIPS_[A-Z0-9_]+)\s+([0-9a-fA-F]{8,16})\s+(\S+)',line)
        if match:
            offset,info,kind,value,name=match.groups()
            normalized.append((sec,int(offset,16),kind,int(value,16),name))
    reloc_hash=digest(('\n'.join(f'{sec}|{offset:08x}|{kind}|{value:08x}|{name}' for sec,offset,kind,value,name in sorted(normalized))+'\n').encode())
    if len(normalized)!=EXPECTED_RELOCS or reloc_hash!=m['original_semantic_relocations_sha256']:
        raise ValueError('Japanese original relocation identities changed')
    return {'format':'goemon-japan-329-native-original-c-v1','status':'PASSED_G2','region':'japan_0',
            'upstream_commit':baseline.PINNED,'baseline_c_functions':39,'new_c_functions':290,
            'new_c_bytes':3264,'matching_c_functions':329,'matching_c_bytes':5356,
            'remaining_assembly_functions':7047,'c_translation_units':35+290,
            'original_elf_function_count':len(funcs),'original_elf_function_identity_sha256':ident_hash,
            'original_semantic_relocations_count':len(normalized), 'semantic_relocations_sha256':reloc_hash,
            'elf_sections':len(sections),'expanded_rom':{'size':len(built),'sha1':sha1(built),'different_bytes':0},
            'retail_rom':{'size':len(built16),'sha1':sha1(built16),'different_bytes':0},
            'native_pc_runtime':'NOT RUN','emulator_gameplay':'NOT RUN'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=('stage','build','verify'))
    p.add_argument('--checkout',type=Path,required=True)
    p.add_argument('--manifest',type=Path,default=MANIFEST)
    p.add_argument('--stage-report',type=Path)
    p.add_argument('--deps',type=Path)
    p.add_argument('--runtime',type=Path)
    p.add_argument('--retail',type=Path)
    p.add_argument('--readelf',default='readelf')
    p.add_argument('--report',type=Path)
    p.add_argument('--jobs',type=int,default=8)
    a=p.parse_args(argv)
    m=load_manifest(a.manifest)
    record=a.stage_report or a.checkout/'build/japan_0/noop-port-stage.json'
    if a.action=='stage':
        result=stage(a.checkout,m,record)
        print(f"JAPAN staged: {result['new_c']} new C, {len(result['parts'])} split sources")
    elif a.action=='build':
        if not a.deps or not a.runtime:p.error('build requires --deps and --runtime')
        result=build(a.checkout,m,record,a.deps,a.runtime,a.jobs)
        print('JAPAN built:',json.dumps(result))
    else:
        if not a.deps or not a.runtime or not a.retail:p.error('verify requires --deps, --runtime and --retail')
        result=verify(a.checkout,m,record,a.retail,a.deps,a.runtime,readelf=a.readelf)
        if a.report:
            with a.report.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
        print('JAPAN 329-C PASSED_G2:',json.dumps({k:v for k,v in result.items() if k in ('status','matching_c_functions','matching_c_bytes','remaining_assembly_functions')}))
    return result

if __name__=='__main__':main()
