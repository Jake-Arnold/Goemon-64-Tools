## Repeated native character cursor sweep and second-battery timing (2026-11-02)

The original native debug menu character-scan export `native_character_cursor_20261102_104302.json` used 8 stable highlights: Goemon, Ebisumaru, Sasuke, Yae, Yae, Sasuke, Ebisumaru, Goemon. Menu state 10, category 3, map 404, stage offset 4. There were 63 candidates (3 linear, 60 lookup), but the meaningful linear candidates are overlapping parts of **one u32 pointer at `0x800C7E60`** with values `0x8007BAD0`, `0x8007BADC`, `0x8007BAE8`, `0x8007BAF4`. Entries are 12 bytes apart. This pointer is not a 0–3 ID, nor is it a validated writable actor-selection command. Do not blindly write it from ordinary gameplay.

Second battery pickup sets `0x8015C609` bit `0x40` at the **end of the cutscene**, not immediately on contact. The separate event script is still unknown. Live Memory decodes this completion bit read-only.

**Client update:** experimental map reload now honours the character dropdown by requesting a **post-load native C-Down** switch only for available party characters, with model/task verification, refusal on locked characters, bounded attempts and timeout. It does **not** reproduce native debug-menu spawn selection or fix spawn XYZ.

## v0.11.1 — Benkei/Ushiwaka storyline A/B protocol

Use Storyline event / quest flag (focused scan). Capture separate A/B pairs: (1) before and after first Benkei conversation; (2) before Ushiwaka fish turn-in and after the reward/cutscene; (3) before and after editing Achilles Heel into inventory alone, without finishing the event; (4) add the required fish directly, then complete Ushiwaka normally. Use disposable checkpoints and avoid changing map/character during each pair.

Inspect event_flag_changes for bit transitions in persistent gamedata+0x00..0x63 at 0x8015C608..0x8015C66B. Each change is only a candidate until a controlled masked-write test reproduces the dialogue or quest gate. No C needed for irreversible story actions. Item possession, quest progression, and cutscene execution may require separate code paths.

F1 opens Live Memory while the toolkit is focused. Experimental cross-map checkpoint restore waits until the desired map and stable player are ready before writing saved XYZ.

## Experimental test harness (v0.10.8)

The app now includes two *deliberately manual* experiments. **Scene browser → EXPERIMENT reload** writes pending destination `0x800C7CA0` followed by game state `0x0C`, logs result and position. Do not infer correct entrance spawn. **Live memory → Experimental movement** resolves `PlayerTask +0x68` dynamically and sends 4-byte f32 values. Press `+4.0`, `-4.0`, or `Speed pulse ×1.5`, compare observed XYZ motion in controlled gameplay. The task field is still unknown; an observed nudge is not proof it is velocity. The app never writes eight adjacent bytes in these controls.

## Confirmed Sasuke battery 1 flag (2026-11-02)

| Meaning | Address | Encoding | Confirmation |
| --- | --- | --- | --- |
| Sasuke battery 1 collected | `0x8015C609` | `u8` bit `0x20` (`gamedata+0x01`) | User wrote bit before pickup, reloaded; battery disappeared and second became spawnable |

Other flags share the byte. Unlocks now set/clear **only mask `0x20`** while preserving every other bit. Old guessed battery address `0x8015C70B` has been removed from the first-battery UI. **Second battery still unmapped** pending its distinct before/after capture.

# Finding remaining original-game state fields

**Status:** These are research targets, not confirmed addresses. The new **State discovery** tab in v0.10.4 captures a before/after pair (and optionally a return-to-before capture), compares the original N64 guest bytes, and exports candidate addresses. Captures do not write game memory and do not imply that changed addresses control a feature. Current known map/character/resource addresses are unchanged.

## Manual map-address write test (2026-11-02)

The user directly tested candidate `0x8015C574` from Ebisumaru's map A/B/C probe. Writing `0x01`, `0x00` and multiple other values opened the map, whereas writing `0x00` did **not** close it. This invalidates the earlier hypothesis of a simple persistent 0/1 map-overlay state. Classify it as **write-triggered/possibly side-effectful**, not a confirmed boolean. A normal map close flag has **not** been mapped.

