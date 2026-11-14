# Mini Ebisumaru active-transformation runtime candidates (14 November 2026)

Source: user-supplied **`ebisumaru power change state.mp4`** (33.185 seconds, 5120×1440 native video) plus accompanying screenshot. The original recording displays an ongoing Goemon Practice Toolkit Value Search `u8` candidate list and Ebisumaru in a stable town scene. Evidence was inspected at two-second intervals, with additional still crops around the key memory rows. This note contains no ROM or video assets.

## Controlled observation

Ebisumaru repeatedly alternates between miniature and normal-size appearance without a map transition. The Value Search display is a narrowed candidate set from previous sampling; the video does not show the full initial search setup. The scanner auto-refreshes visible readings independently of game rendering.

Two candidate patterns repeatedly correlate with the **settled** character size:

| N64 address | Read type | Miniature | Normal | Evidence interpretation |
|---|---|---|---|---|
| `0x8020C8E6` | `u8` | 255 / `0xFF` | 0 / `0x00` | Strong binary-like candidate |
| `0x8020C8E7` | `u8` | 255 / `0xFF` | 0 / `0x00` | Changes identically to preceding byte |
| `0x801C159A` | `u8` | 28 / `0x1C` | 52 / `0x34` | Strong size-correlated candidate, not necessarily a boolean flag |

Representative frame observations (not instruction-atomic):

| Approx. video time | Visual state | `E6/E7` | `801C159A` |
|---|---|---|---|
| 0–6 s | Miniature | FF / FF | 28 |
| 8 s | Normal-looking during/after change | FF / FF | 28 |
| 10 s | Normal, settled | 00 / 00 | 52 |
| 12 s | Miniature | FF / FF | 28 |
| 14 s | Normal-looking during transition | FF / FF | 52 |
| 16 s | Normal, settled | 00 / 00 | 52 |
| 18–20 s | Miniature | FF / FF | 28 |
| 22 s | Transition effect visible | FF / FF | 28 |
| 24 s | Normal, settled | 00 / 00 | 52 |
| 26–28 s | Miniature | FF / FF | 28 |
| 30 s | Normal-looking during/after change | FF / FF | 28 |
| 32 s | Normal, settled | 00 / 00 | 52 |

The apparent delay/mismatch at 8, 14, 22 and 30 seconds prevents concluding these fields are the direct toggle command. UI polling, effect timing, camera distance, interpolation, and game-state transition timing can all confound correlations.

**Structural hypothesis:** since the adjacent bytes `0x8020C8E6–E7` match in the sampled states, they might be the signed halfword `0xFFFF` (−1) for miniature and `0x0000` (0) for normal, or the low halfword of a 32-bit word at `0x8020C8E4`. A user should compare read-only `s16/u16 0x8020C8E6` and `u32 0x8020C8E4` to the single bytes. The original MIPS access width is unknown.

The remaining candidates shown around `0x8014C334`, `0x8014C338`, `0x8014C33C`, `0x8014C464`, `0x8014C46C`, `0x8019208D` and `0x8019208F` sometimes change during animation or motion but are less specifically associated with settled miniature/normal states. No field meanings are assigned.

## Crucial distinction

Existing unlock/ownership field `0x8015C6F3` means **Mini Ebisumaru ability acquired**, not **currently transformed**. It should normally remain acquired in both miniature and normal states. Do not replace that ownership mapping with any of the above active-state candidates.

## Minimal follow-up protocol

1. Add **read-only** custom watches: `u16 0x8020C8E6`, `s16 0x8020C8E6`, `u32 0x8020C8E4`, `u8 0x801C159A`; retain `u8 0x8020C8E6` and `u8 0x8020C8E7`. Optionally add an `hex8` watch at `0x8020C8E0` and another at `0x801C1594` to inspect surrounding raw bytes.
2. Hold **miniature completely still** for 3–5 s and record all values. Switch to **normal**, hold still 3–5 s, record. Repeat several times, focusing on *first frame of change* versus *settled state*.
3. Move, jump, rotate the camera or change facing **without using the transformation**. The true active-state discriminator should remain consistent; position/scale/animation byte candidates may change.
4. Switch to another character and back, and repeat after a map load and full game restart. Note any pointer/offset stability.
5. When appropriate, identify original MIPS readers/writers of these addresses or the base containing them. Do not write to or freeze unknown candidate fields merely because they correlate with Ebisumaru's size.

