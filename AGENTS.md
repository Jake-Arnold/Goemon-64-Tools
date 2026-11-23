# Development instructions for automated contributors

## LEGACY DECOMP REF — DO NOT PUBLISH HERE (23 Nov 2026)

This branch (`chatgptweb/decomp`) is retained for old links and historical evidence. **All new matching-C, ROM/MIPS research and native promotions must start from `stable/decomp`**, using `decomp/<purpose>` topic branches and PR base `stable/decomp`. Toolkit development is independent: `stable/toolkit`, `toolkit/*`. Do not use default `main`, stale ZIPs or prior chat prompts as branch-selection authority. Read `BRANCHES.md` and the *live* `stable/decomp` `AGENTS.md` / `CONTINUE.md` / skills. Never merge entire codebases, force-push or promote from stale proof.


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
`chatgptweb/decomp`, current issues/PRs and original-address ownership
before decomp work. Registry metadata is never native G2 proof; all function
promotions still require original-ROM, ELF, relocations, strict inventory and
full CI. Update `PROGRESS.md` in the same commit.


1. For **every change**, update root `PROGRESS.md` with date, summary, reason, tests, limitations and next step. Include `PROGRESS.md` in the same Git commit as implementation changes.
2. Push each completed commit to the connected GitHub repository `Jake-Arnold/Goemon-64-Tools`; check the remote commit SHA and report truthfully. If credentials/network/repository access are unavailable, provide the local commit or patch and explicitly say that the push did not occur. Do not simulate a push.
3. Maintain or expand Python and portable C tests. Execute appropriate tests before commits; distinguish mock-RAM tests from in-game verification.
4. Treat N64 scene loading, game state, map pointers and character pointers as unsafe until the engine's native transition path is understood. Do not enable raw warp shortcuts based only on apparent map-ID changes.
5. Do not commit ROMs, copyrighted game assets, saves, per-user routes, diagnostics containing personal information, credentials, or raw game memory dumps. Respect `.gitignore`.
6. Preserve existing Python module organisation, autosplitter code and portable C prototypes unless a change explicitly requires restructuring.
7. The initial v0.9.9 imported-baseline work did not establish direct warps. Later native-warp and story-flag work on `main` superseded that historical limitation (user confirmation 2026-11-08). The decomp-only branch must not revisit or modify those features without separate authorization.

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
original-ROM G2, and full local CI remain independent.

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
Keep `decomp/*` research separate from `main`-based toolkit PRs.

## Compiler quirk knowledge base (mandatory for matching-C work)

Maintain [decomp/COMPILER_QUIRKS.md](decomp/COMPILER_QUIRKS.md) as a cumulative, reusable IDO/MIPS matching-C knowledge base. During every native matching attempt, record any **new, reproducible compiler/code-generation quirk** discovered, including unsuccessful experiments that clarify a constraint. Check existing entries before trying variants; deduplicate and improve earlier entries instead of appending repeated folklore. For each entry capture: region, original function and ROM offset/VMA; compiler version and exact flags; minimal C reproducer or source reference; observed versus expected MIPS/ABI, registers, stack, branches, padding or relocations; exact successful workaround or known failure; verification scope (isolated/native/combined G2); evidence paths and commands; and confidence/limitations. Distinguish empirically verified behavior from hypotheses, and note whether a quirk is portable across functions or region-specific. Do not include copyrighted original ROM/ASM dumps or proprietary binaries. Include knowledge-base updates **in the same next implementation/research commit** as the discovery, with root `PROGRESS.md` updated as required; never delay or discard the finding merely because its candidate failed promotion. This documentation does not relax any native or full-ROM acceptance gate.

## Decomp continuation

For autonomous end-to-end matching-C discovery and promotion in ChatGPT or Codex, begin with [goemon-autonomous-decomp](.agents/skills/goemon-autonomous-decomp/SKILL.md); for shell/GitHub connector access mismatches use [goemon-github-source-bridge](.agents/skills/goemon-github-source-bridge/SKILL.md). These coordinate existing narrow skills and never override native proof gates.

