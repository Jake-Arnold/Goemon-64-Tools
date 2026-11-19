# USA camera-mode reset: whole-ROM and ELF scratch proof (17 November 2026)

**Result:** Native source-only scratch integration PASS. **Production:** USA canonical remains 342 matching-C functions / 17,568 bytes; Japanese revision-0 has its own 34-C regional proof. No combined 343-C central promotion is claimed.

## Why this is not duplicate research

The source `func_801F97D4_5B56E4` is the existing 136-byte camera-region reset previously proven in isolation, **not** a reimplementation of upstream `camera.c`. The latest accepted USA `file11_179` fixture still owns the containing region `[0x5B4E1C,0x5B64B8)` in assembly. The earlier camera work identifies a separate 544-byte region updater `func_801F9988_5B5898`, which was **not** touched.

## Authenticated native build and scope

- Pinned upstream revision: `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. (The former shorthand is not a valid pin.)
- Original USA 16 MiB retail ROM SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; decompressed 32 MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Original baseline ROM built with original IDO 5.3, GNU MIPS tools, pinned Splat extraction, and matched the 32 MiB reference byte-for-byte; original linked ELF SHA-256 `83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038`.
- Source SHA-256 `9d47ba199dfd48f5707b7623f45eee5e0853110f725e08bcf4ad7c151f7450c4`; original and candidate 136-byte text SHA-256 `f6266809ac26ff75f44d5f23cab8c15ae338e6185b88b69ec85bd83dfb7c0b8a`.
- A separate scratch checkout split the pristine `file_11` assembly at `0x5B56E4` and `0x5B576C`, retained all other symbol names and assembly text, replaced only the 136-byte target with matching C, used `SUBALIGN(4)`, and removed only verified zero compiler/assembler tail padding in each of three linked objects. No ROM bytes were patched.
- Exact scratch ROM comparison: **33,554,432/33,554,432 bytes equal**, original SHA-1 preserved.
- Exact `file_11` relocation multiset: **8,825 baseline / 8,825 candidate; zero missing, zero extra** (site/type/resolved symbol-target comparison). Raw order is not asserted identical.
- Full original positive-size ELF function inventory: **7,376 baseline / 7,376 candidate; names, VMAs, sizes identical**. `func_801F97D4_5B56E4` remains at VMA `0x801F97D4`, size 136.

## Exact scratch object boundaries

| Object | Original-linked text size | SHA-256 after zero-tail trim |
|---|---:|---|
| `asm/usa/587370.s.o` | 189,300 | `24c0f0b88130dc28f370866ec27cf6d70bd0806fb584627e8193f0717e94a3ad` |
| `src/camera_reset_usa_5b56e4.c.o` | 136 | `1e404dc0f374ffa2d7b1e2f21e8d468014af9ab132f044e90e9a49a99d728c81` |
| `asm/usa/5B576C.s.o` | 11,668 | `a7031d785487b097277edfddc770bfc3780c81f52f15f8720c003afea1a5c77b` |

These three boundaries span the old `[0x587370,0x5B8500)` text object exactly. They do **not** represent the production 179-C mixture, whose unchanged 126 object boundaries require a separate 180-C opt-in stage.

## Reproduction

The source-only `goemon_camera_reset_136_scratch_repro.zip` generated alongside the project chat contains the **tested** fail-closed scratch builder, C fixture, proof JSON and README. Its builder requires a fully expanded, exact-rebuilt pristine USA upstream checkout with original ELF and toolchain, makes a separate copy, and verifies all three checks again. It does not modify or upload the ROM.

Regression: `tests/test_decomp_camera_reset_scratch_20261117.py` validates metadata and source pin, and can authenticate original ROM bytes if `GOEMON_USA_DECOMPRESSED_ROM` is set. The standalone scratch Python builder was actually run successfully here. Full current repository `decomp.local_ci` and combined `decomp.verify` were **not** executed; do not claim 343 production functions.

## Next exact acceptance gate

Create a versioned **180-file11-C** candidate stage on top of the current **179-file11-C / 342-USA-C** baseline; split only the existing assembly-owning chunk `[0x5B4E1C,0x5B64B8)` around the new 136-byte C island while preserving all 179 existing C identities and every original overlay object boundary. Run complete `decomp.verify`, complete 32 MiB USA ROM comparison, all 8,825 `file_11` semantic relocations, complete `decomp.inventory` (7,376 identities), and full `decomp.local_ci`. Only a passing combined gate permits promotion to 343. The Japanese 34-C baseline is a separate regional pipeline and must remain unchanged.
