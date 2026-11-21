"""Read-only story-location anchors for original Goemon USA and Japan-0 ROMs.

A statically referenced 0x8010 text command identifies a candidate dialogue
site. A same-frame loaded resource and live text cursor can associate an
execution sample with that record. Neither observation proves that an arbitrary
function is executed: correlate function PC/call traces independently.

No ROM/asset data is included; only SHA-1 authenticated local 32 MiB
decompressed images are accepted. The original source remains unmodified.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import struct

from decomp.text_tokens import decode_tokens, token_bytes

ROM_SIZE = 32 * 1024 * 1024
RESOURCE_COUNT = 1311
MAX_TOKENS = 4096
TEXT_OPCODE = b'\x00\x00\x80\x10'
# These offsets are region-specific DECOMPRESSED 32 MiB image file offsets.
REGIONS = {
    'usa': {
        'sha1': '6ea0ed71032ce08fc2745f412d84936382197494',
        'resource_table': 0x57FD8,
        'virtual_table': 0x556CC,
    },
    'japan_0': {
        'sha1': '6f8745fecc3a5e7d4918c7a73353eb0726116ded',
        'resource_table': 0x58258,
        'virtual_table': 0x5594C,
    },
}


@dataclass(frozen=True)
class StoryAnchor:
    region: str
    resource_id: int
    resource_start: int  # decompressed-ROM image, not retail ROM
    resource_size: int
    text_offset: int     # relative to the resource
    tokens: tuple[int, ...]  # excludes original -1 terminator
    references: tuple[int, ...]  # 0x8010 command offsets relative to resource

    @property
    def decompressed_text_offset(self) -> int:
        return self.resource_start + self.text_offset

    @property
    def fingerprint(self) -> str:
        # Machine-comparable token fingerprint; no dialogue content persisted.
        return hashlib.sha256(token_bytes(self.tokens) + b'\xff\xff').hexdigest()

    @property
    def key(self) -> str:
        return f'{self.region}:{self.resource_id}:{self.text_offset:#x}'

    def summary(self, *, include_text: bool = False) -> dict:
        item = {
            'key': self.key,
            'fingerprint_sha256': self.fingerprint,
            'region': self.region,
            'resource_id': self.resource_id,
            'text_offset': f'0x{self.text_offset:X}',
            'decompressed_text_offset': f'0x{self.decompressed_text_offset:X}',
            'script_command_offsets': [f'0x{x:X}' for x in self.references],
            'token_count': len(self.tokens),
            'classification': 'static_text_command_reference_not_reachability',
        }
        if include_text:
            item['preview'] = decode_tokens(self.region, self.tokens, visual_aliases=True)[:200]
        return item


def load_verified_image(path: str | Path, region: str) -> bytes:
    if region not in REGIONS:
        raise ValueError('Unsupported ROM revision')
    image = Path(path).read_bytes()
    if (len(image) != ROM_SIZE or image[:4] != b'\x80\x37\x12\x40' or
            hashlib.sha1(image).hexdigest() != REGIONS[region]['sha1']):
        raise ValueError('Expected pinned, unmodified, 32 MiB decompressed ' + region + ' ROM')
    return image


def _read_halfwords(data: bytes, offset: int) -> tuple[int, ...] | None:
    if offset < 0 or offset % 2 or offset + 2 > len(data):
        return None
    end = min(len(data) - 1, offset + 2 * MAX_TOKENS)
    result = []
    for i in range(offset, end, 2):
        value = struct.unpack_from('>h', data, i)[0]
        if value == -1:
            return tuple(result)
        result.append(value)
    return None


def scan_resource(region: str, resource_id: int, resource_start: int,
                  virtual_base: int, data: bytes, *,
                  min_glyphs: int = 2) -> list[StoryAnchor]:
    """Scan aligned 0x8010 words and valid same-resource text operands.

    This intentionally has the original toolkit's static-index limitations:
    opcode-like data may be accidental; dynamic text and indirect references
    can be missed. Region/offset/operand validation reduces false positives.
    """
    if region not in REGIONS or not 1 <= resource_id <= RESOURCE_COUNT:
        raise ValueError('Invalid region/resource')
    if not 0 <= min_glyphs <= MAX_TOKENS:
        raise ValueError('Invalid glyph minimum')
    if not 0 <= virtual_base < 0x80000000:
        raise ValueError('Invalid script virtual base')
    raw = bytes(data)
    grouped: dict[int, set[int]] = {}
    scan_at = 0
    while True:
        pos = raw.find(TEXT_OPCODE, scan_at)
        if pos == -1:
            break
        scan_at = pos + 1
        if pos % 4 or pos + 8 > len(raw):
            continue
        operand = struct.unpack_from('>I', raw, pos + 4)[0]
        offset = operand - virtual_base
        if operand >= 0x80000000 or offset < 0 or offset % 2 or offset + 2 > len(raw):
            continue
        grouped.setdefault(offset, set()).add(pos)

    result = []
    for offset, references in sorted(grouped.items()):
        tokens = _read_halfwords(raw, offset)
        if tokens is not None and sum(token >= 0 for token in tokens) >= min_glyphs:
            result.append(StoryAnchor(region, resource_id, resource_start,
                                      len(raw), offset, tokens,
                                      tuple(sorted(references))))
    return result


def index_image(image: bytes, region: str) -> list[StoryAnchor]:
    """Index a caller-verified full image; load_verified_image enforces SHA-1."""
    if region not in REGIONS or len(image) != ROM_SIZE or image[:4] != b'\x80\x37\x12\x40':
        raise ValueError('Expected 32 MiB decompressed regional image')
    profile = REGIONS[region]
    results = []
    for rid in range(1, RESOURCE_COUNT + 1):
        row = rid - 1
        start, end = struct.unpack_from('>II', image, profile['resource_table'] + 4 * row)
        virtual, vend = struct.unpack_from('>II', image, profile['virtual_table'] + 8 * row)
        if start == end or virtual == vend:
            continue
        if not (0 < start < end <= len(image) and 0 <= virtual < vend < 0x80000000
                and end - start == vend - virtual):
            continue
        results.extend(scan_resource(region, rid, start, virtual, image[start:end]))
    return results


def _u32(value, key: str) -> int:
    if type(value) is int:
        number = value
    elif isinstance(value, str):
        number = int(value, 0)
    else:
        raise ValueError(key + ' must be integer or hexadecimal string')
    if not 0 <= number <= 0xFFFFFFFF:
        raise ValueError(key + ' outside u32 range')
    return number


def resolve_snapshot(anchors: list[StoryAnchor], snapshot: dict) -> list[dict]:
    """Correlate a SAME-FRAME original guest VM snapshot with static records.

    snapshot requires resource_id, loaded_base (0x801C77FC), text_cursor
    (0x801C77E8). Optional program_counter (0x80077858) strengthens the
    association when it equals the next command after a 0x8010 reference.
    A nearby arbitrary function address is NOT an execution or causal proof.
    """
    rid = _u32(snapshot['resource_id'], 'resource_id')
    loaded_base = _u32(snapshot['loaded_base'], 'loaded_base')
    cursor = _u32(snapshot['text_cursor'], 'text_cursor')
    pc = (_u32(snapshot['program_counter'], 'program_counter')
          if snapshot.get('program_counter') is not None else None)
    if cursor == 0 or cursor % 2 or rid < 1 or rid > RESOURCE_COUNT:
        return []
    # See original USA func_8003DDC4: clear bit 30 on the loaded data pointer.
    base = loaded_base & 0xBFFFFFFF
    result = []
    for anchor in anchors:
        if anchor.resource_id != rid:
            continue
        start = base + anchor.text_offset
        term = start + len(anchor.tokens) * 2
        if term > 0xFFFFFFFF or not start <= cursor <= term:
            continue
        index = (cursor - start) // 2
        next_token = anchor.tokens[index] if index < len(anchor.tokens) else -1
        reference_matches = [pos for pos in anchor.references if
                             pc is not None and base + pos + 8 == pc]
        item = anchor.summary()
        item.update({
            'evidence': ('cursor_inside_indexed_record_and_pc_after_0x8010'
                         if reference_matches else 'cursor_inside_indexed_record'),
            'halfword_index': index,
            'next_signed_token': next_token,
            'pc_reference_matches': [f'0x{x:X}' for x in reference_matches],
            'runtime_bytes_verified': False,
            'function_execution_proven': False,
        })
        result.append(item)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--region', required=True, choices=sorted(REGIONS))
    parser.add_argument('--rom', required=True, help='Original decompressed 32 MiB .z64')
    parser.add_argument('--query', help='Optional Unicode dialogue substring')
    parser.add_argument('--resource-id', type=int)
    parser.add_argument('--snapshot', type=Path, help='JSON same-frame VM sample')
    parser.add_argument('--limit', type=int, default=20)
    args = parser.parse_args(argv)
    if not 1 <= args.limit <= 1000:
        parser.error('--limit must be 1..1000')
    anchors = index_image(load_verified_image(args.rom, args.region), args.region)
    filtered = [a for a in anchors if args.resource_id is None or
                a.resource_id == args.resource_id]
    if args.query:
        filtered = [a for a in filtered if args.query.casefold() in
                    decode_tokens(args.region, a.tokens, visual_aliases=True).casefold()]
    output = {
        'region': args.region,
        'total_static_anchors': len(anchors),
        'selected_anchors': len(filtered),
        'records': [r.summary(include_text=bool(args.query))
                    for r in filtered[:args.limit]],
    }
    if args.snapshot:
        sample = json.loads(args.snapshot.read_text(encoding='utf-8'))
        if not isinstance(sample, dict):
            raise ValueError('Expected snapshot JSON object')
        output['snapshot_correlations'] = resolve_snapshot(
            [a for a in anchors if a.region == args.region], sample)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
