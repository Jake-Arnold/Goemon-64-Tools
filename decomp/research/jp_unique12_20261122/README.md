# Japanese rev-0 — 12 new original-address native-exact C candidates (22 November 2026)

**State: `PASSED_ISOLATED_NATIVE / RESEARCH_ONLY`. No accepted matching-C promotion.**

Original Japanese expanded-ROM SHA-1: `6f8745fecc3a5e7d4918c7a73353eb0726116ded` (32 MiB, user-supplied retail ROM normalized/decompressed with original project tooling). C compiler: original **SGI IDO 5.3, `-O2 -mips2 -G 0`**. All candidates linked at their **original actual guest VMA**, not merely compared as relocatable object code. Exact original machine instruction bytes, extent, and separately all original object relocation records were verified in a fresh local replay.

| New previously ASM-owned function | Expanded JP ROM offset | Native original bytes | Original relocations |
|---|---:|---:|---:|
| `func_801EF790_61A210` | `0x61A210` | 20/20 | 2/2 |
| `func_801E818C_5A415C` | `0x5A415C` | 32/32 | 1/1 |
| `func_801E83A0_5A4370` | `0x5A4370` | 32/32 | 0/0 |
| `func_8021B3F8_67A268` | `0x67A268` | 32/32 | 2/2 |
| `func_8021251C_67BC0C` | `0x67BC0C` | 32/32 | 4/4 |
| `func_8021BB68_5D70F8` | `0x5D70F8` | 36/36 | 1/1 |
| `func_801EC4E8_5A84B8` | `0x5A84B8` | 36/36 | 0/0 |
| `func_80200DAC_62B82C` | `0x62B82C` | 36/36 | 1/1 |
| `func_801F9560_5B5530` | `0x5B5530` | 40/40 | 1/1 |
| `func_801E60F0_5A20C0` | `0x5A20C0` | 40/40 | 1/1 |
| `func_801E6118_5A20E8` | `0x5A20E8` | 40/40 | 1/1 |
| `func_8021B3D0_67A240` | `0x67A240` | 40/40 | 2/2 |

**Total: 12 unique Japanese original-address functions, 416 original MIPS instruction bytes, 16 original symbolic relocation records**. The source files preserve the exact original instruction shapes and use no inline assembly.

## Native verifier and replay

Run on x86_64 Linux using your own provided original **expanded Japan** ROM and bundled original toolchain (export the runtime-additions `LD_LIBRARY_PATH` and binutils `PATH` as documented in `GOEMON_BUILD_ENVIRONMENT.md`):

```bash
python3 verify_native.py \
  --rom /path/to/japan_0/baserom.decompressed.z64 \
  --cc /path/to/original/ido-5.3/cc \
  --ld mips-linux-gnu-ld --objdump mips-linux-gnu-objdump \
  --objcopy mips-linux-gnu-objcopy --report /tmp/jp_unique12_isolated.json
```

The verifier authenticates each original ROM function hash and C-source SHA-256, checks original-address linked MIPS machine code and nonzero trailing padding, confirms symbol guest VMA and exact original object relocation identities. The matching original `.s` is read only for private original-relocation reference during research and is not published in this bundle.

## Host semantic fixtures

```bash
python3 tests/test_semantics.py
```

**Actually executed:** all 12 original C sources compiled by host GCC with AddressSanitizer and UndefinedBehaviorSanitizer; 11 ran host semantic fixtures covering 65,536 max-update pairs, structure bitfield operations, pointer stride/addresses, wrapper callback arguments, mutable buffers, and presence checks. `func_8021251C_67BC0C` was **compiled under sanitizers but not executed**: its source deliberately reconstructs an MIPS32 address-valued linker symbol (`D_CF8FC`) by converting its address to a numeric offset. This is architecture-specific and cannot be soundly emulated through a normal 64-bit host pointer without a fake guest memory model. It should receive explicit source review before production use. This is distinct from original-MIPS exactness.

## Deduplication

Each function was checked against the live `chatgptweb/decomp` published Japanese region manifests and completed promotion bundles and against the three prior 22 November research batches (two halfword, eleven actor-table and four main-segment/actor candidates, plus later four small routines). Previously accepted tiny no-ops, wrappers, and previously recovered matches were deliberately excluded. The 12 functions are **new in this batch**, not a recount of an accepted Japanese C source or one of the prior 21 pending research candidates.

## Native promotion not performed

The current entire `chatgptweb/decomp` Git repository cannot be cloned into this native sandbox because the shell has no GitHub DNS. The uploaded `mnsg-japan.zip` contains the pinned original upstream source, not the complete current decomp branch production adapters/stages, and the GitHub connector cannot directly transfer a complete working tree into the shell. As a result **a fresh combined original 33,554,432-byte Japanese ROM + 16 MiB retail ROM, all 7,376 positive-size ELF identities, full 80,747-relocation semantic multiset, strict current accepted-C/ASM inventory, and full `decomp.local_ci` were NOT RUN**. Do not mutate the canonical accepted manifest, counts or live C ownership based on these isolated results.

Official Japanese published baseline stays **2,314 C functions / 123,236 original instruction bytes / 5,062 ASM functions**. Prior pending research: 21 unique / 1,136 bytes. With this distinct batch, **33 unique candidate functions / 1,552 original instruction bytes** are research-exact but not yet officially promoted. Assuming all later pass full G2, potential resulting count would be 2,347 C / 5,029 ASM, **not yet verified**.

No ROMs, generated original assembly, game assets, executable binaries, proprietary compiler or toolchain files are included in this bundle.
