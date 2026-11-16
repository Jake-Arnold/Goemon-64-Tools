# Goemon Speedrun Tools v0.11.29 — GNOME dock WM_CLASS correctness

## v0.11.29 — fix GNOME's stable Tk class and validate numbered X11 instances

The user's Ubuntu re-run on the prior v0.11.28 test branch confirmed the **eight Japanese mock-writer errors are resolved**. The entire `bash scripts/test_japan_party.sh` run executed **265 tests with one remaining failure**: GNOME's actual Tk window advertises `WM_CLASS(STRING) = "goemon-practice-toolkit #2", "Goemon-practice-toolkit"`. The earlier smoke test wrongly demanded an exact lowercase instance, despite the real first token being allowed to acquire a Tk `#N` suffix. The previous version's `StartupWMClass=goemon-practice-toolkit` also matched neither observed token.

The installer now writes **`StartupWMClass=Goemon-practice-toolkit`**, the *stable second X11 WM_CLASS field*, while retaining the lowercase `goemon-practice-toolkit.desktop` filename, icon ID, and lowercase Tk `className` argument. The live X11 test selects the real client by window ID and validates the stable class with either a plain or `#N`-suffixed application instance; explicit tests reject Mutter frames and incorrect classes. An independent **Xvfb experiment passed with two Tk roots**, demonstrating both the unnumbered and numbered `#2` cases. The full user's Ubuntu suite still needs a fresh run; no other production toolkit code changed.

**Reinstall the desktop entry after pulling this branch:** `python3 scripts/install_linux_launcher.py`. Then restart the toolkit before evaluating dock icon grouping. This is a `.desktop` launcher fix, not a Japanese game renderer or native recomp patch.

A **separate** test log for `~/Goemon64Recomp-JP` stopped on stage-3 `test_registry_tracks_guest_lifetimes`. That user's older test compared `context->initialized.wait()` to the first `jp_guest_creations_in_flight.fetch_sub`, which occurs in the legitimate rejection-before-spawn path. The current `feature/japan-reset-guest-quiescence-stage3` branch test instead checks the distinct `memory_order_relaxed` rejection decrement **before** initialization and `memory_order_release` success decrement **after** initialization. No change to C++ reset/guest worker semantics was necessary from that assertion alone; update the game checkout and rerun its four test modules before resuming CMake. The independent intermittent `Goemon64RecompiledJP` SIGSEGV remains unassigned without a native backtrace.

See [Ubuntu failure and evidence report](docs/UBUNTU_TEST_FAILURES_2026-11-16.md). PR #30 remains draft until the Ubuntu suite has been rerun with these changes.

## Previous v0.11.28 — Ubuntu test harness repairs
## v0.11.28 — eight Japanese fixture errors and one GNOME X11 test failure

The first `main` toolkit regression run on Ubuntu completed 264 tests and reported **8 errors and 1 failure**. The eight errors all stem from synthetic `SimpleNamespace` test screens missing the real Toolkit's `_japan_writable_reader` method; they are not evidence that the real toolkit's Japanese writer is absent. The Japanese Unlocks and Live Memory edit tests now share an updated synthetic controller that delegates to the actual writer selector. The regression additionally asserts that the native Japanese recomp still uses PID/ROM/probe writer validation instead of bypassing its security gates.

The GNOME X11 smoke test used `xprop -name` and matched `mutter-x11-frames`, not the tested Tk client. It now gives the test window a unique title, selects that window's ID using `xwininfo -root -tree`, then reads `WM_CLASS` from the selected client with `xprop -id`. An equivalent lookup passed under local Xvfb with `"goemon-practice-toolkit"` as the instance class. **The complete Ubuntu suite has not yet been rerun after these changes.**

The user also reported an **independent intermittent SIGSEGV** from a separate `Goemon64RecompiledJP` binary under `~/Goemon64Recomp-JP` after the runtime heap-initialization message. It cannot be diagnosed from the test-suite failures; a matching native-game backtrace is required. `Failed to preload executable!` also appeared on noncrashing launches and is not sufficient to identify the cause. This patch makes **no changes** to that executable or to production Toolkit memory writes.

See [Ubuntu test failures and native crash report](docs/UBUNTU_TEST_FAILURES_2026-11-16.md) for exact test names, fix rationale, evidence and safe local stack-trace steps. The source/feature branch derives from `main`; all future toolkit changes continue to target `main`.

## Previous v0.11.27 — one unified toolkit development branch
## v0.11.27 — consolidate active USA/Japan toolkit development

The unified v0.11.27 USA/Japan toolkit has been **merged into `main` via PR #27**. The merge preserves the v0.11.26 Japanese-native-recomp toolkit and full 888-entrance atlas, with no feature-code reset or overwrite. It retains the current USA and Japan toolkit implementation, supported writes and process backends, Ubuntu dock launcher, 888-entry source-verified original-USA entrance atlas, unified Scene Browser, and live-memory/checkpoint tooling.

This consolidates **the active development target**, not the separate decompilation project. The older Japan toolkit, Mupen probe, native savestate, Linux prototype and earlier Japan integration branches are now **historical references**, not parallel locations for new toolkit work. Their earlier `practice/toolkit.py` and `practice/ui_extension.py` method inventories were compared with the v0.11.26 baseline; the latest toolkit contains all method names from both earlier consolidation/integration controllers, with later ROM-validation and native-recomp logic. Old code that was deliberately removed, such as the separate experimental speed controls, has not been reintroduced.

**All future toolkit changes should branch from `main` into short-lived `toolkit/*` branches, then merge reviewed PRs back into `main`.** The permanent decomp baseline stays at `chatgptweb/decomp`, with research branches off it. The previous toolkit feature branches remain historical only. Do not merge unrelated `decomp`, `file11`, Impact or ROM-research trees blindly.

Full branch map, scope, old-branch provenance and Ubuntu checkout commands: **[Toolkit branch policy](docs/TOOLKIT_BRANCH_POLICY.md)**.

This is a branch consolidation release; PR #27 merged into `main` on 16 November 2026. Its Ubuntu GUI regression suite and live USA/Japanese warp/write checks had not run at merge time, so runtime acceptance remains outstanding.

## Previous v0.11.26 — bundled complete USA/Japan warp entrance atlas
## v0.11.26 — extracted user-supplied coordinates committed to Git

The full user-extracted original-USA entrance atlas has been **validated and checked into `practice/data/entrance-coordinates.json`**. Both the USA and Japanese Scene Browser controllers now load the same numeric entrance data automatically from the repository, with no ROM selection or original ROM file needed. This fulfills the planned v0.11.25 repository-asset support; v0.11.25's statements that the data was missing are historical and are superseded by this release.

The supplied table contains **333 indexed scenes and 888 entrance records across 266 destination scenes**: 592 exits, 266 native default positions, 16 flute and 14 save entrance records. IDs and distinct entrances are preserved; one scene may have different door/source-specific XYZ coordinates, facing and mode. The table passed SHA256 checksum verification, original-USA ROM-identity verification against the extractor's pinned SHA-1 field, record-type/index/coordinate validation and unique-ID checks. **Only functional numeric metadata is committed, not the ROM.**

