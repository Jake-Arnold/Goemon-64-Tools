# Japan-0 instant scene reload and original debug-menu fallback

**Date:** 2026-11-15  
**Live evidence:** The user confirmed that the Japan-0 Project64 toolkit can open the original debug menu (`0x800CD284 = 0x0A`) and teleport Goemon to known Oedo South XYZ. On a subsequent test, **double-click only opened the debug menu**, which is **not** the requested USA-equivalent instant warp. That incorrect dispatch has now been replaced in source. **The new direct `0x0C` area reload still awaits live confirmation.**

## v0.11.26 — verified original-USA atlas bundled and used by both versions

The complete user-extracted atlas is committed as `practice/data/entrance-coordinates.json`: **333 indexed scenes, 888 entrance records, 266 covered destinations**. This is the exact table accessed by `selected_scene_spawn(destination)` in both the USA and native Japanese Scene Browser; a separate ROM, Japanese-specific capture, or one-time extraction on each install is no longer required.

Entries preserve all source-specific exits/defaults, XYZ, heading and mode. For example, Oedo South (`0x161`) has ten distinct entrance records; the source-scene 351 exit and native default each use `XYZ (-289, 0, -167), heading 256, mode 16`. The new data supersedes older Japanese fallback heading-zero speculation.

The bundled JSON passed original-USA extractor identity/checksum and numeric entrance validation, and has been fetched back from GitHub intact. Real Japanese-native post-reload XYZ placement and collision are still subject to the on-device regression and gameplay test; only the data source is now complete for the 266 covered destinations.

## v0.11.24 — permanent numeric scene/entrance coordinates

The Goemon toolkit no longer depends on the original USA ROM being present at launch for already known warp coordinates. Both USA and Japanese scene browsers now load the validated extracted `entrance-coordinates.json` atlas from the user's persistent config directory, not a checkout-specific file. Previous `practice/entrances.json` data is migrated automatically. The numeric table contains scene ID, source scene when present, entrance ID, X/Y/Z, heading and mode; **scene ID by itself can be ambiguous when a room has multiple doors**.

For an entirely fresh installation with no extracted original-USA atlas, the toolkit includes the one actual observed XYZ from prior gameplay tests: **Oedo Town South (`0x161`) at `(-289, 0, -167)`**. It is offered as a permanent known point with an explicitly unverified 0/0x10 heading/mode. No made-up entries are added for rooms whose XYZ has not been observed or extracted. A verified USA entrance record for Oedo or another scene overrides the built-in fallback. Once the full USA ROM is extracted once and the numbers are cached, further warps into any covered scene use them without needing the ROM again.

The Japanese and USA region-specific write backends continue to use the same selected `Spawn` and identical coordinates. Native Japanese post-load Goemon position writes remain guarded and one-shot; this change only improves how stable entrance records are found.

## v0.11.23 correction — Japan now uses the exact selected USA entrance

The earlier v0.11.22 conclusion that `self.entrance_atlas` was never initialized was incomplete. `EntranceMixin.init_entrances()` does load the USA atlas from the toolkit's cached `entrances.json`. The actual defect was that the Japanese controller never selected from that shared atlas; it consulted a different Japan-only warp point registry, while the Japanese Scene Browser hid the USA entrance dropdown.

v0.11.23 exposes the **same destination entrance combobox** in USA and Japan, along with **Load original USA ROM**. Both regions now use `selected_scene_spawn(destination)` to choose the same source-specific or default entrance. The current Japan source scene comes from guest `0x800CD2A2` instead of the USA RAM layout. The selected `Spawn.pending_bytes()` is staged at Japanese pending address `0x800CD490` exactly as USA stages it at `0x800C7CA0`, then Japanese engine state `0x0C` triggers the load. An unknown or ambiguous entrance blocks both paths instead of silently allowing a Japanese scene-ID-only warp.

As in USA, Japanese Goemon gets a guarded, one-shot **post-load XYZ placement**: after the destination scene and character have stabilized, the toolkit compares Japanese live position at `0x80151B10` against the selected USA entrance's exact 3 float32 values. When different, it reopens a ROM/PID/RDRAM-verified writable handle, checks the scene and unchanged previous position, writes the exact selected USA XYZ once, and reads back the result. The region-specific fixed vector is observed for Goemon; for other Japanese characters the toolkit only stages the common native entrance and reports that post-load placement is not yet mapped. No broad retry/write loop.

The separate Japanese warp-point capture is no longer the default and never overrides the USA entrance chosen in the shared dropdown. This follows the user's stated expectation that both regional warps should have identical coordinates. Actual native Japanese gameplay collision, camera, spawn record mode/heading semantics and other-character positions remain unverified until tested in-game. The new v0.11.23 regression tests cover staging/placement/selection but have not been executed by the GitHub connector.