For native matching-C work, start with [decomp/CONTINUE.md](decomp/CONTINUE.md).
It is the operational runbook; older checkpoints and result reports retain
historical evidence and must not be treated as current instructions/counts.

## Codex project skills

Use narrow repo-local skills in [.agents/skills/](.agents/skills/README.md). Use `python3 -m decomp.skill_context --status` for the published canonical proof/inventory snapshot; it does not build a ROM. Historical G64 execution records remain research evidence, not an active 100-task scheduler.

## Local decomp CI (no GitHub Actions)

Use `python3 -m decomp.local_ci` from any directory in the checkout for the ROM-free local decomp regression gate. It runs both decomp Python suites, cross-validates canonical proof and inventory, and runs a GCC/Clang-compatible ASan/UBSan display-emitter host regression. `python3 -m decomp.local_ci --quick` skips the C sanitizer fixture when diagnosing Python-only failures; it is not the full local gate. These commands require no `.github/workflows`, Docker, GitHub Actions, or proprietary ROM. **Do not use a workflow-based Local CI runner for this repository.** Run additional task-specific host/sanitizer checks as necessary and record actual outcomes. This local gate is **not** original-address native IDO equality or a fresh full-ROM G2; those remain mandatory and separate for production C promotions.

## Decomp target selection (current)

The G64-001–100 execution plan was closed on 14 November 2026 and is retired from active scheduling. Choose work from the current remaining-assembly inventory, live `decomp/CONTINUE.md`, unpromoted native evidence and verified source ownership. Follow [decomp/plans/EXECUTOR_PROTOCOL.md](decomp/plans/EXECUTOR_PROTOCOL.md) for bounded attempts and mandatory full-ROM G2 acceptance. Historical G64 research ledgers remain available in `decomp/plans/execution/`; do not infer current blockers or matching-C counts from those old task statuses.


## Atomic canonical decomp promotion transaction — mandatory (22 November 2026)

An agent must not publish a Git commit or claim `PUBLISHED_REMOTE_VERIFIED` using only a dated `results/*g2*.json` or research-source ZIP. During cross-agent work **the canonical manifest and `combined.json`/`inventory.json` are the only accepted-C count**; staging C code, isolated native match or an alternate integrated ROM proof creates no accepted count.

1. Fetch live `chatgptweb/decomp` HEAD and compare every candidate identity `(region, original ROM offset, VMA, original code size)` against **the entire current canonical function ownership graph** and all pending research manifests. Deduplicate by original ROM address and range, not filename or previous staged count. Record exclusions and source/byte hashes.
2. Pin the exact parent commit and predecessor canonical manifest, proof and inventory hashes. If HEAD moves or new accepted C overlaps, **abort and rebase/reverify**. Never use stale local C counts as an acceptance basis; no history rewriting or force-push.
3. After original IDO, complete 32 MiB ROM, all ELF identities and semantic relocations pass, run strict inventory and **full** `python3 -m decomp.local_ci`; it now includes `python3 -m decomp.promotion_integrity --validate`. This compares **both names and bytes** of every canonical C claim against the complete ROM proof and strict inventory, refusing any unpromoted staged result.
4. Publish **one complete promotion commit** on `chatgptweb/decomp` containing native sources/adapter, canonical `decomp/manifest.json`, `decomp/results/combined.json`, `decomp/results/inventory.json`, dated G2/inventory evidence, tests, `PROGRESS.md`, and `decomp/CONTINUE.md`. Preserve previous canonical proofs separately. If any required file is absent, the work stays `RESEARCH_ONLY`; do not claim a new official count.
5. Use a GitHub atomic tree/commit + expected-HEAD lease (`update_ref(expected_sha=<pinned-base>)`) and **re-fetch** the remote manifest/proof/inventory. A report of success requires the remote count to equal the locally verified count and all CI gates to be documented. Follow-up agents must read that authoritative HEAD first.

Implementation/source: `decomp/promotion_integrity.py`, `decomp/test_promotion_integrity.py`, and the frozen `decomp.usa_canonical_reconcile108` stage. Local CI is a ROM-free consistency check; it **does not replace** native/whole-ROM verification.
