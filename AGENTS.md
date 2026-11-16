# Development instructions for automated contributors

Project: Goemon 64 speedrunning/practice toolkit (Windows Python and portable C core).

1. For **every change**, update root `PROGRESS.md` with date, summary, reason, tests, limitations and next step. Include `PROGRESS.md` in the same Git commit as implementation changes.
2. Push each completed commit to the connected GitHub repository `Jake-Arnold/Goemon-64-Tools`; check the remote commit SHA and report truthfully. If credentials/network/repository access are unavailable, provide the local commit or patch and explicitly say that the push did not occur. Do not simulate a push.
3. Maintain or expand Python and portable C tests. Execute appropriate tests before commits; distinguish mock-RAM tests from in-game verification.
4. Treat N64 scene loading, game state, map pointers and character pointers as unsafe until the engine's native transition path is understood. Do not enable raw warp shortcuts based only on apparent map-ID changes.
5. Do not commit ROMs, copyrighted game assets, saves, per-user routes, diagnostics containing personal information, credentials, or raw game memory dumps. Respect `.gitignore`.
6. Preserve existing Python module organisation, autosplitter code and portable C prototypes unless a change explicitly requires restructuring.
7. Continue from v0.9.9 as the imported baseline; no claim of a successful direct warp is supported.

## Decomp continuation

For native matching-C work, start with [decomp/CONTINUE.md](decomp/CONTINUE.md).
It is the operational runbook; older checkpoints and result reports retain
historical evidence and must not be treated as current instructions/counts.

## Mandatory version increments

Every user-facing toolkit change must increment the patch component of `practice/version.py` (e.g. 0.11.17 → 0.11.18), even if the change is experimental. Update the first README heading and document the version in PROGRESS.md in the same change. The Tk window title and header must always import `DISPLAY_VERSION` from `practice/version.py`, never embed a separate hard-coded release number. Extend release regression tests when changing version behavior. Do not describe experimental emulator/native backend support as live-verified until the user's actual Linux game has been tested.
