# Branch workflow — authoritative since 23 November 2026

Read [BRANCHES.md](../BRANCHES.md) and root `AGENTS.md`. The historical instruction naming `chatgptweb/decomp` as the toolkit's integration branch was superseded and must not be used.

- Toolkit UI/Windows/Linux/runtime: `stable/toolkit` → `toolkit/<purpose>` → PR to `stable/toolkit`.
- Native matching-C/MIPS/USA-Japan decomp research: `stable/decomp` → `decomp/<purpose>` → PR to `stable/decomp`.
- `main` and `chatgptweb/decomp` are legacy refs; preserve old PRs and historical research while migrating.
- Git cannot hold bare `toolkit` alongside `toolkit/*`, or bare `decomp` alongside `decomp/*`.
- Do not merge the long-lived histories wholesale. Reviewed metadata-only imports are the cross-project route.
- Read live GitHub SHA/PRs and scope-specific proof, not stale ZIPs. Update `PROGRESS.md` in the implementation commit.
- Default branch and protections are separate server settings and must be checked independently.

```bash
git fetch origin
git switch -c decomp/my-research origin/stable/decomp
# PR base stable/decomp
```
