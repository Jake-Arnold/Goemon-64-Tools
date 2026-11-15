# USA and Japan file_11: thirteen exact matching-C candidates, USA exact whole-ROM proof

**Date:** 15 November 2026. **Status:** research branch, not central `decomp.verify` promotion. This expands the independent four-function, 332-byte proof in `USA_JAPAN_CHARACTER_SWITCH_MATCHING_2026-11-15.md` without changing the original production `decomp/manifest.json` or published C-function inventory.

## Nine additional assembly-owned actors converted to matching C

Nine contiguous wrappers immediately after the character-switch/reset group call one of three shared actor handlers. Each is a separate 32-byte function in the original retail binaries, even when its implementation is identical to its siblings. For each function, the original MIPS consists of an 0x18 stack frame, saved RA, `jal` (with incoming `a1` spilled into the call delay slot), and a normal return.

| Handler | USA addresses (ROM / VMA) | Japan addresses (ROM / VMA) | Count |
| --- | --- | --- | ---: |
| Shared handler A | `0x599918 / 0x801DDA08`, `0x599938 / 0x801DDA28`, `0x599958 / 0x801DDA48` | `0x59ED88 / 0x801E2DB8`, `0x59EDA8 / 0x801E2DD8`, `0x59EDC8 / 0x801E2DF8` | 3 |
| Shared handler B | `0x599978 / 0x801DDA68`, `0x599998 / 0x801DDA88` | `0x59EDE8 / 0x801E2E18`, `0x59EE08 / 0x801E2E38` | 2 |
| Shared handler C | `0x5999B8 / 0x801DDAA8`, `0x5999D8 / 0x801DDAC8`, `0x5999F8 / 0x801DDAE8`, `0x599A18 / 0x801DDB08` | `0x59EE28 / 0x801E2E58`, `0x59EE48 / 0x801E2E78`, `0x59EE68 / 0x801E2E98`, `0x59EE88 / 0x801E2EB8` | 4 |

USA handler addresses: A `0x801E1B60`, B `0x801E7CC4`, C `0x801E15D0`. Japanese addresses: A `0x801E6DA8`, B `0x801ECDEC`, C `0x801E67F0`. All are exact original code addresses and were found by Splat and instruction inspection. These wrappers are adjacent to character switching; **this does not by itself prove they are invoked by C-Down or that they modify the character index**.

### Required IDO signatures

A critical signature detail was identified in original codegen: declare the wrapper's second argument as a `u32` but do not pass it as an explicit C argument to the handler. The original IDO 5.3 C compiler emits `jal HANDLER` followed by `sw a1,0x1C(sp)` in the delay slot, exactly matching the retail instructions. Declaring/passing a 16-bit argument emits extra `andi` instructions and a 40-byte wrapper; passing the 32-bit argument explicitly emits a NOP delay slot. Both are incorrect and remain rejected variants.

The single portable `decomp/research/character_switch_actor_wrappers.c` uses region macros for the nine names and three original handler addresses. The standalone USA build source `usa_character_switch_actor_wrappers.c` removes the region macros so it can be compiled by the pinned source's original make rules.

## Exact original-address compiler results

Original verified 32 MiB ROM images:

- USA SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Japan SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`.

The `character_switch_actor_native_probe.py` tool authenticates each original ROM, compiles the nine functions under pinned IDO 5.3 `-O2 -mips2 -G 0 -non_shared`, links them at their original **regional** MIPS VMA, resolves the three call targets to their original regional locations, and compares each 32-byte original ROM extent. Both regions pass **9/9 functions, 72/72 instructions, 288/288 bytes**. Existing four functions separately pass **332/332 bytes per region**. These combined results are **13 original-address native matching-C candidate functions / 620 bytes in each region**. Machine-code comparison does not imply JP full-ROM acceptance.

Reproduction command (using the separately authenticated original ROMs and pinned tools):

```bash
python3 -m decomp.research.character_switch_actor_native_probe \
  --usa /PRIVATE/usa.decompressed.z64 \
  --japan /PRIVATE/japan_0.decompressed.z64 \
  --cc /PRIVATE/mnsg/tools/ido-5.3/cc \
  --ld /PRIVATE/mips-linux-gnu-ld \
  --objcopy /PRIVATE/mips-linux-gnu-objcopy \
  --report /PRIVATE/actor-native-proof.json
