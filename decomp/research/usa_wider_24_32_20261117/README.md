# Wider USA resource-adjacency matching-C sweep (24, 28–32)

**17 November 2026 — RESEARCH_ONLY**. The user asked to widen the search beyond original resources 26 and 27. This package contains **60 distinct original-address native-matching C functions / 1,612 original instruction bytes** from original USA file resources **24, 28, 29, 30, 31, 32**. Prior file26 (15 exact) and file27 (21 exact) research is not counted. File25 had a previously discovered 72-byte *isolated-only* candidate with extra relocations, not included here.

## Verified scope

| Resource | Exact C functions | Original instruction bytes | Original file semantic relocations preserved |
|---|---:|---:|---:|
| 24 | 10 | 328 | 160/160 |
| 28 | 3 | 204 | 35/35 |
| 29 | 16 | 516 | 2536/2536 |
| 30 | 25 | 336 | 1826/1826 |
| 31 | 3 | 36 | 1371/1371 |
| 32 | 3 | 192 | 1068/1068 |
| **Total** | **60** | **1,612** | **6996/6996** |

1. All 60 compiled with original IDO 5.3, original project flags `-O2 -mips2`, linked at their **actual original overlay VMAs**, and matched the original USA decompressed ROM instruction bytes independently.
2. The exact C definitions were staged with **all remaining original assembly** in a dedicated *pinned upstream* scratch checkout. Multiple incremental rebuilt ROM checks passed; the final scratch image with **all 60 C functions in six resources simultaneously** is **exactly 33,554,432 bytes identical** to the original expanded USA ROM, SHA-1 **`6ea0ed71032ce08fc2745f412d84936382197494`**.
3. Exact original positive-sized ELF FUNC identities **7,376/7,376** and original resource-specific semantic relocations **6,996/6,996** preserved across the six changed resources. The source-to-ROM code comparisons include original sizes, symbol names and addresses.
4. **GCC AddressSanitizer + UndefinedBehaviorSanitizer PASS** with all **60 actual C source files** linked, and targeted semantic tests for actor angle increments, actor-state gating, saved-event callback, timer underflow, callback selection, simple init calls and state-bit changes. No sanitizer class was disabled for these tests. These are host-only tests and do not prove individual gameplay event execution.
5. No original ROM, MIPS disassembly, save file, memory dump, compiled binary or proprietary toolchain is present in this source-only package.

## Engineering interpretation

The nontrivial exact functions include two original resource24 dynamic angle-field updates (`actor+0xD0` into an associated context angle), three original resource28 event/callback helpers, six resource29 callback timer decrements, a resource30 actor state setter/callback, and three resource32 initialization/callback helpers. Numerous remaining small functions are independently verified original no-op callback/stub entries, **not synthetic duplicate aliases**. They each retain their original address and symbol identity. Some other attempted functions did not match; their original assembly is untouched.

## Reproduce the native per-function comparison

With the user-owned original USA **decompressed 32 MiB** ROM, pinned IDO 5.3, and MIPS GNU ld/objcopy available locally:

```bash
python3 verify_original.py --rom /path/to/usa/baserom.decompressed.z64 \
  --ido /path/to/pinned/mnsg/tools/ido-5.3/cc \
  --report /tmp/wider60-verify.json
```

The verifier refuses a wrong ROM hash, wrong source digest, mismatching native bytes, unexpected nonzero compiler padding or missing tools. It creates scratch objects outside the source bundle. `PATH` and `LD_LIBRARY_PATH` must include the supplied MIPS toolchain as described in `GOEMON_BUILD_ENVIRONMENT.md`.

Host sanitizer regression:

```bash
python3 verify_original.py --host-test-only
```

This builds `test_wider_actual.c` against all 60 actual C source files using host GCC with AddressSanitizer and UBSan. The host regression is independent of original-ROM matching.

## Production boundary

**NOT RUN:** canonical current-branch `python3 -m decomp.verify` combining the then-accepted **864 USA C functions** with these new 60, strict `decomp.inventory`, full `decomp.local_ci`, and Japanese regional exact build. The scratch build was against the **untouched pinned upstream** plus these 60 functions, not the complete connected current decomp branch. **Do not increase production counts or edit the canonical manifest** from this report. With current verified USA checkpoint 864, all 60 would yield **potential 924**, not accepted 924. Japan remains separately 39 C as verified by another task.

Potential next integration sequence: reconstruct/authenticate current GitHub branch checkout, stage matched C into existing overlays with all accepted functions, run fresh combined original 32 MiB ROM, ELF/relocation/inventory and full local CI, then promote only if all gates pass. No new fixed USA/Japan saved RAM fields are established by this sweep; dynamic actor offsets are not subject to a guessed fixed-RAM crosswalk.
