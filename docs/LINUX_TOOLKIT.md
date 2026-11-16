# Native Linux Goemon toolkit (experimental)

The Python/Tk toolkit can run directly on Linux and access native Goemon64Recompiled process memory, without Wine. The game binary is not supplied or built by the toolkit.

## Japan auto-connect and unrestricted original debug (v0.11.30)

In the Japan region, **Connection target defaults to Auto**. Leave PID blank and Japanese RAM base on `Auto (detect)`; click **Connect to game**. The toolkit inventories native Goemon64Recomp, Mupen64Plus and (on Windows) Project64 candidate processes, then checks each against the originally verified Japan ROM using three separate 64-byte game-code fingerprints. Matching copies of the ROM are explicitly rejected. It reads Japanese engine/scene state for plausibility and automatically chooses big, 32-bit word-swapped or 16-bit byte-swapped RDRAM. It does not infer Japan from executable names alone, and it refuses to pick between multiple separately verified processes.

A successful executable/backend/layout may be cached at `~/.config/GoemonSpeedrunTools/japan-connection-hints.json` (subject to XDG_CONFIG_HOME, Windows LocalAppData) as a **hint**, not proof. The exact live process signatures and RAM size/state are checked on every new Connect; a failed hint triggers full discovery. After a successful Auto attachment the toolkit records the PID's process-creation identity. If that process exits or its PID is reused, it closes the stale RDRAM handle and retries verified auto detection with a ten-second minimum interval while the game is unavailable. Explicit backend/manual attachments are not silently replaced. Connect also performs a fresh discovery at any time. Selecting a PID, backend or RAM candidate explicitly remains possible for resolving ambiguity. Windows Project64 is not supported by the Linux process access path.

The original **Open original debug menu (any state)** control only changes Japanese guest engine mode `0x800CD284` to `0x0A` if different; no confirmation, cutscene/loading/character guard, menu stage/entrance write or simulated input. It requires a verified Japanese RAM mapping and write-enabled connection. It is deliberately **not** the Scene Browser instant `0x0C` warp operation.

The Scene Browser still stages the exact shared USA entrance but requires a confirmed post-load scene, transition-clear state and three stable, expected character ID readings before reporting scene ready. For Ebisumaru, Sasuke and Yae the Japanese actor/task pointers are not yet independently validated and the app will not claim verified playable actor initialization. Japanese Goemon post-load XYZ writes are restricted to the original proven **Oedo South (0x161)** vector; other rooms use native staged entrance placement with *no speculative post-load XYZ write*.

Known independent native-game crash: **Gourmet Sub 2F Bazooka Room, scene 0x081**, tracked separately in `docs/JAPAN_NATIVE_SCENE_081_CRASH.md` and not attributed to toolkit warp logic.

**Verification status:** Synthetic unit tests authored; native Ubuntu and real-game smoke checks still required. Do not equate code-signature matches or a scene ID with live actor readiness.

## Checked-in complete entrance coordinates (v0.11.26)

The actual original-USA numeric entrance table supplied by the user has now been **committed** at `practice/data/entrance-coordinates.json`. It is loaded automatically by both USA and Japan. **No ROM extraction, local cache or original-USA ROM file is needed** to access the covered entrance records in any new checkout.

Verified dataset: **333 indexed scenes, 888 entrances for 266 destinations** (592 exits, 266 defaults, 16 flute, 14 save records). Different entrances within a scene retain separate IDs, X/Y/Z, heading and mode. Oedo South (`0x161`) has the original-USA native default and source-scene 351 entry both at `(-289, 0, -167)`, heading 256, mode 16; the old fallback was corrected accordingly.

After `git pull --ff-only`, launch `bash Run-Linux.sh`, choose Japan or USA, open Scene Browser and select the destination/entrance. The entrance header should identify **repository** as the coordinate source. Unmapped scenes still require validated data rather than invented coordinates. A valid per-user or old checkout cache is used only if the checked-in JSON is absent/corrupt. The v0.11.25 instructions to extract and upload a first copy are now historical.

The JSON has been locally checked and freshly fetched from GitHub; the full toolkit test suite and native Japanese in-game warp remain outstanding. Run `bash scripts/test_japan_party.sh` for the new atlas regression.

## Repository-bundled entrance atlas (v0.11.25)

