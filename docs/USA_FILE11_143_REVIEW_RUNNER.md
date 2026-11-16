# One-command 303-C review: USA file_11 143-C candidate

Status: **Native 303/303 original-ROM G2 passed on user Ubuntu (16 Nov 2026); initial inventory blocked by a Splat-created four-byte NOP FUNC at 0x5AEBDC.** This branch now normalizes that exact generated annotation before ELF assembly and repairs the VM source-hash ledger. The full fixed 303-C review (fresh G2, inventory, complete local CI) must be rerun; canonical production count remains 210. This is an opt-in companion to `USA_FILE11_143_CENTRAL_PREFLIGHT_2026-11-16.md`.

From a **complete private repository checkout** at PR #32's head, with the pinned upstream source, original USA retail ROM, original IDO, portable Python/Splat and MIPS binutils:

```bash
python3 -m decomp.review_file11_143 \
  --source-dir decomp \
  --upstream /absolute/path/to/pinned/mnsg-japan \
  --retail-rom "/absolute/path/to/Mystical Ninja Starring Goemon (USA).z64" \
  --workdir /tmp/goemon-303-central-unique \
  --output-dir /tmp/goemon-303-review-unique \
  --jobs 8
```

Optional flags: `--baseline-cache /absolute/path/to/certified/baseline`, `--binutils-root /absolute/path/to/pinned/binutils`, `--uv /path/to/uv`. New and separate work/output directories are mandatory and must be outside both repositories. The runner writes a separate trial manifest and never modifies `decomp/manifest.json` or canonical results.

The tool runs a native full-ROM `decomp.verify`, audits every reported function and 143-C original-object/relocation proof, runs `decomp.inventory` against the pinned original function-identity checksum and zero unexpected aliases, then executes full `decomp.local_ci`. Only after all commands succeed does it create `REVIEW.json` with `ready_for_human_review`. Logs and reports are kept in the output directory even on failure; a failed run never creates the acceptance file. A passing acceptance bundle still requires review before any formal promotion.

User's initial native run (2026-11-16) established all 303 matching C functions, 16,180 instruction bytes, 143 file_11 C functions, 88 object source slots, 8,825 semantic relocations, and an exact 32 MiB USA ROM. The inventory then found 7,377 candidate positive-sized symbols versus 7,376 baseline, with exactly one extra `func_801F2CCC_5AEBDC` at the assembly split after two 12-byte callback C functions. The verified original ROM word at that offset is `00000000`. The new correction removes only the synthetic `glabel/endlabel` lines, retaining the NOP, `NON_MATCHING` marker, and all inventory identity checks. Initial separate local CI also found the VM residual ledger's stale verifier fingerprint; the checked-in ledger is updated to the verifier fingerprint from that successful native G2. **A fresh combined native acceptance pass after this change is still outstanding.**
