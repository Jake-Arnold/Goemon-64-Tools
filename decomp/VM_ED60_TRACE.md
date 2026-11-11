# G64-037: original trace for `func_8003ED60_3F960`

**Result:** `RESEARCH_ONLY`. The 592-byte function remains `GLOBAL_ASM` in
`script_vm.c`. The trace and one bounded IDO probe establish a narrow
`void func_8003ED60_3F960(void)` signature and the observed memory contract;
they do not establish a full C match.

## Pinned extent and ownership

- USA decompressed ROM SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`.
- Function VMA: `0x8003ED60..0x8003EFB0` (592 bytes / 148 words).
- ROM offset: `0x3F960`; mapping used by the guard is `ROM offset = VMA - 0x7FFFF400`.
- Function extent SHA-256: `18db53295f30fa73a9808f3bed402aa085e97de238dfa36d25455f19dac8d89b`.
- The next verified symbol, `func_8003EFB0_3FBB0`, begins exactly at `0x8003EFB0`.
- The live manifest places the target in `script_vm.c`'s `assembly_functions` list;
  the source retains its `GLOBAL_ASM` pragma and `script_vm.h` declares
  `void func_8003ED60_3F960(void)`.

## Caller and ABI

An aligned raw scan of the pinned 32 MiB ROM found one direct JAL encoding to
`0x8003ED60`: ROM offset `0x3FC20`, VMA `0x8003F020`, inside the 136-byte
`func_8003EFB0_3FBB0` caller. The original caller loads the 32-bit
`D_8007785C`, compares it with `0x100`, and uses `beql` to skip the call when
equal. Thus the handler is called when `D_8007785C != 0x100`. The C caller and
header agree that it takes no arguments and returns no value. This scan
establishes direct JAL ownership; it does not rule out indirect references.

The handler itself reads no incoming argument register before assigning the
registers it uses. It calls `func_8003F038_3FC38` twice, each time with:

- `$a0 = *(s32 *)0x8007785C`, freshly loaded at that call site;
- `$a1 = 0`, set in the JAL delay slot;
- `$v0` returned as a 32-bit value.

The first return controls whether the output path runs. The second return is
stored as the second word of the third output pair. The helper's own effects
and higher-level meaning are outside this trace.

## Control-flow map

1. **Entry and first call (`ED60–ED7C`).** Allocate `0x30` bytes, save the
   caller RA at `sp+0x14`, load `D_8007785C`, then call `F038`. The ordinary
   `beqz` at `ED78` exits to `EFA0` when `$v0 == 0`; its `lui` delay slot at
   `ED7C` executes on either path.
2. **Pointer and state gates (`ED80–EDA8`).** Load a 32-bit pointer from
   `D_80167C48`. A null pointer and a zero 32-bit value at pointed offset `0`
   each take a branch-likely exit to `EFA4`; the `lw ra,sp+0x14` delay slot
   executes only on the taken path. Otherwise read a **signed halfword** at
   pointer offset `0x30`. Values other than `4` branch to `EFA0`; the branch
   delay slot forms address `0x8016C5CC`.
3. **Output path (`EDAC–EF9C`).** Read a pointer from the 32-bit global slot at
   `0x8016C5CC`. For every pair, advance the stored pointer by eight bytes and
   write two 32-bit words to the old pointer. The second helper call's pair
   pointer is spilled at `sp+0x18` in its delay slot, restored through `$ra`
   after the call, then used to store `$v0` at offset `+4`. This temporary use
   does not replace the original saved RA at `sp+0x14`.
4. **Return (`EFA0–EFAC`).** Restore the saved RA, release the `0x30`-byte
   frame, return, and execute the `nop` delay slot. Early exits converge on
   `EFA0` or `EFA4` as recorded above.

The branch destinations, likely delay slots, helper calls, global cursor slot,
and function/caller extents are guarded by
[`test_vm_ed60_original.py`](test_vm_ed60_original.py). Its private-ROM check
also pins the complete 592-byte function hash.

## Observed output writes

On the successful gate path, the function advances the cursor twelve times by
eight bytes (96 bytes total) and writes these ordered pairs. Values below are
raw words observed in memory; command names and rendering effects are not
inferred here.

| Pair | First word | Second word |
|---:|---|---|
| 1 | `0x06000000` | `0x800777F0` |
| 2 | `0xBA000E02` | `0x00000000` |
| 3 | `0xFD100000` | second `F038` call's `$v0` |
| 4 | `0xF5100000` | `0x07054150` |
| 5 | `0xE6000000` | `0x00000000` |
| 6 | `0xF3000000` | `0x073FF100` |
| 7 | `0xE7000000` | `0x00000000` |
| 8 | `0xF5101000` | `0x00054150` |
| 9 | `0xF2000000` | `0x0007C07C` |
| 10 | `0xE4000000` combined with packed values below | packed values below |
| 11 | `0xB4000000` | `0x00000400` if `D_8007785C & 1` is zero; otherwise `0x04000400` |
| 12 | `0xB3000000` | `0x10000400` |

For pair 10, let `a = D_801C7758` and `b = D_801C775C`, each loaded as a
32-bit word. These are algebraic aliases only; no field or gameplay meaning is
assigned. The first word is:

```text
0xE4000000 | ((((a + 46) << 2) & 0xFFF) << 12) | (((b + 61) << 2) & 0xFFF)
```

The second word is:

```text
((((a + 15) << 2) & 0xFFF) << 12) | (((b + 30) << 2) & 0xFFF)
```

The arithmetic follows 32-bit MIPS additions and shifts before the `0xFFF`
masks. The original assembly reads both coordinate globals but does not store
to them.

## Global widths and unknowns

| Address / current declaration | Observed access | What the trace supports |
|---|---|---|
| `D_8007785C_7845C` (`s32`) | `lw` | 32-bit value passed to both helper calls and later reloaded for its low bit. |
| `D_80167C48_168848` (declared pointer array) | `lw` of its first word | One 32-bit pointer is checked for null and then dereferenced. |
| pointed object `+0x00` | `lw` | A 32-bit value is checked for zero; its role is unknown. |
| pointed object `+0x30` | `lh` | A signed 16-bit value is compared with `4`; its field name is unknown. |
| `0x8016C5CC` (no source name assigned) | `lw` / `sw` | A 32-bit pointer slot is read and updated twelve times by `+8`. |
| `D_801C7758_1C8358`, `D_801C775C_1C835C` (`s32`) | `lw` | Two 32-bit values feed masked word arithmetic; neither is stored here. |

There is no null check on the output cursor, no buffer-length check, and no
pointer-alignment check. No additional safety behavior is claimed. `F038`
callee effects, the pointer fields' meanings, and the output words' higher-level
semantics remain unknown.

## One bounded native probe

The single trace-derived candidate was compiled with the pinned IDO 5.3
`cc` (`76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0`),
flags `-O2 -mips2 -G 0 -non_shared`, and linked at `0x8003ED60` with the helper
resolved at `0x8003F038`. It was built only under ignored
`practice/diagnostics/decomp-100-inputs/g64-037/`.

- Candidate source SHA-256: `00f2e890deacc5f839416da4707482ed148322c85ddb3f11cb50d50cd5749e3e`.
- Candidate ELF function symbol: **584 bytes**; the linked `.text` section is
  592 bytes including eight bytes outside the function symbol.
- First original-address mismatch: `0x8003ED68`, original `0x3C048007`
  (`lui $a0,0x8007`), candidate `0x3C0E8007` (`lui $t6,0x8007`).
- The 584-byte symbol differs at 136 of its 146 compared word positions.
- Candidate branch at `ED78` also targets `EF98`, eight bytes before the
  original `EFA0`, consistent with its shorter function symbol.

No second source shape was tried: the one probe did not move a prior mismatch,
and the trace has no new compiler hypothesis that warrants another candidate.
The production pragma, header, manifest ownership and stored proof are
unchanged. No host C model was added because opaque helper and field semantics
would require invented behavior.

## Verification and limits

- `python3 -m decomp.test_vm_ed60_original --rom practice/diagnostics/decomp-100-inputs/usa-decompressed.z64`: passed against the exact 32 MiB private ROM, 37 instruction anchors, twelve cursor advances, both helper calls, and one direct caller.
- `python3 -m unittest decomp.test_vm_ed60_original -q`: 4 tests passed.
- Isolated native candidate: nonmatch at `0x8003ED68`; not a source-unit or full-ROM proof.
- `fresh_full_rom=NOT_RUN`; stored proof remains 148/148 functions / 11,020 bytes.
- No in-game verification was performed.
