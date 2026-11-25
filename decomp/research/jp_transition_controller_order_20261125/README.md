# Japanese transition controller-input handlers — 2026-11-25

RESEARCH_ONLY. Live stable/decomp 3669a15a807c77249e85cd177ef2704d5560e5d1, source archive 15066045901 COMMIT and SHA256SUMS checked in a fresh extraction; pinned upstream tracked-clean 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee, original Japanese ROM and IDO 5.3 hashes checked. Stored canonical JP2843 integrity passes, stable post-merge CI 45706409273 success. No overlap with canonical ownership or pending PR250 candidates. No promotion requested.

## Native evidence

- 34D8 (VMA 800028D8, 352 bytes) and 381C (VMA 80002C1C, 280 bytes) are both exact with named `controller[0].button_pressed | controller[1].button_pressed`. Baseline raw-offset operands 3B094 then 3B07C generated loads in the opposite order to the original (86/88 and 68/70 words; same size, all 21/15 genuine relocations). Swapping the raw operands alone produces exact bytes and relocations independently in both functions; replacing them with genuine upstream named fields preserves exact output. First mismatches +0xC8 and +0xA0, original first loads controller 1. NEW_REPRODUCIBLE_QUIRK, narrow observed operand-order sensitivity rather than a C-language sequencing guarantee. Controller input fixture tests both slots and signed disable gate, callback pointer reloading, byte overflow and state transitions.
- Independent entire inferred original main_2BE0 text owner, named ASM and numeric ASM shadow plus mixed candidate: 6,416 bytes exact in all three, 38 positive FUNC identities exact, named original 625 relocations; converting only the 16 synthetic small D_3ADF2/D_3ADD6/D_3ADD5 offset records for the two new C functions independently in original ASM yields 609/609 exact relocation tuples. No native instruction or relocation patch. This is not a canonical mixed-source full ROM proof.
- 2F0C baseline 51/58 (232 B, 12/13 refs), 2FF4 baseline 44/49 (196 B, 20/20 refs), first mismatch +0x54 and +0x34 respectively, original countdown v1 vs generated v0. Five declaration/selector controls each and five independent loop topology/post-loop reuse controls each fail to improve. 3658 previous 92/113 (452 B, 30/31 refs) reproduced from PR227; five word-state controls, including explicit reload and word countdown reuse, no higher total; word-state countdown first mismatch +0xC but 76/113 overall. No further compiler finding; preserve ASM. 3C90 not reattempted. Historical callback declarations remain hypotheses outside observed native ABI.
- 34 final native source replays, 68 GCC/Clang ASan/UBSan builds, 36,811,776 actual-source fixture executions pass. No full candidate G2/strict inventory or candidate hosted CI/gameplay. JP2843 and USA2939 unchanged; cumulative research-only exact 3984/3A10 (previous PR266) and 34D8/381C total four functions, 912 bytes. Next target remaining independent transition handlers or countdown allocation, without promoting until requested.

## Replay

Use the authenticated source checkout, private pinned upstream with original Japanese ROM and Splat extraction and original private toolchain. Set MIPS tools PATH and runtime LD_LIBRARY_PATH according to GOEMON_BUILD_ENVIRONMENT.md. Run with separate nonexistent output directories:

```sh
python3 replay.py --repo "$REPO" --upstream "$UPSTREAM" --out "$WORK/native"
python3 check_owner.py --repo "$REPO" --upstream "$UPSTREAM" --out "$WORK/owner"
bash test_host.sh
```

Each variant evidence JSON includes flags, first mismatches, source and linked hashes, exact relocation tuple counts, classification. Generated original ASM, ROMs, objects, binaries and proprietary toolchain are excluded. The local source-only kit contains all replay scripts and fixtures. No native code or relocation records were patched.