The next stable source of scene warp coordinates is the **version-controlled, checked-in numeric table** `practice/data/entrance-coordinates.json`. Both USA and Japan load it automatically, without a ROM or per-user setup. Each destination scene may contain multiple entrances (source scene, ID, XYZ, heading, mode), all of which remain distinct.

**The actual full table has not been supplied or committed yet.** To generate it once on Ubuntu using your own original USA ROM:

```bash
cd ~/Desktop/Goemon-64-Tools-JP-Recomp
git pull --ff-only
python3 -m practice.entrances \
  --rom "/path/to/original-usa.z64" \
  --output "/tmp/goemon-entrance-coordinates.json"
```

Upload **only** `/tmp/goemon-entrance-coordinates.json`, not the ROM. After validating the extractor's ROM SHA1/schema/checksum and reviewing the numeric data, that JSON can be committed to `practice/data/entrance-coordinates.json`. It will be available to both regional warps with `git pull` and will take precedence over all locally cached coordinate data.

Until the JSON is actually committed, the toolkit loads an existing validated user atlas from XDG_CONFIG_HOME, migrates legacy `practice/entrances.json` where available, and retains the single observed Oedo South position as a no-ROM fallback. The code refuses guessed positions in scenes without any recorded entrance. For the reviewed schema and extraction steps, see `practice/data/README.md`.

## Fixed entrance coordinates without a ROM at launch (v0.11.24)

Both USA and Japanese Scene Browsers now consult a **persistent entrance-coordinate table** keyed by scene and individual entrance ID. The full original-USA ROM-derived table is stored under `~/.config/GoemonSpeedrunTools/entrance-coordinates.json` on Ubuntu (using XDG_CONFIG_HOME if set), **outside** the git checkout. The toolkit loads it automatically every launch. Any validated `practice/entrances.json` created by an older version is migrated on first launch, so changing the toolkit checkout does not lose already extracted coordinates. The original ROM can be removed after a successful one-time import, and does not need to be opened again for regular warps.

A small built-in static table also supplies the user-observed **Oedo Town South, scene 0x161 (353), Goemon XYZ (-289, 0, -167)** with no ROM or cache at all. Its heading/mode defaults have not been confirmed from the original USA entrance record. Verified ROM-derived rows take precedence over that fallback. Other destinations are only available without the ROM when their numeric entrance records already exist in the persistent cache.

**Scene ID alone is not a unique position:** a room can have several entries with different XYZ, heading and mode. The existing shared entrance picker distinguishes entrances and still prefers a unique source-scene route or default; it does not arbitrarily pick between conflicting positions. Japan and USA both use whichever exact recorded entrance is selected.

When data is missing for a room, **Load original USA ROM** once in Scene Browser. After the numeric records are extracted, future USA/Japanese warps use the same cached values automatically. Only coordinates and functional scene/entrance metadata are stored; the ROM is never copied into this cache.

## Identical USA and Japanese scene warp coordinates (v0.11.23)

**Both regions use the original-USA entrance atlas**. In the unified toolkit's **Scene Browser**, the exact same **Destination entrance** selector and **Load original USA ROM** button appear for USA and Japan. The toolkit automatically loads the previously cached original-USA entrance atlas from `practice/entrances.json` if available. If not, load your original USA ROM using that button. This is entrance-data extraction only; the current live Japanese game still connects to its own separately verified Japanese ROM and memory backend.

Select a destination scene and then choose **the exact same entrance** from the dropdown in either region. Automatic selection uses a unique source-room entrance when known (the current Japanese room is read from `0x800CD2A2`) or the same native default fallback used by USA. If entrance data is missing or ambiguous, the toolkit refuses the warp until the user selects an entry; there are no scene-ID-only Japanese shortcuts.

For either region, the selected `Spawn.pending_bytes()` encodes the exact same `scene/mode/X/Y/Z/heading` 12-byte payload, then region-specific native 0x0C reload requests it. USA performs a guarded one-shot post-load XYZ placement. Japanese native Goemon gameplay now likewise writes the same original-USA entrance XYZ as 3 guest float32 coordinates at `0x80151B10` only once if the loaded position differs, after verifying the correct destination, Goemon character and stable gameplay, and re-opening the verified native writable handle. The status then reports requested versus actual XYZ, not merely a scene-ID match.

The old optional per-Japanese-room coordinate capture registry remains historical research metadata, **not an override** of the original-USA entrance choices. The separate capture button has been hidden. Japanese Yae/Sasuke/Ebisumaru post-load placement is *not* forced through the Goemon-only static XYZ address; the common 12-byte entrance staging is still performed. Collision, heading, camera and cross-region map equivalence remain live-test questions.