## v0.11.22 correction — Japanese destination coordinates were never initialized

The original controller's `self.entrance_atlas` attribute was never created. Every previous native Japanese Scene Browser warp therefore chose `spawn=None` and staged only the pending 2-byte destination at `0x800CD490`. The 12-byte path existed only in synthetic tests that injected an atlas. This explains why room loading can appear successful while Goemon appears at incorrect or stale XYZ.

v0.11.22 **removes the dead USA-atlas dependency** rather than making guesses about Japanese ROM entrances. A user can visit a room naturally as Goemon, connect to a stable Japanese RAM session, and press **Record CURRENT loaded Japanese room XYZ (not selected scene)** in the shared Scene Browser. It saves that room's observed float32 player XYZ in the user-specific Japanese warp registry. Native pending mode and heading are preserved only if the observed current-room pending record has the same scene ID and close XYZ; otherwise they are labelled experimental `mode=0x10` / `heading=0` defaults. The Oedo South `(-289, 0, -167)` user-observed coordinates remain available as a separately labelled experimental preset.

Later warps to recorded rooms stage the complete native `>HHhhhH` block: scene ID, mode, signed 16-bit rounded X/Y/Z, heading, **before** engine state `0x0C`. Warps with no recorded native Japanese XYZ still stage the scene ID only and are **explicitly unverified for spawn**. The controller never substitutes arbitrary USA entrance coordinates into Japan. Existing freeze locks are stopped so old-room XYZ freezes cannot resume after a scene reload and overwrite the new location.

After three valid destination gameplay reads, the toolkit compares the requested coordinates with **actual post-load XYZ at `0x80151B10..0x80151B1B`**. If the 3D difference exceeds 16 units it reports `SPAWN MISMATCH` plus requested/observed numbers. If no Japanese spawn was staged it reports `NO DESTINATION XYZ WAS STAGED`. Even a close measurement does not prove grounded collision, facing or controllable actor.

The new `japan-warp-spawns.json` contains only user-recorded scene/spawn metadata under the user's configuration directory; it does not include or modify any ROM, game saves or executable. Native Japanese room metadata extraction remains a future research task. **No new claim of verified cross-scene spawning is made until live Goemon64Recompiled behaviour is observed.**

## Correct implementation: identical reload mechanism, region-specific addresses

The existing **Scene Browser** is the only scene picker in both USA and Japan. Double-click is an immediate memory request in the currently selected version. The original **Open debug menu** button remains an independent, optional manual operation.

| Operation | USA retail | Japan-0 retail |
| --- | --- | --- |
| Pending destination (u16) | `0x800C7CA0` | `0x800CD490` |
| Optional native entry mode / signed XYZ / heading (10 further bytes) | `0x800C7CA2..0x800C7CAB` | `0x800CD492..0x800CD49B` |
| Engine state (u8) | `0x800C7A94` | `0x800CD284` |
| Normal gameplay | `0x0D` | `0x0D` |
| **Immediate area reload** | **`0x0C`** | **`0x0C`** |
| Original debug menu — separate button | `0x0A` | `0x0A` |
| Current map (read only) | `0x800C7AB2` | `0x800CD2A2` |
| Exit / title flag — never changed | `0x800C7A9F` | `0x800CD28F` |

USA's `stage_reload_trial` in `practice/experimental_controls.py` is the source for operation ordering. **Japan's new `stage_japan_direct_reload` in `practice/japan_direct_scene_reload.py` performs the corresponding operations:**

1. Require stable ordinary Goemon/Ebisumaru gameplay, exact ROM/PID/guest-memory verification and write opt-in.
2. Read the original pending destination. Choose the intended scene from the **same shared Scene Browser**; retain the current playable character.
3. Stage a **12-byte native entry block** when an unambiguous, cached **USA-reference entrance** is available; the user has confirmed USA Oedo South XYZ work in Japan, **not** full entrance equivalence in every map. Otherwise stage only the 2-byte scene ID and do **not** invent coordinates. An unambiguous source-room entrance takes priority over the reference default.
4. Verify that the pending bytes match the request and the source context has not changed.
5. **Immediately write `0x0C` to `0x800CD284`, within the same double-click callback.** No debug state `0x0A` is requested. No menu cursor writes, no Project64 keyboard input, no manual confirmation in the original N64 menu.
6. Monitor destination map, game state, loading, exit, character and finite XYZ for **three stable polls**. No retries after a mismatch or timeout. Report that stable gameplay has been observed, without claiming proof of collision or player controls.

The original USA entrance atlas is optional for Japan until a native Japanese entrance atlas is extracted and verified. **A scene ID by itself may preserve stale coordinates and produce a poor spawn.** The toolkit states explicitly when only the destination was staged. Full safety equivalence to USA therefore remains **incomplete**; use a disposable Project64 savestate and validate actual footing in-game.

