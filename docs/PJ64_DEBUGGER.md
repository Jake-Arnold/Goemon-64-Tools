# PJ64-style debugger (native Linux recomp / original-USA guest RAM)

The **Debugger** tab is integrated into the existing Tk toolkit. Use the toolkit's **Connection** panel to attach to a native Goemon64Recompiled PID; existing Linux process permissions and the validated RDRAM mapping still apply. It can also inspect a connected compatible Project64 process using that same RDRAM abstraction. Run `python3 -m practice.toolkit` after installing the toolkit's normal dependencies.

## Implemented (live guest RAM)

- **Memory viewer:** navigate original N64 KSEG0/KSEG1 RDRAM addresses, 16-byte big-endian hex and ASCII rows. Live refresh is opt-in via a checkbox (on by default, 500 ms, only while the Debugger memory page is visible). This view is not a CPU trace.
- **Raw edits:** read expected bytes, enter a new 1/2/4/8-byte hex value, approve the warning, compare against current RAM, write, and verify readback. `--read-only` disables the write control. This comparison is **not atomic** against the game thread; use disposable saves. Writes are session-only and do not modify the ROM or original decomp C.
- **MIPS III disassembly:** static decode of 32-bit instruction words currently present in RDRAM. Supports integer, common memory, branches, jumps, register transfers and selected COP1 instructions. Unsupported encodings display `.word`. This is **not** a listing of currently executing host machine code. Overlays and code not loaded into guest RAM are not shown.
- **Find bytes:** exact hex or ASCII search over a chosen guest-RAM range, in a background worker, with chunk overlap and up to 256 results. Double-click a result to jump to the memory viewer. No external ROM or filesystem search.
- **Change watches:** poll 1/2/4/8-byte addresses every 500 ms and record changes. Up to 64 addresses and the most recent 500 change events per session. Export events (not a full RAM dump) as JSON. Reconnecting clears watches and events; a change observation is not a hardware breakpoint or evidence of the writing instruction.

## Native execution instrumentation still required

Unmodified Goemon64Recompiled is a static native translation, not an N64 CPU emulator. Its host process/RDRAM map does not expose an authoritative running guest MIPS PC, GPRs, FPRs, HI/LO or CP0 state through the toolkit's RDRAM API. The **CPU / breakpoints** panel displays these as unavailable. It does not pretend to pause, single-step, run MIPS execution breakpoints, or produce real instruction traces.

A subsequent *native runtime* change would need a versioned debugger IPC protocol plus coordinated compiler/runtime instrumentation, with guest PC and register snapshots at explicit instruction or function checkpoints, pause/resume/step acknowledgements, breakpoint and watchpoint hit reasons, and safe handling of overlay address spaces and threads. Do not turn a memory-change polling loop into a claimed CPU breakpoint, or infer a guest PC by scanning original code bytes.

## Verification

ROM-free synthetic tests live in `tests/test_pj64_debugger.py`: address bounds, endian-order displays, MIPS instruction rendering, scans across chunks, read-only and stale-write rejection, change-watch events and UI smoke. These do **not** establish verified behaviour against a running native game. Tests can be run with `python3 -m unittest tests.test_pj64_debugger` (use an X11 session or `xvfb-run` for the GUI smoke).

## Scripted trace recording

**Debugger → Scripted tracer** now supports declarative JSON trace scripts with guest-memory watches, edge-triggered conditions, pre/post event capture, markers, script load/save, and JSON/JSONL export. See [SCRIPTED_TRACING.md](SCRIPTED_TRACING.md). Scripts are strictly observational; function-call and CPU execution instrumentation remain unavailable in the unmodified native runtime.

## Mainline toolkit integration

This feature branch is based on canonical toolkit `main` and uses `practice.region_session.active_session`, which distinguishes USA `mem` from Japan `jp_rdram`. The debugger/trace follows the selected region and resets watches when region, PID or reader changes. Trace records remain exportable after reconnect. Default scripted presets are USA-specific, sourced by stable ID from the canonical address registry and rejected when a Japan session is selected.
