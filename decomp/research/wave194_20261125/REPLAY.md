# Wave194 original-ROM native promotion replay

Base `stable/decomp@f16e8f4224501d57359f054bb4e09146ac68f502`, source archive 15009816218, pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Use clean independent regional checkouts, original IDO5.3 and MIPS binutils, private authenticated expanded and retail ROMs, original Splat sources and non-optimized Python. Read `decomp/COMPILER_QUIRKS.md` before every native attempt. No private original binaries or generated assembly are distributed here.

The full USA verifier reconstructs every prior stage, then invokes this one:

```sh
python -m decomp.verify --upstream "$UPSTREAM" --workdir "$USA_WORK" --retail-rom "$USA_ROM" --report "$USA_REPORT" --jobs 5
python -m decomp.inventory --baseline "$USA_BASELINE" --candidate "$USA_WORK/candidate" --report "$USA_INVENTORY"
python -m decomp.promotion_integrity --validate
```

An authenticated immutable baseline cache may be used. For Japan, reconstruct the exact prior JP2664 ELF using the prior adapter `decomp.batch302_promotion` and its predecessors. Copy the verified checkout, retain the independent pristine original Splat tree and invoke:

```sh
python -m decomp.wave194_promotion --region japan_0 --checkout "$JP2664_COPY" --pristine "$JP_PRISTINE" --work "$JP_WORK" --jobs 4
python -m decomp.wave194_promotion
```

Every positive candidate is independently compared with the original assembled function block and its original ROM extent; every altered-source negative must fail. All retained ASM fragment extents and bytes, original expanded and recompressed retail ROM, positive function identities, stable global identities, exact ownership and semantic relocations are checked. The one Japanese local-branch provenance difference has two complete independently assembled original reference links; the omitted-alias control must fail. See `alias_proof.py`; neither native instructions nor relocation records are modified. The globalized predecessor comparison is explicitly unequal; the independently assembled pristine local reference matches the complete native relocation set.

`research-provenance.json` records the prior source-variant hypotheses and original-address replay evidence; `line_grouping_control.c` retains the previous failed source for the reproduced physical-line quirk. The original discovery archive (SHA-256 in that document) retains the full search logs and exact compiler commands. The candidate/negative source manifests and dated native proofs authenticate reconstruction inputs. Use the full required GitHub Actions `Decomp ROM-free regression` on the exact PR revision before merge, not `--quick`. Native validation and ROM-free integrity are distinct gates.
