# Experimental native Mupen64Plus Frame Inspector

The native research frontend runs the Mupen64Plus core in a **separate child process on its main thread**, leaving Tk in the parent. It launches its own session; it does not attach a stock emulator already running or use Windows/Linux external process-memory APIs. On Linux source mode, open the main toolkit **Frame Inspector → Mupen64Plus (native)**. The Dashboard **Advanced connection → Open native Mupen64Plus Frame Inspector** shortcut selects this same embedded page. Switching between backend pages or other toolkit tabs leaves the native session and traces intact. Its external attachment backend is unchanged; other toolkit tabs are not routed to the native session. The native frontend requires a Mupen64Plus 2.6.0 core (or another 2.x core advertising debugger support), matching native graphics/audio/RSP plugins, data files, Python 3 with Tk, and a C11 compiler for the scripted input plugin. No original game files are included. Use only your own original USA or Japan retail revision-0 ROM.

## macOS (source mode; standalone launch retained)

Install Xcode command line tools (`xcode-select --install`) if needed. With Homebrew installed, install Mupen64Plus and Python/Tk for your chosen Python version. The packaged 2.6.0 core can use the documented RDRAM pointer API without the optional debugger. Other 2.x releases must advertise debugger capability for typed reads. CPU breakpoints will require a `DEBUGGER=1` build in a future implementation. Do not disable macOS security protections. Match architectures (arm64 or x86_64) of Python, core and all plugins. Locate the installed core, plugins, data directory and SDK header `m64p_plugin.h` using `brew --prefix mupen64plus` and `brew list mupen64plus`; formula layouts vary. Check `python3 -m tkinter` before launching. Use the header from the installed core SDK, or matching upstream SDK source if headers are not packaged.

Build our scripted P1 plugin from the repository root (the script locates a Homebrew SDK when present; otherwise supply the directory containing the header):

```sh
bash scripts/build_mupen_input.sh /path/to/mupen64plus-sdk
bash Run-Mac.sh
```

## Linux (source mode, integrated toolkit)

On Debian/Ubuntu with Mupen64Plus 2.6.0 packages available:

```sh
sudo apt install mupen64plus-ui-console libmupen64plus-dev mupen64plus-video-rice mupen64plus-audio-sdl mupen64plus-rsp-hle python3-tk python3-psutil build-essential
bash scripts/build_mupen_input.sh
bash Run-Linux.sh
```

Select **Frame Inspector → Mupen64Plus (native)**. Library detection checks bounded `/usr` and `/usr/local` directories including multiarch plugin locations and the Debian shared-data directory. For a custom installation, browse to its matching core and libraries manually. The build script accepts an explicit matching SDK header directory. The native standalone launch (`python3 -m practice.mupen_native_ui`) is retained. The game window remains a separate native SDL window; the inspector controls are embedded.

The native embedded page is disabled on Windows, frozen builds and read-only sessions; the Project64 page retains its existing access policy. Existing Project64 and native recomp connections are unchanged. No changes to external-process permissions are needed.

## Setup and operation

Use **Find Mupen64Plus installation** to prefill installed files, or browse manually. The embedded page tries discovery once when first opened. Choose the exact ROM, `libmupen64plus` core library, native GFX, audio and RSP plugin libraries, and the **custom Goemon input plugin** just built (not the stock SDL input plugin). Choose the Mupen64Plus shared-data directory and a research configuration parent directory; the frontend uses a dedicated `goemon-native-session/research-saves` subdirectory. It selects pure interpreter mode, disables randomized PI/SI timing, and rejects non-debug cores other than 2.6.0. This changes timing relative to normal randomized configurations, so compare only sessions with identical settings. Launch session; the setup panel collapses automatically to leave space for traces. Show setup reopens it. Use Hold input while running to navigate, or Pause then Step +1 / Run timeline. No physical controller passthrough is included; buttons and X/Y inputs are controlled from this inspector. The input plugin presents only P1, no controller pak. Resume resets input to neutral; held input remains active until changed. Closing the UI requests normal emulator stop through its private inherited stdin; no network server is started.

