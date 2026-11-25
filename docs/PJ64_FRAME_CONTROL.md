# Experimental Project64 frame control

Use Project64 with the documented 2022.01.12 JavaScript debugger API and Interpreter core (CPU execution hooks require it). Enable debugger; open Debugger > Scripts and the scripts directory. In Goemon Toolkit, open Debugger > Frame control (PJ64), choose region, export the script there, and start it in Project64. Use a disposable save. Refresh, Pause at boundary, select input, Step +1. Step +5/+60 hold default input unless a relative timeline row overrides it. Example timeline:

```
1 A 0 0
2 - 0 0
3 Z+B 80 0
```

Use Run timeline with Steps=3. Unspecified rows use selected default input; `-` means neutral buttons. Stick values -80..80. The counter is session-relative, not an absolute movie frame. Pending operations refresh automatically. Resume relinquishes bridge ownership; Cancel clears queued input without resuming a debugger pause. If another debugger break or menu pause intervenes, clear the bridge and resynchronize; restart the script after loading a savestate or changing ROM. Do not use simultaneous emulator speed/warp/freeze tools during a step.

Default mode steps matching P1 PIF read responses, then requests a debugger break at the next CPU step. This is not necessarily one Goemon logic update or a rendered frame; the last response may not yet have been consumed by game code at the pause. Optional update PC must be manually verified for the exact ROM and hit once per logic update, before controller polling. The script stops at successive visits to that PC and overrides all matching polls within each interval. An interval with no matching poll stops with an error. No verified game-update PC is shipped. No ROM patch or arbitrary RAM write is used; the script writes only the P1 controller response in PIF RAM using the documented API. The PIF command signature follows Project64's example and other layouts are not supported.

The generated script contains a random session token. Keep it private; the server binds loopback only, accepts a bounded JSON command set, and verifies the selected ROM header CRC pair (not a full ROM hash). One bounded batch can continue even if the toolkit closes; cancel before leaving. Do not expose the port externally. Read-only toolkit mode disables all controls. This initial implementation is not live-verified against Project64 or Goemon; timing and Wine support must be validated on the actual emulator. Script API reference: https://github.com/project64/project64/blob/develop/JS-API-Documentation.html.
