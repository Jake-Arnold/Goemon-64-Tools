# VM text-loop control-flow trace

**G64-031 — research only; no C promotion.** This is an address-ordered graph
for the retained-assembly function `func_8003DBEC_3E7EC`. It records the
original transfer instructions and delay-slot effects before another source
shape is tried.

## Original boundary and evidence

| Property | Value |
| --- | --- |
| Guest VMA | `0x8003DBEC` |
| ROM offset | `0x3E7EC` |
| End-exclusive VMA | `0x8003DDC4` |
| Original extent | `0x1D8` = 472 bytes = 118 MIPS words |
| Original extent SHA-256 | `4ee117dd31f6b8f3ab30ca864c202eb7c974c28cc8236d233a94228b36a0a764` |
| Decompressed USA ROM SHA-1 | `6ea0ed71032ce08fc2745f412d84936382197494` |
| Current ownership | `GLOBAL_ASM` in `script_vm.c` |
| Current C probe | 472-byte research symbol; 53/88 comparable non-relocation words, 17 relocation-layout differences, and a 0x50 frame versus the original 0x48 |

The local guard `test_vm_text_loop_addressing.py` now checks the exact 118-row
extent against the private ROM, its extent hash, global/controller addresses,
and all six branch-likely instructions with their delay slots. The original
ROM/listing and all compiler artifacts remain local.

## Address and data liveness

| Register or address | Original use | Evidence and limit |
| --- | --- | --- |
| `$s1` | Holds the address of global storage `D_801C77E8_1C83E8` (`0x801C77E8`). `lw 0($s1)` loads the current 32-bit script cursor/address value passed as `$a1`; after `DE80`, `sw $v0,0($s1)` stores the returned cursor value. | Direct `lui/addiu`, load and store at `0x8003DC38..0x8003DC6C`. `$s1` is the global's address; DBEC does not dereference the script cursor's pointee. |
| `0xA($s1)` | Separate halfword at global address `0x801C77F2`; cleared on terminal state or button paths, read as a gate, and set to one for a pressed-button retry. | Direct `sh/lhu` at `0x8003DC98`, `0x8003DCD4`, `0x8003DD58`. It is not memory at cursor-value-plus-`0xA`. “Retry latch” is a behavior label, not a recovered field name. |
| `$s2` | Address of VM state global `D_801C77E0_1C83E0`. State is reloaded after each `DE80` call; the function writes state 1 during ordinary processing and zero after the restart handler. | Direct global-base construction at `0x8003DC34/40`, state load at `0x8003DC68`, and stores at `0x8003DCA4`, `0x8003DCB8`, `0x8003DCFC`. |
| `$s3` | Address of controller global `D_801C7908_1C8508`. The routine reads unsigned halfwords at `+2` and `+4`, not a signed word. | `CONTROLLER_W` declares `button_held_down` at `+2` and `button_pressed` at `+4`; original `lhu` instructions are at `0x8003DCC8`, `0x8003DD1C`, and `0x8003DD48`. |
| `$s4` | Address of context argument global `D_801C7754_1C8354`. The value is loaded into `$a0` in the `DE80` call's delay slot each time the call executes. | Direct load at `0x8003DC64`; callback changes to the global can be observed on a later call. Its engine meaning is not inferred here. |
| `$s0` | Inner retry/press counter; initialized to zero at `0x8003DC20` and incremented in the delay slots at `0x8003DD34` and `0x8003DD60`. It is compared with three. | Direct instruction/liveness trace. It is distinct from the outer iteration counter at `sp+0x44`. |
| `sp+0x44` | Outer iteration counter; initialized to zero in `blez` delay slot `0x8003DC28`, read at branch-likely slots `0x8003DCC4`/`0x8003DD54`, incremented at `0x8003DD78`. | Direct stack accesses. The current maximum at `D_801C77D8_1C83D8` is loaded on each outer check at `0x8003DD74`; it is not kept only in the initial `$t6`. |
| `$s5/$s6/$s7/$fp` | Constants 3, 4, 5 and 6 used by the terminal-state comparisons. | Immediate loads at `0x8003DC50..0x8003DC58`; each value is tested against the freshly loaded state. |
| `D_801C7770_1C8370` | Input gate. A nonzero value takes the likely branch directly to the outer-count path, skipping controller handling. | Direct load/test at `0x8003DC70..0x8003DCC0`. The semantic label “input gate” follows control flow. |
| `D_801C7774_1C8374` | Optional argument to `DE48`; when zero, `E680` is called and the routine exits. When nonzero, its `DE48` result is stored to `D_80077858_78458`. | Direct load/call/store sequence at `0x8003DCDC..0x8003DD04`. The deeper handler meaning remains unknown. |

