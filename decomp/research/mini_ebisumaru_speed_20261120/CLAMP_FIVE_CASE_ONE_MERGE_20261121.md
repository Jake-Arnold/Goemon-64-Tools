# USA Mini clamp: five original first-angle case stores and one second-angle merge store

**21 November 2026 · FAILED_NATIVE / RESEARCH_ONLY. No production C or manifest promotion.**

Original USA `func_801CD310_589220`, ROM offset `0x589220`, VMA `0x801CD310`, original function 4,320 bytes and stack frame 232 bytes. Authenticated expanded USA SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Native SGI IDO 5.3 `-O2 -mips2 -G 0 -non_shared`.

## Recovered store ownership

The prior complete C source already matched both trig JAL offsets `+0x19C/+0x1A4`, return store `+0x1B0`, original `sp+0x64/+0x6C/+0x6E` locations and 232-byte frame, but its stores were reversed: **five second-angle case writes and one first-angle merge write**.

The new, full independent `case_first_scalar_second.c` uses the first angle as an independently stack-backed `volatile u16` field and selects the second angle in a lexically non-overlapping existing `s32 pool_s32_0` integer, then stores it once at the merge. Native IDO emits **five case-local `sh` to `sp+0x6E`**, at `+0xCC/+0x100/+0x130/+0x164/+0x184`, and **one merge `sh` to `sp+0x6C` exactly at `+0x198`**. Original five first-angle stores are at `+0xC8/+0xFC/+0x12C/+0x160/+0x180`; original merge has `sh a1,sp+0x6C` at `+0x198`. The candidate instead has `sh v0,sp+0x6C`. The first-angle store PCs are uniformly 4 bytes late. Stack frame remains **232 bytes**, retaining 33 calls, nine native `sqrt.s`, 101 text relocation records, 18 original switch-table grouping entries.

**Joint native gate remains FAILED.** Candidate first/second trig JAL at **`+0x1A0/+0x1A8`**, original **`+0x19C/+0x1A4`**; return store `swc1 f0,sp+0x64` at candidate `+0x1B4` versus original `+0x1B0`. The original **loads the first angle before writing the second** at the merge; candidate reverses the load/store schedule. Candidate function **4,292/4,320 bytes**, **9/888** equal comparable non-relocated same-position words, **1/101** exact relocation offset/type/symbol triples, first mismatch `+0x04` from the long-lived saved `$f20` zero. Do not mistake compiler structural agreement for byte equality.

The previous original-call-offset candidate remains a distinct Pareto source: **4,288 bytes / 232-byte frame / 10/889 fixed-offset words / 4/101 reloc triples**, with both trig calls and return store exact, but its first and second stores are reversed. Neither source dominates or may be promoted.

## Experimental scope and negative results

Four bounded native IDO suites compiled **108 source variants** (some diagnostic/rejected as not semantically valid): five/one case ownership, pool reuse, local type/qualifier changes, scalar case order, merge expression, declaration order, local first-angle read reordering. Neither candidate attains original **five-case first stores + one merge second store + original two trig-call PCs + 232-byte frame** simultaneously. Source that overwrites the live `pool_u16_0` return value was specifically **rejected** despite a higher superficial word score. Volatile is a source/codegen experiment, not evidence that original C used `volatile`.

The strongest valid five/one candidate is the standalone whole-C gzip below. After first store topology recovery, the remaining concrete target is source-level register allocation / load-store scheduling at `+0x194..+0x1A8`, with upstream `$f20` save at `+0x04`. Further low-value scalar casts and lexical rearrangements are not justified by results.

## Actually performed verification

- User USA retail ROM SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66` authenticated; pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
- **Unmodified original USA 32 MiB full build 33,554,432/33,554,432 byte-identical**, expanded SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. This is *not* a candidate-C-integrated ROM.
- 108 authentic original SGI IDO 5.3 native builds (diagnostics included), true original-address ELF/MIPS/relo/frame comparisons; both selected complete C sources freshly recompiled with a fail-closed original-ROM store/call/delay-slot audit **PASS expected FAILED_NATIVE**.
- Independent host fixture for switch angles/call order/lexically non-overlapping vector lifetime: GCC ASan+UBSan **65,536 cases PASS**, Clang ASan+UBSan **65,536 cases PASS**. Does not establish whole-function game semantics.
- Fresh source ZIP extraction, SHA256SUMS, and end-to-end native replay/host tests **PASS**.
- Experimental candidate ROM integration, current all-accepted-C `decomp.verify`, strict `decomp.inventory`, full `decomp.local_ci`, emulator gameplay **NOT RUN** because original-address native equality fails.

## Full source and exact replay

Saved full reconstructed **source-only C gzip**: `decomp/research/mini_ebisumaru_speed_20261120/case_store_first_scalar_second_20261121.c.gz` (original UTF-8 C SHA-256 `612bc4baa9c81b0c2397fa1b9b0853da6f0d4738b2c65c7842a77a4d35546d90`, gzip SHA-256 `937715d1456cc014b2a18235a865e85a934c9d23a2298d4b3358ff7ee80bc7b5`). Restore with `gzip -dc case_store_first_scalar_second_20261121.c.gz > case_first_scalar_second.c`.

Complete user-visible source-only ZIP `GOEMON_CLAMP_CASE_MERGE_20261121.zip` SHA-256 **`94d7cf1826ac9023a3efbf02ad1260c5c24ed56eb49e3e1bb09ab3ba3cef5145`** supplies both complete C files, patch, original-ROM exact-code auditor `audit_case_merge.py`, MIPS/ELF comparator, clean replay `replay.py`, host sanitizer fixture, 108-trial sanitized JSON matrices and SHA256SUMS. From the extracted folder, after original runtime setup:

```sh
python3 replay.py --upstream /path/to/pinned/mnsg-japan --rom /path/to/usa/baserom.decompressed.z64 --elf /path/to/original/usa/mnsg.elf --built-rom /path/to/original/usa/mnsg.z64 --host
```

No original ROM, disassembled code, object/ELF, game assets, proprietary compiler, personal data or secrets committed or included.

**USA G2 is unchanged:** 1,965 accepted C / 84,648 original instruction bytes / 5,398 ASM entries (latest official G2 verified separately). Research PR #144 remains draft; original ASM stays production owner.
