# Japan-0 native scene warp via original debug level selector

**Date:** 2026-11-15  
**Implementation status (user verified 2026-11-15):** The Japanese native debug-menu button **successfully opened the original menu in live Windows Project64**, according to the user's direct gameplay report. This verifies the menu-entry stage in the tested setup. **Manual selection of a different destination and a completed controllable scene load have not yet been reported**; this is not a verified end-to-end or one-click warp.  
**Scope:** The shared Scene Browser now requests full native scene-to-scene warps for Japan-0: enter the game-owned debug menu, stage Japan category/stage fields, send a configurable Project64 N64 A key, and watch for the destination's ordinary gameplay state. **The complete automatic sequence is implemented and synthetic-tested in code, but has not been live-confirmed as a successful cross-scene warp.** Manual original-menu entry remains a separate fallback.

## Provenance and exact boundaries

The original US game's L-button debug patch and the [mn64rando project](https://github.com/abyssonym/mn64rando) show the game can navigate its own debug level selector to load rooms. The USA native debug engine state is `0x800C7A94 = 0x0A`. The externally sourced Japanese Japan-0 debug engine-mode field in the toolkit is **`0x800CD284`**, also using value **`0x0A`** for debug menu, with normal gameplay hypothesised/expected at **`0x0D`**.

The USA controller L button input conditional is at `0x800C7D3B`, mask `0x20`. **Do not take its apparent Japan offset** (`0x800CD52B`) as a verified Japanese L-button code. This new runtime feature **does not patch the ROM or force a physical L press**; it makes a one-time state request consistent with the native debug menu.

Previously tried direct writes to USA pending map + exit request returned to the title screen. The Japanese addresses for current map (`0x800CD2A2`), pending map (`0x800CD490`), exit request (`0x800CD28F`) and loading (`0x80161DC4`) are **never written** here. USA scene IDs and category hints come from an existing reference catalogue and may require Japan-specific verification.

## Automatic warp: shared Scene Browser

This is **not** a second scene list. Exactly the same Scene Browser and double-click action are used for USA and Japan, with the active ROM choosing its own backend:

