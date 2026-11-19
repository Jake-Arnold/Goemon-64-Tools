"""Independent original-address Japanese 18-C source, object, link and ROM gate.

No ROM copies are published. A candidate passes only if two full images match,
all C objects are reviewed, and the final ELF owns exactly the matching C entries.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from . import japan_eighteen_c as stage
from .japan_relocation_policy import verify_text_relocations, REVIEWED

ROOT=Path(__file__).resolve().parent
SHA_EXPANDED='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
SHA_RETAIL='9843ee979b5f6c80f5eda85df0baed9ae7c4e73b'
PINNED='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
F_SYMBOL=re.compile(r'^\s*([0-9a-fA-F]+)\s+[lg! ]\s+([FO])\s+(\.\S+)\s+([0-9a-fA-F]+)\s+(\S+)\s*$')
GLOBAL_SYMBOL=re.compile(r'^\s*([0-9a-fA-F]+)\s+g\s+F\s+\.text\s+([0-9a-fA-F]+)\s+(\S+)\s*$')


def read_image(path:Path, sha:str,size:int) -> bytes:
    data=path.read_bytes()
    if len(data)!=size or hashlib.sha1(data).hexdigest()!=sha:
        raise ValueError(f'Original or candidate Japanese ROM mismatch: {path}')
    return data


def verify(checkout:Path,retail:Path,manifest:dict,source_dir:Path=ROOT,
           objcopy:str='mips-linux-gnu-objcopy',objdump:str='mips-linux-gnu-objdump') -> dict:
    checkout=checkout.resolve(strict=True)
    retail=retail.resolve(strict=True)
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True).strip()!=PINNED:
        raise ValueError('Wrong pinned upstream source revision')
    if subprocess.run(['git','diff','--quiet'],cwd=checkout).returncode!=0:
        raise ValueError('Tracked upstream game source modified')
    if manifest.get('region')!='japan_0' or manifest.get('upstream_commit')!=PINNED:
        raise ValueError('Unexpected Japanese region or revision')
    if manifest.get('splat_candidate')!=str(stage.CONFIG):
        raise ValueError('Unreviewed source staging')
    expected_stage=stage.render_config((checkout/'config/japan_0/splat.yaml').read_text())
    if (checkout/stage.CONFIG).read_text()!=expected_stage:
        raise ValueError('Wrong Japanese Splat assembly/C segmentation')
    original32=read_image(checkout/'config/japan_0/baserom.decompressed.z64',SHA_EXPANDED,0x2000000)
    built32=read_image(checkout/'build/japan_0/mnsg.z64',SHA_EXPANDED,0x2000000)
    original16=read_image(checkout/'config/japan_0/baserom.z64',SHA_RETAIL,0x1000000)
    if retail==(checkout/'config/japan_0/baserom.z64').resolve():
        raise ValueError('Rebuilt retail cannot alias the original')
    built16=read_image(retail,SHA_RETAIL,0x1000000)
    if original32!=built32 or original16!=built16:
        raise ValueError('Game ROM images differ byte-for-byte')
    ld=(checkout/'.splat/japan_0/mnsg.ld').read_text()
    if ld.count('.main 0x80000450 : AT(main_ROM_START) SUBALIGN(4)')!=1:
        raise ValueError('Incorrect original-address linker subalignment')
    mapping=(checkout/'build/japan_0/mnsg.map').read_text()
    functions={};results=[]
    for unit in manifest['units']:
        source=source_dir/unit['source'];staged=checkout/unit['staged_source']
        from_source=source.read_bytes()
        if from_source!=staged.read_bytes() or hashlib.sha256(from_source).hexdigest()!=unit['source_sha256']:
            raise ValueError('C source ownership/content differs: '+unit['source'])
        obj=checkout/unit['object']
        with tempfile.TemporaryDirectory() as temp:
            extracted=Path(temp)/'text.bin'
            subprocess.run([objcopy,'--dump-section',f'.text={extracted}',str(obj)],check=True,capture_output=True)
            machine=extracted.read_bytes()
        if len(machine)!=unit['section_size'] or hashlib.sha256(machine).hexdigest()!=unit['section_sha256']:
            raise ValueError('IDO machine code hash/size mismatch: '+unit['object'])
        map_line=re.compile(r'(?m)^\s*\.text\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\s+'+re.escape(unit['object'])+r'\s*$')
        positions=map_line.findall(mapping)
        if positions!=[(f'{unit["vram"]:x}',f'{unit["section_size"]:x}')]:
            raise ValueError('Original address/size map entry mismatch: '+unit['object']+' '+str(positions))
        syms=subprocess.run([objdump,'-t',str(obj)],check=True,capture_output=True,text=True).stdout
        global_f={m.group(3):(int(m.group(1),16),int(m.group(2),16)) for line in syms.splitlines() if (m:=GLOBAL_SYMBOL.fullmatch(line))}
        expect={f['name']:(f['rom_offset']-unit['rom_offset'],f['size']) for f in unit['functions']}
        if global_f!=expect:
            raise ValueError('Unexpected IDO function symbols or sizes: '+unit['object']+' '+str(global_f))
        reloc=subprocess.run([objdump,'-r','-j','.text',str(obj)],check=True,capture_output=True,text=True).stdout
        count=verify_text_relocations(unit['source'],reloc)
        if unit['source'] not in REVIEWED:
            original_region=original32[unit['rom_offset']:unit['rom_offset']+unit['section_size']]
            if machine!=original_region:
                raise ValueError('Unrelocated C text differs from the original')
        for fn in unit['functions']:
            fnmap=re.compile(r'(?m)^\s*0x([0-9a-fA-F]+)\s+'+re.escape(fn['name'])+r'\s*$')
            entries=fnmap.findall(mapping)
            if [int(v,16) for v in entries]!=[fn['vram']]:
                raise ValueError('Linked function symbol at wrong VMA: '+fn['name'])
            if fn['name'] in functions:
                raise ValueError('Duplicate C claim: '+fn['name'])
            functions[fn['name']]=(fn['vram'],fn['size'])
        results.append({'object':unit['object'],'source_sha256':unit['source_sha256'],
                        'text_sha256':unit['section_sha256'],'size':len(machine),
                        'relocations':count,'functions':len(unit['functions']),'status':'PASS'})
    elf=checkout/'build/japan_0/mnsg.elf'
    listing=subprocess.run([objdump,'-t',str(elf)],check=True,capture_output=True,text=True).stdout
    gamefunctions={};markers=set();sections=set()
    for line in listing.splitlines():
        match=F_SYMBOL.fullmatch(line)
        if match is None:continue
        addr,kind,sec,sz,name=match.groups()
        if not (sec in ('.main','.entry','.ipl3') or re.fullmatch(r'\.file_\d+',sec)):
            continue
        if kind=='F' and int(sz,16)>0:
            gamefunctions[name]=(sec,int(addr,16),int(sz,16));sections.add(sec)
        elif kind=='O' and name.endswith('.NON_MATCHING'):
            markers.add(name[:-13])
    unmarked=set(gamefunctions)-markers
    if unmarked!=set(functions):
        raise ValueError('Unexpected C/assembly ownership in linked ELF: '+str(sorted(unmarked^set(functions))[:10]))
    for name,(vma,size) in functions.items():
        if gamefunctions[name]!=('.main',vma,size):
            raise ValueError('ELF function address/extent mismatch: '+name)
    if len(gamefunctions)!=7376 or len(gamefunctions.keys()&markers)!=7358:
        raise ValueError('ELF function inventory changed unexpectedly')
    result={'format':'goemon-japan-eighteen-native-original-build-v1',
            'upstream_commit':PINNED,'region':'japan_0','status':'PASS',
            'functions':len(functions),'matching_c_bytes':sum(v[1] for v in functions.values()),
            'translation_units':len(results),'assembly_marked_elf_entries':7358,
            'elf_positive_sized_entries':7376,'elf_sections':len(sections),
            'expanded_rom':{'bytes':len(built32),'sha1':SHA_EXPANDED,'different_bytes':0},
            'retail_rom':{'bytes':len(built16),'sha1':SHA_RETAIL,'different_bytes':0},
            'units':results,'native_pc_runtime':'NOT RUN','emulator_gameplay':'NOT RUN'}
    if (result['functions'],result['matching_c_bytes'],result['translation_units'],result['elf_sections'])!=(18,756,14,73):
        raise ValueError('Unexpected reviewed 18-C totals')
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checkout',type=Path,required=True)
    p.add_argument('--retail-output',type=Path,required=True)
    p.add_argument('--manifest',type=Path,default=ROOT/'regions/japan_0.json')
    p.add_argument('--source-dir',type=Path,default=ROOT)
    p.add_argument('--objcopy',default='mips-linux-gnu-objcopy')
    p.add_argument('--objdump',default='mips-linux-gnu-objdump')
    p.add_argument('--report',type=Path,required=True)
    args=p.parse_args(argv)
    report=verify(args.checkout,args.retail_output,json.loads(args.manifest.read_text()),
        args.source_dir,args.objcopy,args.objdump)
    with args.report.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print('JAPAN 18-C PASS: exact original 32/16 MiB ROMs and 18 original functions')

if __name__=='__main__':main()
