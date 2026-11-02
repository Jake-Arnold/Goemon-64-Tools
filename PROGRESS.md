# Goemon 64 Tools — Development Progress

This file is the running development log. **Update it with every code change, commit the notes alongside the code, and push that commit to GitHub.** Keep dated entries newest first. Record what changed, why, evidence/tests, remaining issues and next steps. Distinguish automated tests from results reproduced in-game.

## Current status — 2026-11-01

**Baseline:** v0.9.9 source recovered from the original release ZIP. The deleted conversation was reconstructed separately from 102 screenshots; screenshots and personal conversation transcript are not committed to this public repository.

**Verified locally (source audit, 2026-11-01):**
- Python `pytest -q`: **84 passed, 5 subtests passed**.
- Python compilation: `python -m compileall -q autosplitter practice tests` passed.
- Portable C checkpoint/watch unit tests compiled with `cc -std=c11 -Wall -Wextra -Werror` and passed in a simulated environment.
- **Not verified:** launching the Windows GUI and observing scene/character operations on a running US Goemon64Recomp instance. Automated tests are not evidence of successful in-game warps.

**Working implementation (based on source inspection):**
- Windows-targeted game-memory connection and practice UI.
- LiveSplit autosplitter bridge/engine and an import path for route definitions.
- Read-only scene/transition tracing and native debug-menu observation tools.
- Guarded live N64 guest-memory editing; dangerous fields require explicit additional opt-in.
- Logical checkpoint/character state assistance (not a full N64 savestate).
- Portable C checkpoint/watch prototypes; **not yet installed in a custom N64 ROM**.

**Current blocker:** direct one-click scene warp. The experimental v0.9.7 pending-destination + exit-request write returned to the title screen. v0.9.9 correctly disables this unsafe route. Locate the actual engine scene/door loading routine; do not re-enable direct warp based only on map-ID changes.

**Observed normal door sequence (MACHI 353 → 351):**
- `0x800C7CA0` pending destination changed at ~2715 ms.
- `0x800C7AB2` current map changed at ~3112 ms (~397 ms later).
- `0x800C7ABC` previous map and `0x800C7AB4` stage offset changed with the committed current map.
- This establishes an observed order of values, **not** the invocation or address of a safe scene loader.

**Useful guest-RAM addresses (US build / experimental):**

| Address | Interpretation |
|---|---|
| `0x800C7A94` | Top-level game state; observed debug menu 10 and gameplay 13 |
| `0x800C7AA4` | Debug-menu category / context-dependent gameplay submode |
| `0x800C7AB2` | Current absolute stage/map ID |
| `0x800C7AB4` | Native stage offset |
| `0x800C7ABC` | Previous map ID |
| `0x800C7CA0` | Pending destination |
| `0x800C7A9F` | Suspected exit request; earlier direct write returned to title |
| `0x800C7E60` | Menu-entry pointer, **not** a standalone character ID |
| `0x8015C5DC` | Active gameplay character |

Known debug-menu category bases: SIRO 0, DOUCHU 300, MACHI 350. Additional mappings require validation. These addresses are observational findings, **not** authorisation to perform raw writes.

## Next development steps

1. Trace the native scene loader or door-transition function in the recompilation/reverse-engineered game code; corroborate against a real door transition.
2. Establish a minimal and safe state-preparation + load invocation, first in disposable saves with checks/rollback strategy.
3. Validate the change with a reproducible in-game test, capturing expected versus observed room, player state and failures.
4. Continue work on native N64 ROM menu integration only after the appropriate runtime and build integration are understood.
5. Keep the autosplitter independent from experimental writes and protect competitive-run integrity.

## Change entries

## 2026-11-02 — v0.11.3: Ushiwaka story-event probes, Sasuke battery UI, native pre-load character test

