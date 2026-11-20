# Mini Ebisumaru speed path — native matching-C research (20 November 2026)

**RESEARCH_ONLY, not a production matching-C promotion.** Original-USA ROM/input verification was performed locally; the current 1,723-C decomp baseline could not be transferred into the Linux execution container for combined testing.

## Two original-address exact C candidates

- `mini_reset.c`: `func_801E276C_59E67C`, ROM `0x59E67C`, VMA `0x801E276C`, 148 bytes. Writes `0.8f` miniature / `2.0f` normal into movement-limit fields. IDO native bytes: **148/148 exact**.
- `speed_ease.c`: `func_801E3DE0_59FCF0`, ROM `0x59FCF0`, VMA `0x801E3DE0`, 220 bytes. Eases and clamps task `+0xE4` and writes scaled task `+0xE8`. IDO native bytes: **220/220 exact**. The double-precision divider comparison requires `> 8.0`, not the initially hypothesized reverse.

Compiled with original IDO 5.3, original `mnsg` C flags `-O2 -mips2 -G 0 -non_shared` and pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. The ROM was supplied privately and was never committed.

## Native proof actually run

Clean pinned upstream USA ROM rebuilt SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Both functions replaced **together** by original-order linker staging in `file_11`; surrounding native ASM retained. Only compiler-added trailing `.text` zero alignment padding (12 bytes for reset; 4 for ease) was omitted using section-size metadata, without changing instructions or relocations. Both compiled functions match their original complete code ranges. Resulting full original USA ROM is **33,554,432/33,554,432 bytes identical**. Original-versus-two-C pristine ELFs have **7,376/7,376** positive-sized FUNC name/VMA/size identities and **82,216/82,216** semantic relocation tuples equal across 72 sections, including **8,825/8,825** `file_11` relocations.

## Promotion not performed

The current `chatgptweb/decomp` 1,723-C checkout could not be cloned into this container (`github.com` DNS unavailable; connector source contents are not automatically a local checkout). Combined `python3 -m decomp.verify`, `decomp.inventory`, and full `decomp.local_ci` were **NOT RUN**. Therefore no accepted manifest, combined proof, inventory or production code was changed. The accepted USA count remains **1,723**. Emulator gameplay was **NOT RUN**.

Original 4,320-byte movement clamp `func_801CD310_589220` remains ASM. Bundled m2c decompilation first required `asm/usa/data/5B8500.data.s` to resolve its jump table and then failed with `AssertionError: jtbl list must not be empty`; no matching candidate was generated. The other speed-selector `func_801E1C90_59DBA0` remains open.

Next gate: stage the two exact source bodies with **all** accepted C in the current branch via a fail-closed original-overlay adapter, then run fresh native `decomp.verify`, `decomp.inventory`, full `decomp.local_ci` and inspect ELF/relocation equality. Do not promote from this pristine upstream proof alone. C structures are 32-bit MIPS layout research types, not portable 64-bit host structs.

No original ROM bytes, generated ASM, binaries, assets, toolchains or game-memory dumps are included. See `proof.json` for original address, length and SHA-256 fingerprints.
