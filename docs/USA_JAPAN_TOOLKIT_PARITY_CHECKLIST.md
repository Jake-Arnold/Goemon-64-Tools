# USA ↔ Japan Toolkit feature parity checklist


## Immediate scene-warp correction — 2026-11-15

- **Live failure reported:** Japanese Scene Browser double-click showed the **original debug menu**, unlike USA's instant area reload.
- **Root cause found in source:** Japan was writing engine `0x0A` and waiting for debug category/keyboard-A, while USA uses pending map/entrance followed by **engine `0x0C`**.
- **Correction committed:** `practice/japan_direct_scene_reload.py` and `Toolkit.start_japan_native_scene_warp` now write Japanese pending `0x800CD490` (2 or 12 bytes) and immediately request `0x800CD284=0x0C`. Original debug button remains manual-only; no keyboard input. Optional entrance uses cached USA reference data only when uniquely determined and warns otherwise.
- **New explicit CLI:** `--enable-japan-scene-writes`; legacy `--enable-japan-debug-menu-writes` still allows the direct reload for existing setups, but does not make the original debug menu part of double-click.
- **Tests committed:** `tests.test_japan_direct_scene_reload`, revised `tests.test_japan_native_scene_controller` and exact Scene Browser double-click dispatch tests, wired into Windows/Linux parity suites. [ ] Windows suite rerun. [ ] Live Project64 inter-scene destination/footing verified.

## Latest cross-region implementation (2026-11-15; Windows rerun pending)

**Read this section as current.** The original row-by-row audit below is a historical pre-consolidation baseline, with some “absent”/“disabled” cells superseded by the changes listed here. The user requested one UI shared between both game versions, not a separate Japanese scene browser. The Japanese ROM still cannot inherit arbitrary USA task pointers, event bits or write privileges.

| Shared tab or feature | New Japan-0 implementation | Remaining validation |
| --- | --- | --- |
| Dashboard | Region-specific RDRAM process; Japanese scene, character and position values shown; remembered exact Japan ROM path reverified on each new session | Japan velocity/action/task pointers and logical checkpoints unverified |
| Scene Browser | **Same existing browser; no duplicate Japanese selector.** Double-click **immediately** stages Japan pending destination at 0x800CD490 (u16 or 12-byte reference entrance block) and requests **0x800CD284 = 0x0C** area reload in the same callback, then monitors 3 stable gameplay polls. Original debug menu 0x0A remains a separate manual button | **First real inter-scene Japanese warp not yet live confirmed.** User did verify visible debug menu opening. USA double-click/entrance path remains unchanged |
| Live Memory | **Same Live Memory tab**, reads 58 Japan cheat-backed values, 10 scene probes, 3 observed XYZ floats and isolated Japan custom watches | General Japan raw edit/freeze disabled pending mapped permissions |
| Unlocks | **Same Unlocks tab**, swaps USA editable inventory for JP source-backed read-only fields and separately gated user-confirmed Sasuke/Yae unlock controls | Other JP unlock writes not independently verified |
| Story Progress | **Same nested progress tables**, presents Japan item/map/bonus-mode candidates with addresses and evidence | JP saved-event bank and story-bit causality unknown; no USA bit editing |
| Event Sessions | Same A/B/C event/idle/control flow and ranking. Japan captures 100 user-selected source RAM bytes (default 0x80161D80); provenance stores region, address, and backend. Advanced RAM Comparison still available | These Japan bytes are candidate RAM, **not** a confirmed persistent event bank |
| Damage events | Same event recorder UI uses JP HP byte 0x80161DD7, current scene 0x800CD2A2 and character 0x80161DCC, omitting guessed USA task/object pointers | No proof of JP invulnerability/collision semantics |
| Value Search and A/B/C | Existing shared scan and wide matching, including **all candidate** JSON export separate from 200-row preview | Native Windows wide export/regression rerun pending |
| Value Freezes, checkpoint restore, native menu calibration | Existing panels retain USA-specific semantics and write gates; Japan actions cannot borrow USA raw editor, player-task or event addresses | Region-specific JP task/pointer, freeze and logical checkpoint schemas required before equivalent writes |
| ROM verification | Saved path + exact expected Japan SHA-1 in per-user config, rehash/verify file each future session; PID, host RAM and code signature revalidation unchanged | First post-upgrade remembered-path startup test in Windows pending |

