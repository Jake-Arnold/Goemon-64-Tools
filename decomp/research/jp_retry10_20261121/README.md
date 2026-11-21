# Japan rev-0: alternate-typed C recovery from previously failed assembly

**Four new native IDO-isolated exact originals** (160 bytes) from the published JP2303 original-ASM remainder: three 44-byte display-list emitters and one 28-byte signed-char predicate.

The **three display-list emitters** only compile to the original registers when the global is declared as `Gfx *g_display_list_head_ptr` and is post-incremented. Earlier `void *` declarations compiled to different registers. Their C sources preserve four original MIPS HI16/LO16 relocation records each, including the global-head pair.

The **predicate** `func_08001410_70F980` is an exact original MIPS match using signed-char equality to five and **an intentionally absent false-path return**. The original MIPS also does not write `$v0` on the false path. Thus this C reconstruction has **undefined behaviour for a caller that attempts to use its false-path return value**. The native code remains byte-identical. Host sanitizers test only the fully specified positive path; this limitation must never be hidden or mistaken for a safe total Boolean function.

The original Japanese expanded ROM, ROM offsets, 7,376 original ELF identities, 80,747 relocations and strict accepted-C/ASM boundary must pass in the full 2,303→2,307 native link. The original 16 MiB retail ROM and full `decomp.local_ci` must also pass. This research bundle never contains ROM, original assembly, binaries or proprietary compilers.
