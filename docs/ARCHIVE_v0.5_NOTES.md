# Goemon Speedrun Tools — development prototype v0.5

## v0.5 — Experimental one-click scene requests

**UNVERIFIED WARP MECHANISM — READ THIS FIRST.** The button now has a guest-memory
backend, but no live validation yet demonstrates that setting original game
`0x800C7CA0` (pending map) followed by `0x800C7A9F` (exit-requested flag)
actually runs the whole transition. This is a working *request writer*, not a
proven cross-scene warp. It may do nothing, crash the game, or load into an
invalid spawn. It never directly overwrites the current map ID at
`0x800C7AB2` and refuses unsafe modes, loading, scripts and duplicate requests.

For a disposable test save, double-click `Start-EXPERIMENTAL-Scene-Warp.bat`,
connect to Goemon64Recomp, open **Scene browser**, and single-click a target
row. Confirm to send the request. The UI reports REQUESTED, then monitors
whether the destination map ID actually appears within 7 seconds. An observed
map ID is not sufficient proof that actors/spawn/scene state are correct.
The normal launchers keep list selection read-only.

This is preliminary research for a genuine original-ROM warp routine: the
recompiled host `do_warp` stores a pending request but there is no observable
consumer call on the present branch. Next step is trace or disassembly
validation of the game's real area-change state machine, including entrance
coordinates and loading sequence, before treating this as a stable practice
warp. Practice and autosplitter functions remain separate.


**Status: v0.2 memory discovery and position tracking were confirmed working by a user on Windows; v0.3 logical restore and all new v0.5 features are tested only in simulation, not yet validated in the running game.**

