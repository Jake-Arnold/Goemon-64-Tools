# USA/Japan toolkit architecture audit — 18 November 2026

## Verdict

**One desktop application with two distinct regional backends, not two
separately launched applications.** Both game selections run the same toolkit
entrypoint, construct a single Tk root and Toolkit class, and retain the
same notebook, Unlocks, Story Progress, Live Memory, Discovery and Scene
Browser UI objects when the selected region changes.

**Not yet one region-agnostic runtime engine.** ROM verification, process
attachment, scene semantics, memory layouts, write eligibility, checkpoint
operations and dashboard snapshots differ by retail game. Those differences
remain explicit until independently verified. Full USA/Japan feature parity
has not been demonstrated.

## Before this change

| Layer | Existing architecture | Assessment |
| --- | --- | --- |
| Entry point | goemon_app.py → practice.toolkit.main → Toolkit | One application |
| Pages | One notebook, shared Unlocks, StoryProgress, Inspector, EventSessions mixins | Shared UI |
| Flag records | flags_for_region(region), one schema with region-qualified addresses | Shared schema |
| Flag sampling | read_flag_bytes, one 100-byte guest-memory read | Already batched |
| Flag writes | USA write_story_value; Japan checked write_japan_crosswalk_flag | Separate, safety-critical adapters |
| ROM identity | Exact region-specific retail SHA-1 and code verification | Correct region separation |
| Connection | USA Rdram/process discovery; Japan ROM-code-probe validated connection | Different backend adapters |
| Polling | One tick loop formerly inspected mem and jp_rdram independently | Potential inactive-reader leakage |
| Japanese legacy panel | Built but hidden; its data feed other pages | Legacy duplication |
| Capability boolean | Japan live_memory_supported=False despite working Japanese read-only pages | Overloaded; also gates USA checkpoint operations |

## Changes in v0.11.53

1. **One virtual flag renderer.** VirtualFlagList creates only enough actual
   ttk Off/On button rows and header controls to cover the viewport. The
   logical list can contain hundreds of flags without creating a widget
   for every flag. The one outer scrollbar, named sections and search remain.
2. **One active-region session.** RegionSession exposes the selected ROM's
   active guest-RAM reader, PID and backend. It contains no writer and
   never translates an address. Inactive-region reader handles cannot
   drive the shared flag page or reader-change scheduling.
3. **One selected-region tick policy.** Toolkit.tick gates region-specific
   polling by the currently active RegionSession, even if an inactive
   backend handle remains in memory. Backend-specific extraction remains
   separate because game memory contracts differ.
4. **Same-instance parity tests.** Switching USA ↔ Japan retains the
   shared notebook and virtual flag view; flag addresses and read state
   are reconstructed for the new ROM.
5. **No new game-memory writes.** Checked masked-bit writers, original
   evidence labels and permissions are unchanged.

## v0.11.54 follow-up: user-visible parity audit