The initial outer bound is read from `D_801C77D8_1C83D8` before the early
`blez`; it is read again at `0x8003DD74` after loop work. Both the state and
the bound therefore have callback-visible reloads. The script cursor and the
global storage address remain separate values throughout the trace.

## Basic-block graph

| Block | Address span | Actions | Successors |
| --- | --- | --- | --- |
| B0 — entry and setup | `0x8003DBEC..0x8003DC5C` | Allocate 0x48 bytes; save `$s0..$s7`, `$fp`, `$ra`; initialize `$s0=0`; read outer bound; initialize `sp+0x44=0` in the `blez` delay slot; construct global bases and terminal-state constants; load cursor word from `0($s1)`. | Bound `<=0`: exit B11. Otherwise B1. |
| B1 — paced step call | `0x8003DC60..0x8003DC6C` | Call `DE80`; its delay slot loads `D_801C7754` into `$a0`; store returned `$v0` to global cursor word; reload state from `D_801C77E0`. | B2. |
| B2 — state dispatch | `0x8003DC70..0x8003DC9C` | Compare state to 3, 4, 5, then 6. States 3–5 branch to latch clear. The likely branch for state 6 is not taken and annuls its cursor-load slot, then falls through to latch clear. For other states, the likely slot loads the cursor word before B3. | State 3–6: B2T then B11. Other states: B3. |
| B2T — terminal state | `0x8003DC94..0x8003DC98` | Branch to exit; delay slot clears the global halfword at `+0xA`. | B11. |
| B3 — cursor/state guard | `0x8003DC9C..0x8003DCB8` | For nonterminal state, set VM state to 1. If cursor value at `D_801C77E8+0` is zero, clear that word and state, then exit. | Null cursor: B11. Nonzero cursor: B4. |
| B4 — input gate | `0x8003DCBC..0x8003DCC4` | Load `D_801C7770`; if nonzero, `bnel` takes the branch and its delay slot reads the outer counter. | Gate nonzero: B10. Gate zero: B5. |
| B5 — pressed 0x4000/restart path | `0x8003DCC8..0x8003DD08` | Read unsigned pressed halfword at controller `+4`, mask `0x4000`. If clear, the `beql` delay slot loads the `+0xA` latch and skips to B6. If set, clear latch; load `D_801C7774`. Zero calls `E680` then exits. Nonzero resets state, calls `DE48` with that value, stores its result to `D_80077858`, then reloads latch `+0xA`. | Handler zero: B11. Otherwise B6. |
| B6 — latch and held path | `0x8003DD0C..0x8003DD2C` | Load constant one and compute `$s0<3`. If latch is nonzero, read unsigned held halfword at controller `+2`, mask `0x8000`. | Latch zero: B8. Held mask clear: B7C. Held mask set: B7. |
| B7 — held retry | `0x8003DD30..0x8003DD3C` | Branch on retry-count limit; the delay slot increments `$s0` either way. Below limit, unconditional branch retries B1 and reloads cursor word in its delay slot. At/over limit, proceed to outer path. | Below three: B1. Otherwise B10. |
| B7C — held release | `0x8003DD40..0x8003DD44` | Branch to outer path; delay slot clears latch `+0xA`. | B10. |
| B8 — pressed 0x8000 path | `0x8003DD48..0x8003DD54` | Read unsigned pressed halfword at controller `+4`; mask `0x8000`. If clear, likely branch to B10 reads outer counter in its delay slot. | Clear: B10. Set: B9. |
| B9 — pressed retry | `0x8003DD58..0x8003DD68` | Set latch `+0xA` to one; branch on retry-count limit, increment `$s0` in the branch delay slot; below limit, retry B1 and reload cursor word in the unconditional branch delay slot. | Below three: B1. Otherwise B10. |
| B10 — outer iteration/bound | `0x8003DD6C..0x8003DD90` | Read outer counter; reload current `D_801C77D8`; increment/store counter; compare updated count with current bound. The next likely branch retries only if the outer bound still allows another pass and `$s0<3`; its delay slot reloads current cursor word. | Bound reached or retry count `>=3`: B11. Otherwise B1. |
| B11 — shared epilogue | `0x8003DD94..0x8003DDC0` | Restore `$ra`, `$s0..$s7`, `$fp`; `jr $ra` with `sp += 0x48` in the return delay slot. | Return to caller. |