Watches may be entered before launch or edited during a session. Pause and stop recording, then select **Apply watches (paused)**. Changing the schema clears the previous trace only with explicit confirmation; export first if needed. Invalid changes preserve the previous watch set and rows. The next core callback samples the new schema. The **JP controller preset** fills in the ten catalogue-backed watches established by the Japanese horizontal/vertical/C-Up tests. The preset is not approved for USA.

Each line is `name u8/s8/u16/s16/u32/s32/f32 hex_address` or `name u16 @catalogue_id`. At most 24 watches. An explicit pointer chain such as `example f32 80001000->5C->20` means read a u32 guest pointer at 0x80001000, add 0x5C, read another u32 pointer there, add 0x20 and read the final float. This address is illustrative, not a player root. A `@catalogue_id` root requires a registered 4-byte field. Every hop and final read must be aligned within the first 4 MiB of KSEG0 RAM, with at most four dereferences; invalid/null pointers return unavailable. A valid address does not prove the object is still the player. No pointer scanning, automatic object selection, or arbitrary memory writes. The actual Japanese player root still needs independent identification. Reads occur only in the native frame callback. For debugger-enabled cores, native RAM type/readable flags are also checked. For non-debug 2.6.0, the documented `DebugMemGetPointer` supplies native uint32 words.

Timeline syntax uses the same relative step format as Project64, e.g.:

```
1 - 80 0
2 - 0 0
3 CU 0 0
```

Steps call native `M64CMD_ADVANCE_FRAME` and wait for the native frame callback **and** paused state. A batch rejects extra callbacks, timeouts and oversized input sequences (max 60). Each callback records P1 plugin polls since the previous callback (for a stepped batch the counter resets at the step request) and the last requested input, not proof that the game consumed it. Record toggles continuous capture, with a bounded 600-row buffer; step captures even with Record off. Export CSV/JSON, compare with a compatible JSON trace by relative row, orange for changes and red for differences. Raw traces stay private; don't commit them.

## Mini Ebisumaru ability grant (Japan-0, core 2.6.0 only)

Enter normal gameplay with Ebisumaru available, export and clear the trace, stop recording, and pause. Click **Unlock Mini Ebisumaru (JP)** and confirm. One neutral core frame advances; the native frame callback resolves the existing Japanese inventory byte and original script grant word from the catalogue, checks the pinned mapping, refuses unexpected nonbinary word values, sets the word to 1 only if it was 0, and verifies readback. No forced transformation, party membership, event flags, action or movement edits. The status reports the grant result, not a continuously monitored ability value. Switch to Ebisumaru and use C-Up normally. This changes the research session's live saved-data state and may persist if saved; it does not edit the original ROM. Do not use in title/menu/loading states. Native gameplay acceptance remains untested for this grant.

## Boundaries and current limitations

A Mupen64Plus **core frame** is not a Goemon player update. An emulator pause command may stop between frames. The first recorded stepped sample is the next core callback; input polling may have occurred before or after a given game update. The trace does not establish the Ebi Slide mechanism. A future calibrated player-update hook must independently correlate execution, consumed inputs and player task identity. CPU breakpoints, arbitrary guest writes, savestate control, true logic-update stepping, stock process attachment, full Dashboard memory integration, and physical controller passthrough are **not implemented**. The native frontend is source-mode only. Earlier user-supplied macOS traces demonstrated controller polls, game-side input and dynamic watch reads. The integrated Linux UI has only been exercised with headless Tk and synthetic fixtures; no live core launch was performed for this update. Mock tests exercise the ABI-facing plugin/controller and frontend state machine; they cannot establish live compatibility. See upstream [2.6.0 RDRAM implementation](https://github.com/mupen64plus/mupen64plus-core/blob/2.6.0/src/device/rdram/rdram.c), [2.6.0 pointer API](https://github.com/mupen64plus/mupen64plus-core/blob/2.6.0/src/api/debugger.c), [frontend API](https://github.com/mupen64plus/mupen64plus-core/blob/master/src/api/m64p_frontend.h), [debugger API](https://github.com/mupen64plus/mupen64plus-core/blob/master/src/api/m64p_debugger.h), [plugin API](https://github.com/mupen64plus/mupen64plus-core/blob/master/src/api/m64p_plugin.h), and [native frame callback/pause implementation](https://github.com/mupen64plus/mupen64plus-core/blob/master/src/main/main.c).
