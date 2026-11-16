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
