**22 November 2026 research-only update (do not count as promoted):** Two JP2307 failed halfword routines, `func_80219328_6A0A28` and `func_80222F18_68C608`, now reproduce exactly 28/28 original bytes each using a typed unsigned halfword field at offset `0x18`, with two sequential stores. [Research sources, standalone IDO verifier and sanitizers](research/jp_halfword_retry_20261122/README.md). The original 32 MiB ROM SHA-1 and native instruction matches and 65,536-case ASan/UBSan tests were run; **combined original-ROM G2, retail-ROM, ELF, all relocations, inventory and full local CI were NOT run** due to unavailable complete current-branch source checkout. Both remain ASM, official Japan remains **2,314 C / 5,062 ASM**. The other four JP2307 failed candidates and three 48-byte clear loops remain blocked.

# Goemon 64 matching-C — active continuation

**21 November 2026 Japanese JP2314 structural C published:** Seven previously ASM-owned original Japanese C functions / 284 original MIPS instruction bytes are **PUBLISHED_REMOTE_VERIFIED** in [commit `921b024be4ef`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/921b024be4efd068e98f30853c62401ecae55f92). Japan **2,314 matching C / 123,236 original instruction bytes / 5,062 ASM**. Native original expanded and retail ROMs byte-identical, 7,376 ELF identities, all 80,747 semantic relocations including 15 newly compiled symbolic records, strict inventory and full 363+349 CI with original C sanitizers PASS. [Native original-ROM G2](results/japan_0_2314_expand7_g2_20261121.json), [publication record](results/japan_0_2314_expand7_publication_20261121.json), [source/replay](research/jp_expand7_20261121/README.md). Three original table-clear routines remain FAILED_NATIVE and ASM.


**21 November 2026 Japan JP2307 alternate-type C published:** Four new original C functions / 160 original bytes are **PUBLISHED_REMOTE_VERIFIED** in [commit `ea758300aab5`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/ea758300aab5de1d344d4025a56314de72022bbc). Japan **2,307 C / 122,952 bytes / 5,069 ASM**, exact 32 MiB expanded and 16 MiB retail ROM, 7,376 ELF identities, 80,747 original semantic relocations, strict inventory and 358+349 local CI. The original predicate `func_08001410_70F980` has a deliberately incomplete false-path return in C because the actual MIPS leaves `v0` unchanged there; this is C undefined behaviour, documented rather than presented as portable Boolean logic. [Native G2](results/japan_0_2307_retry10_g2_20261121.json), [publication ledger](results/japan_0_2307_retry10_publication_20261121.json), [six remaining ASM failures](research/jp_retry10_20261121/failed_native.json).


**21 November 2026 Japan JP2303 retry29 published:** 29 previously failed unique functions rechecked; 5 already accepted, **14 newly native exact original C (512 original bytes)**, 10 remain ASM. **PUBLISHED_REMOTE_VERIFIED: Japan 2,303 C / 122,792 bytes / 5,073 ASM** in [implementation commit ca77fe2b4d5b](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/ca77fe2b4d5b47b106b723a23a60da5b34b0d4b7). Native G2 preserves byte-identical expanded/retail ROMs, 7,376 ELF identities and 80,747 semantic relocations; full 353+349 local CI and host sanitizers passed. [G2](results/japan_0_2303_retry29_g2_20261121.json), [publication ledger](results/japan_0_2303_retry29_publication_20261121.json), [source and failures](research/jp_retry29_20261121/README.md).

**21 November 2026 Japanese JP2289 G2 publication:** Seven new original-address C functions / 156 bytes, **PUBLISHED_REMOTE_VERIFIED** in [implementation commit `f7a7f3565540`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/f7a7f3565540b552904ebc21a0cf2ebe3ea8118a). Japanese **2,289 C / 122,280 original machine-code bytes / 5,087 ASM**. The original 32 MiB expanded ROM and 16 MiB retail ROM, all 7,376 ELF identities and all 80,747 semantic relocations are exact; full 348+349 local CI PASS. [Native original-ROM proof](results/japan_0_2289_tiny7_g2_20261121.json), [publication record](results/japan_0_2289_tiny7_publication_20261121.json), [source/replay guide](research/jp_tiny7_20261121/README.md). Three exact isolated matches were excluded as already accepted JP2268 functions.


**21 November 2026 JP2,282 published and remotely verified:** Four new Japanese original C functions / 120 original instruction bytes, [implementation commit `0d4380410965`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/0d438041096567c85b315eb284ea9b548b9f8491). Japanese **2,282 original-address C / 122,124 bytes / 5,094 ASM**. Exact 32 MiB expanded and 16 MiB retail ROM, 7,376 original ELF functions, 80,747 original relocations, strict inventory and full local CI passed. [G2 evidence](results/japan_0_2282_donor4_g2_20261121.json); [publication record](results/japan_0_2282_donor4_publication_20261121.json).


