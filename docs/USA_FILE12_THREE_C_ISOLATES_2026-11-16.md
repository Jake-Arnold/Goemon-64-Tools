# USA file_12: three isolated matching-C lifecycle functions

Date: 2026-11-16. This is research-grade native code verification, **not** a production matching-C promotion.

## Direct original-ROM proof

The original USA retail ROM was re-decompressed and matched the 32 MiB reference SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. The pinned upstream IDO 5.3 compiler was run with original `-O2 -mips2 -G 0 -non_shared` compiler settings. Each source was compiled into MIPS ELF, linked **at its actual original virtual address**, with all named externals resolved, and the complete positive-sized function range was compared byte-for-byte to the original 32 MiB image.

| Original function | ROM offset | Size | Object relocs | SHA-256 of original-linked bytes |
| --- | --- | ---: | ---: | --- |
| `func_8021A644_5D5B14` | `0x5D5B14` | 56 | 1 | `c3b48a6ec00152d9c26c61c72833a94743e6b685ccce00ac2830011af95a865b` |
| `func_80218E7C_5D434C` | `0x5D434C` | 180 | 14 | `d2a256588b93edef53dd1d683d1e5b58d34929040bc091942ce99b1f2c71783d` |
| `func_80218F30_5D4400` | `0x5D4400` | 184 | 10 | `5c7645393a7369851323ae63785154e7b546106bd4ca6fb4c2b8815c4db02b46` |

**Three functions, 420 of 420 bytes exact, 25 declared relocations checked**, including MIPS-26 call and HI16/LO16 pair resolution. The result is intentionally limited to isolated original-address code equality; the original overlay ELF relocation multiset, C/ASM input placement, whole-ROM image, and 315-C combined pipeline have **not** been rerun. The verifier generates no redistributed ROM and fails closed for incorrect ROM identity, code, extent, or relocation symbols/counts.

The pair at `0x80218E7C` and `0x80218F30` is contiguous in the original overlay; its 180 + 184 = 364-byte combined code span is a promising next staged mixed ASM/C candidate. The 56-byte gate at `0x8021A644` is a separate island. IDO ELF input text is 16-byte aligned while the original functions start at 4-byte boundaries, so the verifier uses linker `SUBALIGN(4)`; whole-ROM integration must separately preserve neighboring object padding and relocation fidelity.

## Reconstructed behavior

- The 180-byte update dispatcher runs thirteen actor callbacks when `actor+0x18` is nonzero, clears `actor+0x68` mask `0x00040000`, then **always** invokes the spatial release helper `0x8021A328`.
- The 184-byte state-2 callback clears `actor+0x34/+0x38`, checks bit 2 of `actor+0x68`, requests generic scheduler processing, and conditionally allocates a successor if `actor+0x70` is still linked to a placement. Successful succession assigns state 8, reuses that placement link, installs the same callback and sets `actor+0x76 = (old range + 5) mod 256`. On allocation failure it clears the placement's active byte.
- The 56-byte gate at `0x8021A644` checks `actor+0x70` and `placement+0x10` before calling `0x8021A4E4` with `1.0f`.
- In the state-2 function, `func_80034ED4` does **not** accept an actor parameter in the reconstructed source: the original callee reads the global scheduler pointer at `D_8016DAB4`, then enters `func_80034EF8`, `func_80034F44` and `func_800350C4`. The scheduler routines manipulate linked task entries, callbacks and an active count. This is stronger evidence for scheduler retirement/recycling than for an immediate general-purpose heap free.
- The callback's source contains an unused 3-element volatile local solely to reproduce the original 0x30-byte IDO stack-frame geometry. It is a compiler-layout device, **not** evidence that an original gameplay array existed.

## Reproduction

Run `python3 decomp/research/file12_spatial/verify_isolates.py --rom /path/to/usa.decompressed.z64 --cc /path/to/mnsg/tools/ido-5.3/cc --ld /path/to/mips-linux-gnu-ld --objcopy /path/to/mips-linux-gnu-objcopy`, with the archive-provided MIPS binutils shared libraries on `LD_LIBRARY_PATH`.

The direct local run passed all three original-code comparisons and four new ROM-free regression tests; the previous four spatial-anchor regressions and 38/38 original-ROM anchors also passed. No full `decomp.local_ci` or native 315+3 combined G2 is claimed for this research branch.

## Integration gate

Prepare a versioned USA `file_12` ASM/C/ASM splice that preserves original subsegment order, original symbol sizes/addresses, the complete original `file_12` relocation multiset, and the exact full 32 MiB original ROM. Then run the existing central full `decomp.verify`, `decomp.inventory` and `decomp.local_ci` before updating any production count. Do not merge research-only isolated C directly into the production manifest.