The file also **confirms Oedo Town South (scene 0x161 / 353)**: source-scene 351 entrance `15F:006` and native default `default:353` both place Goemon at `(-289, 0, -167)` with **heading 256 and mode 16**. The older no-ROM fallback now uses those source-verified values instead of experimental heading zero.

**To use:** pull this branch, start `bash Run-Linux.sh`, select USA or Japan, open Scene Browser, choose a destination and the desired entrance. All 888 entries are available immediately. The existing persistent user cache remains a fallback only if the repository file is absent or invalid. Destinations without a decoded entrance remain explicitly unsupported rather than receiving invented coordinates. Native Japanese Goemon's guarded one-shot post-load XYZ correction remains in place.

**Verification:** The uploaded JSON was inspected and its shape, 888 record constraints, distinct IDs and SHA256 checksum checked, then a fresh GitHub fetch confirmed the full JSON is committed without truncation. Added `tests.test_repository_entrance_atlas` and updated existing fallback tests in both Linux/Windows regression suites. The Python/Tk suite and live Japanese game warp have **not yet been run in the user's Ubuntu environment**; the PR remains draft. See `practice/data/README.md` for the exact dataset provenance and optional re-extraction command.

## Previous v0.11.25 — repository-owned entrance coordinate atlas
## v0.11.25 — bundle decoded entrance coordinates with the toolkit

The **complete verified original-USA scene/entrance coordinate table can now be committed to the repository** as `practice/data/entrance-coordinates.json`, and will become the default data source for **both USA and Japanese warps**. Once committed, everyone receives the data with `git pull` and does **not** need a ROM, a user-specific extracted atlas, or an entrance extraction step. It stores only functional numeric metadata and the existing validation checksum, **not** copyrighted ROM bytes, graphics, or audio.

**Data is not yet present in the branch.** One original USA ROM extraction must first be supplied as JSON. From the toolkit checkout:

```bash
python3 -m practice.entrances \
  --rom "/path/to/original-usa.z64" \
  --output "/tmp/goemon-entrance-coordinates.json"
```

The user can attach `/tmp/goemon-entrance-coordinates.json` to the conversation for verification and a follow-up commit to `practice/data/entrance-coordinates.json`. The ROM itself is not needed or wanted. See `practice/data/README.md`. The original extractor validates the ROM identity, checks scene/entrance structure and adds a digest.

**Lookup precedence** is now: (1) valid bundled `practice/data/entrance-coordinates.json` from Git; (2) verified per-user XDG/LocalAppData atlas; (3) validated legacy checkout cache; (4) source-backed individual observed XYZ fallbacks where no full table exists. A corrupt/invalid checked-in file cannot silently override a valid cached atlas. Multiple entrances to the same scene retain their separate IDs, source scenes, positions, headings and modes, and ambiguous choices continue to require explicit selection.

ROM-free tests cover bundle-first loading, invalid-bundle fallback, prior-cache migration, and no-ROM Oedo fallback, including the Tk GUI entrance selector; the Bash and PowerShell suites register them. The schema and full native game behaviour remain subject to tests. No false claim is made that the complete coordinate data is already checked in.

## Previous v0.11.24 — permanent scene-ID entrance coordinates
## v0.11.24 — remember fixed warp coordinates without reloading a ROM

**USA and Japanese games use the same destination/entrance lookup.** A scene ID identifies a room, but a room may have *more than one entrance and different XYZ*. The stored key therefore retains `scene ID + entrance ID` (including source map for exits) rather than collapsing all entrances to one coordinate.

The original-USA ROM extractor already cached its decoded entrance atlas, but only in the current repository checkout (`practice/entrances.json`). Now the toolkit loads validated **persistent user-level entrance coordinate data** from `~/.config/GoemonSpeedrunTools/entrance-coordinates.json` on Linux (or LocalAppData on Windows), independent of the checkout. If an earlier checkout already has a valid `practice/entrances.json`, it is automatically migrated into the persistent cache. On future launches **neither region needs the original ROM file** once a valid atlas is cached. A new one-time **Load original USA ROM** import stores the coordinate table permanently in the user directory rather than in the checkout.

The code also ships a tiny, source-labelled permanent coordinate registry, `practice/known_entrances.py`. It currently includes the only **observed in-game fixed XYZ** already confirmed in the project: **Oedo Town South, scene 0x161 / decimal 353, XYZ (-289, 0, -167)**. Its `heading=0` and `mode=0x10` are explicitly experimental, **not verified USA-ROM entrance fields**. Both USA and Japan can select this known point with **no ROM or cache at all**. Other scenes without a saved atlas remain unknown; the software refuses to invent their coordinates and instead offers the one-time extraction path.

The standard USA/Japan entrance selector gives validated ROM-extracted rows precedence over the single observed fallback, preserving every known entrance for the destination, source-specific route selection, native heading and entrance mode. A selected `Spawn` still stages the same 12-byte destination/mode/XYZ/heading in USA and Japan; Japanese Goemon also gets the guarded one-shot post-load XYZ verification/correction introduced in v0.11.23.

**Tests added:** bundled-known-point validity and missing-scene rejection; original USA and Japanese Scene Browser reuse of known coordinates without a ROM; migration of a validated old atlas to durable user configuration, then reload after deleting the old file. Tests included in Linux and Windows scripts. This PR is still draft. GitHub editing does not execute Python/Tk or the user's live recomp.

## Previous v0.11.23 — identical USA and Japan warp entrance coordinates
## v0.11.23 — shared original-USA entrance selector and XYZ for both regions

The Japanese Scene Browser now uses **the exact same original-USA ROM entrance atlas, dropdown selection, source-room prioritization, 12-byte pending entrance record and post-load XYZ goal as USA**. The user confirmed that their Japanese and USA warps should use identical destination coordinates; the toolkit no longer substitutes separately recorded Japanese positions for the selected USA entrance.

**Correction to v0.11.22's diagnosis:** the shared EntranceMixin *does* initialize the USA atlas via `init_entrances()` and reads cached `practice/entrances.json`. What was missing was **Japanese use of that shared atlas and entrance selector**. The Japan controller ignored `selected_scene_spawn()` and selected an independent Japanese capture/preset path. v0.11.23 routes Japan through **`selected_scene_spawn(destination)`**, just as USA does, with the same explicit entrance choice, heading, mode and `Spawn.pending_bytes()`. The shared entrance panel is visible on both regional Scene Browsers. Japan automatically prefers a unique entrance corresponding to the **current Japanese source scene** (read from `0x800CD2A2`), or the same USA/default fallback selection rules. When the selected entrance is unknown or ambiguous, the warp is blocked rather than staging only a scene ID.

**How to use:** open the unified toolkit, select **Japan** or **USA**, open **Scene Browser**, and in **Destination entrance** click **Load original USA ROM** if entrance data is not already cached. Select the desired map and the same entrance row for either region. Double-click or press Warp. Both stages use exactly the same decoded `(X, Y, Z)`, heading and mode values. A separately captured Japanese warp-point registry is kept only as optional historical research; it does not override this shared entrance choice.

