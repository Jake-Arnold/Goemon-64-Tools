"""Named native-emulator savestate SLOT metadata, never a copied game state.

A recorded slot is an emulator-owned native full savestate request. The toolkit
cannot verify that the emulator finished saving; labels and snapshots are
informational. No original game RAM, ROM, savestate or assets are persisted.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import tempfile

FORMAT = 'goemon-named-native-saves-v1'
REGIONS = ('usa', 'japan')
BACKENDS = ('project64', 'mupen64plus')
MAX_ENTRIES = 40


def _validate(entry):
    if not isinstance(entry, dict) or set(entry) != {
        'name', 'region', 'backend', 'slot', 'scene', 'character', 'xyz',
        'requested_utc'}:
        raise ValueError('Invalid named savestate slot metadata')
    if (not isinstance(entry['name'], str) or
            not 1 <= len(entry['name'].strip()) <= 64):
        raise ValueError('Named checkpoint must be 1–64 characters')
    if entry['region'] not in REGIONS or entry['backend'] not in BACKENDS:
        raise ValueError('Unsupported named checkpoint region/backend')
    if type(entry['slot']) is not int or not 0 <= entry['slot'] <= 9:
        raise ValueError('Emulator save slot must be 0–9')
    if entry['scene'] is not None and (
            type(entry['scene']) is not int or not 0 < entry['scene'] < 0x800):
        raise ValueError('Invalid named checkpoint scene')
    if entry['character'] is not None and (
            type(entry['character']) is not int or entry['character'] not in range(4)):
        raise ValueError('Invalid named checkpoint character')
    xyz = entry['xyz']
    if xyz is not None and (not isinstance(xyz, list) or len(xyz) != 3 or
                            any(type(x) not in (int, float) or
                                not math.isfinite(x) or abs(x) > 1_000_000
                                for x in xyz)):
        raise ValueError('Invalid position metadata')
    try:
        stamp = datetime.fromisoformat(entry['requested_utc'])
        if stamp.tzinfo is None:
            raise ValueError('Timezone required')
    except (ValueError, TypeError) as exc:
        raise ValueError('Invalid named checkpoint timestamp') from exc
    return entry


def make_named_checkpoint(name, region, backend, slot, *, scene=None,
                          character=None, xyz=None):
    record = {
        'name': str(name).strip(), 'region': region, 'backend': backend,
        'slot': slot, 'scene': scene, 'character': character,
        'xyz': list(xyz) if xyz is not None else None,
        'requested_utc': datetime.now(timezone.utc).isoformat(),
    }
    return _validate(record)


def upsert_named_checkpoint(existing, record):
    """Replace the previous label for the same native slot; it was overwritten."""
    _validate(record)
    retained = [
        item for item in existing
        if not (item['region'] == record['region']
                and item['backend'] == record['backend']
                and item['slot'] == record['slot'])
    ]
    for item in retained:
        _validate(item)
    result = [record, *retained]
    if len(result) > MAX_ENTRIES:
        raise ValueError('Too many named state slots')
    return result


def label_named_checkpoint(entry):
    _validate(entry)
    where = f' | scene 0x{entry["scene"]:03X}' if entry['scene'] is not None else ''
    who = f' | char {entry["character"]}' if entry['character'] is not None else ''
    return f'{entry["name"]} — slot {entry["slot"]}{where}{who}'


def load_named_checkpoints(path: Path):
    path = Path(path)
    if not path.exists():
        return []
    if path.stat().st_size > 128_000:
        raise ValueError('Named checkpoint metadata file too large')
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError) as exc:
        raise ValueError('Invalid named checkpoint metadata JSON') from exc
    if not isinstance(payload, dict) or payload.get('format') != FORMAT:
        raise ValueError('Unexpected native checkpoint metadata format')
    entries = payload.get('entries')
    if not isinstance(entries, list) or len(entries) > MAX_ENTRIES:
        raise ValueError('Invalid native checkpoint entries')
    used = set()
    for item in entries:
        _validate(item)
        key = (item['region'], item['backend'], item['slot'])
        if key in used:
            raise ValueError('Duplicate native emulator state slot')
        used.add(key)
    return entries


def save_named_checkpoints(path: Path, entries):
    if len(entries) > MAX_ENTRIES:
        raise ValueError('Too many named checkpoint entries')
    for entry in entries:
        _validate(entry)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {'format': FORMAT, 'entries': entries}
    data = json.dumps(payload, indent=2, allow_nan=False) + '\n'
    name = None
    try:
        with tempfile.NamedTemporaryFile(
                'w', dir=path.parent, prefix='.named-saves-',
                suffix='.tmp', delete=False, encoding='utf-8') as stream:
            name = stream.name
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)


def japan_checkpoint_summary(reader):
    """Read-only scene, character and XYZ annotation, never restore via RAM."""
    if reader is None:
        return {}
    from practice.japan_value_freezes import stable_japan_gameplay
    from practice.japanese_position import read_japan_position
    try:
        state = stable_japan_gameplay(reader)
        if state is None:
            return {}
        _engine, scene, character, _loading = state
        try:
            xyz = list(read_japan_position(reader))
        except (ValueError, OSError, RuntimeError, PermissionError):
            xyz = None
        return {'scene': scene, 'character': character, 'xyz': xyz}
    except (ValueError, OSError, RuntimeError, PermissionError):
        return {}
