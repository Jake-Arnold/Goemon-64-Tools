# Japanese Goemon (Japan-0) — Windows Project64 3.0 support

**Status:** Implemented and pushed on `chatgptweb/japan-controlled-party-writes`. The synthetic regression tests are authored, but **no real Windows Project64 3.0 attach, party write, or savestate has been executed in this GitHub-connector session**. Previous successful Sasuke/Yae write testing was on Linux Mupen64Plus and is not evidence of a Windows PJ64 test.

## Clone the private repository on Windows

Open **PowerShell**, authenticated for the private GitHub repository:

```powershell
Set-Location $HOME
git clone --branch chatgptweb/japan-controlled-party-writes https://github.com/Jake-Arnold/Goemon-64-Tools.git
Set-Location .\Goemon-64-Tools
git status
```

If already cloned, run `git pull --ff-only origin chatgptweb/japan-controlled-party-writes` in the repo root instead of cloning again. The GitHub CLI `gh auth login` is an alternative for Git authentication when requested by Git.

## Install and test

Use a **64-bit Windows Python with Tkinter**. On Windows, `py -3` selects the Python 3 launcher:

```powershell
py -3 -m pip install psutil
.\scripts\test_japan_party.ps1
```

This runs `compileall`, previous Japanese party and read-only memory tests, Project64 4/8 MiB synthetic attach tests, and USA regression/Tk tests. A passing test suite **does not** establish live Project64 compatibility.

If local execution policy blocks PowerShell scripts, without changing your account's permanent policy:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test_japan_party.ps1
```

## Running Project64

1. Start Project64 3.0 with the **Japan revision 0** Goemon ROM, and enter ordinary gameplay. The game ROM needs to match the exact SHA-1-verified Japanese ROM you select in the toolkit. **USA RAM symbols must never be used for this Japanese ROM.**
2. Identify the emulator PID:

   ```powershell
   Get-Process Project64 | Select-Object Id, ProcessName, Path
   ```

3. Start the toolkit:

   ```powershell
   py -3 -m practice.toolkit --game-version japan
   ```

4. On the Dashboard select **Japan - Ganbare Goemon**, **Verify ROM** and choose the exact Japanese ROM file. Select **project64** as the target, enter the PID shown by `Get-Process`, and select **Connect to game**.
5. The toolkit now checks the real `Project64.exe` process identity, scans readable Win32 process memory for **three separate Japanese game-code signatures**, validates the candidate base and byte order, rejects an identified ROM-copy decoy, and determines whether the RDRAM extent is **4 or 8 MiB**. Wrong ROM, wrong process, or ambiguous base fails closed; it never guesses or writes a character-index value.
6. Japan Live, Value Search, typed custom watches and Event Sessions → Advanced RAM Comparison use the verified Japanese reader. A 4 MiB Project64 mapping restricts Value Search and Wide A/B/C to the available 4 MiB; the project no longer blindly reads 8 MiB in that case.

### Optional: fixed RDRAM address

Project64's optional `[default]` config key `Fixed Rdram Address=536870912` requests host RDRAM base `0x20000000`. It is **not** required for automatic discovery. If it is already enabled, you can try this command to avoid a long scan:

```powershell
py -3 -m practice.toolkit --game-version japan --base 0x20000000
```

Still select **project64** and **Verify ROM** in the UI. The supplied address must still satisfy all three executable signatures and the RDRAM size check; the flag is not permission to reinterpret arbitrary process memory. Project64 may ignore the setting if the requested allocation is unavailable, so never assume `0x20000000` is correct from the config alone.

The normal Project64 3.0 configuration location may be under its installation's `Config\Project64.cfg` directory, for example `C:\Program Files (x86)\Project64 3.0\Config\Project64.cfg`. Restart Project64 after changing the setting. Config file location can differ by installation.

### Party unlocks (optional writes)

Only the existing **Sasuke 0→1** flag `0x80161E97` and **Yae 0→1** flag `0x80161E9B` are allowed, and only when explicitly opted in:

```powershell
py -3 -m practice.toolkit --game-version japan --enable-japan-party-writes
```

The toolkit reopens `Project64.exe` for a *single* writable operation only after a confirmation dialog, checks the correct target PID, repeats the same Japanese ROM/base/endian and 4/8 MiB validation, compares read-only and writable handles, reads the result, and closes the writable handle. It **does not write** character-index `0x80161DCC`. Make a complete **Project64 savestate** before testing; use the game's normal C-Down switch afterward.

Use the existing native emulator savestate controls with the Project64 target; the toolkit sends emulator F5/F7 requests and cannot independently guarantee that a savestate completed. Restoring your own savestate is the recovery plan.

## Evidence and troubleshooting

- **Connection failure:** confirm process `Project64.exe`, Japan-0 ROM revision, PID, Python/Project64 permissions and that the game has finished booting. Avoid asking the toolkit to attach to the debugger window as another PID.
- **No signatures:** remove an obsolete `--base` override and retry automatic discovery, or confirm the PJ64 debugger at `Debugger → View Memory` shows Japanese `0x80000450` guest code, then compare with the verified ROM. An arbitrary USA RAM offset cannot repair a mismatched ROM.
- **Multiple candidates:** use the Dashboard's explicit base selector for the matching PID. Live-changing field observations determine which buffer is active; static code signatures alone cannot prove a duplicate copy is the live game state.
- **First live read test:** observe Japanese Ryo at `0x80161DDA` (u16) and the read-only character-index word `0x80161DCC`, switch characters normally, and compare before and after. Validate Sasuke=2/Yae=3 on-screen and via the actual index value before treating those numbers as confirmed.
- **Project64 memory size:** the ROM settings may choose 4 MiB or 8 MiB. Both mappings are now accepted if verified; 8 MiB is not forced.
- **Windows process permission failures:** run the toolkit at the same integrity level as the emulator; do not disable Windows security protections. Report the exact error before changing any permissions or RAM settings.
- **USA branch unaffected:** when USA is selected, existing Project64 attachment and USA-only editors remain separately gated. Japanese party writes are never exposed through those USA editors.
- **What is still unverified:** live PJ64 3.0 RAM discovery, fresh Japan UI tests on Windows, Project64 slot save/load and both Project64-specific party write buttons. These require an actual Windows/PJ64 session and are not established by the authored synthetic tests.

Sources: the [Project64 debugger setup and optional fixed RDRAM address](https://hack64.net/docs/pj64d/), the [Project64 debugger's RDRAM address range](https://github.com/project64/project64/blob/develop/Source/Project64/UserInterface/Debugger/Debugger-ViewMemory.cpp), and [Project64 memory-size settings](https://mib64.github.io/manual/app-game-settings.html).
