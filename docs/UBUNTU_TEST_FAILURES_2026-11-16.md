# Ubuntu Japanese toolkit test failures and native JP crash (2026-11-16)

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
