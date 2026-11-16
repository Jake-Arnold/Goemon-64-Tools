# Japanese Goemon 64 18-C promotion — 2026-11-16

Verified in two independent pinned upstream checkouts; 18 original-address matching-C functions, 756 original instruction bytes, 14 C translation units. Full expanded 32 MiB ROM and recompressed retail 16 MiB ROM both byte-for-byte identical to the Japanese rev-0 references.

Expanded SHA-1: 6f8745fecc3a5e7d4918c7a73353eb0726116ded
Retail SHA-1: 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b

Includes 8 new C sources, Python Splat/layout staging tool, strict native IDO/relocation/full-ROM verifier, unit tests, clean one-command build, updated complete Japanese manifest and metadata proof.

Run: bash decomp/build_japan_eighteen_c.sh /path/to/fresh-pinned-mnsg /path/to/goemon-dependencies /path/to/goemon-runtime-additions

Important: the existing decomp/japan_asm_baseline.py remains the source of the 22-label and two-BSS-identifier normalization. Do not overwrite that module. This source bundle must be applied on top of the repo at chatgptweb/japanese-decomp-port, prior to running the command. Historical 10-C region manifest must be archived first.

No ROMs, compiler executables, proprietary assembly, game assets or native object files are included.

Adjacent unmatched leads: func_80036D58_37958 (204 bytes), func_80036E24_37A24 (208 bytes), func_80036EF4_37AF4 (100 bytes; current C attempts 96 bytes), func_80036F8C_37B8C (192 bytes), func_8003715C_37D5C (92 bytes).

**Clean-build qualification:** One full original-ROM 32/16 MiB native rebuild completed successfully from an entirely fresh pinned upstream mnsg checkout using the new unattended build script. All 14 source/object hash, relocation, linker map and ELF inventory gates passed. The existing `decomp.region_verify` remains a separately supported interface and is updated in this promotion; the new independent eighteen-C verifier has already passed end to end.
