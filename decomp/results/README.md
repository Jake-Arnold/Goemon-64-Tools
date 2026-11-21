# Decomp G2 results and retention policy

This directory contains the published canonical verifier/inventory checkpoint, dated original-ROM G2 promotion reports, and earlier reproducibility snapshots. A later G2 report does **not** make an older original proof redundant: it records a different source fingerprint, accepted set, relocation environment and failure/acceptance history.

## Audited 21 November 2026

- **27** `combined*.json` reports (including `combined.json`), and **27** `inventory*.json` reports (including `inventory.json`): **54 files, 29,811,651 bytes** in the authenticated uploaded checkout matched to `chatgptweb/decomp` commit `553bc85e4f6e3a9be08b8e85c01768a82ad646be`.
- **No two of the 54 files are byte-identical** (SHA-256), and **none are semantically identical** after parsing JSON and canonical sorting of keys. Do not delete any based only on an old numeric checkpoint or apparent naming similarity.
- The default canonical `combined.json`/`inventory.json` remains a genuine **USA 1,956** original-ROM snapshot. The later 1,965 USA and 2,123 Japan functions are proven by additional original-ROM/ELF/relocation/inventory reports; see [active continuation](../CONTINUE.md).
- At least one archived proof is referenced directly by a regression test (for example `combined_1723_pre_isolated233_20261120.json` in `tests/test_decomp_batch.py`). Other snapshots retain provenance, so deleting them safely would require a per-file dependency and unique-evidence audit. None has been deleted in this cleanup.

**Retention rule:** keep distinct proof artifacts, original hash and original-address mapping ledgers, failure reports and source provenance. If future work proposes deduplication, prove exact file or JSON semantic identity first; verify references in tests, source, reports and Git history; preserve the oldest relevant source/proof hashes and original region; only then consider removal in a separate reviewed PR. Never replace immutable G2 evidence with an inferred count.
