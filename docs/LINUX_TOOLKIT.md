# Native Linux Goemon toolkit (experimental)

The Python/Tk toolkit can run directly on Linux and access native Goemon64Recompiled process memory, without Wine. The game binary is not supplied or built by the toolkit.

## Ubuntu installation

```bash
sudo apt install python3-venv python3-tk
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m practice.toolkit --read-only
```

In **Connection**, select **Launch native Linux recomp**, choose a native, executable Goemon64Recompiled binary, then **Connect to game** after the game starts. The toolkit launches the game as its child so Linux ptrace permissions usually permit memory reads. Or run a standalone native game separately and connect using the PID or auto-discovery. The game process name must contain `goemon64recomp` for auto-detection.

## Details and limitations

- The host process adapter reads `/proc/<pid>/maps` and uses `process_vm_readv`. In environments where the syscall returns `ENOSYS`, it falls back to `/proc/<pid>/mem` using Linux's normal process permissions. No root escalation or ptrace security settings are changed.
- The existing RDRAM discovery verifies original-USA game pointers, player/state fields, mapping bounds and endian mode. The Linux native recomp must expose a compatible memory layout; this has **not yet been tested against a live Linux game**.
- **Linux defaults to read-only**. Reads, route observation, checkpoint capture and VM diagnostics do not modify the game. `--linux-enable-writes` explicitly enables experimental memory writes; `--read-only` overrides it. Use disposable saves.
- Native Linux C-Down and N64 A keyboard injection is available on an **X11/Xorg session** with `xdotool` (`sudo apt install xdotool`). The toolkit checks the visible game window's PID, focuses it, verifies the focused PID and balances keydown/keyup. A Wayland desktop is **not** supported by this X11 adapter: it fails closed instead of sending keys to an unverified window. Manual in-game keyboard/controller input still works.
- Native Linux live speed requests (1x–4x) use a user-owned POSIX shared-memory channel with magic/version/PID verification and host acknowledgement. **Only a separately built speed-patched native recomp exposes this channel.** Stock Linux builds cannot change their host clock when the toolkit requests speed. Windows named memory mappings remain unchanged.
- The speed patch is provided in `speed/runtime_channel.inc` and installed by `python -m speed.prepare_live_runtime` into an **isolated runtime checkout already prepared by** `python -m speed.prepare_runtime`; the runtime checkout must be the pinned revision documented in `speed/prepare_runtime.py`. Rebuilding and linking the native Goemon64Recompiled executable against that patched runtime is necessary. These source-preparation scripts do not build the game. Preserve stock binaries, ROMs and saves; use isolated copies for tests.
- Native speed IPC has been tested with a compiled synthetic Linux host using a 4x request and applied-rate acknowledgement; real gameplay, audio, VI scheduling and scene transitions remain unverified.
- Native Flatpak sandbox boundaries may prevent external process-memory access. Prefer a standalone native build of the game under the same user. If access is denied, check the process owner and `kernel.yama.ptrace_scope`; do not weaken global ptrace security just to use the toolkit.
- An explicit `--pid` or `--base 0x...` can select a process or known host RAM address. Core RDRAM snapshot validation still rejects incompatible mappings.

## Script diagnostics

The Live memory inspector now exposes original-ROM-derived VM globals: script cursor (`0x80077858`), VM state (`0x801C77E0`), resource ID (`0x801C78E8`), and signed pause byte (`0x801C78FC`). These are read-only and use original access widths; labels describing their purpose remain inferred.

## Verification status

The native Linux process adapter was tested against a disposable child process. The new X11 input path has subprocess-mocked fail-closed tests; native speed IPC was compiled and checked against a synthetic C++ host with 1x-to-4x acknowledgement. Actual native game input, full GUI and runtime speed behaviour remain unverified. No game ROM is bundled or needed to start the toolkit.
