# Development instructions for automated contributors

Project: Goemon 64 speedrunning/practice toolkit (Windows Python and portable C core).

## Required branch selection (read before editing)

This repository has **two long-lived development baselines**. Choose the
correct one *before making any changes*:

| Work type | Starting branch | Temporary feature branch | PR target |
| --- | --- | --- | --- |
| Toolkit UI, USA/Japan runtime, Linux launchers, practice controls, warps, autosplitter, memory tooling | `main` | `toolkit/<topic>` | `main` |
| Matching-C decomp, MIPS/ROM mapping, function discovery, research observations, relocation proofs | `chatgptweb/decomp` | `decomp/<topic>` | `chatgptweb/decomp` |

**`main` is the canonical toolkit branch** since PR #27 merged v0.11.27
on 16 November 2026. **`chatgptweb/decomp` is the separate canonical
decomp baseline**; PRs #23, #24 and #26 are based on that branch. There is
no permanently active `toolkit` integration branch. Prior branches such as
`chatgptweb/toolkit-unified`,
`chatgptweb/japan-native-recomp-toolkit-v01118`,
`chatgptweb/japan-toolkit-consolidation` and earlier regional prototypes
are historical and **must not be used as new feature branch bases**.

Before any work, inspect `git status`, `git branch --show-current` and
`git fetch origin`; verify the chosen baseline is up to date. Do not
switch/reset a working tree with uncommitted changes or force-push a
shared branch. Do not merge the entire decomp history into `main`
or the toolkit history into the decomp branch; extract only specifically
reviewed cross-project changes. Preserve research PRs and avoid treating
unpromoted matching-C functions as official production matches.

**Full runbook:** [docs/TOOLKIT_BRANCH_POLICY.md](docs/TOOLKIT_BRANCH_POLICY.md).
For decomp-specific continuation also read
[decomp/CONTINUE.md](decomp/CONTINUE.md).
On any conflict between outdated README/PROGRESS historical entries and
these branch rules, treat this section and the current branch policy as
authoritative. If the branch scheme intentionally changes, update
`AGENTS.md` and the runbook together in the same PR.

1. For **every change**, update root `PROGRESS.md` with date, summary, reason, tests, limitations and next step. Include `PROGRESS.md` in the same Git commit as implementation changes.
2. Push each completed commit to the connected GitHub repository `Jake-Arnold/Goemon-64-Tools`; check the remote commit SHA and report truthfully. If credentials/network/repository access are unavailable, provide the local commit or patch and explicitly say that the push did not occur. Do not simulate a push.
3. Maintain or expand Python and portable C tests. Execute appropriate tests before commits; distinguish mock-RAM tests from in-game verification.
4. Treat N64 scene loading, game state, map pointers and character pointers as unsafe until the engine's native transition path is understood. Do not enable raw warp shortcuts based only on apparent map-ID changes.
5. Do not commit ROMs, copyrighted game assets, saves, per-user routes, diagnostics containing personal information, credentials, or raw game memory dumps. Respect `.gitignore`.
6. Preserve existing Python module organisation, autosplitter code and portable C prototypes unless a change explicitly requires restructuring.
7. The current toolkit baseline is v0.11.27 on `main` as of 16 November 2026. Older v0.9.x instructions are historical. Scene-warp code and ROM-derived entrance data exist, but live USA/Japanese native gameplay tests must be distinguished from synthetic memory tests; do not claim unverified behaviour has passed.

## Mandatory USA ↔ Japan memory-discovery crosswalk

Whenever **any agent** discovers, validates, edits, or documents an N64 guest
RAM field in **either** Mystical Ninja Starring Goemon (USA NG5E-0) or
Ganbare Goemon: Neo Momoyama Bakufu no Odori (Japan-0), perform a
**bidirectional cross-region triage in the same task**. This includes a new
fixed global, scene state, resource field, inventory byte, or packed story
event bit. **Do not wait for a separate request.**

1. **Classify the source**: record region/ROM revision, guest address (not host
   process offset), size and big-endian interpretation, bit mask when relevant,
   scope/lifetime (persistent static vs dynamic object/overlay/code), and actual
   source evidence. Never treat a debug/code VMA or ROM offset as saved RAM.
2. **Consult explicit mappings and exceptions before arithmetic.** Read
   [the cross-region evidence and workflow](docs/USA_JAPAN_MEMORY_CROSSWALK_2026-11-16.md),
   `practice/region_memory_crosswalk.py`, and existing regional tables.
   For a **classified fixed global or saved-event bit** without a known pair,
   generate the **unverified** counterpart:
   `JP = USA + 0x57F0`; `USA = JP - 0x57F0`.
   Run `python3 scripts/crosswalk_address.py --source usa --address 0x8015C60C --mask 0x20`
   (replace region/address/mask; use `--kind static-global` or
   `--kind saved-event` when the source address is not yet registered).
3. **Preserve evidence**: label the other-region result
   `offset-candidate`, record its original field width, mask, expected value
   changes, known exceptions, scene/character context, evidence links,
   and what independent test would confirm it. Verify with read-only
   A/B/control trials and/or original regional MIPS before promotion.
4. **Never auto-port** writes, freeze targets, warps, code addresses, script
   VM globals, player/task pointers, Impact allocations or loaded overlays.
   Unknown ownership is a blocker, not permission to apply the delta.
5. **Update both discovery notes and a reviewable crosswalk record** in the
   appropriate short-lived feature branch, with tests and `PROGRESS.md`.
   Record conflicts and negative tests; do not overwrite existing verified
   mappings or infer user confirmation. Preserve the separate main/toolkit
   and decomp branch workflows above.

Existing counterexamples: JP pause `0x800CD2D6` is disputed; the Japanese
Miracle Snowflake byte is `0x80162057` (USA `0x8015C866`, **+0x57F1**);
JP `0x80161DF9 & 0x20` Sasuke battery remains unverified. **A byte change
alone does not establish the meaning of an event flag.**

## Decomp continuation

For native matching-C work, start with [decomp/CONTINUE.md](decomp/CONTINUE.md).
It is the operational runbook; older checkpoints and result reports retain
historical evidence and must not be treated as current instructions/counts.

## Mandatory version increments

Every user-facing toolkit change must increment the patch component of `practice/version.py` (e.g. 0.11.17 → 0.11.18), even if the change is experimental. Update the first README heading and document the version in PROGRESS.md in the same change. The Tk window title and header must always import `DISPLAY_VERSION` from `practice/version.py`, never embed a separate hard-coded release number. Extend release regression tests when changing version behavior. Do not describe experimental emulator/native backend support as live-verified until the user's actual Linux game has been tested.
