# USA resources 25/27 adjacent original-address matching C — 17 November 2026

Status: **21 functions in original file 27 have native IDO exact, source-unit exact, upstream scratch whole-ROM exact**; **one 72-byte function in file 25 has isolated native exact only** because its C syntax introduces new linker relocation symbols. **No canonical production promotion.** Do not merge into a production stage without the full decomp verification gate.

## Verified original-ROM identity

- Region: USA NG5E
- Original 16 MiB retail SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66`
- 32 MiB decompressed SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`
- Pinned upstream: `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`
- Native compiler: IDO 5.3 `-O2 -mips2` and original MIPS binutils

## Original file 27 native-exact C

Seven original-address source units, covering **21 distinct original functions and 1,316 original instruction bytes**:

| Source | VMA | Original ROM | Functions | Bytes | Proof |
| --- | --- | --- | ---: | ---: | --- |
| `group490.c` | `0x08000490` | `0x6AF8A0` | 3 | 108 | Exact |
| `group59c.c` | `0x0800059C` | `0x6AF9AC` | 3 | 172 | Exact |
| `group8c4.c` | `0x080008C4` | `0x6AFCD4` | 3 | 276 | Exact |
| `groupa7c.c` | `0x08000A7C` | `0x6AFE8C` | 5 | 380 | Exact |
| `group1380.c` | `0x08001380` | `0x6B0790` | 5 | 304 | Exact |
| `wrapper172c_v1.c` | `0x0800172C` | `0x6B0B3C` | 1 | 64 | Exact |
| `noop37ec_v1.c` | `0x080037EC` | `0x6B2BFC` | 1 | 12 | Exact |

**Native verification:** each source unit compiled with original IDO and linked at its original overlay address; all machine-code instruction bytes match original ROM. The first five units contain 19 contiguous-in-group functions. The remaining two are isolated single functions. All 21 preserve original FUNC names/addresses/sizes in the full scratch linked ELF.

**Upstream whole-ROM scratch proof:** Reconstructed and authenticated a clean disposable checkout of pinned upstream (not the live production branch), compiled original C units, retained the entire rest of the original assembly, adjusted only proven-zero section-end alignment padding (never game instruction bytes), and successfully rebuilt a **33,554,432-byte ROM exactly equal** to the original SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. All original **7,376 positive-size ELF FUNC identities** match the untouched upstream ELF. **876/876 semantic relocations** for original file 27 match. `scratch25_27_proof.json` records this outcome. The original resource25 file remained entirely unmodified in this passing scratch.

**Semantic host test:** `test_adjacent27.c` was compiled with GCC and `-fsanitize=address,undefined` (no sanitizer class disabled), linking all seven actual candidate sources and mock helper aliases. Test PASS for no-op wrappers, callback registration, the shared `0x12800761`/`0x10000661` wrapper arguments, active timer transition and zero-underflow case, and both completion callbacks. Synthetic host testing does not imply gameplay execution.

## File 25 — one separate isolated lead

`file25_last_v3.c`, original `func_08001228_6AE5E8` at decompressed ROM `0x6AE5E8`, VMA `0x08001228`, **72 original bytes**: isolated IDO compiler and original-address linker comparison **exact**. It requires an artificial symbol `D_0A00C980` to achieve the original `LUI/ADDIU` instruction form, whereas the original ELF has **no** corresponding symbol relocations at these two addresses. Full upstream scratch linking fails with undefined `D_0A00C980`, and injecting this symbol would create extra relocation obligations. **Do not promote** or claim unit/ROM exact for this file25 candidate. It is included solely as a reproducible failed-integration research lead.

`verify_original_file27.py --include-file25` verifies original machine-code bytes for all **22** isolated/unit candidates (1,388 bytes); it **does not** certify that file25 has a relocation-equivalent whole-ROM integration.

## Reproduction

Run from a Linux environment with the original pinned toolchain and **your own** legally held decompressed USA 32 MiB ROM:

```sh
python3 verify_original_file27.py \
  --rom /path/to/usa/baserom.decompressed.z64 \
  --source-dir /path/to/these/sources \
  --ido /path/to/upstream/tools/ido-5.3/cc \
  --report new_native_report.json
```

Requires MIPS tools `mips-linux-gnu-ld` and `mips-linux-gnu-objcopy` on `PATH`, with `LD_LIBRARY_PATH` set per `GOEMON_BUILD_ENVIRONMENT.md`. Add `--include-file25` to verify its isolated code bytes (not the original ELF relocations). All generated objects go into a temporary folder. The original ROM is never modified. A sample output, `native_group_verification.json`, is included.

The script `stage_scratch_file27.py` records the **executed scratch staging procedure** with the explicit original-run `/tmp` workspace paths. It depends on the previously supplied Goemon upstream scratch helpers and is not an untested generic production manifest adapter. Do not run it in the canonical branch; it operates on a throwaway upstream workspace and modifies only its generated linker/assembly inputs.

## Current production gate

During this research, a separate verified commit independently advanced the connected `chatgptweb/decomp` branch to **864 accepted USA C / 37,904 original instruction bytes** and **39 Japanese C / 2,092 original instruction bytes**. The 21 file27 functions and isolated file25 lead are **not** included in those counts. The research scratch does **not** include the 864-C production C stages. Canonical combined `decomp.verify`, strict `decomp.inventory`, current ELF/relocation ownership and full `decomp.local_ci` for **864+21** are **NOT RUN**. Only after those pass could 21 original file27 functions be promoted. The 72-byte file25 lead remains blocked separately.

Do not commit ROMs, extracted assembly, object files, scratch ELF, save states or copyrighted game assets. This bundle contains only original C research source, host tests, verifier scripts and sanitized metadata.
