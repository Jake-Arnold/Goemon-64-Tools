# Matching C reconstruction track

**Continuing work? Start with [CONTINUE.md](CONTINUE.md)** for current paths,
next targets, verification commands and publishing steps. Historical counts below
describe their named checkpoint; current evidence is `results/combined.json` and
`results/inventory.json`.

This directory contains reconstructed C and repeatable matching evidence. It is
separate from the Python companion, autosplitter and existing portable C core.
No game assets, ROMs, generated assembly, object files or saves are included.

Current verified total: **109 functions / 7,788 function bytes across twenty-four units**.
The combined baseline/C-replacement whole-ROM match is recorded in
[combined result metadata](results/combined.json).

The [whole-build inventory](INVENTORY.md) identifies **7,376 function entries**:
**122 matching C entries** (13 upstream plus these 109), leaving **7,254 assembly
entries**, including SDK/runtime code. Exported jump labels are excluded.

## Screen-rectangle bounds helper

`viewport_bounds.c` replaces `func_800216B0_222B0` (144 bytes) with C and passes
the complete original-ROM gate alongside all previous units. It rejects negative
left/top bounds, right beyond 320, bottom beyond 240, and inverted rectangles
before updating four stored bounds. Equal bounds are accepted. Host tests cover
boundary acceptance and rejection without partially changing state:

```bash
gcc -std=c11 -Wall -Wextra -Werror -fsanitize=address,undefined \
  -Idecomp/test_support decomp/viewport_bounds.c decomp/test_viewport_bounds.c \
  -o /tmp/goemon-viewport-test
/tmp/goemon-viewport-test
```

`warp_state.c` adds three exact 16-byte setters for the byte at `0x800C7A95`,
writing values 2, 1 and 3. Their original numeric symbols are retained pending
complete consumer tracing. They are original-engine replacements, not new toolkit
warp controls; all existing direct-warp restrictions remain in place.

Ghost Toys entrance reconstruction is tracked separately in
[GHOST_TOYS_CHECKPOINT.md](GHOST_TOYS_CHECKPOINT.md). It is not counted as matching C.

## Scheduler/audio slices and collectible parameters

`scheduler_views.c` reconstructs two opaque interior-address helpers at offsets
`+0x78` and `+0xB0`; no complete scheduler-object layout is inferred.
`audio_state.c` reconstructs the original byte flag update conditioned on state
`0xF0`. All three pass the whole-ROM gate. To preserve exact lengths around their
four-byte-aligned boundaries, the manifest names only the adjoining assembly
objects for GAS `--no-pad-sections`. This removes assembler-added section tail
padding, not original instructions; independent MIPS integration tests verify the
instruction payload is unchanged. The exact image/symbol gates remain mandatory.
The latest build report records the verifier source hash; older benchmark hashes
remain historical rather than being rewritten to imply a new benchmark run.

The read-only command:

```bash
python -m decomp.pickup_placements --rom /path/to/USA.z64 \
  --report practice/diagnostics/new-pickups.json
```

extracts only instantiated
Mr. Elly Fant/Mr. Arrow definition flags. [Static metadata](results/castle_pickup_placements.json)
covers all ten pickups, corroborates three user observations and adds seven
placement-derived catalog entries without claiming live collection tests.

## Key spawn candidate

[Key/lock code trace](../docs/KEY_LOCK_CODE_TRACE.md) identifies the permanent
pickup flag as the key's no-respawn condition. `candidates/key_spawn_gate.c`
matches all 96 original instruction bytes in an isolated linked probe and has
host control-flow tests. It is excluded from the matching manifest/count until
original-overlay integration passes the full-ROM gate. The carried-key count's
storage/computation remains unconfirmed.

## Fortune Doll reward trace and static catalog

[DOLL_REWARD_TRACE.md](DOLL_REWARD_TRACE.md) connects user-tested pickup flags to
the silver +1 script, separate progress/total words, post-dialogue callback and
already matched four-quarter health helper. It corrects the earlier silver/gold
callback attribution without inflating function counts. The new numbered-event
starter adds 120 fully verified C bytes; resource fields now have supported names.

