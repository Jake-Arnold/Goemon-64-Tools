# Congo defeat, Miracle Moon and Lord of Oedo observations

Date: 2026-11-02. The two Lord-event gates below are supported by original-code
tracing and user-confirmed manual bit tests. Other interval changes remain
observations with unconfirmed semantics. Screenshots and raw
captures remain local. A changed bit is not automatically a story trigger.

## Defeat before collecting the Miracle Moon

The first supplied screenshot compares before Congo's defeat with afterward,
before collecting the Miracle Moon. All eleven listed bits became set:

| Address | Set masks | Saved flag IDs, in matching order |
| --- | --- | --- |
| `0x8015C62D` | `01`, `02`, `08`, `20`, `40`, `80` | `0x128`, `0x129`, `0x12B`, `0x12D`, `0x12E`, `0x12F` |
| `0x8015C62E` | `01`, `04`, `08`, `20` | `0x130`, `0x132`, `0x133`, `0x135` |
| `0x8015C63C` | `02` | `0x1A1` |

The user reports that the Lord can appear in his room after this progression.
The follow-up native trace below identifies ID `0x12D` as a required activation
gate in the Lord-event initializer; other spawning conditions can still apply.
These are changes across the whole interval; boss AI, actor lifecycle and room
state are competing explanations. A bit already set in A would not appear here.
The screenshots show one event trial per comparison and no controls or C capture.

The previously reported `0x8015C61C & 0x10` (ID `0x0A4`) sets when collecting
the Miracle Moon after the fight, according to the user's timing correction.
It is absent from this pre-Moon shortlist. ID `0x132` was observed set in this
defeat interval and clear in the earlier Moon-collection comparison; its precise
meaning remains unknown.

## Lord conversation and subsequent departure

The second supplied screenshot follows speaking to the Lord. The user reports
that he no longer appears in the room afterward. These three bits became set:

| Address | Mask | Saved flag ID | Existing evidence |
| --- | --- | --- | --- |
| `0x8015C608` | `01` | `0x000` | mn64rando labels it Received Super Pass |
| `0x8015C613` | `40` | `0x05E` | mn64rando labels it unknown (`???`) |
| `0x8015C61A` | `80` | `0x097` | No annotation found in the checked pinned dictionary |

The follow-up native trace below identifies ID `0x097` as a suppression gate in
the Lord-event initializer, matching the reported departure.
The Super Pass bit is a known receipt marker; it may also be checked for spawning,
but that reader has not been traced. The other bits could concern dialogue or the
associated room transition. The map change and pointer relocation are retained
as provenance by Event sessions rather than preventing A/B comparison.

## Existing research and new code leads

Checked source: abyssonym/mn64rando at
`9c580d03fe89354f79c3c83ba2e1bcf192f32577`, particularly
`tables/parser_config_en.yaml` and `entities_by_file.txt`. Actor annotations place
Congo (`0x323`) and his event trigger (`0x0CE`) in file `0x01D`, and Miracle Moon
(`0x35F`) in file `0x01E`. The dictionary also labels ID `0x07E` Rejected Lord of
Oedo, which is not among these screenshot changes.

A read-only scan of the verified decompressed US ROM, SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`, requested the fourteen IDs in the two
screenshots and bounded native indirect-call scanning of files `0x01D`/`0x01E`.
It returned 32 GEV pattern leads: 23 tests and one set of ID `0x000`, plus eight
sets of ID `0x05E`. Example decompressed ROM positions: `0x7488E4` and `0x748B08`
for `0x05E` sets, and `0x748B50` for the `0x000` set. The multiple `0x05E` set
locations are a reason not to name it a Lord-only flag.

Thirteen native indirect-call pattern leads were found across the selected files:

| ID | Operations and number of leads |
| --- | --- |
| `0x129` | set (1) |
| `0x12B` | set (1), test (1) |
| `0x12E` | test (4) |
| `0x12F` | clear (1), test (1) |
| `0x130` | test (1) |
| `0x132` | set (1), clear (1) |
| `0x1A1` | set (1) |

These are literal helper-call patterns, not traced actor ownership, full control
flow or verified runtime call sites. Their presence gives decompilation targets;
their absence for other IDs does not exclude direct bit accesses or other
encodings. This extends the earlier GEV-only negative result. The detailed scan
report stays in ignored local diagnostics, with no ROM or game-code excerpts
committed. No matching-C or full-ROM verification count changes follow from it.

## Follow-up: Lord-event activation and completion gates

The annotated Lord/event/Yuki actors are in file `0x036` (`asm/usa/file_54.s`
in the pinned mnsg baseline). Manual control-flow inspection identifies these
checks in initializer `func_08000000_710660`:

- ID `0x12D` (`0x8015C62D & 0x20`) is prepared at ROM `0x7106A8` and tested
  through the known saved-bank helper at call `0x7106DC`. If clear, the function
  calls `func_80034ED4_35AD4` and returns before constructing the event's objects.
- ID `0x097` (`0x8015C61A & 0x80`) is tested at call `0x710704`. If set, it takes
  the same early-exit path. Initialization continues past these two checks only
  when `0x12D` is set and `0x097` is clear. Allocation/other initialization can
  still fail; these are not claimed to be sufficient for every visible actor.
- ID `0x05E` is cleared during initialization at call `0x710754`. Update function
  `func_08000410_710A70` also tests it through a reused helper pointer at
  `0x710CA0`, clears it at `0x710CB4`, and changes local state to 7. This supports
  a script/event handshake role here, not a simple permanent Lord-despawn flag.
- The same update function sets ID `0x097` at `0x7110D0`, after the call at
  `0x7110B8` returns 1; it then resets a local timer and changes local state to 5.
  The callee's complete semantics are not established by this trace.

A bounded scanner pass over file `0x036` returned eight literal-call leads,
including that `0x097` set and `0x05E` clear. It missed both initialization gates:
`0x12D` is prepared earlier than the call delay slot, and `0x097` uses a reused
helper pointer. The manual trace therefore adds evidence beyond the pattern
scanner; zero pattern hits must never be treated as proof a flag is unused.

The 13 Congo/Moon native leads were also located inside their containing ELF
functions. Examples: `0x132` set in `func_080083BC_6BB65C`, clear in
`func_080094D4_6BC774`; `0x1A1` set in `func_0800A228_6BD4C8`. These function
boundaries are verified against the baseline ELF; flag meaning and actor ownership
still need control-flow tracing. No new matching-C replacements were produced.

The toolkit now names `0x12D` Lord of Oedo appearance enabled and `0x097` Lord of
Oedo respawn suppressed. The user has confirmed the exact initializer conditions
and performed manual bit tests: setting `0x8015C62D & 0x20` made the Lord appear;
changing `0x8015C61A` from `0x00` to `0x80` prevented respawning. This is stronger
than the earlier interval correlation and agrees with the original-code gates.
The tests were performed by the user, not independently replayed by the assistant.
They do not establish the meaning of other bits or that these gates are sufficient
for actor construction in every game state.

## Next investigation

Continue tracing the Lord-event object constructors and post-conversation script, and follow the
native leads in the Congo/Moon files to their containing functions. Separately
capture defeat, Moon pickup, Lord conversation and room transition. Any optional
manual bit test should change one mask while preserving other bits and observe
appearance, dialogue, reward and exits separately. No assistant game writes or live quest replays were performed for this analysis;
the manual memory-edit confirmation above was supplied by the user.
