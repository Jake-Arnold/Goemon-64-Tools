# RT64-backed actor model identification and ROM geometry research

**Status: research tooling, not an identified actor model viewer.** The selected actor's type and stage are passed into the research window for context only. No actor-to-graphics resource mapping is verified yet.

## Confirmed Goemon64Recomp / RT64 rendering path

Sources inspected on 17 November 2026:
- [Goemon64Recomp (dev) / src/main/rt64_render_context.cpp](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/src/main/rt64_render_context.cpp): `RT64Context::send_dl(const OSTask*)` resets RSP state, calls `loadUCodeGBI(task->t.ucode, task->t.ucode_data, true)` with addresses masked into RDRAM, then `processDisplayLists(RDRAM, task->t.data_ptr & 0x3FFFFFF, 0, true)`. `update_screen()` calls `updateScreen()`.
- [Goemon64Recomp (dev) / patches/anime.c](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/anime.c): original USA `func_80018908_19508(Skeleton*)` and `func_80018CA0_198A0(Skeleton*, Object*)` traverse animated skeleton limbs and feed display lists to `func_800196F0_1A2F0(Gfx*)`. Their patched matrix tagging uses a generated ID based on a root-object pointer and `skeleton->display_list_vram_addr`. The generated matrix tag is **not an actor ID**.
- [Goemon64Recomp (dev) / patches/functions.h](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/functions.h): original USA signatures for the above functions, plus `func_800141C4_14DC4(u32 file_id)` (loaded file access).
- [Goemon64Recomp (dev) / patches/background.c](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/background.c): an explicit segment-8 resource-load example using `gSPSegment` and `func_800141C4_14DC4`. A background-file reference does not prove NPC use of that same file.
- [Goemon64Recomp (dev) / src/game/recomp_actor_api.cpp](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/src/game/recomp_actor_api.cpp): extended actor data slot-map and monotonically incrementing spawn index; this is **mod-added actor extension state**, not proof of the original game's actor registry or graphics-resource index.
- [RT64 fork (goemon-patches) / src/gbi/rt64_gbi_f3dex.cpp](https://github.com/klorfmorf/rt64/blob/goemon-patches/src/gbi/rt64_gbi_f3dex.cpp): exact field decoding for F3DEX `G_VTX` / `G_TRI1` / `G_TRI2`, matching the offline probe.
- [RT64 fork (goemon-patches) / src/gui/rt64_debugger_inspector.cpp](https://github.com/klorfmorf/rt64/blob/goemon-patches/src/gui/rt64_debugger_inspector.cpp): Pause/Resume, View Draw Call, View Transform Groups, View Native Samplers, Free Camera controls.
- [RT64 fork / src/hle/rt64_application.cpp](https://github.com/klorfmorf/rt64/blob/goemon-patches/src/hle/rt64_application.cpp): **F1** toggles the RT64 inspector, but only when its `developerMode` is enabled. An unverified command-line flag must not be advertised as a solution. F4 is the pause control *within the inspector* and may also have a separate global RT64 developer shortcut.

Goemon64Recomp's submodule is the **klorfmorf/rt64 fork, goemon-patches**; do not assume APIs from rt64/rt64 main match that pinned fork. The reviewed native recomp currently validates USA gameplay, not an independently verified Japanese recomp runtime.

## Toolkit: select actor, then inspect an explicitly chosen ROM resource

1. Open **Scene browser** → **Room actors…**, choose `usa` or `japan_0`, and select an actor row.
2. Click **Research geometry…** or double-click the row. The new window displays the stage/actor context, but warns **NO VERIFIED ACTOR → MODEL MAPPING**.
3. Select your own **region-correct** ROM using **Select local ROM…**. Enter a numbered ROM **resource file ID** and an explicit 8-byte-aligned **start/end** display-list command range. Click **Decode research mesh**.
4. The resulting **untextured vertex-colour geometry** can be orbited with left mouse drag and zoomed with the mouse wheel. No guest RAM is read or written. ROM path and extracted mesh are not persisted.

Two bounded, **unidentified research examples** for either verified regional ROM:

| File ID | Start | End | USA/Japan triangle count | Interpretation |
| --- | --- | --- | ---: | --- |
| 141 | `0xD20` | `0x1220` | 108 | Partial resource geometry, **not attributed to any actor** |
| 263 | `0x3B00` | `0x4358` | 159 | Research span starts mid-list; some triangle indices unresolved |

The original USA ROM SHA-1 is `df8083a54296b8c151917c5333e1c85f014a2a66`. The normalized Japanese rev-0 SHA-1 is `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`; the original byte-swapped .n64 is accepted by the reader. No ROM, textures, or model geometry are checked in.

For a CLI-only metadata report:

```bash
python3 -m practice.model_research --region usa \
  --rom '/path/to/Mystical Ninja Starring Goemon (USA).z64' \
  --file-id 141 --start 0xd20 --end 0x1220

python3 -m practice.model_research --region japan_0 \
  --rom '/path/to/Ganbare Goemon (Japan).n64' \
  --file-id 263 --start 0x3b00 --end 0x4358
```

The JSON output is metadata only: original ROM/resource SHA, command count, opcode counts, resolved triangle count, bounds and missing-feature warnings. It contains no original vertex or texture data.

### Safety and fidelity boundaries

The bounded decoder handles **only** segment-08 `G_VTX`, `G_TRI1`, `G_TRI2`, `G_DL` and `G_ENDDL`; it does not run F3DEX matrices, lighting, texture/TMEM, RDP materials, alpha, animation, occlusion, or culling. The resource spans are research ranges, not automatically discovered complete display-list roots. Invalid alignment/pointers, oversized command windows, cyclic lists, too-deep nesting, oversized meshes, unknown ROM hashes and wrong regions fail closed. Triangle misses and partial spans are labelled. The Tk canvas displays at most 4,000 polygons for responsiveness. **RT64 is the full renderer; the Tk preview is not an RT64 backend.**

## Next live capture: verify one actor

Use an authorized original-USA game instance in Project64 **or** a developer-enabled Goemon64Recomp instance. This step has **not** yet been completed in-game.

**RT64 approach (USA native recomp):** Enable RT64 developer mode in a known-good local build, use F1 to show the inspector; pause inside it, step the **View Draw Call** slider until an identifiable actor appears, then inspect **View Transform Groups** and the free camera. Record observed scene, draw-call index, matrix-group ID, any visible segmented Gfx address, and gameplay screenshot. Keep the screenshot local; don't commit game assets. A single actor can span multiple limb/draw calls.

**PJ64 approach (USA original MIPS):** Set an *execution* breakpoint at `0x80018CA0` (skeleton + object parameters in `a0/a1`), `0x80018908` (skeleton pointer in `a0`), or `0x800196F0` (Gfx pointer in `a0`). Observe the caller (`ra`), resource mapping/segment state and actor identity in a controlled room. Correlate with the RT64 draw calls and identified model. These are **original USA** addresses, not Japan offsets. Inspect existing decomp source around these routines before treating a pointer as an actor identity. Do **not** write guest memory or call animation/spawn functions in the debugger as part of this read-only probe.

When a region-specific actor→resource/display-list mapping is backed by in-game visual and source/trace evidence, add an explicit validated mapping; do not equate a shared graphics resource, a static placement ID, a runtime actor instance or a tagged limb matrix without such evidence.

## Tests

```bash
python3 -m unittest tests.test_model_research -v
xvfb-run -a python3 -m unittest tests.test_model_research_ui -v
```

Six parser tests and one headless Linux/Tk UI test passed in an isolated local source fixture; verified USA and Japan original-ROM probes for files 141 and 263 returned 108 and 159 triangles respectively. Full source repository tests, a built RT64 replay/preview harness, and live actor identity correlation have **not** been run.

## Verified player graphics family and manual PJ64 bridge (17 November 2026)

The next milestone adds original-ROM-verified player graphics table support and segment-`0x09` F3DEX fragment previews in **Research geometry…**. The USA source `g_character_graphics_file_ids[4]` table contains `0x120,0x124,0x128,0x12C`, and the Japanese rev-0 file_11 contains the matching table at a different region-specific offset. These are *player resource slots*, not NPC actor IDs or complete meshes. Four small manually bounded fragment previews (90 / 52 / 12 / 25 faces) have been validated independently in each ROM.

An original-USA **PJ64 object trace…** dialog decodes the 0x68 bytes of the observed `Object*` argument from a paused `func_80018CA0_198A0` call. It exposes source-defined graphics fields and six overlay file references, but never stores or writes memory. No live actor→resource identity has been captured. The complete data, cross-region limits, test commands and offsets are in [PLAYER_GRAPHICS_RESOURCE_TRACE.md](PLAYER_GRAPHICS_RESOURCE_TRACE.md).
