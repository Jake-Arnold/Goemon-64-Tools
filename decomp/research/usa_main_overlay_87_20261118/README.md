# USA main / overlay 13–20 original-address native-exact candidate sources

This directory contains **87 research-only C functions** independently compiled by original IDO 5.3 to exact original USA instruction bytes (912 bytes total). The sources were also installed together in a disposable upstream build yielding the complete byte-identical original USA 32 MiB ROM, while preserving 7,376 ELF identities and 35,563 main/overlay relocation entries.

`sources/` contains the exact per-function C files. `test_actual87.c` is the actual GCC ASan/UBSan test fixture executed for all 87 functions.

The research-only report is `decomp/docs/USA_MAIN_OVERLAY_NATIVE87_USA_20261118.md`; JSON evidence is `decomp/results/usa_main_overlay_native87_upstream_scratch_20261118.json`. A separate ZIP contains the full per-function fingerprints and disposable scratch repro scripts; no game assets are stored here.

**NOT PROMOTED.** The combined decomp production checkout (864 accepted USA C functions) was not available for a fresh canonical native/ROM/ELF/inventory/full CI run. Keep original assembly in production until all gates pass.