## Confidence and next engineering step

These are **high-value runtime candidates**, not confirmed ROM symbols, native flag semantics, transformation multipliers or safe editing targets. Prefer narrowing the original MIPS controller/actor update path over adding unconditional controls or production writes to the toolkit. The toolkit's `Value Search` can maintain live previews while no game-memory modification occurs.

## 11:05:26 follow-up: settled states and manual countdown (14 November 2026)

New evidence: the user's 24.24-second follow-up video `Screencast From 2026-11-14 11-05-26.mp4` and two still screenshots, plus the user's explicit report of a controlled manual memory edit. The video shows the N64 game and custom Live Memory watches; samples below are asynchronous toolkit/video observations, not instruction-atomic readings. No media or raw RAM dumps are stored in the repository.

| Approx. video time | Visible state | `u8 0x8020C8E6` | `u8 0x8020C8E7` | `u16 0x8020C8E6` | `u8 0x801C159A` |
| --- | --- | ---: | ---: | ---: | ---: |
| 0 s | Normal | 0 | 0 | 0 (`0x0000`) | 52 (`0x34`) |
| 6–12 s | Miniature | 255 | 255 | 65535 (`0xFFFF`), `s16 = -1` | 28 (`0x1C`), except transient frames |
| 13–16 s | Normal | 0 | 0 | 0 (`0x0000`) | 52 |
| 17–21 s | Miniature | 255 | 255 | 65535 (`0xFFFF`) | 28 |
| ~22 s | Transforming/transition | 255 | 255 | 65535 | **52**: changes before the combined field |
| 23 s | Normal | 0 | 0 | 0 | 52 |

The upper half of the `u32` word at `0x8020C8E4` changes during motion while its lower half is `0xFFFF` or `0x0000`. This is evidence **against** treating the entire 32-bit word as a single transformation timer; it supports inspecting the aligned big-endian halfword at `0x8020C8E6` separately. `0x801C159A` tracks settled size but is not a synchronous duplicate or established controller flag. The unrelated `0x801671A0` watch changes during movement but no velocity semantics are established.

### Controlled write observation — strong 16-bit countdown hypothesis

The user reports that when Ebisumaru is normal (both bytes `00`), manually writing `255 / 0xFF` **only to byte `0x8020C8E6`** causes the byte to drop to 254 while `0x8020C8E7` jumps to 255, then the low byte counts down; every underflow is accompanied by the high byte decrementing. This exactly matches a big-endian 16-bit decrement sequence:

- Initial `0x0000`; manual high-byte write: `0xFF00`.
- On first decrement: `0xFEFF` (`E6=254,E7=255`).
- Subsequent decrements: `0xFEFE`, `0xFEFD`, ... `0xFE00`, `0xFDFF`.

This arithmetic substantially strengthens the conclusion that these **two bytes together form one 16-bit counter**, with stable sentinel endpoints `0x0000` (normal) and `0xFFFF` (miniature). The user also reports transformation input is rejected if the two values are not both zero or both 255. A guard requiring one of two terminal values is plausible; original MIPS branching and exact update cadence remain unverified. This user write observation is additional evidence beyond the video, which does not clearly capture the intermediate countdown at individual decrement resolution. Avoid extrapolating duration from an unverified update frequency.

