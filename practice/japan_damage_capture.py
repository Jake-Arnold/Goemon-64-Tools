"""Japan-0 damage-triggered read-only events using region-correct RAM fields.

Reuses the existing USA DamageRecorder timeline and ranking logic while
supplying a Japanese _read() implementation; never dereferences USA player
task pointers or guesses a Japanese actor/object structure.
"""
from __future__ import annotations

from practice.damage_event_capture import (
    DamageRecorder, Sample, DamageCaptureError,
)
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE,
    JAPAN_DEBUG_CHARACTER, JAPAN_DEBUG_LOADING,
    JAPAN_ORDINARY_ENGINE_MODE,
)

JAPAN_HP_BYTE = 0x80161DD7
JAPAN_DAMAGE_REGIONS = (
    ("system", 0x800CD000, 0x600),
    ("game_data", 0x80161D80, 0x700),
)


class JapanDamageRecorder(DamageRecorder):
    hp_address = JAPAN_HP_BYTE
    region = 'japan-0'

    def _read(self, now):
        ram=self.ram
        state=ram.read_guest(JAPAN_DEBUG_ENGINE_MODE,1)[0]
        loading=int.from_bytes(ram.read_guest(JAPAN_DEBUG_LOADING,4),'big')
        if state != JAPAN_ORDINARY_ENGINE_MODE or loading:
            raise DamageCaptureError(
                'Japanese game is not in stable ordinary gameplay')
        character=int.from_bytes(
            ram.read_guest(JAPAN_DEBUG_CHARACTER,4),'big')
        map_id=int.from_bytes(ram.read_guest(JAPAN_DEBUG_SCENE,2),'big')
        hp=ram.read_guest(JAPAN_HP_BYTE,1)[0]
        if character > 3 or not 0 < map_id < 0x800 or hp > 127:
            raise DamageCaptureError(
                'Japanese character/map/health unavailable or implausible')
        regions=[]
        for name,address,size in JAPAN_DAMAGE_REGIONS:
            data=ram.read_guest(address,size)
            if len(data) != size:
                raise DamageCaptureError('Incomplete Japanese RAM region read')
            regions.append((name,address,data))
        # No Japanese task/object pointer verified. Preserve the existing
        # Sample schema, with sentinel pointers that are never dereferenced.
        return Sample(now,hp,map_id,character,(0,0),tuple(regions))
