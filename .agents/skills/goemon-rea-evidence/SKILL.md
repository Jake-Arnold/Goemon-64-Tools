---
name: goemon-rea-evidence
description: "Use when evaluating Reverse Engineer Anything or direct Ghidra as optional read-only Goemon MIPS analysis evidence."
---

# goemon-rea-evidence

Read `decomp/plans/REA_PILOT.md` and control list. Run local `python3 -m decomp.rea_pilot_preflight PRIVATE.elf --strict`. Goemon uses `-mips2`, outside REA's currently documented standard MIPS ISA admission. If actual ELF/provider rejects, record REA_UNSUPPORTED_GOEMON and continue normal research; never spoof flags. If admitted, cross-check ten known original functions before trusting pseudocode. All findings are research-only and private.
