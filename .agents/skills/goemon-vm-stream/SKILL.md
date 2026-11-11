---
name: goemon-vm-stream
description: "Use when working on Goemon VM text parser, token walker, branch-likely delays, stream cursor or signed opcode dispatch."
---

# goemon-vm-stream

Read `VM_STREAM_MATCHING.md`, `VM_MAIN_STEP_TRACE.md`, phase 04 and `script_vm.c`. Map DBEC cursor and loop state; DF98 uses signed -71..-32 tokens separately from -1 sentinel. Test null exits, callback rereads, marker/repeat changes and annulled delay slots with ROM anchors. Verify exact extent (F6E8 is 48 bytes, not an old 56-byte annotation). Do not infer retail game semantics from names.