After pulling v0.11.23, run `bash scripts/test_japan_party.sh` and confirm one known room's selected USA entrance yields the requested XYZ in the Japanese recomp. The suite was authored but has not been executed via the GitHub connector. Back up your game save before testing a scene warp.

## Japanese warp XYZ capture and destination comparison (v0.11.22)

Previous native Japanese instant warps had an overlooked bug: the optional `self.entrance_atlas` was never initialized, so the controller always sent **only the 2-byte map ID** instead of the 12-byte destination/mode/XYZ/heading record. A scene ID that loads successfully is not evidence of correct destination XYZ.

To stage Japanese destination coordinates reliably *from your own gameplay*, first visit a room normally as Goemon, connect with the unified toolkit, and choose **Scene Browser → Record CURRENT loaded Japanese room XYZ (not selected scene)**. The toolkit saves that current map and observed float32 XYZ under `~/.config/GoemonSpeedrunTools/japan-warp-spawns.json`. The capture performs no RAM writes and is stored per-scene for later launches. It attempts to read heading/mode from a matching actual native pending entrance record; if this cannot be validated, it uses explicitly **experimental** default heading/mode (`0`/`0x10`), not a claimed original Japanese spawn.

Later warps into that recorded room stage the full native entrance record before `0x0C`. The existing user-tested Oedo South position `(-289, 0, -167)` is also an experimental preset. For other unrecorded rooms, the game still receives only a scene ID; the status states **NO DESTINATION XYZ WAS STAGED**, not “position verified”. After each loaded destination becomes stable, the toolkit compares actual Japanese float32 XYZ with the requested position and reports any 3D difference greater than 16 units as **SPAWN MISMATCH**. It clears old freeze locks before an actual reload to prevent stale XYZ writes from the previous scene.

There is no implicit reuse of USA ROM entrance coordinates and no uncontrolled post-load XYZ write. An approximate match is still not proof of stable collision or gameplay. The Linux/Python tests for this feature are synthetic and **not yet run against a live Japanese recomp**.

## Native Japanese recomp write controls (v0.11.21)

Earlier v0.11.20 builds could attach to the native Japanese recomp and display values, but left write buttons grey because several Japanese UI eligibility checks recognized only Project64/Mupen64Plus. This is fixed in v0.11.21: the verified native `recomp` backend is eligible for mapped Unlocks, Japanese Story Progress inventory edits, Goemon XYZ experiments, native debug-menu entry, Live Memory right-click hex edits, direct **Write raw hex**, and fixed-address freezes. The raw editor uses Japanese-specific `write_japan_raw_bytes` with expected-byte comparison and per-write RDRAM/ROM/PID verification.

These controls **do not** require an extra write toggle or CLI flag. To use the updated UI, `git pull --ff-only`, close the old toolkit window, start `bash Run-Linux.sh`, select **Japan** in the Dashboard, and connect to the native Japanese recomp. For end-to-end validation, run `bash scripts/test_japan_party.sh` and test a single known Japanese inventory byte after backing up the game save. The regression suite includes `tests.test_japan_recomp_write_ui` (synthetic Tk and memory only).

**USA-only operations remain intentionally disabled on Japan:** God Mode/task-pointer/max-health freeze, enemy pass-through, unverified Japanese story event bits and complete recomp savestates. Their Japanese guest layouts or runtime support have not been established. Successful attachment and an enabled button do not by themselves establish that a live process memory write was permitted or acted on by the game.

## Ubuntu Dock cog icon correction (v0.11.20)

The v0.11.19 launcher had a real GNOME identity mismatch: `Tk(className="GoemonPracticeToolkit")` actually exposes **`WM_CLASS = "goemonPracticeToolkit", "Goemonpracticetoolkit"`** on Tk 8.6/X11, but the installed `.desktop` file advertised `StartupWMClass=GoemonPracticeToolkit`. Case matters.

v0.11.20 gives the Tk window a lowercase class-name seed (`goemon-practice-toolkit`), yielding `WM_CLASS = "goemon-practice-toolkit", "Goemon-practice-toolkit"` in a real Xvfb/X11 probe. The installer now sets `StartupWMClass=goemon-practice-toolkit` and the desktop-file basename is `goemon-practice-toolkit.desktop`. These three identities agree.

