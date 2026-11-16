# Isolated Japanese toolkit integration (16 November 2026)

## Scope

This *toolkit-only* candidate is based directly on the current `main` commit `12e7699a42948fa7816b2049eaca60d2ed3f518c`. It carries the user-accepted Japanese region-aware Practice Toolkit without importing the separate 283-file decomp history, .agents instructions or additional decomp-only tests from the original Japanese development branch.

The source is the reconciled `chatgptweb/japan-main-integration-20261116` tree (`d3d4fa1410ddc5b83fb5858b5db50e4c3aec54fa`), which already retains the mainline v0.11.17 Plasma flag research and 13 new USA Plasma Story Progress annotations, while preserving Japanese gameplay features.

## Included

- Whole `practice/` subtree (region-aware Japanese/USA toolkit), `autosplitter/` (cross-platform process/RDRAM access), `speed/` (Linux speed-channel compatibility), `scripts/` (cross-region Windows/Linux regression runners) and two text-only Japanese runtime research records.
- 72 selected toolkit/backend/Tk regression test changes; main's original `tests/` tree remains intact including the new Plasma condition tests. Decomp-only test modules from the Japanese branch are deliberately *excluded* so they cannot refer to source files absent from `main`.
- 35 Japanese/toolkit documentation changes; main's `docs/` tree and Plasma reports remain intact. Decomp-specific branch policy and overlay research docs are excluded from this candidate.
- Updated README from the original Japanese branch; a concise mainline PROGRESS log entry accompanies this commit rather than replacing main's development log with 640KB of unrelated branch history.

## Acceptance and caveats

Prior user acceptance confirms **33/34 Japanese Unlocks**, all Japanese warps, Live Memory Freeze/Unfreeze, named native Project64 checkpoints and Japanese Story Progress work, and the previous source branch passed **195 backend + 94 GUI Windows tests**. The deferred Sasuke Battery 1 mapping remains excluded from default bulk unlock.

These acceptance checks were **before** the isolated integration. The isolated `main`-based tree must be tested using `.\\scripts\\test_japan_party.ps1` on Windows before merging. The suite now includes the original mainline USA Plasma tests. Any Linux-only runtime paths need Linux validation separately. There are no committed ROM or savestate assets.

The original Japanese/decomp source branches and full-history integration draft PR #21 remain unchanged for historical preservation and separate decomp review.
