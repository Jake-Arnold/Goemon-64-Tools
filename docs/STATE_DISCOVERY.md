## Code-backed follow-up (2026-11-02)

[Later Benkei/Kihachi tracing](BENKEI_KIHACHI_TRACE.md) identifies the referral/
native initialization gate as `0x8015C60C & 0x08` and the later Benkei dialogue
condition as `0x8015C60E & 0x04`. Setting the whole latter byte to `2E` also forces
unrelated reward flags; use isolated masks from a preserved baseline. The report
includes existing-source coverage so already annotated states need not be
rediscovered by blind value tests.

[Original-ROM tracing](ROM_FLAG_TRACE.md) now verifies bitwise OR in the event
set helper and identifies `0x8015C60D & 0x80` as the failed Mini-Ebisu training
dialogue selector. Passing training (`0x8015C60D & 0x40`) is separate from magic
granted/recorded (`0x8015C60E & 0x02`) and ability ownership (`0x8015C6F3`). The
report supplies script checks/writes and new reference-index tooling; native
result-writer and actor-placement tracing remain incomplete. The historical
gameplay reports below remain distinct evidence.

## Ushiwaka dialogue-stage findings (2026-11-02)

The user mapped full-byte states at `0x8015C60D`: `00` introduction not asked,
`20` “Who are you?” asked/repeat option, `30` first fish-set dialogue, `38` five
yellow fish dialogue, `3C` eight red fish dialogue and `3E` this sequence's
finished dialogue. The user then forced `3F`: Ushiwaka relocated to Golden Temple
and the Ebisumaru magic-power minigame became available. Completing that minigame
normally produced `7F`, initially putting Ushiwaka outside the temple. After
reload the priest was back inside the temple gardens and Ushiwaka was tiny on
the original-location fence; the user reports the same `7F` dialogue at both
tested locations and no later Ushiwaka story involvement on this route. Actor
placement immediately after the event and after reload must be recorded separately.
Subsequent tracing identifies `0x80` as failed-training dialogue; setting a progression value does not itself prove
ability ownership, reward delivery or an exhaustive story/script audit.

The sequence successively retains and sets bits `0x20`, `0x10`, `0x08`, `0x04`,
`0x02`, `0x01`, then `0x40`. The observations alone did not distinguish addition
from OR; subsequent ROM tracing verifies OR in the flag-set helper. Preserve unrelated bits when
editing. These are user-reported gameplay findings, not new assistant-run write
or code-trace tests. See `practice/MEMORY_MAP.md` for the stage table and evidence
boundaries. The historical blue-fish hand-in observation below describes entry
into `38`; the reported yellow-fish dialogue describes the resulting stage.

Benkei separately changes `0x8015C60E` to `18` after the fight and says “cross any
time you wish”, according to the user. This adds `0x08` to the known `10`
first-dialogue state. A post-fight observation is distinct from proof that a
direct flag write reproduces the fight or all crossing effects.

## Ushiwaka storyline and character-at-spawn investigation (2026-11-02)

Two focused A/B captures taken with Goemon in map 371:

1. **Start Ushiwaka minigame**, `2026-11-02 11:00:51.517→11:01:04.456 UTC`: persistent event byte `0x8015C60D` goes `20→30`, **bit 0x10 set**. This is a strong start-state candidate, not a proven control.
2. **Complete blue fish step**, `11:02:05.125→11:02:09.012 UTC`: same byte `30→38`, **bit 0x08 set**; blue fish at `0x8015C723` falls `03→00`. This is not necessarily the Achilles' Heel/final quest-completion flag; do not conflate acquisition, fish hand-in, and Benkei dialogue progression.

Sasuke's second battery completes its cutscene **before** setting `0x8015C609 & 0x40`. A read-only indicator is now visible in the Unlocks tab; writing this bit by hand cannot invoke the cutscene.

The prior character-select scan at `0x800C7E60` traced 12-byte-spaced pointers while the original character menu was active. The user also observed a persistent value of 128 after visiting the menu, so the address **does not serve as a stable gameplay character selection register**. The experimental scene browser no longer simulates post-load C-Down. It stages the global character ID `0x8015C5DC` immediately before requesting state 0x0C, on the hypothesis that the area-entry model loader reads that ID. **Unverified**: area reset could overwrite it. Tool verifies global and task local ID on the destination and does not repair a mismatch through input injection.

## Benkei and Ushiwaka story-event protocol (2026-11-02)

Use **State discovery → Storyline event / quest flag**, preferably **focused**, and make separate A/B captures for distinct events; do not use C for one-time story flags. Begin with a disposable checkpoint before each event and avoid moving rooms/characters between A and B. Record the precise stage of the dialogue/cutscene relative to each capture.

