# USA Mini movement clamp — original context gate MIPS micro-execution (21 November 2026)

**RESEARCH_ONLY / FAILED_NATIVE. Not a matching-C promotion.** Original `func_801CD310_589220` is 4,320 bytes at ROM `0x589220`, VMA `0x801CD310`, overlay `file_11`. The tested micro-execution window is `+0x1B4..+0x257`. This begins at the previously reported first unmatched context block after the restored exact switch/trigonometry region.

## Measured evidence
- Pinned `mnsg` upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, authentic retail USA SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`, decompressed USA 32MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Rebuilt the **unmodified original** USA ROM: **33,554,432/33,554,432 bytes identical**.
- A read-only Python MIPS micro-interpreter fetched **actual original instruction words from the authenticated private expanded ROM**. It models the scalar loads/stores, COP1 float operations/comparisons, branch and *branch-likely* delay slots in this bounded window, halting before successor code at `+0x258` or `+0xB30`.
- **3,000/3,000** deterministic tests agreed with a separately coded branch/write oracle. Inputs include flags `0,1,2,0x7f,0x80,0x81,0xff`, three task-mode variants, five context status words, signed zero, infinities, NaNs and varying movement/threshold values. Four reset writes, unconditional stack writes, path-specific delay-slot loads and two exit targets were asserted.
- **1,672** runs reset movement; **1,849** exited at `+0x258`; **1,151** exited at `+0xB30`. Original branch opcode/target signatures were checked before execution. Private game instruction bytes were *not* embedded in the script or report.
- The standalone `context_gate_probe.py` script (SHA-256 `208e58baa43c4b29f4bb5fab81c65b3af25deb68a1c393bf571852f533122c2a`) is delivered in the conversation file `GOEMON_CONTEXT_GATE_MICROEXEC_20261121.zip` with full report and read-only JSON. It requires only Python 3 and the user's original decompressed ROM.

## Original dataflow and exact branch semantics

| Relative offset | Original operation / invariant |
| --- | --- |
| `+0x1B4` | `$f14 := +0.0f`, kept live through context branch and used in unconditional `sp+0x8C` store |
| `+0x1B8..+0x1BC` | `$v1 := *(task+0x5C)` using task in `$a3`; `$v0 := *(u8*)(ctx+0x59)` |
| `+0x1C0..+0x1F4` | If flag nonzero and either high bit clear or `(*(f32*)(*(D_801FC60C)+0x20) * 40.0f) < *(f32*)(ctx+0x54)`, enter four-field reset; `c.lt.s` unordered comparison is false |
| `+0x1F8..+0x210` | `$f16 := 0.0f`; store zero to task `+0x7C,+0x74,+0x70,+0x68` in original order, then **reload ctx from task+0x5C and reload flag from ctx+0x59** |
| `+0x214..+0x220` | Initialize `$f16` to zero for all paths; store the earlier `$f14` to `sp+0x8C`; clear halfword `sp+0xE0` in the delay slot of a flag branch |
| `+0x224..+0x240` | When flag is zero, task `+0x98 != 0` and float task `+0xA4 <= 0.0f` bypass the context status-bit gate and enter `+0x258`; task `+0x88` loads to `$f10` in taken-only delay slot |
| `+0x244..+0x254` | Otherwise test `(*(u16*)ctx & 2)`; bit clear branches to `+0xB30` and loads ctx `+0x18` **in taken-only delay slot**; bit set preloads task `+0x88` to `$f10`, then enters `+0x258` |

Critical original branch-likely sites: `bc1fl +0x1F0`, `beqzl +0x228`, `bc1tl +0x23C`, `beqzl +0x24C`. The source must preserve conditional memory accesses, not merely an ordinary C Boolean truth table. The original restores task into `$a3` from `sp+0xE8` after two earlier trig calls; the previous C candidate's `$a0` task lifetime differs. Early `$f14` and later `$f16` are distinct live ranges. Maintain the context and flag reloads after resetting motion before changing control-flow structure.

## Gate state
**PASS:** SHA-1 checks, pristine original full-ROM rebuild, original-block micro-execution (3,000/3,000), branch destinations and delay-slot write/read assertions.

**NOT RUN:** new complete clamp C compile, whole-function native instruction/relocation equality, complete canonical `decomp.verify`, strict inventory, full `decomp.local_ci`, emulator gameplay.

The previous clamp candidate is still `FAILED_NATIVE`. Its full C source is only in a separate prior conversation artifact, not a committed repository file; no unsupported full-source mutation is claimed. The local shell cannot resolve GitHub DNS to materialize the latest decomp checkout. As of the latest independent G2 report: USA **1,965 accepted C, 84,648 instruction bytes, 5,398 ASM**. Older result snapshot files are dated.

**Next:** With the complete candidate source present, test the three interdependent live ranges `sp+0xE8 → $a3`, `task+0x5C → $v1` with mandatory post-reset reload, and early `$f14` vs later `$f16` as a single bounded original-block source experiment. Stop if it worsens original-offset instruction identity.
