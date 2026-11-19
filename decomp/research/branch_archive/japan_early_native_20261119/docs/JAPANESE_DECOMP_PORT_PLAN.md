# Japanese Goemon 64 decompilation and optional native-port plan

**Status:** Approved implementation roadmap; discovery/ROM identity verified, assembly-only Japanese 32 MiB and 16 MiB exact ROM builds verified; matching-C and gameplay not yet verified.
**Date:** 2026-11-15
**Development branch:** `chatgptweb/japanese-decomp-port`, initially branched from `chatgptweb/japanese-region-loader` at `dd301ff5ae80c0f98a95c8911ba0a442d70fe274`.
**Upstream matching-decomp repository:** https://github.com/klorfmorf/mnsg (pin `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` for existing USA proofs).
**Upstream native static-recomp repository:** https://github.com/klorfmorf/Goemon64Recomp (independent workstream, NOT equivalent to matching decomp).
**Existing workspace:** `Jake-Arnold/Goemon-64-Tools` and `decomp/`. The standalone upstream repository is not forked into Jake's GitHub account because the connected GitHub integration lacks fork/create-repository actions. Do not describe this development branch as a GitHub repository fork.

## 1. End products and non-goals

### Track A — Japanese matching decomp (primary)
1. Import and validate the user's *Ganbare Goemon: Neo Momoyama Bakufu no Odori* (Japan rev 0) ROM on the developer's machine; accept byte-swapped `.n64` inputs, normalize without altering original files.
2. Reproduce upstream `japan_0` extraction and the original 32 MiB **decompressed** image exactly.
3. Rebuild a Japanese N64 image with known reference hashes, retaining original assembly/data wherever C has not been matched. Distinguish bit-identical 32 MiB decompressed reconstruction from a bit-identical **recompressed 16 MiB retail image**; prove each separately.
4. Promote Japanese matching-C functions through the same exact comparison, linker/relocation and full-ROM gates as USA, with *independent* per-region counts.
5. Preserve all USA baseline verification and progress; do not overwrite USA code, ROM, symbol maps or output directories.

### Track B — Japanese static recompilation / native PC runtime (secondary, independent)
1. Use the original Japanese ROM to generate Japanese-specific MIPS functions, symbols, overlay tables and runtime patches for `Goemon64Recomp`.
2. Add an independent Japanese `GameEntry`, verifying ROM identity and correct generated code. Never hand Japanese assets to the USA function table.
3. Compile a Linux-native application and validate title screen, controls, cutscenes, effects and saving in the *Japanese* game. This is **not** accomplished by a Japanese ROM decompressor or by Track A's byte-identical N64 output.
4. Release Track B only after actual end-to-end runtime testing. Keep Track B a separately gated upstream fork/worktree and pull request.

**Non-goals:** translate Japanese into English, redistribute ROMs/asset extracts/IDO binaries, claim that structural instruction similarity proves code equivalence, or silently turn unknown Japanese memory addresses into USA addresses.

## 2. Verified source audit (2026-11-15)

Both uploaded cartridge files were examined locally without uploading the bytes to GitHub. Exact normalized retail identities:

| Attribute | USA | Japan rev 0 |
| --- | --- | --- |
| Original on-disk signature | `80 37 12 40` (`.z64`) | `37 80 40 12` (16-bit-swapped `.n64`, effectively V64 order) |
| Size | 16,777,216 bytes | 16,777,216 bytes |
| Game ID / revision | `NG5E` / `00` | `NG5J` / `00` |
| Normalized SHA-1 | `df8083a54296b8c151917c5333e1c85f014a2a66` | `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` |
| Normalized SHA-256 | `1603be37427a33548857fc3d2e8867ede71121c353fb631b79b44f1d94845d80` | `a1d288fa352ef185e0499a63b64dfc937c460da15a10456f180ee71298277413` |
| Original CRC1 / CRC2 | `FCBCCB21` / `72903C6B` | `832C168B` / `56A2CDAE` |
| Nisitenma signature ROM offset | `0x57FC8` | `0x58248` |
| Nisitenma pointer-table ROM offset | `0x57FD8` | `0x58258` |
| Validated 32 MiB expanded SHA-1 in existing research | `6ea0ed71032ce08fc2745f412d84936382197494` | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` |

Japanese source file *as uploaded*, before endian normalization, SHA-256: `881ea6adcb2c7a6fdb80bbc693f5f712e7f0c6a2973d5ace755939d5b1d21ffd`. Hashes above refer to local supplied exact retail images; the expanded hashes come from prior verified `decomp/recomp_rom_input.py` research, **not a new full rebuild on 2026-11-15**.

The pinned upstream `mnsg` checkout already has `config/japan_0/splat.yaml` and `config/japan_0/mnsg.sha1`. Its Makefile has `VERSION ?= usa` and a `COMPRESSED=yes` branch. Japanese `mnsg.uncompressed.sha1` is not tracked upstream; treat this as a build-target/configuration gap, not a reason to invent a hash. The `rommy.yaml` compression manifest is generated/ignored, not an additional ROM resource.

Existing evidence and scripts on the base branch:
- `practice/game_versions.py`: USA/JP retail identity; `practice/entrances.py`: byte-order normalization and block decompression.
- `decomp/recomp_rom_input.py` and `docs/JAPAN_RECOMP_INPUT.md`: exact 32 MiB USA/JP expansion with hard SHA-1 gates.
- `decomp/japan_function_map.py`, `decomp/japan_overlay_map.py`, `docs/JAPAN_FUNCTION_MAPPING.md`: candidate mappings. Japanese indirect function coverage and full runtime compilation remain **unknown**.
- `decomp/prepare_recomp_region_loader.py`, `docs/JAPAN_RECOMP_LOADER.md`: source-only regional decompressor preparation, not Japanese native runtime.
- Earlier `chatgptweb/dual-region-foundation` has `decomp/region_compare.py`; it diverged from the current decomp branch, so selectively port it with tests rather than merge 183 commits of unrelated difference.

## 3. Branch and source architecture

- Use `chatgptweb/japanese-decomp-port` for the research, plan and region-neutral tooling. Leave `main` and `chatgptweb/decomp` untouched. Keep existing Japanese toolkit fixes intact; do not modify active toolkit functionality to complete this track.
- In a local writable checkout, fork or vendor the *pinned* upstream `klorfmorf/mnsg`; preserve its `config/usa`, `config/japan_0`, `src`, `asm`, `bin`, Splat files and `tools` layout. Pin upstream and compiler checksums rather than tracking a drifting `main`.
- Select `VERSION=usa` or `VERSION=japan_0` explicitly. Output and reports must be fully region-scoped (`build/usa` vs `build/japan_0`, separate matching manifests, symbols and checksums). Do not let builds share generated `asm`/binary state accidentally.
- Prefer shared C only when both regions pass their own exact assembly/link/full-ROM proofs. Region-specific code/rodata, structure layouts, relocation labels and encoding belong in explicit per-region paths.
- Region maps must record **ROM offset, VRAM, overlay/section, function size, original bytes, equivalence class, evidence and confidence**; ROM offsets and VRAM values are not interchangeable.
- Any unknown regional mapping must be explicitly `unknown`, not guessed or inherited.

## 4. Phase-by-phase execution and exit gates

### P0 — Reproducible private source inventory (first gate)
- Record active branch HEADs, required upstream hashes, Python/uv, binutils, IDO 5.3 and existing decomp result hashes.
- Identify which existing branches implement candidate mapping, decompression, overlay symbols and source patching; do not copy experimental toolkit code unless needed.
- Ensure `practice/diagnostics`, extracted data, ROMs and build outputs remain ignored.
- **Exit:** source pins recorded, validated Japanese input and normalisation documented, no assets committed. DONE for header/hash/file-table inventory; complete upstream toolchain setup remains untested.

### P1 — Pinned Japanese baseline extraction
- In the pinned upstream `mnsg` checkout, supply **local canonical big-endian** `config/japan_0/baserom.z64` (ROM is ignored). Do not rename the swapped input without converting bytes.
- Prepare Linux dependencies from `README.md`: `uv`, `build-essential`, `binutils-mips-linux-gnu`; obtain the already-required pinned IDO 5.3 binary separately (it cannot be published).
- Run `make setup VERSION=japan_0` to generate `rommy.yaml`, the decompressed image, Splat outputs and generated symbol/link scripts. Compare the expanded SHA-1 against `6f8745fecc3a5e7d4918c7a73353eb0726116ded`.
- If `make setup` fails, capture exact stderr and reproduce each step with `tools/rommy.py`; reconcile file table, 16-byte alignment, compressed blocks and header checksums before modifying code.
- **Exit:** Japanese full Splat split succeeds with exact expanded hash and a recorded command transcript. Current status (2026-11-15): PARTIAL — independent 32 MiB Japanese decompression exact SHA-1 verified; Splat extraction NOT RUN (missing GNU MIPS toolchain/Splat Python dependencies).

### P2 — Baseline Japanese rebuild before migrating C
- In a clean separate worktree, build the unmodified Japanese Splat configuration using `make VERSION=japan_0 COMPRESSED=yes`. Verify against upstream `config/japan_0/mnsg.sha1`.
- Where existing USA C translation units fail on Japan, isolate them by region with original Japanese assembly; do not edit C until baseline emits an exact ROM.
- Independently establish a decompressed image comparison gate; track that Japan's `mnsg.uncompressed.sha1` isn't in the pinned upstream tree. Only add a checksum file after reproducing the actual bytes.
- For compressed rebuild failures, classify raw function/rodata mismatch versus recompressor instability; a correct decompressed binary does not by itself establish byte-identical retail compression.
- **Exit:** (A) exact expanded image and (B) exact compressed retail hash, each independently reported as PASS/FAIL/NOT RUN. Target A is prerequisite; target B is an additional milestone, not a hidden assumption.

### P3 — Overlay, function and relocation inventory
- Parse both `splat.yaml` configurations and reloc tables; enumerate executable main/entry sections and every overlay, their ROM ranges, VRAM and BSS.
- Run the existing verified `japan_function_map`/`japan_overlay_map` over complete 32 MiB images using upstream `Goemon64RecompSyms/mnsg.syms.toml` for candidate anchors.
- Require unique multi-instruction signatures and full-size bounds. Preserve ambiguous/short/missing candidates in a queue; classify exact bytes, relocated operands, code-shape-only and changed semantics.
- Verify overlay relocation records/targets and function pointers, not only instruction text.
- **Exit:** versioned per-overlay JSON with counts of confirmed, candidate, conflicting and `unknown` mappings. No unsupported universal US→JP offset.

### P4 — Region-aware matching-C harness
- Extend `decomp/verify.py`, `decomp/manifest.json` schema and `decomp/inventory.py` by **compatible opt-in region selection**, keeping default USA behavior unchanged.
- Select explicit upstream configs, base/reference ROM paths, compiler flags, build workdir, input SHA-1 and output hash per region. No in-place mutation of the USA manifest.
- Add integration tests for invalid/missing region, crossed ROM inputs, byte-order conversion, overlay boundaries and unchanged USA report schema.
- **Exit:** both region baselines can run independent verification; the USA full-ROM exact G2 proof is re-run on native toolchain before merge.

### P5 — First Japanese matching-C promotion
- Begin with short non-relocating helpers already matching in USA, but revalidate Japanese function ROM/VRAM, calling convention, arguments and codegen. Choose bounded candidates from the existing matching-C manifest.
- Compile using exactly pinned IDO flags. Compare isolated function bytes, original-vs-candidate linked overlay bytes, all applicable reloc sites/targets and entire rebuilt Japanese image.
- Preserve assembly fallback for nonmatching functions. Never count host-only semantic tests as native matching.
- **Exit:** at least one *newly proven* exact Japanese C replacement plus full Japanese build PASS, with a reproducible promotion ledger.

### P6 — Expand shared translation units safely
- Separate verified shared code from `usa` and `japan_0` specialisations. Avoid region-agnostic hardcoded addresses in C.
- Where Japanese text, animation timing, scripts, music, resources, character progress or cutscenes differ, keep region-specific content/logic explicit.
- Track counts independently: USA matching functions / Japanese matching functions / verified identical in both / unconverted assembly. Confirmed prior USA entries must not automatically increment the Japanese tally.
- **Exit:** at least one translation unit verified in *both* regions without breaking original-USA hashes.

### P7 — Japanese N64 gameplay verification
- Boot the exact Japanese rebuilt ROM in a real emulator (Project64 or native Linux Mupen64Plus); do not infer boot success from hashes.
- Record title, initial movement, Oedo south/north scene transitions, controller/character swapping, inventory, Japanese dialogue encoding, audio/music, boss overlays and save/load.
- Use native transition behaviour. Unknown region-specific scene pointers/addresses are `unknown`; the toolkit's runtime memory catalog can guide observation but must not supply assumed proof.
- **Exit:** gameplay smoke checklist with emulator version, ROM hash, expected/observed and reproduction steps. Hash equality and game runtime are separate gates.

### P8 — Japanese static recompilation, isolated follow-up
- Prepare a separately writable upstream `Goemon64Recomp` checkout or real GitHub fork. Run existing `recomp_rom_input` and `prepare_recomp_region_loader` against its *pinned* target source revision.
- Complete Japanese function symbols, entrypoint, overlay relocations, patches, ROM hash gating, file-table selection and asset data. Generate and link original Japanese instructions.
- Add a Japanese `GameEntry` only after its own symbol and function tables are genuinely linked. Keep original USA `GameEntry` byte-for-byte behaviour.
- Build Linux native with upstream CMake instructions and test title/gameplay/audio/saves. Mark any unported feature explicitly, including full recomp savestate behaviour.
- **Exit:** a native Japanese build *runs Japanese gameplay*, not merely accepts a file. Track independently from Track A.

### P9 — CI, documentation and merge policy
- Keep the existing `python3 -m decomp.local_ci` ROM-free gate; do not add GitHub Actions to emulate local ROM/compiler verification.
- Add Japanese ROM-free unit tests and fixture-based Splat/mapping tests. Execute native full-ROM proofs in a local checkout with private inputs; commit only JSON metadata, hashes and evidence.
- Every code change updates root `PROGRESS.md` in the same commit. Push completed work and check remote SHA. Each PR states what was actually run, and what remains unverified.
- Keep historical USA numerical counts and existing docs intact; reconcile only with authoritative generated inventory.
- **Exit:** green relevant tests, two region-specific build reports, no proprietary artefacts, independent review, explicit permission before merging into USA integration branch.

## 5. Immediate work queue (ordered)

1. **JPN-001** Create isolated branch and publish this plan and ROM inventory. *This commit.*
2. **JPN-002 — DONE (2026-11-15).** Added `decomp/prepare_japan_rom.py` with four ROM-free tests; a local end-to-end run converted the supplied byte-swapped Japanese ROM into hash-matching canonical `.z64` without overwriting the original.
3. **JPN-003 — DONE (2026-11-15).** Pinned mnsg checkout, Python 3.12/Splat/LZKN64, GNU MIPS binutils and source hashes verified from supplied offline archives.
4. **JPN-004 — DONE (2026-11-15).** Japanese Splat extraction and full 32 MiB source-linked assembly reconstruction match the original decompressed SHA-1 exactly.
5. **JPN-005 — DONE (2026-11-15).** Upstream Rommy recompressed the linked 32 MiB image into an exact 16 MiB Japanese retail ROM (0 differing bytes). Clean second rebuild reproduced both hashes.
6. **JPN-006 — DONE (2026-11-15).** Implemented `decomp.region_verify` preserving the USA entry point and independently verifying Japanese source hashes, original C objects, ELF symbols, linker VMAs, plus exact complete 32 MiB/16 MiB ROMs. 21 focused tests PASS. See `docs/REGION_VERIFY.md`.
7. **JPN-007 — DONE; UPDATED FIVE-C INVENTORY (2026-11-15).** 7,376 positive-sized Japanese linked-ELF entries across 73 sections; 7,371 ASM-marked, 5 reviewed C, 0 unreviewed unmarked. Previous four-C inventory retained separately.
8. **JPN-008 — 6 FUNCTIONS PROVEN (2026-11-15).** Native Japanese IDO 5.3 matching-C now totals 6 functions / 200 original code bytes across 4 C translation units. Sixth 32-byte float parameter helper at ROM 0x13B70. Both 32 MiB linked and 16 MiB retail ROM images remain exact; strict source/ELF and 37 unit tests PASS. See docs/JAPAN_SIX_C.md.
9. **JPN-009 — PARTIAL (2026-11-15).** Fresh pinned upstream USA reference 32 MiB and 16 MiB exact build passed; Japanese five-C source-linked and retail ROMs remain exact. Fresh full USA Goemon-64-Tools matching-C G2 remains NOT RUN.
10. **JPN-010 — EMULATOR NOT RUN (2026-11-15).** Emulator Japanese gameplay smoke tests; independently decide whether to begin Track B runtime port.

## 6. External resources, accessibility and blockers

| Resource | Known source | Status |
| --- | --- | --- |
| USA and Japanese retail cartridges | User-supplied local project files | **Available privately**, identified |
| Japanese `japan_0` Splat config | `klorfmorf/mnsg` at pinned commit | **Available** |
| Japanese compressed SHA-1 expectation | `config/japan_0/mnsg.sha1` | **Available** |
| Japanese expanded SHA-1 | Current code/docs `decomp/recomp_rom_input.py` | **Recorded**, recompute under P1 |
| IDO 5.3 native compiler | Existing private pinned USA workspace | **Required; not supplied or redistributed through GitHub** |
| MIPS binutils, `uv`, Splat, LZKN64 | Upstream Makefile, `uv.lock`, Ubuntu packages | **Publicly documented; local installation not tested here** |
| USA N64Recomp symbols | `klorfmorf/Goemon64RecompSyms` | **Public** |
| Japanese symbols and patch table | Not completed in existing research | **Must be generated** |
| Separate upstream GitHub fork | GitHub fork/create-repo API | **Unavailable through current connector**; branch created instead |
| Japanese native gameplay test | Writable native build + emulator/desktop | **Not run** |

**Stop conditions:** uncertain ROM identity, code/overlay size mismatch, missing pinned compiler, mistaken USA/JP address equivalence, unverifiable output hashes, or untested runtime claims. Investigate and record rather than bypass equality gates.

## 7. Definition of success

- **A1:** Japanese rev-0 ROM securely accepted and normalized; metadata independently validated.
- **A2:** Japanese 32 MiB decompressed image reconstructed byte-for-byte.
- **A3:** Japanese N64 retail build reproduced bit-for-bit (additional compression gate).
- **A4:** Japanese matching-C function count increases with strict original-address proofs and USA remains exact.
- **A5:** Rebuilt Japanese game boots and plays in N64 emulator with Japanese scripts/audio.
- **B1:** Separately built PC `Goemon64Recomp` Japanese target loads verified original Japanese ROM and runs a gameplay smoke test.
- **B2:** USA PC static-recomp target continues to work and neither release contains copyrighted ROM assets.

Update each criterion as **PASS**, **FAIL** or **NOT RUN**, with reproducible evidence. Never merge or label a branch complete based on candidate mappings alone.

### 2026-11-15 dependency archive follow-up

The private `goemon-dependencies.tar.gz` supplies all four GNU MIPS executables and pinned Splat/Python packages, but it is **not independently portable**. Exact ELF loader failures: `libbfd-2.45.90-mips.20260125.so`, `libopcodes-2.45.90-mips.20260125.so`, `libctf-mips.so.0`, `libsframe.so.3`. The venv interpreter symlink targets an absent external uv-installed Python 3.12 base distribution. Python 3.13 cannot import its CPython 3.12 `lzkn64` and `rabbitizer` native extension modules.

**New verified gate:** The pinned upstream `tools/rommy.py decompress` completed and generated its own `rommy.yaml` using an isolated, pure-Python fallback for the LZKN64 decoder. The resulting **32 MiB Japanese reference image exactly matches** `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. This does not verify Splat or the source-linked 16 MiB image.

