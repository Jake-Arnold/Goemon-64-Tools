# USA Impact battle controller and cockpit HUD

## Provenance and ownership

The seven watched pointers are **fixed roles in the shared Impact cockpit
HUD**. Their targets are generic render-model records from the engine's
192-entry type-2 pool. The boss task is tracked elsewhere, including controller
`+0x1D8` on the five traced boss-selection paths. The controller holds the
HUD pointers, resources and camera fields in one allocation.

This investigation used research base
`10a3599b01ea6de4b3b1af44c0e81e3c8cb16366` on `origin/chatgptweb/decomp`,
pinned `mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, USA retail
SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`, and decompressed SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`. The supplied Recomp recording runs
57.233 seconds. The runtime evidence here comes from that recording and the
user's earlier observations. Live execution, write breakpoints and target
payload reads were outside the evidence collected.

**Owner:** file-table ID 13 / Splat `file_13`, static overlay at
`0x801CB460`. The retail interval `[0x5BF7E4,0x603254)` is byte-identical to
decompressed `[0x5F6840,0x63A2B0)` (277,104 bytes). Its text ends at
decompressed offset `0x634E30`. The live file table at ROM `0x556CC` gives
room through `0x8020EF50`. The overlay's initialized data ends at
`0x8020EED0`, where its BSS begins. That address holds the controller pointer.
The `_63A2B0` suffix in the generated symbol is the file boundary, and the
pointer's live value is written by `801CB770`. It is a BSS slot in a reusable
overlay window. Only trust it while file 13 owns the window.

`80020440` chooses overlay IDs by system submode using a table at ROM
`0x6C33C`. Entry 5 selects `(13, 0)`, as does entry 9. The call at
`800204C4` reaches `800203D4`, whose first-overlay load calls
`80001C00` at `800203FC` with destination `0x801CB460`. Keep that loader
selection distinct from the UI's sampled gameplay submode and from the
boss-selector halfword at `0x800C7AB4` (system base `+0x3ADF4`). The
recording does not display those internal selectors. The strongest code
match for the observed 1,000-HP setup is selector 3.

### Why the address repeats

- `800020B8` and the transition helper `8000383C` call `800148C0` with
  `(system + 0xC7FA4, 0x802F7000, 0xA000)`. The original byte loop at
  `800148C8..800148DC` clears the arena. `800148E0..800148EC` writes base,
  length and null allocation-list head to the descriptor at `0x80154C64`
  for system base `0x8008CCC0`. File 17's entry at `8020D2E8` is another
  verified caller of the same reset.
- `801CB6AC` requests `0x2D0` bytes from this descriptor at `801CB748`
  and stores the result in the overlay BSS at `801CB770`.
  `800148F0` scans low addresses for a fitting gap, with total block
  size `(requested + 0x4F) & ~0x3F` and a trailing `0x10`-byte header.
  The request therefore reserves `0x300` bytes and the allocator clears
  `0x2F0` payload bytes. With an empty descriptor it returns `0x802F7000`,
  explaining the observed stable address. With other live allocations the
  returned address can differ.
- The initializer copies `0xA0` template bytes from `0x80209AFC`
  (decompressed ROM `0x634EDC`) to the returned block at
  `801CB7B0..801CB7E0`. The watched pointers, control, charge, gauge
  alternate value and three floats start at zero in this template.
  The template seeds HP/Ryo/oil at 64/200/500. Subsequent stores in the
  same initializer and the boss-specific initializers override those seeds.

## Memory map

`B` is the pointer read from file 13 BSS at `0x8020EED0`. The table gives
the observed addresses when `B = 0x802F7000`. Offsets in the first column
are relative to the requested watch base.

| From `B+0x40` | Observed address | Guest type | Meaning and original evidence |
| --- | --- | --- | --- |
| +00 | 802F7040 | u16 | HUD reaction/visibility mode. `sh` at `801CDFDC` and `801CE234`, `lhu` at `801CE9AC`. High confidence in the rendering effect, exact video event branch unverified. |
| +02 | 802F7042 | unknown 2 bytes | Zero in initial template and sampled paired word. No controller access identified. Preserve as opaque bytes. |
| +04 | 802F7044 | object pointer | Enemy HP high two digits. Constructor store `801CD9DC`, digit arguments at `801CE8F4` and `801CE914`. |
| +08 | 802F7048 | object pointer | Enemy HP low two digits. Constructor store `801CDA7C`, digit arguments at `801CE940` and `801CE95C`. |
| +0C | 802F704C | object pointer | Ryo three digits. Constructor store `801CD88C`, reader `801CE698` and digit calls from `801CE700`. |
| +10 | 802F7050 | object pointer | Oil three digits. Constructor store `801CD93C`, reader `801CE780` and digit calls from `801CE7E8`. |
| +14 | 802F7054 | object pointer | Charge gauge model. Constructor store `801CDB2C`, selected charge drives object float `+0x28` at `801CEA84` and switches render descriptors. |
| +18 | 802F7058 | object pointer | Cockpit auxiliary model. Constructor store `801CDBE4`. Updated for transform and animated `+0x28` at `801CEB60..801CEC54`. Exact visible mesh unverified. |
| +1C | 802F705C | object pointer | Cockpit auxiliary model. Constructor store `801CDC90`. Updated for transform, animated `+0x28` and visibility at `801CEC5C..801CEE68`. Exact visible mesh unverified. |
| +20 | 802F7060 | s32 | Enemy HP. `lw/sw` at `801D395C/801D3968`, signed zero floor. HUD reads at `801CE83C` and splits four decimal digits. |
| +24 | 802F7064 | s32 | Ryo. `lw/sw` at `801D820C/801D8214`, signed positive guard at `801D81B0`. HUD reads at `801CE698`. |
| +28 | 802F7068 | s32 | Oil. `lw/sw` at `801D38AC/801D38BC`, signed comparisons clamp to 0–999. HUD reads at `801CE780`. |
| +2C | 802F706C | s32 | Charge. `lw/sw` at `801CEE88/801CEE98`, signed comparisons clamp to 0–100. HUD reads at `801CE9EC`. |
| +30 | 802F7070 | s32 | Alternate charge-gauge input. `lw` at `801CE9DC`, signed `cvt.s.w`. Selected when controller byte `B+0x14A` equals 1. A branch in `801D7BC8` sets that byte and clears this word at `801D7DFC`. Full lifecycle unverified. |
| +34 | 802F7074 | f32 | Smoothed horizontal camera angle in degrees. `lwc1/swc1` at `801CC3F0/801CC470`. |
| +38 | 802F7078 | f32 | Smoothed vertical camera angle in degrees. `lwc1/swc1` at `801CC44C/801CC484`. |
| +3C | 802F707C | f32 | First component of derived camera vector. `swc1/lwc1` at `801CC608/801CC630`. Siblings at `B+0x80/+0x84`. |

All seven pointer stores are `sw` through the same saved base register.
All four counter words are signed-arithmetic candidates in C. Unsigned
toolkit display remains equivalent across the observed nonnegative domain.
The watches at `7062/7066/706A/706F` sample the low halves or low byte of
those words in big-endian memory.

A partial C layout for documentation (guest pointers represented as
32-bit integers so offsets also hold in a 64-bit analysis process):

```c
typedef uint32_t GuestPtr32;
typedef struct {
    uint8_t unknown00[0x2e];
    uint16_t cockpit_reaction;      /* B+0x2e, HUD switch */
    uint8_t unknown30[0x10];
    uint16_t hud_visibility_mode;   /* B+0x40 */
    uint8_t unknown42[2];
    GuestPtr32 enemy_digits_high;   /* B+0x44, type-2 object */
    GuestPtr32 enemy_digits_low;
    GuestPtr32 ryo_digits;
    GuestPtr32 oil_digits;
    GuestPtr32 charge_gauge;
    GuestPtr32 cockpit_aux_58;
    GuestPtr32 cockpit_aux_5c;
    int32_t enemy_hp;              /* B+0x60 */
    int32_t ryo;
    int32_t oil;
    int32_t charge;
    int32_t alternate_gauge_value;
    float camera_yaw_deg;          /* B+0x74 */
    float camera_pitch_deg;
    float camera_vector[3];        /* B+0x7c..0x84 */
} ImpactControllerPrefix;
```

## The seven records

`80035B50 → 80035BF8` builds the pool with 192 entries (`slti 0xC0` at
`80035C4C`). The head of type 2 is written to `0x8016DAC8`, value
`0x80148850`. The loop writes the first word of record `i` at
`0x8008CCC0 + 0xB8000 + 0x3B90 + 0x98*i`, setting it to the next
record's address `0x8008CCC0 + 0xBBC28 + 0x98*i`. The slot range is `[0x80148850,0x8014FA50)`. This loop writes the successor
value even for the last slot. The capacity table at ROM `0x6DF54`
also says `0xC0`, and the allocation wrapper checks the in-use count
at `0x8016DADC`. Bounds for an external trace come from the pool extent,
independently of the successor value.

`801CD684` is a one-time cockpit model constructor. `801CC89C` creates
a task with that callback through `80035854` at `801CCA18`. The constructor
first creates two other models stored at controller `+0x20/+0x28`.
It then calls `8000DBF0` once per role in the order below, sets target
byte `+0x05` to 10, and replaces its own callback with
`801CDD10` at `801CDCE8`.

| Creation order among seven | Controller offset | Store VMA | Observed target | Pool index |
| ---: | --- | --- | --- | ---: |
| 1 | +4C | 801CD88C | 801498F0 | 28 |
| 2 | +50 | 801CD93C | 80149988 | 29 |
| 3 | +44 | 801CD9DC | 80149A20 | 30 |
| 4 | +48 | 801CDA7C | 80149AB8 | 31 |
| 5 | +54 | 801CDB2C | 80149B50 | 32 |
| 6 | +58 | 801CDBE4 | 80149BE8 | 33 |
| 7 | +5C | 801CDC90 | 80149C80 | 34 |

The constructor allocates the Ryo and oil digits first, then the two enemy
digit models, while the controller lays out enemy digits first. That
permutation exactly explains the recording. Seven is the count of these
named fields, hard-coded by the shared HUD constructor. The enclosing
model pool has 192 slots and the same constructor creates two preceding
models outside the seven. The slot indices describe this recorded
allocation sequence. `80035FDC` returns records to the free-list head,
which permits a different slot order after reuse.

`8000DBF0 → 80035EEC(owner, 2, 1) → 80035D8C(2)` pops a record,
clears its `+0` link, and attaches it to the owner's model list via owner
`+0x18/+0x1C`. Constructor and updater accesses establish repeated fields
within every target. This layout is recovered from code rather than from
a live dump of the targets:

| Record offset | Type and use | Evidence |
| --- | --- | --- |
| +00 | 32-bit intrusive next link | `80035DB8` reads free successor, `80035DCC` clears it, `80035FAC` links a previous model to the new one. |
| +04, +05 | Byte pool metadata and render category | `80035DC8..80035DD8` clears bit 7 of `+04`. The seven HUD allocations use category 10 at `+05`. |
| +08..+10 | Three f32 translation components | `8000DC48/50/58` populate them. `8000DD04` copies them from the HUD parent transform. |
| +14..+18 | Three u16 orientation components | `8000DC60/68/70` populate them. The HUD reaction switch wraps angles at `0x400`. |
| +1C..+24 | Three f32 scale components | `8000DC78/80/B0`, copied by `8000DD04`; HUD code divides these floats to size some models. |
| +28 | f32 model parameter | Initialized at `8000DCA0`. In the gauge record, `801CEA84` stores normalized charge. The other two auxiliary objects have independent animation updates. |
| +2C, +30 | 32-bit model reference and render data pointer | `8000DC2C/3C`. HUD swaps the gauge's `+30` descriptor at full charge, e.g. `801CEAD8` and `801CEAE8`. Treat model references as engine handles unless their address space is validated. |
| +3C | u16 per-instance tag | `8000DCC0`. The seven constructor calls supply `0x04A8`. |
| +64 | Byte visibility/suppression control | Initialized to zero at `8000DC88`. HUD writes 1 in gated paths, e.g. `801CE9C4`. |
| remaining | Opaque within stride 0x98 | Use the constructor and render consumers to refine individual fields. |

## MIPS call graph and battle state

Arrows below denote direct calls unless described as callback registration.
VMAs refer to file 13 where applicable. The address mapping in that overlay
is `ROM_decompressed = 0x5F6840 + (VMA - 0x801CB460)`.

| Path | Original edges and effects |
| --- | --- |
| Overlay and arena | `80020440 → 800203D4 → 80001C00`; file 13 entry `801CB460` dispatches a three-entry table at ROM `0x634E30` with system byte `0x800C7A9E`. Entry 0 is `801CB4C4`, which schedules `801CB6AC` directly or through `801CB620 → 801CB65C`, and calls the pool initializer `80035B50`. |
| Shared controller | `801CB6AC → 800148F0`, then template copy, resource seeding and registration of shared tasks `801CC078` (camera), `801CC89C` (cockpit), and `801D0260` (boss setup), among others. Ryo/oil stores at `801CBCE0/EC`, `801CBD0C/10` and `801CBD28/30` select carried resources or the 200/500 pair. Resource branches also seed carried values 200/400 at `801CBC20/24` and `801CBC78/7C`. |
| Per-boss setup | `801D0260` indexes five entries by `u16 0x800C7AB4`. From ROM `0x638588`, indices 0–4 call `801E45B4`, `801EEB3C`, `801F7088`, `801FFE80`, `801FFF70` respectively. Indices 1 and 2 write 2000 directly at `801EEBFC` and `801F7148`. Index 0 schedules `801E41F0`, which clears the shared HP field at `801E4298`, then installs `801E42D4`, which can increment that word at `801E4344`. Its encounter role needs a runtime label. Index 3 schedules `80200200`, which writes 1000 at `80200308`, consistent with the recorded Balberra start. Index 4 schedules `801FAEB0`, which writes 2000 at `801FB0A8`. The clip does not show the selector or execute the initializers under a debugger. |
| Model setup and HUD update | `801CC89C` schedules `801CD684`, then `801CD684` installs `801CDD10`. `801CDD10 → 8000DD04` updates model transforms and `→ 8000E23C` writes selected digit descriptors. It reads HP, Ryo, oil and charge directly from the controller and configures the gauge. The numeric labels thus have a direct controller-to-model data path. |
| Firing and charge | `801D06E4 → 801D7670 → 801D8184` on the normal Ryo shot path. On successful projectile creation (`801DAFCC` returns 1), `801D8200` calls `801CEE80(+1)` and `801D8214` spends one Ryo. Other paths call the signed clamp with different deltas, including `+5` at `801D28CC` and `-1` at `801DE368`. |
| Damage and outcomes | `801CDD10 → 801D27BC → 801D38A4` resolves a cockpit hit and subtracts oil. When oil becomes zero, `801D2B50` sets `B+0x2C4 = 2`. The index-3 enemy hit path in `801FFAAC` calls `801D3954` at `801FFD6C` to subtract HP and `801D3A18` at `801FFD74` to test for zero. Several boss scripts set `B+0x2C4 = 1` (e.g. `801FE41C`). `801CBE3C` dispatches different per-boss exits for outcome 1 and 2. |
| Camera | `801CC078` installs `801CC10C`. It updates the camera state inside the same controller. `801CD2E8` reads the angles again at `801CD3C0` and `801CD424` as offsets for aim bounds. |
| Free and scene reuse | File 13 entry phase 2 selects `801CB5C0`. Its call at `801CB5E8` passes the controller pointer and arena descriptor to `80014B74`. The helper unlinks the allocation and zeroes its former extent via `sb` at `80014BE8`. `801CB604` sets the overlay exit byte at system `+0x3ADDF`, which `80002EFC` consumes before requesting transition 3. The cleanup call leaves the saved BSS pointer value in place, so an address-range check alone cannot establish liveness. |

The arena reset and template explain the two stages of zeroes, before
allocation and after allocation but before HUD construction. The
resource writers run during setup and the HUD constructor is scheduled
independently. In the sampled video frames, 5 s and 23 s already show
1000/200/400/0 with zero watched pointers, and 26 s shows populated pointers
and 1000/196/400/4. This pins the constructor to the intro-to-combat interval
in the recording. The exact script event and frame gating its execution
remain open.

### The transient halfword

The observed `0x00010000` is consistent with a big-endian halfword 1 at
`B+0x40` and a zero lower halfword. The parent HUD update reads a reaction
selector at `B+0x2E`. Cases 3–10/21 in the ROM jump table at `0x6383D4`
drive pose changes. Multiple reaction cases set the visibility mode to 1
with `sh`, and the normal/default path clears it at `801CE57C`.
Reads at `801CE9AC`, `801CEC40` and `801CEE54` suppress the gauge and
auxiliary objects for a positive value. Other numeric models use a threshold
of 2 at `801CE74C`, `801CE830` and `801CE96C`. Hit processing can set
the reaction selector, including case 9 at `801D2844` or case 6 at
`801D28DC`. Thus the halfword controls how the cockpit renders during a
reaction. The recording shows a hit/flame sequence while charge stays full.
The exact case and writer that executed on that frame still need a trace.

### Camera calculation

The degree-to-radian constants in ROM `0x6382A0..0x638320` include
`pi` and `180.0`. In `801CC10C` the angle pair converges toward control
targets and is clamped on the ordinary camera path. The code constructs
the three-component vector at `B+0x7C/+0x80/+0x84` from sine and cosine.
The ordinary branch writes the vector to the second triplet at
`B+0xAC/+0xB0/+0xB4` (`801CC640/648/660`) with the first triplet zero.
The alternate branch writes the vector into the first triplet
(`801CC874/87C/884`) and uses the separate distance word at `0x8020EED8`.
The watched three floats therefore span two angles and one Cartesian
component. The normal path uses the relation
`vector_x = -100 * cos(pitch_deg * pi/180) * sin(yaw_deg * pi/180)`.

| Video sample | Yaw | Pitch | Observed vector x | Predicted x |
| ---: | ---: | ---: | ---: | ---: |
| 26 s | -17.03460 | -3.33747 | 29.24523 | 29.24523 |
| 47.5 s | -7.17721 | -6.10558 | 12.42298 | 12.42298 |
| 52.5 s | -5.98334 | -6.11666 | 10.36459 | 10.36459 |
| 55 s | 1.64211 | 11.37009 | -2.80939 | -2.80939 |

The calculation on these four sampled triplets agrees within
`2e-6` camera units. The sampled toolkit display reads oil **160**
at 52.5 s, with transient halfword 1, and still reads 160 at 55 s after
the halfword clears. The assignment's rough 180-at-52.5-s timestamp is
therefore approximate.

### Special activation and Game Over limits

Input handling at `801D83D8` reads and compares `B+0x6C` to 100 at
`801D8594..801D85A0` on the fallback availability path. The decoder can
queue actions `0x28/0x29` at `801D79FC/801D7A44`, and the action
dispatcher `801D7BC8` routes those cases to `801DDAF8` for the two
variants. The resulting attack task
starts at `801DDC70` and advances through `801DDD64`, which sets the
cockpit reaction to 1 at `801DDF24` and registers `801DDF8C` at
`801DDF60`. During that phase, `801DDFB8` calls `801CEE80(-1)` on
each update. Subsequent attack branches register `801DE354` or
`801DE9D0`, which also call `801CEE80(-1)` at `801DE368` and
`801DE9E8`. This verifies a drain during the special action. The update
that reaches zero uses the normal word store at `801CEE98`, and further
decrements saturate at the zero store at `801CEEAC`. Frame-exact drain
timing for each variant and any other reset path remain unverified.
The alternate gauge routing through `B+0x70` has its own selector.

The trace establishes outcome dispatch and one native teardown that clears
the allocation. It does not identify the instruction that produced
`0xC0071020` at `0x802F706C` on the previously reported Game Over screen.
An arena reset/reuse or overlay change invalidates the interpretation of
the old watch address. Distinguish a resource reaching zero, an outcome
byte changing, the free callback running and the next allocation by
logging them as separate events. The dialogue watch at `0x801C792C`
plays no role in this analysis.

## Bounded read-only trace design

Use the existing `LinuxProcess(pid, writable=False)` and canonical
big-endian `RAM.read_guest` interface, including the word-swapped host
conversion in `autosplitter/memory.py`. Reuse the global system-pointer
and loading validation from `snapshot_for_monitoring()`. Ordinary
player-object checks can be omitted from this trace. A missing player
must leave the global sampling active.

1. Read the top-level state, loading flag, submode, map, and boss selector
   (`0x800C7A94`, `0x8015C5D4`, `0x800C7AA4`, `0x800C7AB2`,
   `0x800C7AB4`). Include phase byte `0x800C7A9E` and exit byte
   `0x800C7A9F`. Verify file 13 ownership by matching several text
   anchors in its shared window against the pinned code, including the
   HUD stores at `0x801CD88C` and `0x801CDC90`. Treat a signature
   mismatch as an inactive sample. Check the arena descriptor
   `0x80154C64` and the allocation-list membership of the pointer at
   `0x8020EED0` using bounded, aligned header traversal (at most 64
   links, with bounds and cycle checks). For this request the expected
   header lies at `B+0x2F0` and stores `{B, 0x300, next, prev}`. Check
   that header against the active list rather than inferring membership
   from its address. The requested controller and its
   header must fit the arena. An inconclusive list traversal produces
   a globals-only row.
2. Read `[B+0x2E,B+0x88)` as one block plus `B+0x14A` and
   `[B+0x2C0,B+0x2CC)` for gauge selection, outcome, input gating and
   the controller tick counter. Decode halfwords, signed counters, raw
   float bits and degrees together. Require `p >= 0x80148850`,
   `p + 0x98 <= 0x8014FA50` and
   `(p - 0x80148850) % 0x98 == 0` for each followed object. Require
   distinct nonzero targets for the active HUD view. Read selected
   fields only, e.g. `[p+0x04,p+0x40)` and `[p+0x64,p+0x65)`,
   and check render category and tag. Never follow the embedded model
   references. Record the rejection reason for invalid or missing targets.
3. Read context, allocation identity and pointer-table anchors again
   after target reads. Discard mixed-state samples on any mismatch. On a
   runtime that does not retain original text in guest RAM, require an
   equivalent emulator-provided overlay-load probe before following
   targets.
   Prefer an emulator end-of-frame callback where available. An external
   poll should use monotonic timestamps, the controller tick before and
   after and an explicit non-atomic marker. Preserve the last 120 frames
   in memory. Emit changes to pointers, control, outcome, selector or
   counters, plus adjacent context for those events. Limit capture to
   90 seconds and 2,000 event rows, with sampled float deltas and changed
   byte offsets for selected fields. Store optional local diagnostics
   under the ignored diagnostics directory.
4. In the inspector, display the validated battle base and lifetime
   state, pool indices, named HUD roles, raw hex and decoded values.
   Show inactive/stale states explicitly and keep Impact research
   sampling read-only. No code or live reader changes are part of this
   report.

## Five follow-up experiments

1. **Identify the two auxiliary meshes.** Trace object references at
   `B+0x58/+0x5C`, the constructor calls `801CDBD0/801CDC80` and the
   render consumer of category 10. Record validated `+0x2C/+0x30` and
   visibility transitions. Stop when each descriptor is tied to a
   distinct on-screen cockpit component or the segment binding is
   identified as the remaining blocker.
2. **Catch the reaction at its writer.** Watch `u16 B+0x40`,
   `u16 B+0x2E`, oil and the seven `+0x64` bytes. Capture one idle shot,
   one incoming nonfatal hit and one fatal hit. Break on
   `801D2844/801D28DC` and the `sh` sites in `801CDD10`. Stop when one
   trace shows the writer that causes value 1, its corresponding
   visibility changes, and the clearing PC.
3. **Prove the charge spend.** Trace the input path
   `801D8594 → 801D79FC/801D7A44 → 801D7BC8 → 801DDAF8` and
   watch both `B+0x6C` and `B+0x70` plus selector `B+0x14A`.
   Compare the decrement cadence against `801DDFB8/801DE368/801DE9E8`.
   Stop after both variants show the drain reaching zero and establish
   whether the display switched inputs during either variant.
4. **Verify cross-boss and teardown order.** Log selector `0x800C7AB4`,
   overlay anchors, `B+0x2C4`, arena head and the controller pointer
   from one win, one Game Over and a fresh start on another boss.
   Watch `801CB5C0`, `80014BE8` and subsequent arena allocations.
   Stop once the first reuse write over old `B+0x6C` is attributed
   and each encounter's boss-init index and HUD constructor are recorded.
5. **Confirm camera consumers on both paths.** Log `B+0x74..0x84`,
   `B+0xA0..0xB4`, `0x8020EED4` and `0x8020EED8` while moving
   aim horizontally and vertically. Compare the deltas with `801CC608`
   and `801CC830` and follow the two triplets into the view transform.
   Stop after the branch semantics and world-axis convention are
   verified in both camera modes or the missing mode trigger is identified.

## Reproduction and validation

Use [INPUTS.md](../decomp/INPUTS.md) for the pinned source/ROM and generate
the original USA Splat disassembly there. The primary files are
`asm/usa/5F6840.s`, `36750.s`, `E7F0.s`, `2C40.s`, `204B0.s`, and
`asm/usa/nonmatchings/wave_uty/` for `800148F0` and `80014B74`. The
comparison read each address/word from the disassembly comments and
required equality with the four bytes at the indicated ROM offset in the
pinned decompressed image. In particular all 63,868 annotated file-13
text words, 828 pool-unit words and 1,428 model-unit words passed.
Inspect the two file-table entries through the loader's effective address
`0x57FC8 + 4*(id - 1) + 0x10`. Mask bit 31 on the start and end to
form the interval. For ID 13 the start is unflagged and the next word
has its flag set for ID 14. For allocator and descriptor widths, disassemble
the main segment with `VMA = ROM - 0xC00`. Verify jump tables and camera
constants directly with big-endian word/double reads at the ROM offsets
listed above.

The repository's `python3 -m decomp.local_ci` passed 207 Python tests
(including the private-ROM span check), 116 verifier/ledger tests, the task evidence check, and
the 1,000-case display-emitter sanitizer fixture plus its boundary cases.
The Linux process, state-discovery and inspector suites passed 32 tests.
The original-byte comparisons were separate. This is a documentation
investigation and did not require a new native IDO or full-ROM G2 build.
