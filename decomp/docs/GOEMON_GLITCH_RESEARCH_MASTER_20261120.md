# Goemon N64 — Glitch investigation master record

**Last reviewed:** 20 November 2026  
**Scope:** *Ganbare Goemon: Neo Momoyama Bakufu no Odori* (Japan revision 0) and *Mystical Ninja Starring Goemon* (USA).  
**Repository:** `Jake-Arnold/Goemon-64-Tools`, `chatgptweb/decomp` only.  
**Issue tracking:** [#139 — Gourmet Sub savewarp](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/139), [#95 — Map Glitch initializer](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/95).  
**Latest investigation result:** `STATIC_ROM_VERIFIED / RESEARCH_ONLY`; no in-game execution, no newly matching C, no modified ROM, no changed game save.

## Evidence standard

- **ROM-verified:** exact script operands or original MIPS instruction/call graph checked against an authenticated, original decompressed ROM. Proves the *available code path*, not that every path is reached in the player's playthrough.
- **Existing implementation:** matching-C proven by the decomp project in its published or local-G2 acceptance inventory. Explicitly separate USA and Japanese sources.
- **Empirically documented:** behaviour described by original speedrunners/videos, not replicated in this investigation.
- **Hypothesis:** a proposed cause or new glitch; requires a runtime or replay test.
- **Negative result:** a specific examined path does *not* contain the expected operation. A bounded search is not an exhaustive native xref audit.

### ROM authenticity and input handling

| Image | Expanded size | SHA-1 — independently verified during this follow-up |
|---|---:|---|
| Japan revision 0 | 33,554,432 | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` |
| USA | 33,554,432 | `6ea0ed71032ce08fc2745f412d84936382197494` |

Only hashes, instruction *locations* and observed semantics are reported. ROM bytes, full assembly, extracted strings, game assets and original toolchain are not included. Reproducing the checks requires the user's privately owned original ROMs and the pinned upstream `mnsg` checkout/toolchain in `GOEMON_BUILD_ENVIRONMENT.md`.

## Confirmed core result: the first Gourmet Sub bomb script contains a three-write checkpoint block

The **correct order** is Poron's conversation near the *end of Gourmet Sub*, then the Thaisamba sequence. Poron does **not** speak before the player enters the dungeon. The reported flag `0x32` assignment is script data in resource 95 before the first bomb's checkpoint write; an additional flag-`0x32` assignment exists in resource 102. Neither fact by itself proves a particular Benkei requirement.

Script resource 95, Japanese original:

| Resource-relative command | Guest target | Immediate / action | Evidence |
|---|---|---|---|
| `+0x2624` | `0x8007D28C` | Set `4` (VM-associated field, **not** saved checkpoint) | Original script |
| `+0x2634`, `+0x263C` | Text pointers | Two `0x8010` text commands | Original script |
| **`+0x2644`** | **`0x80161FF8`** | **Checkpoint index = 13** | Original script |
| **`+0x2654`** | **`0x80162018`** | **Saved field `+0x220` = 1** (meaning unknown) | Original script |
| **`+0x2664`** | **`0x801620D0`** | **Gourmet Sub visited-location word = 0** | Original script |
| `+0x2674` | `0x8003F200` | Native callback, opcode `0x800B` | Original script and MIPS |

The USA counterpart is resource 95 at `+0x34EC`, `+0x34FC/+0x3504`, **`+0x350C`**, **`+0x351C`**, **`+0x352C`**, `+0x353C`, targeting checkpoint `0x8015C808`, other saved field `0x8015C828`, and visited word `0x8015C8E0`.

The Japanese checkpoint command begins at expanded ROM **`0x74E9F4`**. Original Japanese `func_8003D77C_3E37C` performs the indirect immediate-value word store at guest PC **`0x8003D7E0`**, reached through VM dispatcher `func_8003D2FC_3DEFC`.

The **post-write callback** `func_8003F200_3FE00` is a 52-byte leaf. It reads the active actor's character byte `+0x60`, stores it in VM field `0x801CCE80`, or records `-1` when no actor is present. It is **not** another checkpoint writer. This is a new bounded negative finding from the original MIPS.

### What this predicts, and does not prove

A successful Start skip *could* prevent the VM from reaching `+0x2644`, leaving the previous checkpoint and, if it aborts before the complete block, leaving the other two saved words unchanged by that block. **This exact interrupt path has not been observed running.** A late interruption might preserve only part of the block. The three memory write watchpoints are needed.

## New VM control-flow findings — the strongest explanation so far

The script interpreter provides a specific way for a text command to leave a pending write:

1. For script opcode **`0x8010`**, Japanese VM dispatcher `func_8003D2FC_3DEFC` calls text walker `func_8003D85C_3E45C` at guest PC `0x8003D528`.
2. The dispatcher advances the global command cursor `0x8007D288` past the text operand (store at `0x8003D54C`), so the checkpoint assignment may be the *next* opcode in memory.
3. While VM state `0x801CCF10` is **3** (continuation input) or **4** (close input), subsequent dispatcher invocations call `func_8003E05C_3EC5C` / `func_8003E130_3ED30` and return without automatically executing the next script opcode.
4. The VM also has a reset path: `func_8003D098_3DC98` calls `func_8003D0D8_3DCD8` with script ID `-1`. On that path, guest PC **`0x8003D1C8` stores zero to the global command cursor**.
5. A dialogue close helper `func_8003E2F0_3EEF0` directly invokes the reset wrapper. This helper is reachable on a **conditional B-input** branch from the two text-input handlers, when their other guard/continuation fields allow that path.
6. Start is tested in a separate main engine function, `func_800020D8_2CD8`, at guest PC **`0x8000218C`**, with mask `0x1000`. The inspected text-input handlers directly test A/B masks `0x8000` / `0x4000`; they do **not** directly test Start. The original code **has not yet established a Start→script-reset call edge**.

**Importance:** the pending-write mechanism and explicit reset mechanism are both original-ROM facts. Their connection during *Bomb Text Skip* remains the critical runtime hypothesis. This supports focused breakpoints instead of decompiling thousands of unrelated functions.

### Script task gate, not automatically a frame timer

- JP `func_8003CC8C_3D88C` installs `func_8003CC40_3D840` as a task callback and sets byte `0x801CD060` to **5**.
- `func_8003CC40_3D840` decrements this gate while nonzero and only calls the VM dispatcher when the gate is zero.
- `func_8003E2F0_3EEF0` sets the gate to **3** after its close/reset work.

These are counts of eligible callback invocations. **They cannot be called 5 or 3 video frames without measuring actual callback frequency.** The gate provides a concrete watchpoint for frame-perfect interruption tests.

## Checkpoint mapping — independently checked in both regions

- Live checkpoint index: JP **`0x80161FF8`**, USA **`0x8015C808`**, offset `+0x200` within the live 0x304-byte saved-data record.
- There are **17** aligned direct-script immediate assignments, with unique assigned values **1 through 17**, across 12 resource files, in *each* region. This is exhaustive for the scanned `0x8004, address, 0x8009, value` pattern, **not** for all possible native/indirect writers.
- Index 0 is not assigned by that pattern and has an all-zero spawn record; this is consistent with, but does not establish, the video's reported SIRO 0 default.
- Original 18×12-byte checkpoint records are byte-identical across JP/USA. Record 13 starts with room **`0x023A` (570)**; record 17 starts with **`0x023B` (571)**.
- Pairs **(2,3), (8,9), (10,11)** have identical full spawn records, so different indices can restore the same destination.
- JP `func_8000B588_C188` reads `+0x200`, indexes the spawn-record array, copies its fields, enforces minimum **3 lives and 10 health units**, and copies 0x304 bytes to shadow save data. Its caller `func_80219AE8_5D5078` is part of the save preparation/serialization path; end-to-end Controller Pak persistence has not been traced in a successful glitch attempt.

### New direct dialogue adjacency census

Both regions contain exactly **two** direct checkpoint assignments immediately following an `0x8010` text command and text operand:

| Checkpoint | Japanese resource/offset | English cue | Assessment |
|---|---|---|---|
| **13** | resource 95 `+0x2644` | Time-bomb dialogue; final Sasuke lines | Primary plausible Bomb Text Skip mechanism |
| **2** | resource 96 `+0x7AFC` | **Oedo Castle Entrance** title, followed by Adventure Diary save prompt | Distinct untested candidate; save-prompt control flow may make it unsuitable |

The other 15 checkpoint assignments are **not in that exact adjacent arrangement**. In particular, second-bomb index **17** follows another saved/non-save assignment, rather than immediately following the nearest text command. This does not rule it out as a text-skip candidate; it merely changes the earliest possible interruption boundary.

### Second bomb event

JP resource 95 `+0x3088` sets a temporary field, then `+0x3098` writes checkpoint **17** and `+0x30A8` writes saved field `+0x224` (`0x8016201C`) to **1**. The USA counterparts are `+0x3FA0`, `+0x3FB0`, and `+0x3FC0`. A bounded whole-resource scan found only one aligned direct immediate assignment to the saved fields `+0x220` and `+0x224` each, both in the corresponding bomb sequences. Their actual purpose remains unknown.

## Gourmet Sub visited-location marker

- JP resource 93 `+0x3820` writes **1** to `0x801620D0`, associated with the area-name sequence. JP resource 95 `+0x2664` writes **0** to the same address.
- USA resource 93 `+0x4334` and resource 95 `+0x352C` perform the same assignments to `0x8015C8E0`.
- In the expanded Japanese and USA ROMs, the *literal full 32-bit address* of this visited word appears **exactly twice**, at these script sites. **This does not exclude pointer arithmetic, bank-relative accesses, masked readers, or copies in native code.**
- An external, third-party save editor separately labels the corresponding low byte of the save-slot word as Gourmet Submarine Castle in its visited-location list; this is corroboration, not proof of travel-menu semantics.
- A broader 16-word visited-location scan finds **15** direct immediate script assignments across **14** words in both ROMs. Twelve set-to-one occurrences are in area-name resource 93. Two slots have no direct assignment in the scanned form.

**Potential consequence, not established:** skipping the first bomb block might retain the prior checkpoint **and** visited-marker value 1. Whether that changes any route, transport menu or event gate depends on currently untraced consumers of the marker.

## Other glitch families and already-verified leads

| Family | Concrete original-code lead | State | Next decisive question |
|---|---|---|---|
| **Map Glitch (J-only)** | JP `func_80212514_5CDAA4` reads held C-Right at `0x8021259C`, branches at `0x802125A0`, deferring stage-task creation/loader callback; 69/99 instruction native-C candidate, currently `FAILED_NATIVE` | Original MIPS + previous PJ64 observations | What is the earliest task/object/collision consumer after button release? |
| **Map Glitch task scheduling** | JP `func_800343A4_34FA4`, stage loader `func_802126A0_5CDC30`; associated C-exact task wrappers already exist | Mixed accepted-C/ASM; partial call graph | Determine real per-frame task order, partial initialization and reset conditions |
| **Mokkori/Chain Pipe Skip** | Existing region-specific collision-query candidates and character-state reset code | Empirical mechanics, selected MIPS leads | Locate actual player displacement/velocity and attack/jump state stores, then compare matched inputs JP/USA |
| **Character swap during transition** | JP `func_801E2970_59E940` and `func_801E2A04_59E9D4` exact C; reset actor fields and animation state | Original code reconstructed, runtime glitch not replicated | Compare interrupted transition frame before/after character-change call |
| **Conversation skips** | JP `func_8003D2FC_3DEFC`, `func_8003D85C_3E45C`, `func_8003E05C_3EC5C`, `func_8003E130_3ED30`; pending command pointer and abort semantics | New original MIPS control-flow proof | Where does Start affect VM callback/cursor for normal versus skipped dialogue? |

Consult the attached earlier reports for historical background and deeper checklists:
`Goemon_Bomb_Text_Skip_Save_Location_Research_2026-11-20.md`, `Goemon_Glitch_Breakthroughs_2026-11-20.md`, `goemon_checkpoint_writer_inventory_2026-11-20.csv`, and the original user-supplied `Pasted markdown.md` historical glitch survey. Do not treat a historical TAS description as native-code proof.

## Next tests — deterministic, read-only, falsifiable

### A. Primary bomb interruption trace

Prepare the **same initial save** for both runs; avoid comparing attempts from different health, character, previous-checkpoint, or progress states. Prefer a debugger capable of guest instruction breakpoints and exact guest store tracing (Project64/mupen-compatible debugger). Record an exact frame marker only if provided by the runtime.

| Guest location | Access | Why |
|---|---|---|
| JP `0x80161FF8` | write (u32) | Checkpoint index 13 writer |
| JP `0x80162018` | write (u32) | First bomb saved `+0x220` assignment |
| JP `0x801620D0` | write (u32) | Gourmet Sub visited marker clear |
| JP `0x8007D288` | write/read (u32) | VM command cursor; determine whether next command remains pending or becomes null |
| JP `0x801CCF10` | write/read (u32) | VM text/continuation state |
| JP `0x801CD060` | read/write (u8) | VM task callback gate |
| JP `0x801CD03C` | read (u16) | VM A/B input |
| JP `g_system_ptr+0x3B07A` | read (u16) | Main-engine Start input when corresponding state path is active |
| JP guest PCs `0x8003D7E0`, `0x8003D1C8`, `0x8003D54C`, `0x8000218C` | instruction breakpoints | Immediate save writer, explicit cursor reset, cursor advance, Start check |

Expected if the proposed mechanism is correct: normal dialogue eventually executes the store of 13 and the next two stores. A successful Start-skip attempt prevents at least the index-13 store; its cursor trace should show the precise divergent branch/callback. A later save then serializes the still-old checkpoint. **If the skip executes the index-13 store, the central explanation is falsified and the save-buffer copy/restore path needs investigation.**

### B. Structural analogue: Oedo Castle Entrance checkpoint 2

USA resource 96 `+0xAC74` contains Oedo Castle Entrance title; `+0xAC84` assigns 2; the following text is an Adventure Diary save prompt. Test only after proving the primary bomb mechanism; the save prompt may make this an entirely different class of interaction.

### C. Widen native xrefs only as needed

Trace the first observed instruction writing any of the three saved fields, and all readers of the visited word on the tested route. Generic memory copies and pointer-relative writers defeat simple literal searches. Record discovered JP/USA addresses separately; **never apply the `+0x57F0` RAM-offset heuristic to function VMAs or overlaid code**.

## Exact verification steps

```
python3 verify_goemon_glitch_checkpoint_matrix.py /path/to/japan.expanded.z64 /path/to/usa.expanded.z64
python3 verify_goemon_text_skip_vm_control.py /path/to/japan.expanded.z64 /path/to/usa.expanded.z64
```

Both scripts passed on the original authenticated 32 MiB ROMs on 20 November 2026. `verify_goemon_text_skip_vm_control.py` checks both ROM checksums, exact script assignments, adjacency classification, two literal visited-word references, and original Japanese MIPS gate/dispatcher/handler/reset/callback anchors. It does **not** contain a working emulator, prove branch reachability, or cause an in-game Start skip.

## Decompilation priority by new information value

1. **Read trace / reconstruct caller edges for `func_8003D2FC_3DEFC`**, not merely match the trivial generic assignment writer.
2. **`func_8003D85C_3E45C` plus `func_8003E05C_3EC5C` / `func_8003E130_3ED30`**: exact text state, input, and resume/abort conditions.
3. **`func_800020D8_2CD8` and intermediate state handlers**: establish or refute Start→VM termination. Do not claim such an edge until runtime or control-flow evidence.
4. **Save-prep `func_80219AE8_5D5078`** only if successful skip still changes the live checkpoint but not persisted checkpoint.
5. **Stage-init `func_80212514_5CDAA4`** and task scheduler/loader for the separate Japanese Map Glitch investigation.
6. **Movement updater** identified from runtime velocity/position writer; avoid promoting arbitrary collision leaf functions without relating them to Mokkori.

## Audit outcome

**Passed:** original JP/USA expanded ROM authentication; prior checkpoint/visited script verifier; new dialogue-adjacency census; new MIPS control-flow anchors; exact first/second bomb sequences and Oedo save prompt; literal visited-word pointer count; callback side effects within its 52-byte function.

**Not run:** emulated gameplay, savestate replay, actual single-frame Start interruption, Controller Pak save/reload, full-program native-writer/reader closure, matching-C promotion or new full-ROM build. GitHub Issue #139 tracks the remaining runtime causal link.


## 20 November 2026 — Additional verified dialogue-grant and event-flag research

See [the 45-write cross-region inventory](GOEMON_DIALOGUE_GRANTS_AND_FLAG_COUPLING_20261120.md) (source: `decomp/docs/GOEMON_DIALOGUE_GRANTS_AND_FLAG_COUPLING_20261120.md`). Original ROM authentication and read-only verifier found **45** text-adjacent live-save assignments affecting **42** fields in each region, **21** externally named item/ability fields at **23** sites, and identical event-field coupling for **nine** distinct grants across **10** sites. The original ROM code confirms the exact command structures; this does not demonstrate new glitches. Original English dialogue independently supports multiple named grants. Chain Pipe is a priority target because its story bit `0x10` is written before a later separate inventory grant, unlike the adjacent Miracle Snow pair. Items, flag storage and region-to-region addresses are recorded in `decomp/address_discoveries_v1.json`, and every new flag has an explicit counterpart. Tests: original JP/USA hash and read-only survey verifier PASS; no game execution, ROM rebuild, matching-C promotion or toolkit write.


## 20 November 2026 — Actual gameplay Start gate and VM reset chain, both regions

[Full original-MIPS research](GOEMON_START_DIALOGUE_SKIP_CONTROL_FLOW_20261120.md): the previous `JP 0x8000218C` Start input check belonged to a Controller Pak/menu path, not the gameplay dialogue trigger. Authenticated original Japanese/USA main code now establishes gameplay Start mask `0x1000` in `JP func_8001F610_20210` / `USA func_8001F940_20540`; both invoke 36-byte script-active queries, **reject Start when VM command cursor is nonzero**, and otherwise can latch a pause phase. Its phase-1 handler conditionally calls the VM reset with script ID `-1` and clears the cursor at `JP 0x8003D1C8` / `USA 0x8003D558`. Static verification **PASS 36/36** exact original instructions plus JAL/branch targets. This establishes a conditional Start→VM-reset code path but **does not** yet prove a successful Bomb Text Skip follows that path at runtime. Breakpoints and control conditions are in the linked report and Issue #139.


## 20 November 2026 — Original-address native-exact C for gameplay Start/VM busy

[Read the full native-C evidence and detailed test results](GOEMON_START_VM_NATIVE_MATCH_20261120.md). **Two new JP isolated exact C functions (252-byte Start updater and 36-byte VM-busy check), one new USA 252-byte Start updater**, plus an already accepted USA 36-byte VM-busy equivalent. All 4 regional targets were reproduced with pinned IDO 5.3 at original VMAs, **144/144 instructions identical**, with 15 GCC ASan/UBSan host gate tests PASS. All four other JP reset wrapper/task callbacks reproduced were already in the JP2118 local G2 batch and are not counted again. Novel regional research bytes: JP 288, USA 252; **zero function promotions** (canonical 32 MiB ROM, relocations and full CI for new C not run). Static caller trace identifies three-entry gameplay callback table at JP `0x80071210`; actual Bomb Text Skip scheduling remains unproven.


## 21 November 2026 — Three new native-exact JP/USA gameplay callback implementations

[Full callback research and verification](GOEMON_GLITCH_CALLBACK_NATIVE_MATCH_20261121.md). New original-address C: Japan `func_8001F580_20180` (100 bytes, 25/25), Japan `func_8001F70C_2030C` (68 bytes, 17/17), USA `func_8001F8B0_204B0` (100 bytes, 25/25). Exact original IDO 5.3 linked extents verified against the original authenticated ROMs; total research verification with four prior sources **7/7 functions, 211/211 MIPS instructions**, and GCC ASan/UBSan callback host tests pass. The original 14-phase pause handler and script reset manager remain `FAILED_NATIVE`, with reproducible mismatch/size results. **Zero full-ROM promotions, zero gameplay skip tests.** The source-only research ZIP includes the full native checker, failed-draft reproduction and original SHA ledgers; no ROM/ASM/ELF/compiler was committed.


### 21 November 2026 — Four consecutive Japanese gameplay functions reproduced together

The newly reconstructed dispatcher and teardown now compile in **one C unit alongside the existing Japanese init and Start handlers**: original ROM range `0x20180..0x2034F`, **464/464 bytes and 116/116 instructions exactly**. See [same-translation-unit proof and original SHA hashes](GOEMON_GLITCH_CALLBACK_NATIVE_MATCH_20261121.md). This is original-address source **code** equality only: **canonical complete 32 MiB ROM and relocation acceptance unperformed**. The Bomb Text Skip pause/reset scheduling hypothesis remains **not gameplay verified**.


## 21 November 2026 — Native G2 promotion: JP 2121 and USA 1958

Five original-address C functions passed strict native full-ROM, ELF identities, complete original main+overlay relocations, C/ASM identity and local CI. Full technical evidence: [GOEMON_START5_G2_PROMOTION_20261121.md](GOEMON_START5_G2_PROMOTION_20261121.md). Japan teardown remains ASM due original-relocation mismatch. Actual Bomb Text Skip in-game is still NOT RUN.
