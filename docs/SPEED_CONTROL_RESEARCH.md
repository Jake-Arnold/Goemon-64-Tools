# Game speed control research

Date: 2026-11-03. This is an investigation and implementation plan; it does not
claim that the toolkit currently controls a game-speed multiplier.

## What is already useful

Matching native code in `decomp/default_entrance.c` selects the default entry
coordinates and mode; this corroborates and can improve entrance-atlas behavior,
but does not itself perform a complete transition. `decomp/transition_state.c`
reconstructs nested state changes used during transition. `decomp/bit_array.c`
provides verified bit-array operations, and the individual Fortune Doll flags
and counter are already surfaced in the toolkit. Do not use a state setter alone
to claim a safe warp.

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

## Project64

Project64 upstream source inspected at commit
`7c2e1e3e8f662933e9f332862be642caec138fce` has increase/decrease speed commands,
a speed limiter and a separate FPS limiter. Its default shortcuts are configurable;
the source lists plus/minus for speed and F4 for FPS limiting. The limiter's
speed changes in steps, and audio synchronization/settings can affect the
result. The user's installed version/settings and live resulting multiplier were
not checked in this investigation. Relative shortcut presses do not reliably
establish an absolute 2x/3x target without knowing current speed and settings.

## Prepared fixed-startup integration

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
There is no in-toolkit speed selector or runtime speed readback yet. A full game
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
after changes; the primitive does not do so automatically.

`speed/test_virtual_clock.cpp` covers continuity, multiple speed changes,
deadline recalculation and rounding, invalid values, overflow, and simultaneous
access. It is a local timing primitive, not connected to the recomp executable,
audio, Project64 or the toolkit UI. It cannot yet speed up the game.

```bash
g++ -std=c++17 -Wall -Wextra -Werror -pthread -fsanitize=address,undefined \
  -Ispeed speed/test_virtual_clock.cpp -o /tmp/goemon-virtual-clock-test
/tmp/goemon-virtual-clock-test
```

The inspected Windows environment did not expose `cmake`, `ninja`, `cl`, or
`clang` on PATH and did not contain the Visual Studio installer locator. The
running binary has not been rebuilt or replaced. Toolchain discovery is not a
conclusive inventory of every compiler installed elsewhere.

## Implementation path

1. Build and validate the fixed-startup runtime path above. For live changes, add
   a supported host control channel with multiplier readback and a bounded setter.
   Keep normal speed as the default, and make reconnect/restart behavior explicit.
2. Replace the compile-time assumption with a synchronized, continuous clock:
   rebase the virtual-time epoch at each change so elapsed guest time and pending
   timer deadlines do not jump. Update VI scheduling and N64 timer conversions
   consistently; do not merely change rendered FPS or the native movement byte.
3. Define audio behavior at higher speed, and test pauses, loading, save timing,
   state transitions, frame pacing and changing speed while timers are active.
4. Add toolkit backend capability detection and controls only after the host can
   report and apply a multiplier. Integrate Project64 separately using a verified
   version-specific interface, with actual speed readback and audio sync accounted
   for. Treat unsupported hosts as unsupported rather than displaying a false 2x.
5. Verify with monotonic wall-clock measurements against guest loop/retrace rates
   at 1x and selected faster settings, then validate actual gameplay and audio on
   a disposable save. Synthetic tests and a checksum-identical ROM alone cannot
   establish speed or real-time behavior.

Source: [Goemon64Recomp](https://github.com/klorfmorf/Goemon64Recomp/tree/6661abc439327b9ed9e235c391720f9034f61a78),
[N64ModernRuntime timer](https://github.com/klorfmorf/N64ModernRuntime/blob/fc4592a31414daf0040c19907e0b1976b2e48a67/ultramodern/src/timer.cpp),
[N64ModernRuntime VI scheduler](https://github.com/klorfmorf/N64ModernRuntime/blob/fc4592a31414daf0040c19907e0b1976b2e48a67/ultramodern/src/events.cpp),
[Project64 speed limiter](https://github.com/project64/project64/blob/7c2e1e3e8f662933e9f332862be642caec138fce/Source/Project64-core/N64System/SpeedLimiter.cpp),
and [Project64 shortcuts](https://github.com/project64/project64/blob/7c2e1e3e8f662933e9f332862be642caec138fce/Source/Project64/UserInterface/MenuShortCuts.cpp).