- **Ushiwaka first A/B JSON** `state_probe_20261102_110106_887579.json`: Goemon (character 0), map 371, 11:00:51.517→11:01:04.456 UTC, **before starting minigame vs after starting**. Within the persistent save event flag block, guest `0x8015C60D` changed **`0x20 → 0x30`**, bit **`0x10` set**. Strong *minigame-start/storyline-state* candidate. Other differences are transient/dynamic; no C captured. Needs controlled bit test before marking confirmed.
- **Ushiwaka second A/B JSON** `state_probe_20261102_110210_650667.json`: same character/map, 11:02:05.125→11:02:09.012 UTC, **before vs after blue-fish completion**. Same guest `0x8015C60D` changed **`0x30 → 0x38`**, bit **`0x08` set**. Blue fish quantity `0x8015C723` changed **`0x03 → 0x00`**. Bit 0x08 is a strong blue-fish completion candidate, not yet a confirmed Achilles' Heel grant or final quest completion. No C capture. Item ownership and storyline completion are separately checked in gameplay, per user's manual tests.
- **Sasuke second battery UI:** confirmed observational timing is first-battery bit `0x20`, then post-cutscene `0x40`: `0x8015C609` becomes `0x60` **at the end of** battery 2 cutscene. It is not the cutscene command. Added a clearly visible **read-only** indicator near the top of Unlocks (also already in Live Memory), plus both Ushiwaka candidate flags with explicit unverified labels.
- **Native cursor correction:** user's `0x800C7E60` persists at **128** once native menu has been opened. Original Goemon/Ebisumaru/Sasuke/Yae `0x8007BAD0...BAF4` pointer progression applied only while highlighting entries in the active native menu. The pointer is **not** a robust gameplay character selector and is never written to trigger a warp.
- **No C-Down workaround:** removed experimental scene browser's automatic post-load C-Down presses. Scene reload now optionally stages *only* global character `0x8015C5DC` (u32 0..3) **before** staging top-level game state `0x0C`, allowing the original initial actor/model loader to choose the character if it honours the ID. Source RE names spawn loader `func_801CB5D0` (reads this global) and `func_801CBC40` (initial model load); it also documents area-transition reset writes, so this is an **unverified hypothesis** until observed in-game. Does not modify per-task ID, menu pointer or XYZ. If pre-load staging fails, restores pending-map/character only while safely in source gameplay; after reload it only verifies both loaded global ID and task-local character ID. No automatic fallback or post-load writes on failure. Party-unlocked status not required for the *experimental initial loader*; this is different from normal C-Down party swapping.
- **Tests:** `xvfb-run -a python -m unittest discover -s tests -q` **171 passed** in simulated game RAM / Linux Tk. Covers pre-load write, invalid-character no-write, character-write rollback, no post-load C-Down, wrong-char result and new Unlocks displays. No Windows in-game validation; potential actor mismatch, wrong spawn, crash/softlock. Use disposable saves.
- **Next:** Observe whether the actor/model actually spawns as chosen in US Goemon64Recomp. If it does not, trace `func_80021444` transition reset and the native menu's character-to-spawn commit instead of post-loading swaps.

## 2026-11-02 — Character-aware experimental reload and battery cutscene timing
- **Live user observation:** second Sasuke battery completion changes packed event byte `0x8015C609` from `0x20` to `0x60` **after** the pickup cutscene ends. Thus bit `0x40` is an observed second-cutscene-complete marker, not evidence of the cutscene trigger. Added a read-only decoded Live Memory watch; did not add an unverified event-trigger write.
- **Character scan:** user-repeated native debug cursor sweep (Goemon/Ebisumaru/Sasuke/Yae then reverse) in map 404, menu state 10, 8 stable samples each. `0x800C7E60` four-byte pointer follows `0x8007BAD0 + 0x0C*character` (0/1/2/3). `0x800C7E62`/`63` are overlapping truncated representations, not independent fields. This is the menu-entry pointer, **not an integer character ID** and should not be written outside the original menu. Other 60 hits are lookup patterns without standalone semantic proof.
- **Fix:** Scene browser's character dropdown was completely ignored by experimental 0x0C reload. It is now captured with the destination and, after 3 playable samples, applied through the original game C-Down switch if that character is already unlocked in the party. Verify idle action, map, global character and per-task ID after native model swap. Up to 4 spaced native key presses or manual C-Down fallback; timeout, wrong map and missing party character fail explicitly. Never directly write character ID, task, or menu-pointer addresses. Native menu may load even locked characters; this fallback cannot mimic that.
- **Testing:** automated synthetic-RAM and Tk/Xvfb tests. **Not yet live-tested with a Windows game**, character-specific spawn/coordinates still unresolved.
- **Next:** verify C-Down automatic input on Windows with each target; test whether `0x800C7E60` is writable and menu-owned *inside native debug menu only* before trying to emulate its character-spawn path.

