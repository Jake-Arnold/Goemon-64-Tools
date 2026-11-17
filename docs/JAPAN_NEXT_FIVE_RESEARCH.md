# Japanese Goemon — five further isolated C matches (research only)

**16 November 2026:** Native IDO 5.3 compiled the five C files in `decomp/japan_adjacent_research/` with `-G 0 -non_shared -O2 -mips2`. Each was linked individually with GNU MIPS at its original Japanese RAM address, with exact global-symbol relocations, and compared to the pinned original 32 MiB Japanese ROM (SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`). All five instructions match across **180 original code bytes**. Each standalone object had exactly 12 zero-only trailing bytes; no original machine-code payload was changed during section metadata adjustment.

| Original ROM | C function | Original bytes | Isolated proof |
|---|---|---:|---|
| `0x3A7AC` | `func_80039BAC_3A7AC` | 36 | Exact |
| `0x3A7D0` | `func_80039BD0_3A7D0` | 36 | Exact |
| `0x3AA34` | `func_80039E34_3AA34` | 36 | Exact |
| `0x3AA74` | `func_80039E74_3AA74` | 36 | Exact |
| `0x3AA98` | `func_80039E98_3AA98` | 36 | Exact |

These are conditional audio/flag state setters. The neighbouring `func_80039E58_3AA58` (28 bytes) compiles to the expected size but differs in register allocation, addressing and branch delay-slot placement; it remains assembly-owned.

**Do not promote:** No complete linked 39-function Japanese ROM was generated or recompressed, and there is no strict final ELF inventory proof for these five. The 34-function / 1,912-byte Japanese baseline remains the formal total. Next acceptance requires fresh Japanese Splat split, reviewed C/ASM boundaries, original GNU MIPS link, exact full 32/16 MiB hashes, strict source/relocation/ELF verifier and new manifest.

The separate source-only archive `goemon-japan-five-next-adjacent-probes.zip` was generated and checked: SHA-256 `016ad4d9a636aec2d44f134bb8c502496924e13751c38bd90ab52d042633aaeb`. No ROM, generated assembly, binary objects or proprietary compilers are included.
