# Independent Japanese N64 ELF function inventory (JPN-007)

**Verified 2026-11-15:** Parsed the native Japanese revision-0 linked ELF with the supplied GNU MIPS objdump, after running the full Japanese region verifier. This inventory is independent of the USA function tally.

## Exact Japanese ownership

| Class | Identified ELF entries |
| --- | ---: |
| All positive-sized executable F symbols | **7,376** |
| Explicit .NON_MATCHING assembly-marked entries | **7,372** |
| Manifest-reviewed native Japanese C entries | **4** |
| Other unmarked entries without reviewed C provenance | **0** |
| Distinct executable ELF sections, including entry and IPL3 | **73** |
| Same-section same-address/size aliases | **0** |

**Important:** The 7,376 count includes the boot entry function and IPL3 binary placeholder exposed as ELF type-F symbols. It is a count of ELF symbol entries, not a proof of 7,376 independently identifiable gameplay functions. Additional data/rodata .NON_MATCHING markers are excluded (9,065 markers have no matching positive-sized type-F symbol). Multiple overlays can share a guest RAM address; identity is preserved by section and name.

The complete per-section inventory and fingerprint are stored in decomp/results/japan_0_elf_inventory_2026-11-15.json.

The largest remaining assembly regions are:
- .main: 1,227 assembly-marked + 4 C = 1,231 entries
- .file_13: 1,000 assembly-marked
- .file_11: 902 assembly-marked
- .file_12: 813 assembly-marked
- .file_14: 392 assembly-marked
- .file_18: 387 assembly-marked

## Reproduction

After an exact Japanese four-function build, run from this Goemon Tools repo with the offline MIPS objdump/objcopy binaries on PATH and their shared libraries in LD_LIBRARY_PATH:

~~~bash
python3 -m decomp.japan_inventory \
  --checkout /path/to/pinned/mnsg-japan \
  --retail-output /path/to/japan-four-c-retail.z64 \
  --report /path/to/new-private-japan-inventory.json
~~~

This first repeats the strict JPN-006 Japan source/ID0/linker/full-ROM proof, then extracts ELF F symbols and NON_MATCHING markers. It rejects unreviewed unmarked functions, missing C claims, symbol-size changes, duplicate symbol names, mismatched assembly markers, and attempts to overwrite the output.

**Tests:** Five inventory-specific synthetic tests plus the prior 21 region/baseline tests: 26/26 PASS. Actual inventory run from the pinned native linked Japanese ELF: PASS. USA's verifier and function counts remain unchanged; no fresh USA G2 was run.

**Next:** Promote additional nontrivial Japanese C functions with exact native source/relocation/full-image gates. This inventory provides a reproducible baseline to detect accidental function status or address changes. No original ROM, extracted assembly or binary assets are committed.
