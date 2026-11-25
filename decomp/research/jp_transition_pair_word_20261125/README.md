# JP transition pair word-local research — 2026-11-25

Status: RESEARCH_ONLY; no canonical ownership change. Authenticated stable/decomp 3669a15a807c77249e85cd177ef2704d5560e5d1, archive 15066045901; pinned pristine upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee. IDO 5.3 cc SHA256 76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0; retail JP SHA1 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b, expanded SHA1 6f8745fecc3a5e7d4918c7a73353eb0726116ded. Compiler ledger SHA256 at attempt 3334338e458e5d04f91e613249ecec1ee857acb450821409ef33784c1a7c6f46.

## Findings

- JP 3984 (VMA 80002D84) and 3A10 (VMA 80002E10), each 140 bytes: true named fields restore all nine symbolic relocations but an unsigned byte local gives 27/35 words (first mismatch +0, 3c03800c vs 3c04800c). Only replacing `u8 state` with `s32 state` produces all 35/35 words and all 9/9 original relocation tuples in both independently compiled functions. The matched field at offset 3ADB6 is `disable_graphics_tasks`. Generator diagnostics distinguish base xr4 vs xr3 and increment input xr3 vs xr2; final machine base a0 vs v1. This is a narrowly reproduced compiler allocation sensitivity, not a general assertion about word locals. NEW_REPRODUCIBLE_QUIRK for the two positive variants. Other source variants and previous alias controls remain in evidence.
- Independent original `main_2BE0` text owner: 6,416/6,416 bytes, 38/38 positive FUNC identities, 625/625 named object relocation tuples; candidate consists of two new C functions and 36 original ASM siblings. No instruction patch, relocation rewrite or synthetic alias. This is the original inferred text owner, not the current canonical full ROM or mixed ownership layout.
- JP 3C90: s16/s32/u32 countdown widths with explicit u8 narrowing are unchanged at 88/111 compared to direct control; u16 is worse (15/111, 448 bytes, 7/36 relocs). Widened masked control remains 108/111, 444 bytes, 36/36 relocs, first +0x7C (3c0f0004 vs 3c020004). The five variants exhaust this hypothesis's budget; no progress at first mismatch. Preserve assembly.
- Fresh 16 ordinary and 16 diagnostic native builds; 32 GCC/Clang ASan/UBSan builds, 1,927,168 actual-source fixture executions passed. Stored canonical JP2843 integrity passes; previous full post-merge CI passed. No fresh full canonical G2 or candidate CI, no gameplay verification. Canonical JP2843/USA2939 unchanged. Candidate increment +2 / +280 original bytes if full native promotion succeeds.

## Replay

Use a clean isolated private checkout at the pinned upstream, original authenticated ROM and original toolchain per repository AGENTS/CONTINUE and the build environment instructions. `--repo` is the authenticated Goemon-64-Tools source checkout, `--upstream` is the pinned upstream with private extracted original reference. Set the private MIPS toolchain PATH and runtime environment. Use separate, nonexistent output directories.

```
python replay.py --repo "$REPO" --upstream "$UPSTREAM" --out "$WORK/native"
python diagnostics.py --repo "$REPO" --upstream "$UPSTREAM" --normal "$WORK/native" --out "$WORK/diagnostics"
python check_owner.py --repo "$REPO" --upstream "$UPSTREAM" --out "$WORK/owner"
bash test_host.sh
```

`replay.py` rereads the ledger, compiles original IDO sources, assembles independent original reference text and links at original VMAs. `diagnostics.py` compares generator diagnostic outputs to ordinary native linked bytes and relocation tuples. `check_owner.py` independently checks the original ASM-backed owner versus the candidate at the original VMA. Each variant is hashed in `evidence/`. Keep raw build output private; this kit contains only authored sources, scripts and sanitized evidence. The next gate is canonical JP2843 predecessor rebuild and strict full-ROM integration of both exact functions.
