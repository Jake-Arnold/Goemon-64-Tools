# Signed stream reader: matching handoff

Date: 2026-11-02. Function `func_8003DE80_3EA80`, decompressed ROM
`0x3EA80..0x3EB68`, guest `0x8003DE80`, size 232 bytes. It is **still assembly**
and excluded from matching C totals. Pinned upstream/ROM identities remain those
in `manifest.json`; source drafts, objects and experiment logs stay local.

## Recovered behavior to preserve

- Read signed 16-bit words. Nonnegative words go to `func_8000D060_DC60` with
  the owner argument. Reread the current word after that call, record it in work
  marker offset 8, then advance by one halfword. The external call can change
  the current word; preloading it changes the characterized behavior.
- Before emitting a nonnegative word, `func_8003DF68_3EB68` can suppress output.
  That path clears the marker to -1, copies `D_801C7798_1C8398` into the repeat
  count, and returns the unchanged cursor.
- Otherwise continue ordinary words while that setting is zero. Once nonzero,
  copy it into the repeat count and return the advanced cursor.
- Negative -1 clears the marker and returns null without updating the repeat
  count. Other negative words clear the marker, delegate to the retained
  `func_8003DF98_3EB98`, copy the setting into the repeat count and return the
  delegated cursor, including a possible null result.

These describe the wrapper, not the effects of the external output/decoder.
Exploratory synthetic cases covered sentinel precedence, repeat suppression,
post-call word changes, control delegation and gate changes. No live execution
or complete decoder semantics were established.

## Experiments already attempted

The pinned m2c draft was adapted to actual halfword cursor advancement. Its raw
pointer-increment spelling must not be copied without checking units against the
original two-byte increment.

Structured infinite loops, goto-shaped m2c output, early returns, shared count
updates, explicit local pointers, volatile views and value/width round trips did
not achieve a full instruction match. Several shortened text to 224 or 228
bytes, shifting all later functions and data references. A `do...while` draft
produced the correct 232-byte length but still differed in 31 instruction words
in the local linked comparison: it placed the gate-test block after the negative
command block, and assigned the work/gate base registers differently. Correct
length alone is not a match.

Two bounded, local, two-worker decomp-permuter runs also failed to reach zero.
External and function type mutation were disabled; the second also disabled AST
removal. They use the already reviewed local toolchain; no distributed workers
or game data uploads were used. Scorer improvements are search hints only.

The stable native target uses one gate base in the ordinary-word loop but direct
loads on the repeat-suppressed and delegated-control exits. Marker stores precede
those exit loads. Preserve these observations while examining basic-block layout
and temporary lifetimes; do not solve register differences with fabricated symbol
aliases, changed external signatures or instruction patches.

## Next bounded experiment

Use the correct-length do-while draft and explicitly compare block ordering,
saved-register allocation and the two exit reloads in the full translation unit.
Preserve known signatures and callback ordering while changing one C structure
at a time. Run synthetic cases again for any candidate, then require original
function size, guest symbol, code bytes and full-ROM identity through a fresh
`verify.py` run before removing the assembly placeholder or increasing totals.
The comparator and command decoder remain independently unresolved.

## Related matching stream implementation

