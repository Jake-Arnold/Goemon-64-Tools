# Original-ROM native G2: two Japanese script-VM functions

**21 November 2026.** **PASSED_G2 / PUBLISHED_REMOTE_VERIFIED.** Native implementation commit [`74f940e7`](https://github.com/Jake-Arnold/Goemon-64-Tools/commit/74f940e7c0fb6b0ef7286bca1018780450ae4993) is published on `chatgptweb/decomp`, the remote code and evidence have been independently re-fetched, and the recorded full-ROM/ELF/relocation/CI checks passed. The original game was **not** executed in an emulator. No North America/USA matching-C implementation changed. No ROM, extracted assembly, object, ELF, save or proprietary compiler is published.

## Genuine new code, deduplicated

| Japan original C function | Guest VMA | Original ROM offset | Size | Meaning | USA already-accepted C equivalent |
|---|---|---|---:|---|---|
| `func_8003CC10_3D810` | `0x8003CC10` | `0x3D810` | **48 B** | Return script-resource pointer, falling back to default when null | `func_8003CFA0_3DBA0` |
| `func_8003E2C4_3EEC4` | `0x8003E2C4` | `0x3EEC4` | **44 B** | Pre-decrement script VM countdown; if now <=0, reset countdown and dialogue state | `func_8003E654_3F254` |

The exact source files are in `decomp/research/vm_g2_20261121/sources/`; the **fail-closed** stage/native-IDO/full-ROM/ELF/relocation/inventory adapter is `decomp/vm_g2_promotion.py`. The Japanese sources compile to exactly the original instruction sequences with pinned IDO 5.3 `-O2 -mips2` at their original addresses.

The countdown's standalone compiler object contains four bytes of **trailing alignment padding**, after its original 44 instruction bytes. The existing reviewed metadata packer removes those four padding bytes and changes alignment metadata from 16 to 4; it neither patches any instruction nor inserts a new MIPS instruction. Its strict linked-ROM result is unchanged.

### Verified native evidence

| Gate | Result |
|---|---|
| Japanese expanded original ROM (32 MiB) | SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded` **PASS** |
| Rebuilt original ROM | **33,554,432 / 33,554,432 bytes identical** |
| Original positive-size ELF function identities | **7,376 / 7,376 identical** |
| Japanese all-section semantic relocations (includes `.rel.main`) | **80,747 / 80,747 identical** |
| Full original relocation multiset digest | `e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20` |
| Strict original-ASM → original-C function partition | Only the above **two** functions changed |
| Japanese exact-C count | **2,121 → 2,123** |
| Japanese accepted instruction bytes | **112,244 → 112,336** |
| Japanese remaining original ASM entries | **5,255 → 5,253** |
| Host test | GCC ASan+UBSan **PASS** (four lookup cases, five countdown cases) |
| Task-specific tests | **3/3 PASS** |
| Full `decomp.local_ci` | **303 decomp tests** (1 skipped), **349 verifier/ledger tests** (4 skipped), configured host sanitizers and task checks **PASS** |
| Clean adapter replay | **PASS** with full original ROM, identities, relocations and inventory |
| Game/emulator/frame input or savewarp replay | **NOT RUN** |
| Additional accepted USA matching-C functions | **0** (USA remains 1,958) |

**Original code SHA-256:**

- `func_8003CC10_3D810`: `911d6fbdc6b9d123514051c49c714bee1ca02d33de8d688f0dbdb98889ac360d`
- `func_8003E2C4_3EEC4`: `9152e34ebf1d4fac577d6f6c8120f6dee74e7c8615030573cc22014cbe5f584a`

**Exact reviewed source SHA-256:**

- Lookup: `d8d2b77d788b7c450d9f78da5fba0f199bd725d70a2e3315025e81fe95c24960`
- Countdown: `99569d89988f6db380aea636c466e17ffe61ce6d2556348dcf187501bef5ff24`

## Cross-region meaning: independently original-code grounded

The already-accepted USA source `decomp/script_vm.c` implements *the same algorithms*: `func_8003CFA0_3DBA0` returns `D_80077550_78150[index]` or fallback `D_8007CCA4_7D8A4`. Japanese uses pointer table `D_8007D030_7DC30` and fallback `D_80082478_83078`. These are **independent original regional symbols**, not derived by a universal address offset.

The USA countdown handler `func_8003E654_3F254` pre-decrements `VmWork.countdown` at `0x801C77F8` and sets its countdown and VM state (`0x801C77E0`) to 0 when expired. Japanese equivalent accesses `D_801CCF18_1CDB18` + `0x10` (= `0x801CCF28`) and VM state `0x801CCF10`. **VM addresses require direct counterpart analysis** and must not be translated by the saved-game `+0x57F0` rule. Only the original input/output fields and code pathways are proven; overlay or task callback lifetime and the Bomb Text Skip frame race remain unverified.

## Other C targets and causation limitations

Japanese gameplay teardown `func_8001F70C_2030C` remains **ASM** because the byte-exact numeric-offset C loses its original `D_3ADDF` HI16/LO16 relocations. Its symbolic C variant has different instruction scheduling and a different function length. Japanese reset manager `func_8003D0D8_3DCD8` (548 B) and pause controller `func_8001F750_20350` (2,184 B) also remain original ASM, with earlier failed C source probes. Their instruction-level semantics remain usable for research without a native exact-C match.

**This update does not prove how Start interrupts Gourmet Sub Bomb Text Skip.** It improves exact native-C coverage of the VM resource fallback and countdown and confirms they correspond to existing USA behaviour. The input-acceptance and eventual reset mechanism remains documented in `GOEMON_START_DIALOGUE_SKIP_CONTROL_FLOW_20261120.md`; successful-frame causation requires an actual trace or equivalent instruction-scheduling execution.