`pickup_placements --kind dolls` extracts 44 static placements using 43 distinct
saved flags, including a shared normal/unused Zazen variant. The catalog adds the
40 not already user-mapped flags with placement-derived evidence, plus the native
Turtle Rock reward record. The Shishi-odoshi dynamic
spawn is now traced as well, completing [45 flag records](results/fortune_doll_catalog.json):
40 silver and five gold. This is room/native-code evidence, not 45 live pickup tests.

## Controller input and two-point angles

`func_8003D17C_3DD7C` now has full-ROM-matching C (404 bytes). It uses the existing
upstream `CONTROLLER_W` type: context 1/2 copies the corresponding complete pad
record; context 3 ORs status/held/pressed buttons and sums/clamps raw axes to
[-128,+128], leaving float/padding fields alone. Other contexts leave the snapshot
unchanged. Host models verify the real 24-byte controller layout and system offset
without bundling the complete SDK header. Existing VM input readers now use those
characterized field names; their machine code remains identical.

`trig_angles.c` adds `func_8000EC04_F804` (176 bytes), from the expanded batch's
single new linked match. It uses relative XYZ, planar magnitude, the existing
angle helper, a 10-bit first-angle mask and the unmasked second angle. Host stubs
verify argument wiring, sign/zero handling and output conventions; the actual
full native function is checked against the original ROM.

## Batch discovery and matching

The [batch workflow](BATCH_PIPELINE.md) now provides a persistent queue, concurrent
C generation/compilation, bounded search and relocated function-byte probes.
Review candidates remain separate from verified matching C. Reports and review
bundles preserve failed work and identify missing type/data-layout information.
The whole-ROM verifier can reuse a certified baseline while still creating and
checking a fresh candidate for each reviewed batch.

## Event/dialogue VM helpers

[VM_CHECKPOINT.md](VM_CHECKPOINT.md) documents 52 matching functions in the 69-function
event/dialogue unit. The remaining 17 functions, including the dispatcher,
comparator and remaining operand handlers, remain assembly and are excluded.
The native comparator's host-only semantic model is explicitly not counted.
The first three reconstructed units below are still complete matching C.

The [local-checkout review](LOCAL_MNSG_REVIEW.md) records useful pre-existing
tools/builds and camera-branch work, including why the camera draft is not yet
part of the matching baseline.

## Save/resource unit

`save_resources.c` reconstructs all ten routines from ROM `0xC1D0..0xC4F0`:
save/live/shadow buffer synchronization, default save initialization, shadow
restoration, elapsed-time accounting, health upgrades and small counter routines.
`save_resources.h` gives byte-offset layouts names only where supported; unknown
fields retain offset-based labels. This is not a complete recovered save schema.

**`func_8000B718_C318` now matches as C**, after local decomp-permuter assistance,
full-unit compilation and a fresh whole-ROM check. It copies six selected spawn
record fields into the saved state, copies live resources into the save mirror,
applies the original saved health/lives minimums, then copies the complete save
to its shadow. The index is unchecked; this routine is not a safe scene loader.
The former 24-function/one-placeholder checkpoint is retained separately for
provenance. No assembly placeholder remains in those first three units; the new
VM unit is deliberately mixed C/assembly.

Behavior checks cover saved-view aliases, synchronization order, unchanged fields,
initial defaults, one-step timer/upgrade thresholds and callback order. The timer
routine consumes at most 60 ticks per invocation, and the health routine handles
one four-doll upgrade per invocation; neither was rewritten into a bulk loop.
These routines operate on unchecked engine buffers and are not a new safe-save or
scene-restoration API. The existing portable checkpoint implementation is unchanged.

## System initialization and byte-memory unit

`system_memory.c` replaces ROM `0x4D70..0x4E40` with three matching functions:
system initialization, byte zeroing and forward byte copying. It uses the pinned
upstream `SYS_W` type and preserves the system-buffer size `0xCF908`, global
system-pointer assignment, loading-byte reset and initial renderer-field values.

