# USA file_11 central verifier integration — 15 November 2026

## Implementation and claim status

An **optional, fail-closed** `overlay_file11_stage` field is now supported by `decomp/verify.py`. The only accepted shape is:

```json
{"overlay_file11_stage":{"format":"goemon-file11-character-switch-13-v1"}}
```

The published production `decomp/manifest.json` intentionally does **not** activate the new stage. Enabling it causes the verifier to split the pinned USA Splat `file_11` into eight ordered C/ASM source objects, compile the original IDO 5.3 C candidates, trim zero-only object padding preserving .rel.text entries, lower the exact overlay SUBALIGN to 4, then rebuild the entire USA image. The selector at ROM `0x59941C` remains an original 180-byte assembly region.

## Mandatory machine-code gates

The new adapter's `verify_linked_stage` executed against the **real pinned original** USA 32 MiB ROM, the previously independently rebuilt 13-function USA 32 MiB ROM, the pristine original linked ELF and its matching-C candidate linked ELF. It passed all these checks:

- Exact authenticated original USA ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; rebuilt image byte-identical.
- Four C sources exactly match their SHA-256 source identities and four after-trim native MIPS ELF objects match their pinned SHA-256.
- The link map shows all **eight** source objects exactly once, in original order and exact start VMA and length, with `file_11` output extent `0x41400` at `0x801CB460`.
- All thirteen linked C FUNC symbols have original VMAs, exact sizes, original machine-code hashes and proper `.file_11` symbol ownership.
- The original/candidate `.rel.file_11` sections contain **8,825 relocation entries each** and have matching (site, relocation type, symbol target value, symbol name) multisets (in the tested 13-function scratch build, also identical in order).
- Nine ROM-free Python fail-closed contract unit tests passed; malformed original ROM, changed Splat boundary, double staging, missing objects, and modified identities are rejected.

**Evidence boundary:** This is a successful native/linked/staged original-ROM provenance check using the independently verified scratch construction, **not** a completed central `decomp.verify` end-to-end build containing the other 160 production claims. Do not promote count or rewrite `results/combined.json` until that central run is performed. The Japanese build blocker remains separate.

## Next bounded work

Activate the opt-in stage in a temporary manifest within the pinned central decomp workspace, run the complete `decomp.verify` G2 including other overlays, compare the full 33,554,432-byte image and semantic relocation table, and check inventory and `decomp/local_ci`. Only after this passes should the canonical manifest and inventory be updated.


## Independent clean pinned-source rebuild (completed later on 15 November)

The opt-in `overlay_file11.py` module has now independently passed **all three phases** on a completely fresh upstream ZIP extraction, rather than merely validating the previously built scratch image:

1. Authenticated original 16 MiB USA game ROM and decompressed original 32 MiB game image. Pinned upstream repository `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
2. `stage_sources` from the new central adapter checked all 13 original code SHA-256 identities, four source checksums, installed the four C source translation units and split the original `file_11` Splat into exactly eight sections, leaving the 180-byte selector as original assembly.
3. Splat extraction and an initial full upstream ROM build completed, then `prepare_objects` successfully trimmed all eight original-size `.text` sections while preserving ELF relocation records and lowered the pinned file_11 link SUBALIGN to four.
4. A final full make rebuilt the whole **33,554,432-byte USA image exactly**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. The new `verify_linked_stage` independently verified all 13 original-VMA linked function symbols, four pinned compiled object identities, all eight original-sized map extents, and **8,825/8,825 semantically identical relocation tuples also identical in record order** to a separately built pristine original ELF. The candidate linked ELF SHA-256 is `659efc987ce80152acfac4891beaa4f44daea0e889f945564d5da634a1013396`.
5. All 36 standalone `goemon_research` Python unit tests passed, including nine new fail-closed file_11 module cases.

The earlier two failed clean trials were due to an accidentally reused Japan-extracted source checkout that injected `asm/japan_0` into the USA Makefile input enumeration, then a standalone-Python `PYTHONHOME` mismatch. Both were isolated to throwaway scratch folders. The independently fresh ZIP extraction plus correct standalone interpreter resolved the problems without changing the source or removing checks. These failures do not represent original USA C code mismatch.

The dedicated reproducible, copyright-safe proof metadata is `decomp/results/file11_optin_clean_proof_20261115.json`. **No complete run of the central production `decomp.verify` pipeline containing all 160 existing C claims has yet occurred.** The canonical `manifest.json`, `results/combined.json`, and `results/inventory.json` remain unchanged. The research result is production-adapter ready but not formally promoted.
