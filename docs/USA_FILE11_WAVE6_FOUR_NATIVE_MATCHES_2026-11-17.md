# USA file_11: four new adjacent native-matching C candidates (17 November 2026)

**Status: research, not production promotion.** Starting from canonical `chatgptweb/decomp` commit `1961f1333e8a5007c3cf8df5dfa0d0ca5a0cea8b`, the USA proof remains **342 matching C functions / 17,568 bytes**, with **179 functions in file_11**. A contemporaneous independent Japanese change did not change that USA G2.

The original PR #24 set of 104 is completely accounted for by the 342-function promotion. **PR #23 still has 82 distinct unpromoted USA functions / 3,512 bytes** after comparing its 114 previously outstanding ROM offsets with the new 179-function canonical file_11 fixture (32 additional offsets have been promoted since that earlier inventory). The best contiguous existing research islands are `0x5B0438–0x5B0598` (9 C / 352 bytes), `0x5AA138–0x5AA30C` (8 C / 468 bytes), `0x5A6F30–0x5A7090` (8 C / 352 bytes), and `0x5B0EB4–0x5B0FB4` (6 C / 256 bytes). These still need a combined central ROM/ELF integration gate.

## Four additional native exact matches

| USA ROM | Original VMA | Bytes | Behaviour |
|---|---|---:|---|
| `0x5A3D28` | `0x801E7E18` | 40 | actor mode in 29–39 or exactly 184 |
| `0x5A3E18` | `0x801E7F08` | 40 | actor mode in 44–48 or exactly 185 |
| `0x5AB904` | `0x801EF9F4` | 36 | state helper for ID 26 returns >=3 |
| `0x5AC4E0` | `0x801F05D0` | 36 | state helper for ID 27 returns >=3 |

Every function is absent from the 179 current production C ownership set, absent from the 82 pending PR #23 set, and absent from the earlier research pool. All four have native **exact original instruction bytes, original symbol VMAs and original function sizes**, using original IDO 5.3 `-O2 -mips2 -G0`, the original 32 MiB USA decompressed ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, MIPS linker `SUBALIGN(4)` and per-function original-VMA linking. **Total: 4 C functions / 152 bytes**.

The local targeted Splat extraction yielded the same 906 original function names and lengths, and all four were matched against the original ROM; its complete assembly text differs from the full-configuration Splat output because unrelated overlay-specific symbols were excluded. Accordingly, no complete Splat-text hash identity is claimed.

## Other short adjacent candidates — not exact yet

`0x5A3C88` (FP easing, 6/10 instructions), `0x5B3050` (scaled float, 6/12), `0x5A7DBC`/`0x5A7DF0`/`0x5A7E24` (three wrappers, each 12/13), and `0x59AA60` (two calls, 10/12) remain **assembly-owned**. No partial matches were counted.

## Stop gate

Full promotion requires a new versioned file_11 adapter and one complete **346-function** central `decomp.verify` G2, exact 32 MiB USA ROM rebuild, original 8,825 semantic file_11 relocations, original symbol inventory, and full local CI. `346` and `17,720` instruction bytes are **projections**, not achievements. No Japanese original-address compilation or full-ROM proof was performed for these four. Official baseline remains **342**. A source-only reproducibility package including a standalone native original-VMA probe and a complete 82-offset dedup list is attached in the project conversation as `goemon-file11-wave6-adjacent-20261117.zip`. No original game ROM, machine code assets, compiled objects or toolchain binaries are committed.