**Post-load parity:** USA performs a guarded **one-shot player XYZ placement after scene loading**. Japan now also reads actual loaded Goemon XYZ and, if the float32 bytes differ from the chosen USA entrance, opens a fresh region-verified Japanese writable handle and writes **the exact same USA entrance XYZ** to `0x80151B10..0x80151B1B` **once**, after confirming stable Japanese gameplay, matching destination scene/Goemon, no loading and an unchanged pre-write vector. Every write includes readback and scene/character rechecks; no retries or stale-frame writes. The result reports requested and observed XYZ; a mismatch greater than eight world units remains visible. Japanese post-load placement is **Goemon-only** until player-coordinate pointers for the other characters are verified; their native 12-byte staging still uses the selected USA entrance.

**Verification boundary:** This fixes the *software path* mismatch and makes both regional warp requests use the same explicit entrance coordinates, but it has **not** been tested on the user's native Japanese recomp in live gameplay. Exact memory readback does not establish correct collision, camera orientation, cutscenes, or that a particular entrance is semantically equivalent across all regional maps. Regression tests for selected source/entrance parity, endian-correct stage/write, one-shot placement and rejection conditions were authored for both Linux/Windows suites. The draft PR remains unmerged until the Ubuntu suite and native in-game warps pass.

## Previous v0.11.22 — Japanese warp spawn coordinates
## v0.11.22 — stop silently warping without destination XYZ

**Root cause found:** The Japanese instant warp controller used `self.entrance_atlas` to find coordinates, but `self.entrance_atlas` was never initialized anywhere in the toolkit. Every uncaptured scene therefore staged a **2-byte map ID only**, not the 12-byte native entrance record `>HHhhhH` (destination, mode, X/Y/Z signed halfwords, heading). The previous code observed the new scene and finite player XYZ but never compared it with the intended destination position, so the UI could claim an apparently successful warp at the wrong coordinates.

The Japanese controller now **never imports guesses from a USA entrance atlas**. In the shared Scene Browser, use **Record CURRENT loaded Japanese room XYZ (not selected scene)** while playing as Goemon in normal gameplay. The button records the current scene's Japanese float32 XYZ and, only if a matching live 12-byte pending entrance record agrees with those coordinates, also captures its actual mode and heading. Otherwise the XYZ is saved with clearly labelled **unverified** heading/mode defaults (`heading=0`, `mode=0x10`). Each record is saved in the user's config at `~/.config/GoemonSpeedrunTools/japan-warp-spawns.json` on Linux and is reused on later launches. No game memory is written during capture.

When later warping **into a recorded scene**, the controller stages the **full 12-byte destination+XYZ+mode+heading block** before sending the Japanese `0x0C` scene reload. The previously user-observed Japanese Oedo South XYZ (`-289, 0, -167`) is offered as an explicitly experimental fallback for that scene; its heading/mode remain unverified. When the destination has **no Japanese warp point**, the controller still allows a scene-only experimental reload but states clearly that **no coordinates were staged**. It does not assert the location is correct.

Once the destination is loaded and stable, the toolkit reads the **actual Japanese XYZ** and compares it to the requested point. A displacement over 16 game units is reported prominently as **SPAWN MISMATCH**, including requested and observed coordinates. If no destination point exists, it reports **SCENE LOADED; NO DESTINATION XYZ WAS STAGED**, not successful positioning. A close XYZ reading is not proof of grounded collision or controllability. Any stale memory freezes are stopped before a validated scene warp request so an old room's frozen XYZ cannot overwrite the new room's position.

**Important limit:** This fixes the missing coordinate staging and false-success reporting, but it cannot guarantee every scene's correct native entrance, collider, facing or spawn from a USA map catalogue. Only user-captured Japanese locations are eligible for automatically staged XYZ; other rooms need live Japanese evidence. These changes are not yet tested against the user's running native Japanese recomp. Both Bash and PowerShell suites now include synthetic Japanese spawn capture and post-load mismatch tests.

## Previous v0.11.21 — Japanese native recomp write controls
## v0.11.21 — fix disabled Japanese recomp writes after successful connection

A successful Japan-0 native `recomp` attachment in v0.11.20 still left several buttons greyed out. Root cause: the connection backend admitted native `recomp`, but older Japanese UI access checks still accepted only `project64` and `mupen64plus`. This was **not** caused by `--read-only`, which remains disabled by default in the unified launcher.

All previously mapped Japanese operations now accept the same verified native recomp session, including the shared Unlocks buttons and bulk action, editable named Story Progress inventory values, bounded Goemon XYZ and original debug-menu controls, Live Memory right-click edit/freeze, and the Japanese raw-freeze worker. The shared Live Memory **Write raw hex** button now uses `write_japan_raw_bytes(..., expected=...)` for Japan, instead of being disabled as if it were a USA-only feature. Native writes continue to reopen a writable host process, verify the original Japanese retail-ROM signature and mapped 8 MiB RDRAM, and check write readback; USA layouts are not silently reused. On completing native attachment, the toolkit immediately refreshes Unlocks and Story Progress editor state.

**Still intentionally grey in Japan:** USA-specific task-pointer health/God Mode/enemy-pass-through freezes and full native emulator savestates. These features require independently mapped Japanese game objects or emulator support; simply forcing their GUI buttons on would apply the wrong ROM's semantics.

ROM-free Tk button-state and Japanese raw-editor dispatch regression tests have been added as `tests/test_japan_recomp_write_ui.py` to both Linux and Windows test suites. No local Linux native-game write was executed from the GitHub connector. The user should relaunch the updated toolkit to load the corrected UI logic.

## Previous v0.11.20 — corrected Ubuntu dock WM_CLASS
## v0.11.20 — Linux GNOME cog icon regression

Fixed the desktop/app identity mismatch responsible for the separate generic cog dock icon. Real Tk 8.6/X11 reports `WM_CLASS = "goemonPracticeToolkit", "Goemonpracticetoolkit"` for the previous `Tk(className="GoemonPracticeToolkit")`, but the v0.11.19 desktop launcher declared `StartupWMClass=GoemonPracticeToolkit`. The difference in capitalization means GNOME cannot reliably associate the running window with the installed desktop entry.

The application now starts with `Tk(className="goemon-practice-toolkit")`, whose real X11 `WM_CLASS` instance is **`goemon-practice-toolkit`**, matching both the desktop-file basename and the corrected `StartupWMClass`. Re-running `python3 scripts/install_linux_launcher.py` replaces the previous per-user launcher while preserving the original logo. Close any running toolkit first, launch **Goemon Practice Toolkit** from the Ubuntu application grid and replace an older pinned cog entry. A real Xvfb/Tk/xprop smoke probe verified the new WM_CLASS instance. Live GNOME Shell association on the user's machine remains to be checked; the new X11 identity regression test is included in the Linux test suite.

## Previous v0.11.19 — unified Linux launcher and dock identity
## v0.11.19 — one launcher, remembered region, Ubuntu dock icon

**Unified startup on Ubuntu:** `bash Run-Linux.sh` or `python -m practice.toolkit` opens the same USA/Japan application. Select the game region in the Dashboard; no `--game-version` option is required. The last selected region is remembered in the user's XDG configuration directory. The Japanese native recomp is the default target when the Dashboard is switched to Japan from auto selection; USA keeps its existing normal discovery. **Write-enabled practice controls remain the default** for both games; the explicit legacy `--read-only` override is preserved for compatibility but is not part of normal launch instructions.