The separate unpaced reader `func_8003EB34_3F734` now matches C. A typed 16-bit
end sentinel preserves its original comparison operands; cursor advancement,
signed token handling and the retained decoder interface have native matching
evidence and synthetic coverage. It does not use the paced reader's gate,
repeat-count or marker-update paths and cannot replace it. See the current
[choice-list checkpoint](VM_CHECKPOINT.md#choice-list-and-unpaced-stream-increment).

## G64-028 — retained negative-token decoder trace

**Research checkpoint — 2026-11-11.** `func_8003DF98_3EB98` remains
`GLOBAL_ASM`. It reads one signed halfword from `$a1`, keeps that cursor in
callee-saved `$s0`, dispatches the token, and returns the saved cursor advanced
by two bytes. It has no null or length check; callers must provide a readable
halfword. The original extent is 528 bytes / 132 words at VMA `0x8003DF98`, ROM
`0x3EB98`, SHA-256
`76285ca92a7f611916d867d9938f93fcb3df32ebfa2962120083f2471a501631`.

### Signed range and command dispatch

The body sign-extends `*(s16 *)$a1`, adds `0x47`, and uses unsigned `< 0x28`
to select a 40-entry table at VMA `0x8007D068`. Thus signed tokens `-71..-32`
(`0xFFB9..0xFFE0`) index the table. Every recognized command and every
unrecognized value returns `input_cursor + 2`; unrecognized values land at
`0x8003E190`, which performs that single-halfword advance. This is a routing
map, not an assignment of game meaning based on command names.

| Signed token(s) | Target | Direct, instruction-supported operation |
| --- | --- | --- |
| `-71 (FFB9)` | `E028` | Call `E5B8`, then advance one halfword. |
| `-70 (FFBA)` | `E018` | Call `E548`, then advance one halfword. |
| `-69..-64 (FFBB..FFC0)` | `E190` | Unmapped table entries; advance one halfword. |
| `-63 (FFC1)` | `E004` | Call `D2C0` with the then-current `D_801C7754`. |
| `-62 (FFC2)` | `DFF0` | Store state value 4 to `D_801C77E0`. |
| `-61 (FFC3)` | `DFE0` | Call `E1A8`. |
| `-60 (FFC4)` | `DFD0` | Call `C3EC`, forwarding the incoming `$a0` value. |
| `-59..-58 (FFC5..FFC6)` | `E190` | Unmapped table entries; advance one halfword. |
| `-57 (FFC7)` | `E17C` | Call `C640` with `D_801C7754` loaded before the call. |
| `-56 (FFC8)` | `E158` | Call `C5E4` with `D_801C7754` and `0x40000000`; reload `D_801C7754` after that call, then call `C60C`. |
| `-55 (FFC9)` | `E144` | Call `C5A4` with `D_801C7754` loaded before the call. |
| `-54 (FFCA)` | `E120` | Call `C570` with `D_801C7754`; reload `D_801C7754` after that call, then call `C568` with `0x40400000`. |
| `-53..-52 (FFCB..FFCC)` | `E108`, `E0F0` | Each calls `C430` with the current `D_801C7754` and immediate 9. |
| `-51 (FFCD)` | `E0DC` | Call `C488` with `D_801C7754` loaded before the call. |
| `-50 (FFCE)` | `E0C8` | Call `C454` with `D_801C7754` loaded before the call. |
| `-49..-38 (FFCF..FFDA)` | `E190` | Unmapped table entries; advance one halfword. |
| `-37..-32 (FFDB..FFE0)` | `E0B0..E038` | Each calls `C53C` with `D_801C7754` and immediate 0, 2, 4, 6, 8, 0 respectively. |

`0xFFFF` / `-1` is **outside** the decoder's valid range. If called directly,
it follows the unmapped one-halfword path. Both known callers intercept it
first: the paced reader clears its marker and returns null; the unpaced reader
uses it as its end sentinel and returns without calling the decoder. Preserve
that caller-side sentinel check. Tokens outside `-71..-32`, including other
negative halfwords, take the same decoder fallback; they do not select a table
entry.

### Helper, marker and cursor ordering

- The decoder does not branch on or store incoming `$a0`. Some handlers forward
  that value unchanged (`E5B8`, `E548`, `C3EC`); other paths replace `$a0` with
  a freshly loaded `D_801C7754` before calling a helper. Keep the declared
  two-argument interface and do not rename the first argument from these facts
  alone.
- `$s0` preserves the input script cursor across helper calls. The decoder
  reads the token before dispatch, does not reread that token after a helper,
  and increments the local cursor only after the helper call(s). It returns
  that cursor; it does not directly update `D_80077858`.
- The two-call commands `FFC8` and `FFCA` load `D_801C7754` again after the
  first helper returns. A callback changing that global is visible to the
  second helper. The script cursor remains the saved `$s0` value.
- In paced reader `DE80`, the initial signed token is read before the repeat
  gate. A nonnegative token is loaded again in the output-call delay slot; after
  the output callback, DE80 reloads both the repeat setting `D_801C7798` and
  current token from the original cursor. It advances by two and stores that
  post-callback token in work marker offset `+8`. Thus callback mutation of
  token memory or the repeat setting is observed there.
- For paced negative input, `-1` clears marker `+8` and returns null without a
  repeat-setting copy. Other negative tokens clear marker before calling this
  decoder; after it returns, DE80 reloads `D_801C7798` and copies it to repeat
  counter `D_801C77A0`.
- In unpaced reader `EB34`, the signed token is loaded before the branch and
  output/decoder call. For a nonnegative token, it passes that value to
  `D060`, then increments its local cursor by two without rereading the same
  halfword. For negative non-sentinel input it passes the current pointer to
  the decoder, then replaces its local cursor with the returned pointer.
- Paced wrapper `DBEC` loads the global cursor before calling `DE80`, then
  stores DE80's returned cursor to `D_80077858` afterward.

The helper command arguments and instruction ordering above are verified;
their external engine effects are not recovered here. In particular, the
trace does not establish that a command helper mutates the resource-ID global.
`D_801C7754` is the observed VM context argument source and is distinct from
the D468 resource-ID word.

### Future host-model matrix

These are future C-model acceptance cases, not executed tests. The ROM-bound
guard `test_vm_control_decoder_original.py` validates the original instruction
extent, token table and critical caller anchors, but no semantic model was
written for this task.

| Case | Setup | Assertions |
| --- | --- | --- |
| Signed range edges | `-72`, `-71`, `-32`, `-31`, `-1`, 0, and positive halfwords. | Only `-71..-32` enter the 40-entry table; others advance by two if directly passed to DF98. |
| Full dispatch | Every token `FFB9..FFE0`. | Target/call sequence matches the ROM table, including the 20 one-halfword fallback entries. |
| Incoming `$a0` forwarding | Exercise `FFB9`, `FFBA`, `FFC4` with distinct owner values. | Calls that do not reload `$a0` receive the incoming value; context-based commands load `D_801C7754`. |
| Context mutation between helpers | For `FFC8` or `FFCA`, first helper changes `D_801C7754`. | Second helper receives the newly loaded context; script cursor still returns as original pointer+2. |
| Token memory mutation | Helper changes the halfword at decoder input. | DF98 itself still returns the saved input pointer+2 without rereading the token. |
| Paced positive callback | Output callback mutates current halfword and `D_801C7798`. | DE80 marker records the updated token; post-callback repeat-setting load observes the updated setting. |
| Paced repeat suppression | Gate helper suppresses a nonnegative token. | No output callback; marker becomes `-1`; cursor remains at the original token; repeat interval is copied as observed. |
| Paced negative sentinel | Current token is `-1`. | Marker clears, no DF98 call or repeat-setting copy, and return cursor is null. |
| Paced negative command | Token is negative but not `-1`; decoder callback changes repeat setting. | Marker clears before DF98; post-return repeat-setting reload is copied to counter. |
| Unpaced positive callback | Output callback mutates current token. | Call uses the preloaded signed token and cursor advances after callback without rereading that halfword. |
| Unpaced sentinel/delegation | Token `-1` versus another negative token. | `-1` exits without decoder; other negatives call decoder and adopt its returned cursor. |
| Unsafe memory | Null cursor, truncated input, or misaligned pointer. | No behavior is promised: the original immediately performs a signed halfword load and has no bounds/null guard. |

The original-bound guard passed 132/132 decoder words and 54 exact instruction
anchors spanning the decoder and callers, plus the 40-token dispatch table.
See `plans/execution/2026-11-11-g64-028-control-decoder-trace.json`.
