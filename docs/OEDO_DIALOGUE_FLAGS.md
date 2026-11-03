# Oedo dialogue flag observations

User observations from US recomp, 2026-11-03. These are event correlations;
values are bit masks within the saved event bank, not whole-byte assignments.
The ROM scan below finds opcode patterns, not independently proven reachable
call sites or proof that each pattern belongs to a particular NPC.

| Observation | Map | Flag ID | Address / mask | Capture |
| --- | ---: | ---: | --- | --- |
| Old man alternates between two dialogues | 353 | `0x002` | `0x8015C608 / 0x04` | A→B sets; C returns to A as dialogue cycles |
| First Omitsu coffee-shop conversation; later dialogue changes | 432 | `0x007` | `0x8015C608 / 0x80` | A→B sets; user reports lasting dialogue change; reload persistence not independently checked |
| Coffee-shop man mentioning Omitsu alternates between two dialogues | 432 | `0x008` | `0x8015C609 / 0x01` | A→B sets; C returns to A as dialogue cycles |

Each row has one event trial and no idle/control trial. The two cycle captures
show reversions, not a permanent completion milestone. The data do not prove
that toggling a bit alone causes the dialogue change. Flag `0x007` was already
present in the external mn64rando-derived catalog as an Omitsu UFO conversation
flag; the user observed an Omitsu conversation in the coffee shop, but did not
establish the UFO detail in this capture. The other two IDs were not previously
named in the toolkit's story tracker; this does not establish global novelty.

A bounded opcode-pattern scan of the verified decompressed US ROM found:

| ID | File | Branch-if-set | Set | Clear |
| --- | ---: | --- | --- | --- |
| `0x002` | 96 | `0x757938` | `0x75796C` | `0x7579A0` |
| `0x007` | 96 | `0x758E80` | `0x758F88` | None found by this scan |
| `0x008` | 96 | `0x759114` | `0x759160` | `0x759194` |

The `0x002` and `0x008` pattern families are consistent with the user's
alternating observations. The scan does not follow native code or prove absence
of other writers. No ROM bytes, screenshots, trial identifiers, player pointers,
or saved game files are included in this record.
