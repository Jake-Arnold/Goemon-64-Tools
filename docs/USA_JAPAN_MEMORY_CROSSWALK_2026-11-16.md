# USA ↔ Japan memory-data crosswalk: mandatory agent procedure

**Canonical toolkit evidence note · 17 November 2026.**
Applies to original USA *Mystical Ninja Starring Goemon* (NG5E-0) and
Japanese *Ganbare Goemon: Neo Momoyama Bakufu no Odori* (retail rev 0).
This file governs future research **even when the toolkit crosswalk UI is
not yet merged**.

## Result: a strong, scoped relocation pattern

Multiple independently observed **fixed RDRAM data fields** differ by the
same displacement:

```text
JP_candidate = USA_guest_vaddr + 0x57F0
USA_candidate = JP_guest_vaddr - 0x57F0
```

The repetition is systematic: engine state, current/pending scene,
character data, unlocks, weapon state and at least one persistent story
bit all support this difference. **A relocation pattern is not proof of
every field or every memory segment.** Use the formula to propose where
to test, not to generate runtime write permissions.

| Field | USA guest address | JP guest address | Evidence |
| --- | --- | --- | --- |
| Engine state | `0x800C7A94` | `0x800CD284` | Previously traced regional game state |
| Current scene | `0x800C7AB2` | `0x800CD2A2` | Previously traced regional scene |
| Pending scene | `0x800C7CA0` | `0x800CD490` | Previously traced regional transition |
| Character index | `0x8015C5DC` | `0x80161DCC` | Japanese runtime and character-switch MIPS traces |
| Equipped weapon index | `0x8015C607` | `0x80161DF7` | User-confirmed cycling values 01/02/03 |
| Gameplay submode | `0x800C7AA4` | `0x800CD294` | User-confirmed |
| Map overlay byte | `0x8015C574` | `0x80161D64` | User-confirmed; observation, NOT a safe toggle |
| Benkei encounter event | `0x8015C60C & 0x20` | `0x80161DFC & 0x20` | User-confirmed |
| Sasuke party | `0x8015C6A7` | `0x80161E97` | Previously tested JP unlock |

The JP unlock list has 33 user-tested entries; the first Sasuke
battery remains the outstanding unverified hypothesis. Source provenance
and byte-format handling are in `practice/region_unlocks.py`.

## Mandatory reciprocal workflow — both directions

On discovering **any** new memory address in either ROM, an agent MUST:

1. **Identify provenance.** Record ROM revision, guest address, width,
   alignment, N64 big-endian interpretation, field type, bit mask, scene/
   character/context and original MIPS or live gameplay evidence. Do
   not confuse host memory bases, ROM offsets, loaded overlays and CPU
   guest addresses.
2. **Classify storage and lifetime.** `fixed-global` and
   `saved-event/inventory` are potentially eligible. Dynamic entity
   memory, player pointers, script cursors/VM globals, allocators, Impact
   boss allocations, overlays, code VMAs and unknown ownership are
   **not** eligible for blind offset translation.
3. **Look up known explicit pairs first.** Check `practice/region_unlocks.py`,
   `practice/japanese_fields.py`, `practice/japanese_scene_probes.py`,
   `practice/story_progress.py`, and the current reviewed mapping
   docs. On a decomp-only checkout use regional manifest/MIPS research.
   Preserve explicit exceptions and existing evidence classifications.
4. **Calculate reciprocal candidate only when eligible.** USA discovery
   uses `+0x57F0`; Japan discovery uses `-0x57F0`. Preserve the exact
   original byte/halfword/word **accessor** and bit mask, rather than
   assuming both regions use the same field width or packing.
5. **Record both addresses and status.** Source may be verified;
   the new counterpart begins as `offset-candidate`. Include a
   specific A/B/control or original-instruction read/write experiment.
   Capture positive, negative, and conflicting findings.
6. **Confirm independently** in the other ROM before promoting a field.
   A plausible value or a single changed byte cannot establish
   meaning. Do not turn hypotheses into unlock actions, memory freezes,
   warps or automated writes.
7. **Publish the mapping evidence with the discovery** and update
   `PROGRESS.md` on the correct feature branch. For decomp work,
   preserve full original-ROM codegen and relocation validation
   independently; a RAM address match never establishes matching C.

## Mandatory negative cases and known exceptions

| USA | Japanese finding | Meaning |
| --- | --- | --- |
| `0x8015C866` | `0x80162057` | Miracle Snowflake verified location is **+0x57F1**, so prefer explicit mapping over naïve delta |
| `0x800C7AE6` | `0x800CD2D6` | Pause-field candidate **disputed** by user observation |
| `0x8015C609 & 0x20` | `0x80161DF9 & 0x20` | First Sasuke battery JP bit **unverified** |
| `0x8015C5E0` USA u32 max HP | `0x80161DD3` JP low-byte cheat | Compare low-byte accessor/width, not the whole 32-bit field as independently verified |
| `0x801FC60C` USA player pointer storage | No automatic JP mapping | Dynamic object/lifetime sensitive |
| `0x801C77E0` USA VM state | No automatic JP mapping | VM/overlay context |
| `0x802F7060` USA Impact sample field | No automatic JP mapping | Runtime allocation, not fixed static data |
| JP `0x80151B10` player XYZ | No automatic USA mapping | Scene/player-position layout requires its own mapping |

The *published toolkit crosswalk prototype* is in
[PR #43](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/43)
and includes a 119-entry **candidate catalogue**, read-only Japanese
comparison UI, and a bidirectional CLI.
**These remain feature-branch capabilities until that PR is separately
validated and merged.** Do not claim the CLI is present on canonical
`main` merely because this procedure is present.

## Research record template

```yaml
source:
  region_and_revision: "USA NG5E-0 | JP retail rev 0"
  guest_address: "0x8015C60C"
  owner: "fixed-global | saved-event | dynamic | overlay | unknown"
  field: "Benkei encounter"
  width_bytes: 1
  endian: "big"
  mask: "0x20"
  scene_and_character: "specified or unknown"
  evidence: "original MIPS site / gameplay A-B / source citation"
counterpart:
  region: "JP retail rev 0"
  guest_address: "0x80161DFC"
  derivation: "explicit pair | +0x57F0 | -0x57F0 | exception | n/a"
  status: "user-confirmed | offset-candidate | disputed | conflicting"
  independent_evidence: "observation/citation or none"
  contrary_evidence: "observation or none"
  next_validation: "concrete other-ROM test"
  game_write_authorized: false
```

The record above illustrates a **known pair**; do not copy its evidence
or confidence status to another discovery. Guest-memory translation is
**bidirectional candidate generation**, never universal address identity.