On the machine with the original Ubuntu tools and `mnsg-japan/.venv`, run:

```bash
bash decomp/package_japan_offline_runtime.sh "$HOME/Desktop/mnsg-japan/.venv" "$HOME/Desktop/goemon-runtime-additions.tar.gz"
```

Keep the resulting tarball **private**; it contains development runtime binaries, not game ROMs. Upload it to the conversation, **not** to GitHub. The script refuses to archive system-wide `/usr` prefixes or overwrite existing output.

See `decomp/results/japan_0_offline_dependency_audit_2026-11-15.json`. Native Splat/linked build status: NOT RUN.

## 2026-11-15 original ROM rebuilt exactly

Using the two supplied dependency archives and pinned mnsg checkout, the actual Splat extraction passed. A separate assembly-only region configuration (189 C descriptors replaced with ASM), 22 generated cross-object labels exported, and 2 clashing BSS labels renamed allowed the Japanese assembly to link. The original **32 MiB** decompressed image and **16 MiB** retail compressed image both matched the independent originals **byte-for-byte (0 differences)**; the clean second source rebuild repeated both. This milestone is strictly original Japanese N64 **assembly**, not new matching C and not a PC-native version. Reproduction helper, tests and proof are in docs/JAPAN_ASM_BASELINE.md and decomp/results/japan_0_asm_baseline_2026-11-15.json. Next: JPN-006 region-aware matching verifier.

