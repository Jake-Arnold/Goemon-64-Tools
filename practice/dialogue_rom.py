"""Offline, USA-only dialogue index and conservative in-place ROM text edits.

Only a SHA-1-pinned 32 MiB *decompressed* USA image is accepted as input.
No emulator connection, ROM decompressor or third-party dependencies are used.
A record is a statically referenced candidate, not proven reachable gameplay.
"""
from __future__ import annotations

from dataclasses import dataclass
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import tempfile

USA_DECOMPRESSED_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
ROM_SIZE = 32 * 1024 * 1024
RESOURCE_TABLE = 0x57FD8
VIRTUAL_TABLE = 0x556CC
RESOURCE_COUNT = 1311
MAX_TOKENS = 4096
# Bound relocated text growth so scripts cannot consume unbounded VM memory.
MAX_RESOURCE_GROWTH = 0x4000
# 1312 real file-table entries (the last is an empty file), then a zero terminator.
FILE_TABLE_ENTRIES = 1312
ORIGINAL_LAST_FILE_END = 0x14D05C0
TEXT_COMMAND = b'\x00\x00\x80\x10'

# Glyph IDs recovered from the original USA font atlas. Other IDs must remain
# numeric rather than being silently converted with ASCII assumptions.
GLYPHS = {n: chr(n + 32) for n in (
    0, 1, 7, 12, 13, 14, 15, 26, 27, 29, 31,
    *range(16, 26), *range(33, 59), *range(65, 91),
)}
GLYPHS.update({59: '[', 60: ',', 61: ']', 62: '"', 64: '.'})
CONTROLS = {
    -71: '<close-window>', -70: '<open-window>', -63: '<clear-glyphs>',
    -62: '<state-4>', -61: '<state-3>', -60: '\n',
}
GLYPH_TO_TOKEN = {value: key for key, value in GLYPHS.items()}
CONTROL_TO_TOKEN = {value: key for key, value in CONTROLS.items() if value != '\n'}
TAG_PATTERN = re.compile(r'<token:([+-]?\d+)>|<(close-window|open-window|clear-glyphs|state-4|state-3)>')


@dataclass(frozen=True)
class DialogueRecord:
    resource_id: int
    text_offset: int
    image_offset: int
    tokens: tuple[int, ...]
    references: tuple[int, ...]

    @property
    def text(self) -> str:
        return decode_tokens(self.tokens)

    @property
    def key(self) -> str:
        return f'{self.resource_id}:{self.text_offset:#x}'

    def as_dict(self) -> dict:
        return {
            'resource_id': self.resource_id,
            'text_offset': f'0x{self.text_offset:X}',
            'decompressed_image_offset': f'0x{self.image_offset:X}',
            'references': [f'0x{r:X}' for r in self.references],
            'token_count': len(self.tokens),
            'text': self.text,
            'classification': 'static_same_resource_reference',
        }


def decode_tokens(tokens: tuple[int, ...]) -> str:
    return ''.join(GLYPHS.get(t, CONTROLS.get(t, f'<token:{t}>')) for t in tokens)


def encode_text(text: str) -> tuple[int, ...]:
    """Round-trip human-readable known glyphs, explicit token tags, controls.

    Unknown glyphs and arbitrary markup are rejected, never guessed. The
    diagnostic <token:N> form can preserve original unknown values exactly.
    """
    result: list[int] = []
    i = 0
    while i < len(text):
        char = text[i]
        if char == '<':
            tag = TAG_PATTERN.match(text, i)
            if tag is None:
                raise ValueError(f'Unrecognised token at character {i}; use <token:N>')
            if tag.group(1) is not None:
                value = int(tag.group(1))
                if not -32768 <= value <= 32767 or value == -1:
                    raise ValueError(f'Invalid text token {value}')
                result.append(value)
            else:
                result.append(CONTROL_TO_TOKEN[f'<{tag.group(2)}>'])
            i = tag.end()
        elif char == '\n':
            result.append(-60)
            i += 1
        elif char in GLYPH_TO_TOKEN:
            result.append(GLYPH_TO_TOKEN[char])
            i += 1
        else:
            raise ValueError(f'Unmapped USA glyph {char!r} at character {i}')
    return tuple(result)


def load_usa_image(path: str | Path) -> bytes:
    image = Path(path).read_bytes()
    if len(image) != ROM_SIZE or hashlib.sha1(image).hexdigest() != USA_DECOMPRESSED_SHA1:
        raise ValueError('Expected unmodified USA decompressed 32 MiB ROM (SHA-1 pinned)')
    return image


