# Goemon USA — nine native C functions linked simultaneously, complete original-ROM / ELF equality

22 November 2026. **PASSED_PRISTINE_FULL_ROM_ELF / RESEARCH_ONLY.** The nine sources replace original `file_11` assembly in a private scratch build, and exactly reproduce the original 33,554,432-byte USA ROM, all 7,376 positive-sized ELF function identities and all 82,216 semantic relocation records. This **is not** canonical `decomp.verify` with the currently accepted 1,965 C functions, and is **not** production G2/promotion. No original assembly is distributed or overwritten.

## Exactly proven replacements

| Function | Original USA ROM offset | VMA | Bytes | History |
| --- | --- | --- | ---: | --- |
| `func_801E1C90_59DBA0` | `0x59DBA0` | `0x801E1C90` | 384 | Earlier exact speed selector; synthetic C jump table re-targeted to original symbol |
| `func_801E276C_59E67C` | `0x59E67C` | `0x801E276C` | 148 | Earlier exact Mini reset |
| `func_801E28D8_59E7E8` | `0x59E7E8` | `0x801E28D8` | 68 | Five new original-address linked exact C functions from preceding session |
| `func_801E2B54_59EA64` | `0x59EA64` | `0x801E2B54` | 84 | New |
| `func_801E31A8_59F0B8` | `0x59F0B8` | `0x801E31A8` | 52 | New |
| `func_801E31DC_59F0EC` | `0x59F0EC` | `0x801E31DC` | 104 | Newly native-exact conditional Mini state/float selector, 7 symbolic relocations |
| `func_801E3244_59F154` | `0x59F154` | `0x801E3244` | 52 | New |
| `func_801E3278_59F188` | `0x59F188` | `0x801E3278` | 92 | New |
| `func_801E3DE0_59FCF0` | `0x59FCF0` | `0x801E3DE0` | 220 | Earlier exact speed ease |
| **Total** | | | **1,204** | 9 original functions, six newly discovered and three previously independently exact |

## Original baseline and complete scratch ROM

- Retail 16MiB USA SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66`.
- Original expanded 32MiB USA SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`.
- Original upstream commit: `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
- Authentic SGI IDO 5.3 `-O2 -mips2 -G 0` with pinned original flags, MIPS GNU assembler/linker/objcopy.
- Pristine unchanged baseline original-ROM comparison: 33,554,432 bytes exact.
- Scratch 9-C replacement ROM comparison: **33,554,432/33,554,432 bytes exact**, SHA-1 identical.
- Positive `FUNC` (name, VMA, extent) identities: **7,376/7,376** exact.
- Full semantic relocations (original PC, type, target name and resolved target value): **82,216/82,216** exact across **72/72** sections, including **8,825/8,825** in `.rel.file_11`. Relocation entries can be emitted in different physical order after splitting; the audit compares sorted semantic tuples, not incidental entry order.
- The nine original function extents, including neighboring functions, stay in their correct locations. The original data and jump table remain byte-identical.

## Genuine linker and padding resolution

The original `file_11` is assembled from a monolithic file. `replay_full_9.py` reads the user-extracted original assembly in the pinned local workspace, replaces only the nine function bodies with section boundaries, assembles the remaining text and splices the nine genuine IDO objects into the exact original linker order. GNU assembler extends the first sliced `.text` section to 16-byte alignment; the verifier trims **section-size metadata** to the original number of instruction bytes and uses 4-byte input alignment. Each compiler `.text` also contains 0–12 trailing zero alignment bytes outside its exact `FUNC` extent; only section-size metadata removes them. No machine instruction is replaced with a diagnostic copy or changed by the adapter.

The C speed selector generates a synthetic `.rodata` jump table with eight compiler `R_MIPS_32` entries, even though the original USA game has the eight exact numeric entries at original symbol `jtbl_8020B2E0_5C71F0` and VMA `0x8020B2E0`. The adapter changes exactly two symbolic relocation targets, at C function offsets `+0x138` and `+0x140`, from the synthetic `.rodata` section symbol to the original named table symbol; it discards the unused generated table. No compiler instruction bits are modified. The original table entries are independently authenticated in the original expanded ROM. Fail-closed full-ROM and relocation comparisons then prove the adjustment reproduces the original.

## Clean replay on Linux

First follow `GOEMON_BUILD_ENVIRONMENT.md` using your private project resources. Decompress, split and byte-identically rebuild the original USA pinned `mnsg` as documented. Restore the bundled native IDO, standalone Python, MIPS assembler/linker/objcopy, and `LD_LIBRARY_PATH` for bundled linker shared libraries. Extract this source-only ZIP to an ordinary directory, and run:

```sh
sha256sum -c SHA256SUMS
python3 replay_full_9.py \
  --upstream /path/to/pinned/mnsg-japan \
  --rom /path/to/pinned/mnsg-japan/config/usa/baserom.decompressed.z64 \
  --built-rom /path/to/pinned/mnsg-japan/build/usa/mnsg.z64 \
  --elf /path/to/pinned/mnsg-japan/build/usa/mnsg.elf \
  --out-dir /tmp/goemon-mini9-private-replay \
  --json /tmp/goemon-mini9-private-proof.json
