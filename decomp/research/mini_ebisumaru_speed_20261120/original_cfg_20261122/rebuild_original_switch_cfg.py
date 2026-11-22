#!/usr/bin/env python3
"""Resolve the original Mini clamp's numeric switch-table targets in private ASM.

Requires user's already-authenticated pinned upstream original ASM/data and m2c.
Writes only *private scratch* ASM and reconstructed C under --output-dir;
never alters the original files or publishes original MIPS opcodes.
"""
import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import sys

EXPECTED_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
FIVE_TARGETS = ('801CD450','801CD484','801CD420','801CD3CC','801CD3F0')
DATA_SYMBOL='jtbl_8020A85C_5C676C'
FUNCTION='func_801CD310_589220'
START=0x589220
ORIGINAL_SIZE=4320

def rewrite(assembly, data):
    assert 'glabel '+FUNCTION in assembly
    assert assembly.count('glabel '+FUNCTION)==1
    start = data.index('dlabel '+DATA_SYMBOL+'\n')
    end = data.index('enddlabel '+DATA_SYMBOL, start)
    before, chunk, after = data[:start], data[start:end], data[end:]
    targets = re.findall(r'(?m)^\s*/\* [0-9A-F]{6} [0-9A-F]{8} ([0-9A-F]{8}) \*/\s*\.word 0x([0-9A-F]{8})', chunk)
    assert len(targets)==18, 'unexpected jump-table entry count'
    assert all(a==b and a in FIVE_TARGETS for a,b in targets), 'unexpected jump-table target'
    assert set(a for a,_ in targets)==set(FIVE_TARGETS)
    labels={}
    for target in FIVE_TARGETS:
        patt=re.compile(r'(?m)^\s*/\* ([0-9A-F]{6}) '+target+r' [0-9A-F]{8} \*/')
        matched=patt.search(assembly)
        assert matched is not None, ('missing native destination', target)
        expected_rom=int(target,16)-0x801CD310+START
        assert int(matched.group(1),16)==expected_rom, 'ROM/VMA mapping mismatch'
        sym=f'.L{target}_{matched.group(1)}'
        if sym+':' not in assembly:
            assembly=assembly[:matched.start()]+f'{sym}:\n'+assembly[matched.start():]
        labels[target]=sym
    for target, label in labels.items():
        pat=re.compile(r'(\.word\s+)0x'+target)
        chunk,n=pat.subn(lambda m:m.group(1)+label,chunk)
        assert n>=1
    assert chunk.count('.word ')==18
    return assembly, before+chunk+after, labels

def read_input(args):
    usa=Path(args.upstream)
    rom=Path(args.rom)
    import hashlib
    assert rom.stat().st_size==33554432
    assert hashlib.sha1(rom.read_bytes()).hexdigest()==EXPECTED_SHA1
    return (usa/'asm/usa/587370.s').read_text(), (usa/'asm/usa/data/5B8500.data.s').read_text()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--upstream',required=True)
    p.add_argument('--rom',required=True)
    p.add_argument('--output-dir',required=True)
    p.add_argument('--run-m2c',action='store_true')
    args=p.parse_args()
    assembly,data=read_input(args)
    asm2,dat2,labels=rewrite(assembly,data)
    d=Path(args.output_dir)
    d.mkdir(exist_ok=True,parents=True)
    assembly_file=d/'original_private_switch_symbols.s'
    data_file=d/'original_private_data_switch_symbols.s'
    assembly_file.write_text(asm2)
    data_file.write_text(dat2)
    print('SWITCH_TABLE_RECONSTRUCTED', 'entries=18', 'distinct_targets=5', 'original_assembly_unchanged=True')
    if args.run_m2c:
        usa=Path(args.upstream)
        m2c=usa/'tools/m2c/m2c.py'
        result=subprocess.run([sys.executable,str(m2c),'-t','mips-ido-c','--valid-syntax','--no-cache','-f',FUNCTION,str(assembly_file),str(data_file)],cwd=usa,capture_output=True,text=True)
        if result.returncode:
            raise RuntimeError(result.stderr[-2000:])
        c=result.stdout
        assert 'sp8C = 0.0f;' in c
        assert 'sp8C = sqrtf(' in c
        assert 'sp8C *= func_80003E10_4A10(' in c
        assert 'sp64 = func_80003EA0_4AA0(' in c
        assert 'sp6C = var_a1;' in c
        assert 'sp6E =' in c
        (d/'original_private_m2c_analysis.c').write_text(c)
        print('COMPLETE_ORIGINAL_CFG_DECOMPILED', 'lines='+str(len(c.splitlines())), 'stack_magnitude=sp8C', 'original_typed_c_unverified=True')
        print('WARNING: original_private_* scratch files contain original derived ASM/C; do not upload or commit')

if __name__=='__main__': main()
