"""Reconstruct the isolated native replay input and verify stored source hashes."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def build():
    records = json.loads((ROOT / 'index.json').read_text())['functions']
    seen = set()
    counts = Counter()
    sizes = Counter()
    result = []
    for record in records:
        region, name = record['region'], record['name']
        assert (region, name) not in seen
        seen.add((region, name))
        counts[region] += 1
        sizes[region] += record['original_bytes']
        evidence = json.loads((ROOT / 'evidence' / region / (name + '.json')).read_text())
        assert all(evidence[k] == v for k, v in record.items())
        assert evidence['status'] == 'LINKED_EXACT'
        assert evidence['reference_linked_rom_match']
        positive, negative = evidence['attempts']
        assert positive['exact_object'] and positive['linked_rom_match']
        assert negative['negative'] and negative['returncode'] == 0 and not negative['exact_object']
        sources = []
        for filename, attempt in [('candidate.c', positive), ('negative.c', negative)]:
            data = (ROOT / 'sources' / region / name / filename).read_bytes()
            assert hashlib.sha256(data).hexdigest() == attempt['source_sha256']
            sources.append(data.decode('utf-8'))
        result.append({**record, 'variants': [{'label': positive['label'], 'source': sources[0], 'flags': positive['flags']}], 'negative_c': sources[1]})
    assert counts == {'usa': 104, 'japan_0': 48}
    assert sizes == {'usa': 15924, 'japan_0': 7268}
    return result

if __name__ == '__main__':
    Path(sys.argv[1]).write_text(json.dumps(build(), indent=2) + '\n')
