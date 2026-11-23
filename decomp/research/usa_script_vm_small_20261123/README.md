# USA script VM small-function continuation — 23 November 2026

RESEARCH_ONLY; published stable/decomp@878d8cffdf3baf98a5dfcf4dc6fc5cb5b7ca45d1, USA 2319 C / 5044 ASM, VM 60/69. Original pinned upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee and original IDO 5.3. Fresh matching-source archive verified; original USA baseline authenticated by exact 32 MiB ROM and original ELF, Japan expanded ROM independently authenticated. No canonical claims added. 27 distinct source files, 58 native invocations including the initial four controls and repeated native replays; all 27 final code hashes identical to the first corresponding result. Read-only comparisons at original VMA and named relocation comparison. Existing ledger read before every compile.

| USA function | Original B | Best measured result | Known blocker |
|---|---:|---|---|
| F6E8 | 48 | 40 exact prefix, 1/1 relocation | Missing terminal return pair |
| F038 | 196 | 196 B, 28/49 exact words, prefix 40 B | Register allocation, spill homes, 2 relocation replacements |
| F480 | 164 | 160 B, first mismatch +20 B, 7/41 exact words including comparison over full original extent | Call and global-reference scheduling; branch-likely loop present, not exact |
| DE80 | 232 | 220 B, 20/58 exact words; alternate 216 B first mismatch +8 B | Saved-register/prologue and control-flow layout |

F038 declaration-order change moves volatile half-index spill from sp+0x24 to the original sp+0x1C, but entry spill becomes sp+0x20 (original sp+0x18); the first register mismatch at +0x28 remains. F480 direct call removes two temporary declarations and improves prefix +0xC to +0x14 (source-expression scheduling). Native emits branch-likely for the digit loop already; global pointer-base reuse and argument-register scheduling remain mismatched. Physical line-grouping controls for F480 and DE80 did not change code. All F6E8 variants reproduce the exact 40-byte prefix, missing the final 8 bytes; never substitute zero padding or synthesize a second return. Across the authenticated original USA ELF 80 positive FUNCs end with the same pair of return sequences and none are accepted C. This is a pattern, not proof of a compiler bug or split function boundary. Original JP counterparts at 0x3FF54, 0x3F8A4, 0x3FCEC, 0x3E6F0 respectively each have a unique full normalized instruction match across the JP main region, and none is in the 2528-C inventory. Normalization masks immediate/jump operands; no JP native proof or donor source claimed. Eight adjacent-address negative controls and two tail-pattern negative controls passed. F038/F480/DE80 source-specific host tests passed 3000/1000/1100 synthetic cases under GCC ASan/UBSan; no gameplay or new-claim G2/CI run.

## Reproduce

Read live policies and ledger. Set REPO, COMPILER, BASE, BIN, LIB, OUT to absolute paths. COMPILER is a clean pinned upstream clone, BASE is the independent original-USA built pinned upstream checkout (ROM exact), BIN is the cross-binutils bin directory, LIB is archived runtime lib. OUT must not exist. From this kit:

```sh
python3 replay.py --repo "$REPO" --compiler "$COMPILER" --baseline "$BASE" --binutils "$BIN" --lib "$LIB" --out "$OUT"
python3 map_jp.py --repo "$REPO" --usa "$BASE/config/usa/baserom.decompressed.z64" --japan "$JP_EXPANDED" --out crosswalk-replay.json
python3 tail_audit.py --repo "$REPO" --baseline "$BASE" --out tail-replay.json
bash host_replay.sh "$REPO"
```

Private original ROM/ASM, compiler binary, generated native objects/ELF and logs containing local paths are not distributed. All sources are research-only. Published C/ASM ownership unchanged.
