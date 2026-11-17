# 2026-11-17: 727-C original-USA native coexistence checkpoint

**Research only: original-ROM build PASS; central G2 and production promotion NOT complete.**

Starting from canonical 342-C commit `1961f1333e8a5007c3cf8df5dfa0d0ca5a0cea8b`, the verified canonical C source files were reconstructed via connector exports with 466 unique Git blob SHA checks and no mismatches. The pinned upstream USA checkout at `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` was independently rebuilt using the original ROM and IDO toolchain. That rebuilt 32 MiB original USA ROM exactly.

A new manual linked candidate preserved all 342 canonical C functions, and replaced the original file_12 text with the 385 research C functions, including the contiguous 374-wrapper source, while retaining the two existing canonical file_12 callbacks. The 24 original-address ASM/C input objects were compiled and adjusted only for zero trailing alignment; original file_12 output layout was preserved.

## Native build and inventory

- **Combined 727-C full original USA ROM:** 33,554,432/33,554,432 original bytes identical; SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- **file_12 original relocation multiset:** 7,051/7,051 matches by site, type, original symbol name and resolved address.
- **Original ELF positive-sized function inventory:** 7,376 entries, same names and VMAs; the repository's actual `decomp.inventory.summarize_inventory` gate PASSED for **727 new matching C functions** and 13 original upstream C entries. Remaining assembly 6,636 entries.
- Two accepted canonical main function-size annotations (already unrelated to the new file_12 C) differ: `func_8000D3B8_DFB8` (64 original, 72 candidate), `func_8003F6E8_402E8` (48 original, 56 candidate). The inventory tool explicitly reports and allows these annotations.
- Complete ELF relocation multisets across every region are **not identical** (original 82,216; candidate 82,111), notwithstanding exact final ROM and exact file_12 relocation provenance. This broader mismatch requires gate-aware interpretation and is not claimed as a success.

## Remaining blockers — NO PROMOTION

- The *versioned central 727-function* manifest/adapter and formal `decomp.verify` + `decomp.inventory` complete run have **not** been executed. The whole-ROM exact candidate was manually linked against the canonical prepared checkout.
- `decomp.local_ci --quick` FAILED because the temporary reconstructed source snapshot lacks `decomp/results/vm_residual_inventory.json` and the 15+ `.agents/skills/*/SKILL.md` fixtures. The sampled 225 decomp test pass/fail summary reported 2 failures and 1 missing-file error. No CI passing claim.
- Canonical `chatgptweb/decomp` has advanced beyond the input snapshot to SHA `f4f1ba28aa0a317471598110f9c0bcebc7ea9b6f`, now **346** matching C / 17,720 bytes, adding four independent file_11 functions: `func_801E7E18_5A3D28`, `func_801E7F08_5A3E18`, `func_801EF9F4_5AB904`, `func_801F05D0_5AC4E0`. All four are outside file_12. Therefore the fresh promotion target is **731**, not 727.

The 727 original-ROM candidate proves the prior 342+385 native coexistence, but does **not** promote 727 or 731. Preserve the production manifest and proofs until a current-head central G2 with complete CI passes. Never commit ROM/ELF/generated game assembly or extracted assets.
