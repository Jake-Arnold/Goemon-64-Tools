# Goemon Speedrun Tools v0.10.2 — clickable unlocks and sprite gallery

![Real Tkinter dashboard running in an offline test environment](docs/images/actual-dashboard.webp)

*Real application screenshot, captured in a virtual Linux display without a running game. The live-memory preview is empty until connected to US Goemon64Recomp.*

The original [README concept illustration](docs/images/readme-showcase.webp) inspired this dark gold/red interface. The actual dashboard now combines **connection, position bookmarks, logical checkpoints, route calibration, searchable scene catalog and a real live-memory preview**. Existing deep-dive tabs, including guarded hex editing and native debug-menu calibration, remain available. **Direct scene warp is still disabled**; the mock illustration's imaginary controls, scene names and RetroArch connection are not implemented.

## Custom live-memory watches (v0.10.5)

The **Live memory** tab now has **Name**, **Address** and **Type** inputs above the table, plus **Add watch** and **Remove selected watch** buttons. Add any guest address such as `0x8015C574` with `u8`, `u16`, `u32`, signed variants, `f32`, `f64` or raw eight-byte hex. Custom rows refresh with the regular memory table, support filtering by name or address, and are visibly labelled **Custom** rather than misrepresented as confirmed mappings. Double-click their Hex cell to edit after enabling **UNSAFE**. Custom watches are saved to `practice/custom_watches.json` (source) or `%LOCALAPPDATA%\GoemonSpeedrunTools\custom_watches.json` (packaged app), separate from the built-in address map.

The **State discovery** tab also has **Watch selected address**, which adds the selected candidate to Live memory in one click. Dynamic task pointers may change after changing character or stage, so watch addresses inside player tasks can become stale across loads.

**Map test correction (2026-11-02):** `0x8015C574` is **read** as `00` while hidden and `01` while visible, but **writing** `00`, `01` or other tested bytes opens the map rather than closes it. Built-in live watch available; no on/off write toggle is claimed.

**Equipped weapon (confirmed):** `0x8015C607` is a one-byte index, `01`/`02`/`03` across all four characters. The Live Memory tab now watches it; UNSAFE permits arbitrary hex writes. Out-of-range values produce unintended next-character weapon assets. Magic-active and internal player velocity remain unconfirmed.

---

## State discovery — mapping remaining live flags (v0.10.4)

A new **State discovery** tab captures N64 guest memory at **A: Before**, **B: After** and optionally **C: Reverted**. It ranks changed bytes and one-bit flags for dragon-travel destination unlocks, the map overlay, selected item/weapon, magic-active state for each character, and player-task float candidates for real velocity. No candidate is automatically treated as a verified address. The dashboard and Live Memory also show a separately labelled **derived XYZ displacement velocity**, in game units per real second.

Detailed test sequences, scope limitations and source evidence: [State discovery guide](docs/STATE_DISCOVERY.md). Captures and comparison reports remain local, never in version control.

---

## Live unlocks and item sprites (v0.10.2)

Use the new **Unlocks** tab to click actual memory values for all 26 currently mapped character, weapon, ability, and key flags. Each control immediately reads the one-byte US N64 guest address, writes the selected exact byte (no pop-up confirmation), reads it back, and refreshes the UI. The tab samples live RAM repeatedly, so values changed by the game or other tools are reflected automatically. You must connect to the game first; source `Run.bat` and the packaged executable already opt into hex editing.

- Binary unlocks write `0x00` or `0x01`. The **Chain Pipe** acquired state is **`0x02`** (not `0x01`).
- Basic weapon upgrades offer three choices (`0x00` normal, `0x01` silver/double, `0x02` gold). This avoids mislabelling multi-level values as booleans.
- The control grid shows the guest address, raw live hex value, and selected state. `0xFF` or an unexpected value remains visible rather than being interpreted as owned. Clicking does not save a disk snapshot or force the game to redraw inventory instantly.
- These mappings follow the existing GameShark-derived `practice/inspector.py` list; **some item labels remain provisional until checked in-game**. No game is connected during automated tests, so actual UI behaviour and reload rules still need verification.

