## Benkei first-conversation state — replayed and user-tested (2026-11-02)

### User-reported timing and write tests

- **`0x8015C60E`, observed mask `0x10`: first-dialogue completion/gating state.**
  Setting this byte to `00` restores the first dialogue on the next conversation.
  The byte becomes `10` at the **end of the conversation**. This is user-reported
  in-game write evidence for restoring the first-dialogue path, beyond A/B
  correlation. It does not establish general quest completion or that writing
  `10` by itself reproduces every consequence of completing that dialogue.
- **`0x8015C60C`, observed mask `0x20`: first-encounter trigger-entry marker.**
  The byte becomes `20` **immediately on reaching the cutscene trigger**, before
  the conversation finishes. Clearing it to `00` while `0x8015C60E` remains `10`,
  then returning to Benkei, neither restores the first dialogue nor sets this
  byte back to `20`. Clearing this marker alone is therefore insufficient to
  reset the first encounter in the tested state.
- **Interpretation:** selection of the first-conversation path appears to depend
  on the completion/gating state at `0x8015C60E`; the trigger-entry update at
  `0x8015C60C` appears conditional on that path. This is an inference from the
  reported behavior, not a recovered script condition or proof of a direct
  dependency between the two fields.

These manual tests were reported by the user, not replayed or traced by the
assistant. They cleared **whole bytes**. The earlier captured `00/20` and `00/10`
transitions identify masks for this state, but unrelated-bit preservation and
isolated masked-write behavior still need verification. Future targeted edits
should clear only `value & ~0x10` or `value & ~0x20`, respectively, retaining all
other bits; that operation is a proposed test, not additional observed evidence.
No new write control is introduced by this documentation update.

### Captured independent trials

Read-only Goemon64Recomp experiment on map **369**, Goemon, with stable player
and task pointers throughout each pair:

| Address / mask | First-conversation A → B | Idle control | Repeat conversation |
| --- | --- | --- | --- |
| `0x8015C60C & 0x20` | byte `00 → 20`, bit set | unchanged | unchanged, bit stays set |
| `0x8015C60E & 0x10` | byte `00 → 10`, bit set | unchanged | unchanged, bit stays set |

The user reported the repeat dialogue as **“so you're back again”**. No other
bytes changed within the captured 100-byte persistent-event block in either
control; the first-conversation pair changed only the two bytes above.

An independent reset/restart and replay reproduced **both exact byte changes**
on map 369 with Goemon. Both 100-byte A blocks match, and both 100-byte B blocks
match. Each bit has event support **2/2**, with no idle or repeat-dialogue changes.

These stored trials alone are **first-conversation interval observations**;
the user-reported tests above add distinct timing and whole-byte intervention
evidence. No isolated masked-write test or original-code reader/writer trace has
been done. ROM identity remains unverified against the running host.

Local evidence session `79b2f960edab424f89d68ed7e0415691`: idle trial
`c82d73fde48641d6a7440d9791aa70b3`, event trial
`4137f3c0e97744358e0ef68d07fe97e6`, repeat-dialogue control
`55d08ff62b574adf8b28f17dd2dcb6e8`, independent replay
`3d04720d7f554a448867a8990dfdd22b`. Raw samples and notes stay in ignored local
diagnostics. Next: trace the dialogue branch, completion write and trigger-entry
write in original-game code, and verify the corresponding masked operations
before exposing dedicated write controls.

## Ushiwaka progression and pre-load character hypothesis (2026-11-02)

