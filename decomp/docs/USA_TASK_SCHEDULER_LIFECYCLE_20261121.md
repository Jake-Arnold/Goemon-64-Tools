# USA task scheduler — original-address lifecycle trace and native-C follow-up

21 November 2026. Region: USA, retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; expanded SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Source of original operations: pinned upstream original MIPS unit `asm/usa/35280.s` and original MIPS unit `asm/usa/10D80.s`, with the pinned `include/common.h::TASK_W`. Addresses below are **USA only**, not Japan guest-memory crosswalk discoveries.

## Task structure and scheduling state

`TASK_W` is a linked scheduler record, not a generic gameplay actor. Confirmed byte offsets are: `next` +0x00, reverse/parent link `unk_4` +0x04, three callback slots `exec[0..2]` +0x08/+0x0C/+0x10, saved previous callback +0x14, callback-data `unk_18` +0x18, `priority` +0x20, and `unk_22` mask +0x22. Unknown fields remain unnamed.

The active scheduler state includes the list root `D_8006D328_6DF28`, current execution cursor `D_8016DAB4_16E6B4`, free/pool list references adjacent to `D_8006D328_6DF28` and the scheduler flag halfword at `D_800BCCC0_BD8C0 + 0xAE24`. Do not treat these as user-safe gameplay memory writes.

## Connected call flow (verified static MIPS)

| Stage | Original USA function | ROM offset | Observed role |
| --- | --- | --- | --- |
| Initialise pool | `func_8003488C_3548C` | `0x3548C` | Resets scheduler pointers; sets a default state; repeatedly initialises the task records |
| Initialise one task | `func_80034A10_35610` | `0x35610` | Clears task links, callbacks and multiple fields; uses the original task layout |
| Allocate/insert core | `func_80034B58_35758` | `0x35758` | Takes free record, initialises it, wires links, sets priority and mask |
| Insert relative to current | `func_80034B24_35724` | `0x35724` | Forwards the execution cursor, new task and mask to insertion core; **native C exact** |
| Insert in mode 1/2 | `func_80034C4C_3584C` / `func_80034C84_35884` | `0x3584C` / `0x35884` | Forwards current execution cursor, new task, mode 1 or 2, and 16-bit mask through `func_80034CBC_358BC`; **both native C exact** |
| Validated mode insertion | `func_80034CBC_358BC` | `0x358BC` | Calls insertion core and conditionally validates/reclaims the record before returning |
| Reposition task | `func_80034D24_35924` | `0x35924` | Traverses and rewires task list based on priority comparisons; not the execution loop |
| Compose insertion + activation | `func_80034DD8_359D8`, `func_80034E08_35A08`, `func_80034E38_35A38`, `func_80034E68_35A68` | `0x359D8..0x35A68` | Four **separately promoted** 48-byte wrappers invoke insertion routines and then the repositioning/activation helper |
| Execute scheduler callbacks | `func_80034734_35334` | `0x35334` | Iterates current list, compares priorities, checks active mask, calls resource-release helper, invokes three callbacks, rereads cursor after each callback; **original assembly retained** |
| Set first callback | `func_80035204_35E04` / `func_80035214_35E14` | `0x35E04` / `0x35E14` | Store slot +0x08 on current or specified task, already accepted C |
| Set other callbacks | `func_8003521C_35E1C`, `func_8003522C_35E2C`, `func_80035234_35E34`, `func_80035244_35E44` | `0x35E1C..0x35E44` | Set slot +0x0C or +0x10 on current or specified task |
| Removal/reclamation | `func_800350C4_35CC4` | `0x35CC4` | Handles priority-sensitive unhook/relink of task and callback changes, including fallback handler at `0x35D94`/`0x360B4`; calls `func_800351B4_35DB4` for resource cleanup |
| Remove current | `func_80035020_35C20` / `func_80035044_35C44` | `0x35C20` / `0x35C44` | Forwards current task to removal routine |
| Cleanup | `func_800351B4_35DB4` | `0x35DB4` | Clears task fields and invokes `func_80036260_36E60` cleanup helper |

This is a **static call graph and memory-layout trace**, not an emulator execution trace. For example, `0x35C44` is a thin forwarder that invokes `0x35CC4`; source ownership at prior accepted C stages must be checked before counting any further C functions.

## Original executor `func_80034734_35334` — unresolved registers

- Original is **344 B** (`0x158`), starts with 0x38-byte stack frame, saves `$s0` through `$s6`, and restores all seven plus `$ra` before returning. `$s5`/`$s6` have no other uses in its visible body.
- Closest semantics-preserving C candidate is **328 B / 82 instructions**, using a 0x30-byte frame and saving only `$s0..$s4`. Removing the original's two extra saves and two extra restores allows positionally aligning operation types of 82 instructions, **not** byte-exact instructions.
- Comparison function `func_80011A9C_1269C` (original USA ROM offset `0x1269C`, 188 B) saves and restores `$s0,$s1,$s2,$s3` although only `$s1` is referenced elsewhere in its body. This independently demonstrates unused callee-save operations in the original ROM. It does **not** prove compiler version, hand-written assembly, deleted source code, or linker postprocessing.
- Direct two-format recompile of identical `explicit_next` C source (compact single-line body vs expanded source-line boundaries) **still generates 328 B** and the same live saved-register set; neither is an original match. Host semantic tests are not MIPS equality evidence.

## Native compiler source-line experiment

Precisely controlled on original IDO 5.3 and original `Makefile` flags:

- `func_80034B24_35724`: the old multiline C function stores `$ra` before loading the cursor global high half, unlike the original. A semantically equivalent **single-line C function body** produces the original order; native G2 verified all 52 original bytes.
- `func_80034C4C_3584C` and `func_80034C84_35884`: single-line C bodies emit the cursor global high-half load before saving `$ra`, unlike the original. Making the same return expression **multiline** restores the original `sw ra` before `lui a0` ordering; both 56-byte functions are native G2 exact.
- This is observed source-layout-sensitive IDO instruction scheduling; the exact internal compiler mechanism is **not established**. C token semantics alone did not predict the instruction ordering. The experiment provides a controlled tool for small wrapper probes but has not forced the executor to save otherwise unused `$s5/$s6`.

## Native proof and boundaries

The two scheduler stages follow accepted 1,962 C: `scheduler5_g2_promotion.py` yields 1,963 C/84,536 instruction bytes and `scheduler6_g2_promotion.py` yields **1,965 C / 84,648 instruction bytes / 5,398 remaining ASM**. Both stages independently verified exactly **33,554,432 original USA ROM bytes** at SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, original **7,376 ELF function identities**, original **82,103 relocation records**, and strict inventory against the pinned original ELF. The two+one new wrappers together add **164 original C instruction bytes**. No original MIPS instruction bytes or relocations were patched; only native-generated, proven-zero alignment padding was normalised.

Original executor remains **FAILED_NATIVE / RESEARCH_ONLY**. New matching-C claims exclude the previously accepted task setter/traversal functions and exclude the 120-byte state dispatcher `func_80002040_2C40` (still research-only). No Japan decomp claim or runtime gameplay tests.
