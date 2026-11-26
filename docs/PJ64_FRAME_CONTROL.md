# Experimental Project64 frame control

Use Project64 with the documented 2022.01.12 JavaScript debugger API and Interpreter core (CPU execution hooks require it). Enable debugger; open Debugger > Scripts and the scripts directory. In Goemon Toolkit, open Frame Inspector > Project64, choose region, export the script there, and start it in Project64. Use a disposable save. Refresh, Pause at boundary, select input, Step +1. Step +5/+60 hold default input unless a relative timeline row overrides it. Example timeline:

```
1 A 0 0
2 - 0 0
3 Z+B 80 0
```

Use Run timeline with Steps=3. Unspecified rows use selected default input; `-` means neutral buttons. Stick values -80..80. The counter is session-relative, not an absolute movie frame. Pending operations refresh automatically. Resume relinquishes bridge ownership; Cancel clears queued input without resuming a debugger pause. If another debugger break or menu pause intervenes, clear the bridge and resynchronize; restart the script after loading a savestate or changing ROM. Do not use simultaneous emulator speed/warp/freeze tools during a step.

Default mode steps matching P1 PIF read responses, then requests a debugger break at the next CPU step. This is not necessarily one Goemon logic update or a rendered frame; the last response may not yet have been consumed by game code at the pause. Optional update PC must be manually verified for the exact ROM and hit once per logic update, before controller polling. The script stops at successive visits to that PC and overrides all matching polls within each interval. An interval with no matching poll stops with an error. No verified game-update PC is shipped. No ROM patch or arbitrary RAM write is used; the script writes only the P1 controller response in PIF RAM using the documented API. The PIF command signature follows Project64's example and other layouts are not supported.

The generated script contains a random session token. Keep it private; the server binds loopback only, accepts a bounded JSON command set, and verifies the selected ROM header CRC pair (not a full ROM hash). One bounded batch can continue even if the toolkit closes; cancel before leaving. Do not expose the port externally. Read-only toolkit mode disables all controls. This initial implementation is not live-verified against Project64 or Goemon; timing and Wine support must be validated on the actual emulator. Script API reference: https://github.com/project64/project64/blob/develop/JS-API-Documentation.html.

## v0.11.86 — Frame Inspector

Open Frame Inspector > Project64. Add up to 12 read-only watches, one per line, with a unique label, type (`u8`, `u16`, `u32`, `f32`) and aligned guest address in the first 4 MiB. A `@catalogue_id` selects an existing region-specific address; `@usa_id|japan_id` selects between explicitly supplied IDs according to the ROM region. No automatic offset translation or dynamic pointer guessing. Re-export and restart the companion after editing watches, region, execution PC or breakpoint. Dynamic player-task addresses must be rechecked for each loaded state. Example syntax (address illustrative, not a game-field identification):

```
example u32 80001000
```

Pause at a boundary, then Record and step or run timelines. The bridge captures a baseline and each completed boundary in the emulator callback; its bounded latest batch has at most 61 samples. Record accumulates up to 600 samples across contiguous completed batches; Stop recording stops collection without resuming. Latest batch / recording switches between views. Resume, cancellation, connection changes and interrupted synchronization end recording. Export CSV or JSON locally; JSON includes the raw aligned words, typed watch definitions, ROM region, execution/poll mode, breakpoint and error metadata. Compare saved JSON uses the same region, hook, watch definitions and breakpoint, aligns samples by relative row and displays current / reference values for differences. Orange rows changed from the preceding sample, red rows differ from the reference. A poll sample is **before game consumption**; an execution-hook sample is at entry to that instruction, not necessarily a game frame. Missing controller polls are errors; do not interpret incomplete traces as completed inputs.

Optional breakpoint: `exec 80123450` or `write 80123450` (illustrative address). The bridge uses the documented interpreter CPU hooks and stops the active step batch at the first hit, before the instruction executes. It records the PC, configured address and a pre-instruction sample. Exact-address write hook only; no claim of overlapping-store coverage. Resume and pause at a fresh boundary to continue. No arbitrary CPU execution, RAM modification or remote debugger commands are exposed. Project64 only; Mupen64Plus, native recomp, actual timing, and live Wine/Windows behavior are not verified. No Ebi-specific dynamic watches or game-update PC are shipped until reviewed regional metadata and live verification are available. Keep exported traces private; do not commit them.
