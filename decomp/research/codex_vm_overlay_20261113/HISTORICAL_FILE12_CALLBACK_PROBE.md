# Original `file_12` dialogue callback isolated-probe notes (13 November 2026)

Source: historical `codex/goemon-vm-overlay-followup` @ `6b5d0d8958bd87fb850c05008acb29650579bf30`, original `decomp/VM_CONVERSATION_TARGETS.md`, appended historical section. This text is preserved verbatim below as a dated research snapshot; its **RESEARCH_ONLY** status applied before later native canonical acceptance.

Both `func_80222034_5DD504` (20 bytes) and `func_80222168_5DD638` (36 bytes) are accepted in the current 1,500-C USA manifest. Their original isolated proof, which was not a full-ROM promotion gate in November 13's snapshot, is preserved separately at [`decomp/results/file12_dialogue_callbacks_research.json`](../../results/file12_dialogue_callbacks_research.json).

---

## File 12 callback follow-up (2026-11-13)

The pinned USA Splat config identifies the callbacks' owner as **`file_12`**,
not `file_43`: ROM `[0x5C8770, 0x5F6840)`, VMA `0x8020D2A0`, text ending at
`0x5E3C90`, data thereafter, and `static_overlay_2` RAM. The verified
decompressed ROM has SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
The text and data SHA-256 fingerprints are
`50365292dbd8cdf7a407114cb88c1807c39bf024e0f5fd4807d192357aad3131`
and `7780f27b76e25d4cd777eb8c35e870e242dcb33675a1214349518d7326397fc4`.
The `file_43` reference guard is for a different overlay and cannot verify
these callbacks.

Two direct C reconstructions under `decomp/candidates/` compile with the pinned
IDO 5.3 `-O2 -mips2 -G 0 -non_shared` flags. The read-only
`python3 -m decomp.probe_file12_callbacks` links each one separately at its
original VMA and verifies the linked ELF function symbol, original ROM/VMA
mapping, section fingerprints, and every instruction byte. The 20-byte copy
at `0x80222034` and 36-byte signed-byte call at `0x80222168` both match
exactly. Each isolated `.text` has 12 trailing zero alignment bytes beyond
the function symbol; those bytes are not claimed as a function match. There
is no mismatching instruction within either function. See
`results/file12_dialogue_callbacks_research.json` for source and original
hashes and tests.

**Status: RESEARCH_ONLY; zero promotions.** The production `manifest.json`
validates only the main-segment `VMA = ROM + 0x7FFFF400` relation. It has no
`file_12` overlay ownership, linked original-unit section/symbol and
relocation proof, or staging adapter. An isolated link cannot establish the
entire `5C8770.s` unit, neighboring symbols, padding, and relocations, and no
fresh full-ROM/inventory gate was run. Keep both functions assembly-owned.
Next, add a fail-closed `file_12` overlay provenance and integration adapter;
then stage one function at a time in the real unit and run original-VMA
whole-unit comparison followed by the fresh 32 MiB ROM and inventory gates.
The existing 11 and 31 static `0x800B` references are search leads, not a
live reachability trace.
