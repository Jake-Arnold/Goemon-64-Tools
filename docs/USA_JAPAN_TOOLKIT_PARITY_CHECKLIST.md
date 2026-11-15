# USA ↔ Japan Toolkit feature parity checklist

**Audit:** 2026-11-15. **Comparison:** current USA integration branch `chatgptweb/decomp` versus Japan-0 feature branch `chatgptweb/japan-controlled-party-writes` (a descendant of the integration branch, 20 commits ahead when audited).

## Status vocabulary

- **USA implemented:** code exists in the integration baseline, not a claim that every experiment works safely in every scene.
- **JP available:** code is reachable for the selected Japanese ROM and PID. Hardware/emulator validation is noted separately.
- **JP partial:** only a narrower read-only or separately guarded capability is available.
- **JP absent:** the corresponding USA tab is intentionally disabled; showing the Tk widget alone is **not** functional porting.
- **Verified:** distinguish (a) sourced game cheat, (b) synthetic unit test, (c) user-recorded live RAM transitions, (d) successful end-to-end toolkit test. Do not conflate these.

### Existing tabs and controls

| # | Current USA tab / feature | USA implementation | Japan-0 status in current branch | JP parity work / acceptance check |
|---|---|---|---|---|
| 1 | **Dashboard — connection** | USA Recomp / Project64 RAM attach, live XYZ, speed, character, action and loading | **Partial.** Exact Japan-0 ROM verify, independently validated Mupen64Plus attach (Linux user-tested) and Windows Project64.exe attach (4/8 MiB implemented, live test pending). Same raw guest reader, custom watches, Value Search and A/B/C; JP XYZ/speed/action still unavailable. | [ ] Region-aware connection backend; [ ] independent Japan pointer/task/XYZ/action mapping; [ ] trace normal gameplay, title, menus, load screens and Impact. Never route JP RDRAM through the USA memory parser. |
| 2 | **Dashboard — full emulator savestates** | Mupen64Plus/Project64 F5/F7 via verified process and visible window, slots 0–9; separate from logical checkpoints | **Shared emulator-owned save/load requests; Japan PJ64 live test pending.** Project64 or Mupen PID is verified before F5/F7 command; connected Japan backend mismatches are rejected. Completion is not guaranteed by the toolkit. | [ ] Live X11 test save/load; [ ] reattach on load and invalidate all field baselines, pointers, pending writes/freezes, scan caches; [ ] verify selected PID and ROM identity, avoid claiming automatic completion. |
| 3 | **Dashboard — logical checkpoints** | USA-only capture/restore includes position, character, map, resources and story fields; legacy position bookmarks | **Absent.** Controls hidden; Japan pointer/map/inventory semantics insufficient for safe restoration. | [ ] JP capture schema with provenance; [ ] read-only preview; [ ] require live-valid player/task and destination; [ ] only later add scene/character-aware restore with actual replay tests. |
| 4 | **Unlocks** | USA 34 named toggles/levels/counts, one-click mapped unlock all | **Partial, separate Japan tab.** Published JP party/item/weapon/fish/map flag leads readable. **Only** Sasuke (0x80161E97) and Yae (0x80161E9B) can be set 0→1 through independently opted-in, confirmed one-shot writes. UI not yet live-tested. | [ ] Build JP-specific names/widths/allowed values from gameplay; [ ] map other party and upgrades; [ ] compare before/after UI; [ ] guarded per-item write proof, then (last) bulk unlock. Do not assume four repeated cheat slots correspond to specific characters without verification. |
| 5 | **Story progress** | USA grouped categories, including Fortune Dolls, Benkei/Kihachi, Ushiwaka, keys, collectibles, annotations, diagnostics; read and individual edit | **Absent.** No Japanese save/event bitfield mapping. Japanese guides document 45 Fortune Dolls (40 silver, 5 gold), not their RAM offsets. | [ ] Identify JP save/event banks; [ ] capture repeatable pickup/dialogue deltas; [ ] map each doll and counters; [ ] keep history and labels region-scoped; [ ] do not add flag writers before validation. |
| 6 | **Live memory** | USA watched fields and custom watches, filter, log/export, raw editor, right-click rename/freeze, persistent custom names | **Partial, user live-tested in Windows/PJ64.** Japan Live has 58 cheat fields, 10 scene probes and now region-scoped typed custom watches with persisted names, live raw/decoded values and baseline compare. No direct reuse of USA Live Memory tab/editor/freeze. | [ ] Shared read-only watch UI with region-selected definitions, widths, endian, validation and alias namespace; [ ] arbitrary JP guest address watches and exports; [ ] keep raw write/freeze unavailable until per-field permissions exist; [ ] confirm menu/title polling without a player. |
| 7 | **Scene browser / entrance atlas / reload** | USA scene catalogue, ROM entrance atlas, native debug-menu call, experimental double-click reload and placement | **Absent tab; partial read-only evidence.** JP Live exposes observed current, previous and pending scene probes; USA-derived scene names are *not* confirmed Japanese names. | [ ] Validate JP stage IDs/names and original entrance data; [ ] read-only scene transitions first; [ ] independently identify JP loader and position pointers; [ ] native debug-menu tests; [ ] scene reload last, in savestate-isolated experiments. |
| 8 | **Native menu calibration** | USA original debug-menu read-only watches, calibration and candidate ranking | **Absent.** JP debug-mode guest address is externally sourced (0x800CD284), but USA menu selection/cursor/watch offsets must not be reused. | [ ] Capture Japan-native debug-menu transitions; [ ] discover menu highlight/pointer fields across scenes; [ ] versioned calibration records and raw proof; [ ] no forced spawn or automatic warp until validated. |
| 9 | **Character cursor scan** | USA character cursor captures and candidate scanner | **Absent.** JP character index 0x80161DCC is confirmed 0=Goemon and 1=Ebisumaru in both switch directions. Sasuke 2 and Yae 3 remain hypotheses until real C-Down switch traces. | [ ] Confirm Sasuke/Yae identity + normal model/controls + read-only index after party unlock; [ ] map actual JP cursor/menu state separately; [ ] avoid writing index to fabricate character switches. |
| 10 | **Value freezes** | USA independent 100 Hz freezer, God Mode, enemy pass-through, raw/field freeze actions | **Absent.** One-shot JP party writes are not a general freeze system. | [ ] Port read-only freeze-candidate diagnostics first; [ ] design strict JP address/width/range allowlist and handle lifetime; [ ] pause on PID/ROM/base/scene changes and savestate loads; [ ] only enable validated, explicitly allowed writes with tested precedence over game engine. |
| 11 | **Value search** | USA focused/wide value scanning and repeat comparisons | **User live-tested in Windows/PJ64 on 2026-11-15.** Screenshot: decreasing `u16` search, 5 snapshots, 1 surviving candidate at `0x80161DDA` (`93`, `0x005D`); scan-to-custom-watch produced `95`/`0x005F` at another instant. The same Value Search tab is enabled in Japan mode and uses the verified JP 4/8 MiB RDRAM extent with a worker; Watch selected creates a Japan-only read-only custom watch. | [ ] Region-neutral scanner over bounded JP 8 MiB with chunking and time limits; [ ] u8/u16/u32 and float endian-aware filters; [ ] changed/unchanged/increased/decreased; [ ] candidate-to-watch; [ ] no write requirement or guessed semantics. |
| 12 | **Automatic events** | USA health-decrement-triggered damage recorder, about 25 Hz, pre/post ring buffer and ranked candidates | **Absent.** JP current-HP guest byte is a published cheat lead but trigger behaviour and event contexts still need end-to-end confirmation. | [ ] Validate JP health decrement; [ ] region-neutral recorder/snapshots; [ ] support no-player periods; [ ] time-stamped correlation export and repeated trials. |
| 13 | **Event sessions → Event flag sessions** | USA A/B/C trials of 100-byte saved-event bank, idle/control/event evidence and candidate rankings | **Absent.** JP fixed-field baseline/compare is simpler and not an equivalent event-bank trial system. | [ ] Map JP saved-event bank(s) first; [ ] region-identified A/B/C and provenance; [ ] repeated control experiments; [ ] preserve uncertain labels and export raw observations. |
| 14 | **Event sessions → Advanced RAM comparison** | USA read-only A/B/C focused/wide probe, no-player support, XOR report, watch selected | **Implemented in JP code; tests and live validation pending.** Existing Event Sessions Advanced subtab now supports Japan-only focused 2×4 KiB and full 8 MiB A/B/C captures, bounded ranking, session checks, JSON export and candidate→JP watch. USA Event flag sessions remains disabled for Japan. | [ ] Reuse generic scanner to capture arbitrary JP ranges with bounded 8 MiB reads; [ ] same-PID/ROM/base/endian snapshots; [ ] A/B/C filters and JSON export; [ ] promote candidates into JP Live watch list, not verified mappings. |
| 15 | **Japan Live / Party Test** | **No USA equivalent dedicated tab.** USA has richer integrated tools listed above. | **Available in code, partially live-validated.** 58 cheat leads + 10 candidate/observed scene fields; real user confirmed some scene/character deltas. Two allowlisted, opted-in party write buttons; UI tests still outstanding after syntax correction. | [ ] Run full Japan synthetic and Tk tests; [ ] live Sasuke/Yae normal switches; [ ] migrate generic watches into shared Live memory/Unlocks/Events without losing evidence badges or unsafe-write isolation. |

