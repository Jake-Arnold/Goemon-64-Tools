# Decomp continuation runbook

> 18 Nov wide USA file_18: 53 new native-exact original-address C / 796 bytes, one exact pristine-upstream scratch ROM, ELF 82,216 semantic relocations and 7,376 FUNC identities, GCC ASan/UBSan PASS. Research-only; canonical 966+53 verifier, inventory and full local CI NOT RUN. Accepted USA 966 / 41,324 bytes, Japan 39. Source catalog and native replay at research/usa_file18_native53_20261118, sanitized proof at results/usa_file18_native53_original_scratch_20261118.json.

> **18 Nov 2026 USA file_26 high-byte expansion — canonical native 966-C build (`PASSED_G2_GITHUB_PUBLISHED`):** 15 previously native-exact C funcs / 2,508 bytes (64–252 B each), integrated with 951 accepted C. Fresh IDO 5.3 combined USA ROM 33,554,432/33,554,432 identical, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, all 7,376 original ELF FUNC identities, exact all overlay/main semantic relocations and strict inventory (966 C / 41,324 bytes, 6,397 ASM), full local CI (242+245 tests and sanitizers) PASS. Japan stays 39. Original source/offsets are pinned in `research/highbyte_file26_20261118/promotion_manifest.json`, proof in `results/usa_file26_highbyte15_966_promotion_20261118.json`, and independent >512-B research in `research/highbyte_search_20261118/README.md`: 696 unconverted original functions totalling 793,572 bytes, no >512-B C-native match yet. Prior 951 proof archived; historical 41-item research queue retained, current 26-item queue excludes promoted 15. Implementation and proof published on `chatgptweb/decomp` at [`ec07c8c`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/ec07c8cd1c0922ec228b760660519d138a76ba95); remote manifest and strict inventory re-fetched and confirmed at 966 USA matching-C functions.

