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

## Captured Project64 four-list skeleton geometry (17 November 2026)

An original-USA Project64 execution breakpoint at `0x80018CA0` supplied `a0=0x80304BB0` (`Skeleton*`) and `a1=0x8014B0B0` (`Object*`). The supplied 104-byte Object header has `graphics_1=0x790047F8`, `graphics_2=0`, and all six `OverlayInfo` file IDs and local addresses zero. The decoder's pointer mask `graphics_1 & 0x8FFFFFFE` produces `0x090047F8`, matching the first captured skeleton display list. **The earlier all-zero object-overlay output is not an error.** It does not identify an actor ID or a texture source.

The first four 0x18-byte-spaced original-USA `Skeleton` entries begin at `0x80304BB0`, `0x80304BC8`, `0x80304BE0` and `0x80304BF8`, with these graphics pointers:

| Limb list | USA segment-09 root | Japan rev-0 root | USA/JP triangles |
| --- | --- | --- | ---: |
| 0 | `0x090047F8` | `0x09004798` | 20 |
| 1 | `0x09004BB0` | `0x09004B50` | 20 |
| 2 | `0x09004930` | `0x090048D0` | 22 |
| 3 | `0x09004CD0` | `0x09004C70` | 22 |

Each root decodes as an independent F3DEX display list in **original file ID `0x120`**, which matches the source-confirmed first player graphics slot. Both ROMs' original retail hashes and file_11 ID tables were independently verified. All four roots have expected RDP texture-source commands, terminate with `G_ENDDL`, and decode all triangle indices. In original USA the first texture references are `0x0900B950` for the first two lists and `0x0900C950` for the next two; Japan has `0x0900B8F0` and `0x0900C8F0`. These addresses extend beyond the single decompressed file-0x120 length (`0xB950` USA, `0xB8F0` Japan). They are **segmented graphics addresses**, and a contiguous runtime memory/resource loading trace is still required before assigning actual texture ownership.

The app now has **Room actors → Research geometry… → Preview traced 4-part skeleton**. Select the original regional ROM, then click that button; no hex snapshot needs pasting. It combines the four lists into a **colour-coded, unposed research view with orbit/zoom**, totalling 84 triangles. The four distinct colours are artificial and the displayed parts overlap because skeletal matrices have not been applied. This is **not** a full Goemon model and **not** an automatically mapped NPC. The existing **PJ64 object trace…** panel recognizes this one captured `graphics_1` value and explains the next action without implying that nonzero overlay slots are required.

CLI (metadata only, no model asset exports):

```bash
python3 -m practice.model_research --region usa --rom '/path/to/USA.z64' --traced-player
python3 -m practice.model_research --region japan_0 --rom '/path/to/JP.n64' --traced-player
```

The new and existing focused tests were run under Linux/Xvfb with both supplied original ROMs: **24/24 PASS**. Full repository CI, actual RT64 GPU replay, animated skeleton transforms, correct RDP textures and visual in-game 3D match have not been verified. No raw ROM data, extracted model binary, memory snapshots or game screenshots are committed.

## Exact ROM source for the paused Project64 skeleton

The 96-byte memory range `0x80304BB0–0x80304C0F` in the screenshot is **byte-for-byte present in original USA resource `0x123` at file-relative offset `0x2A530`**, not just a similar pointer. That 96-byte sequence occurs once in USA file `0x123`. The original Japanese rev-0 `0x123` has the same sequence at `0x2A530`, after the four segment-`0x09` display-list roots have been adjusted by `-0x60`; all other bytes agree. These authenticated original resource spans have SHA-256 `f57d986d224db7318a9342545677deb6fe675914c52f3d15f9882dd4f427302e` (USA) and `3377c9f389433d70ee907add714afbb61454d8a08971bd37da844582c0218857` (JP).

A bounded scanner finds **122 groups** of four skeleton graphic pointers (24 bytes apart) in resource `0x123` in each region. The screenshot's matching group is at **zero-based index 109**, or the **110th** candidate. This strongly associates `0x123` with the player graphics geometry file `0x120` but **does not establish that all 122 are frames played sequentially**. The packed 16-bit values in the `Skeleton` records are not yet decoded into meaningful skeletal transforms; even the source names `scale`, `rotation`, and `translation` should not be applied to preview vertices without tracing the original decoder.

`extract_traced_player_limb_bundle` now includes metadata-only `skeleton_records` with the candidate count, source offsets, exact-capture match, and capture index. The **Preview traced 4-part skeleton** GUI status displays this cross-reference after authentication. No need to paste the original object bytes again; no captured raw game bytes are stored or committed.

The source-capture match is independently checked in both supplied regional original ROMs by the focused tests (**25/25 PASS** under Linux/Xvfb). No full-texture RT64 rendering or original animation-matrix decode is claimed.

## Full source-linked skeleton rig and observed slot-0 weapon fragment

The slot-0 90-triangle fragment (file `0x120`) was visually identified by the user as **Goemon's weapon**. This is visual feedback on that specific preview, not proof that the entire file `0x120` or all 14 linked bones form the weapon or a static NPC model.

In the same authenticated USA/Japan rev-0 file `0x123`, an `AnimatedSkeleton` wrapper at `0x2A590` contains flags `0x80000125`, stream pointer `0x07029980`, and hierarchy root `0x0702A518`. Following signed 0x18-byte Skeleton child offsets finds **14 nodes / 13 F3DEX meshes / 460 triangles**. The 13 original-USA segment-09 display lists are all readable from file `0x120`; Japan rev-0 equivalents resolve identically with graphics offsets changed by `-0x60`.

Disassembly of original MIPS animation helpers establishes immediate `0xB100` as unity scale: subtract `0xB000` to 256, then multiply by 1/256. All 42 scale components are 1.0. **39 rotation and 27 translation components** instead index compressed animation data. They must not be interpreted directly as degrees, coordinates, or 122 sequential animation frames.

The toolkit now provides **Preview linked 14-node skeleton (460 triangles)** and **Inspect rig channels…** alongside the original player slot and four-part research previews. The meshes remain unposed, artificially coloured and untextured. A live emulator/RT64 transform correlation is required for accurate animation and full character identification.

Full methodology, memory/ROM source offsets, usage and limits: [SKELETON_RIG.md](SKELETON_RIG.md). Local verification: 30/30 focused tests PASS across supplied authentic USA/Japan ROMs and Linux/Xvfb UI.