**21 November 2026 Japan donor-template JP2278 publication:** Ten new original-address Japanese C functions / 716 instruction bytes from accepted donor algorithms, [implementation commit `56c01ff13bfc`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/56c01ff13bfc0de545261057a51da9d7cbba11ee). **PUBLISHED_REMOTE_VERIFIED: Japan 2,278 C / 122,004 original instruction bytes / 5,098 ASM**. Original native expanded/retail ROM matches, all 7,376 ELF identities and 80,747 semantic relocations, strict inventory and full CI PASS. [Native G2](results/japan_0_2278_donor10_g2_20261121.json), [publication record](results/japan_0_2278_donor10_publication_20261121.json), [replay guide](research/jp_donor10_20261121/README.md). USA and `main` unchanged.


**21 November 2026 Japan JP2268 publication:** **145 new original-address Japanese C functions / 8,952 bytes**, preserved in [implementation commit `1fa94856a8a5`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/1fa94856a8a52ec069107fceaa7c828149e9b96a). **Published and remotely verified: Japan 2,268 C / 121,288 original code bytes / 5,108 ASM**. Original native complete-ROM/ELF/all-relocation G2 and full local CI passed; see [original G2 evidence](results/japan_0_2268_short145_g2_20261121.json), [remote publication ledger](results/japan_0_2268_publication_20261121.json) and [source/replay guide](research/jp_short145_20261121/README.md). USA unchanged; no emulator gameplay test.

**Verified native G2 snapshot:** USA **1,965** from independent original-ROM proof; Japan **2,314** from the latest full original-ROM G2 and remotely verified implementation `921b024be4ef`, 21 November 2026. Always check live branch HEAD and latest regional proof. Work on `chatgptweb/decomp`, never `main`.

The **entire preceding 170,260-byte runbook, including every dated promotion, native mismatch, original VM observation, local diagnostic command and historical compiler experiment, is preserved unchanged** in [CONTINUE_HISTORY_20261121.md](CONTINUE_HISTORY_20261121.md) (SHA-256 `8e171ea8f9b8466b0bc525a59928c16f92d9c5fbc0e89b04502ddc291e13d2e5`). This file contains only current operational instructions. The root [PROGRESS.md](../PROGRESS.md) and individual proof/research ledgers retain the rest of the audit trail.

## Active task registry and cross-chat resumption

Use [the active curated task registry](tasks/README.md), [task records](tasks/registry.json) and
[goemon-task-registry skill](../.agents/skills/goemon-task-registry/SKILL.md)
for `list`, `resume GQ-...` and `checkpoint` requests. The registry
holds pending and externally blocked work, plus completed maintenance
proofs. The closed 100-task G64 roadmap is historical. Before acting,
re-fetch the live decomp branch, pending PRs and original-address function
ownership. Registry entries are planning metadata, not G2 acceptance.

## Latest complete original-ROM G2 results

| Region | New original-address C | Original C instruction bytes | Original ASM remaining | Complete ROM | Original ELF positive FUNC entries | Semantic relocations |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| USA | **1,965** | **84,648** | **5,398** | 33,554,432/33,554,432 exact | 7,376/7,376 | 82,103/82,103 |
| Japan rev-0 | **2,314** | **123,236** | **5,062** | 33,554,432/33,554,432 exact | 7,376/7,376 | 80,747/80,747 |

- USA expanded original SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`. Latest seven scheduler-related promotions: four original 48-byte wrappers, then one 52-byte and two 56-byte insertion wrappers. Proof: [USA 1,962](results/usa_scheduler4_1962_g2_20261121.json), [USA 1,963](results/usa_scheduler5_1963_g2_20261121.json), [USA 1,965](results/usa_scheduler6_1965_g2_20261121.json), [scheduler research](docs/USA_TASK_SCHEDULER_LIFECYCLE_20261121.md).
- Japan expanded original SHA-1: `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. Latest original-ROM promotion is [JP2314 structural-family G2](results/japan_0_2314_expand7_g2_20261121.json), published in [commit `921b024be4ef`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/921b024be4efd068e98f30853c62401ecae55f92), with a [publication ledger](results/japan_0_2314_expand7_publication_20261121.json). Prior JP2307 G2 remains immutable.
- Each 7,376 includes **13 previously unmarked upstream C functions** in the USA inventory. USA 1,965 newly reconstructed + 13 upstream = 1,978 unmarked, with 5,398 ASM. Do not double-count regions or upstream C.
- **Canonical USA snapshot caveat:** [results/combined.json](results/combined.json) and [results/inventory.json](results/inventory.json) remain authentic snapshots from **1,956** USA matching functions. Later full-G2 reports above establish **1,965**. Do not manually change an original proof or manifest merely to reconcile the displayed count.

## Current unresolved research (not accepted matching C)

