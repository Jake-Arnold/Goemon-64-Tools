# Finding remaining original-game state fields

**Status:** These are research targets, not confirmed addresses. The new **State discovery** tab in v0.10.4 captures a before/after pair (and optionally a return-to-before capture), compares the original N64 guest bytes, and exports candidate addresses. Captures do not write game memory and do not imply that changed addresses control a feature. Current known map/character/resource addresses are unchanged.

## Capture protocol

1. Connect to **US Goemon64Recomp** and select **State discovery**.
2. Choose the appropriate test and keep conditions as close as possible, e.g. same area and same character unless the test explicitly requires changing them.
3. Capture **A** with the feature off/absent. Perform exactly one action. Capture **B** with it on/present.
4. For toggles (map, equipped weapon, magic), undo the action and capture **C**. Comparison with C filters out candidates that do not revert byte-for-byte to A.
5. Click **Compare**. Inspect the address, one-bit mask and values. Use **Export comparison JSON** to save the results under `practice/diagnostics/` or `%LOCALAPPDATA%/GoemonSpeedrunTools/diagnostics/` for a packaged Windows executable.
6. Repeat the same action in multiple scenes and with alternate characters. A repeated address changing consistently in the expected direction is stronger evidence than a single comparison. Real addresses must then be verified by controlled writes in the **Live Memory** tab before promoting them to confirmed controls.

**Focused scan:** system `0x800C7800`–`0x800C87FF`, live + save/game data `0x8015C500`–`0x8015CDFF`, player task + object (if pointers available). **Wide scan:** first 4 MiB of original N64 guest RAM (`0x80000000`–`0x803FFFFF`), including overlays. Use the same scan scope for A/B/C. Wide captures can be slow and span multiple game frames. For a magic effect that ends quickly, the 4 MiB scan may miss it; use focused first.

The export includes every displayed candidate and metadata, **not full RAM dumps or ROM data**. The table shows a ranked, bounded shortlist (1200 rows maximum) to preserve UI responsiveness; high-noise captures may require tighter comparison conditions.

## Target-specific tests

| Target | Controlled experiment | Interpretation |
|---|---|---|
| Oedo tourist/dragon-travel destinations | Capture before and after **first arrival/unlock** at a previously unavailable destination. Avoid unrelated collectibles and cutscenes; check save/global progression changes. | Likely persistent flags or packed bitsets; **not mapped**. Not necessarily `0/1` individual bytes. |
| Map display | In a town/field, press C-Right to show/hide map, capture A/B/C without changing room. | Likely transient UI/global flag, **not mapped**. Be sure not to confuse the pause-map screen with the C-Right overlay. |
| Selected item/weapon | Capture A/B/C while changing only the selected weapon (C-Left), or the selected inventory cursor in the pause menu. | **Not mapped.** Existing `0x8015C5F3/…` item slots describe carried item codes, not selected state. |
| Magic active | For each character in turn, capture A before C-Up, B while the effect is visibly active, and C once it finishes. | **Not mapped.** Each character may use separate task-local and/or global state; distinguish owned/unlocked abilities from *currently active* magic. |
| Player velocity | Stand still, move/run, jump, then stand still; compare floats in dynamic player task. | Existing `PlayerTask` struct contains **unidentified** f32 members at task offsets `+0x68`…`+0xC8`. These are candidates, **not proven velocity**. Dashboard and Live Memory show **measured XYZ displacement per real second**, not true engine velocity. |

### Source notes

- Original game manual: [scan](https://www.videogamemanual.com/n64/Mystical%20Ninja%20Starring%20Goemon%20%28USA%29.pdf). The controller's C-Right button toggles the displayed local map; C-Left changes weapon; C-Up triggers magic.
- [Goemon64Recomp types.h](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/types.h) describes the player task layout but leaves many fields unnamed.
- [Goemon64Recomp variables.h](https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/variables.h) includes the current active character and player task/object pointers.
- [Oedo tourist travel description](https://goemon.fandom.com/wiki/Oedo_Tourist_Center) notes that destinations become available after visiting them and that travel uses Yae's flute.

## Known limitations

- Without actual A/B/C observations from a running game, the feature **cannot** establish authoritative offsets for these targets.
- Byte-level differences can show individual bits inside a larger field. More than one byte may change as a secondary effect; a displayed match is not proof of causality.
- Cross-map transitions change many unrelated state fields, and some character/magic effects are short-lived.
- The derived observed velocity is affected by sampling cadence, frame-rate changes, collisions and temporary game freezes. It cannot replace native engine speed for frame-perfect autosplitting.
