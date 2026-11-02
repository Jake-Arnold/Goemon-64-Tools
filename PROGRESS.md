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

### 2026-11-02 — Project64 connection and fragmented RDRAM discovery

- Changed: Dashboard connection selector for auto/recomp/project64; process selection rejects ambiguous instances instead of choosing the first PID. RAM discovery coalesces adjacent readable memory regions before scanning, preserving gaps and the existing pointer/player/endian validation. Corrected stale GUI version/host labels. Existing Python modules, autosplitter logic and portable C core are retained.
- Why: Project64's live 8 MiB RDRAM buffer was split into regions with different page protections, including small protected-code regions skipped by the previous minimum-region-size filter. The original scanner rejected all candidates despite valid original US addresses.
- Tested: `python -m unittest discover -s tests -q` — 172 passed on Windows, including Tk tests, fragmented-page scans, a signature across chunk boundaries, inaccessible-gap preservation, process ambiguity and read-only GUI worker selection. `git diff --check` passed. Read-only process scan and actual Tk Live memory connection to Project64 3.0.1.5664 succeeded: system pointer, Goemon ID, player/task pointers, map, HP/resources and coordinates decoded at existing guest addresses. User moved Goemon; successive probes changed map 561/XYZ (90, 0, -80) to map 353/XYZ approximately (-143.67, 0, -122.67). GUI showed map 353/Oedo Town South, Goemon, HP 10, Ryo 100 and lives 3. Test process handle was opened without write permissions. No game memory was written by these validation steps.
- Limitations: This verifies the sampled fields on one live US configuration, not every address, ROM revision, quest bit or cross-host write behavior. Project64 warps, checkpoint restores and writes remain untested. Discovery still requires an 8 MiB readable range and a loaded player; 4 MiB support is deferred. Portable C was unchanged and not rebuilt for this connection-only change. Existing executables require rebuilding/restarting to include it.
- Next: Use read-only State discovery on Project64 to collect repeated labelled event captures and compare candidates with existing recomp research; add an evidence registry and repeated-trial filtering before promoting any new flag semantics.

### 2026-11-02 — Discovery automation and unsafe-default implementation plan

- Changed: added `docs/DISCOVERY_PLAN.md` covering consistent unsafe defaults, explicit read-only override, repeated event sessions, noise/control analysis, a versioned evidence registry and a staged function-tracing/decompilation pipeline. Recorded owners, contracts, migration rules, tests, acceptance criteria and non-goals.
- Why: user requested all unsafe options enabled by default and a concrete next-step plan toward flag mapping, decompilation and a companion spanning Project64/recomp. Current launchers already enable most tools, while direct module launch and the UNSAFE checkbox differ.
- Tested: inspected current argument parsing, Run.bat, packaged entry point, raw-edit/reload gates, capture/comparison code and storage helpers. Documentation diff/whitespace validation only; no runtime implementation changed and no new in-game testing was performed.
- Limitations: defaults remain unchanged until phase 1 is implemented. The disabled legacy raw-warp prototype requires native-loader research, not simply an enable flag. Project64 write/restore behavior remains unverified.
- Next: implement phase 1 with startup/override tests, then persistent-event sessions and repeated-trial filtering. Commit and push each completed increment, verifying the remote SHA.

### 2026-11-02 — v0.11.4: consistent unsafe defaults and explicit read-only mode

