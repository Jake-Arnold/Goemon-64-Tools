# Source-backed USA/Japan Goemon player skeleton hierarchy (read-only)

Status: **linked geometry and encoded channel fields recovered; skeletal pose/RT64 texture replay not yet reconstructed.** This is not an automatic NPC actor-to-model mapping and is not a replacement for RT64.

## New visual identification

The user identified the **slot-0 partial 90-triangle preview** (graphics file `0x120`) as **Goemon's weapon** from direct visual inspection of the toolkit. The UI now labels this exact fragment **“Goemon weapon fragment (visual identification)”**. This is *not* a proof that the entire numbered file `0x120`, the 460-triangle linked rig or every associated animation belongs exclusively to the weapon.

## Exact live-capture to ROM crosswalk

Original USA Project64 breakpoint `func_80018CA0_198A0` (`0x80018CA0`) gave `a0=0x80304BB0` (`Skeleton*`) and `a1=0x8014B0B0` (`Object*`). The captured `Object.graphics_1=0x790047F8` masks to `0x090047F8`, one real F3DEX list in file `0x120`. Four consecutive 24-byte `Skeleton` records match **byte-for-byte** original ROM file `0x123` offset `0x2A530`, candidate 110 of 122 repeated four-list pointer groups. The original Japanese rev-0 matches at the same source offset, with the segment-09 geometry pointers shifted by `-0x60`.

At offset **`0x2A590`** in the decompressed file `0x123` is an original `AnimatedSkeleton` wrapper consistent with [Goemon64Recomp `patches/types.h`](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/types.h):

| Wrapper field | Verified USA and Japan value | Interpretation |
| --- | --- | --- |
| `flags` | `0x80000125` | Original animation flags; remaining semantics unresolved |
| `animation` | `0x07029980` | Segment 07 stream at file `0x123` offset `0x29980` |
| `skeletons[0]` | `0x0702A518` | Segment 07 root skeleton at file `0x123` offset `0x2A518` |

Following the **signed, 24-byte-strided** right/left child links from root `0x2A518` reaches **14 connected nodes**, 13 with segment-09 graphics lists in resource file `0x120`. The independent USA and Japan walks each terminate all 13 lists and resolve **460 triangles**, including the earlier four-list 84-triangle subset. Individual display-list pointers in Japanese are `-0x60` relative to the same USA offsets. The rig structure is more complete than the old sample, but the vertices remain in their local coordinate systems.

## Actual encoded-channel interpretation

Original USA ROM instructions at `0x8001A8E4` (scale decoder), `0x8001AABC` (translation), `0x8001AC28` (rotation), `0x80019ED8` (matrix generation), and `0x8001B2C8` (compressed animation sample lookup) establish that a 16-bit skeleton entry is **either an immediate transform component or an animation-stream reference**.

The helper masks the flag `0x4000`, tests `(word & 0xBFFF) >= 0xA001`, and for an immediate subtracts `0xB000` (modulo 16 bits). The transform routine converts the decoded scale using `/256` and translation using `/32`. Therefore a common skeleton value **`0xB100` means scale 1.0**, not `-20224` or an animation offset. The source rig has **42/42 immediate scale components equal to 1.0**. It also contains **39 unresolved rotation stream channels** and **27 unresolved translation stream channels**. The root has immediate zero rotation and translation entries, but parent/child animation data and matrices cannot be inferred from this alone.

For stream-backed entries, the original sampling function reads a compressed data stream through `D_80168520`; that pointer and the current animation time control the sampled value. These channels are reported as `@0x...`, *never* mistaken for absolute angles or XYZ translations. Rotation/translation scaling and the complete hierarchical transform order need further verification against live RT64/PJ64 output before showing a posed model.

The 122 repeated groups are **candidate skeletal records**, not 122 proven sequential animation frames. They are spaced at irregular intervals in the file, consistent with distinct clip/pose descriptors but insufficient to assign clip identities or playback timing.

## Toolkit

In `toolkit/rt64-model-probes`:

1. **Scene browser → Room actors… → Research geometry…**, select the original correct-region ROM.
2. Select **Slot 0 — Goemon weapon fragment (0x120)** for the visually identified partial mesh.
3. Click **Preview linked 14-node skeleton (460 triangles)** for the independently validated hierarchy's combined **unposed, artificially coloured** geometry.
4. Click **Inspect rig channels…** to see each node's source offsets, list pointer, 13 mesh triangle counts, child links, decoded constant scales, and unresolved stream offsets.

CLI metadata only, no original game assets included:

```bash
python3 -m practice.skeleton_rig --region usa --rom /path/to/USA.z64
python3 -m practice.skeleton_rig --region japan_0 --rom /path/to/Japan.n64
```

Validation with supplied USA and Japan original ROMs, Linux/Xvfb, and synthetic corrupt pointers/cycles: **30/30 relevant focused Python tests passed**. Full repository CI, native decomp matching-C/G2 promotion, actual RT64 replay, texture decoding, posed animations and in-game actor→model identity are **not claimed**. No ROM bytes, original assembly, full model assets, screenshots, or memory snapshots are committed.