> **18 Nov 2026 canonical local 951-C USA acceptance (`PASSED_G2`, pending remote push):** Uploaded complete `chatgptweb/decomp` snapshot matching branch `4a51009` was materialized with original ROM and bundled native toolchain. New stage `overlay_native87_stage` authenticated 87 additional research C files (912 bytes), alongside all previously accepted 864 C, with **33,554,432-byte exact USA ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`**, all **7,376** original positive ELF FUNC identities, fully gated main + overlay semantic relocation identities relative to accepted 864, and strict inventory **951 USA C / 38,816 bytes, 6,412 ASM**, JP **39 C / 2,092 bytes**. Existing file_11 14 alias-named relocations and pre-existing 105-record main relocation reduction are pinned, not newly introduced. Exact source pins and ROM original addresses: `research/usa_main_overlay_87_20261118/promotion_manifest.json`. Verified execution report `results/combined.json` and original inventory `results/inventory.json`, previous verified reports archived as `results/{combined,inventory}_864_20261118.json`. The **local** verification is not a remote commit until GitHub is updated and re-fetched. See `results/usa_native87_951_promotion_20261118.json` and root `PROGRESS.md`.


> **18 Nov 2026 original-USA main/overlay expansion (`RESEARCH_ONLY`):** 87 new native-IDO-5.3 exact original-address C functions (912 original instruction bytes) from main plus overlays 13,14,15,17,18,19,20, explicitly excluding four already accepted no-ops. All 87 were integrated in one disposable pinned-original-upstream build: exact USA 33,554,432-byte ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; original 7,376 ELF FUNC identities and 35,563 affected main/overlay semantic relocations exact; actual C under ASan+UBSan PASS. See `docs/USA_MAIN_OVERLAY_NATIVE87_USA_20261118.md`, `results/usa_main_overlay_native87_upstream_scratch_20261118.json` and `research/usa_main_overlay_87_20261118/sources/`. These are **not accepted production**; authoritative remains USA **864 C / 37,904 bytes**, JP **39 C**. Full combined 864+87 production ROM, inventory and full local CI are **NOT RUN** pending a complete authenticated decomp checkout. This task did not alter canonical C ownership or existing manifest.

> **Promotion candidate queue + branch cleanup audit (17 Nov 2026; research-only):** Registered **41 USA native-exact research candidates / 4,108 bytes** with verified original ROM offsets, VMA, ELF sizes, original code SHA-256, pinned Git source blobs and failure-safe statuses in `data/promotion_candidates_20261117.json`: five main graphics (284 B), 15 file_26 (2,508 B), 21 file_27 (1,316 B). One file_25 72-byte isolated C result is BLOCKED_RELOCATION and excluded from eligible count. `python3 -m decomp.promotion_review --usa-expanded /path/to/verified/decompressed.z64` checks original authentic bytes and metadata; `--strict-sources` also requires a fully current checkout to authenticate all Git source contents. This queue is separate from the historic 87-item registry, which is already promoted, and **does not alter 864 USA/39 JP accepted C**. Combine with all 864 accepted C and pass new full-ROM G2, all relocations, original 7,376 ELF identities, inventory, full local CI before production promotion. Audited 34 live branches, five open PRs (#64/#63/#62/#60/#56); older branch blobs may still be unique, see `docs/BRANCH_RETIREMENT_AUDIT_20261117.md` and `data/branch_retirement_audit_20261117.json`. No branches deleted; connector lacks delete-ref.

> **File_26 ledger correction (17 Nov 2026):** All **15** scratch-exact file_26 USA C routines remain unpromoted: original three (312 bytes, original `results/file26_native312_upstream_scratch_20261117.json`) plus 12 later (2,196 bytes, `results/file26_adjacent15_upstream_scratch_20261117.json`). A branch-local research index now preserves both groups separately. The next production integration must stage all 15 with the current 864 USA accepted C and satisfy full ROM/ELF/relocation/inventory/CI gates; no promotion claimed. Full ROM-free local CI including sanitizer PASS.

> **Historical research audit (17 Nov 2026, RESEARCH_ONLY):** Reconciled 100 tasks, 77 historical execution ledgers, 85 research-result reports and 45 historical branch references against accepted USA 864 / Japan 39. Previously pending 87 are all accepted, but new separate research leads remain: five USA main graphics helpers (fresh IDO original-address 284/284 bytes exact, production 869-C G2 NOT RUN), 21 file_27 scratch-exact (1,316 B), 12 additional file_26 scratch-exact (2,196 B), file_25 isolated 72-byte relocation blocker, unresolved 13 script-VM ASM and compiler near misses. All nonpromoted source and reason records are on this branch, `research/historical_audit_20261117/{README.md,INDEX.json,LIVE_LEADS.json}`, plus the original graphics PR #63 source/proof and fresh `results/graphics_five_native_recheck_20261117.json`. Four new ROM-free tests and full decomp local CI (232+238 tests, sanitizer) PASS. All canonical manifest/proof/ASM ownership unchanged. No assertion that every remaining ASM function was natively retried.

> **Legacy native retry (17 Nov 2026; research-only):** A fresh original IDO 5.3 retry of USA `func_80001DF4_29F4` tested three C layouts; all 96 bytes against original 92, first mismatches +0x20/+0x00/+0x14. `func_8003F6E8_402E8` has an exact 40-byte C prefix but original 48-byte symbol includes an additional return pair. No C promoted; retain assembly and avoid counting prefix or linker padding. Focused 6 tests and full ROM-free local CI including ASan/UBSan PASS. Details: `results/legacy_native_revisit_20261117.json` and `research/legacy_revisit_20261117/README.md`.

> **Verified 864-C USA and 39-C Japan original-address production checkpoints (17 Nov 2026):** All prior 82 USA `file_11` research functions (3,512 bytes) passed fresh combined 864/864 original IDO verification with all prior 782 USA C. Original expanded 33,554,432-byte USA ROM identical (SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`), `file_11` semantic relocations 8,825 exact, original 7,376 ELF entries, zero aliases, strict 6,499 ASM entries. USA matching code **37,904 bytes**. The separate five Japanese rev-0 functions (180 bytes) passed a fresh combined 39/39 C original native build, byte-exact 32 MiB expanded + 16 MiB retail ROMs (SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded` / `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`), all original 80,747 ELF relocation identities and 7,376 function identities. JP matching code **2,092 bytes**. Historical 782-C USA and JP 34-C reports/manifests preserved. **Original 87-item research candidate registry is now empty**, with original source/provenance retained in `data/candidate_registry_782_pending_20261117.json`. Production proofs: `results/usa_file11_eighty_two_864_promotion_20261117.json` and `results/japan_0_five_39_promotion_20261117.json`. Do not re-promote these functions. Next candidates must be independently discovered from remaining original assembly and added to registry under distinct source proofs.


> **Verified 782-C USA production checkpoint (17 Nov 2026):** Fresh native 782/782 original-address matching C (34,392 bytes), adding three 104-byte USA `file_11` helpers to the verified 779-C build. The complete 33,554,432-byte ROM is byte-identical to original SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, all 8,825 file_11 semantic relocations and seven previously accepted overlay relocation multisets are preserved, 7,376 original ELF function entries unchanged, zero additional positive aliases, 6,581 ASM entries remain. Japan stays 34 C / 1,912 bytes. Previous 779-C proofs are preserved as `results/combined_779_20261117.json` and `results/inventory_779_20261117.json`. Existing pending registry: 82 USA `file_11` candidates / 3,512 bytes and five Japan / 180 bytes, research-only. Proof `results/usa_file11_three_782_promotion_20261117.json`.


> **Verified 779-C USA production checkpoint (17 Nov 2026):** Fresh native 779/779 original-address matching C (34,288 bytes), combining prior 732 C with 47 verified cross-overlay C. Exact original 33,554,432-byte USA ROM, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, 7,376 original function identities, seven unchanged overlay relocation multisets, and strict 6,584 remaining ASM inventory. Japan remains separately 34 C / 1,912 bytes. Remaining original-address research: USA `file_11` 82 / 3,512 bytes; Japan five / 180 bytes. See `results/usa_crossregion47_779_promotion_20261117.json` and `CANDIDATE_PROMOTION.md`.

> **Historical 732-C USA checkpoint (17 Nov 2026):** One original-address `file_11` camera-reset function (136 bytes) joined all 731 previously accepted C functions in a fresh exact 32 MiB USA ROM rebuild. Original ELF identities, all 8,825 file_11 semantic relocations and strict inventory passed. USA accepted **732 C / 32,068 bytes**; Japan accepted **34 C / 1,912 bytes**. Remaining pending **129 USA / 5,732 bytes** and **5 JP / 180 bytes**, all research-only. The prior 731-C `file_12` proof remains in the dated historical reports. See [CANDIDATE_PROMOTION.md](CANDIDATE_PROMOTION.md) and [the registry](data/candidate_registry.json).


For fast USA/Japan numbered-ROM file sizes and offsets, see [ROM_FILE_INVENTORY.md](ROM_FILE_INVENTORY.md), [the 1,311-file CSV](data/rom_file_inventory.csv), and [the partial semantic catalogue](data/rom_file_semantics.json). This is metadata research, not a new matching-C promotion.

## Region-separated matching-C checkpoints (17 November 2026)

- **Prior USA 720-C checkpoint:** 720 matching-C functions / 31,184 original code bytes; `file_11` contains 183 C functions (5,336 bytes). The full native 33,554,432-byte USA ROM, 8,825 semantic `file_11` relocations, 7,376 function identities and 6,643 remaining ASM entries are verified. The 346-, 342- and 315-function checkpoints below are historical; Japanese rev-0 results remain separately verified.
- **USA remaining:** 82 PR #23 exact original-address research functions (3,512 bytes) remain unpromoted. Strict combined 720 proof includes all 346 earlier functions and 374 original-address file_12 registration wrappers. The remaining 11 candidates in PR #48 are research-only.
- **Japan rev-0:** 34 matching-C functions / 1,912 original code bytes / 30 translation units. Selectively imported from `chatgptweb/japanese-decomp-port` into `chatgptweb/decomp`; the Japanese manifest lives at `decomp/regions/japan_0.json`, and the regional build runner is `decomp/build_japan_thirtyfour_c.sh`. Keep the two regional original-ROM hash gates and counts separate.
- **Acceptance:** The supplied 34-C code package was independently rebuilt from pinned upstream original Japanese source and ROM on 2026-11-17: exact 32 MiB expanded and 16 MiB retail ROMs, strict 34-C ELF ownership/source/relocation verifier PASS; eight ROM-free guardrail tests PASS. All 30 checked-in Japanese C source blob SHAs equal the independently verified package. The imported branch's distinct build wrapper and full combined USA local CI were not rerun. No gameplay or native PC recompilation claim.
- **Next research:** Five further Japanese 36-byte isolated candidates at `0x3A7AC`, `0x3A7D0`, `0x3AA34`, `0x3AA74`, `0x3AA98` remain excluded until a fresh 39-function complete Japanese ROM and strict ELF proof passes.



## USA 720-function promotion (17 November 2026)

The canonical production manifest has a versioned `0goemon-file12-registration-374-v1`0 stage replacing 374 complete 36-byte original registration wrappers at ROM 0x5C9310``0-0x5CC7A8. This stage preserves the two earlier file_12 dialogue callbacks and all 346 previously accepted functions, including 183 original-address file_11 functions. Stage C source and exact compiler/trimmed ELF object digests are pinned and validated; all 374 individual function symbols, 1,122 source relocations and 13,464 machine-code bytes were verified. The central `decomp.verify` full-USA-ROM proof passes 720/720, 31,184 C code bytes, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Semantic 7,051 file_12 and 8,825 file_11 relocations match the original; 7,376 original ELF function identities are preserved, zero extra positive-sized aliases, 6,643 assembly entries.

- Current proof: `decomp/results/combined.json`; identity inventory: `decomp/results/inventory.json`; VM ledger updated to the current manifest/verifier fingerprints.
- Stage implementation: `decomp/file12_registration.py`, `decomp/candidates/file12_reg374.c`, `decomp/overlay_file12.py`; fail-closed ROM-free tests in `tests/test_decomp_file12_registration.py`.
- Full `python3 -m decomp.local_ci` passed after updating historical-checkpoint tests; all C sanitizer fixtures and task/evidence validation passed.
- No unrelated file_12 or file_11 candidates promoted. Japanese rev-0 34-C is separate. No ROM, extracted assembly, ELF, proprietary toolchain or extracted game assets are tracked.

## Historical USA production checkpoint: 315 matching-C functions (16 November 2026)

The canonical manifest and published proofs now record **315/315 verified C functions / 16,660 original instruction bytes**, including 152 original-address C in `file_11` (eight whole-slice research functions / 316 bytes newly promoted), the two `file_13` Impact HP helpers and one dialogue slot setter. The original 32 MiB USA ROM is byte exact, all 8,825 `file_11` semantic relocations match, the 7,376 original function identities are preserved, and 7,048 assembly entries remain. The previous 307-C, 306-C, 303-C and 210-C reports are separately archived and remain unchanged.

- Canonical proof: `results/combined.json` / `results/inventory.json`.
- Native stage: `overlay_file13_stages` on top of canonical `overlay_file11_stage` 152-C in the pinned manifest.
- Further USA candidates: PR #23 (`file11-expansion-20261116`), PR #24 (`file11-transition-52-research`). Their native source proofs and partial scratch builds are not enough to claim combined production C matches. Deduplicate against the 152-C file_11 manifest (105 PR #23 candidates remain after the eight-group function promotion), then run fresh combined full G2 + original inventory + local CI.
- Japan: PR #26 has a separately exact regional 24-C proof, but is not part of the USA count and requires its own integrated regional acceptance.

Start here when continuing the matching-C work. This is the operational handoff;
For the executor-grade 100-task architecture and mandatory verification/stop rules, start at [plans/README.md](plans/README.md) and [plans/EXECUTOR_PROTOCOL.md](plans/EXECUTOR_PROTOCOL.md). These are planning documents only; live manifest/proof remain authoritative.
README.md explains the recovered units, BATCH_PIPELINE.md describes the tools,
and checkpoint documents retain technical research/history. Read root AGENTS.md
first. Update this runbook whenever the next targets or machine paths change.

Optional planning refinement: [plans/ARCHITECT_V3_PILOT.md](plans/ARCHITECT_V3_PILOT.md) defines a bounded compiler-guided selection pilot and model responsibility split. It does not supersede Architect v2's mandatory protocol, tasks or proof gates.

Optional research: [plans/REA_PILOT.md](plans/REA_PILOT.md) tests REA/Ghidra compatibility; Goemon's pinned `-mips2` ISA is not in REA's currently documented standard MIPS lane. The pilot is **not a dependency** for the 100 tasks or a source of matching-C proof.

The current Script VM runtime cursor/resource/text findings are in
[VM_RUNTIME_CURSOR_FIELD_REPORT.md](VM_RUNTIME_CURSOR_FIELD_REPORT.md). It
disambiguates `0x80077858` as the VM program cursor from the separate
text-token cursor at `0x801C77E8`; it does not change the matching-C task queue
or any proof gate.

## Authoritative 2026-11-16 USA matching-C promotion checkpoint (303 functions; supersedes dated 210/160-function checkpoints)

The full native central `decomp.verify` and `decomp.inventory` were run using
pinned upstream revision `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`,
the authenticated original USA retail ROM, original IDO 5.3, portable Python
3.12 / Splat and MIPS binutils, with a fresh candidate checkout and an
independently exact full-ROM baseline cache. The **complete 33,554,432-byte
ROM matches the original byte-for-byte**, SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`.

**Canonical `manifest.json`, `results/combined.json` and `results/inventory.json`
prove 303/303 original-address matching C functions, 16,180 instruction bytes,
7,376 identified original function entries, 316 combined C entries including 13
upstream C functions, and 7,060 remaining assembly entries.** The canonical
USA file_11 stage is `goemon-file11-143-central-v1`: 143 matching functions
(3,908 bytes), of which 93 were formally promoted from the previously accepted
50-function (1,064-byte) stage. All 44 C / 44 assembly source objects retain
original linked bounds. The complete original USA ROM and 8,825 semantic file_11
relocations match. Published 210-function proof and inventory are archived as
`results/combined_210_20261116.json` and `results/inventory_210_20261116.json`.
Promotion and provenance record: `results/file11_143_production_promotion_20261116.json`.

Original and candidate file_11 contain the same **8,825** semantic relocation
records (identical site/type/target/symbol multisets). Only three original
records at indices 2506–2508 appear in a pinned cyclical permutation, after
ID0 codegen; no other order difference is accepted by the fail-closed verifier.
The 180-byte character selector remains assembly-owned. Three synthetic
four-byte NOP FUNC annotations introduced solely by Splat text splitting are
normalized out while preserving all instructions and NON_MATCHING markers.

Fresh central G2/whole-symbol inventory proof and formal promotion record:
`results/combined.json`, `results/inventory.json` and
`results/file11_143_production_promotion_20261116.json` (historical 50-C promotion
remains in `results/file11_central_promotion_20261116.json`). The build proof is a native
exact-ROM test, not in-game character-switch validation. Japan full-ROM build
remains independently blocked by original sources' hardcoded USA assembly paths.
**Do not use the historical 160-function numbers in the dated sections below
as current counts.** The one-shot `decomp.promote_file11` review runner is now
retained for reproduction of the historical transition from a 160-claim manifest;
for later fresh verification of the already-promoted canonical 210 claims, use
`python3 -m decomp.verify` followed by `python3 -m decomp.inventory`.

## Local decomp CI (no GitHub Actions)

Run `python3 -m decomp.local_ci` for the standard ROM-free local test gate (decomp Python regressions, verifier/ledger tests, task evidence validation, and a sanitizer host fixture). For Python-only debugging use `python3 -m decomp.local_ci --quick`, reporting skipped sanitizer coverage. This is intentionally **not** an Actions workflow: absence of `.github/workflows` is not a Local CI blocker. Do not run a workflow-dependent `local-ci` skill or `act` here. Task-specific host tests and the original-VMA native IDO/32 MiB full-ROM G2 gates remain distinct and must be reported separately.

## Japanese Project64 character-switch to USA original C (research follow-up, 15 Nov 2026)

The draft PR #20 (`chatgptweb/japan-character-switch-decomp`) has **13 separately exact USA/JP original-VMA IDO 5.3 C functions per region, 620 bytes per region**. A pinned upstream scratch USA `file_11` mixed-C/ASM reconstruction rebuilt all **33,554,432 ROM bytes exactly**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; its 8,825 relocation records match the already validated four-function scratch build exactly, including their order. See `docs/USA_JAPAN_CHARACTER_SWITCH_13_FUNCTIONS_2026-11-15.md` on that PR branch. The regional character globals are USA `0x8015C5DC`, Japan `0x80161DCC`; candidate availability word arrays USA `0x8015C69C`, Japan `0x80161E8C`. The 180-byte four-character selector remains assembly-owned.

**This is not yet central verification or published matching-C promotion.** The production `decomp/manifest.json`, central `decomp.verify`, combined results and inventory are unchanged. The next bounded integration task is a production-safe mixed C/ASM `file_11` adapter and manifest declarations, followed by the central full-ROM G2, semantic relocations and inventory gate. Do not increase published totals based on standalone research; Java/Japan full-ROM build is still blocked by hard-coded USA `GLOBAL_ASM` paths.

## USA file_11 central verifier adapter (15 November 2026)

An **opt-in, fail-closed** `decomp/overlay_file11.py` stage is now wired into `decomp/verify.py`; see `docs/USA_FILE11_CENTRAL_ADAPTER_2026-11-15.md`. Activate only with `{"overlay_file11_stage":{"format":"goemon-file11-character-switch-13-v1"}}` in a verified candidate manifest. It stages exactly 13 original-USA matching-C functions / 620 bytes in 4 C source islands, retaining the 180-byte selector and all other code in assembly. The module checks the complete 32 MiB ROM, 13 original linked symbols, 8 linker input objects, 4 source/object identities, and all 8,825 file_11 relocation tuples before modifying any function count. The existing previously independently verified 13-function scratch ROM and ELF passed this new module's linked provenance checker. **Not yet a completed full central verifier run; production manifest/results/inventory remain unchanged.** Run central G2 using an opt-in manifest, then audit and promote only if exact.

## Follow-up USA file_11 callback matching-C research (15 Nov 2026)

The same USA `file_11` overlay as the 13 exact character-switch C functions also contains **50 original no-op callback stubs** of 12 bytes apiece. Two adjacent source groups (9 and 28, **37 newly reconstructed functions / 444 bytes**) were demonstrated with authentic original-ID0 and a whole-ROM build in a separate scratch checkout. Together with the earlier 13 functions, the **complete 33,554,432-byte USA ROM matches exactly with 50 C functions / 1,064 bytes staged in file_11**, all 8,825 original overlay relocations identical in order, and the original 180-byte selector still assembly-owned. All 44 ROM-free research Python tests passed. Details: `docs/USA_FILE11_NOOP_CALLBACKS_2026-11-15.md` and `decomp/results/file11_noop_37_native_proof_20261115.json`.

**Important:** The 37 are genuine *empty callbacks*, not 37 newly deciphered gameplay systems. The central opt-in `overlay_file11_stage` still supports only the previous 13 functions. The canonical `decomp/manifest.json`, formal 160-function verifier and inventory have not yet been rebuilt with either optional file_11 stage. The new 37 are research-only until a reviewed stage and complete central G2 test exist.

## Opt-in USA file_11 verifier v2 (15 November 2026)

The verifier accepts only the previous thirteen-function stage format or the new goemon-file11-character-switch-50-v2 format in a temporary reviewed manifest. V2 includes 13 character-switch C functions plus 37 authentic empty actor callbacks (50 C functions/1,064 bytes), and requires all six native compiler C objects, twelve original linker input positions, 8,825 original ELF relocations, original linked symbols and full 32 MiB ROM equality before counting these functions.

The pristine pinned USA upstream scratch build independently met those constraints, but the full central decomp.verify build with the existing 160 C modules has not yet been run. The canonical manifest and inventory remain unchanged. See docs/USA_FILE11_NOOP_CALLBACKS_2026-11-15.md.

## Formal file_11 promotion review runner (15 November 2026)

The reviewed optional v2 50-function USA file_11 stage now has a strictly gated runner at `decomp/promote_file11.py`. Use `python3 -m decomp.promote_file11 --source-dir ./decomp --upstream /path/to/clean/mnsg --retail-rom /path/to/USA.z64 --workdir /tmp/new-g2 --output-dir /tmp/new-file11-review --jobs 2`, optionally with `--baseline-cache` and `--binutils-root`. It generates a temporary 210-function candidate manifest but does not mutate the canonical 160-function manifest or claim verification. It requires the *complete central* G2 and inventory to pass (210 functions / 13,336 bytes / exact 32 MiB original USA ROM / all original file_11 linked C symbols, offsets, hashes, 8,825 relocations / 7,153 ASM entries) before emitting a reviewable promotion bundle. If any criterion fails, no promotion is made. Run `python3 -m decomp.local_ci` and examine the bundle before committing canonical manifest/results/inventory. Details in `docs/USA_FILE11_CENTRAL_PROMOTION_RUNNER_2026-11-15.md`.

**Known execution blocker in this ChatGPT container:** pinned original ROM, upstream ZIP, IDO, native MIPS build inputs exist; the 160-function full production source checkout is only available via private GitHub connector, not as mounted filesystem files. The complete central 210-function G2 was not run; research scratch full-ROM matches do not satisfy that combined gate.

## 0. Cross-conversation handoff

For the reviewed integration blockers and reproducible next steps, see [INTEGRATION_HANDOFF.md](INTEGRATION_HANDOFF.md).

Read [MASTER_WORK_QUEUE.md](MASTER_WORK_QUEUE.md) for the reconciled VM and overlay matching-C backlog; historical main-branch warp/story tasks have been superseded from parallel Goemon conversations. Historical chat totals may lag the latest manifest/proof; this runbook and the live branch remain authoritative. Do not repeat already promoted functions.

## 1. Establish the current state

**Authoritative continuation checkpoint — 2026-11-14; supersedes the dated
142-function and 20-step checkpoints below.** The dialogue-callback follow-up
continues in fresh worktree `codex/vm-dialogue-overlay`, based on verified
`origin/chatgptweb/decomp` commit `652b086527ceaf0a7e07a6ad63b217c95ff35909`.
G64-022 and
earlier milestones are retained as historical checkpoints. The completed
G64-055/056 overlay integration is published at `3062843c95768b898d9430ecfea03ed7e8b8896d`.
`main` was not changed. The private USA retail/decompressed ROMs, pinned `mnsg` source at
`7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, and IDO 5.3 compiler are copied
under ignored `practice/diagnostics/decomp-100-inputs/`, so the prior external
path is not needed in this worktree. Their verified SHA-1/fingerprint values
are recorded at the top of root `PROGRESS.md`. The local input folder is not
published to Git. [INPUTS.md](INPUTS.md) gives the pinned checkout, local ROM
and compiler locations, checksums, and fresh proof commands for recreating it.

The fresh pinned-source baseline reproduced 142 prior claims. Then the resource
dispatch, menu hook and object dispatch production translation units were
integrated and independently gated. Current `manifest.json`, `results/combined.json`
and `results/inventory.json` report **160/160 matching-C claims, 12,272 matching
MIPS bytes, and an exact 33,554,432-byte ROM match** (SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`). Inventory reports **7,376
identified entries, 173 current unmarked entries, and 7,203 remaining ASM
entries**. G64-060 added the exact 20-byte `file_12` callback
`func_80222034_5DD504` at VMA `0x80222034` / ROM `0x5DD504`; the full
188,624-byte overlay and semantic relocation set match. Its 36-byte sibling
`func_80222168_5DD638` now also passes linked-overlay and full-ROM proof; see
`VM_CONVERSATION_TARGETS.md` and
`plans/execution/2026-11-14-vm-file12-dialogue-call.json`. G64-056 added the exact
96-byte overlay initializer
`func_080001BC_6F369C` through the G64-055 file_43 adapter. Its original and
candidate overlay sections and all eight target relocations match; see
`plans/execution/2026-11-14-g64-055-file43-key.json` and
`plans/execution/2026-11-14-g64-056-file43-key.json`. The conversation-trace
follow-up added four exact dialogue helpers (320 bytes) in the existing
`dialogue_window.c` unit. `func_8000D2C0_DEC0` remains assembly-owned. See
`VM_CONVERSATION_TARGETS.md`,
`plans/execution/2026-11-14-dialogue-helper-integration.json`, and the current
combined proof. G64-057 then validated the key initializer's collected and
uncollected host paths against the original overlay instructions, using the
current full-ROM proof without rerunning an unchanged production build. See
`plans/execution/2026-11-14-g64-057-key-semantics.json`. G64-058 is
`RESEARCH_ONLY`: the checked-in Ghost candidate is not the source hash in the
historical two-word spill report, and its bounded native trials are exhausted.
G64-059's sanitized event fixture passes 800/800 cases, including flag-store
timing and callback order; the function remains assembly-owned. See the dated
G64-058/059 execution records. The G64-060 file_12 adapter also records why raw
relocation-section bytes differ: symbol metadata and the zero-size tail alias
use different ELF encodings, while all 7,051 relocation records match after
the explicitly tested narrow normalizations. G64-061 is `RESEARCH_ONLY`: its
verified original-address graph distinguishes the outer `stepw` dispatch, the
separate five-state `800030F0` subdispatcher and the three-entry `8001F8B0`
dispatcher. It identifies an ID-15 overlay-load request but leaves
`D_800548D8`'s meaning and scene teardown/activation unproven; both dispatchers
remain ASM-owned. See
`plans/execution/2026-11-14-g64-061-transition-state-graph.json`. The separate
dialogue-callback follow-up did not reorder the 100-plan queue. G64-062 is now
`RESEARCH_ONLY`: original MIPS and both file tables prove that ID 15 DMA-loads
Splat `file_15` from retail `[0x61D5DE, 0x626E5E)` into the shared
`0x801CB460` overlay window, then zero-fills its `0x14CA0` BSS. Allocation is
caller-owned; no activation, prior-overlay release or room teardown was
proved. See `MAP_TRANSITION_TRACE.md` and
`plans/execution/2026-11-14-g64-062-loader-boundary.json`.
G64-063 completed as `RESEARCH_ONLY`: the middle dispatcher reads the VM
program cursor only through the nonzero predicate at `8003F1D8`, does not
advance it, and retains `GLOBAL_ASM` after two native candidates first
diverged at `+0x10`. No fresh G2 was run; the stored proof is unchanged. See
`plans/execution/2026-11-14-g64-063-middle-transition-dispatch.json`.
G64-064 completed as `RESEARCH_ONLY`: the 116-byte transition helper branches
on `80036908`, updates two raw fields only on its zero path, then increments
`SYS_W+0x3ADD6` through a reloaded pointer. Its callers ignore the return; the
helper calls do not establish scene teardown or activation. See
`plans/execution/2026-11-14-g64-064-transition-loop-gate.json`.
G64-065 completed as `RESEARCH_ONLY`: command-table entry 5 reaches the
220-byte `80039F84` callback, which clears D0 once and applies per-entry pan
to active records in a 16-entry sweep. Its CE/CF neighbors are untouched;
the runtime trigger and meaning of D0 remain unknown. Host boundary tests pass,
while production ASM and stored proof remain unchanged. See
`plans/execution/2026-11-14-g64-065-engine-pan-sweep.json`.
G64-066 completed as `RESEARCH_ONLY`: command-table entry 6 reaches the
216-byte `8003A060` fixed-pan sweep. D0 zero sets it to 1 and scans 16 records;
nonzero D0 returns without writes or calls. One full-unit IDO hypothesis was
212 bytes and first diverged at `+0x0C` in the prologue, so the original ASM
remains. No G2 was run and the stored proof is unchanged. See
`plans/execution/2026-11-14-g64-066-fixed-pan-sweep.json`.
G64-067 completed as `RESEARCH_ONLY`: the 140-byte `8003A138` helper routes
full-word modes 7–10 through a biased byte lookup, conditional byte latches,
and two distinct output-byte pairs. Host tests pass, including a high-word
truncation mutant. One full-unit IDO hypothesis matched all neighboring
functions but changed the first branch delay slot at `+0x10`; production ASM
and the stored proof remain unchanged. See
`ENGINE_STATE_TRACE.md` and
`plans/execution/2026-11-14-g64-067-engine-state-mode-map.json`.
G64-068 completed as RESEARCH_ONLY: 0x80020F10 is a 1,332-byte selection
display handler. It writes a group-local selection and derived intended room
ID; the matched 0x80021444/214E4 chain performs the separate entrance-record
and state-request work. Existing all-zero-coordinate and room-index host tests
passed, but no bounded whole-function C candidate was justified. Keep
GLOBAL_ASM; the stored full-ROM proof remains unchanged. See
DEFAULT_ENTRANCE_TRACE.md and
plans/execution/2026-11-14-g64-068-default-entrance-review.json.
G64-069 completed as RESEARCH_ONLY. MAP_TRANSITION_TRACE.md now separates a
state request, a gated file-15 load request, and a safe playable transition.
The host fixture protects intended-room sentinels and the static file-15
destination window. Disabled direct-warp and scene-list tests now spy on
write_guest, so a write followed by restoration is caught. Production controls,
the manifest, and stored proof are unchanged. See
plans/execution/2026-11-14-g64-069-transition-safety-assertions.json.
G64-070 also completed as RESEARCH_ONLY: the transition source/manifest review
found no new exact C candidate, and all five transition dispatch/loop targets
remain GLOBAL_ASM. A fresh uncached full-ROM verifier and inventory confirmed
the current 160-function / 12,272-byte proof and the 32 MiB ROM identity; no
production source or stored proof changed. See
plans/execution/2026-11-14-g64-070-transition-slice-gate.json. G64-087 then
closed RESEARCH_ONLY: the three-way dispatch trace is verified, but two
bounded native candidates did not match; keep `8001F8B0` GLOBAL_ASM. On
2026-11-14 the user closed this 100-task execution plan after G64-087. The
remaining PLANNED entries, beginning with G64-088, remain unexecuted and are
out of scope for this plan. Do not start another task from it. See
plans/execution/2026-11-14-g64-087-state-dispatcher.json.
G64-074 added the
128-byte `func_80036308_36F08` per-node dispatcher after exact integrated IDO
and fresh G2 verification; its neighboring `func_800362DC_36EDC` is the list
walker. See `plans/execution/2026-11-13-g64-074-object-flags.json`. The old object-dispatch eight-byte mismatch is
historical; `OBJECT_DISPATCH_TRACE.md` records the exact current 96-byte unit
and full-ROM result.

