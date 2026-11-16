# USA and Japan character-switch reconstruction — original-code proof

**Date:** 15 November 2026. **Scope:** original unmodified USA Rev. 00 and Japanese Rev. 0 retail ROMs, the exact pinned `mnsg` source checkout `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, and original native IDO 5.3 at `-O2 -mips2`. Research based on the Japanese Project64 trace from the same date. ROMs, generated assembly, original objects and private compiler binaries are not included in this repository.

## New USA address confirmation

| Native role | USA Rev. 00 | Japan Rev. 0 | Original instruction basis |
| --- | --- | --- | --- |
| Current character index (32-bit) | `0x8015C5DC` | `0x80161DCC` | Selector and synchroniser independently write the global |
| Character-cycle candidate availability (four 32-bit words) | `0x8015C69C + 4*index` | `0x80161E8C + 4*index` | Selector loads candidate-indexed word and accepts nonzero |
| Additional switch-related word set to `1` by selector | `0x8015C604` | `0x80161DF4` | Selector `sw 1,0x2C(base)` |
| Character byte in dynamic object | `object+0x60` | `object+0x60` | Selector and synchroniser read/write this byte |
| Indirect state pointer | `object+0x5C` | `object+0x5C` | Synchroniser dereferences this pointer; **not** a fixed guest address |
| State activation/request byte | `[object+0x5C]+0x69` | `[object+0x5C]+0x69` | Synchroniser writes `1`; exact semantic label unproven |
| Mode halfword reset during switch | `[object+0x5C]+0x86` | `[object+0x5C]+0x86` | Synchroniser writes `0` |

The Japanese selected-character global is exactly `0x57F0` above the USA global **for these mapped addresses**, but this is not a universal relocation rule. The normal game character indices are `0` Goemon, `1` Ebisumaru, `2` Sasuke, `3` Yae. Only 0/1 were dynamically observed in the contemporaneous JP Project64/Mupen trace; 2/3 are statically supported by the four-entry selector and established USA convention.

Directly editing the global index does **not** execute the object/model/animation updates. The C-Down selector checks eligibility and invokes the synchroniser. The USA Ebisumaru miniature-mode character-change restriction checks `[object+0x5C]+0x86` in `func_801DD3C4_5992D4` at VMA `0x801DD430`; the successful switch synchroniser resets this halfword. This relationship is ROM-backed. Avoid treating the dynamic `object+0x5C` pointer as a universally stable RAM address.

## Mapped original functions

| Purpose | USA VMA / ROM | Japan VMA / ROM | Bytes | Identical original instruction words |
| --- | --- | --- | ---: | ---: |
| Wrapper | `0x801DD4D8 / 0x5993E8` | `0x801E2888 / 0x59E858` | 40 | 9/10 |
| State-byte reader | `0x801DD500 / 0x599410` | `0x801E28B0 / 0x59E880` | 12 | 3/3 |
| Four-slot cycling selector | `0x801DD50C / 0x59941C` | `0x801E28BC / 0x59E88C` | 180 | 42/45 |
| Character-state synchroniser | `0x801DD5C0 / 0x5994D0` | `0x801E2970 / 0x59E940` | 148 | 34/37 |
| Alternate state reset | `0x801DD654 / 0x599564` | `0x801E2A04 / 0x59E9D4` | 132 | 30/33 |

All remaining instruction differences in these five original function pairs are regional addresses or JAL targets. The selector is still `GLOBAL_ASM`; its C draft is not matching. The alternate reset now has an exact original-address IDO C candidate in both regions; only the four-slot selector remains assembly-owned.

## New native C, tested in both regions

`decomp/research/character_switch_native_candidates.c` provides a single regional C source with four separately compiled units (`SELECT_READER`, `SELECT_WRAPPER`, `SELECT_SYNC`, `SELECT_ALT`, each under `REGION_USA` or `REGION_JAPAN`). It uses the original IDO 5.3 compiler and original-VMA linker scripts to prove the exact original bytes after relocation. The synchroniser's second argument must be `u16`; `u8` or `u32` parameter declarations produce different MIPS register scheduling. `decomp/research/cross_region_native_probe.py` authenticates both 32 MiB ROM SHA-1 values, compiles, links and compares without exporting game-code bytes.

| Region | State reader | Wrapper | Synchroniser | Alternate reset | Isolated total |
| --- | --- | --- | --- | --- | ---: |
| USA | 12/12 exact | 40/40 exact | 148/148 exact | 132/132 exact | **332/332 bytes** |
| Japan | 12/12 exact | 40/40 exact | 148/148 exact | 132/132 exact | **332/332 bytes** |

Run the isolated comparison with:

```bash
python3 -m decomp.research.cross_region_native_probe \
  --usa /PRIVATE/usa.decompressed.z64 \
  --japan /PRIVATE/japan_0.decompressed.z64 \
  --cc /PRIVATE/mnsg/tools/ido-5.3/cc \
  --ld /PRIVATE/mips-linux-gnu-ld \
  --objcopy /PRIVATE/mips-linux-gnu-objcopy \
  --report /PRIVATE/character-switch-native-proof.json
