# USA consolidated 29 original-C promotion

Base `stable/decomp@64e5445b5b044cfd1f841b21c23af81f44da5644`; exact 2325-C predecessor. Source archive artifact 14952568232, upstream pin and original IDO5.3 authenticated. Recovered source from research PRs #198, #192, #195, #189, #183, #191, #160 and the retained regional scheduler sources. Check exact `usa_manifest.json` and source hashes, original ROM offsets and extents. The corrected original scheduler global symbol spelling is retained; previous spelling was a native relocation negative control.

- 29 original functions, 3,372 bytes, 140 named native text relocation records; all 29 independently assembled references and actual compiled source extents match. All 29 one-variable altered-source controls fail the exact native comparison.
- Existing original ABS metadata correction reproduced for `D_801D7030_6A9C50`: uncorrected native ELF has one changed stable global symbol type; restore the exact original undefined-symbol type byte with identity guards, preserving `.text` and all relocation records. Original ROM and native source instructions are never patched.
- Full integrated 2,354-C original 32 MiB ROM and recompressed 16 MiB retail ROM exact, all 7,376 positive function identities, 26,714 stable global identities, 82,080 canonical relocations and strict original-upstream inventory exact. New source ownership is additive. Frozen 2325-C canonical reports are retained unchanged. See `decomp/results/usa_consolidated29_2354_g2_20261124.json`.
- No gameplay test or toolkit change. Fresh full `decomp.verify` exited 0 (2,354 matches); strict inventory and promotion integrity passed. Initial local regression exposed two stale historical test projections, corrected without relaxing proof gates. Required full hosted ROM-free CI on the exact PR merge revision remains pending.

Replay from a fully rebuilt 2325-C native predecessor and the independently authenticated pinned original-USA baseline:

```sh
python3 -m decomp.consolidated_batch_promotion --checkout "$USA2325" --pristine "$USA_ORIGINAL" --work "$NEW_PRIVATE_WORK" --uv "$UV" --jobs 6
```

For a fresh full canonical native run from the pinned upstream, run `python3 -m decomp.verify` with the original retail ROM, new workdir and report, and the canonical manifest; consult `BRANCHES.md`, `AGENTS.md` and `decomp/CONTINUE.md`. No original game assets, ROMs, generated ASM, native objects or proprietary compiler are included.

## Japan consolidated 13 original-C promotion

PR #199 repository-owned source candidates only. Authenticated Japan-0 2551-C native predecessor, exact original expanded and retail ROMs, 7,376 original function identities, 26,393 stable globals, 80,655 semantic relocations, 13 exact source bodies (2,136 bytes, 107 named relocations) and 13 rejected altered-source controls. No ELF metadata corrections. The complete strict inventory is 2,564 C / 141,596 original bytes / 4,812 ASM. The USA promotion #222 does not change the Japan predecessor inputs. Candidate proof and strict inventory are recorded under `decomp/results/japan_0_2564_consolidated13_*`.

Replay from a freshly rebuilt authenticated Japan2551 predecessor and pristine original Japan checkout: `python3 -m decomp.japan_consolidated13_promotion --checkout "$JP2551" --pristine "$JP_ORIGINAL" --work "$NEW_PRIVATE_WORK" --uv "$UV" --jobs 6`. Full ROM-free hosted regression remains required on the exact merge ref. No ROMs, binaries, generated assembly, or proprietary tools are included.