G64-001–014 have recorded outcomes: G64-001, 002 and 004–014 passed G2; G64-003
was skipped as already complete under the existing G0–G3 proof contract. G64-051
has a tested explicit overlay metadata schema, classified `DOC_ONLY` because it
is not connected to the production verifier. G64-015–018 were retried with the
private ROM/compiler available; every host semantic harness passed, but no
candidate matched its full original C unit under native IDO. Each failed
whole-ROM build was rejected before inventory, and all four production ASM
placeholders remain in place. G64-019 is `RESEARCH_ONLY`; G64-020 is `DOC_ONLY`.
G64-021 is `DOC_ONLY`: [VM_RESOURCE_CALLGRAPH.md](VM_RESOURCE_CALLGRAPH.md)
records original-address call edges, observed ABI facts, direct global effects
and unknown callback behavior. G64-022 is `RESEARCH_ONLY`: offset-annotated
resource types and host endian checks are in place; the 556-byte IDO loader
candidate does not match the 548-byte original, so production ASM remains. A
fresh full-ROM proof refreshed the existing 148 claims without promotion.
G64-023 is `RESEARCH_ONLY`: the volatile F038 candidate reproduces 25/42 direct
words and 3/3 call relocation shapes but still has 17 direct-word and four
table-relocation-layout differences. G64-024 is also `RESEARCH_ONLY`: three
new semantics-preserving IDO variants retained the same mismatch profile.
G64-025's callback-mutation model and endian accessors pass, but its loader
candidate remains nonmatching native research. G64-026 added 36 guards for the
original D468 32-byte frame, saved-register lifetimes, entry-ID spill, and
return sequence. The isolated candidate still has a 24-byte frame and first
mismatches at `+0x8`; production ASM remains. G64-027 traced D68C's 203
original instruction words, 7 state cases, 31 token entries, and 0/1/2 return
paths; its 44-anchor ROM-bound guard and 119-test decomp suite pass. It added a
future host-model matrix without writing C. G64-028 traced DF98's signed
`-71..-32` command range, its 40-entry table, the `-1` caller sentinel, and
paced/unpaced callback ordering for cursor, marker and repeat state. The
132-word/54-anchor ROM-bound guard, 124-test decomp suite and 17 verifier tests
pass; no C model was written. See [`VM_MAIN_STEP_TRACE.md`](VM_MAIN_STEP_TRACE.md),
`VM_STREAM_MATCHING.md` and the execution ledger. G64-029 added a host guard
for DDC4 retry-time global reload and entry-ID preservation; the cached-global
negative control fails as expected, while production source and the proof hash
remain unchanged. G64-030 reconciled the live manifest, proof and inventory;
the `script_vm.c` unit currently has 43 C and 13 ASM entries. The typed
resource/stream interface matrix is in [`VM_RESOURCE_CALLGRAPH.md`](VM_RESOURCE_CALLGRAPH.md).
DDC4 and the context save/restore siblings remain exact; no new candidate met
the G2 gate, so D468, D68C, DF98 and F038 remain ASM. G64-031 traced DBEC's
118-word text-loop CFG and six branch-likely slots in
[`VM_TEXT_LOOP_TRACE.md`](VM_TEXT_LOOP_TRACE.md), with its original assembly
ownership unchanged. G64-032's saved-register/frame comparison and five
native source-shape trials are in
[`VM_TEXT_LOOP_FRAME.md`](VM_TEXT_LOOP_FRAME.md); none matched the 0x48 frame
or complete branch layout. G64-033 added ten fixed MIPS/host edge cases,
10,000-case defaults, 20,000 two-seed passing scenarios, and four killed
signedness, stale-bound and cursor-alias mutants. The VM function remains
`GLOBAL_ASM`; see `plans/execution/2026-11-11-g64-033-text-loop-differential.json`.
G64-034 traced DE80's signed-token branches, callback reloads and separate
`-1`/delegated-negative exits, and added an extent/anchor guard plus 11 host
scenarios. A pinned IDO replay produced a 220-byte symbol, not the older
reported 228-byte size; its first original-VMA mismatch is `0x8003DE84`.
G64-035 applied the pulled Architect v2 budget: four C shapes were compared;
the best moved the first mismatch to `0x8003DE88`, while a 232-byte symbol had
the wrong `0x30` frame. No source-unit match was found, and `script_vm.c`
remains assembly. Details are in
`plans/execution/2026-11-11-g64-034-command-walker-cfg.json` and
`plans/execution/2026-11-11-g64-035-delay-slots.json`. G64-036 reused all
eleven semantic scenarios and the original guard. The gate helper
is known to update the repeat count, not the repeat setting, so no unsupported
callback-mutation case was added. See
`plans/execution/2026-11-11-g64-036-command-walker-semantics.json`. G64-037
traced the 592-byte `0x8003ED60` handler, confirmed its no-argument `void` ABI
and sole direct caller, added a ROM-bound CFG guard, and ran one trace-derived
IDO probe. It remains `GLOBAL_ASM` after a first mismatch at `0x8003ED68`; no
function count changed. Full details are in
[`VM_ED60_TRACE.md`](VM_ED60_TRACE.md) and
`plans/execution/2026-11-11-g64-037-ed60-trace.json`. G64-038 verified
`func_8003F6E8_402E8` as exactly 48 bytes / 12 words at ROM offset `0x402E8`,
ending in two `jr $ra; nop` pairs. It rejects the 40-byte C prefix and 56-byte
candidate annotation as original extents; the function remains `GLOBAL_ASM`.
See `plans/execution/2026-11-11-g64-038-wrapper-extent.json`. G64-039 is now
`RESEARCH_ONLY`: the DBEC fixed cases pin expected cursor/state/latch/callback-
count traces, EB34 asserts emit/decode/resume callback order, and the crosswalk
reuses DE80, DF98, ED60 and F6E8 ROM/host evidence without modeling opaque
callback effects. See [`VM_PARSER_BEHAVIOR_MATRIX.md`](VM_PARSER_BEHAVIOR_MATRIX.md)
and `plans/execution/2026-11-11-g64-039-parser-matrix.json`. G64-040 closes
`RESEARCH_ONLY`: EB34 is already matching C in the stored proof; DBEC, DE80,
DF98, ED60 and F6E8 have no new source-unit-exact candidate. Production source,
manifest and verifier inputs are unchanged, so no new full-ROM or inventory
run was performed. See [`VM_STREAM_MATCHING.md`](VM_STREAM_MATCHING.md#G64-040--vm-parser-production-gate)
and `plans/execution/2026-11-11-g64-040-parser-production-gate.json`. The next
v2 task G64-091 is now `RESEARCH_ONLY`: the batch queue records signed
per-function attempts and skips unchanged completed probes across recipes; old
reports import as unsigned provenance-incomplete summaries. The current matching
count and stored proof are unchanged. See
`plans/execution/2026-11-11-g64-091-attempt-ledger.json`. G64-090 audited the
13 `return_zero.c` placeholders against the pinned Memory Pak disassembly and
ROM; all are nontrivial PFS routines, and all remain `GLOBAL_ASM`. See
`plans/execution/2026-11-11-g64-090-return-zero-audit.json`. G64-071 traced
`func_80001DF4_29F4` as a full-width, 8-byte-stride lookup returning bit 30;
two bounded native shapes remained nonmatching, so it stays `GLOBAL_ASM`. See
`plans/execution/2026-11-11-g64-071-file-table-reader.json`. G64-072 traced
`80001E50` as a four-byte sentinel table lookup. Three bounded IDO candidates
remained 112 bytes and first differed at `+0x04`; keep the helper as
`GLOBAL_ASM`. See `plans/execution/2026-11-13-g64-072-file-table-helper.json`.
G64-073 traced `80001EB0` as a gated inclusive page mapper over two-word,
eight-byte records. The known constant caller passes index 60, selecting row
59; the dynamic caller passes a task halfword. The table's declared extent is
unknown. Two IDO shapes linked at the original VMA but both differed at `+0x04`
in prologue scheduling; the function remains `GLOBAL_ASM`. G2 was not run. See
`plans/execution/2026-11-13-g64-073-file-table-mapper.json`.
G64-074 passed G2. G64-075 traced `80036388` as a move-to-front list operation and stopped after three IDO candidates all first differed at `+0x00`; it remains `GLOBAL_ASM`. G64-076 traced `800363F4` as another caller-gated non-head move-to-front operation; two candidates both first differed at `+0x00`, so it remains `GLOBAL_ASM`. G64-077 traced `80036448` as a 180-byte allocation gate; four IDO candidates failed exact codegen, while both accepted siblings remained exact, so it also remains `GLOBAL_ASM`. G64-078 traced the 308-byte `8000702C` worker: it receives on owner `+0x40`, dispatches `0x29A`–`0x29C`, and for `0x29D` sends owner `+0x20` through each node's `+4` destination queue before reloading node `+0`. Its host reference passed ASan/UBSan and rejected cached-next; the worker remains `GLOBAL_ASM`. G64-079 traced `80007160` as the 164-byte default task-message handler. The worker passes owner in `$a0` and the 32-bit `OSMesg` task pointer in `$a1`. The handler increments owner `+0x2B4` before its duplicate guard, builds two zero-state flags, and conditionally calls the queue/task helpers. Its sanitized mock reference rejected moving the increment after the duplicate check; it remains `GLOBAL_ASM`. G64-080 closed the batch gate with 0 new functions / 0 bytes; G64-074's 128-byte dispatcher is the only promoted item and remains covered by its existing full-ROM proof. Static call-site reports still do not close dynamic scheduler message producers and registration paths. See `plans/execution/2026-11-13-g64-080-files-object-scheduler-gate.json`. G64-081 traced `8000E2D4` as a 200-byte trig helper: raw angles flow to helpers that mask to 10 bits, negative zero is preserved by a strict `< 0` check, and the multiply order is observable. Seven host-reference cases passed ASan/UBSan, while three bounded IDO shapes remained nonmatching (best first mismatch `+0x08`); production stays `GLOBAL_ASM`. See `plans/execution/2026-11-13-g64-081-math-helper.json`. G64-082 passed G2 for `8000E39C` (328 bytes), then G64-084 passed G2 for `8000EA74` (72 bytes). At the G64-084 checkpoint the proof was 151 functions / 11,548 bytes; G64-084 exact-matched the full 400-byte unit while preserving EABC and the EB08/EB50 ASM siblings. See `plans/execution/2026-11-13-g64-084-angle-variant.json`. G64-085 then passed G2 as candidate 3 of 3, adding 72 bytes; the pilot now adds 3 functions / 472 bytes using seven of twelve new variants. Sol later closed the pilot; G64-086 passed under ordinary v2.
`python3 -m decomp.skill_context --status` and Sol's revised execution ranking
both selected G64-041, which is now complete as RESEARCH_ONLY; the trace report records
the 110-word ROM/assembly equality check and sanitized command-store contract. G64-042
then completed RESEARCH_ONLY with zero-input and owner-byte-alias host cases; its
pre-read-order mutant failed at the expected B400 w1 assertion. Production GLOBAL_ASM,
candidate C, manifest, and proof remain unchanged; native comparison, G2, and inventory
were not run. See plans/execution/2026-11-13-g64-042-display-memory-model.json.
G64-043 then completed RESEARCH_ONLY with a separate 109-word EBAC trace and a passing
EBAC host mode; its final B300 store order differs from E234, and the historical
500/464-byte first mismatch remains unavailable because local outputs were not retained.
G64-041's E400 and B400 source offsets were corrected in its sanitized trace. No
production source or proof changed. G64-044 then completed RESEARCH_ONLY after
full-unit native probes. Corrected V2 E234 (444/440 bytes) and EBAC (428/436)
both still differ at entry, with the first full-unit mismatch at `0x8003D0B8`
from a shifted forward-call relocation. The assignment-table pack preserved its
60-byte payload and 15 relocations. EBAC's post-w0 owner read passed the scratch
alias control; its pre-read mutant failed. `GLOBAL_ASM` remains, and G2/inventory
were not run. See `plans/execution/2026-11-13-g64-044-compiler-layouts.json`.
G64-045 completed RESEARCH_ONLY: the corrected 192-byte setup candidate still
differs at `0x8003F384` in float-register order inside the 10,112-byte unit.
The candidate moved scale LO16 and the allocator call by four bytes; no second
variant or G2 was run. The F37C research fixture records the observed word at
`+0x8C` and byte at `+0xD8`, while the shared header stays unchanged;
production ownership remains `GLOBAL_ASM`. See
`plans/execution/2026-11-13-g64-045-vm-setup-abi.json`.
G64-046 completed RESEARCH_ONLY: the pointer-lifetime candidate passes 400
sanitized synthetic cases but compiles to 356 bytes versus the original 348.
The target first differs at `0x8003E6CC` in the saved-register spill; its extra
eight bytes shift a later call target. `GLOBAL_ASM` remains, and G2/inventory
were not run. See
`plans/execution/2026-11-13-g64-046-callback-setup.json`.
G64-047 completed RESEARCH_ONLY: the pinned 164-byte target and `%d` string
were verified, and its host harness passed 1,000 cases. Historical evidence
already covers 15 IDO variants; none reproduce the `bnel` delay slot, and the
best remains 3/13 comparable direct words. No new source hypothesis justified
another trial. `GLOBAL_ASM` remains; no full-unit build or G2 was run. See
`plans/execution/2026-11-13-g64-047-number-formatter.json`.
G64-048 completed RESEARCH_ONLY: E234 and EBAC display emitters, F37C and
E6C0 setup, F480 digits, and the broader VM host regression all passed their
ASan/UBSan mock suites with buffer/state guards. These are separate fixtures,
not combined MIPS or in-game execution. All five targets remain `GLOBAL_ASM`;
source, header, verifier, manifest and stored proof are unchanged, so no new
full-ROM build was run. See
`plans/execution/2026-11-13-g64-048-vm-graphics-boundaries.json`. G64-049 is
complete as RESEARCH_ONLY: the live manifest confirms none of the five
graphics/setup candidates has source-unit exact proof, so all five retain
`GLOBAL_ASM`; no source-unit or G2 build was warranted. See
`plans/execution/2026-11-13-g64-049-vm-graphics-staging.json`. G64-050 is
complete as RESEARCH_ONLY. Its canonical
`results/vm_residual_inventory.json` reconciles all 13 current main-segment
`script_vm.c` ASM functions with pinned extents, hashes, native exactness state,
blockers, and unblock conditions; `results/inventory.json` remains the
generated whole-project inventory. The separate file_12 callback findings
remain on their research branch and are not part of those 13. See
`plans/execution/2026-11-13-g64-050-vm-residual-inventory.json`. G64-051 is
DOC_ONLY. G64-052 completed RESEARCH_ONLY: the new input contract binds exact
Splat layout/source identity to the private decompressed ROM, its text/rodata
hashes, and requested original file_43 function spans; all 27 focused tests,
the private-input CLI check and the ROM-free local gate passed. No overlay ELF,
candidate ROM, G2 or inventory proof ran, so no C claim changed. See
`plans/execution/2026-11-13-g64-052-file43-reference-contract.json`. G64-053
completed RESEARCH_ONLY: the new overlay-specific linked-ELF checker ties the
pinned reference ELF's `.file_43` output section to the mapped ROM bytes, then
checks candidate section layout, function symbols/code and per-function
relocation targets. Synthetic failure controls and retained G64-082 baseline /
candidate ELF validation passed; no new native build, G2, inventory or C
promotion occurred. `verify.py` remains main-segment-only until the planned
G64-055 integration adapter. See
`plans/execution/2026-11-13-g64-053-overlay-elf-provenance.json`. G64-054 is
complete as RESEARCH_ONLY: the overlay checker rejects unrelated allocated
VMA overlap while allowing distinct `.file_N` overlays that intentionally
share the same RAM VMA. It also rejects named aliases, changed text/rodata
bytes, duplicate function bounds, symbol-size lies, and altered undefined
relocation targets. The existing main-segment verifier regressions pass, and
the retained G64-082 baseline/candidate ELF pair still passes the checker. No
new native build or G2 promotion was run. See
`plans/execution/2026-11-13-g64-054-overlay-negative-controls.json`. G64-055
and G64-056 then passed G2: the adapter keeps the 16-byte `.file_43` output
alignment while placing the C candidate at its pinned VMA and the whole ROM
matched byte for byte. The four dialogue helpers from the Sol-reviewed
`codex/goemon-vm-research` branch have since passed a fresh integrated G2;
G64-057's host-semantics checks also passed. No in-game verification was
performed. That older G64-058/G64-087 continuation marker is superseded:
G64-061/062/063 and G64-071–086 are now recorded complete, and G64-087 is the
first PLANNED task in the live ledger.
G64-085 passed G2 as pilot candidate 3 of 3. Sol closed the pilot at 3/3 candidates and 7/12 variants; no extra global budget carries forward. G64-086 then passed ordinary Architect v2 with two of five variants, adding 180 bytes; the stored proof remains 153 matching-C functions / 11,800 bytes. G64-083 closed as `RESEARCH_ONLY` with `GLOBAL_ASM` retained. G64-089 then ranked the five float-state functions and tested two bounded candidates for `80006B44`: V1 had 38 differing target words; Sol diagnosed register lifetime/scheduling and approved one induction-lifetime variant. V2 reduced the mismatch to 36 words but retained the first `$v1`/`$v0` mismatch and missed the predicted `$a2` loop roles. The target remains `GLOBAL_ASM`; G2 and inventory were not run. See [`plans/execution/2026-11-13-g64-089-float-state.json`](plans/execution/2026-11-13-g64-089-float-state.json). G64-041 then completed RESEARCH_ONLY with all 110 words verified locally and the sanitized 11-command store contract; its execution report is plans/execution/2026-11-13-g64-041-display-emitter-trace.json. G64-087 remains gated on G64-061/062/063. Keep concrete predicted instruction deltas as a hypothesis-scoring refinement.

**2026-11-10 execution checkpoint:** `results/next_twenty_execution_20261110.json` records live 142-function branch review and native IDO 5.3 compilation of complete *research* equivalents of three real translation units. Resource dispatch **112/112 bytes exact** (including both 36-byte wrappers and existing middle function); menu hook **256/256 exact** (including existing 8-byte hook and three menu functions). **Object dispatch fails** full-unit comparison: 8 bytes differ at original `0x35C9C`/`0x35CA0` from `lui`/RA-spill scheduling despite earlier standalone 48-byte success. Eleven source variants did not fix it. Research-only `prove_integrated_units.py` is a fail-closed reproducer. **ZERO promoted**; the 2,331-object full-ROM gate was not available on this isolated container, and the prior 142-function formal proof remains authoritative. Resume full current-source build before production integration; do not count isolated matches as promotions.

**Active 20-step integration plan (2026-11-10):** use [NEXT_TWENTY_STEPS.md](NEXT_TWENTY_STEPS.md) for the full gated execution order: reproduce the current 142-function formal baseline; replay six isolated exact IDO/ld.lld candidates (368 bytes); integrate two resource wrappers, object dispatcher and three menu functions in their original translation units with **complete-ROM proof at each safe acceptance checkpoint**; then retry the other four nonmatching main-segment functions. The prior 142-function formal verifier is complete, but the six isolated candidates remain **unpromoted** until their new complete 32 MiB builds pass. Conditional milestones 148/11,020 after six and 152/11,180 after ten are not claims. Root PROGRESS.md has the plan-only record.

**2026-11-10 next-ten completed as isolated matching research:** all ten attempted, six standalone C functions independently linked to their actual original addresses and exact **368 bytes** matching the SHA-pinned USA ROM. New menu functions `func_80011B60_12760` (84 B), `func_80011BB4_127B4` (80 B), `func_80011C04_12804` (84 B) exact isolated outputs after preserving `0xFF7F` mask and deleting an unnecessary local. `prove_three_menu_flags.py` passed 3/3 pinned object/linked-ROM extents; GCC ASan/UBSan host mocks passed 90,000 cases. **None promoted**; no new integrated project ROM build. See `results/next_ten_main_wave2.json`, `NEXT_TEN_MAIN_SEGMENT.md` and `PROGRESS.md`. Prior formal verifier remains complete for 142 only.

**Formal verifier completed on updated live branch (2026-11-10):** current `results/combined.json` records **142/142** exact original-address functions and the **full 33,554,432-byte** ROM match; `formal_verifier_run_completed=true`. This was performed by another contributor; see `PROGRESS.md` and `decomp/INTEGRATION_HANDOFF.md` for formal proof provenance. **New main-segment first wave:** three *research-only* pinned IDO 5.3 + isolated `ld.lld` original-address matching functions `func_80034ED4_35AD4` (36/36 B), `func_80034F20_35B20` (36/36 B), and `func_80035094_35C94` (48/48 B), using separate original VMA links. `prove_three_wrappers.py` reproducibly checks real ROM SHA and linked bytes, including readelf FUNC sizes; 30,000 host mock cases and seven negative/parser tests passed. **NOT PROMOTED** absent a new complete 2,331-object ROM relink after integration. See `results/next_ten_main_wave1.json` and `NEXT_TEN_MAIN_SEGMENT.md`.

**Fresh formal gate (2026-11-10):** The current 142 claimed functions / 10,652 bytes passed the uninterrupted current `decomp.verify` run and complete 32 MiB ROM identity; a fresh inventory confirms 155 total C / 7,221 ASM. `results/combined.json` and `results/inventory.json` contain fresh evidence. References below to a pending formal run are historical and superseded. No additional function was promoted. See [INTEGRATION_HANDOFF.md](INTEGRATION_HANDOFF.md).

**Next ten fresh main-segment C targets (2026-11-10):** [NEXT_TEN_MAIN_SEGMENT.md](NEXT_TEN_MAIN_SEGMENT.md) supersedes the *active function-reconstruction target order* from the previous ten-target VM research batch, not its proof or backlog. Ten distinct live-manifest ASM functions totaling **528 original bytes / 132 words** were individually checked against the SHA-pinned 32 MiB ROM. Prioritize short engine-state writer, state-predicate writer, paired resource wrappers, file-table helpers, object dispatcher, and three menu-state flag handlers. **Current source formal verifier and repaired tests remain prerequisite verification debt**; no new matching C claims. See dated root PROGRESS.md.

**Verification-test repairs (2026-11-09):** `tests/test_decomp_verify.py` had stale 139/140 count assertions; current manifest is 141 unit C + 1 patched upstream C = **142**, now cross-checked against both proof and inventory JSONs. `compare_original.py` had incorrectly doubled backslashes in original function-label, nested-label and `jal`/`j` relocation regexes. Its exact previous files produced **2 failures + 2 errors / 12 tests**; after correction (including broken literal-backslash-newline fixtures), **13/13** parser/negative tests passed from both repo-root and `decomp/` invocations. The corrected comparator was additionally run against SHA-verified private ROM plus two IDO objects; both correctly returned **nonmatch**. **Earlier comparator-based research metrics require recheck before promotion.** Complete current 142-function test suite and uninterrupted formal `decomp.verify` remain pending. No promotion; PROGRESS.md has exact limits.

**Next-five execution checkpoint (2026-11-09):** all five work packages visited, none promoted. Formal 142-function run blocked by locally available 136-function archived source, not marked successful. VM resource lookup stays at original/native 196 bytes, 25/42 direct positions after six further nonimproving bounded trials. New `overlay_file43.py` validates pinned USA Splat `file_43` ROM text/rodata mapping, both original overlay SHA-256 extents and optional full-ROM bytes; 19 parser/negative tests passed; this is not yet linked-ELF source ownership or overlay integration in `decomp.verify`. The existing key initializer host harness passed six cases; new unpromoted `candidates/ghost_probe.c` compiled to 140 bytes but differs in MIPS, with 800 host mock cases passing. See `NEXT_FIVE_ACTIONS.md`, `results/next_five_execution_checkpoint.json` and `PROGRESS.md`. Formal flag and existing 142-function proof unchanged. **Next: restore complete current source and add linked overlay verification, never claim a C promotion from an original reference hash.**

**Next five tasks planned (2026-11-09):** see [NEXT_FIVE_ACTIONS.md](NEXT_FIVE_ACTIONS.md). Ordered: uninterrupted 142-function formal verifier; 196-byte VM lookup register/relocation match; fail-closed overlay ROM/VMA proof; 96-byte overlay key initializer; 140-byte Ghost Toys entrance two-byte compiler stack mismatch. These are work packages, not verified promotions. The authoritative 142-function / 10,652-byte proof and pending formal flag are unchanged.

**Next-ten targets #7–#10 investigated (2026-11-09):** all ten now investigated, **zero promoted**. The new research-only `candidates/vm_resource_halfword_volatile_probe.c` matches the resource lookup's 196-byte native IDO function size and improves direct original-word positions **11/40 → 25/42**, but is NOT exact matching C. Original wrapper `func_8003F6E8_402E8` is **48 bytes / 12 words**; a 56-byte annotation concerns a candidate symbol and cannot justify a promotion. A total of 7,400 fresh synthetic host tests, 18 Python unit tests and all 239 original ROM instruction words for these four functions passed. See `results/vm_next_ten_batch4.json`, `NEXT_TEN_FUNCTIONS.md`, and `PROGRESS.md`. Prior 142-function proof remains unchanged; formal verifier pending. Focus next on #8 register/stack allocation and formal verifier.

**Next-ten #6 complete as research (2026-11-09):** exact current VM text-loop alias candidate reproduces the historical 472-byte pinned IDO native `-c` output and 53 directly comparable nonrelocation words. Ten native codegen variations gave no improvement; GNU MIPS reassembly of IDO `.s` differs (480 bytes). See `results/vm_text_loop_native_codegen_probe.json`. Move to plan #7 `func_8003D468_3E068`; no C promotion or new formal verifier result.

**Next-ten target #5 (2026-11-09):** 14 pinned IDO/MIPS codegen variants of the original 232-byte VM command walker `func_8003DE80_3EA80` were measured against the hash-verified original. Seven passed 8,400 total synthetic mock-C scenarios. No variant reproduced original `bltzl` or saved-register layout; a 232-byte size-only variant was specifically rejected. Baseline remains 228 bytes / 8 of 35 direct words. See `results/vm_next_ten_batch3.json`. **Next #6: text loop `func_8003DBEC_3E7EC`**. Exact 142-function promotion count and formal flag remain unchanged.

**Next-ten target #4 (2026-11-09):** `func_8003E6C0_3F2C0` has a research-only 400-byte IDO source against 348-byte original, with **0/52 directly comparable instruction-position matches**, and 400 synthetic host cases passed. Verified 87 original words and 12 guards; expanded cumulative first-four guards to 354 words/32 anchors. See `candidates/vm_callback_setup_e6c0.c` and `results/vm_next_ten_batch2.json`. No promotion or formal-verifier completion. **Next #5 `func_8003DE80_3EA80`**.

**Next-ten plan targets #1–#3 (2026-11-09):** three *unpromoted* VM C drafts and tests were added: no-call graphics emitters `func_8003E234_3EE34` (original 440, IDO 516 B) and `func_8003EBAC_3F7AC` (original 436, IDO 500 B), plus setup `func_8003F37C_3FF7C` (original and IDO both 192 B, **not** the same instructions). Mock host tests passed 4,300 scenarios, private ROM/assembly 267/267 original words and 20 guards passed, four parser negative tests passed. See `results/vm_next_ten_batch1.json`, `test_vm_display_emitters.c`, `test_vm_setup_f37c.c`, `test_vm_next_ten_original.py`. **Next: #4 `func_8003E6C0_3F2C0`**. Official 142-function proof and pending formal verifier are unchanged; do not promote any of these candidates.

**Next ten selected functions (2026-11-09):** see [NEXT_TEN_FUNCTIONS.md](NEXT_TEN_FUNCTIONS.md) for an evidence-ranked, ten-target execution plan and the ROM/proof acceptance gate. Begin with the two no-call display-list emitters `func_8003E234_3EE34` and `func_8003EBAC_3F7AC` once the current 142-function formal verifier is attempted. The plan is not a promotion: **142 matching-C / 10,652 bytes** remain authoritative. The wrapper's 48/56-byte symbol-boundary difference must be resolved before any claim.

**VM command walker negative-tail branch probe (2026-11-09):** separate research-only `candidates/vm_command_walker_goto_probe.c` moves the negative-token arm below the positive loop. Pinned IDO 5.3 still compiles **228 bytes** (original 232), but ROM-verified isolated direct instruction-position matches improved from **3/33 to 8/35**. No `bltzl` delay-slot or saved-register match; **UNPROMOTED**. Both original and goto research variants passed 1,200 GCC ASan/UBSan synthetic cases each; 12 ROM-comparator parser/negative tests passed. See `results/vm_command_walker_goto_probe.json` and PROGRESS.md. Keep 142 exact-C count, formal-verifier flag and historical full-ROM proof unchanged.

**Guarded isolated comparison and 232-byte VM walker (2026-11-09):** added `compare_original.py` plus ten synthetic tests. It validates original Splat assembly against the exact decompressed 32 MiB USA ROM and compares an IDO-built ELF32 MIPS function to original words, preserving relocation masks and refusing malformed evidence. Example: `python decomp/compare_original.py --rom PATH_TO_VERIFIED_DECOMPRESSED_Z64 --original PATH_TO_PRIVATE_ORIGINAL_ASM --object PATH_TO_ISOLATED_OBJECT --function func_8003DE80_3EA80 --objdump PATH_TO_PINNED_MIPS_OBJDUMP`. **Exit 0 does not mean full-ROM proof.** A research-only `candidates/vm_command_walker_probe.c` compiled to 228 bytes versus 232 original; 1,200 synthetic host cases and 10 comparator tests passed, but only 3/33 directly comparable words matched; UNPROMOTED. Keep 142 matching-C count and `formal_verifier_run_completed=false` unchanged.

**VM loader recovery resource-ID mutation regression (2026-11-09):** new `test_vm_loader_resource_mutation.c` verifies that two consecutive recovery callbacks may mutate the global resource ID, each subsequent original MIPS global reload uses the *current* value, while `func_8003DDC4_3E9C4` receives the entry resource ID preserved across calls. **1,024/1,024 GCC ASan/UBSan synthetic cases passed**, five private original-assembly guards passed, and a deliberately broken ID reuse failed the host test as intended. Two original-address assertions were added to `test_vm_loader_original.py`. These are host/static regression results, **not** matching-C promotion or in-game verification; candidate remains 560 compiled bytes versus 548 original, and the formal full-ROM verifier remains pending.


**VM resource halfword lookup (2026-11-09):** new research-only `candidates/vm_resource_halfword_probe.c` for `func_8003F038_3FC38` (196 original bytes) compiled to **204 bytes**, with only 3/49 relocation-masked positional matches; **NOT** a matching-C promotion. Original 49 instruction bytes were independently compared against the pinned decompressed USA ROM. The source includes signed half-indexing and low-half recovery callback handling; 3,000 synthetic host cases, 16 original-assembly guards, five negative/parser tests passed. See PROGRESS.md; preserve 142-function full-ROM proof.

**VM digit formatter research (2026-11-09):** `func_8003F480_40080` is a NEW unpromoted 164-byte, 41-word VM candidate in `candidates/vm_digits_format_probe.c`; its IDO 5.3 symbol size equals original but **9/41 relocation-masked positions (3/19 non-relocation positions)** match, not an exact reconstruction. Pinned retail/decompressed ROM SHA-1 and original bytes at `0x40080` confirmed. Host GCC ASan/UBSan tests **1,000/1,000** and 15 original-address instruction guards plus four negative parser tests passed. Do not promote. Address original `bnel` delay slot and `sprintf` argument scheduling; see PROGRESS.md.

**VM loader host endian correction (2026-11-09):** original `lhu +2` reads the numerical *low* half of the big-endian resource ID. Research candidate `vm_loader_storage_probe.c` now has a host-only low-half accessor; 400/400 synthetic host cases pass and the previous host model fails the corrected assertion. Pinned IDO/MIPS recompilation proved the original and revised candidate `.text` both equal the same **560-byte** payload. The original is **548 bytes**, so there is **no C promotion** and the 142-function proof is unchanged. Volatile pointer qualifiers do not restore the original `$s0/$s1` saves. See `PROGRESS.md`.

**Unpromoted text-loop experiment (2026-11-09):** separate `candidates/vm_text_loop_alias_probe.c` retains the exact 472-byte IDO symbol size, improving 47/95→53/95 comparable nonrelocation instruction positions using a volatile VM-work pointer and explicit script-argument reload. It passed 10,000 original-MIPS/host-C synthetic differential cases and three structural tests, but its 0x50-byte frame differs from the original 0x48 and it is NOT a matching-C promotion. See `results/vm_text_loop_alias_probe.json`. Keep 142 matching C unchanged.


**Latest independent matching-C promotion (2026-11-09):** 142 functions / 10,652 bytes, 155 combined C, 7,221 ASM entries. The 340-byte comparator `func_8003D9B8_3E5B8` was promoted after complete 2,331-object IDO/Splat integration, original-address 142/142 instruction verification, 32 MiB exact ROM identity, 7,376-entry inventory, and 1,134 synthetic host cases. The uninterrupted formal `decomp.verify` run is **still pending**; previous 141-function prose below is historical.


Automated continuation must commit and push **only** to `chatgptweb/decomp`, never `main`. The workspace and main-branch history below describe the earlier local workflow, not the authorized target for this automated continuation. Verify the branch head before writing; do not force-push.

Historical workspace:

- Windows: `C:/Users/Jake/.codex/worktrees/goemon-entrance-warps/Goemon Toolkit`
- Historical branch: `main` (not the authorized automated target)
- WSL cwd: `/mnt/c/Users/Jake/.codex/worktrees/goemon-entrance-warps/Goemon Toolkit`
- Remote: `Jake-Arnold/Goemon-64-Tools`

Run `git status --short`, `git branch --show-current`, `git rev-parse HEAD` and
`git fetch origin`. Preserve unrelated changes. A separate new task requires a
fresh verified-origin/main workspace; a continuation does not. Do not merge or
delete other branches/worktrees just to tidy the list. Check ancestry first.

Integration on 2026-11-03: the completed entrance-warps branch included main
and both older feature branches. Its history is fast-forwarded into `main`;
the historical workflow continued on main; automated continuation remains on `chatgptweb/decomp`. Redundant branch refs can be removed
without deleting worktrees. Older worktrees retain their original commits in
detached HEAD state; leave their local bookmarks, checkpoints, ROMs and research
artifacts untouched. The primary checkout is also retained at its original commit.
Recheck `git branch --show-current`, fetched remote state and worktree status
before future work; do not use an older detached checkout for new implementation.

Current checkpoint (2026-11-08): 141 newly matching functions / 10,312 bytes:
140 functions in thirty-two migrated units (including the 8-byte heap no-op),
plus the 80-byte collision gate integrated into an existing upstream C unit.
Including 13 upstream C entries: 154 of 7,376 identified entries, leaving 7,222
ASM entries (including SDK/runtime). VM: 55 C / 14 ASM. Both newest candidates
passed independent original-address/full-ROM verification. The collision gate
uses a pinned source hash; the heap no-op uses a narrowly validated ELF .text
metadata layout correction that preserves its two instruction words.

The new 44-byte VM callback registration and 136-byte choice dispatcher have now
passed a fresh 2331-object Linux build and original-address/full-ROM identity
checks. The formal verifier timed out before report emission; its resumed build
was checked independently using the same comparison and inventory routines.
The proof record explicitly distinguishes those methods; no in-game test occurred.

The 204-byte VM choice edge has since been integrated into a separate full source rebuild at the current 140-function code state. The complete ROM and all 141 claimed functions match exactly after Splat regenerated the CRC-damaged archive assembly. This independent proof is not a completed uninterrupted `decomp.verify` run.

Treat these as a dated snapshot. For current claims, read:

1. `manifest.json`: claimed functions and retained assembly.
2. `results/combined.json`: latest successful complete-ROM proof and source hashes.
3. `results/inventory.json`: whole-build counts.

Older JSON/checkpoints are historical evidence. Do not rewrite them to imply a
new run. An isolated linked match, plausible C, or zero permuter score does not
count as a full-ROM-verified function.

## 2. Use the existing Linux tools

### Automatic isolated MIPS binutils environment (Linux / WSL)

The recovered cross-binutils archive bundles an incompatible `libc.so.6`; adding its
entire `usr/lib/x86_64-linux-gnu` directory to `LD_LIBRARY_PATH` can crash
`mips-linux-gnu-ld`. **Do not export that full library directory.**

The formal `decomp.verify` runner now automatically invokes
`prepare_mips_binutils.configure` when given the extracted archive root.
It stages only the five pinned Binutils DSOs in a **new private runtime directory
inside the new verifier workdir**, checks version strings of assembler, linker,
objcopy, objdump and nm, and passes the curated PATH/library environment to
every build subprocess. No system install, persistent shell exports, modifications
to the pinned toolchain, or manual `eval` are needed.

Supply either `--binutils-root /path/to/extracted-archive-root` on the normal
`python -m decomp.verify ...` command, or set
`GOEMON_MIPS_BINUTILS_ROOT=/path/to/extracted-archive-root` in the environment
used to launch the verifier. The root must contain
`usr/bin/mips-linux-gnu-ld` and `usr/lib/x86_64-linux-gnu/`.
The verifier creates `<new-workdir>/.binutils-runtime` itself and rejects
unexpected libraries, missing tools and incompatible versions. Without a root
setting it retains the standard system-toolchain behavior. The extracted archive
and ROM remain local; this setup is recreated in every ephemeral environment.

Run the focused tests:
`python -m unittest discover -s decomp -p 'test_prepare_mips_binutils.py'`
and
`python -m unittest discover -s decomp -p 'test_verify_binutils.py'`.


All commands below run in Ubuntu WSL, from the toolkit cwd above. From PowerShell,
enter with `wsl -d Ubuntu`, then `cd` to that quoted WSL path. Compiler inputs must
use LF line endings; do not build from a CRLF-converted mnsg checkout.

Machine-local paths (verify existence before use; never commit their contents):

| Purpose | Path |
| --- | --- |
| Pinned clean upstream | `/root/goemon64-verified-vm-context-v2/baseline` |
| Certified immutable baseline | `/root/goemon64-batch-gate-fresh-v1/baseline` |
| Latest verified candidate | `/root/goemon64-file-table-v1/candidate` |
| Batch cache | `/root/goemon64-batch-pipeline-v1` |
| m2c | `/root/goemon64-batch-tools/m2c` |
| decomp-permuter | `/root/goemon64-batch-tools/decomp-permuter` |
| Baseline Python | `/root/goemon64-decomp-7e2029c/.venv/bin/python` |
| uv | `/root/goemon-build-tools/bin/uv` |

Tool pins and generic setup are in BATCH_PIPELINE.md. Upstream pin:
`7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
Retail ROM SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66`.
Decompressed ROM SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`.
Use the user's local ROM; do not download or upload it.

## 3. Select useful work; preserve failed attempts

The scalar-context batch already attempted 762 functions, including the remaining
eligible main-segment functions up to 512 bytes. Repeating that unchanged recipe
will not resolve missing types. Improve a reviewed declaration/layout or choose
a concrete target first. Prefer actual upstream types over guessed structures.

For map load/unload research, start with [MAP_TRANSITION_TRACE.md](MAP_TRANSITION_TRACE.md); it lists the native state and entrance candidates, evidence and failed probes.

Next targets, in useful order:

| Target | Existing evidence / next action |
| --- | --- |
| VM comparator `func_8003D9B8_3E5B8` (COMPLETED) | Promoted in the current 142-function complete-ROM reconstruction: 340 exact original bytes, full 32 MiB identical image, 142/142 original-address checks, 7,376-entry readelf inventory, 1,134 sanitizer host cases. Formal uninterrupted verifier still pending. |
| VM text loop `func_8003DBEC_3E7EC` | Latest standalone candidate compiles to original 472-byte symbol, but is unpromoted: 53/95 nonrelocation words in the raw isolated probe (or 53/88 under the separate relocation-layout report), 0x50 vs original 0x48 stack frame. G64-033 now passes ten fixed edges plus 10,000 MIPS/C synthetic cases over two seeds and kills four targeted mutants. Recover register lifetimes and branch scheduling; do not change proof counts. |
| Choice edge `func_8003D0B0_3DCB0` (COMPLETED) | Promoted 204-byte exact C at original address. Fresh 2,331-object compile with regenerated Splat sources gave 33,554,432/33,554,432 matching bytes, all 141 function proofs and unchanged 7,376-entry inventory. 100 host cases passed. Uninterrupted formal verifier still pending. |
| VM loader `func_8003D468_3E068` | Needs resource-prefix interfaces. Derive fields/calls from actual loads and upstream declarations. |
| Key initializer `func_080001BC_6F369C` | Public `candidates/key_spawn_gate.c` matches 96 bytes in an isolated linked probe. Promotion requires reviewed overlay mapping/layout support in verifier, then complete-ROM proof. |

Other known limits:

- `/root/goemon64-vm-target-context-v1` retains the earlier VM context scan.
  Controller D17C from that scan is now solved; do not redo its old failed draft.
- Comparator D9B8 remains ASM. `vm_compare_reference.h` is host-only semantics.
- Wrapper F6E8 is confirmed as a 48-byte original with two trailing `jr $ra; nop`
  pairs. The 40-byte C prefix and 56-byte candidate annotation are not original
  function extents; it remains assembly-owned. See `test_vm_wrapper_extent.py`.
- Ghost Toys entrance: GHOST_TOYS_CHECKPOINT.md; 140-byte draft still differs in
  two stack offsets. It is not matching C.
- Current manifest verifier supports the main-segment mapping only. Overlay
  support must explicitly model original ROM/VMA relationships and section layout.
- Preserve all original instruction/data bytes. Never patch bytes, weaken checks,
  or silently discard allocated sections to manufacture a match.

## 4. Work loop

1. Inspect the original function, callers, typed declarations and nearby data.
2. Change one justified interface/control-flow assumption at a time. Keep drafts
   and logs in ignored diagnostics or private Linux storage.
3. Compile/link at original addresses and inspect exact byte differences. A size
   match alone is insufficient. Use bounded searches; retain failures.
4. Integrate a reviewed candidate into its original unit, retaining unresolved
   ASM/data, and update manifest bounds. Add meaningful host behavior tests.
5. Run the complete-ROM gate and appropriate tests below.
6. Only after success update current proof/inventory/counts and public docs.
7. Update PROGRESS.md, commit and push; verify the remote commit. Continue with
   the next useful target without asking whether to continue.

If an experiment stalls, record the precise mismatch and move to another target.
Do not ask the user to solve compiler/interface questions. Ask only for genuinely
missing user input, such as an explicitly needed live observation. Decomp work
itself requires no game writes or live testing.

### Local whole-ROM mismatch diagnostics (new; no change to verified counts)

When a candidate build exists but fails the exact matching gate, compare the
**local** pinned decompressed reference with the locally rebuilt image:


~~~bash
python -m decomp.rom_diff \
  --reference /path/to/baserom.decompressed.z64 \
  --candidate /path/to/candidate/build/usa/mnsg.z64 \
  --report /path/to/NEW-local-rom-diff.json
~~~

The tool checks the reference SHA-1 against `manifest.json`, compares **actual
bytes**, and reports the changed byte/32-bit-word counts and first changed words
with ROM offsets and claimed matching-C function names where applicable.
Exit status 0 means identical bytes; 1 means differences. Reports must stay
in ignored/local research directories. Do not commit original ROM bytes or
the resulting local diagnostics. No comparison here promotes a function
to matching C; the normal complete-ROM verifier remains mandatory.
The manifest also tracks a narrowly accepted upstream-owned C source patch for
the 80-byte collision gate, verified at its original guest address with a full-ROM
identity match. Do not treat arbitrary existing-source edits as supported patches.

## 5. Exact verification commands

Choose a NEW tag for each attempt. The verifier and inventory refuse existing
output destinations; do not delete previous evidence to reuse a name.

```bash
tag=$(date -u +%Y%m%dT%H%M%S)-decomp
run=/root/goemon64-$tag
report=practice/diagnostics/$tag.json
rom='/mnt/c/Users/Jake/Downloads/Mystical Ninja Starring Goemon/Mystical Ninja Starring Goemon (USA).z64'
python3 -m decomp.verify \
  --upstream /root/goemon64-verified-vm-context-v2/baseline \
  --baseline-cache /root/goemon64-batch-gate-fresh-v1/baseline \
  --workdir "$run" --retail-rom "$rom" --report "$report" \
  --uv /root/goemon-build-tools/bin/uv --jobs 2
```

If the gate fails, stop promotion and inspect the preserved report/logs. After it
passes, run inventory with the same shell variables:

```bash
python3 -m decomp.inventory \
  --baseline /root/goemon64-batch-gate-fresh-v1/baseline \
  --candidate "$run/candidate" \
  --report "practice/diagnostics/$tag-inventory.json"
```

Inspect reports before copying sanitized metadata into `results/combined.json`
and `results/inventory.json`. Retain historical reports. If verifier code changes,
run a new complete-ROM gate so its recorded source hash matches current code.

Run focused Linux pipeline tests when changing pipeline/integration code:

```bash
python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch \
  tests.test_decomp_probe_integration tests.test_decomp_elf_layout \
  tests.test_decomp_inventory tests.test_decomp_baseline_cache \
  tests.test_pickup_placements -q
```

Run affected native host tests; these commands cover the current VM/resource/angle
units. VM needs non-PIE because encoded guest pointers use 32 bits. The VM and
resource tests include their implementation; do not compile it twice.

Isolated candidate semantic test (not complete-ROM proof):

```bash
gcc -std=c11 -Wall -Wextra -Werror -fno-pie -no-pie \\
  -fsanitize=address,undefined decomp/test_vm_choice_edge.c \\
  -o /tmp/goemon-choice-edge-host-test
/tmp/goemon-choice-edge-host-test
```


```bash
gcc -std=c11 -Wall -Wextra -Werror -fno-pie -no-pie \
  -fsanitize=address,undefined -Idecomp/test_support \
  decomp/test_script_vm.c -o /tmp/goemon-vm-test
/tmp/goemon-vm-test
gcc -std=c11 -Wall -Wextra -Werror -fsanitize=address,undefined \
  -Idecomp/test_support decomp/test_save_resources.c decomp/system_memory.c \
  -o /tmp/goemon-resource-test
/tmp/goemon-resource-test
gcc -std=c11 -Wall -Wextra -Werror -fsanitize=address,undefined \
  -Idecomp/test_support decomp/trig_angles.c decomp/test_trig_angles.c \
  -o /tmp/goemon-angle-test
/tmp/goemon-angle-test
```

In Windows PowerShell, run the application suite when code changes require it:
`py -3.13 -m unittest discover -s tests -q`.
Last run: 319 tests, 314 passed and five native skips. This is historical, not a
substitute for validation of new changes. Synthetic tests, exact-ROM matching and
in-game verification are distinct evidence; report them separately.

## 6. Publish a completed change

- Update PROGRESS.md with date, change, reason, tests, limitations and next step.
- Review `git diff --check`, diff and staged file list. Exclude ROMs, generated
  assembly, assets, saves, memory dumps and personal diagnostics/trial IDs.
- Commit a coherent completed change with a descriptive message; push to the
  connected branch. Compare `git rev-parse HEAD` with
  `git ls-remote origin refs/heads/chatgptweb/decomp`.
- Report verified progress and any real blocker. Never claim an unperformed push,
  runtime test, merge, or decompilation promotion.

Do not close existing toolkit windows or disrupt pending captures/freezes. Do not
install rebuilt ROMs, write game memory or enable raw warp shortcuts as part of
native reconstruction. Keep the companion and native C research boundaries intact.
