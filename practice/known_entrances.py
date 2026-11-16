"""Permanent small list of coordinates observed in actual Goemon gameplay.

These are static facts about named scene/entrance pairs, NOT an exhaustive map.
One scene can have many valid entrances; preserve the individual entrance IDs.
The full, validated original-USA entrance atlas may be cached separately.
"""
from __future__ import annotations

from practice.japanese_position import (
    JAPAN_OEDO_SOUTH_SCENE, JAPAN_OEDO_SOUTH_ENTRANCE,
)

# Observed Goemon position in Oedo Town South, Japanese game. The user expects
# the same XYZ for the USA scene. Heading 0 and mode 0x10 are experimental
# fallback values, NOT measured from a native entrance record or original ROM.
# Do not add guessed scene coordinates to this file.
_KNOWN_ENTRANCES = (
    dict(
        id="known:353:oedo-south",
        kind="known",
        source_map=None,
        source_file=None,
        definition=0,
        exit_id=0,
        destination=JAPAN_OEDO_SOUTH_SCENE,
        position=list(JAPAN_OEDO_SOUTH_ENTRANCE),
        heading=0,
        mode=0x10,
        provenance="observed-japan-oedo-south-goemon-xyz",
        heading_mode_verified=False,
    ),
)


def known_entrances(destination: int):
    """Return independent records, so caller edits cannot mutate constants."""
    if type(destination) is not int:
        return []
    return [
        {**row, "position": list(row["position"])}
        for row in _KNOWN_ENTRANCES if row["destination"] == destination
    ]


def known_entrance_count() -> int:
    return len(_KNOWN_ENTRANCES)
