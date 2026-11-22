# USA 92F0: three original-ROM exact C functions (research-only)

22 November 2026. Original pin `mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, native IDO 5.3 `-O2 -mips2`.

These are **newly reconstructed, assembly-owned original USA functions**, not a change to the canonical accepted C inventory. The supplied three authored C files replace exactly three `#pragma GLOBAL_ASM` directives in pinned upstream `src/92F0.c` during a private scratch build.

| Original function | ROM address | VMA | Original bytes |
|---|---|---|---:|
| `func_80008798_9398` | `0x9398` | `0x80008798` | 44 |
| `func_8000A0F0_ACF0` | `0xACF0` | `0x8000A0F0` | 64 |
| `func_8000A18C_AD8C` | `0xAD8C` | `0x8000A18C` | 48 |

**Measured native results (replayed):** an entire **33,554,432-byte USA expanded original ROM match**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; **7,376/7,376 positive-size ELF function identities** and **82,216/82,216 original-build ELF relocation tuples** (section, offset, kind, symbol) identical. Original retail ROM SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66` was checked separately, not recompressed. ELF binaries themselves differ in SHA-256 due to metadata, but function identities and original relocation records match. Original native ELF SHA-256 `83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038`; new native ELF SHA-256 `f9f15561d8d2e97fdee47ae1f3c4b9337910d0365355704a5f8e0039c4e95e45`.

The 44-byte display-list routine has 48 bytes in its standalone IDO object due to final alignment padding. The `STT_FUNC` symbol is correctly 44 bytes and the full linked original ROM matches. The halfword-copy C source uses a typed structure with fields named by actual offsets rather than guessed semantic labels. The five-call dispatcher retains five symbolic call relocations.

**Reproduction:** with a clean, original-USA ROM, fully extracted and natively rebuilt pinned upstream checkout and restored project tools, run:

```bash
python3 decomp/research/usa_92f0_three_full_rom_20261122/verify_original_upstream.py \
  --baseline /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions \
  --out /private/NEW-scratch-output
```

This script rejects incorrect ROM/checkout/function hashes, does not overwrite the original checkout, compiles real `src/92F0.c` using the native build, and independently checks full-ROM bytes, ELF function identities and relocations. The complete **source-only downloadable ZIP** is delivered in the originating ChatGPT task: `goemon_usa_92f0_three_full_rom_research_20261122.zip` (SHA-256 `a25f909b3183d8110171b1fe9f888cd7c206a6b1df7c795a8865fc076d9db322`). That attachment also contains the exact full replay script, GCC/Clang ASan+UBSan tests and metadata-only proof. Both sanitizer builds passed 4,096 actual-source trials per function.

**Strict limitation:** this replay is against **original pinned upstream**, **not** the complete 1,965-function modern accepted-C staging adapter. Thus full canonical decomp.verify, 82,103-record canonical semantic-relocation proof, strict inventory and full `decomp.local_ci` are **NOT_RUN**. No decomp manifest/ownership changes. USA officially remains **1,965 accepted functions / 84,648 original bytes**. Do not merge this as a decomp promotion before those independent canonical gates pass.

No original ROM, raw original ASM, game assets, generated objects, ELFs, toolchains, saves or memory dumps are included.
