# USA original 4,320-byte clamp CFG recovered, exact stack lifetime mapped, and +6 valid original-offset ABI diagnostic

**22 November 2026 · RESEARCH_ONLY / FAILED_NATIVE.** Original target `func_801CD310_589220`, ROM `0x589220`, VMA `0x801CD310`, native length **4,320 bytes**, original frame **232 bytes**. Original USA expanded SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`. Pinned upstream commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; original SGI IDO 5.3.

## Fundamental new decompilation route: repair original numeric switch table for m2c

The original 18-entry table `jtbl_8020A85C_5C676C` contains **five distinct numeric jump targets**. The bundled m2c failed to analyse this complete function because the original assembly/data identify the table entries as raw addresses rather than branch labels. In a private **scratch copy only**, `rebuild_original_switch_cfg.py` validates the original 32 MiB ROM SHA-1, maps five existing function-local target instruction addresses to symbolic labels, and rewrites the 18 *scratch data-table reference strings* to those labels. **No MIPS instruction bytes, original ROM, original upstream source, or production files were changed.**

After the adjustment, `tools/m2c/m2c.py -t mips-ido-c --valid-syntax --no-cache -f func_801CD310_589220` successfully reconstructs the full original function as **565 lines / 23,095 characters** of source-like C control flow (previously impossible because m2c rejected the table). The C output is a heuristic analysis, **not automatically valid original source or matching C**. Some helper function prototypes, float/pointer casts and types are guessed incorrectly; attempting genuine IDO compile of raw auto-output failed those type checks. Private generated ASM and m2c C are not included in the source archive or GitHub.

## Original stack-variable identity is now recovered directly

The private original machine-code and recovered control flow establish these original stack slots:

| Guest sp displacement | Original role |
| --- | --- |
| `0x64` | Second trigonometric-return float |
| `0x6C` / `0x6E` | Second/first switch-selected u16 angles |
| **`0x8C`** | **Same magnitude float from default zero, through 3D sqrt overwrite, through late multiplier** |
| `0xA4,0xA8,0xAC` | First three-component float vector |
| `0xB0,0xB4,0xB8` | Second three-component float vector |

The read-only original-ROM stack auditor, checking opcodes/registers/displacements without publishing machine words, passes original **five magnitude-slot events**: **`+0x218` `swc1 f14,sp+0x8C`** (initial zero), **`+0x4E4` `swc1 f0,sp+0x8C`** (3D magnitude overwrite), **`+0xFE8` `lwc1 f4,sp+0x8C`**, **`+0xFFC` `swc1 f8,sp+0x8C`** (post-multiplier update), **`+0x1000` `lwc1 f10,sp+0x8C`**. Three additional original angle/trig stack signatures pass, **8/8 total**. Original m2c expresses `sp8C = 0.0f` **after the context gate**; actual IDO is able to define `f14` before the gate, but spills it only later. This explains why the previous candidate's eager `f14` spill at `sp+0xD4` differs from original. It is a substantially more specific source-reconstruction constraint than forcing register names.

## New native whole-function original-position improvement

Authentic IDO 5.3 compiled two complete source-only research candidates against the same original ROM/ELF:

| Research C | Candidate size / frame | Exact comparable original-pos instruction words | Original-offset/type/symbol relocation triples |
| --- | --- | --- | --- |
| Prior strongest recoverable F14 source, normal one-argument cosine prototype | **4440 / 232 B** | **117/917** | **30/101** |
| **ABI diagnostic: keep second angle live as extra first cosine argument** | **4440 / 232 B** | **123/917** | **30/101** |

The candidate variation changes only the reconstructed cosine forward declaration to `f32 func_80003EA0_4AA0(u16, ...)` and the **first** call to `func_80003EA0_4AA0(pool_u16_1,pool_s32_0)`. This makes IDO keep the original second switch angle in `$a1` across the first trig JAL, reproducing the **exact original `sh a1,sp+0x6C` instruction at `+0x198`**. Both original trig **R_MIPS_26** call relocation triples at `+0x19C` and `+0x1A4` match. The full switch/trig window is now **55/55 comparable non-relocated words exact**, with jump-table target offset drift zero. F14 initialisation at `+0x1B4`, 232 frame, 33 calls and nine inline `sqrt.s` persist. First nonreloc mismatch stays at `+0x44`; full FUNC remains 120 bytes too long.

**Important ABI limitation:** original cosine implementation `func_80003EA0_4AA0` uses only `$a0 & 0x3FF` and returns a table float via `$f0`; it does **not** read `$a1`. The additional argument does not alter the observed callee machine behaviour, but the original C prototype is unknown and an inconsistent function declaration may be undefined at the source language level. **This candidate is explicitly diagnostic-only and cannot be accepted as matching-C evidence of an original two-argument API.** It also does not recover the original F16 reset words. Retain F14 strict one-arg and historical F16 eight-word sources independently; do not combine different candidate scores.

## Native experiments and evidence actually executed

- Pristine original-USA 32 MiB ROM rebuilt at pinned original upstream and checked **33,554,432/33,554,432 bytes exact**, same expanded ROM SHA-1; this is not an experimental C replacement ROM.
- 400 F14 typed-zero source variants, 432 F16 F14-lifetime variants, 1,144 F14 volatile/typed gate representations, 1,700 stack/object declaration layouts, 84 second-angle temp experiments and a focused cosine ABI matrix compiled under real SGI IDO 5.3. None combines original F14 and F16 in the **same** source. Most are negative diagnostic experiments; output logs retained locally and not claimed as accepted code.
- Full original 565-line m2c analysis from scratch jump labels: **PASS**. Real-ROM stack instruction signatures **8/8 PASS**.
- Four synthetic/rejection-mode switch-table converter tests **PASS**, two source reconstruction tests **PASS**.
- Strict one-arg and ABI diagnostic complete C freshly compiled and compared with original-ROM text, authentic ELF 101 text relocations, five switch groups, original call order, 232 frame and return/sqrt; **117→123** matching original-pos comparable instruction words. Both native-equality **FAIL**.
- Freshly extracted full 12-file source-only archive SHA256SUMS and exact source hashes PASS; both authentic native builds, 8-slot ROM verifier, full private-switch CFG m2c re-run and six unit tests **PASS**.
- Candidate-integrated original USA ROM, current accepted-USA combined `decomp.verify`, strict inventory, full `decomp.local_ci`, emulator gameplay: **NOT RUN** because whole function is not native equal.

**Reproducible 12-file source-only user archive:** `GOEMON_CLAMP_ORIGINAL_CFG_DISCOVERY_20261122.zip`, SHA-256 **`6ec59328d837e96cfa92067984266643777e7ab7093f7ef9ca4d2b5b6ff3e3f5`**. It includes the full two *independently reconstructed* C candidates (not raw original generated m2c), `rebuild_original_switch_cfg.py`, `audit_original_stack.py`, `replay_native.py`, `audit_scaffold.py`, six unit tests, `reconstruct_a1_probe.py`, README, SHA256SUMS and sanitized results. The matching GitHub converter/stack/source-generation scripts have their exact tested Git blob hashes preserved. Neither ZIP nor GitHub commit contains original ASM, ROM, assets, private ELF/objects, original generated m2c C, or compiler.

## Precise next legitimate C task

Using original control flow as a guide, model the *single magnitude backing stack location* equivalent to original `sp+0x8C` from its after-gate zero default through sqrt overwrite and late multiplier, alongside the independent `sp+0xA4/B0` vector buffers. Preserve **distinct F14 default and F16 reset** lifetimes without type-invalid register tricks. Use original CFG/MIPS to inspect original compiler's lifetime splitting and aliasing, not just arbitrary declaration permutations. Continue keeping original ASM authoritative until every original machine instruction and 101 relocations match.

**USA verified production unchanged: 1,965 accepted C / 84,648 original MIPS bytes / 5,398 ASM. PR #144 remains draft.**