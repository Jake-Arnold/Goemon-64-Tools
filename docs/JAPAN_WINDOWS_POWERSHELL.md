# Windows PowerShell — Japan-0 Toolkit testing

This is the native Windows equivalent of the previous Linux Bash instructions.
The helper is `scripts/test_japan_party.ps1`. It runs Python compile checks,
synthetic Japanese/USA memory tests, and actual Tk GUI smoke tests **inside your
normal Windows desktop session**. Bash, `xvfb-run`, WSL and `sudo` are not
required. The tests are synthetic and do not connect to the running emulator.

## Requirements

- 64-bit Windows and 64-bit Python 3 with `tkinter` installed; use `py -3`
  (Windows launcher) or `python`.
- `psutil` and any other dependencies required by this checkout. From repo root,
  `py -3 -m pip install psutil` if the module is missing.
- A local Git checkout of `Jake-Arnold/Goemon-64-Tools`. Run PowerShell in its
  root (the folder containing `practice` and `scripts`).

## Update the experimental branch and test

```powershell
git fetch origin chatgptweb/japan-controlled-party-writes
git switch --detach FETCH_HEAD
.\scripts\test_japan_party.ps1
```

The runner auto-selects `py -3` or `python`. To select an installed Python
executable explicitly, run `.\scripts\test_japan_party.ps1 -PythonCommand python`.

If local execution policy blocks the script, run one PowerShell invocation with
a process-only policy override:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test_japan_party.ps1
```

This does not persistently change the Windows user's execution policy.

## Launch the GUI

```powershell
py -3 -m practice.toolkit --game-version japan
```

For the two separately verified party-unlock buttons only, use the prior opt-in:

```powershell
py -3 -m practice.toolkit --game-version japan --enable-japan-party-writes
```

On the dashboard, select `mupen64plus`, **Verify ROM** using the exact Japan-0
retail ROM, then connect to its process PID. The region-specific raw RDRAM,
Japan Live custom watches, Value Search and Event Sessions → Advanced RAM
Comparison are separate from USA write controls. A full Mupen savestate is the
rollback point for the two party-write experiments.

## Windows support caveat

The shared `HostProcess` backend uses Win32 `OpenProcess`,
`ReadProcessMemory`, `WriteProcessMemory` and `VirtualQueryEx` on Windows.
The Japan-0 scanner and the guarded party writer call that backend through
`HostProcess`, so they are designed to have a native Windows code path.

**Not live-verified here:** Windows process detection for a given Mupen64Plus
distribution, discovery of its actual 8 MiB RAM buffer, its code-signature
matching and the native Windows GUI party-write workflow. The user previously
verified the Linux Mupen party-writing implementation, not this Windows
emulator/OS combination. Windows UAC/anti-cheat/process privilege boundaries
and emulator executable names can differ; failures must be reported rather
than forcing a guessed RAM base. This does not imply Japanese Project64
attachment works: this branch's Japanese connection targets Mupen64Plus only.

The live tests to repeat on Windows are described in
[`JAPAN_READONLY_VALUE_SEARCH.md`](JAPAN_READONLY_VALUE_SEARCH.md).

## Additional notes

- The current `scripts/test_japan_party.sh` remains available for Linux.
- `PROGRESS.md` and the parity checklist identify which changes have actually
  passed tests versus only having authored test coverage.
- Use `py -3` on Windows where `python3` may not be on PATH.
