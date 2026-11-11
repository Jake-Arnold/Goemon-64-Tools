---
name: goemon-original-mips
description: "Use to reconstruct original Goemon MIPS control flow, callers, branch-likely delay slots, data references and return state."
---

# goemon-original-mips

Work from SHA-verified original instructions, exact function start/end and guest VMA. Trace branch delay slots, signed predicates, jal argument timing, loaded/stored widths, callbacks and return values. Use callers to infer parameters. Separate facts from guesses; annotate exact ROM offsets. See `VM_MAIN_STEP_TRACE.md` and `VM_STREAM_MATCHING.md` for VM work. Original-instruction analysis is research, not a match claim.
