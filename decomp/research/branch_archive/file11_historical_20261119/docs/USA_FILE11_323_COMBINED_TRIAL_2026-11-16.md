# USA 323-C trial: integrated file_11 160-function stage (16 November 2026)

**State: DRAFT INTEGRATION / NOT PRODUCTION VERIFIED.** Canonical production stays at 315 USA matching C / 16,660 bytes. This PR only adds an opt-in 160-`file_11` C layout and a fail-closed central verifier/review workflow.

## New native original-ROM proof

The distinct PR #23 eight-callback block at `0x5A6F30–0x5A7090` is 8 functions / 352 instruction bytes. Its whole-slice C source (`decomp/research/file11_next8_group.c`) was originally verified on pinned upstream. For the actual layout intended for the 315-C mixed-overlay, I independently extracted and assembled a **five-split** version of the pristine original overlay:

- ASM `0x587370–0x5A63F8`
- ASM `0x5A63F8–0x5A6F30`
- C `0x5A6F30–0x5A7090` (eight functions)
- ASM `0x5A7090–0x5A74CC`
- ASM `0x5A74CC–0x5B8500`

The original 315-C adapter has 88 C/ASM segments. The proposed 160-file11-C adapter expands this to exactly **90** segments (**50 C, 40 ASM**); **87 of 88** old segments remain unchanged and one previous ASM segment is replaced with the three new exact slices.

Pinned original 352-byte ROM SHA-256: `b1fbaa8f74fec1f63e9f3cf2d0647daf26fd008a135cba0f767e5958113dcff1`.

Trimmed object SHA-256 for the new left ASM / C / right ASM: `303190ce2546616637d48cf01334ce628f05721c1042117f24813634fdd80ec3`, `c79a3a252f4b78ce0e5188a8406842e532ed3a9d4b44ad98f0314eee8c475ca1`, `8942a6c4c238623fa6be9ff168f557d924814d377ab54427f01dd3b891a5e960`.

The scratch build used the uploaded original USA retail ROM, pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, original IDO 5.3, supplied Python 3.12 and MIPS binutils. After Splat extraction, the first and last ASM objects and two interior ASM objects were trimmed only for terminal zero padding, and the original file_11 linker section used `SUBALIGN(4)`, consistent with the existing production adapter. No code or payload bytes were rewritten.

**Fresh result:** complete **33,554,432-byte USA ROM identical**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; **8,825/8,825** semantic file_11 relocations equal; **7,098/7,098** named positive-sized FUNC symbols equal (name, VMA and size), including all eight new C functions. This is a pinned upstream scratch, **not** the combined 323-C central G2, and **not** the separate 7,376-entry original inventory.

## Trial native acceptance

The new `decomp/file11_160_stage.py` and fixture retain all previously approved 152 C claims and add only these eight. `decomp/verify.py` accepts the new `goemon-file11-160-central-v1` format only when explicitly opted in. The canonical `decomp/manifest.json`, `decomp/results/combined.json`, and `decomp/results/inventory.json` are **unchanged**.

Run only from a complete connected repository checkout with the pinned Linux toolchain, original retail USA ROM, and an unused external work/output directory:

```bash
python3 -m decomp.review_file11_143 \
  --candidate-file11-160 \
  --source-dir ./decomp \
  --upstream /path/to/clean-pinned-mnsg \
  --retail-rom '/path/to/Mystical Ninja Starring Goemon (USA).z64' \
  --workdir /tmp/goemon-323-new-work \
  --output-dir /tmp/goemon-323-new-review \
  --uv /path/to/uv \
  --binutils-root /path/to/goemon-dependencies
```

The runner rejects a changed/non-315 canonical baseline, creates a **temporary 323-C manifest** without editing the published manifest, runs full standard native `decomp.verify` with authentic complete USA ROM comparison, validates every function and original `file_11` relocation, runs original-ELF `decomp.inventory` for **7,376** identities / zero extra aliases, and runs full `decomp.local_ci`. A failure produces no successful review record.

Only a successful combined acceptance may justify a separate formal promotion to 323 USA C / 17,012 matching instruction bytes, 160 file_11 C functions, 336 combined C entries including upstream, and 7,040 assembly entries. This draft alone does **not** justify that count.

## Limitations

The current ChatGPT runtime has the authentic original ROM and complete pinned upstream scratch, but **not a native filesystem checkout of the latest connected decomp GitHub branch**. Local source-only tests against the live 315-C production tree and the complete combined 323-C gate have not run in this session. The native scratch with the precise split is a genuine independent reproduction, not a substitute. Do not merge this draft as completed production until all gates pass. No game assets, ROMs, generated assembly, saves or proprietary compiler binaries have been committed.
