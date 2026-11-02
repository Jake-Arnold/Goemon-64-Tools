# Goemon discovery and companion implementation plan

Date: 2026-11-02. Status: phase 1 and bounded persistent-event phase 2/3 recorder
implemented in source; actual labelled gameplay experiments and later phases remain.
Continue in the existing `codex/goemon-discovery` task workspace.
Baseline: `91b387853f900a5222c2a9c145d6ac08c9c6cc98`.

## Outcome and current evidence

Build a companion that shares an evidence-backed description of original US
Goemon state across Project64, Goemon64Recomp and a future decompiled build.
Automate address discovery and function analysis incrementally toward full
decompilation. A useful companion does not depend on completing decompilation.

Project64 connection, map/resources and changing player coordinates have been
verified read-only on one live 8 MiB configuration. That does not verify every
flag, other ROM revisions, writes, scene loading or checkpoint restoration.
The toolkit already captures A/B/C snapshots and ranks individual comparisons;
it does not yet combine repeated experiments or maintain structured evidence.

## 1. Enable existing unsafe tools by default

Owner: Codex implementation and automated checks; user observes game behavior.

- Make teleport, logical checkpoint restore, native debug-menu access, hex editing
  and the Live Memory UNSAFE checkbox enabled on ordinary startup. This also makes
  the existing experimental reload control available without separately checking
  UNSAFE. Enabling a control must not execute it or write memory on startup.
- Use one argument/default policy for `python -m practice.toolkit`, Run.bat and
  the packaged entry point. Preserve existing positive flags for compatibility.
- Add explicit `--read-only` mode that takes precedence over enable flags,
  opens a read-only process handle, disables all write/input actions, and starts
  UNSAFE unchecked. Its precedence must survive the packaged launcher's defaults.
- Keep existing address/width checks, compare-before-write, masked-bit
  preservation and readback. Existing action confirmation behavior is unchanged;
  changing defaults does not require adding new confirmation dialogs.
- The legacy `--enable-scene-warp` prototype is disabled code, not a functional
  unsafe option. Do not revive its known-broken exit-flag shortcut. Correct native
  transitions require the loader research in phase 5. Existing experimental
  0x0C reload stays explicitly labelled as having unverified spawn semantics.
- Update launcher copy, help, README and version labels together when released.

Acceptance: all ordinary entry points expose the same enabled tools; read-only
mode overrides all write opt-ins; no startup, connect or poll writes occur.
Tests: startup/argument precedence, GUI defaults and disabled controls, mocked
write rejection in read-only mode, and existing memory-edit regression tests.
Live validation: restart the exact candidate, connect on each available host,
verify defaults and read-only behavior; report unavailable hosts explicitly.
Do not claim Project64 warp/restore support from connection-only evidence.

## 2. Record repeatable discovery sessions

Owner: Codex builds capture/analysis; user performs labelled gameplay events.

- Add sessions and trials to State discovery: baseline/idle samples, A before,
  B after, optional C reverted, event label and an independent repeat.
- Start with persistent event bits at `0x8015C608..0x8015C66B`. First targets:
  Benkei's initial conversation and separate Ushiwaka start, fish hand-in and
  final reward/dialogue stages. Include an item-only control so inventory edits
  do not masquerade as story completion.
- Use a user-controlled reset to the same pre-event state for one-time events;
  do not automatically restore logical checkpoints as an experimental baseline.
  Existing checkpoints do not reproduce all script/actor state.
- Capture backend, ROM identity/status, map, character, pointers, timestamps and
  coherence checks. Invalidate interrupted, partial or context-mismatched trials.
  Resolve pointers afresh and compare dynamic structures by relative offset only
  when their identity/context permits it. Never silently compare unrelated actors.
- Move large reads/analysis off Tk's thread. Support cancellation and disconnect;
  a failed read must not leave a trial looking complete. Multi-read captures are
  not atomic: check context before/after and label remaining timing uncertainty.

Acceptance: record and reopen multiple trials with context intact; interrupted
or cross-scene captures cannot become apparently valid event comparisons.
Tests: partial reads, pointer relocation, disconnect/cancel, context changes and
GUI responsiveness with representative data. Capture remains read-only even
when the rest of the toolkit starts with unsafe controls enabled.

## 3. Combine evidence and rank candidates

Owner: Codex implements deterministic analysis; user supplies repeat/control data.

- Intersect repeated changes at bit granularity; track set and clear directions
  separately, repeat counts and idle/control overlap. Retain conflicting evidence.
- Display exact supporting and contradicting trials. Noise overlap reduces
  priority but never silently erases the underlying observation.
