"""Persistent display-only names for built-in Live Memory fields.

Keys are stable built-in watch IDs. Renaming never changes guest memory,
watch definitions, verification status or source/provenance.
"""
import json

FORMAT_ID = 'goemon-live-memory-names-v1'
MAX_NAMES = 512


def validate_watch_label(value):
    if not isinstance(value, str):
        raise ValueError('Field name must be text')
    value = value.strip()
    if not value or len(value) > 64 or any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError('Field name must contain 1–64 printable characters')
    return value


def _validated_names(names):
    if not isinstance(names, dict) or len(names) > MAX_NAMES:
        raise ValueError('Invalid Live Memory name list')
    validated = {}
    for key, value in names.items():
        if not isinstance(key, str) or not key or len(key) > 128 or any(ord(c) < 32 for c in key):
            raise ValueError('Invalid original field identifier')
        validated[key] = validate_watch_label(value)
    return validated


def load_watch_names(path):
    if not path.exists():
        return {}
    document = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(document, dict) or document.get('format') != FORMAT_ID:
        raise ValueError('Unsupported Live Memory names file format')
    return _validated_names(document.get('names'))


def save_watch_names(path, names):
    validated = _validated_names(names)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(
        json.dumps({'format': FORMAT_ID, 'names': validated}, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )
    temporary.replace(path)
