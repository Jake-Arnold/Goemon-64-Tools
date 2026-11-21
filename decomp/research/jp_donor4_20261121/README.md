# Japanese second donor-template native matching-C wave: four functions

Region Japan-0 only. Four original functions, 120 original instruction bytes, accepted locally after original compiler build, exact 32 MiB expanded ROM, 16 MiB retail ROM, all 7,376 ELF FUNC identities, all 80,747 semantic relocations, strict C/ASM partition, actual C host tests and full CI. Original upstream is pinned `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` (SGI IDO 5.3 `-O2 -mips2`). This wave retains every earlier JP2278 function. Never modify USA or `main`.

Sources: `sources/`, metadata and original offsets: `manifest.json`. Native staging: `decomp/japan_donor4_promotion.py`; fresh reproduction: `decomp/build_japan_donor4_promotion.sh`. There is no copyrighted ROM, disassembly, object, ELF, private save, toolchain or extracted asset in this package.

Research exclusions: `__osSpSetStatus` reproduced the original machine bytes using a numeric hardware address, but this removes two required symbolic relocations, so **it must remain ASM**. Its symbolic-C alternative adds an extra instruction and fails byte equality. Five other attempted short wrappers differed at the first native instruction or register allocation. Those are not matching-C additions. No gameplay emulator test was run.
