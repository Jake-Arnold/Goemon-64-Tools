# Japan-0 native scene warp via original debug level selector

**Date:** 2026-11-15  
**Implementation status:** Code and synthetic tests committed to `chatgptweb/japan-controlled-party-writes`. **Not live-tested in Project64 with this new button. The debug menu has not yet been shown opening from this toolkit implementation.**  
**Scope:** Open the game's own debug selection UI in Japanese retail revision 0; manually select a destination. Fully automatic cursor staging/confirm remains **unimplemented** until the relevant Japanese menu fields are mapped.

## Provenance and exact boundaries

The original US game's L-button debug patch and the [mn64rando project](https://github.com/abyssonym/mn64rando) show the game can navigate its own debug level selector to load rooms. The USA native debug engine state is `0x800C7A94 = 0x0A`. The externally sourced Japanese Japan-0 debug engine-mode field in the toolkit is **`0x800CD284`**, also using value **`0x0A`** for debug menu, with normal gameplay hypothesised/expected at **`0x0D`**.

The USA controller L button input conditional is at `0x800C7D3B`, mask `0x20`. **Do not take its apparent Japan offset** (`0x800CD52B`) as a verified Japanese L-button code. This new runtime feature **does not patch the ROM or force a physical L press**; it makes a one-time state request consistent with the native debug menu.

Previously tried direct writes to USA pending map + exit request returned to the title screen. The Japanese addresses for current map (`0x800CD2A2`), pending map (`0x800CD490`), exit request (`0x800CD28F`) and loading (`0x80161DC4`) are **never written** here. USA scene IDs and category hints come from an existing reference catalogue and may require Japan-specific verification.

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
8. **Only** `0x800CD284: 0D → 0A` is requested, once; the result is read back. The game may already have advanced to another state by the time it is observed. Inspect Project64 to see if the original debug menu actually opens; an engine-byte read-back alone does not prove the menu rendered.
9. **Select the desired room manually using the game's own debug menu controls and confirm it there.** Observe actual playable destination, character actor, current scene, previous/pending scene and loaded position. The toolkit **does not** press A or stage an unverified menu cursor behind the user's back.
10. If the game does not open the menu, crashes, returns to title, spawns outside geometry or enters an unusable scene, restore the original emulator savestate and reconnect. Report the before/after engine state and observed on-screen behaviour. Never patch the current scene directly to recover.

## What constitutes a working native scene warp

A source scene A → debug menu → selected destination B must complete *both* stages: the debug menu must become visible and the game must perform a full destination load with an alive, controllable character in a coherent map B. A change to the engine byte, map value or memory address on its own is **not** success. Validate at least two source→destination pairs before describing the path as working in Japanese Project64.

## Roadmap for one-click scene warps

The final desired workflow is to double-click a scene in Dashboard/Scene Browser and have it open and commit via the original menu/transition pipeline, without manual navigation.

That requires discovering, via actual Japanese debug-menu A/B/C captures or decompiled JP code, the stable guest fields (or callable native game routine) for:

- the active debug **category** (SHOP/MACHI/DOUCHU/SIRO),
- the selected **index / scene ID** and its validated range,
- the native **accept/commit** path and whether it depends on a real controller input,
- the completion criteria: loading phase, scene, valid player/task and coordinates after crossing overlays.

Only then is it safe to stage selection and commit automatically. **No guessed writes to these fields are enabled.** The existing manual native debug selector is the first experimentally bounded step, not a verified automatic scene warp.

## Tests added

- `tests.test_japanese_debug_warp`: exact engine address, category hints, one-byte state request in big-endian and word-swapped RAM, refusal during loading, unsupported submode or wrong character, read-only handle.
- `tests.test_japan_debug_menu_controller`: declined confirmation, missing opt-in, invalid state, PID mismatch, fresh writable view, matching read-only view and one-mode-only operation.
- `tests.test_japanese_debug_ui`: compact Scene warp tab, selector index hint, write button gating and read-only precedence.
- These run under `scripts/test_japan_party.ps1` and `scripts/test_japan_party.sh`; user execution is **pending**.
