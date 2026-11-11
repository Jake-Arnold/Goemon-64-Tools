# VM main-step trace: `func_8003D68C_3E28C`

**G64-027 research checkpoint — 2026-11-11.** This is an original-instruction
trace, not a C reconstruction or matching-C claim. The function remains
`GLOBAL_ASM` in `script_vm.c`.

## Evidence and boundary

- Worktree branch: `codex/decomp-100-task-plan`; task started at commit
  `510e580b378e4eb9fab58164de36a7366e1d1129`, equal to the fetched
  `origin/chatgptweb/decomp` head.
- Pinned source: `mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
- Function: VMA `0x8003D68C`, ROM offset `0x3E28C`, 812 bytes / 203 words;
  original extent SHA-256
  `e49ad551d97f2f8cac887ee126e99dfdb29924901a4ff69f0792898207bf3da5`.
- The local decompressed USA ROM is SHA-1
  `6ea0ed71032ce08fc2745f412d84936382197494`. The private Splat listing is
  ignored and was compared word-by-word to the ROM extent.
- `test_vm_main_step_original.py` checks the 203-word extent, 44 branch/call/
  delay-slot anchors, ROM/VMA mapping and both jump tables (7 state entries,
  31 token entries). It is run with the private listing and ROM.

## Input/output contract

The routine takes no register arguments. It reads the global script cursor
`D_80077858_78458`, pause byte `D_801C78FC_1C84FC`, and VM state word
`D_801C77E0_1C83E0`; it calls `func_8003D17C_3DD7C` to update controller state
when it proceeds past the initial gates. It returns:

- `0` when the cursor is null at entry, becomes null after the controller
  update, or becomes null at the bottom of the dispatch loop.
- `2` when a non-null cursor is present and the pause byte is nonzero. This
  check precedes the controller update.
- `1` after a state-1 through state-4 or state-7 handler, when a state-5/6 poll
  leaves the state nonzero, or when token `0x8008` runs its reset path. States
  5 and 6 are special: if their poll helper clears the state, the same
  invocation continues to token dispatch.

The loop can consume several control tokens in one invocation. An exact opcode
meaning is only assigned below where the called helper and operands are
observable. Opaque helper behavior and indirect callback effects remain
unknown.

## Address-ordered control-flow map

| Original range | Verified flow |
| --- | --- |
| `0x8003D68C–0x8003D6CC` | Allocate a 40-byte frame and save `$s0/$s1/$s2/$ra`; load cursor. Null cursor returns 0. A nonzero pause byte returns 2. |
| `0x8003D6D0–0x8003D6E8` | Call controller-copy helper `D17C`, reload cursor, and return 0 if the reloaded cursor is null. The null check is branch-likely. |
| `0x8003D6EC–0x8003D710` | Read VM state, subtract 1, range-check unsigned against 7, then indirect through state table `jtbl_8007CF94`. States 1–7 have explicit entries. Other values continue to token dispatch. |
| `0x8003D714–0x8003D7A8` | Run the selected state helper. Most return 1 immediately. State 5/6 poll helpers return 1 if state remains nonzero; otherwise execution falls through to token dispatch. |
| `0x8003D7AC–0x8003D7E0` | Load the current 32-bit token; unsigned-check `token - 0x8004 < 0x1F`, advancing the cursor by one word in the branch delay slot. In-range tokens dispatch through `jtbl_8007CFB0`; out-of-range tokens go to the reset handler at `D988`. |
| `0x8003D7E4–0x8003D850` | Handle token `8004` by `DB0C` then `DE48`; handle token `8006` with comparator `D9B8`, conditionally skipping two additional stream words when the result is zero. |
| `0x8003D854–0x8003D8A4` | Token `8008` resets through `D428`, sets `D_801C7930=3`, and returns 1. Token `800A` relocates the word at the cursor. Token `800B` saves cursor+4, calls the function pointer loaded into `$a2`, then reloads the global cursor. |
| `0x8003D8A8–0x8003D8EC` | Token `8010` relocates the current word and stores it to `D_801C77E8` in the delay slot *before* calling paced reader `DBEC`. It then reloads the cursor and advances it. The state-5 path uses the already computed cursor; other states reload it. |
| `0x8003D8F0–0x8003D908` | Token `8011` calls `E6C0` with the cursor, relocates the returned word with `DE48`, and stores the result as the current cursor. |
| `0x8003D90C–0x8003D984` | Tokens `8020`, `8021`, `8022` call `24038`, `24088`, `240DC`. The first two advance one word. `8022` advances one word when the helper returns zero; otherwise it relocates the following word and installs that as cursor. Its zero test is branch-likely. |
| `0x8003D988–0x8003D9B4` | Default/reset path calls `D428`; loop tail reloads the cursor and branches back to state dispatch only when non-null. This final loop branch is branch-likely. Null cursor returns 0; the shared epilogue restores saved registers. |

## State dispatch table

The table at ROM VMA `0x8007CF94` maps state values 1–7. The dispatch
calculation is an unsigned range check; state 0, negative values, and values
above 7 bypass the state handlers and reach token dispatch.

| State | Target | Direct action | Return/fall-through |
| ---: | --- | --- | --- |
| 1 | `D714` | Call paced stream reader `DBEC`. | Return 1. |
| 2 | `D724` | Call choice handler `E81C`. | Return 1. |
| 3 | `D734` | Call input handler `E3EC`. | Return 1. |
| 4 | `D744` | Call input handler `E4C0`. | Return 1. |
| 5 | `D754` | Call poll helper `E5EC`; reload state. | Return 1 if nonzero; otherwise token dispatch. |
| 6 | `D778` | Call poll helper `E620`; reload state. | Return 1 if nonzero; otherwise token dispatch. |
| 7 | `D79C` | Call countdown helper `E654`. | Return 1. |

## Complete token dispatch table

The table at VMA `0x8007CFB0` has 31 entries for unsigned tokens `0x8004` to
`0x8022` inclusive. The default target is the reset path `D988`; its entries
are listed explicitly so no token meaning is inferred from a gap in the table.

| Token(s) | Target | Observed operation |
| --- | --- | --- |
| `0x8004` | `D7E4` | `DB0C(cursor)`; pass returned word to `DE48`, then store it as cursor. |
| `0x8005` | `D988` | Default/reset. |
| `0x8006` | `D800` | Read three following words; call `D9B8` with `$a0=word[1]`, `$a1=*word[0]`, `$a2=word[2]`. If result is zero, skip two more words. |
| `0x8007` | `D988` | Default/reset. |
| `0x8008` | `D854` | Call `D428`, set `D_801C7930` to 3, return 1. |
| `0x8009` | `D988` | Default/reset. |
| `0x800A` | `D870` | `DE48(*cursor)` becomes the current cursor. |
| `0x800B` | `D888` | Load the callback address from `*cursor` into `$a2`, store `cursor+4`, call via `jalr`, then reload current cursor. Signature and side effects are unknown. |
| `0x800C–0x800F` | `D988` | Default/reset. |
| `0x8010` | `D8A8` | Relocate `*cursor`; write that relocated word to `D_801C77E8` in the `DBEC` call delay slot; call `DBEC`; update cursor. The store is before the call and does not store the call's return value. |
| `0x8011` | `D8F0` | Call `E6C0(cursor)`, relocate its return with `DE48`, and store as cursor. |
| `0x8012–0x801F` | `D988` | Default/reset. |
| `0x8020` | `D90C` | Call `24038(*cursor)` after storing cursor+4; reload cursor. Helper semantics are not assigned here. |
| `0x8021` | `D928` | Call `24088(*cursor)` after storing cursor+4; reload cursor. Helper semantics are not assigned here. |
| `0x8022` | `D944` | Call `240DC(*cursor)` after storing cursor+4. Zero advances one additional word; nonzero relocates the next word with `DE48` and stores that cursor. |

Tokens outside `0x8004–0x8022`, including negative values interpreted as words,
take the same `D988` reset path. The reset wrapper calls D468 with `(0, -1)`;
therefore the exact external reset effects are owned by the already guarded
loader, not inferred anew here.

## Global state and callback boundaries

- The current cursor is repeatedly reloaded from `D_80077858_78458`. The
  indirect callback path advances it before `jalr` and reloads it afterward;
  callback-driven cursor changes therefore affect the next loop condition.
- State comes from `D_801C77E0_1C83E0` and is re-read after the state-5/6 poll
  helpers and at the loop tail.
- The pause byte is read before controller update. The controller helper is
  called only when the cursor is non-null and pause is clear.
- Token `0x8010` writes `D_801C77E8_1C83E8`; token `0x8008` writes
  `D_801C7930_1C8530`.
- `DE48` is the existing relocation helper. The indirect `$a2` callback,
  `E6C0`, and `24038/24088/240DC` retain opaque effects. The trace does not
  assume that any of them changes the resource-ID global.

## Host-model test matrix for a later C attempt

This is a required future matrix, not an executed host model. A model must keep
mock helper calls separate from game behavior and assert call order, cursor,
state and return value for each case.

| Case | Setup | Assertions |
| --- | --- | --- |
| Entry stop | Cursor is null; pause is either value. | Return 0; no controller or state/token helper call. |
| Pause | Cursor non-null; pause byte nonzero. | Return 2; no controller, state, or token helper call. |
| Cursor cleared by controller step | Cursor non-null and unpaused; mock `D17C` clears cursor. | Return 0 after exactly one controller call; no state/token dispatch. |
| States 1–4 and 7 | Non-null cursor; each valid state; helper leaves state unchanged. | Exact mapped helper once; return 1; no token dispatch in that invocation. |
| State 5/6 remains active | Poll helper leaves state nonzero. | Exact poll helper once; return 1; no token dispatch. |
| State 5/6 completes | Poll helper sets state to zero. | Continue through token dispatch in the same call; assert later cursor/state and return. |
| State range boundary | States 0, 8, `-1`, and `0x7FFFFFFF`; non-null cursor. | Bypass state table and dispatch the token. |
| Token range boundary | Tokens `0x8003`, `0x8004`, `0x8022`, `0x8023`, `0xFFFFFFFF`. | Only `0x8004` and `0x8022` use their mapped handlers; others reach default/reset. |
| All table entries | Exercise every token `0x8004–0x8022`. | Compare selected target/call sequence to the pinned 31-entry table, including all 21 reset entries. |
| Compare token | `0x8006`, comparator true versus false. | Three operands consumed in order; false additionally skips exactly two words. |
| Indirect callback | `0x800B`; callback leaves cursor alone, changes cursor, or clears it. | Cursor is advanced before callback; return value is ignored; post-call global cursor controls loop. |
| Relocated stream start | `0x8010`; mock `DE48` returns a word and `DBEC` may leave or mutate cursor/state. | Work global receives `DE48`'s return before `DBEC`; D68C ignores DBEC's direct return and reloads the global cursor/state along the observed paths. |
| External token helper | Each of `0x8020–0x8022`; helper returns zero/nonzero where consumed. | One-word advance for `8020/8021`; branch-likely extra-word/relocation behavior for `8022`. |
| Delay-slot controls | Null cursor at `D6E4`, zero helper result at `D958`, null/non-null loop cursor at `D994`. | Model whether each branch-likely delay-slot instruction executes or is annulled. |
| Resource-ID negative control | D68C's callback stub changes the separate resource global before a later helper. | Only assert reload behavior when the helper's original instructions prove a read; this D68C trace does not establish that the retail callback mutates the resource ID. |

No C candidate, translation-unit build, full-ROM gate, inventory, or in-game
test was run for G64-027. See the evidence packet at
`plans/execution/2026-11-11-g64-027-main-step-trace.json`.
