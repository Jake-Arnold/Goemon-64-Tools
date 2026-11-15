# Japanese player XYZ teleportation — Project64 live evidence (2026-11-15)

**Evidence:** User-operated *Ganbare Goemon: Neo Momoyama Bakufu no Odori* (Japan) in Project64 3.0 on Windows, with Project64 virtual RDRAM editing and Goemon Practice Toolkit v0.11.17 Japan Live custom watches (`f32`). Original user screenshots and descriptions are in the investigation conversation; screenshots are **not included in this repository file**. Addresses below are **N64 guest virtual addresses**, not Windows process addresses. This is gameplay observation, not a matching-C proof or an automated test.

**Status:** High-confidence **functional XYZ position controls**. Direct before/after edits are documented in Oedo Town South and North; the user subsequently reported that the same coordinates **seem to work everywhere** in their additional gameplay testing. The latter is a broader user report without an enumerated scene/character/state matrix, so universal applicability is **not yet proven**.

## Position-controlling XYZ fields

| Axis | Japanese N64 address | Data type | Direct experiment |
| --- | --- | --- | --- |
| X | `0x80151B10` | big-endian IEEE-754 `f32` | Editing to float zero moved the playable character to X=0; previously discovered tracking fields subsequently followed the change |
| Y | `0x80151B14` | big-endian IEEE-754 `f32` | Editing to `0x42500000` (52.0) visibly placed the character above the ceiling |
| Z | `0x80151B18` | big-endian IEEE-754 `f32` | The user's complete 12-byte XYZ entrance write placed the character at the intended Oedo South position; isolated Z-write effect has not been separately documented |

**Native Oedo Town South default entrance test (USA entrance atlas reference):**

| Axis | Decimal | 32-bit guest float (hex) |
| --- | ---: | --- |
| X | -289.0 | `C3908000` |
| Y | 0.0 | `00000000` |
| Z | -167.0 | `C3270000` |

The user wrote `C3908000 00000000 C3270000` into consecutive guest words beginning at `0x80151B10` and reported teleportation to the **exact intended entrance position** in Japanese gameplay. Subsequent Y override `42500000` (52.0) visibly elevated the player above the ceiling. Those outcomes support a position-controlling vector; they do not establish safe arbitrary teleportation or collision handling.

**Cross-scene validation (user follow-up):** The user explicitly confirmed that these **same three addresses continued to control the character in both Oedo Town South (scene 353 / `0x161`) and Oedo Town North (scene 352 / `0x160`)**. This is stronger than a one-scene test, but not proof of all-scene or cross-session lifetime. This validation was reported from gameplay, not produced by an independent debugger trace of each write.

## Later cross-scene user report (2026-11-15)

Following the two specific Oedo-scene validations, the user reported: **“seems to work everywhere”**, referring to `0x80151B10`, `0x80151B14`, and `0x80151B18` as position-controlling floats. This is meaningful evidence that the vector is not limited to the first two scene allocations. No additional scene IDs, character identities, boss states, transformation states, precise debugger readings, or emulator restart results accompanied this report. Preserve the result as **user-reported broad success** rather than a claim that every scene or gameplay mode has been independently tested.

## Readback mirrors / derived candidate vectors

| Address range | Observed behaviour | Interpretation status |
| --- | --- | --- |
| `0x80211870–0x80211878` | XYZ triplet A tracked walking and natural entrance positions; direct overwrite of X did not move the character, and the value was replaced on resume | Position readout/copy candidate; *not authoritative in the tested scenario* |
| `0x802118E0–0x802118E8` | XYZ triplet B matched A across sampled gameplay; direct overwrite of X did not move the character and reverted | Second synchronised position readout/copy candidate |
| `0x80211B10–0x80211B18` | Was zero in the later Project64 movement recording; previously some vertical changes were observed in Mupen testing | Not verified as active player XYZ |
| `0x80151BA8`, `0x80151C40` | Floats observed matching X at multiple points | Possible copies; authority untested |

Do **not** infer a particular copy direction, physics function, collision ownership, or exact update ordering without an original MIPS writer/reader trace. Changes to A/B reverting on resume are consistent with synchronisation or engine corrections.

## USA entrance data corroboration

The repository's [USA entrance extractor](../practice/entrances.py) gives a **USA-derived** default spawn for Oedo South (353) of `(-289, 0, -167)`, and an Oedo North (352) default of `(-298, -7, 305)`. Normal Japanese play yielded readouts near these values:

| Japanese scene/event | USA source spawn | Japanese observed A/B readout | Notes |
| --- | --- | --- | --- |
| Oedo South default | `(-289, 0, -167)` | `(-280.44, 0, -167.54)` | Close after player motion |
| Oedo North default | `(-298, -7, 305)` | `(-306.56, -7, 305.54)` | Close after player motion |
| South (353) → North (352), entrance `161:003` | `(980, 7, -195)` | `(980, 7, -196.2)` | X and Y exact, Z differs by -1.2 |

These comparisons strongly support compatible world coordinates across the versions **for the sampled Oedo entrances**, not a universal equality of all Japanese/USA spawn records.

## Relationship to character-switch pointer research

Separate Japanese Project64 stepping in [JAPAN_PROJECT64_CHARACTER_SWITCH_MIPS_TRACE.md](JAPAN_PROJECT64_CHARACTER_SWITCH_MIPS_TRACE.md) established a **single observed** pointer chain `0x8016F780 + 0x5C → 0x80211650`, with a write to `0x80211650+0x69`. The player-position mirrors at `0x80211870` and `0x802118E0` happen to lie at `+0x220` and `+0x290` from that observed destination. **Proximity does not establish that the object is the player actor**, that the pointer is stable, or that the authoritative `0x80151B10` vector belongs to it.

## Toolkit implications / remaining validation

- The position vector can be **labelled as runtime-confirmed in Oedo South and North, with broader user-reported success elsewhere**, with clear read-only discovery metadata. This document does **not** enable guest writes in the Japanese toolkit.
- Gate any future Japanese teleport/checkpoint implementation on a verified scene and character state; capture/restore complete emulator savestates for experimental writes; reject loading/transition/cutscene/boss states until independently tested.
- Record named scene IDs and evidence for any additional successful locations, especially buildings, unrelated overworld scenes, dungeons, boss fights and character transformations; also verify across emulator restarts or fresh RAM allocations. The user's wider success report is not a complete scene matrix.
- Find original MIPS readers/writers of `0x80151B10`, `+0x04`, `+0x08` to establish update semantics and whether the vector is global or pointer-relative.
- Investigate whether the mirrors are collision/ground positions and identify the airborne-Y field separately. Do not conclude `0x80151B14` has all desired jump physics behaviour solely from a one-time Y teleport.

**No ROM modification, toolkit code change, decomp function promotion or automated integration test accompanies this evidence note.**