**Next original MIPS investigation:** trace reads/writes of halfword `0x8020C8E6` or a pointer-relative offset to it, especially `lh/lhu/sh`, decrement/borrow, comparisons to zero and -1, and the gating path for transformation input. Independently determine what `0x801C159A` controls (animation, size/state, or a downstream transform output). Only promote confirmed original semantics to the toolkit. Avoid further unsafe writes to unknown transition fields without a restore path.

## Controlled endpoint mismatch and cross-character miniature appearance (14 November 2026)

The user independently reports three **controlled memory-edit experiments** performed in the running game after the previous 16-bit countdown work. No new video is claimed for these three experiments; interpretations below are grounded in the user's descriptions.

| Initial visible size | Manually forced `s16 0x8020C8E6` | Action | Visible result | Final observed halfword |
| --- | --- | --- | --- | --- |
| Ebisumaru normal | `-1` / `0xFFFF` (normally the miniature endpoint) | Activate Mini Ebisumaru | Begins to shrink, then returns to normal | `0` / `0x0000` |
| Ebisumaru miniature | `0` / `0x0000` (normally the normal-size endpoint) | Activate power again | Begins to grow, then shrinks back to miniature | `-1` / `0xFFFF` |
| Ebisumaru miniature | `0` / `0x0000` | Switch to another playable character | Other characters also **appear miniature** | Value following switch not separately reported |

### Interpretation

1. **Causal dissociation:** changing this halfword alone does not instantly or reliably force the visible model to the associated size. The character can remain small while the word is 0, or remain large while it is −1.
2. **Endpoint mismatch correction:** pressing the power button from a deliberately mismatched state visibly initiates a transformation, but the final appearance and halfword return to the original state together. This supersedes any overly literal interpretation that checking only 0/−1 is *sufficient* to produce a stable size toggle. A separate state, cached appearance, animation task or size parameter appears necessary.
3. **Cross-character effect:** a mismatched miniature state can propagate to a subsequently selected character, suggesting shared player transformation/scale state or reuse/copying of a character actor field. This does **not** prove the other characters support Ebisumaru's power, that this halfword is a universal scale variable, or that the effect persists across maps.
4. **16-bit arithmetic remains relevant:** earlier single-byte edits produced a `0xFF00 → 0xFEFF` decrement-and-borrow pattern. The current experiments add reconciliation/character-switch behavior; they do not establish whether that decrement is a frame timer, interpolation state or another native transition variable.
5. `0x801C159A` remains a **distinct, size-correlated field** (observed 52 normal / 28 mini) that can change earlier than the E6 halfword. It is a high-value comparison during the reported mismatch, but has not been observed simultaneously with all three new interventions.

### High-value original MIPS questions

- Which function reads/writes signed or unsigned halfword `0x8020C8E6`, including pointer-relative loads/stores rather than direct absolute-address references?
- Which branches initialise, decrement and compare it against 0 / −1? How are attempted transformations accepted and committed/cancelled?
- What field controls the **rendered scale/size** independently of the halfword? Trace writes to `0x801C159A` and any actor/model scale fields, determining whether this byte is an output, state, animation parameter or incidental correlation.
- What data is retained, copied or reused across the character-change path so that a different character can inherit a miniature appearance?
- Where are per-character ability ownership and current visual transformation separated? The acquired-power field `0x8015C6F3` is not a substitute for active size state.

### Next low-risk observations

Use **read-only watches** for `s16 0x8020C8E6`, `u8 0x801C159A`, active character ID, and any independently verified actor scale fields during normal/small idle, button press, animation completion and character switch. Capture whether the halfword or `0x801C159A` resets on character change and on map load. Avoid additional forced writes/freeze of transition fields, particularly in states inconsistent with visible size, without a reproducible recovery route.

**Confidence:** user-reported causal interventions strongly support a halfword/visual-size distinction and cross-character effect. The original native code, exact state-machine structure, renderer scale storage and update ordering remain unknown.

## Movement-speed A/B/C measurements after forced halfword edit (14 November 2026)

