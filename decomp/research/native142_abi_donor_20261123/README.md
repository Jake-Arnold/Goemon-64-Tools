# 142 additional native IDO matches — research only

Base stable/decomp: 512999319638c367005da96aaf1e61003402ca09. Pinned upstream: 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee. 96 USA (6052 bytes / 429 relocations), 46 Japan (3528 bytes / 165 relocations). Total 142, 9580 bytes, 594 symbolic relocations. Native flags: -c -G 0 -non_shared -O2 -mips2. All 142 positives and 142 altered-source controls independently replayed successfully twice (positive exact, negative rejected). All 142 remain ISOLATED_NATIVE_RESEARCH_ONLY. Complete G2, full original linked ROM, whole-unit, full local CI and canonical promotion NOT_RUN; no accepted-count changes.

candidate-index.txt lists region, then VMA_ROMOFFSET:original-byte-count:relocation-count for each func_ identifier. Its SHA256 is b6b04042cd5958755fbe1d1980baff502dbfb9a2aa607080108d5c2d0a82cd6c. Open PR #199 appeared after the archive was generated and was checked separately: zero overlap with these 142 names. Source archive is split for connector transfer; all five Git blob hashes matched the tested local chunks.

Extract the exact 142 source files with:
```sh
cat source_parts/part-*.bin > /tmp/native142-sources.tar.gz
echo 'eacfcef3777e7bee43ac8bb8adb62c5101b234fa9f012dd704e96c9c8b9a77da  /tmp/native142-sources.tar.gz' | sha256sum -c -
tar -xzf /tmp/native142-sources.tar.gz -C /path/to/private/scratch
```

Replay directly without extracting the source archive to your repository. Use authenticated private originals and pristine Splat assembly from pinned upstream. The script verifies the aggregate source archive and index SHA256, exact original 32 MiB regional SHA1, compiler SHA256 and original Splat word/address evidence, and recompiles all positives and their exact regenerated negative controls. It writes sanitized JSON including every source/code hash, relocation tuple, owner, original extent and first mismatch. Example (set W to your local scratch build root):

```sh
LD_LIBRARY_PATH="$W/goemon-runtime-additions/lib" python3 replay_checkpoint.py \
 --usa-rom "$W/mnsg-japan/config/usa/baserom.decompressed.z64" \
 --jp-rom "$W/mnsg-japan/config/japan_0/baserom.decompressed.z64" \
 --usa-splat "$W/mnsg-japan/asm/usa" \
 --jp-splat "$W/mnsg-japan/asm/japan_0" \
 --ido "$W/mnsg-japan/tools/ido-5.3/cc" \
 --objcopy "$W/goemon-dependencies/bin/mips-linux-gnu-objcopy" \
 --readelf /usr/bin/readelf \
 --ledger ../../COMPILER_QUIRKS.md \
 --output /tmp/native142-replay
```

Full source-only session ZIP `goemon-native-142-research.zip` SHA256 cc5ce8efc2e711d8b3edf4522683d547505fd8d89dc0b6509f4baae378df3d12 contains detailed manifest, original variant sources/negative controls, 1204 recorded native attempts and sanitized replay report. Manifest SHA256 a749818d59106fe87b212ab70516bb8b36638e568297d9d374e4cce23509b24b; replay report SHA256 4f170c581f04f9334df5388f54960bdd76219b3ea98a35f1edd07cd1622754bf. The entire ZIP and rejected-variant history are supplied separately in the research session, not uploaded here. This checkpoint contains all positive sources and a tested independently reproducible native proof harness. No ROM, generated ASM, original binary instructions, object files, or proprietary tooling committed.
