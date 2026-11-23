# Japanese C-Right: durable read-only live-trace handoff

**23 November 2026 LIVE PHASE-3 UPDATE (overrides the historic `LIVE_INPUT_PENDING` label below):** Both genuine normal and C-Right held/released Project64 3.x JSONL traces were supplied and audited, with sanitized findings in [GitHub issue #174](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/174#issuecomment-7097435753). Normal/held respectively: 105/704 events, 1/76 initializer entries, 0/75 held bypasses, 13/13 actor constructor calls and unique consecutive actor markers 1–13, 2/2 tracked post-load allocator arguments, 0/0 allocation during stage-slot aliasing, stage flag `+0xD1` 0/1 after loading. **Important:** initial stage task slots were not identical; no paired same-savestate causal proof or freeze trace. Raw JSONL files remain private. A new Japanese adjacent 60B stage handoff native C candidate has passed a full independent original-ASM 32MiB ROM, 7,376 ELF identities and 80,810 relocations; **RESEARCH_ONLY**, not accepted 2,370-C combined G2. See [new native-C research](../../research/jp_cright_tail60_20261123/README.md). The older instructions below remain as historical scripts and tests, not unfulfilled proof of the original held bypass.
**Status: `LIVE_INPUT_PENDING`** as of 21 November 2026. No live Project64 data is asserted. This directory intentionally holds only the ROM-independent trace comparator and its tests. The two debugger JavaScript recorders are available in the original user conversation's `Goemon-Japan-CRight-Project64-LiveTrace-Kit-20261120.zip` (SHA-256 `68cb525a941faa7407a95d62c4c1ede84f2a21195e6c09f35465fbdf5b6494aa`). They embed original-game instruction signatures, so **do not commit the scripts, `verified_opcodes.json`, or generated opcode tables into Git**. Retrieve the original user-provided kit/ROM locally, or regenerate probes from the user's verified ROM when testing.

Primary reference: https://github.com/Jake-Arnold/Goemon-64-Tools/issues/95#issuecomment-7051814616. Related original-MIPS research: https://github.com/Jake-Arnold/Goemon-64-Tools/issues/95#issuecomment-7051410257.

## Required actual gameplay experiment

- Run original **Japan-0**, normalized retail SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` (expanded 32 MiB SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`), using Project64 3.x debugger in interpreter mode. Never use these exact addresses on USA or a native recomp without revalidation.
- From the *same genuine pre-transition savestate*, capture normal transition and C-Right held->released transition separately. No cheats, RAM writes or warp injection.
- Verify overlay code signatures at runtime. Sample held gate `0x802125A0`, resolver call `0x8021BF44`, resolver result `0x8021BF50`, allocator first argument `$a0` at `0x8021BFBC`, stage task `0x80173294`, stage pointers at `0x801624B0` (`+0x90`) and `0x801624B4` (`+0x94`), callback at task `+0x0C`, and stage counter `0x801624F8` (`+0xD8`). Main allocator entries: `0x80035558`, `0x8003542C`, `0x8003492C`.
- Capture two authentic `.jsonl` logs. Never check in raw game memory logs or savestates. Record only sanitized findings, exact PC/field metadata, hashes and failure evidence on #95 and in task `GQ-CRIGHT-001`.

## Comparator (stdlib only)

```bash
python3 decomp/tasks/cright_live_trace/compare_cright_traces.py \
  --normal /path/to/Goemon_CRight_normal.jsonl \
  --held /path/to/Goemon_CRight_held.jsonl \
  --report /tmp/Goemon_CRight_live_comparison.json \
  --markdown /tmp/Goemon_CRight_live_comparison.md

python3 -m unittest discover -s decomp/tasks/cright_live_trace -p 'test_comparator.py' -v
```

Version-controlled `mock_normal.jsonl` and `mock_held.jsonl` are explicitly marked `test_only_mock: true` and contain synthetic pointers and no real gameplay or opcode signatures. They enable clean-checkout CI and must never be interpreted as live evidence. The comparator **rejects synthetic fixture data by default**, returning an inconclusive or rejected result rather than incorrectly claiming live task aliasing. The original kit's additional Node mock tests were run in the originating conversation, not against this Git subset. A lack of executed held gate or allocator call is inconclusive, not disproof. Even an observed aliased `$a0` proves only altered task-creation inputs, **not** a completed mis-parented task or the cause of visible corruption.