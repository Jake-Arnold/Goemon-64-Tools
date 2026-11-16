# USA file_11 expansion: 77 original-address IDO matching-C research candidates

**Research date:** 16 November 2026. **Status:** original-VMA native IDO 5.3 match only; NOT full-ROM matching-C promotion.

## Sources and method

- Inspected the authenticated original USA **33,554,432-byte decompressed ROM** (SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`) and independently built *pristine* pinned upstream `mnsg.elf` (SHA-256 `83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038`).
- Enumerated only original ELF32 big-endian MIPS positive-size `STT_FUNC` symbols within the `file_11` text ROM range `[0x587370, 0x5B8500)`; excluded the nine 32-byte wrappers and 37 no-op callbacks already promoted in the canonical 210-function manifest.
- Recognised exact eight-word stack-frame/JAL/return templates and their original delay-slot semantics. Dynamically generated small C functions, compiled each with original IDO 5.3 `-G 0 -non_shared -Xfullwarn -Xcpluscomm -O2 -mips2` at the function’s *original* VMA using the native MIPS linker, then compared every original instruction byte.
- Separately compiled two contiguous original 20-byte float-field reset functions as one C unit and checked both original 20-byte spans. Compiled each remaining 12-byte no-op separately at its original VMA.
- Evidence: `decomp/results/file11_expansion_native_20261116.json`, reproducible read-only tool `decomp/research/file11_expansion_probe.py`, ROM-free contract tests `tests/test_decomp_file11_expansion.py`. This document contains no raw game instructions or assets.

## Verified original-address matches

| Pattern | New functions | Native C instruction bytes | Status |
| --- | ---: | ---: | --- |
| 32-byte direct-call wrappers | **59** | **1,888** | 59/59 isolated original-address codegen exact |
| 12-byte empty callbacks not in 210 baseline | **16** | **192** | 16/16 isolated original-address codegen exact |
| 20-byte actor float-reset functions | **2** | **40** | 2/2 exact, one combined C unit |
| **Research total** | **77** | **2,120** | **77/77**, *not* linked overlay G2 |

Original 32-byte wrapper argument modes: **46** preserve an unused second argument, **6** take one argument, **6** call with a fixed numerical second argument, and **1** calls its handler with a null pointer. The null-pointer wrapper reproduces the original JAL delay-slot behavior only with a C function taking **no arguments** (adding an unused actor parameter causes a different 48-byte compilation).

There are **68** eight-word simple-JAL wrapper symbols in total in this overlay: **9** already among the 210 canonical C functions and **59** newly confirmed here. These 59 wrappers call **23** distinct destination functions. The strongest families are:

| Native callee VMA | Matching new wrappers | Original callee size | Evidence and research significance |
| --- | ---: | ---: | --- |
| `0x801E3AC0` (`func_801E3AC0_59F9D0`) | **18** | `0xDC` (220 B) | Reads actor `+0x18`, actor `+0x5C`, global `0x8015C604`; later branches depend on actor current character `+0x60`; shared state/event handler, not fully understood |
| `0x801EB6BC` (`func_801EB6BC_5A75CC`) | **8** | `0x184` (388 B) | Branches on actor `+0x60` and `+0x64` and follows actor-linked structures; shared actor-state dispatcher, not yet matching C |
| `0x801E4530` (`func_801E4530_5A0440`) | **4** | `0xF4` (244 B) | Uses common action helper `func_801DD720_599630` and character-state global `0x8015C604`; useful for character-state callgraph |
| `0x801E3400` (`func_801E3400_59F310`) | **3** | `0x350` (848 B) | Event selection checks and calls an actor state/action helper with immediate event IDs |

The six constant-argument wrappers pass IDs `12, 13, 14, 15, 16, 18` (decimal) to shared handlers. Those are **native arguments**, not verified gameplay names. The actual character-cycle selector `func_801DD50C_59941C` remains assembly-owned; one direct call to it was located in `func_801DCE10_598D20` after `func_801DD3C4_5992D4` checks eligibility. Its MIPS sequence searches the four availability words and then invokes the already matched state synchronizer. These traces establish control-flow links, not live character switching verification.

## Corrected original no-op count

The previous dated research note estimated **50** original 12-byte no-op callbacks, 37 of which were promoted. A complete original ELF STT_FUNC-and-byte scan on the pinned USA ROM shows **53**, specifically **37 previously promoted + 16 further unpromoted**. The earlier **50** was an undercount of discovered callbacks, not an error in the 210-function ROM proof or inventory. Newly identified original offsets:

- `0x5874D4` (func_801CB5C4_5874D4), `0x587704` (func_801CB7F4_587704), `0x58E2D8` (func_801D23C8_58E2D8), `0x59C720` (func_801E0810_59C720)
- `0x59C7C0` (func_801E08B0_59C7C0), `0x5A0F94` (func_801E5084_5A0F94), `0x5A5FDC` (func_801EA0CC_5A5FDC), `0x5A63E0` (func_801EA4D0_5A63E0)
- `0x5A63EC` (func_801EA4DC_5A63EC), `0x5A9410` (func_801ED500_5A9410), `0x5A941C` (func_801ED50C_5A941C), `0x5AEBC4` (func_801F2CB4_5AEBC4)
- `0x5AEBD0` (func_801F2CC0_5AEBD0), `0x5B4398` (func_801F8488_5B4398), `0x5B8488` (func_801FC578_5B8488), `0x5B8494` (func_801FC584_5B8494)

## Actor float reset routines (new actual state mutation)

The two adjacent original 20-byte functions `func_801E2FE0_59EEF0` and `func_801E2FF4_59EF04` both write `0.0f` to actor floating-point fields at `+0xE4` and `+0xE8`. The pinned original instruction sequence is reproduced exactly by:

```c
typedef struct { unsigned char pad[0xE4]; float x, y; } Actor;
void func_801E2FE0_59EEF0(Actor *a) { a->x = 0.0f; a->y = 0.0f; }
void func_801E2FF4_59EF04(Actor *a) { a->x = 0.0f; a->y = 0.0f; }
```

The meaning of these floating-point fields (position, motion, or some other actor state) is **not** yet demonstrated.

## Recommended next production/research sequence

1. Design a new reviewed version of the `file_11` Splat mixed C/ASM adapter, preserving the canonical 210-function stage and staging the **59 wrappers, 16 no-ops, 2 float resets** in original ROM order. Patch newly introduced *synthetic* Splat function labels only after exact pinned provenance; do not widen existing alias exceptions without evidence.
2. Compile each original-address source under native IDO 5.3; check all 77 linked FUNC symbols, their code bytes, map input extents and 8,825 semantic relocation tuples. Require **full 33,554,432-byte ROM equality** and complete combined central `decomp.verify` and `decomp.inventory`, including original 210 functions, before any official promotion.
3. Trace the **220-byte `0x801E3AC0`** and **388-byte `0x801EB6BC`** shared handlers next. They contain substantially more gameplay logic than the thin 32-byte forwarding wrappers; analyze their caller argument/state contracts, not just compile-match counts.
4. Attempt the existing 180-byte four-character selector only under a separate bounded compiler trial; the previous 176-byte candidate is not matching.

**Official status:** `chatgptweb/decomp` currently has **210 matching C / 13,336 bytes / 7,153 ASM entries**. This research alone does **not** make the next 77 production claims. If a future central G2 succeeds, the *prospective* total would be **287 C / 15,456 bytes / 7,076 ASM entries**, subject to full inventory verification.
