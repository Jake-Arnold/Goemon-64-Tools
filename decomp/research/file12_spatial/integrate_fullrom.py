"""Fail-closed original-ROM C/ASM integration proof for three USA file_12 functions.

User-provided ROMs, generated assembly and ELF outputs stay in a fresh local
workdir. This does NOT run the central existing 315-C decomp.verify gate.

Requires upstream pinned mnsg checkout with verified original USA baseline build,
Splat + original IDO toolchain on PATH/environment, and the three C sources.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess

BASE_COMMIT = "7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee"
USA_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
USA_RETAIL_SHA1 = "df8083a54296b8c151917c5333e1c85f014a2a66"
BASE_ELF_SHA256 = "83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038"
ROM_BYTES = 33_554_432
FUNC_COUNT = 7376
RELOCS_FILE12 = 7051
FUNCTIONS = (
    ("update_dispatch", "func_80218E7C_5D434C", 0x5D434C, 0xB4,
     "c89c568ba7a1cd590526ea901f2673b0563cd95e081a639ef0f8a68b6529a533"),
    ("state2_callback", "func_80218F30_5D4400", 0x5D4400, 0xB8,
     "a5a18d9ff5bda797ac7b6645eaca77a89ffc422032199a4fed167ad81fcd719f"),
    ("active_gate", "func_8021A644_5D5B14", 0x5D5B14, 0x38,
     "6d8df03a1dccbae56a1b7f88b8d430e02023eb0e9e14b5381c317a6ff4dbd0ba"),
)
LAYOUT = (
    ("asm", "file_12_before_5D434C", 0x5C8770, 0x5D434C),
    ("c", "update_dispatch", 0x5D434C, 0x5D4400),
    ("c", "state2_callback", 0x5D4400, 0x5D44B8),
    ("asm", "file_12_gap_5D44B8_5D5B14", 0x5D44B8, 0x5D5B14),
    ("c", "active_gate", 0x5D5B14, 0x5D5B4C),
    ("asm", "file_12_after_5D5B4C", 0x5D5B4C, 0x5E3C90),
)
SOURCE_BLOCK = """    subalign: 16
    overlay: yes
    exclusive_ram_id: static_overlay_2
    subsegments:
    - [0x5C8770, asm]
    - [0x5E3C90, data]"""
DEST_BLOCK = """    subalign: null
    overlay: yes
    exclusive_ram_id: static_overlay_2
    subsegments:
    - [0x5C8770, asm, file_12_before_5D434C]
    - [0x5D434C, c, update_dispatch]
    - [0x5D4400, c, state2_callback]
    - [0x5D44B8, asm, file_12_gap_5D44B8_5D5B14]
    - [0x5D5B14, c, active_gate]
    - [0x5D5B4C, asm, file_12_after_5D5B4C]
    - [0x5E3C90, data, file_12]"""
TAIL_GENERATED = """nonmatching func_802287BC_5E3C8C, 0x4

glabel func_802287BC_5E3C8C
    /* 5E3C8C 802287BC 00000000 */  nop
