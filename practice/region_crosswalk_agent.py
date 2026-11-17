"""Agent-facing, read-only bidirectional N64 static-data crosswalk proposals.

Known explicit mappings always outrank the simple displacement. An unknown
address requires the caller to classify it as static-global or saved-event
before a speculative other-region address can be generated.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

from practice.region_memory_crosswalk import CROSS_REGION_FIELDS
from practice.region_unlocks import REGION_DELTA


# Examples grounded in the existing research. This is NOT an exhaustive
# classification of overlay/code/dynamic locations; agents must determine
# symbol ownership independently before supplying a new discovery.
EXCLUDED_GUEST_ADDRESSES = frozenset({
    0x80077858,  # USA VM PC storage, not a confirmed Japanese relocatable field
    0x801C77E0,  # USA VM state
    0x801FC60C,  # USA player object pointer storage; scene-dependent
    0x801FC604,  # USA player task pointer storage; scene-dependent
    0x802F7060,  # Dynamic Impact controller sample
    0x80151B10,  # Japanese position, which is not USA position+delta
    0x80151B14,
    0x80151B18,
})
_ALLOWED_KINDS = frozenset(("static-global", "saved-event"))
_ALLOWED_REGIONS = frozenset(("usa", "japan"))


@dataclass(frozen=True)
class Proposal:
    key: str
    source_region: str
    source_address: str
    target_region: str
    target_address: str
    status: str
    width_bytes: int
    mask: str | None
    note: str

    def as_dict(self):
        return asdict(self)


def propose_other_region(source_region: str, address: int, *,
                         kind: str | None = None, width: int = 1,
                         mask: int | None = None) -> tuple[Proposal, ...]:
    """Look up known pairs first; otherwise emit *only* a classified candidate.

    This function never reads or writes game RAM. It does not validate a
    discovered field's semantics; tests in both ROM revisions remain required.
    """
    source_region = source_region.lower()
    if source_region not in _ALLOWED_REGIONS:
        raise ValueError("Source region must be 'usa' or 'japan'")
    if not isinstance(address, int) or not 0x80000000 <= address < 0x80800000:
        raise ValueError("Address must be in canonical 8 MiB N64 guest RDRAM")
    if width not in (1, 2, 4) or address + width > 0x80800000:
        raise ValueError("Invalid source guest width")
    if mask is not None and not 0 < mask < (1 << (8 * width)):
        raise ValueError("Mask must fit the source field width")
    if kind is not None and kind not in _ALLOWED_KINDS:
        raise ValueError("Kind must be 'static-global' or 'saved-event'")
    if address in EXCLUDED_GUEST_ADDRESSES:
        raise ValueError("Known dynamic/VM/player address: do not offset it")

    target_region = "japan" if source_region == "usa" else "usa"
    is_usa = source_region == "usa"
    known = tuple(
        field for field in CROSS_REGION_FIELDS
        if (field.usa if is_usa else field.japan) == address
        and (mask is None or field.mask == mask)
    )
    if known:
        return tuple(Proposal(
            key=field.key,
            source_region=source_region,
            source_address=f"0x{address:08X}",
            target_region=target_region,
            target_address=f"0x{field.japan if is_usa else field.usa:08X}",
            status=field.evidence,
            width_bytes=field.width,
            mask=f"0x{field.mask:X}" if field.mask is not None else None,
            note=(field.note + ("; explicit non-delta exception"
                                if field.is_exception else "")).strip("; "),
        ) for field in known)

    if kind is None:
        raise ValueError(
            "Unknown field: classify --kind static-global or saved-event "
            "after checking original region, lifetime, width and overlay")
    target_address = address + (REGION_DELTA if is_usa else -REGION_DELTA)
    if not 0x80000000 <= target_address < 0x80800000:
        raise ValueError("Offset target outside 8 MiB N64 guest RDRAM")
    return (Proposal(
        key="unmapped-" + kind,
        source_region=source_region,
        source_address=f"0x{address:08X}",
        target_region=target_region,
        target_address=f"0x{target_address:08X}",
        status="offset-candidate",
        width_bytes=width,
        mask=f"0x{mask:X}" if mask is not None else None,
        note=("Inferred from candidate fixed-data offset 0x57F0; NOT "
              "verified in the target ROM. Capture source+target gameplay "
              "A/B/control evidence before naming/promoting."),
    ),)