## 2026-11-15 first Japanese matching C

Beyond the exact all-ASM 32 MiB and 16 MiB baselines, the Japanese toolchain now replaces original ROM offset 0x38620 with native C function func_80037A20_38620. IDO's 16-byte object text matched the original bytes, with no text relocations. The **mixed 1-C / remaining-ASM full image** matched the exact 32 MiB Japanese decompressed ROM, and upstream Rommy produced the exact 16 MiB retail cartridge. This is 1 Japanese matching-C function (8 code bytes); it does not modify the USA C count. See docs/JAPAN_FIRST_C.md and decomp/results/japan_0_first_c_2026-11-15.json. This test does not prove Japanese PC-native gameplay or more substantial source reconstruction.

## 2026-11-15 three new Japanese functional C matches

The Japanese source port now has four native IDO matching-C functions (136 bytes): the prior trivial 8-byte empty helper and three functional bit-array helpers of 36, 40 and 52 bytes, using previously verified USA semantics but freshly verified Japanese original addresses. Their combined 128-byte compiled object text equals the Japanese original bytes with no text relocations. Full 32 MiB N64 link and 16 MiB Rommy recompression remain byte-identical. Ten focused ROM-free regression tests pass. JPN-006 general region-aware verifier, Japanese PC-native gameplay and fresh USA G2 remain uncompleted. See docs/JAPAN_FOUR_C.md and decomp/results/japan_0_four_c_2026-11-15.json.

