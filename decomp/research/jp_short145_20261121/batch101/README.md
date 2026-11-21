# Goemon Japanese ROM — short and repeated C reconstruction (20 Nov 2026)

**Audited outcome: 101 newly recovered original-address isolated C functions,
6,832 Japanese MIPS instruction bytes, zero native-byte mismatches.**
All 101 belong to the current Japanese remaining-assembly snapshot, and remain
unpromoted until a full Japanese G2 integration gate passes.

Proof scope: the original SGI IDO 5.3 -O2 -mips2 compiler emitted code identical
to each individual original function at its Japanese ROM offset. The verification
compares complete function bytes, recorded hashes, and directly name-derived
HI16/LO16/J26 symbol fields; symbols are also present in the original Splat
assembly. A *second* portable verifier independently reproduced 101/101 results.

Two actual reconstructed C bodies also passed GCC ASan/UBSan behaviour smoke tests:
1,000 32-bit memory-field setter cases and 1,000 floating-point interpolation
cases. Host tests are synthetic, not gameplay tests.

**RESEARCH_ONLY / ISOLATED_RELOC_EXACT**: no Japanese *full linked ROM* gate,
original unit ownership, 7,376 ELF function identities, 80,747 semantic
relocations, strict inventory, full local CI, gameplay, or remote GitHub
publication was executed for this batch. The JP2118 C / 5258 ASM baseline
remains unchanged. Do not add 101 to its official matching-C count.

## Files
- `manifest.json`: original ROM offsets, sizes, original bytes SHA-256,
  original native C source SHA-256, and observed individual relocations
- `functions.csv`: sortable 101-function target roster
- `sources/`: reconstructed C source per original function
- `verify_isolated.py`: compiler+original ROM read-only reproducer
- `tests/host_semantic_smoke.c`: 2,000-case host behaviour test

## Reproduce the isolated exact gate

Prepare a pinned `mnsg` checkout at
`7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` and extract the original
Japanese ROM assembly using your private project inputs and the documented
project build environment. Do not commit or redistribute original ROM/assets.

```
python3 verify_isolated.py \
  --upstream /path/to/japan/mnsg-japan \
  --expanded-rom /path/to/japan/mnsg-japan/config/japan_0/baserom.decompressed.z64 \
  --objcopy /path/to/mips-linux-gnu-objcopy \
  --lib-dir /path/to/supplied/binutils-shared-libraries
```

The verifier demands a SHA-1 identical 32MiB Japanese input. It compiles every
C source with the original IDO flags and compares each original function's
complete bytes and symbolic relocatable fields. **This does not rebuild ROM.**

## Reproduce host behaviour tests

```
gcc -std=gnu11 -O1 -g -fsanitize=address,undefined \
  -fno-omit-frame-pointer -Wall -Wextra \
  tests/host_semantic_smoke.c \
  sources/func_8001116C_11D6C.c \
  sources/func_8001203C_12C3C.c -lm -o /tmp/goemon-jp-host-smoke
ASAN_OPTIONS=detect_leaks=0 /tmp/goemon-jp-host-smoke
```

## Required acceptance for actual promotion

Integrate only confirmed original C into the existing fully staged JP2118
baseline, retain all nonconverted assembly, original sections and relocations,
and require the exact original 33,554,432-byte Japanese expanded ROM SHA-1
`6f8745fecc3a5e7d4918c7a73353eb0726116ded` (and retail reference),
unchanged ELF identity/relocation multiset, strict inventory, complete native CI,
then a new `chatgptweb/decomp` commit with `PROGRESS.md` and remote SHA check.
This ZIP is research, not a proven full-ROM promotion.