def _resource(image: bytes, resource_id: int) -> tuple[int, int, memoryview] | None:
    if not 1 <= resource_id <= RESOURCE_COUNT:
        raise ValueError('Resource ID out of range')
    row = resource_id - 1
    source = RESOURCE_TABLE + 4 * row
    virtual = VIRTUAL_TABLE + 8 * row
    start, end = struct.unpack_from('>II', image, source)
    vstart, vend = struct.unpack_from('>II', image, virtual)
    if start == end or vstart == vend:
        return None
    if not (0 < start < end <= len(image) and vend > vstart and end - start == vend - vstart):
        return None
    return start, vstart, memoryview(image)[start:end]


def _read_record(buf: memoryview, offset: int) -> tuple[int, ...] | None:
    if offset < 0 or offset % 2 or offset + 2 > len(buf):
        return None
    end = min(len(buf), offset + MAX_TOKENS * 2)
    tokens = []
    for pos in range(offset, end - 1, 2):
        token = struct.unpack_from('>h', buf, pos)[0]
        if token == -1:
            return tuple(tokens)
        tokens.append(token)
    return None


def extract_dialogue(image: bytes, *, min_glyphs: int = 2) -> list[DialogueRecord]:
    """Index all aligned, in-resource text opcodes; group references by record.

    A script might have unusual alignment or dynamically built text; results
    are candidates, not an exhaustive control-flow or reachability proof.
    """
    if not 0 <= min_glyphs <= MAX_TOKENS:
        raise ValueError('Invalid minimum glyph count')
    if len(image) != ROM_SIZE:
        raise ValueError('Expected 32 MiB decompressed image')
    results: list[DialogueRecord] = []
    for resource_id in range(1, RESOURCE_COUNT + 1):
        item = _resource(image, resource_id)
        if item is None:
            continue
        start, virtual, buf = item
        raw = buf.tobytes()
        grouped: dict[int, list[int]] = {}
        search_from = 0
        while True:
            pos = raw.find(TEXT_COMMAND, search_from)
            if pos < 0:
                break
            search_from = pos + 1
            if pos % 4 or pos + 8 > len(buf):
                continue
            operand = struct.unpack_from('>I', buf, pos + 4)[0]
            offset = operand - virtual
            if operand >= 0x80000000 or offset < 0 or offset % 2 or offset + 2 > len(buf):
                continue
            grouped.setdefault(offset, []).append(pos)
        for offset, refs in grouped.items():
            tokens = _read_record(buf, offset)
            if tokens is None or sum(t >= 0 for t in tokens) < min_glyphs:
                continue
            results.append(DialogueRecord(resource_id, offset, start + offset,
                                          tokens, tuple(sorted(set(refs)))))
    return sorted(results, key=lambda r: (r.resource_id, r.text_offset))


def validate_replacement(original: DialogueRecord, replacement: str) -> tuple[int, ...]:
    proposed = encode_text(replacement)
    old = original.tokens
    if len(proposed) != len(old):
        raise ValueError(f'Token count changed ({len(old)} -> {len(proposed)}); in-place edits must retain length')
    proposed = list(proposed)
    for i, (before, after) in enumerate(zip(old, proposed)):
        # Some USA glyph IDs share the same display character. Keep the
        # exact original ID when the visible character at this slot is
        # unchanged, otherwise a no-op edit could alter original bytes.
        if before >= 0 and GLYPHS.get(before) == GLYPHS.get(after):
            proposed[i] = before
        if before < 0 and before != after:
            raise ValueError(f'Control token at index {i} cannot be changed')
        if before >= 0 and after < 0:
            raise ValueError(f'Cannot insert control token at index {i}')
    return tuple(proposed)


def validate_flexible_replacement(original: DialogueRecord, replacement: str) -> tuple[int, ...]:
    """Allow any glyph count, preserving the exact ordered negative controls.

    The controls include unknown formatting IDs: moving them may change visual
    formatting, but removing/replacing/adding one is prohibited. No separate
    glyph-width/page-layout guarantee is inferred from a token-count check.
    """
    proposed = list(encode_text(replacement))
    old = original.tokens
    if len(proposed) > MAX_TOKENS - 1:
        raise ValueError('Replacement exceeds maximum text record length')
    old_controls = tuple(t for t in old if t < 0)
    new_controls = tuple(t for t in proposed if t < 0)
    if old_controls != new_controls:
        raise ValueError('Control tokens must retain their exact order and values')
    if len(old) == len(proposed):
        # Preserve the original choice of character ID for visually identical
        # glyphs when no position moved. This makes an unchanged edit a no-op.
        for i, (before, after) in enumerate(zip(old, proposed)):
            if before >= 0 and after >= 0 and GLYPHS.get(before) == GLYPHS.get(after):
                proposed[i] = before
    return tuple(proposed)


