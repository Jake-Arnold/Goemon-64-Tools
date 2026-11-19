# Combined 323-C USA G2 — reconstructed-local verification (16 November 2026)

**Native 323-C G2: PASS. Original ELF 323-C inventory: PASS. Host C sanitizer: PASS. Current repository's full ROM-free CI: NOT VERIFIED. PR must remain draft.**

Using the user's uploaded original ROM, pinned upstream, native toolchain archives, archived toolkit and exact 315-stage source/verifier artifacts, a disposable local reconstruction of the 323 C trial was built. Its previous production source files have **95/95 exact SHA-256 matches** against the published verified 315-C G2 report; the only additional source is `file11_eight_callbacks.c`, SHA-256 `7919d61ac0453f342629d51186b1ddf16f3716f527b411c93716815941122d60`.

Native full build: **323/323** matching USA functions, **17,012** matching instruction bytes, 33,554,432-byte ROM byte-identical, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. The new `file_11` stage has **160 C**, **4,628 bytes**, **90 original-size C/ASM objects** all matched to pinned hashes, **8,825/8,825** semantic relocations preserved. Baseline ELF SHA-256 `83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038`; candidate ELF SHA-256 `e51ec045dfd2a562a7253cb2f4bf29e668914c2191eed0d9d4b56b8b2a3f8433`.

Original ELF inventory compared pristine upstream and full combined candidate: **7,376 original function identities**, **323 newly matching C**, **336 current unmarked including 13 upstream**, **7,040 assembly remaining**, zero positive aliases, identity hash unchanged `01f41037ac83f6e18e80c83489a18b870e4fef907c67d20a345871c7c34fe787`.

Sanitizer compilation and test passed, including 1,000 synthetic cases and additional edge cases.

**Do not confuse this local reconstruction with the exact connected PR #41 source tree.** Historical Python stage modules and previous proof files were absent from the older archived ZIP; local scratch substitutes preserved native validation constraints but have different source hashes. Full archived-snapshot CI ran (267 tests) with 2 fingerprint failures and 5 import/missing-fixture errors. Current-branch `decomp.local_ci` and the exact `review_file11_143 --candidate-file11-160` end-to-end official runner have **not** passed, and source hash/report provenance differs at the verifier level.

The complete local G2 and inventory JSONs plus logs were returned to the user as a separate downloadable evidence ZIP, not committed as canonical production results. Their SHA-256 digests and other measured values appear in `decomp/results/file11_323_reconstructed_local_proof_20261116.json`.

**Formal gate remaining:** run the untouched current GitHub PR #41 checkout's full ROM-free CI and official opt-in review runner successfully. Then separately consider production promotion. The canonical 315-C manifest and production reports remain unchanged.
