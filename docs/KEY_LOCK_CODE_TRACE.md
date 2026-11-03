# Shared key pickup, no-respawn gate and locked-door code

Date: 2026-11-03. Read-only trace of verified decompressed USA ROM, SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`, and pinned mnsg baseline
`7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.

## The pickup flag is also the no-respawn flag

Key initialization `func_080001BC_6F369C` reads a 16-bit saved flag ID from
`task + 0xD4` and calls the known saved-bank test at ROM `0x6F36B4`. If set,
it calls `func_80034ED4_35AD4` at `0x6F36CC` and exits. If clear, it installs
`func_0800021C_6F36FC` via the callback helper at `0x6F36E4`.

The subsequent pickup path `func_0800058C_6F3A6C` checks interaction bit `0x200`
in task word `+0x68`. Its silver branch (type 0 at task `+0xD1`) sets the saved
ID from `+0xD4` at `0x6F3AE8`, then requests event `0x6D` at `0x6F3AF8`.
Other key types have separate branches. The detailed event/display semantics
are not fully reconstructed here.

Thus the observed pickup bit is not merely an increased-number flag: the same
persistent record gates key respawning. A second no-respawn flag is not required
by this initializer. Event sessions captured that record; its 100-byte scope
does not cover every possible inventory/count field.

## Separate locked-door flag

Within the activation path of `func_08001020_6F4500`, the code tests the lock ID
from task `+0xD4` at `0x6F4544`. If already set, it follows the already-open path.
Otherwise it tests the required key ID from `+0xD6` at `0x6F4588`; if present,
it sets the lock ID at `0x6F45A8`, then advances the door callback/state. This
path does not clear the key's recorded pickup bit, matching the Oedo captures.

A subsequent call to `func_801FB240_5B7150` leads through
`func_801FB270_5B7180` to `func_801FB2A4_5B71B4`. Inspection finds task/system
field updates and a cleared field group, not an identified key-count arithmetic
operation. The door also clears `0x8015C8F8 + 4 * [0x800C7AA8]`. Its role has
not been established as the carried-key counter and must not be labeled that.

The actual displayed count's storage or calculation remains unresolved. The
capture scope could miss such a field if it lies outside the saved event bank,
or the count could be derived. Neither possibility is promoted to a confirmed
implementation merely from the displayed 2 -> 1 -> 0 sequence.

## Matching C candidate, separate from full-ROM completion

`decomp/candidates/key_spawn_gate.c` reconstructs the complete 96-byte initializer.
An isolated IDO build linked at logical overlay address `0x080001BC` matches every
original instruction byte; metadata is in `decomp/results/key_spawn_gate_candidate.json`.
It uses a partial task view with only the known `+0xD4` field, and symbolic engine
entry addresses to preserve the retail overlay's indirect call ABI.

This is **not yet a whole-ROM-verified replacement** and is deliberately absent
from the matching manifest and verified count. Original-overlay integration and
interface review remain required. Host tests check collected/uncollected paths,
the native field offset, non-one masked getter results, exact callback selection
and absence of task mutation for Oedo/Gourmet flag IDs. GCC sanitizer tests passed;
no live game writes or key tests were performed by the assistant.

## Gourmet Sub clarification

The user's currently open session has two distinct trials, both on map 129:

| User trial note | Actual saved-byte change | Interpretation |
| --- | --- | --- |
| bazooka before and after | `0x8015C63C: 00 -> 20` | Bazooka-room event association only; exact role unresolved |
| key before and after | `0x8015C637: 00 -> 08` | Silver key collection, ID `0x17B` |

Room file `0x39F`, definition 3 is Key actor `0x193`, type 0 (silver), with
key_index `0x17B`; this independently corroborates the second trial. It is
separate from Oedo's IDs `0x110` and `0x114`. Trial identifiers, player/task
pointers, complete session bytes and the local session filename remain private.
The tracker adds only the corroborated key label; it does not invent a precise
bazooka-event meaning. No assistant game writes or session edits were made.