- **Ushiwaka minigame start:** `0x8015C60D`, bit `0x10`, observed `0x20 → 0x30`, same character/map 371. A/B only; **not write-confirmed**.
- **Blue-fish hand-in:** `0x8015C60D`, bit `0x08`, observed `0x30 → 0x38`, alongside blue fish `0x8015C723` 3 → 0. A/B only; **not write-confirmed**. Does not establish Achilles' Heel or final Benkei story gate.
- **Sasuke battery 2:** `0x8015C609`, bit `0x40`, becomes set at **end of** pickup cutscene. Never treat bit write as cutscene execution. Visible read-only in Unlocks and Live Memory.
- **Original debug menu cursor pointer:** `0x800C7E60` repeated pointer sequence is valid during active character highlighting only; user's later 128 value demonstrates nonpersistent interpretation. No writing this pointer for warp.
- **Experimental initial character load:** user-selected `0x8015C5DC` (u32) is written before `0x800C7A94=0x0C`, to test whether the area-entry actor loader uses the staged character ID. Neither character-at-spawn nor model/entrance correctness is proven. No postload C-Down. Both loaded global and task character must agree.

## Second Sasuke battery conclusion + native character cursor scan (2026-11-02)

- Later user experiment isolates **second Sasuke battery bit `0x40`**: confirmed first-battery bit `0x20`, then the second battery cutscene finishes and byte `0x8015C609` becomes `0x60`. This confirms post-cutscene completion correlation; direct writes **do not play cutscenes**. Live Memory exposes bit 0x40 read-only, separate from the first battery bit 0x20.
- Native character cursor while original debug menu state `0x0A`: `0x800C7E60` **u32 pointer** values Goemon `0x8007BAD0`, Ebisumaru `0x8007BADC`, Sasuke `0x8007BAE8`, Yae `0x8007BAF4`. Eight forward/reverse captures, each stable. Stride = 12; the two byte/halfword hits at +2/+3 are aliases. **Pointer is not a character index**. No external write validation yet.
- Experimental reload's character dropdown now invokes *post-load ordinary C-Down* when target is in party. It does not reproduce native debug menu's requested entry character or solve wrong spawn.

## Benkei/Ushiwaka storyline flag investigation (2026-11-02)

- **Gameplay observations (no offsets confirmed):** Benkei's first conversation changes later dialogue. Ushiwaka fish-minigame completion plus Achilles' Heel reward advances another story stage; merely adding Achilles' Heel to inventory does not bypass that gate. Putting the required fish directly in inventory can satisfy the minigame without manually collecting each fish.
- Investigate quest/event flags in the persistent `gamedata` primary bitfield (`0x8015C608..0x8015C66B`). State discovery A/B exports `event_flag_changes` with XOR split into **bits_set / bits_cleared**. No C for irreversible story completion.
- Separate experiments: A before first Benkei talk/B afterward; A before fish turn-in/B after Ushiwaka reward dialogue; A before item-only cheat/B immediately after with **no NPC interaction**. Preserve a disposable checkpoint before each event. Inventory equality does not imply same quest state; identify gameplay script readers/writers next.
- Miracle symbols in Live Memory and Unlocks: Star `0x8015C85B`, Moon `0x8015C85F`, Flower `0x8015C863`, Snowflake `0x8015C866`. User-supplied mapping; avoid claiming a disassembly-level proof.
- Task+0x68 pulse buttons withdrawn after user observed only movement nudges. Do not treat it as reliable velocity.

## v0.11.0 checkpoint map and position restore (2026-11-02)

- Stage the saved absolute map ID as u16 at `0x800C7CA0`, then write `0x0C` to the top-level game state byte `0x800C7A94`. This experimentally requests the game to load the destination. **Do not** directly overwrite current map `0x800C7AB2` or the exit-request byte.
- Wait for `0x800C7AB2 == saved_map`, `0x800C7A94 == 0x0D`, a stable player object and no active transition/script, then write captured exact XYZ floats (`player_ptr +0x08/+0x0C/+0x10`) and rotation (`player_ptr +0x14` length 6) through the existing logical restore function. Saved position is the checkpoint's XYZ, **not** a guessed stage entrance.
- On character mismatch use the original native switch after map loading; do not force raw character IDs or pointers. Actor scripting/scene entrance semantics remain partially unknown. Timeout/cancellation and wrong-map guards leave checkpoint payload unwritten.

## Confirmed first Sasuke battery flag (2026-11-02)

