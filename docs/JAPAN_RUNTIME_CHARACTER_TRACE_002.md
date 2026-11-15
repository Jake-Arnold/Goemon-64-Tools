# Japanese runtime evidence: character A/B and Oedo Castle bridge (capture 002)

Source: user-supplied `Japan-0 Mupen64Plus read-only RAM comparison` from an actual running Japanese Mupen64Plus process. Captures on 2026-11-15 use **PID 959604**, RDRAM host base **0x7AA843EC0000**, **wordswapped**. All accesses were read-only.

Original bytes and the user's contextual descriptions are preserved in `research/japan_scene_character_runtime_2026-11-15.json`. Earlier independent scene trace: `research/japan_scene_runtime_2026-11-15.json`.

## Reversible character selection (confirmed for values 0 and 1)

| Direction stated by user | Japanese guest field | Before | After |
|---|---|---|---|
| Goemon → Ebisumaru | `0x80161DCC` u32 | `00000000` | `00000001` |
| Ebisumaru → Goemon | `0x80161DCC` u32 | `00000001` | `00000000` |

The matching bidirectional value changes directly confirm **Goemon = 0 and Ebisumaru = 1** for the Japanese character index in these gameplay observations. The USA-derived guesses Sasuke=2 and Yae=3 are **not yet independently tested in Japan**. No player-object pointer or XYZ information is established by knowing this global index.

Time counter from those captures: `0000D5B7 → 0000D5B9` (+2 raw units) and `0000D6CF → 0000D6D1` (+2 raw units). A raw unit is not established as a second, frame or tick.

## Second Japanese scene transition: Oedo Town North to castle bridge

User explicitly reports travel from **Oedo Town North** to the **bridge leading to Oedo Castle**.

| Japanese field | Before | After | Result |
|---|---|---|---|
| Current `0x800CD2A2` u16 | `0160` (352) | `0162` (354) | The existing scene catalogue names these Oedo Town (North) and Oedo – Bridge to Oedo Castle |
| Previous `0x800CD2AC` u16 | `0161` (353) | `0160` (352) | After-value matches the **old current** scene 352. Before-value 353 is prior history (Oedo Town South); it does **not** equal the pre-transition current scene 352 |
| Pending `0x800CD490` u16 | `0160` (352) | `0162` (354) | Tracks destination/current scene in the two stable snapshots; the moment it changes *during* loading remains unverified |
| Total time raw `0x8016205C` u32 | `0000D681` | `0000D690` | +15 raw counter units; timebase unknown |

The earlier independent scene transition, 300 → 355, showed the same pattern: after-state Previous became the old current scene, and Pending matched the new current scene at the endpoint. These two traces now provide **replicated evidence** for current, previous and pending scene data, but not a full state-machine timeline.

**Gameplay submode** 1→2 has only one Japanese observation, in the first capture (Kai Highway → Oedo Town), and therefore remains single-trial corroboration. Phase, pause, exit, transition flag, loading state and character values 2/3 remain unverified.

## Toolkit changes

- `practice/japanese_scene_probes.py`: independent confidence labels per field; four scene fields carry one or two observed transitions as appropriate, and the confirmed character index is specific to 0/1; values 2/3 retain tentative labels.
- `practice/japanese_fields_ui.py`: evidence labels now match the field-by-field strength of runtime observations instead of describing all ten as equally speculative.
- No ROM changes, guest RAM writes, freezes, warps, direct character-switch manipulation, or new pointer assumptions.
- Added regression checks for precise archive bytes and display-status distinctions. **These test files are committed but a full test-suite run is not yet claimed for this branch.**

## Remaining validation

A third scene transition using an unrelated scene pair, plus one recording of the Pending and Loading values *before* the current scene updates, would allow stronger inference about loader ordering. Reading the Japanese character index does not unlock XYZ; Japanese player/task pointers still require independent mapping.

## Follow-up: Project64 original MIPS writer trace (2026-11-15)

The subsequent Windows Project64 investigation independently confirmed `0x80161DCC` for Goemon/Ebisumaru and captured the original Japanese MIPS instructions at `0x801E2944` and `0x801E298C` writing the global character index. Single stepping also confirmed a call to `0x801E2970` with a character-related byte at `object+0x60`. See [JAPAN_PROJECT64_CHARACTER_SWITCH_MIPS_TRACE.md](JAPAN_PROJECT64_CHARACTER_SWITCH_MIPS_TRACE.md) for the full observed instruction/register sequence, confidence boundaries, and unresolved pointer/overlay work. The evidence is not yet sufficient to treat the observed object pointer as a stable player pointer.
