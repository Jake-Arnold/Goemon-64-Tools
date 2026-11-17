# USA resource 26 — native 312-byte matching-C callback chain (research only)

**Research date:** 17 November 2026. **Scope:** Original USA NG5E, original IDO 5.3, pinned upstream `klorfmorf/mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. **No production C promotion in this commit.**

## Why this candidate was found

The user used Project64 to stop at the original packed-event setter `0x80024084` while collecting the Oedo Castle Mr. Arrow. Registers showed `A0=0x104`, `V0=0x8015C628`, `T4=0x10`, `S0=0x8016B530`, `RA=0x08000148`. A subsequent live actor memory view confirmed `S0+0xD0 = 01 04 00 00`. Independently checked original ROM MIPS identifies `RA-8 = 0x08000140` as the native saved-event setter call in **resource 26**; the original callback loads `lhu a0,0xD0(s0)` in that call's delay slot. The original generic file12 loader copies the room-definition word `0x01040000` from definition `+4` into the live actor `+0xD0`.

This trace identified a contiguous original resource-26 callback chain appropriate for native C conversion. The matched source is `decomp/research/file26_mr_arrow_chain_20261117.c`. Code does not claim confirmed names for unknown helper roles.

## Original-address function proofs

| Original function name | Decompressed USA ROM offset | Loaded VMA | Original code bytes | Verification |
| --- | --- | --- | ---: | --- |
| `func_080000CC_6AE8AC` | `0x6AE8AC` | `0x080000CC` | 168 | Native IDO exact |
| `func_08000174_6AE954` | `0x6AE954` | `0x08000174` | 64 | Native IDO exact |
| `func_080001B4_6AE994` | `0x6AE994` | `0x080001B4` | 80 | Native IDO exact |

The entire contiguous 312-byte span `0x6AE8AC..0x6AE9E4` matches the original instructions, SHA-256 `28dc78f560e00863470a0034bd08e56873328d39a28bc1632b105024f1aabb17`. All three functions match original positive-sized ELF FUNC names, addresses and sizes. The combined original-ID0-5.3 C object has **26 source relocations**; external symbol address-taking is deliberate because IDO emits the original `lui/addiu/jalr` overlay-call sequence, rather than an incompatible direct `jal`.

## Fresh upstream scratch whole-ROM integration

The untouched pinned upstream original build produced an exact **33,554,432-byte USA ROM** (SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`). In a separate disposable copy of that **upstream checkout**, the original resource-26 assembly was split into prefix and suffix while replacing exactly the 312 bytes in between with native compiled C. To reproduce the original overlay `SUBALIGN(4)` code layout, the integration trimmed **only verified zero compiler/assembler end padding** in ELF section metadata (8 bytes from C, 4-byte prefix padding, 4-byte suffix padding); no instruction bytes or original ROM data were patched. All trimmed sections were checked for zero bytes and absence of relocations into padding.

The resulting scratch rebuilt **full 33,554,432-byte ROM was byte-for-byte identical** to the original, SHA-1 unchanged. Original ELF checks passed **7,376/7,376 positive-sized FUNC identities**, and all **207/207 semantic `.rel.file_26` relocations** remained equal. This was rerun from a fresh scratch copy. The proof is an **upstream-only whole-ROM integration**: it does **not** integrate the connected decomp branch's accepted C functions.

## Host sanitizer regression and limits

The committed `decomp/research/test_file26_mr_arrow_chain_20261117.c` is a GCC host test for the actual candidate source. It passed `-fsanitize=address,undefined` for the actor state `+0x68 & 0x200` gate, saved ID `0x104` argument, callback chain, and both completion-condition branches. These are **synthetic host tests**, not a game test. The native IDO assembly and original ROM comparison are the separate machine-code proof.

The original resource-40 Ghost Toys torch writer `func_08000124_6E9274` (236 bytes) was also attempted with **five bounded variants**; the best candidates had the right length but MIPS register allocation mismatches at function-relative `+0xA8/+0xC0/+0xD0/+0xD4`. **FAILED_NATIVE**, not included in the matched C and not promoted. Continue to retain original ASM there.

**Production block:** During this research, a *complete authenticated checkout of the current GitHub `chatgptweb/decomp` branch* was unavailable to the native build container (shell GitHub DNS failure; GitHub text-file connector is not an archive materializer). The upstream scratch ROM does **not** satisfy the decomp branch's production combined-manifest proof. Specifically **NOT RUN** here: current production combined `decomp.verify`, strict `decomp.inventory`, all linked source/relocation ownership checks, `decomp.local_ci`. This contribution is `RESEARCH_ONLY` with **zero promoted C**. On inspection the branch already had a separately promoted **782 USA C / 34,392 bytes**, Japan **34 C**, which this task must preserve. Its baseline was 779 earlier in the same day; do not overwrite the newer checkpoint.

## Reproducibility

The companion locally generated bundle `goemon_file26_native312_20261117.zip` contains the original-address isolated IDO verifier, full-upstream scratch integration script, exact 32 MiB ROM/ELF/relocation verifier, source, sanitizer host fixture and sanitized machine-readable proof reports. These scripts require the user-supplied original ROM and pinned toolchain; no ROM, extracted original assembly, ELF binary, save or copyrighted asset is contained in this commit or bundle. The C source and sanitizer fixture in this commit are **byte-identical** to the locally tested files (Git blob IDs `4e2e19a4189e6ccd177f411934fc46c86e7c916f` and `f9465043e8072a90aa9b6387b78d74a92ea556d5` respectively).

**Next gate:** stage these three matched functions into a newly authenticated complete live GitHub branch checkout, retain all **782 currently accepted USA C**, then run fresh complete-USA-ROM G2, source/ELF/relocation/inventory and full local CI. Only then count 782→785 if exact. No automatic promotion of an isolated or upstream-only match.
