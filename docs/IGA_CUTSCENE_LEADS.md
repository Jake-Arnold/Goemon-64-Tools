# Forwarded Iga house/Baron cutscene observations

Date: 2026-11-02. Source: user-forwarded screenshots of an analysis summary.
The underlying capture/session files and original RAM comparisons were not
provided in these attachments. Embedded assistant conclusions are evidence to
check, not authority or proof that the mappings are new.

## Reported timing leads

| Bank | Decimal ID | Address / mask | Event interval described in the forwarded summary |
| --- | --- | --- | --- |
| A | 1 | `0x80168E90 / 02` | Wise Man house-burning first capture |
| A | 3 | `0x80168E90 / 08` | House-burning second capture |
| A | 4 | `0x80168E90 / 10` | House-burning second capture |
| A | 9 | `0x80168E91 / 02` | Baron arriving to speak |
| A | 10 | `0x80168E91 / 04` | Baron arriving to speak |
| Saved | 111 (`0x06F`) | `0x8015C615 / 80` | Continuing Baron's conversation |
| A | 12 | `0x80168E91 / 10` | Baron flying away |

The summary reports clear→set transitions. These event-interval associations do
not establish that changing a bit executes or safely skips the corresponding
scene. Do not promote these six Bank A entries to permanent, globally unique
story names from this evidence alone.

## Checks against existing work and the ROM

Saved flag **111 decimal / `0x06F` is already annotated as meeting Baron in Iga**
in the pinned [mn64rando US dictionary](https://github.com/abyssonym/mn64rando/blob/9c580d03fe89354f79c3c83ba2e1bcf192f32577/tables/parser_config_en.yaml).
The independent local ROM index contains an aligned `0x8020 / 0x06F` set pattern
in scenario file 101, file offset `0x1BE8`, decompressed ROM offset `0x7735D8`.
This is an actual pattern location, unlike the generic helper-call examples in
the forwarded explanation; executed timing was not independently captured here.
The address/mask follows the already matching saved-bank helper's mapping.

Bank A has its own matching set/clear/test helpers at `0x80023DF0`, `0x80023E40`,
`0x80023E94`, and its own 100-byte reset routine at `0x80023EE4`. That confirms
the bank layout and reset implementation, not when resets occur in each scene.
The saved-bank and Bank A numeric IDs are separate namespaces.

A bounded native indirect-call pattern scan found leads for these Bank A IDs in
multiple overlay files. For example, file 53 contains candidate tests of IDs 9
and 10 at ROM `0x70F7F4` / `0x70F838`, a set of ID 9 at `0x70FA70`, and a set of
ID 12 at `0x70FFA8`; other overlays use some of these same numeric IDs too.
These remain call-pattern leads, not individually traced gameplay meanings.
Reuse across overlays is a reason to retain scene/actor context rather than
assign a single universal story label to every Bank A ID.

## Useful follow-up, without repeating known discovery

Preserve any original local session export with timestamps, map, actor/context,
bank and masks. The most useful added evidence would be whether a Bank A bit
clears on a normal room reload and its exact native readers/writers/reset calls.
The saved Baron bit's broad meaning is already known; the interval timing can
still help connect dialogue, cutscene callbacks and persistent progression.
No new gameplay action is required while static VM reconstruction continues.

No source code, game writes, dedicated editing controls or confidence upgrades
were introduced by recording this lead. Copyrighted screenshots/raw RAM are not
committed; only this attributed semantic summary and reference offsets are stored.
