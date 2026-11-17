# Consolidated original-address C candidate registry

**Snapshot: 17 November 2026; canonical source commit `bcbf4451f4d2ce2e83af3875d8dbe71b47813b56`.**

The canonical branch remains `chatgptweb/decomp`. The toolkit remains `main`. The two regions have **different** accepted manifests, linker layouts, addresses and full-ROM acceptance gates. Do not create permanent branches per overlay. Short-lived integration branches are acceptable only during a live native batch.

## Current claims, not production promotions

| Region | Accepted C | Accepted code bytes | Pending original-address research | Pending bytes |
|---|---:|---:|---:|---:|
| USA | 731 | 31,932 | 130 | 5,868 |
| Japan revision 0 | 34 | 1,912 | 5 | 180 |

The 130 USA candidates are 82 remaining `file_11` functions (3,512 B), one camera reset (136 B), and 47 functions across seven overlays (2,220 B). The 11 `file_12` spatial/lifecycle functions (748 B) passed fresh combined 731-C G2, ELF relocation, inventory and full Local CI and are no longer in the pending registry. The 374 `file_12` registration wrappers are already accepted and excluded. The five Japanese main-code functions were isolated-exact but not integrated with the 34-C baseline.

**All 135 remaining registry entries remain `RESEARCH_ONLY`, with `canonical_g2=NOT_RUN`.** Earlier native proof tiers describe historical evidence, not a pass against current canonical production. No accepted count, production manifest, or proof file is modified by this registry.

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

Stage every native-exact, nonoverlapping USA candidate together with **all 731 accepted C functions**. Run fresh `python3 -m decomp.verify`, then `python3 -m decomp.inventory` only on success; require full **33,554,432-byte identity**, USA SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, unchanged positive-size original ELF FUNC identities, relocation equality, and no new aliases. Run full `python3 -m decomp.local_ci` with sanitizer coverage; do not treat `--quick` or an Actions run as the full gate.

For Japan, stage five functions atop its **34-C** manifest and run the strict Japan verifier, original source/ELF/relocation ownership, original expanded **32 MiB** SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, and original retail **16 MiB** SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`. Verify its native toolchain separately; never borrow USA ASM or code-address translations.

If a combined build fails, isolate **the failing overlay first**, then bisect candidates in that overlay. Do not perform one full-ROM build per tiny wrapper. Preserve original assembly for failures and keep their source/evidence in the registry. Promote only functions actually passing every required gate, updating C/adapters, the region manifest, combined proof, ELF inventory, candidate ledger, `decomp/CONTINUE.md`, tests and `PROGRESS.md` in the same commit. Refresh the registry's accepted baseline and remove only newly accepted candidates, so no function is counted twice.

## Branch and pull-request retirement

The 45-branch historical audit uses exact original branch HEADs. Candidate C, source Git blobs and native research proofs have been preserved in canonical decomp; no generic merge from a stale old production branch is acceptable. Historical PRs can be closed as superseded by this ledger once all unique files are accounted for; closing a PR is **not** a promotion. Branch deletion requires a GitHub branch-delete-capable interface, a final ref/HEAD check, and no active use by a PR or a contributor. Do not force-push or rewrite the two permanent branches. The toolkit PR #53 targets `main` and is not part of this decomp-native batch.

**17 November 2026 native update:** The uploaded exact canonical checkout and user build archives were reconstructed on Linux. The 11 USA `file_12` spatial/lifecycle functions passed fresh full 731-C native G2, complete 32 MiB ROM equality, all 7,051 original `file_12` relocations, ELF identity inventory and full local CI. These 11 are tracked in `results/usa_file12_spatial_11_promotion_20261117.json` and removed from the pending registry. The remaining 130 USA and five Japan candidates remain research-only until their separate region-wide gates pass.
