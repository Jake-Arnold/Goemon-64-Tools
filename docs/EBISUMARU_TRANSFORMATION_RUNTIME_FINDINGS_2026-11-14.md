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
