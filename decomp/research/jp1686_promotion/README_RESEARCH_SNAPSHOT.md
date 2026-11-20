# Goemon Japan-0 — Unified 1,688-C research batch

**Prepared 20 November 2026. Region `japan_0` only. Tier `ISOLATED_EXACT / RESEARCH_ONLY`.**

This is a **single source-and-evidence input for a future combined Japanese full-ROM promotion**. It does **not** change the canonical decompilation branch or claim that 1,688 functions have already passed regional G2.

## Scope and source evidence

| Origin | JP candidates | Original instruction bytes |
|---|---:|---:|
| Initial contiguous callback research | 15 | 440 |
| Nearby task/timer/lifecycle research | 17 | 784 |
| Outward 500-function search (new native-exact) | 23 | 1,208 |
| First novel matching-C search | 507 | 15,368 |
| Second novel matching-C search | 567 | 27,132 |
| Third novel matching-C search | 509 | 53,316 |
| Fourth novel matching-C search | 50 | 3,464 |
| **Unified total** | **1,688** | **101,712** |

**All 1,688** are unique by original ROM offset and function identifier, with disjoint byte ranges. Their source hashes match the original supplied archives; every original-instruction SHA-256 is recomputed directly from the user-supplied, SHA-1-authenticated expanded Japanese ROM. The original ROM has SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, 33,554,432 bytes. The normalized retail ROM has SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` (16 MiB).

The accepted Japan canon contained **432 functions** at the frozen original research snapshot. Its 432 ROM offsets were independently re-fetched and checked again against the live `chatgptweb/decomp` branch at `0e42cb3fbd2147eefa3ab469d8c22ff19b869831`; the accepted-set fingerprint is `fad6452e` (FNV-1a 32-bit over ascending comma-separated uppercase hexadecimal ROM offsets). **Zero canonical duplicates.** USA accepted totals and sources are unrelated to this package.

A fresh **unified native IDO 5.3 replay passed 1,688/1,688 complete functions, across 1,665 C compilations, 25,428/25,428 MIPS instructions / 101,712/101,712 instruction bytes**. Both original linked VMA and positive function extent were checked. The results are in `native_replay_summary.json`. This is stronger than merely concatenating the historical proofs, but still an isolated-function proof tier: no combined relocations were audited.

## Files

- `candidates.csv` is the **single authoritative manifest**: region, original VMA/ROM offset/size, original-code SHA-256, C-source SHA-256, exact source path, original Splat assembly owner and discovery batch. Never dedupe by function name alone or translate addresses from USA.
- `asm_owner_plan.json` groups all 1,688 functions into **153 original Japanese assembly owners**. This is the staging workplan: existing canonical JP432 replacement fragments **must** be reconciled with these original owners; an owner label is not a current linker object filename.
- `sources/` preserves all source bytes, including their original relative m2c compatibility headers and grouped task C units.
- `scripts/audit.py` checks source hashes, offsets, overlapping byte ranges, current frozen canon and optional original expanded-ROM SHA/code hashes.
- `scripts/canon_preflight.py` fail-closes against a changed JP canonical manifest, a dirty checkout, or the wrong branch.
- `scripts/native_replay.py` recompiles and links all functions at original VMAs using the original pinned IDO 5.3 and binutils, and compares them with the user-owned original ROM. It does not modify the repository.
- `evidence/` preserves original sanitized research reports/verifiers. None of these is a canonical G2 report.

The complete asset is independent of the source archives from which it was built; it does **not** contain the Japanese ROM, extracted raw ASM, objects, linked binaries, saves or compiler toolchain.

## Prepromotion verification: one batch

Unzip to a clean directory. Restore the private pinned Japan upstream/tools and original ROM per `GOEMON_BUILD_ENVIRONMENT.md`, giving workspace paths:

```
$WORK/mnsg-japan/config/japan_0/baserom.decompressed.z64
$WORK/mnsg-japan/tools/ido-5.3/cc
$WORK/goemon-dependencies/bin/mips-linux-gnu-ld
$WORK/goemon-runtime-additions/lib/
```

Run **the complete 1,688-function isolated gate in one invocation**:

```bash
python3 scripts/audit.py --rom "$WORK/mnsg-japan/config/japan_0/baserom.decompressed.z64"
python3 scripts/native_replay.py --work "$WORK" --workers 8
```

When working from an up-to-date, clean **canonical** checkout, also run:

```bash
python3 scripts/canon_preflight.py --repo "$CANON" \
  --rom "$WORK/mnsg-japan/config/japan_0/baserom.decompressed.z64"
```

The original build scripts can validate the **432-C baseline**, but they will not automatically integrate this new batch. A new, original-address, fail-closed **Japan-0 staging adapter is still required**; it must preserve the previous 432 promoted C functions, split all 153 source/ASM ownership units into new C and retained ASM portions, and update the regional linker/object manifests without using USA code or introducing unrelated symbols. Do **not** treat the combined source ZIP as an already buildable, staged Japan ROM.

## One future combined full-ROM promotion gate (not yet run)

The future promotion should be attempted **as one transactional batch against one frozen canonical HEAD**, not four research batches or 1,688 separate branch commits:

1. Re-fetch the live `chatgptweb/decomp` HEAD; require clean checkout; run `canon_preflight.py` and any necessary new-canon deduplication. Freeze source hashes, owner units and the exact original-ROM SHA-1. Stop if any existing accepted entry overlaps.
2. Stage **all 1,688 functions together** with an adapter that preserves all old JP432 functions, correct original translation-unit ownership, all ASM gaps, native symbols, overlay mappings and original relocations. Fail on duplicates, invalid relocation identities, out-of-bounds sections or symbol collisions. Keep original ASM for any invalid unit rather than falsely accepting it.
3. Compile the entire staged Japan-0 codebase using the original IDO build system, compare the **entire 33,554,432-byte expanded ROM** to the original (SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`) and the **entire normalized 16 MiB retail ROM** to SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` if supported by the existing Japan build. Require all **7,376 original ELF positive function identities**, original semantic relocations and 73 ELF sections to remain intact.
4. Run strict Japanese regional inventory and full `python3 -m decomp.local_ci` including ASan/UBSan. A byte-identical standalone candidate is not a complete-ROM pass. Do **not** disable warnings, source ownership checks or relocate calls to force an invalid match.
5. Only if every gate passes, update the Japan manifest, C stage adapters, original-address proof ledgers, strict inventory, `decomp/CONTINUE.md` and `PROGRESS.md` **in one commit**, then publish only to `chatgptweb/decomp` and verify remote HEAD. Otherwise stop without promoting anything and keep a report of original-address mismatches for repair.

**Theoretical only, if all 1,688 integrate and pass**: accepted Japan C would move from 432 to 2,120, original matched C instruction bytes from 10,408 to 112,120, and remaining original ASM entries from 6,944 to 5,256. These are **not** the current accepted metrics and must not appear in the canonical manifest until the entire G2/CI acceptance path passes.

## Important unresolved behavioural targets

The C-Right Japanese stage initializer `func_80212514_5CDAA4` and main scheduler `func_800343A4_34FA4` are **not included as exact candidates**. The former remains 69/99 original instructions; the latter is still ASM. Their research is not silently promoted with this batch.

The candidate set spans many engine subsystems beyond the glitch. A function count alone does not establish new knowledge of the C-Right condition, or correct inferred types for m2c placeholders. No emulator gameplay test is asserted.
