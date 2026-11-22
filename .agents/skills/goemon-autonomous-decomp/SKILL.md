---
name: goemon-autonomous-decomp
description: "Use when autonomously discovering, native-verifying, and formally promoting Goemon 64 matching-C functions during a ChatGPT or Codex session."
---

# Autonomous matching-C decomp

Read `GOEMON_AUTONOMOUS_DECOMP_SESSION_PROMPT.md`, `AGENTS.md`, `decomp/CONTINUE.md`, `decomp/plans/EXECUTOR_PROTOCOL.md`, canonical manifest/proof/inventory **at live `chatgptweb/decomp` HEAD**. Never modify `main` or re-promote C.

1. **Access:** Complete checkout (`goemon-github-source-bridge` for connector limits), authenticated ROM/upstream/IDO/binutils (`goemon-input-reproduce`). No ROM, ASM or proprietary toolchain in Git.
2. **Triage:** Check *all current canonical C ownership and pending research* by region, original ROM/VMA/size/range, not stale filenames. Record collisions; preserve ASM on failure.
3. **Native:** Original IDO with exact code bytes, original address and relocations; preserve ELF layout. Isolated matching is **RESEARCH_ONLY**.
4. **G2:** Stage **all** accepted C on pinned live SHA; fresh `python3 -m decomp.verify`, then strict `python3 -m decomp.inventory`. Exact 33,554,432 bytes / SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, 7,376 ELF functions and semantic relocations.
5. **CI:** Full `python3 -m decomp.local_ci`, not `--quick`. Mandatory `python3 -m decomp.promotion_integrity --validate` requires canonical manifest **and** `combined.json`/`inventory.json`, each original name/size and entire ROM SHA-1 to agree. Staged research never increments counts. No GitHub Actions.
6. **Publish atomically:** One commit with native sources, canonical manifest, `decomp/results/combined.json`, `decomp/results/inventory.json`, dated G2 proof, tests, `decomp/CONTINUE.md`, `PROGRESS.md`. Preserve prior proof. Re-fetch branch and use expected-SHA lease; no force push. Re-fetch remote SHA/manifest/proof/count. Do **not** claim `PUBLISHED_REMOTE_VERIFIED` until live canonical count proves it.

Failure: retain ASM and count. Report `FAILED_NATIVE`, `FAILED_ROM`, `BLOCKED_INPUT`, `RESEARCH_ONLY` accurately. USA and JP acceptance separate.
