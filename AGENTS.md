# Development instructions for automated contributors

Project: Goemon 64 speedrunning/practice toolkit (Windows Python and portable C core).

1. For **every change**, update root `PROGRESS.md` with date, summary, reason, tests, limitations and next step. Include `PROGRESS.md` in the same Git commit as implementation changes.
2. Push each completed commit to the connected GitHub repository `Jake-Arnold/Goemon-64-Tools`; check the remote commit SHA and report truthfully. If credentials/network/repository access are unavailable, provide the local commit or patch and explicitly say that the push did not occur. Do not simulate a push.
3. Maintain or expand Python and portable C tests. Execute appropriate tests before commits; distinguish mock-RAM tests from in-game verification.
4. Treat N64 scene loading, game state, map pointers and character pointers as unsafe until the engine's native transition path is understood. Do not enable raw warp shortcuts based only on apparent map-ID changes.
5. Do not commit ROMs, copyrighted game assets, saves, per-user routes, diagnostics containing personal information, credentials, or raw game memory dumps. Respect `.gitignore`.
6. Preserve existing Python module organisation, autosplitter code and portable C prototypes unless a change explicitly requires restructuring.
7. The initial v0.9.9 imported-baseline work did not establish direct warps. Later native-warp and story-flag work on `main` superseded that historical limitation (user confirmation 2026-11-08). The decomp-only branch must not revisit or modify those features without separate authorization.

## Mandatory USA ↔ Japan memory crosswalk

When any agent discovers or validates a **fixed original-USA or Japan-0
guest-RAM global, packed story flag, inventory field or other static
game-data address**, it MUST immediately record the candidate for the
*other* regional ROM in the same task. Start with the local
[USA/Japan crosswalk playbook](decomp/USA_JAPAN_MEMORY_CROSSWALK_PLAYBOOK.md)
and [.agents/skills/goemon-region-crosswalk/SKILL.md](.agents/skills/goemon-region-crosswalk/SKILL.md).
Check known pairings/exceptions first. For **classified static data only**,
`JP = USA + 0x57F0` and `USA = JP - 0x57F0`, producing an **unverified
candidate**, never an automatic field promotion. Annotate field width,
endianness, saved-event mask, ROM identity, original MIPS evidence,
target independent validation, conflicts and ownership.

Do not apply the delta to VM, player/task pointers, dynamic Impact
controller, overlays or code addresses. Preserve known Snowflake
`+0x57F1` exception, disputed JP pause `0x800CD2D6` and unverified
JP battery `0x80161DF9 & 0x20`. A raw A/B changed byte is not proof
of semantics. Keep research on a `decomp/*` branch and port only a
reviewed mapping to a separate `main`-based toolkit PR.

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
