# Japanese original ROM token 11 — source audit and isolated test

20 November 2026. Status: RESEARCH_ONLY; no native display evidence yet.

Original Japan-0 32 MiB SHA-1: 6f8745fecc3a5e7d4918c7a73353eb0726116ded.
Retail normalized 16 MiB SHA-1: 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b.

## Original source evidence

The existing indexed dialogue extractor was reproduced independently against the hash-verified original decompressed ROM: 5,039 records, 5,694 direct references. Of positive token IDs 0 through 13, only 11 (one indexed occurrence) and 13 (7,305 spaces) occur. The one source record containing 11 is explicitly referenced by a real 0x8010 script command.

| Property | Verified value |
| --- | --- |
| Resource ID | 97 |
| Resource start in decompressed image | 0x7575E0 |
| Record offset in resource | 0x2B60 |
| Decompressed image byte offset | 0x75A140 |
| Script reference within resource | 0x73FC |
| Script command image offset | 0x75E9DC |
| Script instruction and operand | 0x00008010, 0x08002B60 |
| Original signed text tokens | 16, 303, 59, 11, -60, followed by terminator -1 |
| Verified partial Unicode text | う〜ん<token:11> followed by newline |

The surrounding script references text offsets 0x2B5C, 0x003C, 0x2B60, 0x2B6C and 0x2B8C. Token 11 is deliberately present within a valid source record, not an accidental scanner match. Its location after a hesitation phrase suggests a visual or special text effect, but does NOT establish whether it is a glyph, invisible spacing, or engine control. Preserve the unmapped token.

## Local-only A/B native glyph experiment

Two new retail .z64 files were produced from the user-supplied original Japan-0 ROM, using the pinned decompression and manifest-driven native LZKN64 recompression pipeline. The file lengths were padded to exactly 16,777,216 bytes. Both change only the original glyph ID 78 (ど) in the known Kai Highway area banner (resource 82 +0x18, decompressed location 0x742366). The underlying original signed token row is 13,13,13,13,13,19,15,78,16.

Variant 1: 78 -> 11; original visible part かいどう becomes candidate かい<token:11>う.
Retail SHA-1: e7e84f434f89eab32ea871b1c6a0340883f2a1b2.

Variant 2: 78 -> 212 (known ！); positive comparison かい！う.
Retail SHA-1: 1b98fbf664dffcb9f8d737bae3e78a18b8fd7703.

A baseline unmodified retail recompression was decompressed to the exact original 32 MiB image SHA-1; its compressed bytes differ from the historic retail compressed image, which is expected for an independently recompressed image. Both experimental retail ROMs were decompressed and each compared byte-for-byte with its intended altered image. Each altered decompressed 32 MiB image differs from the original at exactly ONE byte, offset 0x742367, encoding the new signed 16-bit token. Header CRC was recalculated by rommy.py. Nothing changes the VM controls or source ROM.

## Boundary and further evidence

There is no available Project64 or other live renderer in this container. No emulator screenshot, texture lookup, or glyph-code semantics were proven. The ROMs are supplied as conversation attachments only; NEVER commit source ROMs, test ROMs, extracted font assets, screenshots, or raw resource bytes.

Expected A/B test: load each retail ROM separately in Project64, travel to Kai Highway, compare third character of the area subtitle. If token 11 displays a glyph, cross-check its visual identity with the original resource-97 phrase before adding it to the canonical editor map. A blank, layout effect, or unexpected rendering is NOT evidence of a specific Unicode glyph. Source guard tests are in tests/test_dialogue_token11_research.py.

## 20 November 2026 — User-supplied native screenshot confirmation

The first image shows Kai Highway with lower line `かい！う`, matching the prebuilt canonical `212=！` control. The second image explicitly identifies the running ROM as **`jp-kai-token11-probe.z64`** and also shows `かい！う`. The token-11 retail ROM was independently proven in this investigation to alter only the third subtitle glyph (78 to 11) at original Japanese resource 82 +`0x18`. Accordingly, **token `11` is a visually rendered fullwidth exclamation mark `！`**. The original resource-97 record can be transcribed visually as `う〜ん！` followed by newline.

**Critical encoding distinction:** `11` and `212` are separate original numeric tokens displaying visually indistinguishable exclamation glyphs. The editor retains canonical `！ -> 212` and records `11` separately as `JP_NATIVE_RENDERED_ALIASES={11:'！'}`. Lossless source text keeps `<token:11>` so an unchanged original record survives byte-for-byte; read-only previews show `！`. No evidence yet proves identical underlying atlas coordinates, glyph advance metrics in other contexts, or identical renderer implementation.

Current project counts: **243 screenshot-backed token IDs**, comprising **242 distinct canonical screenshot-backed editable mappings** plus one duplicate alternate `11`; **326 Unicode-editable IDs** including 84 source-order-inferred kana; and **0 unidentified positive token IDs in the original 5,039-record static index**. Unobserved `183=７` remains source-absent and unproven. The legacy excluded-token guard remains for old generated probe manifests, but current unknown-token discovery explicitly recognises token 11 as a native visual alias.

Toolkit v0.11.77: `practice/dialogue_japan.py`, `practice/dialogue_kana.py`, `practice/dialogue_glyph_probe.py`, read-only preview note and regression tests updated. The original Japanese source image and all proprietary assets remain unmodified and uncommitted. New CI status must be verified independently.
