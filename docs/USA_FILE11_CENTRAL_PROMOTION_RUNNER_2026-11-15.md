# USA `file_11`: formal 50-function promotion gate (15 November 2026)

## Current proven baseline and blocker

The canonical `chatgptweb/decomp` manifest and `results/combined.json` currently record **160 functions / 12,272 matching bytes**, with a complete original-USA ROM match. The original Japan Project64 character-switch work led to **13** native original-address character-switch C reconstructions (620 bytes), and the adjacent USA `file_11` research established **37** additional 12-byte empty callback functions (444 bytes). Their combined **50-function, 1,064-byte** staged USA `file_11` overlay has been rebuilt byte-for-byte to the verified 33,554,432-byte retail-derived USA ROM, including all **8,825** relocation records and original linked function identities. See `USA_FILE11_NOOP_CALLBACKS_2026-11-15.md` and `file11_noop_v2_clean_reproduction_20261115.json`.

**This does not automatically promote the 50 functions.** A *single central build* must apply the opt-in `goemon-file11-character-switch-50-v2` stage **together** with all 160 already-promoted C functions and their other overlay stages, then prove a complete original ROM match, file_11 relocation/symbol provenance, and a reconciled inventory. The private `Goemon-64-Tools` GitHub source tree is connected through the GitHub API but not mounted into the isolated Linux container as a local checkout. The pinned upstream source ZIP and ROMs are mounted, but the entire 160-function C source bundle is not present locally. Therefore that final combined G2 was **not run**, and the canonical manifest/proof/inventory must remain unchanged.

## Promotion runner

`decomp/promote_file11.py` implements a strict, non-destructive promotion review gate. It creates a separate temporary manifest from the canonical 160-function manifest and adds only:

```json
"overlay_file11_stage": {"format": "goemon-file11-character-switch-50-v2"}
```

It invokes the existing central `decomp.verify` on a **new workdir**, then `decomp.inventory` on the candidate ELF. The promotion review bundle is emitted only if all of the following hold:

- Full 33,554,432-byte original USA ROM hash `6ea0ed71032ce08fc2745f412d84936382197494` and complete 210/210 matching functions / 13,336 bytes.
- All 50 original file_11 function names, ROM offsets, VMAs, exact sizes and SHA-256 instruction digests; the previously existing 160 function comparison rows also have matching status.
- Complete 12-object `file_11` linker ownership; 8,825 original semantic relocations, identical in order; exact original 50-function IDO source/object evidence via the v2 adapter.
- Fresh inventory containing 7,376 identified entries, 210 newly matching C functions plus 13 upstream unmarked entries, and 7,153 assembly entries remaining.

The runner writes only to an untracked **external output folder** and its newly created build workdir. On any failure it rejects promotion, retains evidence/logs, never mutates the canonical manifest or published proof, and never increments official counts. The review bundle is an **acceptance candidate**, not an automatic Git commit.

### Command on Linux with complete GitHub checkout and pinned build inputs

From the `Goemon-64-Tools` checkout root (not the upstream `mnsg` checkout):

```bash
python3 -m decomp.promote_file11 \
  --source-dir ./decomp \
  --upstream /path/to/clean/pinned/mnsg-japan \
  --retail-rom "/path/to/Mystical Ninja Starring Goemon (USA).z64" \
  --workdir /tmp/goemon-central-file11-v2-new \
  --output-dir /tmp/goemon-central-file11-v2-review-new \
  --uv /path/to/uv --jobs 2
```

Optional `--baseline-cache /path/to/certified/baseline` can reuse an immutable, previously verified original-ROM baseline. Optional `--binutils-root` supports isolated curated cross-binutils. The complete original IDO toolchain is supplied by the pinned upstream checkout. Both output paths must be new and outside the checked-out repository. Prior to canonical promotion, run `python3 -m decomp.local_ci`, inspect the complete `PROMOTION_REVIEW.json` and provenance, then commit only the sanitized manifest, proof, inventory, code and dated progress update in a reviewed production branch. Never commit ROMs, generated assembly, proprietary tools or ELF objects.

## Tests actually run in this session

64 **ROM-free Python research and promotion acceptance tests** pass using `PYTHONPATH=.` from the local research workspace. They include failures for old 160-only or scratch 50-only reports, wrong ROM, missing function names, changed 50-function original VMA/code hash, changed relocation count/order, insufficient inventory, duplicate stage, and attempted output reuse. The earlier complete native 50-function USA scratch ROM SHA-1 was independently checked against the supplied verified original. **No complete central 210-function run or inventory reconciliation was executed in this session.**
## Formal native promotion completed — 16 November 2026

The one-shot promotion runner was executed with the authenticated USA retail
ROM, original IDO 5.3, a fresh pinned upstream checkout, and a certified
independently exact native baseline. Central G2 passed **210/210 C functions,
13,336 native function bytes, 33,554,432 exact ROM bytes**, SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`. The **8,825** file_11
semantic relocations matched in site, type, target and symbol; the only
record-order difference was the exact three-item permutation at indices
2506–2508, now explicitly whitelisted by identity and count. Splat's two
synthetic 4-byte nop function aliases were removed from generated ASM labels,
retaining all instruction bytes and original NON_MATCHING markers. Inventory
then passed: **7,376 original functions, 223 combined C and 7,153 ASM**.
The real central verifier and inventory were recorded in
`decomp/results/combined.json` and `decomp/results/inventory.json`, with the
hash-bound acceptance summary in
`decomp/results/file11_central_promotion_20261116.json`. Full ROM-free local CI
passed 216 decomp Python tests (one skip), 133 verifier/ledger Python tests
(four skips), task-evidence validation and a C ASan/UBSan display-emitter test.

**The canonical 210-function manifest now enables this original v2 file_11
stage.** The one-time promotion script intentionally refuses manifests that
already claim file_11. For subsequent new original-ROM proofs, run the normal
`python3 -m decomp.verify` plus `python3 -m decomp.inventory` pair instead.
The full Japanese ROM remains independently blocked by USA-specific upstream
assembly source paths; the 180-byte USA character selector remains ASM.