**Real Ubuntu dock logo:** the existing checked-in `assets/goemon_tools_logo.png` is installed as an application icon (not a generated replacement). Run `python scripts/install_linux_launcher.py` from the checkout. It creates `~/.local/share/applications/goemon-practice-toolkit.desktop` and copies the logo into `~/.local/share/icons/` (respecting XDG_DATA_HOME); both point at `Run-Linux.sh` in this checkout. `tk.Tk(className="GoemonPracticeToolkit")` matches the desktop entry's `StartupWMClass`, so GNOME can group and display the correct icon instead of its generic cog. Open from Ubuntu's app grid and pin the application to the dock; old pinned generic/Python entries may need to be unpinned.

**Japanese native recomp:** the user confirmed that the experimental v0.11.18 connection to the running Japanese native recomp works, although process-memory discovery takes noticeable time. There is no claim that gameplay writers/warps or dock integration are independently live tested. Initial Japanese native RAM discovery still scans for verified original-ROM signatures; this release does not bypass or weaken those checks. Additional ROM-free installer/preference tests are in the cross-platform regression scripts.

## Previous v0.11.18 — Japanese native recomp support
## v0.11.18 — Japan-0 native Linux recomp attachment (experimental)

The shared USA/Japan Python/Tk toolkit now supports **Japan-0 Goemon64Recompiled** in addition to Japanese Mupen64Plus and Windows Project64. Select **Japan — Ganbare Goemon**, verify the original Japanese revision-0 retail ROM, select target **recomp**, and connect to the running Linux native Japanese game PID. Alternatively use **Launch native Linux recomp** to start a user-selected native executable.

The Japanese native reader requires three distinct original-ROM-verified guest code fingerprints, a valid 8 MiB guest RDRAM mapping, process identity and plausible Japanese game state. A USA recomp or copied cartridge buffer must never be interpreted as Japanese gameplay RAM. Native Japanese writes reverify the process and code mapping on fresh writable handles. Existing Japanese field, Story Progress, Unlocks, Live Memory and scene-reload logic is reused, but **live native Japanese gameplay has not yet been tested with this branch**. A native recomp does not support full emulator savestates; preserve separate backup save files before trying memory writes. Run `bash scripts/test_japan_party.sh` for synthetic regression tests.

The toolkit's displayed release is centralized in `practice/version.py`. Update that version, the README heading and PROGRESS.md for each future change. This avoids keeping an obsolete version in the title bar.

## Previous v0.11.17 — Plasma advice conditions

## Region-aware shared toolkit — 2026-11-15

The **same Scene Browser, Live Memory, Unlocks, Story Progress, Event Sessions, Value Search and damage-event UI** now select the appropriate address readers according to **USA** versus **Japan-0**. For Japan, source-backed inventory/scene/progress fields are read-only unless a specific user-tested one-shot write exists; USA event-bit and player-task addresses are never silently reused. Additional Japanese watch and stage evidence remains needed for complete semantics.

**Scene Browser is the only scene list.** USA double-click stages native pending entrance/map and writes engine state `0x0C` to reload immediately. Japan now does the **same**, using guest `0x800CD490` for pending destination and `0x800CD284 = 0x0C` for reload. **It no longer opens the debug menu or sends N64 A on double-click.** The original debug-menu button is a separate manual action (`0x0A`). Existing cached USA entrance data can be staged as a reference when unambiguous; otherwise Japan stages only the pending scene ID and warns about unverified spawn. **Full Japanese inter-scene loading remains to be verified in live Project64.** See [the native warp guide](docs/JAPAN_NATIVE_DEBUG_SCENE_WARP.md).

**Japan ROM verification is remembered:** after the first successful exact revision-0 verification, the canonical file path is stored under the user config directory and **the actual ROM is reverified at startup**. The live emulator code probes, PID, mapping and endian are still checked upon attachment and before guarded writes. Changing or removing the ROM invalidates the remembered selection.

New synthetic backend/Tk regressions are in `scripts/test_japan_party.ps1` and `scripts/test_japan_party.sh`. **They have not been run on the user's Windows installation after this consolidation.** The branch is experimental and PR #17 remains draft.

## Unified logical checkpoints

The Dashboard now has one **Logical checkpoints** panel: enter a name, choose **Capture logical checkpoint**, select from **Saved checkpoints**, or **Restore selected checkpoint**. A new full checkpoint already records XYZ position, rotation, character, map, health, lives, Ryo, inventory and saved progression flags. It is a logical snapshot, **not** an N64 savestate; actor state, camera, active scripts and physics are not captured. Cross-room restoration continues to use the guarded experimental stage reload and character-swap flow.

The older `bookmarks.json` is **read-only legacy input**, not silently converted into fabricated progression snapshots. Its entries appear at the end of the same selector as **legacy POSITION ONLY**; restoring one may write XYZ only in the original map with the original character, after a separate warning. Legacy bookmarks with unknown maps cannot be restored. Existing `bookmarks.json` and `checkpoints.json` are preserved; new captures save only to `checkpoints.json`. There is no separate Save position/Restore position UI.

## Experimental Japanese Project64 3.0 support on Windows

Japan-0 can now use the exact-ROM-verified memory attachment with **Project64.exe on Windows** or Mupen64Plus. Project64 RDRAM may be 4 MiB or 8 MiB. Read-only Japanese Live, custom watches, Value Search and Advanced A/B/C compare use the verified region reader; USA-specific field writers remain unavailable in Japanese mode. Japanese writes are now isolated, explicitly opted-in operations: verified Sasuke/Yae party flags; experimentally validated Goemon XYZ in Oedo Town South; and a **user-live-verified** entry into the game's native debug level selector. No Japanese generic raw hex editor, arbitrary freeze, or direct map-ID write is enabled. **The shared Scene Browser now implements a guarded experimental immediate `0x0C` reload for Japanese Project64, patterned after the USA reload; not yet validated end-to-end in the emulator.**

**Status (2026-11-15): user confirms Windows PowerShell tests, live Project64 Japanese read-only memory, Project64 savestate restoration and both Sasuke/Yae unlock writes work.** Screenshots separately verify Ryo Value Search, scene context and focused A/B/C. The user subsequently demonstrated position-controlling Japanese XYZ floats at `0x80151B10/14/18`, including moving Goemon to Oedo South's entrance and raising him by changing Y. A **separately opted-in, Goemon/Oedo South only** manual XYZ panel now exists. The new [native debug-menu entry and scene-warp research path](docs/JAPAN_NATIVE_DEBUG_SCENE_WARP.md) has now **successfully opened the original Japanese debug menu in live Windows Project64**, but the first Japanese Scene Browser double-click only opened that debug menu. The updated code now stages the pending destination and immediately requests `0x0C` area reload instead, like USA. **The resulting automatic cross-scene load remains unverified in live Project64.** Native Sasuke/Yae character-index 2/3 transitions remain separately outstanding. See [Project64 setup](docs/JAPAN_PROJECT64_WINDOWS.md) and [parity checklist](docs/USA_JAPAN_TOOLKIT_PARITY_CHECKLIST.md). The PR remains draft. The user-provided 2026-11-15 log showed 107 backend tests passing and GUI regressions (39 test-host setup errors, one blank savestate slot) that have been corrected in source; post-fix full Windows GUI validation is still pending.

