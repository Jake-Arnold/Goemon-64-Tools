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

### 2026-11-02 — v0.11.1 cross-area checkpoints, nonblocking Connect, storyline research
- Cross-area restore: request pending stage at 0x800C7CA0 then game state 0x0C; wait for correct map, stable gameplay, idle player, no script, then restore saved XYZ/rotation/progression. Abort timeout, wrong map or failed final write; native character switch if needed. Same-map remains immediate. This is not a native savestate.
- Connection discovery now runs in a worker thread; Tk only polls completion queue, so the GUI does not freeze on a long memory scan.
- User observations: first Benkei meeting changes repeated dialogue; Ushiwaka fish turn-in plus Achilles Heel reward advances a quest stage; simply adding Achilles Heel to inventory does not; providing fish by inventory edit satisfies minigame without collecting them manually. Event addresses unknown.
- State discovery now includes Storyline event / quest flag and Item ownership only actions; A/B report event_flag_changes with bits_set and bits_cleared for saved event-byte range 0x8015C608..0x8015C66B. Changes remain unverified candidates.
- F1 opens toolkit Live Memory/hex editor while it has focus (not system-wide). Miracle items show Star/Moon/Flower/Snowflake using existing Unlocks shape mapping. No new in-game shape verification.
- Removed ineffective movement probe/speed pulse buttons after user saw only minor nudges, not reliable speedups. Task+0x68 remains a research watch.
- Local validation: 163 synthetic-memory Tk/Python Xvfb tests passed; compileall passed. Windows real-game restore, connection and item shapes remain untested in this version.
- Next: real Windows cross-area restore tests, and isolated Benkei first-dialogue vs Ushiwaka award A/B flags on disposable checkpoints.

## 2026-11-02 — Second Sasuke battery A/B capture, cutscene separate from flag write

**Attached capture:** `state_probe_20261102_014420_169811(1).json` recorded on 2026-11-02 01:44 UTC, A→B 5.921 seconds apart, character 2 **Sasuke**, same map ID 329. User reports A/B before/after *collecting the second battery*; JSON labels inaccurately say "Map displayed". Focused scan, 81 changed bytes; 100 rows including f32 interpretations. `capture_C=null`. Its `reverting_changes=81` is from the old v1 exporter bug: no reversals were observed.

**Crucial negative evidence:** The confirmed first-battery **packed event byte** `0x8015C609` does **not** appear in second battery A→B changes. No bytes in the **persistent first event-flag block** `0x8015C608..0x8015C66B` changed in this comparison. User separately observed this byte later has value **`0x60`** (includes first bit `0x20` and additional bit `0x40`). **Bit `0x40` is a plausible second-battery progression marker, but this particular A/B capture does not show when it was set**. It might have been set before the A capture, at spawning, during another trigger, or after the sampled period. Do not upgrade battery 2 to confirmed from this evidence.

**Cutscene semantics:** User reports that manually setting the byte to `0x60` **did not play the cutscene** normally seen on collecting battery 2. This is consistent with pickup interaction executing a cutscene/script callback independently of persistent completion bits; it does not establish that another flag alone will launch it. Distinguish pickup hidden/unlocked, quest progression, and event playback.

**Other candidate changes (A→B):** `0x8015C562 00→01`, `0x8015CD07 00→01` (game-data scan region but **outside** the `0x8015C608..0x8015C90B` primary save payload), `0x800C7A71 00→01`, and `0x800C7AE2 00→01` (system). Their meaning is unverified and may be transient. `0x8015C86F 13→19` is **very likely elapsed seconds**: the first-battery capture showed `4D→52` (+5) over 5.191 s, and second showed +6 over 5.921 s, so do not interpret it as a quest counter. Movement/animation and player XYZ changed between A/B as well.

**Next in-game controlled test:** On a disposable save with first battery completed and second visibly uncollected, watch `0x8015C609` **before spawning**, **before touching**, **while cutscene runs**, **immediately after**, and **after area reload**. Record whether `0x20 → 0x60` happens and at which step. Separately compare event/script watch over the cutscene at higher frequency. If toggling bit `0x40` from an authentic pre-second state hides pickup and permits third-stage progression after reload, only then confirm its practical gating semantics. Keep the new first-battery masked UI as-is; no second-battery toggle yet.