## Windows Project64 procedure — instant Scene Browser request

```powershell
git pull --ff-only origin chatgptweb/japan-controlled-party-writes
.\scripts\test_japan_party.ps1
py -3 -m practice.toolkit --game-version japan --enable-japan-scene-writes
```

The previous `--enable-japan-debug-menu-writes` CLI flag is accepted as a backwards-compatible opt-in for the direct reload, but **`--enable-japan-scene-writes`** is the dedicated option. `--read-only` blocks all Japanese scene writes.

Connect to the exact Japan-0 ROM in Project64, verify or automatically restore the previously checked ROM path, save the emulator state, open **Scene Browser**, then **double-click** a destination (e.g. Oedo Town South `0x161` to Goemon's House `0x1D1`). **The original debug menu should no longer appear on double-click.**

If it does not load, the toolkit's Scene Browser status will report the immediate request or later timeout. An original debug menu appearance would indicate the `0x0C` sequence was overridden or old code is still running. Confirm the current branch was pulled and the toolkit process restarted.

## Manual original debug-menu fallback

The separate **Open original debug menu** control still writes only Japan's engine mode `0x800CD284: 0D→0A` after confirmation. This path was previously **live verified** by the user in Windows Project64. It does not select an area or participate in the new double-click reload. The manual menu uses USA-derived category/index **hints**, not directly written map IDs.

The older unverified Japanese category-stage staging prototype (`practice/japan_native_scene_warp.py`) and keyboard-A adapter are **not used** by the current Scene Browser. They remain as research files, not required for instant warp.

## Verified ROM memory across sessions

On first verification, the toolkit stores the canonical Japan-0 ROM path and its expected SHA-1 under the user's config directory (`%LOCALAPPDATA%\GoemonSpeedrunTools\verified_rom_paths.json` on Windows). Future sessions automatically re-open and **reverify the actual ROM file** using the exact retail-revision verifier. If it is missing or edited, the user must reverify it. **Live Project64 PID, ROM code signatures, RAM mapping, 4/8 MiB size and byte order are still validated on every new connection and writable step.** The saved path does not store a process handle or grant write access.

## Live acceptance: menu entry confirmed, full room warp pending

- **User report (15 November 2026):** The new toolkit control opened the game's original Japanese debug menu in Project64; Goemon XYZ preset also successfully moved him to the desired Oedo South coordinates.
- **Distinct validation boundaries:** Oedo South XYZ teleport is **within the same scene** and is not an inter-scene warp. Debug menu **opening** has been verified, but no gameplay report yet shows selecting a different room through it and receiving a controllable actor in the new scene.
- **Automated scene selection remains unmapped:** The USA-derived category/index hints are still just hints. No direct map writes or speculative menu-cursor writes are enabled.
- **Regression status:** A later Windows run of 107 backend tests passed, but the GUI stage reported 39 errors from a minimal Tk Host lacking new write callbacks and one dashboard savestate Combobox default selection failure. Corrective commits `ec35b9c` (inert test-host callbacks) and `7fc29bd` (explicit slot 0) are pushed; **full post-fix suite rerun pending**.

## Acceptance and next evidence

A valid instant scene-to-scene warp must show the destination `0x0C` reload, stable ordinary gameplay at the selected map, correct character and usable spawn/collision. **Only after the next Project64 test can this be called working for Japan.** The earlier visible original debug menu is evidence for the **manual fallback only**, not evidence of instant warping.

Japanese scene-entrance extraction, same-scene reloads, special overlay scenes, and all playable characters still require separate validation. The original stage/category/A-button path is not used as a fallback from the new direct route.

## Tests added

- `tests.test_japan_direct_scene_reload`: exact state `0x0C`, pending-map byte order in big/wordswapped RAM, 12-byte spawn layout, rollback on staging failure, no current-map/exit writes and no debug menu.
- `tests.test_japan_native_scene_controller`: double-click starts direct reload synchronously, never calls debug menu or N64 A input, and monitors stable destination.
- `tests.test_region_views`: actual shared Scene Browser double-click dispatch calls warp, never the manual menu.
- `tests.test_japanese_debug_warp`: exact engine address, category hints, one-byte state request in big-endian and word-swapped RAM, refusal during loading, unsupported submode or wrong character, read-only handle.
- `tests.test_japan_debug_menu_controller`: declined confirmation, missing opt-in, invalid state, PID mismatch, fresh writable view, matching read-only view and one-mode-only operation.
- `tests.test_japanese_debug_ui`: compact Scene warp tab, selector index hint, write button gating and read-only precedence.
- These run under `scripts/test_japan_party.ps1` and `scripts/test_japan_party.sh`; user execution is **pending**.