- **USA:** existing selected ROM entrance reload/placement workflow; the Japanese debug staging does not run.
- **Japan-0:** use the original debug-menu pipeline. A destination such as `0x01D1` (Goemon's House) is translated through the same scene category/index reference used by USA: `SHOP` / menu category `4` / stage index `65`. Japan offsets are `0x800CD294` (category byte) and `0x800CD2A4` (stage-index halfword), with normal game state `0x800CD284=0x0D` and original debug state `=0x0A`. These Japanese stage/category *write behaviours* remain inferred from the regional layout; the user requested implementation assuming parity.
- Once in the original menu, the toolkit writes only those two selector fields, checks that they remain unchanged, then sends the **configured** Project64 keyboard key mapped to N64 A (default `X`). A single A keydown is released after 150 ms. It does **not** write active scene, pending scene, exit flags or player XYZ.
- The toolkit requires multiple consecutive observations of ordinary engine mode, the requested scene ID, no loading/exit, and plausible character/XYZ before reporting a completed load. **This is stronger than observing the scene ID change, but is not a guarantee that the player is controllable.**
- Errors, changed PID/RAM mapping, overwritten menu selection and timeouts stop automatic actions without retries.

**Windows launch**:

```powershell
git pull --ff-only origin chatgptweb/japan-controlled-party-writes
.\scripts\test_japan_party.ps1
py -3 -m practice.toolkit --game-version japan --enable-japan-debug-menu-writes
```

Choose `project64`, connect the verified Japan ROM, create a native savestate, open **Scene Browser**, single-click a room to inspect its region-specific stage index, then **double-click that room to request the full warp**. Configure the N64 A keyboard binding in **Japan Live → Scene warp (debug)** only if Project64 does not map A to `X`.

The JavaScript-free Python implementation is `practice/japan_native_scene_warp.py`, `practice/japan_project64_input.py`, and the `Toolkit.start_japan_native_scene_warp` / `poll_japan_native_scene_warp` controller. The original-menu-only button is retained as a manual fallback; **double-click does not invoke that fallback**.

## Verified ROM memory across sessions

On first verification, the toolkit stores the canonical Japan-0 ROM path and its expected SHA-1 under the user's config directory (`%LOCALAPPDATA%\GoemonSpeedrunTools\verified_rom_paths.json` on Windows). Future sessions automatically re-open and **reverify the actual ROM file** using the exact retail-revision verifier. If it is missing or edited, the user must reverify it. **Live Project64 PID, ROM code signatures, RAM mapping, 4/8 MiB size and byte order are still validated on every new connection and writable step.** The saved path does not store a process handle or grant write access.

## Windows Project64 procedure

1. Run `git pull --ff-only origin chatgptweb/japan-controlled-party-writes` and `.\scripts\test_japan_party.ps1`. The tests cover synthetic bytes/controller/Tk, not an actual emulator.
2. Start Project64 with a matching Japanese revision-0 ROM. Create a **complete Project64 savestate** from an ordinary playable room as Goemon or Ebisumaru. Confirm its restore command works before using the debug path.
3. Start the experimental toolkit:

   ```powershell
   py -3 -m practice.toolkit --game-version japan --enable-japan-debug-menu-writes
   ```

   The other independent flag `--enable-japan-position-writes` is not necessary. `--read-only` overrides both.
4. Verify the exact Japan-0 ROM in the toolkit, select `project64`, attach to the running PID, and open **Japan Live / Party Test → Scene warp (debug)**.
5. Choose a **Destination hint** from the list. For **Oedo Town South** (scene `0x0161` / decimal 353), the USA-derived native selector hint is **MACHI / index 3**. For **Goemon's House** (scene `0x01D1`), it is **SHOP / index 65**. These are **menu hints**, not map writes or guaranteed Japanese category indices.
6. Click **Open native Japanese debug menu (confirm)**. The toolkit displays source scene, destination hint, the only intended write, and the savestate warning. Cancel means no write.
7. On consent, the toolkit rechecks the Project64 PID, verified ROM code signatures and original RAM base/byte-order/4-vs-8-MiB mapping, then compares writable and read-only RAM views. It refuses debug entry if the game has left ordinary mode `0x0D`, the character is not Goemon/Ebisumaru, a load/exit is active or the gameplay submode is unsupported.
8. **Only** `0x800CD284: 0D → 0A` is requested, once; the result is read back. **Live Windows Project64 now confirms the on-screen original debug menu opens** for the user. This gameplay observation is stronger evidence than engine-byte read-back alone. The menu's destination selection and actual scene loading remain the next separate validation.
9. **Select the desired room manually using the game's own debug menu controls and confirm it there.** Observe actual playable destination, character actor, current scene, previous/pending scene and loaded position. The toolkit **does not** press A or stage an unverified menu cursor behind the user's back.
10. If the game does not open the menu, crashes, returns to title, spawns outside geometry or enters an unusable scene, restore the original emulator savestate and reconnect. Report the before/after engine state and observed on-screen behaviour. Never patch the current scene directly to recover.

## Live acceptance: menu entry confirmed, full room warp pending

- **User report (15 November 2026):** The new toolkit control opened the game's original Japanese debug menu in Project64; Goemon XYZ preset also successfully moved him to the desired Oedo South coordinates.
- **Distinct validation boundaries:** Oedo South XYZ teleport is **within the same scene** and is not an inter-scene warp. Debug menu **opening** has been verified, but no gameplay report yet shows selecting a different room through it and receiving a controllable actor in the new scene.
- **Automated scene selection remains unmapped:** The USA-derived category/index hints are still just hints. No direct map writes or speculative menu-cursor writes are enabled.
- **Regression status:** A later Windows run of 107 backend tests passed, but the GUI stage reported 39 errors from a minimal Tk Host lacking new write callbacks and one dashboard savestate Combobox default selection failure. Corrective commits `ec35b9c` (inert test-host callbacks) and `7fc29bd` (explicit slot 0) are pushed; **full post-fix suite rerun pending**.

## What constitutes a working native scene warp

A source scene A → debug menu → selected destination B must complete *both* stages: the debug menu must become visible and the game must perform a full destination load with an alive, controllable character in a coherent map B. A change to the engine byte, map value or memory address on its own is **not** success. Validate at least two source→destination pairs before describing the path as working in Japanese Project64.

## Roadmap for one-click scene warps

The final desired workflow is to double-click a scene in Dashboard/Scene Browser and have it open and commit via the original menu/transition pipeline, without manual navigation.

That requires discovering, via actual Japanese debug-menu A/B/C captures or decompiled JP code, the stable guest fields (or callable native game routine) for:

- the active debug **category** (SHOP/MACHI/DOUCHU/SIRO),
- the selected **index / scene ID** and its validated range,
- the native **accept/commit** path and whether it depends on a real controller input,
- the completion criteria: loading phase, scene, valid player/task and coordinates after crossing overlays.

The category and stage fields have now been *implemented as a testable assumption*, with bounds/readback checks and separate game-owned A input. The final native warp is **not yet live-confirmed**. If Project64 does not select and load the intended room, no alternate guessed current-map writes are used; use the captured menu-state evidence to diagnose and correct the layout.

## Tests added

- `tests.test_japanese_debug_warp`: exact engine address, category hints, one-byte state request in big-endian and word-swapped RAM, refusal during loading, unsupported submode or wrong character, read-only handle.
- `tests.test_japan_debug_menu_controller`: declined confirmation, missing opt-in, invalid state, PID mismatch, fresh writable view, matching read-only view and one-mode-only operation.
- `tests.test_japanese_debug_ui`: compact Scene warp tab, selector index hint, write button gating and read-only precedence.
- These run under `scripts/test_japan_party.ps1` and `scripts/test_japan_party.sh`; user execution is **pending**.