- Changed: shared startup parser enables teleport, logical restore, native debug-menu access and hex editing by default. Live Memory UNSAFE starts checked when editing is enabled. Run.bat and the packaged entry point delegate defaults to that parser and forward arguments. Added `--read-only`, which takes precedence over every legacy enable flag, disables write controls, normalizes programmatic Toolkit arguments and opens a read-only process handle. WindowsProcess rejects writes through a read-only connection before native API access; automated character/debug-menu input paths also honor read-only mode. Existing legacy direct-warp code remains disabled. Updated version labels, README and plan status.
- Why: implement phase 1 of the approved discovery plan and make source/module/packaged-entry startup behavior consistent with the user's requested unsafe defaults.
- Tested: `python -m unittest discover -s tests -q` — 181 passed on Windows, including Tk, argument-order precedence, enabled/disabled controls, handler write/input rejection, startup without automatic process access, and launcher delegation. `git diff --check` passed. Actual Tk connection/poll checks on running Project64 and Goemon64Recompiled both succeeded in ordinary and read-only modes: default handle writable/UNSAFE true, override handle read-only/UNSAFE false even with `--enable-hex-edit`. Instrumented WindowsProcess.write recorded zero calls in all four live checks. Project64 map 465 and recomp map 361 had valid player coordinates. Only connectivity/default behavior was tested live; no game memory writes or game-input actions were exercised.
- Limitations: no new Windows executable was built or published; existing packaged copies need rebuilding. Project64 editing/warps/restore behavior is still unverified. Portable C is unchanged and was not rebuilt. Checkpoint semantics, action confirmations and existing address/write validation are retained.
- Next: implement phase 2/3 repeated persistent-event sessions with idle/control captures and bit-level evidence aggregation, then request labelled gameplay actions from the user.

### 2026-11-02 — v0.11.5: repeated persistent-event sessions and bit evidence

- Changed: added Event sessions tab with event/idle/control A/B trials, optional per-bit C reversion, local atomic session persistence/reopening and a background bit-ranking worker. It reports supporting, opposite, unchanged and noisy-control trials with exact IDs/notes without confirming semantics. The bounded recorder reads only `0x8015C608..0x8015C66B` plus fresh gameplay context checks; it rejects partial reads, active scripts/loading, changed contexts and reconnects without a fresh A. Added schema/version/size/trial limits, failed-save preservation, input-copy isolation and Tk poll cleanup on window destruction. Added the capture guide and updated the implementation plan/version labels.
- Why: implement the first persistent-global portion of phases 2/3 so repeated real experiments can narrow quest flags rather than relying on a single noisy A/B difference.
- Tested: `python -m unittest discover -s tests -q` — 191 passed on Windows. New synthetic/Tk coverage includes repeated packed bits, noise and contradictions, partial reversion, last event byte coverage, bounded/no-write reads, partial/context/cutscene failures, temporal ordering, duplicate IDs, persistence/unknown schema/failed replace, reconnect cancellation, GUI reopening, asynchronous responsiveness and stale analysis suppression. `git diff --check` passed. Read-only capture/save/reopen smoke checks succeeded against live Project64 (map 353) and Goemon64Recompiled (map 361); neither idle-only smoke session produced event candidates. Visually inspected the actual Event sessions tab. Local samples and launch/verification scripts remain ignored under diagnostics.
- Limitations: no new flag is confirmed. Captures are not atomic; ROM SHA-1 is optional/user-supplied and remains explicitly unverified against the running game. One session covers a single backend/map/character, with stable pointers within a trial; cross-scene events, wide/dynamic session capture and the shared semantic registry are deferred. No packaged executable built, portable C changed or in-game writes exercised. Local event samples/notes must not be committed.
- Next: user selected Goemon64Recomp and Benkei's first conversation. Prepare a separate recomp session, record an idle pair and two independent same-map conversation pairs from a backed-up pre-event state, then inspect the shortlist before tracing readers/writers.

### 2026-11-02 — Benkei first-conversation evidence and repeat-dialogue control

