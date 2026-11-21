# Goemon original-address gameplay callback C matches — 21 November 2026

**Tier: ISOLATED_EXACT / RESEARCH_ONLY. No matching-C promotion.**  
**Branch:** `chatgptweb/decomp`, not `main`.  
**Original pin:** `klorfmorf/mnsg` at `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.  
**Original expanded ROM SHA-1:** Japan `6f8745fecc3a5e7d4918c7a73353eb0726116ded`; USA `6ea0ed71032ce08fc2745f412d84936382197494`.

## Three newly reconstructed native-exact C functions

| Region | Original function | ROM offset | Original extent | Native IDO original-address match | Original instruction SHA-256 |
|---|---|---:|---:|---|---|
| Japan | `func_8001F580_20180` | `0x20180` | 100 B | **25/25 instructions, 100/100 B** | `e786bf75d6768439d6b594cdb37b3793b20c5819c39bfcfff78900166e97fc22` |
| USA | `func_8001F8B0_204B0` | `0x204B0` | 100 B | **25/25, 100/100 B** | `ae5cfb9862bed41b69be6c133a0473858409b317f0aed7f7075006a7346e542d` |
| Japan | `func_8001F70C_2030C` | `0x2030C` | 68 B | **17/17, 68/68 B** | `0bd79310cccf59aa36aace43cff81b4968f37625ade36ce5475e82b373ba5ef4` |

**Net new research: JP 2 functions/168 bytes and USA 1/100 bytes.** All three were absent from the inspected live accepted manifests and the Japanese 1,686-source local G2 candidate set. These counts must not be added to canon without a complete region ROM gate.

### C mechanism

The 100-byte dispatcher copies three callback pointers from a constant global table into a local `Table` aggregate and invokes the entry selected by `g_system_ptr[0x3ADDE]`. The Japanese table is at `0x80071210` and the USA table at `0x8006B730`. Original machine code has no bounds check on the selected phase byte. **No invalid phase index or gameplay exploit has been demonstrated.** Japan's entries are initialization `func_8001F5E4`, per-update Start handler `func_8001F610`, and teardown `func_8001F70C`.

The 68-byte Japanese teardown calls `func_80004170`, then `func_80034B68` with `D_80072E08`, then sets `g_system_ptr[0x3ADDF]=1`. Its USA corresponding 68-byte `func_8001FA3C_2063C` is **already canonical matching C**. The Japanese initialization `func_8001F5E4_201E4` also compiled 11/11 exact in this work, but belongs to the existing JP2118 local G2 batch; it was not counted.

Earlier original-address dispatcher C had 23/25 instruction words (ordering mismatch). The aggregate-initializer source form here reproduced **all 25/25** in both regions without adjusting compiler flags or excluding mismatched instructions.

## Remaining targets and precise negative evidence

| Japanese original function | Original size | IDO result | Status |
|---|---:|---|---|
| `func_8003D0D8_3DCD8` script reset manager | 548 B (137 instructions) | Best bounded candidate **30/137** words; compiled 560 B instead of 548 B; first mismatch `+0x08` | **FAILED_NATIVE** |
| `func_8001F750_20350` pause state controller | 2184 B (546 instructions) | m2c-derived trial **16/546** words; compiled 2064 B instead of 2184 B; first mismatch `+0x00` | **FAILED_NATIVE** |

The script reset manager's active owner-pointer null gate, ID `-1` cursor clearing at JP `0x8003D1C8`, and VM state clear sequence are original-MIPS known, but its C source form/register allocation remains unproven. The pause handler has a 14-entry phase switch (0–13), with original phase-1 logic invoking `func_8003D098_3DC98` at `0x8001F800` after a completion helper returns zero. No matching-C claim can be made for either.

A source-only original-ROM verifier, both research-only failing candidates, and complete detailed test record are provided as the user-visible archive `goemon_glitch_native_followup_2026-11-21.zip` (SHA-256 `73b2334a4559dc114f09dccd667e34f5cd263f7d8548b3607dd92f34727aa082`). The archive deliberately excludes original ROM/ASM/objects/ELF/compiler/saves.

## Verification actually performed

- **PASS**: independently SHA-1-verified original expanded Japan and USA ROMs (32 MiB each).
- **PASS**: original IDO 5.3 `-O2 -mips2`, original VMAs and complete instruction bytes, **7/7 original-address targets / 211/211 instructions / 844/844 tested bytes**. Four targets were from prior research, including a previously accepted USA VM-busy function; only three are newly identified here.
- **PASS**: GCC host (ASan+UBSan) synthetic Japanese dispatcher phases 0–2 and teardown order/state, and USA dispatcher phases 0–2.
- **PASS**: Python verifier syntax, source-archive ZIP integrity and original ROM SHA-1.
- **FAIL, expected**: reset-manager and pause-handler native code candidates; detailed counts above.
- **NOT RUN**: original full 32 MiB ROM build with newly staged sources, original ELF function/relocation comparison, strict inventory, full `decomp.local_ci`, live emulator gameplay and the Bomb Text Skip frame trace. No production source/manifest/accepted-C count has changed.

## Next

For promotion, integrate *only the three new* sources against a fresh canonical `chatgptweb/decomp` checkout, preserving all accepted JP and USA code, pass the strict per-region full-ROM/ELF/semantic-relocation/inventory/full-CI gates, then commit same-gate evidence and updated `PROGRESS.md`. Keep the 548/2184-byte targets in assembly until native equality is achieved. The Start→pause→VM-reset path remains a static mechanism, not a demonstrated successful Bomb Text Skip.