### 2026-11-02 — v0.11.1: storyline event discovery, shape labels, F1, retired motion controls
- **Narrative reverse engineering:** user observed (a) first Benkei encounter changes dialogue only once, (b) completing Ushiwaka's fish minigame and receiving Achilles' Heel advances a separate story flag, and (c) inventory ownership of Achilles' Heel **does not** substitute for the actual completion event. Fish requirements can be met with inventory edits without collecting them individually. These are **user-observed gameplay findings**, not yet offset-confirmed Benkei/Ushiwaka bits.
- Added **Storyline event / quest flag** and **Item ownership only** A/B capture instructions in State discovery; 0x015C608..0x8015C66B saved event bytes now appear in a separate `event_flag_changes` summary with set/cleared masks. An event-bit change remains a candidate until write-tested. Focused scan supports the event flag block; C is unnecessary for irreversible events.
- Live Memory now uses **Star** (`0x8015C85B`), **Moon** (`0x8015C85F`), **Flower** (`0x8015C863`), **Snowflake** (`0x8015C866`), matching already-named Unlocks fields instead of "identity unknown". Shape correspondence is taken from existing mapped unlock labels; in-game validation of all four shape addresses has not been reproduced by automated tests.
- **F1** opens the Live Memory/debug hex tab from any widget **while this toolkit has keyboard focus**. No global F1 interception from the running game (and no system hotkey).
- Removed experimentally ineffective +4/-4/speed pulse **buttons** and their dead GUI handler. User found repeated presses only nudged the player, with no usable speedup. Keep the original task+0x68 observation for investigation and derived XYZ readout; do not advertise a speed hack.
- Cross-area checkpoint restore and asynchronous connection from v0.11.0 remain; no change to the engine loader or native movie scripts. The v0.11.0 original fast A/B `reverting_changes` bug in local source is also corrected (no C means zero confirmed reversions).
- **Validation:** `xvfb-run -a python -m unittest discover -s tests -q`: 163 passed, Python compileall succeeded; synthetic RAM and Tk/Xvfb, **not live Windows Goemon64Recomp**.
- Next: capture Benkei first-dialogue A/B and Ushiwaka actual completion A/B from the same map/character and watch `event_flag_changes`. Validate quest bits by controlled masked writes on a disposable checkpoint; confirm cross-area XYZ restore during a running Windows game.

## 2026-11-02 — v0.11.0 cross-area logical checkpoint restore and responsive connection