endlabel func_802287BC_5E3C8C"""
TAIL_ORIGINAL = """  alabel D_802287BC_5E3C8C
    /* 5E3C8C 802287BC 00000000 */  nop"""


def sha1(data): return hashlib.sha1(data).hexdigest()
def sha256(data): return hashlib.sha256(data).hexdigest()


def fail_same(text, old, new, expected_count=1):
    if text.count(old) != expected_count or new in text:
        raise ValueError(f"Pinned source anchor mismatch: {old[:65]!r}")
    return text.replace(old, new)


def elf_text_trim_align(src: bytes, original_bytes: int) -> tuple[bytes, dict]:
    """Shrink only zero-padding and lower only ELF .text input alignment."""
    b = bytearray(src)
    if b[:6] != b"\x7fELF\x01\x02" or struct.unpack_from(">H", b, 18)[0] != 8:
        raise ValueError("Expected big-endian ELF32 MIPS relocatable object")
    if struct.unpack_from(">H", b, 16)[0] != 1:
        raise ValueError("Expected ET_REL")
    shoff = struct.unpack_from(">I", b, 32)[0]
    entsize, count, stridx = struct.unpack_from(">HHH", b, 46)
    if entsize < 40 or shoff + entsize * count > len(b) or stridx >= count:
        raise ValueError("Malformed ELF32 section headers")
    sections = [struct.unpack_from(">IIIIIIIIII", b, shoff+i*entsize) for i in range(count)]
    st = sections[stridx]
    names = b[st[4]:st[4]+st[5]]
    indices = [i for i, s in enumerate(sections)
               if names[s[0]:].split(b"\0", 1)[0] == b".text"]
    if len(indices) != 1:
        raise ValueError("Missing or duplicated .text")
    idx = indices[0]
    s = sections[idx]
    if not (s[2] & 4) or s[8] != 16 or s[5] < original_bytes or s[4] + s[5] > len(b):
        raise ValueError("Original MIPS text section extent/alignment changed")
    if any(b[s[4]+original_bytes:s[4]+s[5]]):
        raise ValueError("Refusing to trim nonzero original code bytes")
    metadata = shoff + idx*entsize
    struct.pack_into(">I", b, metadata+20, original_bytes)
    struct.pack_into(">I", b, metadata+32, 4)
    return bytes(b), {"size_original": s[5], "size_staged": original_bytes,
                       "alignment_original":16, "alignment_staged":4,
                       "zero_padding_removed":s[5]-original_bytes,
                       "sha256_before":sha256(src),"sha256_after":sha256(b)}


def rel_file12(path: Path):
    stdout = subprocess.check_output(["readelf", "-W", "-r", str(path)], text=True)
    marker = re.search(r"Relocation section '\.rel\.file_12'[^\n]*contains\s+(\d+) entries:\n[^\n]*\n", stdout)
    if marker is None:
        raise ValueError("Missing linked .rel.file_12")
    total = int(marker.group(1)); rows=[]
    for line in stdout[marker.end():].splitlines():
        if not line.strip():break
        row=re.match(r"^([0-9a-fA-F]+)\s+[0-9a-fA-F]+\s+(R_MIPS_\w+)\s+([0-9a-fA-F]+)\s+(\S+)",line.strip())
        if row is None: raise ValueError("Unrecognized relocation record")
        rows.append((int(row.group(1),16),row.group(2),int(row.group(3),16),row.group(4)))
    if len(rows)!=total or total!=RELOCS_FILE12:
        raise ValueError("Complete original file_12 relocation count mismatch")
    return rows


def func_inventory(path: Path):
    stdout=subprocess.check_output(["readelf","-W","-s",str(path)],text=True)
    result=[]
    for line in stdout.splitlines():
        m=re.match(r"^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+\S+\s+(.+)",line)
        if m and int(m.group(2))>0:
            result.append((m.group(3),int(m.group(1),16),int(m.group(2))))
    if len(result)!=FUNC_COUNT:
        raise ValueError("Unexpected original function inventory size")
    return Counter(result)


def verify_section(path):
    stdout=subprocess.check_output(["readelf","-W","-S",str(path)],text=True)
    line=next((l for l in stdout.splitlines() if re.search(r"\]\s+\.file_12\s+PROGBITS\s+",l)),None)
    if line is None: raise ValueError("Missing file_12 section")
    m=re.search(r"\.file_12\s+PROGBITS\s+(\S+)\s+(\S+)\s+(\S+)\s+\S+\s+WAX\s+\d+\s+\d+\s+(\d+)",line)
    if not m or (int(m.group(1),16),int(m.group(3),16),int(m.group(4))) != (0x8020D2A0,0x2E0D0,16):
        raise ValueError("Original overlay VMA, size, permissions or alignment differs")
    return {"vma":"0x8020D2A0", "bytes":0x2E0D0, "alignment":16}


def run_step(cmd:list[str], cwd:Path):
    outcome=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if outcome.returncode:
        raise RuntimeError(f"Command failed: {cmd}\n{outcome.stdout[-12000:]}")


def split_original_assembly(original_text: str, candidate: Path) -> None:
    """Re-slice only the authenticated pinned upstream Splat assembly.

    No generated code bytes are embedded. This avoids an expensive unrelated
    1,091-segment extraction and preserves the original tail data alias.
    """
    markers = (
        "nonmatching func_80218E7C_5D434C, 0xB4",
        "nonmatching func_80218F30_5D4400, 0xB8",
        "nonmatching func_80218FE8_5D44B8, 0x274",
        "nonmatching func_8021A644_5D5B14, 0x38",
        "nonmatching func_8021A67C_5D5B4C, 0xE8",
    )
    indices=[]
    for marker in markers:
        if original_text.count(marker)!=1:
            raise ValueError("Pinned source function boundary changed: "+marker)
        indices.append(original_text.index(marker))
    if indices!=sorted(indices):
        raise ValueError("Original function extents not monotonic")
    head=original_text.index("nonmatching func_8020D2A0_5C8770, 0xCC")
    preamble=original_text[:head]
    if '.section .text' not in preamble:
        raise ValueError("Missing original MIPS text prologue")
    asm_ranges=((0,indices[0]),(indices[2],indices[3]),(indices[4],len(original_text)))
    targets=("file_12_before_5D434C", "file_12_gap_5D44B8_5D5B14", "file_12_after_5D5B4C")
    for (start,end),target in zip(asm_ranges,targets):
        piece = original_text[start:end] if start==0 else preamble + original_text[start:end]
        out=candidate/'asm/usa'/(target+'.s')
        if out.exists():raise ValueError("Colliding generated ASM slice: "+str(out))
        out.write_text(piece)
    # Retain original explicit alabel D_802287BC_5E3C8C rather than generating
    # an invented 4-byte function alias. This is pinned disassembler source.
    tail=(candidate/'asm/usa/file_12_after_5D5B4C.s').read_text()
    if tail.count('alabel D_802287BC_5E3C8C')!=1:
        raise ValueError("Missing original file12 end alias")


def integrate(upstream:Path, candidate:Path, sources:Path, jobs:int) -> dict:
    upstream=upstream.resolve(); candidate=candidate.resolve(); sources=sources.resolve()
    if candidate.exists() or candidate == upstream or upstream in candidate.parents:
        raise ValueError("Candidate must be a new independent directory, not inside upstream")
    if subprocess.check_output(["git","rev-parse","HEAD"],cwd=upstream,text=True).strip()!=BASE_COMMIT:
        raise ValueError("Original upstream commit changed")
    original=(upstream/"config/usa/baserom.decompressed.z64").read_bytes()
    if len(original)!=ROM_BYTES or sha1(original)!=USA_SHA1:
        raise ValueError("Original 32 MiB USA ROM is not authenticated")
    retail=(upstream/"config/usa/baserom.z64").read_bytes()
    if len(retail)!=16_777_216 or sha1(retail)!=USA_RETAIL_SHA1:
        raise ValueError("Original retail USA ROM is not authenticated")
    base_build=(upstream/"build/usa/mnsg.z64").read_bytes()
    if base_build!=original:
        raise ValueError("Pinned upstream has no byte-exact original baseline build")
    base_elf=upstream/"build/usa/mnsg.elf"
    if sha256(base_elf.read_bytes())!=BASE_ELF_SHA256:
        raise ValueError("Original linked ELF SHA-256 changed")
    for stem,_,off,sz,hash_value in FUNCTIONS:
        source=sources/(stem+'.c')
        if not source.is_file() or sha256(source.read_bytes().replace(b'\r\n',b'\n'))!=hash_value:
            raise ValueError("Source-only C input identity differs: "+stem)
        if off < 0x5C8770 or off+sz>0x5E3C90:
            raise ValueError("Invalid original file_12 function extent")
    print('Baseline authenticated; staging isolated C/ASM candidate',flush=True)
    shutil.copytree(upstream,candidate,symlinks=True)
    config=candidate/"config/usa/splat.yaml"
    config.write_text(fail_same(config.read_text(),SOURCE_BLOCK,DEST_BLOCK))
    for stem,*_ in FUNCTIONS:
        shutil.copyfile(sources/(stem+'.c'),candidate/'src'/(stem+'.c'))
    print('Slicing only original file12 assembly at proven function boundaries',flush=True)
    split_original_assembly((upstream/'asm/usa/5C8770.s').read_text(),candidate)
    linker=candidate/'.splat/usa/mnsg.ld'
    script=linker.read_text()
    header='.file_12 0x8020D2A0 : AT(file_12_ROM_START) SUBALIGN(16)'
    if script.count(header)!=1:
        raise ValueError('Pinned file12 linker SUBALIGN anchor mismatch')
    script=script.replace(header,header.replace(' SUBALIGN(16)',''))
    original_input='build/usa/asm/usa/5C8770.s.o(.text);'
    objects='\n'.join(
        '        build/usa/'+('src/'+name+'.c.o' if kind=='c' else 'asm/usa/'+name+'.s.o')+'(.text);'
        for kind,name,_,_ in LAYOUT)
    script=fail_same(script,original_input,objects)
    # The original unsplit object must not remain an implicit input via its
    # otherwise-empty data/rodata/bss sections; doing so duplicates every symbol.
    old_object='build/usa/asm/usa/5C8770.s.o'
    if script.count(old_object)!=3:
        raise ValueError('Unexpected original file12 data/rodata/bss linker ownership')
    script=script.replace(old_object,'build/usa/asm/usa/file_12_before_5D434C.s.o')
    linker.write_text(script)
    if script.count('.file_12 0x8020D2A0 : AT(file_12_ROM_START)\n')!=1:
        raise ValueError('Candidate linker section does not retain original input alignment')
    print('Compiling six original-location actor lifecycle input objects',flush=True)
    targets=[f"build/usa/{'src/'+name+'.c.o' if kind=='c' else 'asm/usa/'+name+'.s.o'}"
             for kind,name,_,_ in LAYOUT]
    run_step(['make','-j'+str(jobs),'VERSION=usa',*targets],candidate)
    object_metadata=[]
    for (kind,name,start,end),target in zip(LAYOUT,targets):
        obj=candidate/target
        transformed,evidence=elf_text_trim_align(obj.read_bytes(),end-start)
        obj.write_bytes(transformed)
        object_metadata.append({'object':target,'kind':kind,'rom_start':f'0x{start:X}',
                                'rom_end':f'0x{end:X}',**evidence})
    for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
        (candidate/target).unlink(missing_ok=True)
    print('Linking full 32 MiB original-USA candidate',flush=True)
    run_step(['make','-j'+str(jobs),'VERSION=usa','build/usa/mnsg.z64'],candidate)
    result_rom=(candidate/'build/usa/mnsg.z64').read_bytes()
    if len(result_rom)!=ROM_BYTES or result_rom!=original:
        raise ValueError('Full original-ROM byte identity FAILED')
    cand_elf=candidate/'build/usa/mnsg.elf'
    section=verify_section(cand_elf)
    baseline_rels=rel_file12(base_elf); candidate_rels=rel_file12(cand_elf)
    if Counter(baseline_rels)!=Counter(candidate_rels):
        raise ValueError('file_12 original relocation site/type/symbol multiset differs')
    if func_inventory(base_elf)!=func_inventory(cand_elf):
        raise ValueError('Original positive-size ELF function identity differs')
    return {'status':'exact_original_usa_3_c_overlay_integrated_on_upstream',
            'scope':'Upstream original assembly plus 3 matching C; NOT canonical 315+3 central G2',
            'retail_rom_sha1':USA_RETAIL_SHA1,'full_rom_sha1':USA_SHA1,
            'full_rom_bytes_exact':ROM_BYTES,'linked_file12':section,
            'file12_relocations_original':len(baseline_rels),
            'file12_relocations_candidate':len(candidate_rels),
            'file12_semantic_relocation_multiset_identical':True,
            'file12_raw_relocation_order_identical':baseline_rels==candidate_rels,
            'function_symbol_identities_preserved':FUNC_COUNT,
            'reconstructed_function_count':len(FUNCTIONS),
            'reconstructed_original_code_bytes':sum(f[3] for f in FUNCTIONS),
            'objects':object_metadata,
            'limitations':'No canonical 315-C overlay combination, central decomp.verify, decomp.inventory or full local_ci proof'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--upstream',type=Path,required=True)
    p.add_argument('--candidate',type=Path,required=True)
    p.add_argument('--source-dir',type=Path,default=Path(__file__).parent)
    p.add_argument('--jobs',type=int,default=4)
    p.add_argument('--report',type=Path,required=True)
    a=p.parse_args()
    if a.jobs<1 or a.jobs>32:raise ValueError('Unsafe job count')
    result=integrate(a.upstream,a.candidate,a.source_dir,a.jobs)
    if a.report.exists():raise FileExistsError('Report must be created at a new path')
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='objects'},indent=2))

if __name__=='__main__':main()
