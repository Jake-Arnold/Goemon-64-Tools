# Consolidated Goemon work queue (2026-11-08)

This is the repository's cross-conversation handoff for the Goemon toolkit and matching-C projects. Prior ChatGPT conversations named “Goemon” or “Goemon Decomp Continuation” contain useful research but **are not independent sources of current function counts or proof**. Always read `AGENTS.md`, `decomp/CONTINUE.md`, `decomp/manifest.json`, `decomp/results/combined.json`, `decomp/results/inventory.json`, and the live `chatgptweb/decomp` HEAD first. This file records an evidence-bound snapshot, not a claim that old attempts were freshly re-run.

## Verified checkpoint; do not repeat

- Matching-C branch promotion checkpoint: `869771dc92872a8b4e05f77c7adebe2e7cef260e`. At this checkpoint: **140 reconstructed matching-C functions, 10,108 bytes; 13 upstream C entries; 153 combined C entries; 7,223 assembly entries of 7,376 identified**. VM: 54 C / 15 ASM.
- The **136-byte** `func_8003EFB0_3FBB0` and **44-byte** `func_8003F350_3FF50` have both been promoted. The callback's corrected signed return declaration is integrated. Do not redo the earlier provisional 138/139-function work.
- `decomp/results/combined.json` records exact original-address matches and byte-identical independent assembly/linking of the full **33,554,432-byte** decompressed image, expected SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; the retail input SHA-1 is `df8083a54296b8c151917c5333e1c85f014a2a66`.
- The single uninterrupted formal verification runner timed out; its resumed clean build passed independent full-ROM and inventory comparisons. **An uninterrupted formal verifier run remains outstanding**. Never mislabel the interrupted formal run as successful.
- The earlier collision gate (80 bytes) and heap no-op (8 bytes) are already included in the 140. Their pinned source/layout guards must remain enforced.

## Open matching-C work (ordered)

| Priority | Target | Precise unresolved condition |
| --- | --- | --- |
| P0 | Uninterrupted 140-function formal verifier | Restore exact latest branch/toolchain/baseline and execute `decomp.verify` to completion. Refresh proof provenance only if independently rebuilt output is exact. |
| P2 | VM text loop `func_8003DBEC_3E7EC` | 472 original bytes; earlier 480-byte draft differs in 101 words. Separate pointer/cursor and two unsigned input halfwords, account for six branch-likely delay slots, two counters, dynamically reloaded outer bound, and callback early-return path. This is **static analysis, not a verified match**. |
| P3 | VM loader `func_8003D468_3E068` | Approximately 548-byte original; an old candidate matched 118/137 instruction positions only. Resolve real resource-prefix declarations, address loads, and register allocation. |
| P1 (promotion) | Choice edge `func_8003D0B0_3DCB0` | **New isolated linked match**: IDO 5.3 generated a 204-byte function symbol; all 51 MIPS words matched at 0x8003D0B0 after original-address relocation (SHA-256 `7a3c723bffe43e3b044e60c385b9a6577a34eab380ebcc1eb3f8a38ab3c93fe8`); `.text` carries four additional zero bytes beyond symbol extent. Candidate is `candidates/vm_choice_edge.c`; 100 sanitized host cases pass. **Do not promote without correctly accounting for alignment and independently rebuilt whole-ROM identity.** |
| P4 | VM wrapper `func_8003F6E8_402E8` | Original extent 48 bytes; natural C reproduced first 40 bytes (10 words) but not the unreachable eight-byte return tail. Do not promote a 40/48 prefix. |
| P5 | VM comparator `func_8003D9B8_3E5B8` | Remains ASM. `vm_compare_reference.h` is host-only semantics, not exact C proof. |
| P5 | Overlay key initializer `func_080001BC_6F369C` | 96-byte isolated linked probe matched; main-segment manifest verifier cannot yet prove overlay ROM/VMA/section layout. |
| P5 | Ghost Toys entrance | Historical 140-byte draft retains two incorrect stack offsets; `decomp/GHOST_TOYS_CHECKPOINT.md` documents them. |

Do not rerun the unchanged 762-function scalar sweep. After a failed candidate, preserve the mismatch, improve a concrete typed declaration or code shape, and move to another target. Promotion requires the exact original-address MIPS bytes **and** independent full decompressed-ROM byte identity.

## Main-branch toolkit status (superseded historical backlog)

The user confirmed on 2026-11-08 that the earlier native-warp and story-flag investigation is **already working on `main`**. The former unsolved warp/spawn/Benkei/story-flag checklist in this queue was from early conversations and is no longer an active task. `main` remains the source of truth for that toolkit work; do not revive stale experiments or change `main` under the decomp-only authorization. Continue solely on exact matching-C, original-address/compiler/ROM proof, and relevant safe tests.

## Library, toolchain, and reproducibility notes

- User-supplied Files Library artifacts include `goemon-matching-rebuild.zip`, `toolkit.zip`, `python312.tar.gz`, `mips-binutils.part-00`, `mips-binutils.part-01`, and the USA retail ROM. Re-list and materialize these on **each new execution**; container state is not persistent.
- The two MIPS parts concatenate to a valid inspectable `.tar.gz` archive (555,600,578 combined bytes). The Python 3.12 archive also lists successfully. Validate actual binaries and dependency locks after extraction.
- `goemon-matching-rebuild.zip` contains an older full-build snapshot and has an identified **CRC mismatch** in generated `candidate/asm/usa/file_72.s`. Never invent replacement bytes or treat a partial extraction as a verified clean checkout. Recreate generated assembly only from pinned source/ROM/toolchain using the normal derivation pipeline.
- On 2026-11-08, the recovered archived toolkit checkout at `261ac0badc4cf23ffa0813f44bc5d21097565bad` passed **365 host/unit tests, 4 skips, 0 failures** under `xvfb-run`. This does **not** test the latest 140-function checkout or perform a full-ROM build. A non-Xvfb initial run encountered 15 Tk display errors and was superseded by that passing Xvfb run.
- Remote `git ls-remote` from that container failed DNS resolution; the connected GitHub API remains an alternate source for checking refs and writing reviewed, non-binary documentation. Do not conflate connector access with a local Git fetch.
- Do not commit ROMs, assets, saves, generated assembly, object files, compiler archives, runtime logs, credentials, personal paths or raw memory. Preserve historical proof and diagnostic reports.

## Working rule

The **live `chatgptweb/decomp` branch**, not any conversation's last reply, determines current counts and integrated functions. Implement only substantive, independently validated changes. Record tests (including skips and environment), remaining blockers and next steps in `PROGRESS.md` with every repository change. Commit and push only `chatgptweb/decomp`, without force, and verify the new remote commit SHA.
