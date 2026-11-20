# Goemon USA: 500 novel matching-C research checkpoint (19 Nov 2026)

## Proof boundary

- Canonical `chatgptweb/decomp` remains **1,500 accepted USA matching-C** and **5,863 ASM entries**. None of this research was promoted.
- The prior **116-function** source-only package (`goemon_116_new_isolated_matching_c_20261119.zip`, SHA-256 `ea698abc386e488ea6e6f1e4b51ced38bb75c6d19b6bdc196787e8666bca7d04`) is the fully archived and independently recompiled research baseline. It is a separate conversation attachment.
- During this continuation, native compiler sweeps and deduplication recorded a provisional cumulative **458 isolated original-address matches** against that 1,500-C baseline. These were **not** combined into a final self-contained research archive or recompiled en masse before the tool execution environment was replaced. Do **not** treat the provisional 458 as a fully preserved verified source set or as accepted C. The target of 500 was not reached.
- The sweep recorded 4,236 standard candidate trial entries, including **959 isolated exact original-machine-code matches before ownership deduplication**, plus smaller ABI, pointer-type and unsigned/stride repair batches. The final complete candidate source/report files from those sweeps are not available in this checkpoint.
- Four important reconstruction patterns proved fruitful: missing inherited MIPS argument forwards; signed versus unsigned constants for u8/u16 stores; pointer type correction in generated m2c; and pointer arithmetic scaling (`float *p; p += 1` to produce a 4-byte increment rather than `p += 4`).

## One newly reconstructed source preserved

`func_80033D10_34910` at USA expanded ROM `0x34910`, 48 original bytes, from the main section. The original MIPS increments a float pointer by four bytes per iteration; m2c's C used `var_v0 += 4` on a `float*`, causing a sixteen-byte increment. Correcting to `var_v0 += 1` yielded **48/48 bytes of matching native code with zero relocation records and zero wrong instructions** using original IDO 5.3 `-O2 -mips2 -G 0 -non_shared`. The included source is reconstructed from that verified trial and has not been freshly recompiled after the workspace reset. It remains RESEARCH_ONLY.

## Formal verification not run

No combined candidate 32 MiB ROM/ELF gate, `decomp.verify`, `decomp.inventory`, or `decomp.local_ci` was run. No repository source, manifest, counts, or PROGRESS.md changed. A fresh authenticated canonical checkout and source bundle are required for promotion.