- **Cross-area checkpoints:** Restore now detects if the live map differs from the checkpoint map. It requests the user-tested experimental stage reload by writing the saved map to `0x800C7CA0` and setting game state `0x800C7A94=0x0C`. It **does not** write saved XYZ, rotation, save data, resources or headers during the reload. A polled state machine waits until the actual loaded map ID equals the checkpoint map, ordinary gameplay (`0x0D`), no transitions/scripts, an idle live player, and at least three stable player-pointer observations after a minimum settling delay; only then does it call the existing guarded logical restore, which writes the checkpoint's exact saved coordinates. It preserves the existing native C-Down character-switch path if the loaded character differs. Same-area restores remain immediate. Cancel, a wrong loaded map, timeout and terminal write errors prevent unsafe follow-on writes; final restore errors are not retried.
- **Responsive Connect:** RAM discovery, process opening and snapshot validation moved to a daemon worker thread. Tk is updated only on its main thread via a polled completion queue, and Connect is disabled during discovery. The UI remains responsive even if scanning takes time, but discovery itself may still be slow.
- **Tests:** `xvfb-run -a python -m unittest discover -s tests -q` with synthetic RDRAM and Tk UI, **161 passing tests** (plus nine discovery-class fixtures from imports in isolated targeted runs). Regression tests for cross-area load delays, script lock, timeout/wrong map, character swapping, terminal failed writes, same-area behaviour and responsiveness while a worker blocks.
- **Limits:** This is an experimental **logical** checkpoint, **not** an emulator savestate. Camera, actor spawns, enemies, animation/physics and active cutscenes cannot be reconstructed. The game may move/snap coordinates after the tool writes them, or its forced reload may softlock. No real Windows game integration run has been performed. A disposable/backed-up save is required for safe experimentation.

## 2026-11-02 — First Sasuke battery CONFIRMED by intervention

User wrote `0x20` to `0x8015C609` before collecting first battery. After reload pickup disappeared and second battery became available. `gamedata+0x01` bit `0x20` is confirmed as first-battery progression. Unlocks sets/clears only this bit, preserving other flags. Old `0x8015C70B` guess removed from UI. Second battery not mapped; no separate second-battery JSON attached in latest turn. Synthetic-memory/UI tests passed.

## 2026-11-02 — v0.10.8 experimental 0x0C stage reload and task-float pulse

- Added opt-in **EXPERIMENT reload** in Scene browser (scene selection and double-click remain read-only). Uses user-observed sequence: write pending destination `0x800C7CA0` as u16, then top-level state `0x800C7A94 = 0x0C`. Never writes old exit flag or fabricates spawn XYZ. Read-only monitoring exports source map/character/position and observed result; reaching target map is **not evidence of correct entrance**.
- Added `PlayerTask +0x68` dynamic f32 live watch and experimental buttons for +4.0, −4.0 and 1.5× scaling (single 4-byte write). No 8-byte overlap; no unproven velocity label. Requires both source hex-edit capability and UNSAFE toggle.
- Updated source app version, Windows batch launcher, research guide and memory map. 147 automated tests and 9 subtests passed under Xvfb, including simulated GUI controls. Windows game connection and actual speed/wrap behavior have **not** been tested.
- Next: compare native-debug-menu spawn coordinates with `0x0C` reload, and record effects of positive/negative task float writes against XYZ motion. Player task base must be re-resolved per load.

## 2026-11-02 — weapon index confirmed; map, magic and player-task false positives refined

- **Equipped weapon:** `0x8015C607` (one byte) is user-confirmed across Goemon, Ebisumaru, Sasuke and Yae. Normal values `0x01`, `0x02`, `0x03` select the three current-character weapons. Manually writing out-of-range values accesses unintended next-character weapon artwork/behaviour: Goemon -> Ebisumaru hammer; Ebisumaru -> Sasuke kunai; Sasuke -> Yae sword; Yae -> what user described as `letter 1`. Exact out-of-bounds dispatch mechanics not proven. Added built-in live watch, showing unusual values as CHECK, and unsafe-edit policy permitting any single byte.
- **Map overlay:** `0x8015C574` *reads* `00` while hidden and `01` while displayed (new live user evidence). However manual writes of any tested value open the map, including `00` which does not close it. Separate read behaviour from write behaviour; never implement an `00=close` button from this evidence. Added observed-state live watch.
- **Rejected magic candidate:** `0x800C7A73` oscillates `00/01` outside magic activation. It is NOT a confirmed magic-active flag; find another source through activation-specific testing.
- **Rejected weapon candidate:** `0x8014C340` oscillates `0x40`/`0x41` and sometimes `0x00` independently. Not a dedicated selected-weapon field.
- **Velocity reassessment:** dynamic task float fields `+0x68`/`+0x70`/`+0x74`/`+0x78`/`+0x7C` (observed at `0x8016A0F8`/`0x8016A100`/`0x8016A104`/`0x8016A108`/`0x8016A10C` for one session) read zero while stationary but fluctuate during NPC conversations, weakening their identification as direct locomotion velocity. User reports maximum byte-readings ~192 (and ~191 on `+0x7C`); these are likely first bytes of IEEE-754 floats, e.g. `0xC0=192` is part of `-2.7127` at `+0x68`, **not a 192-unit velocity maximum**. Watch entire four-byte big-endian f32, and always resolve the task pointer dynamically.
- Automated tests now verify built-in equipped-weapon watch, map observed-state watch and unsafe out-of-range weapon edits. Windows gameplay not reproduced inside test runner.