- USA `func_80034734_35334` (344 bytes): scheduler/task executor; native IDO register-save/codegen still mismatches. Original ASM stays. Related research: [scheduler lifecycle](docs/USA_TASK_SCHEDULER_LIFECYCLE_20261121.md) and [issue #138](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/138).
- USA `func_80002040_2C40` (120 bytes): task dispatcher is **still assembly-owned on this canonical HEAD**, but [draft PR #152](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/152) now reports independently full-ROM-exact **1,966 local G2**. Its integration/full CI against the *latest joint checkout* remains pending, so do not count it as published or reattempt the same candidate blindly. See [issue #136](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/136).
- Japan `func_8001F70C_2030C` (68 bytes): isolated C instruction match **fails original semantic relocation identity**; must remain ASM. Japan `func_8003D0D8_3DCD8` (548-byte VM reset manager) and `func_8001F750_20350` (2,184-byte pause controller) remain failed native C. See [Start/VM G2 report](docs/GOEMON_START5_G2_PROMOTION_20261121.md).
- Japan `func_08001228_6B3168` (72 bytes) and `func_080012AC_6B51AC` (192 bytes) remain ASM because the source loses five original branch-relocation records, despite isolated instruction equality. See [issue #117](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/117).
- Open research candidates and lost-input investigations remain separate from verified C; see [issues #86](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/86) and [#124](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/124). Re-deduplicate original addresses against live accepted ownership before any new attempt.

## Source authority and work procedure

1. Confirm `git status --short`, `git branch --show-current`, live remote `chatgptweb/decomp` SHA, pinned original source/ROM/toolchain and regional manifest. Read [AGENTS.md](../AGENTS.md), [executor protocol](plans/EXECUTOR_PROTOCOL.md), [batch pipeline](BATCH_PIPELINE.md), [candidate promotion rules](CANDIDATE_PROMOTION.md) and relevant original-MIPS/ABI/IDO skills. The retired G64-001–100 plan is historical; select actual remaining ASM and independently promising candidates.
2. Establish original ROM offset, VMA, byte extent, ELF/section/translation-unit owner, ABI, caller/callee evidence and all original relocations. Compile using pinned **SGI IDO 5.3** and the original per-region layout; test authentic C host semantics with ASan/UBSan. An isolated exact function or synthetic test cannot increase the matching-C count.
3. Stage only unique new functions with all existing accepted C and surrounding original ASM. Require full **32 MiB exact-ROM**, all **7,376 positive-size ELF function identities**, the complete region-specific **82,103 USA / 80,747 Japan semantic relocation multiset**, strict accepted-C/ASM inventory and full local CI. An exact ROM with altered relocation semantics is rejected.
4. For any failure, preserve original ASM and a bounded, reproducible mismatch report. Do not massage MIPS bytes, replace missing provenance, infer game behaviour from static C, or claim emulator execution without an actual trace.
5. Publish only after passing every required gate: implementation, manifest/region adapters, proof/inventory, tests, `decomp/CONTINUE.md` and root `PROGRESS.md` in the same coherent commit. Re-fetch the GitHub commit SHA and source proof before marking publication verified. Do not change `main` or commit ROMs, raw original ASM, game assets, ELFs/objects, toolchain archives, credentials, saves or memory dumps.

## Reproducible local commands

Run inside a complete, authenticated Linux checkout. Verify tool arguments against `--help`; paths below are placeholders, not assumptions about another machine:

```bash
python3 -m decomp.local_ci               # ROM-free Python + actual-C host sanitizers
python3 -m decomp.verify \
  --upstream /path/to/pinned-mnsg \
  --workdir /path/to/NEW-verify-workdir \
  --retail-rom /path/to/original-USA-retail.z64 \
  --report /path/to/NEW-verify-proof.json \
  --uv /path/to/uv --binutils-root /path/to/pinned-mips-binutils --jobs 2
# Only after successful complete-ROM verification, using its actual outputs:
python3 -m decomp.inventory \
  --baseline /path/to/NEW-verify-workdir/baseline \
  --candidate /path/to/NEW-verify-workdir/candidate \
  --report /path/to/NEW-inventory.json
```

The verifier creates new workdirs and refuses reused output paths. A successful ROM-free `local_ci` is **not** native G2; region-specific promotion adapters may be required beyond the default canonical USA manifest. For private-toolchain environment handling and historical commands, consult [the archived full runbook](CONTINUE_HISTORY_20261121.md) and `GOEMON_BUILD_ENVIRONMENT.md` when supplied in the ChatGPT Project; never reuse archived user-specific absolute paths without validating them.

## Retention and cleanup boundaries

Historical native proof snapshots are not disposable merely because their count is old. [Results retention audit](results/README.md) and [21 November retention review](docs/DECOMP_RETENTION_AUDIT_20261121.md) document which files are uniquely valuable. Keep research, failure traces, real source/code hashes, input provenance and all distinct G2 proofs. No game code is removed by this runbook reorganisation.
