"""Pinned Japan-0 dialogue token extractor and conservative ROM patch/repack.

Japanese glyph IDs are not ASCII or Shift-JIS. Decode only characters whose
token identity has been cross-checked against an original-ROM text record
and a matching gameplay screenshot. Preserve all other glyphs as <token:N>.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import tempfile

from practice.dialogue_rom import (ROM_SIZE, MAX_TOKENS, RESOURCE_COUNT,
    TEXT_COMMAND, _read_record,
    DialogueRecord, CONTROLS, CONTROL_TO_TOKEN)

JP_DECOMPRESSED_SHA1 = '6f8745fecc3a5e7d4918c7a73353eb0726116ded'
JP_RETAIL_SHA1 = '9843ee979b5f6c80f5eda85df0baed9ae7c4e73b'
JP_SWAPPED_SHA1 = 'b6386455c0b8f573e315976bbb47548cbafcedb3'
RETAIL_SIZE = 16 * 1024 * 1024
MAX_RESOURCE_GROWTH = 0x4000
FILE_TABLE_ENTRIES = 1312
RESOURCE_TABLE = 0x58258
VIRTUAL_TABLE = 0x5594C
FIRST_FILE_OFFSET = 0x57C5F0
ORIGINAL_LAST_FILE_END = 0x14B3C40
MAX_JP_GLYPH = 395  # Highest found in original resource references; not a full font atlas proof.
TOKEN_RE = re.compile(r'<token:([+-]?\d+)>|<(close-window|open-window|clear-glyphs|state-4|state-3)>')

# Confirmed against the *original* Japanese decompressed ROM resource 82 and
# the user's matching in-game screenshot of the Kai Highway location banner:
#   +0x04: 13,13,292,-33,99,95,-32,293,-60 -> 【カイ】 + newline
#   +0x18: 13,13,13,13,13,19,15,78,16 -> かいどう
# -33/-32 are title formatting control tokens (orange / reset), NOT glyphs.
# 13 is the separately established Japanese spacing/indent glyph.
# The user's second in-game screenshot (Plasma fortune teller) matches
# resource 112+0x0C (and +0x1E4) in the exact original Japan-0 ROM:
#   166,13,132,13,151,13,124,13,89,13,212,13,212
#     プ      ラ      ズ      マ      ぁ      ！      ！
# The 13 separators are spacing glyphs; -56/-50/-51/-57 are controls.
# The above Plasma callout alone establishes no additional character IDs.
# Further confirmed IDs below come from separately aligned gameplay screenshots.
JP_CONFIRMED_GLYPHS = {
    292: '【', 293: '】', 99: 'カ', 95: 'イ',
    19: 'か', 15: 'い', 78: 'ど', 16: 'う',
    166: 'プ', 132: 'ラ', 151: 'ズ', 124: 'マ', 89: 'ぁ', 212: '！',
    # Screen-verified Plasma fortune-teller sequence, resource 112.
    # Screenshot line matching is recorded in docs/JAPAN_PLASMA_SCREENSHOT_ALIGNMENT_20261119.md.
    # These are character tokens, NOT script controls: preserve all negative IDs.
    75: 'ぢ', 295: '「', 85: 'ぴ', 63: 'ょ', 303: '〜',
    296: '、', 70: 'じ', 61: 'ゃ', 297: '」',
    177: '１', 176: '０', 236: '両', 77: 'で',
    64: 'が', 232: '・', 60: 'っ', 72: 'ぜ', 86: 'ぷ',
    291: '大', 273: '江', 274: '戸', 275: '城',
    258: '（', 259: '）', 304: '入', 79: 'ば',
    341: '屋', 74: 'だ', 334: '出', 305: '口', 278: '山',
    # Thirteen additional user gameplay screenshots: Oedo/Hagure title and
    # Oedo NPC speech, pinned Japan-0 resources 93 and 96.
    # Each ID was aligned by character position across 29 original 16-bit
    # records (including the entire text segment, not just a fuzzy substring).
    # Provenance: docs/JAPAN_OEDO_THIRTEEN_SCREEN_ALIGNMENT_20261119.md
    14: 'あ', 21: 'く', 22: 'け', 23: 'こ', 25: 'し', 28: 'そ',
    29: 'た', 30: 'ち', 31: 'つ', 32: 'て', 33: 'と', 34: 'な',
    35: 'に', 37: 'ね', 38: 'の', 39: 'は', 41: 'ふ', 42: 'へ',
    44: 'ま', 45: 'み', 48: 'も', 49: 'や', 51: 'よ', 52: 'ら',
    53: 'り', 54: 'る', 55: 'れ', 56: 'ろ', 57: 'わ', 58: 'を',
    59: 'ん', 66: 'ぐ', 83: 'ぼ', 91: 'ぅ', 93: 'ぉ', 103: 'コ',
    105: 'シ', 106: 'ス', 108: 'ソ', 109: 'タ', 110: 'チ', 116: 'ヌ',
    119: 'ハ', 127: 'メ', 133: 'リ', 137: 'ワ', 139: 'ン', 140: 'ッ',
    141: 'ャ', 146: 'グ', 158: 'ド', 164: 'パ', 165: 'ピ', 175: 'ー',
    191: 'F', 200: 'O', 206: 'U', 224: '？', 276: '町', 302: '行',
    318: '時', 324: '来', 337: '聞',
    # Two user Project64 screenshots with the exact sequential 186..211 payload:
    # the first proves A..U, the second shows ABCDEFG / HIJKLMN /
    # OPQRSTU / VWXYZ in four manually split lines (V..Z now legible).
    # All A..Z are verified on-screen in a modified original-Japan ROM.
    # In the Kai banner, extra lines draw below the fixed-height window.
    **{186 + index: chr(ord('A') + index) for index in range(26)},
}
JP_CONFIRMED_GLYPH_TO_TOKEN = {character: token for token, character in JP_CONFIRMED_GLYPHS.items()}


def decode_japan_tokens(tokens: tuple[int, ...]) -> str:
    return ''.join(' ' if token == 13 else
                   JP_CONFIRMED_GLYPHS.get(token, CONTROLS.get(token, f'<token:{token}>'))
                   for token in tokens)


def encode_japan_text(value: str) -> tuple[int, ...]:
    """Encode verified glyphs, JP spaces/newlines, and explicit signed token IDs."""
    out = []
    position = 0
    while position < len(value):
        ch = value[position]
        if ch == '<':
            match = TOKEN_RE.match(value, position)
            if match is None:
                raise ValueError(f'Unknown JP tag at character {position}')
            token = (int(match.group(1)) if match.group(1) is not None else
                     CONTROL_TO_TOKEN[f'<{match.group(2)}>'])
            if token == -1 or not (-32768 <= token <= MAX_JP_GLYPH):
                raise ValueError(f'Unverified JP token ID {token}')
            out.append(token)
            position = match.end()
        elif ch in JP_CONFIRMED_GLYPH_TO_TOKEN:
            out.append(JP_CONFIRMED_GLYPH_TO_TOKEN[ch])
            position += 1
        elif ch == ' ':
            out.append(13)
            position += 1
        elif ch == '\n':
            out.append(-60)
            position += 1
        else:
            raise ValueError(f'Japanese glyph {ch!r} has no verified ROM token mapping; use <token:N>')
    return tuple(out)


@dataclass(frozen=True)
class JapanDialogueRecord(DialogueRecord):
    @property
    def text(self) -> str:
        return decode_japan_tokens(self.tokens)

    def as_dict(self) -> dict:
        entry = super().as_dict()
        entry['text'] = self.text
        entry['region'] = 'japan_0'
        entry['encoding'] = 'jp_partially_verified_unicode_with_numeric_fallback'
        return entry


def load_japan_image(path: str | Path) -> bytes:
    image = Path(path).read_bytes()
    if len(image) != ROM_SIZE or hashlib.sha1(image).hexdigest() != JP_DECOMPRESSED_SHA1:
        raise ValueError('Expected the pinned original Japan-0 decompressed 32 MiB ROM')
    return image


def normalise_japan_retail(raw: bytes) -> bytes:
    if len(raw) != RETAIL_SIZE:
        raise ValueError('Expected 16 MiB Japanese retail ROM')
    if raw[:4] == b'\x37\x80\x40\x12':
        if hashlib.sha1(raw).hexdigest() != JP_SWAPPED_SHA1:
            raise ValueError('Unrecognised byte-swapped Japan-0 retail ROM')
        normalized = bytearray(RETAIL_SIZE)
        normalized[::2] = raw[1::2]
        normalized[1::2] = raw[::2]
        raw = bytes(normalized)
    if raw[:4] != b'\x80\x37\x12\x40' or hashlib.sha1(raw).hexdigest() != JP_RETAIL_SHA1:
        raise ValueError('Unrecognised original Japan-0 retail ROM; modified ROMs are not accepted as input')
    return raw


def load_japan_retail(path: str | Path) -> bytes:
    return normalise_japan_retail(Path(path).read_bytes())


def _resource(image: bytes, rid: int):
    if not 1 <= rid <= RESOURCE_COUNT:
        raise ValueError('Resource index out of range')
    row = rid - 1
    start, end = struct.unpack_from('>II', image, RESOURCE_TABLE + row * 4)
    virtual, vend = struct.unpack_from('>II', image, VIRTUAL_TABLE + row * 8)
    if start == end or virtual == vend:
        return None
    if not (0 < start < end <= ROM_SIZE and vend >= virtual and
            end - start == vend - virtual):
        return None
    return start, virtual, memoryview(image)[start:end]


def extract_japan_dialogue(image: bytes, *, min_glyphs: int = 2) -> list[JapanDialogueRecord]:
    if len(image) != ROM_SIZE or image[:4] != b'\x80\x37\x12\x40':
        raise ValueError('Expected 32 MiB big-endian Japan-0 image')
    if not 0 <= min_glyphs <= MAX_TOKENS:
        raise ValueError('Invalid minimum glyph count')
    results = []
    for rid in range(1, RESOURCE_COUNT + 1):
        entry = _resource(image, rid)
        if entry is None:
            continue
        start, virtual, buf = entry
        raw = buf.tobytes()
        grouped = {}
        pos = 0
        while True:
            pos = raw.find(TEXT_COMMAND, pos)
            if pos < 0:
                break
            nxt = pos + 1
            if pos % 4 == 0 and pos + 8 <= len(buf):
                operand = struct.unpack_from('>I', buf, pos + 4)[0]
                off = operand - virtual
                if 0 <= off < len(buf)-1 and off % 2 == 0 and operand < 0x80000000:
                    grouped.setdefault(off, []).append(pos)
            pos = nxt
        for off, refs in grouped.items():
            tokens = _read_record(buf, off)
            if tokens is not None and sum(t >= 0 for t in tokens) >= min_glyphs:
                results.append(JapanDialogueRecord(rid, off, start + off,
                                                    tokens, tuple(sorted(set(refs)))))
    return sorted(results, key=lambda r: (r.resource_id, r.text_offset))


def validate_japan_replacement(record: JapanDialogueRecord, replacement: str) -> tuple[int, ...]:
    proposed = encode_japan_text(replacement)
    if len(proposed) > MAX_TOKENS - 1:
        raise ValueError('Japanese text replacement exceeds maximum record length')
    # Enter is encoded as -60 in both regional dialogue token streams.
    # Allow explicit ADDITIONAL line breaks, but never let a replacement delete
    # original ones or reorder/strip non-newline VM controls. This is *not*
    # automatic wrapping or evidence that a window can fit more rendered lines.
    original_controls = tuple(t for t in record.tokens if t < 0 and t != -60)
    edited_controls = tuple(t for t in proposed if t < 0 and t != -60)
    if edited_controls != original_controls:
        raise ValueError('Japan-0 non-newline VM controls must retain their ordered values')
    if proposed.count(-60) < record.tokens.count(-60):
        raise ValueError('Original Japan-0 -60 line breaks cannot be removed')
    return proposed


def _source_layout(image: bytes):
    if len(image) != ROM_SIZE or hashlib.sha1(image).hexdigest() != JP_DECOMPRESSED_SHA1:
        raise ValueError('Refusing to modify any Japanese image except the verified unmodified original')
    if struct.unpack_from('>I', image, RESOURCE_TABLE)[0] != FIRST_FILE_OFFSET:
        raise ValueError('Unexpected Japanese first resource')
    if struct.unpack_from('>I', image, RESOURCE_TABLE + 4 * (FILE_TABLE_ENTRIES-1))[0] != ORIGINAL_LAST_FILE_END:
        raise ValueError('Unexpected Japanese resource end')
    if struct.unpack_from('>I', image, RESOURCE_TABLE + 4 * FILE_TABLE_ENTRIES)[0] != 0:
        raise ValueError('Unexpected Japanese file-table terminator')


def patch_japan_image(image: bytes, records: list[JapanDialogueRecord], changes: dict[str, str]) -> bytes:
    """Guarded same-resource records. Original text preserved on relocation."""
    _source_layout(image)
    by_key = {r.key: r for r in records}
    if len(by_key) != len(records):
        raise ValueError('Duplicate record keys')
    if not changes:
        raise ValueError('No edits staged')
    changes_by_resource = {}
    for key, value in changes.items():
        r = by_key.get(key)
        if r is None:
            raise ValueError(f'Unknown Japanese dialogue record {key}')
        entry = _resource(image, r.resource_id)
        if entry is None or entry[0] + r.text_offset != r.image_offset or _read_record(entry[2], r.text_offset) != r.tokens:
            raise ValueError('Stale record or invalid source resource')
        if entry[1] != 0x08000000:
            raise ValueError('Unsupported Japanese script segment')
        encoded = validate_japan_replacement(r, value)
        if encoded != r.tokens:
            changes_by_resource.setdefault(r.resource_id, []).append((r, encoded))
    if not changes_by_resource:
        return image
    staged = {}
    for rid, edits in sorted(changes_by_resource.items()):
        start, virtual, original = _resource(image, rid)
        block = bytearray(original)
        if len(block) % 4:
            raise ValueError('Unaligned Japanese resource extent')
        appended = bytearray()
        written = set()
        inplace = []
        text_data_end = max(r.text_offset + 2 * (len(r.tokens)+1) for r in records if r.resource_id == rid)
        for r, proposed in sorted(edits, key=lambda x:x[0].text_offset):
            if len(proposed) == len(r.tokens) and all((a < 0) == (b < 0) for a,b in zip(r.tokens, proposed)):
                lo = r.text_offset
                hi = lo + len(proposed)*2
                if lo < 2 or start + lo < 0x101000:
                    raise ValueError('Unsafe Japanese inline edit')
                inplace.append((lo, hi))
                block[lo:hi] = struct.pack(f'>{len(proposed)}h', *proposed)
            else:
                if not r.references:
                    raise ValueError('No same-resource JP text references')
                off = len(block) + len(appended)
                if off % 4 or virtual+off >= 0x09000000:
                    raise ValueError('Unaligned/out-of-bounds Japanese text relocation')
                for ref in r.references:
                    if ref in written or ref < text_data_end or ref % 4 or ref + 8 > len(block):
                        raise ValueError('Japanese text pointer lacks safe script ownership evidence')
                    if struct.unpack_from('>II', block, ref) != (0x8010, virtual + r.text_offset):
                        raise ValueError('Stale Japanese text pointer')
                    written.add(ref)
                    struct.pack_into('>I', block, ref+4, virtual+off)
                appended.extend(struct.pack(f'>{len(proposed)+1}h',*proposed,-1))
                while len(appended) % 4:
                    appended.append(0)
        sorted_inplace=sorted(inplace)
        for j, (lo,hi) in enumerate(sorted_inplace):
            if j and lo<sorted_inplace[j-1][1]:
                raise ValueError('Overlapping Japanese edits')
            if any(lo < r+8 and hi > r for r in written):
                raise ValueError('In-place record overlaps Japanese script pointer')
        while len(appended)%16:
            appended.append(0)
        if len(appended)>MAX_RESOURCE_GROWTH:
            raise ValueError('Japan resource exceeds bounded relocation budget')
        staged[rid]=(bytes(block+appended),len(appended))
    growth = sum(v for _,v in staged.values())
    if ORIGINAL_LAST_FILE_END + growth>ROM_SIZE or image[ROM_SIZE-growth:] != b'\0'*growth:
        raise ValueError('Not enough original Japanese image padding')
    out=bytearray(image)
    shift=0
    for rid,(block,extra) in sorted(staged.items()):
        start,_,original=_resource(image,rid)
        begin=start+shift
        out[begin:begin+len(original)]=block
        if extra:
            for entry_index in range(rid,FILE_TABLE_ENTRIES):
                point=RESOURCE_TABLE+entry_index*4
                value=struct.unpack_from('>I',out,point)[0]
                if not 0<value<ROM_SIZE:
                    raise ValueError('Unverified Japanese file table extent')
                struct.pack_into('>I',out,point,value+extra)
            vt=VIRTUAL_TABLE+(rid-1)*8+4
            value=struct.unpack_from('>I',out,vt)[0]
            struct.pack_into('>I',out,vt,value+extra)
            shift+=extra
    del out[ROM_SIZE:]
    if len(out)!=ROM_SIZE:
        raise ValueError('Unexpected Japanese decompressed output size')
    return bytes(out)


def _update_crc(out: bytearray):
    from practice.dialogue_repack import _update_usa_crc
    _update_usa_crc(out)  # JP/USA share the verified CIC-6102 bootcode.


def repack_japan_retail(patched: bytes, raw: bytes) -> bytes:
    """Repack using exact original Japanese compression flags."""
    retail=normalise_japan_retail(raw)
    if len(patched)!=ROM_SIZE or patched[:4]!=b'\x80\x37\x12\x40':
        raise ValueError('Invalid decompressed Japanese image')
    if patched.find(b'Nisitenma-Ichigo')!=RESOURCE_TABLE-16:
        raise ValueError('Unexpected Japanese resource-table location')
    import lzkn64
    starts=[struct.unpack_from('>I',patched,RESOURCE_TABLE+i*4)[0] for i in range(FILE_TABLE_ENTRIES+1)]
    base=[struct.unpack_from('>I',retail,RESOURCE_TABLE+i*4)[0] for i in range(FILE_TABLE_ENTRIES+1)]
    if (starts[0]!=FIRST_FILE_OFFSET or starts[-1]!=0 or
        any(not 0<s<=ROM_SIZE for s in starts[:-1]) or
        any(b<a for a,b in zip(starts[:-2],starts[1:-1])) or
        starts[-2]<ORIGINAL_LAST_FILE_END or
        base[0]&0x7fffffff!=FIRST_FILE_OFFSET or base[-1]!=0):
        raise ValueError('Invalid Japanese file-table layout')
    result=bytearray(patched[:FIRST_FILE_OFFSET])
    for i in range(FILE_TABLE_ENTRIES):
        start=starts[i]
        end=starts[i+1] if i<FILE_TABLE_ENTRIES-1 else start
        if not start<=end<=ROM_SIZE:
            raise ValueError(f'Invalid resource extent {i}')
        data=patched[start:end]
        compressed=bool(base[i]&0x80000000) and bool(data)
        if compressed:
            data=lzkn64.compress(data)
            if len(data)%2:data+=b'\0'
        offset=len(result)
        struct.pack_into('>I',result,RESOURCE_TABLE+i*4,offset|(0x80000000 if compressed else 0))
        result.extend(data)
        if len(result)>RETAIL_SIZE:
            raise ValueError('Modified Japanese resources exceed retail ROM capacity')
    struct.pack_into('>I',result,RESOURCE_TABLE+FILE_TABLE_ENTRIES*4,0)
    result.extend(b'\0'*(RETAIL_SIZE-len(result)))
    _update_crc(result)
    return bytes(result)


def _atomic_write(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    name=None
    try:
        with tempfile.NamedTemporaryFile(prefix='.goemon-jp-',suffix='.z64',dir=path.parent,delete=False) as file:
            name=file.name
            file.write(data)
        os.replace(name,path)
    finally:
        if name and os.path.exists(name):os.unlink(name)


def save_japan_patched(source, destination, records, changes) -> str:
    source,destination=Path(source),Path(destination)
    if source.resolve()==destination.resolve():
        raise ValueError('Original Japanese ROM cannot be overwritten')
    edited=patch_japan_image(load_japan_image(source),records,changes)
    out=bytearray(edited)
    _update_crc(out)
    _atomic_write(destination,bytes(out))
    return hashlib.sha1(out).hexdigest()


def save_japan_retail_rom(source, original_retail, destination, records, changes) -> str:
    source,original_retail,destination=Path(source),Path(original_retail),Path(destination)
    if destination.resolve() in (source.resolve(),original_retail.resolve()):
        raise ValueError('Refusing to overwrite original Japanese ROM')
    edited=patch_japan_image(load_japan_image(source),records,changes)
    packed=repack_japan_retail(edited,load_japan_retail(original_retail))
    _atomic_write(destination,packed)
    return hashlib.sha1(packed).hexdigest()


def export_japan_index(records, destination):
    destination=Path(destination)
    items=[r.as_dict() for r in records]
    if destination.suffix.lower()=='.json':
        document={'format':'goemon-japan-0-token-candidates-v1', 'input_sha1':JP_DECOMPRESSED_SHA1,
                  'glyph_mapping':'unresolved; numeric token IDs are not Japanese Unicode',
                  'completeness':'static aligned same-resource references only','records':items}
        destination.write_text(json.dumps(document,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    elif destination.suffix.lower()=='.csv':
        with destination.open('w',encoding='utf-8',newline='') as file:
            writer=csv.DictWriter(file,fieldnames=('resource_id','text_offset','decompressed_image_offset',
                     'references','token_count','text','classification','region','encoding'))
            writer.writeheader()
            for row in items:
                row['references']=', '.join(row['references'])
                writer.writerow(row)
    else:raise ValueError('Expected JSON or CSV index destination')
