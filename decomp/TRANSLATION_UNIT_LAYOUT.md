# Original translation-unit boundaries and source-layout fidelity

**Decision, 24 November 2026 — DOC_ONLY / research backlog.** Preserve all existing accepted matching C. Do not restart, demote, or rewrite working functions merely because reconstructed source objects do not follow the inferred original source-file boundaries.

## Evidence and limitations

IDO 5.3 normally pads code-bearing translation units to 16-byte boundaries in this build convention. Aligned starts and trailing NOP padding are useful heuristics, not proof of a historical C file boundary or filename. Natural alignment, delay slots, assembly and linker layout can confound the inference. The original source organization cannot be uniquely inferred from an exact ROM.

Source-level review at stable/decomp `88c8de3366e1408b2eadd69bcc8d689a2b3d6434`:
- Primary USA manifest: 33 unit entries; 19 have at least one non-16-byte-aligned endpoint, covering 38 manifest-listed matching functions. This is a limited sample of the primary manifest, not a count of all artificial splits or all promoted functions. Additional promotion adapters can introduce individual native objects and ASM fragments.
- Examples: scheduler_views.c 0x7C14–0x7C24, scheduler_queue.c 0x7C24–0x7E04, audio_state.c 0x39964–0x39994, object_flags.c 0x36EDC–0x370FC, resource_dispatch.c 0x35AD4–0x35B44. The manifest's original/replacement Splat entries distinguish inferred upstream boundaries from reconstruction splits.
- verify.py deliberately changes main-segment subalignment from 16 to 4 for staging. This supports a valid matching-ROM workflow but is not evidence of historical source layout.
- COMPILER_QUIRKS.md documents the concrete 0xBEA0 boundary case: two unowned NOPs after the previous function's endlabel were wrongly absorbed into its ELF size (752 -> 760 bytes). Preserving the split and restoring linker-owned padding recovered original function size without changing ROM bytes. Do not strip functional NOPs or delay slots.
- Existing executor protocol already requires original-address native IDO, enclosing unit/neighbor verification, exact ROM, ELF and semantic relocations. Reconstructed units and inferred historical units are distinct.

No fresh private native compilation or ROM verification was performed for this note (NOT_RUN). The full combined proof was unavailable via connector during the assessment; source-level review does not independently re-prove past promotions. No canonical ownership, source, proof, inventory, or count change is authorized.

## Future research and consolidation

1. Build separate USA/Japan boundary inventories from pinned upstream Splat configurations, original expanded ROM/assembly, overlay-aware VMA mappings, text padding and data/rodata layout. Record confidence, evidence, function extent and inferred original owner separately from current source/object owner. Cross-region agreement is corroboration, not proof.
2. Prefer inferred original translation units for new work where practical. Do not impose an unconditional 16-byte rule on every function or artificial staging object.
3. Select nearly or wholly matching inferred units for bounded consolidation; preserve accepted bodies, declarations, source-line-sensitive IDO behavior, data ordering and original padding. Start with a small unit; use existing evidence to investigate blocked siblings.
4. Recompile consolidated units with pinned native IDO/flags and independently verify all affected functions, original extents, section layout, symbolic relocations, and compiler negative controls. Require fresh full original-ROM G2, ELF/global identities, semantic relocations, strict inventory, promotion integrity and the required full hosted regression before merging any source/build changes. If unsuccessful, retain the existing verified layout and record the blocker. Never weaken gates or use synthetic padding/instruction patches to claim a match.
5. Track matching functions/bytes, fully reconstructed inferred translation units, and source-layout fidelity separately. Do not conflate an upstream Splat guess, a matching synthetic object, or a fully matching reconstructed unit with a proven historical file boundary. No double counting or forced mass regrouping.

See [manifest](manifest.json), [verifier](verify.py), [compiler ledger](COMPILER_QUIRKS.md), [executor protocol](plans/EXECUTOR_PROTOCOL.md) and [continuation](CONTINUE.md).
