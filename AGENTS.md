# Development instructions for automated contributors

Project: Goemon 64 speedrunning/practice toolkit (Windows Python and portable C core).

## REQUIRED: canonical branches and route check (23 November 2026)

**Toolkit base / PR target: `stable/toolkit`; only `toolkit/<topic>` feature branches.**
**Decomp base / PR target: `stable/decomp`; only `decomp/<topic>` feature branches.**
`main` and `chatgptweb/decomp` are legacy refs and are **not** new work destinations. Git forbids simultaneously using a bare `toolkit` with `toolkit/*`, or a bare `decomp` with `decomp/*`. Never infer the workstream from GitHub's default branch, an old ZIP, a dated report or a prior chat.

Read [BRANCHES.md](BRANCHES.md) first, classify the work, fetch the live target and inspect open PRs, check the branch/HEAD, then use a correctly named topic PR. Preserve legacy PR/research, never force-push, never merge toolkit/decomp histories wholesale, and require the appropriate tests plus `PROGRESS.md` in the change commit. If an older paragraph below contradicts this section, this section controls. The historical matching-C snapshot has been removed from the toolkit checkout. Use `stable/decomp` for native proof; `research/rom/` contains only retained toolkit research utilities and evidence.

1. For **every change**, update root `PROGRESS.md` with date, summary, reason, tests, limitations and next step. Include `PROGRESS.md` in the same Git commit as implementation changes.
2. Push each completed commit to the connected GitHub repository `Jake-Arnold/Goemon-64-Tools`; check the remote commit SHA and report truthfully. If credentials/network/repository access are unavailable, provide the local commit or patch and explicitly say that the push did not occur. Do not simulate a push.
3. Maintain or expand Python and portable C tests. Execute appropriate tests before commits; distinguish mock-RAM tests from in-game verification.
4. Treat N64 scene loading, game state, map pointers and character pointers as unsafe until the engine's native transition path is understood. Do not enable raw warp shortcuts based only on apparent map-ID changes.
5. Do not commit ROMs, copyrighted game assets, saves, per-user routes, diagnostics containing personal information, credentials, or raw game memory dumps. Respect `.gitignore`.
6. Preserve existing Python module organisation, process-memory backends in `practice/backends/` and portable C prototypes unless a change explicitly requires restructuring.
7. Read the live toolkit version from `practice/version.py`; historical release numbers are not branch-routing authority. Older v0.9.x instructions are historical. Scene-warp code and ROM-derived entrance data exist, but live USA/Japanese native gameplay tests must be distinguished from synthetic memory tests; do not claim unverified behaviour has passed.

## Mandatory USA ↔ Japan memory-data crosswalk for all agents

Whenever an agent discovers or changes a **fixed N64 guest-RAM global,
inventory field or persistent story-event flag in either game**, crosswalk
it **in the same task**; this is not an optional follow-up. Start with the
[evidence and procedure](docs/USA_JAPAN_MEMORY_CROSSWALK_2026-11-16.md).

1. Record original **USA NG5E-0** or **Japan retail rev-0** ROM identity,
   canonical guest address, actual type/width/endianness, packed bit mask,
   scope (fixed/static versus dynamic), context and exact source evidence.
2. Check existing explicit mappings, regional definitions, independent
   observations and exceptions before calculating anything.
3. For eligible **static globals or saved-game fields only**, propose
   `JP = USA + 0x57F0` or `USA = JP - 0x57F0`. Label a new result
   **unverified offset candidate**, even if the source is verified.
4. Record both regional addresses, mask/width, status, conflicting evidence,
   a concrete counterpart validation test and the discovery reference.
   Validate the other ROM independently (read-only A/B/control gameplay
   capture or original MIPS readers/writers). A similar value or a changing
   byte does **not** independently prove identity.
5. Explicitly exclude dynamic player/task pointers, loaded overlays, script
   VM state, Impact allocations, original code VMAs, host process addresses
   and ROM offsets from automatic arithmetic. If classification is unknown,
   use function/structure correlation instead.
