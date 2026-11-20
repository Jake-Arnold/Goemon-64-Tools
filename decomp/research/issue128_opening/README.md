# Issue #128 — USA opening scene setup wrappers

2026-11-20. USA decomp base `a412f9646405866a70115c0da77e6848eba40330`.
[Issue #128](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/128)

## Six wrappers ready for combined verification

The issue reported original ROM matches for ten scene setup wrappers. The
live 1,723-function proof already includes `func_8020D84C_67722C`,
`func_8020D8E4_6772C4`, `func_8020D908_6772E8` and
`func_8020D94C_67732C`. The six object motion helpers from the issue
are also already accepted.

The six remaining setup wrappers were reconstructed from the original
`file_18` owner `676C80.s`. All six match the original relocatable
instructions and every corresponding text relocation tuple (function-relative
offset, kind, symbol). Each function was then linked at its original VMA using
the original ELF symbol values and compared against its bytes in the
authenticated decompressed USA ROM.

| Function | Bytes | Text relocations | Linked instructions SHA-256 |
| --- | ---: | ---: | --- |
| `func_8020D818_6771F8` | 52 | 5 | `12bd2e7878600a396e5d1e335df233ecff7e365f3b4252a0a81e8d73b99763cb` |
| `func_8020D870_677250` | 32 | 1 | `cfc37a1de2389b0272284977abf5dbebee389a13a113c433e6d7d9764c46cda6` |
| `func_8020D890_677270` | 52 | 5 | `61fcda8d6bd8f4c5e7ff163298d5df016c24823944233bbdf41f71c123a47e43` |
| `func_8020D8C4_6772A4` | 32 | 1 | `8de2550b3d5c4ab71cb76f0746eeee5424288a6bee91c27a0b5b2a0a8946de` |
| `func_8020D92C_67730C` | 32 | 1 | `876f2302c3e77dbf15be3f5b7315bd5bffb5de9031b0bf96fd5b6fc74a0573df` |
| `func_8020D978_677358` | 32 | 1 | `34ec8ad82a4de72a155b6d8926fedfe060ec5e3f69616531c86f6598e10b9aee` |

Replay from repository root with a locally built, untouched USA baseline
from pinned mnsg `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. The checker
validates retail and expanded ROM SHA-1 and the native IDO 5.3 digest.

```sh
python3 decomp/research/issue128_opening/verify_wrappers.py /path/to/pinned/mnsg
```

Source SHA-256 for `opening_setups.c` is
`f69087b235b86079f835e24d98ba52069ecc48114a4ec8b30a2ce108222d2c7d`.
Changing the resource ID from `0x4DD` to `0x4DE` in a scratch copy caused
the expected relocatable text mismatch. Full `python3 -m decomp.local_ci`
passed (289 decomp tests with one skip, 349 verifier/ledger tests, task and
evidence validation, and configured host sanitizer suites).

Status is **RESEARCH_ONLY / ISOLATED_EXACT** for 232 instruction bytes and 14
relocations. For promotion, split the wrappers into their six original ranges
around the four accepted siblings, then run the fresh combined `decomp.verify`
and strict inventory. The existing G2 and accepted count remain authoritative.

## Shared context helper and main controller

`func_8020D2A0_676C80` uses a sign-extended halfword at a symbolic offset
from a runtime base, indexes a pointer table, and assigns the result to two
destinations. The direct store form and local pointer form both compiled to
56 bytes. The saved `context_probe.c` form reads back through the first
destination expression and compiled to 60 bytes versus the original 64.
The first difference is the destination register of the initial HI16 load
(original `t8`, generated `t6`). The retained source recovers one explicit
destination address in a register, while the compiler still folds the second
destination into a HI16 and store. Its SHA-256 is
`9dcd7568ca2ea3402c43ecf4a13f7fd908dcad0128bc6bb263642bf4a6061902`.
Keep the helper as ASM (**FAILED_NATIVE**). Any next probe should account for
the two distinct destination address registers and the register allocation in
the enclosing source unit.

The attached checkpoint 6 source reproduced its reported 17,348-byte
instruction extent, 128-byte stack frame, 551 direct calls in order, and
3,058/4,337 same-position raw object words. All 34 switch state entries
match their original offsets. The first raw word difference is at
`+0x5C`, where the state 0 branch delay slot reloads the context pointer
into `t5` instead of the original `t1` for the shared timer increment.

### Controller data matches after restoring the inline literals

Checkpoint 6 declares the controller's floating constants as external
symbols. Original IDO emits the constants and three jump tables in
source order when those constants are expressed as literals. Replaced
22 declarations with round-trip literals read locally from the verified
original ROM. A fresh original-address link at text VMA `0x8020D998`
and pool VMA `0x8022A6C8` produced the following.

| Result | Checkpoint 6 | Restored literals |
| --- | ---: | ---: |
| Linked switch table and constant pool bytes | 160/336 | **336/336** |
| Table entries exact at original offsets | 40/48 | **48/48** |
| Linked instruction words at original offsets | 3,059/4,337 | 3,059/4,337 |
| Linked instruction bytes at original offsets | 15,823/17,348 | 15,824/17,348 |
| Original state entry offsets | 34/34 | 34/34 |

The data region spans USA expanded ROM `0x6940A8..0x6941F8` (exclusive).
The compiler produced the third jump table at the original relative pool
offset `0xD4` after recovering the first 11 literals. Restoring just the
last seven constants in addition left a gap after the third table. Restoring
all 22 recovered the whole region, including alignment. The full
pool source SHA-256 is
`8afc9ebf06ff742922daabab754b056850cfbcf72c8b27553871c338b470232c`.

After the literal rewrite, raw text relocation tuples changed from
671/685 to 629/685 matching exact offset, type and symbol because IDO
references section-relative literals. The linked comparisons above apply
those relocations at the original addresses. Neither result proves
whole-unit relocation equivalence. The separate state 33 volatile base
reload probe retained all 34 state entries but grew the function by 8 B
and reduced the number of same-position raw words from 3,058 to 2,947.
The first executable mismatch remains the state 0 delay slot. Tighten
the epilogue and its incoming control flow next while preserving the exact
pool and state entry offsets.

Replay checkpoint 6, the restored pool and the state 30 probe from the source-only ZIP. Keep the
output and local inputs outside Git.

```sh
python3 decomp/research/issue128_opening/replay_controller_pool.py \
  /path/to/pinned/mnsg /path/to/checkpoint6.zip /path/to/new/private/output
```

The replay links and compares the standalone objects, saves the candidate C,
and writes a JSON report with all 34 per-state extents and matching word counts.
State bounds are measured between adjacent case entries, so the last range
also contains the epilogue. Full ROM-free `python3 -m decomp.local_ci` and
the six-wrapper verifier passed. The controller remains **FAILED_NATIVE /
RESEARCH_ONLY**. Combined G2, strict inventory and gameplay were not run.

### State 30 timer recovery

The original tests the signed timer in a register and writes the 32-bit
value to `sp+0x74` only on the interpolation path. Checkpoint 6 spills a
16-bit temporary to `sp+0x72` before the upper-bound check and omits the
32-bit store. The replay's `state30-timer` variant reads the timer field in
the guard and assigns the widened value inside the guarded block. IDO
combines the field reads as in the original. Keeping the unused halfword
declaration preserves the original interpolation output at `sp+0x4C`.

| Linked result | Restored literals | State 30 timer |
| --- | ---: | ---: |
| Instruction words at original positions | 3,059/4,337 | **3,065/4,337** |
| Instruction bytes at original positions | 15,824/17,348 | **15,855/17,348** |
| State 30 words at original positions | 183/285 | **189/285** |
| State 30 opcode mismatches at original positions | 9 | **0** |
| Constant pool bytes | 336/336 | 336/336 |
| State entry offsets | 34/34 | 34/34 |

The variant has SHA-256
`a161e059220229140b3d9ee031e9e80da225cc243304648e197460bb3c1f1238`.
A volatile state 2 pointer load grew its block by four bytes. Adding
the state 30 word store with the old temporary still live also grew
the function by four bytes. Removing the temporary declaration moved
the interpolation output to `sp+0x50` and lost matches. Those three
variants were discarded.

A position-by-position comparison of the original `.file_18` disassembly
and the linked state 30 variant found 1,250 differing words with the same
mnemonic and operands apart from register spelling, 16 with different
mnemonics, and six with other operand differences. This classification
measures text similarity and does not establish equivalent register use.
The remaining opcode differences are in states 2, 10, 12, 26, 28 and 33.
State 2 is the first such difference, at `+0xC4`: the original commits
the result store before loading the next pointer. The first raw word
difference remains `+0x5C`, in the shared timer branch's delay slot.
The next bounded probe should preserve the instruction count while
recovering the state 2 load ordering or the state 10 cleanup loop.

Fresh native replay, full ROM-free local CI and the separate wrapper
verifier passed. **FAILED_NATIVE** for the controller. G2 still needs an
exact controller and unit integration with original semantic relocations,
followed by the full-ROM comparison and strict inventory.