## Current simplified toolkit layout

Dashboard contains **Connection** and **Logical checkpoints** side by side at its default 1220×790 window size, keeping both panels visible without scrolling. At narrower widths, the cards stack vertically and the scrollbar remains available. Scene Browser and Live Memory are separate dedicated tabs; the dashboard no longer duplicates their tables.

The rebuilt-recomp **Game speed** UI has been removed. Standalone speed research and preparation code remains in the repository but is not part of the toolkit interface.

**Event sessions** has two internal tabs: **Event flag sessions** for repeated 100-byte USA saved-event experiments or a user-selected 100-byte Japanese *research window* (not a known JP saved bank), and **Advanced RAM comparison** for the former State discovery A/B/C probes (including wide scope and no-player contexts). The redundant **Saved / shadow** UI has been removed.

**Story progress** has subject tabs (Fortune Dolls, Benkei/Kihachi, Ushiwaka/training, keys/locks, collectibles, external annotations, diagnostics) plus an **All** view. Fortune Doll pickup flags and the two known word counters are together. Live Memory no longer repeats all story flags or the low-byte alias of the full Fortune Doll progress word.

## Gameplay presets

**God Mode** is a session-only checkbox in **Value freezes**. It uses the existing 10 ms worker to maintain health at its known current maximum, 99 lives and 9,999 Ryo. It is independent of enemy-body pass-through and does not change inventory. Turning it off stops writes; already increased resources are not reverted.

**Unlock all mapped items, weapons and abilities** is a one-time button in **Unlocks**. It sets all 34 mapped party members, weapons, upgrades, known abilities, items, collectible flags and capped fish counts. It preserves unrelated bits in the shared battery field; it does **not** mark general story progression complete or modify unknown inventory slots. Changes are immediate, may partially apply if interrupted, and may require a menu or area reload to appear.

**Open original debug menu** in Scene browser no longer requires scene selection and does not stage a warp or character change. Double-click/reload still requires a destination.

## Experimental player-relative enemy pass-through

The **Value freezes** tab has a **Pass through enemies** checkbox. It continuously resolves the active player-task pointer at `0x801FC604` and targets its `+0x30` byte with value `6` while normal gameplay is active. The game's player task may move in guest RAM after transitions; never substitute a permanently frozen address such as `0x80169FD0`. The existing independent 10 ms freeze worker performs the pointer lookup and suppresses writes during pause, scripts and loading. On disconnection, permission failure or reconnect, the toggle stops; turning it off leaves state restoration to the game.

The value `6` was observed by the user to permit moving through enemies in one tested scene. This is **not** a verified no-damage or terrain-noclip mode and can be overwritten by the game between toolkit writes. Experimental gameplay use only.

## Active development branch and damage-event recorder

Use `main` as the integrated USA/Japan toolkit baseline after PR #22 (16 November 2026). Work on isolated feature branches and merge only after tests and live acceptance. Preserve the existing right-click freeze/rename controls, fast freeze engine and external Linux PID support. See [branch workflow](docs/BRANCH_WORKFLOW.md) before creating, deleting or merging research branches.

The **Automatic events** tab captures read-only memory samples around health-loss events, ranks transient candidate fields and exports JSON evidence. It is designed to investigate damage immunity and collision handling; candidate addresses are not yet verified collision controls. Recording stops on map, character, pointer or connection changes.

## Linux existing PID and write-enabled controls

Enter the PID of an already-running native Linux game, then choose **Connect to
game**. Where Linux Yama permissions block it, the Connection panel offers an
explicit polkit authorization to temporarily permit normal same-user external-PID
memory access; this **weakens system-wide same-user process isolation** until
restored. See [Linux access guidance](docs/LINUX_TOOLKIT.md).

Memory editing, scene reload and Live Memory context-menu freezing are available
without an additional unlock checkbox. Practice writes default on in Linux and
Windows; launch with `--read-only` to disable game writes and automated input.

## Experimental native Linux toolkit

The Python/Tk toolkit has an experimental native Linux process-memory backend, a native-game launch control, existing-PID connection with optional OS authorization, write-enabled practice controls by default, original-ROM-researched script diagnostics, **X11-only verified-target key injection**, and a **Linux speed channel for separately rebuilt patched hosts**. See [Linux setup and limitations](docs/LINUX_TOOLKIT.md). This is not a claim of Wayland input support, stock-recomp speed control or live gameplay verification.

The four normal Plasma locations share one advice event. Story progress now
includes all 39 bits checked or set by its traced advice path. Your two forced
bit tests confirm the first two checks are priority ordered. See
[Plasma advice conditions](docs/PLASMA_TRIGGERS.md) for the ordered path,
provenance, and limits. Later conditions remain unverified in gameplay.

## Oedo dialogue observations

Story progress includes the two observed alternating-dialogue bits for the
map 353 old man and the map 432 coffee-shop man. The existing Omitsu flag
entry now includes the user’s first-conversation observation. See
[Oedo dialogue observations](docs/OEDO_DIALOGUE_FLAGS.md).

## Archived speed-control research

The previous Dashboard speed controls were removed because they required a separately rebuilt recomp. Source preparation and experimental standalone speed-control modules remain for reference; see [speed research](docs/SPEED_CONTROL_RESEARCH.md).

## Connect without a player

The toolkit can connect when the game RAM is initialized but no player object
or task is available, including title screens. Discovery still validates the
system pointer, readable RAM and plausible engine state; ambiguous no-player
candidates are rejected. Live memory and Story progress remain available, while
player-dependent features wait for a player. The no-player path has been checked
read-only on the recomp title screen; Project64 has synthetic coverage only.

## Story progress editing

In **Story progress**, select an individual flag or ownership word, choose its
desired state from the dropdown, and select **Apply state**. The dropdown starts
at the observed state. Flag edits preserve other bits in the same byte; inventory
words have Absent/Present options. Aggregate bank summaries remain read-only.
Edits compare against the displayed sample and verify readback; the game can
still change memory concurrently. `--read-only` disables editing. Editing flags
does not execute associated rewards, dialogues, scene transitions or cutscenes.

## Fortune Doll progress visibility

Live memory now shows the full **Fortune Doll progress (quarters)** word at
`0x8015C704`, and the separately annotated total at `0x8015C708`. The former
boolean 1/4 control now supports quarter states. Individual world-pickup flags
remain separate in Story progress. Event sessions only captures the 100-byte
saved-event bank; use Story progress's Fortune Dolls section or Event sessions → Advanced RAM comparison for outside-bank counters. [Three pickups and code evidence](docs/SILVER_FORTUNE_DOLLS.md).

## Value freezes

Open **Value freezes** and select **Keep health at current maximum** to replenish
the live health word from the current maximum every 10 ms (best effort) during ordinary
gameplay. It follows maximum-health upgrades without changing the maximum itself.
This is periodic replenishment, not guaranteed invulnerability.

