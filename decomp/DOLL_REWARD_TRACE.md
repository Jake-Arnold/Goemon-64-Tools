# Fortune Doll reward and individual saved-flag trace

Date: 2026-11-03. Input: original-USA decompressed ROM SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`; mnsg pin
`7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.

## Silver reward, progress counter and fourth-quarter upgrade

The native one-quarter pickup update `func_080005F8_6AEDD8` sets the saved flag
from task `+0xD0` at ROM `0x6AEE24`. Its normal branch starts event `0x66` at
`0x6AEE60`; a branch on saved ID `0x0E2` instead starts event `0x312`. This is
separate from the gold/+4 path `func_0800083C_6AF01C`, event `0x6A`.

The shared numbered-event tables at ROM `0x785A0` (32-bit logical entries) and
`0x79208` (signed 16-bit file IDs) map `0x66` to file `0x05D`, local `0x1C3C`,
ROM `0x74116C`. Decoding the existing GEV write/add operations identifies:

| ROM position | Action |
| --- | --- |
| `0x7411CC` / `0x7411D4` | Select total word `0x8015C708`, add 1 |
| `0x7411DC` / `0x7411E4` | Select progress word `0x8015C704`, add 1 |
| `0x741214` onward | Test progress 4, 3 and 2 and branch to corresponding shared handlers |
| `0x7412BC` | Set condition ID `0x04E` on the first-quarter continuation |

Progress 4 branches to local `0x1E80`, event `0x69`, ROM `0x7413B0`. That script
clears condition `0x04E` at `0x741430`. The condition is separate from individual
pickup IDs and the counter. Event `0x312` maps to file `0x07A`, local `0x278`;
its continuation also adds 1 to total/progress at ROM `0x7ADB40..0x7ADB58`.
The alternate text/branch behavior is not fully reconstructed here.

After the dialogue/event completes, shared callback `func_080006E0_6AEEC0`
checks VM activity and calls `func_8000B824_C424` at `0x6AEEE8`. The latter was
**already fully reconstructed and verified** in `save_resources.c` before these
captures. Its old anonymous `word_FC` field can now be named
`fortune_doll_progress`, with `fortune_dolls_total` at offset `0x100`:

- If progress is below four, leave the health and progress fields unchanged.
- Otherwise subtract four once, increase maximum health by two native units,
  and set current health to the new maximum.
- It does not loop through multiple upgrades or clamp/cap the maximum itself.

Thus the full chain connects an individual persistent pickup record, the shared
+1 reward script, the separate quarter icon counter, and the existing upgrade
helper. No fresh fourth-doll live replay or heart-grant experiment is claimed.

## Corrected callback attribution

The earlier silver-doll note cited initializer `func_08000740_6AEF20` and update
`func_0800083C_6AF01C`. Following the scripts showed that path requests event
`0x6A` and adds four progress units at `0x7414CC..0x7414D4`. The silver/+1 path is
`func_08000514_6AECF4` / `func_080005F8_6AEDD8`. This corrects a mistaken callback
attribution, not the user's flags or the native progress-reader address. Actor
ordering in an annotation list alone must not be used to assign callbacks.

## Newly matching native C

`func_8003D310_3DF10`, the 120-byte numbered-event starter, now has reviewed C,
idle/active VM host tests, signed-file-ID tests, and exact original-function and
whole-ROM matches. This adds one verified C function. Existing resource helper
field renaming and identification of the health award are semantic progress,
not additional function-count claims. The key initializer candidate and Ghost
Toys pointer-spill draft remain excluded from full-ROM counts.

## Individual static doll flags

Run the read-only extractor with `--kind dolls` (default `maps` remains unchanged):

```bash
python -m decomp.pickup_placements --kind dolls --rom /path/to/USA.z64 \
  --report practice/diagnostics/new-dolls.json
```

[Published factual placement metadata](results/fortune_doll_placements.json)
contains 44 instantiated definitions: 39 silver placements and 5 gold placements,
using 43 distinct flags (38 silver, 5 gold). Silver ID `0x0EF` is shared by the
normal Zazen Waterway map 363 and unused variant map 384; do not count it twice.
The three user samples (356/`0x0ED`, 381/`0x0F1`, 301/`0x0DB`) all match exactly.

The other 40 distinct placement flags are now in Story progress, explicitly
marked ROM placement / not live-collected. The extractor validates ROM identity,
uses instantiated definitions rather than every definition, and rejects invalid
flag ranges. It does not see every scripted/dynamic reward or prove that every
configured room is reachable in normal gameplay.

## Special rewards and completeness boundary

The static silver IDs span `0x0CA..0x0F1` with gaps `0x0E0` and `0x0EE`.
The gaps are leads, not enough by themselves to assign collectible meanings.
Follow-up native tracing adds:

- Turtle Rock actor file `0x041`: `func_08000060_725C90` starts event `0x65` at
  `0x725DC8` and sets ID `0x0E0` at `0x725DFC`. Event `0x65` jumps into shared
  silver reward `0x66` at ROM `0x741160`. Its later callback calls the same health
  helper. This supports an additional code-derived quarter-heart reward record
  at `0x8015C624 & 01`, now named separately in the tracker and not live-tested.
- Kappa/Shishi-odoshi actor file `0x03E`: initializer `func_0800266C_723C8C`
  tests ID `0x0EE` at `0x723CA4` and avoids object creation if set. The writer
  connection is now resolved: `func_080027AC_723DCC` creates a task with callback
  `0x08000514` at `0x723DF0`, assigns pickup module `0x01A` at `0x723E1C..0x723E30`,
  then writes `0x00EE0000` to the child's word at `+0xD0` (`0x723EB0`). On the
  big-endian N64, the silver initializer's halfword read at `+0xD0` therefore
  receives `0x00EE`. The common silver collection path subsequently sets that
  saved flag and runs the quarter reward. It was missed by the earlier search
  because the constructor uses an upper-halfword load and whole-word store,
  not a literal flag-set call. This record is `0x8015C625 & 40`.

[The unified catalog](results/fortune_doll_catalog.json) now contains all 45
identified collection records: 40 silver and five gold. Forty-three flags come
from static room definitions, with Turtle Rock and Shishi-odoshi supplied by
traced native reward/spawn paths. The contiguous `0x0CA..0x0F6` range and the
native total/completion comparison against 45 are cross-checks, not the method
used to invent the two missing entries. The duplicated unused Zazen placement
is still one collectible flag, not two. These are parsed/code-traced mappings;
no claim of 45 independent live collections or every room's normal reachability
is made. Both special records are now named in Story progress.

No ROM bytes, dialogue, image assets or raw memory captures are bundled. No game
writes, freeze activation, inputs or save reloads were performed by the assistant.
