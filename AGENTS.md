# Development instructions for automated contributors

## REQUIRED branch selection — authoritative (23 Nov 2026)

**Toolkit:** base/PR `stable/toolkit`, topic `toolkit/<purpose>`. **Decomp:** base/PR `stable/decomp`, topic `decomp/<purpose>`. Old `main` and `chatgptweb/decomp` are legacy refs; GitHub default is not an agent's task selector. Read `BRANCHES.md` on live GitHub and the relevant runbook before edits; fetch remote SHA/open PRs and confirm current proof. Do not merge complete toolkit/decomp histories. Preserve research and old PRs. Only scope-reviewed metadata can transfer. Include `PROGRESS.md` in same commit; never force-push. This rule supersedes contradictory dated text below.


Project: Goemon 64 speedrunning/practice toolkit (Windows Python and portable C core).

## Required delivery of task-referenced scripts

When a Goemon task, issue, handoff or response references a runnable script, recorder, verifier or script kit, **upload the actual source-only script(s) or ZIP as a downloadable artifact in that same task delivery/conversation**, and link the uploaded artifact directly. A filename, hash, old conversation attachment or description alone is not delivery. Where safe and permitted, also commit the reusable source to the appropriate decomp research/task directory so a later agent can retrieve it; a GitHub link is supplemental, not a substitute for the requested upload. Include all dependencies and a minimal run command, and verify the artifact exists and can be accessed before marking the handoff ready. Never upload ROMs, copyrighted asset dumps, proprietary tools, saves, credentials or raw memory traces. If the script is unavailable or cannot safely be uploaded, explicitly flag the task as missing its script / blocked_input; do not imply the script is attached or retrievable.

## Active resumable Goemon task queue

When asked to list pending Goemon work, resume a queued task or checkpoint
research for another chat, consult [decomp/tasks/README.md](decomp/tasks/README.md),
[decomp/tasks/registry.json](decomp/tasks/registry.json) and the
[goemon-task-registry skill](.agents/skills/goemon-task-registry/SKILL.md)
before any historical G64-001–100 plans. Run
`python3 -m decomp.task_registry list` or
`python3 -m decomp.task_registry resume GQ-...` in a complete checkout.
The registry includes externally blocked, missing-source and rebase tasks;
completed tasks are excluded from the default active listing. Re-fetch live
`stable/decomp`, current issues/PRs and original-address ownership
before decomp work. Registry metadata is never native G2 proof; all function
promotions still require original-ROM, ELF, relocations, strict inventory and
full CI. Update `PROGRESS.md` in the same commit.


1. For **every change**, update root `PROGRESS.md` with date, summary, reason, tests, limitations and next step. Include `PROGRESS.md` in the same Git commit as implementation changes.
2. Push each completed commit to the connected GitHub repository `Jake-Arnold/Goemon-64-Tools`; check the remote commit SHA and report truthfully. If credentials/network/repository access are unavailable, provide the local commit or patch and explicitly say that the push did not occur. Do not simulate a push.
3. Maintain or expand Python and portable C tests. Execute appropriate tests before commits; distinguish mock-RAM tests from in-game verification.
4. Treat N64 scene loading, game state, map pointers and character pointers as unsafe until the engine's native transition path is understood. Do not enable raw warp shortcuts based only on apparent map-ID changes.
5. Do not commit ROMs, copyrighted game assets, saves, per-user routes, diagnostics containing personal information, credentials, or raw game memory dumps. Respect `.gitignore`.
6. Preserve existing Python module organisation, autosplitter code and portable C prototypes unless a change explicitly requires restructuring.
7. The initial v0.9.9 imported-baseline work did not establish direct warps. Later native-warp and story-flag work on `stable/toolkit` superseded that historical limitation (user confirmation 2026-11-08). The decomp-only branch must not revisit or modify those features without separate authorization.

## Decomp address discoveries are research metadata, not toolkit writes

When establishing a new USA/Japan fixed guest global, saved-event bit, script
VM field, original-code VMA or ROM offset, record its **observed** source,
revision, address space, width/endianness where known, evidence and confidence
in `decomp/address_discoveries_v1.json` in the same research task. Preserve
unknown widths and cross-region counterparts as null rather than inferring
a value. Do not translate script VM, overlay VMAs, host pointers or code
addresses with the saved-game `+0x57F0` heuristic.

The toolkit's reviewed `main:practice/data/address_catalogue_v1.json` is the
only authoritative guest-data address source for actual UI reads/writes.
`decomp/memory_registry.py` only consumes a local snapshot of it; it cannot
patch that file or initiate game-memory writes. Synchronisation of research
metadata into the toolkit is **not automated by this change** and always
requires a separate reviewed metadata-only toolkit PR. Decomp acceptance,
original-ROM G2, and the full ROM-free regression gate remain independent.

