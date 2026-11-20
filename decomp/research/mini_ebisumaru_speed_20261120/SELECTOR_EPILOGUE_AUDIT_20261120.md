# Mini Ebisumaru selector: original jump-table and return-block audit (20 November 2026)

**FAILED_NATIVE / RESEARCH_ONLY.** No original-address matching C or formal promotion.

Target func_801E1C90_59DBA0 at ROM 0x59DBA0, VMA 0x801E1C90, 384 bytes (96 instructions). Original IDO 5.3 with -O2 -mips2 -G 0 -non_shared. USA pristine expanded ROM baseline byte-identical, SHA-1 6ea0ed71032ce08fc2745f412d84936382197494.

The best compiled source remains a **380-byte ELF FUNC symbol**, despite 384 bytes in .text after trailing alignment. It differs from the original at 12 non-relocation instruction words. New structural return, variable-lifetime, and argument-ABI tests did not improve this best count; other forms worsened to 36-64 differences.

## Verified new finding

The candidate's eight relocatable .rodata jump-table entry addends **exactly equal** the eight original ROM data-table branch destinations *relative to the original function*: 0x14C, 0x154, 0x15C, 0x164, 0x164, 0x164, 0x164, 0x164. The original table resides at 0x8020B2E0. The native candidate has nine .rel.text relocation sites and eight .rel.rodata entries. This is a structural source-to-original comparison; original data ownership and complete relocations are not verified.

## Remaining mismatch clusters

- Offset +0x5C: floating-point early-exit branch is one instruction shorter because of the epilogue.
- Offsets +0x88 and +0xA8: zero-argument encoding (original addiu, generated or).
- Offsets +0x14C, +0x154 and +0x15C: branch displacement points to earlier return epilogue.
- Offsets +0x164 through +0x178: original default emits an extra temporary register initialization before a branch and register move; IDO emits a direct load in its branch delay slot.

The next task is to recover a C-level default/return control-flow pattern that retains the 384-byte function symbol without modifying the already matching jump-table targets, then independently fix the two argument encodings. Do not use inline MIPS, manual instruction patches, or trailing alignment as evidence of C matching.

Research-only replay and structural auditor, which reads private Splat ASM locally and exports sanitized metadata only, are in the conversation artifact func_801E1C90_epilogue_next_step_2026-11-20.zip. No original ASM, ROM, object bytes or proprietary toolchain are committed.

Combined decomp.verify, inventory, full local_ci, and emulator gameplay NOT RUN; USA formally accepted C remains 1,723, with 5,640 ASM entries.
