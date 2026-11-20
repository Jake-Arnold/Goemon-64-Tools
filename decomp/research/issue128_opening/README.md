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

The issue's checkpoint 6 reports 3,058 of 4,337 same-position raw object words
and 671 of 685 exact relocation tuples for the 17,348-byte
`func_8020D998_677378`. Its source bundle is referenced in the issue as a
conversation attachment. It was unavailable in the checkout and local build
inputs, so this run did not compile or modify the controller. Recover that
source before spending another native experiment on the controller. Combined
G2, strict inventory and gameplay were not run for these research sources.
