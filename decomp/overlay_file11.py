"""Pinned USA file_11 thirteen-function promotion adapter.

This is an opt-in original-ROM verification stage, never a gameplay patch. The
selector and intervening code remain assembly-owned. Assembly slices and all
relocations are retained while lowering the overlay's link SUBALIGN to 4.

Production callers must only append the 13 claimed functions after
verify_linked_stage() succeeds AND the entire 32 MiB candidate ROM compares
byte-for-byte with the trusted baseline. This module never increments a claim.
"""
from __future__ import annotations

from collections import Counter
import hashlib
from pathlib import Path
import re
import shutil
import struct

try:
    from .research.trim_elf32_mips_text import trim_text_section
except ImportError:
    from research.trim_elf32_mips_text import trim_text_section

REGION = "usa"
ROM_SHA1 = "6ea0ed71032ce08fc2745f412d84936382197494"
ROM_START = 0x587370
TEXT_END = 0x5B8500
VMA_START = 0x801CB460
OVERLAY_SIZE = 0x41400
OVERLAY_RELOCATIONS = 8825
STAGE_FORMAT = "goemon-file11-character-switch-13-v1"
LINKER_OLD = ".file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(16)"
LINKER_NEW = ".file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(4)"
SOURCE_SPECS = (
    ("usa_character_switch_entry.c", "character_switch_entry", "f607d2b0342ba9b3ece7bf52769bbb09b5a59faef989752467e6dc2e736b3b18", "5d8cec511b0b7d00c626a1bb3b87dd17454e1e996ae5fd719b7b9df52c9a04e0"),
    ("usa_character_switch_sync.c", "character_switch_sync", "525f8655c5f41681e3fb53841aa8254016a47fa7fd457090ea7cda12521614fb", "d547538caee0555757a297aefc4230c08b93503658b9644e870f8fb5506d9d25"),
    ("usa_character_switch_alt.c", "character_switch_alt", "6816720d380252b8fa789079551c015bd245316565cfc24d96c7d596b323c24d", "7f059fbfb0dde21f450156bd79f234e79f450c3fc8d157b7f6816686a87e03a5"),
    ("usa_character_switch_actor_wrappers.c", "character_switch_wrappers", "5091d28046356990f8b48b269a241da1a596794b0ef588ddb82a41877e663ec9", "e2d70831ab0b5180dc760a7775bf134b772e88abd319ad68e646821f59fc29c9"),
)
# Exactly eight ordered linker sections, not thirteen independent C objects.
# The first C section contains two functions, the last contains nine.
CHUNKS = (
    ("asm", "587370", 0x587370, 0x12078),
    ("c", "character_switch_entry", 0x5993E8, 0x34),
    ("asm", "59941C", 0x59941C, 0xB4),
    ("c", "character_switch_sync", 0x5994D0, 0x94),
    ("c", "character_switch_alt", 0x599564, 0x84),
    ("asm", "5995E8", 0x5995E8, 0x330),
    ("c", "character_switch_wrappers", 0x599918, 0x120),
    ("asm", "599A38", 0x599A38, 0x1EAC8),
)
# Name, ROM address, bytes, trusted SHA-256 of original instruction bytes.
FUNCTIONS = (
    ("func_801DD4D8_5993E8", 0x5993E8, 40, "e5d88c3382a2f7de59e90a2cccd8985f3bfb3d61f167a6d8e9fa82fb8529487d"),
    ("func_801DD500_599410", 0x599410, 12, "b48732223e740fed84b92fbee5fa9a3fb0197fb627625e29f574bc94a423c1a5"),
    ("func_801DD5C0_5994D0", 0x5994D0, 148, "bad0b42cbda479a929526c9585f6d4e0f6a80b3824fb332be9462b685525c81f"),
    ("func_801DD654_599564", 0x599564, 132, "b6db221fe20f44b79ba9f14652a63e6a6febd2e4331ea8e11f5395d3156383bf"),
    ("func_801DDA08_599918", 0x599918, 32, "81cffd3a059aeb31bc478f85cdeacffcbff96279ccd9ba757c96b92c75426ae3"),
    ("func_801DDA28_599938", 0x599938, 32, "81cffd3a059aeb31bc478f85cdeacffcbff96279ccd9ba757c96b92c75426ae3"),
    ("func_801DDA48_599958", 0x599958, 32, "81cffd3a059aeb31bc478f85cdeacffcbff96279ccd9ba757c96b92c75426ae3"),
    ("func_801DDA68_599978", 0x599978, 32, "f2d70d5871d86d9f81579a3c87aa0abd3c6fb76e065c89b7bfe808d80a2f2264"),
    ("func_801DDA88_599998", 0x599998, 32, "f2d70d5871d86d9f81579a3c87aa0abd3c6fb76e065c89b7bfe808d80a2f2264"),
    ("func_801DDAA8_5999B8", 0x5999B8, 32, "7ef80d10f4a8205c1b3b4b5b797b706c3244c1f8626add3a7045f20cc7873aff"),
    ("func_801DDAC8_5999D8", 0x5999D8, 32, "7ef80d10f4a8205c1b3b4b5b797b706c3244c1f8626add3a7045f20cc7873aff"),
    ("func_801DDAE8_5999F8", 0x5999F8, 32, "7ef80d10f4a8205c1b3b4b5b797b706c3244c1f8626add3a7045f20cc7873aff"),
    ("func_801DDB08_599A18", 0x599A18, 32, "7ef80d10f4a8205c1b3b4b5b797b706c3244c1f8626add3a7045f20cc7873aff"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stage_config(text: str) -> str:
    """Patch only the pristine pinned file_11 segment and refuse repeat staging."""
    names = list(re.finditer(r"(?m)^  - name: (\S+)\s*$", text))
    labels = [n.group(1) for n in names]
    if labels.count("file_11") != 1 or labels.count("file_12") != 1:
        raise ValueError("Missing or duplicated file_11 or file_12 Splat segment")
    i = labels.index("file_11")
    if labels[i + 1] != "file_12":
        raise ValueError("Pinned file_11 Splat adjacency changed")
    begin, end = names[i].start(), names[i + 1].start()
    block = text[begin:end]
    original = "    - [0x587370, asm]\n    - [0x5B8500, data]"
    if (block.count(original) != 1 or block.count("    subalign: 16\n") != 1 or
            "    start: 0x587370\n" not in block or
            "    vram: 0x801CB460\n" not in block):
        raise ValueError("Pinned file_11 Splat layout differs")
    replacement = "\n".join(
        f"    - [0x{start:X}, {kind}{(', ' + name) if kind == 'c' else ''}]"
        for kind, name, start, _ in CHUNKS
    ) + "\n    - [0x5B8500, data]"
    return text[:begin] + block.replace(original, replacement) + text[end:]


def checked_source_copies(checkout: Path, research_dir: Path,
                          reference_rom: bytes) -> list[tuple[Path, Path]]:
    """Return prevalidated copies without filesystem mutations."""
    checkout = Path(checkout)
    research_dir = Path(research_dir)
    if len(reference_rom) != 0x2000000 or hashlib.sha1(reference_rom).hexdigest() != ROM_SHA1:
        raise ValueError("USA decompressed ROM identity mismatch")
    for name, offset, size, hash_value in FUNCTIONS:
        if sha256(reference_rom[offset:offset + size]) != hash_value:
            raise ValueError(f"Original function identity changed: {name}")
    sources = []
    for source_name, target_name, expected_hash, _ in SOURCE_SPECS:
        source = research_dir / source_name
        dest = checkout / "src" / (target_name + ".c")
        if not source.is_file() or dest.exists():
            raise ValueError("Missing or colliding staged file_11 source: " + target_name)
        source_bytes = source.read_bytes()
        if sha256(source_bytes.replace(b"\r\n", b"\n")) != expected_hash or b"GLOBAL_ASM" in source_bytes:
            raise ValueError("Unreviewed file_11 source hash or assembly ownership")
        sources.append((source, dest))
    return sources


def stage_sources(checkout: Path, research_dir: Path, reference_rom: bytes):
    """Validate all sources and trusted original input before changing checkout."""
    checkout = Path(checkout)
    sources = checked_source_copies(checkout, research_dir, reference_rom)
    config = checkout / "config/usa/splat.yaml"
    staged = stage_config(config.read_text(encoding="utf-8"))
    for source, dest in sources:
        shutil.copyfile(source, dest)
    config.write_text(staged, encoding="utf-8", newline="\n")


def object_targets() -> list[str]:
    return [
        f"build/usa/{'src/' + name + '.c.o' if kind == 'c' else 'asm/usa/' + name + '.s.o'}"
        for kind, name, _, _ in CHUNKS
    ]


def prepare_objects(checkout: Path) -> dict:
    """Preflight all eight compiled objects, then patch ELF text and linker once."""
    checkout = Path(checkout)
    linker = checkout / ".splat/usa/mnsg.ld"
    script = linker.read_text(encoding="utf-8")
    if script.count(LINKER_OLD) != 1:
        raise ValueError("Pinned generated file_11 linker SUBALIGN anchor changed")
    staged = []
    for (kind, name, _, size), target in zip(CHUNKS, object_targets()):
        path = checkout / target
        before = path.read_bytes()
        after = trim_text_section(before, size)
        if kind == "c":
            spec = next(x for x in SOURCE_SPECS if x[1] == name)
            if sha256(after) != spec[3]:
                raise ValueError("Staged file_11 IDO object SHA mismatch: " + name)
        staged.append((path, after))
    for path, data in staged:
        path.write_bytes(data)
    linker.write_text(script.replace(LINKER_OLD, LINKER_NEW), encoding="utf-8", newline="\n")
    return {"object_count": len(staged), "chunks": len(CHUNKS), "compiler_c_objects": 4}


class ElfInspector:
    """Small read-only ELF32 BE parser for exact linked overlay provenance."""

    def __init__(self, data: bytes):
        self.data = data
        if (len(data) < 52 or data[:6] != b"\x7fELF\x01\x02" or
                struct.unpack_from(">H", data, 18)[0] != 8):
            raise ValueError("Expected ELF32 big-endian MIPS image")
        shoff = struct.unpack_from(">I", data, 32)[0]
        entsize, count, str_index = struct.unpack_from(">HHH", data, 46)
        if entsize < 40 or count == 0 or str_index >= count or shoff + entsize * count > len(data):
            raise ValueError("Malformed ELF section table")
        hdrs = [struct.unpack_from(">IIIIIIIIII", data, shoff + i * entsize) for i in range(count)]
        names = self._bytes(hdrs[str_index][4], hdrs[str_index][5])
        self.sections = {}
        for i, h in enumerate(hdrs):
            self.sections[self._cstring(names, h[0])] = (i, h)
        self.hdrs = hdrs
        self._symbols = None

    def _bytes(self, offset, size):
        if offset < 0 or size < 0 or offset + size > len(self.data):
            raise ValueError("ELF section outside file")
        return self.data[offset:offset + size]

    @staticmethod
    def _cstring(data: bytes, offset: int) -> str:
        if offset < 0 or offset >= len(data):
            raise ValueError("ELF string offset outside table")
        end = data.find(b"\0", offset)
        if end < 0:
            raise ValueError("Unterminated ELF string")
        return data[offset:end].decode("utf-8", errors="replace")

    def symbols(self):
        if self._symbols is not None:
            return self._symbols
        _, sym = self.sections[".symtab"]
        if sym[9] != 16 or sym[5] % 16 or sym[6] >= len(self.hdrs):
            raise ValueError("Malformed ELF32 symbol table")
        strings = self._bytes(self.hdrs[sym[6]][4], self.hdrs[sym[6]][5])
        blob = self._bytes(sym[4], sym[5])
        output = []
        for off in range(0, len(blob), 16):
            name_offset, value, size, info, other, section = struct.unpack_from(">IIIBBH", blob, off)
            output.append((self._cstring(strings, name_offset), value, size, info, section))
        self._symbols = output
        return output

    def overlay_info(self):
        index, section = self.sections[".file_11"]
        if section[3] != VMA_START or section[5] != OVERLAY_SIZE:
            raise ValueError("Linked file_11 section VMA/size changed")
        return index, section

    def relocations(self):
        _, rel = self.sections[".rel.file_11"]
        if rel[1] != 9 or rel[5] % 8 or rel[7] != self.overlay_info()[0]:
            raise ValueError("Unexpected file_11 ELF relocation section")
        sym = self.symbols()
        result = []
        blob = self._bytes(rel[4], rel[5])
        for off in range(0, len(blob), 8):
            site, info = struct.unpack_from(">II", blob, off)
            symid = info >> 8
            if symid >= len(sym):
                raise ValueError("Invalid file_11 relocation symbol index")
            name, value, _, _, _ = sym[symid]
            result.append((site, info & 255, value, name))
        return result


def verify_linked_map(mapping: str) -> dict:
    """Require the 8 expected C/ASM objects, exact VMAs, and exact lengths."""
    start = re.search(r"(?m)^\.file_11\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)", mapping)
    if start is None or (int(start.group(1), 16), int(start.group(2), 16)) != (VMA_START, OVERLAY_SIZE):
        raise ValueError("Linked file_11 map output section changed")
    end = re.search(r"(?m)^\.file_11_bss(?:\s|$)", mapping[start.end():])
    if end is None:
        raise ValueError("Missing file_11 BSS map boundary")
    block = mapping[start.end():start.end() + end.start()]
    positions = []
    for (kind, name, rom, size), target in zip(CHUNKS, object_targets()):
        word = target + "(.text)"
        hits = list(re.finditer(r"(?m)^\s*" + re.escape(word) + r"\s*$", block))
        if len(hits) != 1:
            raise ValueError("Staged file_11 input not linked exactly once: " + word)
        positions.append(hits[0].start())
        extent = re.search(r"(?m)^\s*\.text\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\s+" + re.escape(target) + r"\s*$", block)
        expected = (VMA_START + rom - ROM_START, size)
        if extent is None or (int(extent.group(1), 16), int(extent.group(2), 16)) != expected:
            raise ValueError("Staged file_11 object link extent differs: " + target)
    if positions != sorted(positions):
        raise ValueError("Staged file_11 objects linked out of original order")
    if "build/usa/asm/usa/587370.s.o(.text)" not in block:
        raise ValueError("Missing initial file_11 assembly owner")
    return {"ordered_objects": len(positions), "text_bytes": sum(c[3] for c in CHUNKS)}


def verify_linked_stage(original_rom: bytes, rebuilt_rom: bytes,
                        baseline_elf: bytes, candidate_elf: bytes,
                        candidate_checkout: Path, research_dir: Path) -> dict:
    """Fail closed unless C ownership, native symbols, ROM and relocations match."""
    if (len(original_rom) != 0x2000000 or
            hashlib.sha1(original_rom).hexdigest() != ROM_SHA1 or
            rebuilt_rom != original_rom):
        raise ValueError("Required exact 32 MiB USA ROM gate failed")
    checkout = Path(candidate_checkout)
    sources = Path(research_dir)
    splat = checkout / "config/usa/splat.yaml"
    content = splat.read_text(encoding="utf-8")
    if not all(f"[0x{start:X}, {kind}" in content for kind, _, start, _ in CHUNKS):
        raise ValueError("Missing staged file_11 Splat chunks")
    if content.count("    - [0x587370, asm]") != 1 or content.count("    - [0x5B8500, data]") != 1:
        raise ValueError("Nonunique staged file_11 extents")
    if (checkout / ".splat/usa/mnsg.ld").read_text().count(LINKER_NEW) != 1:
        raise ValueError("file_11 overlay linker alignment not verified")
    map_proof = verify_linked_map((checkout / "build/usa/mnsg.map").read_text(encoding="utf-8"))
    for source_name, target_name, expected_source, expected_object in SOURCE_SPECS:
        content = (checkout / "src" / (target_name + ".c")).read_bytes()
        if (sha256(content.replace(b"\r\n", b"\n")) != expected_source or
                sha256((sources / source_name).read_bytes().replace(b"\r\n", b"\n")) != expected_source or
                sha256((checkout / "build/usa/src" / (target_name + ".c.o")).read_bytes()) != expected_object):
            raise ValueError("file_11 source/object ownership proof failed: " + target_name)
    original = ElfInspector(baseline_elf)
    candidate = ElfInspector(candidate_elf)
    original.overlay_info()
    candidate.overlay_info()
    original_rel = original.relocations()
    candidate_rel = candidate.relocations()
    if (len(original_rel) != OVERLAY_RELOCATIONS or
            len(candidate_rel) != OVERLAY_RELOCATIONS or
            Counter(original_rel) != Counter(candidate_rel)):
        raise ValueError("file_11 semantic relocation set changed")
    symbols = candidate.symbols()
    linked_section = candidate.overlay_info()[0]
    for name, rom, size, digest in FUNCTIONS:
        address = VMA_START + (rom - ROM_START)
        matches = [s for s in symbols if s[0] == name and s[1] == address and s[2] == size and s[4] == linked_section and (s[3] & 15) == 2]
        if len(matches) != 1 or sha256(rebuilt_rom[rom:rom + size]) != digest:
            raise ValueError("file_11 linked function ownership or bytes failed: " + name)
    return {
        "stage": STAGE_FORMAT,
        "full_rom_match": True,
        "rom_sha1": ROM_SHA1,
        "overlay_vma": hex(VMA_START),
        "overlay_bytes": OVERLAY_SIZE,
        "relocations_identical_multiset": len(candidate_rel),
        "relocations_identical_order": original_rel == candidate_rel,
        "claimed_functions": len(FUNCTIONS),
        "claimed_bytes": sum(f[2] for f in FUNCTIONS),
        "ownership": map_proof,
        "functions": [{"name": name, "rom_offset": rom, "vma": VMA_START + rom - ROM_START, "size": size, "sha256": digest} for name, rom, size, digest in FUNCTIONS],
    }