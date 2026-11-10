# Plasma advice conditions

This traces the USA game's common Plasma dialogue event, not every possible
Plasma-related native behavior. In all four normal Plasma rooms (stages 423–426,
Oedo/Zazen/Folkypoke/Festival), the instantiated Plasma actor `0x306` references
event `0x288`. The event tables map it to scenario file `0x70`, entry
`0x08002F98`. Its advice-selection path reaches file-local `0x3208`.

The bounded path contains **40 branch-if-set checks on 37 distinct saved bits**
and **11 set operations** touching 11 distinct bits. Two set-only bits bring
the combined checked-or-set total to **39**. The generated, text-free
[condition metadata](../decomp/results/plasma_conditions.json) records each
check, address/mask, order and target. The separate
[writer leads](../decomp/results/plasma_writers.json) contain 69 aligned script
set/clear pattern candidates across those 39 bits; they do not include a native
code scan or prove that every pattern is reachable. The only independently
force-tested Plasma conditions here are the user's first two bits below.

These are **priority-ordered** checks, not independent unlock switches. A bit
further down the list may have no visible effect while an earlier condition
still selects an earlier message. Script set operations can also change other
story flags; asking Plasma is not necessarily read-only. Editing the bits in
Story progress preserves other bits in the same byte, but does not run other
story events, rewards or cutscenes.

## User-confirmed first three advice stages

| Chain Pipe bit | Super Pass bit | Result reported by user |
| --- | --- | --- |
| `0x8015C60A & 0x01` clear | clear | First dialogue |
| set | `0x8015C608 & 0x01` clear | Second dialogue |
| set | set | Third dialogue in the tested state |
| clear | set | First dialogue still has priority |

The script checks `0x010` (Chain Pipe bit) first and only reaches `0x000`
(Super Pass bit) if the first is set. The acquisition names are existing
[mn64rando annotations](https://github.com/abyssonym/mn64rando/blob/9c580d03fe89354f79c3c83ba2e1bcf192f32577/tables/parser_config_en.yaml);
the user tested the bits' dialogue effects, not their acquisition semantics.
Other later flags can affect the third and subsequent outcomes.

## Ordered advice path

The table describes the first applicable path after earlier checks have been
satisfied. Unless a row says otherwise, **clear** selects that advice and **set**
continues to a later check. Names for story conditions are existing annotations;
individual game effects outside the verified first two bits remain to be tested.

| Check (flag ID; address / mask) | Advice or routing when reached |
| --- | --- |
| `0x010`; `0x8015C60A / 01` | Oedo Castle route via Kai Highway / Mt. Fuji. |
| `0x000`; `0x8015C608 / 01` | Use Chain Pipe at the damaged bridge to reach Oedo Castle. |
| `0x03A`; `0x8015C60F / 04` | Travel west toward Iga and the Wise Man. |
| `0x029`; `0x8015C60D / 02` | Speak with the fisherman at Duck Creek about Benkei; this path sets `0x025`. |
| `0x033`; `0x8015C60E / 08` | Use Achilles' Heel against Benkei. |
| `0x063`; `0x8015C614 / 08` | Travel through Yamato and Kii–Awaji to Shikoku. |
| `0x014`; `0x8015C60A / 10` | Disable the dragon's control machine. |
| `0x00A`; `0x8015C609 / 04` | Seek Dogo Hot Springs information and visit Mt. Kompira. |
| `0x028`; `0x8015C60D / 01` | Find the fisherman in Zazen; this path also sets `0x00A`. |
| `0x031`; `0x8015C60E / 02` | Seek shrinking training at Golden Temple. |
| `0x018`; `0x8015C60B / 01` | Use the small opening to enter Dogo Hot Springs. |
| `0x00D`; `0x8015C609 / 20` | If clear, `0x03E` or `0x03F` set routes to the Inaba battery hint. If both are clear, `0x080` chooses first Sasuke-revival advice (then sets `0x080`) versus the Izumo coffee-shop follow-up. |
| `0x00E`; `0x8015C609 / 40` | Investigate the tree at Izumo Shrine with the camera. |
| `0x040`; `0x8015C610 / 01` | Use a Fire Cracker Bomb on the Akiyoshidai cracked door. |
| `0x017`; `0x8015C60A / 80` | Head west to Kyushu. |
| `0x01C`; `0x8015C60B / 10` | If clear, `0x03C` chooses first Mt. Fear / Oedo training advice (then sets `0x03C`) versus the shorter training follow-up. |
| `0x042`; `0x8015C610 / 04` | Use Sudden Impact on the metal box and travel north. |
| `0x011`; `0x8015C60A / 02` | Get stronger weapons from a technician; this path sets `0x041` and `0x011`. |
| `0x012`; `0x8015C60A / 04` | Visit Mokubei for a weapon upgrade. |
| `0x015`; `0x8015C60A / 20` | Break the rock at Mt. Fear's rear entrance. |
| `0x01F`; `0x8015C60B / 80` | While clear, nested checks `0x043` then `0x044` select Festival Village advice, ocean advice, then the Kegon sign. The first two paths respectively set `0x043` and `0x044`. |
| `0x032`; `0x8015C60E / 04` | Find the underwater switch in the Japan Sea. |
| `0x023`; `0x8015C60C / 08` | If clear, `0x045` chooses a first collector hint (then sets `0x045`) versus naming Benkei. |
| `0x022`; `0x8015C60C / 04` | Find Kihachi near the bamboo forest pond. |
| `0x024`; `0x8015C60C / 10` | Learn the cucumber clue; this path sets `0x024`. |
| `0x027`; `0x8015C60C / 80` | Ask the Golden Temple priest about jump training. |
| `0x020`; `0x8015C60C / 01` | Find the Bizen training gym. |
| `0x00F`; `0x8015C609 / 80` | Use jumping ability to reach the cucumber maker. |
| `0x035`; `0x8015C60E / 20` | Take the cucumber to Kihachi. |
| `0x046`; `0x8015C610 / 40` | If clear, Ugo Stone Circle / outer-space advice and set `0x046`; if set, final Fortune Doll advice. |

The [Kegon NPC capture](KEGON_HINT_FLAG.md) established that an NPC conversation
also sets `0x044`. This trace adds that Plasma's own ocean-advice path can set
the same bit. When reached with `0x043` already set and Mermaid magic bit
`0x01F` still clear, that bit directs the subsequent path to the Kegon hint.
It does not prove the bit opens the waterfall or is required for access.

## Reproduce

Run with the user's own verified US ROM; both retail and decompressed versions
produce identical text-free condition metadata:

```bash
python -m decomp.plasma_conditions --rom /path/to/USA.z64 --report practice/diagnostics/plasma.json
python -m decomp.plasma_writers --rom /path/to/decompressed.z64 --report practice/diagnostics/plasma-writers.json
```

Reports require new paths and contain flags/addresses/offsets, not dialogue text,
raw script bytes, ROMs, saves or personal trial details. The script branch scan
is scoped to the identified event path; native uses and undiscovered alternate
scripts are not ruled out.
