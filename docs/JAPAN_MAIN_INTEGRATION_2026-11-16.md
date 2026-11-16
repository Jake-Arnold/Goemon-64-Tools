# Japanese/Main Integration Candidate — 16 November 2026

The candidate is a **two-parent Git merge**, with the full live-accepted Japanese toolkit source `dd35df81b36a4230f1a6396ead8479722b3b5ccd` and the latest mainline Plasma research `12e7699a42948fa7816b2049eaca60d2ed3f518c`. Their common ancestor is `5ff51ec0f16bc080617063d27b9270bb0008dde7`. Neither source branch is rewritten or deleted.

## Reconciliation

- The eight unchanged/new main-only paths are restored by their **exact Git blob SHA**: `Run.bat`, `docs/KEGON_HINT_FLAG.md`, `decomp/plasma_conditions.py`, `decomp/plasma_writers.py`, `decomp/results/plasma_conditions.json`, `decomp/results/plasma_writers.json`, `docs/PLASMA_TRIGGERS.md`, and `tests/test_plasma_conditions.py`.
- `PROGRESS.md` gains the mainline Plasma research record; `decomp/CONTINUE.md` gains the mainline Plasma link.
- `practice/story_progress.py` keeps existing Japanese/USA story models but incorporates the 13 USA Plasma condition flags, both user-verified priority-bit provenance notes, and the merged `FLAGS` registry.
- `tests/test_story_progress.py` gains the mainline Plasma priority test. `tests/test_story_progress_ui.py` counts address matches dynamically so added USA Plasma flags do not invalidate the GUI test.
- `README.md` already contained the mainline Plasma description, and Japanese `practice/toolkit.py` already had the matching v0.11.17 version labels. Both files are intentionally retained from the Japanese branch. None of the live-tested Japanese unlocks, warps, freezes, Story Progress edits or named checkpoints are changed by this reconciliation.

## Verification and merge gate

The Japanese branch's **195 backend + 94 GUI Windows suite** and all user-tested Japanese functions passed **before** this merge. The original Plasma work passed mainline tests in its own branch. The newly combined tree has **not yet been tested**. PR scope is much broader than the 93 files shown against #17's immediate base because the Japanese branch contains hundreds of decomp/toolkit commits. Review all incoming code paths before final merge to `main`.

For the combined candidate:

```powershell
.\scripts\test_japan_party.ps1
py -3 -m unittest tests.test_plasma_conditions tests.test_story_progress tests.test_story_progress_ui -v
```

No GitHub Actions or ROM/savestate assets are added. Sasuke battery mapping remains deferred.
