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


def patch_image(image: bytes, records: list[DialogueRecord], replacements: dict[str, str]) -> bytes:
    """Only touches exact original character halfwords; no relocation/repacker."""
    if len(image) != ROM_SIZE or hashlib.sha1(image).hexdigest() != USA_DECOMPRESSED_SHA1:
        raise ValueError('Refusing to edit an unverified or already modified ROM')
    indexed = {r.key: r for r in records}
    if len(indexed) != len(records):
        raise ValueError('Duplicate dialogue record keys')
    if not replacements:
        raise ValueError('No edits provided')
    edits: list[tuple[int, bytes]] = []
    for key, replacement in replacements.items():
        if key not in indexed:
            raise ValueError(f'Unknown record {key}')
        record = indexed[key]
        item = _resource(image, record.resource_id)
        if item is None:
            raise ValueError(f'Resource disappeared for {key}')
        start, _, buf = item
        if record.image_offset != start + record.text_offset or _read_record(buf, record.text_offset) != record.tokens:
            raise ValueError(f'Stale or corrupted index entry {key}')
        new = validate_replacement(record, replacement)
        # All known resource data are past the IPL checksum window; refuse any
        # early write rather than silently emitting an invalid N64 header CRC.
        if record.image_offset < 0x101000:
            raise ValueError('Refusing checksum-region edit')
        payload = struct.pack(f'>{len(new)}h', *new) if new else b''
        edits.append((record.image_offset, payload))
    edits.sort()
    for (offset, data), (next_offset, _) in zip(edits, edits[1:]):
        if offset + len(data) > next_offset:
            raise ValueError('Overlapping dialogue edits are unsafe')
    patched = bytearray(image)
    for offset, payload in edits:
        patched[offset:offset + len(payload)] = payload
    return bytes(patched)


def save_patched_image(source: str | Path, destination: str | Path,
                       records: list[DialogueRecord], replacements: dict[str, str]) -> str:
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError('Output path must differ from the original ROM')
    patched = patch_image(load_usa_image(source), records, replacements)
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
