# Japanese Project64 character-switch MIPS trace (2026-11-15)

**Source and scope:** User-operated Project64 **3.0.1.5664-2df3434** on Windows, running *Ganbare Goemon: Neo Momoyama Bakufu no Odori* (Japan). Evidence consists of Project64's virtual N64 RAM viewer, Commands disassembler, breakpoint/register screenshots, and the user's report of a native C-Down character switch. The original screenshots were supplied in the conversation; **no screenshot files or raw debugger export are committed here**. All addresses below are **guest N64 virtual addresses**, not Cheat Engine host pointers.

**Status:** Dynamic Japanese MIPS evidence for two stores to the active-character index, the direct call into a second routine, and an object-relative character byte. Neither the object type nor the owning ROM/overlay section/function boundaries have been proven. This trace is a manual runtime observation, not a ROM-derived function match or a passing automated test.

Related Japanese RAM A/B evidence: [JAPAN_RUNTIME_CHARACTER_TRACE_002.md](JAPAN_RUNTIME_CHARACTER_TRACE_002.md). Related party flag experiments: [JAPAN_PARTY_WRITE_EXPERIMENT.md](JAPAN_PARTY_WRITE_EXPERIMENT.md).

## Confirmed guest data and object-relative observations

| Address / field | Type | Observed evidence | Confidence |
| --- | --- | --- | --- |
| `0x80161DCC` | u32 BE | Project64 virtual memory displays `00000000` for Goemon and `00000001` for Ebisumaru after native switching, independently of earlier Mupen A/B | **Runtime confirmed for values 0/1** |
| `0x80161DC8` | guest pointer in `V0` | `V0 = 0x80161DC8` at `0x801E2944`; destination `V0+4 = 0x80161DCC` | **Register/address arithmetic observed** |
| `0x8016F780` | `S0`/`A0` in this capture | Object-like pointer passed through the call to `0x801E2970`; do not assume it is stable, a player object or a task pointer | **Observed instance only** |
| `0x8016F7E0` | byte at `S0+0x60` | Memory viewer showed `01`; `LBU A1,0x60(S0)` loaded `A1=1` before the call | **Runtime-confirmed character-related byte in this path** |
| `0x80161DF4` | u32 write destination | `SW T1,0x2C(V0)` has this calculated destination; semantic meaning unknown | **Disassembly/address only** |
| `0x8016F7DC` | `A0+0x5C` | Read by subsequent `LW T7,0x5C(A0)`; meaning unknown | **Disassembly/address only** |

The values 2/Sasuke and 3/Yae remain outside this Project64 step trace, even though separate Cheat Engine observations may exist. Do not interpret a forced write to the global index as a complete character swap: the original game also manages object, model, animation and other state.

## MIPS trace: caller and callee

Project64 Commands showed the following instructions in the running Japanese game. Register names follow the debugger disassembly; surrounding instructions not shown here are not reconstructed.

```mips
# Caller excerpt; function entry and ROM file/overlay ownership unknown
801E2944  SW    T9, 0x0004(V0)       # at V0=80161DC8, writes global 80161DCC
801E2948  SW    T1, 0x002C(V0)       # at V0=80161DC8, writes 80161DF4
801E294C  LBU   A1, 0x0060(S0)       # in capture S0=8016F780 -> read 8016F7E0
801E2950  JAL   0x801E2970
801E2954  OR    A0, S0, R0           # JAL delay slot: argument object pointer

# Called function begins at 801E2970 in observed execution
801E2970  ADDIU SP, SP, -0x18
801E2974  OR    A2, A1, R0
801E2978  SW    RA, 0x0014(SP)
801E297C  SW    A1, 0x001C(SP)
801E2980  SB    A2, 0x0060(A0)       # object + 0x60
801E2984  ANDI  T6, A2, 0x00FF
801E2988  LUI   AT, 0x8016
801E298C  SW    T6, 0x1DCC(AT)      # global 80161DCC
801E2990  LW    T7, 0x005C(A0)      # next instruction after confirmed store
```

### Runtime breakpoint and single-step evidence

1. Set a **PC execution breakpoint** at `0x801E2944` in Project64 Commands. The debugger displayed `E 801E2944`, and the user reported it **paused again upon a normal character switch** (not merely manual navigation to the instruction).
2. Captures at the writer showed `V0=0x80161DC8` and `T9=0` on one occasion and `T9=1` on another. The target is `0x80161DCC`. A step from `PC=801E2944` to `PC=801E2948` was accompanied by guest memory displaying `00000001` at `0x80161DCC` during the `T9=1` capture.
3. The caller advanced through `0x801E2948`, `0x801E294C`, and the `JAL` at `0x801E2950`. At the callee entry, the captured registers were `A0=0x8016F780`, `A1=1`, and `RA=0x801E2958`. This independently establishes the **direct call at runtime** and the correct return address.
4. Single stepping through the callee reached `PC=0x801E298C` with `A0=0x8016F780`, `A1=1`, `T6=1`, and `AT=0x80160000`. The debugger then advanced from **`0x801E298C` to `0x801E2990`**, confirming that the second global store executed. The global already held `1`, so this is proof of the executed store, **not evidence of a second value transition**.
5. A separately attempted PC breakpoint at `0x801E298C` did not initially interrupt on switching, whereas stepping into the caller's `JAL` reached and executed it. Therefore a missed standalone breakpoint must not be interpreted as proof the path is unused.

