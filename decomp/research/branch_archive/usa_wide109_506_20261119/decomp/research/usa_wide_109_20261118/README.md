# Goemon original-USA wide 109-function matching-C research

**18 November 2026. RESEARCH_ONLY — not canonical accepted C.**

A broad original USA assembly/IDO search yielded **109 new original-address C functions**, **1,228 original instruction bytes** across **15 distinct game overlays**, in **71 original-address native IDO C translation units**. These were deduplicated against the latest 987-C canonical count, prior accepted native87/file26/file27, older 69/52/41 research queues, the previous 53-function file_18 batch and earlier individual graphics/dracam discoveries. A broad first pass had many duplicates; those were removed before the 109 new-functions claim.

## Source and provenance

- All **71 native-tested C translation units** are preserved byte-for-byte in `source_catalog.txt.gz`, original uncompressed catalog SHA-256 `2135ade4ae21af39c5963f446f109a9add3673d7eb48b95646114da34d6c9970`. Uploaded compressed Git blob SHA-1 `36ace8e5b717ad1bc507b14940b780a661b5a5a2`.
- `candidate_index.tsv.gz` enumerates all **109 original function names, ROM offsets, VMAs, sizes, source unit and per-function SHA-256 of the original ROM bytes**. Original uncompressed index SHA-256 `2e81f4e5e2fe68d72b5eeadeed8eea1ff9a724e6ea5ac2ac0f53a3526193a086`, compressed Git blob SHA-1 `18745d0cd1e42b6d917fe116f004e1c6834c9c39`.
- `unpack_sources.py` restores the exact 71 original C source units to a `sources/` directory with fail-closed catalog hashes. `verify_original.py` authenticates original expanded ROM SHA-1 and all 109 original-instruction SHA-256 anchors. `test109.c.gz` contains the exact actual host regression source compiled in the native research session (Git blob `aa8da77ba96c4aaa8bc26640a48eaf12e4f40131`). No ROM or original assembly bytes are uploaded.

## Regional evidence and actual native verification

Authenticated original USA retail 16 MiB ROM SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66`.
Authenticated expanded 32 MiB ROM SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`.
Pinned upstream `klorfmorf/mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Compiler: original IDO 5.3 `-O2 -mips2`.

1. Untouched original USA upstream rebuilt to the full authentic **33,554,432-byte expanded ROM**, exact.
2. Each of 109 new function candidates was native-compiled at its original MIPS code location and compared against the original instruction code and ELF symbol VMA/size. All **109/109 native-exact**.
3. One *disposable pristine-original-upstream scratch build* staged all 71 C translation units together, retaining surrounding original ASM. Fifteen original Splat overlay code files were segmented at C boundaries using `SUBALIGN(4)` and split ASM `-no-pad-sections`. Original generated zero-only `.text` trailing alignment totaling **420 bytes** was removed through ELF section-size metadata assertions; no original MIPS instructions or relocation bytes modified. Three synthetic NOP FUNC aliases were removed and the original zero-size `D_802287BC_5E3C8C` symbol was restored, preserving original instruction bytes and references.
4. Combined scratch ROM: **33,554,432/33,554,432 bytes identical**, SHA-1 unchanged. Original vs candidate ELF positive-sized FUNC identity triples **7,376/7,376 exact**, new aliases zero; semantic relocations **82,216/82,216 across 72/72 sections exact**. Scratch linked ELF SHA-256: `473f575421cc63091940c9b1f972af54f42a69a4c3617678a211be67350df561`.
5. Host GCC `-std=c11 -Wall -Wextra -Werror -Wno-unused-parameter -O1 -fno-omit-frame-pointer -fsanitize=address,undefined`, compiling all original 71 published C source files together with the exact regression source `test109.c`: **PASS**, 109 individual semantic test cases. These exercise no-op callbacks, byte/halfword/word stores, float setters, getters, and non-target memory preservation.

## Reproduction

```bash
cd decomp/research/usa_wide_109_20261118
python3 unpack_sources.py
python3 verify_original.py --usa-expanded /path/to/owned/usa/baserom.decompressed.z64
gzip -dc test109.c.gz > test109.c
gcc -std=c11 -Wall -Wextra -Werror -Wno-unused-parameter -O1 \
    -fno-omit-frame-pointer -fsanitize=address,undefined \
    sources/*.c test109.c -o /tmp/goemon-wide-109-test
ASAN_OPTIONS=detect_leaks=1 UBSAN_OPTIONS=halt_on_error=1 /tmp/goemon-wide-109-test
```

The above host regression and ROM anchors are ROM-free/local guards, *not* the full native production integration gate. To replay scratch original-MIPS equality, use original IDO, Splat, original linker metadata and this catalog with the pinned upstream source and original ROM, retaining original ELF identities.

## Production boundary

At publication, canonical accepted USA **987 C / 42,640 original instruction bytes** (newly promoted 21 file_27 functions independently during this session), Japanese rev-0 **39 C / 2,092 bytes**. No functions in this research are accepted from this work. Conditional USA accepted total **1,096 C / 43,868 bytes** only if every candidate passes independent canonical integration.

**NOT RUN:** full current canonical 987+109 `python3 -m decomp.verify`, strict `python3 -m decomp.inventory` and full `python3 -m decomp.local_ci`. The complete authenticated current canonical checkout could not be materialized in the native toolchain container due local GitHub DNS failure. Do not promote or merge into `chatgptweb/decomp` until these gates pass. Keep all original ASM owned by the production manifest. No Japanese native matching claimed.

No original ROM, game assets, generated game assembly, object/ELF code, game memory snapshots, proprietary toolchains or personal information committed.
