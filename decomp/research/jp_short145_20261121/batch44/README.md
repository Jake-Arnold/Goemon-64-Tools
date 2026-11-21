# Goemon Japan second pass: alternative structural C research

This is a **new non-overlapping batch** following the earlier 101 isolated exact reconstructions. The algorithm groups Japanese assembly by instruction-word structural signatures **after masking immediate operands**, then reconstructs C from parameterized field offsets, calling ABI, floating-point argument types and volatile stores. It checks each candidate independently against its **original Japanese ROM offset** using the original SGI IDO 5.3 compiler and source-symbol-derived MIPS relocation fields.

**Proof: ISOLATED_RELOC_EXACT / RESEARCH_ONLY**. The second-pass count is not added to the official 2,118 Japan C count. No combined 33,554,432-byte original ROM acceptance, 7,376 original ELF identities, all 80,747 semantic relocations, full local CI or GitHub promotion was run in this batch. The existing 101 and this new batch have no function-name overlap; source C and hashes are included. No ROM, proprietary compiler, assembly, object files or other game assets are packaged.

**Reproduce** (Linux, pinned original `mnsg` checkout plus private Japanese expanded ROM):

```sh
python3 verify_isolated.py --upstream /path/to/pinned/mnsg --expanded-rom /path/to/JP_expanded_32MB.z64 --lib-dir /path/to/binutils/lib --objcopy /path/to/mips-linux-gnu-objcopy
```

The reproducer compiles original IDO C, reads original Splat assembly for referenced symbols, checks all reported relocations and compares each instruction byte to the original Japanese expanded ROM. This still does not prove native whole-ROM compatibility or source/overlay placement.
