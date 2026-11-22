**CANONICAL FOLLOW-UP — PASSED_G2_LOCAL:** All three functions documented here subsequently passed the complete current-branch USA gates and are part of the six-function canonical promotion at **1,962 C / 84,340 original bytes / 5,401 ASM**. See [six-function canonical promotion proof](../../results/usa_92f0_six_g2_promotion_20261122.json), [combined G2](../../results/combined.json), and [strict inventory](../../results/inventory.json). Japan was not changed.

**Original-upstream research update — 22 November 2026:** The third ELF-layout blocker described below was resolved. The [padding proof](PADDING_FIXED_20261122.md) and [verifier](verify_original_unit.py) prove all three USA C sources (156 original bytes) *together* against a clean pinned-original full 32 MiB ROM, all 7,376 original positive-size ELF function identities and 82,216 original-upstream relocations. The previous failure report below is preserved for reproducibility, not current status. The next canonical gate was pending when this original-upstream research update was written; it passed later as recorded above.

---

# USA original-native C: two whole-ROM/ELF exact, third native and ROM exact but ELF-blocked

**22 November 2026. Research-only; NO canonical USA accepted-C promotion.**

## Corrected provenance / deduplication

Before counting any function, the complete historical *accepted* original-ROM proof `decomp/results/combined.json` (1,956 matching original-USA C functions, Git blob `b56df0396798ef6607a1beaed55274654fb05fe7`) was searched by exact original function name and ROM offset. The most recent nine additional accepted functions in the documented USA 1,965 total are scheduler routines. The separate `usa_crossregion51_20261122/manifest.json` (51 names) and later `usa_crossregion48_followup_20261122/manifest.json` (48 more names) isolated-matching research sets were also checked. None of the following three functions is in those accepted/research sets.

Earlier USA draft PR #162's `func_80008798_9398` and `func_8000A0F0_ACF0`, all five purportedly new functions in draft PR #164, and another six rediscovered functions investigated in the originating chat **were already accepted C**. PR #164 was closed unmerged and PR #162 corrected. These duplicate routines must **never** add to new-function counts.

## Genuine original-address C evidence

| Function (guest VMA) | Original USA ROM offset | Bytes | Proven level |
|---|---:|---:|---|
| `func_8000A18C_AD8C` (`0x8000A18C`) | `0xAD8C` | 48 | Original-IDO exact, full original-upstream ROM+ELF+relocs exact |
| `func_8000AAE8_B6E8` (`0x8000AAE8`) | `0xB6E8` | 40 | Original-IDO exact, full original-upstream ROM+ELF+relocs exact |
| `func_8000AB30_B730` (`0x8000AB30`) | `0xB730` | 68 | Original-IDO 68/68 bytes exact, 2 symbolic relocations, full original-upstream ROM and relocations exact; **strict ELF blocked** |

**Two fully verified new functions / 88 original machine-code bytes:** an actual clean scratch copy of pinned `mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, original SGI IDO 5.3 `-O2 -mips2`, Splat, and MIPS binutils rebuilt **33,554,432/33,554,432 original USA bytes identical**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, complete **7,376/7,376 positive-size original ELF function identities**, **82,216/82,216 original-upstream ELF relocations** (section/offset/type/symbol). The original 16 MiB retail source SHA-1 was `df8083a54296b8c151917c5333e1c85f014a2a66`. The two targets themselves have exact original 48B/40B boundaries. **A fresh, separate extraction and native build reproduced this exact full-ROM result.** The original ELF SHA-256 is `83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038`; candidate ELF SHA-256 is `71c82f7a2e3c578a64e4a910c91b4e127efd110ed5aae2b680623986eabff52f` (ELF file hashes differ; original semantic inventories match).

### Third-function native challenge

The third source writes a byte in a large indexed state-table offset and compiles to the exact original 17 MIPS instructions. IDO emits its correct 68-byte ELF `STT_FUNC` extent within an 80-byte section due to alignment, and the candidate has the original pair of `R_MIPS_HI16` / `R_MIPS_LO16` relocations for `D_8008CCC0_8D8C0` at text offsets `0x0` and `0x4`. With it included in the original mixed `B280`/`BEA0` source unit, the **complete 32 MiB ROM remains byte-identical** and all **82,216 relocation records remain exact**. The three newly authored target symbols retain the exact original extents.

**Not full original ELF:** the assembler integration erroneously enlarges the **unchanged** adjacent `func_8000AFA8_BBA8` symbol from **752 to 760 bytes** (eight trailing section-padding bytes). The overall positive-FUNC count remains 7,376 but the identity multiset mismatches in this one place. Three structural experiments (splitting at `0xB730`, extending the mixed unit to `0xC1D0`, and retaining natural NOP alignment with original `GLOBAL_ASM` siblings) still left the same eight-byte FUNC extent problem. No original opcodes, linker output bytes, or original function semantics were modified; source/metadata patching to evade the strict gate is **not** accepted. The third function remains `FAILED_ELF / RESEARCH_ONLY`, not promoted.

### Host tests

GCC 14.2 and Clang 17 compiled the **actual three authored C source files** with `-fsanitize=address,undefined -fno-sanitize-recover=all`. Both passed **4,096 deterministic input cases per function**, checking untouched bytes, 12 iteration boundaries, correct state-field propagation and all expected indexed byte writes. This is synthetic host memory, not actual N64 gameplay testing.

## Replay (private ROM and original IDO toolchain required)

Run from an x86-64 Linux host with the **already restored** project environment. The verifier never writes to the pinned source; it refuses an existing scratch output directory.

```bash
python3 verify_pinned_original.py \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions \
  --out /private/NEW-proof-dir

bash tests/run_host.sh /private/NEW-host-dir
```

Optional negative-control replay of the third function (`--try-third`) builds three C implementations and expects the ROM and relocations to match, **but exits with status 2** because the positive-size ELF identity gate fails. The private output includes a `sanitized_report.json`; generated ROM, objects, raw assembly and ELF remain local and should not be uploaded.

## Canonical promotion boundary

This is an **original-upstream** original-ROM proof, not a `decomp.verify` build with all **1,965** currently accepted USA C functions. The canonical **82,103 semantic-relocation gate**, strict inventory, all 7,376 staged function identities and full `decomp.local_ci` **were not executed** in this work because the live complete toolkit checkout is unavailable in the native build shell. None of the three functions was staged into the official manifest or promoted. **USA stays 1,965 accepted C / 84,648 original bytes / 5,398 ASM.** Japan remains independent.

The deliverable includes only authored C, a source-only verifier, host tests and sanitized findings. No original ROM bytes, proprietary compiler, extracted original ASM, game assets, ELF/object binaries, saves, memory dumps or personal data are included.
