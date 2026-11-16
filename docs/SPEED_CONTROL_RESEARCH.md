# Game speed control research

Date: 2026-11-03. The toolkit has an experimental live multiplier for a separately
built compatible recomp. The stock recomp and Project64 are not changed.
Host-clock and UI/channel checks passed; actual gameplay, audio and cutscene
behavior at increased speed still require in-game validation.

## What is already useful

Matching native code in `decomp/default_entrance.c` selects the default entry
coordinates and mode; this corroborates and can improve entrance-atlas behavior,
but does not itself perform a complete transition. `decomp/transition_state.c`
reconstructs nested state changes used during transition. `decomp/bit_array.c`
provides verified bit-array operations, and the individual Fortune Doll flags
and counter are already surfaced in the toolkit. Do not use a state setter alone
to claim a safe warp.

## Live speed control

The Dashboard **Game speed (recomp)** panel can launch a compatible local build,
then request 1x–4x at runtime. **Speed up** enables the selected 2x/3x/4x rate;
clearing it returns to 1x. The host acknowledges the applied multiplier via a
process-scoped Windows shared-memory channel; the UI shows the selected PID and
applied value. The channel has a version/magic/PID check and uses the process
security descriptor. A normal stock recomp or Project64 has no compatible
channel, so the control is unavailable rather than claiming to have changed speed.
Read-only mode blocks launches and speed requests.

The local compatible executable was built separately under the user's
`g64-speed-build/build-speed` directory. It is in portable mode, with a separate
copy of the user's on-disk save files taken after two matching reads. Existing
saves and the running stock process were not modified. Portable changes do not
sync back automatically. The user-supplied ROM and local executable/saves are
not committed to Git. Controls/configuration are also separate.

`speed/prepare_runtime.py`, `speed/prepare_live_runtime.py` and
`speed/prepare_recomp_title.py` reproduce the source modifications against the
pinned commits. The live runtime uses one continuous virtual clock for guest
timers and VI scheduling, wakes pending timer waits on speed changes, and checks
for premature deadlines after a slowdown. VI waits can respond after the current
host sleep. A live mapping exposes requested/applied rates and a diagnostic guest
clock. In isolated frontend testing, GUI requests 1x–4x were acknowledged and
the clock advanced at approximately 0.99x, 1.99x, 3.04x, 3.95x, then 0.99x;
this does not establish gameplay, cutscene, renderer or audio behavior.

The Windows build used local LLVM 23.1.4, Visual Studio Build Tools, a local GNU
Make and WSL Clang/LLD for MIPS patches. Two local SDL 2.26.3 header guards were
adjusted for Clang 23's `_m_prefetch` builtin; these are build-checkout changes,
not committed upstream patches. The build also used the user's verified ROM
locally. The prepared runtime files match the built source and the title-label
edit matches `prepare_recomp_title.py`. Existing source and saves are preserved.

## Recomp timing

The Goemon64Recomp upstream source at commit
`6661abc439327b9ed9e235c391720f9034f61a78` pins N64ModernRuntime
`fc4592a31414daf0040c19907e0b1976b2e48a67`. Its
`ultramodern/src/timer.cpp` defines `speed_multiplier` as a compile-time constant
of one and derives `counter_per_ms` from it. Its `ultramodern/src/events.cpp`
uses `get_speed_multiplier()` to schedule VI interrupts. In that source there is
no runtime setter or toolkit-facing speed interface. The exact source/build
identity of the user's existing executable was not established; do not assume it
has the identical implementation without verification.

The native game byte `retraces_per_game_step`, at static-system address
`0x800C7A8A`, affects game-loop pacing: the main loop compares its retrace
counter against that byte. The recomp graphics patch also reads it to set the
render refresh hint. The game itself writes different values in several states,
including resetting it to two in the already matched transition-state helper.
Changing/freezing this byte is an unverified timing experiment, not a general
host-wide multiplier, and has not been tested here. It does not establish correct
speeding of audio, timers, cutscenes or transitions. Do not label a generic
memory write or movement pulse as an established arbitrary-speed mode.

## Experimental native Linux live speed (2026-11-13)

The patched runtime channel now also exposes a Linux-only v2 POSIX shared-memory
mapping at `/goemon64speed_<PID>` (`/dev/shm/goemon64speed_<PID>`).
It is created with owner-only 0600 permissions and unlinked on a normal exit.
The Python Linux client checks that the selected PID actually maps that shared
memory, checks owner/permissions/length and validates the same magic/version/PID
and requested/applied fields used on Windows. No stock executable contains
the patch; this is **not** a speedhack for existing unmodified game processes.

The native Linux channel was compiled and tested against a synthetic host:
a 1x channel accepted a 4x request, acknowledged 4x, and cleaned up the
shared-memory name on normal exit. It was not tested with a real Goemon game.
To use it, prepare a separate pinned runtime with `speed.prepare_runtime`
and `speed.prepare_live_runtime`, then build the native game against that
runtime. Do not alter the installed stock game or its saves.

## Project64

