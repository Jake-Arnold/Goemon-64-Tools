---
name: goemon-bounded-probes
description: "Use to batch Goemon IDO compiler variants efficiently and avoid repetitive trial-and-error and large model-context dumps."
---

# goemon-bounded-probes

Read `decomp/batch.py`, `probe.py`, `BATCH_PIPELINE.md` and previous attempt logs. Generate a small grid tied to concrete first mismatches; skip unchanged 762-target scalar trials. Automate compilation and scoring, preserve source hashes/first relocation difference in local diagnostics, and summarize only best hypothesis and stop reason to Codex. Stop when variants fail to improve a specific difference. No approximate match counts.
