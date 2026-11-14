# Japanese NG5J live status — source-backed, read-only

This extends the already working Japan-0 Mupen64Plus PID/RDRAM attachment with a **dedicated Japanese Live tab**, without applying a global USA-to-Japan RAM offset or permitting memory edits.

## What is supported

- Select **Japan - Ganbare Goemon**, verify the exact 16 MiB NG5J revision-0 retail ROM, set target `mupen64plus`, and attach to its running PID.
- After the three Japanese executable probes validate RDRAM, the GUI opens **Japan Live (read-only)**.
- The tab displays **58 independently address-specified published cheat-code field leads** organised by Vitals, Party, Weapons and skills, Items, World map, and Modes and engine. One debug-mode address is independently published by TCRF; the rest come from the Japanese GameHacking.org cheat listing.
- Every row displays original N64 guest address, decoded numeric/flag value, big-endian raw bytes, and evidence/validation status. Background polling updates at most every 0.75 seconds. A Refresh button forces an update.
- Implausible flags (e.g. a value other than 0/1) remain visible and are marked `CHECK: unusual value`, rather than being silently normalised. Failed reads stay isolated to their rows.
- The underlying Japanese process handle is still **writable=False** and kept as `self.jp_rdram`, never `self.mem`. The existing USA memory editors/freezes/checkpoints/warps are unavailable in Japan mode.
- The global footer explicitly reads **JAPAN RAM READ ONLY**, rather than the USA default `Memory writes enabled`. The legacy raw 1–64 byte reader remains on the Dashboard.
- The Japanese status table is cleared on detach, ROM switch or savestate load. This prevents stale data being displayed from an invalidated RAM base.

## Published addresses (NG5J revision 0)

Authoritative external source for this phase: [GameHacking.org — Ganbare Goemon NG5J](https://gamehacking.org/game/20438) (26 published GameShark cheats). The debug-menu address is independently provided by [The Cutting Room Floor](https://tcrf.net/Mystical_Ninja_Starring_Goemon_(Nintendo_64)).

| Field | Address / type | Evidence |
| --- | --- | --- |
| Maximum HP (low byte) | `0x80161DD3` u8 | JP infinite HP cheat |
| Current HP (low byte) | `0x80161DD7` u8 | JP infinite HP cheat |
| Ryo | `0x80161DDA` u16 BE | JP infinite Ryo cheat `81161DDA 270F` |
| Lives (low byte) | `0x80161DDF` u8 | JP infinite lives cheat |
| Riceballs, helmet, armour | `0x80161DE3/E7/EF` u8 | JP supplies |
| Sasuke, Yae in party | `0x80161E97/9B` u8 | JP party cheat |
| Four weapon levels | `0x80161E9F` +4 ×4 | JP `50000404` repeat |
| Four super weapons | `0x80161EAF` +4 ×4 | JP repeat |
| Four sub-weapons | `0x80161EC3` +4 ×4 | JP repeat |
| Four Jutsu skills | `0x80161EDF` +4 ×4 | JP repeat |
| Triton Shell, Super Pass | `0x80161EEF/F3` u8 | JP cheats |
| Benkei weakness, Cucumber | `0x80161EFF`, `0x80161F07` u8 | JP cheats |
| Red, yellow, blue fish | `0x80161F0B/0F/13` u8 | JP cheats |
| Four treasures | `0x8016204B` +4 ×4 | JP repeat |
| World map access | `0x80162063` u8 | JP cheat |
| 16 world-map stops | `0x8016209F` +4 ×16 | JP repeat |
| Total-time counter (raw) | `0x8016205C` u32 BE | JP cheat uses two 16-bit writes; unit unknown |
| Three mode / bonus-song flags | `0x8016240B` +4 ×3 | JP repeat |
| Debug-menu game state | `0x800CD284` u8 | TCRF JP GameShark code, value 10 enters menu |

**Do not assume every field is completely documented.** The four-slot repeated cheats establish slot locations but not reliable individual item names. The three mode flags are unlabelled. Total playtime is left as a hex counter because its unit is not established. There is no automatic USA `+0x57F0` translation in code.

## Status / validation

- Nine decoder tests and three real Tk widget tests passed using synthetic RAM (12/12 locally). Tk tests run under `xvfb-run -a` on a headless Linux CI host.
- No actual running Japanese Mupen was available in the test container for dynamic field confirmation. The prior read-only PID attach **was confirmed working by the user** with raw Japanese code bytes at `0x80000450`.
- These are externally published **cheat addresses**, not fully replayed Japanese game-state observations. Health, Ryo, lives, flag transitions and world-map progression should be checked in Japanese gameplay before treating them as validated.
- Scene ID, player object, task pointers, coordinates, active actor list and script VM require separate code analysis and runtime traces. The base offset `+0x57F0` is supported for several global fields but not every game symbol or overlay.
- Running the Japanese ROM in Goemon64Recomp still requires Japanese-generated recompiler code, overlay relocations, patches and a separate executable; this UI change does not solve that build.

## Tests

```bash
python3 -m unittest tests.test_japanese_fields -v
xvfb-run -a python3 -m unittest tests.test_japanese_fields_ui -v
```

The new Japanese functionality is on `chatgptweb/japan-readonly-gameplay-fields`, stacked on PR #11. The standalone USA external cheat/actor registry remains separately recorded on PR #12 for the next decomp session.
