"""ROM-backed USA dialogue width analysis and guarded word wrapping.

The original renderer reads a 96-entry byte-width table at decompressed USA
0x5C710 and advances the window x field by table[token] + 1. Only the known
line-break token (-60) resets horizontal advance. All window caps here are
USER-SUPPLIED, not reconstructed window-style dimensions.
"""
from __future__ import annotations

from dataclasses import dataclass

FONT_WIDTH_OFFSET = 0x5C710
FONT_WIDTH_COUNT = 96
RENDER_ENTRY_CAPACITY = 120

# Native negative-token dispatch: -71..-32, from original USA DF98 trace.
# These descriptions intentionally don't invent semantics for opaque helpers.
CONTROL_NOTES = {
    -71: 'close-window request',
    -70: 'open-window request',
    -63: 'clear glyphs/reset layout',
    -62: 'state 4 (continuation/close handling)',
    -61: 'state 3 (continue prompt)',
    -60: 'explicit line break',
    -57: 'window helper C640 (layout effect not verified)',
    -56: 'window helpers C5E4/C60C (effect not verified)',
    -55: 'window helper C5A4 (effect not verified)',
    -54: 'window helpers C570/C568 (effect not verified)',
    -53: 'window helper C430, parameter 9 (effect not verified)',
    -52: 'window helper C430, parameter 9 (effect not verified)',
    -51: 'window helper C488 (effect not verified)',
    -50: 'window helper C454 (effect not verified)',
    -37: 'presentation selector 0',
    -36: 'presentation selector 2',
    -35: 'presentation selector 4',
    -34: 'presentation selector 6',
    -33: 'presentation selector 8',
    -32: 'presentation selector 0',
}
NOOP_TOKENS = set(range(-69, -63)) | {-59, -58} | set(range(-49, -37))
OPAQUE_LAYOUT_TOKENS = set(range(-57, -49))


@dataclass(frozen=True)
class LayoutReport:
    line_widths: tuple[int, ...]
    glyphs_since_clear_max: int
    unknown_width_tokens: tuple[int, ...]
    opaque_controls: tuple[int, ...]
    messages: tuple[str, ...]

    @property
    def longest_line(self) -> int:
        return max(self.line_widths, default=0)


def font_widths_from_rom(image: bytes) -> tuple[int, ...]:
    """Extract width bytes from a previously SHA-1-verified USA image."""
    if len(image) != 32 * 1024 * 1024 or image[:4] != b'\x80\x37\x12\x40':
        raise ValueError('Expected the original 32 MiB decompressed USA image')
    widths = tuple(image[FONT_WIDTH_OFFSET:FONT_WIDTH_OFFSET + FONT_WIDTH_COUNT])
    if len(widths) != FONT_WIDTH_COUNT or any(n > 15 for n in widths):
        raise ValueError('Unexpected USA font-width table')
    return widths


def glyph_advance(token: int, widths: tuple[int, ...]) -> int | None:
    if token < 0:
        return 0
    if token >= len(widths):
        return None
    return widths[token] + 1


