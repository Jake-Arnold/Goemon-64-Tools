"""Local native inspector editor drafts, not proof of RAM identity."""
from __future__ import annotations
import json
import os
from pathlib import Path
import tempfile

from practice.launcher_preferences import preferences_path

FORMAT = 'goemon-native-inspector-v1'
MAX_TIMELINE_TEXT = 65536


def inspector_preferences_path():
    return preferences_path().with_name('native-inspector.json')


def validated(doc):
    if not isinstance(doc, dict) or doc.get('format') != FORMAT:
        return {}
    watches, timeline, steps = (doc.get(k, '') for k in ('watches', 'timeline', 'steps'))
    if not all(isinstance(v, str) for v in (watches, timeline, steps)):
        return {}
    if len(watches) > 8192 or len(timeline) > MAX_TIMELINE_TEXT or len(steps) > 4:
        return {}
    return dict(watches=watches, timeline=timeline, steps=steps,
                located=doc.get('located') is True)


def load_editor_preferences(path):
    try:
        with Path(path).open('r', encoding='utf-8') as stream:
            raw = stream.read(512000 + 1)
        if len(raw) > 512000:
            return {}
        return validated(json.loads(raw))
    except (OSError, ValueError, TypeError):
        return {}


def save_editor_preferences(path, *, watches, timeline, steps, located):
    dest = Path(path)
    doc = dict(format=FORMAT, watches=watches, timeline=timeline, steps=steps, located=located)
    if not validated(doc):
        raise ValueError('Inspector editor settings exceed supported bounds')
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=dest.parent,
                                         prefix=f'.{dest.name}.', suffix='.tmp', delete=False) as stream:
            tmp = Path(stream.name)
            json.dump(doc, stream, ensure_ascii=False)
            stream.write('\n')
        os.replace(tmp, dest)
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)
