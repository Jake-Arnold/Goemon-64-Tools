# Japanese rev-0 matching-C import into canonical decomp (17 November 2026)

This is a **selective regional integration**, not a whole-history merge of the diverged Japanese and USA development branches. The 34 Japanese matching-C functions, 30 C units, strict original-address manifest, native IDO/ROM build pipeline, independent verifier, and 8 targeted unit tests were copied without changing the USA manifest, generated build settings or any USA source.

## Verification

- Pinned `klorfmorf/mnsg` checkout: `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
- Independent fresh Linux reproduction from the 34-function verified package: IDO 5.3, GNU MIPS linker and Rommy; original 32 MiB SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, original 16 MiB SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`, both byte-identical.
- Independent strict verifier: 34 original guest functions / 1,912 machine-code bytes, 30 C source units, 7,376 ELF game-function identities (7,342 assembly-owned), 73 sections, zero unreviewed unmarked.
- ROM-free tests: 8/8.
- All 30 imported production Japanese C files were compared by Git blob hash to the independently reproduced package. SHA-256 of tested source package: `7d0c80741ee7fdb5c3c780601c536fcca9e8dde51363b3267a9e6b1585fdcf96`.

## Region isolation

Canonical USA remains **342 matching-C functions / 17,568 instruction bytes** according to existing USA proof. Do not sum the Japanese function count with USA, share generated Splat assets, or apply Japanese addresses to USA ROM data.

The native Japanese reproduction entrypoint is `bash decomp/build_japan_thirtyfour_c.sh <fresh-pinned-upstream> <dependencies> <runtime>`. A complete fresh combined-branch run of that published wrapper, USA G2, and full `decomp.local_ci` was not performed in this merge session; the fresh verified-runner execution was from the supplied source package. Emulator gameplay and PC-native recompilation were not run.

The five newer isolated adjacent Japanese candidates were deliberately **not** imported as production functions. Their correct acceptance gate is a further fully linked and recompressed 39-C Japanese ROM and strict ELF verifier.

No ROMs, compiler binaries, generated original assembly, saves, or game assets are included.
