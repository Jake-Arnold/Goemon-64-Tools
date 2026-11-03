# Native map transition research targets

Date: 2026-11-03. Evidence is from the pinned US baseline at commit
`7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, whose decompressed ROM SHA-1 is
`6ea0ed71032ce08fc2745f412d84936382197494`. Addresses below are original guest
addresses and ROM offsets. These functions are assembly unless noted; none has
been established as the complete scene loader or unload routine.

## Isolated pieces and call links

| Function | ROM offset / size | Evidence | Status |
| --- | --- | --- | --- |
| `func_80215330_5D0800` | `0x5D0800` / `0x1C0` | Exit actor path reads its packed fields, writes destination/entry parameters through the system pointer, and can alter a special destination based on saved flag `0x17`. Called at `0x5D07B8` and `0x5D07DC`. See [entrance trace](../docs/ENTRANCE_WARPS.md). | ASM; scene/overlay context matters. |
| `func_800214E4_220E4` | `0x220E4` / `0xE4` | Reads 10-byte default entry records at ROM `0x6C380`; copies coordinate and mode fields to saved entry fields, or zeros them if all three coordinates are zero. Called at `0x220AC` and `0xBFB0`. | ASM; immediate reconstruction target. |
| `func_80021444_22044` | `0x22044` / `0xA0` | When a guard is not `0xFF`, copies map/entry context, calls `800214E4`, then `8000B864`; all paths call `80003728(0x0B)`. | ASM; exact branch and effects visible, broader state meaning needs tracing. |
| `func_80003728_4328` | `0x4328` / `0x64` | Stores its argument to system offset `0x3ADD4`, zeros `0x3ADD5`, sets `0x3ADCA` to 2, then calls `80003628(0)`. Static initial system base `0x8008CCC0` makes the first two bytes `0x800C7A94` and `0x800C7A95`. | Matching C in `transition_state.c`; state setter, not a complete loader. |
| `func_80003628_4228` | `0x4228` / `0x50` | Writes its argument to system `+0x3ADD6`, zeros `+0x3ADD7`, and calls `80003528(0)`. `80003528` similarly writes `+0x3ADD8`, clears `+0x3ADD9`, calls `80003428(0)`. | Both matching C in `transition_state.c`; do not assume these are room cleanup. |
| `func_80002718_3318` | `0x3318` / `0x220` | Dispatches using system byte `+0x3ADD6`; one path reads `0x800C7A95` and calls `80003728` with different states, including 8 and 15. | ASM; state-machine lead, no complete lifecycle proof. |
| `func_801CB5D0_5874E0` | `0x5874E0` / `0x1D8` | Reads signed pending coordinates for player creation; native stores downstream are documented in the entrance trace. | ASM; relevant to placement after a transition. |
| `func_80037060_37C60`, `80037070_37C70`, `80037080_37C80` | `0x37C60..0x37C90` | Write 2, 1, 3 respectively to `0x800C7A95`. | Already fully matching C in `warp_state.c`; not proof of a complete warp. |

`func_80021444` is evidence of a chain leading to state `0x0B`, not evidence
that calling this function is safe or sufficient to unload/reload a map. The
previous door trace in [recovery baseline](../docs/RECOVERY_BASELINE.md) is a
sampled runtime observation, not a native call trace. A separate in-game replay
was not conducted for this analysis.

## Work performed and next step

The existing batch's minimal-context attempts for `800214E4` and `80003728`
reported missing types. An initial `80003728` C draft reproduced the observed
field updates and one-argument `80003628(0)` call, but IDO produced 88 bytes
versus the original 100; variants using the first inferred two-argument call
were also mismatches. The second register is overwritten by the callee and must
not be treated as a confirmed argument. Drafts and logs are in private Linux
research directories `/root/goemon64-scene-state-probe-v1`, `-v2`, and `-v3`.
They are not matching C and are excluded from the manifest and count.

Next, recover actual `SYS_W` field declarations and compile with reviewed SDK
context, then compare relocated instructions for `80003728` and `80003628`.
Trace the dispatch path from `80002718` to resource allocation, release and
actor creation; distinguish file/overlay loading from room teardown. Promote only
after semantic host checks, unchanged inventory and complete-ROM equality. No
raw scene-request write, automatic warp, or claim of safe unloading follows from
this trace.

## State setter reconstruction

`func_80003728_4328` is now fully matching C (100 bytes). Existing upstream
`SYS_W` calls the three affected fields `stepw`, `stepw_end` and
`retraces_per_game_step`. Using a narrowed argument produces an exact match;
both unsigned 8-bit and unsigned 16-bit source forms match, so the original
parameter width is not uniquely established. The implementation uses `u8`
because the value is stored as a byte. The synthetic host test verifies writes
occur before the `80003628(0)` call. This does not establish scene load or
unload safety.

The called helpers `func_80003628_4228` and `func_80003528_4128` now also
match as C (80 bytes each). Their combined synthetic test checks the full chain
through the stubbed `80003428(0)`, including all intermediate byte resets.
The state bytes and downstream function remain incompletely characterized.

`func_80003428_4028` also matches as C (80 bytes). It sets system
`+0x3ADDE`, clears `+0x3ADDF`, and calls `80003380(0)`. The combined host
test now exercises the four matching setters up to a stub of that next call.
These are state-machine primitives, not identified room unload operations.
