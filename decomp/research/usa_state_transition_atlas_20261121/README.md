# USA original-ROM state transition atlas — 21 November 2026

Deliverable: machine-validated **read-only static graph** of the engine's 18 outer state handlers and a new cross-overlay connection between main state 3 and state 4. No C matching claim or game-memory write.

- `STATE_TRANSITION_ATLAS.md`: human-readable analysis, evidence levels and read-only runtime capture proposal.
- `state_atlas.json`: all 18 entries, 20 direct canonical setter call sites, four increment-helper call sites, select known loader sites, state-15 five-way table, file22 two-way table and direct state-4 store.
- `verify_static_atlas.py`: SHA-1 gated checker of authentic ROM pointer tables, selected MIPS instruction **properties**, target calls, argument anchors and overlay stores. No ROM opcode dumping.
- `test_static_atlas.py`: schema/provenance/decoder checks; optional original-ROM integration case.
- `proof.json`: sanitized result from original USA 32 MiB image; no copyrighted bytes.

Execute from this directory:

```bash
python3 -m unittest -v test_static_atlas
GOEMON_DECOMPRESSED_ROM=/path/to/private/baserom.decompressed.z64 python3 -m unittest -v test_static_atlas
python3 verify_static_atlas.py --rom /path/to/private/baserom.decompressed.z64 --report /tmp/proof.json
```

Status `STATIC_ROM_VERIFIED / RESEARCH_ONLY`: this is not original IDO 5.3 matching-C promotion and does not modify the canonical manifest, accepted C counts, ELF relocations or ROM.
