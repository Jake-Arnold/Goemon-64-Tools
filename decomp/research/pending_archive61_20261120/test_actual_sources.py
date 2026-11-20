"""Compile all 61 authentic original C units under GCC sanitizers, run 10 safe units."""
from __future__ import annotations
import hashlib
import os
import shlex
import subprocess
import tempfile
from pathlib import Path
from decomp import overlay_archive61 as native

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
SELECTED=[14,19,20,22,36,48,49,50,59,60]

def main():
    fixture=native.load_fixture()
    sources=sorted((HERE/'sources').glob('archive61_*.c'))
    if len(sources)!=61:
        raise ValueError(f'Archive61 original-source completeness failure: {len(sources)}')
    for unit,path in zip(fixture['units'],sources):
        if path.name!=unit['name']+'.c' or hashlib.sha256(path.read_bytes()).hexdigest()!=unit['source_sha256']:
            raise ValueError('Archive61 genuine source proof failed: '+path.name)
    compiler=shlex.split(os.environ.get('CC','cc'))
    flags=['-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror',
           '-Wno-unused-parameter','-Wno-unused-function','-Wno-int-conversion',
           '-Wno-int-to-pointer-cast','-Wno-pointer-to-int-cast',
           '-Wno-incompatible-pointer-types','-Wno-implicit-function-declaration',
           '-fsanitize=address,undefined','-fno-sanitize-recover=all',
           '-fno-omit-frame-pointer']
    with tempfile.TemporaryDirectory(prefix='goemon-archive61-actual-c-') as work:
        tmp=Path(work)
        for path in sources:
            subprocess.run(compiler+flags+['-c',str(path),'-o',str(tmp/(path.stem+'.o'))],
                           cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
        executable=tmp/'archive61-actual-host'
        subset=[sources[i] for i in SELECTED]
        subprocess.run(compiler+flags+[str(HERE/'test_actual_archive61.c'),
                       *[str(p) for p in subset],'-lm','-o',str(executable)],
                       cwd=ROOT,check=True)
        subprocess.run([str(executable)],cwd=ROOT,check=True)
    print('Archive61 actual-source ASan/UBSan PASS: 61/61 independently compiled; '
          '10/10 safe real-source functions executed 1000 cases each')

if __name__=='__main__':main()