## All transfers and delay-slot effects

For regular branches and calls, the delay instruction always executes. For the
six branch-likely instructions, the slot executes only when the branch is
taken; when not taken, it is annulled. This distinction is part of the graph,
not a compiler hint.

| Transfer PC | Transfer and edge | Delay-slot instruction and effect |
| --- | --- | --- |
| `0x8003DC24` | `blez $t6` → `0x8003DD94` when initial bound `<=0` | `0x8003DC28 sw $zero,0x44($sp)` initializes outer count even on the early exit. |
| `0x8003DC60` | `jal DE80`; return at `0x8003DC68` | `0x8003DC64 lw $a0,0($s4)` reloads callback context. |
| `0x8003DC74` | `beq $s5,$v1` → `0x8003DC94` for state 3 | `0x8003DC78 nop`. |
| `0x8003DC7C` | `beq $s6,$v1` → `0x8003DC94` for state 4 | `0x8003DC80 nop`. |
| `0x8003DC84` | `beq $s7,$v1` → `0x8003DC94` for state 5 | `0x8003DC88 nop`. |
| **`0x8003DC8C`** | **`bnel $fp,$v1` → `0x8003DCA0` when state is not 6** | **`0x8003DC90 lw $t8,0($s1)` loads cursor only on the taken edge; state 6 annuls it and falls through to terminal cleanup.** |
| `0x8003DC94` | `b` → `0x8003DD94` | `0x8003DC98 sh $zero,0xA($s1)` clears the latch. |
| `0x8003DCA8` | `bnez $t8` → `0x8003DCBC` for nonzero cursor | `0x8003DCAC lui $v0,%hi(D_801C7774)` executes on either edge. |
| `0x8003DCB4` | `b` → `0x8003DD94` for null cursor | `0x8003DCB8 sw $zero,0($s2)` clears VM state. |
| **`0x8003DCC0`** | **`bnel $t9,$zero` → `0x8003DD70` when input gate is nonzero** | **`0x8003DCC4 lw $t8,0x44($sp)` reads outer count only on the taken edge; the zero-gate path annuls it.** |
| **`0x8003DCD0`** | **`beql $t1,$zero` → `0x8003DD0C` when pressed `0x4000` is clear** | **`0x8003DCD4 lhu $t2,0xA($s1)` loads latch only on the taken edge; when pressed, the slot is annulled before latch clear/handler logic.** |
| `0x8003DCE0` | `bnez $v0` → `0x8003DCF8` when handler value is nonzero | `0x8003DCE4 or $a0,$v0,$zero` supplies the `DE48` argument on the nonzero edge; for zero, `E680` is called next. |
| `0x8003DCE8` | `jal E680` for zero handler value | `0x8003DCEC nop`. |
| `0x8003DCF0` | `b` → `0x8003DD98` after `E680` | `0x8003DCF4 lw $ra,0x3C($sp)` starts the early-return epilogue. |
| `0x8003DCF8` | `jal DE48` for nonzero handler value | `0x8003DCFC sw $zero,0($s2)` clears state before the call returns. |
| **`0x8003DD14`** | **`beql $t2,$zero` → `0x8003DD4C` when latch is clear** | **`0x8003DD18 lhu $t5,0x4($s3)` reads pressed input only on the taken edge; a set latch annuls it and tests held input instead.** |
| `0x8003DD28` | `beqz $t4` → `0x8003DD40` when held `0x8000` is clear | `0x8003DD2C nop`. |
| `0x8003DD30` | `beqz $v0` → `0x8003DD6C` when retry count is not below 3 | `0x8003DD34 addiu $s0,$s0,1` increments on either edge. |
| `0x8003DD38` | `b` → `0x8003DC60` for immediate retry | `0x8003DD3C lw $a1,0($s1)` reloads the current script cursor. |
| `0x8003DD40` | `b` → `0x8003DD6C` after held input release | `0x8003DD44 sh $zero,0xA($s1)` clears latch. |
| **`0x8003DD50`** | **`beql $t6,$zero` → `0x8003DD70` when pressed `0x8000` is clear** | **`0x8003DD54 lw $t8,0x44($sp)` reads outer count only on the taken edge; pressed input annuls it before latch set.** |
| `0x8003DD5C` | `beqz $v0` → `0x8003DD6C` when retry count is not below 3 | `0x8003DD60 addiu $s0,$s0,1` increments on either edge. |
| `0x8003DD64` | `b` → `0x8003DC60` for immediate retry | `0x8003DD68 lw $a1,0($s1)` reloads the current script cursor. |
| `0x8003DD84` | `beqz $at` → `0x8003DD94` when updated outer count reaches bound | `0x8003DD88 slti $at,$s0,3` computes retry condition on either edge. |
| **`0x8003DD8C`** | **`bnel $at,$zero` → `0x8003DC60` when outer bound allows and `$s0<3`** | **`0x8003DD90 lw $a1,0($s1)` reloads cursor only for the taken retry; otherwise the slot is annulled and the function returns.** |
| `0x8003DDBC` | `jr $ra` | `0x8003DDC0 addiu $sp,$sp,0x48` restores frame size in the return delay slot. |

