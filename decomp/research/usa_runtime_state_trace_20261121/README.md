# USA frame-state and overlay-image read-only runtime observer

**Status: static overlay identity verified; Linux synthetic process-reader integration verified; LIVE GAMEPLAY NOT CAPTURED.** This is a ready-to-run instrumentation/diagnostics tool, not an emulator, an existing gameplay trace, or a matching-C promotion.

## Source authentication

Original USA retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`, expanded reference SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494` (33,554,432 bytes), pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.

The pinned Splat `static_overlay_1` group has **eight interchangeable file images at guest VMA `0x801CB460`**: files **11, 13, 14, 15, 16, 20, 22 and 23**. The committed SHA-256-only fingerprint catalogue captures 16-byte instruction windows at code offsets 0, 0x40 and 0x80 in each image, without committing any instruction bytes. The aggregate of three hashes uniquely identifies all eight reference images. Verified using the original code regions in the private 32 MiB ROM. The fingerprints identify **which executable bytes remain in guest RAM**; they do not independently prove that a particular file is *active*, newly loaded or currently executing. Code can remain as stale bytes after a loader has returned.

### Fields observed

- USA dynamic `SYS_W` pointer `0x8015C5C8`, required to equal authenticated `0x8008CCC0`.
- Outer state `SYS_W+0x3ADD4` / `0x800C7A94` (u8); completion/end byte `+0x3ADD5` (u8); secondary selector `+0x3ADD6` (u8); tertiary byte `+0x3ADD7` (u8).
- VM nested selector `+0x3ADDE` (u8) and nested end `+0x3ADDF` (u8).
- Map ID `0x800C7AB2` (u16), group-local room selection `0x800C7AB4` (u16). The previous `scheduler_mode` key was a misnomer; see `decomp/DEFAULT_ENTRANCE_TRACE.md`.
- Original file-22-only condition halfword `SYS_W+0x3B07C` / `0x800C7D3C` (u16); file22 counter `0x801D7008` (u32) **only interpreted when code image 22 is verified**.
- Global gate `D_800548D8` (u32) and fingerprint of 0x801CB460 code window.

No game RAM bytes, copyrighted overlay code, host pointer values or per-user game save contents are exported. Only decoded numeric fields and fingerprint identities are retained.

## Execute in live USA runtime (read-only but NOT frame-atomic)

This environment did not have a running USA game process, emulator or native recomp at the time of this investigation. On a Linux host with a supported process exposing **USA original RDRAM**, the existing `autosplitter.memory` Linux process adapter can collect observations:

```bash
cd /path/to/Goemon-64-Tools
python3 -m decomp.state_runtime_trace --pid 12345 --seconds 40 \
  --interval-ms 10 --output /tmp/goemon-usa-state-observations.json
```

Use the actual USA emulator/native recomp process PID. The process is opened **with `writable=False`** and only `read_guest` is used. An explicit verified memory base can be supplied as `--base 0x...`. This module never relaxes kernel ptrace permissions or injects input. A Japanese-only native recomp is **not compatible** with this USA address and signature catalogue. It will reject a mismatched system pointer or yield unknown image signatures; do not treat that as a Japanese crosswalk discovery.

The collector checks that the state block, overlay signature region and system pointer are unchanged across two reads, dropping torn observations. **This does not make polling frame-atomic.** The output always marks such observations `host_poll_non_atomic`, with `guest_frame: null` and `guest_pc: null`. A change between polls is an *observed value difference*, not proof of the exact MIPS writer, frame number or elapsed game frame count. Overwritten overlay code may remain readable after a transition.

## Room-transition reporting and schema correction (21 November 2026)

The original-USA field at `0x800C7AB4` is the **group-local room selection**, not a scheduler mode. A separate, user-reported live host capture (no raw RAM included) showed a constant outer state while multiple `map_id` values changed, consistently with original room-group base arithmetic. This finding corrects the previous `scheduler_mode` label. New traces use JSON format `goemon-usa-state-overlay-observations-v2`, field `room_group_selection`, and append `room_map_changed` records to `observed_transitions` even when the outer state stays constant. Older v1 files still use `scheduler_mode` and do not automatically contain room transition events. Their original samples should be reinterpreted, not overwritten.

