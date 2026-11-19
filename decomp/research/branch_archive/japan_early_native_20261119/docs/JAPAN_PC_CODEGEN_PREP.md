# Japanese PC-native codegen preparation and fresh USA reference regression

**Date: 2026-11-15. Status: USA reference build exact; Japanese N64Recomp candidate prepared, not executed.**

## Fresh USA reference rebuild

A new independent upstream klorfmorf/mnsg checkout at commit 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee was extracted from the user's project ZIP. The USA retail ROM, offline CPython 3.12/Splat/LZKN64 runtime and GNU MIPS toolchain were reused. The following actually ran:

- Original USA Rommy decompress: PASS; SHA-1 6ea0ed71032ce08fc2745f412d84936382197494.
- Original USA Splat extraction: PASS.
- Native GNU MIPS assembler/linker source rebuild: PASS, 33,554,432 bytes, zero differing bytes.
- Original USA Rommy retail recompression: PASS, 16,777,216 bytes, SHA-1 df8083a54296b8c151917c5333e1c85f014a2a66, zero differing bytes.

This covers the pinned upstream USA reference source. It is **not** the full Goemon-64-Tools USA manifest-based matching-C G2 on the current integration branch, which remains unrun. See decomp/results/usa_reference_regression_2026-11-15.json.

## Japanese PC recompiler candidate

The prior verified five-C Japanese ROM provides a complete original-address linked MIPS ELF. The new generator decomp/japan_recomp_codegen.py uses GNU MIPS objdump to recover code sections, ROM load addresses and positive-sized function symbols from this ELF, independently of USA address guesses. It insists that the source checkout is the pinned upstream commit, that tracked files are unchanged and that both expanded Japanese reference and rebuilt 32 MiB ROMs match SHA-1 6f8745fecc3a5e7d4918c7a73353eb0726116ded and each other exactly.

Output is generated in a new directory (existing destinations are refused):

1. mnsg.japan_0.syms.toml — 72 CODE sections with 7,375 function symbols; 529,035 bytes, SHA-256 2aa804bd2c2718314ac7ab103eeb85855299e196794655e1c8a2f3369fefd0da. Raw IPL3 is intentionally excluded; the sole entry function is named recomp_entrypoint at 0x80000400.
2. mnsg.japan_0.overlays.txt — 57 overlay names .file_24 through .file_80, each confirmed present in the Japanese ELF.
3. mnsg.japan_0.toml — Japanese-only N64Recomp input path, symbols file, overlay list, output folder and entrypoint. No unsupported copy of the USA-only instruction patch.
4. proof.json — output identity metadata; no ROM or extracted game code.

The generated TOML files were parsed successfully with tomllib; native Japanese ELF parsing and six synthetic validation/unit tests passed. This is **candidate symbol metadata**, not successfully recompiled CPU code. N64Recomp may reject/need additional Japanese symbols, overlay relocations, patch hooks or runtime implementations.

To regenerate, from the Goemon-64-Tools repository with GNU MIPS binutils on PATH:

    python3 -m unittest discover -s decomp -p 'test_japan_recomp_codegen.py' -v
    python3 -m decomp.japan_recomp_codegen --checkout /path/to/pinned-mnsg-japan --output-dir /path/to/NEW-output-directory

Generated files stay outside Git and can be copied to an independent, fully cloned upstream Goemon64Recomp checkout for future trials. The corresponding private decompressed Japanese ROM would be named mnsg.japan_0.z64 only in the private working copy.

## Native Japanese game remains blocked

The current upstream Goemon64Recomp dev branch has USA-oriented mnsg.toml, Goemon64RecompSyms/mnsg.syms.toml, overlays, runtime patches and a USA-only GameEntry. Building a PC executable requires running N64Recomp against these Japanese candidate inputs, preparing region-correct RSP functions, overlay relocations and native patches, then registering a Japanese GameEntry tied to Japanese generated code and an exact Japanese ROM identity. The existing decomp/prepare_recomp_region_loader.py covers only ROM decompression source preparation. Registering the Japanese ROM against existing USA recompiled functions would be unsafe and invalid.

Real N64Recomp executable, complete Goemon64Recomp source/submodules and required rendering/build dependencies were not provided in the project runtime and were not installed in this offline environment. Native C++ compile, PC boot and gameplay are **NOT RUN**.

## Japanese N64 emulator check

There is no mupen64plus, ares, or other N64 emulator executable in the uploaded project files or current execution container. Direct network/DNS access is unavailable for installing it. Japanese emulator boot, gameplay, audio, controls and graphical output are therefore **NOT RUN**. Exact 16 MiB Japanese ROM reconstruction proves ROM byte identity; it is not evidence of an emulator gameplay test.

The user's original USA/Japan retail ROMs, decompressed ROMs, original assembly, extracted assets, original compiler binaries, and save data must never be committed to GitHub.

Additional proof: decomp/results/japan_pc_codegen_candidate_2026-11-15.json.
