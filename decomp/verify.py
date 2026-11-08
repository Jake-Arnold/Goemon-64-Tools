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

try:
    from .elf_layout import pack_object_file, pack_heap_noop_file
    from .collision_patch import prepare_collision_gate
except ImportError:
    from elf_layout import pack_object_file, pack_heap_noop_file
    from collision_patch import prepare_collision_gate

ROOT = Path(__file__).resolve().parent

# The only accepted patch of an upstream-owned C translation unit. The staged
# source hash is from the reviewed LF-only integration; changed upstream context
# must be reviewed explicitly rather than relying on an ambiguous pragma match.
COLLISION_GATE_PATCH = {
    'source': '27FE0.c',
    'candidate_source': 'candidates/collision_gate.c',
    'patched_sha256_lf': 'b6ac4275ec56796e23482765a82d3fd15d8c44f7148cd31f7cf8eb9fa408ab63',
    'function': {'name': 'func_80029E08_2AA08', 'rom_offset': 0x2AA08, 'size': 80},
}


def claimed_functions(manifest):
    """All original-address verified C claims, including patched upstream C."""
    return [f for unit in manifest['units'] for f in unit['functions']] + [
        entry['function'] for entry in manifest.get('existing_source_patches', [])]



def digest(data,algorithm='sha1'):
    return hashlib.new(algorithm,data).hexdigest()


def load_manifest(path):
    manifest=json.loads(Path(path).read_text(encoding='utf-8'))
    if manifest.get('format')!='goemon-matching-decomp-v1':raise ValueError('Unsupported manifest format')
    for key,length in (('upstream_commit',40),('retail_sha1',40),('decompressed_sha1',40)):
        if not re.fullmatch('[0-9a-f]{'+str(length)+'}',manifest.get(key,'')):raise ValueError('Invalid '+key)
    seen=set();assembly_seen=set();ranges=[]
    if not manifest.get('units'):raise ValueError('No reconstructed units')
    if manifest.get('splat_options',{}) not in ({},{'asm_jtbl_label_macro':'glabel'}):
        raise ValueError('Unsupported Splat override')
    headers=manifest.get('support_headers',[])
    if len(headers)!=len(set(headers)) or any(not re.fullmatch('[a-z][a-z0-9_]*[.]h',name) for name in headers):
        raise ValueError('Invalid support header names')
    for unit in manifest['units']:
        if not re.fullmatch('[a-z][a-z0-9_]*[.]c',unit['source']):raise ValueError('Unsafe source name')
        start,end=unit['rom_start'],unit['rom_end']
        if not 0<=start<end or start%4 or end%4:raise ValueError('Invalid unit bounds')
        ranges.append((start,end))
        no_padding=unit.get('asm_no_padding',[])
        if len(no_padding)!=len(set(no_padding)) or any(not re.fullmatch('[0-9A-F]{4,5}',name) for name in no_padding):
            raise ValueError('Invalid assembly no-padding object name')
        previous=start
        for fn in unit['functions']:
            if not re.fullmatch('func_[0-9A-F]{8}_[0-9A-F]+',fn['name']) or fn['name'] in seen or fn['name'] in assembly_seen:
                raise ValueError('Invalid/duplicate function name')
            seen.add(fn['name']);offset,size=fn['rom_offset'],fn['size']
            if offset<previous or size<=0 or offset%4 or size%4 or offset+size>end:
                raise ValueError('Invalid/overlapping function bounds')
            if int(fn['name'].split('_')[2],16)!=offset:raise ValueError('Function ROM offset disagrees with symbol')
            if int(fn['name'].split('_')[1],16)!=offset+0x7FFFF400:raise ValueError('Function guest address disagrees with main mapping')
            previous=offset+size
        assembly=unit.get('assembly_functions',[])
        if len(set(assembly))!=len(assembly) or any(name in seen or name in assembly_seen or not re.fullmatch('func_[0-9A-F]{8}_[0-9A-F]+',name) for name in assembly):
            raise ValueError('Invalid/claimed assembly placeholder')
        for name in assembly:
            offset=int(name.split('_')[2],16)
            if not start<=offset<end or int(name.split('_')[1],16)!=offset+0x7FFFF400:
                raise ValueError('Assembly placeholder outside unit/mapping')
            if any(fn['rom_offset']<=offset<fn['rom_offset']+fn['size'] for fn in unit['functions']):
                raise ValueError('Assembly placeholder overlaps claimed C')
        assembly_seen.update(assembly)
    patches = manifest.get('existing_source_patches', [])
    if patches not in ([], [COLLISION_GATE_PATCH]):
        raise ValueError('Unsupported existing-source patch; manual layout review required')
    if patches:
        if manifest['upstream_commit'] != '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee':
            raise ValueError('Existing-source patch requires pinned upstream commit')
        fn = COLLISION_GATE_PATCH['function']
        if fn['name'] in seen or fn['name'] in assembly_seen:
            raise ValueError('Existing-source patch function already claimed')
        if any(start < fn['rom_offset']+fn['size'] and fn['rom_offset'] < end for start,end in ranges):
            raise ValueError('Existing-source patch overlaps migrated unit')
    ranges.sort()
    if any(a[1]>b[0] for a,b in zip(ranges,ranges[1:])):raise ValueError('Overlapping units')
    if 'heap_noop_text_layout' in manifest:
        if manifest['heap_noop_text_layout'] is not True or manifest['upstream_commit'] != '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee':
            raise ValueError('Unsupported empty-function layout preset')
        targets=[u for u in manifest['units'] if u['source']=='heap_noop.c']
        if len(targets)!=1 or targets[0] != dict(
            source='heap_noop.c', rom_start=0x36984, rom_end=0x3698C,
            splat_original='[0x36750, asm]',
            splat_replacement='[0x36750, asm]\n    - [0x36984, c, heap_noop]\n    - [0x3698C, asm]',
            asm_no_padding=['3698C'],
            functions=[dict(name='func_80035D84_36984',rom_offset=0x36984,size=8)]):
            raise ValueError('Pinned empty-function split mismatch')
    if 'vm_assignment_table_layout' in manifest:
        if manifest['vm_assignment_table_layout'] is not True:
            raise ValueError('Unsupported VM table layout preset')
        vm=[u for u in manifest['units'] if u['source']=='script_vm.c']
        if (manifest['upstream_commit']!='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee' or len(vm)!=1 or
            not any(f==dict(name='func_8003DB0C_3E70C',rom_offset=0x3E70C,size=224) for f in vm[0]['functions'])):
            raise ValueError('VM table layout requires pinned assignment handler')
    return manifest