The separate **Sprites** tab is a clickable gallery of those same 26 flags. It can display **original-game PNG sprites imported from your own extraction or a legitimately obtained asset set**. Select **Import original PNGs from folder** and provide images named after their snake_case item names (e.g. `chain_pipe.png`, `goemon_pipe_upgrade.png`). Imported images are stored locally in `practice/sprites/` for source runs or `%LOCALAPPDATA%\GoemonSpeedrunTools\sprites/` for the Windows executable. Only recognised filenames are copied.

**Game sprites are not bundled in this public repository.** The tab shows labelled empty image slots until you import PNG exports. It does not pretend that art from another Goemon game is the original N64 sprite. See [sprite-import guide](docs/ORIGINAL_SPRITES.md) for the full naming map. You can use the clickable cards without importing any images.

## Windows desktop build

A single-file branded Windows executable can be built with `build/Build-Windows.cmd` (double-click it on **Windows**, with 64-bit Python 3.11+ installed). The script installs PyInstaller into an isolated `.build-venv` and writes `dist/GoemonSpeedrunTools.exe`. **Windows is required to build the Windows executable; this repository does not include a prebuilt .exe.**

The executable embeds `assets/goemon_tools_logo.ico` as the Windows Explorer/taskbar icon and includes the logo resources for Tkinter's window icon. The graphical app is launched with the same opt-in practice flags as `Run.bat`, but **direct scene warp remains disabled**. Use a disposable save.