- Changed: recorded two first-conversation interval candidates in `practice/MEMORY_MAP.md`: `0x8015C60C & 0x20` and `0x8015C60E & 0x10`, including evidence IDs and explicit interpretation limits. No runtime behavior changed.
- Why: preserve the first actual labelled Event sessions experiment while keeping raw local samples out of Git and observational correlation separate from individual flag semantics.
- Tested: read-only captures in live Goemon64Recomp on map 369 with Goemon and stable per-trial pointers. Idle pair: no changed event bytes. First conversation: `0x8015C60C` byte `00→20` and `0x8015C60E` byte `00→10`. Repeat dialogue, reported by user as “so you're back again”: no changed event bytes; both bits remain set. Reopened/validated the local session and reran deterministic ranking. Documentation-only diff checked with `git diff --check`; Python/C tests not rerun for this evidence-only update.
- Limitations: one first-conversation trial, not an independent replay; neither bit's causal role is established. No memory writes, ROM identity proof or reader/writer trace. Raw samples remain in ignored diagnostics, not this commit.
- Next: obtain an independent replay from the user's backed-up pre-conversation state if available, then trace the two candidate bits separately.

### 2026-11-02 — Independent replay reproduces both Benkei candidate bits

- Changed: updated `practice/MEMORY_MAP.md` with independent replay evidence for both candidate bits and event support 2/2. No runtime changes or new unlock controls.
- Why: the user reset/restarted Goemon64Recomp, returned to pre-conversation gameplay and repeated the first conversation, allowing independent confirmation of the observed transitions.
- Tested: verified the toolkit's current PID matched the restarted recomp; fresh A/B captures on map 369, Goemon, passed per-trial context checks. Reopened/validated saved session and reran ranking. Both 100-byte pre-event blocks match each other; both after-event blocks match each other. Each replay changed only `0x8015C60C` byte `00→20` and `0x8015C60E` byte `00→10`. Idle and recurring-dialogue controls changed no event bytes. Documentation diff checked with `git diff --check`; Python/C suites not rerun for this evidence-only update.
- Limitations: semantic roles and causality remain unknown; two correlated bits are not two proven dialogue gates. No write tests, code tracing or live-ROM identity verification. Raw samples remain local/ignored.
- Next: inspect original-game code readers/writers for each bit and document their distinct roles. No further user gameplay action is needed yet.

### 2026-11-02 — User distinguishes Benkei dialogue completion from trigger entry

- Changed: updated `practice/MEMORY_MAP.md` with user-reported timing and intervention evidence. `0x8015C60E` cleared to `00` restores the first dialogue and becomes `10` at conversation end. `0x8015C60C` becomes `20` immediately at cutscene-trigger entry; clearing it with the other byte still `10` neither restores the first dialogue nor causes it to become `20` again. Marked the apparent path dependency as inference, distinct from captured replay evidence.
- Why: replace the undifferentiated two-candidate interpretation with the distinct behaviors observed by the user, without overstating bit isolation, script knowledge or general quest-completion semantics.
- Tested: documentation checked against the user's report and existing independent A/B/idle/control findings; `git diff --check`. No new assistant-run in-game tests, code tracing or Python/C suite run for this documentation-only change.
- Limitations: reported interventions cleared whole bytes, not isolated masks; independent masked-write/readback and unrelated-bit preservation remain unverified. The exact script conditions and wider consequences of either flag are unknown. No runtime change or new unlock control.
- Next: trace original-code readers/writers for the first-dialogue branch and the two writes; use bit-preserving operations in any future targeted validation.

### 2026-11-02 — User identifies Benkei encounter flag as Ushiwaka dialogue prerequisite

- Changed: documented `0x8015C60C & 0x20` as the user-identified Benkei encounter-recorded / Ushiwaka dialogue-prerequisite state. Updated the earlier trigger-entry label while retaining its observed timing. Kept `0x8015C60E & 0x10` separate as Benkei's own first-dialogue completion/gating state. No runtime change.
- Why: the user identified the cross-NPC purpose and supplied before/after Ushiwaka screenshots: fish-catching complaint versus the dialogue offering “Who are you?” / “Do you know Benkei?”. This adds a gameplay meaning to the previously captured trigger-entry transition.
- Tested: inspected the supplied screenshots and reconciled the report with prior captured timing/replays and the user's byte-clearing tests. The screenshots establish the visible dialogue difference; the user report establishes its address association. `git diff --check` for the documentation change. No new assistant-run in-game experiment or Python/C suite run.
- Limitations: exact script readers/branches and isolated masked-write behavior remain unverified. This does not identify Ushiwaka minigame/reward completion or imply quest completion from one edit. Copyrighted screenshots and raw samples are not committed.
- Next: trace Ushiwaka's reader of the Benkei encounter state, separately from Benkei's own completion reader and the two writes.

