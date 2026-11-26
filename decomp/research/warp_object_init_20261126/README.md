# Task-system object initializers — 26 November 2026

UNIT_TEXT_EXACT / RESEARCH_ONLY. Four new regional C functions, 960 original bytes, continuing PR #276. Stable/decomp base 9932e4bac45bd3f41513b2f6ff0eb8ee438d0997; authenticated source archive 15074968037. Canonical USA 3052 and Japan 2990 unchanged. Original pinned upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee. Both retail/expanded ROM hashes and IDO hash enforced by replay.py.

| Region | Function | ROM offset | Bytes |
|---|---|---:|---:|
| USA | func_80035964_36564 | 0x36564 | 248 |
| USA | func_80035A5C_3665C | 0x3665C | 232 |
| Japan | func_800355D4_361D4 | 0x361D4 | 248 |
| Japan | func_800356CC_362CC | 0x362CC | 232 |

These routines preserve task return and null guards, initialize pointer fields, XYZ, three halfwords, three float fields, and object +0x44. The primary reads +0x44 from original system-relative D_C2D90; the sibling accepts this value as an explicit unsigned halfword. Three halfwords clear before the callback and ten fields afterward. Historical declarations and precise semantic names remain provisional.

Four independently compiled positives match original linked bytes, exact positive FUNC identity and extent, raw object text/addends and all 12 original named relocations. Four altered-field controls rejected (extent 252/236 B; first mismatch +0x10 branch displacement). Two numeric-offset controls reproduce identical linked ROM bytes and FUNC identity but lose both named D_C2D90 relocations; rejected. All native attempts recorded in evidence.tsv; combined tails reproduce 480 bytes per region. IDO flags and compiler hash in replay.py; exact compiler ledger SHA256 at attempts 1e07a27bf1a8e0ccb2f9d1633b59303b4417a99c81051142cd2b1a133ae54e1a.

## Independent complete text-owner results

USA owner ROM 0x35280, VMA 0x80034680; JP owner ROM 0x34EF0, VMA 0x800342F0. Each original and mixed owner links 5328/5328 exact original bytes, 59/59 positive FUNC identities, and 167/167 named relocation tuples including resolved symbol values. USA owner SHA256 e6e02624108bc4be75786b317a1cd2bb28866031513d6047afcaa931cf3afc70; JP owner SHA256 270fc04f3d2ce6c343764a3bfbef13fd48d0248c82f6ce7b950d5fe28090be3f. Custom unpadded prefix section + SUBALIGN(4) avoids artificial input padding; final linker alignment restores original owner padding. No instruction or relocation edits. Three external ABS metadata differences in each isolated mixed ELF: D_C2D90 and regional system pointer NOTYPE -> OBJECT, callback NOTYPE -> FUNC. Same names, values and sizes; preserve differences pending canonical global checks. First script replay failed comparing local FILE symbols; exclude FILE only, not external ABS. No whole data/rodata proof.

Replay from authenticated extracted regional upstream with MIPS binutils on PATH and runtime libs available:

    python3 replay.py --usa-upstream /path/to/usa/mnsg-japan --jp-upstream /path/to/jp/mnsg-japan --ledger /path/to/Goemon-64-Tools/decomp/COMPILER_QUIRKS.md --output replayed.json

Original detailed local replay JSON SHA256 dd27011419f1915200bd89bc01544f386aaf0e8da259d0beca654638824b3084; full JSON in the source-only ZIP delivered in the originating conversation. Source variants derived deterministically from the exact combined tails; isolated source hashes equal initial standalone sources. Replay writes all detailed relocation tuples, proof and source hashes. Original ledger hash may differ after append; code/relocations and positive and negative outcomes must not.

Actual-source host tests:

    for cc in gcc clang; do
      for region in USA JAPAN; do
        "$cc" -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -fno-strict-aliasing -fno-pie -no-pie -Wno-pointer-to-int-cast -Wl,--defsym,D_C2D90=0xc2d90 -D"$region" test_host.c -o /tmp/warp-host
        /tmp/warp-host
      done
    done

Four GCC/Clang ASan/UBSan 64-bit runs PASS, 131076 calls per run (524304 total). GCC 32-bit layout assertions compiled both regions with -m32 -DFREESTANDING32 -O2 -ffreestanding -fno-builtin -fno-stack-protector -fno-pie -no-pie -nostdlib -static -Wl,--defsym,D_C2D90=0xc2d90 and -DUSA/-DJAPAN. 32-bit execution blocked by Exec format error; no 32-bit runtime or gameplay claim. Layout independently verified by native IDO stores. No canonical count overlap; broad pending PR filenames #250/#202/#200/#194/#191/#190/#186/#184/#183 no address-name hit, not exhaustive pending manifest audit. Full canonical candidate G2, strict inventory, promotion integrity NOT_RUN. Retain ASM. No toolkit changes. Next spawn caller 801CB5D0 / JP counterpart, then Warps owner USA 0x37C00 / JP 0x37870.