## 2026-11-02 — First Sasuke battery CONFIRMED by intervention

User reached the first battery while it was **visible and not collected**, manually wrote `0x20` at guest `0x8015C609` and reloaded the room. Battery disappeared, and the next quest step allowed the **second battery** to spawn. Thus `0x8015C609 & 0x20` is a confirmed first-battery progression bit (gamedata+0x01). Earlier before/after A/B capture also showed `00→20`.

Replaced unsupported `0x8015C70B` first-battery guess with a masked bit toggle in Unlocks. Live Memory decodes Yes/No, and writes use read-modify-write, **preserving all unrelated bits** in this packed event byte. Automated unit/UI tests exercise set, clear, no-op and preservation; not yet game-tested via new UI.

**Second battery:** Its flag is still unknown. User mentioned a second before/after comparison, but **no separate second-battery file was attached** in the current message. Do not confuse earlier `state_probe_20261102_013150_717731.json` (first battery) with a second-battery probe.

## 2026-11-02 — Sasuke battery #1 pickup before/after probe

**User-provided JSON:** `state_probe_20261102_013150_717731.json`. Ebisumaru (`character=1`), same map `330`, capture A `01:31:40 UTC`, B `01:31:45 UTC`; recorded immediately before and after **first Sasuke battery**. The export's labels accidentally read "Map displayed A/B", but user identifies the actual action as first-battery collection. **No C snapshot** (`capture_C=null`), appropriate for a persistent pickup.

**Strongest candidate:** `0x8015C609`: `00 → 20` (u8 bit `0x20` set). The address is `gamedata+0x01` where saved `gamedata` starts at `0x8015C608`; independent reverse-engineering documents `gamedata +0x00..+0x63` as the persistent event-flag bitfield (https://github.com/ogdanimal/Goemon64Recomp-Android/blob/main/docs/re-notes/goemon_save_re.md). This is consistent with a one-time pickup/event and is a **strong candidate, not confirmed**.

Other changed persistent-looking bytes: `0x8015C86B` `01 → 02` (gamedata+0x263; possible progression counter, unverified), `0x8015CC30` `5C → 5D`, `0x8015CC7A` `01 → 00`. These may be unrelated event, timer or temporary context changes. The former tentative **Sasuke battery candidate** `0x8015C70B` lies inside the scanned game-data range but **did not change**; downgrade it / do not promote it as acquired battery.

**Verification:** using a session/save from before the first pickup, toggle only bit `0x20` of `0x8015C609` (`byte |= 0x20`), reload area and check battery visual/pickup/story behaviour. To reverse, clear only that bit (`byte &= 0xDF`), preserving other progress bits. A/B scans for Sasuke's second battery may independently corroborate first-battery progress semantics. Do not equate this with the inventory item code slots.

**Bug found and corrected:** `compare_captures` previously incremented `reverting_changes` even when `capture_C=null`, so this export misleadingly showed 67 "reverting" changes. The true result is 67 observed changed bytes and **no reversibility test**; new reports count only actual C-matched bytes. Regression test added; no live-memory behaviour altered.

## 2026-11-02 — v0.10.8 experimental reload and movement probes

- Added dedicated, opt-in scene reload from the observed pending destination (`0x800C7CA0`) → state `0x0C`. No exit-flag, current-map, or XYZ overwrite. Double-click remains read-only. Uses UNSAFE and explicit consent; monitors target scene and position, and does **not** claim correct spawn.
- Added dynamic player-task `f32` watch at `task_ptr +0x68` and experimental +4/−4/×1.5 four-byte pulses, with the next field `+0x6C` untouched. Speed benefit is a hypothesis, not confirmed.
- Improved transitional-state polling to retain connection during state `0x0C`; independent GUI, warp and movement synthetic tests **147 passed, 9 subtests** in Linux/Xvfb. Actual US Goemon64Recomp behaviour unverified.
- Next tests: compare debug-menu correct entrance XYZ to reload result; test +4 vs −4 f32 values at dynamic task+0x68 while measuring XYZ displacement in different movement directions.

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