**Implementation constraints:** Japan automatic warp only targets the Project64 backend in the current code; `--enable-japan-debug-menu-writes` is the explicit opt-in, and `--read-only` overrides it. The previous debug-category/stage/A-input double-click prototype was replaced after the user confirmed it **only opened the original menu**. The new 0x0C native reload writes the pending destination/optional entrance (not current map or exit flag), **exactly as the USA reload does**. It is not yet live verified; the original debug-menu opening is only evidence for the separate manual control. Files are committed, but complete new Windows PowerShell tests and first actual destination load remain outstanding.


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
| 1 | **Dashboard — connection** | USA Recomp / Project64 RAM attach, live XYZ, speed, character, action and loading | **Partial.** Exact Japan-0 ROM verify, independently validated Mupen64Plus attach (Linux user-tested) and Windows Project64.exe attach (live read-only Value Search, scene context and focused A/B/C reported/illustrated 2026-11-15; 4/8 MiB mapping size not documented). Same raw guest reader, custom watches, Value Search and A/B/C; JP XYZ/speed/action still unavailable. | [ ] Region-aware connection backend; [ ] independent Japan pointer/task/XYZ/action mapping; [ ] trace normal gameplay, title, menus, load screens and Impact. Never route JP RDRAM through the USA memory parser. |
| 2 | **Dashboard — full emulator savestates** | Mupen64Plus/Project64 F5/F7 via verified process and visible window, slots 0–9; separate from logical checkpoints | **Project64 savestate restoration user-verified (2026-11-15).** Project64 or Mupen PID is checked before F5/F7; backend mismatches are rejected. The user confirms successful restoration on Windows PJ64, although the toolkit still reports a request rather than independently confirming save completion. | [ ] Live X11 test save/load; [ ] reattach on load and invalidate all field baselines, pointers, pending writes/freezes, scan caches; [ ] verify selected PID and ROM identity, avoid claiming automatic completion. |
| 3 | **Dashboard — logical checkpoints** | USA-only capture/restore includes position, character, map, resources and story fields; legacy position bookmarks | **Absent.** Controls hidden; Japan pointer/map/inventory semantics insufficient for safe restoration. | [ ] JP capture schema with provenance; [ ] read-only preview; [ ] require live-valid player/task and destination; [ ] only later add scene/character-aware restore with actual replay tests. |
| 4 | **Unlocks** | USA 34 named toggles/levels/counts, one-click mapped unlock all | **Partial, separate Japan tab.** Published JP party/item/weapon/fish/map flag leads readable. **Only** Sasuke (0x80161E97) and Yae (0x80161E9B) can be set 0→1 through independently opted-in, confirmed one-shot writes. UI not yet live-tested. | [ ] Build JP-specific names/widths/allowed values from gameplay; [ ] map other party and upgrades; [ ] compare before/after UI; [ ] guarded per-item write proof, then (last) bulk unlock. Do not assume four repeated cheat slots correspond to specific characters without verification. |
| 5 | **Story progress** | USA grouped categories, including Fortune Dolls, Benkei/Kihachi, Ushiwaka, keys, collectibles, annotations, diagnostics; read and individual edit | **Absent.** No Japanese save/event bitfield mapping. Japanese guides document 45 Fortune Dolls (40 silver, 5 gold), not their RAM offsets. | [ ] Identify JP save/event banks; [ ] capture repeatable pickup/dialogue deltas; [ ] map each doll and counters; [ ] keep history and labels region-scoped; [ ] do not add flag writers before validation. |
| 6 | **Live memory** | USA watched fields and custom watches, filter, log/export, raw editor, right-click rename/freeze, persistent custom names | **Partial, user live-tested in Windows/PJ64.** Japan Live has 58 cheat fields, 10 scene probes and now region-scoped typed custom watches with persisted names, live raw/decoded values and baseline compare. No direct reuse of USA Live Memory tab/editor/freeze. | [ ] Shared read-only watch UI with region-selected definitions, widths, endian, validation and alias namespace; [ ] arbitrary JP guest address watches and exports; [ ] keep raw write/freeze unavailable until per-field permissions exist; [ ] confirm menu/title polling without a player. |
| 7 | **Scene browser / entrance atlas / reload** | USA scene catalogue, ROM entrance atlas, native debug-menu call, experimental double-click reload and placement | **Partial experimental native debug-menu route.** JP Live → Scene warp (debug) now offers a destination category/index hint and a separately opted-in **one-byte engine 0x0D→0x0A** menu-entry request at Japanese 0x800CD284, revalidated by ROM/PID and full gameplay context. **On-screen original menu opening is now user-verified in Windows Project64 (2026-11-15); destination selection and a full playable scene load are still pending.** No pending/current map writes. | [ ] Validate JP stage IDs/names/entrance indices; [x] user-observed read-only transitions; [x] native debug engine-entry code and synthetic Tk/controller tests authored; [x] user-confirmed Project64 debug-menu opening; [ ] native selection and playable level load; [ ] discover Japanese cursor/category and native accept/commit to make double-click one-click warp. No direct map ID writes. |
| 8 | **Native menu calibration** | USA original debug-menu read-only watches, calibration and candidate ranking | **Absent.** JP debug-mode guest address is externally sourced (0x800CD284), but USA menu selection/cursor/watch offsets must not be reused. | [ ] Capture Japan-native debug-menu transitions; [ ] discover menu highlight/pointer fields across scenes; [ ] versioned calibration records and raw proof; [ ] no forced spawn or automatic warp until validated. |
| 9 | **Character cursor scan** | USA character cursor captures and candidate scanner | **Absent.** JP character index 0x80161DCC is confirmed 0=Goemon and 1=Ebisumaru in both switch directions. Sasuke 2 and Yae 3 remain hypotheses until real C-Down switch traces. | [ ] Confirm Sasuke/Yae identity + normal model/controls + read-only index after party unlock; [ ] map actual JP cursor/menu state separately; [ ] avoid writing index to fabricate character switches. |
| 10 | **Value freezes** | USA independent 100 Hz freezer, God Mode, enemy pass-through, raw/field freeze actions | **Absent.** One-shot JP party writes are not a general freeze system. | [ ] Port read-only freeze-candidate diagnostics first; [ ] design strict JP address/width/range allowlist and handle lifetime; [ ] pause on PID/ROM/base/scene changes and savestate loads; [ ] only enable validated, explicitly allowed writes with tested precedence over game engine. |
| 11 | **Value search** | USA focused/wide value scanning and repeat comparisons | **User live-tested in Windows/PJ64 on 2026-11-15.** Screenshot: decreasing `u16` search, 5 snapshots, 1 surviving candidate at `0x80161DDA` (`93`, `0x005D`); scan-to-custom-watch produced `95`/`0x005F` at another instant. The same Value Search tab is enabled in Japan mode and uses the verified JP 4/8 MiB RDRAM extent with a worker; Watch selected creates a Japan-only read-only custom watch. | [ ] Region-neutral scanner over bounded JP 8 MiB with chunking and time limits; [ ] u8/u16/u32 and float endian-aware filters; [ ] changed/unchanged/increased/decreased; [ ] candidate-to-watch; [ ] no write requirement or guessed semantics. |
| 12 | **Automatic events** | USA health-decrement-triggered damage recorder, about 25 Hz, pre/post ring buffer and ranked candidates | **Absent.** JP current-HP guest byte is a published cheat lead but trigger behaviour and event contexts still need end-to-end confirmation. | [ ] Validate JP health decrement; [ ] region-neutral recorder/snapshots; [ ] support no-player periods; [ ] time-stamped correlation export and repeated trials. |
| 13 | **Event sessions → Event flag sessions** | USA A/B/C trials of 100-byte saved-event bank, idle/control/event evidence and candidate rankings | **Absent.** JP fixed-field baseline/compare is simpler and not an equivalent event-bank trial system. | [ ] Map JP saved-event bank(s) first; [ ] region-identified A/B/C and provenance; [ ] repeated control experiments; [ ] preserve uncertain labels and export raw observations. |
| 14 | **Event sessions → Advanced RAM comparison** | USA read-only A/B/C focused/wide probe, no-player support, XOR report, watch selected | **User-verified focused A/B/C on PJ64 (2026-11-15):** 2 compared regions, 22 raw byte changes, 2 displayed reversible candidates (`0x80161DCF`, `0x80161DBD`), both C=A; **wide capture and event meanings unverified**. Existing Event Sessions Advanced subtab now supports Japan-only focused 2×4 KiB and full 8 MiB A/B/C captures, bounded ranking, session checks, JSON export and candidate→JP watch. USA Event flag sessions remains disabled for Japan. | [ ] Reuse generic scanner to capture arbitrary JP ranges with bounded 8 MiB reads; [ ] same-PID/ROM/base/endian snapshots; [ ] A/B/C filters and JSON export; [ ] promote candidates into JP Live watch list, not verified mappings. |
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
- New synthetic and Tk tests plus the PowerShell regression script **passed on the user's Windows machine by report**; the focused A/B/C runtime is now supported by a screenshot, but wide mode and candidate semantics are not proven. Details: [`JAPAN_READONLY_VALUE_SEARCH.md`](JAPAN_READONLY_VALUE_SEARCH.md).