def apply_units(checkout,manifest,source_dir=ROOT):
    """Apply only to a newly cloned candidate; fail before writes on collisions."""
    checkout=Path(checkout);source_dir=Path(source_dir)
    config=checkout/'config/usa/splat.yaml'
    text=config.read_text(encoding='utf-8')
    if manifest.get('splat_options'):
        if text.count('options:\n')!=1:raise ValueError('Missing/ambiguous Splat options anchor')
        text=text.replace('options:\n','options:\n  asm_jtbl_label_macro: glabel\n')
    makefile=None
    if manifest.get('vm_assignment_table_layout'):
        replacements={
            '    - [0x7B6F0, rodata, main_continued]':
            '    - [0x7B6F0, rodata, main_continued]\n    - [0x7DC2C, .rodata, script_vm]\n    - [0x7DC68, rodata, main_continued_after_vm_store]'}
        # Restrict subalignment to the pinned main segment only.
        main_start=text.index('    start: 0x1050')
        main_end=text.index('    subsegments:',main_start)
        header=text[main_start:main_end]
        if header.count('    subalign: 16')!=1:raise ValueError('Missing main subalignment anchor')
        text=text[:main_start]+header.replace('    subalign: 16','    subalign: 4')+text[main_end:]
        for before,after in replacements.items():
            if text.count(before)!=1:raise ValueError('Missing/ambiguous VM layout anchor')
            text=text.replace(before,after)
        makefile=(checkout/'Makefile').read_text(encoding='utf-8')
        makefile+='\n# Preserve the 4-byte-aligned prefix before the migrated VM table.\nbuild/usa/asm/usa/data/main_continued.rodata.s.o: ASFLAGS += --no-pad-sections\n'
    no_padding=[name for unit in manifest['units'] for name in unit.get('asm_no_padding',[])]
    if no_padding:
        if len(no_padding)!=len(set(no_padding)):raise ValueError('Duplicate assembly no-padding object')
        if makefile is None:makefile=(checkout/'Makefile').read_text(encoding='utf-8')
        makefile+='\n# Preserve exact lengths of assembly slices adjoining C functions.\n'
        for name in no_padding:
            makefile+=f'build/usa/asm/usa/{name}.s.o: ASFLAGS += --no-pad-sections\n'
    copies=[]
    for name in manifest.get('support_headers',[]):
        source=source_dir/name;destination=checkout/'src'/name
        if not source.is_file() or destination.exists():raise ValueError('Missing or existing support header')
        copies.append((source,destination))
    for unit in manifest['units']:
        anchor=unit['splat_original']
        if text.count(anchor)!=1:raise ValueError('Pinned assembly anchor missing/ambiguous: '+anchor)
        source=source_dir/unit['source'];destination=checkout/'src'/unit['source']
        if not source.is_file() or destination.exists():raise ValueError('Missing source or existing candidate source')
        text_source=source.read_text(encoding='utf-8')
        placeholders=re.findall(r'^#pragma GLOBAL_ASM\("[^"\n]*/(func_[0-9A-F_]+)\.s"\)',text_source,re.MULTILINE)
        if set(placeholders)!=set(unit.get('assembly_functions',[])) or text_source.count('GLOBAL_ASM')!=len(placeholders):
            raise ValueError('Undeclared assembly placeholder in C unit')
        copies.append((source,destination));text=text.replace(anchor,unit['splat_replacement'])
    staged_patches=[]
    for entry in manifest.get('existing_source_patches', []):
        destination=checkout/'src'/entry['source']
        candidate=source_dir/entry['candidate_source']
        if not destination.is_file() or not candidate.is_file():
            raise ValueError('Existing C source or reviewed candidate missing')
        staged=prepare_collision_gate(destination.read_text(encoding='utf-8'),
                                      candidate.read_text(encoding='utf-8'))
        if digest(staged.encode('utf-8'), 'sha256') != entry['patched_sha256_lf']:
            raise ValueError('Pinned collision source patch hash mismatch')
        staged_patches.append((destination,staged))
    for source,destination in copies:shutil.copyfile(source,destination)
    for destination,staged in staged_patches:
        destination.write_text(staged,encoding='utf-8',newline='\n')
    config.write_text(text,encoding='utf-8',newline='\n')
    if makefile is not None:(checkout/'Makefile').write_text(makefile,encoding='utf-8',newline='\n')


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
    for fn in claimed_functions(manifest):
        if fn['rom_offset'] + fn['size'] > len(expected):
            raise ValueError('Claimed function extends outside reference ROM')
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



