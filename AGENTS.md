# Development instructions for automated contributors

Project: Goemon 64 speedrunning/practice toolkit (Windows Python and portable C core).

1. For **every change**, update root `PROGRESS.md` with date, summary, reason, tests, limitations and next step. Include `PROGRESS.md` in the same Git commit as implementation changes.
2. Push each completed commit to the connected GitHub repository `Jake-Arnold/Goemon-64-Tools`; check the remote commit SHA and report truthfully. If credentials/network/repository access are unavailable, provide the local commit or patch and explicitly say that the push did not occur. Do not simulate a push.
3. Maintain or expand Python and portable C tests. Execute appropriate tests before commits; distinguish mock-RAM tests from in-game verification.
4. Treat N64 scene loading, game state, map pointers and character pointers as unsafe until the engine's native transition path is understood. Do not enable raw warp shortcuts based only on apparent map-ID changes.
5. Do not commit ROMs, copyrighted game assets, saves, per-user routes, diagnostics containing personal information, credentials, or raw game memory dumps. Respect `.gitignore`.
6. Preserve existing Python module organisation, autosplitter code and portable C prototypes unless a change explicitly requires restructuring.
7. The initial v0.9.9 imported-baseline work did not establish direct warps. Later native-warp and story-flag work on `main` superseded that historical limitation (user confirmation 2026-11-08). The decomp-only branch must not revisit or modify those features without separate authorization.

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

## Decomp continuation

For native matching-C work, start with [decomp/CONTINUE.md](decomp/CONTINUE.md).
It is the operational runbook; older checkpoints and result reports retain
historical evidence and must not be treated as current instructions/counts.

## Codex project skills

Use narrow repo-local skills in [.agents/skills/](.agents/skills/README.md). Start a G64 task with `python3 -m decomp.skill_context --task G64-NNN`, or check `--status`; request `--detail` only when needed. The helper reads checked-in results but never builds a ROM.

## Local decomp CI (no GitHub Actions)

Use `python3 -m decomp.local_ci` from any directory in the checkout for the ROM-free local decomp regression gate. It runs both decomp Python suites, validates the task/evidence ledger, and runs a GCC/Clang-compatible ASan/UBSan display-emitter host regression. `python3 -m decomp.local_ci --quick` skips the C sanitizer fixture when diagnosing Python-only failures; it is not the full local gate. These commands require no `.github/workflows`, Docker, GitHub Actions, or proprietary ROM. **Do not use a workflow-based Local CI runner for this repository.** Run additional task-specific host/sanitizer checks as necessary and record actual outcomes. This local gate is **not** original-address native IDO equality or a fresh full-ROM G2; those remain mandatory and separate for production C promotions.

## Decomp architect v2 (current)

Use [decomp/plans/EXECUTION_STRATEGY_V2.md](decomp/plans/EXECUTION_STRATEGY_V2.md) and each pending G64 task's `architect_override_v2` for priority, finite codegen budgets and task-specific stop rules. Do not restart the plan, repeat completed promotions, or relax any full-ROM verification. Task briefs include the new override.