### User live confirmations and Windows regression triage — 2026-11-15

- [x] **Goemon XYZ coordinate teleport succeeded through the new Japan Live GUI in Oedo Town South**; `0x80151B10/14/18` form the behaviourally validated position-controlling float vector for the tested scene. This is same-scene relocation, not scene warping.
- [x] **Original Japanese debug menu visibly opened in Windows Project64** via the new Japan Live debug control (`0x800CD284: 0D→0A`); do not conflate this with destination selection / room-load success.
- [x] Windows script run after the XYZ message fix: targeted controller `7/7` and full backend `107/107` tests pass. [ ] Full GUI regression post-fix pending: 39 tests errored at construction of the minimal Tk test host due to missing `move_japan_oedo_xyz` callback, and one dashboard test observed an empty displayed savestate slot. Fixes committed `ec35b9c` (inert Host callbacks for XYZ and debug) and `7fc29bd` (explicit Combobox slot 0).
- [ ] Select a different room in native debug menu, confirm scene-load and controllable player, then replicate across at least two source/destination pairs before marking an inter-scene warp working.

### Japanese native debug-menu entry — 2026-11-15 (user live-verified opening; inter-scene warp pending)

- [x] Add `Scene warp (debug)` experimental tab within Japan Live, with catalogued scene hint and USA-derived category/index. The hint **does not** write the map and category/index parity is not yet verified in Japan.
- [x] One-shot, explicitly confirmed `0x800CD284: 0D→0A` original debug engine entry; current/pending/previous scene, exit flags, character, and XYZ left untouched. Must match exact Japan ROM, PID/backend, 4/8 MiB RDRAM and stable normal Goemon/Ebisumaru gameplay.
- [x] `--enable-japan-debug-menu-writes` is a separate opt-in; `--read-only` disables it. The native menu destination is then selected by the player in Project64. No automatic menu-cursor or confirm writes have been guessed.
- [x] Add big/wordswapped byte tests, controller refusal tests, Tk menu hint and write gating tests. [ ] Rerun full PowerShell suite.
- [x] Live PJ64: user reports the original debug menu visibly opens after the state request. [ ] Native selection actually loads a playable different scene. [ ] Map JP debug cursor/commit fields before implementing automatic scene-browser double-click warp.
- [Experimental protocol](JAPAN_NATIVE_DEBUG_SCENE_WARP.md).

