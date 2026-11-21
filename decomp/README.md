# Goemon 64 — matching-C decompilation

**Operational entrypoint:** [CONTINUE.md](CONTINUE.md) and the live `chatgptweb/decomp` branch. This track is separate from the toolkit on `main`. Do not merge decomp-only changes into `main`.

## Latest verified results — 21 November 2026

The most recent **published, full original-ROM G2** report records:

| Region | Newly matching C functions | Original instruction bytes recovered | ASM functions remaining |
| --- | ---: | ---: | ---: |
| USA | **1,958** | **84,292** | **5,405** |
| Japan rev-0 | **2,121** | **112,244** | **5,255** |

Each region has **7,376 original positive-sized ELF function entries**. These figures are region-specific; do not add USA and Japan counts or count original upstream-C functions as new reconstructions.

The latest five-function batch is [documented here](docs/GOEMON_START5_G2_PROMOTION_20261121.md) and [published with independent remote re-verification](../PROGRESS.md). Both rebuilt expanded 32 MiB ROMs match **33,554,432 / 33,554,432 original bytes**, preserving original ELF function identities and all semantic relocations. The native G2 tier proves code/layout equivalence, **not** emulator gameplay or Bomb Text Skip success.

**Snapshot caveat:** The checked-in canonical USA [combined proof](results/combined.json) and [inventory](results/inventory.json) still represent the earlier **1,956-function** stage. The later **1,958-function** published G2 acceptance is separately recorded in [the five-function ledger](results/glitch_start5_2121jp_1958usa_g2_20261121.json). Do not edit a proof JSON or inventory count without a fresh authentic rebuild. See [INVENTORY.md](INVENTORY.md) for the arithmetic and provenance boundaries.

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