- `0x8015C609 & 0x20` (`gamedata+0x01`): first battery collected/progression complete. Verified by writing it before pickup, then reloading; pickup disappeared and second battery became spawnable.
- Packed event byte: unlock buttons preserve all other bits. Old guessed `0x8015C70B` removed from battery mapping. Second battery unknown.

# New experimental observations (2026-11-02, v0.10.8)

- Reload trial: `0x800C7CA0` (pending destination, u16), then `0x800C7A94 = 0x0C` (game state reload). User saw destination map load but incorrect entrance coordinates. Tool now explicitly offers this exact pair, not the old exit flag; never describes the result as a fully correct warp.
- Task-relative f32: `PlayerTask +0x68`, an unnamed field declared `f32` in upstream `types.h`. User observed movement nudge on writes; genuine velocity is **not confirmed**. The tool resolves task pointer dynamically, writes exactly 4 IEEE-754 bytes, and provides ±4 and ×1.5 tests; no neighbouring +0x6C changes.
- Selected weapon: `0x8015C607` (u8, 1–3) confirmed all characters; map visible state `0x8015C574` read 0/1 but manual writes are side-effectful; `0x800C7A73` not magic.

---

# Original MNSG (USA) memory-map watch specification

All addresses below are **original guest N64 addresses** (not host-process pointers). The only confirmed working *host* integration at present is the v0.2 PC RAM discovery and XYZ display; live validation for the new fields is still required.

## Fields to validate against the game UI

| Meaning | Address | Guest representation | Confidence |
| --- | --- | --- | --- |
| Character | `0x8015C5DC` | u32, 0–3 | high (Goemon64Recomp `variables.h`) |
| Current map | `0x800C7AB2` | u16 | high (Android fork static RE notes) |
| Max health | `0x8015C5E0` | s32 | high (Android fork static RE notes) |
| Current health | `0x8015C5E4` | s32 | high |
| Ryo | `0x8015C5E8` | s32 | high |
| Lives | `0x8015C5EC` | s32 | high |
| Item code slot 1 | `0x8015C5F3` | u8 | confirmed by user in live game |
| Item code slot 2 | `0x8015C5F7` | u8 | confirmed by user in live game |
| Item code slot 3 | `0x8015C5FF` | u8 | confirmed by user in live game |
| Item 2 quantity | `0x8015C5FB` | u8 | confirmed by user in live game |
| Item 3 quantity | `0x8015C603` | u8 | confirmed by user in live game |
| Party membership | `0x8015C69F`, `0x8015C6A3`, `0x8015C6A7`, `0x8015C6AB` | u8 | provisional |
| Weapon upgrades | `0x8015C6AF`, `0x8015C6B3`, `0x8015C6B7`, `0x8015C6BB` | u8 | confirmed by user in live game |
| Stage progress / flags | `0x8015C608` + `0x304` | bytes, incompletely decoded | byte layout known, semantics incomplete |
| Global unlock header | `0x8015CC18` + `0x0C` | bytes | static RE |
| Live resource block | `0x8015C5D8` + `0x30` | bytes | high |
| Original-game native debug menu state | `0x800C7A94 = 0x0A` | u8 | code patch shown by ROM randomizer; not yet tested in US PC recomp |

**Equipped weapon index is confirmed at `0x8015C607` (u8, values `01`/`02`/`03`).** Carried item slot codes/quantities are distinct from this current-weapon selection. The currently highlighted consumable inventory cursor remains unknown.

Health has 2 internal units per visible HUD heart segment; typical starting state is HP 10 / maximum HP 10, ryo 100, lives 3. Live Ryo should not exceed 9999. Room/scene ID is NOT the saved continue-point ID at `gamedata+0x200`.

## Native debug menu category indices (user-observed 2026-11-02)

`0x800C7AA4` is a `u8` menu category when top-level state is `0x0A`; its gameplay meaning is context-dependent. **MAIN occupies index 0.** The first five categories are:

| Hex | Native menu row |
| --- | --- |
| `00` | MAIN |
| `01` | SIRO |
| `02` | DOUCHU |
| `03` | MACHI |
| `04` | SHOP |

