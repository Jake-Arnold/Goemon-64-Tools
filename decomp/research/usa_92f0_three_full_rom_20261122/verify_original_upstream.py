#!/usr/bin/env python3
"""Exact original-upstream USA ROM and ELF replay for three file92 C functions.

Inputs are private and remain outside Git. This does not run canonical decomp G2.
"""
import argparse
from collections import Counter
import hashlib
from pathlib import Path
import re
import shutil
import subprocess
import os

PIN = "7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee"
USA16 = "df8083a54296b8c151917c5333e1c85f014a2a66"
USA32 = "6ea0ed71032ce08fc2745f412d84936382197494"
FUNCTIONS = {
    "func_80008798_9398": (0x9398, 44, "27f93c1513ad93f7fb6228b512d6eb178efe9971de423f89ebbcd9a8838826ce"),
    "func_8000A0F0_ACF0": (0xACF0, 64, "f1ebbd24fec5ed12a5193bc3ff26d1abebe594df4f4c1064eb6b9c2d59d9375b"),
    "func_8000A18C_AD8C": (0xAD8C, 48, "a494dc6ba7f3ed16e1aa8232fd8e54d8948e40a7f8d2b22b80df3f6a3686a385"),
}
def sha1(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()

def records(path):
    relocs, funcs = [], []
    section = ""
    for line in subprocess.check_output(["readelf", "-rW", str(path)], text=True).splitlines():
        sm = re.search(r"^Relocation section '([^']+)'", line)
        if sm:
            section = sm.group(1)
            continue
        m = re.match(r"^\s*([0-9a-fA-F]+)\s+[0-9a-fA-F]+\s+(R_MIPS_\S+)\s+[0-9a-fA-F]+\s+(\S+)", line)
        if m:
            relocs.append((section, int(m.group(1),16), m.group(2), m.group(3)))
    for line in subprocess.check_output(["readelf", "-sW", str(path)], text=True).splitlines():
        m = re.match(r"^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+FUNC\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", line)
        if m and int(m.group(2))>0:
            funcs.append((m.group(6),int(m.group(1),16),int(m.group(2)),m.group(3),m.group(4),m.group(5)))
    return relocs, funcs

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--baseline", type=Path, required=True)
    ap.add_argument("--deps", type=Path, required=True)
    ap.add_argument("--runtime", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a=ap.parse_args()
    base=a.baseline.resolve()
    out=a.out.resolve()
    if out.exists():
        raise SystemExit("Refusing existing output")
    head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=base,text=True).strip()
    assert head == PIN, "Pinned source mismatch"
    rom16=base/"config/usa/baserom.z64"
    rom32=base/"config/usa/baserom.decompressed.z64"
    rebuilt=base/"build/usa/mnsg.z64"
    orig_elf=base/"build/usa/mnsg.elf"
    assert sha1(rom16)==USA16 and sha1(rom32)==USA32
    assert rebuilt.is_file() and orig_elf.is_file() and rebuilt.read_bytes()==rom32.read_bytes()
    original=rom32.read_bytes()
    for name,(off,length,digest) in FUNCTIONS.items():
        assert hashlib.sha256(original[off:off+length]).hexdigest()==digest, name
    old_source=(base/"src/92F0.c").read_text()
    assert old_source.count('#include "common.h"')==1
    for name in FUNCTIONS:
        marker=f'#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/{name}.s")'
        assert old_source.count(marker)==1, name
    project=Path(__file__).resolve().parent
    out.mkdir(parents=True)
    work=out/"mnsg"
    shutil.copytree(base,work,symlinks=True)
    new_source=old_source
    for name in FUNCTIONS:
        src=(project/"source"/f"{name}.c").read_text()
        assert src.startswith('#include "common.h"\n')
        snippet=src.split("\n",1)[1].strip("\n")
        marker=f'#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/{name}.s")'
        new_source=new_source.replace(marker,snippet)
    (work/"src/92F0.c").write_text(new_source)
    env=os.environ.copy()
    env["PATH"]=str(a.deps.resolve()/"bin")+os.pathsep+env.get("PATH","")
    env["LD_LIBRARY_PATH"]=str(a.runtime.resolve()/"lib")+os.pathsep+env.get("LD_LIBRARY_PATH","")
    env["PYTHONHOME"]=str(a.runtime.resolve()/"python")
    env["PYTHONPATH"]=str(a.deps.resolve()/".venv/lib/python3.12/site-packages")
    with (out/"native_build.log").open("w") as log:
        result=subprocess.run(["make","-j4","VERSION=usa","build/usa/mnsg.z64"],cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT)
    assert result.returncode==0, "IDO upstream ROM build failed"
    assert (work/"build/usa/mnsg.z64").read_bytes()==original, "32MiB mismatch"
    r0,f0=records(orig_elf)
    r1,f1=records(work/"build/usa/mnsg.elf")
    assert len(r0)==len(r1)==82216 and Counter(r0)==Counter(r1), "Relocation mismatch"
    assert len(f0)==len(f1)==7376 and Counter(f0)==Counter(f1), "ELF function mismatch"
    byname={n:(addr,size) for n,addr,size,*_ in f1}
    for name,(_,length,_) in FUNCTIONS.items():
        assert byname[name][1]==length, "ELF function extent mismatch: "+name
    print("PASS: original USA upstream 33,554,432-byte ROM exact")
    print("PASS: all 7,376 original positive ELF function identities")
    print("PASS: all 82,216 original ELF relocation identities")
    print("RESEARCH_ONLY; combined decomp G2, strict inventory and full local CI NOT_RUN")

if __name__=="__main__":
    main()