1. **First Benkei dialogue:** A directly before first approach; B once the initial conversation finishes. Then repeat conversation and compare with a new A/B to separate initial encounter from recurring dialogue.
2. **Ushiwaka fish completion:** A immediately before the fish hand-in; B immediately after the minigame reward and cutscene conclude. Do not assume Achilles' Heel ownership by itself changes this progression bit.
3. **Item-only control:** from an otherwise identical pre-completion state, A before inserting Achilles' Heel into the inventory, B after inserting it without completing Ushiwaka. Compare with the genuine reward event to distinguish inventory from storyline completion.
4. **Fish shortcut control:** separately add only the required fish and perform the normal Ushiwaka turn-in. The user found fish inventory is enough to satisfy the minigame without manual fish collection; identify which event flags then change at real completion.

New JSON field **`event_flag_changes`** captures changes only inside original persistent event bitfield `gamedata+0x00..+0x63` (`0x8015C608..0x8015C66B`), reporting **bits_set**, **bits_cleared**. These remain candidates until repeated observation and causal masked write tests. Changes elsewhere, player motions and timer bytes are likely incidental. A/B captures never certify reversibility: `reverting_changes` is zero without C.

**Cutscene note:** a persistent quest flag may suppress a pickup or unlock dialogue without executing the cutscene callback. Identify script execution separately rather than treating a completion bit as an event trigger.

## v0.11.0: staged cross-area checkpoint restore and asynchronous Connect

Restoring an existing logical checkpoint from another map now requests a scene reload using the confirmed experimental sequence, waits for map ID and stable gameplay, and **only then** restores checkpoint XYZ, rotation, progress and resources. This bypasses the prior manually required trip to the saved map but does not reproduce native entrance scripts, enemy state, physics or camera. Native character switching is still required if the character differs. The game must actually reach the saved map; a wrong-map outcome or timeout cancels the checkpoint restore.

Connection discovery runs on a separate worker thread, with results marshalled to Tk's main thread. During memory scanning the app stays responsive.

## First Sasuke battery flag verified (2026-11-02)

`0x8015C609 & 0x20` is confirmed by writing the bit before collecting pickup. On reload pickup was gone and second battery became accessible later. The app now masks writes to preserve other progression flags. Second battery remains unmapped, pending a separate capture.

## Native character cursor scan and battery cutscene timing (2026-11-02)

On second battery pickup, `0x8015C609` changes from `0x20` to `0x60` **only after the cutscene completes**. The added bit `0x40` is a post-cutscene progression marker, not the script trigger itself. It is decoded read-only in Live Memory.

The repeated eight-step native debug menu character cursor scan (menu state 0x0A, map 404) matches a **u32 menu entry pointer** at `0x800C7E60`: Goemon `0x8007BAD0`, Ebisumaru `0x8007BADC`, Sasuke `0x8007BAE8`, Yae `0x8007BAF4`. Values follow 12-byte table entries and repeat in the reverse sweep. The 8-bit/16-bit candidates at +3/+2 are overlapping parts of this pointer; no zero-based 0..3 direct RAM field was found. These are **read-only observations**, and the pointer is not safe to write to change gameplay character.

**Scene browser fix:** the dropdown previously controlled only the separate native menu action; an experimental reload ignored it. Experimental reload now requests the selected character via ordinary post-load C-Down if unlocked, verifying the native model/task. This is **not** a native debug-menu spawn and does not correct entrance coordinates.

## Experimental test harness (v0.10.8)

The app now includes two *deliberately manual* experiments. **Scene browser → EXPERIMENT reload** writes pending destination `0x800C7CA0` followed by game state `0x0C`, logs result and position. Do not infer correct entrance spawn. **Live memory → Experimental movement** resolves `PlayerTask +0x68` dynamically and sends 4-byte f32 values. Press `+4.0`, `-4.0`, or `Speed pulse ×1.5`, compare observed XYZ motion in controlled gameplay. The task field is still unknown; an observed nudge is not proof it is velocity. The app never writes eight adjacent bytes in these controls.

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

## Additional C-Right map comparison (2026-11-03)

The user captured map off → on → off using C-Right. `0x8015C574` changed
`00 → 01 → 00`, consistent with the previously observed read state. Other
changes appeared in player-task bytes; their role is unknown and the displayed
float candidate overlaps changing bytes, so it is not established as a float.
This is an event correlation, not a new independent finding of safe write
behavior; earlier direct-write tests remain relevant.

The user's additional wide A/B/C export compared one 4 MiB region. It reports
106,840 changed A→B bytes, 30,443 returning to A, and retains the top 1,200
ranked candidates. The established `0x8015C574` row is among them; the large
number of simultaneous changes prevents attributing other candidates to the map
without repeated focused tests or a control. The export does not contain all
30,443 candidate rows, and no additional flag is confirmed by it. The personal
raw export remains local and is not part of the repository.
