# Engine-state mode and byte-latch trace

This note records instruction-backed behavior for the adjacent engine-state
helpers. Field names describe observed addresses and widths; no semantic names
are inferred for the latch bytes.

## G64-067 — `func_8003A138_3AD38`

The target is a 35-word / 140-byte leaf at VMA `0x8003A138`, ROM
`[0x3AD38,0x3ADC4)`. The pinned `392E0.s` slice matches both SHA-verified USA
ROM images. Its SHA-256 is
`031705fa6374a1c63de6e57a830755039d9d568c17aaf2fa864d78bef32014c5`.
It has no stack frame or call instructions.

### Entry and table mapping

The queue dispatcher at `0x80038F68` stores the full queue word to
`D_801C0A20` before using the low halfword to choose an indirect command-table
entry. Entries 7, 8, 9, and 10 in the table at ROM `0x6F1CC` all point to this
helper. A separate direct call at `0x80039008` stores 10 to `D_801C0A20` in
the `jal` delay slot, so that call follows the mode-10 branch.

The target reloads the full 32-bit `D_801C0A20` word and uses it both for the
equality check against 10 and as a byte-table index. It does not mask or range
check that word. The lookup expression is `D_8006E601 + mode`; that symbol is
seven bytes before the four-byte table at ROM `[0x6F208,0x6F20C)`. For the
demonstrated command modes 7–10, the byte results are `{1, 2, 8, 8}`. The
table layout and these four values were checked in both USA images.

### Branch effects

- For any mode other than 10, the target reads `D_801C09D3` as an unsigned
  byte. If it is zero, it writes byte `0xFF` there. It then reads the indexed
  table byte and stores that byte separately to `D_801C09D1` and
  `D_801C09D2`. The `D2` store is in the return delay slot.
- For mode 10, it performs the same zero-to-`0xFF` latch update at
  `D_801C09D6`, then stores the indexed byte separately to `D_801C09D4` and
  `D_801C09D5` before returning.
- Nonzero latch values are preserved. These paths do not write `D7`, the
  neighboring `D8` halfword, `DA`, `DB`, or `DC`; the adjacent helpers use
  those locations independently.

The instructions establish a full-width word load and address addition, but
they do not distinguish signed from unsigned C declarations for that word.
The two latches are unsigned byte reads, and all six output/latch accesses are
byte-sized. The observed command modes and direct call do not establish what
other producers may place in the word.

### Host reference and native probe

`test_engine_state.c` models modes 7–10, the `{1, 2, 8, 8}` mapping, zero and
nonzero latches, distinct `D1`–`D7` sentinels, and untouched `D8`–`DC`
neighbors. A synthetic mode `0x100` distinguishes full-word indexing from
low-byte truncation; it is a host edge case, not a claim about normal runtime
input. The ASan/UBSan host reference passes. A temporary mutant that casts the
mode to `u8` is rejected by the `0x100` case.

One pinned-IDO 5.3 source-unit hypothesis used a 32-bit mode local, unsigned
byte latches, one indexed table load per branch, and separate byte stores. The
complete 784-byte `engine_state.c` unit linked at its original VMA. The
candidate target was 140 bytes and all eight neighboring C/ASM functions
matched. The target first differed at instruction offset `+0x10` (`0x8003A148`),
with the first differing byte at `+0x13`: IDO placed the mode-10 latch address
calculation in the branch delay slot and moved the non-10 latch address
calculation into the fallthrough body. The original delay slot forms the
non-10 latch address. This is a code-generation scheduling mismatch; stop
after this one v2 hypothesis and keep the production target `GLOBAL_ASM`.

No fresh full-ROM G2 or live-game check was run. Production source, manifest,
stored proof, and inventory remain unchanged. See
[`plans/execution/2026-11-14-g64-067-engine-state-mode-map.json`](plans/execution/2026-11-14-g64-067-engine-state-mode-map.json).
