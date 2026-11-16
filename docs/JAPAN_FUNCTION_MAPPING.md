# Japanese executable and overlay function mapping

These are **reverse-engineering candidate discovery tools**, not a playable Japanese build.

## Inputs

- USA expanded 32 MiB ROM SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`
- Japan revision-0 expanded 32 MiB SHA-1: `6f8745fecc3a5e7d4918c7a73353eb0726116ded`
- USA N64Recomp symbol file: upstream `klorfmorf/Goemon64RecompSyms/mnsg.syms.toml`
- Section/overlay boundaries: `klorfmorf/mnsg/config/{usa,japan_0}/splat.yaml`

All sources must be provided locally. No ROM/assets are bundled or exported.

## Main executable scan

    python3 -m decomp.japan_function_map USA.decompressed.z64 JP.decompressed.z64 --output /tmp/main-candidates.json

On the supplied ROM revisions, this yields **633 unique structural starts from 781 distinct USA direct-JAL entrypoints**. The other 148 are either ambiguous/unmatched (129) or not informative (19). It uses unique 16-instruction signatures, not evidence of whole-function equivalence. Use `--us-symbols /path/to/mnsg.syms.toml` to verify the full normalized instruction shape of known USA functions.

## Main and every matched executable overlay

    python3 -m decomp.japan_overlay_map USA.decompressed.z64 JP.decompressed.z64 \
      --us-splat /path/to/mnsg/config/usa/splat.yaml \
      --jp-splat /path/to/mnsg/config/japan_0/splat.yaml \
      --us-symbols /path/to/Goemon64RecompSyms/mnsg.syms.toml \
      --output /tmp/jp-overlay-candidates.json

The overlay parser filters CPU code from data using the original Splat file boundaries, validates the USA symbol section identities, and searches each corresponding Japanese overlay independently. It never assumes one universal ROM or VRAM offset. Ambiguous candidates and out-of-range functions are excluded. A function is exported only when the **entire original instruction length** has the same normalised code structure at the mapped Japanese address.

### Verified samples

| Area | Tested | Full structural matches |
| --- | ---: | ---: |
| USA `.main` symbol sample | 20 | 16 |
| Impact `.file_13` original-symbol sample | 24 | 14 |

Impact examples:

| USA code address | Japanese code address | Size | Exact instruction words |
| --- | --- | ---: | ---: |
| `0x801D2F40` | `0x801D8660` | 216 bytes | 54/54 |
| `0x801E2874` | `0x801E7FB0` | 192 bytes | 43/48 |

The USA N64Recomp symbol corpus has 7,376 functions across 72 sections, including 1,231 in `.main`. These candidates provide an evidence-based basis for a Japanese symbol port. They do not identify all indirect-call functions or source-level gameplay differences.

**Important:** The normalization deliberately masks I-format immediates and J/JAL targets, so structural equivalence is NOT behavioural equivalence. The JSON is not a complete N64Recomp symbols file and does not enable a Japanese game in the existing USA executable.

## Verification and next gates

- Run `python3 -m unittest tests.test_japan_function_map tests.test_japan_overlay_map -v` (nine synthetic tests passed locally).
- Both original expanded ROM hashes verified; 20 main and 24 Impact real-symbol samples ran against real ROM bytes.
- Full-overlay whole-project run, Japanese N64Recomp code generation, runtime build, gameplay, and runtime savestates remain outstanding.
- Next: run using complete original symbols and the two complete upstream Splat configs; fill gaps and remap Japanese patch functions/overlays; test an isolated Japanese recomp target in a writable upstream checkout.