The six likely branches are exactly `DC8C`, `DCC0`, `DCD0`, `DD14`, `DD50` and
`DD8C`. Their slots are all present in the ROM-bound test. In particular,
`DD8C/DD90` is the tail retry edge: the cursor is loaded from global storage
only when another step is actually taken.

## Exit and retry summary

1. An initial nonpositive bound exits after the prologue. A state of 3, 4, 5 or
   6 clears the `+0xA` latch and exits after the callback/state reload.
2. A null cursor clears global word `+0`, clears VM state, and exits.
3. A pressed `0x4000` with zero `D_801C7774` calls `E680` and exits. A nonzero
   value takes the `DE48` restart path, stores its result to
   `D_80077858_78458`, then continues with the latch check.
4. A held `0x8000` while latch `+0xA` is set increments `$s0`; a newly pressed
   `0x8000` while the latch is clear sets the latch and increments `$s0`.
   Both immediate retries reload the cursor from `D_801C77E8+0` in the branch
   delay slot when `$s0<3`.
5. The outer path increments `sp+0x44`, rereads `D_801C77D8`, and retries only
   when the current bound permits another iteration and `$s0<3`. If either
   condition is false, the shared epilogue restores the 0x48 frame.

`DE80`, `DE48`, and `E680` effects are not modeled beyond the observed return
values, direct global reloads, and control flow. The 472-byte alias probe and
the separate 15-group/10,000-case host research do not make this function a
matching-C claim. Its original assembly ownership remains.

## G64-031 validation

- `test_vm_text_loop_addressing.py` passed the full 118-word ROM extent, ten
  addressing/controller anchors, and six branch-likely slots.
- Focused parser/alias/codegen tests passed **10** tests with `PYTHONPATH=decomp`.
- The 15-group GCC ASan/UBSan host harness passed. Existing differential
  harness runs passed **2,500** cases at seed `0x1D8` and **2,500** at
  `0xDEADBEEF` against local verified-ROM instructions.
- Full decomp Python suite: **128 passed**; verifier suite: **17 passed**.
- No native IDO build, original-address C comparison, new full-ROM build,
  inventory build, or in-game test was performed. The candidate and
  `GLOBAL_ASM`/manifest ownership remain unchanged.

**Next:** G64-032, isolate the 0x48 versus 0x50 frame and original saved-register
lifetimes without changing callback order or branch behavior.