## 2026-11-15 JPN-006 verifier milestone

The region-aware verification entry point now accepts `--region usa` (unchanged existing USA verifier) and `--region japan_0` (strict separate manifest and source-linked Japanese object/ROM proof). All 4 current Japanese native matching-C functions / 136 function bytes pass source SHA-256, compiled object code and symbol extents, linker VMA ownership, and exact complete 32 MiB and 16 MiB ROM comparisons. 21 focused ROM-free tests passed. No further C promoted. Full Japanese function inventory and a new USA G2 remain outstanding. See `docs/REGION_VERIFY.md`.

## 2026-11-15 independent Japanese ELF inventory

After strict Japanese original-address/source/whole-ROM verification, GNU MIPS objdump on the real linked Japanese ELF identified 7,376 positive-sized F symbol entries across 73 executable sections, including entry and IPL3 placeholders. Explicit `.NON_MATCHING` markers classify 7,372 as assembly and the four unmarked entries match all four reviewed native Japanese C functions (136 bytes). Same-section aliases and unreviewed unmarked entries: zero. The full per-section inventory is in decomp/results/japan_0_elf_inventory_2026-11-15.json; tools and tests in decomp/japan_inventory.py and decomp/test_japan_inventory.py. Five new and 21 prior focused tests pass (26/26). Further C promotions and Japanese PC native runtime remain outstanding.

