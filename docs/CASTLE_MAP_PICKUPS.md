# Castle map pickup flags: Mr. Elly Fant and Mr. Arrow

User gameplay reports and A/B captures, 2026-11-03. These observations are not
independent assistant replays or forced-bit causal tests.

| Pickup | Address | Mask set | Saved flag ID | User evidence |
| --- | --- | --- | --- | --- |
| Oedo Castle Mr. Elly Fant (map) | `0x8015C627` | `80` | `0x0FF` (255) | Touch changes byte 00 to 80; pickup does not respawn |
| Ghost Toys Mr. Arrow (boss location) | `0x8015C628` | `20` | `0x105` (261) | One event A/B on map 57, character 0; same player/task pointers |
| Musical Castle Mr. Arrow (boss location) | `0x8015C629` | `01` | `0x108` (264) | One event A/B screenshot; bit becomes set |

The flag IDs follow the verified bank formula: address `0x8015C608 + (id >> 3)`,
mask `1 << (id & 7)`. These names describe pickup collection, not boss defeat or
whole-castle completion. Other bits in the same bytes can hold unrelated state.
Only the Oedo report explicitly establishes observed no-respawn behavior here;
Arrow reload/persistence behavior remains to be tested. No controls or reverted
captures were provided for the two Arrow observations.

## Existing research and native-code lead

Pinned mn64rando `9c580d03fe89354f79c3c83ba2e1bcf192f32577` already identifies
Mr. Elly Fant actor `0x086` and Mr. Arrow actor `0x087` in file `0x01A`, alongside
other pickups. The checked US parser dictionary does not annotate these three
saved flag IDs. This is separate from its existing Map of Japan flag ID `0x009`.

A read-only scan of the verified decompressed US ROM (SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`) found no aligned GEV/literal-native
references for these three IDs, including native scanning of pickup file `0x01A`.
Manual inspection explains a likely scanner limitation: pickup routines load a
16-bit flag ID from task offset `0xD0` before invoking the saved-bank helpers.
They do not need to contain the individual collectible's ID as an instruction.

Examples in `asm/usa/file_26.s`:

- `func_08000204_6AE9E4` tests the task-supplied ID via call `0x6AEA00`, with
  `lhu` from offset `0xD0` in the delay slot. Its update counterpart
  `func_080002D0_6AEAB0` sets the task-supplied ID at `0x6AEB28`.
- `func_08000514_6AECF4` tests the same parameter field at `0x6AED10`;
  `func_080005F8_6AEDD8` sets it at `0x6AEE24`.

These are pickup-module code paths, not yet a complete registration/placement
trace binding each screenshot instance to one specific function pair. The
private scan report remains ignored. There is no new matching-C replacement or
change to verified decomp counts from these observations alone.

## Toolkit and next steps

All three bits now appear independently in Story progress. Next, trace the
pickup registration and task-parameter setup to the room placement definitions;
that can reveal more collectible IDs without individually collecting every item.
Do not infer other castles' flag IDs solely from numerical spacing. Check Arrow
map visibility and no-respawn behavior after re-entry/reload separately. No game
writes, freeze activation or save reloads were performed by the assistant.