After pulling the new branch, **close existing toolkit windows** and rerun:

```bash
python3 scripts/install_linux_launcher.py
bash Run-Linux.sh
```

To verify exact runtime identity while the toolkit window is visible, run `xprop WM_CLASS` (install `x11-utils` if absent), then click the actual toolkit window. The first quoted value must be `goemon-practice-toolkit`. Unpin the old anonymous cog entry, launch the registered **Goemon Practice Toolkit** application from the Ubuntu app grid, and pin that running application instead. If GNOME retains an old launcher association, log out and back in before retrying. On GNOME's Wayland session, Tk may run as XWayland and still report an X11 WM_CLASS.

## Unified Ubuntu application launcher (v0.11.19)

This single launcher works for **USA and Japan-0**. There is no region-specific CLI startup or read-only default. Writes, freezes, unlock controls and supported practice actions are enabled on both regional dashboards by default; selecting a region merely chooses the correct memory interpretation and runtime backend.

From the toolkit checkout:

```bash
# One-time setup for Ubuntu; creates a .desktop app and installs our existing logo.
python3 scripts/install_linux_launcher.py

# Launch without choosing a region in the terminal.
bash Run-Linux.sh
```

The launcher uses the checkout's `.venv/bin/python` if available, otherwise the system `python3`. The GUI remembers the last selected USA/Japan region at `~/.config/GoemonSpeedrunTools/launcher-preferences.json` (or XDG_CONFIG_HOME). To switch regions, use **Dashboard → Game version**; reconnect to the appropriate backend. When selecting Japan from the default auto target, the toolkit selects `recomp`; Mupen64Plus/Project64 remain available in the target selector.

The installer copies the existing `assets/goemon_tools_logo.png` to the user XDG icon directory and writes `~/.local/share/applications/goemon-practice-toolkit.desktop` (or XDG_DATA_HOME). It uses **StartupWMClass=goemon-practice-toolkit**, matching Tk's verified X11 WM_CLASS instance, which allows GNOME Shell/Ubuntu Dock to associate the window with the correct logo instead of the generic settings cog. Open **Goemon Practice Toolkit** from the Ubuntu application grid and pin it to the dock. If an older generic icon was pinned, unpin it and pin this registered application. No root/sudo required. Repeat installation only if the toolkit checkout moves; the installed app points at that directory.

This changes only the desktop application identity and user configuration. It does not change the game ROM, native recomp, RDRAM backend or Linux process security settings.

## Japanese native recomp (v0.11.18 experimental)

The native Japanese PC port is developed on `Jake-Arnold/Goemon64Recomp` branch `feature/japan-native-recomp`. The toolkit does **not** build the game. The user reports successful connection to their working Japanese native Linux recomp, but other gameplay writes and dock behavior still require direct testing. Unlike Mupen64Plus, native recompilation does not provide complete emulator savestates.

From a clean toolkit checkout with the dependencies below installed:

```bash
bash Run-Linux.sh
```

In Dashboard → Connection, select **Japan — Ganbare Goemon**, verify the exact original Japanese revision-0 retail ROM, set connection target **recomp**, provide the native game's PID (or use **Launch native Linux recomp**), and press **Connect to game** after the ROM has booted. Reconnect if the native game restarts. Other instances of the USA and Japanese executable may have the same name; with multiple instances, specify the correct PID.

Connection uses the **same Japanese guest-memory fields** as the emulator and retains ROM verification, endian detection, reject-ROM-copy checks and fail-closed ambiguity handling. It requires the Japanese native executable to preserve three original main-code fingerprints at the usual guest RDRAM offsets. If this developing port omits original code from RDRAM, the toolkit will reject attachment instead of silently scanning based on USA offsets. Native recomp compatibility is not guaranteed until that runtime detail is established with a live game.

Japanese unlock edits, Live Memory writes/freezes and guarded `0x0C` scene reload are already enabled by default once a verified writable connection is established. Every native recomp writer revalidates the PID, Japanese ROM fingerprints and guest mapping. Avoid treating successful readback as proof of a safe gameplay state; make an independent backup of the game save first.

Run synthetic tests (no live game writes):

```bash
bash scripts/test_japan_party.sh
```

**Version discipline:** `practice/version.py` controls the title/header. Increase the patch version for every toolkit release and keep README/PROGRESS in sync.

## Ubuntu installation

```bash
sudo apt install python3-venv python3-tk
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
bash Run-Linux.sh
```

