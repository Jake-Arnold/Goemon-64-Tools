# Japan C-Right +0xD1 and next-door freeze: read-only Phase 4 research

**RESEARCH_ONLY / no matching-C promotion.** Live preflight stable/decomp SHA `56e4754255403f012cc9bc88ba39ec1f4fadfb6c`, 23 Nov 2026. User instruction explicitly defers promotion. Original Japanese retail ROM was authenticated locally and expanded to the original SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. Private ROM and toolchain are **not** included here.

## Reproducible findings

- Original stage `D_80162420_163020 + 0xD1` is fixed JP RAM `0x801624F1`: stores **1** at original guest PCs `0x802125C4` and `0x80212680`, stores **0** at `0x8021DBC0` inside stage reset `func_8021DB74_5D9104` (`0x5D9104`, 120B).
- Reset is called from original stage manager `0x801FC350` and `0x801FCF50`. The reset clears +0x8C, +0x90 and +0x98 through +0xAC task pointers, but **preserves +0x94**. Old real normal/held Project64 Phase3 traces confirm that +0x94 is unchanged through the first initializer entry, though their initial task-pointer states differ. The reset does **not** prove a stale pointer/freeze.
- Original MIPS scanner (`scan_stage_orig.py`) checked 2,546 Splat assembly files and 567,959 instructions; found three direct stores to +0xD1, one store to adjacent +0xD0, and **zero statically resolved direct reads**. This is a **bounded static scan**; indirect/aliased/VM reads are not excluded. See `stage_d1_static_audit.json`. The original 128B periodic callback `func_80212BD0_5CE160` has no direct +0xD1 access in its inspected body.
- **Ownership correction**: `func_8021DB74_5D9104` is already included in the accepted Japan `jp1686` promotion (live `decomp/research/jp1686_promotion/candidates.csv`; excluded names in `decomp/japan_1686_promotion.py` are only two different `0x0800...` functions). Its independent native 28/28 nonreloc+2 reloc reproduction is a **duplicate verification, not a new C function**. Do not count it.
- Four user-requested unconverted targets **remain ASM** after bounded original SGI IDO5.3 experiments: indexed record clearer `func_800041AC_4DAC` 48B, phase updater `func_8000339C_3F9C` 88B, zero-terminated 16-bit registration loader `func_80013654_14254` 80B, and stage periodic callback `func_80212BD0_5CE160` 128B. See `native_negative_summary.json` and `native_negative_controls/`; older 14 48B variants and callback negative are already archived at `decomp/research/jp_cright_reset16_20261123/`. No new native-exact C functions are claimed, all failures keep original ASM.
- Prior real Phase3 normal/held Project64 logs showed 13 unique actor markers on each, and post-load +0xD1 normal 0 vs held 1. No later freeze was captured. Pair starts differed, so causality of actor address differences is not established.

## Reproduction

```sh
# After authenticating and extracting the user's original JP source:
python3 decomp/research/jp_cright_phase4_20261123/scan_stage_orig.py \
  --asm-dir /private/pinned/mnsg/asm/japan_0 \
  --out /private/sanitized_stage_static.json

python3 -m unittest discover \
  -s decomp/research/jp_cright_phase4_20261123 \
  -p test_analyzer.py -v

# Project64 JSONL analysis, after a REAL capture, not a synthetic fixture:
python3 decomp/research/jp_cright_phase4_20261123/analyze_phase4.py \
  --trace /private/Goemon_CRight_phase4_held_followthrough.jsonl \
  --normal /private/Goemon_CRight_phase4_normal_followthrough.jsonl \
  --out /private/phase4_sanitized_comparison.json
```

The **two read-only Project64 3.x scripts** are supplied as a source-only **downloadable research ZIP in the original user conversation**, *not committed to Git*, because they contain an original-game code-signature hash guard. The scripts and mock tests passed 4 host mock scenarios but **actual Phase4 Project64 runs are NOT yet completed**. `analyze_phase4.py` validates log schema/sequence/footer and reports whether the initial non-controller fields are truly identical; a user-entered `finish('freeze_observed')` is *a report*, not instrumentation proof of freeze/cause. Further read hooks are optional and must be tested in the emulator. No tool ever writes to game memory.

## Verification scope

- Original research preflight was Japan **2,370 C / 5,006 ASM** at `56e47542`; live `stable/decomp` advanced independently to **2,398 C / 4,978 ASM** (JP short28 work), with no overlap with these four requested targets. **This Phase4 research adds 0 matching C functions.**
- This research's native isolated verification of **already accepted reset**: 120B, 28/28 nonrelocation words, correct two HI16/LO16 relocation types. Original full-ROM G2 for this *independent duplicate source* **NOT RUN**. Full live-stable `decomp.local_ci` **NOT RUN**.
- `scan_stage_orig.py` direct-read coverage is non-exhaustive. A freeze cause is **NOT_PROVEN**.
- Stage+0xD1 is one byte of stage memory, unrelated to an automatically writable toolkit field. Nothing in this PR modifies toolkit, source promotion manifests or proof inventories.