For other values, enter a guest address in hex, a width of 1/2/4/8 bytes, and the
exact target hex, then **Freeze raw hex**. Or select a Live memory watch and use
**Freeze selected Live memory watch at its current value**. Live memory's existing
raw fields also have a Freeze button and a link to manage locks. The list shows
all raw targets; use **Stop selected** or **Stop all freezes** to release them.
Values are N64 big-endian hex; a raw freeze holds every bit in its byte range.
Raw and health freezes are available in writable sessions without an unlock checkbox.
Explicit `--read-only` mode blocks all freeze entry points.

Freezes start inactive and run in a separate thread, not the GUI refresh loop.
They stay only in memory for this connection and stop on
reconnect/disconnect, revoked permission, invalid data or a write/readback failure.
They pause during loading, scripts, menus and pause screens. Only changed targets
are written, with compare-before-write/readback checks; a failure clears all locks
without retry. This polling reduces visible overwrites, but it cannot make the
lock frame-perfect when the game overwrites a value more frequently. Up to 32 non-overlapping raw ranges are supported. Raw actor addresses
can be reused across rooms; they remain fixed addresses rather than tracked actors.
No saved configuration can automatically enable a freeze on launch.

Ghost Toys entrance flags are also mapped: `0x8015C63B` mask `04` is the right
torch, `08` the left torch, and `10` the independent door-unlocked latch. The user's
decimal sequences and original-code tests agree. [Evidence](docs/GHOST_TOYS_ENTRANCE.md).

[Congo/Lord research follow-up](docs/CONGO_LORD_OBSERVATIONS.md): the original
Lord-event initializer requires `0x8015C62D & 0x20` set and
`0x8015C61A & 0x80` clear. Both gates now appear in Story progress. Both gate conditions are now user-confirmed by manual bit tests, matching the
static trace. No independent assistant replay or matching-C promotion is claimed.

## v0.11.10: cross-room event comparisons

Event sessions now allows map, character and player/task pointers to differ between A/B/C captures. Capture A before post-boss NPC dialogue, finish the transition, then capture B after normal gameplay resumes. Each individual read must remain stable; reconnecting still requires a fresh A. The UI preserves every capture context and counts context-changing trials. No game writes are involved and existing v1 sessions remain readable. [Capture guide](docs/EVENT_SESSIONS.md).

The Congo `0x8015C61C & 0x10` label now records the user's timing correction: **Miracle Moon collected after Congo**, rather than boss defeated. The `0x8015C62E & 0x04` encounter-state meaning remains tentative.

## v0.11.9: event capture feedback and room labels

The completed Native menu calibration, Character cursor scan and Checkpoint compare tabs have been removed. Existing calibration profiles still support native-menu warps; checkpoints remain available on Dashboard. Older scanner instructions below are historical.

Event sessions now shows a UI clock, time since Capture A, and the native game-loop counter. Capturing B immediately reports raw changed bytes/bits, regardless of trial role. **Record trial** updates the ranked list; idle/control trials supply noise evidence and do not create candidates. Identical A/B values are explicitly reported.

Event sessions deliberately captures only the 100 saved event bytes at `0x8015C608..0x8015C66B`. It excludes clocks, temporary Bank A/B flags and the shadow buffer. Use **Event sessions → Advanced RAM comparison**, focused scope, for the system clock and saved/shadow regions; use wide scope for temporary Bank A/B flags. The separate **Saved / shadow** tab was removed because it duplicated the research workflows.

