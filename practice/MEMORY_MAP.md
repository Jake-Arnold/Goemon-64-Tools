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

### Sasuke battery #1 pickup probe (2026-11-02)

- Same map 330, Ebisumaru; A/B only (no C), immediately before/after collecting the first battery. Label "Map displayed" on JSON is incorrect for actual action.
- **Best candidate:** `0x8015C609`, `00 → 20`. This is **gamedata+0x01, bit `0x20`** in the saved event-flag bitfield `gamedata+0x00..+0x63`; pickup control still unverified.
- Secondary `0x8015C86B`, `01 → 02`, might be progression counting but unverified. `0x8015CC30`: `5C → 5D`, `0x8015CC7A`: `01 → 00`.
- Earlier guessed battery address `0x8015C70B` remained unchanged in the scanned region; **not supported by this pickup**.
- To verify, modify only bit `0x20` at `0x8015C609` and test stage reload/second battery progression with a disposable save. Do not overwrite other event bits.

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
- Same-map/character checkpoint restoration restrictions remain. A different room must actually be loaded by the original game before restoring its progression data.
- The memory browser is read-only. The `practice/diagnostics` files contain observations and are suitable for investigating which flags changed across gameplay events.
- Recomp UI and Windows process APIs are adapters, never required by the portable C core.
