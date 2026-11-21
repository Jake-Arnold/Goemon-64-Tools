# GQ-VM-001 — Project64 Japanese first-bomb live trace handoff

**Task status:** BLOCKED_EXTERNAL / awaiting user's actual Windows Project64 manual gameplay input (21 Nov 2026).  
**Task system:** `decomp/tasks/registry.json`; primary [task registry skill](../../../.agents/skills/goemon-task-registry/SKILL.md).  
**Evidence:** [Bomb Text Skip #139](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/139), [research #151](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/151).

## Research scope and kit provenance

Original Japanese game ROM rev 0; original script after first Gourmet Sub bomb dialogue assigns checkpoint index **13**. A controlled original-MIPS microtrace (synthetic trigger/renderer/task setup) demonstrated a conditional Start→pause-mask→fade-complete→VM-reset path bypassing checkpoint writer. **This is not a real game trace.**

Prepared **source-only** kit for Windows Project64 3.x, delivered as a conversation attachment:

- `Goemon_Bomb_Text_Skip_Project64_Trace_Kit_2026-11-21.zip`
- **SHA-256:** `0de4a714b96cbf6158596e236ac72b4033e50653f95180a58ffc6a87e7f3e933`
- Contains `Goemon_Bomb_JP_normal.js`, `Goemon_Bomb_JP_start.js`, `compare_bomb_traces.py`, `test_pj64_mock.js`, `test_comparator.py`, `README.md` and `MANUAL_CHECKLIST.md`.
- No original ROM, original ASM dumps, proprietary compilers, savestates or real captured RAM data. Recorder scripts are **not** checked into Git because they contain original resource-script opcode/operand signatures; they remain available as the user's kit attachment.

## Manual session, in order

1. Install/run the original **Japan revision-0** ROM (header CRC1 `832C168B`, CRC2 `56A2CDAE`); configure Project64 3.x advanced debugger and **Always use interpreter core**. This kit **must not** be used for USA or native recompilation.
2. Obtain an **authentic** pre-first-bomb-dialogue Gourmet Sub savestate. Its current checkpoint must **not** be 13. Keep the savestate private.
3. Run the **normal** JS recorder from the Project64 Scripts folder **after** restoring the savestate; do not press Start, advance the real bomb conversation, and stop via `GOEMON_BOMB_STOP()`. Preserve `Goemon_Bomb_JP_normal.jsonl`.
4. Restore the **same** savestate, then run the **Start** recorder. Press Start manually for one update in the pre-dialogue window, allow fade/transition to settle and stop via `GOEMON_BOMB_STOP()`. Preserve `Goemon_Bomb_JP_start.jsonl`.
5. Execute the kit comparator: `python compare_bomb_traces.py --normal Goemon_Bomb_JP_normal.jsonl --start Goemon_Bomb_JP_start.jsonl --report bomb_pair_comparison.json --markdown bomb_pair_comparison.md`.
6. Independently observe and record whether the skip actually occurs and whether a save/reload yields the previous checkpoint; a static trace cannot verify saved warp persistence.
7. Keep raw JSONL, savestate and personal paths **local**. Checkpoint **sanitized** result + hashes, valid/invalid PC ordering, VM task flags and exact blockers in registry, #139 and PROGRESS.

## Original Japanese watchpoints

| Event | PC / live field |
|---|---|
| Gameplay update then scheduler | `0x8000327C` / `0x800343A4` |
| Start accepted | `0x8001F6DC` |
| VM text command advances pending cursor | `0x8003D54C` |
| Scheduler reads task flags `+0x22` | `0x8003440C` |
| Scheduler pause-mask decision | `0x8003441C` |
| VM callback entry | `0x8003CC40` |
| Pause mask set | `0x8001F7BC` |
| Fade query / reset call | `0x8001F7D4` / `0x8001F800` |
| VM cursor clear / script store | `0x8003D1C8` / `0x8003D7E0` |
| VM cursor / saved checkpoint / system pause flags | `0x8007D288` / `0x80161FF8` / `0x800CD2D4` |

Project64 hooks are **read only**, log original instruction hits and pending memory writes, and automatically decode original scheduler task-register addressing to identify the real VM task's flag word. Script includes an original command-signature check to distinguish the first-bomb checkpoint13 assignment from unrelated dialogues.

## Evidence and safety boundary

The comparator rejects incomplete captures, synthetic fixtures and mismatched ROMs by default. It only reports `SUPPORTS_START_PAUSE_VM_RESET_MECHANISM` when two authentic captures show the same precheckpoint, normal checkpoint13 write, Start accepted before the first-bomb script, actual task masking during the fade, fade queries and cursor reset preceding any checkpoint13 write. No executed successful run has yet been observed.

**Tests performed while preparing the kit:** `node test_pj64_mock.js` PASS (both recorder modes and wrong-ROM guard); `python -m unittest -q test_comparator.py` PASS (9 cases); `python -m py_compile compare_bomb_traces.py` PASS; ZIP integrity PASS. These are mock tests only. **No Project64/real input run, no ROM mutation, no native-C promotion and no production changes.**
