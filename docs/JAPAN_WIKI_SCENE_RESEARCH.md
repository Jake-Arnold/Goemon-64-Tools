# Japanese scene-memory research and Wiki review

## Source assessment

- Newer gameplay wiki: https://w.atwiki.jp/match6974/
- Earlier wiki: https://wikiwiki.jp/goe1070momo/
- The newer wiki explicitly names the older one as its predecessor. The two are not independent corroboration of memory addresses.
- Neither source provides a verified Japanese-RAM player-pointer or full scene-global table.

Relevant playable test cases:

1. Forty-five Fortune Dolls are documented, split into 40 silver and five gold, with locations and required abilities: https://w.atwiki.jp/match6974/pages/23.html and https://wikiwiki.jp/goe1070momo/招き猫一覧. Locations do not establish corresponding RAM bit positions.
2. Japan map-glitch: holding C-Right through a transition can suppress interactive objects/events. The wiki lists freeze-prone doors. Do not trigger this automatically or treat its failure list as a safe-warp table: https://w.atwiki.jp/match6974/pages/17.html and https://w.atwiki.jp/match6974/pages/19.html.
3. Speed and motion probes: 7-frame jump (6 on slopes/underwater), 1-frame entry acceleration, chain-pipe movement, wall edge-running and slope techniques. These are useful once player position/action data is mapped: https://w.atwiki.jp/match6974/pages/30.html and https://w.atwiki.jp/match6974/pages/18.html.
4. Weapon and ability progression can be checked against the four Japan weapon-level watches: https://w.atwiki.jp/match6974/pages/24.html.

## Evidence and limitations

The earlier Japanese Mupen64Plus PID attach was confirmed by a live code read. The user reports that the 58 Japanese cheat/debug watches in PR #13 respond well. That is useful empirical feedback but does not verify the semantics of every published cheat field.

TCRF provides explicitly regional debug codes for USA 0x800C7A94 -> Japan 0x800CD284 and USA 0x800C7D3B -> Japan 0x800CD52B. Both have displacement +0x57F0. This is a clue for a limited region of globals, NOT a general instruction to relocate every value by +0x57F0.

## Ten scene candidates, unverified, read only

| Label | USA value | Japan candidate | Width |
|---|---|---|---|
| Current scene ID | 0x800C7AB2 | 0x800CD2A2 | u16 |
| Phase | 0x800C7A9E | 0x800CD28E | u8 |
| Submode | 0x800C7AA4 | 0x800CD294 | u8 |
| Previous scene | 0x800C7ABC | 0x800CD2AC | u16 |
| Pending scene | 0x800C7CA0 | 0x800CD490 | u16 |
| Transition flag | 0x800C7AD6 | 0x800CD2C6 | u8 |
| Exit request | 0x800C7A9F | 0x800CD28F | u8 |
| Pause flag | 0x800C7AE6 | 0x800CD2D6 | u8 |
| Character index | 0x8015C5DC | 0x80161DCC | u32 |
| Loading word | 0x8015C5D4 | 0x80161DC4 | u32 |

These addresses are deliberately enumerated in practice/japanese_scene_probes.py, tagged as UNVERIFIED regional-offset hypotheses. The independently reported Japan debug state at 0x800CD284 remains in the 58 cheat/debug watches and is not duplicated.

## Test workflow

The Japan Live tab has 58 cheat-backed entries and a separate 10-row scene research group. With the verified external Mupen64Plus PID attached, Capture baseline reads the current raw bytes. Change scene through ordinary gameplay, then Compare to mark fields whose raw bytes changed. Copy changes places the raw-byte comparison in the clipboard. It does not modify the game. Comparison continues updating every 0.75 seconds. Baseline and changes are cleared on disconnect, region change and savestate load; a different PID or RAM base invalidates the comparison.

A changed value is evidence of association, not complete proof of field meaning. There are no Japanese-specific writes, input triggers, freezes or warps.

## Tests

Python unit tests were added for unique/ranged addresses, read-only reads, per-field errors and raw-byte comparison. Tk tests were expanded for table presence, baseline/compare, and invalidation on PID change.

The independent build commands are:

python3 -m unittest tests.test_japanese_scene_probes tests.test_japanese_fields -v

xvfb-run -a python3 -m unittest tests.test_japanese_fields_ui tests.test_japanese_scene_probe_ui -v

No actual Japanese player/task pointer values or native Goemon64Recomp boot were established by this work. The USA decomp research stays separately on PR #12.