The user measured movement using the toolkit's **observed velocity magnitude** (position displacement divided by elapsed sample time, **not a recovered original-engine velocity field**). Approximate maxima:

| Visible size | Signed 16-bit word `0x8020C8E6` | Observed velocity magnitude maximum |
| --- | --- | ---: |
| Normal | `0` / `0x0000` | ~98 |
| Miniature | `-1` / `0xFFFF` | ~32 |
| Miniature, manually forced normal halfword | `0` / `0x0000` | ~98 |

The miniature/−1 maximum is approximately 32/98 = **0.327** of the normal/0 maximum, roughly **67% slower**. Crucially, the visual model remains miniature under the forced 0 while the measured speed rises to approximately the ordinary full-size maximum. This falsifies the weaker alternative that the model only *looks* faster due to apparent scale in the camera; measured displacement speed changes.

**Interpretation (strong behavioral evidence):** the halfword at `0x8020C8E6` controls or selects a movement-speed path associated with miniature mode, independently of the displayed model size. This does **not** identify a native velocity variable or prove the halfword directly stores a speed multiplier. A guard, distinct movement routine, input scaling, or other movement calculation could depend on it.

**Limitations:** the maxima are user-reported approximations from toolkit polling, without a formal matched-route experiment, fixed frame timing, acceleration control or direct native velocity field. They should be treated as strong intervention evidence but not as a recovered exact speed ratio or MIPS instruction semantics.

**Original-code targets:** trace both readers and writers of `s16 0x8020C8E6`, find branches splitting miniature vs ordinary locomotion, inspect movement calculation and any distinct actor/model scale data, and identify actual movement/velocity fields via MIPS stores. Compare ordinary and forced-mismatch execution paths. Preserve the already-established distinction from the Mini Ebisumaru ownership flag `0x8015C6F3`.

## Miniature action restrictions and movement-speed-cap research priority (14 November 2026)

The user clarified that with Mini Ebisumaru power active and `s16 0x8020C8E6 = -1`, the character **cannot switch to another character** and **cannot attack normally**. Walking, jumping, and interacting with NPCs/signs continue to work. When the user manually changes the same halfword to `0` while Ebisumaru remains visibly small, ordinary attacks and character switching become available. The earlier observation of switching to another character that remains miniature was performed in this forced-zero state, and therefore is **not contradictory** to the native miniature-mode character-switch lock.

| Miniature appearance | `s16 0x8020C8E6` | Walking / jumping | NPC/sign interaction | Normal attack | Character switch | Measured max movement magnitude |
| --- | --- | --- | --- | --- | --- | --- |
| Yes | `-1` | Allowed | Allowed | Blocked | Blocked | ~32 |
| Yes (manual mismatch) | `0` | Allowed | Not separately compared | Allowed | Allowed | ~98 |
| No (normal) | `0` | Normal gameplay | Normal gameplay | Normal gameplay | Normal gameplay | ~98 |

**Significance:** the halfword may select a broader **miniature gameplay-restriction mode**, not just a movement-speed path. Correlated movement and action changes make it especially valuable to trace MIPS code that checks `0x8020C8E6` (including equivalent pointer-relative access) for **locomotion max-speed selection**, **attack input gating**, and **character-switch input gating**. Those may be separate readers of one field rather than a single central controller. Do not infer that only the listed actions are available or unavailable; the user explicitly tested only those actions.

**Revised investigation priority:** Recover the game's **maximum movement speed parameter/limit or equivalent computed speed cap**, rather than merely the position-derived velocity magnitude or any instantaneous velocity component. Determine whether speed is limited by an actor-field value, a constant selected by mode, separate acceleration curves, a vector clamp, or frame-dependent movement routine. Trace the exact decision path causing approximately 32 in legitimate miniature/−1 and approximately 98 in normal/0 and miniature/forced-0. Report the original function/PC, field address or offset (if stored), original instruction and data width, source constant(s), and verification. If there is no stored max-speed variable, report the control-flow and calculation instead of inventing one. Native velocity storage is a secondary follow-up, not the primary deliverable.

