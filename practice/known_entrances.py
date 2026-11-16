"""Permanent small list of coordinates observed in actual Goemon gameplay.

These are static facts about named scene/entrance pairs, NOT an exhaustive map.
One scene can have many valid entrances; preserve the individual entrance IDs.
The full, validated original-USA entrance atlas may be cached separately.
"""
from __future__ import annotations

from practice.japanese_position import (
    JAPAN_OEDO_SOUTH_SCENE, JAPAN_OEDO_SOUTH_ENTRANCE,
)

# Oedo South XYZ first observed in the Japanese game. Confirmed in the
# verified original-USA ROM atlas supplied on 2026-11-16: both the native
# default:353 and source-scene 351 entrance 15F:006 have XYZ (-289,0,-167),
# heading 256, mode 16. This built-in fallback now matches those values.
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
        heading=256,
        mode=16,
        provenance="observed-japan-oedo-south-goemon-xyz",
        heading_mode_verified=True,
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
