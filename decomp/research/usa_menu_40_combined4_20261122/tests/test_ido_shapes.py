#!/usr/bin/env python3
"""IDO 5.3 word-struct versus SDK Gfx union scheduling regression.

Uses a privately installed native compiler and original ROM; contains no proprietary bytes.
Checks the exact symbolic relocation offsets and every non-relocated instruction.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile

TARGET_OFF = 0x114BC
TARGET_BYTES = 40
SYMBOL = 'D_800637C0_643C0'

FLAGS = ['-c','-G','0','-non_shared','-Xfullwarn','-Xcpluscomm',
         '-Iinclude','-Ilibultra/include','-Ilibultra/include/PR','-Isrc','-I.',
         '-Wab,-r4300_mul','-woff','649,838,712','-D_LANGUAGE_C',
         '-D_FINALROM','-DF3DEX_GBI','-D__sgi','-DNDEBUG','-O2','-mips2']


def relocs(path):
    text = subprocess.check_output(['readelf','-rW',str(path)],text=True)
    rx = re.compile(r'^\s*([a-fA-F0-9]+)\s+[a-fA-F0-9]+\s+(R_MIPS_\S+)\s+[a-fA-F0-9]+\s+(\S+)',re.M)
    return [(int(a,16),kind,sym) for a,kind,sym in rx.findall(text)]


def compile_source(checkout, env, source, output):
    cc = checkout/'tools/ido-5.3/cc'
    subprocess.run([str(cc),*FLAGS,'-o',str(output),str(source)],cwd=checkout,env=env,check=True,
                   stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    data=subprocess.check_output(['mips-linux-gnu-objdump','-dr',str(output)],env=env,text=True)
    lines = [x for x in data.splitlines() if re.match(r'^\s*[a-f0-9]+:\s+[0-9a-f]{8}\s',x)]
    return [int(re.search(r':\s+([0-9a-f]{8})\s',x).group(1),16) for x in lines]


def main():
    p=argparse.ArgumentParser()
    for x in ('checkout','deps','runtime'):
        p.add_argument('--'+x,required=True,type=Path)
    opt=p.parse_args()
    base, deps, runtime = (getattr(opt,x).resolve() for x in ('checkout','deps','runtime'))
    source = Path(__file__).resolve().parents[1]/'source/func_800108BC_114BC.c'
    env=os.environ.copy()
    env['PATH']=str(deps/'bin')+os.pathsep+env.get('PATH','')
    env['LD_LIBRARY_PATH']=str(runtime/'lib')+(os.pathsep+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
    original=(base/'config/usa/baserom.decompressed.z64').read_bytes()[TARGET_OFF:TARGET_OFF+TARGET_BYTES]
    assert len(original)==TARGET_BYTES
    orig_words=[int.from_bytes(original[i:i+4],'big') for i in range(0,TARGET_BYTES,4)]
    union_control='''#include "common.h"
extern char D_800637C0_643C0[];
Gfx* func_800108BC_114BC(Gfx*p){p->words.w0=0x06000000;p->words.w1=(u32)D_800637C0_643C0;p++;p->words.w0=0xb8000000;p->words.w1=0;return p;}
'''
    same_line = 'p->w0=0x06000000;p->w1='
    assert source.read_text().count(same_line)==1, 'Test requires pinned source shape'
    newline_negative = source.read_text().replace(same_line,'p->w0=0x06000000;\np->w1=',1)
    with tempfile.TemporaryDirectory(prefix='goemon-ido-shape-') as directory:
        d=Path(directory)
        pos=d/'raw.o'; neg=d/'newline.o'; uns=d/'union.o'
        negsrc=d/'newline.c';unsrc=d/'union.c'
        negsrc.write_text(newline_negative);unsrc.write_text(union_control)
        positive_words=compile_source(base,env,source,pos)
        negative_words=compile_source(base,env,negsrc,neg)
        union_words=compile_source(base,env,unsrc,uns)
        expect0=[(0,'R_MIPS_HI16',SYMBOL),(4,'R_MIPS_LO16',SYMBOL)]
        expect1=[(0,'R_MIPS_HI16',SYMBOL),(8,'R_MIPS_LO16',SYMBOL)]
        assert relocs(pos)==expect0,relocs(pos)
        assert relocs(neg)==expect1,relocs(neg)
        assert relocs(uns)==expect0,relocs(uns)
        assert len(positive_words)>=10 and len(negative_words)>=10
        # The exact runtime-patched relocation pair in the original is known from
        # its original address, so compare every other native instruction unmasked.
        assert positive_words[0]&0xffff0000 == orig_words[0]&0xffff0000
        assert positive_words[1]&0xffff0000 == orig_words[1]&0xffff0000
        assert positive_words[2:10] == orig_words[2:10],(positive_words,orig_words)
        assert negative_words[1:10] != orig_words[1:10]
        assert union_words[:10] == positive_words[:10], (union_words,positive_words)
        assert positive_words[1] != negative_words[1]
        print('PASS: 10/10 same-line two-word struct MIPS instruction shapes; HI16+LO16 at 0,4')
        print('PASS: newline-only negative control moves LO16 from 4 to 8')
        print('PASS: same-line SDK Gfx union is codegen-equivalent, eliminating type as cause')

if __name__=='__main__':main()
