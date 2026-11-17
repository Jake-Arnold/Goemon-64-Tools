# Dual-region Goemon 64 support: foundation (2026-11-14)

## State

**USA-only remains the supported runtime.** This initial research change does not enable Japanese recompilation, Japanese toolkit memory writes, Japanese warps, or interchangeable save files. It deliberately avoids changes to the live UI, checkpoints and USA decomp proof.

The verified source ROMs are 16 MiB:

| Region | N64 code | Canonical .z64 SHA-1 |
| --- | --- | --- |
| USA | NG5E | df8083a54296b8c151917c5333e1c85f014a2a66 |
| Japan | NG5J | 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b |

Japanese input may be .n64 word-swapped; canonicalisation to .z64 precedes hash checks. Only those exact revisions are accepted.

## ROM mapping utility

Run: `python3 -m decomp.region_compare USA.z64 Japan.n64 --output region-spans.json`.

The output contains checksummed identity and exact byte-identical spans in both ROMs, not game assets. On supplied copies: 707 disjoint exact spans, 6,641,072 verified equal bytes (39.6% of the ROM). This is a conservative *lower bound of exactly identical data*, not an estimate of game-code identity or a RAM translation.

Test (ROM-free): `python3 -m unittest tests.test_region_compare -v`. All five synthetic tests passed in the development environment. ROM comparison also completed with both supplied retail dumps.

## Recompilation path

Goemon64Recomp's `mnsg.toml` and `Goemon64RecompSyms/mnsg.syms.toml` target the USA build. Japanese support needs its own decompressed ROM layout, symbols/sections, overlays, patches and N64Recomp output. Do not swap Japanese ROM bytes into the existing USA-generated executable. Initial implementation can use separate regional executables; a shared executable should follow once the code/data/runtime contracts are proven.

## Toolkit path

Keep existing USA addresses untouched. Inventory every absolute guest address, pointer chain and ROM entrance lookup in `practice/`, `autosplitter/`, and C helpers. Build a Japanese profile keyed by **verified running version**, not merely a user-selected filename. Validate foundational read-only runtime state (game state, current map, character, player pointer, event flags) with original Japanese ROM under a suitable emulator before enabling memory writes. Region-aware GUI labels, checkpoint formats and warp commands follow that validation. A ROM-offset match does not establish a RAM address.

## Next verification gates

1. Create and validate Japanese decompressed ROM and original-section/overlay map independently from the USA decomp exact-byte gate.
2. Generate Japanese recomp code with region-specific symbols, confirm all required runtime patches and assets, then test title, load, level transitions, cutscenes and saves.
3. Measure Japanese RAM addresses in a running verified Japanese build and add region-specific read-only toolkit watches.
4. Gate all writes, checkpoints and transitions behind region-specific behavioural tests; do not reuse USA-only saved checkpoints by default.

No ROMs, translated assets, memory dumps or executable binaries are committed.
