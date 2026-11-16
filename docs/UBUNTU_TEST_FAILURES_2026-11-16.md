# Ubuntu Japanese toolkit test failures and native JP crash (2026-11-16)

## Later v0.11.30 user run (14:55 UTC): 290 core tests passed, GUI stalled

User launched the *separate* `Goemon64RecompiledJP` from
`~/Goemon64Recomp-JP` after successfully completing its 15 stage-5 unit
tests and Clang/CMake build. This game run logged a clean timer-worker join
and cleaner audit, with guest teardown still explicitly not proven. No
segmentation fault or native-game freeze is shown in this later log.

The user then checked out
`toolkit/japan-debug-autoattach-warp-reliability` and ran
`bash scripts/test_japan_party.sh`. **All 290 non-GUI tests passed**.
The Xvfb GUI section passed the Japanese-focused tests and GNOME launcher
test but reported multiple USA-only test FAIL/ERROR results in
`tests.test_value_freezes_ui`, `tests.test_story_progress_ui`,
`tests.test_dashboard` and `tests.test_entrance_ui`. The supplied log
ends without a GUI suite result on
`tests.test_entrance_ui.EntranceUITests.test_scene_request_blocks_overlapping_checkpoint_restore`,
whose `restore_full_checkpoint()` can open a modal
`messagebox.askyesno` if `pending_direct_warp` is absent.
**The log does not show a Python traceback or process thread dump**;
the hidden-modal mechanism is a strongly supported hypothesis, not a
directly observed stack trace.

### Identified cross-test dependency and scoped correction

The GUI tests intentionally switch the toolkit to Japan using
`on_game_version_changed()`, which persists the selection with
`save_last_region()`. The subsequent **USA-only** test fixtures
constructed `Toolkit(..., parse_args([]))` without specifying a
region, causing them to inherit the last saved Japanese selection
from the same test sequence or user's settings. This explains the
broad cluster of unrelated USA-only failures and why the synthetic USA
scene request would not produce the expected pending warp.
Calling `restore_full_checkpoint()` then bypasses the pending-warp
guard and reaches the confirmation dialog, which is invisible under
Xvfb and can wait indefinitely.

Corrections on the v0.11.30 feature branch:

1. Pin USA-only fixture constructors in
   `test_value_freezes_ui.py`, `test_story_progress_ui.py`,
   `test_dashboard.py`, and `test_entrance_ui.py` to explicitly
   select `usa`, independent of persisted preferences. Each checks
   `active_version.key == 'usa'` during setup.
2. Pin initial USA state in Japanese transition tests
   `test_japan_named_checkpoint_ui.py`, `test_japan_value_freezes_ui.py`,
   `test_japan_story_progress_ui.py`, and `test_region_unlocks_ui.py`
   and prevent their `save_last_region` calls from writing to the
   developer's own launcher preferences.
3. Isolate the entire Linux test run with a disposable
   `XDG_CONFIG_HOME` directory; remove it on script exit.
   This prevents tests from modifying the installed toolkit's
   persistent region, ROM cache, or connection hints.
4. The formerly hanging entrance/checkpoint test explicitly asserts
   that `pending_direct_warp` exists and mocks
   `practice.toolkit.messagebox.askyesno` to raise an immediate
   test error rather than block on a hidden GUI dialog if the
   precondition unexpectedly fails.
5. Bound the Xvfb and DISPLAY GUI smoke phase with coreutils
   `timeout` (default **120 seconds**, configurable with
   `GOEMON_GUI_TEST_TIMEOUT_SECONDS`), so any further unmocked
   modal deadlock fails with nonzero exit instead of waiting forever.

These changes touch **test fixtures and the Linux test runner only**;
native recomp executable and production toolkit RAM/discovery/warp
logic are unchanged by this correction.

**Verification boundary:** These corrections were committed on GitHub
after the observed 290-pass/hung-GUI run. The user has **not yet
rerun** the corrected GUI suite. Do not claim this issue is closed
until the full GUI test summary succeeds, including the formerly
stalled entrance/checkpoint test.

### Reproduction / verification after fetching the new commit

```bash
cd ~/Desktop/Goemon-64-Tools-JP-Recomp
git fetch origin
git switch toolkit/japan-debug-autoattach-warp-reliability
git pull --ff-only
bash scripts/test_japan_party.sh
```

The command tests in an isolated temporary preferences environment.
An unrelated live game process is **not** required; the memory/write
fixtures are synthetic. Only run `bash Run-Linux.sh` separately
after the tests, and perform live game validation independently.

---


## Reproduction evidence

User ran `bash scripts/test_japan_party.sh` from a fresh toolkit
`main` checkout and reported **264 tests, 8 errors and 1 failure**.
This test count is from the user's Ubuntu output, not a GitHub CI run.

### Eight Python errors — stale synthetic controller fixtures

