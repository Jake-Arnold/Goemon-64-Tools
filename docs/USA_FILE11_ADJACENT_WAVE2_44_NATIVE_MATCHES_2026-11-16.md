# USA file_11 adjacent research — second sweep (16 November 2026)

## Verified scope

The original USA 32 MiB ROM (`SHA-1 6ea0ed71032ce08fc2745f412d84936382197494`) and the pinned generated Splat `asm/usa/587370.s` (`SHA-256 e936f86295b8d8795369fd6db6a42da5b13184b9856058878066b9448e4a5f8b`) were reauthenticated. The original source was extracted from upstream `mnsg` revision `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.

**44 additional non-overlapping C functions, 1,976 original USA instruction bytes, match under IDO 5.3 at their original VMAs.** The native compiler and linker were the supplied original IDO and pinned MIPS toolchain. The probe linked each function at the original virtual address and compared every byte against the original retail ROM. A separate rerun produced the same exact result after adding the previous 50 promoted functions to the rejection set. No copyright-sensitive ROM bytes, extracted assembly or compiler binaries are included in this research commit.

These 44 are **in addition to** the previous 77 and 68 research functions in draft PR #23; they do not overlap those 145 or the 50 previously promoted file_11 functions. Research candidates beyond the formal 210-function baseline now total **189 functions / 6,512 matching instruction bytes**. If all eventually passed full native ROM/inventory integration, the prospective matching-C count would be **399 / 19,848 bytes**. These last figures are *not* production claims.

## Important adjacent C islands

The native probe compiled **nine contiguous C islands** as complete translation units, with **all nine exactly matching the original instructions**. These islands span 44 functions / 1,892 original bytes; **37 of their functions are newly identified in this pass**, while seven come from the earlier 77/68 research proofs. The prior functions are counted once, not again as new candidates.

| USA ROM interval | Total functions | Newly found | Original bytes | Combined native C match |
|---|---:|---:|---:|---|
| `0x5AA138–0x5AA320` | 9 | 8 | 488 | Exact, 122/122 words |
| `0x5A3CB0–0x5A3CF8` | 2 | 2 | 72 | Exact, 18/18 words |
| `0x5B0438–0x5B0568` | 8 | 4 | 304 | Exact, 76/76 words |
| `0x5B0EB4–0x5B0FB4` | 6 | 6 | 256 | Exact, 64/64 words |
| `0x5B1C80–0x5B1D04` | 3 | 3 | 132 | Exact, 33/33 words |
| `0x5B1F4C–0x5B1FA4` | 2 | 2 | 88 | Exact, 22/22 words |
| `0x5B2004–0x5B20AC` | 4 | 4 | 168 | Exact, 42/42 words |
| `0x5B2578–0x5B2680` | 6 | 6 | 264 | Exact, 66/66 words |
| `0x5B8488–0x5B8500` | 4 | 2 | 120 | Exact, 30/30 words |
| **Totals** | **44** | **37** | **1,892** | **9/9 exact** |

### The most useful block: `0x5AA138–0x5AA320`

This 488-byte run is more substantial than a series of empty callbacks. The nine functions, in original order, initialise actor fields at offsets `+0x30`, `+0x48`, `+0x4C`, `+0x4E`, `+0x50` and `+0x52`; conditionally copy three floats at offsets `+0x08/+0x0C/+0x10`; copy three floats at `+0x1C/+0x20/+0x24`; copy three 16-bit values at `+0x14/+0x16/+0x18`; perform **two different saturated byte-step operations**; copy either four or seven bytes; and finish with a previously identified 20-byte no-op hook. The two byte-step routines update the pointed byte toward a supplied bound by a supplied step, returning an indicator for whether the bound was reached. The original unsigned byte parameter promotion and repeated dereference are necessary for exact IDO code generation. The exact game-facing semantics of the fields and event thresholds remain unverified.

### The callback runs

The six contiguous functions at `0x5B0EB4–0x5B0FB4` (256 bytes) are fixed-argument handler dispatchers; six functions at `0x5B2578–0x5B2680` (264 bytes) form another continuous call-forwarding family. The eight-function run at `0x5B0438–0x5B0568` (304 bytes) extends a previously known three-function C island by adding four new wrappers and incorporating one additional older function. Several wrappers pass bit patterns such as `0x40900000`, `0x41000000` or `0x3F800000` as raw integer arguments; these may correspond to floating-point parameters at the callee boundary, but the native wrapper proof alone does not establish parameter type or player-facing meaning.

### State flags and predicates

- `0x5B8488–0x5B8500` contains two previously found empty callbacks and two newly reconstructed functions which clear and set bit mask `0x14` in an indirect state structure. Both look up the same pointer through a value at USA RAM `0x8015C5C8` and access a nested 16-bit field at `+0x22`.
- `0x5A3CB0–0x5A3CF8` contains an actor action-byte range predicate and a character-zero plus nested-state predicate. Both compile together as 72 original bytes.
- A third 32-byte actor state range predicate at `0x5A3E40` matches individually, but remains isolated because the intervening assembly is not yet matching C.

## Exact native proof and reproducibility

Committed inputs:

- `decomp/research/file11_adjacent_wave2_sources.json`: exact C source and original code hashes for all **44 new functions** and nine contiguous island membership inventories.
- `decomp/research/file11_adjacent_wave2_probe.py`: authenticates the original USA ROM, original Splat assembly, original function offset/name/size, C fixtures and previous research sets, then compiles all 44 original-VMA functions and all nine combined C islands; fails closed if a function overlaps the 77/68 research sets or the previous 50 promoted functions.
- `decomp/results/file11_adjacent_wave2_native_proof_20261116.json`: every new function and C-island byte hash, original byte counts and exact-match outcomes.
- `tests/test_decomp_file11_adjacent_wave2.py`: **18** new ROM-free proof-metadata and overlap regression tests.

Reproduction command in the supplied Linux IDO/MIPS environment:

```bash
python3 -m decomp.research.file11_adjacent_wave2_probe \
  --rom /path/to/mnsg-japan/config/usa/baserom.decompressed.z64 \
  --asm /path/to/mnsg-japan/asm/usa/587370.s \
  --cc /path/to/mnsg-japan/tools/ido-5.3/cc \
  --ld /path/to/mips-linux-gnu-ld \
  --objcopy /path/to/mips-linux-gnu-objcopy \
  --report /tmp/new-unique-wave2-proof.json
