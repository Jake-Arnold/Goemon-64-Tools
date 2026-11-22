# Goemon USA — five Mini Ebisumaru functions reconstructed exactly in original-address native IDO

22 November 2026. **PASSED_ISOLATED_LINKED_NATIVE / RESEARCH_ONLY**, not production G2. No original assembly/function ownership has changed.

Original retail USA SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66`.
Authentic original expanded 32 MiB SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`.
Pinned upstream: `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
Native compiler: original SGI IDO 5.3 `-O2 -mips2 -G 0` with the pinned upstream compiler flags. Native big-endian MIPS GNU linker and objcopy are used solely to resolve original addresses independently.

## Original-address results

| Function | Original ROM offset | Original guest VMA | Original size | Matching symbolic relocations |
|---|---|---|---:|---:|
| `func_801E28D8_59E7E8` | `0x59E7E8` | `0x801E28D8` | 68 B | 1/1 |
| `func_801E2B54_59EA64` | `0x59EA64` | `0x801E2B54` | 84 B | 4/4 |
| `func_801E31A8_59F0B8` | `0x59F0B8` | `0x801E31A8` | 52 B | 3/3 |
| `func_801E3244_59F154` | `0x59F154` | `0x801E3244` | 52 B | 3/3 |
| `func_801E3278_59F188` | `0x59F188` | `0x801E3278` | 92 B | 5/5 |
| **Total** | | | **348/348 native bytes** | **16/16** |

The verifier reads and authenticates the user's original 32 MiB USA ROM and its pristine rebuilt image (all 33,554,432 bytes). It checks the original ELF function identity, original address and extent; SGI IDO native C compile; the complete and ordered MIPS ELF text-relocation symbol/type/offset triples; adapts only ELF `.text` section alignment metadata to the 4-byte-aligned original guest function start; links each C source independently at the original guest VMA with original symbol definitions; and compares the *entire final linked instruction range byte for byte* against the original ROM. No native machine-code instruction bytes or relocations are patched.

Source-only SHA-256 of `exact_five.c`: `574b87495f85ca510639256a3f54f569a4cf67b20ad26c61bbdfce5586236cf5`.

## Native replay

Use the project `GOEMON_BUILD_ENVIRONMENT.md` setup for the original USA ROM, standalone Python and MIPS toolchain. Make `LD_LIBRARY_PATH` point to the bundled MIPS binutils shared libraries, and add the MIPS tools directory to PATH. In a native system with the original pinned checkout and user's ROM:

```sh
python3 replay_native.py \
  --upstream /path/to/pinned/mnsg-japan \
  --rom /path/to/usa/baserom.decompressed.z64 \
  --built-rom /path/to/usa/build/usa/mnsg.z64 \
  --elf /path/to/usa/build/usa/mnsg.elf \
  --json /tmp/goemon-native5-proof.json
```

The verifier creates compiler and linker intermediates only in a disposable private temporary directory. All five assertions must pass. It does not read/write production manifest or assembly ownership.

## Real C host-regression test

```sh
gcc -std=c11 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer \
  -Itests/stubs exact_five.c tests/test_native_five.c -lm -o /tmp/goemon-five-host-gcc
/tmp/goemon-five-host-gcc

clang -std=c11 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer \
  -Itests/stubs exact_five.c tests/test_native_five.c -lm -o /tmp/goemon-five-host-clang
/tmp/goemon-five-host-clang
```

Both compilers ran 32,768 deterministic iterations of all five original C bodies (163,840 total calls per compiler), including captured helper-argument identity, float values, pointer writes, and side effects. Original mini helper code was not emulated; host tests alone do not prove in-game equivalence.

## Negative controls and limitations

The original-address linker verifier rejected two deliberately corrupted source variants: changing `120.0f` to `121.0f` failed full linked-MIPS equality, and changing a referenced global symbol failed exact relocation comparison. A wrong function size, relocated instruction, symbolic target, ROM SHA-1, compiler output or original ELF function address also aborts the replay.

The longer movement clamp `func_801CD310_589220` remains **FAILED_NATIVE** after extensive bounded float/stack source experiments; the strongest existing whole-C result retains **123/917 same-position nonrelocation words, 30/101 exact relocations, 232-byte frame**, and the two correctly placed vector buffers `sp+0xA4` and `sp+0xB0`. Its magnitude backing slot `sp+0x8C` and independent F14/F16 reset lifetimes are not recovered. Neighboring `func_801E2CEC_59EBFC` and `func_801E30E4_59EFF4` also remain **FAILED_NATIVE** and assembly-owned.

**NOT RUN:** integrated 33,554,432-byte candidate ROM with every currently accepted USA C function; canonical `python3 -m decomp.verify`; `python3 -m decomp.inventory`; full `python3 -m decomp.local_ci`; in-game emulator regression. The five proven isolated functions must **not be promoted** until these gates pass. Last verified production USA: **1,965 accepted C, 84,648 original instruction bytes, 5,398 ASM entries**. The GitHub PR remains draft.

The package contains only human-authored/reconstructed C and verifier/host-test sources, sanitized hashes/metadata, and replay instructions. It contains no ROM, original assembly, machine-code bytes, original object files, generated ELF, proprietary compiler, game assets, credentials, or user data.
