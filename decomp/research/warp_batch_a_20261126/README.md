# Goemon warp reconstruction — Phase 1 Batch A native verification

26 November 2026. PASSED_G2_LOCAL — private canonical promotion candidate, not published. Authenticated live `stable/decomp` commit `ee6328ab121bb59b27f03a54c3c80563a720fe77`, source artifact 15127952620; pinned original upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. The current canonical source-integrity validators passed (USA 3056, JP 2995). The exact original regional predecessor builds were independently reproduced.

Nineteen distinct original functions (USA 10 / 1548 bytes; Japan 9 / 1496 bytes), 76 named relocations: 19 positive exact native IDO objects and original-address linked ROM comparisons; 19 altered-source controls rejected. Twelve positive/negative source pairs match the exact research PR blobs (#276, #279, #280); four additional object initializers were split from two authenticated combined sources; seven fresh negative controls were generated. All 38 compile attempts read the compiler ledger and record NO_NEW_COMPILER_FINDING. `isolated-replay.json` contains flags, fingerprints, mismatch offsets and results. Seven complete original text owners were independently assembled and linked, then rebuilt with the selected C and unchanged original ASM. All 149488 original text bytes, 1061 positive FUNC identities and 5210 semantic relocations match. Initial owner replay failed on two unresolved jump-table symbols; independently generated original data assembly provided the symbol names and addresses; final replay passed. These are complete text-owner checks, not a proof of original historical source layout or whole-ROM data/rodata integration.

`dedup.json`: all 3056 USA accepted reconstructed ranges and 13 additional upstream names checked, all 2995 Japanese accepted names checked, 2993 resolved Japanese original ranges checked, no overlap. Two JP names lacked a resolved original Splat range. Principal pending PR #250 manifests checked; the known overlapping candidate 0x800374AC was excluded. Additional principal pending PR manifests #194, #199, #200 and #202 were checked with no new overlap; an exhaustive historical pending manifest audit was not performed.

## Reproduce

Read live `BRANCHES.md`, `AGENTS.md`, `decomp/CONTINUE.md`, autonomous skill, executor protocol and compiler quirks; reauthenticate exact live source before proceeding. Use private pinned original ROMs and toolchain and independently extracted regional Splat checkouts. See repository `GOEMON_BUILD_ENVIRONMENT.md`. No proprietary inputs are distributed in this archive. From canonical repo root, with the original MIPS cross-binutils on PATH and native toolchain dependencies configured:

```sh
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
python3 "$KIT/replay.py" --repo "$PWD" --usa "$USA_ORIGINAL_SPLAT" --jp "$JP_ORIGINAL_SPLAT" --work "$PRIVATE_ISOLATED_WORK"
python3 "$KIT/owner_replay.py" --usa "$USA_ORIGINAL_SPLAT" --jp "$JP_ORIGINAL_SPLAT" --isolated "$PRIVATE_ISOLATED_WORK" --work "$PRIVATE_OWNER_WORK"
```

`prepare.py` regenerates the archived sources and original manifest, including their research-source Git blob fingerprints. The two regional candidate manifests additionally pin original ROM offsets, extents, original-code/source SHA256 and flags. `integration_trial.py` is a **successfully executed** adaptation of the existing Ebi Slide9 canonical integration trial; it retains the exact predecessor and original reference gates and uses existing canonical owner stagers and finish checks. It requires the exact canonical predecessor and provides fresh native G2 proof when all checks pass. For example:

```sh
python3 "$KIT/integration_trial.py" --region usa --checkout "$USA_CANONICAL_PREDECESSOR_COPY" --pristine "$USA_ORIGINAL_BASELINE" --original-reference "$USA_ORIGINAL_SPLAT" --manifest "$KIT/usa-candidates.json" --work "$USA_NEW_TRIAL" --uv "$UV" --jobs 4
python3 "$KIT/integration_trial.py" --region japan_0 --checkout "$JP_CANONICAL_PREDECESSOR_COPY" --pristine "$JP_ORIGINAL_SPLAT" --original-reference "$JP_ORIGINAL_SPLAT" --manifest "$KIT/japan_0-candidates.json" --work "$JP_NEW_TRIAL" --uv "$UV" --jobs 4
```

Full predecessor reconstruction is required, including all prior canonical stages. USA uses `python3 -m decomp.verify`, Japan follows the chain in `decomp/CONTINUE.md` and `decomp/research/cright_promotion_checkpoint_20261124/replay_jp6_from_2118.sh` and subsequent native stages through `decomp.ebi_slide9_promotion`. Expected canonical USA3056 ELF SHA256 `62558a4650f2609eda0ab1bfc7d654bf752f4f7af796fe0e04e0ec645527d51e`; JP2995 `f37be891f83ad2d9fc6b52bc8b6ffd31add7550a8458f403a54daa8e30b33b0d`. Both fingerprints were reproduced by the private native rebuild. Do not substitute the intermediate predecessor checkpoints for them. `checkpoint.json` records actual completion status.

Both regional candidate G2 trials passed original expanded and recompressed retail ROM, complete ELF identity/relocation/ownership and strict inventory. The atomic promotion-integrity transaction and full hosted ROM-free regression on the current PR remain mandatory. Keep the 19 functions ASM-owned until every applicable gate passes. No gameplay or toolkit claim. Do not commit private inputs, generated binaries or extracted original assembly.

## Native acceptance receipts

- usa: 10 positive objects and controls, 7376 positive FUNC identities, 82080 semantic relocations and 26714 stable globals unchanged; candidate ELF SHA256 `1107b0f4d2d7eaf17107323ae5119076476a773aabba01f77d27113353abb6ff`. 4 original ABS metadata restorations with unchanged instructions and relocations. Dated native proof: `decomp/results/usa_warp_batch_a_g2_20261126.json`.
- japan_0: 9 positive objects and controls, 7376 positive FUNC identities, 80652 semantic relocations and 26393 stable globals unchanged; candidate ELF SHA256 `8b62b85eb9e32bc5b499017ac882c54e34ad666bdd47f3cd3867d36477935b0d`. 2 original ABS metadata restorations with unchanged instructions and relocations. Dated native proof: `decomp/results/japan_0_warp_batch_a_g2_20261126.json`.

No new general compiler quirk or gameplay claim.
