# Goemon Speedrun Tools v0.9.9 — source audit and continuation baseline

## Materials reviewed

- `Goemon_Speedrun_Tools_v0.9.9(1).zip` (43 archive entries; Windows Python GUI, autosplitter, portable C prototype, tests, and documentation).
- `Goemon_Reconstructed_Conversation.md` and `Goemon_Resume_Notes.md`, reconstructed from the 102 screenshots of the deleted thread.
- The source archive was **inspected and tested without modifying its contents**.

## Checks actually performed (2026-11-01)

- `python -m pytest -q`: **84 passed, 5 subtests passed**.
- `python -m compileall -q autosplitter practice tests`: passed.
- `cc -std=c11 -Wall -Wextra -Werror goemon_checkpoint.c test_checkpoint.c` then executed: **portable checkpoint core passed simulated guest-memory tests**.
- `cc -std=c11 -Wall -Wextra -Werror goemon_watch.c test_watch.c` then executed: **portable native watch tests passed**.
- The actual Windows Tkinter GUI and Goemon64Recomp memory integration **have not been executed in this environment**; these test results do not prove in-game functionality.

## What's new relative to the deleted conversation's v0.9.7 endpoint

The captured conversation ended at v0.9.7, with an **untested** experimental destination+exit-flag warp. The v0.9.9 README and code explicitly report that the v0.9.7 trial **returned to the title screen, not the requested room**. The source of v0.9.9 disables this method; the double-click scene action displays a warning and performs no memory writes.

v0.9.9 retains an optional native debug-menu path. When calibration data is unavailable, the user must navigate the game's own menu manually. With calibration data, it may stage learned menu fields and send a game A input after rechecking values; this is experimental and its correctness depends on the recorded field mappings. The debug-menu entry itself writes state 10.

### New evidence from a real door

The README documents a normal MACHI **353 → 351** door transition measured over 307 observations in 9.36 seconds:

- Pending destination `0x800C7CA0`: **353 → 351**, at 2715 ms.
- Current map `0x800C7AB2`: **353 → 351**, at 3112 ms.
- Previous map `0x800C7ABC`: **465 → 353**, at 3112 ms.
- Stage offset `0x800C7AB4`: **3 → 1**, at 3112 ms.
- Approximate pending-to-current observed delay: **397 ms**.
- The report says top state remained 13, phase 1, exit request 0 and loading flag 0 *in the observed samples*; a transient signal could have been missed.

**Interpretation:** pending destination changed before the committed current map, but the observation does not establish how the engine began the transition. A raw pending-map write cannot be considered a valid scene warp.

## Existing implemented modules

| Module | Purpose | Scope / limitation |
| --- | --- | --- |
| `practice/toolkit.py` | Windows Tk GUI, connection, bookmarks, logical checkpoints, route calibration | Requires live US Goemon64Recomp for runtime verification |
| `practice/ui_extension.py` | Memory inspector, scene browser, native debug-menu research, transition tracer and manual hex editing | Direct double-click scene warp is disabled |
| `practice/scene_controls.py` | Native debug-menu entry, scene ID labels | `request_scene_warp()` raises without writing |
| `practice/transition_trace.py` | Approximately 50 Hz requested, read-only, sampled transition history | Captures state deltas, not native function calls |
| `practice/hex_edit.py` | Explicitly whitelisted N64 guest RAM scalar writes with readback | Engine/warp/pointer fields need additional unsafe opt-in; writes may still be risky |
| `practice/checkpoints.py` | Logical game-data, resource and position checkpoint snapshots | Not an actual game savestate; scene and active actor constraints remain |
| `practice/native_character.py` | Temporary party unlock and native C-Down swap coordination | Uses Windows game-window keyboard injection; not a ROM-native implementation |
| `autosplitter/bridge.py`, `engine.py`, `livesplit.py` | Windows memory-based LiveSplit route runner | Route file/triggers must be supplied or configured |
| `portable/goemon_checkpoint.*`, `goemon_watch.*` | C data model and RAM callback prototypes | **Not integrated into a patched N64 ROM** |

## Known N64 memory observations worth retaining

| N64 guest address | Interpretation |
| --- | --- |
| `0x800C7A94` | Top-level game state (native debug menu 10; gameplay 13 in observed build) |
| `0x800C7AA4` | Debug category while in menu; gameplay submode otherwise |
| `0x800C7AB2` | Current / highlighted absolute map ID (not a scene-load command) |
| `0x800C7AB4` | Native stage offset |
| `0x800C7ABC` | Previous loaded map ID |
| `0x800C7CA0` | Pending destination |
| `0x800C7A9F` | Exit request: the earlier attempted write sent the game to title |
| `0x800C7E60` | Native highlighted menu-entry pointer, **not** dedicated character ID |
| `0x8015C5DC` | Active gameplay character |

The known category bases from the conversation were SIRO 0, DOUCHU 300, MACHI 350. Other category mapping is catalogued in `practice/scene_controls.py` but should not be equated with validated warp behaviour.

## Distribution and setup details

- The ZIP contains `Run.bat`, Windows-targeted Python source and `requirements.txt` (`psutil>=5.9`).
- `Run.bat` calls `py -m practice.toolkit --route route.json --enable-teleport --enable-state-restore --enable-debug-menu --enable-hex-edit`.
- **No `route.json` or `.lss` file is included in this ZIP.** The toolkit GUI can still load, but route-trigger calibration needs a route file. The `autosplitter.bridge import-splits <file.lss> route.json` command creates an uncalibrated route from a LiveSplit splits file.
- The dangerous-state memory edit toggle starts disabled even though `Run.bat` enables the hex editor overall.
- All gameplay changes should be tested on disposable saves; experimental tooling should not be used in submitted competitive runs.

## Practical project state and next technical investigation

1. Continue from **v0.9.9**, not v0.9.7. Retain the disabled unsafe shortcut.
2. Locate the original game's native **door / exit / level transition loader** in the recompilation or reverse-engineered game logic. Instrument the call sequence immediately before and after the pending destination changes, identifying what makes the game commit `current_map` and rebuild actors.
3. Separately investigate original native debug-menu **A / confirm** callback. The menu cursor and selected map are not the same as the engine's actual load request.
4. Implement any future one-click warp by invoking or correctly patching the real loader with the required entrance, cleanup and actor state, not by writing `0x800C7A9F = 1`.
5. Validate checkpoint fidelity in an actual game session, including inventory, max/current HP, ryo, lives, actor/model reinitialisation and scene-dependent flags.
6. Preserve the separation between PC-host adapters and a later ROM-native implementation.

## Reliability of this audit

Statements about source behaviour and passing tests were checked in the uploaded project. Statements about previously performed in-game transitions are **reported by the project's README** and recovered screenshots, not independently replayed here. No original ROM or Goemon64Recomp process was available to run a live integration test in this environment.
