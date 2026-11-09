"""Compare a single isolated GNU MIPS object with ROM-verified USA assembly.

Research diagnostic ONLY: relocation-masked isolated matches are not original-
address matches and cannot replace an independently linked full-ROM proof.
Input ROM, original assembly and compiled objects must remain outside Git.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess

ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
ROM_SIZE = 33554432
LINE = re.compile(r"/\*\s+([0-9A-Fa-f]+)\s+([0-9A-Fa-f]{8})\s+([0-9A-Fa-f]{8})\s*\*/\s*(.*)")
WORD = re.compile(r"^\s*([0-9a-fA-F]+):\s+([0-9a-fA-F]{8})\s+", re.M)
RELOC = re.compile(r"^\s*([0-9a-fA-F]+):\s+R_MIPS_([A-Z0-9_]+)\b", re.M)
SYMBOL = re.compile(r"^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+FUNC\s+\w+\s+\w+\s+(\d+)\s+(\S+)\s*$", re.M)
MASKS = {"26": 0xFC000000, "HI16": 0xFFFF0000, "LO16": 0xFFFF0000, "GPREL16": 0xFFFF0000}


def original_rows(source, function):
    expected = re.fullmatch(r"func_([0-9A-F]{8})_([0-9A-F]+)", function)
    if expected is None:
        raise ValueError("invalid main-segment function name")
    vma, offset = (int(x, 16) for x in expected.groups())
    if vma != offset + 0x7FFFF400:
        raise ValueError("function ROM/VMA mapping differs")
    lines = source.splitlines()
    starts = [i for i, line in enumerate(lines)
              if re.fullmatch(r"glabel\s+" + re.escape(function) + r"\s*", line)]
    if len(starts) != 1:
        raise ValueError("missing original function label (or ambiguous duplicate)")
    begin = starts[0]
    ends = [i for i in range(begin + 1, len(lines))
            if re.fullmatch(r"endlabel\s+" + re.escape(function) + r"\s*", lines[i])]
    if len(ends) != 1:
        raise ValueError("missing or ambiguous original endlabel")
    end = ends[0]
    if any(re.match(r"(?:glabel|endlabel)\s+", line) for line in lines[begin+1:end]):
        raise ValueError("nested or overlapping original function labels")
    rows = []
    for line in lines[begin+1:end]:
        match = LINE.search(line)
        if not match:
            continue
        off, address, word = (int(match.group(i), 16) for i in (1, 2, 3))
        if off != offset + 4 * len(rows) or address != vma + 4 * len(rows):
            raise ValueError(f"noncontiguous original ROM/VMA at {address:#x}")
        asm = match.group(4).strip()
        reloc = "26" if re.search(r"\b(?:jal|j)\s+\S+", asm) else (
            "HI16" if "%hi(" in asm else "LO16" if "%lo(" in asm else None)
        rows.append((word, reloc))
    if not rows:
        raise ValueError("missing original instruction rows")
    return offset, rows


def verify_rom(rom, offset, rows):
    data = Path(rom).read_bytes()
    if len(data) != ROM_SIZE or hashlib.sha1(data).hexdigest() != ROM_SHA1:
        raise ValueError("reference decompressed USA ROM size/SHA-1 mismatch")
    original_bytes = b"".join(struct.pack(">I", w) for w, _ in rows)
    if data[offset:offset + len(original_bytes)] != original_bytes:
        raise ValueError("original ASM instruction words do not match reference ROM")


def parse_elf_info(header, symbols, name):
    if not re.search(r"Class:\s+ELF32\b", header) or not re.search(r"Data:\s+2's complement, big endian", header):
        raise ValueError("expected ELF32 big-endian object")
    if not re.search(r"Machine:\s+MIPS", header):
        raise ValueError("expected MIPS ELF machine")
    found = [(int(m.group(1), 16), int(m.group(2))) for m in SYMBOL.finditer(symbols)
             if m.group(4) == name]
    if len(found) != 1 or found[0][1] <= 0:
        raise ValueError("missing, ambiguous or empty defined FUNC symbol")
    return found[0]


def parse_objdump(text, start, size):
    section = re.search(r"Disassembly of section \.text:\n(.*?)(?=\nDisassembly of section |\Z)", text, re.S)
    if section is None:
        raise ValueError("missing disassembled .text section")
    ins = {}
    for m in WORD.finditer(section.group(1)):
        off = int(m.group(1), 16)
        if off in ins:
            raise ValueError("duplicate disassembled instruction address")
        ins[off] = int(m.group(2), 16)
    relocs = {}
    for m in RELOC.finditer(section.group(1)):
        off, kind = int(m.group(1), 16), m.group(2)
        if off in relocs or kind not in MASKS:
            raise ValueError("duplicate or unsupported MIPS relocation")
        relocs[off] = kind
    if size % 4 or any(start+i not in ins for i in range(0, size, 4)):
        raise ValueError("incomplete or misaligned candidate symbol instruction stream")
    if any(start <= off < start+size and off not in ins for off in relocs):
        raise ValueError("relocation does not address an instruction")
    return [(ins[start+i], relocs.get(start+i)) for i in range(0, size, 4)]


def comparison(original, candidate):
    direct = matched = masked = matched_masked = layout = 0
    mismatches = []
    for i in range(min(len(original), len(candidate))):
        ow, okind = original[i]
        cw, ckind = candidate[i]
        if okind is None and ckind is None:
            direct += 1
            good = ow == cw
            matched += good
        elif okind is not None and okind == ckind:
            masked += 1
            good = (ow & MASKS[okind]) == (cw & MASKS[ckind])
            matched_masked += good
        else:
            layout += 1
            good = False
        if not good:
            mismatches.append(f"+0x{i*4:X}")
    structurally_equal = (len(original) == len(candidate) and not mismatches and not layout)
    return {"original_bytes": len(original)*4, "candidate_bytes": len(candidate)*4,
            "matching_nonreloc_words": matched, "comparable_nonreloc_words": direct,
            "matching_relocated_shapes": matched_masked, "comparable_relocated_shapes": masked,
            "relocation_layout_differences": layout, "first_mismatches": mismatches[:20],
            "isolated_structural_match_only": structurally_equal}


def run(args):
    offset, original = original_rows(args.original.read_text(encoding="utf-8"), args.function)
    verify_rom(args.rom, offset, original)
    def tool(*parts):
        return subprocess.run(parts, capture_output=True, text=True, check=True).stdout
    header = tool("readelf", "-Wh", str(args.object))
    symbols = tool("readelf", "-Ws", str(args.object))
    start, size = parse_elf_info(header, symbols, args.function)
    candidate = parse_objdump(tool(args.objdump, "-dr", "-z", str(args.object)), start, size)
    result = comparison(original, candidate)
    result.update({"function": args.function, "rom_sha1": ROM_SHA1,
                   "proof_level": "ROM-validated original plus isolated relocatable object; NO full-ROM match"})
    print(json.dumps(result, indent=2))
    return 0 if result["isolated_structural_match_only"] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--object", type=Path, required=True)
    parser.add_argument("--function", required=True)
    parser.add_argument("--objdump", default="mips-linux-gnu-objdump")
    args = parser.parse_args()
    try:
        return run(args)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