```

The command is fail-closed and performs compiler builds, complete 32 MiB ROM equality, every positive FUNC name/address/extent, every relocation semantic tuple, and canonical reference counts. Scratch build outputs (ASM, object files, ELFs and ROM) remain local in `--out-dir`; never upload them. `replay_native.py` separately authenticates the previous five newly reconstructed isolated functions.

The previous five *actual* reconstructed C bodies also passed both real GCC and Clang AddressSanitizer/UBSan tests across 32,768 deterministic scenarios / 163,840 calls each compiler:

```sh
gcc -std=c11 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -I. exact_five.c test_native_five.c -lm -o /tmp/goemon-five-gcc
/tmp/goemon-five-gcc
clang -std=c11 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -I. exact_five.c test_native_five.c -lm -o /tmp/goemon-five-clang
/tmp/goemon-five-clang
```

The ninth reconstructed  conditional selector `conditional_speeds.c` was also tested as the actual C body under GCC and Clang AddressSanitizer/UBSan for 65,536 deterministic cases per compiler (branch choice, callback identity and all three bitwise-exact floating arguments):

```sh
gcc -std=c11 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer conditional_speeds.c test_conditional_speeds.c -o /tmp/goemon-conditional-gcc
/tmp/goemon-conditional-gcc
clang -std=c11 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer conditional_speeds.c test_conditional_speeds.c -o /tmp/goemon-conditional-clang
/tmp/goemon-conditional-clang
```

A deliberate change to the selector source constant is rejected before compilation by the immutable source SHA-256 assertion. The preceding five-function native verifier had already rejected wrong constants and incorrect symbolic relocation targets. Host tests do not prove emulator gameplay.

## Publication boundary

This archive contains only reconstructed C, native replay/audit Python source, a portable host test and sanitized proof. It includes **no** original ROM, ASM, proprietary compiler, generated ELF/object/binary, original instruction words, game assets, credentials or traces.

The current canonical `chatgptweb/decomp` **1,965 accepted USA C functions / 84,648 original instruction bytes / 5,398 ASM** remains a separate verified historical production checkpoint. Live full-branch checkout is not present in this execution container; terminal DNS to github.com failed, and GitHub connector read access did not materialize the full current branch into the local native build workspace. Therefore fresh combined `python3 -m decomp.verify`, `python3 -m decomp.inventory`, and full `python3 -m decomp.local_ci` **were NOT RUN**, even though pristine nine-function ROM/ELF proof PASS. No promotion, no manifest or original ASM ownership modifications, no merge. Keep PR #144 draft.

The separate 4,320-byte `func_801CD310_589220` clamp is still `FAILED_NATIVE`: previously highest full-C candidate 123/917 same original-position comparable MIPS words, 30/101 exact relocations, 232-byte frame; magnitude `sp+0x8C` and merged `$f14` / `$f16` lifetimes remain open. The nine successes do not imply that clamp matches.
