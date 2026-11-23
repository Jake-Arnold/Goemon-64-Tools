# Japanese file_18 family13 donor ports — RESEARCH_ONLY

## 23 November 2026 — Japan file18 family13 exact native donor ports (research only)

- Verified live stable/decomp@512999319638c367005da96aaf1e61003402ca09, authenticated same-SHA source archive, original Japanese retail and expanded ROMs, pinned upstream and original IDO5.3. Translated all 13 USA family13 PR #198 native C sources using original Japanese instruction correspondences and region-specific ELF symbols/addends, not a fixed address delta. All 13 Japanese functions (2,136 original bytes, 534 instructions, 107 original ELF symbolic relocations) exact in isolated linked original-ROM/ELF extent/relocation checks, 13/13 compiled negative controls rejected. All direct static callees of JP func_80212788_67BE78; emulator runtime not traced. Per-function source and control hashes, original ROM hashes, source owners and offsets in decomp/research/jp_file18_family13_20261123/manifest.json.
- Nine constructor/initializer original line-grouping controls independently reproduce scheduling mismatch at +0x8; two nested state handlers reuse existing source pattern, mutated-state controls differ at +0x0; two unsigned conversion controls with signed intermediate yield wrong extent (24 vs 144 bytes). No new compiler generalization. Actual-source GCC ASan/UBSan tests 38,912 PASS. Fresh JP2428 stored integrity validation PASS.
- RESEARCH_ONLY: Japanese 2,428 C / 4,948 ASM and USA 2,164 C / 5,199 ASM remain unchanged. Full canonical Japan 2,428+13 source-unit integration, complete expanded/retail ROM identity, full function/global/relocation inventories, new-claim promotion integrity and full local_ci NOT RUN. Source-only ZIP goemon-japan-file18-family13-native-research-20261123.zip SHA256 ac00a07dfbf106f9c9deee6522e1c0def2134a1b3ed4f366cfda75e97c6c2151 delivered in task conversation; includes original native replay, full per-instruction relocation correspondence, all C sources and controls and host test. No ROMs, original ASM or binaries included.


## Reproduction

Authenticate private Japan-0 ROM and pinned upstream. Use the original build environment and Splat split config/japan_0/splat.yaml, then assemble three original ELF parent objects:

```sh
make VERSION=japan_0 build/japan_0/asm/japan_0/680430.s.o build/japan_0/asm/japan_0/682300.s.o build/japan_0/asm/japan_0/685A30.s.o
```

Unpack the supplied source-only ZIP, then run its exact original-ROM replay and host sanitizer test:

```sh
python3 replay.py --upstream /private/mnsg --binutils /private/deps/bin --lib /private/runtime/lib --quirks /private/current-Goemon-64-Tools/decomp/COMPILER_QUIRKS.md --out /tmp/jp13-replay.json
sh run_host.sh
```

The committed manifest records original offsets, sizes, source and control hashes, original-code hashes, symbolic relocation counts and donor function identities. The ZIP includes full per-instruction mapping and replay evidence. Do not merge as a matching-C promotion.
