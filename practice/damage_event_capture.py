"""Read-only, damage-triggered memory recording for the USA Goemon toolkit.

Candidate fields are correlations only, never verified collision flags.
Samples use canonical big-endian guest bytes. Cadence is best effort.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import time

from practice.backends.memory import Rdram

HP = 0x8015C5E4
CHARACTER = 0x8015C5DC
MAP = 0x800C7AB2
LOADING = 0x8015C5D4
TASK_POINTER = 0x801FC604
OBJECT_POINTER = 0x801FC60C
REGIONS = (("system", 0x800C7800, 0x1000),
           ("game_data", 0x8015C500, 0x900))
DYNAMIC_REGIONS = (("player_task", "task", 0xF0),
                   ("player_object", "object", 0x98))
MAX_EVENTS = 8
PRE_SAMPLES = 30
POST_SECONDS = 3.5
MAX_ROWS = 100


@dataclass(frozen=True)
class Sample:
    when: float
    hp: int
    map_id: int
    character: int
    pointers: tuple[int, int]
    regions: tuple[tuple[str, int, bytes], ...]

    def region(self, name):
        for key, address, data in self.regions:
            if key == name:
                return address, data
        return None


@dataclass
class Event:
    before: tuple[Sample, ...]
    after: list[Sample]
    complete: bool = False

    @property
    def start(self):
        return self.after[0].when

    @property
    def baseline(self):
        return self.before[-1]


class DamageCaptureError(RuntimeError):
    """Session cannot continue without mixing unrelated game states."""


class DamageRecorder:
    def __init__(self, ram, *, post_seconds=POST_SECONDS, max_events=MAX_EVENTS):
        if not 0.25 <= post_seconds <= 20 or not 1 <= max_events <= 20:
            raise ValueError("Invalid recording limits")
        self.ram = ram
        self.post_seconds = post_seconds
        self.max_events = max_events
        self.before = deque(maxlen=PRE_SAMPLES)
        self.events = []
        self.active = None
        self.context = None
        self.previous = None
        self.stopped = False
        self.samples = 0

    def _read(self, now):
        ram = self.ram
        if ram.u8(LOADING) != 0:
            raise DamageCaptureError("Game is loading; recording stopped")
        character = ram.u32(CHARACTER)
        map_id = ram.u16(MAP)
        hp = ram.u32(HP)
        if character > 3 or map_id >= 0x800 or hp > 127:
            raise DamageCaptureError("Player/map/health unavailable or implausible")
        pointers = (ram.u32(TASK_POINTER), ram.u32(OBJECT_POINTER))
        if not all(Rdram.is_ram_pointer(p, size) for p, (_, _, size) in
                   zip(pointers, DYNAMIC_REGIONS)):
            raise DamageCaptureError("Player pointers unavailable or out of RAM")
        regions = []
        for name, addr, size in REGIONS:
            data = ram.read_guest(addr, size)
            if len(data) != size:
                raise DamageCaptureError("Incomplete memory read")
            regions.append((name, addr, data))
        for (name, _, size), address in zip(DYNAMIC_REGIONS, pointers):
            data = ram.read_guest(address, size)
            if len(data) != size:
                raise DamageCaptureError("Incomplete player memory read")
            regions.append((name, address, data))
        return Sample(now, hp, map_id, character, pointers, tuple(regions))

    def sample(self, now=None):
        if self.stopped:
            return False
        try:
            snap = self._read(time.monotonic() if now is None else now)
            if self.context is None:
                self.context = (snap.map_id, snap.character, snap.pointers)
            elif (snap.map_id, snap.character, snap.pointers) != self.context:
                raise DamageCaptureError("Scene, character or player pointers changed")
            self.samples += 1
            if self.active is not None:
                self.active.after.append(snap)
                if snap.when - self.active.start >= self.post_seconds:
                    self.active.complete = True
                    self.events.append(self.active)
                    self.active = None
                    self.before.clear()
                    if len(self.events) >= self.max_events:
                        self.stopped = True
            elif self.previous is not None and snap.hp < self.previous.hp and self.before:
                self.active = Event(tuple(self.before), [snap])
                self.before.clear()
            else:
                self.before.append(snap)
            self.previous = snap
            return True
        except (OSError, ValueError, RuntimeError):
            self.stopped = True
            raise

    def stop(self):
        self.stopped = True
        if self.active is not None:
            self.events.append(self.active)  # Incomplete event is labelled partial.
            self.active = None


def _value(sample, region, offset, width):
    item = sample.region(region)
    if item is None or offset + width > len(item[1]):
        return None
    return int.from_bytes(item[1][offset:offset + width], "big")


def _features(event, region, offset, width):
    original = _value(event.baseline, region, offset, width)
    if original is None:
        return None
    # Exclude fields already changing in the preceding window.
    if any(_value(s, region, offset, width) != original for s in event.before[-4:]):
        return None
    early = [s for s in event.after if s.when - event.start <= 0.75]
    values = [_value(s, region, offset, width) for s in early]
    changed = [v for v in values if v is not None and v != original]
    if not changed:
        return None
    final = _value(event.after[-1], region, offset, width)
    returned = event.complete and final == original
    monotone = len(changed) > 2 and (
        all(a >= b for a, b in zip(changed, changed[1:])) or
        all(a <= b for a, b in zip(changed, changed[1:])))
    return {"baseline": original, "peak": changed[0], "last": final,
            "returned": returned, "monotone": monotone}


def candidate_report(events, *, limit=MAX_ROWS):
    """Rank correlated changes; do not infer collision semantics."""
    completed = [e for e in events if e.complete and e.before and e.after]
    if not completed:
        return []
    candidates = {}
    for event_index, event in enumerate(completed):
        for name, address, data in event.baseline.regions:
            for width, kind in ((1, "u8"), (2, "u16"), (4, "u32")):
                for offset in range(0, len(data) - width + 1, width):
                    guest_addr = address + offset
                    # HP itself is the event trigger, not a discovered
                    # invulnerability timer. Mask both known regional forms.
                    # USA HP is a word; Japan-0 HP is the last byte of a word.
                    if any(guest_addr < addr+span and guest_addr+width > addr
                           for addr,span in ((HP,4),(0x80161DD7,1))):
                        continue
                    features = _features(event, name, offset, width)
                    if features is None:
                        continue
                    key = (name, offset, kind)
                    record = candidates.setdefault(key, {"region": name,
                        "offset": offset, "address": f"0x{guest_addr:08X}",
                        "type": kind, "events": [], "hits": 0, "returns": 0,
                        "monotone": 0})
                    record["hits"] += 1
                    record["returns"] += int(features["returned"])
                    record["monotone"] += int(features["monotone"])
                    record["events"].append({"index": event_index + 1, **features})
    results = []
    for record in candidates.values():
        record["score"] = (10 * record["hits"] + 8 * record["returns"] +
                           2 * record["monotone"])
        results.append(record)
    return sorted(results, key=lambda row: (-row["hits"], -row["returns"],
                      -row["score"], row["address"], row["type"]))[:limit]


def event_timeline(event, candidate):
    samples = list(event.before[-10:]) + event.after
    return [{"t": round(s.when - event.start, 3), "hp": s.hp,
             "value": _value(s, candidate["region"], candidate["offset"],
                             {"u8": 1, "u16": 2, "u32": 4}[candidate["type"]])}
            for s in samples]


def export_report(recorder, *, limit=MAX_ROWS):
    candidates = candidate_report(recorder.events, limit=limit)
    return {"schema": "goemon-damage-event-v1", "read_only": True,
            "sample_count": recorder.samples, "event_count": len(recorder.events),
            "complete_events": sum(e.complete for e in recorder.events),
            "post_seconds": recorder.post_seconds, "context": recorder.context,
            "events": [{"complete": e.complete, "baseline_hp": e.baseline.hp,
                        "hit_hp": e.after[0].hp, "duration": round(e.after[-1].when - e.start, 3),
                        "samples": len(e.after)} for e in recorder.events],
            "candidates": [{**row,
                            "timelines": [event_timeline(e, row) for e in recorder.events]}
                           for row in candidates],
            "limitations": "Correlated transient memory changes; not proof of collision or invulnerability semantics."}
