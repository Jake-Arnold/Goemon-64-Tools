"""Independent Japanese ELF function and assembly ownership inventory.

Gate the linked image via region_verify before claiming functions are C-owned.
Japanese overlay VMAs can repeat; track identity by section AND symbol name.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

from . import region_verify

SYMBOL = re.compile(r"^\s*([0-9a-fA-F]+)\s+([lg! ])\s+([FO])\s+(\.\S+)\s+([0-9a-fA-F]+)\s+(\S+)\s*$")


def is_executable_section(name: str) -> bool:
    return name in (".main", ".entry", ".ipl3") or re.fullmatch(r"\.file_\d+", name) is not None


def summarize_symbols(text: str, manifest: dict) -> dict:
    functions: dict[str, tuple[str, int, int]] = {}
    markers: dict[str, tuple[str, int, int]] = {}
    for line in text.splitlines():
        m = SYMBOL.fullmatch(line)
        if m is None:
            continue
        addr_str, _binding, kind, section, size_str, name = m.groups()
        if not is_executable_section(section):
            continue
        addr, size = int(addr_str, 16), int(size_str, 16)
        record = (section, addr, size)
        if kind == "F" and size > 0:
            if name in functions:
                raise ValueError("Duplicate ELF function symbol name: " + name)
            functions[name] = record
        elif kind == "O" and name.endswith(".NON_MATCHING"):
            original = name.removesuffix(".NON_MATCHING")
            if original in markers:
                raise ValueError("Duplicate ASM marker: " + name)
            markers[original] = record
    if not functions:
        raise ValueError("No executable ELF functions found")
    claimed = {fn["name"] for unit in manifest["units"] for fn in unit["functions"]}
    unmarked = set(functions) - set(markers)
    if unmarked != claimed:
        raise ValueError("Japanese C-vs-assembly ownership differs from verified manifest: "
                         + str(sorted(unmarked ^ claimed)[:8]))
    for unit in manifest["units"]:
        for fn in unit["functions"]:
            record = functions[fn["name"]]
            if record != (".main", fn["vram"], fn["size"]):
                raise ValueError("Japanese C function symbol extent differs from manifest")
    for name in functions.keys() & markers.keys():
        fn, marker = functions[name], markers[name]
        if fn[:2] != marker[:2]:
            raise ValueError("Original ASM marker section or address mismatch: " + name)
        if fn[2] != marker[2] and not (name == "__ipl3_textbin" and marker[2] == 1):
            raise ValueError("Original ASM marker size mismatch: " + name)
    alias_extents = Counter((section, addr, size) for section, addr, size in functions.values())
    sections: dict[str, dict[str, int]] = {}
    for name, (section, _addr, size) in functions.items():
        row = sections.setdefault(section, {"function_entries": 0, "assembly_marked": 0,
                                            "matching_c": 0, "total_symbol_bytes": 0})
        row["function_entries"] += 1
        row["assembly_marked" if name in markers else "matching_c"] += 1
        row["total_symbol_bytes"] += size
    sorted_symbols = [(name, *functions[name], name in markers) for name in sorted(functions)]
    identity_sha256 = hashlib.sha256(json.dumps(sorted_symbols, separators=(",", ":")).encode()).hexdigest()
    return {"format": "goemon-japan-elf-function-inventory-v1", "region": "japan_0",
            "identified_positive_size_elf_entries": len(functions),
            "assembly_marked_entries": len(functions.keys() & markers.keys()),
            "reviewed_matching_c_entries": len(claimed),
            "unmarked_unreviewed_entries": 0,
            "reviewed_matching_c_bytes": sum(fn["size"] for unit in manifest["units"] for fn in unit["functions"]),
            "section_count": len(sections),
            "same_section_address_size_aliases": sum(count-1 for count in alias_extents.values() if count > 1),
            "nonfunction_NON_MATCHING_markers_excluded": len(set(markers)-set(functions)),
            "symbol_identity_sha256": identity_sha256,
            "sections": {name: sections[name] for name in sorted(sections)},
            "notes": ["Includes .entry and .ipl3 ELF F symbols, not necessarily ordinary game functions.",
                      "Overlay function VMAs can repeat; identifiers preserve section identity.",
                      "Remaining ASM count is based on explicit NON_MATCHING markers only.",
                      "C count is accepted only after independent exact 32/16 MiB region verification."]}


def collect(checkout: Path, retail: Path, *, source_dir: Path = region_verify.ROOT,
            objdump: str = "mips-linux-gnu-objdump", objcopy: str = "mips-linux-gnu-objcopy") -> dict:
    manifest = region_verify.load_manifest()
    proof = region_verify.verify_japan(checkout, retail, manifest, source_dir=source_dir,
                                        objcopy=objcopy, objdump=objdump)
    executable = checkout / "build/japan_0/mnsg.elf"
    symbols = subprocess.run([objdump, "-t", str(executable)], check=True,
                             capture_output=True, text=True).stdout
    summary = summarize_symbols(symbols, manifest)
    summary.update({"source_upstream_commit": manifest["upstream_commit"],
                    "linked_expanded_rom_sha1": proof["expanded"]["sha1"],
                    "recompressed_retail_sha1": proof["retail"]["sha1"],
                    "matching_c_gate": proof["status"]})
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", required=True, type=Path)
    parser.add_argument("--retail-output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--source-dir", type=Path, default=region_verify.ROOT)
    parser.add_argument("--objdump", default="mips-linux-gnu-objdump")
    parser.add_argument("--objcopy", default="mips-linux-gnu-objcopy")
    args = parser.parse_args(argv)
    if args.report.exists() or args.report.is_symlink():
        parser.error("Report exists; refuses overwrite")
    if args.report.resolve() in (args.retail_output.resolve(),
                                  (args.checkout / "config/japan_0/baserom.z64").resolve()):
        parser.error("Report must not be a ROM")
    result = collect(args.checkout, args.retail_output, source_dir=args.source_dir,
                     objdump=args.objdump, objcopy=args.objcopy)
    with args.report.open("x", encoding="utf-8") as out:
        json.dump(result, out, indent=2)
        out.write("\n")
    print(f"Japanese ELF: {result['identified_positive_size_elf_entries']} entries; "
          f"{result['assembly_marked_entries']} assembly-marked; "
          f"{result['reviewed_matching_c_entries']} exact C")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
