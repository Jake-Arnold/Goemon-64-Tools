# Next 20 steps — verified matching-C integration and remaining four functions

**Execution plan, not a completion claim.** Prepared from the live `chatgptweb/decomp` branch at `b1a519e01e3fb4184ae0ce441202883a60b1230a`, after both isolated matching-research waves. This is the active runbook for the next stretch of Goemon-64 matching-C work, while `NEXT_TEN_MAIN_SEGMENT.md`, the two wave research JSON files and `PROGRESS.md` remain historical evidence.

## Starting state and nonnegotiable proof boundaries

- **Live verified:** 142 reconstructed matching-C function claims (141 new C plus one reviewed upstream patch); 10,652 exact original MIPS bytes, 155 combined upstream+reconstructed C, 7,221 ASM out of 7,376 identified. Current `results/combined.json` records **142/142 exact original-address checks, 33,554,432/33,554,432 original decompressed ROM bytes identical and `formal_verifier_run_completed=true`**. This applies to the already integrated 142 functions, not to the next six candidates.
- **Available but NOT promoted:** original-address isolated IDO+ld.lld exact links of `func_80034ED4_35AD4` (36), `func_80034F20_35B20` (36), `func_80035094_35C94` (48), `func_80011B60_12760` (84), `func_80011BB4_127B4` (80) and `func_80011C04_12804` (84). **Six functions / 368 isolated matching MIPS bytes**, no whole-project integration yet.
- **Four previously investigated but nonmatching:** `func_8003A1E8_3ADE8` (28), `func_80006274_6E74` (36), `func_80001D94_2994` (44), `func_80001DC0_29C0` (52). These are the remaining 160 bytes in the ten-function main-segment batch.
- **Source context verified:** resource wrappers share `resource_dispatch.c` around an existing C function; object dispatcher belongs to `object_dispatch.c`; menu trio and 8-byte existing hook are in `empty_menu_hook.c`. Integrating isolated candidates into the **actual translation units** may change compiler output, relocations, sections or padding. Recheck all before promotion.
- **Production acceptance gate on every proposed promotion:** exact original-address instructions and relocations, pinned native IDO source ownership in the correct translation unit, **complete 2,331-object linked ROM 33,554,432-byte identity** to SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, all previously matching functions intact, readelf symbol/section and full inventory identity, verified current manifest and proof source hashes. Isolated matches and host tests never substitute. Original/compiled ASM, private ROM, tools, saves, and raw diagnostics must not be committed.

## I. Baseline proof and six-candidate replay

1. **Freeze the live branch baseline.** Re-fetch `chatgptweb/decomp` and its current `AGENTS.md`, `CONTINUE.md`, manifest, proof, inventory and source files. Confirm all six candidates are *still* assembly placeholders and the formal 142-function proof is intact; do not merge or modify `main`.

   **Pass gate:** Record HEAD/source hashes and 142/10,652/7,221 counts; abort a stale plan if any target was promoted meanwhile.