- Existing source usage remains `Run.bat`; the source-run launcher keeps local state in `practice/`.
- The packaged executable writes bookmarks, checkpoints, debug-menu profile and exported diagnostics under `%LOCALAPPDATA%\GoemonSpeedrunTools\` to avoid PyInstaller's temporary directory.
- Existing source-based bookmarks/checkpoints are *not migrated automatically*. Copy any wanted `practice/bookmarks.json`, `practice/checkpoints.json` and `practice/native_debug_fields.json` to the packaged app data directory manually.
- Only the Python unit tests have been run in this environment; the Windows packaging step and real Windows taskbar icon have not yet been verified on Windows.

## Visual assets

- `assets/goemon_tools_logo.png` — app logo artwork.
- `assets/goemon_tools_logo.ico` — multi-size Windows icon (embedded in `.exe`).
- `assets/goemon_tools_logo_small.png` — high-quality pre-rendered header icon.
- `docs/images/actual-dashboard.webp` — screenshot of the working application.
- `docs/images/readme-showcase.webp` — original concept-art reference, not a UI screenshot.

---

## v0.10.2 — Fish counts, missing items and unrestricted memory values

- **Fish counts:** red `0x8015C71B`, yellow `0x8015C71F`, blue `0x8015C723`. Use `Set hex count` to set `00..FF` (e.g. `08` for eight fish); the old 0/1 interpretation was incomplete.
- **Cucumber:** the byte previously called *Blue Sausage* at `0x8015C717` is now tentatively labelled Cucumber.
- **Four Miracle Items:** new buttons use `0x8015C85B`, `0x8015C85F`, `0x8015C863`, and `0x8015C866`. Individual icons/names are not yet mapped.
- **Achilles' Heel / Sasuke battery:** labelled **candidate** slots, not proven item identity; test against in-game status before treating them as definitive.
- **Live Memory:** enable `UNSAFE` to write any width-appropriate hex value, bypass mapped limits, or explicitly enter a guest N64 address and 1/2/4/8-byte value. The write checks old memory and verifies the result; arbitrary values can crash or corrupt game state. This does not provide a working warp.
- **Original sprites:** Sprites tab includes a link to the [referenced original sheet](https://www.spriters-resource.com/nintendo_64/mysticalninjastarringgoemon/asset/123088/) and retains the local PNG import workflow. Original copyright art is not committed to the public repository.

---

## Verified normal door transition (MACHI 353 → 351)

Observed 307 samples over 9.36 seconds on 2026-11-01. At 2715 ms, the pending destination changed **353 → 351**. At 3112 ms, the current map changed **353 → 351**, previous map changed **465 → 353**, and stage offset changed **3 → 1**. The measured gap was approximately **397 ms**. During all reported observations, top state remained **13**, game phase **1**, exit request **0**, and loading flag **0**. This does not imply those values never change within unobserved frames. A write to pending destination alone has not been established to initiate a valid area transition. Do not use the disabled v0.9.7 exit-bit warp trick.

## Live Memory tab

The tab now includes confirmed stage offset, previous map, pending destination, exit request and native menu pointer, alongside context-sensitive native category/gameplay submode. It refreshes while the native debug menu is open. Some transition-related fields are meaningful only under specific states; the UI labels distinguish these contexts.

**Double-click the Hex CELL** (third data column, labelled Hex) to open an editor. For resources and explicitly mapped inventory entries, enter a hexadecimal value (with optional `0x` prefix), review a before/after dialog, and confirm. The app checks the old value immediately before writing and verifies readback. Changes are in **canonical original N64 byte order** and appear in the diagnostic event log. They are not persisted as a game save. A changed value or in-flight game transition can prevent a write.

Game-state, map, pending destination, exit request, character, loading and menu-pointer addresses are **locked by default**. To edit them, deliberately tick the `UNSAFE: allow editing game-state/transition/pointer fields` checkbox, then confirm the individual write. These fields are unsafe and **manual writes do not implement direct warp**; they can cause a return to title, softlock or crash. The editor does not make unsupported fields (e.g. dynamic position floats) editable. The `Run.bat` launcher opts into hex-edit capability, but the separate dangerous-address toggle resets every launch. The GUI does not write anything on a simple row selection.

The version retains the v0.9.8 read-only real-door transition tracer and does not re-enable the broken direct-warp shortcut.

---

# Goemon Speedrun Tools v0.9.7 — direct scene warp experiment, no menu

**Double-click a scene in Scene browser while playing.** The first attempt asks for explicit consent because the transition is HIGH RISK and NOT validated on a live game. Once accepted, double-click attempts a scene transition without entering the original debug menu. A separate **Instead OPEN original debug menu** button remains available.

## What v0.9.7 actually does

1. Requires stable US Goemon64Recomp gameplay (state 13, phase 1, player available; no pause, script or transition).
2. Requires a known catalogued map and refuses a pending request.
3. Writes the proposed destination to `0x800C7CA0` (2-byte big-endian N64 guest value).
4. Writes `0x01` to `0x800C7A9F` (one-byte proposed exit request).
5. Monitors state, phase, map, loading, and character for eight seconds. **Only reports success after three consecutive observations of playable gameplay at the target map.** Writing a map ID or seeing a temporary match is not success.
6. Saves a JSON trace to `practice/diagnostics/direct_warp_*.json` at the moment of request and on observation completion.

**No native debug menu is opened.** The original N64 character selection highlight pointer is **not written**. Direct warp does not change the gameplay character; the separate character dropdown applies only to the original debug-menu path. The toolkit does not auto-repeat failed requests and does not attempt to revert game memory following a triggered transition, because another scene's state may already own those fields.

**Important:** The pending map/exit flag mechanism is **hypothetical**. The original engine normally runs cleanup before setting its exit request. This experiment may bypass that cleanup, fail, or corrupt live state. Do not assume it is a correct native warp procedure. Use disposable saves; back up the Goemon save directory before testing. Stop testing if the game behaves incorrectly. The actual engine transition routine still needs reverse engineering. Tests only validate Python guardrails and fake RAM; no live warp has been verified.

## Test

- Back up the game save, enter a stable non-cutscene stage, launch `Run.bat`, connect.
- Open **Scene browser**. **Double-click a different known stage** (e.g., SIRO 90 → SIRO 96). A warning appears on the first attempt; accepting sends the request immediately.
- Observe whether gameplay actually loads, not just whether the current map field changes. The status line will say either `loaded` or `NOT CONFIRMED` after eight seconds.
- Save the `direct_warp_*.json` diagnostic and describe what appeared on-screen (new room, unchanged, black screen, crash, etc.).

---

# Goemon Speedrun Tools v0.9.6 — live character-pointer verification

The character-cursor scan from November 1, 2026 returned 63 candidates. Its clearest match was the original-N64 **u32 pointer at 0x800C7E60**, which changed exactly as the original menu highlight was moved through the four characters, eight times:

| Highlight | Pointer value |
| --- | --- |
| Goemon | `0x8007BAD0` |
| Ebisumaru | `0x8007BADC` |
| Sasuke | `0x8007BAE8` |
| Yae | `0x8007BAF4` |

The pointer moves in **12-byte steps**. The one- and two-byte matches at `0x800C7E63`/`0x800C7E62` were overlapping portions of this same four-byte pointer. This is a strong *candidate* for the menu entry selection. **It has not been confirmed to be safe to write** and is not necessarily a writable character ID.

## One verification test

1. Extract this version, double-click `Run.bat`, connect to the game, and open the original game's character selection menu.
2. Open the toolkit's **Native menu calibration** tab. The LIVE read-only table now includes `Character menu entry pointer` at `0x800C7E60`.
3. Highlight **Goemon**, then **Ebisumaru**, **Sasuke**, **Yae** in the original game. Confirm the table's **Hex** column follows the four pointer values above; the status line also decodes the expected name.
4. Repeat after returning to gameplay and reopening the native debug menu in a different scene/category. The pointer must match again to be considered stable across menu entries.
5. Mark each highlight if useful, then **Export LIVE watch log**. The pointer is included in the exported log.

There are **no new memory writes** in v0.9.6. Do not select the previous **Use selected field** control for this address. A pointer to a menu record can be necessary but not sufficient for character selection and game/model loading. Direct warp/character application still requires identification of the native menu confirmation behaviour.

`Game phase (0x800C7A9E)` and `Exit request (0x800C7A9F)` can remain constant in stable gameplay; the 200 ms UI polling interval can miss momentary changes during a loading transition. Not observing changes does not prove those addresses are wrong.

---

# Goemon Speedrun Tools v0.9.5 — character cursor research

The new **Character cursor scan** tab is a read-only tool for identifying the original game's character-highlight cursor. It uses eight labelled highlights in forward and reverse order and scans original N64 guest memory from `0x80080000` to `0x80400000`, including the level-select overlay. The UI stays responsive during 300 ms paired captures and full comparison. No raw N64 RAM or ROM images are exported.

**Instructions:** Unzip and launch the single `Run.bat`, connect to the US Goemon64Recomp game, and open the original N64 debug menu with its **character selection list** visible. Open **Character cursor scan** in the toolkit. Highlight the named character in the **game's native menu** (not the toolkit dropdown), then click the matching `Record #` button. Leave the game cursor still until the toolkit reports the recording complete. Capture in this exact order:

1. Goemon
2. Ebisumaru
3. Sasuke
4. Yae
5. Yae again (stay on Yae; separate recording)
6. Sasuke
7. Ebisumaru
8. Goemon

Do not change the selected category, scene, or currently loaded game character; the scanner rejects inconsistent captures. Do not press A to enter a scene. Then click **Analyse character cursor** and **Export FULL character report**. The resulting `practice/diagnostics/native_character_cursor_*.json` contains all matching original N64 addresses, widths, and per-character values, without raw RAM. Upload that JSON for analysis. If the result has zero matches, the cursor may be outside this N64 memory region or represented by non-repeating state; this tool does not claim to find it in every build. No memory addresses are made writable by these results.

**Existing tools** from v0.9.4 remain available, including scene browser, checkpoint practice and live-watch diagnostics. The existing user-confirmed mappings for native menu category, stage offset, and absolute map were not changed. The old `Use selected field` experimental functionality remains separate and should not be used to configure the character cursor from unverified matches.

---


# v0.9.4 — complete original debug-menu ↔ gameplay watch log

v0.9.3 had a fundamental diagnostics bug: automatic log events were saved **only when state == 10**, and markers refused to record in gameplay (state 13). A marker labelled "loaded" therefore actually described another moment inside the debug menu, not the loaded gameplay state.

**v0.9.4 fixes both:** All observed changes are logged in every game state, including transitions to gameplay and intermediate loading states. The manual marker works in both native debug menu (state 10) and stable gameplay (state 13). Read-only diagnostic watches now also include game phase (0x800C7A9E), transition/exit request (0x800C7A9F), and pending scene (0x800C7CA0). User observations establish `0x800C7AA4` as native category index (in state 10), `0x800C7AB4` as stage offset, and `0x800C7AB2` as category base + offset (the absolute map ID). `0x800C7AAC` has not tracked the character highlighted in the debug menu; the original character cursor and confirm routine remain unidentified. These observations DO NOT authorise writes.

## One focused test

