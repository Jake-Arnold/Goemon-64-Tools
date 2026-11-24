> **18 Nov 2026 — GitHub publication confirmed (`PASSED_G2_GITHUB_PUBLISHED`):** The locally verified 106-function wide109 promotion below was committed to canonical `chatgptweb/decomp` at [`fd37d519d647e6d35ee8d306de64afcb9ab765e5`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/fd37d519d647e6d35ee8d306de64afcb9ab765e5). GitHub re-fetch verified all 103 intended source/proof/test files by their exact Git blob SHAs; remote manifest and strict inventory confirm USA **1,225 matching C / 52,028 matching bytes / 6,138 ASM remaining**, JP **39 C** unchanged. Full original-ROM G2 and local CI were run for the published source in the preceding local acceptance, **not rerun by this documentation update**. The immutable proof JSON retains its truthful historical pre-publication status. The old research PR #74 must not be merged as an additional promotion.

## 18 November 2026 — USA wide109 deduplicated 106-C production integration (`PASSED_G2_LOCAL`, remote publication pending)

- Matched research PR #74 against the authenticated 1119-C production tree. Three of its 109 C functions / 28 bytes already belonged to the canonical `file_12` stage: `func_80218DF8_5D42C8` (12 B), `func_8021A308_5D57D8` (8 B), `func_8021A4DC_5D59AC` (8 B). Preserved the original acceptance claims and promoted only **106 distinct original functions / 1,200 instruction bytes**, in 68 IDO source units across 15 overlays.
- **Fresh standard native `python3 -m decomp.verify`: PASS, 1225/1225 exact C / 52,028 instruction bytes, 33,554,432/33,554,432 byte-identical USA ROM**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Previous accepted 1119 C were rebuilt unchanged. New ELF linkage retains all original **7,376 positive-sized FUNC identities**, unchanged accepted semantic relocations for 70 overlays, no added C/ASM overlap, and zero positive-sized aliases. The earlier 105 main relocation delta and 14 `file_11` name aliases are historical approved differences, not introduced by this batch.
- **Strict `python3 -m decomp.inventory`: PASS**, 7,376 original functions, 1,225 matching C and **6,138 remaining ASM**. Full `python3 -m decomp.local_ci`: **PASS**, 256 decomp tests (one skipped), 245 verifier/ledger tests, task/evidence validation, GCC ASan/UBSan actual C source tests (including all 68 new translation units with 1,000 host iterations). No game emulator test is claimed.
- Updated manifest, staged fail-closed overlay adapter/source fixtures, verifier, official combined proof, inventory, historical 1119 checkpoints, CI and regression tests in one local source tree. Source/proof hashes and all 106 identities are in `decomp/results/usa_wide109_1225_promotion_20261118.json`.
- **Publication status: LOCAL ONLY / NOT PUSHED.** The native host has no GitHub transport and the connector cannot directly ingest the local tested source. Do not claim `PASSED_G2_GITHUB_PUBLISHED`, update the remote canonical count or merge research PR #74 without first uploading this *exact* tested source bundle and confirming remote source/proof hashes.