### 2026-11-02 — User identifies Ushiwaka introduction-seen bit

- Changed: documented `0x8015C60D & 0x20` as the user-identified state for having asked Ushiwaka “Who are you?” before, with repeat dialogue afterward. Added packed-byte interpretation to the memory map and State discovery guide; kept the `0x10` minigame-start and `0x08` blue-fish-hand-in candidates separate.
- Why: preserve the user's new Event sessions finding and prevent treating the entire byte as a single 0/0x20 boolean once other progression bits are set.
- Tested: checked against the user's report and the existing `20→30→38` observations; `git diff --check`. Documentation only; no new assistant-run in-game capture/write/code trace or Python/C suite run.
- Limitations: new report has no supplied local session file or isolated masked-write evidence. Later progression candidates are not upgraded by this observation. No runtime behavior or unlock controls changed.
- Next: trace the introduction-state reader/writer separately from the later minigame/reward state readers/writers, preserving bit-level provenance.

### 2026-11-02 — User maps cumulative Ushiwaka fish-dialogue stages

- Changed: expanded the memory map and State discovery guide with user-reported full-byte dialogue stages at `0x8015C60D`: `30` first fish set, `38` five yellow fish, `3C` eight red fish and `3E` finished dialogue for this sequence, following introduction state `20`. Listed added masks separately and retained the earlier blue-fish hand-in observation as transition timing into the yellow-fish dialogue stage. Marked later dialogue unmapped.
- Why: preserve the new stage mapping without mislabelling requested fish as already collected/handed in, this dialogue sequence as the entire quest, or cumulative values as proof of an arithmetic-add instruction.
- Tested: reconciled the user's report with existing `20→30` and `30→38` evidence; checked the mask decompositions and documentation with `git diff --check`. No new assistant-run gameplay, write, code trace or Python/C suite run for this documentation-only update.
- Limitations: new full-byte stage observations have no supplied local session evidence; precise individual bit roles and the original code's update operation remain unverified. Later Ushiwaka dialogue, reward delivery and final Benkei progression are not established by `3E`. No runtime behavior or controls changed.
- Next: trace the stage readers/writers and map later dialogue independently, preserving this sequence's evidence and the other bits in the byte.

### 2026-11-02 — User maps Benkei post-fight and Ushiwaka temple/post-minigame states

- Changed: expanded memory-map/State discovery evidence for Benkei `0x8015C60E = 18` after fighting, with crossing-permission dialogue (additional `0x08` over intro state `10`). Added Ushiwaka `0x8015C60D = 3F` forced relocation/minigame availability (`0x01` over `3E`) and normal post-minigame transition to `7F` (`0x40` over `3F`). Recorded immediate versus reloaded actor placements, shared dialogue at both tested locations, and the user's reported route endpoint.
- Why: preserve the user's new progression findings while separating a directly tested relocation value, observed normal completion, actor reconstruction on reload and unverified reward/ability side effects.
- Tested: checked the report against existing progression states and mask decompositions; `git diff --check`. Documentation-only update: no new assistant-run gameplay/flag writes, code traces or Python/C suite run.
- Limitations: no new local session files supplied for these reports. Setting `18`/`7F` or isolated masks has not been proven to reproduce fights, rewards or ability ownership. No exhaustive story audit or original-code reader/writer proof; Ushiwaka mask `0x80` remains unmapped. No runtime changes or new controls.
- Next: trace the mapped branch conditions and writes; verify separate ability ownership/crossing effects before implementing dedicated progression controls. Preserve reload-sensitive actor observations.

