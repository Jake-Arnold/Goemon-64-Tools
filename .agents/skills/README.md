# Goemon repository-local agent skills

22 repository-local, task-specific skills are discoverable under `.agents/skills/<name>/SKILL.md`. Only skill metadata is loaded at discovery. Load the body of one relevant skill and an optional second specialist, not all 21.

Use `python3 -m decomp.skill_context --status` for the published canonical proof/inventory snapshot. `--validate` checks those two reports without building a ROM. The retired G64-001–100 plan no longer supplies live task packets.

| Skill | Trigger |
|---|---|
| [goemon-autonomous-decomp](goemon-autonomous-decomp/SKILL.md) | Use to coordinate a complete original-ROM C discovery → native verification → formal promotion session in ChatGPT or Codex. |
| [goemon-github-source-bridge](goemon-github-source-bridge/SKILL.md) | Use to recover source when GitHub connector access works but Linux cloning or filesystem transfer fails. |
| [goemon-target-triage](goemon-target-triage/SKILL.md) | Use to choose or prioritize the next Goemon assembly function instead of wasting variants on exhausted candidates. |
| [goemon-original-mips](goemon-original-mips/SKILL.md) | Use to reconstruct original Goemon MIPS control flow, callers, branch-likely delay slots, data references and return state. |
| [goemon-abi-layout](goemon-abi-layout/SKILL.md) | Use to recover Goemon o32 ABI, original struct offsets, signedness, endian widths, aliasing and callback-mutated pointers. |
| [goemon-ido-codegen](goemon-ido-codegen/SKILL.md) | Use to refine Goemon C syntax so native IDO 5.3 generates the original register allocation, stack frame, branches and instruction order. |
| [goemon-mismatch-triage](goemon-mismatch-triage/SKILL.md) | Use to diagnose near-matching compiler code with register, delay-slot, relocation, section, rodata or entire-unit scheduling mismatches. |
| [goemon-unit-promotion](goemon-unit-promotion/SKILL.md) | Use to integrate a researched Goemon C candidate into its production source and replace exactly one GLOBAL_ASM ownership claim. |
| [goemon-full-rom-proof](goemon-full-rom-proof/SKILL.md) | Use when validating production Goemon matching C, complete 32 MiB ROM identity, ELF inventory and final function promotions. |
| [goemon-proof-hardening](goemon-proof-hardening/SKILL.md) | Use when strengthening Goemon verifier, manifest checks, original-MIPS comparators, inventory or cache validation against false positive matches. |
| [goemon-host-regression](goemon-host-regression/SKILL.md) | Use to create deterministic host regression and sanitizer tests for Goemon function semantics, flags, callbacks, resources and linked lists. |
| [goemon-vm-resources](goemon-vm-resources/SKILL.md) | Use for Goemon VM resource lookup, loader, retries, signed halfword indices and entry versus live resource IDs. |
| [goemon-vm-stream](goemon-vm-stream/SKILL.md) | Use when working on Goemon VM text parser, token walker, branch-likely delays, stream cursor or signed opcode dispatch. |
| [goemon-vm-graphics](goemon-vm-graphics/SKILL.md) | Use for Goemon VM display-list emitters, two-word graphics writes, float callback ABI and number formatting. |
| [goemon-overlay-analysis](goemon-overlay-analysis/SKILL.md) | Use for Goemon N64 overlays, file_43 ROM/VMA mapping, ELF sections, rodata, key and Ghost Toys reconstruction. |
| [goemon-region-crosswalk](goemon-region-crosswalk/SKILL.md) | Use for every static USA or Japanese game-RAM discovery to propose and independently test the counterpart while preserving exceptions. |
| [goemon-scene-state](goemon-scene-state/SKILL.md) | Use for Goemon scene transitions, native map loading, reset state, entrances and story flags without unsafe warp changes. |
| [goemon-rea-evidence](goemon-rea-evidence/SKILL.md) | Use when evaluating Reverse Engineer Anything or direct Ghidra as optional read-only Goemon MIPS analysis evidence. |
| [goemon-upstream-review](goemon-upstream-review/SKILL.md) | Use to review pinned mnsg source or Goemon camera branches without merging speculative code or types. |
| [goemon-bounded-probes](goemon-bounded-probes/SKILL.md) | Use to batch Goemon IDO compiler variants efficiently and avoid repetitive trial-and-error and large model-context dumps. |
| [goemon-evidence-publish](goemon-evidence-publish/SKILL.md) | Use after any Goemon matching-C task to write a truthful evidence ledger, update progress, commit and verify remote branch state. |
| [goemon-input-reproduce](goemon-input-reproduce/SKILL.md) | Use to prepare or diagnose pinned Goemon ROM, IDO, upstream checkout, binutils, baseline cache and isolated build workdirs safely. |

Run `python3 -m unittest decomp.test_skill_context decomp.test_codex_skills -v` in the actual repository. Core `AGENTS.md` and `decomp/plans/EXECUTOR_PROTOCOL.md` remain the source of authority. Never include private ROM/code bytes, huge objdump logs, or global Codex settings in skill packages.

**ChatGPT usage:** These are GitHub-hosted repository instructions, not independently installed ChatGPT plugin skills. ChatGPT can read them using the connected GitHub tool or from a local checkout. For new Project chats, retain the Project source `GOEMON_AUTONOMOUS_DECOMP_SESSION_PROMPT.md` and its custom-instruction trigger. A Skill file does not grant network, filesystem, GitHub write or native compiler access.
