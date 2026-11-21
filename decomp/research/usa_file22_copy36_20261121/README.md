# Original USA file22 36-byte copy — native exact original-ROM scratch research

**Status: RESEARCH_ONLY. NOT PROMOTED.** `func_801CBF5C_69EB7C` is original file22 guest VMA `0x801CBF5C`, original ROM offset `0x69EB7C`, 60 original MIPS bytes. This file is part of the `static_overlay_1` code slot, **not** a main-segment owner. It copies a 36-byte, 9-word structure to `D_801D7030_6A9C50` using native SGI IDO 5.3 codegen.

## Exact evidence actually run (21 November 2026)

- Original USA retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`. Original decompressed 32 MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Independently rebuilt clean pinned upstream `klorfmorf/mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`: **33,554,432 bytes exact**.
- Candidate original native IDO compiled C: 60/60 instruction bytes exact after correct original-symbol relocation; `R_MIPS_HI16` and `R_MIPS_LO16` two-entry source-relocation pair. Four extra compiler alignment bytes were all zero.
- The original overlay ASM source was separated on either side of this function at the original ROM offset; only zero-filled ELF section tails were trimmed, then prefix + original IDO C + suffix were combined as the original overlay linker input. Scratch *whole-ROM* rebuild: **33,554,432/33,554,432 exact**, all **7,376** positive-size ELF function identities identical, **82,216/82,216** clean-upstream semantic relocation records identical, zero additional aliases.
- Reproduced again via a source-only independent scratch runner; original `.s` and ROM bytes not included in this PR. GCC ASan/UBSan and Clang ASan/UBSan semantic tests each PASS on **256** source patterns.

The clean upstream has 82,216 semantic relocations; the accepted USA1,965 stage has **82,103**. These reflect distinct object/layout sources. **Do not** use the clean upstream count as proof of the accepted-stage relocation gate.

## Source-only reproducibility

Source C and its host test are in this folder. A separate tested `reproduce_file22_clean_upstream.py` script was supplied in the user's ChatGPT handoff ZIP `goemon-usa-decomp-proof-20261121.zip`, SHA-256 `6c99bfad9a72b59661cb09b66bfbc9674708b89ebd98b0305fafd38bbe978a90`. It accepts a pinned *already fully rebuilt* original-USA `mnsg` checkout plus the user's `goemon-dependencies` and `goemon-runtime-additions` directories, copies the complete checkout to an unused scratch path, validates all original boundaries, compiles with IDO, links only the original overlay slot, and asserts complete-ROM/ELF/relocation equality. No private ROM, original ASM, ELF, binaries or toolchain is part of the committed research files.

Host-only test command at repository root:

```sh
gcc -std=gnu99 -O1 -g -Wall -Wextra -Werror -fsanitize=address,undefined -fno-sanitize-recover=all  decomp/research/usa_file22_copy36_20261121/sources/usa_file22_copy36.c  decomp/research/usa_file22_copy36_20261121/tests/test_usa_file22_copy36.c  -o /tmp/goemon-file22-copy36-host
/tmp/goemon-file22-copy36-host
```

## Mandatory pending gates

No current `chatgptweb/decomp` accepted-USA1,965-stage source adapter, no current-HEAD `decomp.verify`, no strict inventory promotion and no full `decomp.local_ci` was executed in this chat host. PR #152's original dispatcher candidate is independently native-exact but remains draft and needs latest combined-source verification. `file22` needs its own verified overlay placement/relocation/translation-unit adapter; using main-segment address arithmetic would be incorrect. Until both exact stage integration and tests pass, **USA accepted count remains 1,965 C / 84,648 bytes**. This is neither a game feature patch nor a native recomp patch.