1. Use `Run.bat`, connect, and **Clear watch history**. While PLAYING SIRO 91 as Goemon, click **Mark current state** with label `PLAYING SIRO 91 GOEMON` (must show GAMEPLAY / state 13).
2. Open original debug menu (scene browser double-click is fine), navigate to Goemon / SIRO 90, and mark `MENU GOEMON SIRO 90` (DEBUG MENU / state 10).
3. Press the game's A button to load SIRO 90, and **without reopening the debug menu**, mark `PLAYING SIRO 90 GOEMON` once the character can move (GAMEPLAY / state 13).
4. Reopen native debug menu, highlight Ebisumaru / SIRO 96, mark `MENU EBISUMARU SIRO 96` (state 10). Press A to load, wait for player control, and mark `PLAYING SIRO 96 EBISUMARU` (state 13).
5. **Export LIVE watch log**. No 4 MB calibration scanning needed; never choose 'Use selected field' based on these probes.

The 0.2-second polling interval can miss extremely fast transitions; markers are anchored to observed stable states. All watched addresses are READ-ONLY.

---

# v0.9.3 — read-only native debug-menu watch

Use `Run.bat`; connect during gameplay, open original N64 debug menu, then go to **Native menu calibration**. The live watch reads `0x800C7AB4` (scene candidate), `0x800C7AAC` (character candidate), `0x800C7AA4` (submode), actual map `0x800C7AB2`, character `0x8015C5DC`, and game state `0x800C7A94`.

With the debug menu **open**, highlight Goemon + SIRO 90 and click **Mark highlighted selection**, change to Goemon + SIRO 96 and mark again, and change Goemon to Ebisumaru at SIRO 90 and mark a third time. Edit the manual marker before each mark. Click **Export LIVE watch log**, and share the generated `practice/diagnostics/native_watch_*.json`. No 4 MB scan required. All sampled addresses are read-only; do **not** use **Use selected field** yet.

Experimental scene warping remains unverified; v0.9.3 does not auto-apply any candidate address. All original experimental features still launch from `Run.bat`.

---

# Goemon Speedrun Tools v0.9.2 — corrected native menu calibration scanner

**v0.9.2 fixes a major limitation found in the 2026-11-01 calibration report:**
The older scanner stopped at N64 address `0x801CB460`, exactly where the original
Nintendo 64 overlay memory begins. It could miss the native menu cursor fields.
This version scans `0x80000000..0x803FFFFF` (the base 4 MiB) when in the N64
debug menu. It rejects misaligned 16/32-bit candidates and the known resident
executable region. The full candidate export remains untruncated.

The previous report had 1,864 candidates, but only four distinct scene addresses,
all found in single pair comparisons. **Do not use any of those addresses for
warping.** The older report contains no raw memory snapshots and cannot be
reanalysed with the fixed overlay scanner.

**To calibrate:** Restart the toolkit and record SIX menu highlights, keeping
the in-game selection and Toolkit character/scene labels synchronized:

1. Goemon / SIRO 90
2. Goemon / SIRO 96
3. Ebisumaru / SIRO 90
4. Goemon / MACHI 350
5. Goemon / SIRO 91
6. Ebisumaru / SIRO 96

This provides repeated scene/character comparisons. Press Find candidate memory
fields and Export FULL candidate report. Only candidates matching at least TWO
pair comparisons may be selected as experimental writable fields, and this
still does not prove they are the correct game cursor fields.



**v0.9.1 changes (retained):** Export candidate report now includes **every matched candidate**, with
no 400-entry cutoff and per-role/method totals. Only a balanced sample of at
most 400 is shown in the UI to avoid freezing while displaying thousands of
coincidental addresses; the full list is saved to a JSON file in
`practice/diagnostics/`. The analysis still depends on accurate labels for
the selected character and scene. Session observations are not persisted;
a fresh session requires fresh captures.

**Experimental practice software; Windows, US Goemon64Recomp, Python 3.11+.**

## Starting

Launch Goemon64Recomp into normal gameplay. Unzip this folder and double-click **`Run.bat`**, then connect. The launcher enables experimental tools by default. Keep a disposable save. Original `practice/checkpoints.json`, `practice/bookmarks.json`, and `route.json` can be copied from earlier releases.

## What the source establishes