## 2026-11-15 five Japanese native matching-C functions

Function `func_80012160_12D60` (32 bytes; mode byte and three floats) is the fifth native IDO original-address C promotion. Its compiled object matches the original 32 bytes with zero text relocations. Strict region verifier confirms the C source hash, exact ELF/linker symbol at VMA 0x80012160, and a zero-difference full **32 MiB** linked image and **16 MiB** original retail cartridge. Japanese total now **5 functions / 168 C function bytes**, 3 C units; 7,371 ELF function entries remain explicitly assembly-marked. The original four-C manifest is preserved for historic verification. Focused ROM-free tests: 32/32 pass. Full single-command runner was interrupted during reassembly; resuming its native Make objects, recompression and verification succeeded. See docs/JAPAN_FIVE_C.md and decomp/results/japan_0_five_c_2026-11-15.json. Fresh USA native G2 and gameplay are not verified.

## 2026-11-15 USA reference proof and Japanese PC codegen readiness

Ran fresh pinned upstream USA Rommy/Splat/MIPS link and retail recompression. The 32 MiB reconstructed source image and 16 MiB retail output each matched their original USA SHA-1 exactly, with no differing bytes. This validates the source/toolchain baseline, not the current USA private decomp matching-C manifest/G2. Separately, a Japanese native PC codegen preparation utility parsed the existing verified original-address Japanese 5-C linked ELF into 72 executable sections, 7,375 positive-sized ELF function symbols (IPL3 excluded), and 57 candidate overlay names. Generated candidate N64Recomp symbol/config TOMLs parse successfully; six synthetic tests passed; source derived entirely from the Japanese build, without copying USA addresses or instruction patches. It is NOT a functioning Japanese PC executable: actual N64Recomp CPU generation, RSP, Japanese GameEntry and native linkage are NOT RUN. Japanese emulator boot/gameplay remains blocked by lack of a runnable N64 emulator in the provided container resources. See docs/JAPAN_PC_CODEGEN_PREP.md and the two hash-only verification reports.

