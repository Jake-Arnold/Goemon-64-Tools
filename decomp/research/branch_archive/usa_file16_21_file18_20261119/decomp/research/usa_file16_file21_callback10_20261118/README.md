# USA file_16 / file_21 original-address C callback research — 18 Nov 2026

**RESEARCH_ONLY** — all ten match in an original-upstream scratch full-ROM reconstruction, but they have **not** passed a combined build with all canonical accepted C. At the live start, the canonical inventory had **951 accepted USA C / 38,816 bytes** and **39 Japan-0 C / 2,092 bytes**. This batch does not change those accepted counts.

## Ten distinct original functions, two separate code overlays

| Overlay | Original function / ROM offset | Bytes | Observed write |
|---|---|---:|---|
| file_16 | `func_801CBE68_668598` / `0x668598` | 16 | second argument `+0x05 = 7` |
| file_16 | `func_801CC1FC_66892C` / `0x66892C` | 16 | second argument `+0x05 = 8` |
| file_16 | `func_801CC20C_66893C` / `0x66893C` | 16 | second argument `+0x05 = 2` |
| file_16 | `func_801CC21C_66894C` / `0x66894C` | 16 | second argument `+0x05 = 8` |
| file_16 | `func_801CC22C_66895C` / `0x66895C` | 16 | second argument `+0x05 = 2` |
| file_21 | `func_8020D734_69D974` / `0x69D974` | 16 | second argument `+0x05 = 6` |
| file_21 | `func_8020D744_69D984` / `0x69D984` | 16 | second argument `+0x05 = 1` |
| file_21 | `func_8020D754_69D994` / `0x69D994` | 16 | second argument `+0x05 = 7` |
| file_21 | `func_8020D764_69D9A4` / `0x69D9A4` | 12 | second argument `+0x05 = 0` |
| file_21 | `func_8020D770_69D9B0` / `0x69D9B0` | 12 | second argument `+0x05 = 0` |

The five `file_16` pointer references occur in original `667B90.s`; four `file_21` pointer references occur in `69D4E0.s` (the fifth did not occur as a resolved `%hi` address-load in this static scan). No observed direct `jal` call sites. This points to **callback-table or callback-registration state transitions**, not yet identified gameplay meaning. The field `+0x05` cannot responsibly be assigned a specific enum/phase name without runtime evidence. The routines use an unused first argument whose original IDO 5.3 compilation writes `$a0` to `0($sp)`. There is no instruction padding inside each recovered function.

## Verification actually run

- Authentic original retail USA SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66`. Original decompressed 32 MiB USA SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`. Original upstream `mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, verified from the provided source archive.
- Bundled standalone Python 3.12, Splat, original IDO 5.3 `-O2 -mips2` and GNU MIPS binutils 2.45.90. Original USA decompression, extraction, original full-ROM baseline build and byte comparison **PASS**.
- Four exact original function-slice boundaries for `file_16` and three for `file_21` restored in a scratch Splat configuration. See below.
- Three C translation units (`sources/file16_status_single.c`, `sources/file16_status_four.c`, `sources/file21_status_five.c`), **10/10 original MIPS bodies native IDO exact**; all original symbol start/size identities preserved.
- Scratch ROM after combined staged native C + unmodified surrounding original ASM: **33,554,432 / 33,554,432 bytes identical**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Semantic ELF relocation records **82,216 / 82,216**, all **72 / 72** sections match; linked original positive-size ELF FUNC names/VMAs/sizes **7,376 / 7,376**, zero missing/extra; full source/toolchain comparison script reported no differences.
- GCC `-std=c11 -Wall -Wextra -Werror -Wno-unused-parameter -O1 -fno-omit-frame-pointer -fsanitize=address,undefined` host regression PASS, 120 invocations; verified all constant writes and intact adjacent bytes. Source file and test Git blob SHA-1 hashes in proof report equal actual locally executed files.
- Original code anchor checker `verify_rom_anchors.py` passed **10/10** SHA-256 original offsets, rejecting a 16 MiB retail-ROM argument.

## Exact original-address scratch layout

Copy the verified original upstream to a **separate disposable workspace**; never modify the pinned pristine baseline. Modify the scratch `config/usa/splat.yaml` only:

```text
file_16, subalign: 4
  [0x667B90, asm]
  [0x668598, c, file16_status_single]
  [0x6685A8, asm]
  [0x66892C, c, file16_status_four]
  [0x66896C, asm]
  [0x66BD60, data]

file_21, subalign: 4
  [0x69D4E0, asm]
  [0x69D974, c, file21_status_five]
  [0x69D9BC, asm]
  [0x69DA50, data]
```

Copy the three `sources/*.c` into scratch `src/`, run Splat and then the original Makefile's IDO compilation. For the five split ASM slices `667B90.s`, `6685A8.s`, `66896C.s`, `69D4E0.s`, `69D9BC.s`, assemble with original MIPS flags plus `-no-pad-sections` so the generated assembly object cannot insert artificial alignment at original C boundaries. For `file21_status_five.c.o` only, original IDO's `.text` section has eight generated trailing **zero** padding bytes (`sh_size 0x50`). Assert those eight bytes zero; reduce only the big-endian ELF32 `.text` section-header `sh_size` to `0x48`. No relocation entries or original MIPS instruction payloads are altered. Re-link using the original `.splat/usa/mnsg.ld` plus original undefined symbol/function scripts and `--emit-relocs`, extract binary via `mips-linux-gnu-objcopy -O binary --pad-to=0x2000000 --gap-fill=0x00`; require exact entire ROM and complete identity/relocation gates. Do not treat an isolated object match as an accepted C promotion.

Host reproduction:

```bash
d=decomp/research/usa_file16_file21_callback10_20261118
gcc -std=c11 -Wall -Wextra -Werror -Wno-unused-parameter -O1 \
  -fno-omit-frame-pointer -fsanitize=address,undefined \
  "$d/sources/file16_status_single.c" "$d/sources/file16_status_four.c" \
  "$d/sources/file21_status_five.c" "$d/test_ten.c" -o /tmp/goemon-file16-file21-test
ASAN_OPTIONS=detect_leaks=1 UBSAN_OPTIONS=halt_on_error=1 /tmp/goemon-file16-file21-test
python3 "$d/verify_rom_anchors.py" \
  --usa-expanded /path/to/privately/owned/usa/baserom.decompressed.z64
```

## Bounded neighboring failure

`func_8020D7E0_69DA20` (ROM `0x69DA20`, original 40 bytes): five C layout/assignment-order variants native-compiled to **28 bytes**, with different address-load/instruction scheduling. Retained ASM, excluded from the ten and from all prospective counts. Another adjacent function `func_8020D77C_69D9BC` (92 bytes) was statically inspected but not native-proved or counted.

## Strict production boundary

A complete current 951-C canonical `chatgptweb/decomp` source checkout was not available in the native host because `git ls-remote` fails GitHub DNS and a live GitHub connector response is not a local checkout. Therefore **961-C combined `python3 -m decomp.verify`, original inventory, and full `python3 -m decomp.local_ci` NOT RUN**. Do not promote/merge the ten functions until all prior 951 C plus the ten satisfy full-ROM, original ELF, semantic relocation, strict inventory and complete sanitizer local CI; compare against any new canonical work before staging. No ROMs, generated MIPS ASM, original assets, object files or binaries are committed.
