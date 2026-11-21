# Goemon 64 — matching-C decompilation

**Operational entrypoint:** [CONTINUE.md](CONTINUE.md) and the live `chatgptweb/decomp` branch. This track is separate from the toolkit on `main`. Do not merge decomp-only changes into `main`.

## Latest verified results — 21 November 2026 (live update)

The latest authentic full original-ROM G2 proofs record the following region-specific totals. **USA 1,965 and Japan 2,123 are present in the published decomp source.** USA 1,965 was independently verified by full original-ROM local G2, with source publication separately confirmed; Japan 2,123 is recorded as `PASSED_G2` and remotely re-verified.

| Region | Newly matching C functions | Original instruction bytes recovered | ASM functions remaining |
| --- | ---: | ---: | ---: |
| USA | **1,965** | **84,648** | **5,398** |
| Japan rev-0 (published G2) | **2,123** | **112,336** | **5,253** |

Each region has **7,376 original positive-sized ELF function entries**. These figures are region-specific; do not add USA and Japan counts or count original upstream-C functions as new reconstructions.

The prior five-function batch is [documented here](docs/GOEMON_START5_G2_PROMOTION_20261121.md) and remotely re-verified in [PROGRESS.md](../PROGRESS.md). Seven subsequent USA scheduler/insertion wrapper functions (192 + 164 original bytes) were independently full-G2 verified and published; see [scheduler lifecycle](docs/USA_TASK_SCHEDULER_LIFECYCLE_20261121.md), [four-wrapper proof](results/usa_scheduler4_1962_g2_20261121.json), [one-wrapper proof](results/usa_scheduler5_1963_g2_20261121.json) and [two-wrapper proof](results/usa_scheduler6_1965_g2_20261121.json). The latest two Japan-only VM functions are [documented separately](docs/GOEMON_VM_TWO_G2_PROMOTION_20261121.md) as **published and remotely verified G2**. Both rebuilt expanded 32 MiB ROMs match **33,554,432 / 33,554,432 original bytes**, preserving original ELF function identities and all semantic relocations. The native G2 tier proves code/layout equivalence, **not** emulator gameplay or Bomb Text Skip success.

**Snapshot caveat:** The checked-in canonical USA [combined proof](results/combined.json) and [inventory](results/inventory.json) still represent the earlier **1,956-function** stage. The later **1,958-function** USA G2 acceptance is [here](results/glitch_start5_2121jp_1958usa_g2_20261121.json); subsequent scheduler G2 ledgers reach **1,965** with preserved ROM/ELF/relocation identity. The **2,123 Japan published G2** proof is [here](results/japan_0_2123_vm_g2_20261121.json). Do not edit a proof JSON or inventory count without a fresh authentic rebuild. See [INVENTORY.md](INVENTORY.md) for the arithmetic and provenance boundaries.

## How work is selected

Use current unconverted assembly ownership, original function offsets/VMAs, caller context and already tested candidates. The retired G64-001–100 execution plan is **not** an authoritative backlog. Historical research stays available for native codegen hints and blocked candidates.

1. Check branch HEAD, [CONTINUE.md](CONTINUE.md), accepted sources and the region's latest G2 ledger.
2. Check original assembly/source ownership and deduplicate against accepted functions before attempting new C.
3. Use the original pinned SGI IDO 5.3 and original-address compiler/linker evidence, including the complete relevant source translation unit and relocations.
4. Only promote after full exact original-ROM, function-identity, complete semantic relocation, strict inventory and full local CI acceptance. Record both regional totals independently.
5. Publish to `chatgptweb/decomp` only; re-fetch remote source and proof SHA before marking `PASSED_G2`.

## Core references

- [Current decomp handoff](CONTINUE.md) — latest completed and pending work.
- [G2 verifier](verify.py) and [strict inventory](inventory.py) — executable verification gates.
- [Candidate promotion](CANDIDATE_PROMOTION.md), [native batch pipeline](BATCH_PIPELINE.md) and [executor protocol](plans/EXECUTOR_PROTOCOL.md) — methods and rejection rules.
- [USA canonical proof](results/combined.json), [USA function inventory](results/inventory.json), and [Japanese region metadata](regions/japan_0.json) — region-aware provenance.
- [Historical research and prior status notes](history/README_20261118.md) — original pre-cleanup decomp README, retained intact apart from path-relative link adjustment.
- [Root project progress log](../PROGRESS.md) — dated acceptance history, not a live-only status page.

## Original-ROM verification requirements

A full-G2 promotion requires the original authenticated regional ROM, pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, IDO 5.3 and the regional original-address build. Host tests and isolated IDO matches alone do not establish matching C. Keep ROMs, original assembly dumps, compiler binaries, linked ELF/object files and save data out of Git.

`python3 -m decomp.local_ci` runs the ROM-free regressions; **it does not substitute** for a fresh full-ROM G2 verification. Follow [CONTINUE.md](CONTINUE.md) for region-specific staging and actual verification commands.

## Preserved history

The original README contained 18 November checkpoint notes claiming 987, 966 and 951 USA functions as the then-current state. Those dated findings remain in [the archived original](history/README_20261118.md), not at the top of the live onboarding documentation. The old five/ten/twenty-action plans are separately marked as completed historical records and remain at their original paths to avoid breaking existing research links.