The screenshot continues with OBOMBER, an unclear label, DATMAP, OPENING, GOPENING, BOSS3D.OP, DIARY, another unclear label and GAMEOVER. Last entry is index `0D`. The two unclear spellings remain provisional in `practice/native_menu_categories.py`. This category byte is **not** the top-level game-state byte `0x800C7A94`.

## Item slot addresses verified in-game

- Slot 1 code: `0x8015C5F3` (`u8`)
- Slot 2 code: `0x8015C5F7` (`u8`)
- Slot 2 quantity: `0x8015C5FB` (`u8`)
- Slot 3 code: `0x8015C5FF` (`u8`)
- Slot 3 quantity: `0x8015C603` (`u8`)

All five are user-confirmed. They represent **stored item slots and quantities**, not a proven currently equipped/selected item pointer.

## Confirmed weapon selection and clarified map/magic candidates (2026-11-02)

| Meaning | Guest address | Representation | Evidence |
| --- | --- | --- | --- |
| Equipped weapon index | `0x8015C607` | u8: `01`, `02`, `03` normal | User-confirmed for **all four characters** |
| Map overlay read state | `0x8015C574` | u8: `00` hidden, `01` visible | User-confirmed read behaviour; **manual writes do not act as a close toggle** |
| Magic-active candidate rejected | `0x800C7A73` | oscillating u8 `00`/`01` | Oscillates when magic is not activated |
| Selected-weapon candidate rejected | `0x8014C340` | u8 `40`/`41`, occasionally `00` | Oscillates outside weapon changes |

`0x8015C607` values outside 1–3 cause unexpected neighbouring-character weapons: Goemon -> Ebisumaru hammer; Ebisumaru -> Sasuke kunai; Sasuke -> Yae sword; Yae -> user-reported `letter 1`. These values must remain inspectable and only editable with the UNSAFE option; they should not silently clamp to three.

The map address may be involved in UI state and side effects. Do not equate writing `00` with closing the displayed map. The true magic-active flag remains unlocated.

Player-task f32 probes from Ebisumaru are **not proven velocity**: values also vary while stationary during NPC conversations. The `~192` maximum reported from byte watches is the numeric value of `0xC0`, the high byte of some negative f32 encodings, rather than a velocity cap. To inspect these fields, read four bytes as f32 and follow the live dynamic player-task pointer.

## Provenance

- Original recomp game types and player object pointers: https://github.com/klorfmorf/Goemon64Recomp/blob/dev/patches/variables.h
- Scene name list: https://github.com/klorfmorf/Goemon64Recomp/blob/dev/src/game/scene_table.cpp
- Resource/save data and map reverse-engineering: https://github.com/ogdanimal/Goemon64Recomp-Android/blob/main/docs/re-notes/goemon_save_re.md
- Health/ryo/lives disassembly: https://github.com/ogdanimal/Goemon64Recomp-Android/blob/main/docs/re-notes/goemon_cheats_re.md
- Item, party and upgrade address references: https://gamefaqs.gamespot.com/n64/198022-mystical-ninja-starring-goemon/faqs/3274
- Native debug-menu patch demonstrating original-game state 10: https://github.com/abyssonym/mn64rando/blob/master/tables/patch_debug_menu_en.txt

## Safety decisions

- No writes to guessed inventory offsets or raw scene ID.
- Original debug menu is the only currently exposed experimental method of entering a scene selector. It changes the top-level game mode, not the map number. Selecting a scene within the debug menu is still manual.
- Cross-map logical checkpoint restoration is now staged: experimental pending-destination/state-0x0C reload into saved map first; only after confirmed stable gameplay does the toolkit restore captured XYZ and game flags. This is not a native savestate or a verified native entrance loader.
- The memory browser is read-only. The `practice/diagnostics` files contain observations and are suitable for investigating which flags changed across gameplay events.
- Recomp UI and Windows process APIs are adapters, never required by the portable C core.