In **Connection**, enter the PID of an already-running native Goemon64Recompiled game and select **Connect to game**. The toolkit attaches directly when Linux permits it; there is no need to launch the game through the toolkit. Auto-detection also works if the executable name contains `goemon64recomp`. The **Launch native Linux recomp** button remains available.

On Ubuntu, a separately launched game is often **not a child of the toolkit**, so the default kernel Yama policy (`kernel.yama.ptrace_scope=1`) may reject process memory reads even with the correct PID. To permit an external PID, use **Permit connection to existing Linux PID**. After a warning, the toolkit requests administrator authorization via the installed `pkexec` and `sysctl` utilities to set the *runtime-only* `kernel.yama.ptrace_scope=0`. This weakens process inspection isolation for all same-user programs while active; it is **not** scoped to the game. **Restore original PID protection** reverses the setting recorded in this toolkit session. Reboot normally restores the machine's configured value. This is never done automatically during Connect, and it does not permanently write sysctl configuration. If authorization fails or polkit is absent, adjust ptrace permissions manually or continue launching the game as a toolkit child. Different process owners and Flatpak sandboxes may still prevent connection.

## Details and limitations

- The host process adapter reads `/proc/<pid>/maps` and uses `process_vm_readv`. In environments where the syscall returns `ENOSYS`, it falls back to `/proc/<pid>/mem` using Linux's normal process permissions. No root escalation or ptrace security settings are changed.
- The existing RDRAM discovery verifies original-USA game pointers, player/state fields, mapping bounds and endian mode. The Linux native recomp must expose a compatible memory layout; this has **not yet been tested against a live Linux game**.
- **Linux and Windows now default to write-enabled practice controls**. Reading and connecting do not write game memory. Memory editing, freezes and scene reloads no longer require a separate unlock checkbox. `--read-only` explicitly disables game-memory writes and input. The old `--linux-enable-writes` option remains accepted but is unnecessary. Use disposable saves for experiments.
- Native Linux C-Down and N64 A keyboard injection is available on an **X11/Xorg session** with `xdotool` (`sudo apt install xdotool`). The toolkit checks the visible game window's PID, focuses it, verifies the focused PID and balances keydown/keyup. A Wayland desktop is **not** supported by this X11 adapter: it fails closed instead of sending keys to an unverified window. Manual in-game keyboard/controller input still works.
- Native Linux live speed requests (1x–4x) use a user-owned POSIX shared-memory channel with magic/version/PID verification and host acknowledgement. **Only a separately built speed-patched native recomp exposes this channel.** Stock Linux builds cannot change their host clock when the toolkit requests speed. Windows named memory mappings remain unchanged.
- The speed patch is provided in `speed/runtime_channel.inc` and installed by `python -m speed.prepare_live_runtime` into an **isolated runtime checkout already prepared by** `python -m speed.prepare_runtime`; the runtime checkout must be the pinned revision documented in `speed/prepare_runtime.py`. Rebuilding and linking the native Goemon64Recompiled executable against that patched runtime is necessary. These source-preparation scripts do not build the game. Preserve stock binaries, ROMs and saves; use isolated copies for tests.
- Native speed IPC has been tested with a compiled synthetic Linux host using a 4x request and applied-rate acknowledgement; real gameplay, audio, VI scheduling and scene transitions remain unverified.
- Native Flatpak sandbox boundaries may prevent external process-memory access. Prefer a standalone native build of the game under the same user. Inspect process ownership and `kernel.yama.ptrace_scope` if access is denied. The optional OS permission button intentionally relaxes global same-user ptrace isolation until restored, and should be used only if that trade-off is acceptable.
- An explicit `--pid` or `--base 0x...` can select a process or known host RAM address. Core RDRAM snapshot validation still rejects incompatible mappings.

## Script diagnostics

The Live memory inspector now exposes original-ROM-derived VM globals: script cursor (`0x80077858`), VM state (`0x801C77E0`), resource ID (`0x801C78E8`), and signed pause byte (`0x801C78FC`). These are read-only and use original access widths; labels describing their purpose remain inferred.

## Verification status

The native Linux process adapter was tested against a disposable child process. The new X11 input path has subprocess-mocked fail-closed tests; native speed IPC was compiled and checked against a synthetic C++ host with 1x-to-4x acknowledgement. Actual native game input, full GUI and runtime speed behaviour remain unverified. No game ROM is bundled or needed to start the toolkit.
