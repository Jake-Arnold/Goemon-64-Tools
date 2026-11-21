# Goemon 64 matching-C — active continuation

**Verified snapshot:** `chatgptweb/decomp` commit `553bc85e4f6e3a9be08b8e85c01768a82ad646be`, 21 November 2026. **Always fetch the live remote HEAD and latest regional proof before starting.** The numbers below are a dated snapshot, not a fixed acceptance target. Work on `chatgptweb/decomp`, never `main`.

The **entire preceding 170,260-byte runbook, including every dated promotion, native mismatch, original VM observation, local diagnostic command and historical compiler experiment, is preserved unchanged** in [CONTINUE_HISTORY_20261121.md](CONTINUE_HISTORY_20261121.md) (SHA-256 `8e171ea8f9b8466b0bc525a59928c16f92d9c5fbc0e89b04502ddc291e13d2e5`). This file contains only current operational instructions. The root [PROGRESS.md](../PROGRESS.md) and individual proof/research ledgers retain the rest of the audit trail.

## Latest complete original-ROM G2 results

| Region | New original-address C | Original C instruction bytes | Original ASM remaining | Complete ROM | Original ELF positive FUNC entries | Semantic relocations |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| USA | **1,965** | **84,648** | **5,398** | 33,554,432/33,554,432 exact | 7,376/7,376 | 82,103/82,103 |
| Japan rev-0 | **2,123** | **112,336** | **5,253** | 33,554,432/33,554,432 exact | 7,376/7,376 | 80,747/80,747 |

- USA expanded original SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`. Latest seven scheduler-related promotions: four original 48-byte wrappers, then one 52-byte and two 56-byte insertion wrappers. Proof: [USA 1,962](results/usa_scheduler4_1962_g2_20261121.json), [USA 1,963](results/usa_scheduler5_1963_g2_20261121.json), [USA 1,965](results/usa_scheduler6_1965_g2_20261121.json), [scheduler research](docs/USA_TASK_SCHEDULER_LIFECYCLE_20261121.md).
- Japan expanded original SHA-1: `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. Latest two original VM resource/countdown functions are documented in [Japan 2,123](results/japan_0_2123_vm_g2_20261121.json) and [the VM source/proof report](docs/GOEMON_VM_TWO_G2_PROMOTION_20261121.md). Source and proof were remotely re-verified.
- Each 7,376 includes **13 previously unmarked upstream C functions** in the USA inventory. USA 1,965 newly reconstructed + 13 upstream = 1,978 unmarked, with 5,398 ASM. Do not double-count regions or upstream C.
- **Canonical USA snapshot caveat:** [results/combined.json](results/combined.json) and [results/inventory.json](results/inventory.json) remain authentic snapshots from **1,956** USA matching functions. Later full-G2 reports above establish **1,965**. Do not manually change an original proof or manifest merely to reconcile the displayed count.

## Current unresolved research (not accepted matching C)

- USA `func_80034734_35334` (344 bytes): scheduler/task executor; native IDO register-save/codegen still mismatches. Original ASM stays. Related research: [scheduler lifecycle](docs/USA_TASK_SCHEDULER_LIFECYCLE_20261121.md) and [issue #138](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/138).
- USA `func_80002040_2C40` (120 bytes): task dispatcher; original-address source remains research-only. See [issue #136](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/136).
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
