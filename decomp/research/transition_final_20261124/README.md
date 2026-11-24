# Final transition-state research / native verification (2026-11-24)

Base `stable/decomp@bd11874060a88dcac218550013796a82b802a89b`. USA target 3CF0 (568 bytes); Japan 3C90 (444 bytes). Prior official inventories USA 2324, Japan 2551. See JSON native experiment records, `relocation-delta.json`, `strict-inventory.json`, and `decomp/COMPILER_QUIRKS.md`.

The USA source's formal `s32 state` is intentionally confined to the original assembly caller. The incoming register is overwritten before use. Historical prototype unknown; no incompatible C-to-C call is introduced. Future source recovery of the dispatcher must review the boundary. No-argument candidates remain failed. Whole native unit and original reference reproduce all original instructions and pool entries. Independent reference normalizes original numeric offset provenance and native local pool ownership; no native instruction/relocation records are patched. Guarded original metadata-only corrections and zero padding trim are required. Japan best remains 85/111; retain ASM.

Replay from the complete authenticated private USA2324 build and pristine original baseline, with original pinned IDO/binutils and ROM inputs already present:

```
PYTHONPATH=/path/to/Goemon-64-Tools python decomp/research/transition_final_20261124/verify_usa_3cf0.py --checkout /private/usa2324/candidate --baseline /private/usa2324/baseline --work /private/new-work --uv /path/to/uv --ledger decomp/COMPILER_QUIRKS.md --jobs 4
```

Use an expendable isolated checkout: the verifier edits local generated source/link layout and leaves the native object linked. Original reference ASM and all native/ROM outputs must stay private. To replay isolated controls use `replay_isolated.py --upstream /private/pinned-upstream --out /private/new-work --ledger decomp/COMPILER_QUIRKS.md --region usa arg_s32_add.c` (or `--region japan_0 japan/func_80003090_3C90_arg_reuse_i.c`). Original region expanded ROMs and pinned compiler must be present in upstream. Native replay and whole-ROM proof are distinct from canonical acceptance; no gameplay test.