**Actual UI gating:** `Toolkit._apply_game_version_ui` disables every non-Dashboard, non-`Japan Live / Party Test` tab when Japan is selected. There is **no current Japanese parity** for tabs merely because the same tab classes exist in the Python package. `practice/game_versions.py` marks Japanese `live_memory_supported=False` to prevent USA-only methods being invoked; changing it to True alone would be dangerous.

## Field-level starting inventory and uncertainty

- **Japan-0 confirmed through actual user traces:** RDRAM attach, raw changing 68-field display, index 0 ↔ 1 for Goemon/Ebisumaru, stable endpoint transitions 300→355 and 352→354; current/previous/pending scene globals, one submode change.
- **Japan-0 source-backed, not automatically gameplay-verified:** 58 watch fields from published Japanese GameShark and TCRF addresses. Category breakdown: vitals/currency, party, weapon/ability repeated slots, items/fish/treasures, map access/stops, bonus/debug modes and raw time counter.
- **Japan-0 limited write evidence:** the user independently confirmed Sasuke/Yae flags via Cheat Engine; the newly coded toolkit writer itself has not passed live emulator validation. Neither Sasuke=2 nor Yae=3 is confirmed by normal C-Down trace yet.
- **Japan-0 hypotheses:** other scene/transition/loading/paused candidates; actor/player/task pointers, XYZ/action/velocity, save-event bank, Fortune Doll flags, entrance table and script VM remain unmapped.
- **Separate concern:** native Japanese Goemon64Recomp boot/play is not implemented. It is not a prerequisite for read-only Japanese Mupen tools.

