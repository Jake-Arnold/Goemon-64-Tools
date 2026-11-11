# Executor protocol — Goemon 64 matching-C (mandatory for every task)

This document is designed for a comparatively weak, stateless code-execution model. It is an algorithm, not prose encouragement. Perform only the numbered task currently assigned; use the actual branch and files, never reconstructed assumptions from chat history.

## Source authority, truth and branch
1. Work only on `Jake-Arnold/Goemon-64-Tools` branch `chatgptweb/decomp`. Do not merge, reset or change `main`. Never force-push. Preserve unrelated working trees.
2. Read root `AGENTS.md`, `decomp/CONTINUE.md`, `decomp/manifest.json`, `decomp/results/combined.json`, `decomp/results/inventory.json`, this protocol, the assigned phase, and the task's exact focus files.
3. Check live `git fetch origin`, `git status --short`, `git branch --show-current`, `git rev-parse HEAD`, and remote ref before each implementation. Verify fresh proof if current HEAD has moved; do not substitute an older 136-function archive.
4. The starting recorded baseline is **142 newly matching functions, 10,652 original MIPS bytes, 155 total C, 7,221 ASM**, and a recorded `formal_verifier_run_completed=true` ROM proof. Recompute if the branch moves.
5. Confidential input stays local: retail USA ROM SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; decompressed exact 33,554,432-byte ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Do not download or commit ROMs, generated ASM, binaries, saves, user diagnostics, passwords, memory dumps or toolchain archives.
6. Upstream `klorfmorf/mnsg` pin is `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; tools include the pinned native IDO 5.3, Splat 0.36.3 and MIPS cross-binutils. Do not replace native IDO by host GCC for MIPS proof. Compare original code at its true VMA and verify relocations.

## State machine: no false promotions
`PLANNED -> INSPECTED -> HOST_TESTED -> ISOLATED_EXACT -> UNIT_EXACT -> FULL_ROM_EXACT -> PUBLISHED`.
A task may remain `BLOCKED` or `RESEARCH_ONLY`. States are NOT interchangeable:
- `HOST_TESTED`: synthetic semantic tests only; no original binary proof.
- `ISOLATED_EXACT`: single native candidate function linked at original address, not an original source unit or full image.
- `UNIT_EXACT`: all functions (including prior siblings) in the actual translation-unit text match. Not enough for promotion.
- `FULL_ROM_EXACT`: fresh, complete project build; original-address claimed functions exact; complete 33,554,432 bytes identical; original symbols, alignment, sections, readelf inventory and source fingerprints valid.
- `PUBLISHED`: committed status and verification metadata, `PROGRESS.md` updated, remote SHA checked.
Never update official count, manifest ownership, `results/combined.json` or inventory from any lesser evidence.

## Always execute in this order
1. **Identify task and prerequisites.** Look at the task ID, dependencies and all relevant live files. If an earlier task is blocked but not a true prerequisite, continue with a separate independent unit. If a target is already accepted, report `SKIPPED_ALREADY_COMPLETE`.
2. **Establish original boundary.** From pinned ROM and assembly determine function name, actual ROM offset, actual VMA, original length/hash, and enclosing source translation unit. Preserve original instruction order and branch-delay slots. For an overlay, use its own mapping (not main-segment formula).
3. **Recover interfaces.** Read actual caller(s), callee(s), global widths/offsets, assembly loads/stores and source sibling declarations. Use an opaque type and offset when uncertain; don't invent ABI or meaning.
4. **Write one minimal hypothesis.** Prefer fixing field width/signedness/aliasing/branch order over a full rewrite. Keep unknown functions as `GLOBAL_ASM`. Never patch raw instructions or weaken verifiers.
5. **Execute semantic tests.** Make positive and negative cases, include callback mutation, null and boundary paths when applicable. Use ASan/UBSan as appropriate. Record exact command and tested source digest. `test passed` is not `MIPS matched`.
6. **Compile native original unit.** Use pinned original flags, compare original instruction bytes and relocations at original address; include all neighboring functions. Exact size alone is insufficient. `decomp/prove_integrated_units.py` is *expected to fail* on the known object dispatcher until that codegen discrepancy is fixed.
7. **Run complete-ROM gate.** Use fresh workdir + report, all objects/Splat/IDO, previous accepted functions, symbols and inventory. The previous baseline comprised 2,331 objects; verify current counts rather than hard-coding that number as a pass condition.
8. **Decide.** All comparisons exact: candidate can be promoted and evidence updated. Any mismatch, absent private ROM, failed compiler or interrupted verifier: no promotion. Keep current ASM and record first mismatching word/register/relocation along with bounded next hypothesis. Do not alter a previously approved result to claim success.
9. **Publish only coherent work.** Review `git diff --check`, `git status --short`, staged paths, new proof hashes; update root `PROGRESS.md` with date, reason, commands actually run, measured outcome, limitations, next action. Push only branch, check remote commit SHA. Do not invent a push.
10. **Leave a handoff.** Update the task ledger with `PASSED_G2`, `RESEARCH_ONLY`, `BLOCKED_INPUT`, `FAILED_NATIVE`, `FAILED_ROM`, `SKIPPED_ALREADY_COMPLETE` or `DOC_ONLY`, never generic "done". State exact next candidate.

## Exact repeatable commands
Run in the toolkit repository root on Linux/WSL; variables are local inputs and must not be included in commits:
```bash
git fetch origin
git status --short
git branch --show-current
git rev-parse HEAD
git ls-remote origin refs/heads/chatgptweb/decomp
python3 -m unittest discover -s decomp -p 'test_*.py' -q
python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch \
  tests.test_decomp_probe_integration tests.test_decomp_elf_layout \
  tests.test_decomp_inventory tests.test_decomp_baseline_cache \
  tests.test_pickup_placements -q
