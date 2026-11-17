# Oedo Castle Mr. Arrow native saved-event writer — USA live capture and USA/JP original-MIPS pair

**Research date:** 2026-11-17. **Branch:** `chatgptweb/decomp`. This report distinguishes a user-observed original-USA Project64 debugger stop from independently authenticated original-USA and Japanese rev-0 MIPS instructions. No ROM, save file, register dump or screenshot is committed.

## USA Project64 debugger observation (user supplied)

After attempting the Oedo Mr. Arrow pickup, Project64 paused on original USA code PC **`0x80024084`** (native saved-event setter, the final byte-write instruction `sb t5,0(v0)`). The reported key registers were:

| Register | Captured value | Evidence |
| --- | --- | --- |
| `A0` | `0x00000104` | Native setter is passed packed bank-C bit ID **260** |
| `V0` | `0x8015C628` | Original-USA saved flag byte |
| `T4` | `0x10` | Bit mask for bit 4, matching bit ID `0x104` |
| `T5` | `0x10` | Byte value about to be stored, not necessarily a previously stored value |
| `S0` | `0x8016B530` | Actor/context pointer retained by the caller |
| `RA` | `0x08000148` | Return address, which identifies `jalr` call at **`0x08000140`** |

This is first direct runtime confirmation that the Mr. Arrow pickup reaches the **saved-event flag setter with ID `0x104`**. Earlier research had established original instantiated room-file 835 actor definition 13 with actor type `0x087`, field `0x0104`, and JP analogue at stage 4, but **not** its actual native writer. This runtime capture fills in the writer.

**Namespace caution:** the *other* occurrence of numeric `0x104` in resource 77 launches **VM event ID 260**. It is not this write. The observed source here is a separate actor callback in resource 26.

## Original ROM evidence — native caller in resource 26

ROM original compressed-release identities were checked through their previously authenticated 32 MiB decompressed products (SHA-1s below). The file table independently locates resource 26 in each region:

| Field | USA NG5E | Japan rev-0 NG5J |
| --- | --- | --- |
| 32 MiB decompressed ROM SHA-1 | `6ea0ed71032ce08fc2745f412d84936382197494` | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` |
| Resource 26 file start | `0x6AE7E0` | `0x6B3360` |
| Callback function start, resource-relative | `+0xCC` | `+0xCC` |
| Native setter call, resource-relative | **`+0x140`** | **`+0x130`** |
| Native setter call as loaded overlay VMA | **`0x08000140`** | **`0x08000130`** |
| Absolute decompressed-ROM call offset | `0x6AE920` | `0x6B3490` |
| Regional native bank-C setter address | `0x80024038` | `0x80023CF8` |

Both original regional ROMs contain the following three-instruction call pattern:

```asm
# USA resource 26, relative +0x138..+0x144
lui   t9, 0x8002
addiu t9, t9, 0x4038
jalr  t9
lhu   a0, 0xD0(s0)   # delay-slot argument

# Japan resource 26, relative +0x128..+0x134
lui   t9, 0x8002
addiu t9, t9, 0x3CF8
jalr  t9
lhu   a0, 0xD0(s0)
```

The callback has an original 32-byte-stack function prologue at `+0xCC`. At `+0xDC`, original MIPS reads the actor's `+0x68` word, masks the `0x200` bit at `+0xE8`, and branches around the setter if the bit is absent. This is a condition on the actor state, not a bit in the persistent saved-event bank.

Given the USA live `S0=0x8016B530`, the original **`lhu a0,0xD0(s0)`** instruction reads the actor's 16-bit flag field at guest RAM **`0x8016B600`**. The observed `A0=0x0104` means this instruction supplied flag ID `0x104`. **The memory contents of `0x8016B600` have not yet been independently screenshot-verified by the user.** This can be checked read-only with Project64 paused.

The Japanese original function is shorter than USA: the JP helper call occupies `+0x130` versus USA `+0x140`, while retaining the same actor-flag field offset `+0xD0`. Do not automatically transfer the USA **overlay code address** or actor pointer to Japanese RAM. The paired **saved bank-C storage location** for this bit is JP **`0x80161E18 & 0x10`**, based on independently verified JP native flag helper base.

## Relation to preceding Ghost Toys traces

The earlier user-recorded Ghost Toys torches use a distinct native setter call at **resource 40 `+0x168`**, with the same actor field offset `+0xD0`, supplying flag IDs `0x19A` and `0x19B`. Their entrance controller sets `0x19C` at resource 43 `+0x64D0` after testing both. This new Mr. Arrow capture demonstrates **reuse of the common native packed-event setter**, not identity of the high-level callback. Source resources and callback offsets differ: Ghost Toys actor writer resource40 `+0x168`; Mr. Arrow writer resource26 `+0x140` (USA).

## Verification performed and remaining gaps

**Executed on local authenticated original-ROM images:** verified USA SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494` and JP SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, extracted original resource-26 intervals, and checked exact MIPS words for the regional target address load, `jalr`, delay-slot `lhu a0,0xD0(s0)`, function prologue and actor state-word read. **Both regions PASS**. Original MIPS disassembled locally for interpretation. The user's real Project64 GPR capture is **direct USA runtime execution evidence**.

**Not run:** live JP pickup, live inspection of USA `S0+0xD0`, verification of which room-definition loader copies record `+4..+5` into actor `+0xD0`, actual item visual/collision path, fresh native C compilation or original-address match, full-ROM G2/ELF inventory, full local decomp CI. **No new matching-C promotion**. At start, accepted baseline remains USA **779**, Japan **34**.

**Next single Project64 step:** while paused, inspect two bytes at USA guest RAM `0x8016B600`; expected `01 04`. This establishes the runtime actor field storage directly and closes one remaining gap without writing any memory.
