# Goemon toolkit branch workflow

**Current canonical toolkit branch: `stable/toolkit`.** Decomplication and original-ROM matching-C work belong on `stable/decomp`, not in this toolkit branch.

See the authoritative [BRANCHES.md](../BRANCHES.md) for the full agent preflight, two-workstream table, topic branch naming, Git limitations, legacy redirects, and separate checkout commands.

```bash
git fetch origin
git switch -c toolkit/my-feature origin/stable/toolkit
# Make scoped changes, update PROGRESS.md, run toolkit tests.
# Open a PR with base stable/toolkit; delete the topic branch only after merge and review.
```

The `main` branch is a legacy snapshot/previous default, not the source for new toolkit features. Do not merge the entire decomp history into toolkit. Only reviewed metadata-only address imports may cross from decomp, and they grant no new runtime write authority. Confirm the default branch and server-side protections separately on GitHub.
