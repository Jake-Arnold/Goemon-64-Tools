# USA ↔ Japan Toolkit feature parity checklist

## Japanese toolkit acceptance and parity expansion — 15 November 2026 (current)

**User acceptance before this batch:** the existing native Project64 Japanese scene warps work, and the then-current Windows and Linux regression suites passed. Right-click Live Memory Hex Edit worked; Freeze was disabled by an explicit Japan-only UI gate.

**This batch, implemented and pushed to draft PR #17:**

- **Live Memory freezes:** Japanese fixed guest-address 1/2/4/8-byte Freeze/Unfreeze is now available from the right-click menu and the shared Value freezes tab. A 10 ms best-effort worker checks Japan-0 gameplay context, pauses during scene reloads/menus, and opens a short-lived writable handle only when a value diverges. Freezes stop on disconnect, backend/region changes and toolkit savestate actions. USA health/God Mode/player-task freezes remain USA-specific; the original USA freeze path is preserved.
- **Story Progress:** 17 user-verified Japanese inventory/party progression rows now appear across the existing grouped Story Progress tabs. They are readable and writable through the existing region-specific mapped unlock writer, with stale-value checks. These rows represent **inventory progress**, not Japanese permanent saved-event flags; unknown JP story bits are still read-only research subjects. USA story bit mappings remain unchanged.
- **Named Japanese checkpoints:** the existing native emulator full savestate card offers a name field, **Save named slot** and **Load named slot** for Japan Project64/Mupen64Plus. Native slots 0–9 are still owned by the emulator, which preserves position, actor state, inventory and progress. The toolkit saves **only local slot metadata**, optional scene/character/XYZ observations, and request timestamp; it never serializes game state. Commands explicitly say **requested**, not confirmed complete, and named LOAD requires a connected matching Japanese emulator.
- **Regression coverage:** added Japanese synthetic freeze tests, Story Progress model tests, native slot metadata tests, and Tk tests covering all three features. Cross-region scripts now include the existing USA raw-freeze backend, USA freeze UI and USA Story Progress UI suites. Fixed the preexisting stale USA menu-index expectation (Freeze is item 2 after Hex Edit and separator). Documentation: [Named checkpoint design](JAPAN_NAMED_CHECKPOINTS.md) and `PROGRESS.md`.

**Verification boundary:** The user's previously reported test pass and live warp success predate these feature commits. This new batch has been statically reviewed and committed, **but has not yet completed an independent Windows/Tk regression run or live Project64 test**. PR #17 remains draft. No Japanese actor pointer/USA story-event mapping was fabricated or imported.

The earlier entries below are historical checkpoints and may describe features previously missing or disabled; this section supersedes them.



## Japanese Unlocks — live user acceptance (15 November 2026, latest)

The user reports that **33 of the 34 Japanese Unlocks controls work correctly in Project64**, including the individual Miracle items, Gold Key, Silver Fortune Doll progress, all weapons, upgrades and abilities. The sole **unverified** entry is **Sasuke battery 1** at candidate `0x80161DF9` (bit `0x20`). Toolkit metadata now records independent `user_verified` status while retaining the original source provenance; only that battery row retains a visible question mark. Japanese Unlock All covers **33/34**, battery excluded, and USA Unlocks behaviour is unchanged.

The next investigation is the unverified battery byte. A Japan-only, read-only **Sasuke battery probe** preset is available in Event Sessions, selecting `0x80161DC0` as the 100-byte window start. Documentation: [Sasuke battery investigation](JAPAN_SASUKE_BATTERY_RESEARCH.md). The user report verifies the preceding toolkit build, **not** this new post-report code revision; the new GUI and regression changes still need to be run on Windows.

Historical entries below describe prior stages and are superseded by this section where they disagree.

## Latest research-to-code mapping — 15 November 2026

**Experimental candidate implementation, not 34 gameplay-verified unlocks.** The shared 34-row USA/Japan Unlocks interface now has Japanese address proposals for every row: **nine named source-backed mappings, sixteen inferred from published Japanese four-slot GameShark arrays, four inferred from the consistent USA+0x57F0 regional displacement, and five explicitly marked guesses**. Names and confidence labels are in [the full mapping table](USA_JAPAN_UNLOCK_MAPPING.md). The original USA row addresses, button values, and write implementation were not modified.