```
For a fresh verifier **without relying on a certified baseline cache**:
```bash
: "${GOEMON_ROM:?Set path to privately owned original USA retail ROM}"
: "${GOEMON_UPSTREAM:?Set path to clean pinned mnsg checkout}"
tag="$(date -u +%Y%m%dT%H%M%S)-goemon"
workdir="/tmp/${tag}-build"
report="practice/diagnostics/${tag}-verify.json"
python3 -m decomp.verify \
  --upstream "$GOEMON_UPSTREAM" \
  --workdir "$workdir" \
  --retail-rom "$GOEMON_ROM" \
  --report "$report" --uv "$(command -v uv)" --jobs 2
python3 -m decomp.inventory \
  --baseline "$workdir/baseline" \
  --candidate "$workdir/candidate" \
  --report "practice/diagnostics/${tag}-inventory.json"
```
**Do not run the inventory command if verifier fails.** Work/report paths must not exist in advance. An optional cached baseline may only be used with the verifier's validated `--baseline-cache` provenance. For a private original **decompressed** ROM, once the exact IDO/linker paths are verified:
```bash
python3 -m decomp.prove_three_wrappers --rom "$GOEMON_DECOMPRESSED" --ido "$GOEMON_IDO"
python3 -m decomp.prove_three_menu_flags --rom "$GOEMON_DECOMPRESSED" --ido "$GOEMON_IDO"
python3 -m decomp.prove_integrated_units --rom "$GOEMON_DECOMPRESSED" --ido "$GOEMON_IDO"
```
The last command intentionally exits nonzero with the current object unit; never redefine success to suppress it. Read each script's `--help` to supply actual linker/objcopy/readelf paths if defaults are absent. Follow `CONTINUE.md` if the toolchain requires a curated `--binutils-root`.

## Strict evidence record (one per attempted task, sanitized JSON)
```json
{
 "task_id":"G64-005","branch":"chatgptweb/decomp","base_sha":"<actual>",
 "function":"func_80034ED4_35AD4","original_rom_offset":"0x35AD4",
 "original_vma":"0x80034ED4","original_bytes":36,
 "source_sha256":"<actual>","toolchain":"<version-and-hash>",
 "semantic_tests":{"status":"PASS|FAIL|NOT_RUN","cases":0},
 "isolated_proof":"PASS|FAIL|NOT_RUN",
 "whole_unit_proof":"PASS|FAIL|NOT_RUN",
 "complete_rom_proof":"PASS|FAIL|NOT_RUN",
 "inventory_proof":"PASS|FAIL|NOT_RUN",
 "status":"RESEARCH_ONLY|BLOCKED_INPUT|FAILED_NATIVE|FAILED_ROM|PASSED_G2",
 "mismatch":{"first_rom_offset":null,"original_instruction":null,"candidate_instruction":null,"root_cause_hypothesis":null},
 "published_commit":null
}
```
All placeholders above must be replaced with facts or explicit null/NOT_RUN. Do not fabricate test counts, sha, versions or evidence. Store private original bytes/objdump locally and publish only safe hashes and summary metadata.

## Known exact baseline blockers and tricks
- Five *whole-research-unit* matching functions: resource wrappers at `0x35AD4` and `0x35B20` (36 each); menu B60/BB4/C04 (84/80/84). They still require G2 full-ROM production proof.
- Object dispatcher `0x35C94` (48) matched standalone but mismatches eight bytes in the combined 96-byte source unit: original `sw $ra` before `lui`; candidate reversed at ROM `0x35C9C/0x35CA0`. Eleven variants already failed; keep ASM.
- Menu disable needs literal `0xFF7F` source mask for native ANDI schedule. Nested menu helper's extra cached local changed registers and was removed in matching research.
- VM resource half-index 196 bytes is only `25/42` directly comparable non-relocation positions; loader original 548 bytes versus 560 in old candidate. Callback can mutate global resource ID.
- Text loop original stack frame is `0x48` versus candidate `0x50`; preserve branch-likely slots. Stream walker is 232 original versus 228 research; branch-likely `bltzl` differs.
- VM wrapper F6E8 original is **48** bytes, not a 56-byte candidate inventory annotation; an apparently matching 40-byte prefix is insufficient.
- Overlay `file_43` uses ROM `0x6F34E0..0x6FB200`, VMA `0x08000000` and distinct rodata boundary. Key initializer 96 bytes isolated, Ghost 140-byte probe has `sp+0x18` versus original `sp+0x1C` twice; neither is promoted.
- Upstream `camera` branch was research-only and had a source-generated `memset` linker mismatch. Do not import wholesale or create synthetic linker alias.
- Previously attempted scalar sweep included 762 functions. Repeating unchanged broad recipes is wasted effort; improve typed context and target selection.

## How to respond to a blocker
When expected tool/file/ROM is absent: write `BLOCKED_INPUT`, list the exact missing artifact (without requesting user secrets), and continue only an independently doable research task. When candidate compiles but mismatch remains: record exact first differing word and categorise it, then stop after a bounded hypothesis batch and preserve the ASM. If the source changes during verification: mark current proof stale and restart from a fresh snapshot. Do not claim full-ROM progress from old proof JSON.

## Session completion / handoff template
```text
Branch and base SHA:
Task IDs and final states:
Files actually changed:
Original function offsets/sizes:
Semantic command + observed result:
Native IDO original-address match:
Full original translation-unit match:
Full 32 MiB ROM exactness + inventory:
Reported new matching function count (only from G2):
Commit SHA + verified remote SHA (or NOT PUSHED):
Unresolved first mismatch and next bounded hypothesis:
```
