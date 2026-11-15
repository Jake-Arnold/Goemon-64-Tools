# PR #17 consolidation and merge-readiness audit — 15 November 2026

## Current GitHub dependency stack

All of these pull requests were confirmed **open, draft and unmerged**:

| PR | Head | Base | Role |
| --- | --- | --- | --- |
| #13 | chatgptweb/japan-readonly-gameplay-fields | chatgptweb/japan-mupen-ambiguity-fix | Japanese source-backed fields |
| #14 | chatgptweb/japan-scene-probes-and-diff | chatgptweb/japan-readonly-gameplay-fields | Scene probes and comparisons |
| #15 | chatgptweb/japan-scene-trace-001 | chatgptweb/japan-scene-probes-and-diff | First scene trace |
| #16 | chatgptweb/japan-scene-character-traces-002 | chatgptweb/japan-scene-trace-001 | Character traces |
| #17 | chatgptweb/japan-controlled-party-writes | chatgptweb/japan-scene-character-traces-002 | Shared toolkit and Japanese writes |

PR #17 includes 285 commits as of this audit. The branch is NOT an independent patch against main; merging it without reconciling the ancestors would import the complete stacked history. Do not close or delete the ancestor branches before comparing their merge bases and independently validating the integrated result.

## Production and historical paths

- The production Japanese scene request uses practice/japan_direct_scene_reload.py: stage_japan_direct_reload. It writes the target pending scene and engine mode 0x0C. The **old** practice/japan_native_scene_warp.py still contains stage_japan_native_destination, which is exercised by historical tests but is not the production staging function.
- However, practice/toolkit.py still imports **is_japan_scene_loaded** from the old practice/japan_native_scene_warp.py. Therefore deleting that module without migrating its shared scene-state reader would break production imports. Keep it until references and tests are migrated.
- The old practice/japanese_party_unlock.py includes unlock_japan_party_member, now used by its regression tests rather than the shared Japanese UI. The production shared Unlocks path uses practice/region_unlocks.py with direct writes. Keep the old standalone test fixture until its behavioural equivalence has been proven.
- practice/unlocks.py retains all 34 original USA addresses, modes, and values. practice/region_unlocks.py now defines 34 Japanese candidate mappings: 9 named, 16 array-correlated, 4 regional-offset candidates, and 5 guesses; default Japanese Unlock All covers only the first 29. No individual guessed address is represented as user-live-verified.
- The original names, subweapon ownership, Treasure slots, and battery 0x20 bit require gameplay or control-flow evidence. ROM word-reference matches cannot prove those semantics.

## Tests and CI policy

- The repo AGENTS.md explicitly says: **local CI, no GitHub Actions workflows**, and decomp/CONTINUE.md reiterates it. Do not add a .github/workflows pipeline to circumvent that instruction.
- Existing scripts/test_japan_party.ps1 and .sh cover the Japanese/USA toolkit backend and GUI. The ROM-free MIPS scanner tests are included in those runners.
- When BOTH GOEMON_USA_DECOMPRESSED and GOEMON_JAPAN_DECOMPRESSED are supplied, the runners also verify the two exact 32 MiB hashes and execute the optional read-only ROM pattern scan.
- The scanned original ROMs passed SHA-1 verification; four synthetic scanner tests passed locally. The **complete private toolkit suite and live Windows/Project64 gameplay tests have not been run here**. This is an explicit merge blocker.
- decomp.local_ci remains an independent ROM-free C/verification gate. Nothing in this audit changes the USA exact-ROM matching-C evidence or production promotions.

## Merge gate and conservative cleanup sequence

1. Execute complete Windows PowerShell / Linux toolkit suites and confirm the latest test files pass. Verify Japanese warp with Goemon/Ebisumaru/Sasuke/Yae; character selection; unlock scroll; live memory edits; known nine unlock fields.
2. Validate provisional Bazooka, Medal of Flames, Chain Pipe, Gold Key, fortune-doll and treasure byte assignments in disposable emulator savestates; correct the provenance labels if they fail.
3. Isolate production uses of the old scene-state helper before removing the old native-menu staging prototype. Remove or archive redundant dead paths only after test proofs, not before.
4. Decide whether to land the Japanese stack sequentially in dependency order or create one reviewed integration PR targeting chatgptweb/decomp. For a single PR, compare the ancestry and file diffs first; do not force-push or erase other active worktrees.
5. After the region integration is verified and merged, prune only confirmed merged/unused remote branches. Keep active matching-C branches separate and do not mutate main or decomp manifests as part of toolkit cleanup.

Status: **research / local regression integration complete; full merge gate outstanding.** PR #17 should remain draft.
