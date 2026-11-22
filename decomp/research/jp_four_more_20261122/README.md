# Japan rev-0: four additional original-address matching-C candidates (22 Nov 2026)

**PASSED_ISOLATED_NATIVE / RESEARCH_ONLY. No canonical promotion.**

Input original Japan expanded 32 MiB SHA-1: `6f8745fecc3a5e7d4918c7a73353eb0726116ded`; original supplied retail Japanese ROM normalized SHA-1: `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`. Original SGI IDO 5.3 `-O2 -mips2 -G 0`, MIPS32 big-endian original guest VMA, native symbol relocation checks. Sources are human-reviewable observed-type reconstructions; the file contains no ROM, original game ASM, game assets, proprietary toolchain or compiled code.

## Newly recovered, previous assembly-owned (deduped against live Japanese manifests)

| Function | Original expanded ROM | Guest VMA | Function bytes | Isolated symbol relocations | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| `func_8000BFFC_CBFC` | `0xCBFC` | `0x8000BFFC` | 140 | 2/2 HI16/LO16 (`+0x4`, `+0xC`) | **140/140 exact** |
| `func_8000C088_CC88` | `0xCC88` | `0x8000C088` | 76 | 2/2 HI16/LO16 (`+0x4`, `+0xC`) | **76/76 exact** |
| `func_8000C0D4_CCD4` | `0xCCD4` | `0x8000C0D4` | 68 | 2/2 HI16/LO16 (`+0x4`, `+0xC`) | **68/68 exact** |
| `func_8000D108_DD08` | `0xDD08` | `0x8000D108` | 64 | 2/2 HI16/LO16 (`+0x0`, `+0x8`) | **64/64 exact** |

**Total: four new C candidates, 348 original instruction bytes, 8 expected isolated symbolic relocations.** The global symbol `D_8016D430_16E030` is the previously observed Japanese pointer array; no unverified gameplay name is introduced. Actual source/ASM owner for all four: original Japanese `main_C320` (and its adjacent C320–DD50 unit). The matching-C status is compiler and region specific. The `func_8000BFFC_CBFC` branch-likely chain was reproduced only after reusing input parameter `i` as the loaded mode value; the first local variable variant produced 29/35 exact words with `$v1` instead of original `$a0`. The two other state-mutating routines match with explicit typed `u64` and signed halfwords.

**Already accepted control, not a new recovery:** `func_8000B720_C320` (original 0xC320, 64 B) also compiled 64/64 exact with a simple three-call `for` loop. It is present in the published JP1686 candidates.csv, so it was excluded from the count and package.

**Failed independent candidate:** `func_8000C5A8_D1A8` (88 B) remains ASM. Initial typed-pointer C had 7/22 matching words (first mismatch +0x10), variant with cached `p` had 6/22 with original stack frame/schedule mismatch. No G2 integration attempted.

## Reproduction (Linux)

```sh
# From extracted source research bundle, with user-supplied authentic original ROM and IDO compiler
export LD_LIBRARY_PATH=/path/to/goemon-runtime-additions/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export PATH=/path/to/goemon-dependencies/bin:$PATH
python3 verify_native.py \
  --rom /path/to/config/japan_0/baserom.decompressed.z64 \
  --cc /path/to/mnsg-japan/tools/ido-5.3/cc \
  --report /tmp/jp_four_more_native_proof.json

gcc -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined \
  -Isrc -o /tmp/jp_four_more_host tests/test_semantics.c src/*.c
ASAN_OPTIONS=detect_leaks=1 /tmp/jp_four_more_host
```

Native verifier compares every instruction byte against the SHA-1-authenticated original 32 MiB Japanese ROM after compiling and linking C at its original guest VMA, with correct subalignment and resolved original global address. Each original function retains **exact two symbolic relocations**; trailing zero linker padding is excluded from the function byte extent. It also checks linked function symbols and source hashes.

Host regression **PASS**: all four real C implementations, 4,097 actor states, null-pointer cases and eight pointer-presence mask combinations, built and run with GCC ASan/UBSan. No N64 emulator execution or original game unit integration implied.

## Acceptance not performed

The execution environment has the original Japanese ROM, pinned upstream source, IDO 5.3, Splat, binutils and runtime. GitHub is available through a connector but `git ls-remote`/clone fails DNS in the local shell. The complete newest `chatgptweb/decomp` source checkout and 2,314 C candidates are **not** available in the native build filesystem. Thus the combined 33,554,432-byte and retail-ROM gates, 7,376 ELF original function identities, 80,747 semantic relocations, strict C/ASM inventory and full decomp.local_ci were **NOT RUN**. Never promote from isolated native matching alone. Official published Japanese totals stay **2,314 C, 123,236 bytes, 5,062 ASM**.

This adds four independent new candidates to the earlier two halfword (56 B) and eleven actor-table (588 B) isolated research candidates. **Seventeen total candidate functions / 992 original bytes** across those three research packages remain unpromoted pending integrated full original ROM proof. These 17 are *not* part of the 2,314 accepted Japanese C functions.
