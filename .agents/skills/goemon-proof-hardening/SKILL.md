---
name: goemon-proof-hardening
description: "Use when strengthening Goemon verifier, manifest checks, original-MIPS comparators, inventory or cache validation against false positive matches."
---

# goemon-proof-hardening

Read `verify.py`, `compare_original.py`, `inventory.py` and applicable tests. Define false-positive risk before editing. Add positive and negative fixtures for wrong ROM SHA, stale source hash, overlapping ownership, mismatched relocations, section shifts, altered extents and invalid cache. Negative controls must fail closed. Never weaken thresholds or masks to get a candidate accepted. Separate synthetic tests from fresh native full-ROM results.
