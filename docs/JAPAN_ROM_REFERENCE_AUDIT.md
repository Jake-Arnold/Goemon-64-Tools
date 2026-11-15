# Cross-region ROM MIPS reference audit — 15 November 2026

## Inputs and method

Both original decompressed 32 MiB, big-endian ROMs passed exact SHA-1 verification:

- USA: 6ea0ed71032ce08fc2745f412d84936382197494
- Japan-0: 6f8745fecc3a5e7d4918c7a73353eb0726116ded

Read-only scanner: practice/rom_layout_audit.py. It looks for MIPS LUI instructions followed within 16 instructions by a load or store whose base register matches and whose SIGNED low immediate resolves to an aligned 32-bit word containing the mapped unlock byte. It outputs instruction operation counts and ROM file offsets only. There is no ROM data in the repository.

## Results

**23 of 34 candidate aligned-word pairs have exactly matching direct access-operation counts** in the USA and Japan images. This is stronger than the regional delta alone, but does not prove byte/item identity. Indexed loads, pointer arithmetic and variable registers can explain absent or unequal direct references.

| Candidate | USA aligned word | Japan aligned word | USA and Japan direct operations |
| --- | --- | --- | --- |
| Goemon party | 0x8015C69C | 0x80161E8C | 1 lw, 1 sw each |
| Ebisumaru party | 0x8015C6A0 | 0x80161E90 | 1 lw, 1 sw each |
| Sasuke party | 0x8015C6A4 | 0x80161E94 | 1 lw, 1 sw each |
| Yae party | 0x8015C6A8 | 0x80161E98 | 1 lw, 1 sw each |
| Bazooka candidate | 0x8015C6D8 | 0x80161EC8 | 1 lw, 1 sw each |
| Medal of Flames candidate | 0x8015C6DC | 0x80161ECC | 3 lw, 1 sw each |
| Sudden Impact candidate | 0x8015C6EC | 0x80161EDC | 3 lw, 1 sw each |
| Magic Mermaid candidate | 0x8015C6F8 | 0x80161EE8 | 1 lw, 1 sw each |
| Four treasure aligned words | 0x8015C858..864 | 0x80162048..054 | 1 lw each |

Notable nonmatches include Gold Key, Triton Shell and Fortune Doll: neither image exposes a direct reference in the scanner, likely because accesses are indirect. The main Goemon upgrade aligned word has 24 USA and 21 Japan lw hits plus one sw each. A changed count is not proof of a bad address.

**Important limitation:** 32-bit word accesses to a word containing a flag cannot independently identify a particular byte in that word. The inferred Sasuke battery address at 0x80161DF9 remains a guess even though its aligned word appears in both scans. The four treasures' identities remain unverified; matching read operations establish only array correspondence.

## Reproduce locally

Run both existing toolkit test runners without ROMs for the four synthetic scanner unit tests. Optional exact-ROM scan on local Windows or Linux uses the two environment variables GOEMON_USA_DECOMPRESSED and GOEMON_JAPAN_DECOMPRESSED pointing to their decompressed 32 MiB images. The runner invokes practice.rom_layout_audit --summary when BOTH are set. A standalone full metadata report can be generated with:

    python -m practice.rom_layout_audit --usa /path/to/usa.decompressed.z64 --japan /path/to/jp.decompressed.z64 --output /tmp/goemon-rom-ref-audit.json

Never commit decompressed ROMs or diagnostic snapshots. The CLI verifies exact image hashes, outputs only guest addresses, operation types and ROM offsets, and does not modify game assets. No live Project64 or GUI test was performed by this ROM scan.

## Next evidence step

Inspect the referencing functions and compare their control flow for Bazooka, Goemon/Ebisumaru party and treasure slot dispatch; test inventory changes live before promoting individual names to confirmed. Maintain the mapping provenance labels in practice/region_unlocks.py.


## Second-pass direct/indirect reference and matching instruction-context analysis

A separate research CLI, practice/rom_context_audit.py, conservatively tracks LUI-derived register constants through selected MIPS arithmetic and movement instructions for up to 64 instructions, stopping at a branch/jump delay slot and invalidating overwritten registers. It compares **eleven-instruction opcode/register-shape windows** around accesses. Literal immediate and branch targets are masked, not raw instructions exported. It is deliberately distinct from the prior first-pass direct scan so its 23/34 baseline remains reproducible.

On the same two verified original decompressed 32 MiB images:

- **30/34 candidate aligned-word pairs** have at least one identical 11-instruction shaped access context (same load/store mnemonic). This supports related code paths, not named byte identity.
- **26/34 pairs** have exactly matching deduplicated read/write mnemonic counts in this deeper bounded tracker.
- **4/34 without observed paired context**: Gold Key, Cucumber, Lord's Pass, and Achilles' Heel. Not disproven: all four can be accessed via pointer/indirect pathways not resolved by static local register tracking.
- **4 additional pairs** have matching opcode context but unequal operation counts: Sasuke kunai upgrade and red/blue/yellow fish. This is consistent with region-specific code paths; one shared code path is identifiable, but inventory semantics remain unproven.
- Triton Shell and Silver Fortune Doll progress gain identical bounded-context references despite having zero matches in the first-pass direct scanner.

Especially useful Bazooka evidence: USA ROM offset 0x006724B0 uses a word load from aligned guest 0x8015C6D8; Japan ROM offset 0x00677190 loads aligned guest 0x80161EC8 with the same eleven-instruction shape, including corresponding conditional control flow. This strongly supports regional structure placement, not identification of the last byte as the Bazooka item flag.

**False confidence example:** the guessed Sasuke battery field's matched store at USA offset 0x00024D50 / Japan 0x00024A10 is inside a byte-clearing loop (four sequential zero stores), not a demonstrated battery-acquisition handler. Keep both the byte/bit mapping and item name classified as a guess. Matching instruction context can reflect initialization logic.

Local reproduction after setting the two exact-ROM environment variables:

    python -m practice.rom_context_audit --usa /path/usa.decompressed.z64 --japan /path/japan.decompressed.z64 --summary

For the platform test runners, GOEMON_ROM_CONTEXT_AUDIT=1 opts into this *additional* full-ROM scan when both ROM path variables are already set. The six new ROM-free synthetic unit tests always run in the standard toolkit backend suite. The actual PR toolkit suite still needs native Windows/GUI verification.

The context scanner is bounded, flow-insensitive across branches, and not an executable-code-only disassembler. Treat results as *correlation*, not control-flow or gameplay proof.

## Distinguishing reads from initialization-only matches

The 30/34 matching local instruction contexts have different evidence strengths:

| Correlation type | Count | Interpretation |
| --- | ---: | --- |
| Identical local read context (load) | 26 | At least one corresponding read path; still only word-level alignment |
| Identical context, but stores only | 4 | Could be initializer/clearing logic; weaker evidence for item names |
| No paired local context | 4 | This scanner cannot resolve the address; not evidence against it |

The **four store-only matches** are Sasuke kunai upgrade, Sudden Impact, Mini Ebisumaru, and Magic Mermaid. The **four with no matched context** remain Gold Key, Cucumber, Lord's Pass, and Achilles' Heel. A matched read alone is not proof of acquisition logic or of a bit-mask, particularly when the code reads aligned words and the UI edits the last byte.

Seven ROM-free synthetic tests were run locally and passed, including a new check that a shared write-only pattern does not count as a paired read. The output JSON and --summary now expose `paired_read_context_count` separately from `paired_context_count`.
