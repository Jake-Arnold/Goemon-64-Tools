"""Rebuild pinned mnsg in new Linux/WSL checkouts and verify reconstructed C.

Requires an existing local pinned upstream clone, the user's retail ROM, uv,
make, GCC and MIPS binutils. Never resets/deletes a checkout or overwrites a
report. ROMs, generated assembly, binaries and logs belong in local research
storage, not Git. Does not deploy, launch a game or submit upstream patches.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent


def digest(data,algorithm='sha1'):
    return hashlib.new(algorithm,data).hexdigest()


def load_manifest(path):
    manifest=json.loads(Path(path).read_text(encoding='utf-8'))
    if manifest.get('format')!='goemon-matching-decomp-v1':raise ValueError('Unsupported manifest format')
    for key,length in (('upstream_commit',40),('retail_sha1',40),('decompressed_sha1',40)):
        if not re.fullmatch('[0-9a-f]{'+str(length)+'}',manifest.get(key,'')):raise ValueError('Invalid '+key)
    seen=set();ranges=[]
    if not manifest.get('units'):raise ValueError('No reconstructed units')
    for unit in manifest['units']:
        if not re.fullmatch('[a-z][a-z0-9_]*[.]c',unit['source']):raise ValueError('Unsafe source name')
        start,end=unit['rom_start'],unit['rom_end']
        if not 0<=start<end or start%4 or end%4:raise ValueError('Invalid unit bounds')
        ranges.append((start,end))
        previous=start
        for fn in unit['functions']:
            if not re.fullmatch('func_[0-9A-F]{8}_[0-9A-F]+',fn['name']) or fn['name'] in seen:
                raise ValueError('Invalid/duplicate function name')
            seen.add(fn['name']);offset,size=fn['rom_offset'],fn['size']
            if offset<previous or size<=0 or offset%4 or size%4 or offset+size>end:
                raise ValueError('Invalid/overlapping function bounds')
            if int(fn['name'].split('_')[2],16)!=offset:raise ValueError('Function ROM offset disagrees with symbol')
            if int(fn['name'].split('_')[1],16)!=offset+0x7FFFF400:raise ValueError('Function guest address disagrees with main mapping')
            previous=offset+size
    ranges.sort()
    if any(a[1]>b[0] for a,b in zip(ranges,ranges[1:])):raise ValueError('Overlapping units')
    return manifest


def apply_units(checkout,manifest,source_dir=ROOT):
    """Apply only to a newly cloned candidate; fail before writes on collisions."""
    checkout=Path(checkout);source_dir=Path(source_dir)
    config=checkout/'config/usa/splat.yaml'
    text=config.read_text(encoding='utf-8')
    copies=[]
    for unit in manifest['units']:
        anchor=unit['splat_original']
        if text.count(anchor)!=1:raise ValueError('Pinned assembly anchor missing/ambiguous: '+anchor)
        source=source_dir/unit['source'];destination=checkout/'src'/unit['source']
        if not source.is_file() or destination.exists():raise ValueError('Missing source or existing candidate source')
        if 'GLOBAL_ASM' in source.read_text(encoding='utf-8'):raise ValueError('Claimed C unit includes assembly placeholders')
        copies.append((source,destination));text=text.replace(anchor,unit['splat_replacement'])
    for source,destination in copies:shutil.copyfile(source,destination)
    config.write_text(text,encoding='utf-8',newline='\n')


def parse_symbols(text):
    symbols={}
    for line in text.splitlines():
        match=re.fullmatch(r'([0-9a-fA-F]+)\s+[A-Za-z]\s+(\S+)',line.strip())
        if match:symbols[match[2]]=int(match[1],16)
    return symbols


def compare_images(expected,candidate,manifest,symbols):
    if digest(expected)!=manifest['decompressed_sha1']:raise ValueError('Reference ROM identity mismatch')
    functions=[]
    for unit in manifest['units']:
        if unit['rom_end']>len(expected):raise ValueError('Unit extends outside reference ROM')
        for fn in unit['functions']:
            offset,size=fn['rom_offset'],fn['size']
            expected_address=int(fn['name'].split('_')[1],16)
            address=symbols.get(fn['name'])
            actual_offset=(address-0x7FFFF400) if address is not None else -1
            actual=candidate[actual_offset:actual_offset+size] if actual_offset>=0 else b''
            matched=(address==expected_address and len(actual)==size and
                     expected[offset:offset+size]==actual and fn['name']+'.NON_MATCHING' not in symbols)
            functions.append(dict(name=fn['name'],size=size,guest_address=f'0x{expected_address:08X}',
                rom_offset=f'0x{offset:X}',matched=matched,
                expected_sha256=digest(expected[offset:offset+size],'sha256'),
                candidate_sha256=digest(actual,'sha256')))
    full_match=len(expected)==len(candidate) and digest(candidate)==manifest['decompressed_sha1']
    return dict(full_rom_match=full_match,expected_sha1=digest(expected),candidate_sha1=digest(candidate),
        rom_size=len(candidate),matched_functions=sum(f['matched'] for f in functions),
        claimed_functions=len(functions),matched_function_bytes=sum(f['size'] for f in functions if f['matched']),
        functions=functions)


def run_build(args,manifest,report):
    if os.name=='nt':raise ValueError('Run the build verifier inside Linux/WSL, not native Windows')
    upstream=args.upstream.resolve();work=args.workdir.resolve()
    if work.exists():raise ValueError('Work directory already exists; choose a new path')
    if digest(args.retail_rom.read_bytes())!=manifest['retail_sha1']:raise ValueError('Retail ROM identity mismatch')
    def capture(command,cwd=None):
        return subprocess.check_output(command,cwd=cwd,text=True,stderr=subprocess.STDOUT).strip()
    if capture(['git','rev-parse','HEAD'],upstream)!=manifest['upstream_commit']:
        raise ValueError('Upstream checkout is not the pinned commit')
    for tool in ('git','make','gcc','mips-linux-gnu-as','mips-linux-gnu-ld','mips-linux-gnu-objcopy','mips-linux-gnu-nm'):
        if not shutil.which(tool):raise ValueError('Required tool unavailable: '+tool)
    uv=shutil.which(args.uv)
    if uv is None:raise ValueError('uv is unavailable')
    work.mkdir(parents=True)
    report.update(upstream_commit=manifest['upstream_commit'],retail_sha1=manifest['retail_sha1'],
        tool_versions={name:capture(command).splitlines()[0] for name,command in {
            'uv':[uv,'--version'],'gcc':['gcc','--version'],'assembler':['mips-linux-gnu-as','--version']}.items()})
    def logged(stage,command,cwd):
        report['stage']=stage
        with (work/(stage+'.log')).open('w',encoding='utf-8') as log:
            subprocess.run(command,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,check=True)
    baseline=work/'baseline';candidate=work/'candidate'
    logged('clone-baseline',['git','clone','--no-hardlinks',str(upstream),str(baseline)],work)
    logged('dependencies',[uv,'sync','--python','3.12','--frozen'],baseline)
    shutil.copyfile(args.retail_rom,baseline/'config/usa/baserom.z64')
    logged('baseline-setup',['make','setup','UV='+uv],baseline)
    logged('baseline-build',['make','-j'+str(args.jobs),'UV='+uv],baseline)
    expected=(baseline/'config/usa/baserom.decompressed.z64').read_bytes()
    baseline_image=(baseline/'build/usa/mnsg.z64').read_bytes()
    if digest(expected)!=manifest['decompressed_sha1'] or baseline_image!=expected:
        raise ValueError('Baseline does not rebuild byte-identically')
    report['baseline_sha1']=digest(baseline_image)
    logged('clone-candidate',['git','clone','--no-hardlinks',str(upstream),str(candidate)],work)
    apply_units(candidate,manifest)
    (candidate/'.venv').symlink_to(baseline/'.venv',target_is_directory=True)
    shutil.copyfile(args.retail_rom,candidate/'config/usa/baserom.z64')
    logged('candidate-setup',['make','setup','UV='+uv],candidate)
    logged('candidate-build',['make','-j'+str(args.jobs),'UV='+uv],candidate)
    symbols=parse_symbols(capture(['mips-linux-gnu-nm','-n','build/usa/mnsg.elf'],candidate))
    result=compare_images(expected,(candidate/'build/usa/mnsg.z64').read_bytes(),manifest,symbols)
    report['comparison']=result
    report['sources_sha256_lf']={unit['source']:digest((ROOT/unit['source']).read_bytes().replace(b'\r\n',b'\n'),'sha256')
                               for unit in manifest['units']}
    mapping=(candidate/'build/usa/mnsg.map').read_text()
    for unit in manifest['units']:
        object_name='build/usa/src/'+unit['source']+'.o'
        if not (candidate/object_name).is_file() or object_name not in mapping:
            raise ValueError('Reconstructed C object absent from link evidence')
    if not result['full_rom_match'] or result['matched_functions']!=result['claimed_functions']:
        raise ValueError('Candidate failed exact matching')
    report['stage']='complete';report['status']='matched'


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream',type=Path,required=True)
    parser.add_argument('--workdir',type=Path,required=True,help='New directory; never reused or deleted')
    parser.add_argument('--retail-rom',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True,help='New local/ignored JSON report')
    parser.add_argument('--uv',default='uv')
    parser.add_argument('--jobs',type=int,default=4)
    args=parser.parse_args(argv)
    if args.jobs<1:parser.error('--jobs must be positive')
    report=dict(format='goemon-matching-build-result-v1',started_utc=datetime.now(timezone.utc).isoformat(),status='failed')
    if args.report.resolve()==args.retail_rom.resolve():parser.error('Report must differ from ROM')
    try:
        # Reserve before any build changes. An existing report is never replaced.
        with args.report.open('x',encoding='utf-8') as output:
            try:run_build(args,load_manifest(ROOT/'manifest.json'),report)
            except (OSError,ValueError,subprocess.SubprocessError) as exc:report['error']=str(exc)
            finally:
                report['ended_utc']=datetime.now(timezone.utc).isoformat()
                json.dump(report,output,indent=2);output.write('\n')
    except OSError as exc:parser.exit(1,str(exc)+'\n')
    if report['status']!='matched':parser.exit(1,report.get('error','Build failed')+'\n')
    print(f'MATCH: {report["comparison"]["matched_functions"]} functions; whole-ROM SHA-1 {report["comparison"]["candidate_sha1"]}')


if __name__=='__main__':main()
