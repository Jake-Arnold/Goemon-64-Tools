# Japan-0 character switching: ROM-offset decompilation target (15 November 2026)

**Scope:** Follow-up to the user-observed Project64 switch trace in `docs/JAPAN_PROJECT64_CHARACTER_SWITCH_MIPS_TRACE.md`. This is static function-discovery research, **not matching C**, a new ROM build, or a claim that the debugger's instance pointers are permanent symbols.

## Concrete code path

The observed native switch executed two stores to Japanese global `u32 0x80161DCC`: the caller `0x801E2944: sw t9,4(v0)` (observed `v0=0x80161DC8`) and the callee `0x801E298C: sw t6,0x1DCC(at)` after an `andi` with `0xFF`. The caller invokes `0x801E2970` from `0x801E2950` and loads a character-related byte from object `+0x60`. The callee writes that object byte, writes the masked global index, dereferences object `+0x5C`, and writes `1` to the pointed-to allocation at `+0x69`. The actual observed allocation was `0x80211650`, target byte `0x802116B9`; the byte changed `00→01`. The remainder of the callee, the caller's function start, and the true meaning of the secondary byte are not proven.

## The overlapping-overlay problem

The pinned upstream `klorfmorf/mnsg` Japan-0 `config/japan_0/splat.yaml` lists multiple overlays mapped to guest `0x801D0B90`. Consequently `0x801E2944` is **not a unique ROM location**.

| Section | ROM `0x801E2944` | ROM `0x801E2970` | ROM `0x801E299C` |
| --- | --- | --- | --- |
| `file_11` | `0x59E914` | `0x59E940` | `0x59E96C` |
| `file_13` | `0x60D3C4` | `0x60D3F0` | `0x60D41C` |
| `file_14` | `0x650E34` | `0x650E60` | `0x650E8C` |

`file_11` is a priority candidate because its BSS starts at `0x80211650`, the *observed* pointer returned by `lw t7,0x5c(a0)`. This precise correlation is not exclusive proof: the same address could contain another overlay's loaded data, and the pointer might be reused. **Only matching the actual code words in the loaded overlay resolves it.**

## New reproducible probe

`python3 -m decomp.japan_character_switch_probe /path/to/japan_0/baserom.decompressed.z64 --splat /path/to/mnsg/config/japan_0/splat.yaml --report /tmp/japan-character-switch.json`

The probe verifies the exact 32 MiB Japanese ROM SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, validates the Splat version, checks the original instruction words at 18 observed PCs in all overlay candidates, and reports matching sections. A unique instruction match is **section identification only**; it does not prove a matching-C reconstruction, boundaries, semantics of every field, or full-ROM equality. The gap `0x801E2958..0x801E296C` is intentionally left unmodelled. It neither changes ROMs nor exports game bytes.

Host-only tests: `python3 -m unittest tests.test_japan_character_switch_probe -v`. In the standalone research environment, six synthetic tests passed 15 November 2026; no original Japanese ROM byte check was possible from this chat's project-storage interface.

## Bounded C reconstruction of the observed writes (research only)

`decomp/research/japan_character_switch_prefix_model.[ch]` encodes the **observed** memory effects of caller `0x801E2944..0x801E2954` and callee `0x801E2970..0x801E299C` against a simulated big-endian guest RDRAM. In order, the caller stores `T9` to `V0+4` (the character global in the capture), stores `T1` to `V0+0x2C` (opaque), reads `u8[S0+0x60]`, and passes `S0`. The callee re-stores that byte to `object+0x60`, writes its zero-extended value to global `0x80161DCC`, follows a guest pointer at `object+0x5C`, and writes byte `1` at `pointer+0x69`.

A relevant consequence is that **the callee's `SW` can overwrite the caller's `T9` value** if the object byte differs. This is a directly supported prefix-level MIPS fact, not a proven normal gameplay case. The model validates guest addresses and referenced allocations before writing, for safety in the host fixture; this is a model guard, not a proven native branch. The real MIPS also sets `F0` to zero and writes registers to the stack; neither effect is modelled because the subsequent use is not traced. Unknown caller gap and callee tail are excluded. No full-function C claim is made, and the research model is not included in any build manifest.

Host smoke and sanitizer command (ROM-free):

```sh
cc -std=c11 -O1 -g -Wall -Wextra -Werror -pedantic -fsanitize=address,undefined \
  decomp/research/japan_character_switch_prefix_model.c \
  decomp/research/test_japan_character_switch_prefix_model.c \
  -o /tmp/goemon-jp-switch-prefix-model
/tmp/goemon-jp-switch-prefix-model
```

The host model and ASan/UBSan test passed in this research session. Tests cover both observed values, a deliberately mismatched T9/object byte, use of a second object/indirect allocation, big-endian stores, and invalid pointer rejection with no memory modification.

## Next matching-C work once the probe identifies the section

1. Resolve the actual original function start and end for the caller and `0x801E2970` using that section's generated Splat assembly and symbol boundaries. Do not derive a function boundary from the short trace alone.
2. Trace the remaining instructions after `0x801E29A0` and the unobserved caller `0x801E2958..0x801E296C`; find the incoming call sites and control-flow paths for character values `0..3`.
3. Establish object `+0x5C` and `+0x60` types from native readers/writers, and determine why the pointed allocation `+0x69` is set. Keep `0x80151B10` Japanese gameplay XYZ independent until proven related.
4. Write a C candidate in the correct regional source/overlay unit, preserve MIPS ABI and delay-slot behaviour, then run original-address IDO codegen, linked-overlay relocation checks and full 32 MiB exact-ROM proof. Do not count code-model tests or a structural signature as a production promotion.