### 2026-11-02 — v0.10.5: user-defined Live Memory watches + map write-trigger finding

- Added persistent custom Live memory watchers with names, arbitrary N64 guest addresses, and byte/word/signed/float interpretations. New **Add watch / Remove selected watch** controls; double-click custom Hex cells to edit only when UNSAFE is enabled. Watch definitions are stored in `custom_watches.json` in the existing source/user-data directory, not committed to GitHub.
- Added **Watch selected address** to the State discovery comparison screen for quick transfer of candidate addresses to Live memory.
- **New live finding:** the user's controlled manual writes to `0x8015C574` of `0x00`, `0x01` and other values **all caused the map to open**. Writing zero did not close it. Therefore `0x8015C574` is NOT validated as a normal map-visible 0/1 flag; could be a command/refresh trigger or a different state variable with side effects. Preserve candidate status. Do not ship a map-close toggle based on this field.
- Tests: custom watch parsing/persistence/big-endian decoding, GUI add/remove/live refresh/discovery import, mocked RAM only. No Windows live game session available in this environment.
- Next: read-only watch the address before/after C-Right without manual writes, then test alternate map closing semantics and identify the actual map visibility or menu state separately.

## 2026-11-01 — v0.10.2 inventory corrections and raw memory editor

- Reinterpreted the three fisherman fish entries as **counts**, rather than boolean unlocks: red `0x8015C71B`, yellow `0x8015C71F`, blue `0x8015C723`. Adds 00–FF hexadecimal count input buttons to Unlocks, with live readback. Based on user-reported in-game observation (01 displays one).
- Relabelled former **Blue Sausage** entry at `0x8015C717` as **Cucumber (tentative)**; item identity remains to be independently confirmed.
- Marked Triton Shell `0x8015C6FF`, Gold Key `0x8015C713`, and weapon ownership/upgrades as user-verified mappings. Existing provisional labels on other fields remain.
- Added original game cheat-list slots at `0x8015C703` (brown item), `0x8015C707` (Silver Fortune Doll?), and `0x8015C70F` (round brown item). The **Achilles' Heel** identity among those is NOT confirmed.
- Added a **Sasuke battery candidate** at `0x8015C70B`, inferred from neighbouring four-byte inventory record spacing; **not verified**. Do not describe as a confirmed battery mapping.
- Added four documented **Miracle Items** at `0x8015C85B`, `0x8015C85F`, `0x8015C863`, `0x8015C866`. Exact item/symbol correspondence (star, moon, etc.) is unknown. The last byte is the published `0xC866` address and needs verification on the running US build.
- The Live Memory **UNSAFE** checkbox now enables unrestricted 1/2/4/8-byte canonical guest hex values, including bypassing ordinary mapped field value limits and editing dynamic/watch addresses. Added a raw address/width/value editor for N64 guest RDRAM `0x80000000..0x807FFFFF`; compares original bytes and verifies readback. No Windows host address writes. This does **not** implement scene loading.
- Sprites tab now opens the exact Spriters Resource asset reference supplied by the user; original art remains optional, user-imported PNGs and is not committed in this public repository.
- Tests: see current test command output; Python mock memory and virtual display tests cannot establish in-game semantics or Windows runtime behavior.

