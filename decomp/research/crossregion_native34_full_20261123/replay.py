#!/usr/bin/env python3
"""Source-only original-SGI-IDO 5.3 isolated native replay; no original code is distributed.

Usage: python3 replay.py --usa-rom /private/usa-expanded.z64 --jp-rom /private/jp-expanded.z64 \
  --cc /private/mnsg/tools/ido-5.3/cc --objcopy /private/bin/mips-linux-gnu-objcopy \
  --ld /private/bin/mips-linux-gnu-ld --binutils-lib /private/runtime/lib --out /tmp/goemon-native34

ONLY reports isolated compiled-original-function code identity and per-function
linked original VMA for symbolic cases; this is NOT a regional full-ROM G2 proof.
"""
import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

VALID_HASHES={'usa':'6ea0ed71032ce08fc2745f412d84936382197494',
              'japan_0':'6f8745fecc3a5e7d4918c7a73353eb0726116ded'}
IDO_SHA256='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'


def digest(buf): return hashlib.sha256(buf).hexdigest()


def run_cmd(command, environment):
    p=subprocess.run([str(x) for x in command],env=environment,capture_output=True,
                     text=True,timeout=60)
    if p.returncode:
        raise RuntimeError('command failed (%s): %s' % (p.returncode,p.stderr[-1100:]))


def replay(record,root,args,roms,env):
    tag=record['region']+'_'+record['name'];work=args.out/tag
    work.mkdir(parents=True,exist_ok=True)
    offset=int(record['original_rom_offset'],16);size=record['original_instruction_bytes'];vma=int(record['original_vma'],16)
    original=roms[record['region']][offset:offset+size]
    if digest(original)!=record['original_code_sha256']:
        raise AssertionError('original ROM range fingerprint mismatch: '+tag)
    def compile_and_link(variant):
        source_path=root/record[variant+'_source_path'];source=source_path.read_bytes()
        if digest(source)!=record[variant+'_source_sha256']:
            raise AssertionError('source SHA-256 mismatch: '+str(source_path))
        c=work/(variant+'.c');c.write_bytes(source)
        obj=work/(variant+'.o');output=work/(variant+'.bin')
        run_cmd([args.cc,'-c','-G','0','-non_shared','-O2','-mips2',c,'-o',obj],env)
        if record['symbolic']:
            script=work/(variant+'.ld')
            script.write_text('SECTIONS {\n. = 0x%X;\n.text : SUBALIGN(4) { *(.text) }\n.data : { *(.data) }\n.bss : { *(.bss) }\n}\n'%vma)
            elf=work/(variant+'.elf')
            defs=['--defsym=%s=0x%X'%(k,v) for k,v in record['resolved_original_symbol_addresses'].items()]
            run_cmd([args.ld,'-EB','-m','elf32btsmip','-T',script,'-e',record['name'],*defs,'-o',elf,obj],env)
            run_cmd([args.objcopy,'-O','binary','-j','.text',elf,output],env)
        else:
            run_cmd([args.objcopy,'-O','binary','-j','.text',obj,output],env)
        return output.read_bytes()
    positive=compile_and_link('candidate');negative=compile_and_link('negative')
    match=len(positive)>=size and positive[:size]==original
    reject=len(negative)<size or negative[:size]!=original
    first_diff=next((i for i in range(0,size,4)
                     if positive[i:i+4]!=original[i:i+4]),None) if not match else None
    return {'region':record['region'],'name':record['name'],'size':size,
            'original_rom_offset':record['original_rom_offset'],
            'positive_compiled_code_SHA256':digest(positive[:size]),
            'target_original_code_SHA256':digest(original),
            'positive_native_exact':match,'negative_control_rejected':reject,
            'first_differing_word_offset':first_diff,
            'linked_symbolic_original_vma':bool(record['symbolic']),
            'full_original_rom_G2':'NOT_RUN','new_canonical_accepted_C':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--usa-rom',type=Path,required=True)
    parser.add_argument('--jp-rom',type=Path,required=True)
    parser.add_argument('--cc',type=Path,required=True)
    parser.add_argument('--objcopy',type=Path,required=True)
    parser.add_argument('--ld',type=Path,required=True)
    parser.add_argument('--binutils-lib',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    a=parser.parse_args()
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'manifest.json').read_text())
    assert digest(a.cc.read_bytes())==IDO_SHA256,'Original SGI IDO 5.3 compiler SHA mismatch'
    roms={}
    for region,path in [('usa',a.usa_rom),('japan_0',a.jp_rom)]:
        b=path.read_bytes()
        if len(b)!=33554432 or hashlib.sha1(b).hexdigest()!=VALID_HASHES[region]:
            raise AssertionError('original '+region+' ROM SHA-1/size mismatch')
        roms[region]=b
    env={**os.environ,'LD_LIBRARY_PATH':str(a.binutils_lib)+(':'+os.environ['LD_LIBRARY_PATH'] if 'LD_LIBRARY_PATH' in os.environ else '')}
    results=[]
    for item in manifest['functions']:
        result=replay(item,root,a,roms,env)
        print(result['region'],result['name'],'PASS' if result['positive_native_exact'] and result['negative_control_rejected'] else 'FAIL',flush=True)
        results.append(result)
    good=sum(z['positive_native_exact'] and z['negative_control_rejected'] for z in results)
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'replay_results.json').write_text(json.dumps({'tested':len(results),'exact_with_negative_controls':good,'results':results},indent=2)+'\n')
    print('ISOLATED_NATIVE_EXACT_REPLAY:',good,'/',len(results))
    raise SystemExit(0 if good==len(results) else 1)
if __name__=='__main__': main()