2. **Validate pinned input and build environment.** Use the verified retail USA ROM SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`, 32 MiB decompressed reference SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, Splat 0.36.3, IDO 5.3 and pinned MIPS binutils. Create a fresh isolated workdir and preserve prior reports.

   **Pass gate:** Correct hashes, compiler paths and cache provenance; no archived 136-function source substituted for current 142-function checkout.

3. **Reproduce the current 142-function full-ROM checkpoint.** Run the current Linux and relevant Python verification suites, followed by one clean `python3 -m decomp.verify` and `decomp.inventory` using the runbook's fresh-path commands. Check the actual report's source/manifest hashes and exact image identity.

   **Pass gate:** 142/142 original function addresses and 33,554,432/33,554,432 reference ROM bytes identical, with inventory 155 C / 7,221 ASM; otherwise fix baseline before any promotion.

4. **Replay all six isolated matching proofs.** Run `python -m decomp.prove_three_wrappers` and `python -m decomp.prove_three_menu_flags` with private ROM, pinned native IDO `-c`, linker, objcopy and readelf. Execute the focused negative tests and the two GCC sanitizer host suites.

   **Pass gate:** Exactly 36+36+48+84+80+84 = **368 linked original bytes** and six correct ELF symbol sizes/VMAs; retain failures without editing compiled machine-code bytes.

## II. Resource/object integration and exact first-wave gate

5. **Audit original-unit ABI and layout before staging.** Review original source units `resource_dispatch.c`, `object_dispatch.c`, `empty_menu_hook.c`, their Splat splits, `asm_no_padding`, current header types, real symbol visibility and cross-unit call addresses. Plan shared struct declarations for menu routines, preserving original source-function order.

   **Pass gate:** No duplicate type names, missing callback prototypes, reordered functions or unreviewed section/rodata changes; stage changes in temporary checkout only.

6. **Stage resource wrapper ED4 in its original C unit.** Replace only `func_80034ED4_35AD4`'s `GLOBAL_ASM` with the typed C from `candidates/resource_wrapper_ed4.c`, preserving the existing `func_80034EF8_35AF8` between the wrappers. Compile as part of the **actual** `resource_dispatch.c` translation unit.

   **Pass gate:** Original 36-byte function code and `0x80034ED4` address reproduced under the production compile; if not, keep standalone candidate unpromoted.

7. **Stage resource wrapper F20 in the same unit.** Replace only `func_80034F20_35B20`'s pragma using `candidates/resource_wrapper_f20.c`; keep its distinct callee `func_80034F44_35B44`. Build the combined production unit with both wrapper functions and the already matching middle function.

   **Pass gate:** Both wrapper code extents remain exact and noncontiguous at ROM `0x35AD4` and `0x35B20`; the intervening `func_80034EF8_35AF8` stays unchanged.

8. **Run full project ROM gate for the resource unit.** Stage exact manifest ownership/removal of two ASM entries in the temporary tree, build all **2,331 objects**, verify each promoted function at its original address, check the entire output image and readelf inventory; run focused resource callback tests.

   **Pass gate:** Only if full ROM equals pinned 32 MiB and all existing claims survive may two functions be promoted (**144 C / 10,724 bytes**). On mismatch stop and preserve a non-promoted research diff.

9. **Stage object dispatcher C94 in its original translation unit.** Replace the `object_dispatch.c` pragma with `candidates/object_dispatch_c94.c`. Keep the preexisting `func_80035064_35C64` and its old callback target intact. Preserve the new function's saved actor across its first call and the target `func_800350C4_35CC4` on the second.

   **Pass gate:** Actual unit compile has the correct `func_80035094_35C94` symbol (48 bytes) and exact call relocations; no unreviewed changes to the sibling function.

10. **Verify and, if exact, promote the first wave.** Run full current-source compile/link, ROM SHA/byte comparison, all old+new function comparisons, manifest uniqueness/source ownership and inventory after the object wrapper is staged. Rerun the 30,000-case host harness and relevant Python tests.

   **Pass gate:** Conditional first-wave milestone: **145 matching C, 10,772 MIPS bytes, 158 combined C, 7,218 ASM**. Update proof and record an atomic verified commit only if full gates pass.

## III. Menu translation-unit integration

11. **Prepare the three-function menu type model.** Merge the three standalone menu candidates into the existing `empty_menu_hook.c` context, keeping one consistent set of `MenuPanel`, `MenuOptions`, `MenuBit` and nested-pointer declarations. Verify offsets `+0x22`, `+0x64`, `+0x4`, `+0x18` and global identifiers.

   **Pass gate:** The original empty hook stays 8 bytes; no duplicate C typedefs or compiler alias assumptions silently change existing symbol sizes.

12. **Integrate menu enable B60.** Replace only `func_80011B60_12760` with `candidates/menu_enable_b60.c` logic. Preserve double global-pointer guards, setting bits `0x14`, `0x80` and byte `+0x64 = 1` plus original load order.

   **Pass gate:** Exact 84-byte function under the production translation-unit IDO compiler, original VMA/ROM position; retain assembly if compilation reorders instructions.

13. **Integrate menu disable BB4.** Stage `func_80011BB4_127B4` immediately after the enable function. Preserve the **explicit `0xFF7F` mask** that produced the original `andi` instruction, and the two-pointer guard semantics.

   **Pass gate:** Exact 80-byte native instruction layout and unchanged preceding 84-byte function; check byte and halfword masks with synthetic tests.

14. **Integrate nested menu updater C04.** Stage `func_80011C04_12804` last. Preserve the original nested pointer dereferences without an unnecessary cached local that previously changed `$a0/$a1` allocation. Keep the sibling menu functions' source order.

   **Pass gate:** Exact 84-byte original function symbol and no codegen regressions for the other two or the existing 8-byte hook.

15. **Prove complete-ROM identity with all three menu replacements.** Stage precise manifest `functions` additions and `assembly_functions` removals, then run the **uninterrupted** current-source full ROM verifier and inventory on a fresh workdir. Validate every source hash and all existing main-segment functions.

   **Pass gate:** If all six first/second-wave replacements pass, conditional checkpoint: **148 matching C / 11,020 exact MIPS bytes / 161 combined C / 7,215 ASM**. Otherwise promote only the fully proven subset, reverting unverified C stages.

## IV. Verification, remaining four targets and batch closure

16. **Audit and publish the six-function milestone.** Run the fixed MIPS comparison and manifest consistency tests, both focused C host harnesses, ELF/layout and pipeline tests, and application tests affected by source/verification changes. Review full ROM and inventory report metadata; keep old reports immutable.

   **Pass gate:** Update `PROGRESS.md`, `CONTINUE.md`, manifest/results with evidence, commit and non-force push only independently proven production changes. Any zero-promotion blocker receives an explicit report, not inflated counts.

17. **Retry the 28-byte engine reset.** Revisit `func_8003A1E8_3ADE8` in `engine_state.c`; analyze the original two global writes and the previously incorrect native IDO 20-byte/28-byte variants. Test declaration type, alias and immediate register scheduling one at a time.

   **Pass gate:** Original 28-byte machine instructions *and* 32 MiB production ROM gate; otherwise record the strongest mismatching words and move on.

18. **Retry the 36-byte state-field writer.** Investigate `func_80006274_6E74` in `state_predicate.c`, preserving the original halfword/word widths, base adjustments and argument spill. Test the ABI-spill reason the earlier native source emitted only 28 bytes.

   **Pass gate:** Original 36-byte address-bound machine code and whole-ROM/inventory verification before adding to the matching count.

19. **Retry the 44-byte file-table lookup.** Rebuild `func_80001D94_2994` in `file_table.c`, referencing sibling `func_80001D68_2968` but preserving the different table base and repeated `0x7FFFFFFF` masking. Fix the historical same-size/different-register instruction scheduling.

   **Pass gate:** All original 44 bytes exact in the real unit, then the full-ROM promotion gate; a correct 44-byte size alone is not a match.

20. **Retry the 52-byte file-size function and close the batch.** Reconstruct `func_80001DC0_29C0` with the original zero-input branch and late-return instruction scheduling, unsigned table-field subtraction and delay-slot semantics. Then rerun focused tests and a complete ROM/inventory verification for any newly integrated function and publish a final **20-step status ledger**.

   **Pass gate:** Only ROM-verified functions change totals. Stretch result **152 C / 11,180 exact bytes / 165 combined C / 7,211 ASM** if all ten have passed; otherwise preserve blockers and carry forward unpromoted ASM.

## Handling blockers and commits

- The 20 steps are **ordered work units, not guaranteed promotions or a commitment to patch machine-code bytes**. If an integration changes another function, fails Splat splitting, padding or the whole-ROM comparison, **do not commit the failing production replacement or update manifest counts**. Preserve a separate research-only C candidate and exact mismatch evidence, and advance to the next independent unit.
- Keep original assembler for every unpromoted function and maintain exact source-function order. Fix C declarations/aliases/control flow, not the ROM, the linker output, comparison masks or byte patches. Original link and branch-delay accuracy matter more than matching function length.
- Update root `PROGRESS.md` in every code/documentation commit with what actually ran, source/tool hashes and what remains unverified. Use only `chatgptweb/decomp`; check remote HEAD immediately before non-force push and independently verify the resulting remote SHA. Do not modify `main` or unrelated speedrun features.
- If all six already isolated-matching functions promote, conditional 148-function milestone applies; if the last four also match and promote, conditional 152-function milestone applies. **Neither is a verified outcome today.** Existing completed 142-function formal proof is not retrospectively evidence for changes introduced after that proof.

## Minimal commands and evidence pointers

- Formal full gate, inventory, pinned paths and focused pipeline test commands: `decomp/CONTINUE.md` §5. Always use a fresh output workdir and report path.
- Existing original-address research reproducers: `decomp/prove_three_wrappers.py` and `decomp/prove_three_menu_flags.py`. Strict symbol-size/address and SHA-pinned original ROM comparison, but **not** a complete project link.
- Host regression harnesses: `decomp/test_three_dispatch_wrappers.c` (30,000 synthetic cases) and `decomp/test_three_menu_flags.c` (90,000 synthetic cases); supporting negative tests `decomp/test_prove_three_wrappers.py`. Historical results are not an automatic pass on a new source state.
- Original candidate evidence: `decomp/results/next_ten_main_wave1.json`, `decomp/results/next_ten_main_wave2.json`, and `decomp/NEXT_TEN_MAIN_SEGMENT.md`. Preserve old proof JSONs rather than overwriting their source identifiers.
