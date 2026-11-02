# Goemon 64 Tools — Development Progress

This file is the running development log. **Update it with every code change, commit the notes alongside the code, and push that commit to GitHub.** Keep dated entries newest first. Record what changed, why, evidence/tests, remaining issues and next steps. Distinguish automated tests from results reproduced in-game.

## Current status — 2026-11-02

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

**Current blocker:** complete, correctly positioned one-click scene warp. The v0.9.7 pending-destination + exit-request approach returned to the title screen, but a later live test found **pending destination (`0x800C7CA0`) + top-level state `0x0C`** successfully loads the target stage with incorrect spawn coordinates. The app still has no validated native-equivalent warp. Determine entrance/spawn selection and correct initialization timing before enabling automation.

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

### 2026-11-02 — v0.10.5: persistent custom Live Memory watches and corrected map candidate

- Added **Custom memory watches** section to Live Memory with name, hexadecimal original N64 guest address, and explicit type (`u8/s8/u16/s16/u32/s32/f32/f64/hex8`), **Add watch** and **Remove selected watch**. Watches refresh with built-in readings, are searchable by name or address, and are explicitly marked **CUSTOM/unverified**. Hex editing of a custom row requires the existing **UNSAFE** switch. User definitions persist in `custom_watches.json` under the existing writable app data directory, not in the public Git repository.
- Added **Watch selected address** to State discovery so a chosen candidate can be monitored immediately without becoming a claimed built-in mapping.
- **Corrected hypothesis for `0x8015C574`:** live manual writes of `0x01`, `0x00`, and other values all **opened the map**; writing zero did not close it. This is **not a confirmed map-visible 0/1 boolean**. It could be a write-triggered refresh/command or state with side effects. Do not implement a map-close toggle from this address without further evidence.
- Local development tests: **127 Python tests passed** via `xvfb-run -a python -m unittest discover -s tests -q`; custom watch parsing, persistence, big-endian decoding, GUI add/remove/refresh and candidate transfer were tested with simulated guest memory. Windows in-game operation remains unverified.
- Next: inspect `0x8015C574` on ordinary C-Right open/close without writes; compare against additional map UI state candidates. Recheck dynamic player-task addresses after stage reload.

## 2026-11-02 — Ebisumaru A/B/C probes (map overlay, weapon selection, magic, movement)

User-provided screenshot comparisons plus exported `state_probe_20261102_002851_246683.json`. Original US Goemon64Recomp, **Ebisumaru character ID 1**, focused memory range. All listed candidates returned to the original bytes on C; that is correlation, **not proof of control**. No address here has been independently write-validated.

| Action | Candidate address | A → B | Assessment |
| --- | --- | --- | --- |
| Map overlay hidden → shown | `0x8015C574` (game_data byte) | `00 → 01` | Top candidate for display flag |
| Map overlay | `0x8016A165`, `0x8016A166` (player task bytes) | `00 → 01` both | Lower priority; same addresses also change during weapon selection |
| Weapon/item selection | `0x8015C607` (game_data byte) | `01 → 02` | Top candidate for selected item/weapon index |
| Weapon/item selection | `0x8014C340` (player object byte) | `40 → 41` | Possible animation/visual state |
| Weapon/item selection | `0x8016A165`, `0x8016A166` | `03 → 04` both | Likely shared task/input/animation state, not feature-specific |
| Ebisumaru magic inactive → active | `0x800C7A73` (system byte) | `00 → 01` | Top candidate for activation flag |
| Ebisumaru magic | `0x8015C5CD` (game data byte) | `0A → 08` | Secondary candidate; may be resource/state change |
| Ebisumaru magic | `0x800C79C8`, `0x800C79CA` | `08 → 09`, `ED → EC` | Secondary changing system values; ambiguous |

**Movement probe:** A=stationary, B=moving, C=stationary, same character 1 and map ID 328. Export reports 145 changed bytes, 87 returning bytes, and 98 candidates across four regions. Dynamic player-task base inferred for that session as `0x8016A090`. Compared against original recomp's `PlayerTask` struct: `+0x68` (`0x8016A0F8`) is a genuine f32 changing `0 → -2.7127`; `+0x70`/`+0x74`/`+0x78`/`+0x7C` (`0x8016A100`, `0x8016A104`, `0x8016A108`, `0x8016A10C`) are genuine f32 members changing `0 → 0.44024/-0.80182/-0.17552/0.17856`. Also `+0xD0` (`0x8016A160`) f32 `0.3 → 1`. **None is proven velocity**; may be direction/animation/camera. Conversely `+0xE8` (`0x8016A178`) is declared **s32**, and `+0x0C` / `+0x58` are in the generic task header, so f32 decoding there is misleading. Avoid promoting arbitrary subnormal f32 interpretations.

**Next tests:** Repeated open/close map probe with an isolated write to `0x8015C574`; cycle all Ebisumaru weapons and check whether `0x8015C607` advances with the selected slot and restores; repeat magic start/end for other characters to identify shared vs per-character state; check task f32 floats while running forward/backward/strafing and jumping with fixed camera. For task-local pointers, identify base dynamically each run; do not hardcode the live instance addresses.

Source of structural typing: https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/types.h . This is a research evidence update only; no runtime code or confirmed toggle mapping changed.

## 2026-11-02 — live top-level state survey and confirmed reload-triggered stage transition

**Source:** user manually edited original US Goemon64Recomp guest RAM during live gameplay. These are in-game observations, not independently reproduced automated tests. Address `0x800C7A94` holds the top-level game state (u8).

| Value written | Observed result | Confidence |
| --- | --- | --- |
| `0x04` | Game crashes | User-observed |
| `0x05` | Title screen | User-observed |
| `0x06` | Title-screen song/music state | User-observed; exact subsystem semantics unresolved |
| `0x07` | Attract/demo gameplay reached after idling at title | User-observed |
| `0x08` | Controller Pak: use / do not use prompt | User-observed |
| `0x09` | Opening cutscene | User-observed |
| `0x0A` | Original native debug menu | Established earlier |
| `0x0C` | Re-enters / reloads stage | User-observed |
| `0x0D` | Gameplay | Established earlier |
| `0x0E` | Game-over screen | User-observed |
| `0x0F` | Game crashes | User-observed |

**Important confirmed partial warp:** While in gameplay, the user wrote a different destination map to `0x800C7CA0` (pending destination, u16) and then manually forced top-level state `0x800C7A94 = 0x0C`. The game **successfully transitioned to the requested stage**. However, the character arrived with **incorrect/unexpected stage-entry coordinates**. This is substantially stronger evidence than changing the map field alone and must not be conflated with the earlier failed v0.9.7 `pending destination + exit request` experiment (which returned to title). No claim yet of a complete native-equivalent warp.

**Working hypothesis:** A direct practice warp could set pending destination, invoke state `0x0C` for a valid scene reload, and supply the correct entrance/spawn context. Merely writing player XYZ after the fact may not be fully equivalent to the native debug-menu transition: entrance selector/previous map, facing, camera, active objects, scripts, loading timing and player task construction may also matter.

**Next validation:** Capture the same target stage entered (a) through the original debug menu and (b) through the new `pending destination → 0x0C` method. Compare source map, pending/current/previous map, stage offset, top-level states, spawn XYZ, facing, camera, loading/phase and player task/entrance identifiers at multiple points before and after load. Find the entrance-selection rule and correct application timing before implementing one-click warp. Avoid interpreting `0x04` or `0x0F` as safe states.

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