```

## Full USA ROM proof: all thirteen functions

The `usa_character_switch_extended_rebuild.py` adapter extends the **already proven four-function mixed C/ASM scratch checkout** described in the earlier report with one additional 288-byte C island. The resulting exact original linker layout of USA `file_11` has eight segments, with assembly intact where no C function matched:

| Segment | ROM start | Exact text bytes |
| --- | --- | ---: |
| Original ASM prefix | `0x587370` | `0x12078` |
| Earlier C wrapper+reader | `0x5993E8` | `0x34` |
| Original 180-byte selector ASM | `0x59941C` | `0xB4` |
| Earlier 148-byte synchroniser C | `0x5994D0` | `0x94` |
| Earlier 132-byte alternate reset C | `0x599564` | `0x84` |
| Original ASM before wrappers | `0x5995E8` | `0x330` |
| **Nine wrapper C functions** | **`0x599918`** | **`0x120`** |
| Remaining original ASM | `0x599A38` | `0x1EAC8` |

The eight extents exactly cover the original `file_11` text interval `[0x587370,0x5B8500)`, without gaps or overlaps. The pinned Splat extraction, original make and link, relocation-preserving ELF section-size trimming, and final make were run against a separate scratch checkout based on the earlier four-function proof. The resulting USA `build/usa/mnsg.z64` is **33,554,432 bytes and byte-for-byte identical to the authenticated original expanded ROM**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.

The `file_11` ELF `.rel.file_11` sections in the four-function and 13-function full-ROM builds have **8,825 entries each**, and this comparison confirms their complete ordered tuples `(site, relocation type, resolved target, symbol)` are identical. The earlier four-function build itself had an identity-equivalent multiset against pristine upstream with three relocation records in a different ordering; this latest check does not reinterpret the prior original-vs-four-function record-order caveat.

### Full-ROM reproduction

With a private USA four-function scratch checkout already prepared and verified using the prior `usa_character_switch_rebuild.py` script:

```bash
python3 -m decomp.research.usa_character_switch_extended_rebuild --checkout /PRIVATE/mnsg --phase prepare
# run pinned Python + Splat split on config/usa/splat.yaml; run first make -j4 VERSION=usa build/usa/mnsg.z64
python3 -m decomp.research.usa_character_switch_extended_rebuild --checkout /PRIVATE/mnsg --phase trim
# run pinned make again; do not reassemble the trimmed original-length .o chunks
python3 -m decomp.research.usa_character_switch_extended_rebuild --checkout /PRIVATE/mnsg --phase verify
```

The adapter refuses non-pinned upstream commit IDs, missing/wrong original ROM hash, missing four-function source layout, duplicate stages and missing object inputs. It only operates in the passed scratch checkout. It does not alter or overwrite private ROM inputs.

## Tests and nonpromotions

- 13 new ROM-free Python unit tests for wrapper region/address registry, original comparison integrity, exact-length enforcement, and fail-closed extended adapter checks passed. The six original JP trace unit tests also passed in the same local discovery run, for 19 tested Python cases.
- Host-GCC C11 `-Wall -Wextra -Werror` and ASan/UBSan dispatch checks passed all nine wrapper functions, including correct actor pointer and handler route. These host tests do **not** replace original IDO or game tests.
- Both regional nine-function original-address IDO probes passed; the earlier eight original-address IDO probes cover the other four functions. The USA exact 32 MiB ROM and the full `file_11` relocation comparison passed.
- The **180-byte USA/JP four-slot character selector remains ASM-owned**. A structurally similar USA C draft compiled to 176 bytes, not 180, with wrong caller-saved versus saved-register treatment and different control flow; it was **rejected**, not counted as decompiled.
- The adjacent USA 64-byte table-driven action selector is also not matching C; one initial 64-byte candidate matched 11/16 instruction words, with incorrect register assignment. It remains assembly-owned.
- The Japanese whole-ROM build is still blocked by upstream source integration using hardcoded USA `GLOBAL_ASM` paths; this is separate from the successful original-address Japan function matches.
- This is **not yet** a central `decomp.verify`/manifest promotion: `decomp/manifest.json` is intentionally unmodified, and the published verified-function count must remain based on the central combined proof, not the research findings. The needed integration is a production-safe `file_11` C/ASM adapter with formal stage definitions, independent full-ROM proof and inventory recalculation.

No game ROMs, original disassembly bytes, generated ELF/object code, game saves, or private toolchain binary files are committed.