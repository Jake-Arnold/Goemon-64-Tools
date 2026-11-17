# USA Goemon external memory, cheat and actor leads (source-only)

This register records previously **unmapped in the active USA toolkit** locations found while reviewing The Cutting Room Floor notes, the TCRF main page and GameHacking.org. They are research leads **not** gameplay-validated, and this document makes **no change** to the USA or Japanese runtime memory readers, freezes, cheats, scene controls or write permissions.

Machine-readable data: `research/usa_external_memory_leads.json`.

## Provenance

- [TCRF USA-only notes](https://tcrf.net/Notes:Mystical_Ninja_Starring_Goemon_(Nintendo_64)) — source explicitly says GameShark codes apply to USA only; includes actor IDs/record patterns and code addresses.
- [TCRF game page](https://tcrf.net/Mystical_Ninja_Starring_Goemon_(Nintendo_64)) — debug menu code (USA and Japan separately), unused warp flags and other USA code modifications.
- [GameHacking.org USA NG5E](https://gamehacking.org/game/20650) — menu unlocks, warp-repeater, skybox, size, sound and miscellaneous cheats.

## New USA RAM/progression candidates

| USA address | External description | Evidence |
|---|---|---|
| `0x8015C8B7` | First of 11 repeating 4-byte-spaced warp unlock flags, through `0x8015C8DF` | GameHacking; GameShark `50000B04 0000` / `8015C8B7 0001` |
| `0x8015C8E0` | Gourmet Submarine Castle warp entry | TCRF |
| `0x8015C8E4` | Folkypoke Village dragon warp entry | TCRF |
| `0x8015C8E8` | Awaji Island warp entry | TCRF |
| `0x8015CC1B` | Consecutive large-boss option unlock | GameHacking |
| `0x8015CC1F` | I Am Impact sound-test unlock | GameHacking |
| `0x8015CC21` | Gorgeous My Stage sound-test unlock | GameHacking |
| `0x80167FE9` | Skybox selector candidate | GameHacking; conditional code with unknown selector values |
| `0x8014C334` | Three-component size vector (also `0x8014C338`, `0x8014C33C`) | GameHacking; 16-bit half-word patches from an Ultimate Size Modifier |
| `0x800C7D3B` | L-button input condition in USA debug-menu cheat | TCRF |
| `0x800C7D3A` | Button masks used by size modifier | GameHacking |

The warp and sound-test flags are plausible data fields, **not** locally confirmed safe write targets. The size vector may be temporary scene/actor state rather than the permanent player object.

## Other USA code/patch addresses to preserve as leads

- `0x801F4FB3` — always-fire-Ryo cheat (`801F4FB3 0012`).
- `0x801D7967` — unused Impact projectile (GS-triggered `881D7967 0047`).
- `0x801E1AA8` through `0x801E1AAE` — conditional I Am Impact song instruction patch.
- `0x801E20BA` — conditional Super Jump instruction patch.
- `0x80204156` — Yae footstep sound patch; published replacement value `????` is **missing**.
- `0x801DECC3` — conditional crawling/unused animation selector.
- `0x80216EAC`, `0x80216EB3` — unusual GameShark 89/88 warp-screen patches.
- `0x801E7E04` — Ebisumaru small-form weapon modification.
- `0x801F9ED0` — background music suppression cheat.
- `0x8016A070` — hyper-character code.
- `0xA0172972` — Xplorer64 echo cheat.

Original cheat types and values are preserved verbatim in the JSON: **80, 81, 88, 89, A0 and Xplorer64 codes do not all have the same write semantics**. Some published 80-prefixed codes contain wider-looking values such as `2400`; do not guess a byte/half-word width.

### USA code function leads from TCRF

| USA code address | External label |
|---|---|
| `0x80218A98` | Grabs first map actor into `T8` |
| `0x80216CE0` | Loads graphics |
| `0x80218AF4` | Loads actor positions into `T6` |

These are **instruction addresses**, not readable game-status fields or persistent character pointers.

## Actor catalogue from the notes

There are **47 externally annotated actor IDs** in the JSON, including `0x0088` Silver Doll, `0x0089` Gold Doll, `0x008E` death plane, `0x0192` Pot, `0x0193` Key, `0x0308` fixed-camera actor and `0x0323` Congo. NPC, enemy, key and pot record sketches are stored verbatim with notes. Do not treat these as confirmed Japanese actor IDs or record offsets until independently checked.

## Regional cross-check: independent +0x57F0 examples

The TCRF main page publishes region-specific debug menu codes:

| Meaning | USA | Japan | Difference |
|---|---|---|---|
| Debug-menu state field | `0x800C7A94` | `0x800CD284` | `+0x57F0` |
| L-button input conditional | `0x800C7D3B` | `0x800CD52B` | `+0x57F0` |

The first **USA** state field was already known in `practice/checkpoints.py`; only the USA L-button conditional is a new USA lead. The matching Japanese values offer two additional **regional offset checks**, but `+0x57F0` must **not** be applied blindly to all ROM code, overlays, actor pointers or RAM objects.

## Deliberate exclusions and limitations

The following user-provided USA fields were already present in toolkit definitions and **are not counted as new**: `0x800C7A94` debug state, `0x8015C6A7` Sasuke and `0x8015C6AB` Yae party flags, `0x8015C6AF/B3/B7/BB` weapon upgrades and `0x8015C85B/5F/63/66` Miracle items.

No external cheat has been executed or checked against a running USA game in this update. The new records are kept out of built-in Watch/Inspector/Unlocks lists until their field type and intended runtime semantics are verified separately. In particular, never automatically export instruction-patch addresses as editable live-memory fields.
