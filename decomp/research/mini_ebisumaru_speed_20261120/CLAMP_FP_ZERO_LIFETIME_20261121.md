# Goemon USA Mini clamp — native FP-zero lifetime and motion-argument audit

**21 November 2026. Research status: `FAILED_NATIVE / RESEARCH_ONLY`.**

Target: `func_801CD310_589220` (ROM `0x589220`, VMA `0x801CD310`, original **4,320 bytes**, `file_11`). This package contains rebuilt **C research only**, original-MIPS comparison tools and sanitized numerical results. It contains no ROM, original disassembly, ELF, object files, or compiler.

## Proven original-ROM and native compiler results

- Retail USA SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66` (PASS).
- Pinned upstream commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` and original **IDO 5.3** with `-O2 -mips2 -G 0 -non_shared`.
- Clean, *unchanged* upstream USA ROM rebuild: **33,554,432 / 33,554,432 bytes exact** against expanded original SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494` (PASS).
- Native C baseline `clamp_whole_original_scaffold.c`: 4,288 bytes, **232-byte frame**, 33 original calls, nine inline `sqrt.s`, 101 text relocations with **99/101 type-and-symbol identities** in order; **9/882** comparable original-offset nonrelocation words equal. Candidate **not** original-address exact.
- `clamp_motion_arg_split_nonmatching.c`: same length, frame and 9/882 instruction positions, but now emits the original incoming `mtc1 $a2,$f12` and `swc1 $f12,sp+0xF0` at the second helper-call delay slot. This is a source-level lifetime/ABI improvement even though the global original-position score remains unchanged, because earlier mismatches still displace those instructions by four bytes. C SHA-256 `138b0adc84ad2a90b8621e380f3102a8b27c3af94215c9c2b69cbd6576d5f80c`.
- First mismatch remains candidate `sdc1 $f20,sp+0x10` at `+0x04` instead of original `mtc1 $zero,$f0`. Original saves `$ra` at `sp+0x14`, candidate at `sp+0x1C`.
- Nine native source combinations tested, including literal-zero C syntax, a single volatile local and the corrected arg2 lifetime. Four- or twelve-byte whole-size movements are not acceptance. See `evidence.json` for every frame, extent and fixed-offset match count.

## Important quantitative discriminator

A decoder over the authenticated original **4,320-byte** function counts **58 distinct `mtc1 $zero,$fN` instructions** across **12 FP registers**. The 4,288-byte native C candidate has only **10** `mtc1 $zero,$fN` instructions, one of which initialises `$f20` at `+0x08` and remains live across most calls. The original instead reinitialises `$f16` 17 times and several other scratch FP registers independently. These were measured from actual instructions, not guessed from C text. `audit_clamp_zero_lifetime.py` reports names and relative offsets without disclosing original instruction words.

Changing later float zeros to integer zeros raised fixed-offset word matches from **9/882** to **16/890** and the same-offset relocation triples from 0 to 6, but retained `$f20`. Making the long-lived `pool_fp_2` volatile in combination raised these diagnostic scores to **23/897** and 9 relocation triples. **This is not a proven semantic or original-code improvement**: `volatile` is only a memory/code-generation probe, not reconstructed original C. Other literal variants changed the frame to 224 bytes or enlarged the function to 4,584 bytes. None removed the original first mismatch.

## Next reconstruction step

Treat the first-block float zero as a short-lived value and recover distinct later float-zero def/use chains from original MIPS, especially before/after calls and the original context gate `+0x1B4..+0x257`. Do **not** substitute non-equivalent arithmetic zero expressions or raw assembly. The existing stronger 4,320-byte/232-frame C candidate from the prior `GOEMON_CLAMP_VECTOR_RESTORE_20261121.zip` remains a better *instruction-matching* source if restored; it achieved 157/925 comparable original-position identities, but it is not part of this ZIP and is not a production match. Independently source-correct motion argument passing as above.

## Reproduction

Point `GOEMON_UPSTREAM`, `GOEMON_EXPANDED_ROM`, and `GOEMON_BASELINE_ELF` at the authenticated pinned upstream checkout, expanded original ROM and byte-exact baseline ELF. Make `mips-linux-gnu-objcopy`, `readelf` and the supplied IDO 5.3 runtime libraries available. Run `bash replay.sh` in this folder. It produces a fresh C object in a temporary directory, runs `audit_scaffold.py` and `audit_clamp_zero_lifetime.py` read-only, and runs three synthetic opcode-decoder unit tests. It does not stage C in any production ROM.

**Actual gates:** native compiler / baseline original ROM / isolated research audit PASS; full matching C FAIL; current canonical `decomp.verify`, strict inventory, full `decomp.local_ci` and emulator gameplay NOT RUN. Accepted USA remains **1,965 C / 84,648 instruction bytes / 5,398 ASM** from the latest independent G2 proof. No production promotion.