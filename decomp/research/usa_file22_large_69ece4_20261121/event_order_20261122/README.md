# Goemon USA file22 large function: original MIPS vs native IDO C memory-event equivalence

**22 November 2026. RESEARCH_ONLY / FAILED_NATIVE.** This research targets the entire original function `func_801CC0C4_69ECE4` (ROM `[0x69ECE4,0x69F3F4)`, guest `0x801CC0C4`, **1,808 bytes / 452 MIPS instructions**) rather than any adjacent helper. It does not change the accepted decompilation source.

## Original source authentication

- Original 32 MiB expanded USA ROM SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`.
- Original function SHA-256: `eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9`.
- Pinned source checkout: `klorfmorf/mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
- Native compiler: original SGI IDO 5.3, `-O2 -mips2`, canonical `-G 0` and other pinned flags in `reproduce_compiled_ido.py`.
- Reconstructed original ASM and proprietary compiler are *not* distributed in this package.
- The original upstream USA 32 MiB rebuild was independently performed byte-for-byte and exactly matched the same SHA-1 before this experiment.

## New source-level diagnosis: descriptor memory-load order

A direct original-MIPS memory-read journal identified four **per-tile halfword** field loads whose order differed between the original function and the prior IDO-compiled source:

| Relative descriptor offset | Meaning | Original order | Prior compiled order |
|---|---|---:|---:|
| `+0x20` | Source-page pixel width (`s16`) | 1 | 4 |
| `+0x1C` | Page-grid columns (`s16`) | 2 | 3 |
| `+0x22` | Source-page pixel height (`s16`) | 3 | 1 |
| `+0x1E` | Page-grid rows (`s16`) | 4 | 2 |

The prior compiled function performed exactly the same *number* of non-stack reads but in the wrong order. On the original mode-2 input, it had 777 external read events, with a longest ordered identical subsequence of 617. The **160 missed ordered matches correspond to two of the four reordered field reads for each of 80 tile visits**. This matters when descriptor data can change between loads or memory aliasing is possible.

**Bounded compiler hypothesis:** Qualifying the original C field reads at offsets `+0x20`, `+0x1C`, and `+0x22` as `volatile s16` while leaving `+0x1E` nonvolatile causes the original IDO 5.3 compiler to issue the **same four loads in the original order**. (All four `volatile` also works; one or two alone does not.) The change generates no extra instructions in the padded diagnostic and leaves its original 0x140 frame intact. The semantic C source without any diagnostic stack padding exhibits the same corrected read ordering. These qualifiers are an *experiment to control compiler codegen*, **not** proof that the game's original declarations used `volatile`.

## Full native-compiled MIPS execution result

The reproducible `full_effects_oracle.py` uses the **genuine IDO-compiled MIPS machine instructions** of each C source. It executes those and the original MIPS with the same isolated, synthetic big-endian guest address space. It records each *non-stack* guest-data load `(address, width, value)` and each non-stack store `(address, width, value)` in exact order. Instruction fetches and private stack operations are intentionally not part of this external-event equivalence condition.

| Synthetic input class | Completed | Result |
|---|---:|---|
| Original tile maps and alternate format/layouts | 20 | All external reads, stores, graphics exact |
| 64 seeded deterministic alternate positive page/grid geometries | 64 | All external reads, stores, graphics exact |
| Graphics destination deliberately overlaps page map, tile map or texture metadata | 29 | All external reads, stores, graphics exact |
| **Completed total** | **113 / 113** | **Exact ordered event streams** |

**Aggregated per implementation over those 113 executions:**

- **90,910** external guest-memory loads: same addresses, widths, read values and order.
- **100,869** external guest-memory stores: same addresses, widths, stored values and order.
- **33,623** 64-bit graphics commands: identical command bytes and order.
- **4/4** synthetic zero-dimension cases trigger original division guards in both implementations. The break PCs differ and the invalid inputs are excluded from the 113 successful normal runs.
- **10** additional overlapping-memory configurations run beyond the interpreter's allocated memory region in **both** implementations. These are not passes or failures; they were excluded.

Two corrected sources were independently compiled and each passed the full suite:

| Source | IDO output text | Frame | Raw positional words* | Ordered opcode shape* | F300/E700 loads |
|---|---:|---:|---:|---:|---:|
| Corrected *unpadded* semantic C (`...RESEARCH.c`) | 1,728 B | `0xF0` | 21/432 | 334/452 | 1/1 |
| Corrected **artificial-stack** diagnostic (`...DIAGNOSTIC.c`) | 1,744 B | `0x140` | 31/436 | 357/452 | 1/1 |
| Original ROM function | **1,808 B** | **`0x140`** | 452/452 | 452/452 | **3/3** |

*The raw positional denominator is the shorter of the compiled and original code lengths, expressed in 32-bit words, **not** an original-ROM accepted matching count. The ordered opcode-shape score ignores register operands and branch displacements and only measures the ordered longest matching subsequence of opcode types and non-branch immediates. It is a research hint, **not** native matching or a claim that 357 machine instructions are identical. Original C still uses distinct `$fp`/`$ra` allocations and branch-local `F300`/`E700` constants.*

The original startup stack receives different loads and stores from the generated C, even when the diagnostic frame has the original size. There is still **no full machine-code match**.

### Negative control

The former C draft with the **double-scaled u16 tile pointer** was compiled using the same original IDO toolchain. `full_effects_oracle.py` correctly **rejected it immediately** in the original format-0 rendering case: original **767 reads / 825 stores**, incorrect candidate **965 reads / 1,287 stores**, and graphics not equal. This demonstrates the new verifier can detect an authentic prior semantic error rather than passing arbitrary compiled code.

## Reproduction

In a fresh directory, extract this source-only ZIP. Supply your original 32 MiB expanded USA ROM at the pinned upstream checkout's `config/usa/baserom.decompressed.z64`, and provide the original pinned upstream plus the already restored toolchain directories. From the extracted ZIP directory:

```bash
python3 reproduce.py \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions \
  --output /private/NEW-reproduction-directory
```

The orchestrator validates the ROM and original function hashes, checks the Git commit, compiles the two corrected sources and the negative control with the real IDO compiler, validates precisely the original symbol's two HI16/LO16 relocations, runs the 127-case event suite for each corrected source (113 completed cases + 10 excluded alias cases + 4 guard traps), checks opcode shape, rejects the old bug, and writes sanitized JSON and private original-MIPS output objects only inside your selected research output directory. **Do not publish that private output directory**; it contains IDO-produced object files and compiler artefacts. The script itself and `summary.json` contain no original ROM, extracted assembly, game assets or original instruction words.

## Technical implications and limits

- **Memory aliasing no longer explains an output mismatch** for the 113 tested guest-memory configurations. The corrected C has the same *ordered externally visible data-memory operations* and graphics output as the original in those executions. It is still possible that exotic untested input states, true N64 bus/hardware behaviour, different memory-mapped registers or exception paths differ.
- **Compiler source structure and private stack/register liveness remain blockers.** The matched read order requires a codegen-directing source qualifier, and the two long-lived original constants remain allocated to the wrong registers in IDO output. Texture `F300` and `E700` instructions are still globally hoisted instead of emitted once per mode branch. A different C control-flow/variable-lifetime reconstruction is needed for exact MIPS.
- The weak opcode-shape comparison reveals where that next reconstruction can focus. In the padded version, **82/120** tile-lookup instruction shapes align (up from 81); mode dispatch is **12/12**; loop tails **21/21**; texture rectangle emission is only **16/29**. These are aligned instruction categories, not exact words.
- The isolated original-MIPS interpreter is a **research implementation**, not a complete independently verified N64 emulator or a real gameplay-frame capture. The results do not prove universal behavioural equivalence, original Konami source typing, a byte-identical function, or full-ROM acceptance.
- No original-address matching C promotion, complete current USA ROM/ELF/relocation G2, strict inventory or full `decomp.local_ci` has been run on this failed-native target. Previously published USA matching count was **1,965 functions / 84,648 original instruction bytes**, subject to rechecking the current live branch.

## Files in this source-only package

`reproduce.py` is the sole entry point. It depends on `full_effects_oracle.py`, `compare_function_shape.py`, `trace_original_file22_mips.py`, `reproduce_compiled_ido.py` and `dual_region_native_probe.py`. The two corrected C files are separate unpadded and explicitly artificial-stack diagnostics; the old broken source is a negative control. `evidence.json` is a metadata-only result snapshot. No copyrighted original ROM, extracted MIPS, emulator state dump, linker object or proprietary compiler is included.
