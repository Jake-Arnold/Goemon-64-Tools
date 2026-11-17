"""Versioned USA file_12 374-function registration island acceptance contract.

The source and object fingerprints are pinned to IDO 5.3. These claims apply
only to the original USA decompressed ROM. The full-ROM and linked relocation
checks still run through decomp.verify and overlay_file12.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import re
import struct

from .probe import Elf32

STAGE_FORMAT = 'goemon-file12-registration-374-v1'
ROM_START = 0x5C9310
VMA_START = 0x8020DE40
COUNT = 374
FUNCTION_BYTES = 0x24
TOTAL_BYTES = COUNT * FUNCTION_BYTES
SOURCE_SHA256 = '046af7d8140efca107fd45b79ea7a08cd8562ad857b9dcbde9323754a6aa639a'
COMPILER_OBJECT_SHA256 = '116ca84053a49004c17c0b5ebdcc527510f0f9d36a53e7b26c0d141a13ebe4dd'
STAGED_OBJECT_SHA256 = '73e8e7207e87531a32dfb5364147c83416cbf7b6ceaeb57459e7ae419454320d'
SOURCE_NAME = 'candidates/file12_reg374.c'
GROUP_NAME = 'file12_registration_374'


def functions():
    """All named original-ROM functions, not a synthetic 13,464-byte function."""
    return tuple({
        'name': f'func_{VMA_START + index * FUNCTION_BYTES:08X}_{ROM_START + index * FUNCTION_BYTES:X}',
        'rom_offset': ROM_START + index * FUNCTION_BYTES,
        'vma': VMA_START + index * FUNCTION_BYTES,
        'size': FUNCTION_BYTES,
    } for index in range(COUNT))


def is_group(stage):
    return isinstance(stage, dict) and stage.get('format') == STAGE_FORMAT


def claims(stage):
    return functions() if is_group(stage) else (stage['function'],)


def validate_stage(stage):
    if not isinstance(stage, dict) or set(stage) != {
            'format', 'source', 'source_sha256', 'compiler_object_sha256',
            'object_sha256', 'function'}:
        raise ValueError('Invalid registration group stage fields')
    if (stage['format'] != STAGE_FORMAT or stage['source'] != SOURCE_NAME or
            stage['source_sha256'] != SOURCE_SHA256 or
            stage['compiler_object_sha256'] != COMPILER_OBJECT_SHA256 or
            stage['object_sha256'] != STAGED_OBJECT_SHA256 or
            stage['function'] != {
                'name': GROUP_NAME, 'rom_offset': ROM_START,
                'vma': VMA_START, 'size': TOTAL_BYTES}):
        raise ValueError('USA 374-registration group identity differs from pinned contract')
    return Path(SOURCE_NAME)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def validate_object(data, *, staged):
    """Require all exact symbols and three original relocation classes per wrapper."""
    elf = Elf32(data)
    if elf.kind != 1:
        raise ValueError('Registration input is not a relocatable ELF')
    text_sections = [i for i, name in enumerate(elf.names) if name == '.text']
    if len(text_sections) != 1:
        raise ValueError('Registration object lacks a unique .text section')
    index = text_sections[0]
    section = elf.sections[index]
    length, alignment = (TOTAL_BYTES, 4) if staged else (TOTAL_BYTES + 8, 16)
    if (section[5], section[8], section[2] & 0x6) != (length, alignment, 0x6):
        raise ValueError('Registration object .text extent/alignment differs')
    actual = [symbol for symbol in elf.symbols if symbol.kind == 2 and symbol.size > 0
              and symbol.section == index]
    expected = functions()
    if len(actual) != COUNT:
        raise ValueError('Incorrect number of positive-size registration symbols')
    for offset, (symbol, definition) in enumerate(zip(actual, expected)):
        if (symbol.name, symbol.value, symbol.size, symbol.binding) != (
                definition['name'], offset * FUNCTION_BYTES, FUNCTION_BYTES, 1):
            raise ValueError(f'Registration function ELF identity differs at {offset}')
    relocs = elf.relocations(index)
    if len(relocs) != COUNT * 3:
        raise ValueError('Registration object must have exactly 1122 relocations')
    by_offset = {}
    for reloc in relocs:
        if reloc.offset < 0 or reloc.offset >= TOTAL_BYTES:
            raise ValueError('Registration relocation is outside verified functions')
        by_offset.setdefault(reloc.offset // FUNCTION_BYTES, []).append(reloc)
    for i in range(COUNT):
        items = by_offset.get(i, [])
        relative = sorted((r.offset - i * FUNCTION_BYTES, r.relocation_type, r.symbol.name)
                          for r in items)
        if (len(relative) != 3 or
                [(a, b) for a, b, _ in relative] != [(8, 5), (12, 4), (16, 6)] or
                relative[1][2] != 'func_80013AC4_146C4' or
                relative[0][2] != relative[2][2] or
                re.fullmatch(r'D_[0-9A-F]{8}_[0-9A-F]+', relative[0][2]) is None):
            raise ValueError(f'Registration relocations differ for wrapper {i}')
    if not staged and any(elf.payload(index)[TOTAL_BYTES:]):
        raise ValueError('Refusing to remove nonzero registration code')
    return dict(functions=COUNT, bytes=TOTAL_BYTES, relocations=len(relocs),
                section_alignment=alignment)


def pack(data):
    """Trim only zero IDO pad and lower input ELF .text alignment 16 -> 4."""
    if _sha(data) != COMPILER_OBJECT_SHA256:
        raise ValueError('Registration compiler object SHA-256 differs')
    before = validate_object(data, staged=False)
    result = bytearray(data)
    elf = Elf32(data)
    index = elf.names.index('.text')
    section_table = struct.unpack_from('>I', result, 32)[0]
    header = section_table + index * 40
    struct.pack_into('>I', result, header + 20, TOTAL_BYTES)
    struct.pack_into('>I', result, header + 32, 4)
    output = bytes(result)
    if _sha(output) != STAGED_OBJECT_SHA256:
        raise ValueError('Registration staged object SHA-256 differs')
    after = validate_object(output, staged=True)
    return output, dict(before=before, after=after,
                        compiler_object_sha256=COMPILER_OBJECT_SHA256,
                        staged_object_sha256=STAGED_OBJECT_SHA256,
                        trimmed_zero_padding_bytes=8)
