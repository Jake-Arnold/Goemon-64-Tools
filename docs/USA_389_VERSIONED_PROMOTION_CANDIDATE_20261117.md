# Original-USA 47-overlay source promotion: versioned 389-C candidate

**State:** fail-closed `decomp.overlay_crossregion47` stage applied on top of the live canonical **342 C**, native original-ROM acceptance passed. The *production* count stays **342** until the complete latest-source verifier, standalone inventory, and full local CI are green and the canonical proof files are regenerated.

## Native verification (17 November)

- Current baseline commit: `1961f1333e8a5007c3cf8df5dfa0d0ca5a0cea8b`, canonical **342 matching C / 17,568 original bytes**. The previous 315 C snapshot is historical.
- Additional **47 genuinely new C functions / 2,220 instruction bytes**, overlays file_12 (5), file_13 (15), file_14 (8), file_15 (2), file_17 (1), file_18 (9), file_19 (7). All 47 source SHA-256s, original ROM code hashes, original function names/sizes and 4-byte alignment are pinned in `decomp/research/jp_recomp_to_c/overlay47_promoted_manifest.json`. No functions overlap current 179-file_11/342-C production ownership.
- Independently reconstructed native 342 baseline: exact original USA 32 MiB ROM, linked ELF SHA-256 `bbd86a77d315072fcf1112819e80c7807fbbe1288a68ef7c4b4b87b5fd4b7002`.
- The new versioned adapter splits only original MIPS assembly text around the 47 source-owned original function spans. Zero-only C/ASM padding is trimmed after exact original checks and five unsplit overlays switch from object subalignment 16 to 4. Original nontext ASM references are removed **only after confirming they are empty**.
- Fresh adapter native result: ROM **33,554,432/33,554,432 bytes exact**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, native candidate linked ELF SHA-256 `949d6159726fec772c1c9d36d0dad68d4c842bae608c4a9ca5020a7395848b2f`. The original **7,376/7,376 positive-sized ELF function name/VMA/size identities** were preserved against 342; all seven semantic relocation tables matched the exact original (file_12 7,051; file_13 9,589; file_14 3,041; file_15 1,625; file_17 1,739; file_18 3,365; file_19 1,078). File_11 8,825 relocations were not touched by this stage.
- The new `decomp/test_overlay_crossregion47.py` covers six fixture/source/duplicate/wrong-ROM guardrails. Exact source/code matches against the original ROM require local user-owned ROM and may skip on ROM-free CI.
- The versioned `decomp.verify` integration requires its **unchanged 342-C original ROM gate to pass first** before splitting the 47 functions, then requires another 32 MiB original ROM, complete ELF and relocation pass before adding exactly 47 new C ownership rows. Unexpected preexisting C overlaps or an advanced canonical branch fail closed.

## Required gates before canonical 342 → 389

`python3 -m decomp.local_ci` from the *current* production-based checkout; full `python3 -m decomp.verify` native original-ROM proof using the versioned adapter and verified compiler; `python3 -m decomp.inventory` with all **389** C claims and all **7,376** original positive-sized function identities. Only with all three passing should `decomp/results/combined.json`, `decomp/results/inventory.json`, `decomp/CONTINUE.md` official count and `PROGRESS.md` be updated for canonical 389 and the PR merged. The research native proof is not a substitute for these official gates.

No original ROM, asset, original ASM, object, ELF, proprietary compiler, save, or credential may be committed.
