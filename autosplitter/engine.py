"""Ordered, conservative state-change triggers for LiveSplit.

Never emits a split purely because a save loaded inside a trigger region.
A segment must be entered from outside while the timer is running.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import json
import math
import pathlib
import xml.etree.ElementTree as ET


def segment_names(lss: str) -> list[str]:
    root = ET.parse(lss).getroot()
    return [node.findtext("Name", "").strip() for node in root.findall("./Segments/Segment")]


def make_route(names: list[str]):
    return {"game": "Mystical Ninja Starring Goemon", "variant": "US Goemon64Recomp",
            "source": "Any% Unrestricted speedrun.com community route (not verified ZAR personal splits)",
            "segments": [{"name": name, "trigger": None} for name in names]}


def save_route(route: dict, filename: str):
    pathlib.Path(filename).write_text(json.dumps(route, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")


def load_route(filename: str):
    data = json.loads(pathlib.Path(filename).read_text(encoding="utf-8"))
    if not isinstance(data.get("segments"), list):
        raise ValueError("Expected a segments list")
    return data


def nearby(frame: dict, trigger: dict) -> bool:
    if any(frame.get(c) is None for c in ("x", "y", "z")): return False
    if "character" in trigger and frame.get("character") != trigger["character"]: return False
    # Optional extra observable guard, for route nodes sharing nearby coordinates.
    if "action" in trigger and frame.get("action") != trigger["action"]: return False
    radius = float(trigger.get("radius", 50))
    if not (0 < radius < 10000): raise ValueError("Radius must be between 0 and 10000")
    distance = math.sqrt(sum((frame[c]-trigger[c])**2 for c in ("x", "y", "z")))
    return distance <= radius


@dataclass
class SplitResult:
    index: int
    name: str


class SplitEngine:
    def __init__(self, route: dict, *, stable_samples: int=2):
        self.route = route
        self.index = 0
        self.old = None
        self.stable_samples = stable_samples
        self.inside_count = 0
        self.armed = False
        self.last_timer_phase = None

    def align_index(self, index: int):
        self.index = min(max(0,index), len(self.route["segments"]))
        self.inside_count = 0
        self.armed = False
        self.old = None

    def update(self, frame: dict, timer_running: bool) -> Optional[SplitResult]:
        if not timer_running:
            self.inside_count = 0
            self.armed = False
            self.old = frame
            return None
        if self.index >= len(self.route["segments"]):
            self.old = frame
            return None
        segment = self.route["segments"][self.index]
        trigger = segment.get("trigger")
        if not trigger:
            self.old = frame
            return None  # Unconfigured: never guess or skip.
        kind = trigger.get("type")
        if kind == "position_enter":
            inside = nearby(frame, trigger)
            if not inside: self.armed = True; self.inside_count = 0
            elif self.armed and frame.get("loading") == 0:
                self.inside_count += 1
                if self.inside_count >= self.stable_samples:
                    result = SplitResult(self.index, segment["name"])
                    self.index += 1
                    self.inside_count = 0
                    self.armed = False
                    self.old = frame
                    return result
        elif kind == "character_change":
            if (self.old is not None and self.old.get("character") == trigger.get("from")
                    and frame.get("character") == trigger.get("to")):
                result = SplitResult(self.index, segment["name"])
                self.index += 1
                self.old = frame
                return result
        else: raise ValueError(f"Unknown trigger type: {kind}")
        self.old = frame
        return None
