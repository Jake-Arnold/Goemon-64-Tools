# Decomp continuation runbook

Start here when continuing the matching-C work. This is the operational handoff;
README.md explains the recovered units, BATCH_PIPELINE.md describes the tools,
and checkpoint documents retain technical research/history. Read root AGENTS.md
first. Update this runbook whenever the next targets or machine paths change.

## 0. Cross-conversation handoff

Read [MASTER_WORK_QUEUE.md](MASTER_WORK_QUEUE.md) for the reconciled VM and overlay matching-C backlog; historical main-branch warp/story tasks have been superseded from parallel Goemon conversations. Historical chat totals may lag the latest manifest/proof; this runbook and the live branch remain authoritative. Do not repeat already promoted functions.

## 1. Establish the current state

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
| VM text loop `func_8003DBEC_3E7EC` | Latest standalone candidate compiles to original 472-byte symbol, but is unpromoted: 47/95 equal non-relocation instruction positions without original-address relocation, 0x50 vs original 0x48 stack frame. 10,000 MIPS/C synthetic differential cases passed. Recover register lifetimes and branch scheduling; do not change proof counts. |
| Choice edge `func_8003D0B0_3DCB0` (COMPLETED) | Promoted 204-byte exact C at original address. Fresh 2,331-object compile with regenerated Splat sources gave 33,554,432/33,554,432 matching bytes, all 141 function proofs and unchanged 7,376-entry inventory. 100 host cases passed. Uninterrupted formal verifier still pending. |
| VM loader `func_8003D468_3E068` | Needs resource-prefix interfaces. Derive fields/calls from actual loads and upstream declarations. |
| Key initializer `func_080001BC_6F369C` | Public `candidates/key_spawn_gate.c` matches 96 bytes in an isolated linked probe. Promotion requires reviewed overlay mapping/layout support in verifier, then complete-ROM proof. |

Other known limits:

- `/root/goemon64-vm-target-context-v1` retains the earlier VM context scan.
  Controller D17C from that scan is now solved; do not redo its old failed draft.
- Comparator D9B8 remains ASM. `vm_compare_reference.h` is host-only semantics.
- Wrapper F6E8 has a boundary/unreachable-return discrepancy; natural 40-byte C
  does not establish the original function extent. See inventory size annotations.
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
