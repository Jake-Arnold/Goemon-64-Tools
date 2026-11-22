# Japan rev-0: two previously blocked halfword updates (22 November 2026)

**PASSED_ISOLATED_NATIVE / RESEARCH_ONLY; no canonical promotion.** The complete Japanese branch remains at **2,314 accepted matching-C functions / 5,062 original ASM functions**. This directory contains only original C reconstructions and a reproducible test; no ROM, compiler, binary, original ASM or game asset.

A typed structure with `unsigned short` at +0x18 and two explicit sequential stores changes IDO register allocation and instruction scheduling compared with prior raw-pointer C variants. With SGI IDO 5.3 `-O2 -mips2 -G 0`, `func_80219328_6A0A28` at expanded JP ROM offset `0x6A0A28` and `func_80222F18_68C608` at `0x68C608` both match all **28/28 original bytes**. Both compiled `.text` sections are 32 bytes with an extra 4-byte alignment NOP beyond each declared 28-byte function. No external symbolic relocations occur inside either function.

The first function subtracts two and masks 0x3FF; the second subtracts four and applies the same mask. Both preserve the original intermediate halfword store in this IDO build. A different C compiler is not required to preserve both stores, so the machine-level claim is compiler-specific. All 65,536 possible field inputs per function passed host GCC ASan/UBSan tests.

Reproduce locally:
```
python3 verify_isolated.py --rom /path/to/japan_0/baserom.decompressed.z64 --cc /path/to/ido-5.3/cc
cc -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -o /tmp/jp_halfword_semantics tests/test_semantics.c src/*.c
/tmp/jp_halfword_semantics
```

**Not performed:** staged combined build with all 2,314 accepted C functions, exact 32 MiB and retail ROM reconstruction, all 7,376 ELF identities and 80,747 semantic relocations, strict accepted-C/ASM inventory, and full local CI. GitHub connector can read the branch, but the execution host cannot clone the full repository (DNS fails) and the uploaded source ZIP is upstream, not the current branch. Do not increase matching C counts. Remaining four JP2307 retry blockers and three 48-byte table clears remain assembly.

Source-only companion bundle with matching local source files and proof metadata was delivered in the ChatGPT session; SHA-256 of its results JSON: `9c37b4bcb6c08c878ef3542ace43ae157b1c1bfd1fe7f08265c8d165030b0e31`.
