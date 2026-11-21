# USA main game-state dispatcher — verified 18-way handler map

Original USA VMA `0x80002040` / expanded ROM `0x2C40`; 18-entry dispatch table starts at VMA `0x80058908` (expanded ROM `0x59508`). All addresses below read directly from the authenticated original USA ROM; function names and ASM/C ownership are verified against the original 1,966-C linked ELF.

| State byte | Function | RAM address | Status |
|---:|---|---|---|
| 0 | `func_800020B8_2CB8` | `0x800020B8` | ASM |
| 1 | `func_80002138_2D38` | `0x80002138` | ASM |
| 2 | `func_8000236C_2F6C` | `0x8000236C` | ASM |
| 3 | `func_80002454_3054` | `0x80002454` | ASM |
| 4 | `func_80002518_3118` | `0x80002518` | ASM |
| 5 | `func_80002718_3318` | `0x80002718` | ASM |
| 6 | `func_80002938_3538` | `0x80002938` | ASM |
| 7 | `func_80002A98_3698` | `0x80002A98` | C |
| 8 | `func_80002AB8_36B8` | `0x80002AB8` | ASM |
| 9 | `func_80002C7C_387C` | `0x80002C7C` | ASM |
| 10 | `func_80002D94_3994` | `0x80002D94` | ASM |
| 11 | `func_80002DE4_39E4` | `0x80002DE4` | ASM |
| 12 | `func_80002E70_3A70` | `0x80002E70` | ASM |
| 13 | `func_80002EFC_3AFC` | `0x80002EFC` | ASM |
| 14 | `func_80002F54_3B54` | `0x80002F54` | ASM |
| 15 | `func_800030F0_3CF0` | `0x800030F0` | ASM |
| 16 | `func_80003328_3F28` | `0x80003328` | C |
| 17 | `func_80003358_3F58` | `0x80003358` | C |

The state byte is read from `D_8015C5C8_15D1C8` plus original absolute field offset `0x3ADD4`. The engine does not bounds-check it inside `func_80002040_2C40`. Table membership alone does not establish each handler's gameplay mode; those semantics require separate call-graph and runtime evidence.

Native matching source, acceptance adapter, tests, immutable original-address hashes and proof metadata live in `decomp/research/usa_dispatcher_2c40_20261121/` and `decomp/results/usa_dispatcher_1966_g2_20261121.json`.
