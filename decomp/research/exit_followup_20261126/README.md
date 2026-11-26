# Exit overlay follow-up: two native-exact coordinate initializers

Status: **ISOLATED_EXACT / RESEARCH_ONLY**; original assembly remains. Verified live `stable/decomp@ee6328ab121bb59b27f03a54c3c80563a720fe77`, private original USA and Japan retail/expanded ROM SHA1, pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, native IDO 5.3 SHA256 `76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0`.

| Region | Function | Original ROM offset | Instructions | Original relocations |
| --- | --- | --- | --- | --- |
| USA | `func_80216E1C_5D22EC` | `0x5D22EC` | 14/14 (56 B) | 3/3 named |
| JP | `func_8021BB8C_5D711C` | `0x5D711C` | 14/14 (56 B) | 3/3 named |

Both compiled with the exact pinned original IDO flags and linked at original VMAs. Compared against the ROM independently reconstructed from original Splat ASM. Exact output includes raw and linked named relocations and positive-sized ELF identity. Two altered-source negatives set Z to 0.0 instead of the common float: both produce 60 B, 3/14 identical instructions and first +0x0C mismatch; correctly rejected. Per-attempt classification: `NO_NEW_COMPILER_FINDING`.

Both objects expose task->child at +0x18 and x/y/z at object +0x1C/+0x20/+0x24. Native callback follows all three coordinate stores. GCC and Clang address/UB sanitizer runs of actual sources: 4 runs x 4096 iterations = 16384 successful semantic cases.

Exact verified C source and altered controls are committed in `sources/`. The complete portable native replay source `replay.py`, full 4-attempt JSON proof with source and compiler hashes, host test `test_coords_host.c`, README and SHA256SUMS are supplied in the **same-chat** source-only archive `goemon-exit-followup-20261126.zip`, SHA256 `175b3f4702b4a9ef20b85ede7c0d9a286cdd78ba40b8d08088d4d13e22692ade`. Neither ROMs, toolchain nor generated original ASM are distributed.

Bounded adjacent negative research: USA `80215230` / JP `80219FC0` dispatchers 17/64, wrong stack/register allocation and size 260 vs 256. USA `802157C4` initializer 24/27 instructions, correct extent, +0x28 scheduling mismatch; JP counterpart remains nonmatching. USA `8021617C` and JP `8021AEF4` 172 B field initializers 25/43, +0x08 register allocation mismatch; retain ASM. A trivially matched callback pair already accepted by canonical inventory; not counted. Separate open draft #279 already owns both decoders and the 80 B initializer pair; not counted. Pending PR filename audit #279/#276/#250/#202/#200/#194/#191/#190/#186 gave no address-name overlap; not an exhaustive pending-manifest audit.

**Not run**: whole original owner, full native G2 original 32MiB ROM, global/ELF inventory, promotion-integrity. **Canonical counts unchanged**: USA 3056 C, JP 2995 C. No toolkit changes or gameplay claim. Next targeted work: fix three IDO scheduling differences in the adjacent 108 B initializer, or verify the two 56 B candidates under an integrated G2 promotion.
