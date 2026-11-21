# Original-address Japanese script-VM C promotion — 21 November 2026

**Acceptance:** `PASSED_G2_LOCAL` until the exact GitHub implementation commit is remotely re-fetched. No game ROM, proprietary compiler, extracted original assembly, ELF/object files or saves are stored in this directory.

**Targets:** `func_8003CC10_3D810` (48 bytes, resource fallback lookup) and `func_8003E2C4_3EEC4` (44 bytes, VM countdown expiry). Original USA functional counterparts already exist in `decomp/script_vm.c` as `func_8003CFA0_3DBA0` and `func_8003E654_3F254`; USA matching-C totals are **unchanged**.

## Reproduce from a separate clean Japanese 2,121-C workspace

The original Japanese and USA retail images must remain private. Use the supplied pinned IDO 5.3 toolchain, Japanese Splat extraction and independent original-ROM baseline as documented in `GOEMON_BUILD_ENVIRONMENT.md` and the existing `decomp/glitch_g2_promotion.py` pipeline.

```sh
python3 -m decomp.vm_g2_promotion stage --checkout "$JP_2121_CHECKOUT"
python3 -m decomp.vm_g2_promotion build --checkout "$JP_2121_CHECKOUT" --deps "$DEPS" --runtime "$RUNTIME"
python3 -m decomp.vm_g2_promotion verify --checkout "$JP_2121_CHECKOUT" --baseline "$JP_2121_UNCHANGED_BASELINE"
python3 -m unittest decomp.test_vm_g2_promotion -v
python3 -m decomp.local_ci
```

`stage` refuses unverified Japanese ROM, missing Japanese 1,686-source accepted batch, incorrect 3-function gameplay Start batch, modified source hashes, duplicate targets or changed original ASM object ownership. `build` compiles the actual C with IDO 5.3 and preserves the original 44-byte function while stripping **only** four bytes of compiler-generated object alignment padding. It requires a byte-identical 32 MiB ROM. `verify` rejects changes to any of the 7,376 original ELF function identities, the 80,747 exact semantic relocations, or the expected original C/ASM partition.

The original ROM SHA-1 is `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. Original relocation digest: `e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20`.

The stage verifies two **new** Japanese original-address C sources, 92 bytes total, producing Japanese **2,123 C / 112,336 C bytes / 5,253 remaining ASM**. The USA accepted 1,958-C count and C sources are not modified.

**Two independent local demonstrations** were performed before publication: a direct source/linker integration and a clean replay of the fail-closed stage/build/verify adapter. Both passed identical ROM, ELF and relocation checks. A GCC ASan/UBSan host fixture checks resource lookup (4 cases) and countdown behaviour (5 cases). The task-specific Python tests and full local CI also passed. None of these tests reproduces in-game Bomb Text Skip input timing.

[Technical report](../../docs/GOEMON_VM_TWO_G2_PROMOTION_20261121.md) · [Glitch Issue #139](https://github.com/Jake-Arnold/Goemon-64-Tools/issues/139).