### 2026-11-02 — Original-ROM flag helpers, scenario references and independent annotations

- Changed: added read-only `practice.rom_flag_trace` command, four synthetic tests and `docs/ROM_FLAG_TRACE.md`. Updated discovery plan, guide and memory map with original-code/script evidence. The CLI requires the exact decompressed US hash, derives one-based file ranges from the ROM table, indexes aligned set/clear/conditional flag patterns, maps numeric IDs to guest address/mask, resolves eligible local branch targets and exclusively creates a local JSON report. It explicitly labels unreviewed matches as candidates, not decoded execution proof. No GUI behavior or dedicated progression controls changed.
- Why: user requested tracing/extrapolation without manually testing every value. Known gameplay observations now anchor the original bit helpers and scenario branches, while an existing randomizer dictionary supplies independently annotated research leads without bundling external labels as confirmed state.
- Evidence: supplied retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66` matches upstream; decompressed research SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494` also matches. Pinned mnsg `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` and mn64rando `9c580d03fe89354f79c3c83ba2e1bcf192f32577`. Direct main-code disassembly verifies set=OR at helper `0x80024038`, clear at `0x80024088` and test at `0x800240DC`, plus GEV opcodes `8020/8021/8022`. Traced known Benkei/Ushiwaka readers/writes in scenario files 97/121. The `0x8015C60D & 0x80` branch selects failed-training/retry dialogue; `0x8015C60E & 0x02` is separate magic-granted state, and its reward path writes ability ownership at word `0x8015C6F0`. Achilles' Heel inventory word `0x8015C70C` is written separately from the event flag Benkei checks. Exact offsets and limits are in the report.
- Tested: `python -m unittest discover -s tests -q` — 195 passed on Windows. Four new tests cover flag bounds/mapping, aligned references versus decoys/truncated commands, file-table validation/compression rejection, unknown-ROM rejection and preservation of the ROM path; focused tests reran after test-output cleanup. Real-ROM CLI produced 892 opcode-pattern candidates across 136 flag IDs in 1,311 nonempty file ranges. Checked the known failure branch target against that report. A separate ignored local index joins 136 external labels to references with unverified-annotation status. `git diff --check` passed and ignored status was checked for ROM/reports. No game writes or new in-game experiments performed; portable C unchanged/not rebuilt.
- Environment: isolated Python 3.13 research environment with capstone 5.0.9, PyYAML 6.0.3, lzkn64 0.2.0; the lzkn64 build rejected Python 3.14, so the existing installed 3.13 was used. Upstream decompression needed `-X utf8` on Windows. No full MIPS compiler/matching build was attempted. All cloned sources, environments, generated ROM/data and decoded dialogue remain local/ignored.
- Limitations: pattern indexing is not a complete script CFG/native dataflow scan; external labels are not all verified. Native training-result writers, exhaustive actor reload/placement logic, live-host ROM identity and full decompilation remain unresolved. Original code confirms failure-dialogue selection, not the timing of the native failure writer. No ROMs/assets/raw disassembly or full text dumps committed.
- Next: from a preserved pre-training state, have the user fail normal Mini-Ebisu training once and read `0x8015C60D`, `0x8015C60E` and ownership `0x8015C6F3` before/after using Live memory; then extend native result-writer tracing and the shared evidence registry.

### 2026-11-02 — Correct ROM scan file-range count

- Changed: corrected the ROM trace report's file-range count to 1,084 nonempty ranges. The previous entry's 1,311 figure counted adjacent file-table entries before excluding empty ranges; it was not the scanner's reported coverage count. Reference count 892 and distinct flag count 136 are unchanged.
- Why: final inspection of the generated report showed `file_ranges: 1084`; duplicate offsets represent empty entries.
- Tested: read the generated JSON counts and checked `git diff --check`; documentation only, no test-suite or gameplay rerun.
- Limitations: all previously documented opcode-pattern/native-tracing limitations remain.
- Next: focused natural failure test, then native writer tracing and registry work.