### Full candidate XYZ export and first live wide scan — 2026-11-15

- [x] User supplied **live 8 MiB wide Japanese XYZ scan** with matching scene `353`, character `0`, A/B/C, wordswapped Project64 RDRAM: **1,240 XYZ candidates** detected. The old JSON exported only the top **200**, so it cannot be used to cross-reference the missing 1,040 addresses.
- [x] Preview continues showing **200 best-ranked** candidates, but **Export ALL XYZ candidates** now writes **all** scan matches to JSON sorted by guest address using a worker and atomic temporary file. Count must match original A/B/C preview count. The exported JSON includes `counts.exported_candidates`, session identity and per-candidate XYZ, but no 4/8 MiB raw snapshots.
- [x] Synthetic tests for **240+** matches and Tk full export written; [ ] user re-runs these new tests under Windows and performs two complete live wide captures for exact address cross-reference.
- [x] High-priority duplicate position family observed at `0x80151B10`, `0x80151BA8`, `0x80151C40`, `0x80211870` and `0x802118E0`; [ ] verify ownership and stability across movement, jump and scene/actor transitions. **No player pointer or writable XYZ confirmed**.
- [First full-width live capture findings](JAPAN_XYZ_LIVE_PROJECT64_RUN_001_2026-11-15.md) · [Updated export procedure](JAPAN_XYZ_DISCOVERY.md).

