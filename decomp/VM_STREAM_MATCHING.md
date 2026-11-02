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
