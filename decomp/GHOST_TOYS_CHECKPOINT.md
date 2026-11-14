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
- Historical isolated linked C probe: correct size, 35 instructions, with two
  differing words at the pointer save/reload (`sp+0x18` candidate versus
  `sp+0x1C` original). Its recorded candidate source SHA-256 is
  `1b3d52c6f3e73bfb422a83ceff6ad12560fdb13da2fa7d58443d9760003482b0`.
- That historical source is not present. The checked-in draft
  `decomp/candidates/ghost_probe.c` hashes to
  `666eb7a02d1768aa6f1983e6600aca315e0463098ff8cc2c064c57097a4993de`;
  the historical two-word comparison therefore does **not** describe this
  draft. The sanitized result remains useful only as historical provenance.
  See [the comparison record](results/ghost_entrance_candidate.json) and
  [G64-058 execution evidence](plans/execution/2026-11-14-g64-058-ghost-spill.json).

The ordinary m2c draft loses the original reused-pointer call shape. Earlier
logged source variants and a bounded 30-second permuter search did not produce
an exact match. The current draft's source hash is not bound to the historical
near-match report. No code-byte patching was used. The bounded v2 trial budget
is exhausted; without the historical source or new ABI evidence, another
compiler variant has no falsifiable basis.

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

Keep `func_08006490_6F9970` assembly-owned. Resume native work only if the
historical source is recovered or original interface evidence predicts a new
spill layout. Continue with G64-059's bounded semantic fixture, then the
overlay promotion gate; preserve all other overlay functions as assembly until
each replacement passes exact source-unit, address, relocation and full-ROM
proof.
