# USA return-extent and transition dispatcher research

RESEARCH_ONLY / ISOLATED_EXACT. Base 0ad88225c1a11f85454b259103f0f4c6ff49fa16; source archive artifact 15183344072 (archive checksum PASS); original USA expanded SHA-1 6ea0ed71032ce08fc2745f412d84936382197494, authentic IDO 5.3 SHA-256 76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0. The private original baseline rebuilt byte-exactly; its native provenance is the supplied upstream archive, not a fresh Git checkout (direct Git DNS blocked).

12 distinct USA functions, 320 original bytes, 6 named relocations. Ten are independently replayed previous-session findings; two new ones are func_080073DC_6BA67C (32 B) and func_080072D0_6C6A20 (24 B). Each candidate and independent pristine reference were assembled/linked at its original VMA, with exact ROM bytes, original extent and symbol identity, exact named relocations and rejected altered-source controls. Eleven O0 functions also reject the O2 control. No original ASM/ROM bytes or binaries are published. A 350-target O2/g3 sweep produced 312 mismatches, 28 compile failures, 9 near misses, 1 m2c failure, zero exact matches. The repeated-return form is narrowly demonstrated, not a rule for all trailing returns.

Canonical claims at base USA 3167 / JP 3107 unchanged, no overlapping USA canonical ranges in the replay. No full candidate G2, whole source-owner, strict candidate inventory, stable-global or full semantic relocation audit run. No independent new Japan work; USA 100 target incomplete. Retain ASM ownership. Do not merge as a promotion.

## Reproduction

Place this directory at `decomp/research/return_extent_20261127` in a complete repository checkout. Use a private pristine USA Splat upstream with the original expanded ROM, exact original baseline ROM and ELF in build/usa and authenticated IDO toolchain. Put pinned MIPS binutils on PATH and set their runtime library path. Use a new work path outside the repository.

```sh
python3 decomp/research/return_extent_20261127/replay.py /path/to/private/mnsg /path/to/new-private-work
```

Requires the repository's existing decomp modules. `candidates.json` pins C hashes and exact flags; `evidence.json` records actual observed outcomes against the pre-edit ledger. Negative controls are compiler-only fixtures and must not run in game. The replay writes private intermediate binaries only outside the repository. Future replay after the ledger update will record the updated ledger hash.
