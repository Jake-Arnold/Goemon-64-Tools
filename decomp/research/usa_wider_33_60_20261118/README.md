# USA resource 33–60 original-address C sweep — 69 matching functions

**2026-11-18 · RESEARCH_ONLY · USA NG5E**. Expands the previous source-only `file24–32` sweep into the **28 adjacent resources numbered 33–60**. Original MIPS instruction byte identity and whole upstream USA ROM scratch rebuild were independently checked. This package includes **69 native exact C functions across 21 resource files**, covering **852 original instruction bytes**. Original ROM data, original assembly, ELF, saves, debug dumps and proprietary binaries are **excluded**.

## Native verified results

| Original file | Exact C functions | Original code bytes | Original ELF relocations preserved |
| ---: | ---: | ---: | ---: |
| 36 | 1 | 8 | 1025 |
| 37 | 1 | 12 | 1079 |
| 38 | 2 | 24 | 761 |
| 40 | 6 | 72 | 892 |
| 42 | 5 | 68 | 555 |
| 43 | 17 | 200 | 1593 |
| 44 | 5 | 68 | 598 |
| 45 | 1 | 12 | 545 |
| 46 | 5 | 60 | 817 |
| 47 | 2 | 32 | 275 |
| 48 | 2 | 28 | 469 |
| 49 | 4 | 64 | 602 |
| 50 | 3 | 36 | 228 |
| 51 | 1 | 12 | 143 |
| 52 | 1 | 12 | 8 |
| 53 | 1 | 12 | 534 |
| 54 | 2 | 24 | 341 |
| 55 | 2 | 20 | 390 |
| 56 | 5 | 56 | 436 |
| 57 | 2 | 20 | 708 |
| 59 | 1 | 12 | 508 |
| **TOTAL** | **69** | **852** | **12,507** |

Pattern breakdown: **51 original two-argument no-op actor callbacks**, **eight zero-argument no-op functions**, **three multiplication/scale setters**, **three integer-division getters**, **three actor-field argument stores**, **one context 16-bit decrement**. Even no-op functions are original positive-sized functions with unique original offsets and ELF function identities; they are not synthetic alias labels.

Nontrivial examples include original resource42 `func_080008B8_6F0AC8` (20 bytes, scale by 30), `func_080008CC_6F0ADC` (24 bytes, divide by 30), two resource42 actor-field setters at `+0x8E4/+0x8EC`, and original resource44 `func_080012C8_6FC4C8` (20 bytes, context angle decrement). The C does not reassign semantic meanings to any original room fields.

## Verification actually performed

- Every one of the **69 C sources** was compiled using original IDO 5.3 with pinned `-O2 -mips2` flags, linked to its original overlay VMA and matched against authenticated original-USA decompressed 32MiB ROM instruction bytes. Source-to-ROM fingerprints are listed per function in `manifest.json`.
- The C was then staged in a **disposable pinned-upstream scratch checkout** across all **21 changed original resources** and rebuilt successfully into a **33,554,432/33,554,432-byte identical original USA ROM**, SHA-1 **`6ea0ed71032ce08fc2745f412d84936382197494`**. No original instruction bytes were modified, and only verified zero trailing object-alignment padding was trimmed where necessary.
- Original positive-sized ELF identities **7,376/7,376** and semantic relocations **12,507/12,507** across the 21 changed resources were independently verified equal against original upstream baseline.
- Host GCC tests linked all **69 actual C sources**, passed `-fsanitize=address,undefined` and `-Werror`, and checked no-op side effects, signed division/negative inputs, unsigned multiply overflow wrap, setters and angle decrement. No sanitizer class was disabled.

## Candidates not matched

Eleven bounded candidates remain **FAILED_NATIVE**: seven callback registration wrappers mismatch at instruction-relative `+0x0C` due register scheduling after baseline plus three bounded C-prototype variants; four register-to-float stores did not match at their first instruction. Their original assembly remains untouched. This 69-function package contains **no nonmatching candidate C**.

## Reproduce without bundled ROM

Use the user's own original USA **decompressed 32MiB** ROM and pinned toolchain (in `GOEMON_BUILD_ENVIRONMENT.md`):

```bash
python3 verify_original.py --rom /path/to/config/usa/baserom.decompressed.z64 --ido /path/to/ido-5.3/cc --report /tmp/file33-60-native.json
python3 verify_original.py --host-test-only
```

The standalone verifier refuses incorrect ROM/file-size/hash, mismatching source SHA-256/Git-blob hashes, incorrect MIPS bytes and nonzero trailing compiler padding; the host suite does not depend on ROM bytes.

## Production boundary

This exact scratch build is from the pinned **original upstream** tree, **not** a fully authenticated checkout containing all accepted C on `chatgptweb/decomp`. Therefore the canonical combined `decomp.verify`, strict `decomp.inventory`, complete-source ELF ownership and full `decomp.local_ci` for the production manifest were **NOT RUN**. No production C promotion, no manifest/proof/inventory modification, no Japan native claim. The live production baseline recorded at research start was **864 USA C / 39 Japan C** (recheck GitHub before future integration). A successful independent integration of these **69 distinct** functions with current USA 864 would yield **933**, not accepted 933. Other unpromoted batches (files26/27/24–32) must be tracked and integrated separately without double-counting.

**Next step:** Authenticate complete current decomp checkout; stage 69 exact C alongside accepted C; run full combined native 32MiB ROM/ELF/relocation/inventory/CI gate; promote only on PASS.