### 2026-11-02 — Later Benkei dialogue, Kihachi native gate and existing-source review

- Changed: added detailed `docs/BENKEI_KIHACHI_TRACE.md` with the user's `0x2E`/`20→28` observations, original script/native offsets, evidence limits, source inventory and clean-test procedure. Linked it from the memory map, discovery guide, README and earlier trace report. Extended the read-only ROM scanner with opt-in bounded native `LUI/ADDIU/JALR` patterns and separate native reference output; register clobbers, control flow and nonliteral/truncated arguments are conservatively excluded.
- Why: Benkei has later story involvement beyond crossing permission. The user requested extensive checks for pre-existing information and clarification of what was scanned. Original ROM bytes are the scan input; mnsg supplies layout/decompression and mn64rando supplies independently annotated technical leads, not replacement game code or automatically verified meanings.
- Findings: original Benkei dispatch tests flag `0x032` (`0x8015C60E & 0x04`) for the later Miracle Item conversation at ROM `0x7AC68C`. Its end sets flag `0x023` (`0x8015C60C & 0x08`) at `0x7AD7C0`, explaining `20→28`; an earlier-priority check then selects the repeat collector dialogue. Native file 62 initialization tests `0x023` through indirect helper call at ROM `0x72163C`, taking an early exit if clear and proceeding with setup if set. The user-reported spawn link therefore has independent native-code support. The whole `2E` also contains Mini-Ebisu-granted, Benkei-defeated and Miracle-Snow-recorded states; it is not a single later-Benkei stage. Immediate mid-room spawning is not proven.
- Existing research: inspected pinned mn64rando flag dictionary, routes, entity definitions, event patches and release notes; pinned mnsg reconstructed sources/layout; Android RE notes; the requested marshmallow FAQ 3273, Ushiwaka FAQ 26153 and Zeality script 45558 via available indexed content/find. Recorded exact links/pins and scope in the report. The requested guide corroborates the late return to Benkei and pond/food quest but supplies no flag addresses. Randomizer patches explicitly change cucumber-in-hand quest activation and are not treated as stock-ROM evidence. No exhaustive-internet coverage claim.
- Tested: `python -m unittest discover -s tests -q` — 197 passed on Windows, including six ROM-scanner tests. Focused real-ROM CLI returned four script candidates plus the manually inspected native call for flag `0x023`. Wider local bounded scan: 255 call-pattern candidates over 68 configured native code ranges; these are not complete/native-execution proofs. `git diff --check` passed. No in-game writes/new gameplay tests, portable C changes or packaged build.
- Limitations: matcher does not follow spilled pointers/nonliteral arguments or build complete CFG/dataflow; the native Kihachi guard is a required initialization condition, not proof it alone spawns the actor in every context. Further hint/reward states combine inspected script access and existing annotations; not every alternative path or mask intervention is runtime tested. Raw ROMs, disassembly, full dialogue, external research clones and generated reports remain ignored/local.
- Next: use the annotated-source index before requesting further discovery tests; if runtime confirmation is needed, use only the Thaisamba bit from a clean pre-referral backup, finish Benkei's referral, observe `0x8015C60C & 0x08`, then enter Kappa Pond normally. Do not assess vanilla Miracle Snow rewards from the `2E`-forced state.

### 2026-11-02 — First matching C decompilation checkpoint: 12 flag-bank functions