## First parity implementation milestone — 2026-11-15

- Commits: `6cc7d76` (region-selected Value Search reader), `d183393` (Japan tab and disconnect gating), `5b596cb` (persistent JP custom watches), `b8ae73e` (new regression tests), `3eef60a` (runner integration), `e67c33c` (test isolation). The new GUI/runtime tests have **not yet been executed** here.
- New protocol and exact Ubuntu reproduction steps: [`docs/JAPAN_READONLY_VALUE_SEARCH.md`](JAPAN_READONLY_VALUE_SEARCH.md).
- User reports prior Japan party-writing tests passed and Sasuke/Yae buttons worked in the live emulator. No claim yet on normal-switch index values or new search/watch feature success.

### Advanced RAM Comparison checkpoint (same date)

- `3c3851f` adds `practice/japan_state_comparison.py` (JP-only scene/character context, arbitrary focused/full-RDRAM snapshot, 1,200-row max candidate shortlist, no bulk RAM export).
- `a23d6cf` and `cfef2cb` bring Japan experiment names and async A/B/C capture to the existing Advanced tab. `4914796` enables **only** Advanced RAM Comparison within Japan Event Sessions, not the USA 100-byte saved-event tab.
- `420ab9f` / `edd3b70` require a distinct reader-session token to prevent A/B/C comparisons across otherwise identical PID/base/endian reconnects; `1415d59` adds A/B/C sequence gate and region-labelled export names.
- New synthetic and Tk tests, plus an expanded parity regression script, are **authored but not yet executed here**; do not mark A/B/C runtime-verified. Details: [`JAPAN_READONLY_VALUE_SEARCH.md`](JAPAN_READONLY_VALUE_SEARCH.md).

