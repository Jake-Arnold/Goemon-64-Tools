**HISTORICAL REVIEW ONLY — DO NOT MERGE DECOMP INTO `main`.** This November 2026 handoff describes a former 142-function snapshot and is not current merge authorization. Active C reconstruction remains on `chatgptweb/decomp`; preserve the independent toolkit `main` branch. See [CONTINUE.md](CONTINUE.md) and [current README](README.md).

---

# Integration handoff: chatgptweb/decomp into main

Reviewed branch head: `877312c991cdcf1d43db3a7403ceeaf04be9fb51`; main at review: `12e7699a42948fa7816b2049eaca60d2ed3f518c`. Fetch both heads again and reassess any new commits before integrating. This document and its test fixes are on a separate handoff branch; preserve concurrent work and do not force-push.

## What is already established

- Branch records 142 matching-C functions, 10,652 bytes, including six beyond the 136-function base. `results/combined.json` records a full-image match for the staged sources; this review did not independently rerun the build. A fresh uninterrupted formal verifier now completes successfully against the current source; see `results/combined.json`. Candidate probes marked unpromoted must remain so.
- The user-provided ROM and local toolchains are private; do not commit ROMs, binaries, generated assembly, raw memory or personal diagnostics.
- The old comparator test expected an assembly-only comparator and outdated VM counts. The handoff fixes it to check one promoted manifest owner and continued assembly status for the unpromoted walker. The callback test uses standard `unittest`, retaining four compiled host cases without requiring pytest.
- On WSL, `python3 -m unittest discover -s decomp -p 'test_*.py' -q` passed 81 tests. The focused comparator/callback tests passed, including all four callback cases. The decomp tests invoke Linux tooling and are not expected to work as a native Windows suite.

## Verification completed on 2026-11-10

The previously mismatched verifier hash was resolved by running the documented formal verifier, not by editing the old evidence. It reported **142/142 original-address functions matched**, 10,652 function bytes and a full **33,554,432-byte** match to SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. The fresh inventory reports 7,376 identified entries, 155 total C and 7,221 assembly entries. Windows toolkit suite: 378 tests run, 372 passed and six skipped; WSL decomp suite: 81 passed; WSL focused pipeline tests: 37 passed. No new function is promoted by this run. Sanitized fresh results are in `results/combined.json` and `results/inventory.json`; the previous independent-build record is retained as `results/independent_142_historical.json`.

## Remaining integration steps

1. Merge the handoff commit with any newer branch work, then run the full Windows toolkit and WSL decomp suites against the actual combined tree. If verifier or matching sources change, rerun the formal gate using the exact command in `CONTINUE.md`; keep old results historical. Do not bypass source-hash checks.
2. Reconcile `PROGRESS.md` and `decomp/CONTINUE.md` with current main, preserving the Plasma findings and branch research; remove the branch-only push restriction from the integrated main runbook. Review the branch change to `AGENTS.md` against the user's current instructions rather than taking it automatically.
3. Verify the resulting merge, commit `PROGRESS.md`, and push as instructed. Do not include private ROM, raw diagnostics or local generated assets.

The branch's research artifacts and host tests are not themselves new matching-C promotions. A passed host test is not a native original-address or full-ROM match. No game writes or live gameplay testing were performed in this review.
