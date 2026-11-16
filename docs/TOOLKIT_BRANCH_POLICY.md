# Goemon repository branch workflow

## Permanent branches

- **`main`** is the canonical, stable USA/Japan Goemon Practice Toolkit. It
  contains toolkit v0.11.27, the current Linux and regional backends, and the
  full committed 888-entry original-USA entrance atlas.
- **`chatgptweb/decomp`** is the existing long-lived decompilation baseline.
  The decomp project, function promotion, original-ROM equivalence and research
  verification remain separate from routine toolkit changes.

There is **no separate permanent toolkit branch**. PR #27 merged
`chatgptweb/toolkit-unified` into `main` on 16 November 2026 at
`7d808a5b36b4efd1078894a8798bdc59fee1b85e`.

## New toolkit features and fixes

Branch from **`main`**:

```bash
git fetch origin
git switch main
git pull --ff-only
git switch -c toolkit/my-feature
```

Commit the change and its tests to `toolkit/my-feature`; open a PR with
base **`main`**. After review, run the Linux/Windows regression suites
and relevant live game checks, merge the PR back into main, then retire the
temporary feature branch.

Toolkit UI, scene-warp coordinates, memory attachment, mapped write controls,
checkpoints, launcher and the shared USA/Japan backends belong here. Maintain
`practice/version.py`, README and PROGRESS for user-facing toolkit changes.

## Decompilation observations and function promotion

Start from the **existing** `chatgptweb/decomp` branch, not `main`:

```bash
git fetch origin
git switch --track origin/chatgptweb/decomp
git switch -c decomp/my-research
```

If the local decomp branch already exists, use
`git switch chatgptweb/decomp` and `git pull --ff-only` instead of
`git switch --track`.

Use short-lived `decomp/*` feature branches for MIPS traces, ROM/symbol
comparisons, C-match candidates and research observations. PRs target
**`chatgptweb/decomp`**. Review independently matched functions and
promote only after strict full-ROM/codegen/relocation and inventory checks;
keep exploratory findings labelled research until that proof is available.

The active decomp integration PR is #26, targeting `chatgptweb/decomp`.
Existing research PRs #23 and #24 also target that same branch. Do not
rename or delete that baseline without first retargeting open PRs and
updating scheduled monitoring jobs.

## Important separation

Do **not** repeatedly merge the entire long-lived decomp branch into
`main`, or all of `main` into `chatgptweb/decomp`: each contains
different intended work and accumulated history. Port a particular
reviewed toolkit/decomp integration change deliberately when it becomes
necessary, with scope-specific tests.

The previous branches `chatgptweb/toolkit-unified`,
`chatgptweb/japan-native-recomp-toolkit-v01118`,
`chatgptweb/japan-toolkit-consolidation`, and
`chatgptweb/japan-main-integration-20261116` are now historical
toolkit branches. They can be retained for traceability but are no
longer active destinations. The old toolkit integration PR #25 was
closed as superseded; PR #27 was merged. Preserve unrelated Japanese
port and decomp research until its status is resolved separately.

## Ubuntu: use the canonical toolkit

For a checkout with no uncommitted changes:

```bash
cd ~/Desktop/Goemon-64-Tools-JP-Recomp
git fetch origin
git switch main || git switch --track origin/main
git pull --ff-only
bash scripts/test_japan_party.sh
bash Run-Linux.sh
```

Before switching branches, commit or stash any local modifications.
Test results and live USA/Japan game compatibility remain separate from
the fact that GitHub accepted the v0.11.27 merge. GitHub reported no CI
status checks on PR #27 at the time of merge, so its runtime verification
remains outstanding.