def inspect_layout(tokens: tuple[int, ...], widths: tuple[int, ...], *,
                   max_width: int | None = None,
                   max_lines: int | None = None) -> LayoutReport:
    """Predict advances from glyph widths; do not claim clipping/layout semantics."""
    if max_width is not None and not 1 <= max_width <= 4096:
        raise ValueError('User width limit must be 1..4096')
    if max_lines is not None and not 1 <= max_lines <= 120:
        raise ValueError('User line limit must be 1..120')
    line_widths = [0]
    unknown = set()
    opaque = set()
    entries = 0
    max_entries = 0
    page_lines = 1
    max_page_lines = 1
    for token in tokens:
        if token >= 0:
            width = glyph_advance(token, widths)
            if width is None:
                unknown.add(token)
            else:
                line_widths[-1] += width
            entries += 1
            max_entries = max(max_entries, entries)
        elif token == -60:
            line_widths.append(0)
            page_lines += 1
            max_page_lines = max(max_page_lines, page_lines)
        elif token in (-63, -70, -71):
            entries = 0
            page_lines = 1
            if token != -71:
                line_widths.append(0)
        elif token in OPAQUE_LAYOUT_TOKENS or (token not in CONTROL_NOTES and token not in NOOP_TOKENS):
            opaque.add(token)
    messages = []
    if max_width is not None:
        exceeded = [(i + 1, w) for i, w in enumerate(line_widths) if w > max_width]
        if exceeded:
            messages.append('Width exceeds user limit: ' + ', '.join(
                f'line {line} ({width}/{max_width})' for line, width in exceeded[:5]))
    if max_lines is not None and max_page_lines > max_lines:
        messages.append(f'{max_page_lines} lines between clears exceeds user limit {max_lines}')
    if max_entries > RENDER_ENTRY_CAPACITY:
        messages.append(f'{max_entries} glyphs between clears exceeds the {RENDER_ENTRY_CAPACITY}-entry renderer pool')
    if unknown:
        messages.append('Unverified widths for token IDs: ' + ', '.join(map(str, sorted(unknown))))
    if opaque:
        messages.append('Opaque layout controls present: ' + ', '.join(map(str, sorted(opaque))))
    return LayoutReport(tuple(line_widths), max_entries, tuple(sorted(unknown)),
                        tuple(sorted(opaque)), tuple(messages))


def wrap_plain_dialogue(tokens: tuple[int, ...], widths: tuple[int, ...], *,
                        max_width: int, max_lines: int) -> tuple[int, ...]:
    """Replace overflow separator spaces with -60 in opt-in multiline text.

    Only glyphs, existing -60 and an optional final -61/-62 are accepted.
    Never split a word, move a control, or guess a target window's capacity.
    """
    if not 1 <= max_width <= 4096 or not 1 <= max_lines <= 120:
        raise ValueError('Set a positive manual width (1..4096) and line limit (1..120)')
    content = list(tokens)
    suffix = []
    if content and content[-1] in (-61, -62):
        suffix.append(content.pop())
    if any(t < 0 and t != -60 for t in content):
        raise ValueError('Auto-wrap requires plain glyph text with only -60 line breaks and an optional final state token')
    if any(t >= len(widths) for t in content if t >= 0):
        raise ValueError('Cannot auto-wrap glyphs without verified widths')
    result: list[int] = []
    lines_used = 0
    for paragraph_index, part in enumerate(_split_paragraphs(content)):
        if paragraph_index:
            result.append(-60)
        lines_used += 1
        if lines_used > max_lines:
            raise ValueError(f'Text needs more than {max_lines} lines')
        if not part:
            continue
        if part[0] == 0 or part[-1] == 0 or any(a == 0 and b == 0 for a, b in zip(part, part[1:])):
            raise ValueError('Leading, trailing or repeated spaces require manual line breaks')
        words = _split_words(part)
        advance = 0
        for word_index, word in enumerate(words):
            word_advance = sum(widths[t] + 1 for t in word)
            if word_advance > max_width:
                raise ValueError(f'Word needs {word_advance} units, over the {max_width}-unit cap')
            if word_index == 0:
                result.extend(word)
                advance = word_advance
                continue
            sep_advance = widths[0] + 1
            if advance + sep_advance + word_advance <= max_width:
                result.append(0)
                result.extend(word)
                advance += sep_advance + word_advance
            else:
                if lines_used >= max_lines:
                    raise ValueError(f'Text needs more than {max_lines} lines')
                result.append(-60)
                result.extend(word)
                advance = word_advance
                lines_used += 1
    return tuple(result + suffix)


def _split_paragraphs(tokens: list[int]) -> list[list[int]]:
    parts: list[list[int]] = [[]]
    for t in tokens:
        if t == -60:
            parts.append([])
        else:
            parts[-1].append(t)
    return parts


def _split_words(tokens: list[int]) -> list[list[int]]:
    words: list[list[int]] = [[]]
    for t in tokens:
        if t == 0:
            words.append([])
        else:
            words[-1].append(t)
    return words
