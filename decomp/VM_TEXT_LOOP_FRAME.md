# VM text-loop frame investigation

**G64-032 — research only.** The matching target is
`func_8003DBEC_3E7EC` at VMA `0x8003DBEC`, ROM offset `0x3E7EC`, with a
ROM-verified extent of 472 bytes. Its original assembly ownership remains in
place.

## Original and candidate stack layout

The original reserves `0x48` bytes. It saves the callee-saved registers and
return address at these offsets; `sp+0x44` holds the outer-loop counter.

| Register/local | Original slot | IDO alias candidate slot |
| --- | ---: | ---: |
| `$s0` retry counter | `sp+0x18` | `sp+0x18` |
| `$s1` work-global address | `sp+0x1C` | `sp+0x1C` |
| `$s2` VM-state address | `sp+0x20` | `sp+0x20` |
| `$s3` controller address | `sp+0x24` | `sp+0x24` |
| `$s4` context address | `sp+0x28` | `sp+0x28` |
| `$s5` terminal state 3 | `sp+0x2C` | `sp+0x2C` |
| `$s6` terminal state 4 | `sp+0x30` | `sp+0x30` |
| `$s7` terminal state 5 | `sp+0x34` | `sp+0x34` |
| `$fp` / `$s8` terminal state 6 | `sp+0x38` | `sp+0x38` |
| `$ra` | `sp+0x3C` | `sp+0x3C` |
| Outer-loop counter | `sp+0x44` | `sp+0x44` |

The isolated IDO object reserves `0x50` bytes. Its disassembly has no stack
load or store in `sp+0x48..sp+0x4F`; all ten saved-register offsets and the
outer-counter slot match the original. The excess eight bytes are therefore
unused in this object. The source-shape trials below did not identify which
IDO frame-allocation rule accounts for those bytes.

The exact frame-only remaining instruction differences are:

| Original address | Original instruction | Candidate object instruction at the corresponding offset |
| --- | --- | --- |
| `0x8003DBEC` | `addiu $sp,$sp,-0x48` | `addiu $sp,$sp,-0x50` |
| `0x8003DDC0` | `addiu $sp,$sp,0x48` | `addiu $sp,$sp,0x50` |

These are not the only full-function differences. The raw isolated-object probe
compares 95 words after excluding candidate relocation sites and reports 53
equal words. The relocation-layout report separately records 53/88 comparable
non-relocation words and 17 relocation-layout differences. Those denominators
come from different comparison rules and should not be combined.
The execution ledger records the complete set of 42 raw direct-mismatch VMAs;
it does not include instruction encodings or object bytes.

## Branch-likely layout

The baseline alias candidate emits all six branch-likely operations, but four
are at different offsets from the original. GNU's disassembler prints some
zero-comparison aliases (`bnezl`/`beqzl`) for the original `bnel`/`beql`
encodings.

| Original PC | Baseline candidate PC | Offset change |
| --- | --- | ---: |
| `0x8003DC8C` | `0x8003DC90` | `+4` |
| `0x8003DCC0` | `0x8003DCC4` | `+4` |
| `0x8003DCD0` | `0x8003DCD8` | `+8` |
| `0x8003DD14` | `0x8003DD14` | `0` |
| `0x8003DD50` | `0x8003DD58` | `+8` |
| `0x8003DD8C` | `0x8003DD8C` | `0` |

The baseline candidate's delay instructions are the corresponding cursor,
counter, latch, and controller accesses, but moved branch addresses mean the
whole native branch layout still differs. The state-reload-before-store trial
puts the first two likely branches at their original PCs; the remaining four
still do not all line up.

## Source-lifetime trials

Each source variant was written under the ignored local
`practice/diagnostics/decomp-100-inputs/g64-032/variants/` directory, compiled
with the pinned IDO 5.3 `-O2 -mips2 -G 0 -non_shared` flags, and compared to the
verified local ROM. Host differential tests used the same two deterministic
seeds for each variant.

| Variant | Native symbol bytes | Raw comparable words | Equal words | Native frame | Host differential |
| --- | ---: | ---: | ---: | ---: | --- |
| Alias baseline | 472 | 95 | 53 | `0x50` | 5,000/5,000 pass |
| Inline script argument | 472 | 95 | 49 | `0x50` | 5,000/5,000 pass |
| Reload state before volatile cursor store | 468 | 94 | 29 | `0x50` | 5,000/5,000 pass |
| Add `register` hint to outer counter | 472 | 95 | 53 | `0x50` | 5,000/5,000 pass |
| Replace terminal-state switch with range check | 456 | 91 | 15 | `0x50` | 5,000/5,000 pass |
| Make work pointer non-volatile | 476 | 93 | 18 | `0x50` | 5,000/5,000 pass |

The variants retained the modeled behavior in the synthetic differential, but
none moved the frame to `0x48`, preserved the entire original branch layout,
or matched the function. This closes G64-032 as `RESEARCH_ONLY`; it does not
change the matching-C count or claim any callback behavior beyond the model.

## Validation and limits

- The pinned IDO compiler SHA-256 is
  `76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0`.
- The isolated candidate and all five source variants compiled; the pinned
  codegen probe and `mips-linux-gnu-objdump -dr` exposed frame, saves, stack
  slots, and branch-likely positions.
- All six C sources passed 2,500 original-MIPS/host-C synthetic cases at seed
  `0x1D8` and 2,500 at seed `0xDEADBEEF` (30,000 total). The local ROM was
  SHA-1-checked by the differential harness.
- No candidate was linked into the production translation unit. No new
  complete-ROM build, inventory build, or in-game test was run. No ROM, object,
  compiler binary, or generated disassembly is included in Git.

**Next:** G64-033, exercise and strengthen the differential harness's mutable
callback, signed-halfword, bound-reload, and aliasing controls.
