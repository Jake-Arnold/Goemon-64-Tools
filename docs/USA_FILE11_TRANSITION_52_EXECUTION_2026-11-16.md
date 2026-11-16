# USA and Japan file_11: 52-function scratch result (16 November 2026)

## Purpose and base
This research extends the **formally promoted 50-function** `file_11` stage on PR #20, commit `d394efe7f8a54bff5c60415e466183d4b5de0bd2`, by two additional transition callback functions. The new C source is in `decomp/research/file11_transition_pair.c`. It is research-only; the canonical `overlay_file11_stage` stays at v2/50 and the new functions are not marked as promoted.

## Two new native matches
| Region | Function | ROM offset | Size | Behaviour |
|---|---|---|---:|---|
| USA | `func_801F845C_5B436C` | `0x5B436C` | 44 | Calls helper then installs a callback |
| USA | `func_801F8488_5B4398` | `0x5B4398` | 12 | Empty callback |
| Japan | `func_801FD364_5B9334` | `0x5B9334` | 44 | Regional equivalent |
| Japan | `func_801FD390_5B9360` | `0x5B9360` | 12 | Regional equivalent |

Both new functions compiled with pinned IDO 5.3 and matched each region's original instruction bytes at original VMA. The Japan complete-ROM build remains blocked by upstream `GLOBAL_ASM` region paths.

## Native USA 52-function rebuild — exact
1. Verified original USA and Japan retail inputs and decompressed both into authenticated 32 MiB images.
2. Reproduced the original USA 32 MiB image from pinned `mnsg` source `7e2029c5`.
3. Revalidated both new functions under the original-address IDO/MIPS link for USA and Japan.
4. Reconstructed PR #20's six existing C files; each SHA-256 matched its pinned repository source.
5. Built an independent two-function USA C/ASM overlay, preserving the 32 MiB original ROM.
6. Built a **14-link-chunk** scratch `file_11` containing all prior 50 functions plus the two new ones.
7. Enforced text sizes/4-byte subalignment; corrected only two synthetic Splat padding labels, not machine instructions.
8. Proved byte-for-byte USA ROM identity: 33,554,432/33,554,432 bytes and SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
9. Audited 52 original-VMA function-symbol identities (1,120 matching bytes), a constant 7,376-entry inventory, and **8,825/8,825 relocation tuples**.
10. Ran 12 fail-closed research tests and five repository metadata/claim-guard tests; published source and metadata without changing canonical promotion results.

The 52-function scratch ELF has **two exact three-record relocation-order cycles**, at indices `2506–2508` and `6131–6133`. All relocation sites, types, symbol names and resolved targets are identical as a multiset. **Raw relocation order is not identical.** Do not report this as an unmodified ordered-ELF match.

Original baseline has 7,376 identified positive-size functions and 13 C; independent scratch has the same 7,376 entries and 65 C (= 13 upstream + 52), with precisely the expected 52 ownership changes. The `file_11` overlay size remains `0x41400`.

## Reproduction and stop gates
The private source-only reproducibility package is retained in the project conversation as `goemon-file11-52-research-20261116.zip`: 14-chunk stage script, ELF text trimmer, ROM/ELF/symbol/relocation auditor, 12 research tests, C source pins, regional native pair probe and a 52-function hash report. No ROM, generated assembly, compiler, object, savestate or ELF is committed.

**Still required for production:** add a separate v3 `file_11` stage that preserves the existing v2's 50-function proof and incorporates these two C functions. Run a **single central 212/212 full-ROM G2**, complete 52-function relocation and original symbol gate, and reconciled inventory before updating canonical manifest/combined proof. Target: 212 newly matched C / 13,392 bytes / 7,151 assembly entries. These are targets, not completed promotion results. Do not reinterpret isolated Japan function matching as Japanese full-ROM verification.

The existing PR #20 proves 210/210 on its own promoted branch. Its base `chatgptweb/decomp` is not implicitly updated by this research branch.
