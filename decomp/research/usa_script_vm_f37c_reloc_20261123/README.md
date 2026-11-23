# F37C named floating-point relocation investigation — USA, 23 November 2026

RESEARCH_ONLY. Live base 1ddb1b0941b0f39d4db6b0a3534fc1f230b51e0e (USA 2316 C / 5047 ASM; VM 57/69). PR #203 owns prior research; this follow-up does not claim a new function or alter any verifier. Authenticated same-commit workflow archive, original pinned upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee, original native IDO 5.3 and complete original expanded USA baseline hash 6ea0ed71032ce08fc2745f412d84936382197494. Original owner 3DBA0, current mixed script_vm.c, ROM 0x3FF7C, VMA 0x8003F37C, 192 B. No new canonical claims.

Seven native source cases: two previous controls and five new bounded variants. The latter all reproduce the named baseline's same 8 instruction-word differences and LO16 movement +8 to +12. Literal: 48/48 instructions, 17/19 original named relocations; only HI16 +4 and LO16 +8 point to .rodata instead of D_8007D108_7DD08. Section-relative addend zero, resolved original target 0x8007D108; 4-byte pool word and all linked instruction bytes exact. Defining a named const float generates writable .data, not the original read-only pool, and retains all eight mismatches. Ordinary linker alias keeps name and address but does not change relocation provenance. Read-only audit rejects four in-memory negative controls (wrong literal word, addend, instruction, linked pool address).

Compiler -S inspections (same original flags except -S instead of -c): literal emits li.s $f0, 0.0 and li.s $f2, 0.1; named emits li.s $f2, 0.0 and l.s $f0, D_8007D108_7DD08. This directly distinguishes compiler register allocation from the assembler's literal-pool expansion. The reconstructed original Splat assembly uses named data label at 0x8007D108; the original retail ROM contains no original ELF relocation metadata. These findings do not prove original C source spelling or permit weakening the reconstructed named-relocation gate. No new generalized compiler quirk claimed. Full new canonical G2 and CI NOT_RUN. No gameplay observed.

## Replay

Use a clean pinned original upstream checkout with the authenticated original-USA ROM decompressed, Splat-extracted and exact baseline built, and authenticated stable repository source. Set REPO, BASE, BIN, LIB and OUT to absolute paths (OUT must not exist). Read live project policy and compiler quirks before native work. From this kit:

```sh
python3 replay.py --repo "$REPO" --baseline "$BASE" --binutils "$BIN" --lib "$LIB" --out "$OUT"
python3 audit_pool.py --repo "$REPO" --baseline "$BASE" --binutils "$BIN" --lib "$LIB" --probes "$OUT"
```

To inspect pre-assembler scheduling use the exact flags listed in evidence/native_probes.json with `-S` replacing `-c`; run in a private scratch copy of BASE because IDO writes basename.s in cwd even when -o is specified. No ROM, original ASM, generated native ASM, object files, proprietary binaries or other private assets in this kit. `replay.py` uses the repository's unchanged decomp.probe parser and comparator. `audit_pool.py` uses only read-only inspections and ordinary isolated linking; it never changes production ELF or relocation records.
