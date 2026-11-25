# Japanese 3C90 scoped-pointer lifetime controls — 25 November 2026

RESEARCH_ONLY. Authenticated stable/decomp `3669a15a807c77249e85cd177ef2704d5560e5d1`, archive 15066045901 (COMMIT.txt and SHA256SUMS verified). Original pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, tracked-clean, original expanded Japanese ROM SHA1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, retail `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`, IDO5.3 cc SHA256 `76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0`. Original compiler ledger SHA256 `3334338e458e5d04f91e613249ecec1ee857acb450821409ef33784c1a7c6f46`.

Hypothesis: block-scoped pointer or countdown lifetime may preserve direct INC while changing the global pointer allocation from v0 to v1. Five variants tested with the direct and best explicit-mask controls. All five reproduce the direct control's 88/111, original 444-byte extent, 35/36 reference relocation tuples, 36 generated, first mismatch +0 (original LUI v1, generated LUI v0). Best explicit-mask control reproduces 108/111, 36/36, 444 bytes, first mismatch +0x7C (address construction t7 versus v0). The five new variants have identical diagnostic load, mask and add register tuples to the direct control. Seven ordinary and seven diagnostic builds agree; fourteen GCC/Clang ASan/UBSan runs (1,835,008 actual-source fixture cases) pass. NO_NEW_COMPILER_FINDING for new variants; EXISTING_QUIRK_REPRODUCED for best control. No whole-owner or full canonical G2 for unchanged/nonexact hashes, no ownership delta. Scope/`register` declaration alone is not sufficient for this function. Budget exhausted; avoid additional equivalent direct spelling trials. No original binaries, ROM, compiler, generated ASM or raw trace included.

With the pinned clean upstream and original Japanese Splat extraction already prepared, native toolchain paths set, and current authenticated repository archive in REPO:

```bash
python3 replay.py --repo "$REPO" --upstream "$PRISTINE" --out "$WORK/native"
python3 diagnostics.py --repo "$REPO" --upstream "$PRISTINE" --normal "$WORK/native" --out "$WORK/diagnostics"
bash test_host.sh
```

The native output directories must be fresh and private. Original compiler flags and per-source SHA256 values are in evidence JSON. Scripts derive the independently assembled numeric-offset reference from the authenticated original extraction. No compiler or verification gate was modified.
