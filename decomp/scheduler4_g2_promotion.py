"""Fail-closed USA task scheduler wrapper promotion after verified USA 1958.

This stage runs *after* the canonical 1956-C `decomp.verify` and independently
published Start-path +2 stage. It does not modify decomp matching accounting
unless every original-byte, ELF/relocation and strict-inventory gate passes.
Only non-instruction ELF section-padding metadata may be normalised.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess

from . import glitch_g2_promotion as glitch
from . import japan_noop_port as jp329
from . import verify as decomp_verify
from .inventory import summarize_inventory

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'research/scheduler4_20261121/sources'
FIXTURE = ROOT / 'research/scheduler4_20261121/manifest.json'
FORMAT = 'goemon-usa-scheduler4-after-1958-v1'
SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
VMA_DELTA = 0x7FFFF400


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_fixture():
    data = json.loads(FIXTURE.read_text())
    if set(data) != {'format','rom_sha1','accepted_prior_count','accepted_prior_instruction_bytes','owner','functions'}:
        raise ValueError('Unreviewed scheduler4 fixture fields')
    if data['format'] != FORMAT or data['rom_sha1'] != SHA1 or data['accepted_prior_count'] != 1958 or data['accepted_prior_instruction_bytes'] != 84292 or data['owner'] != 'asm/usa/35280_wa61_01.s':
        raise ValueError('Unreviewed scheduler4 fixture identity')
    expected = (('func_80034DD8_359D8',0x359D8,48),('func_80034E08_35A08',0x35A08,48),('func_80034E38_35A38',0x35A38,48),('func_80034E68_35A68',0x35A68,48))
    if len(data['functions']) != 4:
        raise ValueError('Must contain exactly four distinct original functions')
    for i,(entry,(name,offset,size)) in enumerate(zip(data['functions'],expected)):
        if set(entry) != {'name','rom_offset','vma','size','source','source_sha256','original_code_sha256'}:
            raise ValueError('Unexpected scheduler4 source fields')
        if (entry['name'],entry['rom_offset'],entry['vma'],entry['size'],entry['source']) != (name,offset,offset+VMA_DELTA,size,f'goemon_sched4_{i:02}.c'):
            raise ValueError('Scheduler4 original identity drift')
        if any(not re.fullmatch('[0-9a-f]{64}',entry[k]) for k in ('source_sha256','original_code_sha256')):
            raise ValueError('Malformed scheduler4 hash')
        if digest((SOURCE/entry['source']).read_bytes())!=entry['source_sha256']:
            raise ValueError('Scheduler4 native C source changed')
    return data


def original_rom(checkout):
    p = Path(checkout)/'config/usa/baserom.decompressed.z64'
    data=p.read_bytes()
    if len(data)!=33554432 or hashlib.sha1(data).hexdigest()!=SHA1:
        raise ValueError('Wrong original USA decompressed ROM')
    return data


def relocs(path):
    raw=subprocess.check_output(['readelf','-rW',str(path)],text=True)
    counter=Counter(); section=''
    for line in raw.splitlines():
        if line.startswith('Relocation section '):section=line.split("'")[1]
        elif re.match(r'^\s*[0-9a-f]{8}\s+[0-9a-f]{8}\s+R_MIPS_',line):
            parts=line.split(); counter[(section,parts[0],parts[2],parts[3])]+=1
    return counter


def funcs(path):
    raw=subprocess.check_output(['readelf','-sW',str(path)],text=True)
    counter=Counter()
    for line in raw.splitlines():
        m=re.match(r'\s*\d+:\s+([0-9a-fA-F]{8})\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+(\S+)\s+(.+?)\s*$',line)
        if m and int(m[2]):counter[(m[4],int(m[1],16),int(m[2]),m[3])]+=1
    return counter


def shrink_zero_text_tail(path,size):
    b=bytearray(path.read_bytes())
    if b[:6]!=b'\x7fELF\x01\x02':raise ValueError('Not original big-endian 32-bit ELF')
    offset=struct.unpack_from('>I',b,0x20)[0]
    ent=struct.unpack_from('>H',b,0x2e)[0]
    num=struct.unpack_from('>H',b,0x30)[0]
    idx=struct.unpack_from('>H',b,0x32)[0]
    st=offset+ent*idx
    start=struct.unpack_from('>I',b,st+16)[0]
    for i in range(num):
        entry=offset+i*ent
        no=struct.unpack_from('>I',b,entry)[0]
        name=b[start+no:b.index(0,start+no)]
        if name==b'.text':
            fileoff, length=struct.unpack_from('>II',b,entry+16)
            if not size<=length<size+16 or any(b[fileoff+size:fileoff+length]):
                raise ValueError('Nonzero bytes or illegal section length in original native object')
            struct.pack_into('>I',b,entry+20,size)
            struct.pack_into('>I',b,entry+32,4)
            path.write_bytes(b)
            return
    raise ValueError('C object has no original text section')


def validate_before(checkout,entries):
    checkout=Path(checkout)
    rom=original_rom(checkout)
    if (checkout/'build/usa/mnsg.z64').read_bytes()!=rom:
        raise ValueError('Must begin from exact accepted USA 1958 ROM')
    proof_file=checkout/'build/usa/glitch-g2-proof.json'
    if not proof_file.exists():raise ValueError('Missing independently verified USA1958 proof')
    proof=json.loads(proof_file.read_text())
    if proof['matched_c_functions']!=1958 or proof['original_rom_sha1']!=SHA1 or proof['relocation_multiset_same'] is not True:
        raise ValueError('Incorrect predecessor USA1958 proof')
    existing={f['name'] for f in decomp_verify.claimed_functions(decomp_verify.load_manifest(ROOT/'manifest.json'))}
    existing.update(('func_8001F8B0_204B0','func_8001F940_20540'))
    for f in entries:
        if f['name'] in existing or digest(rom[f['rom_offset']:f['rom_offset']+f['size']])!=f['original_code_sha256']:
            raise ValueError('Previously accepted function or changed original code '+f['name'])
    return rom


def stage(checkout,prior):
    checkout=Path(checkout).resolve();prior=Path(prior).resolve()
    fixture=load_fixture();entries=fixture['functions']
    validate_before(checkout,entries)
    if prior.exists():raise ValueError('Pre-stage backup must not exist')
    (prior/'build/usa').mkdir(parents=True)
    for name in ('mnsg.elf','mnsg.z64'):
        shutil.copy2(checkout/'build/usa'/name,prior/'build/usa'/name)
    owner=checkout/fixture['owner'];text=owner.read_text()
    linker=checkout/'.splat/usa/mnsg.ld';ld=linker.read_text()
    marker='build/usa/asm/usa/35280_wa61_01.s.o(.text);'
    if ld.count(marker)!=1 or '.main 0x80000450 : AT(main_ROM_START) SUBALIGN(4)' not in ld:
        raise ValueError('Wrong original owner/linker context')
    head=text[:text.index('nonmatching ')]
    matches=[]
    for entry in entries:
        name,offset,size=entry['name'],entry['rom_offset'],entry['size']
        pattern=r'(?m)^nonmatching '+re.escape(name)+r', 0x30\s*.*?^endlabel '+re.escape(name)+r'\s*'
        match=re.search(pattern,text,re.S|re.M)
        if not match:raise ValueError('Target not still owned by original ASM: '+name)
        offsets=[int(i,16) for i in re.findall(r'/\* ([0-9a-fA-F]+) [0-9a-fA-F]+ [0-9a-fA-F]+ \*/',match.group(0))]
        if len(offsets)!=size//4 or offsets[0]!=offset or offsets[-1]!=offset+size-4:
            raise ValueError('Original target span changed: '+name)
        matches.append((match.start(),match.end(),entry))
    if matches!=sorted(matches):raise ValueError('Original function ordering changed')
    fragments=[];pieces=[];pos=0
    for i,(start,end,entry) in enumerate(matches):
        frag=f'35280_sched4_{i:02}.s'
        (checkout/'asm/usa'/frag).write_text((text[pos:start] if i==0 else head+text[pos:start]))
        fragments.append(frag)
        src=checkout/'src'/entry['source'];shutil.copy2(SOURCE/entry['source'],src)
        pieces.extend((f'build/usa/asm/usa/{frag}.o(.text);',f'build/usa/src/{entry["source"]}.o(.text);'))
        pos=end
    last=f'35280_sched4_{len(matches):02}.s'
    (checkout/'asm/usa'/last).write_text(head+text[pos:])
    fragments.append(last);pieces.append(f'build/usa/asm/usa/{last}.o(.text);')
    linker.write_text(ld.replace(marker,'\n'.join('        '+piece for piece in pieces)))
    plan={'format':FORMAT,'old_c_count':1958,'new_c_count':1962,'original_rom_sha1':SHA1,'functions':entries,'asm_fragments':fragments,'previous_elf_sha256':digest((prior/'build/usa/mnsg.elf').read_bytes())}
    outfile=checkout/'build/usa/scheduler4-stage.json'
    if outfile.exists():raise ValueError('Previous scheduler4 stage exists')
    outfile.write_text(json.dumps(plan,indent=2)+'\n')
    return plan


def build(checkout,deps,runtime):
    checkout=Path(checkout).resolve();fixture=load_fixture()
    plan=json.loads((checkout/'build/usa/scheduler4-stage.json').read_text())
    if plan['format']!=FORMAT or plan['functions']!=fixture['functions'] or plan['old_c_count']!=1958:
        raise ValueError('Stale or altered scheduler4 stage')
    env=jp329.env_for(Path(deps).resolve(),Path(runtime).resolve())
    def run(cmd):subprocess.run(cmd,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
    for frag in plan['asm_fragments']:
        opath=checkout/'build/usa/asm/usa'/(frag+'.o')
        run(['mips-linux-gnu-as','-no-pad-sections','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',str(opath),f'asm/usa/{frag}'])
    for entry in fixture['functions']:
        src=entry['source'];path=checkout/'src'/src
        if digest(path.read_bytes())!=entry['source_sha256']:
            raise ValueError('Staged native source changed '+src)
        obj=checkout/'build/usa/src'/(src+'.o')
        run(['make','-j4','VERSION=usa',f'build/usa/src/{src}.o'])
        shrink_zero_text_tail(obj,entry['size'])
    for name in ('mnsg.elf','mnsg.z64'):(checkout/'build/usa'/name).unlink(missing_ok=True)
    run(['make','-j4','VERSION=usa','build/usa/mnsg.z64'])
    rom=original_rom(checkout)
    if (checkout/'build/usa/mnsg.z64').read_bytes()!=rom:
        raise ValueError('FAILED_ROM: original USA full-ROM image differs')
    return {'full_rom_bytes':len(rom),'full_rom_sha1':SHA1,'new_c_count':4,'new_original_bytes':192}


def verify(checkout,prior,original):
    checkout=Path(checkout).resolve();prior=Path(prior).resolve();original=Path(original).resolve()
    fixture=load_fixture();entries=fixture['functions']
    rom=original_rom(checkout)
    if (checkout/'build/usa/mnsg.z64').read_bytes()!=rom or (prior/'build/usa/mnsg.z64').read_bytes()!=rom:
        raise ValueError('FAILED_ROM: staging changed original ROM')
    oldelf=prior/'build/usa/mnsg.elf';newelf=checkout/'build/usa/mnsg.elf'
    a,b=funcs(oldelf),funcs(newelf)
    if a!=b or sum(b.values())!=7376:raise ValueError('Original function identities/size changed')
    r1,r2=relocs(oldelf),relocs(newelf)
    if r1!=r2 or sum(r2.values())!=82103:raise ValueError('Original semantic relocation multiset changed')
    allsyms=subprocess.check_output(['mips-linux-gnu-objdump','-t',str(newelf)],text=True)
    for f in entries:
        if f['name']+'.NON_MATCHING' in allsyms or f['name']+'\n' not in allsyms:
            raise ValueError('Original C function still ASM or missing: '+f['name'])
        if digest(rom[f['rom_offset']:f['rom_offset']+f['size']])!=f['original_code_sha256']:
            raise ValueError('Original exact extent mismatched '+f['name'])
    source=decomp_verify.load_manifest(ROOT/'manifest.json')
    claims=[e['name'] for e in decomp_verify.claimed_functions(source)]
    claims+=['func_8001F8B0_204B0','func_8001F940_20540']+[e['name'] for e in entries]
    bl=(original/'build/usa/mnsg.elf')
    baseline_text=subprocess.check_output(['readelf','-Ws',str(bl)],text=True)
    candidate_text=subprocess.check_output(['readelf','-Ws',str(newelf)],text=True)
    inventory=summarize_inventory(baseline_text,candidate_text,claims)
    if inventory['newly_matching_c']!=1962 or inventory['remaining_assembly_entries']!=5401 or inventory['extra_positive_alias_entries']!=0:
        raise ValueError('Strict inventoried C/ASM count differs')
    result={'format':'goemon-usa-scheduler4-g2-v1','status':'PASSED_G2_LOCAL','region':'usa','accepted_before':1958,'new_functions':4,'original_instruction_bytes_added':192,
            'accepted_after':1962,'total_original_C_instruction_bytes':84484,'remaining_assembly_entries':5401,
            'rom_sha1':SHA1,'original_rom_bytes':len(rom),'elf_function_identities':7376,
            'semantic_relocations':82103,'all_relocations_equal':True,'inventory':inventory,'functions':entries}
    dest=checkout/'build/usa/scheduler4-proof.json';dest.write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['stage','build','verify']);p.add_argument('--checkout',type=Path,required=True)
    p.add_argument('--prior',type=Path);p.add_argument('--original',type=Path)
    p.add_argument('--deps',type=Path);p.add_argument('--runtime',type=Path)
    a=p.parse_args()
    if a.action=='stage':
        if not a.prior:p.error('stage requires --prior for immutable USA1958 ELF backup')
        result=stage(a.checkout,a.prior)
    elif a.action=='build':
        if not a.deps or not a.runtime:p.error('build requires --deps and --runtime')
        result=build(a.checkout,a.deps,a.runtime)
    else:
        if not a.prior or not a.original:p.error('verify requires --prior and --original')
        result=verify(a.checkout,a.prior,a.original)
    print(json.dumps({k:v for k,v in result.items() if k not in ('inventory','functions','asm_fragments')},indent=2))

if __name__=='__main__':main()