def _record_bytes(tokens: tuple[int, ...]) -> bytes:
    return struct.pack(f'>{len(tokens) + 1}h', *tokens, -1)


def _source_layout(image: bytes) -> None:
    """Fail closed on a changed source image/table layout."""
    if len(image) != ROM_SIZE or hashlib.sha1(image).hexdigest() != USA_DECOMPRESSED_SHA1:
        raise ValueError('Refusing to edit an unverified or already modified USA ROM')
    if struct.unpack_from('>I', image, RESOURCE_TABLE)[0] != 0x576E00:
        raise ValueError('Unexpected USA resource table layout')
    if struct.unpack_from('>I', image, RESOURCE_TABLE + 4 * (FILE_TABLE_ENTRIES - 1))[0] != ORIGINAL_LAST_FILE_END:
        raise ValueError('Unexpected final resource end')
    if struct.unpack_from('>I', image, RESOURCE_TABLE + 4 * FILE_TABLE_ENTRIES)[0] != 0:
        raise ValueError('Expected the file table terminator')


def patch_image(image: bytes, records: list[DialogueRecord], replacements: dict[str, str]) -> bytes:
    """Patch original-USA text in-place or relocate longer/shorter records.

    Relocations append a new text record to its own resource, patch all
    discovered same-resource 0x8010 operands, increase that resource's virtual
    length, and shift following file-table offsets. Original records stay
    intact for untraced references. Input and output are 32 MiB decompressed
    images; retail repacking is a separate independently verified operation.
    """
    _source_layout(image)
    indexed = {r.key: r for r in records}
    if len(indexed) != len(records):
        raise ValueError('Duplicate dialogue record keys')
    if not replacements:
        raise ValueError('No edits provided')

    by_resource: dict[int, list[tuple[DialogueRecord, tuple[int, ...]]]] = {}
    for key, replacement in replacements.items():
        record = indexed.get(key)
        if record is None:
            raise ValueError(f'Unknown record {key}')
        item = _resource(image, record.resource_id)
        if item is None:
            raise ValueError(f'Resource disappeared for {key}')
        start, virtual, raw = item
        if (record.image_offset != start + record.text_offset or
                _read_record(raw, record.text_offset) != record.tokens):
            raise ValueError(f'Stale or corrupted index entry {key}')
        if virtual != 0x08000000:
            raise ValueError(f'Unsupported resource segment for {key}')
        proposed = validate_flexible_replacement(record, replacement)
        if proposed != record.tokens:
            by_resource.setdefault(record.resource_id, []).append((record, proposed))

    if not by_resource:
        return image

    # Construct each changed resource from the pinned original; offsets in a
    # resource remain fixed until its original end, and appended text offsets
    # are relative to its original virtual base.
    staged: dict[int, tuple[bytes, int]] = {}
    for rid, edits in sorted(by_resource.items()):
        start, virtual, old_buf = _resource(image, rid)
        block = bytearray(old_buf)
        original_length = len(block)
        old_virtual_end = struct.unpack_from('>I', image, VIRTUAL_TABLE + 8 * (rid - 1) + 4)[0]
        if original_length % 4 or old_virtual_end != virtual + original_length:
            raise ValueError(f'Unsupported unaligned/bad virtual resource {rid}')
        references_written: set[int] = set()
        inplace_ranges: list[tuple[int, int]] = []
        appended = bytearray()

        for record, proposed in sorted(edits, key=lambda p: p[0].text_offset):
            if len(proposed) == len(record.tokens) and all(
                (a < 0) == (b < 0) for a, b in zip(record.tokens, proposed)
            ):
                # Same-size replacement doesn't move negative controls and
                # cannot change another record or script's data.
                lo = record.text_offset
                hi = lo + len(record.tokens) * 2
                if lo < 2 or start + lo < 0x101000:
                    raise ValueError('Refusing checksum-region or header edit')
                inplace_ranges.append((lo, hi))
                block[lo:hi] = struct.pack(f'>{len(proposed)}h', *proposed)
                continue

            if not record.references:
                raise ValueError(f'No verified same-resource text references for {record.key}')
            # Every referenced command must occur beyond the known dialogue
            # data region, protecting text records from scan false positives.
            text_data_end = max(
                r.text_offset + (len(r.tokens) + 1) * 2
                for r in records if r.resource_id == rid
            )
            offset = original_length + len(appended)
            if offset % 4:
                raise ValueError('New text offset is not word-aligned')
            operand = virtual + offset
            if operand >= 0x09000000:
                raise ValueError('Text relocation exceeded resource segment')
            for command_offset in record.references:
                if (command_offset < text_data_end or command_offset % 4 or
                        command_offset + 8 > original_length):
                    raise ValueError(f'Unverified or overlapping text command at {command_offset:#x}')
                if command_offset in references_written:
                    raise ValueError('Multiple records share one text-command address')
                if struct.unpack_from('>II', block, command_offset) != (
                    0x8010, virtual + record.text_offset
                ):
                    raise ValueError(f'Stale text-command reference at {command_offset:#x}')
                references_written.add(command_offset)
                struct.pack_into('>I', block, command_offset + 4, operand)
            appended.extend(_record_bytes(proposed))
            while len(appended) % 4:
                appended.append(0)

        for i, (lo, hi) in enumerate(sorted(inplace_ranges)):
            if i and lo < sorted(inplace_ranges)[i-1][1]:
                raise ValueError('Overlapping in-place edits')
            if any(lo < ref + 8 and hi > ref for ref in references_written):
                raise ValueError('Text edit overlaps a relocated script reference')
        while len(appended) % 16:
            appended.append(0)
        if len(appended) > MAX_RESOURCE_GROWTH:
            raise ValueError(f'Expanded resource {rid} exceeds {MAX_RESOURCE_GROWTH} byte budget')
        staged[rid] = (bytes(block + appended), len(appended))

    total_growth = sum(growth for _, growth in staged.values())
    if (ORIGINAL_LAST_FILE_END + total_growth > ROM_SIZE or
            image[ROM_SIZE - total_growth:] != b'\0' * total_growth):
        raise ValueError('Not enough verifiable trailing padding for appended text')

    result = bytearray(image)
    shifted = 0
    for rid in sorted(staged):
        block, growth = staged[rid]
        start, _, original = _resource(image, rid)
        current_start = start + shifted
        current_end = current_start + len(original)
        result[current_start:current_end] = block
        if growth:
            # Only file starts AFTER the edited resource shift. The last
            # real entry is a zero-size file, and the terminator stays zero.
            for index in range(rid, FILE_TABLE_ENTRIES):
                off = RESOURCE_TABLE + 4 * index
                value = struct.unpack_from('>I', result, off)[0]
                if not (0 < value < ROM_SIZE):
                    raise ValueError('Corrupt original resource file table')
                struct.pack_into('>I', result, off, value + growth)
            end_word = VIRTUAL_TABLE + 8 * (rid - 1) + 4
            virtual_end = struct.unpack_from('>I', result, end_word)[0]
            struct.pack_into('>I', result, end_word, virtual_end + growth)
            shifted += growth

    del result[ROM_SIZE:]
    if len(result) != ROM_SIZE:
        raise ValueError('Patched image did not retain 32 MiB decompressed size')
    return bytes(result)


