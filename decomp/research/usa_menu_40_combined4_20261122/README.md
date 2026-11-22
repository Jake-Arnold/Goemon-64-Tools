> **Later canonical result:** All four functions here are included in the six-function USA canonical promotion, which passed native G2, strict inventory, complete ELF identity and relocation comparison, and full local CI. `func_800108BC_114BC` was already in the crossregion48 research set. See [the six-function promotion proof](../../results/usa_92f0_six_g2_promotion_20261122.json).

# USA IDO 5.3: menu graphics donor and four-function original-ROM proof

**22 November 2026. RESEARCH_ONLY; no canonical accepted-C promotion.**

The already-discovered but unpromoted cross-region donor `func_800108BC_114BC` (ROM `0x114BC`, VMA `0x800108BC`, 40 original instruction bytes) has now been integrated into the actual pinned original USA source layout. It was previously isolated-native-exact in `decomp/research/usa_crossregion48_followup_20261122`; this is **new whole-ROM, all-ELF and all-relocation integration proof**, not a claim of a newly discovered or accepted function.

It was also compiled together with three *other distinct unpromoted* USA C functions previously proven separately in research PR #165:

| Original function | USA ROM address | Guest VMA | Original bytes | Research provenance |
|---|---:|---:|---:|---|
| `func_8000A18C_AD8C` | `0xAD8C` | `0x8000A18C` | 48 | earlier PR #165 |
| `func_8000AAE8_B6E8` | `0xB6E8` | `0x8000AAE8` | 40 | earlier PR #165 |
| `func_8000AB30_B730` | `0xB730` | `0x8000AB30` | 68 | earlier PR #165 |
| `func_800108BC_114BC` | `0x114BC` | `0x800108BC` | 40 | cross-region followup 48 |
| **Combined** | | | **196** | all research-only |

## Measured native integration

- Original pinned `klorfmorf/mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; original SGI IDO 5.3 `-G 0 -non_shared -O2 -mips2` with the unchanged production flags.
- Original USA 16 MiB retail SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66`.
- **Original USA 32 MiB expanded ROM: 33,554,432 / 33,554,432 bytes exact**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- **All 7,376 / 7,376 original positive-size ELF FUNC identity tuples exact**; includes the previously resolved 752-byte neighbouring `func_8000AFA8_BBA8`.
- **All 82,216 / 82,216 original-upstream ELF relocation tuples exact** by section/offset/type/symbol.
- Both GCC14 and Clang17 AddressSanitizer/UndefinedBehaviorSanitizer host tests on four actual C implementations: **4,096 deterministic iterations each, PASS**. Three fail-closed padding tests PASS.

The original unit `0x10D80..0x12760` contains cross-assembly jump-table targets in `main_continued.rodata.s`. Naively replacing the entire unit with mixed C and 41 `GLOBAL_ASM` pragmas **fails linking** because rodata references labels such as `.L800109C4_115C4` and `.L80011254_11E54` that the pragma processing does not export. The exact successful source window is the six-function original range **`0x112F0..0x11580`** (two 16-byte-aligned boundaries): five original ASM neighbours and one compiled C. Remaining menu graphics functions are retained as their original ASM code, and their jump-table labels remain linked.

For the older three functions the already-proven `0xBEA0` original segment boundary and strict two-NOP post-endlabel padding treatment is unchanged. No game instructions are edited. This research verifier reproduces all four in one original-upstream build.

## Compiler line-break quirk: empirically isolated

An exact original 10-instruction rendering wrapper can become native-inexact by adding a **single source newline** between its first and second `p->w0` and `p->w1` assignments, even though C behaviour is unchanged:

- **Same source line, raw two-word C struct:** IDO emits symbol HI16 at offset `+0` and LO16 at `+4`; ten original instructions and the full ROM match.
- **Identical tokens with newline after the first store:** LO16 moves to `+8`, the constant `0x06000000` LUI moves ahead of the LO16 instruction. Full-ROM matching fails.
- **Same-line SDK `Gfx` union control:** emits the *same* original sequence as the raw struct. The problem is **source-line grouping**, not the SDK union type itself.
- **Flat `u32*` pointer control:** may reorder later stores; avoid substituting pointer casts without native re-verification.

This effect was replicated on the original compiler with unmodified flags and explicitly verified by `tests/test_ido_shapes.py`. The exact source file is pinned by SHA-256 in `verify_original_combo.py`; a formatter-induced change fails closed. The reproducible compiler-specific findings belong in `decomp/COMPILER_QUIRKS.md` in the same research commit, not in canonical C ownership.

## Reproduce (private inputs kept local)

Prepare a **clean, pinned, already decompressed, Splat-extracted and byte-identical original-USA upstream checkout** using the user-supplied `GOEMON_BUILD_ENVIRONMENT.md`. All tools, code and test inputs remain local; no original ROM, generated ASM, ELF, proprietary toolchain or other game assets are included in this kit.

```bash
python3 verify_original_combo.py \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions \
  --out /private/new-unused-output --jobs 16

python3 -m unittest discover -s tests -p 'test_padding.py' -v
bash tests/run_host.sh /private/new-unused-host-output
python3 tests/test_ido_shapes.py \
  --checkout /private/pinned/mnsg \
  --deps /private/goemon-dependencies \
  --runtime /private/goemon-runtime-additions
```

The verifier refuses existing output directories, a wrong source commit or ROM hash, dirty tracked original upstream, mismatched function original SHA-256, unexpected ASM window functions or unexpectedly changed compiler-sensitive C text. It builds only in a scratch copy, checks all 33,554,432 ROM bytes, 7,376 full ELF FUNC identities and 82,216 original-upstream relocations, and writes only sanitized metadata outside the private scratch build. The original `GLOBAL_ASM` owners remain intact in the repository.

**Not run / NOT PROMOTED:** the complete modern `chatgptweb/decomp` 1,965-accepted-USA-C staging checkout is still unavailable to the native Linux build host (`git ls-remote` cannot resolve github.com). The canonical `decomp.verify` with 82,103 semantic relocations, strict `decomp.inventory`, and full `decomp.local_ci` **remain NOT_RUN** for these four together. This original-upstream proof cannot be promoted as canonical `PASSED_G2`. Official USA count is still **1,965 C / 84,648 original instruction bytes**, unchanged; Japan is separate. No game-process/emulator runtime testing was performed.
