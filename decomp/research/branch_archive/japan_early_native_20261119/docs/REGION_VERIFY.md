# Region-aware Goemon C verification (JPN-006)

**Status: Japanese native build verification PASS on 2026-11-15.**

The existing USA verifier, decomp/verify.py, is not modified. The new
decomp/region_verify.py entry point accepts two regions:

- USA (default): delegates original arguments unchanged to decomp.verify.main.
- Japan revision 0: checks an existing original-address Japanese source-linked
  MIPS build against decomp/regions/japan_0.json.

USA continues to use its original manifest, overlay stages and baseline cache.
Japanese locations, hashes, C sources and compiler objects are recorded separately.

## Japanese verification command

After running the pinned Japanese four-function build from docs/JAPAN_FOUR_C.md,
load the offline binutils PATH and LD_LIBRARY_PATH and execute from this repo root:

~~~bash
python3 -m decomp.region_verify --region japan_0 \
  --checkout /path/to/pinned/mnsg-japan \
  --retail-output /path/to/japan-four-c-retail.z64 \
  --report /path/to/new-japan-region-proof.json
~~~

Select a report path that does not exist. Output reports are never overwritten.
The verifier does not generate or redistribute ROM bytes.

For USA, use the existing command unmodified or invoke the dispatcher with:

~~~bash
python3 -m decomp.region_verify --region usa \
  --upstream /path/to/pinned-mnsg \
  --workdir /path/to/new-workdir \
  --retail-rom /path/to/USA.z64 \
  --report /path/to/new-usa-report.json
~~~

## Japanese proof gates

1. Require exact pinned upstream commit
   7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee with no modified tracked files.
2. Validate the reviewed four-function Splat layout from the original Japanese
   Splat and the separate staged C config.
3. Validate original and rebuilt Japanese expanded ROMs (33,554,432 bytes),
   matching SHA-1 6f8745fecc3a5e7d4918c7a73353eb0726116ded and zero byte differences.
4. Validate original and rebuilt Japanese compressed retail ROMs (16,777,216
   bytes), matching SHA-1 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b and zero differences.
5. Validate the independently reviewed SHA-256 of each C source and enforce
   exact staged-source equality.
6. Compare each native IDO C object's .text bytes and SHA-256 with the original
   Japanese ROM segment. Reject unexpected text relocation entries and extra
   globally defined functions.
7. Confirm the linker map contains exactly one C text section at each original
   Japanese VMA and the expected symbol address, function size and section size.
8. Reject overlapping, duplicate, misaligned or out-of-region manifest entries;
   never map Japanese functions from USA offsets by assumption.

## Verified local run

- Region: japan_0
- Source: pinned mnsg at 7e2029c5...
- Manifest-backed native C: **4 functions, 136 function bytes, two translation units**
- Complete 32 MiB decompressed ROM: **PASS, 0 differing bytes**
- Complete 16 MiB compressed retail ROM: **PASS, 0 differing bytes**
- Both C object source hashes, symbol extents, link-map VMA, machine code: PASS
- Unexpected .text relocations: 0
- Focused ROM-free regressions: **21/21 PASS** (11 new plus 10 earlier Japanese)
- USA verifier entry point: delegated unchanged (unit test); fresh USA native G2 NOT RUN
- Japanese emulator gameplay: NOT RUN
- Japanese PC-native static recompilation: NOT RUN
- New Japanese matching functions: none in this step

The inventory in this verifier is **only four reviewed Japanese C claims**.
It is not a complete list of Japanese ELF functions or remaining assembly.
JPN-007 will build that independent inventory.

Evidence: decomp/results/japan_0_region_verify_2026-11-15.json.
No original ROM, asset extract, generated assembly or compiler binary is committed.
