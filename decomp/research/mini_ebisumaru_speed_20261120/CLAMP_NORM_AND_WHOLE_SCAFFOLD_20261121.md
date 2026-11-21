# USA Mini movement clamp: independent whole-C scaffold and original-MIPS 3D/2D norm verification

**21 November 2026. Status: `FAILED_NATIVE / RESEARCH_ONLY`.** No C function promotion.

Original USA target `func_801CD310_589220` at ROM `0x589220`, VMA `0x801CD310`, original 4,320 bytes, `file_11`.

## Independent 3D and 2D MIPS evidence

The new `clamp_norm_microexec.py` reads and executes the **actual private original USA MIPS instructions** in two bounded arithmetic branches; the script embeds no original ROM words. It independently checks a float32-rounding C-like oracle, output memory, stack norm/factor at `sp+0xDC`, case-specific write order, branch-likely behaviour and context reload. The source validates the original ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494` and fails closed on selected opcode and branch signatures.

| Verified original block | Original function-relative range | Actual test cases | Cap active | Cap inactive |
| --- | --- | ---: | ---: | ---: |
| 3D x/y/z | `+0x988..+0x9EB` | **5,000 PASS** | 4,051 | 949 |
| 2D horizontal x/z | `+0xDC0..+0xE17` | **5,000 PASS** | 3,636 | 1,364 |

The original 3D computes float32 `sqrt((z*z)+((x*x)+(y*y)))`, and 2D computes `sqrt((z*z)+(x*x))`. When `cap < norm`, the original scales x/z (and y in 3D) by `cap/norm`; otherwise it keeps the sums. The 2D branch **always sets task+0x6C (y) to +0.0f** at its exit, even without a cap. Every tested path reloads the context pointer. NaNs, infinities and signed zeros were included; unordered comparisons never spuriously take the clamp branch. Single-precision intermediate rounding was enforced.

The previous context gate `+0x1B4..+0x257` also independently replayed **3,000/3,000 PASS**. This gives **13,000 executed bounded original-MIPS test cases** across three independent windows (3D, 2D and gate), not whole-function execution and not a native matching-C replacement.

## Regenerated whole-function C — native but not exact

The full previously stronger 4,320-byte-frame-exact research C is not committed in this PR: it was delivered in a prior conversation ZIP. Instead, m2c was rerun on the authenticated original `file_11` assembly and an independent 565-line C draft was corrected for task/motion helper ABIs, three-pointer vector transforms, 33 authentic calls, 9 `sqrt.s`, the explicit `0x9F` switch case, original external symbols, and four contiguous three-float vector backing stores. Bounded lexical nonoverlapping scalar/pointer pooling plus direct task/context reload recovered the genuine original **232-byte stack frame** in the new standalone source.

Native original IDO 5.3 `-O2 -mips2 -G 0 -non_shared` generated **4,288 bytes**, **32 short** of the original. All **33 original call relocs in order**, **9 inline square roots**, **101/101 in-function text relocations**, and **18 jump-table entries with identical five destination groups** were preserved. **99/101 exact type-and-symbol relocation records match in order**, with only the compiler-owned `.rodata` switch pair differing from the original named jump table. The C table targets are still 4–20 bytes displaced; no original-address relocation offsets match. Critically, **only 9/882** comparable nonrelocated same-offset MIPS instructions match. First mismatch `+0x04`: generated `$f20` save instead of the original `$f0` zero initialization; it also changes the prologue and stack slot assignment. **Seven pointer typing warnings remain.**

The independently regenerated C is a **portable resumption scaffold**, not an improvement over the previous unavailable original 4,320-byte/232-frame 157-word candidate. Source SHA-256 `e26d242f2ea4ac46b0c3ee303a2107f12009cef20af1764a45192a5f1c1bad82`. It is supplied with the original-ROM comparator, 10,000-case micro-executor, JSON evidence and read-only native replay in the conversation artifact `GOEMON_WHOLE_CLAMP_BLOCK_RECON_20261121.zip`. No ROM, extracted ASM, object, ELF, proprietary compiler, or disassembly bytes are in the artifact or GitHub evidence.

## Actually run
- User retail USA SHA-1 authenticated; pinned original USA rebuilt **33,554,432/33,554,432 exact**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Native IDO 5.3 complete reconstructed C compilation **PASS**, with 7 pointer warnings.
- Original ELF/text/relocation/jump-table native comparison **PASS for measured structure, FAIL full function**.
- Original bounded 3D/2D MIPS tests **10,000/10,000 PASS**. Context-gate micro-exec replay **3,000/3,000 PASS**.
- Clean ZIP extraction/recompile/audit/micro-exec replay **PASS** (reproduced 4,288-byte failed native result); Python syntax, ZIP integrity and SHA hashes verified.
- **NOT RUN:** experimental clamp linked into candidate ROM, current canonical combined `decomp.verify`, strict `decomp.inventory`, full `decomp.local_ci`, emulator gameplay.

## Next work

Recover the zero-value lifetime responsible for generated `$f20` save and original `$f0` startup, without chasing size alone. Confirm context-pointer aliasing and delay-slot memory accesses through the actual source CFG; then use the earlier stronger 4,320-byte/232-frame candidate if its standalone source becomes available. Keep original ASM and this PR draft. Official latest independent USA G2 is **1,965 C / 84,648 original instruction bytes / 5,398 ASM**; `combined.json` remains an older 1,956 snapshot.
