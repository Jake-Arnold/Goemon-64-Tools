"""Source-backed regional read models for the SAME toolkit tabs.

Region is an explicit argument, never an implicit USA->Japan address offset.
Japan's recorded fields are rendered as candidates unless behaviour verified.
No writable guest-RAM interface is provided by this module.
"""
from __future__ import annotations

from practice.inspector import Watch
from practice.japanese_fields import JAPAN_FIELDS, read_japan_field
from practice.japanese_scene_probes import (
    JAPAN_SCENE_PROBES, read_japan_scene_probes,
)
from practice.japanese_position import JAPAN_PLAYER_XYZ, read_japan_position
from practice.custom_watches import read_watch
from practice.region_memory_crosswalk import CROSS_REGION_FIELDS, read_cross_region_field
from practice.story_progress import story_section_for_key


def japan_live_watches(rdram, custom=()):
    """Return main Live Memory rows with Japanese guest addresses and status."""
    results = []
    for field in JAPAN_FIELDS:
        observed = read_japan_field(rdram, field)
        results.append(Watch(
            f'{field.group}: {field.label}', field.address,
            observed.value, observed.raw, observed.status,
            f'Japan-0 {field.source}; {field.key}; external lead'))
    scene = read_japan_scene_probes(rdram)
    for field in JAPAN_SCENE_PROBES:
        observed = scene[field.key]
        results.append(Watch(
            f'Scene: {field.label}', field.address,
            observed.value, observed.raw, observed.status,
            f'Japan-0 {field.source}; {field.key}'))
    # Existing shared Live Memory page: add independently observed static pairs
    # where the canonical JP field/probe tables have no entry yet. Speculative
    # and disputed offsets are intentionally not turned into editable rows.
    seen_addresses = {row.addr for row in results}
    for field in CROSS_REGION_FIELDS:
        if (not field.key.startswith('static:') or
                field.evidence not in ('user-confirmed', 'observed') or
                field.japan in seen_addresses):
            continue
        reading = (read_cross_region_field(rdram, field)
                   if rdram is not None else None)
        results.append(Watch(
            field.label, field.japan,
            reading.value if reading else '—',
            reading.raw if reading else '—',
            'ERROR' if reading and reading.error else 'OBSERVED' if reading else 'DISCONNECTED',
            f'Japan-0; USA 0x{field.usa:08X}; {field.evidence}; {field.note}'))
        seen_addresses.add(field.japan)
    try:
        xyz = read_japan_position(rdram)
        for axis, address, value in zip('XYZ', JAPAN_PLAYER_XYZ, xyz):
            data = rdram.read_guest(address, 4)
            results.append(Watch(
                f'Player position {axis} (Goemon test)', address,
                f'{value:.4f}', data.hex().upper(), 'OBSERVED',
                'Japan-0; position-controlling in Goemon Oedo South; '
                'cross-scene/character ownership not proven'))
    except (OSError, RuntimeError, ValueError, PermissionError):
        pass
    for item in custom:
        observed = read_watch(rdram, item)
        results.append(Watch(
            item.row_name, item.address, observed.value, observed.raw,
            'CUSTOM' if observed.status == 'CUSTOM' else observed.status,
            f'Japan-0 typed custom watch: {item.kind}; no automatic write permission'))
    return results


def japan_unlock_fields():
    """Separate Japanese sources; never translate USA item addresses."""
    return tuple(field for field in JAPAN_FIELDS if field.group in (
        'Party', 'Weapons and skills', 'Items', 'World map', 'Vitals'))


def japan_story_fields():
    """Only source-backed Japanese progress-like values; not USA event flags."""
    return tuple(field for field in JAPAN_FIELDS if field.group in (
        'Items', 'World map', 'Modes and engine'))


def japan_story_crosswalk_rows(rdram):
    """Region-correct event-bit research rows in the shared Story Progress page.

    Unverified offsets are visible as bit observations only. No edit controls
    or semantic claims are created for these hypotheses.
    """
    rows = []
    for field in CROSS_REGION_FIELDS:
        if not field.key.startswith(('event:', 'plasma:')):
            continue
        reading = read_cross_region_field(rdram, field) if rdram is not None else None
        raw = '0x' + reading.raw if reading and not reading.error else '—'
        if reading and not reading.error and field.mask is not None:
            bit_set = bool(int(reading.raw, 16) & field.mask)
            value = ('Set' if bit_set else 'Clear') if field.evidence == 'user-confirmed' else (
                'Bit set (unverified)' if bit_set else 'Bit clear (unverified)')
        else:
            value = 'Unavailable'
        key = 'jp_cross_' + field.key.replace(':', '_')
        rows.append(dict(
            key=key, name=field.label,
            section=story_section_for_key(field.key.split(':', 1)[1]),
            bank='JP story bit' if field.evidence == 'user-confirmed' else 'JP candidate bit',
            address=field.japan, mask=f'0x{field.mask:X}' if field.mask is not None else '—',
            value=value, raw=raw,
            source=(f'Japan-0 {field.evidence}; USA 0x{field.usa:08X}; '
                    f'{field.note}; read-only; bit change is not event proof')))
    return tuple(rows)
