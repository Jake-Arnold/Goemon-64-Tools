# USA 389 matching-C native integration checkpoint — 17 November 2026

**Status: native original-ROM/ELF acceptance PASS; formal canonical promotion and current full local CI PENDING.**

The live `chatgptweb/decomp` production branch moved from **315** to **342** USA matching-C functions during the continuation work, by independently adding **27 `file_11` C functions / 908 bytes**. This is already published production work and must not be counted a second time. This research adds **47 distinct, previously unpromoted C functions / 2,220 original MIPS instruction bytes**, in overlays `file_12` (5), `file_13` (15), `file_14` (8), `file_15` (2), `file_17` (1), `file_18` (9) and `file_19` (7). Japan's separately published 34 original Japanese C functions are not part of these USA totals.

## Actual native build and proof

The prior 315-C native source reconstruction (saved user Library stage fixture + pinned IDO and sources), with 47 cross-region matching-C overlays, already passed the full original USA ROM. This pass **then integrated exactly the 27 additional C sources from the live canonical 179-function file_11 fixture**, preserving the previous 362 linked C code. All 27 C sources and packed MIPS object SHA-256s were independently compared with the **official current production fixture** `decomp/research/file11_143_candidate/file11_179_source_fixture.json` (Git blob `a36d7cde46eb7779d85ea168151f536e5b5a5157`).

The resulting **389-C native candidate** passed:

| Gate | Actual result |
| --- | --- |
| Complete USA ROM | **33,554,432/33,554,432 bytes exactly original** |
| USA ROM SHA-1 | `6ea0ed71032ce08fc2745f412d84936382197494` |
| Distinct source-owned C identities | **389 / 389** |
| Total source-owned C instruction bytes | **19,788**, of which **2,220** are the new 47 |
| Original ELF positive-sized function identities | **7,376**, all preserved |
| ELF functions relative to current 315-C anchor | Names, VMAs, sizes and sections **exact** |
| Original ASM unmarked vs candidate unmarked | **13 → 402** (389 additional) |
| Remaining assembly function entries | **6,974** |
| Original `file_11` semantic relocs | **8,825 / 8,825 exact** |
| Original `file_12` semantic relocs | **7,051 / 7,051 exact** |
| Original `file_13` semantic relocs | **9,589 / 9,589 exact** |
| Original `file_14` semantic relocs | **3,041 / 3,041 exact** |
| Original `file_15` semantic relocs | **1,625 / 1,625 exact** |
| Original `file_17` semantic relocs | **1,739 / 1,739 exact** |
| Original `file_18` semantic relocs | **3,365 / 3,365 exact** |
| Original `file_19` semantic relocs | **1,078 / 1,078 exact** |
| Complete candidate linked ELF SHA-256 | `c3f6ba01b4438ac7b08bdaa5b8d01d2a687512f01d86977f82a34e1f2b423c71` |
| Host ASan/UBSan display-emitter test | **PASS** — 1,000 synthetic plus zero/alias cases |

The built-in `decomp.inventory.summarize_inventory` function passed the complete 389-name ownership list and its original 7,376-entry ELF audit with **zero extra positive-sized aliases** and `function_entry_identity_sha256=01f41037ac83f6e18e80c83489a18b870e4fef907c67d20a345871c7c34fe787`.

Two pre-existing, approved original-to-production C size annotations remain unchanged: `func_8000D3B8_DFB8` **64→72 bytes**, `func_8003F6E8_402E8` **48→56 bytes**. No additional symbol-size changes were introduced by the 47.

One failed earlier link attempt had duplicate ASM functions because obsolete original ASM objects remained referenced from the `file_12`/`file_13` data/rodata/BSS output lists. Each such ELF section was verified to have **size zero** before those stale input-object references were excluded; the resulting linked executable is exactly the original. Other canonical objects and data were never omitted. The 179-C `file_11` split likewise verified zero original section payloads and used the original 152-C stage's already-verified object extents.

## Source and CI limitations

The 389-C candidate was constructed using real original-ID0 compiled sources and manually reviewed original-Splat linker staging; **the unchanged production `decomp.verify` does not yet contain a versioned 47-overlay stage, nor a 389-function manifest**. The official USA production remains **342-C**, not 389.

The fully connected current source checkout is not accessible to native Linux `git clone` in this isolated environment, so the only local source ZIP is from **14 November** and required hash-verified individual source updates. The unchanged `decomp.local_ci` entrypoint from this older checkout failed on stale tests (an obsolete `stage_file11_splat` import and outdated source/evidence SHA expectations), not on the new 47 native code; the current full local CI has **not passed or been claimed**. The separate ASan/UBSan display-emitter host gate passed.

Formal production requires a versioned **342+47 original-address mixed C/ASM verifier stage**, fail-closed original source/object/link provenance, complete current-source ROM-free `decomp.local_ci`, `decomp.verify` original-ROM G2, and original `decomp.inventory` in the same combined checkout. Only then update current `decomp/manifest.json`, `decomp/results/combined.json`, `decomp/results/inventory.json`, and the canonical 342→389 counter. Prior proofs must remain immutable.

**Reproducer (original ROM/compiler/assets excluded):** user-delivered `goemon_389_native_integration_20261117.zip` (SHA-256 `f916f45824a137884829a9ea451f1d2402f1184f60276c5604dbdd39f7a21bca`), with reconstructed source-stage scripts, 27 canonical source hashes/object proofs, original-ROM inventory/relocation verification script, and full JSON evidence. Only this document, machine-readable numeric proof and source-only regression test are committed here; no ROM/ELF/object/proprietary compiler/game asset is checked into Git.
