# Retention-safe decomp repository cleanup audit — 21 November 2026

**Baseline:** uploaded repository ZIP, authenticated against GitHub `chatgptweb/decomp` HEAD `553bc85e4f6e3a9be08b8e85c01768a82ad646be` (21 November 2026). **Scope:** documentation handoff, original-ROM proof snapshot retention and remote branch refs. This is not a new native compilation or ROM proof.

## Active continuation vs historical content

Prior `decomp/CONTINUE.md` was **170,260 bytes / 997 lines** and contained dated promotions since 9 November, obsolete 142-C runbooks, old machine-specific `/root/` and WSL paths, and pre-18 November blocked claims contradicted by later G2 results. All exact original bytes (SHA-256 `8e171ea8f9b8466b0bc525a59928c16f92d9c5fbc0e89b04502ddc291e13d2e5`) are preserved in [the adjacent full historical runbook](../CONTINUE_HISTORY_20261121.md), retaining its original relative links. The revised [operational continuation](../CONTINUE.md) is compact, points to authentic region-specific G2 ledgers and preserves all relevant native acceptance gates. No research text is discarded.

## Verification proof snapshots: no safe duplicates to delete

A complete local digest and parsed-JSON comparison of `decomp/results/{combined*,inventory*}.json` found **27 combined proofs + 27 inventories**, **54 distinct raw SHA-256s**, **54 distinct JSON-content canonical SHA-256s**, and **29,811,651 total bytes**. Every report differs. Known test dependencies include `tests/test_decomp_batch.py`, `tests/test_decomp_archive22.py`, `tests/test_decomp_archive33.py`, and `tests/test_decomp_statecopy1.py`; removing these files would require additional proof of dispensability. **Result: zero proof snapshot deletions.** [Retention policy](../results/README.md).

## Branch refs: conservative remote read-only recheck

At the audited live ref snapshot: **18 branches** and **four open PRs** (heads of #149, #150, #144 and #132). The permanent refs `main` and `chatgptweb/decomp`, as well as every open PR head, are protected from this audit. **No remote branches were deleted.**

The **ten** non-PR historical source branches below had *diverged* commit history relative to both current `main` and `chatgptweb/decomp`; they may contain original branch-only research or unpublished code. They are **not safe for automatic deletion**:

- `codex/decomp-start`
- `decomp/archive22-1523-20261120`
- `decomp/archive33-1556-20261120`
- `decomp/archive61-1617-20261120`
- `decomp/provisional342-recovery-20261120`
- `decomp/rediscovery5-1623-20261120`
- `decomp/session-source-export-20261120`
- `decomp/session-source-transfer-20261119`
- `decomp/statecopy1-1501-20261119`
- `feature/decomp-dialogue-story-anchors-20261121`

Two inactive toolkit branches were *strict ancestors of `main`*, not divergent, and were not open PR heads: `toolkit/address-metadata-sync-44812649342` (`bff8f97702f218a235f5f9218cb7b1188460cb56`) and `toolkit/address-metadata-sync-44880333478` (`6b29ec50eb8938cc74914eebfff69ebf355ed98`). These are the only immediately plausible redundant refs, but **their deletion has not been requested or performed by this PR**; retain until current ref SHA and other consumers/tags are checked by an authorized deletion-capable workflow. Exact commit ancestry alone does not establish the absence of external branch references.

The repository's existing [SHA-leased branch-retirement mechanism](../../scripts/retire_legacy_branches.py) and [archived research retirement script](../../scripts/retire_archived_branches.py) explicitly fail closed on moved refs, open PR heads and missing preservation. Do not replace those requirements with an unconditional cleanup.

## Deletions authorized by this audit

**None of the 54 unique proofs or 18 live branches.** This change only makes the current handoff smaller, preserves all original content in a same-directory archive and adds retention guidance. Any future proof or branch deletion needs fresh live provenance, tests and independent review.