### Constrained interpretation

**Supported:** a native switch reaches `0x801E2944`; the caller writes the global character index, reads an object-relative byte at `+0x60`, and calls `0x801E2970`. The callee writes a byte to `A0+0x60` and a masked value to the same global index. Both original Japanese MIPS stores were actually stepped/executed.

**Inferred:** `0x801E2970` behaves like a character-related state synchronisation/update helper. The semantic label is provisional pending callers and object-structure analysis.

**Not established:** the caller's complete function start/end, overlay identity and ROM offset, meaning of `object+0x5C` or global `0x80161DF4`, lifetime/type of the `0x8016F780` object, Sasuke/Yae behaviour through this function, actor/XYZ pointer equivalence, or a C implementation matching either region.

## Follow-up: pointer dereference and secondary byte write (2026-11-15)

Further user-supplied Project64 Commands and Memory screenshots single-stepped the **same captured invocation** beyond `0x801E2990`. These screenshots were displayed in the conversation but are not included as repository binary assets.

| PC / step | Register or guest-memory observation | Conclusion |
| --- | --- | --- |
| Before `0x801E2990` | `A0=0x8016F780`; guest word at `0x8016F7DC` is `80211650` | `A0+0x5C` contains a guest pointer in this instance |
| After `LW T7,0x5C(A0)`, PC `0x801E2994` | `T7=0x80211650` | **Runtime-confirmed pointer dereference** |
| Before `SB V0,0x69(T7)`, PC `0x801E299C` | `T7=0x80211650`, `V0=1`; debugger at `0x802116B9` displays four bytes `00 01 00 BF` | Store about to target byte `0x802116B9` |
| After stepping once, PC `0x801E29A0` | Same memory row starts `01 01 00 BF` | **Runtime-confirmed byte transition `00 → 01` at `0x802116B9`** |

```mips
801E2990  LW    T7, 0x005C(A0)     # *(u32 *)(8016F780+5C) = 80211650
801E2994  ADDIU V0, R0, 0x0001
801E2998  MTC1  R0, F0
801E299C  SB    V0, 0x0069(T7)     # 80211650+69 = 802116B9, observed 00->01
801E29A0  LW    T8, 0x005C(A0)     # next instruction, not yet traced here
```

**Interpretation constraint:** The callee follows a pointer held in the character-related object and sets a byte in the pointed-to allocation during a native character switch. The byte's semantic meaning (reset/request/activation/animation/etc.) is **unknown**. `0x80211650` is an observed allocation, **not a validated fixed player/task pointer**. Earlier Mupen float-address hypotheses falling near it were obtained in a different emulator session and are not proof that this pointer owns player XYZ. No universal cross-session pointer stability is established.

**Next validation:** Sample the pointer from `0x8016F7DC` in independent scenes and for all four characters, and test whether the value at `pointer+0x69` changes under ordinary non-switch conditions; separately verify positional fields dynamically before naming this allocation an actor or player.

## Next static/dynamic investigation

- Determine the loaded section/overlay for Japanese address range `0x801E2944..0x801E2990` **at this point in gameplay**; overlay VRAM ranges may be reused. Then map to its original Japanese ROM offset and actual function boundaries using the region-specific Splat map and the decompressed ROM, rather than a blanket USA offset.
- Disassemble backward from `0x801E2944` to the caller prologue and inspect other callers of `0x801E2970`; separately analyse downstream reads/writes of `0x80161DF4`, `object+0x5C`, and `object+0x60`.
- Re-run an isolated normal switch with fresh register/guest snapshots for both directions, and compare object-pointer identity over an unrelated scene transition. Preserve debugger captures/exports if available. Do not freeze or force-write pointers to infer ownership.
- For toolkit integration, treat `0x80161DCC` as confirmed Japanese current-character state (0/1), but **do not** promote `0x8016F780` to a fixed player pointer, expose arbitrary writes, or assume Project64's host RDRAM base is `0x20000000`. The Windows Cheat Engine host mapping was not confirmed in this session.

No game-memory writes, patching, decomp matching promotion, new toolkit permissions, or CI assertions are introduced by this document.
