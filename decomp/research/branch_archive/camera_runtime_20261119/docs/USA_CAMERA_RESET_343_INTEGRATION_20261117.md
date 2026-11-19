# USA camera reset — 180-file11 / 343-USA opt-in integration (17 November 2026)

**State: REVIEWED STAGE CODE ONLY. The canonical production USA count remains 342.**

The source-only candidate was rebased onto live `chatgptweb/decomp`, whose canonical manifest claims 342 original-address matching-C functions / 17,568 bytes, including 179 in `file_11`. Japanese rev-0's independently verified 34 functions remain separate. No official proof or production manifest was overwritten.

## New work

- Added `decomp/file11_180_stage.py` with a versioned, *opt-in* `goemon-file11-180-camera-reset-v1` stage, `decomp/candidates/manifest_camera_343_20261117.json` pointing at it, `tests/test_decomp_file11_180_stage.py` and fail-closed routing in `decomp/verify.py`.
- The new stage **derives** all 179 accepted C function/ASM ownership records from the immutable parent fixture at `decomp/research/file11_143_candidate/file11_179_source_fixture.json`. It does not copy or regenerate their C bodies.
- Only the parent ASM region `[0x5B4E1C,0x5B64B8)` is replaced by `ASM [0x5B4E1C,0x5B56E4)` (2,248 bytes), existing matching camera-reset `C [0x5B56E4,0x5B576C)` (136 bytes), and `ASM [0x5B576C,0x5B64B8)` (3,404 bytes).
- Original function `func_801F97D4_5B56E4` remains at original VMA `0x801F97D4`. All prior 179 functions must remain identical. Expected 180 matching `file_11` C entries / 5,320 instruction bytes, 128 original ownership chunks: 77 C, 51 ASM.
- Source pin: `9d47ba199dfd48f5707b7623f45eee5e0853110f725e08bcf4ad7c151f7450c4`. The three complete original ROM ranges, native ELF text object pins and expected original global symbol relocations are individually checked; the exact 32 MiB USA ROM, 8,825 semantic relocations, and 7,376 original function identities remain mandatory for acceptance.
- This stage **never** permits `GOEMON_STAGE179_PROBE=1` to bypass any unreviewed object hash; only the three *historically approved* synthetic NOP-alias ASM objects retain their already published exception.

## Evidence before this integration

A clean, pinned upstream-only scratch build with this same C source already succeeded: **33,554,432 exact ROM bytes**, `file_11` relocations **8,825/8,825** with identical semantic multiset, original FUNC inventory **7,376/7,376**. Authenticated USA ROM and original IDO 5.3 were used. That scratch proof is preserved at `decomp/results/camera_reset_136_scratch_proof_20261117.json`; it must not be confused with the complete existing 342-C mixed-build and new 343-C combined gate.

The two new assembly slices were independently assembled natively at their original bounds and trimmed only overrun zero padding. Byte SHA-256 values and ELF object SHA-256s are pinned in the new adapter. The earlier isolated 136-byte C object was independently byte-matching.

## Required central acceptance

Run the candidate against an authenticated complete 342-function production checkout (not solely pristine upstream):

```bash
python3 -m decomp.verify --manifest decomp/candidates/manifest_camera_343_20261117.json \
  --source-dir decomp --upstream "$GOEMON_UPSTREAM" --retail-rom "$GOEMON_ROM" \
  --workdir /tmp/goemon-camera343-combined --report /tmp/goemon-camera343-combined.json --jobs 2
python3 -m decomp.inventory --baseline /tmp/goemon-camera343-combined/baseline \
  --candidate /tmp/goemon-camera343-combined/candidate \
  --report /tmp/goemon-camera343-inventory.json
python3 -m decomp.local_ci
```

Use new, nonexisting work/report paths. If any check fails, **no production promotion**; inspect the exact first mismatch. The 343-C candidate is not a published count until central G2, inventory and full local CI pass and the canonical manifest/proof is separately updated and committed.

## Splat regeneration and native object check (17 November 2026)

In the mounted authenticated USA workspace, the **exact complete 128-subsegment file_11 Splat layout** was regenerated (51 ASM, 77 C) using pinned Splat and original USA ROM. Native MIPS binutils compiled the two new original-address ASM objects, and IDO 5.3 compiled the unchanged camera C source. The exact observed trimmed ELF SHA-256s are:

- `asm/usa/5B4E1C.s.o`, 2,248 bytes: `6463f33b5dadd81a60f3cb91871fdf054a3f9df78840d0597c92811025738bfb`.
- `src/camera_reset_usa_5b56e4.c.o`, 136 bytes: `1e404dc0f374ffa2d7b1e2f21e8d468014af9ab132f044e90e9a49a99d728c81`.
- `asm/usa/5B576C.s.o`, 3,404 bytes: `f187e7d38ceba6cc9cacbc7b47889e4d757924fbbca1aa728267674805a717ad`.

The first adapter commit used two object hashes from a hand-sliced copy of the original one-piece assembly. Those were **not** the Splat-emitted objects and were intentionally replaced here with the tested full-layout hashes. This eliminates that preflight mismatch; **it does not prove the 343-C combined full-ROM gate**.

## Exact native validation update (17 November 2026)

A second clean original-ROM workspace recompiled **all 77 C source objects and all 51 assembly source objects** in the 128-segment file11 layout, with all 76 accepted prior C source bodies reproduced from the live original fixture (not guessed), and the camera reset added as the 77th C source unit. It completed `make VERSION=usa build/usa/mnsg.z64`. The **entire 32 MiB USA ROM was byte-for-byte identical**, its SHA-1 was `6ea0ed71032ce08fc2745f412d84936382197494`, the linked `file_11` relocation multiset was **8,825/8,825 identical**, and the original positive-size ELF function identity table was **7,376/7,376 identical** (all names, VMAs and sizes).

**Pin correction:** The first experimental hand-slice hash pins were in fact correct for this complete native layout. The subsequent claimed regenerated-Splat pins were not reproducible in the clean original-ROM build. Restored exact verified hashes:
- ASM `[0x5B4E1C,0x5B56E4)`: `5d5796c691bd98450bbc4f256c03b5e9b787af6e60d58e816ecc7f0d444ae66c`
- C `[0x5B56E4,0x5B576C)`: `1e404dc0f374ffa2d7b1e2f21e8d468014af9ab132f044e90e9a49a99d728c81`
- ASM `[0x5B576C,0x5B64B8)`: `64f5b4cfc95ac0be408ab21423132e26873077a8dda3834a4053b89ead185444`

All remaining 125 normal object hashes match the canonical 179-file11 fixture; the other three objects are existing, explicitly allowed Splat NOP-alias ASM exceptions. Evidence: `decomp/results/camera_reset_file11_180_native_proof_20261117.json`. All source/ROM/proprietary binary contents remain local; GitHub contains only hashes and provenance. This repeat was not a complete combined **343-C central verification** or full `decomp.local_ci`. Neither official USA production 342 nor Japanese 34 is changed.