Project64 upstream source inspected at commit
`7c2e1e3e8f662933e9f332862be642caec138fce` has increase/decrease speed commands,
a speed limiter and a separate FPS limiter. Its default shortcuts are configurable;
the source lists plus/minus for speed and F4 for FPS limiting. The limiter's
speed changes in steps, and audio synchronization/settings can affect the
result. The user's installed version/settings and live resulting multiplier were
not checked in this investigation. Relative shortcut presses do not reliably
establish an absolute 2x/3x target without knowing current speed and settings.

## Earlier fixed-startup prototype

`speed/prepare_runtime.py` can prepare a clean, isolated N64ModernRuntime checkout
at the exact pinned commit. It adds a small header and changes the runtime's
compile-time multiplier to a process-start value from `GOEMON_SPEED_MULTIPLIER`.
Only whole-number values `1`, `2`, `3`, `4` are accepted; missing or invalid
values fall back to 1x. The value remains fixed for the process lifetime, so the
existing VI and guest-timer calculations continue using one consistent rate.
The script rejects a dirty or wrong-revision checkout and an existing target
header; it atomically publishes the modified timer source. It does not build,
install or launch the recomp, and does not alter an existing executable.

The prepared runtime was checked against a fresh local checkout of the exact
pinned source. The startup parser was compiled and tested at 1x, 2x, 4x and
invalid input, and unit tests cover source preparation/refusal and launch
arguments. **This is source-level integration, not a built or live-tested game.**
Audio, high-speed playback, runtime performance and game behavior are unverified.

After building a separate Goemon64Recomp executable against the prepared runtime,
request a fixed rate at launch with:

```powershell
py -3.13 -m speed.launch_recomp "C:\path\to\speed-enabled\Goemon64Recompiled.exe" --multiplier 2
```

The launcher sets the child process environment, starts the chosen executable in
its own folder and reports the requested rate. It cannot tell whether that binary
actually contains the patch, so the stock executable may ignore the setting.
At this earlier stage there was no in-toolkit selector or readback. A full game
build requires the upstream build dependencies, generated recompiler output and
submodules; see the pinned Goemon64Recomp `BUILDING.md`. Changing speed requires
restarting this startup-only build. Do not replace or stop the currently running
game or its saves while preparing a separate build.

## Implemented timing primitive

`speed/virtual_clock.h` provides a standalone synchronized virtual clock with
1x–4x multipliers in quarter-speed increments. It rebases the epoch on each
change, retains fractional microseconds and converts a guest deadline to a host
deadline. It rejects backwards host timestamps and arithmetic overflow. Callers
must use a monotonic host source and wake/recalculate existing timer and VI waits
after changes; the primitive does not do so automatically. The live runtime
integration implements these responsibilities as described above.

`speed/test_virtual_clock.cpp` covers continuity, multiple speed changes,
deadline recalculation and rounding, invalid values, overflow, and simultaneous
access. It is now used by the experimental rebuilt recomp runtime. The standalone
test itself does not validate gameplay or audio, and Project64 is separate.

```bash
g++ -std=c++17 -Wall -Wextra -Werror -pthread -fsanitize=address,undefined \
  -Ispeed speed/test_virtual_clock.cpp -o /tmp/goemon-virtual-clock-test
/tmp/goemon-virtual-clock-test
```

An initial PATH-only search did not find the Windows C++ tools. A later search
found Visual Studio Build Tools and CMake outside PATH; a local Clang toolchain
was added for the separate build described above. The stock executable remains
unchanged.

## Remaining work

1. Verify actual gameplay, audio, cutscenes, scene transitions and save behavior at
   1x and higher rates. Frontend host-clock measurements alone do not prove this.
2. Exercise timer deadline changes under real game load, including pauses and
   repeated changes. The standalone clock and source preparation tests do not
   replace that integration evidence.
3. Investigate a separate Project64 speed interface with readback and audio sync;
   the recomp channel does not apply to Project64.
4. Continue tracing the native room loader and unloader; speed control is a host
   timing feature and does not validate scene-warp behavior.

Source: [Goemon64Recomp](https://github.com/klorfmorf/Goemon64Recomp/tree/6661abc439327b9ed9e235c391720f9034f61a78),
[N64ModernRuntime timer](https://github.com/klorfmorf/N64ModernRuntime/blob/fc4592a31414daf0040c19907e0b1976b2e48a67/ultramodern/src/timer.cpp),
[N64ModernRuntime VI scheduler](https://github.com/klorfmorf/N64ModernRuntime/blob/fc4592a31414daf0040c19907e0b1976b2e48a67/ultramodern/src/events.cpp),
[Project64 speed limiter](https://github.com/project64/project64/blob/7c2e1e3e8f662933e9f332862be642caec138fce/Source/Project64-core/N64System/SpeedLimiter.cpp),
and [Project64 shortcuts](https://github.com/project64/project64/blob/7c2e1e3e8f662933e9f332862be642caec138fce/Source/Project64/UserInterface/MenuShortCuts.cpp).
