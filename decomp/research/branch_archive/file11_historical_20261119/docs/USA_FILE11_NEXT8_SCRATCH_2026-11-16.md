# USA file_11 next-eight contiguous callback scratch — 16 November 2026

**Status: NATIVE_SCRATCH_VERIFIED_NOT_CENTRAL.** The canonical matching-C count remains **315**, not 323.

## Candidate

Original ROM bytes `0x5A6F30..0x5A7090` (352 bytes) contain eight adjacent, 44-byte MIPS functions `func_801EB020_5A6F30` through `func_801EB154_5A7064`. They call the original named handler `func_801EB180_5A7090` with four modes, repeated twice.

The source in [`decomp/research/file11_next8_group.c`](../decomp/research/file11_next8_group.c) is the exact text used in this native build (SHA-256 `7919d61ac0453f342629d51186b1ddf16f3716f527b411c93716815941122d60`). The adjacent research fixture in PR #23 already recorded native original-VMA grouped matches. This run independently rebuilt the **complete pristine-upstream USA ROM** with the eight C functions together.

## Reproduced Linux native scratch

Inputs: user's authentic original USA retail ROM, pinned `mnsg` git revision `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, supplied IDO 5.3, Splat, MIPS binutils and standalone Python 3.12. The project build-environment runbook explains the portable runtime setup. No copyrighted input or compiled output is checked into Git.

1. Rebuild the pinned original USA `mnsg` checkout, using `rommy decompress`, `splat split`, `make -j8 VERSION=usa build/usa/mnsg.z64`; assert SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
2. In a **separate copy** of that checkout, edit only the `file_11` Splat block, replacing the original `[0x587370, asm]` / `[0x5B8500, data]` adjacency with:

```yaml
    - [0x587370, asm]
    - [0x5A6F30, c, file11_eight_callbacks]
    - [0x5A7090, asm]
    - [0x5B8500, data]
```

3. Copy the checked-in C file into candidate `src/file11_eight_callbacks.c`. Rerun `splat split config/usa/splat.yaml`, then `make -j8 VERSION=usa build/usa/mnsg.z64`.
4. `cmp` the candidate and original 32 MiB images and check the candidate hash. Run `readelf -Wr` for both ELFs; compare each `.rel.file_11` relocation as an unordered `(offset, relocation type, symbol value)` tuple. Run `readelf -Ws`; compare every original named `func_<hex>_<hex>` positive-sized `FUNC GLOBAL DEFAULT` symbol, including all eight new C functions' original names, sizes and addresses.

## Actual results

| Gate | Fresh result |
| --- | --- |
| Original baseline 32 MiB ROM | Exact |
| Candidate with 8 grouped C functions | Exact original 32 MiB ROM |
| SHA-1 | `6ea0ed71032ce08fc2745f412d84936382197494` |
| Original versus candidate `file_11` relocations | **8,825 / 8,825**, equal semantic multisets |
| Named positive-sized `func_*` ELF identities | **7,098 / 7,098**, same name, VMA and size |
| New 8 C function names, original VMAs and sizes | **8 / 8** |
| Original 352-byte source span SHA-256 | `b1fbaa8f74fec1f63e9f3cf2d0647daf26fd008a135cba0f767e5958113dcff1` |

The 7,098 subset comparison **is not** the full original 7,376-entry central inventory and is not presented as such. No gameplay test was run.

## Production gate still outstanding

The current 152-file11-C stage has a larger ASM slice `0x5A63F8..0x5A74CC` spanning this new group. The next 160-C layout must split it into ASM `0x5A63F8..0x5A6F30`, C `0x5A6F30..0x5A7090`, and ASM `0x5A7090..0x5A74CC`, preserving the other 87 source/object chunks. The new versioned adapter must prove all original native object extents and hashes. Then rerun complete **323-C** central `decomp.verify` + `decomp.inventory` and the full `decomp.local_ci`.

Prospective only: USA **323 C / 17,012 instruction bytes**, file_11 **160 C / 4,628 bytes**, remaining PR #23 backlog **97** after promotion. Nothing in the canonical manifest or proof ledger has been changed by this PR.
