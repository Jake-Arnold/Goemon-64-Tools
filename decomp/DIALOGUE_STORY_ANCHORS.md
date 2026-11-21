# Region-specific text tokens as story/VM execution anchors

21 November 2026. This is read-only decomp research tooling, not a matching-C
promotion or a modification to the original ROM. It deliberately lives in
decomp rather than in a GUI toolkit module.

## Where the authoritative mapping came from

The token source was copied from the latest reviewed main branch at commit
1a58d3c159c47d0e02b4fbd1fb12e0748871cd73 and kept REGION-SPECIFIC:

- USA glyphs: practice/dialogue_rom.py, source blob 87deee49ebaf2800c8db7bdedff06ecfd506ca3c
- USA negative-control dispatch notes: practice/dialogue_layout.py, source blob f0006770cbdfe385e035fb5ae5cdbcc9109854ec
- Japan: practice/dialogue_japan.py, source blob ae7c10475810ea0b08c1433c703f6a0734e48146
- Japan font-order kana: practice/dialogue_kana_table.py, source blob 0c7a4eec37cc44e0f889c9670946f34590c208af

The read-only Python module decomp/text_tokens.py vendors ONLY glyph/control
tables and adds a lossless diagnostic decoder/encoder. It does not import the
toolkit branch and does not include extracted game dialogue or font assets.

At this source revision Japan has 242 canonical screenshot-backed glyph IDs
and one distinct screenshot-backed alternate (11 displays the same visual
exclamation mark as canonical 212), for 243 screenshot-backed token IDs.
There are 326 editable glyph IDs after adding inferred kana positions;
84 kana positions lack individual screenshot confirmation. Japan token 13
means space, and unknown/unconfirmed source tokens retain numeric tags.
The 5,039-record Japanese static index has no as-yet-unidentified positive
tokens; that does NOT prove complete coverage of all in-game renderer IDs
or dynamic strings. The predicted glyph 183 is not source-observed and is
not promoted as a confirmed mapping. USA shares neither the numeric glyph
IDs nor the font ordering; its table is derived from its own original atlas.

The diagnostic rendering is lossless: alternate token 11 remains
<token:11> except in display-only mode. Multiple USA glyph IDs with the
same Unicode representation also remain numeric in the reversible view.
Negative signed control values preserve their original ordering and bytes.
Only six commonly documented control tags are expanded in the lossless
text view; other negatives remain numeric. USA-specific dispatch notes
from the original DF98 trace are also preserved as research metadata. Do not apply USA control
semantics to Japan without verifying original MIPS dispatch.

## Offline indexing from authentic expanded ROMs

Use a local original DECOMPRESSED 32 MiB image, not the 16 MiB retail ROM.
The command verifies the full image size, big-endian N64 header and SHA-1.
It reads the region-specific file and virtual-resource tables, searches
aligned big-endian 0x00008010 script commands, resolves the same-resource
text operand, decodes signed halfwords up to the -1 sentinel and records
every direct script-command offset referencing that record.

    python3 -m decomp.story_dialogue --region usa --rom /path/to/usa.decompressed.z64
    python3 -m decomp.story_dialogue --region japan_0 --rom /path/to/japan.decompressed.z64
    python3 -m decomp.story_dialogue --region japan_0 --rom /path/to/japan.decompressed.z64 --query う〜ん！

Independent original-image extraction in this session (both SHA-1s authenticated)
reproduced **USA 5,186 indexed records / 6,006 direct 0x8010 references**
and **Japan-0 5,039 records / 5,694 references**. These were produced
with a separate standalone scanner following the same source-table rules;
the exact PR module and its tests were not executed in that environment.
Optional original-ROM regressions are enabled by GOEMON_USA_DECOMPRESSED
and GOEMON_JAPAN_DECOMPRESSED environment paths. The checked-in suite
otherwise uses synthetic resource bytes and does not require a ROM.

The result is a bounded JSON summary by default. A query includes a short
display-only preview for each match; it never commits or persists extracted
dialogue. Anchors identify region, resource ID, relative text offset,
decompressed file offset, signed-token SHA-256 fingerprint, and all direct
0x8010 command offsets. Relative offsets are NOT direct locations in the
compressed retail image. They are not original C-function addresses.

An example previously established independently in the original Japan-0
resource 97 is text offset 0x2B60, source token 11 in a hesitation line,
and a direct 0x8010 reference at resource offset 0x73FC. The toolkit
investigation docs/JAPAN_TOKEN_11_INVESTIGATION_20261120.md on main
contains the original alignment evidence. This reference proves an
indexed script command and matching text bytes; not that the story path
has reached the record in a particular playthrough.

## Correlate a traced function with story position

For an authentic ORIGINAL USA game runtime snapshot, collect in the SAME FRAME:

- resource_id: active original script resource ID from 0x801C78E8
- loaded_base: resolved current resource base from 0x801C77FC
- text_cursor: separate signed-halfword stream cursor from 0x801C77E8
- program_counter (optional): 32-bit script command PC from 0x80077858

The above addresses are original USA guest RAM, not host pointers.
Japanese guest globals and recomp addresses must be validated separately,
rather than guessed by the saved-data +0x57F0 translation rule.

Save a local JSON object containing these fields, for example:

    {
      "resource_id": 97,
      "loaded_base": "0x80300000",
      "text_cursor": "0x80302B64",
      "program_counter": "0x80307404"
    }

This is a FORMAT example with illustrative runtime addresses, NOT a capture
from an actual game. Run:

    python3 -m decomp.story_dialogue --region japan_0 --rom /path/to/japan.decompressed.z64 --snapshot /path/to/local-same-frame.json

The resolver masks the loaded-resource base exactly as the investigated
resolver does (bit 30 cleared), translates the live halfword cursor into
the original resource-relative text offset, and checks which indexed
record contains that cursor. If the script PC equals a referenced
0x8010 command offset + 8 (the next instruction after opcode and operand),
it reports the stronger command-PC association. Otherwise it reports
cursor-in-static-record only. Neither category verifies RAM bytes.
A later PC may have advanced past the text command while the text cursor
continues to advance. Null/misaligned/out-of-resource cursors do not match.

For FUNCTION execution research, record a timestamped MIPS PC or breakpoint
hit at the function original VMA, then capture the same-frame resource,
script PC, and text cursor. The resulting anchor identifies a concrete
script/story location co-observed at execution. A call-stack/caller trace
or an 0x800B callback trace is still required to establish that the
function caused or belonged to that text event. Static coincidence,
loaded scene, and a single VM resource ID cannot prove reachability,
cause or a unique chronological chapter.

## Proof limits and workflow

This index is source-identical in approach to the toolkit static text index;
it is NOT a full script CFG, a dynamic text monitor or an exhaustive index
of indirect references, choice text and generated RAM strings. It can
contain false positives from opcode-looking data, even with alignment
and resource bounds checks. Signed negative controls may alter the cursor
or VM state before the -1 terminator. Record keys and fingerprints are
not a replacement for original script control-flow proof.

Do not import full dialogue corpora, images, ROMs, patched ROMs, extracted
assets, object files or local runtime memory dumps into Git. Only code,
mapping constants, provenance and synthetic unit tests belong here.

Checks: python3 -m unittest decomp.test_story_dialogue, and then full
python3 -m decomp.local_ci in a complete checkout. This is ROM-FREE
tooling and does not change accepted matching-C counts, production
manifests, canonical G2 or inventory. The existing USA/JP ROM acceptance
gates stay independent.
