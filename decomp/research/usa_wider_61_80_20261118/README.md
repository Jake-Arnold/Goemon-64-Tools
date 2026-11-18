# Original USA resource 61–80: 52 matching-C functions

**18 November 2026 — RESEARCH_ONLY (production +0).** This extends the verified adjacent resource sweeps into the final numbered code-overlay resources in the original USA game.

## Original-address matches

Native IDO 5.3 (`-O2 -mips2`) produced **52/52 exact original MIPS functions / 576 instruction bytes** across 15 resources. Every compiled function was linked at its original overlay VMA; source blobs and original offsets are recorded in `source_registry.json`. All 52 source-file Git blob hashes were checked against the independently compiled, tested local files before publication.

**31 original no-op callbacks; 21 nontrivial functions** including flag/zero tests, actor field getters/setters, constant byte/word writes, and signed division or unsigned multiplication by 30. These are distinct original function addresses, not synthetic aliases. Research sources are in `sources/file_N/`. 

## Full original upstream scratch proof

- Authenticated original decompressed USA 32 MiB ROM SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`.
- An unchanged pinned upstream checkout (`klorfmorf/mnsg` `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`) rebuilt 33,554,432 / 33,554,432 original ROM bytes exactly.
- In a separate *disposable original upstream* checkout, all **52 exact C sources were simultaneously staged** while retaining surrounding original ASM. Only verified zero ELF alignment padding was trimmed; no instruction code was patched.
- The scratch output retained **33,554,432/33,554,432 identical ROM bytes**, unchanged SHA-1, **7,376/7,376 positive-sized original ELF function identities**, and **5,416/5,416 semantic relocations** across all 15 changed resource overlays. Recorded per-resource relocation counts appear in `scratch_proof.json`.
- GCC host tests compiled the actual 52 C sources with `-Werror -fsanitize=address,undefined` and passed: no-op calls; zero/nonzero checks; read and writes; byte constants; unsigned multiply wrap; signed divide on negatives. No sanitizer types disabled.
- The standalone reproduction package also contains the local split-ASM/IDO/scratch-link integration program and full semantic fixture. It does **not** contain the ROM, original game assembly, ELF, object files, saves or toolchain.

## Reproduction

Given the separately owned original decompressed USA ROM and pinned native toolchain:

```bash
export PATH=/path/to/goemon-dependencies/bin:$PATH
export LD_LIBRARY_PATH=/path/to/goemon-runtime-additions/lib
python3 verify_research.py --rom /path/to/32MiB-USA.z64 --ido /path/to/mnsg-japan/tools/ido-5.3/cc
gcc -std=gnu11 -O1 -Werror -Wall -Wextra -Wno-unused-parameter \
  -fno-omit-frame-pointer -fsanitize=address,undefined -fno-pie -no-pie \
  sources/file_*/*.c test_smoke.c -o /tmp/goemon61-smoke && /tmp/goemon61-smoke
```

Both commands passed in the research build environment. `verify_research.py` rechecks source Git hashes, original ROM identity and individual native MIPS bytes. The canonical current-branch combined build is **not run by that script**.

## Limits and remaining work

A bounded first pass identified seven adjacent nested-pointer accessors but their compiled MIPS register choices or extents did not match, so they remain ASM (**FAILED_NATIVE**). Larger functions in resources 61–80 were not exhaustively attempted.

A **complete authenticated checkout of current `chatgptweb/decomp`** could not be materialized in the native compiler container because local GitHub DNS was unavailable. Therefore the current accepted production C, canonical `decomp.verify` / `decomp.inventory`, all production ownership and full `decomp.local_ci` were **NOT RUN** for this batch. This result is `RESEARCH_ONLY`, **zero accepted C added**. At research start: accepted **USA 864 matching C / 37,904 bytes, Japanese 39**.

**Next:** integrate the 52 functions (without double-counting other research batches) into a verified current source checkout. Promote only on fresh byte-identical 33,554,432-byte ROM, original ELF/relocations, strict inventory, and full local CI acceptance.