The **original Nintendo 64 debug menu** is a game state, *not* a direct write to the current map ID. The [original US debug-mode patch](https://github.com/abyssonym/mn64rando/blob/master/tables/patch_debug_menu_en.txt) switches top-level state `0x800C7A94` to 10. The [decomp's US segment map](https://github.com/klorfmorf/mnsg/blob/main/config/usa/splat.yaml) identifies the level-select assembly translation unit around ROM `0x21330`, but the C source and exact debug-menu cursor/commit function aren't publicly reconstructed there. The [recomp's `src/game/debug.cpp`](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/src/game/debug.cpp) exposes a separate **host-side** `do_warp()`/pending-warp helper for its settings UI; this does not establish the original N64 menu's selection routine. Writing `0x800C7CA0` + the exit flag (as v0.7 tried) is NOT equivalent to making the selection in the original menu.

Therefore **v0.9.2 does not ship fictional character/stage cursor offsets or claim direct warping works immediately**. Instead it can learn actual native menu values from the running game, then use the learned original-game fields to stage menu selection and press the original N64 A control. The selection fields and resulting game warp still require *live verification*. The auto-warp remains disabled until calibrated.

## Character picker, double-click, and one-time calibration

The **Scene browser** tab now has a **Character for warp** picker above the list (0 Goemon, 1 Ebisumaru, 2 Sasuke and 3 Yae; the last two names remain inferred). Single-click a scene to select it.

Initially, double-click still opens the native debug menu for manual navigation, with its `SIRO` / `DOUCHU` / `MACHI` / `SHOP` index displayed. This is intentional until the cursor addresses are verified. To make double-click *actually* select and confirm a scene:

1. From gameplay open the **native debug menu** using Scene browser. In the game, highlight one scene and character but **do not press A to launch it**.
2. In the toolkit, pick **exactly the scene and character currently highlighted in the game**, then open **Native menu calibration** and click **Record highlighted native selection**. The toolkit reads two snapshots 300 ms apart, excluding memory bytes changing on their own.
3. In the original game menu, change to a different scene *in the same category*, leaving the character unchanged. Select its corresponding row in the toolkit and record again.
4. Change the original menu to the initial scene but with a different character. Update the toolkit picker to match, then record again. Also record at least one different scene **category** (`SIRO`, `DOUCHU`, `MACHI`, `SHOP`), and ideally repeat your first selections for confidence.
5. Click **Find candidate memory fields**. The list shows original N64 addresses whose values track either the complete scene ID (`map_id`), within-category stage number (`stage_index`), character number (`character_id`), or category ordinal (`category_index`). **Candidate ≠ confirmed field**; copies and counters can mimic the selection.
6. Inspect candidate addresses/widths. Highlight the genuine **scene** and **character** fields, one at a time, and click **Use selected field**. If the scene uses a stage number rather than the whole ID, also set a **category** field. The profile is saved locally as `practice/native_debug_fields.json`.
7. **Only when profile is complete** does a scene double-click enter the original menu, set the selected character/scene in its learned fields, verify they remain set on a later poll, and press the recomp's default N64 **A = Space** key. It monitors the game for the requested scene and character. A mismatched result is not reported as success. Customized game controls may require manual A confirmation.

The user needs to demonstrate several actual menu choices *once*, because the native menu's RAM layout has not been decompiled. This is not a native-ROM mod yet. If candidate fields aren't stable or aren't found, auto-warp stays disabled rather than writing unverified state.

### Diagnostics

The calibration tab's **Export FULL candidate report** writes an untruncated JSON file under `practice/diagnostics/` with addresses and labels, not ROM data or raw RAM snapshots. Only the field profile is persisted; observations are held in memory for the current toolkit session. Keep this export for later debugging.

### Safety and platform portability

All learned addresses refer to **original N64 guest RAM**, so the semantic knowledge is portable to a future custom N64 ROM. External Windows process access and simulated keystrokes are PC adapters only. A reliable future native ROM implementation should hook the real game's debug selector and execute the same scene-commit function in its own safe game-loop phase, not blindly copy PC memory.

- Auto-warp is opt-in after explicit field selection; it requires menu state 10.
- It refuses writes to known gameplay map ID, global character/inventory, and live-resource regions.
- It checks the selected bytes stayed written before sending A, and waits for both map and character to match after the transition.
- It **does not** provide fully proven scene warp or a true savestate. Game crashes/softlocks are possible in experimental mode.
- Old checkpoint/LiveSplit/inspector functionality remains, including limitations around cross-map restore.

## Testing

```powershell
py -m unittest discover -s tests -v
```

The automated suite uses simulated N64 memory; it cannot validate the native debug-menu field hypotheses against a running game. Source and tests are provided and no ROM assets are included.