```

**Source and proof are region-specific:** a successful isolated IDO byte comparison does not establish linked overlay relocation integrity or a complete matching full-ROM build.

## Full USA ROM build verified (independent reproduction)

The three research C files `usa_character_switch_entry.c` (40-byte wrapper followed by 12-byte reader), `usa_character_switch_sync.c` (148-byte synchroniser), and `usa_character_switch_alt.c` (132-byte alternate reset) were staged into an isolated copy of the pinned original USA source. The 180-byte selector and all surrounding functions were left in original assembly. The generated `file_11` linker script was switched from `SUBALIGN(16)` to `SUBALIGN(4)` for this overlay alone. The original assembler/IDO objects carried 16-byte section-tail padding; `trim_elf32_mips_text.py` adjusted the ELF32 big-endian `.text` section lengths while preserving *all* `.rel.text` relocations. GNU `objcopy --update-section` was explicitly rejected for this use because it strips the text relocation records in this toolchain.

The exact original-C island comprises `0x5993E8..0x5995E8` including the retained 180-byte ASM selector; the C portions are 332 bytes. The six staged chunks are:

| Object / subsegment | Original .text bytes |
| --- | ---: |
| ASM before `0x5993E8` | `0x12078` |
| C wrapper and reader | `0x34` |
| ASM selector | `0xB4` |
| C synchroniser | `0x94` |
| C alternate reset | `0x84` |
| ASM after `0x5995E8` | `0x1EF18` |

**Independent full-ROM proof:** a new fresh extraction of the supplied upstream archive, fresh original-ROM expansion, fresh Splat and unmodified USA build, followed by the standalone C staging script and a fresh candidate build, all succeeded. Final original and rebuilt images were **33,554,432 bytes** and both SHA-1 **`6ea0ed71032ce08fc2745f412d84936382197494`**. The `file_11` baseline and candidate ELF relocation sections both contain **8,825 entries**; their **multisets** of `(relocation site, type, resolved target, symbol name)` are identical. The fourth C function reorders three otherwise identical relocation records (indices 2506–2508), so the raw ordered relocation lists are **not** identical. The entire original-ROM image remains byte-exact. The `file_11` text and data boundaries remained unchanged. No raw game memory or gameplay writes were performed.

### Full-ROM reproduction phases

Use a **separate temporary checkout** of pinned upstream `mnsg`, with the USA retail ROM expanded into `config/usa/baserom.decompressed.z64` and the same environment/toolchain pins as `GOEMON_BUILD_ENVIRONMENT.md`:

```bash
# With the repository's Python package root on PYTHONPATH:
python3 -m decomp.research.usa_character_switch_rebuild \
  --checkout /PRIVATE/clean-mnsg --phase prepare

# From the upstream scratch checkout, with the original Splat/IDO/binutils:
# <pinned python> <pinned splat> split config/usa/splat.yaml
# make -j4 VERSION=usa build/usa/mnsg.z64

python3 -m decomp.research.usa_character_switch_rebuild \
  --checkout /PRIVATE/clean-mnsg --phase trim

# From the upstream scratch checkout again:
# make -j4 VERSION=usa build/usa/mnsg.z64

python3 -m decomp.research.usa_character_switch_rebuild \
  --checkout /PRIVATE/clean-mnsg --phase verify
```

`--phase trim` changes six **scratch build objects** and a generated linker script; it does **not** patch the ROM or write to a running game. The first candidate build will normally differ before padding is removed. Preserve all relocation records. `--phase verify` rejects any different full-ROM byte or checksum. This tested standalone integration method is not yet wired into the central production `decomp.verify` manifest; until formal integration plus a fresh verifier/inventory gate, **do not increment the repository's published verified-function count**.

## Verification matrix and outstanding work

- Six original JP Project64-overlap unit tests and eight new unit tests for byte comparison/ELF relocation preservation passed (14 in total). They are ROM-free tests.
- Eight original-address IDO candidates checked against two real ROMs: all exact (332 original instruction bytes per region).
- A complete original USA ROM baseline and two C-replacement stages (three-function and four-function) matched. The three-function reproduction was also repeated from a fresh upstream extraction; the four-function image was rebuilt from that clean checkout. All checked USA images had the exact 32 MiB original SHA-1.
- USA `file_11` semantic relocation records: 8,825/8,825 identical as a multiset, with three original records in a different order in the four-function candidate.
- **Not yet done:** Register the `file_11` mixed C/ASM object adapter and matching manifest entries in the production decomp pipeline; rerun the central `decomp.verify` and inventory. This work may require harmonising the existing overlay adapters without changing previous matched sources.
- **Japanese full-ROM build:** still blocked by upstream source files with hardcoded USA `GLOBAL_ASM` paths. Isolated Japanese C function equality is proven, but there is no Japan-0 full-ROM rebuild/overlay acceptance gate yet.
- **Next C target:** 180-byte four-character selector (`func_801DD50C_59941C` / `func_801E28BC_59E88C`). The selector is still 180-byte ASM; the alternate reset now matches and is a full-ROM-proven USA C candidate.