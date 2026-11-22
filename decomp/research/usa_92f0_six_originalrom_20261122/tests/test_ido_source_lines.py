#!/usr/bin/env python3
"""Native IDO 5.3 regression for C source-line-sensitive struct copy/loop.

Only reads private original-USA ROM locally; no original instruction words embedded.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile

FLAGS=['-c','-G','0','-non_shared','-Xfullwarn','-Xcpluscomm',
       '-Iinclude','-Ilibultra/include','-Ilibultra/include/PR','-Isrc','-I.',
       '-Wab,-r4300_mul','-woff','649,838,712','-D_LANGUAGE_C',
       '-D_FINALROM','-DF3DEX_GBI','-D__sgi','-DNDEBUG','-O2','-mips2']
TARGETS={
 'func_8000A548_B148': (0xB148,124,
   [(0x28,'R_MIPS_HI16','D_8008CCC0_8D8C0'),
    (0x38,'R_MIPS_LO16','D_8008CCC0_8D8C0'),
    (0x50,'R_MIPS_26','func_8000A5C4_B1C4')]),
 'func_8000A5C4_B1C4': (0xB1C4,80,
   [(0,'R_MIPS_HI16','D_8005B974_5C574'),
    (4,'R_MIPS_LO16','D_8005B974_5C574')]),
}

def compile_file(checkout,env,content,out):
    source=out.with_suffix('.c')
    source.write_text(content)
    cc=checkout/'tools/ido-5.3/cc'
    r=subprocess.run([str(cc),*FLAGS,'-o',str(out),str(source)],cwd=checkout,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if r.returncode:raise RuntimeError('Native IDO failed: '+r.stderr[-900:])
    disasm=subprocess.check_output(['mips-linux-gnu-objdump','-dr',str(out)],env=env,text=True)
    words=[int(m.group(1),16) for line in disasm.splitlines() if (m:=re.search(r':\s+([0-9a-f]{8})\s',line))]
    relocs=re.findall(r'^\s*([0-9a-f]+):\s+(R_MIPS_\S+)\s+(\S+)',disasm,re.M)
    # On some objdump versions relocation lines have a "0:" prefix; symbols unaffected.
    rec=[(int(off,16),kind,sym) for off,kind,sym in relocs]
    return words,rec

def main():
    p=argparse.ArgumentParser()
    for n in ('checkout','deps','runtime'):p.add_argument('--'+n,type=Path,required=True)
    o=p.parse_args()
    base,deps,rt=(getattr(o,n).resolve() for n in ('checkout','deps','runtime'))
    env=os.environ.copy();env['PATH']=str(deps/'bin')+os.pathsep+env.get('PATH','')
    env['LD_LIBRARY_PATH']=str(rt/'lib')+(os.pathsep+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
    root=Path(__file__).resolve().parents[1]
    rom=(base/'config/usa/baserom.decompressed.z64').read_bytes()
    assert len(rom)==33554432
    with tempfile.TemporaryDirectory(prefix='goemon-ido-lines-') as d0:
      d=Path(d0)
      for name,(off,size,relocs) in TARGETS.items():
        source=(root/'source'/(name+'.c')).read_text()
        raw=rom[off:off+size]
        original=[int.from_bytes(raw[i:i+4],'big') for i in range(0,size,4)]
        good,recs=compile_file(base,env,source,d/(name+'.o'))
        assert len(good)>=len(original),(name,len(good),len(original))
        assert recs==relocs,(name,recs,relocs)
        offsets={r[0] for r in relocs}
        for i,(x,y) in enumerate(zip(good[:len(original)],original)):
            if i*4 not in offsets:assert x==y,(name,i,'non-relocated instruction mismatch')
            elif any(r[0]==i*4 and r[1]=='R_MIPS_26' for r in relocs):assert x>>26==y>>26
            else:assert x>>16==y>>16,(name,i,'relocation instruction shape mismatch')
        if name=='func_8000A548_B148':
            # Flatten the C function body onto one source line, changing no tokens.
            # This is the previously measured 124-byte compiler scheduling control.
            before=source[source.index('void func_8000A548_B148(s32 start,s32 end) {'):]
            after=before.replace('\n',' ')
        else:
            before='u32 old_word0 = p->words[0];\n    *p = D_8005B974_5C574;'
            after='u32 old_word0 = p->words[0]; *p = D_8005B974_5C574;'
        assert source.count(before)==1,(name,'negative source pattern absent')
        bad,recs_bad=compile_file(base,env,source.replace(before,after),d/(name+'-one-line.o'))
        # Negative line regroup must affect at least one non-relocated instruction
        # before it can be cited as evidence of source-line-sensitive scheduling.
        differences=[i for i,(x,y) in enumerate(zip(bad,good)) if x!=y and i*4 not in offsets]
        assert differences,(name,'line-regroup negative did not alter codegen')
        print('PASS:',name,len(original),'native instruction bytes original-code exact; negative line-group variant changes',len(differences),'nonrelocated words')

if __name__=='__main__':main()
