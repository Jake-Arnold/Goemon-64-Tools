# Oedo Castle silver key pickups and separate lock flag

Date: 2026-11-03. User captures corroborated by original-USA room definitions.

| Event | Map | Saved address/mask | Flag ID |
| --- | --- | --- | --- |
| 1F silver key collected | 7 | `0x8015C62A & 01` | `0x110` (272) |
| 2F silver key collected | 18 | `0x8015C62A & 10` | `0x114` (276) |
| Silver lock opened, transition to map 14 | 13 -> 14 | `0x8015C62A & 08` | `0x113` (275) |

All table masks are hexadecimal. The first saved pickup pair is byte `00 -> 01`;
the second is `01 -> 11`. The door-use pair is `11 -> 19`, setting only `08`
and clearing nothing. Therefore both collection-history flags remain recorded
after this door use. These flags are not current carried-key counts. No claim is
made about where or how the actual key inventory/count is decremented.

## Mixed session interpretation

The third screenshot retains the second pickup trial in the same session. Its
`10` set candidate comes from that earlier map-18 pickup; `08` comes from the
map-13-to-14 door trial. The 1/2 figures are not repeated verification of the same
action. The saved A/B bytes isolate the new door bit without clearing the session.
The default Benkei experiment title is not event identity evidence. No private
trial IDs, player/task pointers or screenshots are committed.

## Existing structure annotations and original room data

Pinned mn64rando `9c580d03fe89354f79c3c83ba2e1bcf192f32577` annotates Key actor
`0x193`: byte 5 is its type (0 silver, 1 gold, 2 diamond), bytes 8..9 its key_index.
Locked Door actor `0x23E` uses byte 5 for type (2 silver), bytes 8..9 for lock_index,
bytes 10..11 for accept_key, and byte 13 for exit_id. These two actors use different
type-number conventions; do not apply the key's type enum to a door.

Read-only inspection of the verified decompressed USA ROM (SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`) gives:

| Stage | Room file | Definition | Actor/type | Relevant fields |
| --- | --- | --- | --- | --- |
| 7 | `0x33D` | 5 | Key `0x193`, type 0 | key_index `0x110` |
| 7 | `0x33D` | 4 | Locked Door `0x23E`, type 2 | lock_index `0x10F`, accept_key `0x110`, exit 2 |
| 18 | `0x348` | 6 | Key `0x193`, type 0 | key_index `0x114` |
| 13 | `0x343` | 4 | Locked Door `0x23E`, type 2 | lock_index `0x113`, accept_key `0x114`, exit 2 |

This corroborates both observed pickups and the second door's separate lock flag
and accepted key. The first door's placement-derived lock ID `0x10F` would map to
`0x8015C629 & 80`, but no manual use capture for that lock is claimed here and it
has not been added as a user-confirmed tracker entry. Enumeration here inspects
room definitions; it is not a new complete key/door task-parameter/native-reader
trace or matching-C replacement.

Next: trace key/lock actor initialization and inventory consumption, then automate
instantiated key/door parameter extraction as with the map pickups. No assistant
game writes, freezes, reloads or independent quest replays were performed.
