# Repository branches — handoff guide (2026-11-14)

## Active development

**`chatgptweb/decomp` is the single integration branch** for the up-to-date Goemon Practice Toolkit. Start changes here, or use a disposable local worktree based on its current HEAD. Integrate reviewed changes back here promptly; do not create a permanent branch for each feature.

The latest integration branch includes native Linux existing-PID access, right-click Live Memory field rename and freeze/unfreeze, a UI-independent 100 Hz freeze worker, current scene controls, and Automatic events damage-event capture. Do not rebuild the toolkit from older branch snapshots.

**`main` is currently stale and diverged**, not the toolkit release baseline. Synchronizing or replacing it requires an explicit, separately reviewed decision; avoid blind merges or force pushes.

## Existing research branches

These are **not alternative toolkit baselines**:
- `codex/ebisumaru-mini-research`: independent Ebisumaru movement/transform investigation; preserve its unmerged findings.
- `codex/goemon-impact-research`: Impact HUD/battle research and evidence; preserve its unmerged findings.
- Other `codex/*` branches: audit against integration before deciding to archive or delete.

The following toolkit topic branches are older than, or mainly superseded by, `chatgptweb/decomp`: `chatgptweb/toolkit-decomp-insights`, `chatgptweb/decomp-linux-integration`, `chatgptweb/toolkit-linux-native`, `chatgptweb/impact-value-search`. The last two have divergence, so inspect their unique commits before deleting. No branch deletion is authorized by this note.

## New agent checklist

1. Fetch branch heads and compare with `chatgptweb/decomp`; avoid using old commit counts as live truth.
2. Read `AGENTS.md`, `PROGRESS.md` and this handoff before editing.
3. Develop against the newest integration HEAD and keep unrelated research commits untouched.
4. Add synthetic tests, record exactly what was executed, update `PROGRESS.md` in the same commit, then publish atomically with a branch-head lease.
5. Promote evidence from research branches with explicit scope and review; never discard independent commits or rewrite active branches without the user's instruction.

The branch relationships recorded here are a point-in-time map, not proof that every experimental branch is safe to delete.