```

The native probe was run twice with **44/44 exact individual functions / 1,976 bytes and 9/9 exact native grouped translations / 1,892 bytes**. The 18 new regression tests passed. The older uploaded repository ZIP predates the merged 210-function promotion: its general ROM-free local CI still reports **two stale pre-existing source-fingerprint failures** (`test_overlay_file11` and `test_vm_residual_inventory`), unrelated to the new 44-function proof. Do not claim that full repository CI passed in that older snapshot.

## What has not been proved

The full mixed C/assembly overlay has **not** been re-linked with these 44 additions or the earlier 145 pending additions. There is **no complete 399-function native G2**, no new 32 MiB ROM byte-for-byte comparison for the combined build, and no new relocation-order or inventory proof. The canonical `decomp/manifest.json`, `decomp/results/combined.json` and `decomp/results/inventory.json` must remain at **210 official C functions / 13,336 matching bytes / 7,153 remaining ASM entries** until the complete promotion gate passes. The Japanese whole-ROM build and the 180-byte character selector are separate unresolved tasks.

The logical next step is to place the nine exact islands into a new opt-in, size-locked `file_11` mixed-C/ASM adapter, starting with the 488-byte state-helper island and the 256-byte event-dispatch island; preserve all intervening assembly, full ROM identity and 8,825 original semantic overlay relocations, then run `decomp.verify` plus `decomp.inventory` against the *current merged* 210-function baseline. Only after those gates may counts be increased.
