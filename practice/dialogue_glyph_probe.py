"""Create a Japanese dialogue glyph identification suite rendered by the real game.

This is deliberately NOT a synthetic font extractor. The Japanese glyph
texture atlas/layout is not yet established; these probes use the retail
ROM's own renderer to display the original numeric token IDs. Only source
hash-pinned originals are accepted. No ROM assets are embedded in source.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile

from practice.dialogue_japan import (
    JP_EDITABLE_GLYPHS, JP_NATIVE_RENDERED_ALIASES, JP_DECOMPRESSED_SHA1, JP_RETAIL_SHA1,
    extract_japan_dialogue, load_japan_image, load_japan_retail,
    save_japan_retail_rom, validate_japan_replacement,
)

PROBE_RESOURCE = 82
PROBE_OFFSET = 0x18
# Kai is a two-line banner. Additional -60s are rendered outside the fixed
# artwork as user-confirmed by the native Japanese Project64 screenshot.
COLUMNS = 7
ROWS = 4
PER_PAGE = COLUMNS * ROWS
# Legacy exclusion retained for the v1 probe format and mocked tests.
# Actual original-token discovery now excludes 11 as a proven rendered alias.
SUSPECT_NON_GLYPHS = frozenset((11,))
FORMAT = 'goemon-japan-glyph-probe-v1'


@dataclass(frozen=True)
class ProbePage:
    number: int
    ids: tuple[int, ...]
    text: str
    rows: tuple[tuple[int, ...], ...]


def unknown_token_counts(records) -> Counter:
    """Only nonnegative, as-yet-unmapped source tokens, never VM controls."""
    return Counter(
        token for record in records for token in record.tokens
        if token >= 0 and token != 13 and token not in JP_EDITABLE_GLYPHS
        and token not in JP_NATIVE_RENDERED_ALIASES
    )


def make_probe_pages(token_ids, *, columns: int = COLUMNS, rows: int = ROWS):
    """Rows of numeric glyphs separated by a real space and -60 newlines.

    Does not add decorative labels to the game's narrow text window. The
    manifest independently associates positions with exact numeric IDs.
    """
    if not 1 <= columns <= 10 or not 1 <= rows <= 4:
        raise ValueError('Probe layout outside tested limits')
    ids = tuple(token_ids)
    if not ids or len(set(ids)) != len(ids):
        raise ValueError('Probe IDs must be nonempty and unique')
    if any(type(value) is not int or not 0 <= value <= 395 for value in ids):
        raise ValueError('Probe token outside source-observed glyph range')
    pages = []
    capacity = rows * columns
    for index in range(0, len(ids), capacity):
        chunk = ids[index:index + capacity]
        lines = tuple(tuple(chunk[i:i+columns]) for i in range(0, len(chunk), columns))
        text = '\n'.join(' '.join(f'<token:{n}>' for n in line) for line in lines)
        pages.append(ProbePage(1 + len(pages), chunk, text, lines))
    return pages


def _manifest(pages, frequencies, excluded, *, rom_hashes):
    return {
        'format': FORMAT,
        'source': 'pinned original Japan-0 retail/decompressed ROM',
        'original_rom_sha1': dict(rom_hashes),
        'target_resource': PROBE_RESOURCE,
        'target_record_offset': f'0x{PROBE_OFFSET:X}',
        'emulator_instruction': (
            'Load each generated .z64 in Project64 and travel to Kai Highway. '
            'Read the glyph positions top to bottom, left to right. The '\
            'window art is fixed-height: lines 2-4 may appear below the green box.'),
        'columns_per_line': COLUMNS,
        'lines_per_page': ROWS,
        'excluded_suspect_ids': sorted(excluded),
        'pages': [
            {
                'page': p.number,
                'rom_file': f'jp-glyph-probe-{p.number:02d}-of-{len(pages):02d}.z64',
                'rows': [
                    [ {'column': j+1,'id': tid,'occurrences': frequencies[tid]}
                      for j,tid in enumerate(row)]
                    for row in p.rows
                ],
                'position_order': list(p.ids),
            } for p in pages
        ],
    }


def build_probe_suite(original_decompressed, original_retail, destination,
                      *, include_suspect: bool = False, progress=None):
    """Build safe, independently bootable retail probe ROMs and JSON index.

    Input paths are always original SHA-1-verified ROMs. The output directory
    can contain unrelated files but existing probe filenames are never
    overwritten. A temporary staging directory prevents half-built pages
    being published on encode/repack failure.
    """
    source = Path(original_decompressed)
    retail = Path(original_retail)
    output = Path(destination)
    image = load_japan_image(source)
    load_japan_retail(retail)
    records = extract_japan_dialogue(image)
    record = next((r for r in records if r.resource_id == PROBE_RESOURCE
                   and r.text_offset == PROBE_OFFSET), None)
    if record is None:
        raise ValueError('Pinned Japanese Kai Highway record missing')
    counts = unknown_token_counts(records)
    excluded = set() if include_suspect else set(counts) & SUSPECT_NON_GLYPHS
    ids = sorted(set(counts) - excluded)
    pages = make_probe_pages(ids)
    if not pages:
        raise ValueError('No unrecognised glyph IDs found')
    target_names = [f'jp-glyph-probe-{p.number:02d}-of-{len(pages):02d}.z64'
                    for p in pages] + ['jp-glyph-probe-manifest.json','jp-glyph-probe-guide.html']
    output.mkdir(parents=True, exist_ok=True)
    if (source.resolve().parent == output.resolve() or retail.resolve().parent == output.resolve()):
        # Never emit modified probe ROMs alongside a user's original image.
        raise ValueError('Choose a separate output directory away from original ROMs')
    if any((output / name).exists() for name in target_names):
        raise FileExistsError('Probe output already exists; choose another folder')
    manifest = _manifest(pages, counts, excluded,
        rom_hashes={'decompressed':JP_DECOMPRESSED_SHA1,'retail':JP_RETAIL_SHA1})
    manifest['indexed_records'] = len(records)
    manifest['unknown_ids_in_index'] = len(counts)
    manifest['emitted_probe_ids'] = len(ids)
    manifest['unknown_token_occurrences'] = sum(counts.values())
    manifest['generated_utc'] = datetime.now(timezone.utc).isoformat()
    with tempfile.TemporaryDirectory(prefix='.jp-probe-',dir=output) as temp:
        stage = Path(temp)
        for p, name in zip(pages,target_names):
            proposed = validate_japan_replacement(record,p.text)
            if tuple(t for t in proposed if t >= 0 and t != 13) != p.ids:
                raise ValueError(f'Unexpected glyph ordering on probe page {p.number}')
            sha = save_japan_retail_rom(source,retail,stage/name,records,{record.key:p.text})
            manifest['pages'][p.number-1]['rom_sha1'] = sha
            if progress:progress(p.number,len(pages))
        (stage/'jp-glyph-probe-manifest.json').write_text(
            json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (stage/'jp-glyph-probe-guide.html').write_text(
            _html_guide(manifest),encoding='utf-8')
        if any((output / name).exists() for name in target_names):
            raise FileExistsError('Probe output appeared while building')
        for name in target_names:
            os.replace(stage/name,output/name)
    return manifest


def _html_guide(manifest):
    """Pure HTML position guide; no copyrighted glyphs or external assets."""
    from html import escape
    parts = [
        '<!doctype html><html lang="en"><meta charset="utf-8">',
        '<title>Japan ROM glyph probe position guide</title>',
        '<style>body{font:16px system-ui,sans-serif;max-width:1000px;margin:2rem auto}',
        'table{border-collapse:collapse;margin-bottom:2rem;width:100%}',
        'td,th{border:1px solid #bbb;padding:.6rem;text-align:center}',
        '.num{font-weight:bold;font-size:1.2rem}small{color:#555}</style>',
        '<h1>Japan ROM glyph probe position guide</h1>',
        '<p>Load a page ROM in Project64 and enter Kai Highway. ',
        'Each cell corresponds to exactly one displayed glyph, ',
        'row-major. Source screenshots must be matched by position.</p>',
    ]
    for p in manifest['pages']:
        parts.append(f'<h2>Page {p["page"]}: {escape(p["rom_file"])}</h2><table>')
        for line_no,row in enumerate(p['rows'],1):
            parts.append(f'<tr><th>Line {line_no}</th>')
            for cell in row:
                parts.append(f'<td><div class="num">token {cell["id"]}</div>'
                             f'<small>{cell["occurrences"]} instances</small></td>')
            parts.append('</tr>')
        parts.append('</table>')
    if manifest['excluded_suspect_ids']:
        parts.append('<p>Separately excluded suspect non-glyph token IDs: '
                     + ', '.join(str(x) for x in manifest['excluded_suspect_ids']) + '.</p>')
    return '\n'.join(parts)+'</html>\n'
