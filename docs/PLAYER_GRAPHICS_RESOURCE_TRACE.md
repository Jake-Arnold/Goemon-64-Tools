# USA/Japan player graphics resources — reproducible ROM evidence

**Verified static source data only.** This does not identify an NPC actor or reconstruct a complete player model. The preview draws a small, selected F3DEX limb/resource fragment. Full textures, matrices, normals, animation and actor identity require runtime RT64/PJ64 traces.

## Original character graphics ID table

Goemon64Recomp's original-USA `patches/variables.h` names `D_80204020_5BFF30[4]` as `g_character_graphics_file_ids`. The original-USA `file_11` overlay starts at `0x801CB460`; the table resides at file-relative offset `0x38BC0` (guest VMA `0x80204020`, decompressed ROM offset `0x5BFF30`). The original Japanese rev-0 ROM contains the exact same 16-byte eight-entry run at file_11 offset `0x38380`. Japan is **not** assumed to use the USA original guest address.

The eight big-endian 16-bit values are `0120 0124 0128 012C 0123 0127 012B 012F` in both versions.

| Unassigned slot | Named graphics entry | Immediately following four-value table |
|---|---:|---:|
| 0 | `0x120` | `0x123` |
| 1 | `0x124` | `0x127` |
| 2 | `0x128` | `0x12B` |
| 3 | `0x12C` | `0x12F` |

The original source describes only the **first** four entries as character graphics IDs. The second four are physically adjacent and associated by order but their separate semantics are **not yet verified**. There is no direct actor-ID correspondence in this table. The decoder refuses an unexpected table signature rather than silently applying this mapping to other ROM revisions.

## Region-specific F3DEX fragment probes

The named files (`0x120`, `0x124`, `0x128`, `0x12C`) contain valid F3DEX `G_VTX` and `G_TRI1` command streams whose vertex pointers target **segment `0x09`**. This differs from the previous arbitrary scene/resource probes (`141`, `263`), which use segment `0x08`. The selected spans below begin at a verified vertex load and end immediately after a `G_ENDDL` for **one** partial graphics fragment. The original 16 MiB ROMs were authenticated before the file table was used.

| Slot | File | USA byte span `[start,end)` | Japanese rev-0 byte span | Decoded triangles (each region) |
|---|---|---|---|---:|
| 0 | `0x120` | `0x25A8–0x28C0` | `0x2548–0x2860` | 90 |
| 1 | `0x124` | `0x24A8–0x2670` | `0x2448–0x2610` | 52 |
| 2 | `0x128` | `0x2B38–0x2BB0` | `0x2AD8–0x2B50` | 12 |
| 3 | `0x12C` | `0x2778–0x2860` | `0x26F8–0x27E0` | 25 |

Each decoded segment ends with `G_ENDDL`. No unresolved triangle indices were observed inside these eight windows. All eight resulting geometry bounds match pairwise across regions, despite some different file lengths and fragment offsets. This supports shared geometry data, **not** a complete actor-model match. Vertex RGB bytes may represent normals rather than literal colours; the Tk renderer is a rough untextured projection, not RT64.

## Usage

In the toolkit **Room actors → Research geometry…** window, choose the original ROM matching the selected region, then choose `Slot 0…3` under **Verified player graphics file family** and **Preview player resource fragment**. The app validates the region-specific original ROM hash and file_11 ID table, loads a source-backed segment-09 span and shows orbit/zoom geometry. The selected NPC row provides context only; these player resource presets are not attributed to that NPC.

CLI source-backed example:

```bash
python3 -m practice.model_research --region usa --rom '/path/to/USA.z64' --player-slot 0
python3 -m practice.model_research --region japan_0 --rom '/path/to/JP.n64' --player-slot 2
```

Manual probes also accept `--file-id`, `--start`, `--end`, and `--segment 0x08` or `--segment 0x09`.

## Original-USA Project64 object-graphics trace

A known-original USA MIPS skeleton draw function is `func_80018CA0_198A0(Skeleton *skeleton, Object *object)`. When its execution breakpoint fires, `a0` is the `Skeleton*` argument and **`a1` is the `Object*` argument**. In PJ64's memory viewer, read exactly `0x68` contiguous bytes at the observed guest `a1` address, without modifying the game. Enter only those 104 byte values in **Research geometry → PJ64 object trace…**. No raw bytes or snapshots are stored.

The original-USA `Object` and `OverlayInfo` layout in Goemon64Recomp `patches/types.h` gives:

| Offset within `Object*` | Type | Field |
|---:|---|---|
| `+0x2C` | `u32` | `graphics_1` (encoded graphical data, role unverified) |
| `+0x30` | `u32` | `graphics_2` (pointer, role unverified) |
| `+0x34 + 8*i` | `u16` | `overlay_info[i].file_id` for `i=0..5` |
| `+0x38 + 8*i` | `u32` | `overlay_info[i].vram_addr` |
| `+0x64` | `u8` | first unknown flag after the six overlay entries |

The parser is read-only and reports up to six numeric file IDs plus VRAM pointers. It neither follows the pointers nor proves that a file belongs to a specific static ROM actor placement. **These addresses and struct offsets have not been independently validated for Japan.** A live trace, an in-game screenshot and an RT64 draw-call/transform correlation remain necessary before publishing an actor→model binding.

The adjacent original USA resource functions in the pinned `mnsg` checkout's `src/wave_uty.c` include `func_800141C4_14DC4` (loaded wave number → data address) and `func_80014840_15440` (wave-relative pointer adjustment). Source presence is not equivalent to accepted original-address matching-C promotion: neither is among the current 779 verified C function names. Do not automatically translate these original-USA code addresses to the Japanese runtime.

## Reproducibility and limits

```
GOEMON_TEST_USA_ROM=/path/to/USA.z64 \
GOEMON_TEST_JP_ROM=/path/to/JP.n64 \
xvfb-run -a python3 -m unittest tests.test_model_research tests.test_player_model_resources tests.test_model_object_probe tests.test_model_research_ui -v
```

15 relevant focused tests pass with both original ROMs, including GUI, parser source-layout, invalid resource ID, segment-8 regression, segment-9 extraction, per-region original file_11 tables and all eight fragment counts. Full repository CI, live PJ64 source-offset capture, native RT64 engine build and complete textured model reconstruction **not run**. No game ROM, textures, assets, GLB or memory dumps are included.

Reference implementations: [Goemon64Recomp variables.h](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/variables.h), [Goemon64Recomp types.h](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/types.h), [upstream mnsg wave_uty.c](https://github.com/klorfmorf/mnsg/blob/main/src/wave_uty.c), [RT64 Goemon fork F3DEX decoder](https://github.com/klorfmorf/rt64/blob/goemon-patches/src/gbi/rt64_gbi_f3dex.cpp).