def save_patched_image(source: str | Path, destination: str | Path,
                       records: list[DialogueRecord], replacements: dict[str, str]) -> str:
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError('Output path must differ from the original ROM')
    patched = patch_image(load_usa_image(source), records, replacements)
    # Expanding a resource changes the file table inside the N64 checksum
    # window. Recalculate CIC-6102 header CRCs for an emulator-ready image.
    if struct.unpack_from('>I', patched, RESOURCE_TABLE + 4 * (FILE_TABLE_ENTRIES-1))[0] != ORIGINAL_LAST_FILE_END:
        from practice.dialogue_repack import _update_usa_crc
        rebuilt_header = bytearray(patched)
        _update_usa_crc(rebuilt_header)
        patched = bytes(rebuilt_header)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.goemon-dialogue-', suffix='.z64',
                                         dir=destination.parent, delete=False) as out:
            temp_name = out.name
            out.write(patched)
        os.replace(temp_name, destination)
    finally:
        if temp_name is not None and os.path.exists(temp_name):
            os.unlink(temp_name)
    return hashlib.sha1(patched).hexdigest()


def export_index(records: list[DialogueRecord], destination: str | Path) -> None:
    destination = Path(destination)
    if destination.suffix.lower() == '.json':
        destination.write_text(json.dumps({
            'format': 'goemon-usa-dialogue-candidates-v1',
            'input_sha1': USA_DECOMPRESSED_SHA1,
            'completeness': 'aligned same-resource opcode references only; not full script reachability',
            'records': [r.as_dict() for r in records],
        }, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    elif destination.suffix.lower() == '.csv':
        with destination.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=(
                'resource_id', 'text_offset', 'decompressed_image_offset',
                'references', 'token_count', 'text', 'classification'))
            writer.writeheader()
            for record in records:
                row = record.as_dict()
                row['references'] = ', '.join(row['references'])
                writer.writerow(row)
    else:
        raise ValueError('Export index as .json or .csv')
