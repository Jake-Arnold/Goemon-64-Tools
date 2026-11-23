# USA + JP: 100 additional short-function IDO matches — original ROM research

**23 November 2026 — RESEARCH_ONLY. This PR does not publish matching-C into the canonical manifest.**

Base: `stable/decomp` `4b289a015a2ffd9f47ca3356d09a248836e8dee8`; original pinned upstream `klorfmorf/mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, original SGI IDO 5.3 `cc` SHA256 `76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0`, flags `-c -G 0 -non_shared -O2 -mips2`.

## Fresh isolated-native results

| Family | Matches | Summary |
|---|---:|---|
| Callback registration | 17 | 52-byte wrappers |
| Conditional callback installation | 18 | 68-byte wrappers |
| Float initializer/callback | 10 | 84 bytes each |
| Three-call dispatch | 9 | 84 bytes each |
| Actor initializers | 8 | 68 bytes each |
| Float initializer/callback II | 8 | 88 bytes each |
| Indexed actor selectors | 8 | 68 bytes each |
| Small stub callers | 4 | 44 bytes each |
| Float initializer/callback III | 6 | 88 bytes each |
| Timer dispatch | 6 | 48 bytes each |
| Indexed callback | 6 | 56 bytes each |
| **Total** | **100** | **72 USA, 28 JP; 6,824 original bytes** |

- Verified complete original 32MiB input ROM SHA-1 hashes independently for USA and Japanese images. Each candidate is original ASM-owned and strictly under 100 original bytes, excluding all 6 earlier candidates in PR #183, canonical accepted C and open PR overlap.
- 100 isolated SGI IDO original instruction-body matches; 478 symbolic original linker relocations checked by offset/type/symbol, with original MIPS addend rejection; 100 exact positive `STT_FUNC` extents; 94 harmless original-body-external zero-padding object tails. This is not source-unit/layout/complete-original-ROM G2.
- 100/100 native source-mutated negative controls measurably fail comparison: 57 raw instruction differences, 35 relocation identity differences, 8 hidden relocation-addend differences. All compiler quirks preflighted; outcome `NO_NEW_COMPILER_FINDING` on matching candidates.
- `python3 -m decomp.local_ci` on a clean exact live source snapshot: **PASS**, exit 0, including configured ROM-free sanitizer tests; `python3 -m decomp.promotion_integrity --validate`: **PASS only for unchanged USA accepted C 2,092 / 94,760 bytes / 5,271 ASM**.

## Attached source-only research bundle

Full independently executable evidence is provided **in the ChatGPT conversation artifact** `goemon-native100-20261123.zip`, SHA256:

```text
b8733ae1670e0a7345f26744b41c33c25c44f1088247000610dc32cfa9b39226
```

It contains **all 100 real C source files**, all 100 compilable mutant controls, `manifest.json` (all original ROM offset / VMA / length / owning Splat ASM / SHA-256), `evidence.json`, `replay.py` and `README.md`. The companion repo checker `verify_bundle.py` audits ZIP SHA256, exact source hashes and absence of duplicate regional ranges without requiring ROMs. The full source bundle is **not attached to this GitHub PR**; this PR holds provenance and outcome metadata only. For native reproduction follow the delivered ZIP README and provide private user-owned original ROMs, original upstream Splat trees and pinned compiler. Do not commit these private inputs or generated objects.

## Mandatory incomplete gates

**NOT_RUN:** native compilation in the complete real source units, complete new original-USA and original-Japan 33,554,432-byte ROM G2 comparisons, all positive ELF identities and full semantic relocation preservation, new strict inventory, updated manifest/combined proof and comprehensive promotion integrity. **Canonical C delta zero**. No emulator/gameplay testing performed. Targeted native positive/negative source matching is research, not a production promotion.
