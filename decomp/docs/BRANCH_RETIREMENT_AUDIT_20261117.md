# Decomp historical branch retirement audit — 17 November 2026

**Branch:** `chatgptweb/decomp`. This is a **read-only branch-audit and research preservation report**, not evidence that any branch was deleted. The live evidence snapshot is `decomp/data/branch_retirement_audit_20261117.json`. Re-query refs before acting: branch heads and open PRs change during autonomous research.

## Current scope and protected work

At the audited snapshot the repository contained **34 live branch refs** and **five open pull requests**. The permanent refs `main` (toolkit) and `chatgptweb/decomp` (canonical matching-C) must never be deleted. Open PR head branches are protected: `chatgptweb/graphics-pose-actor-research` (#64), `chatgptweb/graphics-adjacent-c-research` (#63), `chatgptweb/rt64-model-probes` (#62), `chatgptweb/room-actor-browser` (#60), and `decomp/address-manifest-contract-20261117` (#56). PR #62 additionally depends on `chatgptweb/room-actor-browser` as its *base*. Do not delete either branch while the stacked PR is open.

PR #63's **five 284-byte source functions** are already copied into canonical `decomp/research/graphics_adjacent_20261117/` with original Git blob SHA identities, and have a fresh independent native compiler recheck. This preserves specific source research but **does not close #63 or establish that its entire branch is disposable**, and does not constitute production promotion. PR #64's **three additional 404-byte actor/pose candidates** were announced while this audit ran; their source is still on an active PR branch and was **not** included in the 41-function promotion review queue. Review independently before import or deletion.

## Six historical branch tree spot checks

Comparison used Git blob identities from branch HEAD recursive trees against the union of current `main` and `chatgptweb/decomp` recursive trees. These six branches are **diverged**, not ancestors of canonical. Each still has blobs absent from either permanent branch, including some historical sources or proof metadata:

| Old branch | Blobs not identical to a permanent-branch blob | Decision |
|---|---:|---|
| `chatgptweb/camera-reset-136-native-20261116` | 25 | Audit before deletion |
| `chatgptweb/camera-reset-343-integration-20261117` | 20 | Audit before deletion |
| `chatgptweb/decomp-file11-next8-scratch-20261116` | 31 | Audit before deletion |
| `chatgptweb/promote-47-crossregion-to-389-20261117` | 21 | Audit before deletion |
| `chatgptweb/jp-recomp-cross-region-c-research-20261116` | 25 | Audit before deletion |
| `chatgptweb/file11-transition-52-research` | 21 | Audit before deletion |

These are **conservative blob-identity checks**, not proofs that their functionality is absent from canonical: native C may have been reworked and re-promoted, yet historical standalone evidence might not have been imported byte-for-byte. The full 45-branch archive in `decomp/data/branch_snapshot_20261117.json` is historical and must not be mistaken for the live branch list.

`toolkit/rt64-model-probes` points to the same commit SHA as the active PR #62 head `chatgptweb/rt64-model-probes` at the checked snapshot. It could become a safe redundant *ref* after verifying that no independent work or consumer depends on that name. It has **not** been deleted. Never delete the PR's actual head or base while open.

## Required deletion gate

For each proposed old branch, verify its current HEAD SHA, identify all open PRs where it is head or base (including stacked PRs), and inventory branch-exclusive files and commits against the current permanent trees. Copy unique and relevant source, proof metadata and research records onto `chatgptweb/decomp` with Git blob hashes; link or close obsolete PRs while retaining their discussion. A closed PR by itself is not enough. Re-fetch the candidate ref and target refs immediately before deletion. Never delete `main`, canonical decomp, or active PR refs.

**No deletions were performed.** The connected GitHub action set provides branch create/update but no branch-delete action, and native shell Git currently cannot resolve `github.com`. Consequently this session cannot reliably delete a remote ref. Cleanup must be performed through an authorized deletion-capable GitHub UI/API or authenticated Git once branch-by-branch evidence is complete. Do not force-push refs as a substitute for deletion.

## Separate promotion-candidate bookkeeping

Newly native-exact original-address source research is registered in `decomp/data/promotion_candidates_20261117.json`: **41 USA functions, 4,108 original bytes**, split main graphics five / 284 B, file_26 fifteen / 2,508 B, file_27 twenty-one / 1,316 B. One isolated file_25 72-byte function remains explicitly blocked by an extra relocation. The old 87-function promotion registry remains empty for the *historically accepted* batch, and now links this separate queue. These 41 candidates are **not production C**. Validating original ROM slices, source blob identities and no-overlap does not replace the full combined USA ROM / ELF / inventory / CI promotion gate.
