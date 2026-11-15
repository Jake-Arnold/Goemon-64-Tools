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