Two deliberately separate Windows utilities for **Mystical Ninja Starring Goemon (USA)** running through [`klorfmorf/Goemon64Recomp`](https://github.com/klorfmorf/Goemon64Recomp):

- `autosplitter/` — external memory-based LiveSplit Server bridge, with sequential checkpoint triggers.
- `practice/` — always-on-top desktop practice window: coordinates, observed displacement speed, character/action, position bookmarks, checkpoint calibration, optional explicitly unsafe position restoration, plus experimental original-N64-data logical checkpoints (live stats, flags, inventory/progression, global unlocks, position).

Neither utility patches a ROM, includes game assets, changes game timing, or installs an in-game `.nrm` mod. They are **not validated for official leaderboard submissions**. The LiveSplit bridge reads emulated N64 RAM in the Windows process, not the image on screen.

## NEW v0.5: live inspector, checkpoint diagnostics and scene navigation

**Run the safe read-only inspector:** double-click `Start-Verified-Inspector.bat` (or `Start-Practice-Toolkit.bat`) and Connect. The notebook tabs are:

- **Practice / checkpoints** — existing positions, logical checkpoint saves/restores and autosplit checkpoint calibration. Experimental restore remains opt-in.
- **Live memory** — continually refreshes original N64 addresses for character, health, max health, ryo, lives, map ID, position, game mode, item slot codes, party members, weapons and ability flags. Displays raw hexadecimal, N64 address and confidence/source. Select *Log changed values* and *Export diagnostic JSON* to document which bits change when collecting an item or changing scenes. Fields that look implausible are marked `CHECK`. **Equipped/selected item remains `UNKNOWN`: its address has not been verified.**
- **Scene browser** — searchable **partial** US scene name reference. `Start-Experimental-Debug-Menu.bat` additionally enables **Enter original-game debug / level-select menu (EXPERIMENTAL)**. This writes game state `10` using a method found in the original-ROM randomizer. It has **not** been tested against your Goemon64Recomp build and may not function. The menu is operated with normal in-game controls. **Clicking a scene name does not warp you.** Direct one-click warps are not implemented: simply changing the current map ID would corrupt scene state.
- **Checkpoint compare** — read-only per-byte comparison of live resource/progression/header data versus a chosen checkpoint, showing saved/current values, changed memory addresses and whether map/character match. Excludes the stale resource mirror `gamedata+0x64..0x93` to reduce false mismatches. This helps diagnose why the logical restore refuses to run.

**Typical cross-scene practice workflow (experimental):** capture a logical checkpoint, open the native debug menu (if supported by your build), navigate to the checkpoint's scene in the game, wait for regular gameplay, connect/reconnect the toolkit, then manually restore the same-map checkpoint. If your recomp build doesn't support the native menu, cross-scene restore remains unavailable; do not force it by writing scene ID directly. No automatic warps or emulator-style savestates are claimed.

The new original-game field catalog is documented in [`practice/MEMORY_MAP.md`](practice/MEMORY_MAP.md). New code in `portable/goemon_watch.c` and `.h` exposes the same stat/party/slot fields through a callback interface usable in a future original N64 ROM patch. Neither the C watch core nor the checkpoint C core needs Goemon64Recomp, Win32, or a host UI.

**Important:** The original game maintains transient entities, pointers and scripts beyond its save buffer. Some reads may be inconsistent while the game is running. No unsynchronised full-RAM writes or automatic scene-ID writes are used. The experimental logical restore is still prone to live-game races; only test with disposable saves.

## World record and segment names

The top listed **Any% Unrestricted** run was **ZAR — 1:07:26** when researched on 1 November 2026:

- [WR record](https://www.speedrun.com/mnsg/runs/y6qgkg1z)
- [Community Any% Unrestricted .lss](https://www.speedrun.com/mnsg/resources/mvg6d) — updated for the **Taisamba 2 Skip** route

**Important:** The community `.lss` contains a current community route. It has **not been verified to be ZAR's personal splits or precisely the route followed in the WR video**. We could not download its binary attachment in this environment, so this ZIP does not invent split names. It imports them exactly when you supply the official file.

The WR was performed on **original Japanese-region N64**. Goemon64Recomp currently accepts a **US ROM**, so this bridge is for practice on the recompilation, not for timing the original N64 recording or Japanese version. Differences in game version and mechanics must be evaluated separately.

## Requirements

- Windows 10/11 64-bit, Python 3.11+ (Tkinter included in standard Windows Python)
- Installed `Goemon64Recomp` running the US version, with an original copy of the game
- LiveSplit with the **LiveSplit Server** component for automatic splitting
- `psutil` for process discovery (or specify `--pid`; automatic discovery still needs `psutil` otherwise)

Run in PowerShell from the extracted project root:

```powershell
py -m pip install -r requirements.txt
py -m unittest discover -s tests -v
```

## 1. Import official Any% split names

Download the `.lss` from the [speedrun.com community resource](https://www.speedrun.com/mnsg/resources/mvg6d) and save it in the project root, e.g. `MysticalNinjaStarringGoemonAnyUnrestricted_0f615b3a.lss`.

```powershell
py -m autosplitter.bridge import-splits .\MysticalNinjaStarringGoemonAnyUnrestricted_0f615b3a.lss .\route.json
```

This creates a route with the **actual names and order**. Triggers are initially `null`: no splits will fire automatically until an individual checkpoint is calibrated. Never assume a stage or boss can be detected merely from its segment label.

Load the **same** `.lss` in LiveSplit (Open Splits). The bridge compares the **active segment name** against the imported route before triggering; it stops on a mismatch. It does not require newer LiveSplit Server commands.

## 2. Start LiveSplit Server

In LiveSplit, use **Edit Layout → + → Control → LiveSplit Server**. Start the TCP server (normally `127.0.0.1:16834`). Do not expose it to the internet. Start and reset LiveSplit **manually**; the correct category start/end frame has not been reverse-engineered yet. `Real Time` is used; **no load removal** is claimed.

## 3. Practice tool and checkpoint calibration

Start Goemon64Recomp and load gameplay. Then:

```powershell
py -m practice.toolkit --route route.json
```

Click **Connect**. Watch the coordinates change as the character moves; check that the character and action values make sense. If memory discovery fails, open a debugging session to find the game RDRAM host base and run with `--base 0xYOUR_BASE` (this is a Windows process address, not `0x80000000`). Both endian layouts can be selected with `--endian`.

To define a split checkpoint: get to the exact place the split should fire, choose the segment number, set a radius in game coordinate units (initially 45), and press **Capture split trigger here**. It stores `x/y/z` plus current character into `route.json`. Leave the radius and re-enter it during a LiveSplit attempt. The bridge requires two consecutive samples inside the radius, entered from outside, while the timer is running.

**Limitations:** A coordinate boundary is not equivalent to a confirmed cutscene or boss defeat. Reused positions across areas, skipped checkpoints, reloads or tricks can cause missed or incorrect triggers. The engine enforces segment order, but does not yet know a stable scene identifier. Calibrate only after confirming the route and stage context. We still need to reverse-engineer scene changes and key flags for leaderboard-quality triggers.

Position **bookmarks** are read-only and safe. The optional restore feature is deliberately disabled unless launched with:

```powershell
py -m practice.toolkit --route route.json --enable-teleport
```

This performs **unsafe direct coordinate writes** on the current player object, not a true save-state restore. It may softlock or crash if used across scenes, on moving platforms, or during cutscenes. Use only for private practice. It asks for confirmation each time and refuses during a file load or when the bookmark's character differs.

The upstream recompilation has quicksave code, but **currently disables it with `#if 0`**; it is not a reliable feature to depend on. Original-game logical checkpoint restoration is new in v0.3, described below. **True full native savestates are not implemented.**


## 3b. Original-game logical checkpoints (experimental, v0.3)

This format is intentionally independent of Goemon64Recomp-specific functionality: it captures known **original N64** game-data fields, not host state, and includes a portable C prototype under `portable/` for a future custom N64 ROM patch.

To run the opt-in **experimental full logical checkpoint restore** mode, double-click:

```text
Start-Experimental-Full-Checkpoint.bat
```

`Start-Practice-Toolkit.bat` remains read-only. Experimental writes also require the `--enable-state-restore` CLI flag. Keep the game in **ordinary non-paused gameplay** for capture and restore.

1. At the practice location, enter a checkpoint name and click **Capture logical checkpoint**. This records the current character, map, position and orientation; the live 0x30-byte resource block; the complete original game's 0x304-byte save-data buffer (including its event flags/inventory/progression); and the 12-byte global unlock header. Saves to `practice/checkpoints.json`, a distinct format from older position bookmarks.
2. Change your resources and/or flags and move elsewhere **in the same map** with the **same character**. Select the saved checkpoint and click **Restore logical checkpoint (experimental)**.
3. The tool synchronizes live stats with the save mirror/shadow, restores saved flags, position and orientation, then checks what it wrote. Current map mismatch, character mismatch, transitions, pausing, or script activity cause the operation to be refused.

**Safety warning:** The restoring Windows process is NOT game-frame synchronized; another game thread may change values during the write. Even if the bytes verify, active actors, physics/momentum, script VM state and current dynamic room objects are **not** reset; changing event flags in the middle of a room can produce inconsistent gameplay. Test on a disposable save and **do not trust/save over important progression**. Reaching a different area or changing character requires a proper original-game scene-reload implementation (not available yet). This is a **logical progression checkpoint**, *not* a complete savestate or verified full flag/variable restoration.

Known source-derived USA addresses:

| Original N64 guest address | Region |
|---|---|
| `0x8015C5D8` (0x30 bytes) | Live resources (max/current HP, ryo, lives, other live fields) |
| `0x8015C608` (0x304 bytes) | Savedata with stage, inventory, event/progression flags |
| `0x8015C910` (0x304 bytes) | Shadow savedata (kept coherent after restore) |
| `0x8015CC18` (12 bytes) | Global progression/unlocks |
| `0x800C7AB2` | Current map ID (not the save/continue stage) |

For the hardware target, start with [`portable/PORTING_TO_N64.md`](portable/PORTING_TO_N64.md). No PC recompilation API is required by its C core; a safe gameplay hook and N64 IO adapter are **still to be developed**.

## 4. Run the autosplitter

```powershell
py -m autosplitter.bridge monitor --route route.json
```

Start LiveSplit manually. It polls memory at 20 Hz, checks the LiveSplit Server's current segment index, and issues `split` only on a configured, ordered, stable state transition.

**First validate memory discovery.** Automatic scanning checks for the known game-system pointer at N64 address `0x8015C5C8`, which should hold `0x8008CCC0`, **then also checks** a valid character ID (0–3), loading flag (0/1), both player pointers, finite player coordinates and action, an aligned host RAM base and readable final RAM bytes. Endianness is detected automatically. This deliberately fails instead of reporting bogus data when it sees a coincidental pointer value elsewhere in the process. User testing with v0.2 confirmed the RAM scanner can find a real Goemon64Recomp instance. Different builds/ROMs may still differ.

If automatic discovery fails, ensure the game is loaded **in active gameplay** (not the title/menu/pause screen), then reconnect. The first release incorrectly accepted a false host base such as `0x2076379E2C4` and displayed an impossible character ID such as `80167552`. v0.2 rejects those observations. If scanning still fails, a game-version-specific host memory investigation is required rather than guessing `--base`. To override discovery, use `--base 0x...` with a verified host pointer; optionally force `--endian wordswapped` or `--endian big`.

## Known N64 memory references (USA recomp)

| Field | N64 address | Interpretation |
|---|---|---|
| `g_system_p` | `0x8015C5C8` | 32-bit pointer; initialization sets `0x8008CCC0` |
| `g_player_1_object` | `0x801FC60C` | 32-bit pointer to `Object` |
| `g_player_1_task` | `0x801FC604` | 32-bit pointer to `PlayerTask` |
| `g_current_player_character_id` | `0x8015C5DC` | 32-bit integer |
| `g_is_loading_file` | `0x8015C5D4` | 8-bit flag; **not** full loading-screen detector |
| `Object.position.x/y/z` | `Object + 0x08/0x0C/0x10` | floats |
| `PlayerTask.action_id` | `PlayerTask + 0xCC` | 8-bit field |

Source: [`patches/variables.h`](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/variables.h), [`patches/types.h`](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/types.h), [`patches/init_patches.c`](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/init_patches.c).

These references are reverse-engineering observations, not a guarantee that the windows PC port preserves every mapped RAM region between releases.

## What remains before a fully working Any% WR autosplitter

1. Repeat the successful v0.2 Windows memory-reader test on multiple Goemon64Recomp releases and confirm byte order/position tracking.
2. Obtain the `.lss` and compare its segments to the WR recording; the community template may not exactly match ZAR's personal splits.
3. Recover a stable scene identifier and progress/event flags from the decomp or recompilation; prefer those over proximity triggers.
4. Calibrate each segment against gameplay and record transition traces. Validate with run playback and false-positive cases.
5. Implement category-correct automatic timer start, completion, and possibly loading rules only after checking published rules.
6. Test against LiveSplit on Windows and then distribute an installer or native integration.

## Test coverage

The 12 Python unit tests simulate word-swapped and big-endian RAM, discovery with a decoy pointer, player data validation, LiveSplit segment import, ordered triggers, invalid-memory rejection, original-game logical checkpoint capture/restore, cross-map/character guard and checksum errors. The native-portable C checkpoint core also passes a simulated guest-memory test. They **do not** test the real Windows process, `.lss` attachment, the game's actual build, or LiveSplit integration.

## Development references

- [Goemon64Recomp](https://github.com/klorfmorf/Goemon64Recomp)
- [MNSG decomp](https://github.com/klorfmorf/mnsg)
- [Recomp mod template](https://github.com/klorfmorf/MNSGRecompModTemplate)
- [LiveSplit.Server commands](https://github.com/LiveSplit/LiveSplit.Server)