**Non-goals:** No toolkit changes, new cheats, auto-warp, unverified pointer writes, ROM/asset upload, or changes to `main`.

## Original Japan-0 ROM and Splat verification completed (15 November 2026, later session)

**This later verification supersedes the earlier project-storage access blocker above.** All five local project files were directly mounted at `/mnt/data`. The original Japan-0 ROM was independently checksum-verified (normalised 16 MiB SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`) and decompressed with the supplied Python 3.12 runtime and pinned `mnsg-japan` tools. The resulting 33,554,432-byte Japanese image has SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. Splat extraction of the original Japanese image succeeded.

Running the committed `japan_character_switch_probe.py` on that verified 32 MiB image and `config/japan_0/splat.yaml` established a **unique exact 18/18 word match for `file_11`**. `file_13` and `file_14` each matched 0/18 observed words. This resolves original overlay ownership of the observed Project64 instruction sequence, but it does not by itself establish IDO matching-C reconstruction.

| Routine and actual generated Splat symbol | Japanese ROM | VMA | Original bytes |
|---|---|---|---:|
| `func_801E2888_59E858` alternate wrapper/caller | `0x59E858` | `0x801E2888` | 40 |
| `func_801E28B0_59E880` reads `[object+0x5C]+0x69` | `0x59E880` | `0x801E28B0` | 12 |
| `func_801E28BC_59E88C` four-character cyclic selector | `0x59E88C` | `0x801E28BC` | 180 |
| `func_801E2970_59E940` character state/animation reset | `0x59E940` | `0x801E2970` | 148 |
| `func_801E2A04_59E9D4` related alternate state reset | `0x59E9D4` | `0x801E2A04` | 132 |

These are precise function boundaries from the actual generated Japanese Splat assembly, not approximate guesses from the debugger window.

### Recovered selector and state synchronisation logic

- The 180-byte function at `0x801E28BC` starts with object byte `+0x60`, tests up to four cyclic character choices in order, and wraps candidates `>=4` to zero. Its availability test loads a 32-bit word indexed by `candidate*4` at global `0x80161E8C` (derived from `0x80161DF8+0x94`). The availability-table entries' lifecycle remains to be investigated.
- On a selected available character, it sets object byte `+0x60`, global `u32 0x80161DCC`, and global `u32 0x80161DF4=1`, then calls `func_801E2970_59E940`. It returns zero on successful selection, and one if no available candidate was found.
- **Important refinement:** the selector explicitly writes `object+0x60` with its chosen value *before* storing the global character index and invoking the callee. The callee's later global store ordinarily agrees with the selector's write; the previous prefix-only observation that it *could* overwrite a divergent global value is true for the callee invoked with arbitrary states, but does not establish a normal-game inconsistency.
- The 148-byte callee writes `object+0x60`, re-establishes `u32 0x80161DCC`, sets byte `[object+0x5C]+0x69=1`, and **clears halfword `[object+0x5C]+0x86`**. The latter is especially valuable because earlier USA miniature-mode research identified the corresponding field `+0x86` as an Ebisumaru switch/attack restriction gate. Whether all JP semantics map identically still requires verification.
- Additional callee actions include clearing halfword `[object+0x5C]+0x30`, clearing object halfword `+0x80`, zeroing object floats `+0x68/+0x6C/+0x70/+0xE8`, writing halfword `1` to `[object+0x5C]+0x00`, clearing object word `+0x48`, setting object byte `+0xDB=1`, masking low bit of object byte `+0x30`, setting byte `+0xCC=0xBA`, then passing callback `0x801E5B5C` to original engine helper `0x80034E9C`. The callback interpretation is provisional.
- The 132-byte sibling at `0x801E2A04` performs a similar but not identical reset, sets object `+0xCC=0xBB`, and dispatches callback `0x801E5E10`. Unlike the main synchroniser it does **not** clear pointed-to `+0x86` in its own body. The two paths must remain distinct.
- The observed runtime pointed allocation `0x80211650` is also **exactly the start of `file_11` BSS** in the pinned Splat layout. This corroborates overlay identity but does not by itself make the pointer universally stable over every scene.

### Fresh checks and continuing limitation

Six synthetic Python probe tests passed in the current session. The C prefix model passed a strict GCC C11 build with ASan/UBSan. The original 32 MiB Japanese image authenticated successfully and the original-code overlay/instruction match ran on real bytes. **No original-address IDO C-equivalence or exact full-ROM Japanese rebuild has been performed**; the upstream Japanese build remains blocked by source files with USA-specific `GLOBAL_ASM` paths, as explained in `GOEMON_BUILD_ENVIRONMENT.md`. These functions remain assembly-owned and excluded from matching-C totals.

Next bounded step: reconstruct `func_801E2970_59E940` and `func_801E28BC_59E88C` as separate full-function C candidates, compare complete native IDO object code at the original JP addresses, and develop/fix the Japan-0 exact-build gate rather than using the USA baseline.