**Evidence scope:** user-reported runtime interventions; no original MIPS reader/writer or precise speed ceiling proven. No toolkit memory-writing behaviour changed.

## USA ROM/MIPS trace: movement limit and action gates (14 November 2026)

### Source identity and method

The original USA Rev. 00 retail image was checked against SHA-1
`df8083a54296b8c151917c5333e1c85f014a2a66`. Using the pinned USA `mnsg` layout,
the decompressed image matched SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494` (33,554,432 bytes). The layout was
split with Splat from pinned source commit
`7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; the matching-C repository does not
contain the player movement implementation, so the findings below are from
original USA MIPS and its mapped data. No ROM or generated disassembly was
added to Git.

### A. Maximum movement limit: ROM/MIPS verified

The user supplied a live task pointer of `0x80169FA0`; its `f32 +0xE4` is
`0x8016A084`, and `f32 +0x74` is `0x8016A014`. The supplied runtime readings are
`+0xE4 = 2.8` in ordinary Ebisumaru mode and `1.12` in miniature mode. The
pointer value itself was not read by me from a running game.

The MIPS trace explains the `+0xE4` field directly:

1. `func_801E1C90_59DBA0` (`VMA 0x801E1C90`, ROM `0x59DBA0`) calls
   `func_801E7DE8_5A3CF8` at `0x801E1CF4`.
2. `func_801E7DE8_5A3CF8` checks task `+0x60` for `1` at `0x801E7DE8`. It loads
   task `+0x5C` at `0x801E7DFC`, performs `lhu 0x86(pointer)` at `0x801E7E04`,
   and returns true only when that halfword equals `0xFFFF` (`xor` at
   `0x801E7E08`, boolean reduction at `0x801E7E0C`). For the user-supplied
   task/context mapping, this is `u16 0x8020C8E6 == 0xFFFF`.
3. At `0x801E1CFC`, `func_801E1C90` branches on that predicate. The true branch
   builds `1.12f` (`0x3F8F5C29`) at `0x801E1D04–0x801E1D10`; the false branch
   builds `2.8f` (`0x40333333`) at `0x801E1D24–0x801E1D30`. Both call
   `func_801E3DE0_59FCF0` (`VMA 0x801E3DE0`, ROM `0x59FCF0`) with the same
   `0.3f` transition parameter. That helper writes a single precision value to
   task `+0xE4` with `swc1` at `0x801E3E88` and clamps its result to the selected
   target at `0x801E3E94`.
4. The player update path loads task `+0xE4` as a 32-bit word at
   `0x801CBF2C`, passes it through `func_801CC4C0_5883D0`, and reaches
   `func_801CD310_589220` (`VMA 0x801CD310`, ROM `0x589220`). The latter stores
   the scalar at `0x801CD31C` and computes the magnitude of its three movement
   components. At `0x801CDCB8` it compares that magnitude with the scalar; when
   the vector is larger, it divides the limit by the magnitude and scales all three
   components before continuing movement.

In the USA Splat map, `file_11` is loaded at `0x801CB460`; its BSS starts at
`0x8020C860` and ends at `0x8020D2A0`, so the halfword is exactly context `+0x86`.
The player-task initializer stores this BSS base through task `+0x5C`. This
interpretation is overlay-specific: other mutually exclusive overlays reuse
part of the same RAM range for ROM-backed data. The active overlay for the
user's live experiments was not independently inspected.

The linked task base `0x80169FA0` is the user's runtime value, not a ROM-fixed
address. If it is the current object stored by the overlay, its word at `+0x5C`
should resolve to `0x8020C860`; that exact live pointer read was not made here.