| Feature | Divergence found | v0.11.54 decision |
| --- | --- | --- |
| Open debug menu | USA checked normal gameplay/player pointer; Japan accepted every state | **Fixed:** both only request exact byte 0x0A at verified region-specific engine address; no selected scene or automatic warp |
| Native current-scene display | JP rendered 0xHHH/label from its Live Memory refresh; USA rendered decimal/hex/label only from its Live Memory refresh | **Fixed:** shared RegionSession read, same label and visible-Scene-Browser polling; no player snapshot |
| Scene list | JP excluded local original-USA atlas-only rooms while USA included them | **Unified list**, but a label in an atlas is not proof that an experimental JP reload can safely enter it |
| Character selector | JP defaulted to Keep current; USA defaulted to Goemon and forced a character change | **Fixed:** same five options/default, explicit optional character override in the USA backend |
| Legacy USA debug selection | A second entry point staged post-load entrance placement while claiming merely to open the debug menu | **Fixed:** aliases the same manual 0x0A command; no pending warp object |
| ROM capability flag | JP had live_memory_supported=False despite functioning guest-RAM Live Memory | **Clarified:** both support verified guest-RAM reads; legacy boolean describes USA logical checkpoint semantics |
| Custom watches | USA/JP store custom records differently and certain rename paths reference only USA watches | **Outstanding:** migrate persistence and edit actions to one region-aware custom-watch repository |
| Story Progress edit | USA directly edits flags, JP marks many research rows read-only even though Unlocks explicitly exposes guarded candidate toggles | **Outstanding:** unify UI policy only after mapping identical row identities; retain provenance and bit-write guards |
| Scene instant reload | USA requires actor snapshots for entrance/spawn staging; JP reads global state but also rejects non-normal gameplay | **Outstanding:** no safe proof for starting 0x0C in Impact, so do not bypass the guards |
| Logical checkpoints & native states | USA logical RAM checkpoints versus emulator-owned full states available to both | **Intentional:** game and emulator contract differs; do not misrepresent one as the other |
| Process attachment | Japan performs exact ROM/code-probe verification and backend-specific write revalidation; USA uses a distinct discovery path | **Intentional until refactored:** identical user-facing Connect command must not bypass separate executable verification |

## v0.11.55 — Pointer-independent double-click reload

A shared source-globals check now allows experimental 0x0C staged scene
reloads from observed Impact battle submode 4 in USA and Japan without
demanding ordinary gameplay player/task pointers. The selected region still
provides its own explicitly mapped engine, scene, character, loading,
submode, exit and pending-entrance addresses.

USA recovers the destination actor after transition through the existing
guarded one-shot SpawnPlacement instead of using any stale source pointer.
Japan native recomp retains independent ROM/PID/RDRAM verification but
accepts an absent ordinary player during Impact.

This does not prove Impact teardown is compatible with an injected 0x0C
request. Debug-menu 0x0A is separate and is never treated as a direct
destination reload. No unsupported non-gameplay states are enabled.

## v0.11.56 — User-requested submode 5 trial

Japanese Impact screenshot showed `engine=0x0D, scene=0x223,
loading=0, submode=5, exit=0`. The shared `0x0C` double-click
reload's former submode 0–4 allowlist was an avoidable behaviour
restriction, not an established memory-layout difference. The
shared source guard now accepts an arbitrary u8 submode on
both versions, but still requires engine 0x0D, plausible scene,
loading=0, exit=0 and a resolved character. The change does not
alter debug-menu `0x0A`, ROM/PID/write validation or guarded
post-load placement. Native success is not established by
synthetic tests and forcing a boss-fight reload remains experimental.

## Remaining architectural debt

- Toolkit remains a large class with separate USA and Japan connection
  workers and dashboard snapshots. This is a maintainability concern, not
  evidence that two GUI applications are being run.
- Japan's player/task, warp and USA-specific checkpoint/god-mode
  capabilities are not equivalent or all independently validated.
- The old live_memory_supported boolean should become a granular
  capability model (guest reads, checkpoints, task-pointer operations,
  scene writes, native input). Do not simply change it to True.
- A future stable backend protocol should cover identify, attach,
  read_guest, sample_dashboard, capabilities and guarded writes while
  preserving separately verified adapters and regional addresses.
- The hidden legacy Japanese panel should eventually be removed after
  its useful probes are migrated behind shared views.

## Verification and limits

- Isolated Tk/Xvfb tests passed with 450 logical flags, viewport recycling,
  direct Off/On actions, read-only controls, filtering and region-slot reset.
- Isolated active-session tests passed with both USA and Japanese readers
  present to ensure only the selected reader is returned.
- An isolated 2,000-row Tk/Xvfb benchmark used 16 pooled row/header slots;
  logical setup was approximately 0.05 s, and 75 scroll updates approximately
  0.26 s on the execution host. These are not real Ubuntu/Wine in-app results.
- Full toolkit integration tests and live USA/Japan emulator tests remain
  outstanding; passing isolated tests does not establish release readiness.
