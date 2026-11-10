# Waterfall of Kegon hint condition

User observation, 2026-11-03: speaking to an NPC in Festival Village East who
mentions the Waterfall of Kegon sets `0x8015C610 & 0x10`, saved ID `0x044` (68).
The changed bit is decimal 16. The supplied saved session's supporting pair is
whole-byte `04 -> 14` hexadecimal, preserving the pre-existing `04` bit.

## Existing annotation and interpretation

Pinned mn64rando `9c580d03fe89354f79c3c83ba2e1bcf192f32577`,
`tables/parser_config_en.yaml`, already annotates ID `0x044` as the condition for
Plasma's Waterfall of Kegon advice. This is corroboration of existing research,
not a newly claimed discovery of the flag. The surrounding annotated flags also
concern Plasma's advice progression.

The user suspects a learned-information prerequisite. The present evidence
supports the NPC conversation setting an advice-related condition. It does not
yet prove the flag opens the waterfall, changes its loading zone, or is required
to progress there. The tracker therefore says Plasma Waterfall of Kegon hint
condition, rather than Waterfall unlocked.

## Read-only ROM reference candidates

Verified decompressed US ROM SHA-1:
`6ea0ed71032ce08fc2745f412d84936382197494`.

| File ID | Decompressed ROM position | Pattern |
| --- | --- | --- |
| `0x063` | `0x76DA60` | Set ID `0x044` |
| `0x063` | `0x76DACC` | Set ID `0x044` |
| `0x070` | `0x7A2404` | Branch if ID `0x044` is set |
| `0x070` | `0x7A2450` | Set ID `0x044` |

The branch encodes local target `0x08003A34`, corresponding to ROM `0x7A2464`
within that file. These four aligned GEV patterns are leads, not a complete
control-flow/native-dataflow analysis. No native-file scan was requested; zero
native results therefore say nothing about native uses. Detailed report remains
in ignored diagnostics. No dialogue text, raw scripts, screenshots or private
trial identifiers are committed.

## Interpreting 1/4 event support

The three unchanged trials supplied with the report cover other map contexts
 (maps 406, 377, and 377 to 378), not established pre-state repeats of this
same NPC event. This particular bit was clear in both A and B in each of them.
The supporting trial stayed on map 378 and changed this bit from clear to set.
Thus 1/4 describes this mixed session's evidence; it is not four controlled
attempts at the same event or a 25-percent probability that the flag is correct.
Start a separately named experiment and restore the same pre-event state for
actual repetition. No recording/ranking rules were changed here.

Next: trace the reader's dialogue branch and compare Plasma's advice with the
bit clear/set before assigning any physical-access meaning. No assistant game
writes, freezes, save reloads or independent live reproduction were performed.

Follow-up: the common Plasma event's own ocean-advice path can also set
`0x044`; when that later check is reached with the earlier priority conditions
satisfied, it routes to the Kegon sign advice. See the full
[ordered Plasma conditions](PLASMA_TRIGGERS.md).
