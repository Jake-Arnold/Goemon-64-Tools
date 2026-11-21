# Scripted guest-RAM tracer for the PJ64-style toolkit debugger

This feature is on `toolkit/pj64-debugger`, based on toolkit `main`, not on the decomp branch. Open **Debugger → Scripted tracer** in the existing Tk toolkit and connect to a verified USA or Japan native recomp/emulator backend. The canonical `main` toolkit's `active_session` selects the correct regional RDRAM reader; no game patches.

## Usage

1. Choose **Script VM / dialogue** or **Scene transitions**, then **Load preset**, or **Open script…** for a JSON script.
2. Press **Start trace**. The first sample establishes a baseline and **never** emits synthetic changes. The recorder then polls the configured original N64 guest addresses at the requested minimum interval while the toolkit stays connected, including when another toolkit tab is selected.
3. Reproduce the behaviour in-game. Use **Mark** for a timestamped annotation without altering RAM. **Stop trace** preserves observed events.
4. Export **JSON** (whole session) or **JSONL** (one metadata record followed by individual event records), even after disconnect. Exporting does not include any unconfigured RAM bytes.

The interval is a minimum; the toolkit's existing refresh loop is approximately 170 ms. Shorter changes, intermediate writes and back-to-back changes between polls can be missed. The timestamps are **host observation times, not precise game-event times**. The engine records *observed changes*, not the identity of the writer. No controller input, auto-gameplay, writes, CPU breakpoints or native function hooks are executed by trace scripts.

## Script format

```json
{
  "format": "goemon-scripted-trace-v1",
  "name": "Dialogue change example",
  "region": "usa",
  "sample_ms": 200,
  "max_events": 1000,
  "log_changes": true,
  "watches": [
    {"name": "vm", "address": "0x801C77E0", "type": "u32"},
    {"name": "cursor", "address": "0x80077858", "type": "u32"}
  ],
  "triggers": [
    {"name": "vm_changed", "watch": "vm", "op": "changed",
     "pre_samples": 4, "post_samples": 6, "capture": ["vm", "cursor"]},
    {"name": "waiting_for_A", "watch": "vm", "op": "eq", "value": 3,
     "pre_samples": 4, "post_samples": 4, "once": false, "cooldown_ms": 0}
  ]
}
```

`watches` have unique identifiers and guest KSEG0/KSEG1 addresses, not host pointers. Types: `u8`, `u16`, `u32`, `u64`, `s8`, `s16`, `s32`, `s64`, `f32`; all use canonical guest big endian. Signed integers and finite floats have numeric decoded values; non-finite floats are reported as `null`. Supported trigger operations: `changed`, `increased`, `decreased`, `eq`, `ne`, `gt`, `lt`, `ge`, `le`, `bit_set`, `bit_clear`. Comparison/bit triggers fire on **false → true** transitions; `changed` fires when raw bytes differ across polls. `bit_set`/`bit_clear` use a nonzero integer `mask`, e.g. `"0x20"`. Numeric comparisons require `value`, an integer/float or `0x`-prefixed integer string. Repeating observations can use `cooldown_ms`, or `once: true` to fire only once per recording. Trigger `capture` selects the named watch subset; it defaults to all watches. A trigger records up to `pre_samples` prior observations, the hit observation, and up to `post_samples` later observations. A stopped trace's unfinished windows remain explicitly `complete: false`.

Limits are enforced before reading any RAM: 64 KiB JSON script, up to 32 watches, 16 triggers, sampling minimum 100 ms, at most 32 preceding and 32 following samples, no more than 128 scalar observations per trigger capture window, at most 1,500 retained events. There is no `eval`, Python execution, process launching, or script-specified filesystem/network operation. An unreadable address or process read error stops recording and preserves previously observed events for inspection/export. Reconnect stops the active trace; it cannot silently continue against a new process.

## Built-in examples

**Script VM / dialogue** monitors the observed USA script-state `0x801C77E0`, cursor `0x80077858`, resource ID `0x801C78E8`, high-level game state `0x800C7A94` and gameplay submode `0x800C7AA4`. The preset triggers on VM-state and cursor changes, with pre/post context. Labels are observation-based, not complete proof of semantic meaning.

**Scene transitions** monitors the observed USA game state and scene/map fields, and captures the context around state and map changes. These are original-USA addresses; *do not* apply a blanket USA↔JP offset translation. Built-in preset addresses resolve from `practice.address_registry` and are **USA-only**. Attempting to start them on a Japanese session is rejected before sampling. Custom scripts without a `region` may observe either game with explicitly chosen region-correct addresses; scripts with `region: "usa"` or `"japan"` are locked to that selection.

## Diagnostics and limitations

JSONL records include session provenance, a script snapshot, per-change hexadecimal before/after bytes and decoded values, and for triggers a before/current/after series. They do not include a ROM dump, entire RAM pages, CPU registers, guest PC or native stack frames. Export files are user-selected local files; they are not committed to GitHub.

This is a first operational stage of script-driven debugging. For exact **native C/C++ function entry/exit traces** with arguments, return values or call stacks, an independent, instrumented native runtime with a versioned event interface is still required; polling alone cannot supply these reliably.

## Verification

ROM-free unit/UI tests: `xvfb-run -a python3 -m unittest tests.test_scripted_trace tests.test_pj64_debugger -v`. Tests use a synthetic in-memory guest RAM adapter and a virtual X11 display. They do not establish actual running-game timing, effect on frame rate, or native instrumentation.