def baseline_identity(checkout, manifest):
    checkout = Path(checkout)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout, text=True).strip()
    dirty = subprocess.check_output(['git', 'diff', '--name-only'], cwd=checkout, text=True).strip()
    if revision != manifest['upstream_commit'] or dirty:
        raise ValueError('Baseline cache source identity changed')
    expected = (checkout/'config/usa/baserom.decompressed.z64').read_bytes()
    image = (checkout/'build/usa/mnsg.z64').read_bytes()
    if digest(expected) != manifest['decompressed_sha1'] or image != expected:
        raise ValueError('Baseline cache ROM identity mismatch')
    compiler = {p.name: digest(p.read_bytes(), 'sha256') for p in sorted((checkout/'tools/ido-5.3').iterdir()) if p.is_file()}
    return dict(format='goemon-baseline-cache-v1', upstream_commit=revision,
                decompressed_sha1=digest(image), elf_sha256=digest((checkout/'build/usa/mnsg.elf').read_bytes(), 'sha256'),
                compiler_sha256=digest(json.dumps(compiler, sort_keys=True).encode(), 'sha256'),
                dependency_lock_sha256=digest((checkout/'uv.lock').read_bytes(), 'sha256'))


def certify_baseline(checkout, manifest):
    proof = baseline_identity(checkout, manifest)
    with (Path(checkout)/'build/goemon-baseline-proof.json').open('x', encoding='utf-8') as output:
        json.dump(proof, output, indent=2); output.write('\n')
    return proof


