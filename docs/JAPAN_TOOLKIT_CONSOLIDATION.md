# Japanese toolkit consolidation (integration checkpoint)

Source: chatgptweb/japan-controlled-party-writes (PR #17), incorporating toolkit changes from PRs #2–3, #9, #11 and #13–17. The independent PR #10 RAM prototype is not yet reconciled.

85 toolkit implementation, tests, documentation and runtime-evidence files have been transferred to a new branch based directly on chatgptweb/decomp. Japanese recompilation research from PRs #4–8 is intentionally excluded. Existing decomp/ and PROGRESS.md on the target are preserved.

## Merge gates (NOT COMPLETE)
- Run compileall and complete USA/Japan unit/Tk regression suites on Linux and Windows.
- Validate Japan scene-browser double-click performs immediate scene-to-scene warp rather than only opening the original debug menu.
- Verify USA scene navigation, save/load, custom watches, freezes, event sessions and checkpoints.
- Reconcile PR #10 scanner if it contains distinct improvements.
- Update PROGRESS.md and README after validation.
- Do not merge this branch into decomp or close older PRs until these gates pass.

This is a staging branch, not a validated release.
