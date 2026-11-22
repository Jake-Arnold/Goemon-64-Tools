# Japanese N64 original-address native-C recovery — additional four (22 November 2026)

**Status: `PASSED_ISOLATED_NATIVE / RESEARCH_ONLY`; canonical C and ASM ownership unchanged.**

Authenticated original Japan rev-0 33,554,432-byte expanded ROM SHA-1: `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. The original 16 MiB normalized Japanese retail ROM SHA-1 is `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`. The source was compiled with the pinned SGI IDO 5.3 compiler, `-O2 -mips2 -G 0`, linked at each original main-segment guest VMA and compared to the authenticated original ROM. Four **previously ASM-owned**, deduplicated functions passed all their isolated native instruction bytes and **15/15 required original symbolic relocation records**.

| New function | Expanded ROM offset | Original VMA | Original instruction bytes | Symbolic relocs |
| --- | --- | --- | ---: | ---: |
| `func_80008500_9100` | `0x9100` | `0x80008500` | 64/64 | 9/9 |
| `func_80008540_9140` | `0x9140` | `0x80008540` | 24/24 | 4/4 |
| `func_80008558_9158` | `0x9158` | `0x80008558` | 28/28 | 0/0 |
| `func_80010118_10D18` | `0x10D18` | `0x80010118` | 28/28 | 2/2 |

`func_80008500_9100` installs the observed symbolic data pointer at system-relative offset `D_C5F78` then invokes the original setup helper. `func_80008540_9140` writes a 32-bit value at adjacent system-relative symbol `D_C5F7C`. `func_80008558_9158` reads an indexed 8-byte record and stores its second 32-bit word at destination offset `0x34`. Its exact MIPS compiler register allocation depends on the original *operand order* in pointer arithmetic. `func_80010118_10D18` zeros one halfword in a table of 12-byte records, symbol `D_8016D6DA_16E2DA`.

The hexadecimal C global names are original symbols, not newly asserted gameplay meanings. In C, pointer-to-integer conversions using `unsigned long` are implementation-defined and rely on the 32-bit MIPS / 64-bit LP64 host address representations tested here. Host tests use a `GOEMON_HOST_TEST` offset shim only for the two absolute-offset linker symbols; native C instruction/relocation verification compiles the **unmodified non-host code path**.

## Replay native exactness

On a Linux machine with the original Japan rev-0 expanded ROM, compiler and binutils:

```sh
export LD_LIBRARY_PATH=/path/to/goemon-runtime-additions/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export PATH=/path/to/goemon-dependencies/bin:$PATH
python3 verify_native.py \
  --rom /path/to/japan_0/baserom.decompressed.z64 \
  --cc /path/to/pinned/ido-5.3/cc \
  --report /tmp/jp_native_next4_proof.json
```

The verifier refuses unexpected ROM hashes, instruction bytes, relocation types/offsets/symbols, nonzero padding and incorrect original function addresses. It emits a self-contained sanitized JSON proof (source hashes and code hashes only, **no copyrighted original bytes**). `proof.json` is the actual result of the replay in this conversation.

## Host sanitizer regression

```sh
gcc -std=gnu11 -O1 -g -DGOEMON_HOST_TEST \
  -fno-omit-frame-pointer -fsanitize=address,undefined \
  -I src -o /tmp/jp_next4_host tests/test_semantics.c src/*.c
ASAN_OPTIONS=detect_leaks=1 /tmp/jp_next4_host
```

**Actually run: PASS.** Four original C implementations were tested against their observed C effects, including 65,536 unsigned-halfword indices, 300 record-clear operations, system-relative pointer installation, 32-bit field writes and helper argument/call checks. The C host test is not emulator execution.

## Deduplication and official acceptance

The four names are absent from all 20 examined published Japan-0 region/source manifests (including the full 1,686-function archive, JP2268 short145 bundles, latest donor, retry and expansion manifests). The other two exact matches found in the same work session—`func_8000C568_D168` and `func_8000D910_E510`—were identified as *already accepted* JP1686 functions and **excluded**. They contribute zero new recovery.

This adds **4 unique / 144 original instruction bytes** to the previously reported **17 unique / 992 bytes** of unpromoted research, yielding **21 isolated-native-exact pending functions / 1,136 original code bytes**. They have not been integrated with the currently published Japanese 2,314 matching-C set.

**NOT RUN, required before official C promotion:** fully staged original Japanese 33,554,432-byte ROM and normalized 16 MiB retail-ROM rebuild, all 7,376 original ELF function identities, all 80,747 semantic relocations, strict original C/ASM ownership inventory, and full `decomp.local_ci`. The complete current `chatgptweb/decomp` source checkout was inaccessible to the native build host because direct GitHub DNS/clone access failed; the uploaded source ZIP is the pinned upstream, not a full decomp branch checkout. No production source, accepted manifest, `decomp/results/combined.json`, canonical inventory or official function count may be changed on this isolated evidence.

Official Japanese totals remain **2,314 accepted C / 123,236 original instruction bytes / 5,062 assembly**. Original assembly retained for all four. Full acceptance remains blocked by local availability of the complete live branch and full combined native gates.
