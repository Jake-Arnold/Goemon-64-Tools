# VM parser behavior matrix

**G64-039 research checkpoint — 2026-11-11.** This matrix composes existing
ROM-bound traces and host tests for the VM stream readers and decoder boundary.
The private decompressed USA image used for the differential run is pinned by
SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. It records tested callback
contracts; it is not a playable VM emulator, live-game trace, or matching-C
claim.

## Behavior coverage

| Boundary | Original evidence and test | Expected trace / covered paths |
| --- | --- | --- |
| `func_8003DBEC_3E7EC` (DBEC) | 472 bytes / 118 words; ROM-bound CFG in [`VM_TEXT_LOOP_TRACE.md`](VM_TEXT_LOOP_TRACE.md); fixed cases in [`test_vm_text_loop_differential.py`](test_vm_text_loop_differential.py). | Ten named cases pin return cursor, VM state, bound, work latch, separate cursor-pointee halfword, and DE80/DE48/E680 callback counts. Cases cover nonpositive bound, held/pressed `0x8000`, pressed `0x4000` reset/zero paths, callback-lowered/raised bound, null return, terminal state and distinct `+0xA` storage. Existing two-seed 10,000-case runs and four killed mutants remain prior evidence; this task adds no large random run. |
| `func_8003DE80_3EA80` (DE80) | 232 bytes / 58 words; 24 ROM anchors and the 11-scenario host probe are cross-mapped in [`VM_STREAM_MATCHING.md`](VM_STREAM_MATCHING.md#G64-036--semantics-coverage-crosswalk). | `-1` returns null before suppression and preserves the repeat count; other negative values delegate to DF98 and return its configured cursor (including null); suppression returns the same cursor; nonnegative values emit and advance by one halfword, then use the callback-reread token and repeat setting to loop or return. The gate stub chooses each wrapper arm; it does not emulate DF68's counter decrement. |
| `func_8003DF98_3EB98` (DF98) | 528 bytes / 132 words; signed range, table, cursor advance and caller anchors are guarded by [`test_vm_control_decoder_original.py`](test_vm_control_decoder_original.py). | The host stub records owner and input cursor and returns a test-selected pointer. DE80 and EB34 tests assert the delegated input and resumed cursor. Token side effects stay opaque; the stub does not assign command meanings or mutate unrelated globals. |
| `func_8003EB34_3F734` (EB34) | 112-byte caller range in the same ROM guard; production C remains independently matched. Direct host assertions are in `test_script_vm.c::check_choice_stream_rendering`. | `[0, 0x7fff, -2, -1]` produces emit, emit, decode at `first+2`, then emit from the decoder-selected cursor; owner remains 17 and `-1` stops. `[-1]` makes no calls. Signed `0x8000` delegates at the initial cursor. The test now asserts event order as well as values and callback arguments. |
| `func_8003F6E8_402E8` (F6E8) | 48 bytes / 12 words and two final `jr $ra; nop` pairs; checked by [`test_vm_wrapper_extent.py`](test_vm_wrapper_extent.py). | Extent-only guard. No C prefix or fabricated behavior is used to model the wrapper. |
| `func_8003ED60_3F960` (ED60), adjacent dispatch callback | 592-byte ROM trace and caller guard in [`VM_ED60_TRACE.md`](VM_ED60_TRACE.md); dispatcher coverage is `test_script_vm.c::check_new_vm_dispatch_and_callback`. | The C harness asserts when the dispatcher calls the ED60 stub. The stub only increments a count; it does not model ED60's output writes. Original trace evidence records twelve cursor updates, not their higher-level meaning. |

The DBEC fixed-trace tuple order is `(returned cursor, VM state, bound, work
latch, independent script-pointee halfword, DE80 calls, DE48 calls, E680
calls)`. The expected values live next to the cases in
`EXPECTED_FIXED_TRACES`, so a new fixed scenario must add its trace as well as
its differential comparison.

## Mock boundary and result

- DBEC's DE80, DE48 and E680 hooks use synthetic state changes configured by
  the test. A passing MIPS-interpreter/host-C comparison checks that model
  against the pinned instructions; it does not establish the helpers' complete
  retail effects.
- DE80's D060 stub records the emitted value. Its DF68 stub selects the gate
  result to reach both wrapper branches. DF68's known C body decrements
  `D_801C77A0` when at least two remain; it does not write
  `D_801C7798`. No unsupported gate mutation is tested.
- DF98's configured returned pointer lets its callers' cursor behavior be
  tested. Decoder command effects remain unknown wherever the original trace
  does not establish them.
- No new parser C candidate, native IDO comparison, full-ROM build, inventory
  rebuild, or in-game run was needed. Production ownership and the stored
  148-function proof remain unchanged.

**Classification:** `RESEARCH_ONLY`; see
[`plans/execution/2026-11-11-g64-039-parser-matrix.json`](plans/execution/2026-11-11-g64-039-parser-matrix.json).