**References:** https://gamefaqs.gamespot.com/n64/198022-mystical-ninja-starring-goemon/faqs/3274 ; https://almarsguides.com/retro/walkthroughs/n64/games/mysticalninjastarringgoemon/actionreplay/ ; https://www.spriters-resource.com/nintendo_64/mysticalninjastarringgoemon/asset/123088/ .


### 2026-11-01 — v0.10.1: one-click unlock flags and sprite gallery

- Added `practice/unlocks.py`, using only mapped one-byte GameShark-era unlocks from the live inspector. 26 character, weapon, ability and item flags with grouped controls; values are read directly from N64 guest RAM and written instantly without a confirmation dialog. Corrected interpretation of multi-level weapon upgrades (`0/1/2`) and Chain Pipe acquired state (`0/2`).
- Added **Unlocks** tab with live hex sampling, direct state-selection buttons, and before/after verification and event logging through the existing compare-before-write memory helper. No bulk guessing of unknown item codes.
- Added **Sprites** tab with live clickable cards and an import flow for original PNG item graphics. No copyrighted game textures are committed or bundled. Original assets must be provided locally; missing art is explicitly labelled. Added the full naming/attribution workflow in `docs/ORIGINAL_SPRITES.md`.
- Existing advanced hex editor remains separate. Scene warp remains disabled; no memory write tries to trigger a map load.
- Tests: all existing automated tests plus new fake-RAM tests for writes, invalid values, adjacent bytes, transitions and Tk graphical click tests. Windows/in-game integration still to verify.


### 2026-11-01 — v0.10.0: implement the README dashboard concept

- Added `practice/theme.py` with a real themed Tk/ttk dark appearance: charcoal cards, gold headings, deep-red selected tabs/buttons, teal numeric accents and dark tree/listboxes.
- Rebuilt the first tab as a two-column dashboard: live connection/coordinates, functional position and logical checkpoint controls, route calibration, searchable SCENES catalog and *actual* guest-memory preview.
- Search/scene selection synchronises to the existing full scene browser; the dashboard's scene preview does not write RAM or attempt unsafe direct warps. Double-click opens the existing detailed scene tab, not an unverified loader.
- The live-memory preview reflects the existing inspector's sampled values when connected and stays empty while disconnected. Guarded hex editing and all diagnostic tools remain in their existing tabs.
- Added a true application screenshot to `docs/images/actual-dashboard.webp`, retained original concept art separately, and included a pre-sized header logo (and PyInstaller inclusion) for sharp rendering without extra runtime dependencies.
- Kept direct scene warp disabled, advanced engine-address write opt-in unchanged, and all observed N64 addresses intact. The README does not portray imagined concept-art behaviours as working features.
- Validation: `python -m unittest discover -s tests -q` passed; a Tk desktop headless smoke test checks startup, read-only preview, scene selection, and navigation. UI run in Linux Xvfb, not yet tested in Windows or with a running US Goemon64Recomp instance.
- Next: validate Windows executable and actual live connection; refine smaller-screen layout and focus on the legitimate game loader separately.

### 2026-11-01 — Windows branded executable build and README concept art

- Changed: embedded icon branding for Tkinter window and explicit Windows taskbar AppUserModelID in `practice/toolkit.py`.
- Changed: added 256-colour PNG artwork and multi-resolution ICO in `assets/`, and conceptual README hero `docs/images/readme-showcase.webp`.
- Changed: added `goemon_app.py` and `build/Build-Windows.ps1` / `.cmd` to build a one-file windowed PyInstaller exe embedding the icon and both assets.
- Changed: moved writable data paths **only for frozen executables** into `%LOCALAPPDATA%\GoemonSpeedrunTools`, preserving source-run data layout; diagnostics and debug profile also use the writable directory.
- Why: prevent Python's default taskbar identity and allow Windows standalone startup without writing into PyInstaller's extracted temporary tree.
- Tested: `python -m unittest discover -s tests -q` — **89 tests passed**; Python syntax compilation. Windows build and actual icon display are **not tested on Windows** in this environment.
- Remaining: build on Windows, inspect taskbar and Windows Explorer icon, connect to the game, confirm app data persistence. No direct warp changes.
- Next: validate Windows build with `build\Build-Windows.cmd` and investigate safe scene-loading routine separately.

