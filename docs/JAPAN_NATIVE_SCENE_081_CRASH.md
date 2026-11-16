# Japanese native recomp: independent room crash (0x081)

**Evidence status:** User report, 16 November 2026. This document does not
claim a tested root cause.

## Gourmet Sub 2F Bazooka Room — scene 0x081

The user reports that **Gourmet Sub 2F Bazooka Room (`0x081`) crashes
independently within the Japanese native Goemon64Recomp client**, not only
when entered through the toolkit's custom warp.

Therefore:

- Track this as a **native-game recompilation/runtime** crash, owned by the
  Goemon64Recomp project (its own repository and test/build process).
- **Do not attribute the crash to the toolkit's scene reload or its
  USA/Japan shared entrance coordinates** without a reproducer demonstrating
  causation.
- **Do not work around it by making speculative guest-memory writes,
  overwriting actor pointers, or altering the native transition mechanism**.
- Keep toolkit warp diagnostics honest: a scene/map-ID change does not prove
  that the engine completed actor or room initialization. No room-specific
  crash workaround is part of the toolkit changes.
- A crash in the native client could still be triggered while a scene warp
  is active; that does not establish which component is at fault.

## Outstanding native-game evidence

Relevant supporting data would be an exact native game branch/commit, the
Gourmet Sub 2F Bazooka Room entry path, whether `0x081` crashes from
normal gameplay/debug-menu selection as well as direct toolkit warp,
and a symbolized native core dump stack trace. A raw core dump can
contain game assets, ROM buffers and other private memory: it is **not**
suitable for committing to this repository.

The earlier user log also showed an intermittent SIGSEGV after
`Initializing recomp heap` in a native JP executable. Without a backtrace
and same-scene repro, this startup crash is **not proven to be the 0x081
room crash**.

**Toolkit responsibility:** read-only status and no false positive
"playable actor confirmed" claim. **Native recomp team responsibility:**
inspect and fix the room-specific crash at its source.