## 2026-11-15 Japanese six-function original-address matching C

The sixth function `func_80012F70_13B70` (VMA 0x80012F70, 32 bytes) compiles byte-identically under original IDO 5.3, links at its original address with 0 text relocations, and preserves both full Japanese ROM SHA-1 values exactly. Japanese total is **6 matching-C functions / 200 bytes**, with **7,370** assembly-marked positive-sized ELF entries and zero unexplained unmarked entries. Source-based six-C Splat variant and build script were added, historic five-C manifest preserved, 37/37 focused tests passed, native strict 32 MiB and retail 16 MiB full-ROM proofs passed. See `docs/JAPAN_SIX_C.md` and `decomp/results/japan_0_six_c_2026-11-15.json`. The one-command wrapper is syntax-tested; individually executed stages establish the complete real build. Emulator, full USA private G2 and Japanese PC native runtime remain unrun.

## 2026-11-16 nine Japanese C functions

Retains the concurrent six-function/200-byte baseline and adds three original-address 16-byte C mode setters. Nine matching-C functions / 248 original bytes / five translation units reproduce the Japanese 32 MiB expanded ROM and original 16 MiB retail ROM byte-for-byte. Reviewed six g_system relocations. ELF inventory: 7,376 entries, 7,367 ASM-marked, nine C. Native proof PASS; modified formal region verifier and one-command runner NOT RUN after writing. Details: docs/JAPAN_NINE_C.md.

## 2026-11-16 tenth Japanese C and next candidate

Native IDO 5.3 compiled the 32-byte `func_80036D00_37900` warp-adjacent dispatcher at Japanese ROM `0x37900` / RAM `0x80036D00`. It issues `func_8000364C_424C(15)` with one original-address `R_MIPS_26` call relocation. Full re-extraction, MIPS link and Rommy recompression were byte-identical to the Japanese expanded and retail ROMs. Current C total: **10 functions / 280 code bytes**, 7,366 assembly-marked ELF entries. The next function `func_80036D20_37920` has 56 matching compiled instruction bytes but an 8-byte trailing alignment pad that would overwrite the next live assembly function. It is NOT PROMOTED until the object is safely packed and both ROMs still match. The updated formal 10-C runner and test suite have NOT been executed end-to-end. See `docs/JAPAN_TEN_C.md`.

## 2026-11-16 additional Japanese warp-function candidates (NOT PROMOTED)

An isolated native IDO 5.3 + original-address LLD comparison found **eight exact Japanese warp C functions / 476 candidate bytes**. Two fit their original size with no instruction tail trim (96 and 64 bytes); six require reviewed zero-only ELF section metadata size/alignment reductions before an original GNU MIPS full linker build. All 8/8 local probes, 4/4 ROM-free tests and a mutation negative check PASS. None passed the new complete 32 MiB/16 MiB Japanese ROM gates, so the formal Japan count stays **10 functions / 280 bytes**. The candidate technical inventory and proof SHA-256s are in `docs/JAPAN_WARP_ELIGIBILITY_2026-11-16.md` and `decomp/results/japan_0_warp_eligibility_2026-11-16.json`.

## 2026-11-16 verified native Japanese eighteen-function ROM milestone

Eight adjacent Japanese warp/transition C functions (476 bytes) are now formally integrated alongside the previous ten (280), totalling **18 exact original-address C functions / 756 instruction bytes across 14 translation units**. Native IDO, GNU MIPS full 32 MiB link and upstream Rommy recompressed original 16 MiB ROM both match their Japanese references byte-for-byte. A clean second checkout completed the new self-contained build runner and strict independent source/reloc/ELF/ROM verifier. Guarded zero-only ELF metadata packing and generated main-section four-byte subalignment were necessary; no original instruction or relocation bytes changed. Japanese ELF C/ASM inventory 18 / 7,358, 7,376 total entries, zero unexplained. Eight focused unit tests pass. Still ASM: five adjacent 204/208/100/192/92-byte routines; full USA private G2 and Japanese emulator/native PC are separate outstanding gates. See `docs/JAPAN_EIGHTEEN_C.md` and `decomp/results/japan_0_eighteen_c_2026-11-16.json`.
