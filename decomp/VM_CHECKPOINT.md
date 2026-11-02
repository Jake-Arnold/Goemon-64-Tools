# Event/dialogue VM reconstruction checkpoint

Date: 2026-11-02. Pinned mnsg baseline and ROM identity are unchanged.
**18 matching VM functions / 992 function bytes**, bringing the track to
**43 matching C functions / 2,868 function bytes**. The full 32 MiB baseline and
candidate both match decompressed SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
Current source hashes, guest addresses and byte-range comparisons are in
[combined.json](results/combined.json). The previous complete-save checkpoint is
retained as [save_resources_complete.json](results/save_resources_complete.json).

## Selected unit and evidence boundaries

The original `0x3DBA0..0x40320` unit contains 69 functions. `script_vm.c` replaces
18 functions and retains 51 explicitly declared assembly functions. The main
dispatcher, remaining operand handlers and comparison routine remain
assembly; the complete VM is not decompiled. A name appears in the matching count
only when linked guest address, original bytes and absence of its assembly marker
all pass, alongside the complete ROM identity check.

| Matching helper(s) | Recovered operation |
| --- | --- |
| `func_8003CFA0_3DBA0` | Indexed pointer lookup with fallback; table contents/format not newly characterized |
| `func_8003CFD0_3DBD0` | Decrement initial delay; afterward step VM, then update drawing |
| `func_8003D01C_3DC1C` | Store owner pointer, reset context, install callback, initialize delay to five |
| `func_8003D058_3DC58` | Create/register the initialization callback |
| `func_8003D080_3DC80` | Cleanup, release stored owner, then clear owner pointer |
| `func_8003D428_3E028` | Reset wrapper passing `0, -1` to the retained initialization routine |
| `func_8003D44C_3E04C`, `func_8003D45C_3E05C` | Set/clear raw VM pause/gate byte |
| `func_8003DB0C_3E70C` | Consume destination/opcode operands; immediate stores (`8009/8016/8017`), wrapping add/sub (`8013/8014`), relocated indirect copy (`8015`); unknown modes consume no value |
| `func_8003DE48_3EA48` | Preserve negative encoded addresses; conditionally relocate nonnegative values using active-context delta |
| `func_8003DF68_3EB68` | Consume one repeat count only when at least two remain |
| `func_8003E548_3F148`, `func_8003E5B8_3F1B8` | Start external dialogue/render operations, set state 5/6, then poll |
| `func_8003E5EC_3F1EC`, `func_8003E620_3F220` | Return to state 1 when the external poll reports zero |
| `func_8003E654_3F254` | Decrement countdown; clamp to zero and clear state when finished |
| `func_8003EA0C_3F60C`, `func_8003EBA4_3F7A4` | Original no-operation hooks |

Raw engine preconditions are preserved: no new pointer/index/length safety API is
introduced, and callbacks are not wired into the running companion. This is
original-ROM C reconstruction, not a new native PC port.

## Assignment handler increment

`func_8003DB0C_3E70C` replaces another 224 assembly bytes. In indirect-copy
mode the source operand cursor advances after address resolution and the load;
that ordering is required for the original IDO code match. The handler preserves
raw pointer preconditions and is not exposed as a new live-memory operation.
Synthetic host tests cover literal modes, wrapping arithmetic, indirect and
self copies, active/inactive relocation, unknown-mode cursor lengths and guards.

Its regenerated 15-word jump table requires the narrowly validated metadata-only
layout adjustment described in [README.md](README.md#assignment-jump-table-layout).
Whole-ROM equality includes the table and every retained assembly function/data
range. The prior [42-function checkpoint](results/vm_helpers.json) remains intact.

## Jump-table label compatibility

The first mixed-unit build exposed unresolved external jump labels from retained
assembly handlers. The vendored asm-processor understands exported `glabel`
labels; its default handling did not retain the original `jlabel` exports needed
by the separately assembled jump tables.

The candidate's Splat configuration therefore uses the narrow override
`asm_jtbl_label_macro: glabel`. This changes generated label declarations, not
jump-table entries or instructions. The baseline remains unmodified. The verifier
allows only this documented override and tests its candidate-only application.
Afterward the original retained handlers and tables link, and the exact whole-ROM
match verifies that their binary contents/targets remain unchanged.

No linker-address alias, instruction patch, raw RAM restore or runtime transition
shortcut was used to make the checksum pass.

## Comparator remains assembly; model is not counted

`func_8003D9B8_3E5B8` compares signed operands in six immediate modes and six
indirect modes. The source drafts passed semantic cases but did not achieve exact
native output. Local, bounded two-worker permutation/manual runs improved the
draft substantially; the closest inspected form still differed in return
sequencing. No zero-score/equivalent-code claim was substituted for exact bytes.

The native candidate retains the original comparator assembly and marker.
`vm_compare_reference.h` is included **only by host tests**, explicitly excluded
from the 18/43-function counts. It is a semantic aid for subsequent work, not a
published matching reconstruction or production evaluator. Retained assembly
also includes the dispatcher and assignment/operand decoders.

Indirect comparison modes use a raw encoded 32-bit address. The original path
also loads an indirect word for unknown modes before returning false; unknown
inputs must not be assumed safe. Host tests provide a valid low-address synthetic
operand and compile non-PIE so the pointer fits the original 32-bit interface.
This does not solve general 64-bit portability or make arbitrary script operands
safe to evaluate.

## Validation

- Fresh verifier baseline and combined candidate builds both passed the full ROM
  check; all 43 claimed function ranges/addresses matched without assembly markers.
- **223 Windows Python unittest tests passed**, including declared-assembly exclusion and
  the narrow Splat-label override. The comparator is asserted to remain excluded.
- Sanitizer-enabled synthetic VM tests passed pointer fallback, five delayed
  callback invocations, step/draw ordering, initialization/cleanup order, gate
  toggles, repeat/countdown thresholds, seven-argument forwarding and state/poll
  transitions.
- The host comparator model passed 588 signed immediate/indirect comparisons
  across seven operand values including `INT_MIN`/`INT_MAX`, plus valid-address
  unknown modes. The matching relocation helper passed inactive, direct-negative,
  active and 32-bit wrapping cases. The remaining signed countdown-overflow case
  is outside the characterized engine inputs.

```bash
gcc -std=c11 -Wall -Wextra -Werror -fno-pie -no-pie \
  -fsanitize=address,undefined -Idecomp/test_support \
  decomp/test_script_vm.c -o practice/diagnostics/test_script_vm
practice/diagnostics/test_script_vm
```

No game writes, live callback calls or rebuilt-ROM runtime launch were performed.
The referenced generic callbacks/render routines are stubs in host tests. Original
ROM data, generated assembly, full local logs and failed drafts remain ignored.

## Next work

Resolve the comparator's exact control-flow/return form and reconstruct the
remaining operand handlers while retaining their table data/layout correctly.
Only after those primitives pass should the central dispatcher replace assembly.
Use existing mn64rando opcode definitions and independently traced accesses to
interpret behavior; do not infer story semantics from helper names alone.