- `tests/test_japan_party_controller.py`:
  `test_bulk_unlock_writes_33_user_verified_but_skips_battery`,
  `test_direct_triton_shell_cucumber_and_fish_count`, and
  `test_no_opt_in_or_dialog_for_sasuke_and_yae_on_off`.
- `tests/test_japan_live_memory_edit.py`:
  `test_arbitrary_japanese_addresses_write_one_two_and_four_bytes`
  produced **three** independent subtest errors (width 1/2/4);
  `test_stale_expected_value_rejected_without_write` and
  `test_unknown_guest_address_is_allowed_in_live_editor`.

Each raised
`AttributeError: 'types.SimpleNamespace' object has no attribute '_japan_writable_reader'`
in `practice/toolkit.py` on the path to a Japanese writable host handle.

**Cause:** Synthetic `SimpleNamespace` test screens were constructed before
`Toolkit._japan_writable_reader` was introduced. Production Toolkit has
the helper; the old mock screens did not. These traces therefore do **not**
by themselves demonstrate a broken real Japanese unlock/editor write.

**Fix:** Both test modules now use one shared synthetic screen factory.
The factory attaches a closure invoking the real
`Toolkit._japan_writable_reader(screen, host, attached)`; it does **not**
bypass the production method. A regression additionally asserts that the
recomp backend still performs its process/verified-JP-ROM/probe writer
validation and calls `validate_japan_recomp_writer`.

### One Linux launcher test failure — GNOME frame selected

`tests.test_linux_launcher.LinuxLauncherTests.test_real_tk_x11_window_instance_matches_installed_desktop_id`
used `xprop -name "Goemon Practice Toolkit Dock Identity Smoke Test" WM_CLASS`.
On the user's GNOME session, X11 title matching returned
`"mutter-x11-frames", "mutter-x11-frames"`, not the Tk application.
This establishes an **ambiguous/incorrect test selector**, not by itself
incorrect GTK/Tk app identity or dock grouping.

**Fix:** Use a title unique to the test process and Tk window ID;
enumerate X11 windows with `xwininfo -root -tree`, then invoke
`xprop -id <matched-client-window-id> WM_CLASS`.
The test checks for an exact `"goemon-practice-toolkit"` X11 class.
If `xwininfo` or X11 is unavailable the GUI test is explicitly skipped.
A standalone equivalent selection check was executed in local Xvfb and
identified the real Tk wrapper:
`WM_CLASS(STRING) = "goemon-practice-toolkit", "Goemon-practice-toolkit"`.
This is **not** a claim that the entire Ubuntu suite passed.

## Independent native Japanese recomp segmentation fault

From a **different local checkout**, `~/Goemon64Recomp-JP`,
the user launched
`./build-generated/japan-native-game/Goemon64RecompiledJP` three times.
All printed `Failed to preload executable!` but continued to initialize
SDL, GPU and fonts. The first two ended with
`[Goemon JP runtime] Timer worker joined cleanly`. The third
reached `Initializing recomp heap at offset 0x01000000 with size
0x1F000000` and then `Segmentation fault (core dumped)`.

**Do not conflate these logs with the nine Python test errors.**
The standalone JP executable is distinct from the toolkit test process.
The preload message occurs on runs without a reported crash, so it
cannot alone establish the crash cause. The third-run SIGSEGV is
unresolved: no stack trace, offending thread, instruction pointer or
core analysis was supplied, and the exact local game branch/commit is
unknown.

For local native-game diagnosis (run after a fresh crash; do **not**
upload/share a potentially ROM-containing raw core):

```bash
cd ~/Goemon64Recomp-JP
git branch --show-current
git rev-parse HEAD
coredumpctl --no-pager list | tail -20
coredumpctl --no-pager info -1
coredumpctl dump -1 -o /tmp/goemon-jp.core
gdb -q -batch -ex 'set pagination off' \
    -ex 'thread apply all bt 25' \
    ./build-generated/japan-native-game/Goemon64RecompiledJP \
    /tmp/goemon-jp.core
rm -f /tmp/goemon-jp.core
```

Verify that the latest coredump (`-1`) is for
`Goemon64RecompiledJP` before extracting it. A backtrace plus exact
local recomp branch/commit is required to isolate and fix this
separate runtime defect. Avoid speculating that the experimental reset
workers caused this crash merely because they appear in earlier log
lines.

## Acceptance

1. Re-run the full toolkit suite:
   `bash scripts/test_japan_party.sh`.
2. In particular verify
   `python3 -m unittest tests.test_japan_party_controller
   tests.test_japan_live_memory_edit tests.test_linux_launcher -v`
   under the user's graphical Ubuntu session.
3. Only then mark the Python test failures resolved.
4. Investigate native recomp's intermittent SIGSEGV in the separate
   Goemon64Recomp checkout with a real stack trace.

**Change scope:** this test-fix branch updates synthetic test fixtures,
X11 window selection, and documentation/version only. No production
gameplay, memory-write, loader or native recomp code is changed.
