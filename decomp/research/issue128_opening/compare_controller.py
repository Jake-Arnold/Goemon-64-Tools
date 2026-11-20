"""Measure a locally compiled issue #128 controller against the original object."""

import argparse
import hashlib
import json
from pathlib import Path
import struct
from tempfile import TemporaryDirectory

from verify_wrappers import (
    OWNER_ROM, PIN, ROM_SHA1, extract_text, region_relocations, relocations, run, symbols,
)

NAME = "func_8020D998_677378"
VMA = 0x8020D998
ROM_OFFSET = 0x677378
SIZE = 0x43C4
ORIGINAL_TABLE = 0x6940A8
STATE_COUNT = 34
POOL_END = 0x6941F8
TABLES = ((0x6940A8, 34), (0x694130, 6), (0x69417C, 8))


def words(code):
    return [word for (word,) in struct.iter_unpack(">I", code)]


def ordered_calls(relocs):
    return [symbol for offset, kind, symbol in sorted(relocs.elements())
            if kind == "R_MIPS_26"]


def frame_size(first_word):
    if first_word >> 16 != 0x27BD or not first_word & 0x8000:
        raise ValueError("Expected a negative addiu sp, sp prologue")
    return 0x10000 - (first_word & 0xFFFF)


def compare(upstream, candidate, scratch):
    baseline = upstream / "build/usa"
    original_obj = baseline / "asm/usa/676C80.s.o"
    start = ROM_OFFSET - OWNER_ROM
    rom = (upstream / "config/usa/baserom.decompressed.z64").read_bytes()
    if (run("git", "rev-parse", "HEAD", cwd=upstream).strip() != PIN
            or len(rom) != 33554432 or hashlib.sha1(rom).hexdigest() != ROM_SHA1
            or (start, SIZE, "FUNC") not in symbols(original_obj)[NAME]
            or (VMA, SIZE, "FUNC") not in symbols(baseline / "mnsg.elf")[NAME]):
        raise ValueError("Original USA input identity differs")

    original_text = extract_text(original_obj, scratch / "original.text")[start:start + SIZE]
    original_words = words(original_text)
    old_reloc = region_relocations(relocations(original_obj), start, SIZE)
    reloc_sites = {offset for offset, _, _ in old_reloc}
    rom_words = words(rom[ROM_OFFSET:ROM_OFFSET + SIZE])
    if any(a != b and i * 4 not in reloc_sites
           for i, (a, b) in enumerate(zip(original_words, rom_words, strict=True))):
        raise ValueError("Original object text differs from ROM outside relocation sites")

    (entry,) = symbols(candidate)[NAME]
    position, extent, kind = entry
    if kind != "FUNC" or not extent or (position | extent) & 3:
        raise ValueError("Candidate function symbol or extent is invalid")
    candidate_text = extract_text(candidate, scratch / "candidate.text")[position:position + extent]
    if len(candidate_text) != extent:
        raise ValueError("Candidate function exceeds .text")
    candidate_words = words(candidate_text)
    new_reloc = region_relocations(relocations(candidate), position, extent)

    # The first table in this IDO object is the outer dispatch table. Reject a
    # layout outside this known form instead of guessing at state boundaries.
    rodata_relocs = relocations(candidate, ".rel.rodata")
    expected = [(state * 4, "R_MIPS_32", ".text") for state in range(STATE_COUNT)]
    if sorted(row for row in rodata_relocs if row[0] < STATE_COUNT * 4) != expected:
        raise ValueError("Candidate outer dispatch table is not first in .rodata")
    dest = scratch / "candidate.rodata"
    run("mips-linux-gnu-objcopy", "--dump-section", f".rodata={dest}", candidate,
        scratch / "candidate.rodata.copy.o")
    pool = bytearray(dest.read_bytes())
    table = words(pool[:STATE_COUNT * 4])
    target_offsets = set()
    for offset, kind, symbol in rodata_relocs:
        if (kind, symbol) != ("R_MIPS_32", ".text"):
            raise ValueError("Unexpected candidate pool relocation")
        if not 0 <= offset <= len(pool) - 4 or offset & 3 or offset in target_offsets:
            raise ValueError("Candidate table relocation offset is invalid")
        target_offsets.add(offset)
        (section_relative_target,) = struct.unpack_from(">I", pool, offset)
        relative_target = section_relative_target - position
        if not 0 <= relative_target < extent or relative_target & 3:
            raise ValueError("Candidate table target falls outside the controller")
        struct.pack_into(">I", pool, offset, VMA + relative_target)
    original_slots = {
        table_rom - ORIGINAL_TABLE + i * 4
        for table_rom, count in TABLES for i in range(count)
    }
    original_pool = rom[ORIGINAL_TABLE:POOL_END]
    pool_prefix = next((i for i, (before, after) in enumerate(zip(original_pool, pool))
                        if before != after), min(len(original_pool), len(pool)))
    old_starts = [word - VMA for word in words(rom[ORIGINAL_TABLE:ORIGINAL_TABLE + STATE_COUNT * 4])]
    new_starts = [word - position for word in table]
    states = []
    for starts, limit in ((old_starts, SIZE), (new_starts, extent)):
        if (len(starts) != STATE_COUNT or starts != sorted(set(starts))
                or starts[0] <= 0 or starts[-1] >= limit or any(x & 3 for x in starts)):
            raise ValueError("Dispatch table targets are not ordered inside the function")
    old_ends = old_starts[1:] + [SIZE]
    new_ends = new_starts[1:] + [extent]
    for state, (lo, hi, new_lo, new_hi) in enumerate(
            zip(old_starts, old_ends, new_starts, new_ends, strict=True)):
        old = original_words[lo // 4:hi // 4]
        new = candidate_words[new_lo // 4:new_hi // 4]
        states.append({
            "state": state,
            "original_entry": lo,
            "candidate_entry": new_lo,
            "original_words": len(old),
            "candidate_words": len(new),
            "state_relative_exact_words": sum(a == b for a, b in zip(old, new)),
        })
    first_diff = next((i * 4 for i, (a, b) in enumerate(zip(original_words, candidate_words))
                       if a != b), None)
    original_calls = ordered_calls(old_reloc)
    candidate_calls = ordered_calls(new_reloc)
    return {
        "function": NAME,
        "candidate_object_sha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
        "original_extent": SIZE,
        "candidate_extent": extent,
        "original_stack": frame_size(original_words[0]),
        "candidate_stack": frame_size(candidate_words[0]),
        "first_different_text_offset": first_diff,
        "same_offset_raw_words": sum(a == b for a, b in zip(original_words, candidate_words)),
        "original_text_relocations": old_reloc.total(),
        "candidate_text_relocations": new_reloc.total(),
        "same_offset_type_symbol_relocations": (old_reloc & new_reloc).total(),
        "original_direct_call_count": len(original_calls),
        "candidate_direct_call_count": len(candidate_calls),
        "direct_call_relocations_in_same_order": original_calls == candidate_calls,
        "exact_relocatable_text_and_tuples": original_text == candidate_text and old_reloc == new_reloc,
        "state_entries_same_offset": sum(a == b for a, b in zip(old_starts, new_starts)),
        "original_pool_extent": len(original_pool),
        "candidate_pool_section_extent": len(pool),
        "projected_pool_matching_prefix_bytes": pool_prefix,
        "original_pool_target_words": len(original_slots),
        "candidate_pool_target_words": len(target_offsets),
        "pool_target_words_same_offset_and_value": sum(
            original_pool[i:i + 4] == pool[i:i + 4] for i in original_slots & target_offsets
        ),
        "states": states,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("upstream", type=Path, help="Built pinned original USA checkout")
    parser.add_argument("candidate", type=Path, help="Unlinked native IDO controller object")
    args = parser.parse_args()
    with TemporaryDirectory(prefix="goemon-opening-controller-") as temp:
        print(json.dumps(compare(args.upstream.resolve(), args.candidate.resolve(), Path(temp)),
                         indent=2))


if __name__ == "__main__":
    main()
