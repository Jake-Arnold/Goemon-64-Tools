# Original-ROM flag tracing: Benkei and Ushiwaka

Date: 2026-11-02. Analysis is read-only. No runtime controls changed and no game
memory writes were performed. This is a binary/script analysis result, not a
matching decompilation build or proof of every flag's gameplay effects.

Follow-up: [later Benkei/Kihachi trace](BENKEI_KIHACHI_TRACE.md) adds a broader
existing-source review and the native initialization gate. The scanner now has
optional bounded native indirect-call matching in addition to the GEV index.

## Reproducible input and sources

- Supplied retail US ROM SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66`.
- Decompressed research copy SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`.
  Both match the upstream US reference hashes. Original ROM was only read;
  decompressed output, tools and reports remain in ignored local diagnostics.
- [mnsg decompilation](https://github.com/klorfmorf/mnsg/tree/7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee)
  pinned at `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`: used its US file layout,
  hash references and `tools/rommy.py` decompressor. The decompressed output hash
  was checked before analysis. No complete compiler/build baseline was attempted.
- [mn64rando US parser configuration](https://github.com/abyssonym/mn64rando/blob/9c580d03fe89354f79c3c83ba2e1bcf192f32577/tables/parser_config_en.yaml)
  pinned at `9c580d03fe89354f79c3c83ba2e1bcf192f32577`: independent flag labels,
  script-opcode descriptions and text character mappings. Labels were checked
  against the original ROM where stated below, not automatically accepted as
  individually verified. The external label dictionary is not copied into Git.
- [Goemon64Recomp-Android research notes](https://github.com/ogdanimal/Goemon64Recomp-Android/tree/f2614817ce51aebf15069a8b0f032139cc5aff25/docs/re-notes)
  provided leads to the event VM. Its conclusions were not substituted for the
  direct instruction/script checks in this report.

Research environment: Python 3.13, capstone 5.0.9, PyYAML 6.0.3, lzkn64 0.2.0.
The decompressor dependency's PyO3 binding does not support the installed Python
3.14 build; an isolated existing Python 3.13 environment was used. Windows console
encoding also required Python's `-X utf8`. Neither issue changed project runtime
requirements. No external source patches or third-party submissions were made.

## The game's own event-flag API

Original main-code helpers, verified by disassembling the supplied ROM:

| Guest code address | Operation for the positive flag IDs used here |
| --- | --- |
| `0x80024038` | Set: OR the selected byte with the selected mask |
| `0x80024088` | Clear: AND the selected byte with the inverted mask |
| `0x800240DC` | Test: AND the selected byte with the mask; return zero/nonzero mask |

For IDs in the primary 100-byte event field:

```text
byte_address = 0x8015C608 + (flag_id >> 3)
mask = 1 << (flag_id & 7)
```

The set helper uses an `or` instruction at `0x8002407C`; clear uses `and` at
`0x800240D0`, and test uses `and` at `0x8002411C`. Thus the traced flag-set path
uses bitwise OR, not arithmetic addition. Other game variables can still use
different update operations.

The event VM at `0x8003D68C` dispatches through the table at `0x8007CFB0`:

| Script opcode | VM handler | Effect |
| --- | --- | --- |
| `0x8020` | `0x8003D90C` | Read flag ID and call set helper |
| `0x8021` | `0x8003D928` | Read flag ID and call clear helper |
| `0x8022` | `0x8003D944` | Read flag ID and branch to script target when set |

Offsets below refer to the **decompressed ROM**, not compressed retail offsets.
`file_97` and `file_121` are scenario assets containing multiple scripts, not
necessarily one actor each. A segmented script address such as `0x0800CBEC` is
file-local addressing, not a ready-to-use host pointer or guest-code breakpoint.

## Checks and writes tied to the observed progression

| Flag ID | Guest byte / mask | Traced role | Example decompressed ROM references |
| --- | --- | --- | --- |
| `0x025` | `0x8015C60C / 20` | Benkei encounter enables Ushiwaka discussion | Set in file 121 `0x7AC714`; check in file 97 `0x765E68` |
| `0x02D` | `0x8015C60D / 20` | Ushiwaka introduction seen | Check `0x765EDC`; set `0x765F58` |
| `0x02C` | `0x8015C60D / 10` | Blue-fish request stage | Check `0x765E5C`; set `0x7660F8` |
| `0x02B` | `0x8015C60D / 08` | Yellow-fish request stage | Check `0x765E50`; set `0x7661CC` |
| `0x02A` | `0x8015C60D / 04` | Red-fish request stage | Check `0x765E44`; set `0x766264` |
| `0x029` | `0x8015C60D / 02` | Achilles' Heel reward recorded | Check `0x765E38`; set `0x766454`; Benkei also checks it at `0x7AC6D4` |
| `0x028` | `0x8015C60D / 01` | Ushiwaka temple-stage transition | Check `0x765E18`; set `0x76661C` |
| `0x02E` | `0x8015C60D / 40` | Passed Mini-Ebisu training | Check `0x766630` selects success/reward branch |
| `0x02F` | `0x8015C60D / 80` | Failed Mini-Ebisu training | Check `0x766668` selects failed/retry dialogue |
| `0x030` | `0x8015C60E / 01` | Declined Mini-Ebisu training | Check `0x76665C`; set on decline path `0x766A94` |
| `0x031` | `0x8015C60E / 02` | Mini-Ebisu magic granted/recorded | Check `0x76684C`; set after ownership write at `0x7669C8` |
| `0x033` | `0x8015C60E / 08` | Benkei defeated | Check `0x7AC6A4`; set `0x7AD254` |
| `0x034` | `0x8015C60E / 10` | Benkei introductory meeting completed | Check `0x7AC6E0`; set `0x7AC7C0` or `0x7AC7F4` on introductory branches |

The meanings above combine direct script branches/writes, nearby decoded dialogue,
external annotations and the earlier gameplay evidence. Exact native writers for
the training-success/failure bits have **not** been recovered: their script
readers are verified, but no direct `0x8020` writer was found by this scanner.
Do not call that an exhaustive native-writer search.

### Concrete new deductions

1. **The formerly unknown `0x80` is a failure state, not forward progression.**
   At `0x766668`, flag `0x02F` branches to file-97 offset `0xCBEC`
   (ROM `0x7669DC`). That branch contains failure dialogue and a retry choice.
   The retry path sets flag `0x07D` at `0x766A68`; the initial training path also
   sets `0x07D` at `0x76680C`. It maps to `0x8015C617 & 0x20`, a code-backed
   training request/start signal candidate, not a standalone proven launch API.
2. **Success and failure are separate bits.** The same dispatcher checks success
   `0x02E` before failure `0x02F`. If both are set, this dispatcher takes the
   success path first. Whole-byte `FF` experiments would obscure that ordering.
3. **Training passed is separate from ability granted.** Success selects file-97
   offset `0xCA5C`; that branch first checks flag `0x031`. If not already granted,
   it runs the reward dialogue, assigns word `0x8015C6F0 = 1` at ROM `0x7669B8`,
   then sets `0x031` at `0x7669C8`. The assignment handler for `0x8004 / 0x8009`
   resolves the destination and stores a word (`0x8003DB64..0x8003DB70`). The low
   canonical big-endian byte is `0x8015C6F3`, matching the toolkit's Mini Ebisumaru
   ownership watch. Forcing the granted flag without ownership can therefore
   bypass this reward branch; flag edits must not be assumed to grant abilities.
4. **Achilles' Heel has both inventory and event state.** The reward path writes
   word `0x8015C70C = 1` at ROM `0x766444` before setting flag `0x029`. Its low byte
   is `0x8015C70F`, matching the toolkit's item address. The adjacent decoded item
   announcement identifies Achilles' Heel. This explains why inventory-only edits
   need not advance Benkei's script: Benkei checks the separate event flag.
5. **Fish counts can be derived from script conditions.** File 97 compares the
   blue count word `0x8015C720` against 3 at `0x766140`, yellow `0x8015C71C`
   against 5 at `0x7661E0`, and red `0x8015C718` against 8 at `0x766280`.
   Subsequent hand-in branches clear those counts and set the next stage flag.
   These are script conditions, not claims that writing only a count executes
   every associated event.

The actor placement/reload behavior reported by the user is retained as gameplay
evidence. No exhaustive actor-spawn or minigame-result native-code trace was done.

## Reusable scan and its limits

The new standard-library command reads the verified decompressed ROM and creates
a **local** reference index. It does not alter the ROM, connect to a process or
need Capstone/PyYAML at runtime:

```powershell
python -m practice.rom_flag_trace --rom practice/diagnostics/mnsg.decompressed.z64 --output practice/diagnostics/rom-flag-references-v2.json
```

Optional repeated `--flag-id 0x02F` arguments restrict the index. Repeated
`--native-file-id 62` arguments additionally scan selected files for bounded
literal flag-helper `JALR` patterns; those are reported separately and still
require manual review. The output must
be a new file; existing output or the input ROM cannot be overwritten.

Actual scan: **892 aligned opcode-pattern candidates across 136 primary-field
flag IDs**, over 1,084 nonempty file ranges (empty ranges in the file table are
excluded). These are not 892 confirmed executed
instructions or 136 individually verified meanings. Pattern matches can be data
false positives, and the scan does not recover a complete script CFG or indirect
native writes. Bounded indirect-call patterns are not a general native dataflow
analysis. The manually traced branches above have stronger evidence than
the unreviewed index.

A separate ignored local index joins 136 external primary-field annotations to
their references, marking them `external_annotation_not_individually_verified`.
Those labels offer a research backlog, not automatic confirmation. The existing
GUI and custom watches are unchanged; the shared evidence-registry UI remains a
later milestone. No full matching decompilation or release artifact is claimed.

## Next focused gameplay check

Preserve a pre-training backup. From the temple/minigame-available state, read
`0x8015C60D`, deliberately fail the normal Mini-Ebisu training once, then read it
again after returning to ordinary dialogue. Observe without forcing another flag.
The code-backed expectation is that failure selects bit `0x80`; the exact result
writer/timing still needs validation. Also note `0x8015C60E` and Mini Ebisumaru
ownership byte `0x8015C6F3` so failure is not confused with a reward already held.
Use Live memory/custom watches for this cross-scene check: Event sessions v1
requires stable pointers within a trial and may reject the scene transition.

## Congo observations (2026-11-02, tentative)

One user-supplied event-session screenshot shows saved flag ID `0x0A4` (164),
`0x8015C61C & 0x10`, becoming set and ID `0x132` (306),
`0x8015C62E & 0x04`, becoming clear. The user associates the first with defeating
Congo (first boss), and suspects the second controls cutscene/actor/room state.
Only these masked bits were isolated, not either entire byte. The session retained
the default Benkei experiment label, so that label is not evidence of the event.
There was one event trial, no idle/control overlap trials and no reverted C capture.

The toolkit displays both as candidates, not proven semantics. Its read-only story
sample now covers all 100 event bytes, including these offsets beyond the original
16-byte catalog prefix. A verified decompressed US ROM scan for both IDs found
zero aligned GEV opcode-pattern references; no native-file indirect scan was
requested. That limited negative result cannot exclude native direct bit accesses,
other script encodings or computed IDs. The private scan report remains ignored.

Next: name a fresh session for Congo; check the bits before/after the fight and
after room re-entry/save reload. On a disposable pre-fight state, test each bit
independently while preserving other bits, observing boss spawn, cutscene,
room exits and reward separately. No automated game edits were performed.

### Congo timing correction

The user subsequently reports that `0x8015C61C & 0x10` sets on **collecting the
Miracle Moon after defeating Congo**, rather than at boss defeat itself. Story
progress now labels it Congo Miracle Moon collected, with user-reported evidence
and no claim of independent reproduction. `0x8015C62E & 0x04` remains a tentative
encounter-state hypothesis. Post-fight NPC dialogue can move the player to another
map and change flags; Event sessions now supports these A/B context transitions.

### Congo defeat and Lord follow-up

[Separate before-Moon and after-Lord captures, native function leads and Lord-event
activation/completion gates](CONGO_LORD_OBSERVATIONS.md) identify required ID
`0x12D` set and ID `0x097` clear in `func_08000000_710660`. This extends the
initial pattern scan with manual control-flow evidence. The user subsequently confirmed both gate conditions with manual bit tests:
mask `0x20` enables appearance and mask `0x80` prevents respawning. These tests
were user-performed; no independent assistant replay is claimed.
