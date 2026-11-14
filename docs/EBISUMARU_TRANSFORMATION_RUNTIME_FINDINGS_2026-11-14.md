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
