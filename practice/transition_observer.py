"""Read-only original-ROM-derived scene and Script VM context.

These values are diagnostic observations, not validated scene transitions or
boss health. This module never writes guest memory or requires a player pointer.
"""
from __future__ import annotations

FIELDS = (
    ("Map ID", 0x800C7AB2, "u16"),
    ("VM program cursor", 0x80077858, "u32"),
    ("VM state", 0x801C77E0, "u32"),
    ("VM resource ID", 0x801C78E8, "u32"),
    ("VM pause byte", 0x801C78FC, "s8"),
)


def read_transition_observation(ram):
    """Read independent fields; one unreadable field does not hide the rest."""
    result = {}
    for label, address, kind in FIELDS:
        try:
            if kind == "u16":
                value = ram.u16(address)
            elif kind == "u32":
                value = ram.u32(address)
            else:
                raw = ram.read_guest(address, 1)
                if len(raw) != 1:
                    raise OSError("Incomplete read")
                value = int.from_bytes(raw, "big", signed=True)
            result[label] = value
        except (OSError, ValueError, RuntimeError):
            result[label] = None
    return result


def format_transition_observation(observation):
    def display(label):
        value = observation.get(label)
        if value is None:
            return "unavailable"
        if label == "VM pause byte":
            return str(value)
        return f"0x{value:08X}" if label == "VM program cursor" else str(value)

    return (
        f"Map: {display('Map ID')}   |   VM cursor: {display('VM program cursor')}   |   "
        f"VM state: {display('VM state')}\n"
        f"Resource ID: {display('VM resource ID')}   |   Pause: {display('VM pause byte')}\n"
        "VM cursor is not the text-token cursor. A resource request does not prove "
        "scene activation. Compare repeated captures; do not infer boss HP from these fields."
    )
