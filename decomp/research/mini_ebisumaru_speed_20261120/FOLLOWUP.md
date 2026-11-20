# Mini Ebisumaru speed follow-up: native selector and movement clamp

Date: 2026-11-20. STATUS: RESEARCH_ONLY / FAILED_NATIVE. No production matching-C promotion.

## Selector

Original function func_801E1C90_59DBA0: USA ROM offset 0x59DBA0, VMA 0x801E1C90, 384 original bytes. Eight bounded original IDO 5.3 source variants compiled using the pinned mnsg flags. The best structural candidate (speed_selector_nearmatch.c) generated a 384-byte text section including trailing zero padding but DOES NOT MATCH the original function: 12 non-relocation instruction words differ. The first non-relocation mismatch is original PC 0x801E1CEC (local +0x5C): expected 0x45010044, generated 0x45010043. Two zero-argument instructions are move instead of original addiu, and the switch-default epilogue is four bytes shorter. Candidate jump table is compiler-emitted .rodata; no original owner/address/relocation proof. Not exact; do not promote.

## Clamp

Original function func_801CD310_589220: USA ROM 0x589220, VMA 0x801CD310, 4320 bytes. Bundled m2c initially fails with AssertionError: jtbl list must not be empty. Its 18-entry jump table has five distinct destinations, stored as raw numeric .word targets. Running m2c_jump_table_labels.py on a CLEAN original mnsg checkout writes scratch-only symbolic ASM/data input copies. The same m2c then emits a complete 565-line C-like draft (unverified). This draft does not yet pass C source-check: missing NULL, wrong inferred callback arities and invalid float/pointer conversions. It is not native exact and has no full-ROM replacement proof.

## Reproduction

Run: python m2c_jump_table_labels.py --upstream /path/to/mnsg --out /tmp/mini-m2c

Then, from the pinned mnsg checkout, invoke:
python tools/m2c/m2c.py --valid-syntax -f func_801CD310_589220 /tmp/mini-m2c/file11_symbolic_m2c.s /tmp/mini-m2c/file11_data_symbolic_m2c.s

Original assembly and ROM are never modified. The machine-generated C draft and complete research report are available in the session's separately generated research ZIP; do not mistake that draft for matching C.

## Acceptance state

Canonical USA total before and after: 1723 original-address C functions, 5640 remaining assembly entries. Original full-USA baseline and the two previously exact speed functions remain unchanged. No fresh full combined decomp.verify, decomp.inventory, decomp.local_ci, or in-game tests ran. This PR must stay draft until all existing 1723 C functions are integrated with any new candidate and the complete original-ROM gate and full local CI pass. No original ROM/ASM, binaries, objects, extracted assets, or toolchains committed.