The new Live Memory **Custom watches** controls can monitor the raw byte continuously without requiring a built-in mapping. The State discovery table's **Watch selected address** button adds a candidate directly to that list. Watch-only observation does not trigger a memory write.

## Follow-up manual tests (2026-11-02): stronger evidence and rejected hypotheses

- **Selected weapon confirmed:** `0x8015C607`, one byte. For each character, `01`/`02`/`03` select that character's three normal weapons. Out-of-range values display unintended next-character weapons (Goemon -> Ebisumaru hammer, Ebisumaru -> Sasuke kunai, Sasuke -> Yae sword, Yae -> user-described `letter 1`). The game-data field is now a built-in Live Memory watch and an UNSAFE-editable one-byte address. This is distinct from currently selected inventory-slot code or consumable pointer.
- **Map observed but not settable as simple boolean:** `0x8015C574` reports `00` when hidden and `01` when shown, but manually writing `00`, `01` or other tested bytes opens the overlay rather than closing it. Read semantics are verified, write semantics are unresolved; avoid adding a naïve on/off control.
- **Magic candidate rejected:** `0x800C7A73` oscillates between `00` and `01` without magic. It cannot be labelled a magic-active flag on current evidence.
- **Secondary weapon candidate rejected:** `0x8014C340` oscillates `0x40`/`0x41` and sometimes `0x00`; it does not identify the selected weapon.
- **Velocity remains unconfirmed:** session-local player-task f32 offsets `+0x68`, `+0x70`, `+0x74`, `+0x78`, `+0x7C` all read zero while still but can vary during an NPC conversation. The reported `~192` maxima came from byte-level watches: `0xC0` (decimal `192`) is merely the most-significant byte of a negative IEEE-754 f32, e.g. `0xC02D9CA2` is about `-2.7127`. Compare **f32** values in running / jumping / stationary / dialogue states; do not assume byte values represent speed. Dynamic absolute player-task addresses may change after room loads.

## Sasuke first battery pickup probe (2026-11-02)

A/B captured before and after the first Sasuke battery (Ebisumaru, map 330; JSON labels incorrectly say "Map displayed"). The key change is **`0x8015C609: 00 → 20`**. This is at `gamedata+0x01`, inside the known persistent event-flag block. It is the strongest **unverified** flag candidate. Other changes `0x8015C86B: 01 → 02`, `0x8015CC30: 5C → 5D`, `0x8015CC7A: 01 → 00` require further tests. Previous hypothesised battery slot `0x8015C70B` was in the scan but did not change.

Capture C was **not taken** and is generally inappropriate after an irreversible collection. In v1 exports, `reverting_changes` was erroneously incremented without C. That count was fixed: without C, only `observed_changes` has meaning. Keep the full before/after JSON as your private diagnostic (do not commit it to the public repository).

## Sasuke second battery acquisition and cutscene distinction (2026-11-02)

The user supplied second pickup A/B JSON with Sasuke in map 329, 5.921 s between reads. **No primary event-flag bytes changed** (including `0x8015C609`), though the user separately saw `0x8015C609 = 0x60`. Extra bit `0x40` is only a candidate for second-battery progress; its actual write timing was **not captured**. Manually writing `0x60` did not replay the second pickup's cutscene; persistent completion state and one-off pickup script execution should be investigated separately.

Possible transient changes `0x8015C562 00→01`, `0x8015CD07 00→01`, `0x800C7A71 00→01`, `0x800C7AE2 00→01` were seen, but no causal role is established. The probable time byte `0x8015C86F` advanced by 5 over 5.19 s in the first comparison and 6 over 5.92 s in the second. A/B is not a C revert test; ignore older erroneous `reverting_changes=81` metadata when `capture_C=null`.

**Recommended high-resolution test:** Log the confirmed first-byte `0x8015C609` before second battery appears, immediately before contact, during pickup cutscene, after playback and after reload. Confirm whether `0x40` is the second stage gate by writing only that bit into an actual uncollected state; do not assume a state-bit write initiates the cutscene.

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
| Selected item/weapon | Capture A/B/C while changing only the selected weapon (C-Left), or the selected inventory cursor in the pause menu. | **Equipped weapon is confirmed at `0x8015C607` (u8, slots 1–3).** The consumable inventory cursor remains unmapped. |
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
