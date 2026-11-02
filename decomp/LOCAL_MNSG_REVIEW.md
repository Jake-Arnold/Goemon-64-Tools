# User-specified local mnsg checkout: findings and reuse

Date: 2026-11-02. The user asked to inspect their local mnsg checkout before
continuing. The checkout's tracked files and branches were not changed, reset,
cleaned or switched. Its worktrees and existing build products were preserved.
Experiments used new WSL scratch clones; no external upstream submission occurred.

## What was already available

| Item inspected | Observed result | Usefulness |
| --- | --- | --- |
| Main checkout | Clean `main`, commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, upstream klorfmorf/mnsg | Same baseline as our existing matching track; no extra main-branch C files to claim as new work |
| Retail ROM | SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66` | Matches the original US reference |
| asm-differ submodule | `4eb23bcd4bbeab81c16535c6318389e0c55584f7` | Existing pinned comparison tooling |
| m2c submodule | `a21c1dcd7255b176c032bb932f521846e98d4372` | Same decompiler pin already used |
| decomp-permuter submodule | `ec2efeebb33e2b1de81e39fbf7cbe3cd97350472` | Fully initialized here; used locally for the unresolved spawn-copy function |
| Pre-existing managed build worktree | Same baseline commit, clean tracked state; existing uncompressed and recompressed outputs | Their SHA-1 values match `6ea0ed71032ce08fc2745f412d84936382197494` and the retail SHA above; observed output identity is separate from our independently executed fresh builds |
| `origin/camera` ref | `f1a86c328be09d2d35a8d0817bd41e67783d343a`; remote ref confirmed at the same commit | Substantial pre-existing camera source/structure work to reuse as reference |

No additional hidden reconstructed functions were found on the inspected local
main/build branch. The camera branch is a separate source of prior work, not our
new reconstruction or an established fully matching baseline.

## Local permutation resolved the remaining save routine

The initialized permuter was run from the user checkout with bytecode-cache writes
disabled, against a separate WSL scratch checkout. Its importer recovered the
pinned Makefile's IDO flags and the original generated assembly target for
`func_8000B718_C318`. Execution used **two local workers**, not distributed mode.
No source/ROM was uploaded to remote compute.

The starting score was 880. A generated candidate scored zero by repeating the
direct global table/index expression for the first five halfword assignments,
while retaining the saved pointer for the last field. This changes IDO's alias/
scheduling choices without changing the intended valid-input behavior. The source
expression shape is retained; simplifying it requires another matching check.

A zero permuter score alone was not accepted as proof. The candidate was inserted
into the full unit, rebuilt, and then checked again through the fresh baseline/
candidate verifier. **All 25 functions / 1,876 function bytes match**, and the
whole 32 MiB output still has SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
The prior assembly placeholder is gone and the function's assembly marker is
absent from the candidate ELF. The current selected units have no retained
assembly placeholders; the rest of the game's untouched assembly is still present.

The expanded sanitizer-enabled host test checks three synthetic table records,
all six field destinations including negative-coordinate encodings, preservation
of unrelated state, saved health/lives minimums, unchanged live resources and the
complete shadow copy. The table index remains unchecked like the original; this
is not a new safe warp or checkpoint API.

## Camera branch: useful draft, not accepted as matching

The [existing camera branch](https://github.com/klorfmorf/mnsg/tree/f1a86c328be09d2d35a8d0817bd41e67783d343a)
adds about 4,600 source lines in `src/overlay_11/camera.c`, new symbol annotations
and a layout split at ROM `0x58E2D0..0x5957F0`. It includes provisional camera
structure maps, callbacks and reconstructed functions, without assembly placeholders.
That is valuable prior research, but source volume is not matching proof.

An isolated clone at that exact commit completed setup and compilation but failed
at link with **undefined reference to `memset`**, originating in
`func_801D27A4_58E6B4` (`.text+0x404` in the camera object). The original routine
contains an inline word-clearing loop; treating the missing call as a harmless
link alias would not establish the original code or register behavior. No linker
alias, source patch or synthetic success claim was applied to the user's checkout.

This branch was therefore **not integrated into the matching manifest**, and no
camera functions were added to our count. Its field descriptions are provisional
and must be checked against original accesses when used. The next camera step is
to repair the initializer in an isolated research copy, build it, and measure
actual per-function differences before selecting which routines to integrate.

## Evidence retained

Current clean published build metadata: [combined.json](results/combined.json).
Previous 24-function checkpoint: [save_resources_partial.json](results/save_resources_partial.json).
The earlier 12/15-function results are retained too. Full import/permutation
inputs, score/source outputs, failed camera logs and build artifacts remain in
local/ignored research storage; ROMs, disassembly and upstream tool copies are
not bundled in this repository. The original local checkout still has a clean
tracked working tree after inspection/tool use.
