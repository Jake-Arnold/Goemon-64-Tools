> **Later canonical result:** All six functions described here passed canonical USA combined G2, full ELF/relocation comparison, strict inventory and full `decomp.local_ci`. Final canonical USA is **1,962 C / 84,340 original bytes / 5,401 ASM**. See [the six-function promotion proof](../../results/usa_92f0_six_g2_promotion_20261122.json). The research details below preserve native/source provenance and the earlier original-upstream proof.

# USA six original-upstream ROM/ELF exact C functions — two newly recovered (204 bytes)

**22 November 2026 · RESEARCH_ONLY. No canonical accepted-C promotion.**

Recovered two previously ASM-owned and not-yet-researched original-USA C functions from the real pinned `src/92F0.c` unit. The original SGI IDO 5.3 compiler emits exact original MIPS instructions and symbol relocations only when specific source-line grouping and loop comparison expressions are retained:

| Original function | ROM | Guest VMA | Bytes | Status |
|---|---:|---:|---:|---|
| `func_8000A548_B148` | `0xB148` | `0x8000A548` | **124** | **NEW** original exact |
| `func_8000A5C4_B1C4` | `0xB1C4` | `0x8000A5C4` | **80** | **NEW** original exact |
| `func_8000A18C_AD8C` | `0xAD8C` | `0x8000A18C` | 48 | earlier draft PR #165 |
| `func_8000AAE8_B6E8` | `0xB6E8` | `0x8000AAE8` | 40 | earlier draft PR #165 |
| `func_8000AB30_B730` | `0xB730` | `0x8000AB30` | 68 | earlier draft PR #165 |
| `func_800108BC_114BC` | `0x114BC` | `0x800108BC` | 40 | existing cross-region 48 research; first integrated in predecessor kit |
| **Six combined** | | | **400** | original-upstream ROM/ELF exact |

A deduplication against the **entire** canonical 1,956-function `decomp/results/combined.json` original-USA accepted list, the subsequent nine scheduler functions, and both independent research crossregion51 and crossregion48 indices found the **two new 92F0 functions absent**. Do not count the other four as new in this task. The 40-byte menu graphics function was already part of the research cross-region48 index; this kit also retains its previously measured original-upstream whole-ROM integration.

## Independently verified native proof

Both a resumed IDO build after a documented C-prototype error and a **second fresh, clean pinned-upstream scratch extraction/build** passed the same complete checks. Original repository pin `klorfmorf/mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. USA original retail ROM SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`. Final original expanded USA ROM **33,554,432/33,554,432 byte-identical**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. **7,376/7,376** original positive-size ELF function identity tuples exact; **82,216/82,216** original-upstream ELF relocations exact. All six original function symbol addresses, byte extents and original instruction bytes exact. Final ELF SHA-256 `ad7416d0342eb98210aeea739954efe0bfaf8dc736e936f432936927002486e9`; original ELF SHA-256 `83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038`. Overall ELF file hash need not equal the original, but function/relocation identities do.

**Compiler and source-layout quirks:** Detailed positive/negative IDO controls in [COMPILER_QUIRKS_addendum.md](COMPILER_QUIRKS_addendum.md). `A5C4` is a 0x98-byte structure copy preserving destination word zero; `A548` applies that copy across the inclusive 0x98-byte table range. Source newlines influence instruction scheduling. The original `0xBEA0` linker-alignment workaround for two *unowned* NOP padding words is retained. The `0x112F0..0x11580` menu-graphics subunit avoids breaking original rodata jump-table labels.

## Reproduction — original compiler, pinned checkout and private ROM

Use the uploaded private original USA ROM and original SGI IDO 5.3/Splat environment configured by the Project `GOEMON_BUILD_ENVIRONMENT.md`. The source kit contains **no ROM, original assembly dump, binary, original ELF, compiler, or asset data**. Have an already extracted and exact-rebuilt clean pinned-original upstream checkout.

```bash
python3 verify_original_six.py \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions \
  --out /private/NEW-unexisting-output --jobs 24

python3 tests/test_ido_source_lines.py \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions
python3 tests/test_ido_shapes.py \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions
python3 -m unittest discover -s tests -p test_padding.py -v
bash tests/run_host.sh /private/NEW-host-output
```

`verify_original_six.py` rejects a dirty/wrong original checkout, a wrong 16 MiB or 32 MiB ROM SHA-1, already existing output, unexpected original function-byte SHA-256, modified line-sensitive C text, changed Splat source-window lists, incorrect post-endlabel unowned NOPs, any output ROM difference, any of the 7,376 ELF positive functions changing, or any of the 82,216 original-upstream relocations changing. It uses a **scratch copy** and restores eight NOP padding bytes through the original linker, without instruction patching or artificial symbols. Tests compile and execute **the actual C files**, not approximated copies. GCC14.2/Clang17 ASan+UBSan 4,096 cases each of six source functions were run PASS; IDO source-line positive and negative controls PASS; three Python padding controls PASS.

## Strict promotion limitation

The current `chatgptweb/decomp` **1,965-accepted-USA-C complete staging checkout cannot be cloned from the native build shell** because GitHub DNS is unavailable. The original-upstream byte-exact ROM/ELF proof is not the **modern canonical decomp** combined proof: canonical `python3 -m decomp.verify`, **82,103 semantic relocations**, strict `decomp.inventory`, and full post-integration `decomp.local_ci` are **NOT RUN**. **Do not promote or merge** until those are actually completed. Official USA stays **1,965 accepted C / 84,648 original machine-code bytes**, 5,398 ASM; two new functions are **RESEARCH_ONLY / ORIGINAL_UPSTREAM_ROM_ELF_EXACT**.