The byte helpers support nonnegative lengths and retain original forward-copy
behavior; they are **not memmove** and provide no general overlap/negative-length
safety. Zero-length operations make no accesses. The host test checks length 0,
1 and other boundaries, guards, source preservation, same/overlapping pointers,
and initialization against an opaque synthetic system layout with checked offsets.
No system initialization was executed against live game RAM.

## First verified unit

`event_flags.c` replaces upstream assembly unit ROM `0x249F0..0x24D60`:

- **12 functions / 876 function bytes**: set, clear, masked test and 100-byte reset
  operations for each of three flag banks. The unit also includes alignment.
- Additional banks begin at guest `0x80168E90` and `0x80168EF8`; their complete
  gameplay lifecycle/meaning has not been established. The known persistent
  event bank starts at `0x8015C608`.
- Test functions return the **mask**, not a normalized boolean. Set operations
  are idempotent ORs; clear operations retain unrelated bits. Signed division,
  byte casts and shift narrowing are preserved for instruction matching.
- These engine routines are unchecked. Host semantic tests cover the 800 valid
  primary-field bit IDs for each bank, not negative/arbitrary IDs or a new public
  memory-edit API. No companion controls are wired to this code.

The full upstream baseline rebuild and the candidate with this C unit both
produce **the same complete 32 MiB decompressed ROM**:

```text
SHA-1: 6ea0ed71032ce08fc2745f412d84936382197494
```

All 12 linked function ranges and guest addresses match; their assembly-placeholder
markers are absent from the candidate ELF. The C object is present in the link
map. [Observed result metadata](results/event_flags.json) includes source hashes,
tool versions, whole-image identity and per-function matching hashes. It is local
build evidence, not independent third-party verification or an upstream merge.

## Provenance and scope

