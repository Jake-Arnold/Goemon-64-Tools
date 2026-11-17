---
name: goemon-autonomous-decomp
description: "Use when autonomously discovering, native-verifying, and formally promoting Goemon 64 matching-C functions during a ChatGPT or Codex session."
---

# goemon-autonomous-decomp

Execute a bounded batch. Read Project `GOEMON_AUTONOMOUS_DECOMP_SESSION_PROMPT.md`, root `AGENTS.md`, `decomp/CONTINUE.md`, `decomp/plans/EXECUTOR_PROTOCOL.md`, manifest/proof/inventory **at `chatgptweb/decomp` HEAD**. Never touch `main` or re-promote C.

1. **Access:** Obtain a complete source checkout. For shell/connector mismatches use `goemon-github-source-bridge`; connector access is not a local checkout. Use `goemon-input-reproduce` to verify ROM, upstream, IDO and MIPS tools. Keep ROM/ASM/binaries out of Git.
2. **Discovery:** Read unpromoted source/research and Issues/PRs; use `goemon-target-triage`, original MIPS, ABI and bounded probes. Deduplicate. Record ROM/VMA, region/overlay, size, callers and unit. Preserve ASM on failure.
3. **Exactness:** Compile C with original IDO/flags; verify behavior, unit bytes, sibling layout, symbols and relocations. Isolated matching or source hash is not a promotion.
4. **G2:** Stage candidates with **all** accepted C; run fresh `python3 -m decomp.verify`, then `python3 -m decomp.inventory` only if G2 passes. Audit ELF identities and relocations. USA must match original 33,554,432 ROM bytes and SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
5. **CI:** Run full `python3 -m decomp.local_ci`, not `--quick`; run focused tests. No GitHub Actions.
6. **Publish:** Only on PASS, update C/stages, manifest, combined proof, inventory, ledgers, tests, `decomp/CONTINUE.md` and `PROGRESS.md` together; archive prior proof. Use `goemon-evidence-publish`; verify remote SHA/count on decomp only. No force-push.

Missing input or failed gate: do **not** change accepted count. Report `BLOCKED_INPUT`, `FAILED_NATIVE`, `FAILED_ROM`, or `RESEARCH_ONLY` with first measured failure. Continue independent targets. Separate USA and Japan proof. No invented tests or pushes.
