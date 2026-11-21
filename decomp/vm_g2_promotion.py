"""Fail-closed Japan-only original-ROM promotion of two script VM C functions.

Stage onto an independently verified Japan2121 state (JP2118 + Start3). No
copyrighted original ASM, original ROM bytes, or proprietary IDO are published.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

from . import glitch_g2_promotion as previous
from . import japan_noop_port as jp329
from . import japan_thirtyfour_c as jp34
from . import japan_1686_promotion as jp1686
from . import overlay_crossregion47 as cross

ROOT=Path(__file__).resolve().parent
SOURCES=ROOT/'research/vm_g2_20261121/sources'
REGION='japan_0'
ORIG_SHA1='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
RELOC_COUNT=80747
RELOC_SHA='e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20'
OLD_C=2121
OLD_BYTES=112244
IDENTITIES=7376
TARGETS=(
    ('func_8003CC10_3D810',0x3D810,48,'jp_vm_resource_lookup.c','jp1686_044_000.s',
     'd8d2b77d788b7c450d9f78da5fba0f199bd725d70a2e3315025e81fe95c24960',
     '911d6fbdc6b9d123514051c49c714bee1ca02d33de8d688f0dbdb98889ac360d'),
    ('func_8003E2C4_3EEC4',0x3EEC4,44,'jp_vm_countdown.c','jp1686_045_009.s',
     '99569d89988f6db380aea636c466e17ffe61ce6d2556348dcf187501bef5ff24',
     '9152e34ebf1d4fac577d6f6c8120f6dee74e7c8615030573cc22014cbe5f584a'),
)

def digest(blob):return hashlib.sha256(blob).hexdigest()
def rom(checkout):
    p=checkout/'config/japan_0/baserom.decompressed.z64';b=p.read_bytes()
    if len(b)!=33554432 or hashlib.sha1(b).hexdigest()!=ORIG_SHA1:raise ValueError('FAILED_ROM: wrong original Japanese image identity')
    return b

def _prior(checkout):
    path=checkout/'build/japan_0/glitch-g2-stage.json'
    if not path.is_file():raise ValueError('Missing accepted Start3 native G2 stage')
    obj=json.loads(path.read_text())
    if len(obj.get('new_functions',[]))!=3 or {x['name'] for x in obj['new_functions']} != {
      'func_8001F580_20180','func_8001F610_20210','func_8003EE44_3FA44'}:
      raise ValueError('Drifted JP2121 Start3 stage')
    if json.loads((checkout/'build/japan_0/jp1686-stage.json').read_text()).get('candidate_count')!=1686:
      raise ValueError('Missing original JP2118 stage')
    return obj

def stage(checkout):
    checkout=Path(checkout).resolve();b=rom(checkout);_prior(checkout)
    if (checkout/'build/japan_0/mnsg.z64').read_bytes()!=b:raise ValueError('FAILED_ROM: baseline is not exact')
    report=checkout/'build/japan_0/vm-g2-stage.json'
    dest=checkout/'src/vm_g2'
    if dest.exists() or report.exists():raise ValueError('Duplicate or stale VM G2 stage')
    linker=checkout/'.splat/japan_0/mnsg.ld';ld=linker.read_text()
    new=[]
    for name,off,size,filename,owner,source_sha,code_sha in TARGETS:
        source=SOURCES/filename
        if not source.is_file() or digest(source.read_bytes())!=source_sha:
            raise ValueError('Unreviewed C source drift: '+filename)
        if digest(b[off:off+size])!=code_sha:raise ValueError('Original MIPS code drift: '+name)
        origasm=checkout/f'asm/japan_0/{owner}'
        s=origasm.read_text()
        if s.count(f'nonmatching {name}, 0x{size:X}')!=1 or s.count(f'nonmatching ')!=1:
            raise ValueError('Original owner changed or contains multiple functions: '+owner)
        if previous.asm_span(s)!=(off,off+size):raise ValueError('Original ASM extent drift: '+name)
        # Existing .bss/data owner link references are empty, not just ignored.
        previous.check_nontext(checkout/f'build/japan_0/asm/japan_0/{owner}.o')
        ref=f'build/japan_0/asm/japan_0/{owner}.o(.text);'
        replacement=f'build/japan_0/src/vm_g2/{filename}.o(.text);'
        if ld.count(ref)!=1 or replacement in ld:raise ValueError('Original linker owner missing/duplicate '+owner)
        ld=ld.replace(ref,replacement,1)
        for section in ('.data','.bss','.rodata','.sdata','.sbss'):
            extra=f'build/japan_0/asm/japan_0/{owner}.o({section});'
            if ld.count(extra)>1:raise ValueError('Unreviewed original section ownership '+owner)
            ld=ld.replace(extra,'')
        if f'build/japan_0/asm/japan_0/{owner}.o(' in ld:
            raise ValueError('Original ASM nontext owner retained unexpectedly '+owner)
        new.append({'name':name,'rom_offset':off,'vma':int(name.split('_')[1],16),
             'size':size,'source':f'src/vm_g2/{filename}','source_sha256':source_sha,
             'original_code_sha256':code_sha,'owner':owner})
    dest.mkdir(parents=True)
    for entry in new:
        filename=Path(entry['source']).name
        (dest/filename).write_bytes((SOURCES/filename).read_bytes())
    linker.write_text(ld)
    payload={'format':'goemon-jp-vm-two-original-g2-stage-v1','region':REGION,
            'baseline_c':OLD_C,'prior_start_stage':3,'prior_native_batch':1686,
            'original_rom_sha1':ORIG_SHA1,'functions':new}
    report.write_text(json.dumps(payload,indent=2)+'\n')
    return payload

def build(checkout,deps,runtime):
    checkout=Path(checkout).resolve();rom(checkout);_prior(checkout)
    report=json.loads((checkout/'build/japan_0/vm-g2-stage.json').read_text())
    rows=report['functions'];names={x['name'] for x in rows}
    if names!={x[0] for x in TARGETS}:raise ValueError('Missing staged VM C function')
    env=jp329.env_for(Path(deps).resolve(),Path(runtime).resolve())
    pre=json.loads((checkout/'build/japan_0/glitch-g2-stage.json').read_text())
    prior_sources=[x['source'] for x in pre['new_functions']]
    plan={'new_functions':[{'source':x} for x in prior_sources]+[{'source':x['source']} for x in rows]}
    cmd=previous.makeargs(checkout,REGION,plan)
    for e in rows:
        source=checkout/e['source'];obj=checkout/f'build/japan_0/{e["source"]}.o'
        if digest(source.read_bytes())!=e['source_sha256']:raise ValueError('Staged source SHA drift')
        if obj.exists():obj.unlink()
        subprocess.run(cmd+[str(obj.relative_to(checkout))],cwd=checkout,env=env,check=True,
                       stdout=subprocess.DEVNULL)
        _old,n,c,align=jp329.text_section(obj)
        expected=e['size']
        if n not in (expected, (expected+15)&~15) or align not in (4,16):
            raise ValueError('Native IDO source size/alignment mismatch '+e['name']+f' {n}/{align} vs {expected}')
        if n!=expected or align!=4:
            obj.write_bytes(jp34.pack_text_metadata(obj.read_bytes(),expected)[0])
        _,n,c,align=jp329.text_section(obj)
        if n!=expected or align!=4:raise ValueError('Native object extent after padding-only fix changed')
        sym=subprocess.check_output(['readelf','-Ws',str(obj)],env=env,text=True)
        matches=[]
        for l in sym.splitlines():
            q=l.split()
            if len(q)>7 and q[3]=='FUNC' and q[7]==e['name'] and q[6] not in ('UND','ABS'):
                matches.append((int(q[1],16),int(q[2])))
        if matches != [(0,expected)]:raise ValueError('Original symbol name/function extent mismatch '+str(matches))
    for n in ('mnsg.elf','mnsg.z64'):
        p=checkout/'build/japan_0'/n
        if p.exists():p.unlink()
    subprocess.run(cmd+['build/japan_0/mnsg.z64'],cwd=checkout,env=env,check=True,
                   stdout=subprocess.DEVNULL)
    image=(checkout/'build/japan_0/mnsg.z64').read_bytes()
    if image!=rom(checkout):raise ValueError('FAILED_ROM: rebuilt ROM differs from authentic 32 MiB reference')
    payload={'format':'goemon-jp-vm2-g2-built-v1','status':'FULL_ROM_BYTE_IDENTICAL',
             'original_sha1':ORIG_SHA1,'original_rom_bytes':len(image),'functions':rows}
    (checkout/'build/japan_0/vm-g2-built.json').write_text(json.dumps(payload,indent=2)+'\n')
    return payload

def verify(checkout,baseline):
    checkout=Path(checkout).resolve();baseline=Path(baseline).resolve()
    b=rom(checkout)
    if b!=(checkout/'build/japan_0/mnsg.z64').read_bytes() or b!=(baseline/'build/japan_0/mnsg.z64').read_bytes():
        raise ValueError('FAILED_ROM: baseline/new rebuilt image not exact')
    oldelf=baseline/'build/japan_0/mnsg.elf';newelf=checkout/'build/japan_0/mnsg.elf'
    oldf=cross._funcs(oldelf);newf=cross._funcs(newelf)
    if oldf!=newf or sum(newf.values())!=IDENTITIES:raise ValueError('Original ELF identities changed')
    oldrel,oldn,oldh=previous.all_semantic_relocations(oldelf)
    newrel,newn,newh=previous.all_semantic_relocations(newelf)
    if oldn!=RELOC_COUNT or newn!=RELOC_COUNT or oldh!=RELOC_SHA or newh!=RELOC_SHA or oldrel!=newrel:
        raise ValueError('FAILED_RELOC: original full semantic relocation records drifted')
    stage=json.loads((checkout/'build/japan_0/vm-g2-stage.json').read_text())
    rows=stage['functions']
    if len(rows)!=len(TARGETS):raise ValueError('Stage rows drifted')
    def classified(elf):
        out=subprocess.check_output(['mips-linux-gnu-objdump','-t',str(elf)],text=True)
        funcs={};marked=set()
        for line in out.splitlines():
            m=jp1686.jp39.F_SYMBOL.fullmatch(line)
            if not m:continue
            addr,kind,sec,size,name=m.groups()
            if sec not in ('.main','.entry','.ipl3') and not re.fullmatch(r'\.file_\d+',sec):continue
            if kind=='F' and int(size,16)>0:funcs[name]=(sec,int(addr,16),int(size,16))
            elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
        return set(funcs)-marked
    before=classified(oldelf);after=classified(newelf)
    expected={x['name'] for x in rows}
    if len(before)!=OLD_C or len(after)!=OLD_C+2 or (after-before)!=expected or before-after:
        raise ValueError(f'FAILED_INVENTORY: old={len(before)} new={len(after)} +{after-before} -{before-after}')
    for row in rows:
        if digest((checkout/row['source']).read_bytes())!=row['source_sha256']:
            raise ValueError('Promoted C source mutated: '+row['name'])
        off=row['rom_offset'];size=row['size']
        if digest(b[off:off+size])!=row['original_code_sha256']:
            raise ValueError('Original instruction extent digest differed')
    proof={'format':'goemon-jp-vm-two-full-original-g2-v1','acceptance_tier':'PASSED_G2_LOCAL',
        'region':'japan_0','full_original_rom_bytes':len(b),
        'original_rom_sha1':ORIG_SHA1,'original_elf_function_identities':IDENTITIES,
        'semantic_relocations':newn,'semantic_relocation_sha256':newh,
        'prior_matching_c_functions':OLD_C,'new_matching_c_functions':2,
        'matching_c_functions':OLD_C+2,'prior_matching_c_bytes':OLD_BYTES,
        'new_c_bytes':sum(x['size'] for x in rows),
        'matching_c_instruction_bytes':OLD_BYTES+sum(x['size'] for x in rows),
        'assembly_remaining':IDENTITIES-OLD_C-2,'new_functions':rows,
        'gameplay':'NOT_RUN'}
    (checkout/'build/japan_0/vm-g2-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
    return proof

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=('stage','build','verify'))
    p.add_argument('--checkout',type=Path,required=True)
    p.add_argument('--baseline',type=Path)
    p.add_argument('--deps',type=Path)
    p.add_argument('--runtime',type=Path)
    args=p.parse_args()
    if args.action=='stage':res=stage(args.checkout)
    elif args.action=='build':
        if args.deps is None or args.runtime is None:p.error('--deps and --runtime required for build')
        res=build(args.checkout,args.deps,args.runtime)
    else:
        if args.baseline is None:p.error('--baseline required for verify')
        res=verify(args.checkout,args.baseline)
    print(json.dumps(res,indent=2))
if __name__=='__main__':main()