The entrance atlas had exposed 153 valid rooms missing from the old name catalog. Another 125 now have descriptive labels from [mn64rando's pinned room index](https://github.com/abyssonym/mn64rando/blob/9c580d03fe89354f79c3c83ba2e1bcf192f32577/tables/room_indexes.txt). Existing names are retained; 28 atlas rooms still show “Unidentified room” with their native menu index. Labels do not establish safe spawn coordinates or make unused rooms playable.

The Scene browser now loads entrance coordinates from your original USA ROM,
stages XYZ/heading before experimental reloads and checks the loaded player before
one position correction. Unique source-room routes or native defaults are selected;
ambiguous entrances require a choice. Checkpoint reloads stage their saved position.

The local atlas contains 888 records for 266 destination stages. Missing points
block the request instead of using stale/zero coordinates. Read-only and position
restore settings are respected. [Usage, coverage and native evidence](docs/ENTRANCE_WARPS.md).
No live warp test was performed; collision/camera/script behavior remains unverified.
Restart source via Run.bat; no executable was rebuilt.

# Goemon Speedrun Tools v0.11.7 — externally annotated story flags

Story progress now includes **37 additional mappings from existing mn64rando
research**, covering boss, recruitment, magic, weapon, priest and travel states.
Filter **external** to view them; each is explicitly labelled as an external
annotation with numeric ROM-reference leads, not locally gameplay-verified meaning.
Current catalog: 58 named flags plus four bank/inventory watches.

218 tests passed, with a live read-only recomp sample and visual filter check.
[External catalog provenance and examples](docs/EXTERNAL_FLAG_CATALOG.md).
Existing write/default behavior is unchanged; no executable was rebuilt.

# Goemon Speedrun Tools v0.11.6 — live story progress

The new **Story progress** tab shows mapped Benkei/Ushiwaka/Kihachi milestones,
known flag masks, raw values and evidence. It distinguishes training success,
recorded reward and actual Mini-Ebisu ownership, with advisory flag/inventory
discrepancies. Raw Bank A/B views retain separate labels and unknown lifecycle.
Named story flag rows are now grouped in Story progress instead of being repeated in Live Memory; Unlocks still provides item controls.

215 tests passed, with a successful live read-only recomp sample and visual Tk
check. [Panel guide and limitations](docs/STORY_PROGRESS.md). Existing unsafe
defaults are unchanged. Restart from this checkout; existing executables require
a rebuild to include the new panel.

# Matching C reconstruction

The [decompilation track](decomp/README.md) now includes **74 matching functions / 5,564 function bytes**
across flag-bank, system/byte-memory, save/resource and VM helper, assignment, resource and control routines.
The VM unit intentionally retains 20 unresolved functions as assembly; its host
comparator model is not counted as matching C. Most of the game remains unreconstructed.
Fresh baseline and C-replacement builds both match the complete
original decompressed US ROM byte-for-byte. Reproducible verification, synthetic
C tests and per-function result metadata are included; game data stays local.
The [whole-build inventory](decomp/INVENTORY.md) identifies 7,376 function entries:
87 matching C entries including 13 already upstream, and 7,289 still in assembly.
The count includes SDK/runtime code and is not proof of complete function discovery.
The [batch pipeline](decomp/BATCH_PIPELINE.md) now automates draft generation,
parallel byte probes and bounded search, with cached baseline verification for
reviewed batches. Probe candidates are excluded from the verified count.
This remains a partial decompilation, not a new release.

# Read-only ROM flag analysis

[The Benkei/Kihachi follow-up](docs/BENKEI_KIHACHI_TRACE.md) locates the later
dialogue condition and Kihachi's native initialization gate, inventories existing
research, and explains why whole-byte `0x2E` writes alter unrelated reward flags.

[The ROM tracing report](docs/ROM_FLAG_TRACE.md) documents verified original US
event-flag helpers, Benkei/Ushiwaka script checks and writes, and separate
minigame success, failure and ability-granted state. A new read-only
`python -m practice.rom_flag_trace` command indexes reference candidates from a
verified local decompressed ROM. It does not bundle game data or change the GUI.
Unreviewed reference patterns and external labels are not confirmed semantics.

# Goemon Speedrun Tools v0.11.5 — repeated event sessions

**Event sessions** records labelled event, idle and control A/B trials from the
100-byte persistent event block. Repeat an event from your own pre-event save,
then compare individual bits with supporting, conflicting and noisy trial evidence.
Optional C records per-bit reversions. Sessions save locally and can be reopened;
analysis runs in the background. No candidate is automatically confirmed or written.

Read-only capture/save/reopen smoke tests passed against both running Project64
and Goemon64Recomp. No new quest flag has been confirmed. See the
[step-by-step capture guide](docs/EVENT_SESSIONS.md).

# Goemon Speedrun Tools v0.11.4 — historical write-access defaults

At v0.11.4, game-memory editing and practice controls were enabled at startup.
The extra write-unlock checkbox that existed in this older release was removed.
Connecting and polling game memory do not perform any writes by themselves.

`Run.bat`, `python -m practice.toolkit` and the packaged entry point share these
defaults. Existing `--enable-*` flags remain accepted. Use `Run.bat --read-only`,
`python -m practice.toolkit --read-only`, or the executable's `--read-only` option
to disable game writes and automated game input. Read-only takes precedence over
all enable flags; the edit controls remain disabled in read-only mode.
Read-only sessions still support watches, captures and local report exports.

The legacy direct-warp prototype remains disabled. Existing action confirmations,
write validation and experimental reload limitations still apply. Project64
writes and checkpoint restores remain unverified. Existing executables must be
rebuilt to receive this change.

# Project64 connection (2026-11-02)

On Dashboard select `project64`, `recomp`, or `auto`, then **Connect to game**.
Run the US game in normal gameplay with a visible player. Automatic selection
requires one matching process; if both hosts are running, select one explicitly.
Multiple instances of the same host require `--pid`.

Read-only testing on Project64 3.0.1.5664 confirmed the existing guest addresses
for system/player pointers, character, map, resources and changing XYZ. Its RAM
is word-swapped and split across readable regions with different protections;
the scanner now joins adjacent readable regions without crossing inaccessible gaps.
The host RAM base is discovered each time, not hardcoded. Dynamic player pointers
can change on scene loads even when the addresses storing those pointers agree.

Project64 writes, warps, checkpoint restores and every quest-bit interpretation
remain unverified. No new flag semantics are established by a successful connection.
The original 8 MiB readable-range check remains: 4 MiB configurations are not
supported by this change. Restart the toolkit from this checkout to use it;
already-running copies and packaged executables are not updated automatically.

# Goemon Speedrun Tools v0.11.3 — storyline probes and pre-load character experiment

The **Unlocks** tab now exposes **read-only** Sasuke battery 2 post-cutscene completion (`0x8015C609 & 0x40`) near the top, alongside Ushiwaka progression **candidates** (`0x8015C60D & 0x10` start, `& 0x08` blue-fish hand-in). The first Sasuke battery (`& 0x20`) remains the only write-verified battery unlock. Completing Ushiwaka's blue-fish hand-in also reduced blue fish count at `0x8015C723` from 3 to 0. These event bits do not execute a cutscene.

**Scene browser now has NO automatic C-Down presses.** When an experimental 0x0C reload is requested, the selected character ID (`0x8015C5DC`, u32) is staged **before loading**, then the game may spawn its model using its ordinary area-entry loader. Both global and player-task character IDs are checked after loading. **This behaviour is experimental and has not been validated in a running Windows game**; the loader may override the ID, cause an inconsistent actor, or use the wrong entrance coordinates. If verification fails the tool only reports failure and will not attempt to repair the actor through simulated input. The observed native debug-menu pointer `0x800C7E60` is not modified and is only meaningful during highlighted native-menu entries; the user observed it later reading 128.

Local simulated-memory and Linux/Xvfb GUI tests: **171 passed**. Use disposable saves for experimental reloads.

---

# Goemon Speedrun Tools v0.11.2 — post-warp character selection and second battery flag

The Scene browser character dropdown now applies to **experimental 0x0C reloads**: once the map is playable, the toolkit uses ordinary C-Down to request the selected character, if that character is available in the current party, and verifies both global and per-task character IDs. This changes character **after loading**, not through the original debug-menu actor spawn path; the initial spawn and coordinates may still be incorrect. It never writes global character IDs, task pointers, or the observed debug-menu pointer. A failed automatic input allows a manual C-Down, with a bounded timeout and explicit failure reporting.

**Native cursor scan:** eight forward/reverse highlights match `0x800C7E60 = 0x8007BAD0 + 12*selected_character` while the original debug menu is open. This is a native *menu-entry pointer*, not an ID and not writable for gameplay character switching without further validation.

**Battery:** The second Sasuke battery event sets `0x8015C609` bit `0x40` **after its cutscene completes**, giving `0x20 -> 0x60`. Live Memory shows this as an *observed cutscene-completed bit*, read-only; the event-script trigger remains unknown.

- **F1** selects the **Live Memory** debug/hex editor tab when this toolkit has keyboard focus. It is not a global hotkey over the game.
- The Live Memory item rows show **Star, Moon, Flower and Snowflake**, consistent with the existing Unlocks controls.
- **State discovery** includes **Storyline event / quest flag** and **Item ownership only** A/B probes. Comparisons export `event_flag_changes` with per-byte set and cleared bits in the primary persistent event-flag block `0x8015C608..0x8015C66B` to help isolate Benkei's first conversation from Ushiwaka fish completion and Achilles' Heel ownership. These flags are not yet mapped.
- The experimental movement/speed-pulse **buttons have been removed**: manual testing produced only minor nudges, not a reliable speed effect. The task-relative field remains observed but semantically unverified.
- Cross-area checkpoint restores still stage-load the checkpoint's map and **then** restore saved XYZ/rotation/progression once gameplay is stable. The **Connect** scan stays on a background worker to avoid freezing Tk. Both features are Windows game-integration experiments, not full native savestates.
- Validated with **163 Python/Tk synthetic-memory tests** on Linux/Xvfb, not in-game Windows testing.

---

# Goemon Speedrun Tools v0.11.0 — cross-area checkpoint restore and responsive Connect

**Checkpoint restore now supports saved positions across areas (experimental).** Capture a checkpoint in stable gameplay as before. Restoring from another room first requests the saved map using the observed `0x800C7CA0` destination / game-state `0x0C` sequence. The toolkit waits for the saved map, normal gameplay, and a stable player before restoring the saved **X/Y/Z, rotation, character, inventory, progression flags and resources**. If the character differs it uses the existing native C-Down character-switch workflow before restoring the checkpoint. Same-map restores remain immediate; Cancel can abort a pending cross-area attempt. **Do not use this as a real savestate:** transient actors, cutscenes, physics and the camera are not captured. The experimental reload may still softlock; gameplay may subsequently reposition the player. Save backups are recommended.

**Connect remains responsive:** expensive RAM discovery and process opening now run off Tkinter's UI thread. The button is disabled while connecting; the UI shows a status message and remains interactive. An actual slow scan still takes as long as it takes, but no longer locks the application window.

**Testing:** 161 synthetic-memory/Python/Tk tests passed with Xvfb; Windows Goemon64Recomp live integration was not run in this environment.

---

# Goemon Speedrun Tools v0.10.9 — first Sasuke battery confirmed

**Confirmed:** Unlocks → Sasuke battery 1 collected changes only bit `0x20` at `0x8015C609` and preserves other event bits. Verified in-game: writing this bit before collecting the battery removed the pickup upon reload and unlocked the second part of the chain. The second-battery flag remains unmapped.

---

# Goemon Speedrun Tools v0.10.8 — experimental stage reload and movement probes

![Real application dashboard](docs/images/actual-dashboard.webp)

This US Goemon64Recomp desktop toolkit now includes **explicit, experimental** controls for a manually observed stage-reload warp and the suspected PlayerTask movement field. Both operate on live game memory and have **not been verified in this build on Windows**. Existing Live Memory watches, checkpoint tools, inventory unlocks and diagnostics remain available.

## Experimental controls (v0.10.8)

**Experimental warp (historical):** The original button required extra steps and was unverified. Current builds reload from the dashboard or Scene Browser by double-clicking the destination, staging its selected ROM entrance without extra confirmations. The inactive exit-flag route remains blocked. Collision, scripts and camera must still be checked in-game.

**Movement offset test (historical):** Earlier builds exposed PlayerTask movement probes at `task_ptr + 0x68`. These probe buttons were later removed after they failed to establish a reliable speed modifier.

**Manual 4-byte float test:** `00000000` = 0.0, `3F800000` = +1.0, `40800000` = +4.0, `C0800000` = −4.0. Entering `192` in the hex editor does *not* mean decimal float 192. The absolute pointer found during an earlier capture (`0x8016A0F8`) may change every scene; only the offset `+0x68` is stable by struct definition. Avoid 8-byte writes (which overwrite `+0x6C`).

**Known fields:** Weapon index `0x8015C607` uses 1/2/3 for all characters; `0x8015C574` reports map visibility 00/01 but manual writes open the map instead of closing it. `0x800C7A73` was rejected as a magic flag. Dragon travel unlocks and true internal velocity remain unresolved.

**Testing:** Source and GUI tests pass in Linux/Xvfb with simulated N64 memory; real Windows warp and speedup behaviour are still to be measured. Run `build/Build-Windows.cmd` on Windows for the standalone `.exe` or `Run.bat` to launch from source.

---

## Earlier development notes (historical; superseded where contradicted above)

## Custom live-memory watches (v0.10.5)

The **Live memory** tab now has **Name**, **Address** and **Type** inputs above the table, plus **Add watch** and **Remove selected watch** buttons. Add any guest address such as `0x8015C574` with `u8`, `u16`, `u32`, signed variants, `f32`, `f64` or raw eight-byte hex. Custom rows refresh with the regular memory table, support filtering by name or address, and are visibly labelled **Custom** rather than misrepresented as confirmed mappings. Double-click their Hex cell to edit in a writable session (the default). Custom watches are saved to `practice/custom_watches.json` (source) or `%LOCALAPPDATA%\GoemonSpeedrunTools\custom_watches.json` (packaged app), separate from the built-in address map.

The **State discovery** tab also has **Watch selected address**, which adds the selected candidate to Live memory in one click. Dynamic task pointers may change after changing character or stage, so watch addresses inside player tasks can become stale across loads.

**Map test correction (2026-11-02):** `0x8015C574` is **read** as `00` while hidden and `01` while visible, but **writing** `00`, `01` or other tested bytes opens the map rather than closes it. Built-in live watch available; no on/off write toggle is claimed.

**Equipped weapon (confirmed):** `0x8015C607` is a one-byte index, `01`/`02`/`03` across all four characters. The Live Memory tab now watches it; Writable sessions permit arbitrary hex writes. Out-of-range values produce unintended next-character weapon assets. Magic-active and internal player velocity remain unconfirmed.

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
- The packaged executable writes bookmarks, checkpoints, debug-menu profile and exported diagnostics under `%LOCALAPPDATA%\GoemonSpeedrunTools` to avoid PyInstaller's temporary directory.
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
- **Live Memory:** enable `separate write-unlock` to write any width-appropriate hex value, bypass mapped limits, or explicitly enter a guest N64 address and 1/2/4/8-byte value. The write checks old memory and verifies the result; arbitrary values can crash or corrupt game state. This does not provide a working warp.
- **Original sprites:** Sprites tab includes a link to the [referenced original sheet](https://www.spriters-resource.com/nintendo_64/mysticalninjastarringgoemon/asset/123088/) and retains the local PNG import workflow. Original copyright art is not committed to the public repository.

---

## Verified normal door transition (MACHI 353 → 351)

Observed 307 samples over 9.36 seconds on 2026-11-01. At 2715 ms, the pending destination changed **353 → 351**. At 3112 ms, the current map changed **353 → 351**, previous map changed **465 → 353**, and stage offset changed **3 → 1**. The measured gap was approximately **397 ms**. During all reported observations, top state remained **13**, game phase **1**, exit request **0**, and loading flag **0**. This does not imply those values never change within unobserved frames. A write to pending destination alone has not been established to initiate a valid area transition. Do not use the disabled v0.9.7 exit-bit warp trick.

## Live Memory tab

The tab now includes confirmed stage offset, previous map, pending destination, exit request and native menu pointer, alongside context-sensitive native category/gameplay submode. It refreshes while the native debug menu is open. Some transition-related fields are meaningful only under specific states; the UI labels distinguish these contexts.

**Double-click the Hex CELL** (third data column, labelled Hex) to open an editor. For resources and explicitly mapped inventory entries, enter a hexadecimal value (with optional `0x` prefix), review a before/after dialog, and confirm. The app checks the old value immediately before writing and verifies readback. Changes are in **canonical original N64 byte order** and appear in the diagnostic event log. They are not persisted as a game save. A changed value or in-flight game transition can prevent a write.

Game-state, map, pending destination, exit request, character, loading and menu-pointer addresses are **locked by default**. To edit them, deliberately tick the `separate write-unlock: allow editing game-state/transition/pointer fields` checkbox, then confirm the individual write. These fields are unsafe and **manual writes do not implement direct warp**; they can cause a return to title, softlock or crash. The editor does not make unsupported fields (e.g. dynamic position floats) editable. The `Run.bat` launcher opts into hex-edit capability, but the separate dangerous-address toggle resets every launch. The GUI does not write anything on a simple row selection.

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

Launch Goemon64Recomp into normal gameplay. Unzip this folder and double-click **`Run.bat`**, then connect. The launcher enables experimental tools by default. Keep a disposable save. Original `practice/checkpoints.json` and `practice/bookmarks.json` can be copied from earlier releases.

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
- Checkpoint and inspector functionality remains, including experimental cross-map restore (not a native savestate).

## Testing

```powershell
py -m unittest discover -s tests -v
```

The automated suite uses simulated N64 memory; it cannot validate the native debug-menu field hypotheses against a running game. Source and tests are provided and no ROM assets are included.