### Windows Project64 live evidence — 2026-11-15

- [x] User reports passing Windows PowerShell regression suite and operating Project64 with the Japanese toolkit.
- [x] User screenshot: `u32` custom Japanese Goemon index `0x80161DCC=0`, matching the built-in field.
- [x] User screenshots: Ryo-like `u16` field `0x80161DDA` read via Value Search and promoted Japan Live watch; 5-snapshot Decreased filter yields one candidate at `93`, custom watch displays `95` at a separate instant.
- [x] User screenshot: Scene / boss investigation context identifies Oedo Town South, prior South Oedo Goemon's House, and Goemon index; respect per-field `UNVERIFIED` labels.
- [x] User screenshot: **focused** A/B/C comparison, **2 regions**, **22 raw byte changes**, **2 reversible shortlisted candidates**: `0x80161DCF` `00→01` (XOR `01`), `0x80161DBD` `0B→09` (XOR `02`), both `C matched A=yes`. Neither has an established event-flag meaning.
- [ ] **Wide** A/B/C session, savestate restore, normal character switch and exact Project64 PID/base/mapping size still require separate evidence.
- Detailed screenshot transcription and evidence tiers: [`JAPAN_PROJECT64_LIVE_SCREENSHOT_EVIDENCE_2026-11-15.md`](JAPAN_PROJECT64_LIVE_SCREENSHOT_EVIDENCE_2026-11-15.md). Original PNG attachments are in the conversation, not repository binary artifacts.

### Windows Project64 3.0 checkpoint — 2026-11-15

- [x] Implement verified Japanese `Project64.exe` PID discovery on Windows using the existing Win32 process-reader backend and three separate exact Japan-0 ROM code probes; ensure wrong kind, mismatched code and stale/ambiguous bases fail closed.
- [x] Support either unexpanded **4 MiB** or expanded **8 MiB** PJ64 RDRAM where process memory is readable; bound Japanese raw guest accesses, Value Search and Wide A/B/C captures by verified size, without modifying USA Recomp/Project64 behaviour.
- [x] Reuse the two existing separately opted-in Sasuke/Yae one-byte party writes on PJ64 with per-write confirmation, same PID/ROM/base/size revalidation and a short-lived process writer. Never write the character index.
- [x] Add synthetic 4/8 MiB attach, process kind, byte-order, mismatch and guarded-write tests to PowerShell/Bash suites.
- [ ] Execute the expanded suite **on Windows**, attach to real Project64 3.0 with the Japanese ROM, compare a changing Ryo/character watch and validate native savestate restore; Linux Mupen results do not substitute for this.
- [ ] Confirm Project64 window hotkeys and game actor state after normal C-Down. **Implementation code is pushed but Windows PJ64 runtime remains unverified.**
- See [`JAPAN_PROJECT64_WINDOWS.md`](JAPAN_PROJECT64_WINDOWS.md) for the full clone, configuration, smoke tests, optional fixed RDRAM address and recovery.

## Ordered delivery checklist

### Phase A — reliability and architecture (P0)
- [x] Keep USA toolkit integration as ancestry of Japan branch (verified in Git compare during this audit: Japan branch 20 commits ahead of `chatgptweb/decomp`).
- [x] Fix `practice/japanese_fields_ui.py` import-blocking extra parenthesis, commit `0bd9979`.
- [x] User reports prior Sasuke/Yae party tests pass and toolkit unlock buttons work on live Mupen. [ ] Execute the newly expanded Japan read-only parity suite and record output; retain synthetic/live distinction.
- [ ] Verify native Mupen save/load and reconnection; do not reuse handles or snapshots across loads.
- [ ] Define a `RegionProfile` / `MemorySession` contract: exact game identity, PID, RDRAM map+endian, read-only capability, structured field definitions, optional scoped permitted actions, evidence level and persistence namespace.
- [ ] Add per-feature gates: `can_read_raw`, `can_scan`, `can_write_party`, `can_read_player`, `can_modify_scene`, etc. Avoid one broad `live_memory_supported` switch.