This is a stored, dynamic `f32` movement-vector limit, not an instantaneous
velocity component. The native limit ratio is `1.12 / 2.8 = 0.4`, a 60%
reduction. The earlier toolkit-derived displacement maxima (~32 versus ~98,
ratio ~0.327) are different measurements and do not equal this native scalar
ratio; the extra difference is not explained by the MIPS chain traced so far.
The user also reports transient `+0xE4` values of `2.0` on stopping normally,
`0.8` on stopping while miniature, and `1.0` during a normal-size hurt
animation, before returning to the steady mode limit. These runtime reports
show that other movement/action states can adjust the same field. The stop
values retain the same ratio (`0.8 / 2.0 = 0.4`), supporting a mode factor that
also applies during deceleration; the exact transient writers were not fully
mapped here.

The movement routine has another branch that substitutes `4.0f` when a
separate context flag is set. No evidence shows that branch was active in the
reported normal/miniature A/B tests.

| Function | VMA / ROM start (size) | Relevant MIPS evidence | Meaning and confidence |
| --- | --- | --- | --- |
| `func_801CB5D0_5874E0` | `0x801CB5D0` / `0x5874E0` (`0x1D8`) | Builds `D_8020C860`, stores it at task `+0x5C` (`0x801CB678–0x801CB684`) | Context pointer assignment, ROM/MIPS verified |
| `func_801E7DE8_5A3CF8` | `0x801E7DE8` / `0x5A3CF8` (`0x30`) | `lbu +0x60`; `lhu +0x86`; compares against `0xFFFF` | Mini-mode predicate, ROM/MIPS verified |
| `func_801E1C90_59DBA0` | `0x801E1C90` / `0x59DBA0` (`0x180`) | Calls the predicate; selects `0x3F8F5C29` or `0x40333333` | Mode-dependent target, ROM/MIPS verified |
| `func_801E3DE0_59FCF0` | `0x801E3DE0` / `0x59FCF0` (`0xDC`) | `swc1` to task `+0xE4`, with target clamp | Speed-limit writer/smoother, ROM/MIPS verified |
| `func_801CD310_589220` | `0x801CD310` / `0x589220` (`0x10E0`) | `sqrt.s` of movement vector, compares to supplied cap, scales vector if needed | Movement-vector clamp, ROM/MIPS verified |
| `func_801D6B80_592A90` | `0x801D6B80` / `0x592A90` (`0x4D8`) | Selects `f32` profile data and writes task `+0x74` | Separate current/profile speed state; exact character mapping unverified |

Other same-offset accesses in this overlay include `lhu` in
`func_801CBD88_587C98` (`0x801CBE60`), `func_801CBF0C_587E1C`
(`0x801CBF80`, `0x801CBFA4`), `func_801D90D8_594FE8` (`0x801D916C`),
`func_801DA758_596668` (`0x801DA77C`), `func_801DC120_598030` (`0x801DC1C8`),
`func_801E0158_59C068` (`0x801E0184`), `func_801E3834_59F744`
(`0x801E397C`), `func_801E572C_5A163C` (`0x801E5754`), and the four small
predicates `func_801E7DC0_5A3CD0`, `func_801E7DE8_5A3CF8`,
`func_801E7E40_5A3D50`, and `func_801E7E90_5A3DA0`. Additional
`lhu/sh` accesses occur in the action/reset callbacks listed below. No `lh`
access to this field was found. No immediate absolute load/store of
`0x8020C8E6` appears in the traced routines; they reach it through task `+0x5C`.

The `f32 +0x74` field is updated separately from the `+0xE4` clamp. Original
MIPS selects `+0x74` from a profile table at `0x801FC91C`, indexed by a profile
byte and a movement-mode byte. The first four decoded profile groups contain
values `40/70/100`, `50/80/120`, `40/50/70`, and `40/50/60`; the selector accepts
more than four internal profile IDs, so these groups do not prove a one-to-one
mapping to Goemon, Ebisumaru, Sasuke, and Yae. Their relationship to the
`+0xE4` limit is not yet established.

### B. Action restrictions: ROM/MIPS verified with runtime mapping

