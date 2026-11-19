# Japanese Goemon rev-0 — 31 native matching-C functions

**Native ROM proof: PASS, independently reproduced on 16 November 2026.**

The seven functions below have been fully integrated with the previous 24-function baseline. The pinned upstream `mnsg` source (commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`), native IDO 5.3 (`-G 0 -non_shared -O2 -mips2`), GNU MIPS assembler/linker, Splat and upstream Rommy produced two complete byte-identical Japanese images:

- 32 MiB expanded: SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`.
- 16 MiB retail: SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`.

Independent strict verification confirmed **31 matching-C functions, 1,784 bytes, 27 source units**, source SHA-256 fingerprints, exact compiled object sections/relocations, original guest RAM addresses and the final ELF inventory: 7,376 positive-sized function entries, 7,345 assembly-marked, 31 C-owned, zero unreviewed unmarked, across 73 code sections. Two independent clean pinned-source workspaces reproduced the full ROMs and verifier. Eight ROM-free guardrail tests passed.

| ROM offset | Function | Bytes |
|---|---|---:|
| `0x370B0` | `func_800364B0_370B0` | 32 |
| `0x37178` | `func_80036578_37178` | 32 |
| `0x3757C` | `func_8003697C_3757C` | 32 |
| `0x3769C` | `func_80036A9C_3769C` | 8 |
| `0x383C4` | `func_800377C4_383C4` | 36 |
| `0x3847C` | `func_8003787C_3847C` | 20 |
| `0x3850C` | `func_8003790C_3850C` | 20 |

## Linker-layout acceptance

21 individually reviewed C objects and seven original assembly boundary slices were checked for executable extent, trailing zero-only padding and relocation safety. Assembly slices requiring fail-closed trims were `main_370D0` (8 bytes), `main_37198` (12), `main_376A4` (4), `main_37DB8` (12), `main_38240` (12), `main_383E8` (12) and `main_38490` (4). The adapter changes only ELF32 section size/alignment fields and generated main linker SUBALIGN(4). No instruction payload or relocation is changed.

## Fresh build

```bash
bash decomp/build_japan_thirtyone_c.sh <fresh-pinned-mnsg-checkout> <dependencies-dir> <runtime-additions-dir>
python3 -m unittest decomp.test_japan_thirtyone_c
```

The cartridge must be privately staged as `config/japan_0/baserom.z64` in the pinned upstream checkout. Do not commit game ROMs, generated ASM, binaries, or proprietary compiler tools. The verified offline reproduction archive is `goemon-japan-thirtyone-c-verified.zip` (SHA-256 `dd2c10236a906b05efd555eb89bbb603c89ca815d2e6e2e968df11c7e9ffd76b`).

## Further adjacent research

Three additional **isolated only**, not yet source-linked into a complete ROM, IDO/GNU MIPS exact matches total 128 bytes:

- `func_80038984_39584` — 40 bytes; `func_800389AC_395AC` — 40 bytes; `func_800389D4_395D4` — 48 bytes.

C sources are retained under `decomp/japan_adjacent_research/`, not production `japan_matching`. The 0x39408/39438/39468 wrappers diverge in register/prologue ordering; initial 0x38C34/0x38DF8 candidates fail the size gate. Larger 308/324/468-byte warp neighbours remain assembly-owned. No Japanese emulator gameplay or native PC recompilation was tested.