- Source: [GameHacking.org's NG5J cheats](https://gamehacking.org/game/20438) prove array starting addresses, width, repeat count and stride, **not the identities of individual slots**.
- **Bazooka candidate: 0x80161ECB** (Japanese subweapon slot 3). Medal of Flames is subweapon slot 4 at `0x80161ECF`. Do not confuse these with the dialogue/event-bit deltas from the earlier Bazooka pickup screenshot; Bazooka identity is still pending a live toggle check.
- **Japanese Chain Pipe uses On=01**, unlike USA On=02; the shared button labels and on-wire write values are region-aware while USA definitions remain unchanged.
- The five weak guesses are Sasuke battery 1 (`0x80161DF9`, bit `0x20`), and Star/Moon/Flower/Snowflake assigned in order to Japanese treasure slots `0x8016204B/4F/53/57`. These five are **manually writable for experiments, but excluded from the default Japanese Unlock All**.
- Default Japanese Unlock All writes **29 rows** (named + array/offset inferences) and skips these five guesses. `--read-only` disables all writes.
- Added/updated region mapping, backend write, USA regression, and Tk GUI tests. **The latest Windows tests and emulator confirmation are pending**. PR #17 remains draft.

The sections below are historical implementation notes. Any older statement that Japanese Unlocks only contain nine mappings, that Sasuke/Yae need a confirmation dialog, or that 25 rows remain `unknown` is superseded by the current mapping table above.

## Character-compatible warps, editable Live Memory and additional identity mappings — 2026-11-15

- User confirms live Japanese Sasuke/Yae party unlock, Triton Shell, Cucumber, all fish counts and normal scene teleports work. Scene warp while currently playing Sasuke/Yae was rejected by a character-0/1-only predicate. The same 0x0C native reload is now allowed in stable gameplay for all characters 0–3; no scene or submode restrictions were otherwise changed.
- Scene Browser now exposes **the shared character selector** in Japan mode. Default is **Keep current character**. Choosing a different character stages the Japanese character-index word **experimentally** just before the 0x0C reload; this target-character override has **not** been live verified.
- Unlocks scrolling with Windows wheel or Linux Button-4/5 works over its canvas, cards and buttons without global event handlers.
- Shared Live Memory now provides **Edit value (hex)** via right-click for both USA and Japan, in addition to double-click on Hex. Japan uses direct guest-RDRAM byte writes with readback to the verified attached emulator PID/base/endian; `--read-only` blocks it. No arbitrary JP editor field is mislabelled a verified gameplay flag.
- Added JP **Super Pass 0x80161EF3 → USA Lord's Pass** and **Benkei weakness 0x80161EFF → USA Achilles' Heel** from user-supplied identity matching, raising confirmed source-backed counterparts from 7 to 9; 25 remain `unknown`.
- Bazooka pickup screenshot recorded three changed bits at 0x80161DBE (0x01 clear) and 0x80161DBF (0x10 clear, 0x80 set), with only one event trial. **Bazooka mapping remains unknown** pending controlled repeat comparisons. See `docs/JAPAN_BAZOOKA_PICKUP_TRACE.md`.

## Immediate scene-warp correction — 2026-11-15

- **Live failure reported:** Japanese Scene Browser double-click showed the **original debug menu**, unlike USA's instant area reload.
- **Root cause found in source:** Japan was writing engine `0x0A` and waiting for debug category/keyboard-A, while USA uses pending map/entrance followed by **engine `0x0C`**.
- **Correction committed:** `practice/japan_direct_scene_reload.py` and `Toolkit.start_japan_native_scene_warp` now write Japanese pending `0x800CD490` (2 or 12 bytes) and immediately request `0x800CD284=0x0C`. Original debug button remains manual-only; no keyboard input. Optional entrance uses cached USA reference data only when uniquely determined and warns otherwise.
- **New explicit CLI:** `--enable-japan-scene-writes`; legacy `--enable-japan-debug-menu-writes` still allows the direct reload for existing setups, but does not make the original debug menu part of double-click.
- **Tests committed:** `tests.test_japan_direct_scene_reload`, revised `tests.test_japan_native_scene_controller` and exact Scene Browser double-click dispatch tests, wired into Windows/Linux parity suites. [ ] Windows suite rerun. [ ] Live Project64 inter-scene destination/footing verified.

## Shared Unlocks parity update — 2026-11-15 (post user-passing test suite)

- The **original USA Unlocks panel is shared** in both regions: all 34 USA rows, buttons and seven groups remain intact. A region switch updates the displayed guest address; an unmapped equivalent is displayed literally as `unknown`, never substituted with a USA address.
- Nine Japanese fields now map to USA Unlocks identities: Sasuke, Yae, Triton Shell, Cucumber, Lord's Pass → JP Super Pass, Achilles' Heel → JP Benkei weakness, and the three fish counts. The remaining 25 Japanese counterparts are `unknown`.
- **Revision: direct writes now replace the guarded party-only writer.** All nine mapped Japanese rows support one-click edits by default (Sasuke/Yae On/Off, Triton Shell/Cucumber On/Off, red/blue/yellow fish counts). A short-lived writable handle does not revalidate ROM/scene/character on every click. Mapped-only **Unlock All** sets these nine values; all 25 unknown addresses stay disabled. `--read-only` still overrides writes.
- The user reports the previous Windows backend/Tk suite passed. The new direct-write code and revised regional UI/controller regression tests are committed but **have not yet been executed in Windows**. Japanese native scene-warp implementation is unchanged.

## Latest cross-region implementation (2026-11-15; Windows rerun pending)

**Read this section as current.** The original row-by-row audit below is a historical pre-consolidation baseline, with some “absent”/“disabled” cells superseded by the changes listed here. The user requested one UI shared between both game versions, not a separate Japanese scene browser. The Japanese ROM still cannot inherit arbitrary USA task pointers, event bits or write privileges.

| Shared tab or feature | New Japan-0 implementation | Remaining validation |
| --- | --- | --- |
| Dashboard | Region-specific RDRAM process; Japanese scene, character and position values shown; remembered exact Japan ROM path reverified on each new session | Japan velocity/action/task pointers and logical checkpoints unverified |
| Scene Browser | **Same existing browser; no duplicate Japanese selector.** Double-click **immediately** stages Japan pending destination at 0x800CD490 (u16 or 12-byte reference entrance block) and requests **0x800CD284 = 0x0C** area reload in the same callback, then monitors 3 stable gameplay polls. Original debug menu 0x0A remains a separate manual button | **First real inter-scene Japanese warp not yet live confirmed.** User did verify visible debug menu opening. USA double-click/entrance path remains unchanged |
| Live Memory | **Same Live Memory tab**, reads 58 Japan cheat-backed values, 10 scene probes, 3 observed XYZ floats and isolated Japan custom watches | General Japan raw edit/freeze disabled pending mapped permissions |
| Unlocks | **Same 34 USA rows and seven groups**; 33/34 Japanese controls user-confirmed in live Project64 gameplay, all except Sasuke battery 1. Japanese Unlock All writes 33 and skips only the unverified battery. Source provenance retained separately from user verification. | Run updated Windows tests; investigate the JP battery byte/bit using the read-only Event Sessions preset; reconcile PR stack before merge. |
| Story Progress | **Same nested progress tables**, presents Japan item/map/bonus-mode candidates with addresses and evidence | JP saved-event bank and story-bit causality unknown; no USA bit editing |
| Event Sessions | Same A/B/C event/idle/control flow and ranking. Japan captures 100 user-selected source RAM bytes (default 0x80161D80); provenance stores region, address, and backend. Advanced RAM Comparison still available | These Japan bytes are candidate RAM, **not** a confirmed persistent event bank |
| Damage events | Same event recorder UI uses JP HP byte 0x80161DD7, current scene 0x800CD2A2 and character 0x80161DCC, omitting guessed USA task/object pointers | No proof of JP invulnerability/collision semantics |
| Value Search and A/B/C | Existing shared scan and wide matching, including **all candidate** JSON export separate from 200-row preview | Native Windows wide export/regression rerun pending |
| Value Freezes, checkpoint restore, native menu calibration | Existing panels retain USA-specific semantics and write gates; Japan actions cannot borrow USA raw editor, player-task or event addresses | Region-specific JP task/pointer, freeze and logical checkpoint schemas required before equivalent writes |
| ROM verification | Saved path + exact expected Japan SHA-1 in per-user config, rehash/verify file each future session; PID, host RAM and code signature revalidation unchanged | First post-upgrade remembered-path startup test in Windows pending |

**Implementation constraints:** Japanese experimental write switches default on from CLI; `--read-only` overrides them. Per-action confirmation still exists for manual Goemon XYZ/debug experiments; shared Unlocks writes are immediate. The previous debug-category/stage/A-input double-click prototype was replaced after the user confirmed it **only opened the original menu**. The new 0x0C native reload writes the pending destination/optional entrance (not current map or exit flag), **exactly as the USA reload does**. It is not yet live verified; the original debug-menu opening is only evidence for the separate manual control. Files are committed, but complete new Windows PowerShell tests and first actual destination load remain outstanding.


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
| 4 | **Unlocks** | USA 34 named toggles/levels/counts, one-click mapped unlock all | **Shared 34-row UI:** Seven named Japanese source-backed fields are directly writable by default; 25 others display `unknown`. No separate Japanese Unlocks panel, party consent dialog, or per-click ROM re-probe. JP Unlock All operates only on the nine mapped fields. Native gameplay verification remains pending. | [ ] Build JP-specific names/widths/allowed values from gameplay; [ ] map other party and upgrades; [ ] compare before/after UI; [ ] guarded per-item write proof, then (last) bulk unlock. Do not assume four repeated cheat slots correspond to specific characters without verification. |
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
