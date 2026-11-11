# Object dispatcher wrapper trace

Current result on `chatgptweb/decomp` after the 2026-11-11 fresh IDO replay:
the 96-byte production translation unit at ROM `0x35C64` matches exactly. The
earlier 2026-11-10 note about an eight-byte swap is superseded by the rerun and
complete-ROM result. Keep the dated report as historical evidence, but use the
current manifest and `results/combined.json` for accepted ownership.

## `func_80035094_35C94`

| Point | Verified behavior |
| --- | --- |
| Entry | One signed 32-bit actor argument arrives in `$a0`. |
| Frame | The function reserves `0x18` bytes, saves the actor at `sp+0x18`, and saves `$ra` at `sp+0x14`. |
| First call | It loads the current resource global at `0x8016DAB4` and passes it to `func_800362DC_36EDC`. |
| Second call | It reloads the saved actor from `sp+0x18` and passes it to `func_800350C4_35CC4`. |
| Return | It restores `$ra`, releases the `0x18`-byte frame, and returns. |

The first callback may mutate the resource global. The actor argument remains
independently saved across that callback and is the second callback's argument.
The neighboring `func_80035064_35C64` remains 48 bytes and is unchanged.

## Current native and full-ROM evidence

- Pinned IDO 5.3, original function addresses and the full 96-byte source-unit
  comparison passed with the current `object_dispatch.c` source.
- Fresh G2 candidate build reports 148/148 accepted functions, 11,020 function
  bytes, and identical 33,554,432-byte ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Fresh inventory reports 161 combined C, 7,215 ASM and 7,376 total entries.
- Host regression coverage checks callback order, global mutation and preserving
  the actor input. It is synthetic and does not replace the native or ROM gates.

The prior eight-byte mismatch was a useful stop condition for the earlier source
variant. The current byte-for-byte unit and G2 proofs establish that this
production source compiles as required. No speculative behavior names were
introduced.
