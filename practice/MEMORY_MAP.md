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

**Selected equipped item is unknown.** Item slot fields are not necessarily an equipped/selected item. `UNKNOWN` is deliberately displayed rather than a made-up value.

Health has 2 internal units per visible HUD heart segment; typical starting state is HP 10 / maximum HP 10, ryo 100, lives 3. Live Ryo should not exceed 9999. Room/scene ID is NOT the saved continue-point ID at `gamedata+0x200`.

## Top-level game state: user-verified 2026-11-02 observations

Address: `0x800C7A94`, single guest-RAM byte. Editing this field can force a game state, but some values crash.

| Hex | Observed effect |
| --- | --- |
| `04` | Crash |
| `05` | Title screen |
| `06` | Title-screen song |
| `07` | Title idle/demo gameplay |
| `08` | Controller Pak use / do not use screen |
| `09` | Opening cutscene |
| `0A` | Native debug menu (previously established) |
| `0C` | Stage reload / re-entry |
| `0D` | Normal gameplay (previously established) |
| `0E` | Game over |
| `0F` | Crash |

**Live cross-stage reload demonstrated:** Write target stage ID to pending destination `0x800C7CA0` (u16), then set `0x800C7A94` to `0x0C`. The target stage loads, but the spawn XYZ/entry behavior is wrong. This is **partially working**, not a proven full native debug-menu equivalent. Need trace of entrance selection, spawn, facing, prior map and camera task initialization against original-menu stage entry.

## New A/B/C candidates (Ebisumaru, 2026-11-02)

- Map displayed `0x8015C574`: `00 → 01`, reverted on hide; **candidate**, not confirmed.
- Selected item/weapon `0x8015C607`: `01 → 02`, reverted on reselect; **candidate**, not confirmed.
- Magic active `0x800C7A73`: `00 → 01`, reverted at effect end; **candidate**, not confirmed. Secondary `0x8015C5CD`: `0A → 08`.
- Internal velocity **not mapped**: player task f32 candidates `+0x68`, `+0x70`, `+0x74`, `+0x78`, `+0x7C`, `+0xD0`. Full analysis in `docs/STATE_DISCOVERY.md`.
- No persistent dragon travel unlock mapping yet. 

## User-confirmed item slots and native menu category index (2026-11-02)

- Slot 1 code `0x8015C5F3` (u8).
- Slot 2 code `0x8015C5F7` (u8).
- Slot 2 quantity `0x8015C5FB` (u8).
- Slot 3 code `0x8015C5FF` (u8).
- Slot 3 quantity `0x8015C603` (u8).

All five addresses were verified by the user in gameplay. They describe stored item contents, **not** confirmed equipped-item selection.

While top-level state is `0x0A`, `0x800C7AA4` is the native debug-menu category byte and the screenshot shows `0x00 MAIN`, `0x01 SIRO`, `0x02 DOUCHU`, `0x03 MACHI`, `0x04 SHOP`, continuing through `0x0D GAMEOVER`. Two lower pixelated names remain uncertain. This is distinct from top-level state `0x800C7A94`.

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
