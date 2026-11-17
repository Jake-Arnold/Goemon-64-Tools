---
name: goemon-github-source-bridge
description: "Use when Goemon repository access works via the GitHub connector but Linux git clone, network access or local checkout materialization fails."
---

# goemon-github-source-bridge

**Different processes have different network access.** The public GitHub repository may be readable through the connector while `git clone` fails DNS in the code-execution container. Avoid claiming a checkout from GitHub metadata alone.

1. Check `git ls-remote`/`git clone` from the current execution host first. Read live branch SHA from GitHub even if cloning fails. Work on `chatgptweb/decomp`; do not alter `main`.
2. If shell cloning fails, use authorized GitHub connector read actions (`fetch`, `fetch_file`, Git commit/tree/blob APIs) to enumerate and retrieve source. Prefer a supported, verifiable transfer into the actual build filesystem (for example a materialized file or a full repository archive). **Connector text replies are not automatically local files.** If no viable transfer path exists, request a user-exported fresh `git archive` ZIP; never silently build from a stale snapshot.
3. Authenticate every transferred source against its Git blob SHA and the selected remote commit/tree. Preserve file paths, names, file modes and symlinks. Reject missing files, truncation, inconsistent heads and accidental assets. Keep repository source separate from ROMs, extracted assembly and proprietary toolchains.
4. Before native verification, check all required modules, manifests, scripts and build sources are **actually present** in one local tree. If materialization remains unavailable, mark `BLOCKED_INPUT`; do not claim a full-ROM verification.
5. For remote publishing without shell `git push`, use connector Git APIs: upload exact UTF-8 or base64 blobs, build tree on the live parent tree, create commit with that parent, then `update_ref` with `expected_sha`. Confirm returned remote head, changed paths and required `PROGRESS.md` update. On races, re-fetch/rebase and revalidate instead of force pushing.

Never fabricate a transfer, commit SHA, CI result or merge. Verify each operation's actual returned status.