### Phase B — maximum parity without RAM writes (P1)
- [x] JP typed custom watches, persistence isolation and baseline compare **implemented in code**. [ ] Live validation, full same-tab USA-style field management and export remain outstanding.
- [x] JP bounded Value Search over verified 8 MiB RDRAM and promote selected candidate to Japan-only watch **implemented in code**; [ ] execute fresh tests and live Mupen scan.
- [x] JP Advanced RAM Comparison A/B/C with 2×4 KiB focused / 8 MiB full ranges, async snapshot reads, source-tagged candidates and bounded exports **implemented in code**. [ ] New tests and live emulator validation.
- [ ] Region-scoped JSON session exports, alias names and ROM fingerprints.
- [ ] Bring 58 known JP fields into common watch model, preserving external evidence badges.

### Phase C — gameplay semantics (P2)
- [ ] Complete native Sasuke and Yae index tests and restore initial savestate.
- [ ] Map JP player/task pointers, XYZ, action, loading and validated scene names/entrances.
- [ ] Region-specific Event Sessions with independently mapped saved-event ranges.
- [ ] JP damage event recorder using confirmed health changes.
- [ ] Map and verify 45 Fortune Doll entries and other story flags.

### Phase D — controlled actions (P3)
- [ ] Port JP Unlocks one independently confirmed field at a time with bounded one-shot writes.
- [ ] Add JP native menu calibration and entrance atlas, validate scene load in emulator.
- [ ] Port guarded logical checkpoints and safe stage reload only after live end-to-end validation.
- [ ] Consider specific freeze/god-mode writers only after proved semantics, foreground opt-in and savestate rollback tests.
- [ ] Keep Japanese native recomp project as separately tracked effort.

## Potential USA improvements discovered through this cross-region review

- [ ] **Use the Japan read-only attachment strategy for USA Mupen64Plus.** USA `connect()` currently selects an existing Mupen PID for savestates but reports unsupported RAM layout; verified region-specific ROM signatures + RDRAM attach could give USA Mupen the same memory access as Japan (without touching the established USA Recomp/Project64 path).
- [ ] **Share fast read-only generic scans across both regions.** No known player pointer should be required for live watches, full-RAM diffs or scene tracing; this improves Impact, loading, title and boss observations in USA.
- [ ] **Promote Japan Live's one-click Capture baseline / Compare / Copy changes into common Live Memory**, and pair with existing USA A/B/C experiments; make raw capture easy without conflating candidate addresses with proof.
- [ ] **Move write authorization from whole tabs to per-field capability rules**, with explicit region/revision, allowed values, size/endian, transaction readback and worker pause. Existing USA `checked_write` and JP party write guards can inform the common API; do not lower safety to match another region.
- [ ] **Keep watch names, value freezes, event sessions and checkpoints separated by ROM revision and session identity** so saved USA addresses never silently appear in Japan.
- [ ] **Correlate shared item and party data layouts with independent regional evidence** to audit slot naming, word packing and masks. A repeated regional offset may generate *research candidates* but never automatically authorizes a watch or write.
- [ ] **Make unavailability explicit per feature** instead of disabling the entire Japan notebook; grey out only actions lacking a verified backend, and distinguish read-only features from safe writes.

## Required verification before checking a parity box

1. Unit tests of decoding, bounds, endian, identity, failure isolation and permission gates using synthetic guest RAM.
2. Tk smoke tests asserting the correct tabs/actions are enabled for USA vs Japan, with no USA writer accessible from Japan.
3. Same-process live Japan Mupen testing including a scene transition, normal character swap and savestate restore. Record ROM SHA-1, PID/base/endian and exact before/after guest bytes; label anecdotes vs repeatable runs.
4. Regression tests of full existing USA behaviour (Recomp/Project64), including no-player contexts and disconnection.
5. Update `PROGRESS.md` and this checklist after each milestone. Commit and push after small testable changes, keep experimental PRs draft until verified, and never represent monitoring automations as ongoing code development.

**Sources in repository:** `practice/toolkit.py`, `practice/ui_extension.py`, `practice/game_versions.py`, `practice/japanese_fields.py`, `practice/japanese_scene_probes.py`, `practice/japanese_party_unlock.py`, `practice/emulator_savestates.py`, `practice/*_ui.py`, `docs/JAPAN_DEVELOPMENT_ROADMAP.md`, `docs/JAPAN_RUNTIME_CHARACTER_TRACE_002.md`, and `PROGRESS.md`.
