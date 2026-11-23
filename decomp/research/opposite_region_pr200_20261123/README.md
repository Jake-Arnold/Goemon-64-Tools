# PR #200 counterpart audit — research only

## 23 November 2026 — Opposite-region audit of PR #200 (eight additional USA isolated native matches)

Live base `78e6303e2fe5f4e5f5a17bab50cb62fc792d241b`; pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Authenticated both original expanded ROMs and IDO 5.3. Examined 142 donor entries in PR #200 using same-segment instruction skeletons, unique peers or anchored ordered runs; reconstructed exact canonical offset inventories (USA 2165 / Japan 2428). Outcomes: 95 already canonical, 30 entries in PR #200 itself (15 reciprocal pairs), eight previous research sources, eight new JP-to-USA isolated native matches, one unresolved USA donor at 0x6D64AC. The eight new 72-byte functions total 576 bytes and 35 symbolic relocations. Independent native replay: 8/8 positives exact; 8/8 volatile-local negative controls rejected. Compiler outcome NO_NEW_COMPILER_FINDING. Complete original-ROM integration, linked ELF/inventory/promotion integrity and full local CI NOT_RUN; accepted counts unchanged. Sources, controls, exact manifest, compact counterpart index and replay under `decomp/research/opposite_region_pr200_20261123/`. Full source-only audit and canonical offset lists delivered in the session ZIP SHA256 7e4ed92d687086ce33273279abf55f3ba0c683e58b98c091a2da55e31eb283d4.


The compact index has one row per donor original ROM offset and opposite-region offset. C=canonical, B=PR200, P=prior research, N=new native, U=unresolved. The unresolved USA file_35 function has no unambiguous same-segment structural counterpart: the nearest two Japanese 48-byte candidates are already accepted and indistinguishable by the tested skeleton; no new claim.

Replay against private authenticated inputs, using the same arguments as PR #200's standalone checkpoint:
```sh
LD_LIBRARY_PATH="$W/goemon-runtime-additions/lib" python3 replay.py \
 --usa-rom "$W/mnsg-japan/config/usa/baserom.decompressed.z64" \
 --jp-rom "$W/mnsg-japan/config/japan_0/baserom.decompressed.z64" \
 --usa-splat "$W/mnsg-japan/asm/usa" \
 --jp-splat "$W/mnsg-japan/asm/japan_0" \
 --ido "$W/mnsg-japan/tools/ido-5.3/cc" \
 --objcopy "$W/goemon-dependencies/bin/mips-linux-gnu-objcopy" \
 --readelf /usr/bin/readelf --ledger ../../COMPILER_QUIRKS.md \
 --output /tmp/goemon-cross8-replay
```

No ROM, generated ASM, proprietary binaries or raw machine instructions are committed. Full audit JSON and canonical address lists are in the downloadable session archive rather than this compact GitHub checkpoint.
