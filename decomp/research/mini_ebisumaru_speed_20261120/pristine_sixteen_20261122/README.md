# 22 November 2026 — Seven additional USA Mini functions exact at original linked addresses

**PASSED_PRISTINE_FULL_ROM_ELF / RESEARCH_ONLY. No accepted-C promotion.**

Seven previously ASM-owned USA `file_11` functions now compile byte-identically under authentic pinned SGI IDO 5.3:

| Original C function | Expanded-USA ROM | Native instruction bytes | Symbolic relocations |
| --- | --- | ---: | ---: |
| `func_801E2180_59E090` | `0x59E090` | 160 | 11 |
| `func_801E2220_59E130` | `0x59E130` | 68 | 3 |
| `func_801E2800_59E710` | `0x59E710` | 176 | 1 |
| `func_801E2AA0_59E9B0` | `0x59E9B0` | 180 | 4 |
| `func_801E2BA8_59EAB8` | `0x59EAB8` | 168 | 1 |
| `func_801E2CEC_59EBFC` | `0x59EBFC` | 64 | 1 |
| `func_801E2D74_59EC84` | `0x59EC84` | 188 | 2 |
| **New this session** | | **1,004/1,004** | **23/23** |

All seven are independently linked at their original guest VMA; original positive-sized ELF FUNC identities, native instruction bytes and relocation offset/type/symbol triples are exact. Their seven complete C source files are published in this directory, each verified by exact Git blob SHA-1 against the tested bytes.

**New combined original-ROM proof:** the seven C functions, plus six newly researched in the previous sessions and three older Mini native-exact functions, replace **16 complete C functions / 2,208 original instruction bytes** at true original linker positions within pristine pinned upstream. Original 32 MiB USA ROM rebuilt **33,554,432/33,554,432 byte-identical**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; all **7,376** positive-sized ELF function identities and **82,216** semantic relocation tuples across **72** sections (including all **8,825** `file_11` records) equal. Baseline original ELF SHA-256 `83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038`; 16-C ELF SHA-256 `68cba222c1ebc2d419d12f8b8a3d9eed75c8d28a9fb10462ba9acee277b8f8f9`.

**Actually tested:** pristine pin `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, genuine IDO 5.3 original flags, clean 26-file source archive extraction/checksum, seven original-address native replays, complete 16-C scratch ROM/ELF replay, GCC ASan/UBSan and Clang ASan/UBSan on **all seven actual C bodies** (8,192 deterministic scenarios, 65,536 function calls per compiler), and deliberate source-tampering rejection. All PASS for the stated test scopes. No emulator gameplay.

**Source-only reproducibility:** user-facing `GOEMON_USA_MINI_SIXTEEN_FULL_ROM_PROOF_20261122.zip` SHA-256 **`7bf4bb80ec7a2a4fd5eda086e5e9d4ffa93ae7de5da0874a20ea7636e2204fea`** (31 KB), delivered in the originating conversation. Contains complete 16-C source material, seven-function original-address verifier, 16-C whole-USA-ROM linker/ELF verifier, original selector relocation adapter, GCC/Clang real-source regression and sanitized proof. The portable seven-function verifier is stored here as `replay_new_seven.py`; the complete pristine full-16 linker replay remains attached in the conversation ZIP, not bundled into GitHub. User supplies the original private ROM and pinned upstream/toolchain separately. No original assembly, ROM, object, binaries, proprietary compiler or game assets published.

**Why not promote:** the exact 16-function integration is against pristine upstream, **not with the current 1,965 production-accepted C functions**. The full live decomp checkout cannot be materialized locally (shell GitHub DNS fails; connector only exports text endpoints). Required combined `python3 -m decomp.verify`, `python3 -m decomp.inventory`, full `python3 -m decomp.local_ci` and gameplay are **NOT RUN**. ASM, canonical manifests, results and accepted counts unchanged. USA remains **1,965 original matching C / 84,648 accepted instruction bytes / 5,398 ASM**; draft PR #144 remains open and unmerged.

**Other blocks:** 4,320-B clamp `func_801CD310_589220` remains FAILED_NATIVE (123/917 same-position code words, 30/101 exact relocations on previous strongest C). Newly tried `func_801E26AC_59E5BC` is 29/37 words with 4/4 relocations and correct 148-B size but wrong FP register allocation; `func_801E30E4_59EFF4` and `func_801E29A0_59E8B0` remain FAILED_NATIVE. No partial C is promoted.
