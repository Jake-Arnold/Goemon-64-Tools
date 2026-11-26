# Promo36 — original native C promotion candidate

Authenticated base `ad5c02dbba2a82ac37e94184c5aa82d53bb5561f`, source archive 15020042724 (COMMIT and SHA256SUMS verified), upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, pinned IDO 5.3. Both regional pristine original ROMs are authenticated. Rebuilt the full USA2939 production verifier and independently replayed the full JP2842 chain before adding the 21 and 15 new original-address C owners. Native trials, exact ROM/ELF/relocations, 36 negative controls, strict inventory and both canonical integrity validators passed. The historical original translation-unit layout and live gameplay are not proven. Artificial C/ASM split owners retain original boundaries and padding. Source-only; no proprietary ROM/toolchain, generated original assembly, or objects.

## Reproduction

Follow `AGENTS.md`, `BRANCHES.md`, `decomp/CONTINUE.md` and read `decomp/COMPILER_QUIRKS.md` before native attempts. Using the original authenticated private ROM and pinned toolchain, the new USA adapter is called by the production verifier after its original predecessor:

```sh
python3 -m decomp.verify --upstream "$USA_UPSTREAM" --workdir "$USA_WORK" --retail-rom "$USA_ROM" --report "$USA_REPORT" --jobs 8
python3 -m decomp.inventory --baseline "$USA_WORK/baseline" --candidate "$USA_WORK/candidate" --report "$USA_INVENTORY"
```

For Japan independently replay the preceding stages to the exact JP2842 predecessor per the retained repository replay instructions. Original per-function Splat references must be present in the pristine checkout (including original ROM-generated `wave_uty.s` and `main_4D70.s` for the earlier JP2534 stage). Then:

```sh
python3 -m decomp.promo36_promotion --region japan_0 --checkout "$JP2842_CHECKOUT" --pristine "$JP_ORIGINAL_SPLAT_CHECKOUT" --work "$JP36_WORK" --uv "$UV" --jobs 8
```

Both regions can independently replay the isolated original object comparison with `python3 decomp/research/promo36_20261125/isolated_replay.py --region usa --pristine "$USA_PRISTINE" --work "$ISOLATED_WORK"` (substitute `japan_0` and JP pristine as appropriate, with repo root on PYTHONPATH). The fresh integrated trial is `attempt.py` from this folder, invoked by the canonical adapter with exact predecessor ELF, original ROM and source manifest. It rejects any unexpected source, object, ownership or relocation mismatch. `python3 -m decomp.promotion_integrity --validate` and `python3 -m decomp.promo36_promotion` check the stored canonical transaction. Full hosted regression is required before merge; local full suite intentionally not duplicated.