- Changed: added `decomp/event_flags.c`, pinned unit/function manifest, fresh-checkout verifier, synthetic host C tests, four Python verifier tests and clean matching-result metadata. Reconstructed all 12 set/clear/test/reset functions in upstream assembly unit ROM `249F0..24D60`, covering three flag banks and 876 function bytes. Linked the separate decomp track from README; existing companion/autosplitter/portable C behavior is unchanged.
- Why: user explicitly requested decompilation using existing available research. Establish a byte-identical upstream baseline and counted matching C before expanding native reconstruction; generated drafts/annotations alone do not count as decompiled functions.
- Baseline/evidence: pinned mnsg `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, upstream-pinned m2c `a21c1dcd7255b176c032bb932f521846e98d4372`. Initial draft reviewed and adjusted for narrowing casts/loop forms. Both the complete baseline and C-replacement 32 MiB ROM match SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. All 12 function byte ranges and guest addresses match; candidate has no assembly-placeholder markers for these functions, and its C object is present in the link map. Source/tool/per-function hashes are recorded in `decomp/results/event_flags.json` without private paths or game bytes.
- Tested: fresh `decomp/verify.py` baseline and candidate builds completed successfully under WSL Ubuntu with uv 0.13.6, locked Python 3.12 dependencies, upstream IDO and installed MIPS binutils. Host C build with `-std=c11 -Wall -Wextra -Werror -fsanitize=address,undefined` passed all 800 flags in each synthetic bank, idempotence, exact mask returns, unrelated-byte/bank isolation and 100-byte clear/sentinel bounds. `python -m unittest discover -s tests -q` — 201 passed on Windows; four verifier tests cover malformed bounds/identity, source collisions, tampered binaries, symbol movement and assembly markers. Whitespace validation performed before commit. Original ROM only read; no game writes or live rebuilt-ROM launch.
- Environment: installed local WSL build prerequisites, bootstrapped uv/locked Python in research storage, and preserved new baseline/candidate work directories. An initial Windows-written shell wrapper had a trailing CR in its final SHA command; independent hash checks and the Python verifier confirmed the successful build. Reproducible committed tooling uses Python rather than that wrapper. Nonmatching experimental attempts remain local and are not counted.
- Limitations: only this unit is newly reconstructed; untouched assembly/data remain in the build. Other two bank lifecycles and negative/arbitrary flag IDs are not newly characterized. No complete decompilation percentage, upstream acceptance, executable publication or runtime scene-loading claim. ROMs, generated assembly, binaries, compiler/dependency copies and full logs remain local/ignored. Existing portable C prototypes are unchanged.
- Next: reconstruct the system initialization/byte-memory unit, keep full-ROM matching as the gate, then expand resource/state and VM coverage using existing actor/script knowledge.

### 2026-11-02 — Matching system initialization and byte-memory unit: 15 functions total

- Changed: reconstructed all three functions in ROM unit `4D70..4E40` as `decomp/system_memory.c`: system initialization, byte zeroing and forward byte copy. Added the unit to the pinned manifest, synthetic system/buffer tests and combined result metadata. Current newly matching total is 15 functions / 1,076 function bytes across two units; all remain separate from live toolkit/portable C behavior.
- Why: expand from flag helpers into engine initialization and memory primitives while retaining exact binary behavior. Existing upstream system types were reused for renderer field accesses rather than inventing names/layouts.
- Tested: fresh verifier run built both baseline and combined candidate successfully; whole 32 MiB output SHA-1 remains `6ea0ed71032ce08fc2745f412d84936382197494` and all 15 function ranges/addresses match without assembly markers. `python -m unittest discover -s tests -q` — 201 passed on Windows. Sanitizer-enabled host C test passed zero lengths including null pointers, lengths 1/2/3/63/64/100/255/4096, sentinels/source preservation, exact forward-overlap behavior and full synthetic system initialization. The original 12-function matching result remains retained separately.
- Limitations: helper lengths are assumed nonnegative; forward copy is not a safe general-purpose memmove. Original prototypes/unknown fields are not all semantically recovered. No live game RAM init/copy calls, rebuilt-ROM launch, upstream merge, whole-game completion or binary release claimed. Failed experiments and compiler-generated files remain local/ignored.
- Next: reconstruct resource/save-state accessors, then expand event-VM coverage while using existing actor/script research for meanings and the full-ROM hash gate for matching claims.

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
