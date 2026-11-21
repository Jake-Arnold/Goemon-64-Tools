# USA 18-way game-state dispatcher — original-address IDO C match

**Status: `PASSED_G2_LOCAL`; remote branch promotion is a separate acceptance step.**

The original USA `func_80002040_2C40` starts at expanded ROM `0x2C40`, guest VMA `0x80002040`, and consists of 120 bytes (30 MIPS instructions). The source recovered earlier in GitHub [issue #136](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/136) has been recompiled with native IDO 5.3, integrated with all **1,965** already accepted USA original-address C functions, and verified again independently in a fresh staging replay on 21 November 2026.

## Observed behaviour and original ABI

- Copies the 18 function pointers (72 bytes) from ROM global `D_80058908_59508` into a local `DispatchTable` stack object.
- Reads an **unsigned byte** at `D_8015C5C8_15D1C8[0x3ADD4]`, i.e. offset `0x3ADD4` within the live system-state block, and performs an unchecked indirect call through that stack-local table.
- The original register usage, frame size (`0x68`), 30 instruction positions, and six original function/global relocations require a local `volatile int unused[2]`. Its original source intent is unknown; do not rename it to a gameplay feature.
- The original absolute linker symbol `D_3ADD4` is required by the MIPS compilation path to preserve two `R_MIPS_HI16`/`R_MIPS_LO16` relocations; a literal offset generated the same instruction bytes but **not** the same relocation metadata.
- Native compile text `.text` is emitted as 128 bytes, including eight **all-zero trailing alignment bytes**. The stage shrinks only ELF object `.text` metadata to its true 120-byte instruction extent and requires 4-byte section alignment. No MIPS instructions, function bytes, ROM data or ASM instructions are modified or patched.

## Actual verification (21 November 2026)

- Original retail USA SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; decompressed SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Original compiler IDO 5.3 with the pinned original USA flags; native instruction order and registers, 120/120 original bytes at `0x80002040`.
- Full USA ROM `33,554,432 / 33,554,432` bytes identical after adding the dispatcher to 1,965 accepted C functions; same SHA-1.
- Original ELF positive-sized identities `7,376 / 7,376` identical, including function extent and output section.
- Original entire semantic relocation multiset `82,103 / 82,103` identical.
- Strict `decomp.inventory.summarize_inventory`: `1,966 original matching C`, `84,768 original matching C instruction bytes`, `5,397 remaining ASM`, no new positive-sized aliases; two pre-existing section-size annotations unchanged.
- Independently replayed with this stage's own `stage`, `build` and `verify` commands on a second copied predecessor checkout, same native ROM, ELF, relocations and inventory result.
- Actual original-source GCC ASan/UBSan host test: **54 valid-state calls** across all 18 states, including three repetitions per state, correct selection exactly once per call.
- Full `python3 -m decomp.local_ci` on the supplied `(17)` zip snapshot with added dispatcher adapter/tests and sanitizer step: **330 decomp Python tests (3 skipped)** and **349 verifier tests (4 skipped)**, all configured host sanitizer and research/ledger checks passed. This snapshot predates remote scheduler5/scheduler6 source files; **the full suite on latest live HEAD 553bc85e was not executed as one combined checkout**, so this is still local proof, not a remotely promoted function.
- No gameplay emulation executed; valid state range 0..17 is an observed 18-pointer array size, not proof that higher byte values never occur. No bounds guard is added to the matching source.

## Reproduction

The build requires the user-supplied retail USA ROM, pinned clean upstream `klorfmorf/mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, and bundled original IDO 5.3/toolchain. First produce an exact **1,965-C accepted predecessor** using the existing current branch native stages through `decomp.scheduler6_g2_promotion`, and retain a fresh pinned original-USA baseline ELF checkout.

```bash
python3 -m decomp.usa_dispatcher_g2_promotion stage --checkout "$CANDIDATE_1965" --prior "$WORK/dispatcher-prior-1965"
python3 -m decomp.usa_dispatcher_g2_promotion build --checkout "$CANDIDATE_1965" --deps "$DEPS" --runtime "$RUNTIME"
python3 -m decomp.usa_dispatcher_g2_promotion verify --checkout "$CANDIDATE_1965" --prior "$WORK/dispatcher-prior-1965" --original "$ORIGINAL_UPSTREAM_BASELINE"
python3 -m unittest decomp.test_usa_dispatcher_g2_promotion
python3 -m decomp.local_ci
```

The stage verifies precise ROM, source hash, accepted 1965 predecessor proof, original ASM ownership, exact 30-instruction span, six existing original relocations, ELF function IDs and full ROM SHA-1. It refuses stale or already accepted targets and does not alter production inventories until all gates pass. The private original ROM, original extracted ASM, built objects and ELF are **not** distributed.