### Japanese XYZ discovery milestone — 2026-11-15 (code, synthetic tests not yet rerun)

- [x] Implement a **read-only**, user-labelled `Find XYZ triples` action within Event Sessions → Advanced RAM comparison. Requires **three WIDE, same-region/PID/base/endian/reader, same-scene/character** snapshots: A stationary, B after moving, C stationary at B (not returning to A).
- [x] Rank bounded aligned `>fff` triples where horizontal position changes A→B but remains stable B→C, rejecting nonfinite/implausible values. Export candidate values, scores, session identity only; never export raw 4/8 MiB snapshots or infer writable player pointers.
- [x] Make the CPU-heavy XYZ ranking asynchronous and discard stale worker results on reconnect/Clear; promote a selected *X coordinate* candidate as Japan-only `f32` custom watch.
- [x] Mark `0x80161DCF` A/B/C byte transitions as the **known low-byte alias of `u32` character index `0x80161DCC`**, not an independent event flag. Other reversible `0x80161DBD` remains unknown.
- [x] Add synthetic 4 MiB moving/stationary candidate, invalid scene/session, float range, word-alias and Tk presentation tests to Windows PowerShell/Linux regression scripts. **New tests have not yet been executed on the user's machine.**
- [ ] User repeats the PowerShell suite, completes one WIDE A/B/C movement experiment, and identifies a stable candidate across two areas and movement directions. Do not enable Japanese checkpoint, warp, freeze or collision writes from this heuristic alone.
- Details: [`JAPAN_XYZ_DISCOVERY.md`](JAPAN_XYZ_DISCOVERY.md).

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
- [x] User reports the expanded pre-XYZ PowerShell suite passes on Windows; Project64 3.0 Japanese read-only memory and changing Ryo UI have screenshot evidence; user confirms PJ64 savestate restoration succeeds. [ ] New XYZ tests and live XYZ research still pending.
- [x] User confirms Project64 savestate restoration and the separately consented Sasuke/Yae **unlock RAM writes** work in their Windows session. [ ] Confirm normal C-Down actor/model behaviour and character index values `2` and `3` separately.
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
- [x] JP Advanced RAM Comparison A/B/C with 2×4 KiB focused / verified 4/8 MiB wide ranges, async snapshot reads, source-tagged candidates and bounded exports **implemented in code; focused live experiment user-verified**. [ ] Wide live trial and event-meaning confirmation.
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
