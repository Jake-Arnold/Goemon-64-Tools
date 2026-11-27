# Goemon 64 Decomp Continuation Handoff (Active Checkpoint)

> **Historical archives:** Full prior continuation logs are preserved verbatim in [CONTINUE_HISTORY_20261126.md](CONTINUE_HISTORY_20261126.md) (91 KB) and [CONTINUE_HISTORY_20261121.md](CONTINUE_HISTORY_20261121.md) (167 KB).

## Current Canonical State (`stable/decomp` after Batch #13 `exec_batch13_47`)

| Region | Reconstructed C | Matching Bytes | Remaining ASM | Total Positive ELF FUNCs | Expanded 32 MiB SHA-1 | Retail 16 MiB SHA-1 | Semantic Relocs | Stable Globals |
| --- | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: |
| **USA** | **3,505** *(+13 upstream = 3,518)* | **256,060** | **3,858** | 7,376 | `6ea0ed71032ce08fc2745f412d84936382197494` | `df8083a54296b8c151917c5333e1c85f014a2a66` | 82,080 | 26,714 |
| **Japan (`japan_0`)** | **3,377** | **238,476** | **3,999** | 7,376 | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` | `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` | 80,652 | 26,393 |

- **Pinned upstream:** `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`
- **Authentic compiler:** SGI IDO 5.3 `cc` SHA-256 `76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0`
- **Current canonical ELF SHA-256s:**
  - USA 3,505: `bf0215272a2adc8f13214ef45fba4aade33d6e520329e31872c868fa2a055ad4`
  - Japan 3,377: `59e518b26bb59ab240b3f4d1326e827f74c4e5c9267ad28ac6837f5831812802`

## Unified Data-Driven Promotion Workflow (All Future Batches)

All promotions after `promo36_promotion` use the single declarative batch registry — **do not create new one-off `promoN_promotion.py` modules or hand-edit hardcoded count tests:**

1. **Zero-token CPU harvesting (outside LLM):**
   - Cross-region mechanical port: `python3 scripts/harvest_cross_region.py ...`
   - `m2c --valid-syntax` + IDO 5.3 + near-miss packet export: `python3 scripts/harvest_zero_token.py ...`
2. **Minimal-context Executor loop (for near-misses & harder targets):**
   - Generate 4–8 KB quirk-indexed packets via `decomp/task_packet.py` (reads only the 1–2 relevant sections of `decomp/COMPILER_QUIRKS.md`, enforces a 3-attempt non-improving escalation ceiling).
3. **Standalone zero-LLM native G2 verification & activation:**
   - `python3 -m decomp.run_promotion --batch-id <id> --namespace <ns> --research-dir research/<dir> --base-commit <sha> --work <private-work> --usa-snapshot <usa-snap> --usa-pristine <usa-prist> --jp-snapshot <jp-snap> --jp-pristine <jp-prist> --uv <uv> --jobs 10 --activate`
   - Automatically verifies native IDO positives/negatives, full expanded & retail ROMs, 7,376 FUNC identities, semantic relocations, stable globals, strict inventory, updates `decomp/batches/registry.json`, `manifest.json`, `results/combined.json`, `results/inventory.json`, and `regions/japan_0.json`, and prints a ~30-line JSON receipt.
4. **Canonical ROM-free validation & PR:**
   - Local spot-check: `python3 -m decomp.promotion_integrity --validate && python3 -m decomp.batch_registry`
   - Push `decomp/<topic>`, open PR against `stable/decomp`, require hosted GitHub Actions `Decomp ROM-free regression` + `Branch base and topic prefix` before merging.

## Next High-Value Targets

- **Ready open research PR:** **#266** (2 JP transition functions, 280 B, clean named relocations).
- **Shadow/dual-reference research PRs:** **#283** (6 float-pool warp helpers, 712 B), **#267** (2 JP controller handlers, 632 B), **#279** residual (2 exit decoders, 896 B).
- **Near-miss executor queue:** 77 compact 2.5–3.5 KB task packets (38 USA + 39 JP, <=6 differing words) exported by `scripts/harvest_zero_token.py`.
- **Cross-region multi-function donors:** ~32 remaining USA->JP fingerprint-matched pairs that only need header/extern resolution.
