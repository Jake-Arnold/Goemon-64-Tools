"""USA→JP four nontrivial original-address C transfers with byte-exact native gates.

Requires privately supplied original ROMs and pinned upstream toolchain. Never
commits generated MIPS assembly, object files or ROM images.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from pathlib import Path
import hashlib
import json
import re
import subprocess

from . import japan_usa_equivalent_two_remaining as jp423
from . import japan_noop_port as jp329
from . import japan_thirtynine_verify as jp39
from .japan_thirtyfour_c import pack_text_metadata

HERE = Path(__file__).resolve().parent
MANIFEST = HERE/'regions/japan_0_grouped4.json'
STAGE = Path('build/japan_0/jp-grouped4-stage.json')
SOURCE1 = 'decomp/research/file11_three_isolated_20261117.c'
SOURCE2 = 'decomp/candidates/vector_cross.c'

def digest(data:bytes)->str: return hashlib.sha256(data).hexdigest()

def manifest() -> dict:
    m=json.loads(MANIFEST.read_text())
    keys=('format','region','upstream_commit','baseline_c','baseline_bytes','added_c','added_bytes','total_c','total_bytes','original_expanded_sha1','original_retail_sha1')
    expect=('goemon-japan-usa-grouped-c-port4-v1','japan_0',jp39.PINNED,423,9676,4,216,427,9892,jp39.SHA_EXPANDED,jp39.SHA_RETAIL)
    if tuple(m[k] for k in keys)!=expect:raise ValueError('JP 4-grouped manifest changed')
    if not jp423.manifest()['total_functions']==423:raise ValueError('Prior combined production missing')
    accepted={f['name'] for u in json.loads((HERE/'regions/japan_0.json').read_text())['units'] for f in u['functions']}
    accepted|={n for p in jp329.load_manifest()['parents'] for n,_ in p['c']}
    from . import japan_character_switch_four as jp333
    from . import japan_usa_equivalent_eleven as jp344
    from . import japan_usa_equivalent_36 as jp380
    from . import japan_usa_equivalent_four_more as jp384
    from . import japan_usa_equivalent_thirtyseven_more as jp421
    accepted|=jp333.EXPECTED_NAMES
    for module in [jp344,jp380,jp384,jp421,jp423]:
        accepted|={v['jp'] for v in module.manifest()['candidates']}
    if len(accepted)!=423:raise ValueError('Base JP 423-C identities changed')
    seen=set();total=0
    for x in m['candidates']:
        n=x['jp'];p=HERE.parent/x['source_path'];parent=x['original_parent']
        if n in seen or n in accepted or int(n.rsplit('_',1)[1],16)!=x['jp_rom'] or x['sz']%4:
            raise ValueError('Bad or duplicate JP original function '+n)
        if not x['source_path'].startswith('decomp/') or not p.resolve().is_relative_to(HERE.parent.resolve()):
            raise ValueError('Unsafe source path')
        if digest(p.read_bytes())!=x['source_sha256']:raise ValueError('USA source provenance changed '+n)
        if x['section'] not in ('file_11','file_12') or not parent.startswith('asm/japan_0/'):
            raise ValueError('Unreviewed original owner')
        if x['vma']!=int(n.split('_')[1],16):raise ValueError('Original VMA drift')
        seen.add(n);total+=x['sz']
    if len(seen)!=4 or total!=216:raise ValueError('Original C total drift')
    return m

def source_text(x:dict)->str:
    s=(HERE.parent/x['source_path']).read_text()
    n=x['usa']
    if x['source_path']==SOURCE1:
        if n=='func_801E7D78_5A3C88': t=s[s.index('float func_801E7D78_5A3C88'):]
        elif n=='func_801F23C8_5AE2D8': t=s[s.index('void func_801F23C8_5AE2D8'):s.index('float func_801E7D78_5A3C88')]
        elif n=='func_801F3AD0_5AF9E0': t=s[:s.index('void func_801F23C8_5AE2D8')]
        else: raise ValueError('Source 1 original symbol is unreviewed')
    elif x['source_path']==SOURCE2 and n=='func_8021A7E8_5D5CB8':t=s
    else:raise ValueError('Unreviewed USA C original source')
    if t.count(n)!=1:raise ValueError('Incorrect original function source')
    return t.replace(n,x['jp']).rstrip()+'\n'

def _owner_bounds(checkout:Path,owner:str)->tuple[int,int]:
    parts=json.loads((checkout/'build/japan_0/noop-port-stage.json').read_text())['parts']
    generated=[p for p in parts if p['path']==owner]
    if generated:
        if len(generated)!=1 or generated[0]['kind']!='asm':raise ValueError('Original ASM generation owner changed')
        start,end=generated[0]['start'],generated[0]['end']
    else:
        m=re.fullmatch(r'asm/japan_0/([0-9A-F]{5,7})\.s',owner)
        if not m:raise ValueError('Unrecognised original ASM owner '+owner)
        start=int(m[1],16)
        end=start+jp329.text_section(checkout/f'build/japan_0/{owner}.o')[1]
    _,size,_,_=jp329.text_section(checkout/f'build/japan_0/{owner}.o')
    if end-start!=size:raise ValueError('Original text owner size changed')
    return start,end

def stage(checkout:Path,m:dict):
    rom=jp329.original_image(checkout)
    ldpath=checkout/'.splat/japan_0/mnsg.ld';ld=ldpath.read_text()
    byowner=defaultdict(list)
    for x in m['candidates']:
        if digest(rom[x['jp_rom']:x['jp_rom']+x['sz']])!=x['code_sha256']:
            raise ValueError('Original JP ROM opcode mismatch '+x['jp'])
        byowner[x['original_parent']].append(x)
    parts=[]
    for ix,(owner,cs) in enumerate(sorted(byowner.items())):
        start,end=_owner_bounds(checkout,owner)
        asm=(checkout/owner).read_text();matches=list(jp329.BLOCK.finditer(asm))
        if not matches:raise ValueError('No original function signatures '+owner)
        definitions={m['name']:m for m in matches}
        header=asm[:matches[0].start()]
        cs.sort(key=lambda x:x['jp_rom']);cursor=start;pos=0;pieces=[]
        for x in cs:
            name=x['jp'];off=x['jp_rom'];sz=x['sz'];r=definitions.get(name)
            if r is None or int(r['size'],16)!=sz or off<cursor or off+sz>end:
                raise ValueError('Invalid candidate original ASM function extent '+name)
            if off>cursor:
                path=f'asm/japan_0/jpgroup_{ix:03}_{len(pieces):03}.s';fragment=asm[pos:r.start()]
                if not fragment.strip():raise ValueError('Expected original ASM gap '+name)
                (checkout/path).write_text(fragment if pos==0 else header+fragment)
                pieces.append({'kind':'asm','path':path,'start':cursor,'end':off})
            elif asm[pos:r.start()].strip() and not (pos==0 and asm[:r.start()]==header):
                raise ValueError('Original ASMs between adjacent code blocks')
            path=f'src/jp_grouped4/{name}.c';dest=checkout/path;dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():raise ValueError('Stale source '+path)
            contents=source_text(x);dest.write_text(contents)
            pieces.append({'kind':'c','path':path,'start':off,'end':off+sz,'name':name,'code_sha256':x['code_sha256'],'source_sha256':digest(contents.encode())})
            cursor=off+sz;pos=r.end()
        if cursor<end:
            path=f'asm/japan_0/jpgroup_{ix:03}_{len(pieces):03}.s'
            (checkout/path).write_text((asm[pos:] if pos==0 else header+asm[pos:]))
            pieces.append({'kind':'asm','path':path,'start':cursor,'end':end})
        if pieces[0]['start']!=start or pieces[-1]['end']!=end or any(a['end']!=b['start'] for a,b in zip(pieces,pieces[1:])):
            raise ValueError('Original source function/ASM extents noncontiguous')
        needle=f'        build/japan_0/{owner}.o(.text);'
        if ld.count(needle)!=1:raise ValueError('Original active linker ownership not unique: '+owner)
        sec_match=list(re.finditer(r'(?m)^    \.file_(\d+) ',ld[:ld.index(needle)]))[-1]
        sec=f'file_{sec_match.group(1)}'
        if any(x['section']!=sec for x in cs):raise ValueError('Overlay linker section changed '+owner)
        overlay_pat=r'(?m)^(    \.'+sec+r' [^\n]+)SUBALIGN\(16\)'
        ld,nchanged=re.subn(overlay_pat,r'\1SUBALIGN(4)',ld)
        if nchanged>1:raise ValueError('Unexpected linker overlay section count')
        ld=ld.replace(needle,'\n'.join(f"        build/japan_0/{p['path']}.o(.text);" for p in pieces))
        nontext_prefix=f'build/japan_0/{owner}.o('
        n=ld.count(nontext_prefix)
        if n not in (0,3):raise ValueError('Nontext relocation owner changed '+owner)
        if n:
            if pieces[0]['kind']!='asm':raise ValueError('Cannot preserve nontext owner')
            ld=ld.replace(nontext_prefix,f"build/japan_0/{pieces[0]['path']}.o(")
        parts.extend(pieces)
    if len([p for p in parts if p['kind']=='c'])!=4:raise ValueError('Stage must include four new C functions')
    ldpath.write_text(ld)
    result={'format':'goemon-japan-grouped4-stage-v1','new_c':4,'new_bytes':216,'parts':parts}
    if (checkout/STAGE).exists():raise ValueError('Stage already exists')
    (checkout/STAGE).write_text(json.dumps(result,indent=2)+'\n')
    return result

def full_c_list(checkout:Path,m:dict)->str:
    return jp423.full_c_list(checkout,jp423.manifest())+' '+' '.join(f"src/jp_grouped4/{x['jp']}.c" for x in m['candidates'])

def build(checkout:Path,deps:Path,runtime:Path,m:dict,jobs:int=4):
    original=jp329.original_image(checkout)
    stage=json.loads((checkout/STAGE).read_text())
    if stage['new_c']!=4 or stage['new_bytes']!=216:raise ValueError('Incorrect initial stage')
    env=jp329.env_for(deps,runtime)
    common=['make',f'-j{jobs}','VERSION=japan_0','C_FILES='+full_c_list(checkout,m)]
    objs=[f"build/japan_0/{p['path']}.o" for p in stage['parts']]
    subprocess.run(common+objs,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    cmap={x['jp']:x for x in m['candidates']}
    for p in stage['parts']:
        target=checkout/f"build/japan_0/{p['path']}.o"
        _,size,code,align=jp329.text_section(target);length=p['end']-p['start']
        if size not in (length,(length+15)&~15) or align not in (4,16):raise ValueError('Native translation-unit dimensions unexpected '+p['path'])
        if p['kind']=='c':
            x=cmap[p['name']];csrc=(checkout/p['path']).read_bytes()
            if digest(csrc)!=p['source_sha256'] or csrc.decode()!=source_text(x):raise ValueError('Source body changed '+p['name'])
            if code[:length]!=original[p['start']:p['end']]:raise ValueError('Original MIPS machine code mismatch '+p['name'])
            reloc=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-r','-j','.text',str(target)],text=True,env=env)
            if 'R_MIPS_' in reloc:raise ValueError('Unreviewed C native relocations '+p['name'])
        if size!=length or align!=4:target.write_bytes(pack_text_metadata(target.read_bytes(),length)[0])
        _,newsize,newcode,newalign=jp329.text_section(target)
        if newsize!=length or newalign!=4 or (p['kind']=='c' and newcode!=original[p['start']:p['end']]):
            raise ValueError('Packed original source extent mismatch '+p['path'])
    subprocess.run(common+['build/japan_0/mnsg.z64'],cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    if (checkout/'build/japan_0/mnsg.z64').read_bytes()!=original:raise ValueError('Expanded 32MiB JP ROM not original')
    retail=checkout/'build/japan_0/mnsg.equiv427.retail.z64'
    subprocess.run([str(runtime/'python/bin/python3.12'),'tools/rommy.py','compress','--input','build/japan_0/mnsg.z64','--output',str(retail),'--manifest','config/japan_0/rommy.yaml','--pad','--verify'],cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    if retail.read_bytes()!=jp39.read_image(checkout/'config/japan_0/baserom.z64',jp39.SHA_RETAIL,0x1000000):
        raise ValueError('Retail JP ROM not original')
    return retail

def verify(checkout:Path,deps:Path,runtime:Path,retail:Path,m:dict):
    reference=jp329.original_image(checkout)
    if jp39.read_image(checkout/'build/japan_0/mnsg.z64',jp39.SHA_EXPANDED,0x2000000)!=reference:raise ValueError('Expanded JP ROM identity failed')
    if jp39.read_image(retail,jp39.SHA_RETAIL,0x1000000)!=jp39.read_image(checkout/'config/japan_0/baserom.z64',jp39.SHA_RETAIL,0x1000000):raise ValueError('Retail JP ROM identity failed')
    env=jp329.env_for(deps,runtime)
    prior=json.loads((HERE/'regions/japan_0.json').read_text())
    elf=checkout/'build/japan_0/mnsg.elf'
    symbols=subprocess.check_output([str(deps/'bin/mips-linux-gnu-objdump'),'-t',str(elf)],text=True,env=env)
    funcs={};marked=set();sections=set()
    for line in symbols.splitlines():
        mat=jp39.F_SYMBOL.fullmatch(line)
        if not mat:continue
        a,kind,sec,size,name=mat.groups()
        if sec not in ('.main','.entry','.ipl3') and re.fullmatch(r'\.file_\d+',sec) is None:continue
        if kind=='F' and int(size,16)>0:
            if name in funcs:raise ValueError('Duplicate ELF original function identity')
            funcs[name]=(sec,int(a,16),int(size,16));sections.add(sec)
        elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
    baseline={f['name'] for u in prior['units'] for f in u['functions']}
    from . import japan_character_switch_four as jp333
    from . import japan_usa_equivalent_eleven as jp344
    from . import japan_usa_equivalent_36 as jp380
    from . import japan_usa_equivalent_four_more as jp384
    from . import japan_usa_equivalent_thirtyseven_more as jp421
    previous=baseline|{n for p in jp329.load_manifest()['parents'] for n,_ in p['c']}|jp333.EXPECTED_NAMES
    for x in [jp344,jp380,jp384,jp421,jp423]: previous|={y['jp'] for y in x.manifest()['candidates']}
    if len(previous)!=423:raise ValueError('Prior original ROM matched C not 423')
    expected=previous|{x['jp'] for x in m['candidates']}
    if len(expected)!=427 or set(funcs)-marked!=expected or len(funcs)!=7376 or len(marked&funcs.keys())!=6949 or len(sections)!=73:
        raise ValueError('Combined ELF function inventory failed')
    for x in m['candidates']:
        if funcs.get(x['jp'])!=(f".{x['section']}",x['vma'],x['sz']):
            raise ValueError('Original JP overlay ELF FUNC ownership mismatch '+x['jp'])
    ident=digest(('\n'.join(f'{n}|{s}|{v:08x}|{z:08x}' for n,(s,v,z) in sorted(funcs.items()))+'\n').encode())
    if ident!=prior['proven_original_elf_function_identities_sha256']:raise ValueError('Original positive ELF identities changed')
    out=subprocess.check_output(['readelf','-r','-W',str(elf)],text=True,env=env)
    sec='';records=[]
    for line in out.splitlines():
        g=re.search(r"^Relocation section '([^']+)'",line)
        if g:sec=g[1];continue
        q=re.match(r'^\s*([0-9a-fA-F]{8,16})\s+([0-9a-fA-F]{8})\s+(R_MIPS_[A-Z0-9_]+)\s+([0-9a-fA-F]{8,16})\s+(\S+)',line)
        if q:
            off,info,kind,val,name=q.groups();records.append((sec,int(off,16),kind,int(val,16),name))
    rel=digest(('\n'.join(f'{s}|{o:08x}|{k}|{v:08x}|{n}' for s,o,k,v,n in sorted(records))+'\n').encode())
    if len(records)!=80747 or rel!=prior['proven_original_semantic_relocations_sha256']:raise ValueError('Semantic relocation identities changed')
    return {'status':'PASSED_G2','region':'japan_0','baseline_c':423,'added_c':4,'added_instruction_bytes':216,'matching_c_functions':427,'matching_c_bytes':9892,'remaining_assembly_entries':6949,'original_elf_function_count':len(funcs),'original_elf_identity_sha256':ident,'semantic_relocations_count':len(records),'semantic_relocations_sha256':rel,'expanded_rom_sha1':jp39.SHA_EXPANDED,'retail_rom_sha1':jp39.SHA_RETAIL,'original_functions':[{'name':x['jp'],'rom_offset':f"0x{x['jp_rom']:X}",'size':x['sz']} for x in m['candidates']],'emulator_gameplay':'NOT_RUN'}

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
    m=manifest();c=args.checkout.resolve(strict=True)
    if args.action=='stage':res=stage(c,m)
    else:
        if not args.deps or not args.runtime:parser.error('Missing original native compiler inputs')
        if args.action=='build':res={'retail':str(build(c,args.deps,args.runtime,m,args.jobs))}
        else:
            if not args.retail:parser.error('Original JP retail output required')
            res=verify(c,args.deps,args.runtime,args.retail,m)
    if args.report:
        with args.report.open('x') as out:json.dump(res,out,indent=2);out.write('\n')
    print(json.dumps({k:v for k,v in res.items() if k not in ('parts','original_functions')},indent=2))
if __name__=='__main__':main()
