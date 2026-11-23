# USA Mini Ebisumaru — canonical 11-C promotion, 23 November 2026

**PASSED_G2_LOCAL, awaiting atomic remote commit verification.** Canonical
USA production predecessor `cc4e1e1973770afad4c3c6cd7899731e1a64d571`: 2,079 matching C /
93,016 original bytes / 5,284 ASM. Ten original-file11 C functions were
staged first and verified as 2,089; the 384-byte Mini speed selector is then
staged as 2,090 with its preexisting original jump table preserved.

| Original function | Original USA ROM offset | Matching native bytes |
|---|---|---:|
| `func_801E2180_59E090` | `0x59E090` | 160 |
| `func_801E2220_59E130` | `0x59E130` | 68 |
| `func_801E2800_59E710` | `0x59E710` | 176 |
| `func_801E28D8_59E7E8` | `0x59E7E8` | 68 |
| `func_801E2AA0_59E9B0` | `0x59E9B0` | 180 |
| `func_801E2BA8_59EAB8` | `0x59EAB8` | 168 |
| `func_801E2CEC_59EBFC` | `0x59EBFC` | 64 |
| `func_801E2D74_59EC84` | `0x59EC84` | 188 |
| `func_801E31DC_59F0EC` | `0x59F0EC` | 104 |
| `func_801E3278_59F188` | `0x59F188` | 92 |
| `func_801E1C90_59DBA0` | `0x59DBA0` | 384 |
| **Eleven newly promoted candidates** | | **1,652** |

## Native original-address and entire ROM proof

- Authentic USA retail ROM SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`;
  expanded original 32MiB ROM SHA-1 **`6ea0ed71032ce08fc2745f412d84936382197494`**.
- Pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`,
  native SGI IDO 5.3 and pinned MIPS linker, original ROM addresses and
  original function extents. No MIPS opcode changes/assembly rewriting.
- **Canonical `python3 -m decomp.verify` PASS:** 2,090/2,090 functions and
  94,668 original instruction bytes, **33,554,432/33,554,432 byte-identical ROM**;
  all **7,376** positive-sized ELF function identities unchanged and
  **82,103/82,103** semantic relocations, including 8,825 file11, exactly equal.
  Complete semantic relocation SHA-256
  `f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97`.
  Original ELF SHA-256 `83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038`;
  2,090-C ELF SHA-256 `be30ab4a7add4378abe704fc2f8078582fdf1a81a5774243c040fdec0fca55ba`.
- **Canonical strict `python3 -m decomp.inventory` PASS:** 2,090 accepted-C
  candidates, 5,273 assembly remaining, 7,376 identified ELF functions,
  zero unexpected positive ELF aliases. `python3 -m decomp.promotion_integrity
  --validate` PASS, with name+bytes proof identities cross-checked.
- Ten-function `decomp.usa_mini10_promotion` requires immutable original
  source SHA-256, original 2,079 predecessor manifest SHA, original ROM
  identity/hash and disjoint original ROM ranges. The selector 
  `decomp.usa_mini_selector_promotion` requires exact predecessor 2,089,
  single native IDO symbol range, eight original jump-table data entries at
  `0x8020B2E0`, and changes only two compiler-produced ELF symbol references
  at text offsets `+0x138`/`+0x140` (original HI16/LO16). It explicitly
  compares complete compiled `.text` before/after the relocation-symbol
  adjustment; the compiled machine instructions remain byte-identical.

## Test and reproduction scope

Run from a complete checkout with the original private USA ROM, pinned upstream,
IDO 5.3 toolchain and original offline Python 3.12 environment installed:

```sh
python3 -m decomp.verify
python3 -m decomp.inventory
python3 -m decomp.promotion_integrity --validate
python3 -m decomp.local_ci
```

The four added host regression groups compile and execute the **actual eleven
original-ID0 C sources** under GCC or Clang compatible ASan+UBSan with real
function arguments, captured side effects and explicit stubs for external game
helpers; they do not emulate gameplay. The historical decomp and
verifier/ledger suites retain their archived checkpoint assertions by explicitly
omitting newer C stages only inside their historical tests, not in production.

- Decomp Python suite: **435 tests (3 skipped) PASS**.
- Verifier/ledger Python suite: **350 tests PASS**.
- C-Right comparator and canonical promotion integrity **PASS**.
- Full `decomp.local_ci` final result: **PASS (exit 0)**.
- Original on-console/emulator gameplay: **NOT RUN**.

Proof: `decomp/results/usa_mini11_2090_g2_20261123.json`, canonical
`decomp/results/combined.json` and `decomp/results/inventory.json`.
The original 2,079-function proof remains preserved in historical G2 artifacts.
No ROM, extracted original ASM, compiler/object binaries or game assets are
published. The previous independent source-only research PR #144 remains draft;
this work atomically promotes through the `chatgptweb/decomp` production branch
only after full local CI and expected-parent remote publication complete.