## Mandatory reciprocal USA ↔ Japan guest-memory discovery

Whenever any decomp agent discovers, validates or changes an original USA
or Japan-0 **fixed guest-RAM global, saved inventory field or packed event
bit**, it MUST investigate and record the candidate for the **other ROM
in the same task**. Read the
[decomp crosswalk playbook](decomp/USA_JAPAN_MEMORY_CROSSWALK_PLAYBOOK.md)
and [goemon-region-crosswalk skill](.agents/skills/goemon-region-crosswalk/SKILL.md).

For eligible fixed data and saved-game fields only, propose
`JP = USA + 0x57F0` or `USA = JP - 0x57F0`, **after** checking
explicit pairings and exceptions. Treat the counterpart as an
**unverified candidate** until independently tested. Preserve source
region/revision, guest address, width, mask, endianness, memory lifetime,
original-MIPS/gameplay evidence, the target candidate, and a concrete
confirmation experiment. A raw changed byte does not prove identity.
Never translate host process memory bases, ROM offsets, original code
addresses, dynamic player pointers, VM globals, Impact allocations or
loaded overlays using this rule.

Explicit exceptions: JP Miracle Snowflake `0x80162057` is a
`+0x57F1` mapping; JP pause `0x800CD2D6` is disputed; JP first
Sasuke battery `0x80161DF9 & 0x20` is unverified. Do not automatically
promote hypotheses into matching-C claims, RAM editors, freezes or warps.
Keep `decomp/*` research separate from `stable/toolkit`-based toolkit PRs.

## Mandatory native IDO quirks preflight and every-attempt outcome

Before **each** original-ROM native matching-C attempt, read `decomp/COMPILER_QUIRKS.md` and identify relevant previously verified behaviours. Classify the **first** original/generated mismatch (register, ABI/stack, scheduling, branch/delay slot, signedness, rodata, padding/sections, relocation or unknown) **before** variant generation. Try relevant verified workarounds using bounded controlled one-variable tests under exact original compiler flags.

For each native attempt, record exactly one of `EXISTING_QUIRK_REPRODUCED`, `EXISTING_QUIRK_NOT_APPLICABLE`, `NEW_REPRODUCIBLE_QUIRK`, or `NO_NEW_COMPILER_FINDING` in sanitized evidence and handoff. Record ledger IDs/none, exact compiler flags/version, original region/ROM offset/VMA, first original-versus-generated instruction/relocation differences, SHA-256 for each source variant, reproduction commands and failed controls. `NOT_RUN` means no native compile occurred. Deduplicate reproducible new findings and useful failed hypotheses in the central ledger and `PROGRESS.md` **in the same research/implementation commit**, even if no C promotes. Never claim quirk transfer to another function without independent reproduction; full G2 proof stays mandatory.

## Original translation-unit layout (decomp only)

Read [decomp/TRANSLATION_UNIT_LAYOUT.md](decomp/TRANSLATION_UNIT_LAYOUT.md) before selecting or regrouping native C. Distinguish inferred original translation-unit ownership from current reconstructed source/object ownership. Prefer original inferred boundaries where practical; IDO 16-byte text alignment and NOP padding are evidence, not proof. Preserve accepted matching functions and canonical counts; do not force realignment or mass regrouping. Record artificial splits and investigate original owners when layout affects matching. Consolidate one bounded inferred unit at a time, with fresh native whole-unit and full original-ROM/ELF/relocation/inventory/promotion-integrity proof and required hosted CI before publishing any source/build layout change. If any gate fails, retain the verified layout. Track historical source-layout fidelity separately from matching-C progress.

## Decomp continuation

For autonomous end-to-end matching-C discovery and promotion in ChatGPT or Codex, begin with [goemon-autonomous-decomp](.agents/skills/goemon-autonomous-decomp/SKILL.md); for shell/GitHub connector access mismatches use [goemon-github-source-bridge](.agents/skills/goemon-github-source-bridge/SKILL.md). These coordinate existing narrow skills and never override native proof gates.

For native matching-C work, start with [decomp/CONTINUE.md](decomp/CONTINUE.md).
It is the operational runbook; older checkpoints and result reports retain
historical evidence and must not be treated as current instructions/counts.

## Codex project skills

Use narrow repo-local skills in [.agents/skills/](.agents/skills/README.md). Use `python3 -m decomp.skill_context --status` for the published canonical proof/inventory snapshot; it does not build a ROM. Historical G64 execution records remain research evidence, not an active 100-task scheduler.

## ROM-free decomp CI (GitHub Actions)

