# C-Right stage helper and spatial loader native retry — 23 November 2026

FAILED_NATIVE / RESEARCH_ONLY. Base stable/decomp 1ddb1b0941b0f39d4db6b0a3534fc1f230b51e0e; SHA-pinned source archive, pinned clean original upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee, original USA and JP retail/expanded ROM SHA1s and SGI IDO5.3 compiler SHA256 authenticated. Checked live refs and open PRs using connector; direct Git DNS blocked. All 26 new C sources compiled, independently replayed with identical results, no positives. Original reference assembly annotations verified against original private ROM; references independently assembled and linked at original VMA. Native flags and every attempt in full downloadable source-only research ZIP.

| Function | Original bytes | New candidate bytes | Best exact prefix | Best aligned words |
|---|---:|---:|---:|---:|
| USA func_8020DC78_5C9148 | 256 | 264 | 12 (previous 8) | 3/64 |
| JP func_80212AD0_5CE060 | 256 | 264 | 12 (previous 8) | 3/64 |
| USA func_8020D670_5C8B40 | 76 | 76 | 0 | 9/19 |
| JP func_80212460_5CD9F0 | 76 | 76 | 0 | 9/19 |
| USA func_8020D36C_5C883C | 772 | 756 radius-local / 848 prior-shape | 0 | 2/193 radius-local, 5/193 prior-shape |
| USA func_8020D848_5C8D18 | 1072 | 1200 | 80 | 22/268 |

Stage helper reversed local initialization independently restores the initial marker-load register; first remaining mismatch at +0xC is original marker copy to return register versus candidate start pointer copy. Both variants emit eight rather than six named relocations due redundant global HI16/LO16 and subsequent loop register allocation is wrong. Array, register, line splitting, declaration reorder, int depth, byte-array variants did not resolve. This is not a native matching breakthrough. The descriptor comparators retain exact extent and relocations but swap state/descriptor registers; typed callback pointer and register keyword do not resolve.

Grid radius-local variant with refresh after resource-list processing reduces absolute size error from 76 to 16 bytes but exact-word count worsens and first stack-frame mismatch stays -152 vs -176. Candidate semantics not proven. Cached request and cast-zero float variants do not improve loader. Larger JP counterparts not attempted. No new reusable compiler rule claimed. Existing workarounds did not transfer to helper/comparator; larger attempts NO_NEW_COMPILER_FINDING. Retain all ASM. No G2, strict inventory, full local CI or gameplay run. Canonical counts unchanged.

Source-only research artifact Goemon_CRight_Stage_Helper_Retry_20261123.zip SHA256 391f0590c3aebfa23644741578b823ebaeae00cf3b77c5b3dec6b758aa87d476 contains all 26 new sources, six prior controls, replay.py/native_helpers.py, per-attempt evidence and instructions. Source fingerprints validated; 36 ZIP entries and ZIP integrity verified. Delivered as downloadable conversation attachment. This checkpoint retains the two helper source-order pairs and USA grid radius pair with exact tested source. No original bytes, ROM, objects, tools, raw traces or saves committed. Follow GOEMON_BUILD_ENVIRONMENT.md and the kit instructions for exact replay with private inputs.
