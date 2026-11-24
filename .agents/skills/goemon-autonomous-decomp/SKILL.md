---
name: goemon-autonomous-decomp
description: "Use when autonomously discovering, native-verifying, and formally promoting Goemon 64 matching-C functions during a ChatGPT or Codex session."
---

# Autonomous matching-C decomp

**Base `stable/decomp`, topics `decomp/*`.** Toolkit `stable/toolkit`; `main` and `chatgptweb/decomp` legacy. Read `BRANCHES.md`, Project prompt, `AGENTS.md`, `decomp/CONTINUE.md`, `decomp/plans/EXECUTOR_PROTOCOL.md`, current manifest/proof/inventory and PRs. Fetch live SHA.

Read [the source-layout strategy](../../../decomp/TRANSLATION_UNIT_LAYOUT.md) for original versus reconstructed ownership. Prefer evidenced original unit boundaries where practical; keep accepted C intact, record artificial splits, and require full fresh native proof for bounded layout consolidation. Alignment is a heuristic, not historical proof; layout-only work does not increase matching-C counts.

1. Authenticate complete checkout, ROM, upstream and pinned IDO; check region/ROM/VMA/ASM ownership, canonical C and pending PRs.
2. **Before every native IDO attempt**, read `decomp/COMPILER_QUIRKS.md`; identify relevant verified behaviour. Classify first original/generated mismatch **before variants**; test one-variable bounded workarounds.
3. **Every attempt** records one `EXISTING_QUIRK_REPRODUCED`, `EXISTING_QUIRK_NOT_APPLICABLE`, `NEW_REPRODUCIBLE_QUIRK`, or `NO_NEW_COMPILER_FINDING`. Include exact flags, source hashes, first instruction/relocation difference, commands and negative controls. No generality without independent reproduction.
4. Record new reproducible or useful falsified compiler findings in central ledger and `PROGRESS.md` in **same research/implementation commit**; keep ASM if not promoted.
5. Match original IDO at original VMA, whole unit, ELF identities and relocations. Isolated matching is research only.
6. Stage all accepted C. Run fresh `decomp.verify`, strict `decomp.inventory`, `decomp.promotion_integrity --validate`, exact 33,554,432 ROM bytes/region hash, ELF/reloc checks and require the full **Decomp ROM-free regression** GitHub Actions job (runs `decomp.local_ci`, not `--quick`) on the current PR merge commit. Follow the rollout fallback in `AGENTS.md`; GitHub CI is not native G2.
7. Publish C/manifest/proof/inventory/tests/ledger/`CONTINUE.md`/`PROGRESS.md` atomically with SHA lease. Verify remote counts; no force-push or duplicate promotions.

Failed gates retain ASM/count: `FAILED_NATIVE`, `FAILED_ROM`, `BLOCKED_INPUT` or `RESEARCH_ONLY`. USA and JP proof independent.