- Support irreversible A/B events separately from reversible A/B/C effects.
  No automatic promotion from changed byte to named or causally verified flag.
- Aggregate complete comparison data, not the current UI's truncated candidate
  list. Keep deterministic ordering and export schema versioning.

Acceptance: synthetic fixtures with a real event bit, noisy timer, conflicting
trial and inventory-only change produce explainable rankings; repeated live
captures produce a shortlist with evidence links, not a claim of new semantics.

## 4. Introduce a shared address/evidence registry

Owner: Codex owns schema/adapters; user validates game-facing labels.

Contract: versioned records contain stable ID, ROM hash/revision applicability,
guest address or pointer-chain/relative offset, width, signedness/type, canonical
big-endian interpretation, mask, scope/lifetime, backend observations, semantic
description, source references and evidence status. Separate observational,
code-traced and write-tested evidence; preserve contradictions and provenance.
Do not represent a heuristic score as a statistical probability.

- Seed existing mappings without upgrading their documented confidence.
- Add an adapter so Live Memory and discovery can consume records while existing
  module organization and autosplitter/portable C interfaces remain stable.
- Store local trials under the existing ignored diagnostics directory. Reuse
  `practice_data_dir()` for packaged data. Raw RAM, ROMs, saves and user routes
  never enter commits. Publish only reviewed semantic records and synthetic data.
- Migrate custom watches additively: preserve names and values, retain backups,
  keep custom watches distinct from confirmed mappings. Unknown/new schema
  versions fail clearly without overwriting existing local files.

Acceptance: the same semantic watch resolves on both available backends;
ROM/backend applicability is visible; unsupported identities remain unverified;
old watches remain usable and no user data is lost.
Tests: schema validation/version rejection, masks, pointer lifetimes, migration
round trips, guest byte-order parity and source/packaged storage paths.

## 5. Trace code and establish a decompilation pipeline

Owner: Codex performs source/tooling analysis; user supplies gameplay checkpoints
and verifies reconstructed behavior. Upstream contributions require a separately
reviewed patch; do not automatically publish to other maintainers.

- Inspect the current upstream `klorfmorf/mnsg` layout, symbols, license and build
  instructions; pin a commit and verify the supplied ROM identity before setup.
  Build locally and establish a reproducible baseline before editing functions.
- For shortlisted flags, inspect static readers/writers and original MIPS code.
  Check the installed Project64 debugger's actual tracing facilities before
  choosing an integration; log instruction/function context where supported.
- Correlate quest scripts, callbacks and flag accesses. Distinguish completion
  markers, item ownership and event triggers. A final cutscene bit is not itself
  the function that starts the cutscene.
- Generate candidate C functions, compile with the pinned toolchain and compare
  machine code against original functions. Track matching coverage separately
  from semantic understanding and runtime validation; no full-decomp ETA yet.
- Investigate native transition ordering, entrance parameters, actor setup and
  character loading before implementing a dependable warp path.

Acceptance: reproducible baseline build; one targeted routine traced to a
documented candidate; reconstructed functions have explicit match results and
known limitations. Raw disassembly/generated game data remain local as required.

## Delivery, validation and non-goals

Implement phases 1, 2/3 and 4 as separate reviewable increments, then begin phase
5 using the first useful shortlist. Each completed change includes PROGRESS.md,
appropriate tests, a descriptive commit and a push to Jake-Arnold/Goemon-64-Tools.
Verify the remote commit SHA and distinguish feature-branch pushes from merges.
Do not leave completed changes only in a local commit.

Run focused tests while developing and the full Python suite before each
functional delivery. Rebuild/retest portable C when shared contracts change.
Keep synthetic-RAM, Windows GUI, build/matching and actual in-game evidence
separate. Validate the exact packaged artifact before claiming its release.

Out of scope for the first milestone: complete flag coverage, automatic game
playthrough, blind unknown-memory writes, bulk RAM restoration, every emulator
or ROM version, a new UI architecture and a completed full decompilation.

Phase 5 now has an initial read-only original-ROM/script trace and numeric
reference-index command (see ROM_FLAG_TRACE.md). Known Benkei/Ushiwaka checks and
script writes are traced; native minigame result writers, actor loading, complete
CFG reconstruction and a matching decompilation baseline are not complete. A
local external-label index is a research aid, not the phase 4 shared GUI registry.
Immediate next action: validate the naturally occurring failed-training state,
then use the traced evidence to build the registry and expand writer coverage.
The first phase 2/3 implementation
captures only 100 global event bytes plus bounded context checks, synchronously;
analysis runs off Tk. Wide/dynamic captures and automatic ROM verification are
deferred rather than claimed complete. Packaged executable build and host checks
must be reported separately from automated validation.