6. Update the research mapping and `PROGRESS.md` on the correct feature
   branch. Never auto-promote guessed addresses to confirmed game-memory
   writes, freezes, warps or decomp symbol identities.

Known exceptions: Japanese Miracle Snowflake `0x80162057` corresponds
to USA `0x8015C866` (**+0x57F1**, not +0x57F0); proposed Japanese pause
`0x800CD2D6` is **disputed**; Japanese Sasuke battery
`0x80161DF9 & 0x20` remains **unverified**. Keep toolkit changes based
on `stable/toolkit` and original-MIPS/decomp changes based on `stable/decomp`;
never merge those unrelated histories.

## Mandatory canonical address-registry updates (toolkit and decomp agents)

The **runtime source of truth** for Goemon N64 guest addresses, field widths,
bit masks and regional counterparts is
`practice/data/address_catalogue_v1.json`, accessed through
`practice/address_registry.py`. It is not a supplementary watch-list or a
crosswalk-only report. Existing Unlocks, Story Progress, Japanese fields and
Live Memory must resolve mapped addresses from it. Do not introduce a second
hard-coded address authority in a new UI panel.

**In the same task as every newly discovered address:**

1. Record a stable ID, original game region/revision, exact guest address
   (or explicitly classify a ROM offset, code VMA, patch or host pointer),
   known width/type/mask, original reader/writer evidence, scene/lifetime,
   confidence, counterpart status, source revision and date in the appropriate
   versioned discovery manifest. Use null for genuinely unknown metadata;
   never invent an access width or semantic meaning.
2. Toolkit work updates `practice/data/address_discoveries_v1.json`.
   Matching-C/decomp research updates `decomp/address_discoveries_v1.json`
   on `stable/decomp`, not the toolkit tree. The import workflow creates
   a **metadata-only PR**; no decomp code is implicitly merged to `stable/toolkit`.
3. Run `python3 -m scripts.sync_address_catalogue --write`, then
   `python3 -m scripts.sync_address_catalogue --check`; add relevant ROM-free
   tests and update `PROGRESS.md` in the same change. Review any generated
   unknown, disputed or overlapping entries without erasing evidence.
4. Existing manually triggered Japanese crosswalk Story & event flag On/Off
   controls are intentionally **not evidence-gated**. Confidence labels
   describe the mapping rather than controlling those current tests. Newly
   downloaded registry metadata never authorizes an automatic memory write.
5. The in-app **Refresh Address Catalogue** must remain schema-validated,
   size-limited, offline-safe, nonblocking and metadata-only. Code and
   addresses fetched over the network may not be executed or promoted to
   new automatic write permissions.

Detailed contract and correction procedure:
[docs/ADDRESS_CATALOGUE_WORKFLOW.md](docs/ADDRESS_CATALOGUE_WORKFLOW.md).

### Source archive handoff

For Project sessions with shell DNS failures, use the **Goemon source archive** GitHub Actions artifact for the live stable branch SHA. Verify its commit and checksum as described in [BRANCHES.md](BRANCHES.md). Matching-C promotion work follows the live `stable/decomp` instructions for fresh archive download before every attempt and publication verification after every merge.

## Decomp continuation

For native matching-C work, start with [decomp/CONTINUE.md](https://github.com/Jake-Arnold/Goemon-64-Tools/blob/stable/decomp/decomp/CONTINUE.md).
It is the operational runbook; older checkpoints and result reports retain
historical evidence and must not be treated as current instructions/counts.

## Mandatory version increments

Every user-facing toolkit change must increment the patch component of `practice/version.py` (e.g. 0.11.17 → 0.11.18), even if the change is experimental. Update the first README heading and document the version in PROGRESS.md in the same change. The Tk window title and header must always import `DISPLAY_VERSION` from `practice/version.py`, never embed a separate hard-coded release number. Extend release regression tests when changing version behavior. Do not describe experimental emulator/native backend support as live-verified until the user's actual Linux game has been tested.