def validate_baseline_cache(checkout, manifest):
    recorded = json.loads((Path(checkout)/'build/goemon-baseline-proof.json').read_text(encoding='utf-8'))
    if recorded != baseline_identity(checkout, manifest):
        raise ValueError('Baseline cache provenance changed')
    if not (Path(checkout)/'.venv/bin/python').is_file():
        raise ValueError('Baseline cache dependency environment is missing')
    return recorded


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
    requested_cache = getattr(args, 'baseline_cache', None)
    if requested_cache and work.is_relative_to(requested_cache.resolve()):
        raise ValueError('New work directory must be outside the immutable baseline cache')
    work.mkdir(parents=True)
    report.update(upstream_commit=manifest['upstream_commit'],retail_sha1=manifest['retail_sha1'],
        verifier_source_sha256_lf=digest(Path(__file__).read_bytes().replace(b'\r\n',b'\n'),'sha256'),
        tool_versions={name:capture(command).splitlines()[0] for name,command in {
            'uv':[uv,'--version'],'gcc':['gcc','--version'],'assembler':['mips-linux-gnu-as','--version']}.items()})
    def logged(stage,command,cwd):
        report['stage']=stage
        with (work/(stage+'.log')).open('w',encoding='utf-8') as log:
            subprocess.run(command,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,check=True)
    cache = getattr(args, 'baseline_cache', None)
    baseline = cache.resolve() if cache else work/'baseline'
    candidate = work/'candidate'
    if cache:
        if work.is_relative_to(baseline):
            raise ValueError('New work directory must be outside the immutable baseline cache')
        proof = validate_baseline_cache(baseline, manifest)
        report['baseline_cache_used'] = True
    else:
        logged('clone-baseline',['git','clone','--no-hardlinks',str(upstream),str(baseline)],work)
        logged('dependencies',[uv,'sync','--python','3.12','--frozen'],baseline)
        shutil.copyfile(args.retail_rom,baseline/'config/usa/baserom.z64')
        logged('baseline-setup',['make','setup','UV='+uv],baseline)
        logged('baseline-build',['make','-j'+str(args.jobs),'UV='+uv],baseline)
        proof = certify_baseline(baseline, manifest)
        report['baseline_cache_used'] = False
    expected=(baseline/'config/usa/baserom.decompressed.z64').read_bytes()
    report['baseline_sha1']=proof['decompressed_sha1']
    report['baseline_provenance']=proof
    logged('clone-candidate',['git','clone','--no-hardlinks',str(upstream),str(candidate)],work)
    source_dir = getattr(args, 'source_dir', ROOT).resolve()
    apply_units(candidate,manifest,source_dir)
    (candidate/'.venv').symlink_to(baseline/'.venv',target_is_directory=True)
    shutil.copyfile(args.retail_rom,candidate/'config/usa/baserom.z64')
    logged('candidate-setup',['make','setup','UV='+uv],candidate)
    if manifest.get('vm_assignment_table_layout'):
        logged('candidate-vm-object',['make','-j'+str(args.jobs),'UV='+uv,
            'build/usa/src/script_vm.c.o','build/usa/asm/usa/data/main_continued.rodata.s.o'],candidate)
        report['object_layout']=pack_object_file(candidate/'build/usa/src/script_vm.c.o')
    if manifest.get('heap_noop_text_layout'):
        logged('candidate-heap-noop-object',['make','-j'+str(args.jobs),'UV='+uv,
            'build/usa/src/heap_noop.c.o','build/usa/asm/usa/3698C.s.o'],candidate)
        report['heap_noop_layout']=pack_heap_noop_file(candidate/'build/usa/src/heap_noop.c.o')
    logged('candidate-build',['make','-j'+str(args.jobs),'UV='+uv],candidate)
    symbols=parse_symbols(capture(['mips-linux-gnu-nm','-n','build/usa/mnsg.elf'],candidate))
    result=compare_images(expected,(candidate/'build/usa/mnsg.z64').read_bytes(),manifest,symbols)
    if manifest.get('vm_assignment_table_layout'):
        image=(candidate/'build/usa/mnsg.z64').read_bytes()
        report['assignment_table']=dict(rom_start='0x7DC2C',size=60,
            matched=expected[0x7DC2C:0x7DC68]==image[0x7DC2C:0x7DC68],
            sha256=digest(image[0x7DC2C:0x7DC68],'sha256'))
    report['comparison']=result
    report['retained_assembly_functions']=[name for unit in manifest['units'] for name in unit.get('assembly_functions',[])]
    source_names=[unit['source'] for unit in manifest['units']]+manifest.get('support_headers',[])+[p['source'] for p in manifest.get('existing_source_patches',[])]
    report['sources_sha256_lf']={name:digest((candidate/'src'/name).read_bytes().replace(b'\r\n',b'\n'),'sha256')
                               for name in source_names}
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
    parser.add_argument('--baseline-cache',type=Path,help='Immutable baseline from a completed fresh verifier run')
    parser.add_argument('--manifest',type=Path,default=ROOT/'manifest.json',help='Reviewed matching manifest')
    parser.add_argument('--source-dir',type=Path,default=ROOT,help='Reviewed source/header bundle')
    args=parser.parse_args(argv)
    if args.jobs<1:parser.error('--jobs must be positive')
    report=dict(format='goemon-matching-build-result-v1',started_utc=datetime.now(timezone.utc).isoformat(),status='failed')
    if args.report.resolve()==args.retail_rom.resolve():parser.error('Report must differ from ROM')
    try:
        # Reserve before any build changes. An existing report is never replaced.
        with args.report.open('x',encoding='utf-8') as output:
            try:run_build(args,load_manifest(args.manifest),report)
            except (OSError,ValueError,subprocess.SubprocessError) as exc:report['error']=str(exc)
            finally:
                report['ended_utc']=datetime.now(timezone.utc).isoformat()
                json.dump(report,output,indent=2);output.write('\n')
    except OSError as exc:parser.exit(1,str(exc)+'\n')
    if report['status']!='matched':parser.exit(1,report.get('error','Build failed')+'\n')
    print(f'MATCH: {report["comparison"]["matched_functions"]} functions; whole-ROM SHA-1 {report["comparison"]["candidate_sha1"]}')


if __name__=='__main__':main()
