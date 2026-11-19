# dracam wide-native eight-C scratch proof — 18 November 2026

**RESEARCH_ONLY. Not yet production accepted.** This follow-up resolves PR #66's original three target hypotheses and extends to five adjacent main-code functions. The verified canonical baseline remains **864 USA / 37,904 bytes**, **39 Japan-0 / 2,092 bytes**. This batch totals **eight new USA C / 352 instruction bytes**, distinct from PRs #63-65 and the earlier 41-function queue.

| USA VMA | Original expanded-ROM offset | Size | Source unit | Recovered observable behavior |
|---|---:|---:|---|---|
| `0x800125D0` | `0x131D0` | 32 | `dracam_controls.c` | Byte at +0x5D and 3 floats at +0x60/+0x64/+0x68 |
| `0x800125F0` | `0x131F0` | 56 | `dracam_controls.c` | Volatile record pointer at +0xCC, byte/halfword/float/word initialization, counters |
| `0x80012878` | `0x13478` | 136 | `dracam_three.c` | Copy a 0x60-byte state, forward two float triples, forward 16-bit field at +0x1A |
| `0x80012900` | `0x13500` | 56 | `dracam_three.c` | Copy 0x60-byte state from owner to caller |
| `0x80012938` | `0x13538` | 8 | `dracam_three.c` | Return pointer at owner +0x6C |
| `0x800133D4` | `0x13FD4` | 12 | `dracam_floats.c` | Float at +0x5C |
| `0x800133E0` | `0x13FE0` | 32 | `dracam_floats.c` | Float triple at +0x60/+0x6C/+0x78 |
| `0x80013508` | `0x14108` | 20 | `dracam_flag.c` | Set 0x80 in byte +4 of linked object pointed to at owner +0x1C |

Original retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`. Original expanded SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Pinned upstream commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Original IDO 5.3 `-O2 -mips2`; MIPS binutils 2.45.90.20260125. The supplied original upstream archive was byte-split, rebuilt and authenticated before research.

## Actual full-ROM scratch result

1. Fresh pinned upstream USA original-ROM baseline rebuilt exactly (33,554,432/33,554,432 bytes).
2. A separate disposable pristine-upstream copy replaced only four complete original code slices, with remaining original ASM preserved:
   - `[0x131D0, c, dracam_controls]` to `[0x13228, asm]`
   - `[0x13478, c, dracam_three]` to `[0x13540, asm]`
   - `[0x13FD4, c, dracam_floats]` to `[0x14000, asm]`
   - `[0x14108, c, dracam_flag]` to `[0x1411C, asm]`
3. Native IDO compiled all eight original functions. `.main` linker `SUBALIGN(4)` and assembler `-no-pad-sections` maintained non-16-byte original boundaries. The four C objects' generated **zero-only** `.text` tail alignment was removed only by reducing ELF32 big-endian `sh_size` headers: controls `0x60→0x58`, three `0xD0→0xC8`, floats `0x30→0x2C`, flag `0x20→0x14`. Trimmed regions were asserted zero; original MIPS instruction bytes and relocations were **not changed**.
4. Full scratch ROM matched original **33,554,432/33,554,432 bytes**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Both generated ELF files preserved **82,216/82,216 semantic relocation identities across 72 sections**, and **7,376/7,376 original positive-sized FUNC name/address/size identities**, with zero additional positive-size aliases.
5. Original-region SHA-256 metadata checker `verify_rom_anchors.py`: eight checks PASS on authenticated expanded USA; invalid retail (16 MiB) input rejected. Metadata and original hashes are in the sanitized JSON report; no original instruction bytes committed.

## Host semantic test

```bash
d=decomp/research/dracam_cross_overlay_20261118
gcc -std=c11 -Wall -Wextra -Werror -O1 -fno-omit-frame-pointer \
  -fsanitize=address,undefined \
  "$d/sources/dracam_three.c" "$d/sources/dracam_controls.c" \
  "$d/sources/dracam_floats.c" "$d/sources/dracam_flag.c" \
  "$d/test_eight.c" -o /tmp/goemon-dracam-eight-test
ASAN_OPTIONS=detect_leaks=1 UBSAN_OPTIONS=halt_on_error=1 /tmp/goemon-dracam-eight-test
python3 "$d/verify_rom_anchors.py" --usa-expanded /path/to/private/baserom.decompressed.z64
```

Host result **PASS**. A host-native pointer has 8-byte alignment unlike N64 o32's 4-byte pointer, so host tests assert behavior and local data consistency, not N64 `offsetof` for pointer-bearing owner structures. This does not change the original MIPS C source.

## Limitations

The native filesystem cannot access a complete authenticated live `chatgptweb/decomp` 864-C checkout because direct `git clone` fails DNS and available GitHub file operations do not materialize the whole source tree. **864+8 canonical combined `decomp.verify`, `decomp.inventory`, and full `decomp.local_ci` have NOT RUN.** Do not merge production C, increase accepted counts, or claim combined proof based on this original-upstream scratch. New functions retain original ASM in the canonical manifest. No Japan native matching run. The previously observed broad cross-overlay callback references remain static reference evidence, not gameplay semantics.
