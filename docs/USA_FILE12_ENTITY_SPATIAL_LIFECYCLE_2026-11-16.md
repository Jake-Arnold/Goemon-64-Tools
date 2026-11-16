# USA file_12: spatial actor streaming and release (2026-11-16)

**Evidence status:** original-USA ROM static disassembly and user-provided Project64 runtime screenshots. Not a matching-C claim or assistant-run gameplay test.

## Sources and exact build identity

- Retail USA 16 MiB SHA-1: \`df8083a54296b8c151917c5333e1c85f014a2a66\`.
- Reconstructed original 32 MiB USA decompressed SHA-1: \`6ea0ed71032ce08fc2745f412d84936382197494\` (directly reproduced and hashed using pinned upstream \`tools/rommy.py\`).
- Pinned upstream Splat commit: \`7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee\`; \`file_12\` code begins at decompressed ROM \`0x5C8770\`, VRAM \`0x8020D2A0\`, ending at ROM \`0x5E3C90\`.
- Independent read-only \`python3 -m decomp.file12_spatial_probe --rom <decompressed-original-USA>\`: **38/38 opcode and call-site anchors PASS**. Four ROM-free Python synthetic tests PASS. No game bytes are embedded or exported.
- ROM offsets below refer to the decompressed 32 MiB source, **not** the 16 MiB cartridge ROM.

## Function map from original Splat assembly

| Function | PC / decompressed-ROM start | Size | Interpretation |
| --- | --- | ---: | --- |
| \`func_8020D2A0_5C8770\` | \`0x8020D2A0 / 0x5C8770\` | \`0xCC\` | Calculate three spatial cell indices from reference XYZ |
| \`func_8020D36C_5C883C\` | \`0x8020D36C / 0x5C883C\` | \`0x304\` | Scan neighboring cell lists for inactive placements |
| \`func_80218A54_5D3F24\` | \`0x80218A54 / 0x5D3F24\` | \`0x1D4\` | Initialize actor ID, position, parameters and handlers |
| \`func_80218E7C_5D434C\` | \`0x80218E7C / 0x5D434C\` | \`0xB4\` | Actor update chain, calls release checker |
| \`func_8021A328_5D57F8\` | \`0x8021A328 / 0x5D57F8\` | \`0x1B4\` | Axis-wise range check and optional deactivation |

All five are **still original assembly**. The canonical matching-C production count is unchanged.

## Static spawn trace

1. \`0x8020D2A0\` reads grid configuration rooted at \`0x8015CC30\`, reference-position pointer at grid \`+0x130\`, coordinate origins/scale and cell counts, then calls \`0x8020D36C\` at \`0x8020D354\`.
2. \`0x8020D36C\` iterates bounded X/Y/Z grid cells. It reads axis counts at grid \`+0x1C/+0x20/+0x24\`, candidate-cell expansion at \`+0x44\`, and cell pointer storage at \`+0x38\`. Calls to \`0x80014840\` resolve table handles; raw values must not all be assumed direct RAM pointers.
3. On a candidate 20-byte placement record, \`0x8020D500\` reads the active byte at \`+0x10\`. A nonzero value skips creation; \`0x8020D5D8\` advances by \`0x14\` bytes.
4. After eligibility and successful actor allocation, \`0x8020D5B8\` sets placement active byte to 1, \`0x8020D5BC\` calls \`0x80218A54\`, \`0x8020D5CC\` sets actor state/flags \`+0x68 = 8\`, and \`0x8020D5D0\` retains the placement link at actor \`+0x70\`. **Correction:** \`0x8020D5CC\` sets state 8, not the placement pointer.
5. Two other call sites at \`0x8020DAFC\` and \`0x8020DC18\` call the same initializer by different allocation paths; identical grid-activation semantics are not established for these.

## Confirmed placement and actor fields

| Input from placement | Type | Runtime destination |
| --- | --- | --- |
| \`+0x00/+0x02/+0x04\` | signed 16-bit X/Y/Z | position \`+0x08/+0x0C/+0x10\`, three floats |
| \`+0x06/+0x08/+0x0A\` | unsigned 16-bit parameters | position \`+0x14/+0x16/+0x18\` |
| \`+0x10\` | active byte | changes from 1 to 0 on deactivation |

The actor ID comes from a separately resolved definition at \`0x80218A98\`, stored at actor \`+0x5C\`. The initializer also sets actor \`+0x76\` to 20, then various callbacks may alter state.

Five user-captured successive hits at \`0x80218AF4\`:

| Hit | Actor ID | Placement A2 | Actor S0 | Position V1 |
| ---: | --- | --- | --- | --- |
| 1 | \`0x008E\` | \`0x80387200\` | \`0x8016A900\` | \`0x8014C6A8\` |
| 2 | \`0x008C\` | \`0x80387214\` | \`0x8016A9F0\` | \`0x8014C740\` |
| 3 | \`0x0256\` | \`0x80387228\` | \`0x8016AAE0\` | \`0x8014C7D8\` |
| 4 | \`0x02D3\` | \`0x8038723C\` | \`0x8016ABD0\` | \`0x8014C870\` |
| 5 | \`0x02D4\` | \`0x80387250\` | \`0x8016ACC0\` | \`0x8014C908\` |

Observed strides: \`A2 +0x14\`, \`S0 +0xF0\`, \`V1 +0x98\`; a separate definition pointer advanced \`+0x10\`. Only the placement loop stride is established statically here as a general step. Reused/overwritten RAM staging addresses must not be treated as stable tables or permanent ROM identifiers.

## Conditional range-based deactivation

At \`0x80218F14\` the actor update chain invokes \`0x8021A328\`. That function requires \`actor+0x68 & 8 != 0\` and \`actor+0x70\` non-null. It reads placement signed X/Y/Z and compares the absolute difference to the reference XYZ (pointer at grid \`+0x130\`), individually for each axis:

\`\`\`text
factor = float((u8)actor[0x76]) / 10.0
within_range = abs(placement.x - ref.x) < factor * grid.float_at_0x04
            && abs(placement.y - ref.y) < factor * grid.float_at_0x08
            && abs(placement.z - ref.z) < factor * grid.float_at_0x0C
\`\`\`

The initializer's default actor byte \`+0x76 = 20\` gives initial factor 2.0, but this byte may change. **This is an axis-aligned check, not Euclidean radial distance.** If out of range, an optional flag-controlled helper may execute, then the release path clears \`placement+0x10\`, nulls \`actor+0x70\` and sets \`actor+0x68 = 2\`.

The user's runtime capture at \`PC=0x8021A4B8\`, \`A0=0x8016B350\`, \`V1=0x8039A558\` recorded:

| Field | Before | After | Original PC |
| --- | --- | --- | --- |
| \`0x8039A568\` = placement+0x10 | \`01\` | \`00\` | \`0x8021A4B8\` |
| \`0x8016B3C0\` = actor+0x70 | not recorded | \`00000000\` | \`0x8021A4C0\` |
| \`0x8016B3B8\` = actor+0x68 | not recorded | \`00000002\` | \`0x8021A4C4\` |

The user observed the initializer breakpoint firing on NPC entering range and again on re-entry, not when leaving, while the release breakpoint fired around the NPC disappearing. This supports streaming activation/release **but does not prove immediate memory free, exact timing of visual removal, or that every actor uses the same policy**.

## Next research gates

Trace who schedules \`0x8020D2A0\` and \`0x80218E7C\`, the allocator's reuse/reclamation of state-2 tasks, the two alternate initializer callers, and the types and units of the grid-axis scale fields. Validate the full condition flow before constructing exact original-IDO C. No production manifest, verifier, ROM proof, or toolkit changes are authorized by this research evidence alone.