`func_801DCE10_598D20` (`VMA 0x801DCE10`, ROM `0x598D20`) reads the per-player
input record and dispatches three internal action cases. The case sourced from
input mask `0x8` calls `func_801DCFB0_598EC0`; on success it enters the
per-character action handler `func_801E75D4_5A34E4`. For task character index
`1`, `func_801DCFB0` reads `u16 task[+0x5C]+0x86` at `0x801DD068` and its
character-specific success path requires zero. With `0xFFFF`, that ordinary
action path is bypassed. `func_801DD114_599024` is a separate fallback
predicate and can route a different state action through
`func_801E77E4_5A36F4`.

The user identifies the blocked input as ordinary attack. The MIPS verifies a
separate Ebisumaru input gate tied to the same halfword; the mapping from the
internal `0x8` input mask and action handler name to the human-facing attack
button is runtime-informed rather than a symbol label in the ROM.

Character switching is clearer. The internal case sourced from input mask
`0x4` in `func_801DCE10` calls `func_801DD3C4_5992D4` before
`func_801DD50C_59941C`. In `func_801DD3C4`, when task character index is `1`,
`lhu 0x86(task+0x5C) == 0xFFFF` returns false at `0x801DD430–0x801DD440`; the
dispatcher then skips the character-cycle function. `func_801DD50C` advances
the character index through available entries and `func_801DD5C0_5994D0`
resets the `+0x86` halfword to zero. This matches the user's attack and
character-switch experiments and shows the restrictions are in separate
input predicates.

Walking and jumping use the movement update path and remain available in the
user's runtime tests. No universal “disable input” branch was found in the
movement clamp. NPC/sign interactions were not separately traced in MIPS; their
continued availability is user-runtime evidence.

### C. Transformation state and ownership boundaries

`func_801E78DC_5A37EC` (`VMA 0x801E78DC`, ROM `0x5A37EC`) implements the
reported 16-bit decrement. It loads `u16 +0x86` with `lhu` at `0x801E78EC`,
returns unchanged for `0` and `0xFFFF`, otherwise subtracts one and stores with
`sh` at `0x801E7900`. A second `lhu` at `0x801E7908` detects reaching zero. This
exactly explains the user's `0xFF00 → 0xFEFF → 0xFEFE …` high-byte write
sequence. Although the toolkit monitor may display this as signed `s16`, the
identified native reads are unsigned `lhu` operations.

When that decrement reaches zero, the routine sets context byte `+0x84` to `2`,
calls `func_801DD498_5993A8`, then clears `+0x84`—but only on its task-character
index `0` path. That conditional side effect does not by itself identify
Ebisumaru's rendered-size completion. The user-reported rule that transformation
input is rejected for intermediate halfwords is consistent with endpoint
predicates, but the complete Ebisumaru input/animation commit path remains
unresolved.

Other original writers show that the halfword is a broader task state/timer:

- `func_801E77A4_5A36B4` writes a table value to `+0x86` (`sh` at
  `0x801E77E0`); the four halfwords are `0x0384, 0xFFFF, 0xFFFF, 0xFFFF`.
- `func_801F6FB4_5B2EC4` calls a reset helper, then stores `0xFFFF` at
  `0x801F6FD4`.
- `func_801E50C0_5A0FD0`, `func_801F7034_5B2F44`, and the character-change
  reset `func_801DD5C0_5994D0` store zero. `func_801E50C0` does so after its
  separate `+0x30` counter reaches `0x3C`. Other zero stores are in
  `func_801E5208_5A1118` (`0x801E5260`), `func_801EDCE0_5A9BF0`
  (`0x801EDDDC`), `func_801F56EC_5B15FC` (`0x801F5720`), and
  `func_801F5F4C_5B1E5C` (`0x801F5FC8`, `0x801F600C`).

