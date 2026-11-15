"""Read-only MIPS reference comparison of exact USA and Japan decompressed ROMs.

No ROM bytes or disassembly are emitted, only guest address, operation and
ROM-offset metadata. Aligned-word access correspondence is *not* proof of the
meaning of any one byte or of an individual item identity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_SHA1 = {
    "usa": "6ea0ed71032ce08fc2745f412d84936382197494",
    "japan_0": "6f8745fecc3a5e7d4918c7a73353eb0726116ded",
}
OPS = {
    0x20: "lb", 0x21: "lh", 0x23: "lw", 0x24: "lbu",
    0x25: "lhu", 0x27: "lwu", 0x28: "sb", 0x29: "sh",
    0x2B: "sw", 0x31: "lwc1", 0x39: "swc1",
}


def direct_word_refs(data: bytes, targets, window: int = 16):
    """Find LUI + base-register memory operations at selected guest words.

    Signed MIPS low immediate matters: 8015C6D8 is LUI 8016 + -0x3928.
    This does not detect pointer arithmetic or indexed arrays. As the image
    also contains data, individual matches may be false positives.
    """
    if len(data) % 4:
        raise ValueError("Instruction scan needs a word-aligned image")
    if window < 1 or window > 64:
        raise ValueError("Window must be 1-64 instructions")
    target_set = frozenset(targets)
    highs = {((address + 0x8000) >> 16) & 0xFFFF for address in target_set}
    found = defaultdict(list)
    limit = len(data) - 4
    for i in range(0, len(data), 4):
        word = struct.unpack_from(">I", data, i)[0]
        if (word >> 26) != 0x0F:
            continue
        register = (word >> 16) & 31
        high = word & 0xFFFF
        if not register or high not in highs:
            continue
        for j in range(i + 4, min(i + 4 * (window + 1), limit + 1), 4):
            operation_word = struct.unpack_from(">I", data, j)[0]
            opcode = operation_word >> 26
            if opcode in OPS and ((operation_word >> 21) & 31) == register:
                low = operation_word & 0xFFFF
                signed_low = low if low < 0x8000 else low - 0x10000
                address = ((high << 16) + signed_low) & 0xFFFFFFFF
                if address in target_set:
                    found[address].append({
                        "rom_offset": f"0x{j:08X}",
                        "operation": OPS[opcode],
                    })
            if opcode == 0x0F and ((operation_word >> 16) & 31) == register:
                break
    return found


def load_verified(path, version):
    data = Path(path).read_bytes()
    actual = hashlib.sha1(data).hexdigest()
    expected = EXPECTED_SHA1[version]
    if actual != expected or len(data) != 33554432:
        raise ValueError(
            f"{version} input must be original 32 MiB decompressed ROM: "
            f"expected {expected}, got {actual} ({len(data)} bytes)")
    return data


def compare(usa, japan, rows):
    """rows: (slug, USA guest byte, Japanese guest byte, provenance)."""
    rows = list(rows)
    usa_words = {address & ~3 for _, address, _, _ in rows}
    jp_words = {address & ~3 for _, _, address, _ in rows}
    usa_refs = direct_word_refs(usa, usa_words)
    jp_refs = direct_word_refs(japan, jp_words)
    result = []
    for slug, usa_byte, jp_byte, provenance in rows:
        a = usa_refs.get(usa_byte & ~3, [])
        b = jp_refs.get(jp_byte & ~3, [])
        usa_ops = dict(sorted(Counter(row["operation"] for row in a).items()))
        jp_ops = dict(sorted(Counter(row["operation"] for row in b).items()))
        result.append({
            "slug": slug,
            "mapping_provenance": provenance,
            "usa_byte_address": f"0x{usa_byte:08X}",
            "japan_byte_address": f"0x{jp_byte:08X}",
            "usa_word_address": f"0x{usa_byte & ~3:08X}",
            "japan_word_address": f"0x{jp_byte & ~3:08X}",
            "usa_accesses": usa_ops,
            "japan_accesses": jp_ops,
            "both_have_same_direct_access_pattern": bool(usa_ops and usa_ops == jp_ops),
            "usa_rom_sites": [row["rom_offset"] for row in a],
            "japan_rom_sites": [row["rom_offset"] for row in b],
        })
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--usa", type=Path, required=True,
                        help="32 MiB decompressed USA ROM (big-endian)")
    parser.add_argument("--japan", type=Path, required=True,
                        help="32 MiB decompressed Japan ROM (big-endian)")
    parser.add_argument("--output", type=Path,
                        help="Write JSON metadata, never ROM bytes")
    parser.add_argument("--summary", action="store_true",
                        help="Only show correspondence counts")
    args = parser.parse_args(argv)
    from practice.unlocks import UNLOCKS
    from practice.region_unlocks import japan_unlock_lead
    rows = []
    for item in UNLOCKS:
        lead = japan_unlock_lead(item)
        if lead is not None:
            rows.append((item.slug, item.address, lead.address, lead.confidence))
    observed = compare(load_verified(args.usa, "usa"),
                       load_verified(args.japan, "japan_0"), rows)
    count = sum(row["both_have_same_direct_access_pattern"] for row in observed)
    result = {
        "description": "Direct MIPS aligned-word refs; not item identity proof",
        "rom_sha1": EXPECTED_SHA1,
        "candidate_count": len(observed),
        "same_access_pattern_count": count,
        "candidates": observed,
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.summary:
        print(f"ROM direct-reference scan: {count}/{len(observed)} paired patterns")
    elif not args.output:
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
