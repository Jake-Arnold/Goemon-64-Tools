# Silver Fortune Dolls: world pickups versus quarter progress

Date: 2026-11-03. User pickup captures, original-room parameters, native item
renderer and one independent read-only live memory sample.

| Pickup | Saved event address/mask | Flag ID | Room corroboration | User item-screen observation |
| --- | --- | --- | --- | --- |
| Map 356 | `0x8015C625 & 20` | `0x0ED` | File `0x40E`, definition 10, Silver Doll actor `0x088` | 1/4 |
| Map 381 | `0x8015C626 & 02` | `0x0F1` | File `0x42B`, definition 5, actor `0x088` | 1/2 |
| Mt. Fuji main map (301) | `0x8015C623 & 08` | `0x0DB` | File `0x3D8`, definition 11, actor `0x088` | 3/4 |

All masks are hexadecimal. These are separate individual collection records,
not a binary representation of the current quarter count. Room definition bytes
4..5 supply the per-pickup ID. The native doll update uses a task-supplied ID,
so a literal-ID opcode search need not find each individual doll.

## Why the event comparison did not show half a doll

Event sessions deliberately reads only the 100 saved event bytes
`0x8015C608..0x8015C66B`. The item-screen quarter progress is a **32-bit word at
`0x8015C704`**, outside that range. Pinned mn64rando annotations separately name
`0x8015C704` Fortune Doll Progress and `0x8015C708` Total Fortune Dolls Obtained.

Native item renderer `func_802135B8_672568` loads saved data offset `0xFC`
(`0x8015C704`) at ROM `0x6725D8` and calls `func_80212660_671610` with the value
at `0x6725D4`. The callee selects image regions for values 1, 2, 3 and 4 and
renders nothing for other values. No image/asset data is copied here.

A read-only handle to the running recomp independently observed state 13,
map 381, progress word 2 and annotated total word 2, corroborating the user's
half-doll display. The third 3/4 observation is user-reported and room-corroborated;
no separate live read of 3 is claimed. The follow-up reward trace below now identifies the +1 script and connects the
post-dialogue callback to the already reconstructed four-quarter health helper.

Use Live memory's full-word **Fortune Doll progress (quarters)** watch, or State
discovery focused captures, to see this counter. Saved / shadow also includes
it. The old `0x8015C707` boolean item control was only the low byte of this word;
it now exposes 0/4, 1/4, 1/2, 3/4 and 4/4 display states. This does not itself
replay collection or grant a heart. Raw-edit/freeze permissions remain unchanged.

## The extra first-pickup flag

The map-356 capture additionally sets `0x8015C611 & 40`, ID `0x04E`. The pinned
mn64rando US dictionary already annotates it as Strength Gauge is Increasing.
In the saved map-381 trial that byte remains `40 -> 40`; it is not a quarter
counter and need not change when the icon advances. The exact instruction/
first-message/animation role of this condition remains untraced; no automatic
permanence or one-time-message meaning is assigned to it.

## Shared actor code

Correction to the initial callback attribution: the one-quarter/silver path uses
initializer `func_08000514_6AECF4` and update `func_080005F8_6AEDD8`, not the
`0x6AEF20`/`0x6AF01C` pair initially cited. The latter starts event `0x6A`, which
adds four quarters and belongs to the full-heart/gold path. The observed pickup
flags and item-screen progress-word address were unaffected by this correction.

The silver update sets its task-supplied flag and normally requests event `0x66`;
a conditional alternative uses `0x312`. Both paths have one-quarter increment
code. Shared callback `func_080006E0_6AEEC0` waits for the event VM to finish,
then calls the already matched `func_8000B824_C424`, restores engine state and
finishes. That health helper subtracts four quarters when progress is at least
four, increases max health by two native units, and fills current health.
It processes one upgrade per invocation, retaining any extra quarters.

[Full reward/individual-flag follow-up](https://github.com/Jake-Arnold/Goemon-64-Tools/blob/dae81a70fc6e4adf22f76846d202253d3f201b2d/decomp/DOLL_REWARD_TRACE.md) records
script positions, the callback correction, static placement coverage and the
special reward leads. Existing health-upgrade code is not counted as a new C
function; the newly reconstructed event-start routine passes the full-ROM gate.

The original verified decompressed US ROM SHA-1 is
`6ea0ed71032ce08fc2745f412d84936382197494`. External annotations come from
mn64rando pin `9c580d03fe89354f79c3c83ba2e1bcf192f32577`. No assistant pickup,
flag edit, freeze activation, game input, save reload or memory write was used;
private captures/pointers and assets remain uncommitted.
