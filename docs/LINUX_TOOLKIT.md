# Native Linux Goemon toolkit (experimental)

The Python/Tk toolkit can run directly on Linux and access native Goemon64Recompiled process memory, without Wine. The game binary is not supplied or built by the toolkit.

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
