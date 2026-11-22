# USA native-exact research: five new C functions, eight combined original-ROM-exact

**22 November 2026 · RESEARCH_ONLY, not canonical accepted-C promotion.**

The original USA version of *Mystical Ninja Starring Goemon* includes five assembly-owned functions reconstructed as human-readable C and compiled using the **original SGI IDO 5.3, `-O2 -mips2`**. The five function extents total **160 original MIPS instruction bytes**. None of the five is listed in the current `chatgptweb/decomp` USA accepted-C manifest. Three additional C functions proved independently in the previous file92 research can coexist with these five, establishing **eight functions / 316 original instruction bytes** together in one original-ROM build.

| New original C function | Original ROM | Original size | Action (only source-grounded) |
| --- | ---: | ---: | --- |
| `func_80012500_13100` | `0x13100` | 24 B | Set two floating-point fields from zero/integer input |
| `func_800127FC_133FC` | `0x133FC` | 28 B | Read three floating-point fields at offsets `0x80..0x88` |
| `func_8001285C_1345C` | `0x1345C` | 28 B | Read three floating-point fields at offsets `0x8C..0x94` |
| `func_8001C9BC_1D5BC` | `0x1D5BC` | 28 B | Copy three floating-point fields at offsets 8, 12, 16 |
| `func_8001C9D8_1D5D8` | `0x1D5D8` | 52 B | Add three floating-point fields at offsets 8, 12, 16 |

## Critical linker/layout finding

A naïve Splat change that places each C function in its own translation unit **FAILED_ROM**: native IDO emits trailing object alignment, shifting following functions by several instructions. Replacing the full original `0x12760` and `0x1D570` ASM segments with separate mixed C/ASM units preserves original function order and code bytes, but the first segment originally ends with eight bytes of anonymous NOP padding. When included at the end of a mixed C object, the assembly processor incorrectly expands the last original function's ELF size from 284 to 292 bytes, despite an exact ROM.

The accepted **research workaround is source-boundary selection, not machine-byte patching**: divide the first segment at `0x14000`, an original function boundary aligned to 16 bytes. Keep `[0x14000,0x14540)` in its original assembly unit. The earlier `[0x12760,0x14000)` can be a C/`GLOBAL_ASM` unit containing the three new C functions while preserving all remaining ASM. The entire `[0x1D570,0x204B0)` unit can contain the other two original C functions and its unconverted assembly. No original MIPS instructions are rewritten and no synthetic ELF symbols are introduced.

## Verification actually performed

- Retail USA ROM SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66`.
- Expanded original USA ROM: `6ea0ed71032ce08fc2745f412d84936382197494`.
- Expanded native rebuilt ROM: **33,554,432 / 33,554,432 bytes identical**; same SHA-1.
- **7,376 / 7,376** positive-size ELF function records match exactly, including all original names, VMAs, extents and symbol properties.
- **82,216 / 82,216** native original-upstream ELF relocations match exactly by section, offset, kind and symbol.
- New five-C candidate ELF SHA-256: `1f6eac845ea6fcd916fd7765da171930008cd3ea5d21da317cd006e5efe869f1`.
- Combined **eight C** candidate ELF SHA-256: `15405c2dd87c8e03f19f747f96bae4de058686220d5a95258ad4b4d149cd6344`. Combined ROM, ELF and relocation checks all passed again.
- The five actual C sources passed **4,096 deterministic trials per source** using GCC 14 and Clang 17 with AddressSanitizer and UndefinedBehaviorSanitizer; in-place float additions were included. The previous three C sources passed their separate sanitised source tests.
- A second, newly extracted pinned upstream scratch workspace completed successful Splat/native IDO make (resumed after the shell execution-limit interruption), full-ROM comparison, all positive-size ELF and all relocation checks.

**These are original-upstream ROM/ELF checks, not full production `decomp.verify` gates.** The modern accepted-USA staging adapter includes 1,965 pre-existing C functions; original-upstream's 82,216 ELF relocations are **not** its 82,103 canonical semantic-relocation records. Full combined modern `decomp.verify`, `decomp.inventory`, and full `decomp.local_ci` are **NOT_RUN** because the current decomp branch could not be cloned into the build shell (DNS failure). No original ASM or accepted manifest has been replaced. Official accepted count **remains USA 1,965 C / 84,648 instruction bytes**.

## Reproduction from private user-owned inputs

This ZIP includes **source files, verifier and host tests only**. It excludes original ROMs, game assets, generated assembly, object files, ELF binaries, toolchains and raw original instruction dumps.

With a clean pinned, extracted and original-built `mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` checkout and the user-provided Goemon dependency/runtime archives restored, run:

```bash
bash tests/run_host.sh /private/new-host-output
python3 verify_pinned_original.py \
  --checkout /private/clean-pinned-mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions \
  --output /private/new-unused-replay-output \
  --also-92f0 --jobs 6
```

The verifier demands correct original ROM/build and commit hashes, reproduces the mixed Splat layout in a scratch copy, recompiles with original IDO 5.3, compares all expanded ROM bytes, 7,376 ELF functions and 82,216 original-upstream relocations; optionally integrates the three earlier proven `92F0.c` C sources. It refuses an existing output directory and leaves the original checkout unchanged. On systems with a short command execution timeout, make may need to be resumed inside the scratch copy before post-build checks. No private original code or data is emitted into this ZIP.

**Next gate:** stage all five functions with the full current canonical USA accepted-C branch, run fresh `python3 -m decomp.verify` against the original retail ROM, then strict `decomp.inventory` and full `decomp.local_ci`. Only if all gates pass may five new functions be counted and published as matching C.
