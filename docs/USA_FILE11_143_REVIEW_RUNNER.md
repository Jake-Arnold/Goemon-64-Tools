# One-command 303-C review: USA file_11 143-C candidate

Status: **ROM-free acceptance tests passed; native combined build not executed.** The canonical production count remains 210. This is an opt-in companion to `USA_FILE11_143_CENTRAL_PREFLIGHT_2026-11-16.md`.

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

The five standalone synthetic acceptance tests and Python compilation passed in an isolated runtime. **No private 303-C native build, combined ROM verification, inventory or full local CI was run in that runtime.**
