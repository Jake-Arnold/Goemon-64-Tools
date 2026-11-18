#!/usr/bin/env python3
"""Replay isolated original-USA exact C, refusing unknown source/ROM identities."""
import argparse,hashlib,json,pathlib,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
FLAGS='-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2'.split()
def run(cmd):
    p=subprocess.run(list(map(str,cmd)),capture_output=True,text=True)
    if p.returncode:raise RuntimeError(f'{cmd}: {(p.stdout+p.stderr)[-2500:]}')
    return p.stdout
def main(rom,ido):
    registry=json.loads((ROOT/'source_registry.json').read_text())
    data=pathlib.Path(rom).read_bytes()
    assert len(data)==33_554_432 and hashlib.sha1(data).hexdigest()==registry['original_decompressed_sha1']
    records=registry['sources'];assert len(records)==52
    with tempfile.TemporaryDirectory(prefix='goemon-file61-80-') as temp:
        folder=pathlib.Path(temp)
        for i,r in enumerate(records):
            source=ROOT/r['path'];content=source.read_bytes()
            assert hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()==r['source_git_sha1'],r['function']
            section=folder/f'{i}.ld';obj=folder/f'{i}.o';elf=folder/f'{i}.elf';out=folder/f'{i}.bin'
            section.write_text(f'SECTIONS {{ .text {r["vma"]} : SUBALIGN(4) {{ *(.text) *(.text.*) }} /DISCARD/ : {{ *(.note*) *(.comment*) }} }}\n')
            run([ido,*FLAGS,'-o',obj,source]);run(['mips-linux-gnu-ld','-T',section,'-o',elf,obj])
            run(['mips-linux-gnu-objcopy','-O','binary','-j','.text',elf,out])
            got=out.read_bytes();start=int(r['original_rom_offset'],16);size=r['size']
            assert got[:size]==data[start:start+size] and not any(got[size:]),r['function']
    assert sum(r['size'] for r in records)==576
    print('PASS: 52 original-address native-IDO matching-C functions, 576 instruction bytes')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--ido',required=True)
    a=p.parse_args()
    try:main(a.rom,a.ido)
    except Exception as exc:print('FAIL',repr(exc),file=sys.stderr);sys.exit(1)
