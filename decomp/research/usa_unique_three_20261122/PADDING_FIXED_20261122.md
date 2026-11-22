# Three truly new USA original-ROM- and ELF-exact C functions

**22 November 2026 — RESEARCH_ONLY / native original-upstream fully proven. No canonical accepted-C promotion.**

This source-only kit contains an independently replayed, original-SGI-IDO matching-C build for three original USA ASM-owned functions. It resolves the previous eight-byte ELF function-size discrepancy caused by the original mixed C/`GLOBAL_ASM` source unit.

| Function | ROM offset | Guest VMA | Original bytes |
|---|---|---|---:|
| `func_8000A18C_AD8C` | `0xAD8C` | `0x8000A18C` | 48 |
| `func_8000AAE8_B6E8` | `0xB6E8` | `0x8000AAE8` | 40 |
| `func_8000AB30_B730` | `0xB730` | `0x8000AB30` | 68 |
| **Total** | | | **156** |

The functions are absent from the complete 1,956-function historical accepted-C proof, the nine newer accepted scheduler functions, and the 51+48 independent USA research candidate lists. Earlier draft PRs #162/#164 included seven accepted rediscoveries; those **do not** count and are explicitly excluded.

## Compiler quirk and its resolution

The unchanged neighbour `func_8000AFA8_BBA8` has original ROM function extent **752 bytes** ending at `0xBE98`; its main-segment source contains two further unowned `nop` padding instructions at `0xBE98` and `0xBE9C`. The original next function starts at the 16-byte-aligned address `0xBEA0`. The vendored `asm-processor` incorrectly attributes the final two padding NOPs to the neighbouring `FUNC` symbol whenever those NOPs remain inside its embedded `GLOBAL_ASM` source file, inflating the symbol to 760. Explicit `.size` is not sufficient in the injected object, although standalone GNU `as` obeys it.

**Proven workaround, no machine-code patch and no synthetic function:** keep the Splat mixed C/ASM segment `0xB280` ending at the next existing **original** ASM segment boundary `0xBEA0`; after every Splat split, extract the original generated neighbour assembly and remove exactly those two *post-endlabel* padding NOPs from the `GLOBAL_ASM` fragment (fail closed if any instruction, offset or count differs); let the original linker fill the eight unowned alignment bytes automatically. All three authored function bodies and the neighbour have their **original** symbol extents.

The `COMPILER_QUIRKS_entry.md` file contains the exact compiler flags, unsuccessful controls, native and ELF evidence, caveats and instructions for adding the finding to `decomp/COMPILER_QUIRKS.md` in the repository.

## Actual verification

The repaired candidate and the original pinned upstream source were independently built with original IDO 5.3. A separate clean scratch extraction/build reproduced all checks:

- Original USA retail SHA-1: `df8083a54296b8c151917c5333e1c85f014a2a66` (16 MiB).
- Original decompressed/rebuilt USA ROM: **33,554,432/33,554,432 bytes exact**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Exact **7,376/7,376** positive-sized original ELF `FUNC` identity multiset (addresses, lengths, binding, visibility, section and names).
- Exact **82,216/82,216** original-upstream ELF relocation multiset (section, offset, kind and symbol).
- Neighbour `func_8000AFA8_BBA8`: **752/752 bytes**, not the previous 760-byte artifact.
- GCC 14.2 and Clang 17 AddressSanitizer + UndefinedBehaviorSanitizer **PASS** (4,096 deterministic test cases per original C source); **three** mock-input Python quirk tests PASS.

The verified candidate ELF SHA-256 (metadata only): `af291875532b674fde3070a460d356c611108af58c3088114eb4fdb1904d9a73`. Complete metadata evidence is in `evidence_padding_fixed.json`.

## Reproduce with locally owned private inputs

Use a **clean original pinned upstream checkout** with already extracted Splat ASM and rebuilt reference ROM. Set `<PRIVATE_UPSTREAM>`, `<DEPS>`, `<RUNTIME>`, `<NEW_OUT>` to real local paths; never place private ROMs or compiled outputs in the source-only ZIP or Git.

```bash
python3 verify_original_unit.py \
  --checkout <PRIVATE_UPSTREAM> \
  --deps <DEPS> --runtime <RUNTIME> \
  --out <NEW_OUT> --jobs 16
python3 -m unittest discover -s tests -p test_padding.py -v
bash tests/run_host.sh <NEW_HOST_OUT>
```

The verifier refuses existing output directories, mismatched ROM and commit hashes, dirty tracked upstream sources, wrong original instruction hashes and unexpected generated ASM. It alters only a copied scratch checkout. Raw original assembly, ROM, ELF, compiler and compiled objects are never exported; sanitized JSON records the results.

**Mandatory unresolved production gates:** no full current USA 1,965-accepted-C staging adapter build was available in this execution environment. Thus `python3 -m decomp.verify`, canonical 82,103 semantic relocations, strict inventory and full `decomp.local_ci` are **NOT RUN**. USA official **1,965 accepted C / 84,648 original bytes**, unchanged; all original ASM ownership remains. Japan unaffected. This research is not ready to merge as a production acceptance change.
