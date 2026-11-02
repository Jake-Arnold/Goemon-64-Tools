# Benkei's later Miracle Item dialogue and Kihachi activation

Date: 2026-11-02. Follows the user's whole-byte `0x8015C60E = 0x2E` experiment.
No game writes or new gameplay tests were performed by the assistant. Input ROM,
decompression identity and pinned research tools are documented in
[ROM_FLAG_TRACE.md](ROM_FLAG_TRACE.md).

## What was actually scanned

The primary data is the user's **original retail US ROM**, decompressed into a
separate verified research copy. It contains original MIPS machine code, event
bytecode and game data. Capstone was used locally to disassemble selected MIPS
instructions. The committed standard-library scanner reads those ROM bytes; it
does not scan a Python library or pretend that generated code is reconstructed
original C.

The mnsg decomp project supplied layout, identity references and decompression
tooling. Its checked-out reconstructed C sources are limited; a full matching
build was not run. The existing mn64rando project supplied independently authored
annotations, script formats, text mappings, actor descriptions and route logic.
These are research leads, checked against the original ROM where stated. Its
patches are **modifications**, not evidence that stock game logic behaves that way.

## Existing research inventory: search before more gameplay tests

Sources inspected for this question (coverage, not a claim that all web sources
have been exhausted):

| Source | Existing information and how it was used |
| --- | --- |
| [mn64rando US flag dictionary](https://github.com/abyssonym/mn64rando/blob/9c580d03fe89354f79c3c83ba2e1bcf192f32577/tables/parser_config_en.yaml) | Already names Benkei/Kihachi discovery, food quest/hints, Thaisamba completion and Miracle Snow flags. Used as an annotated starting point rather than asking the user to rediscover those labels. |
| [mn64rando route logic](https://github.com/abyssonym/mn64rando/blob/9c580d03fe89354f79c3c83ba2e1bcf192f32577/tables/router_logic.txt) | Models Benkei-after-Thaisamba as a prerequisite for the Kappa Pond event; corroborates the story dependency, not raw address identity. |
| [mn64rando entity definitions](https://github.com/abyssonym/mn64rando/blob/9c580d03fe89354f79c3c83ba2e1bcf192f32577/tables/entity_structures.yaml) | Actor/event descriptions including the Kappa event trigger. Names guide the binary investigation but do not alone prove its spawn guard. |
| [mn64rando event patches](https://github.com/abyssonym/mn64rando/blob/9c580d03fe89354f79c3c83ba2e1bcf192f32577/tables/script_missable_events_en.txt) | Specifically patches Kihachi quest activation when a cucumber is already held. This is a known original-versus-patched behavior distinction; the patch was not applied. |
| [mnsg decomp](https://github.com/klorfmorf/mnsg/tree/7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee) and [Android RE notes](https://github.com/ogdanimal/Goemon64Recomp-Android/tree/f2614817ce51aebf15069a8b0f032139cc5aff25/docs/re-notes) | Pinned ROM layout and VM/native-function leads. No already reconstructed Benkei/Kihachi C implementation was found in the inspected decomp source tree. |
| [Requested marshmallow walkthrough, FAQ 3273](https://gamefaqs.gamespot.com/n64/198022-mystical-ninja-starring-goemon/faqs/3273) | Its later Zazen section describes the post-submarine return to Benkei, collector referral, pond encounter and cucumber exchange. Direct opening was initially blocked; indexed content/find returned the relevant passage. It uses variant/misspelled names for the NPCs and supplies story context, not memory addresses. |
| [Ushiwaka walkthrough, FAQ 26153](https://gamefaqs.gamespot.com/n64/198022-mystical-ninja-starring-goemon/faqs/26153) and [Zeality game script, FAQ 45558](https://gamefaqs.gamespot.com/n64/198022-mystical-ninja-starring-goemon/faqs/45558) | Independently cover the later collector/food quest and the changed Benkei dialogue. Used to corroborate the decoded dialogue/route, not infer flag addresses. |

Targeted searches also covered combinations of Benkei/Kihachi, flag/memory map,
decompilation and event-script terms. The existing randomizer remains the most
specific annotated technical source found for these fields. Its existing 136
compatible primary-field labels are kept as an unverified local research index;
they are not all individually confirmed or redistributed as our own discoveries.

## Whole-byte `0x2E` is several independent states

The existing annotations and original script references distinguish:

| `0x8015C60E` mask | Flag ID | Meaning / evidence |
| --- | --- | --- |
| `0x02` | `0x031` | Mini-Ebisu magic granted/recorded; earlier reward-script trace |
| `0x04` | `0x032` | Thaisamba-completed progression; Benkei's later-dialogue branch checks this flag |
| `0x08` | `0x033` | Benkei defeated; earlier fight-script trace and user observation |
| `0x10` | `0x034` | Benkei first dialogue completed; earlier trace/tests |
| `0x20` | `0x035` | Miracle Snow already obtained; read by Kihachi's dialogue and written by its reward path |

`0x2E = 0x20 | 0x08 | 0x04 | 0x02`; it also leaves `0x10` clear. It is **not** a
single later-Benkei stage. In particular, it marks Miracle Snow obtained without
necessarily changing actual inventory. Kihachi's dialogue checks that flag first
at decompressed ROM `0x766B94` and selects its post-reward branch when set.

For a clean later-dialogue test, preserve the baseline byte and set only `0x04`.
If the baseline is exactly `0x18`, the result would be `0x1C`, not `0x2E`. Do not
assume the baseline is `0x18` if additional legitimate states are already set.
No such targeted write was performed in this investigation.

## The unknown activation flag is now located

**`0x8015C60C & 0x08` = heard about Kihachi from Benkei / Kihachi initialization gate.**
This is event flag ID `0x023`, distinct from the existing Benkei-encounter bit
`0x20` in the same byte. It explains the user's **`0x20 → 0x28`** result.

Original scenario file 121 begins its Benkei dispatch with these priorities:

1. At ROM `0x7AC680`, flag `0x023` branches to local script `0x08002E34`, the
   repeat collector dialogue observed by the user.
2. At ROM `0x7AC68C`, flag `0x032` branches to local script `0x08002998`, the
   Miracle Item question/referral path.
3. Other early-game checks follow. Clearing the introduction bit does not block
   the later path when the earlier-priority Thaisamba condition is met.

The referral path ends with `0x8020 0x023` at ROM **`0x7AD7C0`**, after Benkei
identifies the collector and the Center Pond. The following repeat path at ROM
`0x7AD7D4` contains his rivalry/collection dialogue, corroborating the game script.

### Native initialization guard, beyond script-pattern matching

Original **file 62** begins at decompressed ROM `0x721620`. Its initialization
routine constructs `0x800240DC` (the test helper), calls it indirectly through
`JALR` at **ROM `0x72163C`, file offset `0x1C`**, and supplies flag `0x023` in the
delay slot. The following branch at file offset `0x24` distinguishes flag set
from clear. With the flag clear it calls an early-exit routine and skips normal
initialization; with it set it continues through allocation and callback setup.
The same overlay contains Kihachi debug-identification strings. This independently
ties the referral flag to Kihachi's native initialization, not only his dialogue.

This establishes a required native initialization condition. It does not prove
that setting the bit immediately creates an actor in an already loaded room or
that there are no other room/trigger/allocation requirements. Re-enter the pond
normally when validating appearance; no raw map/character/actor-pointer edits.

## Related quest states already labelled and script-referenced

| Address / mask | Flag ID | Existing annotation and checked original references |
| --- | --- | --- |
| `0x8015C60C / 04` | `0x022` | Food quest active; set at ROM `0x7671F8`; numerous town-dialogue checks |
| `0x8015C60C / 10` | `0x024` | Food identity learned; set on the repeated Kihachi hint path at `0x76726C` and other hint paths |
| `0x8015C60E / 80` | `0x037` | Kihachi food-hint stage; set at `0x7671F0`, read at `0x766BAC` |
| `0x8015C60F / 01` | `0x038` | First repeated food hint already given; read at `0x767224`, set at `0x767238` |
| `0x8015C60E / 20` | `0x035` | Miracle Snow recorded; read at `0x766B94`, set at `0x7673C0` |

These combine prior annotations with inspected original script accesses. Exact
runtime timing, every alternative branch and isolated mask interventions have
not all been tested. The randomizer's cucumber-in-hand fix must not be mistaken
for the unmodified ROM's quest activation behavior.

## Reusable native-call index and validation

The scanner now optionally recognizes bounded `LUI/ADDIU/JALR` flag-helper call
patterns with a literal flag ID in the delay slot. It stops at target-register
clobbers and intervening control flow. This catches the Kihachi initializer,
which the earlier GEV-only scan could not cover:

```powershell
python -m practice.rom_flag_trace --rom practice/diagnostics/mnsg.decompressed.z64 --native-file-id 62 --flag-id 0x23 --output practice/diagnostics/kihachi-native-reference-v2.json
```

The actual focused run returned four script candidates and one native test call
for `0x023`; that native call was manually inspected as described above. A wider
local run over 68 configured native code ranges found 255 bounded call-pattern
candidates. It remains a limited matcher: spilled function pointers, nonliteral
arguments, other instruction constructions and full reachability are unresolved.
It does not turn all candidates into proven semantics.

Validation: 197 Windows Python tests passed, including two new synthetic native-
pattern tests for valid calls, file filtering, intervening clobbers/branches,
nonliteral delay-slot arguments and truncation. No ROM, raw disassembly, full
dialogue dump or save is committed. No matching C build, packaged release or live
game write test is claimed.

## Next gameplay check

There is no need to rediscover the spawn flag by sweeping byte values. If a clean
runtime confirmation is wanted, restore a pre-referral backup, preserve unrelated
bits, enable only the Thaisamba condition, complete Benkei's referral and observe
`0x8015C60C & 0x08` being set. Then enter/re-enter Kappa Pond normally. Do not use
the `0x2E`-modified state to assess the normal Miracle Snow reward path because
its already-obtained flag has been forced on.
