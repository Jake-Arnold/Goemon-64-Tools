---
name: goemon-scene-state
description: "Use for Goemon scene transitions, native map loading, reset state, entrances and story flags without unsafe warp changes."
---

# goemon-scene-state

Read `MAP_TRANSITION_TRACE.md`, `transition_state.c`, `default_entrance.c` and callers. Trace request state, resource load/unload, object teardown and actual transition distinctly. Annotate observed globals and external calls. Matching setter C does not establish safe runtime room warp. Avoid raw map writes and unrelated gameplay features on this decomp branch. Host, byte-match and in-game claims are separate.