The exact visible-scale state and the user's `u8 0x801C159A` candidate remain
unresolved. No literal reference to `0x801C159A` was found in the USA Splat
disassembly, and no renderer/collision scale field was proven. The user's
mismatched-size and cross-character experiments therefore remain runtime
evidence that visible size is partly separate from `+0x86`; they do not yet
identify the scale owner or corrective animation routine. The known ability
ownership byte `0x8015C6F3` remains a separate acquired-power flag; it is not the
active mode predicate used by the speed selector above.

The character-cycle MIPS updates the current character index on the existing
task and clears `+0x86`, but it does not establish why a different character
retains a miniature-looking model after the user's forced-zero experiment.
Reused/shared visual state is a strong inference; copied renderer scale and
collision size are unverified.

### D. Consolidated memory/function map

| Address / offset | Width | Meaning | Original MIPS owner/readers/writers | Evidence |
| --- | --- | --- | --- | --- |
| `task +0x5C` | 32-bit pointer | Player-task context pointer | `func_801CB5D0_5874E0` stores `D_8020C860` here | ROM/MIPS verified; runtime task base supplied by user |
| `0x8020C860` | BSS base | `file_11` task-context block | `file_11` BSS starts here; `func_801CB5D0` zeros its first word | ROM/layout verified; structure remains opaque |
| `0x8020C8E6` = context `+0x86` | 16-bit | Mini/action/countdown state; endpoints `0`, `0xFFFF` | `lhu/sh` in `func_801E7DE8`, `func_801E1C90`, `func_801E78DC`, `func_801DCFB0`, `func_801DD114`, `func_801DD3C4`, and other task callbacks | MIPS plus user runtime; native reads are unsigned |
| `task +0x60` | `u8` | Current task character index | `func_801E7DE8`, `func_801DCE10`, `func_801DD50C` | MIPS verified; index `1` is the Ebisumaru case used by the speed predicate |
| `task +0x74` | `f32` | Current/profile speed state | `func_801D896C_59487C`, `func_801D6B80_592A90` | MIPS field accesses; user labels it current speed |
| `task +0xE4` (`0x8016A084` for supplied base `0x80169FA0`) | `f32` | Movement-vector limit supplied to `func_801CD310` | `func_801E3DE0` writes it; `func_801CBF0C` loads it; `func_801CD310` clamps movement vector to it | MIPS verified; specific live base/value reported by user |
| `0x801C159A` | `u8` | Size-correlated candidate (`52` normal / `28` miniature) | No literal MIPS reference identified; pointer-relative owner unresolved | Runtime correlation only |
| `0x8015C6F3` | `u8` | Mini ability acquired/owned | Existing toolkit/research mapping; not part of the verified active-mode speed branch | Separate ownership evidence |

### E. Toolkit integration recommendations

- A read-only task view can show current `f32 +0xE4` limit, `f32 +0x74`
  current/profile speed, and the `u16 +0x86` mode/countdown together. Resolve the
  live task pointer per session/overlay; the user-supplied `0x80169FA0` has not
  been independently validated across scene transitions.
- Show `0` and `0xFFFF` as the two verified endpoints and other values as
  intermediate. Do not label `0x801C159A` as model scale until its owner is
  established.
- Keep ability ownership `0x8015C6F3` separate from the active miniature mode.
- Do not add a production write/freeze for `+0x86` or `+0xE4`; this investigation
  verified read paths and engine-selected values, not a safe write workflow.

### Remaining gaps

- The direct MIPS cap is 40% of normal (`1.12/2.8`); the earlier displacement
  maxima ratio (~0.327) is approximate and its remaining difference is
  unresolved.
- The `+0x74` profile table varies by internal profile, but profile-to-character
  mapping is not established.
- The user's transient hurt/stopping values (`1.0`, `2.0`, `0.8`) are confirmed
  runtime observations; the exact state writers were not fully traced.
- Visible model scale, collision dimensions, `0x801C159A`, and the miniature
  appearance carried to another character remain unresolved.
- No assistant-run live game or emulator validation was performed; runtime
  values above were supplied by the user.