Pinned [mnsg](https://github.com/klorfmorf/mnsg/tree/7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee)
is the upstream layout/build baseline. Its supplied IDO 5.3 compiler and canonical
Makefile flags are retained. Function/global names are the upstream disassembler's
address-derived labels, not recovered original Nintendo/Konami source names.

The initial draft was assisted by upstream-pinned
[m2c](https://github.com/matt-kempster/m2c/tree/a21c1dcd7255b176c032bb932f521846e98d4372),
then reviewed, typed and adjusted against original instruction output. Draft
decompiler output is not itself counted as matching. Existing mn64rando annotations
and our earlier flag traces inform interpretation; they do not replace compiler
comparison. No third-party code/label dictionary is bundled by this directory.

This is a real matching-C increment, **not full game decompilation**. All untouched
upstream code/data still comes from its existing reconstructed sources, original
assembly or extracted assets. The whole-ROM match proves this replacement did
not change that binary; it does not mean the entire ROM has become C. No new
in-game behavior, playable port or published executable is claimed.

## Rebuild from a fresh local work directory

Run inside Linux/WSL with Git, build-essential/GCC, MIPS binutils and uv installed.
The upstream README documents its toolchain requirements. Tested here with WSL
Ubuntu, uv 0.13.6 and the pinned dependency lock using managed Python 3.12.
The verifier creates fresh baseline and candidate clones; it never resets or
deletes the supplied upstream checkout and refuses to reuse a work directory.

```bash
python3 decomp/verify.py \
  --upstream /path/to/pinned-mnsg-clone \
  --workdir /path/to/NEW-local-build-directory \
  --retail-rom /path/to/your-original-US-ROM.z64 \
  --report practice/diagnostics/NEW-matching-result.json \
  --uv /path/to/uv
```

The upstream clone must be at manifest commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
The original retail SHA-1 must be `df8083a54296b8c151917c5333e1c85f014a2a66`.
Keep the work directory and result report local/ignored. Python, tools and locked
dependencies may be downloaded by uv. On Windows invoke this Python script
through WSL; it deliberately refuses native Windows builds. No ROM is uploaded.

`manifest.json` selects the exact assembly/C configuration replacement and function
bounds. By default the verifier builds baseline first and checks its complete output;
optional certified-baseline reuse validates the same reference identities. It then
builds the C replacement, checks symbol identity and per-function bytes, and
requires another whole-ROM match. Reports are exclusively created; failed builds
retain logs/workspaces and record failure without claiming success. The verifier
does not run the game, merge changes or submit anything to upstream maintainers.
Explicitly declared retained-assembly functions remain excluded from the C count;
their presence does not relax byte/address checks on the claimed functions.

## Semantic and verifier checks

```bash
gcc -std=c11 -Wall -Wextra -Werror -fsanitize=address,undefined \
  -Idecomp/test_support decomp/event_flags.c decomp/test_event_flags.c \
  -o practice/diagnostics/test_event_flags
practice/diagnostics/test_event_flags
python -m unittest tests.test_decomp_verify -q
```

The host C test uses synthetic banks and verifies all 800 flags in each bank,
set/clear idempotence, exact test-mask returns, adjacent-byte/other-bank isolation
and exact 100-byte reset boundaries with sentinel bytes. It is not an in-game
test. Python tests reject bad manifest bounds, source collisions, changed output,
wrong symbols/reference identity and remaining assembly markers. The existing
Python application suite is run separately.

The second unit's host check is:

```bash
gcc -std=c11 -Wall -Wextra -Werror -fsanitize=address,undefined \
  -Idecomp/test_support decomp/system_memory.c decomp/test_system_memory.c \
  -o practice/diagnostics/test_system_memory
practice/diagnostics/test_system_memory
```

The save/resource host check uses GNU symbol aliases to model overlapping views
inside synthetic save/system buffers, without copying Nintendo's SDK headers:

```bash
gcc -std=c11 -Wall -Wextra -Werror -fsanitize=address,undefined \
  -Idecomp/test_support decomp/test_save_resources.c decomp/system_memory.c \
  -o practice/diagnostics/test_save_resources
practice/diagnostics/test_save_resources
```

The host test now includes the spawn-copy routine, three synthetic table records,
all field destinations, signed coordinate encodings and clamp/copy ordering.
Matching MIPS output, synthetic host behavior and actual in-game tests remain
separate evidence.

The VM host test command and model-versus-native evidence limits are documented
in [VM_CHECKPOINT.md](VM_CHECKPOINT.md). It requires non-PIE host compilation for
the original encoded 32-bit indirect operand interface.

## Assignment jump-table layout

The assignment handler `func_8003DB0C_3E70C` now compiles to its original 224
instruction bytes. Its 15-entry switch table is regenerated by IDO and matches
all 60 original bytes at decompressed ROM `0x7DC2C..0x7DC68` after relocation.

The pinned candidate-only layout preset splits the original assembly rodata
around that table, lowers the main segment's subalignment to four, and assembles
only the preceding rodata object with `--no-pad-sections`. IDO rounds the new
C object's table section to 64 bytes; `elf_layout.py` validates its exact shape,
zero padding, all 15 MIPS relocations and symbol references before changing only
the ELF section header's logical size (64 to 60) and alignment (16 to 4).
The original object is preserved in an exclusive `.before-layout` backup.
No payload, instruction, table entry, relocation or symbol is modified. The
verifier records object hashes, layout evidence and the final linked-table hash,
then still requires every claimed function and the entire ROM to match.

This is an explicit mixed C/assembly layout adaptation, not an unmodified
upstream build recipe. It accepts only the pinned handler/table shape and is
covered by synthetic-object rejection/preservation tests. The earlier 42-function
checkpoint remains in [vm_helpers.json](results/vm_helpers.json).

## Next units

Continue with small, well-bounded engine translation units and retain the same
full-ROM comparison gate. Continue the event VM and its operand/branch handlers,
and review the pre-existing camera branch without assuming it already matches.
Actor and
script exports from the existing randomizer remain useful semantic context;
native reconstruction still requires compiler matching and tests. Do not rename
unknown fields or infer state-transition safety from a matching helper alone.
