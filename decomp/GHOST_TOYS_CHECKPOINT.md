# Ghost Toys entrance reconstruction checkpoint

The user's torch/door experiment supplied the exact byte and masks needed to
locate the native entrance update. [Behavior and native call trace](../docs/GHOST_TOYS_ENTRANCE.md).

## Target and result

- Original function: `func_08006490_6F9970`, 140 bytes at ROM `0x6F9970`, overlay
  file `0x02B`, logical guest entry `0x08006490`.
- Behavior: test saved IDs `0x19A` and `0x19B`; only if both are set, set `0x19C`,
  set task flags bit 0 at offset `0x60`, call the helper with argument `0x224`,
  then replace the callback with `func_0800651C_6F99FC`.
- Reconstruction: m2c plus reviewed partial task-field context, then direct
  examination of IDO output and bounded source/ABI variants.
- Best isolated linked C probe: correct size, 35 instructions, two differing
  bytes in two words. Both are the stack displacement for preserving/reloading
  the reused saved-flag test pointer: candidate `sp+0x18`, original `sp+0x1C`.
- [Sanitized machine-code comparison](results/ghost_entrance_candidate.json)
  records expected/candidate code hashes and the exact differing words.

The ordinary m2c draft loses the original reused-pointer call shape. Restoring
the shared test pointer and symbolic indirect entry calls reproduces the rest
of the instructions. Simple stack-padding declarations alter the entire frame
instead of fixing just that slot. A bounded 30-second permuter search did not
produce an exact match. No code-byte patching was used.

## Evidence boundary

This remains **non-matching work**, excluded from the manifest, combined result
and verified C count. The native source already establishes the condition; the
remaining mismatch concerns compiled layout, not a newly discovered flag meaning.
The engine entry-point declarations and complete overlay interface still require
review. The draft/variants/compiler logs are preserved locally in the ignored
research workspace, not bundled with the published matching units.

No new game writes, warp shortcuts, health freezes or actor experiments were
performed by this decomp work. A linked function match alone would still require
original-unit integration and a whole-ROM build before promotion.

## Next

Resolve the pointer spill location through the original compiler/interface
context, then handle the overlay's non-16-byte function boundary without altering
payload bytes. Continue tracing torch flag writers and the subsequent callback's
loading-zone/animation behavior. Preserve all other overlay functions as assembly
until each replacement passes the same exact-byte/address and full-ROM gate.
