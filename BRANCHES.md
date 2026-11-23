# Goemon repository branch policy — authoritative

**Read this before editing, creating a PR, merging, or running an agent.** This repository has two independent, long-lived development baselines. GitHub has one default branch; the default is a convenience, not an authorization to mix the codebases.

| Workstream | Canonical base / PR destination | Topic branches |
| --- | --- | --- |
| Toolkit UI, practice controls, memory editor, debugger, Windows/Linux runtime, USA/Japan attachment, releases | `stable/toolkit` | `toolkit/<short-purpose>` |
| Original-ROM matching C, MIPS/ABI analysis, USA/Japan decomp, compiler research, exact-ROM verification | `stable/decomp` | `decomp/<short-purpose>` |

**Do not create bare `toolkit` or `decomp` branches.** Git cannot store `toolkit` alongside `toolkit/feature`, or `decomp` alongside `decomp/feature`. The `stable/` prefix is deliberate.

### Agent preflight — mandatory

1. Classify the request as **toolkit** or **decomp**, before editing; if truly cross-cutting, split into two separately scoped changes and explicit reviewed metadata transfer.
2. Fetch the **live GitHub** refs and open PRs; never trust a Project ZIP, old `PROGRESS.md`, historical branch, stored handoff, or the default GitHub checkout as the newest authority.
3. Start from the correct `stable/*` ref, verify `git status --short`, `git branch --show-current`, `git fetch origin`, and live commit SHA. Refuse to push when base moved; revalidate proof/test gates. Never force-push shared branches.
4. Make a short-lived `toolkit/*` or `decomp/*` topic branch and target only its corresponding stable branch. Use PRs; merge verified changes, then delete the **reviewed** topic branch. A former branch name is never a valid destination merely because it appears in old docs.
5. **Never merge full toolkit and decomp histories into each other.** Transfer reviewed address discoveries through the existing metadata-only import workflow; changing runtime memory writes requires toolkit-specific review. Decomp native proof is independent.
6. Toolkit: follow the toolkit regression/live verification policy. Decomp: follow `decomp/CONTINUE.md`, the autonomous skill, and exact original-ROM/ELF/relocation/inventory/full-local-CI gates. Research findings, staged proof and native promotion have distinct statuses.
7. Include `PROGRESS.md` in the same commit as changes; preserve historical results accurately and report exactly which checks ran.

### Clone / worktrees

```bash
# Toolkit
git clone --branch stable/toolkit --single-branch https://github.com/Jake-Arnold/Goemon-64-Tools.git goemon-toolkit
# Decomp — use a separate checkout
git clone --branch stable/decomp --single-branch https://github.com/Jake-Arnold/Goemon-64-Tools.git goemon-decomp
```

Create topics after fetching the appropriate base: `git switch -c toolkit/my-feature origin/stable/toolkit` or `git switch -c decomp/my-research origin/stable/decomp`. Update refs by `git pull --ff-only`; do not switch a dirty working tree.

### Legacy refs and existing work

`main` and `chatgptweb/decomp` are **legacy aliases/snapshots**, not new work destinations. Never delete them until default-branch migration, open PR retargeting, automation migration, and reference checks finish. Old research and branch names are historical evidence, not instructions. Preserve unmerged evidence, original source hashes, and PR discussions. Existing open PRs created before this policy may keep their original head name, but must target the corresponding `stable/*` base after review.

### Operational limitation

GitHub defaults to `stable/toolkit`. For decomp work, fetch and select `stable/decomp` explicitly. Check the live repository rules before merging.

For unattended sessions and ChatGPT Project instructions, use this policy as the entry point. On the live decomp checkout, follow `decomp/CONTINUE.md`, `.agents/skills/goemon-autonomous-decomp/SKILL.md`, and `decomp/plans/EXECUTOR_PROTOCOL.md`. Read `decomp/COMPILER_QUIRKS.md` before each native IDO attempt, record the outcome and reproduction evidence even for negative attempts, and run the full native proof gates before promotion. Refresh any copied prompt against these files at the start of every session.

The scheduled toolkit address import reads the published address manifest from `stable/decomp` and proposes a metadata-only `toolkit/*` PR against `stable/toolkit`. Windows release automation publishes from `stable/toolkit`. Keep the historical refs while [issue #175](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/175) tracks agent and branch retirement.

### Source archives for ChatGPT Project sessions

Resolve the current stable ref to its full commit SHA using GitHub. Find a successful **Goemon source archive** workflow run for that branch and SHA. Download its `goemon-source-stable-decomp-<sha>` or `goemon-source-stable-toolkit-<sha>` artifact with the GitHub connector's **Download workflow artifact** action. Check `COMMIT.txt` against the live SHA and verify `source.tar.gz` against `SHA256SUMS`. Extract to an empty directory with safe tar extraction. The inner tar preserves executable bits and Git symlinks. It contains tracked source at the workflow commit. Git history and native build inputs are separate.

Every push to either stable branch publishes an artifact. If the current artifact is missing or expired, dispatch **Goemon source archive** on that stable branch, wait for the run to succeed, and check its SHA again. Never substitute an artifact from a previous commit. For Goemon matching-C promotions, fetch and verify a fresh artifact before each attempt and verify publication again after the merged promotion.
