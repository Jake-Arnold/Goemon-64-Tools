# Japanese Impact dynamic RAM observations — 16 November 2026

**Source:** user-supplied `Impact Values.zip`, three `goemon-discovery-report-v1` read-only value-search exports dated 2026-11-16 20:03–20:04 UTC. This evidence is guest-RAM value matching, not MIPS instruction-access tracing or a live pointer-chain capture.

| Report name | JP guest address | Type | Previous / initial | Final | Samples | Interpretation |
| --- | --- | --- | --- | --- | ---: | --- |
| Impact Values Japanese enemy hp | `0x802F7060` | big-endian `u32` | 1965 | 1965 (0x7AD) | 1 | Candidate enemy HP |
| Impact Values impact ryo | `0x802F7064` | big-endian `u32` | 400 | 396 (0x18C) | 2 | Candidate Ryo, decrease observed |
| Impact Values impact hp | `0x802F7068` | big-endian `u32` | 140 | 440 (0x1B8) | 2 | **Likely oil**, despite user report's HP label |

The aligned fields imply the sampled controller structure base **B = `0x802F7000`**, producing offsets B+0x60/B+0x64/B+0x68. Original USA MIPS field references and the independently written USA controller analysis `codex/goemon-impact-research:docs/IMPACT_BATTLE_MEMORY_TRACE.md` establish the corresponding meanings: enemy HP, Ryo, oil. The Japan values corroborate layout reuse at this observed dynamically allocated address, which may be reused or freed on scene changes.

**Limits:** One or two snapshots are insufficient to establish who writes each field. These reports do not contain load/store watchpoints or the actual pointer held in the Japanese `file_13` overlay's BSS. Original Japanese Splat says `file_13` starts at `0x801D0B90` and BSS begins `0x80214600`; that boundary is **not** automatically a proven live controller-pointer slot. Do not add toolkit writes, assume a stable arena allocation, or rename HP/oil from the misleading search title without code/scene confirmation. Cross-region function VMAs belong to code, not these heap addresses.

**Impact on matching C:** the layout annotations can guide 16/32-bit offsets, signed counter selection, and callback producers in forthcoming functions. Exact IDO instruction equality and separate full-ROM/relocation acceptance remain mandatory.
