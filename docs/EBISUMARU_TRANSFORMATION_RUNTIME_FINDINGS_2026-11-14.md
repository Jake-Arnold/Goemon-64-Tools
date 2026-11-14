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
