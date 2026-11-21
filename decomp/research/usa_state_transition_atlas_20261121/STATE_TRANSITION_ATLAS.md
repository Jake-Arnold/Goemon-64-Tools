# Original USA engine: 18-state transition atlas and file-22 bridge

**Research tier: STATIC_ROM_VERIFIED / RESEARCH_ONLY.** Original retail USA SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; expanded 32 MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; pinned `mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. This report adds a source-anchored **outer-state edge inventory** and a **cross-overlay bridge** to the earlier `decomp/MAP_TRANSITION_TRACE.md` and 18-handler map. It does not change the matching-C ledger, emulator/toolkit state or accepted function count.

## Method and boundaries

The original 18-pointer table at expanded ROM `0x59508` selects on `SYS_W.stepw`, an unsigned byte at dynamic system pointer `D_8015C5C8 + 0x3ADD4`; the dispatcher has **no local bounds check**. The five-entry table for outer state 15 at `0x7B48C` selects on system byte `+0x3ADD6` with an unsigned `<5` check. The file-22 overlay at `0x69E080`/VMA `0x801CB460` contains a separate **two-pointer, unchecked** selector at ROM `0x6A9850`, *also* using `+0x3ADD6`. These tables have been independently checked against the original decompressed USA ROM, not inferred from the apparent file names.

The matrix below inventories **direct calls** to the original state setter `func_80003728_4328` within each of the 18 primary handlers, and calls to the separate increment helper `func_8000378C_438C`. Multiple target values mean conditional execution paths, **not** a single deterministic successor. Other functions, callback side effects and loaded overlay functions can write state independently: the matrix is not a proof of absence of other transitions.

| Outer state | Original handler, ROM offset | Direct `set(value)` requests | Increment helper | Other observed context |
|---:|---|---|---|---|
| 0 | `func_800020B8_2CB8` | — | Yes | Engine initialisation/helper calls |
| 1 | `func_80002138_2D38` | — | Three call sites | Loader request ID 23; nested-state adjustment |
| 2 | `func_8000236C_2F6C` | 3 | — | Loader request ID 15 |
| 3 | `func_80002454_3054` | — | — | Loads file 22; calls file-22 overlay dispatcher; **overlay can directly assign outer state 4** |
| 4 | `func_80002518_3118` | 6, 5 | — | Loader request ID 20; task scheduler, reset/transition helpers |
| 5 | `func_80002718_3318` | 6, 7, 8, 15 | — | Nested selectors, transition and cleanup gating |
| 6 | `func_80002938_3538` | 5 | — | Nested selectors, task and transition helpers |
| 7 | `func_80002A98_3698` | — | — | Forwards to `func_80005B90_6790`, which conditionally requests 3 or 5 |
| 8 | `func_80002AB8_36B8` | 5, 9, 11 | — | Loader request ID 15, scheduler and transition helpers |
| 9 | `func_80002C7C_387C` | 11 | — | Reset and task/transition loop |
| 10 | `func_80002D94_3994` | 3 | — | Conditional on `stepw_end` and helper result |
| 11 | `func_80002DE4_39E4` | 13 | — | `D_800548D8` gate |
| 12 | `func_80002E70_3A70` | 13 | — | `D_800548D8` gate |
| 13 | `func_80002EFC_3AFC` | 3 | — | Nested dispatcher and scheduler |
| 14 | `func_80002F54_3B54` | 11, 3 | — | `D_800548D8` gate; nested `stepw_end` branches |
| 15 | `func_800030F0_3CF0` | 5 | — | **Five-way** bounded substate table, file-15 request, task callbacks |
| 16 | `func_80003328_3F28` | 17 | — | Direct confirmed request for state 17 |
| 17 | `func_80003358_3F58` | — | — | Three-way VM dispatcher followed by the task executor |

The machine-validated set comprises **20 original call sites** to `func_80003728_4328` plus **four** `func_8000378C_438C` call sites inside these 18 handlers. The data file records each call's exact ROM offset and original immediate-provenance instruction. The checked loader sites are a deliberately bounded subset, not every loader call or every resource boundary. In particular the entry-7 forwarding target's `3/5` possibilities are **transitive**, not direct requests from the entry-7 wrapper.

## New verified path: outer state 3 -> file 22 -> outer state 4

1. At outer handler `func_80002454_3054`, the nested-state-zero path requests resource **ID 22** through `func_80001C00_2800`, destination `0x801CB460` (original callsite ROM `0x3080`), then invokes `func_801CB460` at `0x30A8`.
2. Pinned Splat maps file 22 to original expanded ROM `[0x69E080,0x6A9920)` and guest VMA `0x801CB460` within mutually exclusive `static_overlay_1`. Its first callable is `func_801CB460_69E080`, an **unchecked two-entry dispatcher**; the exact table at `0x6A9850` contains `0x801CB4BC` (nested 0) and `0x801CB53C` (nested 1).
3. Nested entry 0 (`func_801CB4BC_69E0DC`) advances `SYS_W +0x3ADD6` by one after its preparation calls. Consequently the next invocation **may** select nested entry 1; the code alone does not establish a particular game's frame sequence.
4. Nested entry 1 (`func_801CB53C_69E15C`) checks `(system[0x3B07C] & 0x9000) != 0` and the overlay-local 32-bit counter at `D_801D7008`. Counter **1** is changed to **2** and returns along the common path. Counter **at least 2** can call `func_80038BC8(1)` and then **directly** store outer state byte **4** (`0x69E1D8`), clear nested byte `+0x3ADD6` (`0x69E1E8`) and reset the overlay word `D_801D6D00`. Its additional counter==5 branch sets `stepw_end=1` independently.
5. That outer-state store does **not call** `func_80003728_4328`, unlike the usual edge. The normal setter resets `stepw_end`, the secondary and deeper selectors, and configures `retraces_per_game_step=2`; the direct overlay store does not itself do those things. Thus asserting a universal reset invariant after every state transition would be **false**. Other callee side effects are unknown.

The file-22 entrypoint and file-15 loading path share **guest** VMA `0x801CB460` as mutually exclusive overlay occupants. It is essential to identify the resident file at runtime before interpreting a PC at this VMA; an address alone cannot disambiguate the active overlay.

## Outer state 15: bounded nested dispatcher and edge to state 5

The five entrypoints at ROM `0x7B48C` are `0x80003128`, `0x80003144`, `0x800031AC`, `0x800031DC`, `0x80003228`. Original ROM code checks the unsigned nested selector against 5. The following are observed static effects, not gameplay labels:

- Nested 0 sets a system halfword to 1, resets the end byte, increments the nested selector.
- Nested 1 checks global `D_800548D8`. Nonzero returns without loading; zero performs `func_8000383C`, requests **file 15** into `0x801CB460`, runs a fixed countdown and increments the nested selector.
- Nested 2 clears the same system halfword and increments the nested selector.
- Nested 3 sets system halfword `+0x3ADF4 = 3`, calls task-list pool initializer `func_8003488C(0x801CCB7C)` and increments the nested selector.
- Nested 4 checks the outer `stepw_end` byte: 0 runs the task executor; 1/2 call `func_8000383C`, choose `+0x3ADF4` as 3/1, clear the end byte and reset the task pool; 3 calls `func_8000383C`, writes `0x8000` to a control halfword and calls the **canonical** outer setter with argument **5**. Values outside 0..3 return.

This complements earlier detailed transition and loader research, rather than replacing it. It proves a *request* for file 15, not that it was successfully loaded or that a particular scene is ready.

## Confidence and remaining unknowns

**Authenticated static facts:** all three original pointer tables; exact 18/5/2 entry counts; 20 state-setter call sites with literal arguments; four increment-helper calls; selected loader request IDs; the file-22 direct state-4 store and nested-state reset; and the state-15 direct outer-state-5 request.

**Unresolved:** gameplay meanings for the numerical outer states; complete edge coverage from overlays, callbacks, SDK, and writes through computed pointers; whether state-3 reaches the overlay nested-1 branch on a particular frame; why the overlay path bypasses the normal reset routine; precise timing of file22/file15 overlay residency and resource retirement; whether external code constrains the otherwise unchecked 18- and 2-entry dispatch selectors; all resource-loader side effects; and runtime execution evidence.

## Read-only runtime capture prescription (not executed)

Capture, on the same frame, original guest PC, current resident overlay file ID, `*(D_8015C5C8) + {0x3ADD4,0x3ADD5,0x3ADD6,0x3ADD7,0x3ADDE}`, `D_800548D8`, and when file 22 is resident the local counter at `D_801D7008` plus the relevant `+0x3B07C` halfword. Break at `0x800024A8`, `0x801CB53C`, `0x801CB5B8` (only for file22), `0x80003148`, `0x80003164`, and `0x80003728`. Compare pre/post states and verify the active overlay before interpreting those guest code VMAs. This is an observation recipe **only**; no writes, artificial state forced transitions, emulation, or safety guarantees are implied.

## Reproduction

With the user's private pinned original-USA expanded ROM, outside Git:

```sh
python3 verify_static_atlas.py --rom /path/to/private/baserom.decompressed.z64 --report /tmp/state_atlas_proof.json
python3 -m unittest -q test_static_atlas.py
```

The machine-readable `state_atlas.json`, decoder/checker and synthetic tests contain no original-ROM/extracted-ASM instruction dumps, assets, binaries, or toolchains. The sanitized proof contains only addresses, counts, hashes and event-edge metadata.
