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
