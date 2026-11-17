# Japan region recomp: 69-section executable overlay scan

## Verified source inputs

- USA decompressed ROM SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`
- Japanese revision-0 decompressed SHA-1: `6f8745fecc3a5e7d4918c7a73353eb0726116ded`
- Original per-region code-section boundaries: upstream `klorfmorf/mnsg/config/usa/splat.yaml` and `config/japan_0/splat.yaml`
- USA patch and function bounds: upstream `klorfmorf/Goemon64Recomp/mnsg.toml` and `klorfmorf/Goemon64RecompSyms/mnsg.syms.toml`

The tools take **local original decompressed ROM images** and Splat configs; they do not redistribute Nintendo game code or assets. The scan was run against the user's two supplied ROMs and the 69 original Splat executable sections (section-only representations of their explicit ROM/VRAM and code/data boundaries).

## Complete direct-JAL section scan

```bash
python3 -m decomp.japan_overlay_entrypoints \
  usa.decompressed.z64 japan.decompressed.z64 \
  --us-splat /path/to/mnsg/config/usa/splat.yaml \
  --jp-splat /path/to/mnsg/config/japan_0/splat.yaml \
  --output /tmp/japan-direct-jal.json
```

| Measured quantity | Count |
| --- | ---: |
| Common executable code sections | 69 |
| USA direct JAL instructions found | 15,919 |
| Distinct USA in-section JAL destination candidates | 2,550 |
| Unique 16-instruction Japanese matches | **1,922** |
| No unique Japanese anchor | 577 |
| Uninformative USA anchor | 42 |
| Too close to section end | 9 |
| Japanese destination collisions within sections | 0 |

Most matching anchors: `.main` 633, `.file_11` 419, `.file_13` 227, `.file_12` 107, `.file_18` 102, `.file_14` 75, `.file_19` 72.

MIPS direct JAL target decoding preserves the nibble from the caller PC. This is necessary for `0x08000000` overlays and for `0x80000000` main/large overlays. Every candidate is qualified by its original *file/section identity*, even if multiple overlays reuse the same runtime address.

**These 1,922 are candidate function entrypoints, not full matching functions.** The scan masks immediate and J/JAL target fields over a 16-instruction anchor and does not prove an equivalent implementation. Indirect functions, non-JAL entrypoints, different code, and ambiguous candidates remain unresolved.

## Audit the Japanese equivalent of the existing USA audio patch

```bash
python3 -m decomp.japan_patch_audit \
  usa.decompressed.z64 japan.decompressed.z64 \
  --output /tmp/japan-audio-patch.json
```

Original USA `func_80038210_38E10` is 436 bytes. Its 109 instruction structures all match Japanese `0x80037E80` (90/109 words byte-identical). Original patch site `0x80038290` maps to Japan `0x80037F00`, where both versions have original word `0x00E3082B`. Candidate patched word `0x00E3082A` is the same as USA.

The patch audit fails closed unless the complete normalised function body, original patch word and unique destination agree. Its output is **an unapplied candidate**, not a modified ROM, registered N64Recomp instruction patch or tested fix.

## Tests and remaining blockers

**26 local ROM-free tests passed**, including four overlay JAL tests and five audio-patch fail-closed tests. Both actual 32 MiB ROMs were exercised in the 69-section integration scan and function-size check.

The Japanese Goemon64Recomp executable is still not buildable: N64Recomp needs a full Japanese symbols/functions/relocations corpus, region-specific overlays/patches and a separate Japanese executable entrypoint. The current USA GameEntry must not be reused for Japan. Complete Goemon64Recomp savestates require a separate host runtime snapshot implementation.

No actual Japanese native runtime, title screen, gameplay, input, saving or audio has been built or executed. The connected GitHub tool can write the Goemon-64-Tools branch but cannot fork `klorfmorf/Goemon64Recomp`.
