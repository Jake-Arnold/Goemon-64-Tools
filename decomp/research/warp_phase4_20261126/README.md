# Warp reconstruction Phase 4 — exit dispatcher research

**FAILED_NATIVE / RESEARCH_ONLY — neither target promoted.**

Base `stable/decomp@8b195d8ce5a31723a71af428ee4f7bccf32b0bf8`, source archive artifact 15142908886 (outer SHA256 3b519656c4acb56a035483abb0072cfda35845058ff65c91e26637ed4239eb7f, inner checksum and COMMIT.txt verified), pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Both retail and decompressed regional hashes verified, IDO 5.3 SHA256 `76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0`. Original Splat-generated function slices independently assembled and linked to both original ROM bytes at their real VMA, not generated from native candidate objects.

| Region | Name | Size | Best |
|---|---|---:|---:|
| USA | func_80215230_5D0700 | 256 | 61/64 |
| Japan | func_80219FC0_5D5550 | 256 | 61/64 |

Historical plan reported 17/64; the old source was unavailable in the inspected PR #279 paths. New reconstructed aggregate-copy baseline 12/64 (260-byte extent, 0x30 frame); scalar `u32` word copy followed by byte alias reads restores 256-byte extent, 0x28 frame, all 24 named relocations including addends and 61/64 original linked instruction words in each region. Existing typed-local and stack-layout sensitivity reproduced, not a new universal compiler law. The eight distinct source variants per region are retained; baseline plus seven allowed attempts (five + two after measured first-mismatch improvement). All 16 compiled and linked, none exact. Some variants were repeated during staged exploration; the retained final sweep is the 16 distinct variants. Operand reversal, physical-line grouping, their combination, direct early-return guard, explicit system reload and explicit nibble local do not improve upon 61/64. No native instruction/relocation patches or comparator relaxation. Preserve ASM.

Remaining mismatches at +0xB0/+0xB4 (original task reload precedes address calculation; candidate swaps scheduling) and +0xD4 (branch not-equal source operands reversed). First original linked word 8fa40028 vs candidate 002c0821 in both regions. These are codegen mismatches, not an original-address match. See `native-results.json` for every source hash, exact compiler flags, first mismatch and relocation/extent result. Suggested next bounded hypothesis: original expression/temporary lifetime for store to system+CF894 before decoder, and signed/unsigned operand representation in low-nibble direct condition; don't repeat the exact same variants.

## Interface recovery

First argument is the task pointer. Second is an object pointer forwarded unchanged to the collision checker (callee uses coordinate fields at offsets +8/+C/+10). Dispatcher reads task+0xD8 as a word and uses byte +2 of its local representation. Eligibility byte system+CF898 must be nonzero and system+3AE29 zero. For kind >=17, require a nonnull player object and collision helper return 0x7FFF with upper nibble of the byte as third argument; set player flags+0x22 bit 4, call the preparatory callback, reload global system and player object, save that object at system+CF894, decode task and register the adjacent callback. For kind <17, direct decoding and registration occur only when low nibble equals kind. Symbol meanings remain provisional. No runtime gameplay claim.

## Tests and replay

`./test_host.sh` uses GCC ASan/UBSan on the actual best source from each region: 32,768 synthetic cases per region, including eligibility, nibble masking, nonnull checks, collision success/failure, callback order and mutable globals. The host fixture deliberately aligns the 64-bit host pointer store and seeds the word's byte representation. It is not an N64 gameplay test. `python3 validate_checkpoint.py` validates source/evidence consistency only. Canonical USA promotion-integrity and JP Batch A validator passed unchanged (3066/3004 C). Pending manifests #250, #200, #194, #202 checked for exact identity strings with no overlaps; #279 references these targets but has no candidate C bodies for them. Not exhaustive across all historical pending manifests. Both canonical inventories have no target name or in-range claim start. Full candidate G2, owner match, strict candidate inventory and promotion integrity NOT_RUN because the source is nonmatching.

To reproduce native research, use the authenticated canonical source at the base above, the pinned original upstream checkout with private original regional ROMs and Splat extraction, and the project dependency/runtime archives. Configure `PATH`, `PYTHONHOME`, `PYTHONPATH` (including the authenticated repository) and `LD_LIBRARY_PATH` as in GOEMON_BUILD_ENVIRONMENT.md. Run:

```
python probe.py --repo AUTHENTICATED_REPO --usa PINNED_USA --jp PINNED_JP --work NEW_ABSOLUTE_WORK_DIR
```

No original ROM, original ASM, toolchain, extracted asset or compiled binary is shipped. `generate.py` contains the symbol map used to derive equivalent JP sources. No change to toolkit. Phase 2/3 PRs #283/#284 have passed hosted regression but remain unpromoted; Batch B is separately outstanding.
