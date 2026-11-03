# Decomp continuation runbook

Start here when continuing the matching-C work. This is the operational handoff;
README.md explains the recovered units, BATCH_PIPELINE.md describes the tools,
and checkpoint documents retain technical research/history. Read root AGENTS.md
first. Update this runbook whenever the next targets or machine paths change.

## 1. Establish the current state

Continue this ongoing task in its existing workspace:

- Windows: `C:/Users/Jake/.codex/worktrees/goemon-entrance-warps/Goemon Toolkit`
- Branch: `main` (the workspace directory retains its original name)
- WSL cwd: `/mnt/c/Users/Jake/.codex/worktrees/goemon-entrance-warps/Goemon Toolkit`
- Remote: `Jake-Arnold/Goemon-64-Tools`

Run `git status --short`, `git branch --show-current`, `git rev-parse HEAD` and
`git fetch origin`. Preserve unrelated changes. A separate new task requires a
fresh verified-origin/main workspace; a continuation does not. Do not merge or
delete other branches/worktrees just to tidy the list. Check ancestry first.

Integration on 2026-11-03: the completed entrance-warps branch included main
and both older feature branches. Its history is fast-forwarded into `main`;
continue on main in this same workspace. Redundant branch refs can be removed
without deleting worktrees. Older worktrees retain their original commits in
detached HEAD state; leave their local bookmarks, checkpoints, ROMs and research
artifacts untouched. The primary checkout is also retained at its original commit.
Recheck `git branch --show-current`, fetched remote state and worktree status
before future work; do not use an older detached checkout for new implementation.

Current checkpoint (2026-11-03): 97 newly matching functions / 7,260 bytes in fifteen
units. Including 13 upstream C entries: 110 of 7,376 identified entries, leaving
7,266 ASM entries (including SDK/runtime). VM: 52 C / 17 ASM.

Treat these as a dated snapshot. For current claims, read:

1. `manifest.json`: claimed functions and retained assembly.
2. `results/combined.json`: latest successful complete-ROM proof and source hashes.
3. `results/inventory.json`: whole-build counts.

Older JSON/checkpoints are historical evidence. Do not rewrite them to imply a
new run. An isolated linked match, plausible C, or zero permuter score does not
count as a full-ROM-verified function.

## 2. Use the existing Linux tools

All commands below run in Ubuntu WSL, from the toolkit cwd above. From PowerShell,
enter with `wsl -d Ubuntu`, then `cd` to that quoted WSL path. Compiler inputs must
use LF line endings; do not build from a CRLF-converted mnsg checkout.

Machine-local paths (verify existence before use; never commit their contents):

| Purpose | Path |
| --- | --- |
| Pinned clean upstream | `/root/goemon64-verified-vm-context-v2/baseline` |
| Certified immutable baseline | `/root/goemon64-batch-gate-fresh-v1/baseline` |
| Latest verified candidate | `/root/goemon64-decode-loop-v1/candidate` |
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

Next targets, in useful order:

| Target | Existing evidence / next action |
| --- | --- |
| VM text loop `func_8003DBEC_3E7EC` | Original 472 bytes; draft 480, with 101 differing words. Resolve cursor/halfword input fields and control flow before register tuning. Private draft: `/root/goemon64-text-loop-v1`. |
| Choice edge `func_8003D0B0_3DCB0` | Original 204 bytes; drafts 200/208. Final conditional/unreachable-store shape unresolved; volatile variants failed. Private attempts: `/root/goemon64-choice-edge-v1`. |
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
  `git ls-remote origin refs/heads/main`.
- Report verified progress and any real blocker. Never claim an unperformed push,
  runtime test, merge, or decompilation promotion.

Do not close existing toolkit windows or disrupt pending captures/freezes. Do not
install rebuilt ROMs, write game memory or enable raw warp shortcuts as part of
native reconstruction. Keep the companion and native C research boundaries intact.
