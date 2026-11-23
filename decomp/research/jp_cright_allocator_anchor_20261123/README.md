# Japan-0 C-Right: retained stage anchor and allocator lifetime audit (23 November 2026)

Status: RESEARCH_ONLY / original MIPS bounded synthetic task-memory replay. No actual gameplay, native IDO attempt, G2 change or accepted-C increment.

## Provenance
- Base stable/decomp `1ddb1b0941b0f39d4db6b0a3534fc1f230b51e0e`, verified source archive 14865248967.
- Upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee; privately supplied normalized Japan-0 retail SHA-1 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b; freshly expanded 33,554,432-byte ROM SHA-1 6f8745fecc3a5e7d4918c7a73353eb0726116ded. Splat extraction successful. Compared 8,691 generated instruction/data annotation rows across ten selected original source files against the expanded ROM; all exact.
- Existing research: #174, #95, draft #188 and draft #205. No promotion claims and no duplication of their candidate C.

## Static chain
The original stage reset at 0x8021DB74 clears +0x90 and +0x98..+0xAC but not +0x94. The two caller sites (0x801FC350 and 0x801FCF50) subsequently create the +0x90 task and schedule the stage initializer. Category 11 in the resolver jump table at expanded ROM 0x5FA824 selects the return at 0x8021EAC0/0x8021EAC4, which reads stage+0x94. The unsigned counter guards compare +0xCC against +0xC8 and +0xC4; the reset clears the latter two. Both normal and held initializer paths overwrite +0x94; a retained old pointer is relevant only if consumed before that overwrite, or if the overwritten task later becomes invalid.

At the low-level allocator 0x800347C8, a nonempty free list causes allocation-count increment, reading the anchor's next link, assigning the free-list head to anchor.next (0x80034810), then reading the free head's next link (0x80034818), and invoking task clearing (0x8003482C -> 0x80034680). It then reloads anchor.next at 0x80034840 and writes the old successor through it at 0x80034848. This path does not check active-list membership of the anchor. Original task destruction 0x80034D34 can unlink a task and put it on the free list. This alone does not establish that any particular stage task was destroyed.

## Bounded original-instruction replay
The original integer MIPS instructions are fetched directly from the authenticated private ROM, with explicit branch-delay semantics and a synthetic memory map. Stop at 0x80034878 (after callback installation, before the external resource call), on return, or on an invalid synthetic memory access. No original bytes are embedded or output. The source-only user artifact goemon_cright_allocator_microtrace.py SHA-256 babf525b965e1de8ef7540a452d33e26ec01b789700d9125f356cc319f3b106b is delivered in the conversation. Run it using Python 3 and the privately expanded ROM path.

| Case | Result |
| --- | --- |
| Active anchor, available free nodes | 141 instructions; prefix completes, free head advances and allocated callback installed |
| Anchor equals free head | 129 instructions before invalid store at 0x80034848 to address 0x00000000; free head still equals cleared anchor |
| Anchor is interior free node | 141 instructions; prefix completes but the allocated node remains reachable from the free head, with changed list links |
| Empty free pool | 14 instructions; returns without increment or splice |

All four assertions passed, independently agreeing with a four-case abstract splice model. Python syntax compilation passed. This is not emulator-level exception handling or a full scheduler execution. The interior-node result is measured at a prefix boundary; later resource and insertion/sort callbacks are not executed.

## Discriminating live evidence
Use the same genuine pre-transition savestate for normal, held/released C-Right, and separate bit-8 control. Capture the category-11 resolver return and actual allocation anchor, active-list membership/free-list membership at allocator entry, free head and next link, the stage +0x94 overwrite, and the first exception/loop or door freeze if any. First establish whether the retained pointer is consumed in the reset-to-initializer window at all. Held-state aliasing of valid active nodes is not the same as a free-list alias. If no category-11 allocation occurs in this window, this specific mechanism is not demonstrated. No game mutation or live trace has been performed.

No native compiler attempt (NOT_RUN); no new quirk classification, no full ROM rebuild or local CI for these documentation-only findings. No toolkit changes. Current regional C ownership and existing G2 gates unchanged.
