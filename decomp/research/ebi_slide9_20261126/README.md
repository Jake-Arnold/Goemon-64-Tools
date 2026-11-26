# Nine Ebi Slide candidates — native replay and promotion checkpoint

**PASSED_G2_LOCAL — private canonical promotion candidate, not published.** Live source commit `9932e4bac45bd3f41513b2f6ff0eb8ee438d0997`, archive artifact 15074968037; original upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. The previous research candidates from #268, #270 and #272 were retrieved and authenticated individually against their Git blobs. The nine exact source variants and nine deliberately nonmatching controls are unchanged. The current native replay used the original pinned IDO 5.3 and cross-binutils, with original Splat-derived references authenticated at their region-specific ROM offset and VMA. All nine positive object comparisons and all nine negative control rejections passed; 4,020 bytes and 169 named relocations. See `isolated-replay.json` and the manifests for flags, source/original-code fingerprints, compiler ledger fingerprint, extent and control evidence. No new compiler workaround was invented. The current canonical integrity checks passed, independently of these candidates. Pending #250 candidates did not overlap these functions.

## Reproduction

Use the current repository runbook, project build environment, original user-owned regional ROMs, and original pinned upstream. Check the live `stable/decomp` SHA and all predecessor digests in `checkpoint.json` before any native integration. If the base changed, reconcile and reverify the affected stages. This kit is based on the stated commit and is not automatically suitable for a later commit. Run from that repository root with its Python dependencies and cross-binutils on PATH; set `KIT` to the extracted kit's absolute path, and provide separate original regional Splat reference checkouts. All work directories must be new private directories. Do not copy native generated files into the repository.

```sh
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
python3 "$KIT/replay_isolated.py" --repo "$PWD" --source "$KIT/sources" \
    --usa "$USA_ORIGINAL_SPLIT" --jp "$JP_ORIGINAL_SPLIT" --work "$NEW_ISOLATED_WORK"
```

The full USA predecessor is obtained using `python3 -m decomp.verify` as documented in `decomp/CONTINUE.md`; preserve the baseline and verified candidate. Japan uses the published predecessor build chain, including `decomp/research/cright_promotion_checkpoint_20261124/replay_jp6_from_2118.sh` and each subsequent native stage, through `decomp.promo65_promotion`. Both predecessor ELFs must match the pinned fingerprints, and both expanded and retail ROMs must be authenticated. Never use a partial predecessor as a substitute. See `checkpoint.json`.

Run the following on a **copy of a verified regional predecessor checkout**. For USA, the pristine reference must also contain the separately verified original baseline ELF. For Japan, use the independent original upstream Splat reference (original source layout). This integration driver is adapted from the canonical Promo65 stager and preserves existing ASM siblings and padding; it refuses a wrong predecessor and invokes the full original-ROM/ELF/relocation/inventory gates. Both regional invocations passed in this session; see the dated G2 records.

```sh
python3 "$KIT/attempt.py" --region usa --checkout "$USA_PREDECESSOR_COPY" \
    --pristine "$USA_ORIGINAL_BASELINE" --original-reference "$USA_ORIGINAL_BASELINE" \
    --manifest "$KIT/usa-candidates.json" --work "$NEW_USA_TRIAL" --uv "$UV" --jobs 8
python3 "$KIT/attempt.py" --region japan_0 --checkout "$JP_PREDECESSOR_COPY" \
    --pristine "$JP_ORIGINAL_SPLIT" --original-reference "$JP_ORIGINAL_SPLIT" \
    --manifest "$KIT/japan_0-candidates.json" --work "$NEW_JP_TRIAL" --uv "$UV" --jobs 8
```

Do not promote unless the actual current predecessor, every native function/owner, complete expanded and recompressed retail ROM, all original positive FUNC identities, stable globals, all semantic relocations and strict inventory pass. Apply the complete atomic canonical transaction and current hosted full regression/branch routing check before merging. Record and verify the remote new commit and post-merge artifact. No original ROMs, extracted original ASM, toolchains, or compiled binaries are distributed in this source-only kit.

## Native integration outcome

USA 4 and Japan 5 integrated, exact expanded and retail ROM equality, complete ELF identity and semantic relocations, strict inventory and candidate integrity validators passed. USA input ABS type restorations are guarded by exact original provenance and unchanged code/relocation bytes; five records. Full original-baseline USA inventory matches the candidate transaction. Full predecessor verifier and additive candidate replay executed separately. Full hosted regression and routing are still required.
