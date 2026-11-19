"""ROM-backed USA dialogue window-style evidence (not a width calibration).

Original instruction anchors, USA decompressed image:
  800038B4: pass 800627F0 to 8000B8A4; 8000B8AC installs style table.
  8000C260: style = VM word at 801C7768; record size = 36 bytes.
  8000C6A8: width/geometry fields +3E/+40/+42 from record words 2/3/4;
             +6A = (+40 * +42), text origin +54 = 7.
  8000D180: glyph drawing entry height = 12, see glyph atlas 12 rows.
  8000C3EC: explicit -60 advances y by +76 (16).

The +3E=256 record value is a texture stride and must NOT be presented as
an independently verified textbox-width limit. Line capacity is derived
from the 40/56/72-unit backgrounds with 7-unit glyph origin and 12-pixel
font height, before any animated scaling or custom layouts.
"""
from __future__ import annotations

from dataclasses import dataclass
import struct

from practice.dialogue_rom import DialogueRecord, _resource

STYLE_TABLE_OFFSET = 0x633F0
STYLE_RECORD_SIZE = 36
STYLE_COUNT = 12
STYLE_SELECTOR_GLOBAL = 0x801C7768
ASSIGN_OPCODE = 0x8004
ASSIGN_IMMEDIATE = 0x8009
TEXT_OPCODE = 0x8010
SCREEN_NATIVE_GLYPH_HEIGHT = 12
WINDOW_TOP_PADDING = 7
WINDOW_LINE_STEP = 16


@dataclass(frozen=True)
class WindowStyle:
    index: int
    texture_stride: int
    column_factor: int
    row_factor: int
    background_height: int
    max_full_lines: int


def styles_from_rom(image: bytes) -> tuple[WindowStyle, ...]:
    """Read the native style table from the pinned USA decompressed image."""
    if len(image) != 32 * 1024 * 1024 or image[:4] != b'\x80\x37\x12\x40':
        raise ValueError('Expected 32 MiB big-endian decompressed USA ROM')
    styles = []
    for i in range(STYLE_COUNT):
        at = STYLE_TABLE_OFFSET + i * STYLE_RECORD_SIZE
        texture_a, palette, stride, columns, rows = struct.unpack_from('>5I', image, at)
        # These properties are uniform in the original USA table. Fail closed
        # if an unverified ROM revision or alternate layout is encountered.
        if not (0x80000000 <= texture_a < 0x81000000 and
                0x80000000 <= palette < 0x81000000 and
                stride == 256 and columns == 8 and rows in (5, 7, 9)):
            raise ValueError(f'Unrecognized original USA window style table, row {i}')
        height = columns * rows
        full_lines = max(0, 1 + (height - WINDOW_TOP_PADDING - SCREEN_NATIVE_GLYPH_HEIGHT) // WINDOW_LINE_STEP)
        styles.append(WindowStyle(i, stride, columns, rows, height, full_lines))
    return tuple(styles)


@dataclass(frozen=True)
class WindowContext:
    style: WindowStyle
    starting_line: int  # zero-based, after preceding visible linebreaks
    command_offset: int

    @property
    def remaining_lines(self) -> int:
        return max(0, self.style.max_full_lines - self.starting_line)


def _linear_chain_context(resource: memoryview, cursor: int, target: int,
                          vbase: int) -> int | None:
    """Track vertical line index only on a completely understood direct path.

    Do not treat a raw sequence containing conditional jumps, callbacks or
    unknown opcodes as validated control flow.
    """
    length = len(resource)
    if not 0 <= cursor <= target < length:
        return None
    line = 0
    while cursor < target:
        if cursor + 4 > length:
            return None
        opcode = struct.unpack_from('>I', resource, cursor)[0]
        if opcode == ASSIGN_OPCODE:
            if cursor + 16 > length or struct.unpack_from('>I', resource, cursor + 8)[0] != ASSIGN_IMMEDIATE:
                return None
            destination = struct.unpack_from('>I', resource, cursor + 4)[0]
            if destination == STYLE_SELECTOR_GLOBAL:
                return None
            cursor += 16
        elif opcode == TEXT_OPCODE:
            if cursor + 8 > length:
                return None
            operand = struct.unpack_from('>I', resource, cursor + 4)[0]
            if operand < vbase or operand >= vbase + length or (operand - vbase) % 2:
                return None
            text_offset = operand - vbase
            terminated = False
            # Keep the walker bounded and never confuse accidental 0x8010
            # patterns inside encoded text with a validated program.
            for at in range(text_offset, min(length - 1, text_offset + 8192), 2):
                token = struct.unpack_from('>h', resource, at)[0]
                if token == -1:
                    terminated = True
                    break
                if token in (-70, -63):
                    line = 0
                elif token == -60:
                    line += 1
                elif token == -71:
                    return None  # closed window, no proven next-window state
                elif token in (-61, -62) or -37 <= token <= -32 or token >= 0:
                    pass
                else:
                    return None  # opaque formatting/layout control
            if not terminated:
                return None
            cursor += 8
        else:
            return None
    return line if cursor == target else None


def window_context_for_record(image: bytes, record: DialogueRecord,
                              *, max_lookback: int = 192) -> WindowContext | None:
    """Infer a window style and current line from a locally linear VM trace.

    Requires a direct assignment to 801C7768 followed by known 8004/8010
    commands. This is source-backed evidence for those specific script words,
    not proof that the path always executes for every NPC/state.
    """
    info = _resource(image, record.resource_id)
    if info is None:
        return None
    _, vbase, block = info
    styles = styles_from_rom(image)
    found = set()
    for target in record.references:
        if target % 4 or target < 16 or target > len(block) - 8:
            continue
        begin = max(0, target - max_lookback) // 4 * 4
        for at in range(begin, target - 15, 4):
            if struct.unpack_from('>III', block, at) != (
                    ASSIGN_OPCODE, STYLE_SELECTOR_GLOBAL, ASSIGN_IMMEDIATE):
                continue
            index = struct.unpack_from('>I', block, at + 12)[0]
            if index >= len(styles):
                continue
            line = _linear_chain_context(block, at + 16, target, vbase)
            if line is not None:
                found.add((index, line, target))
    if len(found) != 1:
        return None
    index, line, target = found.pop()
    return WindowContext(styles[index], line, target)


def style_for_record(image: bytes, record: DialogueRecord,
                     *, max_lookback: int = 192) -> WindowStyle | None:
    """Convenience accessor for native style identity when statically proven."""
    context = window_context_for_record(image, record, max_lookback=max_lookback)
    return context.style if context else None