The authoritative ROM-free regression gate is the GitHub Actions job **Decomp ROM-free regression** (`.github/workflows/decomp-ci.yml`), running the complete, unchanged `python3 -m decomp.local_ci` suite (never `--quick`) against the PR merge commit. A green result for the current PR revision and current base is required before merging. Record the run URL and tested SHA; if the base or head changes, refresh the merge-ref result and native proof as applicable. Local execution remains available for diagnosis and task-specific tests, but duplicating the full suite locally is unnecessary once the new job has passed and a decomp-only required status check is active. Until both are verified, retain the existing full local gate. Native IDO, exact original ROM, ELF/relocations and strict inventory remain mandatory independent private proofs; Actions does not receive ROMs or proprietary tools.

For local diagnosis, use `python3 -m decomp.local_ci` from a complete checkout; `--quick` runs only the Python checks and cannot satisfy the full regression gate. Run additional task-specific host/sanitizer tests as necessary and record actual results.

## Decomp target selection (current)

The G64-001–100 execution plan was closed on 14 November 2026 and is retired from active scheduling. Choose work from the current remaining-assembly inventory, live `decomp/CONTINUE.md`, unpromoted native evidence and verified source ownership. Follow [decomp/plans/EXECUTOR_PROTOCOL.md](decomp/plans/EXECUTOR_PROTOCOL.md) for bounded attempts and mandatory full-ROM G2 acceptance. Historical G64 research ledgers remain available in `decomp/plans/execution/`; do not infer current blockers or matching-C counts from those old task statuses.


### Source archive preflight for every promotion

Before each promotion attempt, resolve the live `stable/decomp` SHA and download a fresh matching **Goemon source archive** via the GitHub connector. Follow the checksum and extraction steps in [BRANCHES.md](BRANCHES.md). Reuse a repository-backed Git worktree for edits and publication only after verifying its base against the same SHA. If the artifact is missing or stale, dispatch the workflow on `stable/decomp` and wait for the matching artifact. Keep the attempt blocked if the live source cannot be verified.

After every successful promotion merge, confirm that the workflow published an artifact for the new `stable/decomp` SHA. If automatic publication fails, rerun or dispatch the workflow and verify the new artifact before closing the handoff. Record the archive run or artifact with the published promotion evidence. The archive carries source only. All native proof gates remain required.

## Atomic canonical decomp promotion transaction — mandatory (22 November 2026)

An agent must not publish a Git commit or claim `PUBLISHED_REMOTE_VERIFIED` using only a dated `results/*g2*.json` or research-source ZIP. During cross-agent work **the canonical manifest and `combined.json`/`inventory.json` are the only accepted-C count**; staging C code, isolated native match or an alternate integrated ROM proof creates no accepted count.

1. Fetch live `stable/decomp` HEAD and compare every candidate identity `(region, original ROM offset, VMA, original code size)` against **the entire current canonical function ownership graph** and all pending research manifests. Deduplicate by original ROM address and range, not filename or previous staged count. Record exclusions and source/byte hashes.
2. Pin the exact parent commit and predecessor canonical manifest, proof and inventory hashes. If HEAD moves or new accepted C overlaps, **abort and rebase/reverify**. Never use stale local C counts as an acceptance basis; no history rewriting or force-push.
3. After original IDO, complete 32 MiB ROM, all ELF identities and semantic relocations pass, run strict inventory, then require the **full** ROM-free regression job on the exact PR revision (see the CI policy above); the unchanged suite includes `python3 -m decomp.promotion_integrity --validate`. This compares **both names and bytes** of every canonical C claim against the complete ROM proof and strict inventory, refusing any unpromoted staged result.
4. Publish **one complete promotion commit** on `stable/decomp` containing native sources/adapter, canonical `decomp/manifest.json`, `decomp/results/combined.json`, `decomp/results/inventory.json`, dated G2/inventory evidence, tests, `PROGRESS.md`, and `decomp/CONTINUE.md`. Preserve previous canonical proofs separately. If any required file is absent, the work stays `RESEARCH_ONLY`; do not claim a new official count.
5. Use a GitHub atomic tree/commit + expected-HEAD lease (`update_ref(expected_sha=<pinned-base>)`) and **re-fetch** the remote manifest/proof/inventory. A report of success requires the remote count to equal the locally verified count and all CI gates to be documented. Follow-up agents must read that authoritative HEAD first.

Implementation/source: `decomp/promotion_integrity.py`, `decomp/test_promotion_integrity.py`, and the frozen `decomp.usa_canonical_reconcile108` stage. GitHub ROM-free CI is a consistency and regression check; it **does not replace** native/whole-ROM verification.
