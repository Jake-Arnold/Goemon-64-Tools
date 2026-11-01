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