**18 Nov 2026 USA file_27 21-function promotion (`PASSED_G2_GITHUB_PUBLISHED`):** Original IDO 5.3 matched 21/21 original-address resource27 C functions (1,316 bytes). Combined all prior 966 C functions, resulting in **987 C / 42,640 instruction bytes**, 6,376 remaining ASM. Native combined 33,554,432-byte USA ROM is byte-identical (SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`); original 7,376 ELF FUNC identities and 876 file27 semantic relocations exact; other overlay relocations preserved; strict inventory PASS (zero unexpected positive aliases). Full local CI PASS: 247 decomp tests (one skipped), 245 verifier/ledger tests, host sanitizers including an actual-source file27 C fixture; Japan unchanged at 39 C. Five 284-byte main graphics candidates remain research-only; four >512-byte reconstructed graphics routines are FAILED_NATIVE. See `decomp/results/usa_file27_adjacent21_987_promotion_20261118.json`, `decomp/research/file27_promotion_20261118/` and `decomp/research/highbyte_search_20261118/continued_probes.json`. **Published and remotely verified on `chatgptweb/decomp` at [commit `ab76a39`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/ab76a397957b5e21df1d6d29dfffaf4c695378fa).**

**18 Nov 2026 verified local USA file_26 promotion (GitHub-published at `ec07c8c`):** 15 C (2,508 bytes) integrated with 951 prior, now 966 USA C / 41,324 original bytes, exact full original 32MiB USA ROM, 7,376 ELF entries, relocations and strict inventory, full local CI PASS. Research queue now has 26 ready candidates (1,600 bytes), unchanged historical 41-queue preserved. Larger-than-512-byte ASM inventory and nonmatching compiler probes are documented in `research/highbyte_search_20261118/`.

**18 Nov 2026 local 951-C promotion proof, pending GitHub publication:** 87 additional original-address USA main/overlay C / 912 instruction bytes passed canonical combined 864+87 native G2, strict inventory, ELF/relocation identity, and local CI. USA = 951 / 38,816 bytes, Japan remains 39. See `results/usa_native87_951_promotion_20261118.json` and `CONTINUE.md`. The 41 separate main graphics / file26 / file27 candidates remain unpromoted and were rebased against 951.

# Consolidated original-address C candidate registry

**Snapshot: 17 November 2026; canonical source commit `bcbf4451f4d2ce2e83af3875d8dbe71b47813b56`.**

The canonical branch remains `chatgptweb/decomp`. The toolkit remains `main`. The two regions have **different** accepted manifests, linker layouts, addresses and full-ROM acceptance gates. Do not create permanent branches per overlay. Short-lived integration branches are acceptable only during a live native batch.

**Superseding regional production update (17 November 2026):** All 82 USA `file_11` registry candidates passed full native 864-C combined ROM, strict inventory and original semantic relocation gates; all five Japanese main-code registry candidates passed full 39-C original native 32/16 MiB ROM, ELF and 80,747 relocation gates. The 87 candidates have been removed from the pending registry and their historical records preserved as `data/candidate_registry_782_pending_20261117.json`. Historical statements below documenting earlier `RESEARCH_ONLY` snapshots remain archival and no longer describe the live registry.

## Current claims, not production promotions

| Region | Accepted C | Accepted code bytes | Pending original-address research | Pending bytes |
|---|---:|---:|---:|---:|
| USA | 864 | 37,904 | 0 | 0 |
| Japan revision 0 | 39 | 2,092 | 0 | 0 |

The three additional original-address USA file_11 routines (104 bytes) passed fresh 782-C complete-ROM, 8,825 file_11 relocation, strict ELF identity and inventory acceptance; they were not in the existing 82-item candidate registry and are now accepted. The 82 USA pending candidates are all in `file_11` (3,512 B). The separate 47-function cross-overlay batch (2,220 B) passed fresh native combined 779-C G2 and is no longer pending. The 136-byte file_11 camera reset has passed fresh combined 732-C USA G2 and is no longer pending. The 11 `file_12` spatial/lifecycle functions (748 B) passed fresh combined 731-C G2, ELF relocation, inventory and full Local CI and are no longer in the pending registry. The 374 `file_12` registration wrappers are already accepted and excluded. The five Japanese main-code functions were isolated-exact but not integrated with the 34-C baseline.

**All 87 remaining registry entries remain `RESEARCH_ONLY`, with `canonical_g2=NOT_RUN`.** Earlier native proof tiers describe historical evidence, not a pass against current canonical production. No accepted count, production manifest, or proof file is modified by this registry.

## Integration with the 1,311-file inventory

`decomp/data/candidate_registry.json` records original expanded-ROM offsets, VRAM addresses, full function lengths, original instruction hashes, source Git blob hashes, old branch heads and proof references. `decomp/data/rom_file_inventory.csv` supplies per-region expanded-ROM boundaries for all 1,311 numbered file slots. A function in `file_12` must lie within that region's *expanded* `file_12` extent; the raw retail ROM offset is not interchangeable. The five Japanese pending functions lie in the **main** executable, not a numbered `file_` overlay.

`decomp/data/rom_file_semantics.json` is an independent partial, evidence-linked description of known file purposes; it is not a source of exact C byte matches. Never map code addresses via the USA/Japan fixed-guest-RAM crosswalk.

## One-pass preflight and two regional full-ROM gates

Before compiling, run:

```bash
python3 -m decomp.candidate_registry
python3 -m decomp.candidate_registry \
  --usa-expanded /absolute/path/to/verified/usa/decompressed.z64 \
  --japan-expanded /absolute/path/to/verified/japan/decompressed.z64
python3 -m unittest tests.test_decomp_candidate_registry -v
```

The optional expanded-ROM check authenticates the complete 32 MiB reference and the original instruction hash for **every** candidate in one read per region. It does **not** prove any C implementation. The registry fails closed on missing or changed source, bad Git blob provenance, duplicate or overlapping original intervals, invalid guest VMA/name, code lying outside its authentic file segment, stale production baseline, or a false promotion status.

Then perform a **single native preflight per region**, compiling all original-address candidates with pinned IDO 5.3 and genuine linker/ASM context. Compare function bytes, exact symbol extents, translation-unit ownership, padding and semantic relocations. The following previously published sources are available without reopening the old topic branches:

- USA `file_11`: existing `decomp/research/file11_adjacent*_sources.json`, native proof ledgers, and the canonical 183-C fixture.
- USA `file_12`: existing `decomp/research/file12_spatial/` C sources and 385/387 research proofs; stage **only the 11 unpromoted functions** against the canonical 374-wrapper implementation.
- USA seven-overlay candidate: `decomp/research/jp_recomp_to_c/src/` and original-address 47-function manifest imported intact from PR #49.
- USA camera reset: original C source plus native file11-only proof imported intact.
- Japan next five: exact isolated C sources and research proof imported intact.

Stage every native-exact, nonoverlapping USA candidate together with **all 779 accepted C functions**. Run fresh `python3 -m decomp.verify`, then `python3 -m decomp.inventory` only on success; require full **33,554,432-byte identity**, USA SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, unchanged positive-size original ELF FUNC identities, relocation equality, and no new aliases. Require the full **Decomp ROM-free regression** Actions job (unchanged `python3 -m decomp.local_ci` with sanitizer coverage) on the current PR merge commit, with the rollout fallback in `AGENTS.md`. `--quick` cannot satisfy the gate and Actions does not replace native G2.

For Japan, stage five functions atop its **34-C** manifest and run the strict Japan verifier, original source/ELF/relocation ownership, original expanded **32 MiB** SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, and original retail **16 MiB** SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`. Verify its native toolchain separately; never borrow USA ASM or code-address translations.

If a combined build fails, isolate **the failing overlay first**, then bisect candidates in that overlay. Do not perform one full-ROM build per tiny wrapper. Preserve original assembly for failures and keep their source/evidence in the registry. Promote only functions actually passing every required gate, updating C/adapters, the region manifest, combined proof, ELF inventory, candidate ledger, `decomp/CONTINUE.md`, tests and `PROGRESS.md` in the same commit. Refresh the registry's accepted baseline and remove only newly accepted candidates, so no function is counted twice.

## Branch and pull-request retirement

The 45-branch historical audit uses exact original branch HEADs. Candidate C, source Git blobs and native research proofs have been preserved in canonical decomp; no generic merge from a stale old production branch is acceptable. Historical PRs can be closed as superseded by this ledger once all unique files are accounted for; closing a PR is **not** a promotion. Branch deletion requires a GitHub branch-delete-capable interface, a final ref/HEAD check, and no active use by a PR or a contributor. Do not force-push or rewrite the two permanent branches. The toolkit PR #53 targets `main` and is not part of this decomp-native batch.

**17 November 2026 native update:** The uploaded exact canonical checkout and user build archives were reconstructed on Linux. The 11 USA `file_12` spatial/lifecycle functions passed fresh full 731-C native G2, complete 32 MiB ROM equality, all 7,051 original `file_12` relocations, ELF identity inventory and full local CI. These 11 are tracked in `results/usa_file12_spatial_11_promotion_20261117.json` and removed from the pending registry. The remaining 129 USA and five Japan candidates remain research-only until their separate region-wide gates pass.

**17 November 2026 camera reset integration:** The original 136-byte `func_801F97D4_5B56E4` in `file_11` passed combined native 732-C G2, full USA ROM identity, all 8,825 `file_11` semantic relocations and strict ELF inventory (7,376 original positive-sized functions, zero extra aliases). See `results/usa_camera_reset_136_promotion_20261117.json` and the pinned 184-C stage fixture. USA now has 732 C / 32,068 bytes; Japan remains 34 / 1,912 bytes. Remaining unpromoted: USA 129 / 5,732 bytes and JP 5 / 180 bytes. Full Local CI including sanitizer tests passed before publication.

**17 November 2026 cross-overlay production integration:** All 47 original-address USA functions across `file_12`, `file_13`, `file_14`, `file_15`, `file_17`, `file_18` and `file_19` have passed the fresh native combined 779-C verifier, full 32MiB ROM exactness, all seven overlay semantic relocation multisets and strict original 7,376-function inventory. The two historically documented main-code ELF size annotations are identical to the accepted 732-C stage, with zero new identities or aliases. The 732-C combined proof remains immutable as `results/combined_732_20261117.json` and inventory `results/inventory_732_20261117.json`; promotion evidence is `results/usa_crossregion47_779_promotion_20261117.json`. Remaining pending: USA file_11 82 / 3,512 bytes, Japan five / 180 bytes. Full Local CI including sanitizer must pass before publication.

**17 November 2026 native file_11 three-function promotion:** A fresh 782-C native original USA ROM is 33,554,432 bytes identical (SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`); strict 7,376-function identity, zero extra aliases, 8,825 file_11 relocations and original seven cross-overlay relocation sets preserved. See `results/usa_file11_three_782_promotion_20261117.json`; 779-C evidence preserved separately. Existing 82 USA and five Japanese research-only candidates remain unchanged.

**17 November 2026 complete registry promotion:** USA 864/37,904 original machine-code bytes, JP 39/2,092 bytes. Region-specific complete ROM/ELF and full relocation evidence: `results/usa_file11_eighty_two_864_promotion_20261117.json`, `results/japan_0_five_39_promotion_20261117.json`. No research candidates remain in the canonical registry; separate prospective research must not be counted until native and inventory proof.
