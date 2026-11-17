---
name: goemon-region-crosswalk
description: "Use whenever a fixed USA or Japan Goemon 64 guest-RAM global, inventory field, packed event bit, or region-specific memory mapping is discovered or verified; propose and investigate the counterpart ROM address without making speculative writes."
---

# goemon-region-crosswalk

For every new original USA or Japanese **static memory-data** discovery, immediately inspect both ROMs in the same research task. Read `decomp/USA_JAPAN_MEMORY_CROSSWALK_PLAYBOOK.md` and the two regional symbol/evidence maps.

1. Record source ROM identity, guest VMA, width and endianness, mask (for flags), static/dynamic ownership, scene/overlay lifetime, and exact evidence.
2. Search already proven per-region mappings and known exceptions **before** arithmetic. Eligible fixed globals and saved flags: JP candidate = USA + `0x57F0`; USA candidate = JP - `0x57F0`. This is **only a read-only hypothesis**.
3. Investigate the target's original regional MIPS readers/writers or test controlled live A/B/idle samples. Preserve aliasing, packed bit masks, low-byte/full-word distinctions and any counterexamples.
4. Document both addresses, confidence status and independent evidence; list unresolved tests. **Never** auto-translate dynamic player pointers, VM globals, Impact controller allocations, overlays, ROM offsets or code VMAs. Never automatically promote a candidate to a writable toolkit field or official matching-C claim.
5. Commit evidence on a `decomp/*` branch with PROGRESS; port only reviewed toolkit-relevant findings separately to a `toolkit/*` branch from main.

Known examples: `0x8015C607 → 0x80161DF7` weapon, `0x800C7AA4 → 0x800CD294` submode, `0x8015C60C & 0x20 → 0x80161DFC & 0x20` Benkei. JP pause `0x800CD2D6` disputed; JP snowflake `0x80162057` is a `+0x57F1` exception; JP battery `0x80161DF9 & 0x20` unverified.