### 2026-11-01 — Initial GitHub source import (v0.9.9)

- Imported the complete v0.9.9 source release (Python GUI, autosplitter, portable C prototypes, unit tests, existing documentation).
- Added `PROGRESS.md`, `AGENTS.md`, and `.gitignore` to make change logging and safe source tracking explicit.
- Added `docs/RECOVERY_BASELINE.md` recording the audit and limitations.
- No game-memory writes, warp algorithms or feature behaviour changed in this import.
- Validation: existing source audit ran 84 Python tests plus 5 subtests, Python compile checks and both portable C tests; live gameplay remains unverified.

### Earlier development (reconstructed; not separate Git commits)

- v0.9.3–v0.9.6: Native debug-menu field calibration and read-only character-pointer discovery.
- v0.9.7: Experimental direct warp created, later shown to return to title instead of target scene.
- v0.9.8–v0.9.9: Direct warp disabled; added real-door tracing and guarded live hex editor.
- Original version-by-version notes are retained in `README.md` and `docs/ARCHIVE_v0.5_NOTES.md`.

### 2026-11-02 — v0.10.4: targeted live-state discovery

- Added `practice/state_discovery.py` and a separate **State discovery** tab with A/B/C before/after/reverted comparisons, 2 KiB system plus live/save RAM and player-task/object probes, optional 4 MiB wide scan, candidate ranking (including changed-bit masks), candidate copying and JSON export. This provides experiments to identify dragon-travel destination flags, map visibility, equipped item/weapon selection, per-character active magic and native velocity. **No new RAM offsets have been confirmed by these tests** without gameplay samples.
- Added `practice/state_discovery_ui.py`, documentation in `docs/STATE_DISCOVERY.md` and new synthetic-memory tests. Export contains filtered candidate values and context but no complete RAM dumps.
- Added derived observed XYZ velocity components and magnitude in the dashboard and Live Memory (position delta / measured wall-clock seconds). This is **not the internal per-frame physics velocity**; the unlabelled PlayerTask f32 members `+0x68..+0xC8` are only float candidates.
- Source research: official original game instructions establish C-Right (map), C-Left (weapon) and C-Up (magic); `Goemon64Recomp` player-task types do not name velocity or magic fields; Oedo tourist transport unlocks destinations after prior visits. See guide for sources and tests.
- Tested: `xvfb-run -a python3 -m unittest discover -s tests -q` — **115 tests passed** (including Tk GUI tests); no Windows build or live memory connection was available in this environment.
- Distribution: game-HUD sprite crops from the user-supplied sheet remain in the downloadable local source package but are excluded from the public repository because the original game art is copyrighted. The existing Sprites importer still works without them.
- Remaining: capture game-state comparisons and identify actual addresses, validate stable maps over restarts and test each character's magic activation. Wide capture during very short effects may miss them.
- Next: record A/B/C JSON for each of the five targets and confirm addresses in-game before exposing persistent unlock toggles or writing candidate velocity values.

## Mandatory change-log template

```markdown
### YYYY-MM-DD — Short change title
- Changed: ...
- Why: ...
- Tested: exact commands/results; specify if in-game testing was NOT performed
- Remaining: ...
- Next: ...
```

**Commit rule:** Every functional/documentation change must update this file in the same commit. Push the commit to `main` (or push a feature branch and merge it) as part of completing the change; never claim a push succeeded without checking GitHub.
