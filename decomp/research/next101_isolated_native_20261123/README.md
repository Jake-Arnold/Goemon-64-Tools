# Additional 101 USA/Japan native SGI IDO 5.3 matching-C research candidates

Authenticated live base `stable/decomp@838e9f87c3a860973e9d168b58fcf88bd456bfb4` (post previous 72 USA / 28 Japan promotions). The 101 original-address targets were still ASM-owned at this base: **47 USA + 54 Japan**, all **less than 100 original instruction bytes**. Official accepted C at the base is USA 2,164 / JP 2,398.

**Native isolated exact (research only): 101 functions, 6,788 original bytes, 347 symbolic relocations, and 101/101 compiled mutated C negative controls rejected.** Complete current C baseline mixed-unit integration, expanded 32 MiB ROM identity, complete original ELF and relocation inventory, exact retail ROM, region-wise strict inventory, full local CI and atomic canonical G2 promotions were **NOT RUN** for these 101. Do **not** increment official matching C counts, change accepted manifests, or treat matching ASM signatures alone as matching-C proof.

The original USA and Japanese private expanded ROMs, their genuine Splat original ASM, pinned IDO 5.3 compiler and MIPS objcopy are required to reproduce. Sources and native harness are shareable; original retail ROMs, original ASM and compiler binaries, object files, symbols and original machine-byte dumps are deliberately excluded.

```bash
LD_LIBRARY_PATH=/PRIVATE/goemon-runtime-additions/lib \
python3 replay.py \
  --usa-rom /PRIVATE/usa/mnsg-japan/config/usa/baserom.decompressed.z64 \
  --jp-rom /PRIVATE/jp/mnsg-japan/config/japan_0/baserom.decompressed.z64 \
  --usa-splat /PRIVATE/usa/mnsg-japan/asm/usa \
  --jp-splat /PRIVATE/jp/mnsg-japan/asm/japan_0 \
  --ido /PRIVATE/usa/mnsg-japan/tools/ido-5.3/cc \
  --objcopy /PRIVATE/goemon-dependencies/bin/mips-linux-gnu-objcopy \
  --readelf /usr/bin/readelf \
  --ledger /PRIVATE/Goemon-64-Tools/decomp/COMPILER_QUIRKS.md \
  --output /tmp/goemon-replay-new100
```

`replay.py` authenticates both 32 MiB ROM hashes, every original ASM instruction and source/target code SHA256, original MIPS guest VMA and ROM offset, original source ownership and size, IDO compiler hash and flags, exact generated machine instructions (relocation-masked), all original symbolic relocation tuples and target STT_FUNC extents. It rereads the compiler quirks ledger before every attempt. Negative controls add one volatile local declaration to *each target function* and independently compile and reject the changed result. The output is a sanitized `native_results.json`.

**Compiler classification:** `NO_NEW_COMPILER_FINDING` for each successful attempt; no new generalizable IDO quirk is claimed. The recorded 101 are independent distinct original addresses; original decomp research-only matches in nine existing-source C files, plus seven independently reported in open research PR #191, were excluded from this count (but remain available for promotion analysis). Candidate selection combined cross-region/source donor ports and fresh original ASM state/timer/callback reconstruction. The recorded negative control is a deliberate source behavior change, not an instruction patch.
