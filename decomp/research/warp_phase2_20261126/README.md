# Warp phase 2 — six floating-point initializers, dual-reference research

**Status: LOCAL_DUAL_REFERENCE_EXACT_PENDING_CANONICAL_VALIDATOR.** Not a canonical promotion. No modification to a manifest, production comparator, canonical proof, toolkit, or original game data is proposed by this research checkpoint.

Authenticated stable/decomp `8b195d8ce5a31723a71af428ee4f7bccf32b0bf8` (source artifact 15142908886, preceding hosted CI 45873014074 passed); pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Reused the exact private Batch A predecessor build trees, independently authenticated their ELF digests against the current canonical proof and checked their expanded images against the original ROMs. Shell Git DNS unavailable. Live canonical ownership remains USA 3066 / JP 3004. Six new targets remain assembly-owned in canonical source. Phase 1 Batch B is deferred.

| USA | Japan | Bytes per region | Previous best | Native linked words |
|---|---|---:|---:|---:|
| func_802150E4_5D05B4 | func_80219E74_5D5404 | 128 | 30/32 | 32/32 |
| func_80215164_5D0634 | func_80219EF4_5D5484 | 120 | 28/30 | 30/30 |
| func_802157C4_5D0C94 | func_8021A554_5D5AE4 | 108 | 24/27 | 27/27 |

Earlier selected best sources were not available; recreated named-global variants independently reproduce the reported word counts, not their source hashes. Six original IDO literal forms and six alternate literal/local forms reproduce all 178 linked words, six extents and their original four-byte floating constants. Native object reference tuples: 48 total, of which 12 HI/LO records use local `.rodata` instead of the original Splat names. The strict named reference intentionally remains unequal to native. Independently assemble the original named form and a local-label form using the original Splat text/data (not generated native data). All original reference text and local relocation tuples match; 24 negative controls rejected (six changed C constants, six wrong pool words, six wrong pool addresses, six wrong addends). Existing literal pool quirk reproduced; no claim of a new general compiler rule. Initial sweep 36 distinct C variants, then six distinct altered constants (42 source variants); replay records exact flags and hashes. Initial diagnostic link incorrectly aligned local pools; rejected, then replayed with original placement.

## Full native trial

Each regional overlay data owner is split around three original four-byte float slots. Independently check every retained raw data byte and all 3160 USA / 3149 JP input data relocation identities; preserve original global labels and extents, trim authenticated trailing zero padding only, express final-fragment alignment relative to the original guest address. Initial splits failed assembler alignment checks; later named reference links succeeded but the initial inventory assertion incorrectly required original ASM references to lose their ASM markers. Corrected diagnostic assertions require reference markers unchanged and exactly three native markers removed. The ordinary comparator is unmodified. All three complete regional images (named reference, local shadow, native) equal the original expanded ROM and original function/global identity sets. Recompressed native images equal original retail ROMs. Full named relocation multiset equals the exact predecessor, full native multiset equals the independent local shadow. Exactly six HI/LO named records removed and six section-relative records added per region; position/type preserved, resolved original instructions/data exact. Existing guarded USA zero-sized ABS metadata restoration only. No instruction, data payload or relocation record patched. Candidate strict ownership delta three per region; no extra positive aliases or size annotation changes against exact predecessors.

Canonical projection only: USA 3069 C / 210992 bytes / 4294 ASM (3082 C including 13 upstream); Japan 3007 C / 201356 bytes / 4369 ASM. Before acceptance implement additive canonical dual-reference validator and production replay path, retain frozen predecessors, independently verify strict canonical inventory, both promotion-integrity validators, current full hosted regression and branch routing. No new gameplay or toolkit claim. Do not count these functions as canonically promoted.

## Private replay

Requires authenticated base repo, pinned original upstream with both privately supplied and extracted original ROMs, native IDO 5.3, pinned cross-binutils and dependency environment (see project instructions), exact current canonical predecessor builds, and pristine original USA ELF for guarded metadata restoration. No ROM, original ASM, compiler or object binaries included. Run from repository root with `PYTHONPATH` set to that root. All assertions must be enabled; no `python -O`. Work directories must be new except `finish_trial.py`, which resumes an interrupted trial with the same inputs and authenticates saved linked ELF fingerprints before comparing them.

```sh
K=decomp/research/warp_phase2_20261126
python "$K/replay.py" --repo "$PWD" --usa "$USA_ORIGINAL" --jp "$JP_ORIGINAL" --work "$WORK/probes" --sources "$PWD/$K/sources"
python "$K/pool_reference.py" --repo "$PWD" --usa "$USA_ORIGINAL" --jp "$JP_ORIGINAL" --work "$WORK/pools"
python "$K/integration.py" --repo "$PWD" --region usa --predecessor "$USA_PREDECESSOR" --original "$USA_ORIGINAL" --pristine "$USA_PRISTINE" --work "$WORK/usa" --uv "$UV" --pool-proof "$WORK/pools/pool-proof.json"
python "$K/integration.py" --repo "$PWD" --region japan_0 --predecessor "$JP_PREDECESSOR" --original "$JP_ORIGINAL" --pristine "$USA_PRISTINE" --work "$WORK/jp" --uv "$UV" --pool-proof "$WORK/pools/pool-proof.json"
```

`evidence/` includes historical initial and corrected sweeps, independently assembled pool proof, failed integration attempts and complete regional trial records. Source paths in historical evidence are diagnostic local paths; select source files by name/hash. The earlier isolated records explicitly say full G2 NOT_RUN at that stage; the final regional records provide subsequent full local dual-reference trial evidence, not canonical promotion.
