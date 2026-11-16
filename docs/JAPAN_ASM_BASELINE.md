# Japanese revision-0 ROM: reproducible assembly-only baseline

**Status (2026-11-15): PASS.** Exact Japanese N64 reconstruction was achieved in a separate pinned klorfmorf/mnsg checkout. This is an assembly-only source-linked ROM rebuild. It is not a Japanese matching-C port and does not make Goemon64Recomp natively execute the Japanese game.

## Required private inputs

- Pinned klorfmorf/mnsg checkout at commit 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee. The user's mnsg-japan.zip includes it, its submodules, and native IDO 5.3.
- Exact Japanese revision-0 original ROM normalized to config/japan_0/baserom.z64, SHA-1 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b.
- Unpacked goemon-dependencies directory: MIPS GNU binutils and Python 3.12 site packages.
- Unpacked goemon-runtime-additions directory: Python 3.12 interpreter/stdlib and MIPS binutils shared libraries.

Never commit ROMs, assets, extracted assembly or these private runtime binaries.

## One-command offline reproduction

Run from the Goemon-64-Tools checkout containing this document:

~~~bash
bash decomp/build_japan_asm_baseline.sh \
  /path/to/mnsg-japan \
  /path/to/goemon-dependencies \
  /path/to/goemon-runtime-additions
~~~

If the Japanese original remains in .n64 16-bit-swapped format, first create the canonical input without modifying the original:

~~~bash
python3 -m decomp.prepare_japan_rom \
  /path/to/original-japanese.n64 \
  /path/to/mnsg-japan/config/japan_0/baserom.z64
~~~

The runner validates the source pin and ROM hashes, loads Python 3.12/Splat/LZKN64, extracts the compressed file table if needed, creates a separate Japanese assembly-only Splat config, regenerates assembly, fixes linker symbols, assembles/links, recompresses using upstream Rommy, and verifies both resulting images byte-for-byte. It leaves upstream config/japan_0/splat.yaml untouched. GOEMON_JOBS controls build concurrency (default 6).

Local-only outputs under the pinned mnsg checkout:

- build/japan_0/mnsg.z64 — 32 MiB decompressed source-linked build
- build/japan_0/mnsg.retail.z64 — 16 MiB original-format compressed build
- build/japan_0/asm-baseline-proof.json — verification metadata

The helper's three commands can also be run individually:

~~~bash
python3 -m decomp.japan_asm_baseline stage-config /path/to/mnsg-japan
# Run Splat in the pinned checkout: python3.12 -m splat split config/japan_0/splat_asm_only.local.yaml
python3 -m decomp.japan_asm_baseline patch-asm /path/to/mnsg-japan
python3 -m decomp.japan_asm_baseline verify /path/to/mnsg-japan \
  --retail-output /path/to/mnsg-japan/build/japan_0/mnsg.retail.z64
~~~

## Root causes and reproducible repairs

1. Original make setup VERSION=japan_0 passed using Splat 0.36.3.
2. The ordinary Japanese make failed because shared USA-specific C files reference asm/usa/nonmatchings; they are unsuitable for Japan before regional C porting.
3. Exactly **189** Japanese Splat C subsegments were replaced by assembly in a separate local configuration; make was invoked with C_FILES=, avoiding USA C inputs.
4. Exactly **22** generated .L symbols were uniquely defined in one assembly object and referenced from another; adding explicit .globl declarations repaired the unresolved symbols. The helper checks all cross-object definitions and fails if they are missing/ambiguous.
5. Exactly **2** generated BSS labels collided with executable symbol names in another overlay. These labels were renamed in the generated assembly only; no data layout or instruction bytes changed.
6. Rebuilt the 32 MiB Japanese image using MIPS assembler, linker and objcopy. Recompressed with original tools/rommy.py --pad --verify. Both images matched reference bytes exactly.

The clean extraction, symbol repairs, full assembly link and recompression were repeated successfully after removing generated build/japan_0 objects. The independent full-byte comparison reported **zero differences**.

## Evidence and verification

| Test | Result |
| --- | --- |
| Pinned source and Japanese input identity | PASS |
| Original Japanese Splat extraction | PASS |
| Fresh Japanese assembly-only split | PASS |
| Unique cross-object labels and BSS aliases | 22 / 2 fixed |
| Rebuilt decompressed ROM | 33,554,432 bytes, SHA-1 6f8745fecc3a5e7d4918c7a73353eb0726116ded, **0 differences** |
| Rebuilt retail ROM | 16,777,216 bytes, SHA-1 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b, **0 differences** |
| ROM-free helper unit tests | 3/3 PASS |
| Shell runner syntax | PASS |
| Matching Japanese C functions | **0 new claims** |
| Fresh USA native full-ROM verification | NOT RUN |
| Emulator gameplay test | NOT RUN |
| Japanese native PC static-recompiled build | NOT RUN |

Reference evidence: decomp/results/japan_0_asm_baseline_2026-11-15.json.

**Next:** Build an opt-in Japan matching-C verifier while keeping the exact assembly-only baseline and USA verification intact. Start with a small native IDO-matching helper; validate its function bytes, relocations, overlay and full ROM before incrementing Japanese C totals.
