# USA original opening-sequence file_18 — bounded SGI IDO5.3 native research
Date: 23 November 2026. **RESEARCH_ONLY; zero canonical ownership changes**.
Base: `stable/decomp@838e9f87c3a860973e9d168b58fcf88bd456bfb4`. This source-only research was measured against clean pinned `klorfmorf/mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, native SGI IDO5.3 (SHA256 `76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0`) and authenticated original expanded USA ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; private inputs are not in this PR.

| New ASM-owned identity | ROM | Bytes / MIPS words | Original relocations | Status |
|---|---|---|---|---|
| `func_802142F8_67DCD8` | `0x67DCD8` | 72 / 18 | 0 | Original-ROM 72/72 exact, original symbol length |
| `func_80217700_6810E0` | `0x6810E0` | 84 / 21 | 1 `R_MIPS_26` (original callback) | Original-ROM 84/84 exact, original symbol length |

Both statically called by the large `func_8020D998_677378`; opening gameplay runtime not measured.

## Source and compiler quirks

- `sources/func_802142F8_67DCD8.c` SHA256 `d17312313de75b416d05c63b281c5bc7a73a542431b413d6d1ff5a13f6170e91`. The original `div.s` and FPU register order require `float d=(float)2` and store/reload before division. Alternative `d=2.0f` fails via `mul.s` and source reordering changes `$f2/$f0` scheduling. **EXISTING_QUIRK_REPRODUCED**, source-expression-order sensitivity.
- `sources/func_80217700_6810E0.c` SHA256 `cdd9907b975f7a1f738b13b195abed63e85b703c285352251c3678c033a07f3a`. Cloned exact semantic source form from **already accepted**, separately reverified 80/80 original bytes donor `func_80217970_681350`, retaining prototype `int func_800040A8_4CA8(float,float)` and adding original `+0x240` before `&0x3FF`. **EXISTING_QUIRK_REPRODUCED**, prototyped float callback ABI/expression scheduling.
- Two deliberate mutated negative controls in `negative_controls/` are incorrect and must never be promoted. Full session sweep: 84 native variants, 5 exact variants (3 from 72B, 1 from 84B, 1 already accepted donor), 77 failed and 2 expected-fail controls. Remaining `0x677160`, `0x677194`, `0x676C80`, `0x681968` remain ASM due register/scheduling and branch mismatches.

Standalone original ROM/ELF/relocation checker passed with the separately delivered source-only reproduction ZIP, and 131,072 test cases with GCC ASan/UBSan passed. No machine-code patching or ELF type alteration was performed. Source SHA and full variant evidence are in that downloadable session ZIP; ZIP contains scripts `run_native.sh`, `batch_native.py`, `verify_exact_rom.py` and all failing variants.

**No integrated original-ROM 33,554,432-byte G2, strict inventory, promotion-integrity or full local CI** for these new functions: a complete authenticated current live `stable/decomp` checkout was not available in the execution container. No accepted C count changes; live USA remains 2,164 C / 5,199 ASM (file_18 184 C / 203 ASM). This PR is **draft RESEARCH_ONLY**, not an integration/promotion PR.
