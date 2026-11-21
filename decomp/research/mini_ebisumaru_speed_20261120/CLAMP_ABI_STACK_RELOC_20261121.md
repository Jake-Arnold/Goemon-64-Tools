# 21 November 2026 — clamp ABI, floating-zero register lifetime and original global relocation reconciliation

**FAILED_NATIVE / RESEARCH_ONLY. No matching-C promotion.** Target original USA `func_801CD310_589220`, ROM `0x589220`, guest VMA `0x801CD310`, original length **4,320 bytes**. Pinned original IDO 5.3, upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Original retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`, original 32 MiB baseline rebuild SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; independent read-only original-vs-baseline byte comparison PASS.

## Register allocation: removed saved `$f20` without volatile

After the previous 4,200-byte candidate, a bounded source comparison confirmed IDO 5.3 makes different FP register lifetime choices when selected `0.0f` constants are spelled integer `0` in an existing float-typed context. This keeps numeric floating-point zero but eliminates the compiler's saved `$f20`. Native stack frame falls **448 → 440 bytes**, original **232 bytes**. **Two candidates generate exactly a 4,320-byte ELF FUNC**, one by changing the final 26 zero expressions, another by changing the first 16. Both are **NOT matching C**; exact code length alone is insufficient. The strongest size-exact candidate preserves the original 18-entry jump table at the same relative target offsets, 33 function calls in the original order, nine inline `sqrt.s` and 101 text relocation records.

## Original MIPS interface discoveries (source-proven)

- `func_801CEAD4_58A9E4`: its original entry immediately overwrites `$a2` with `$a1`, before any use of the incoming third argument. The previous three-argument research prototype was misleading. A two-argument C call restores the **original `beql` and `lw $t9,0x5C($a3)` delay slot** in the clamp early-return block, avoiding gratuitous `mfc1` and `mov.s` instructions.
- `func_801E7DE8_5A3CF8`: original Mini-state predicate uses the player task pointer in `$a0` only. The old three-argument float/float/task prototype was wrong. It is now called as `func_801E7DE8(arg0)`, matching the original call-site ABI and reducing native register-preparation work.
- The corrected ABI variant with selected zero expressions and all original `D_` extern globals compiles to **4,316-byte ELF FUNC**, **four bytes shorter** than original. It retains 33 original calls, nine `sqrt.s`, 18 jump-table case groups, 101 relocation records and **no saved `$f20`**. Its original-relative jump destinations are uniformly shifted four bytes. Several identical original-address contiguous instruction runs are observed (24 B at `+0x3A8`, 20 B at `+0x54`). Complete code still differs.

## Exact relocation symbol/type inventory (not just counts)

The m2c draft had declared original game constants as `static` initialized values, causing IDO to emit `.data` relocation targets rather than original `D_8020...` global symbols. Changing 25 original FP constants plus two pointer globals `D_801FC604_5B8514` and `D_801FC60C_5B851C` to **extern declarations** leaves compiler function lengths unchanged and preserves original named relocation targets.

After these changes, independently comparing current native `.rel.text` against **only the original `.rel.file_11` 4,320-byte function range** yields **99/101 exact relocation records in original order by type and symbol**. Both remaining differences are the HI16/LO16 address pair for original **`jtbl_8020A85C_5C676C`**, currently bound to IDO-generated `.rodata`. Both candidates have the original 33 `R_MIPS_26`, 34 `R_MIPS_HI16` and 34 `R_MIPS_LO16` counts. Complete relocation position/linker and whole-ROM equality are **not** claimed.

## Trials, truth and handoff

Multiple fully native C variants tested: fixed-layout stack struct (worsened frame to 568), volatile-zero diagnostics (removed `$f20` but added memory operations and larger code), ordinary C zero-source alternatives, corrected helper prototypes, and original extern global declarations. Final candidates are ordinary C only and retain original IDO compiler flags; no inline MIPS or instruction patches. The 4,320-byte source is **size-only** and still retains misleading early helper ABI; the 4,316-byte source has the corrected ABI and is the preferred next candidate.

**Actually run this session:** IDO native C compiles, `readelf` function extents, MIPS objdump FP register/frame inspection, 101-entry relocation-order/type/symbol diff, read-only jump-table and call-order audit, original USA baseline SHA-1, packaged `replay.sh` from project inputs exit 0, Python syntax check on the scripts, ZIP integrity pass. Original 32 MiB image was not rebuilt afresh this turn; prior authentic baseline was rechecked byte-for-byte.

**NOT RUN / FAILED:** original-address full-function exact matching FAIL; current production combined `python3 -m decomp.verify`, `decomp.inventory`, full `decomp.local_ci`, emulator gameplay NOT RUN. No production C or manifest count changed; live checked USA inventory **1,956 C / 83,940 accepted instruction bytes / 5,407 remaining ASM**.

The reproducible 10-file research ZIP `GOEMON_CLAMP_ABI_RELOC_20261121.zip` in the conversation contains both full C candidates, native replay script, original ASM/ELF audit, symbol comparison, sanitized proof and trial ledger. No original ROM/ASM, proprietary toolchain or generated ELF/object was published. Next: reduce native stack 440 → 232, recover initial `$f0/$f12` lifetimes, and resolve the table code/relocation layout with the exact original function only if a native match exists.