The new `room_map_changed` event includes old/new map IDs, old/new group-local room selections, original outer state on both sides, overlay fingerprint identities, and poll elapsed time where available. These are sampled value differences, not proof of the guest instruction that caused the room change. Short-lived intermediate rooms can be missed.

For a new v2 capture, review room-map events using:

```bash
jq -r '.observed_transitions[] | select(.event == "room_map_changed") | "\(.elapsed_ms // 0) ms: map \(.from_map_id) → \(.to_map_id); selector \(.from_room_group_selection) → \(.to_room_group_selection); outer \(.outer_state_after)"' /tmp/usa-state-trace-v2.json
```

## Requirements for genuinely same-frame evidence

`decomp.state_runtime_trace.capture_halted_frame(ram, fingerprints, frame=..., guest_pc=...)` is the callback interface for a debugger/emulator that **actually pauses guest execution at one frame boundary** and supplies an authenticated game-frame index and guest PC. While the guest is halted, the bounded RDRAM fields and overlay image are read, yielding a `guest_halted_frame_callback` record. The caller, not this Python module, must establish that the guest really was halted; simply supplying a frame number does not create atomicity. The emulator must instrument original guest PC/execution and loader-completion events independently. A loader ID can be attached only when it comes from a confirmed successful loader completion and matches the independently fingerprinted code image; the API raises on disagreement.

Minimal callback integration outline (the names `debugger.*` are an interface sketch, **not** a currently implemented Goemon emulator API):

```python
# Executed by a real debugger frame-boundary callback, while guest is HALTED.
# ram = debugger.read_only_rdram()
# sample = capture_halted_frame(ram, fingerprints,
#     frame=debugger.authenticated_frame_counter,
#     guest_pc=debugger.guest_program_counter,
#     proven_loader_file_id=debugger.confirmed_overlay1_loader_completion)
# log.append(sample)
```

The original MIPS state setters and overlay direct-store points of interest are guest PC `0x800024A8`, `0x801CB53C`, `0x801CB5B8` (file22 only), `0x80003148`, `0x80003164` and `0x80003728`. To assert **that a particular instruction executed**, the debugger must record an execution or write breakpoint hit, not just a matching memory value in a subsequent frame. The authentic original-USA resource loaded at the shared guest code address must be identified before mapping any overlay PC to file22/file15 names.

## Verification (no game execution)

```bash
python3 -m unittest -v decomp.test_state_runtime_trace
python3 -m decomp.local_ci
python3 -m decomp.research.usa_runtime_state_trace_20261121.verify_overlay_fingerprints \
   --rom /private/usa/baserom.decompressed.z64 --report /tmp/overlay-fingerprint-proof.json
```

The first tests use synthetic memory and deliberately *cannot* prove gameplay. A separate actual `process_vm_readv` integration was exercised against a disposable Linux child process with a synthetic USA memory block and authenticated overlay-22 reference bytes. No Goemon emulator process was available for a genuine gameplay capture. Do not publish private diagnostics or raw RAM.

## Interpretation controls

- `3→4` with previous memory image file22 is `consistent_with_file22_overlay_state3_to4_path`, **not** proven caused by file22 without an executed-PC or store-breakpoint event. A canonical `func_80003728` call could produce the same state difference.
- A file22 code signature present does not prove file22 is currently executing; it may be stale after a loader unload.
- IDs 15 and 22 share a RAM destination, and the fingerprint refers to guest code bytes rather than a file-request ID.
- Capturing numerical states and map IDs does not by itself assign a narrative gameplay-mode label. Keep external user-observed action markers separate from ROM-proven numerical fields.
- Host polling may miss short transitions, and a stable double read cannot detect every concurrent instruction or transient state change.

**No accepted C functions, ROM, ELF or relocation changes are made by this research.** Related static atlas draft PR #155 and native dispatcher draft PR #152 stay independent.
