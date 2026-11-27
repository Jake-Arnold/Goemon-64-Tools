"""ROM-free semantic index of canonical reconstructed C, never a G2 promoter."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from . import batch_registry as batches, japan_character_switch_four as switches
from .verify import claimed_functions, load_manifest

ROOT = Path(__file__).resolve().parent
REGIONS = ('usa', 'japan_0')
LEVELS = ('Confirmed', 'High', 'Medium', 'Unknown')
NOOP_HASHES = {
    '78aa5094d5ec7291c79f799c009d04f06c2f20187988e3dcc8d35ee5efdbb378',
    '691e766163b1b8288cf1e76b4dc9eb7dde764cde7f749bf5aef916d919300f2b',
}
HISTORICAL_JP = ('glitch_g2_20261121', 'vm_g2_20261121', 'jp_donor10_20261121',
    'jp_donor4_20261121', 'jp_tiny7_20261121', 'jp_retry29_20261121',
    'jp_retry10_20261121', 'jp_expand7_20261121', 'jp_short145_20261121/batch44',
    'jp_short145_20261121/batch101', 'jp55_allatonce_20261122')


def read(path):
    return json.loads(path.read_text())


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def number(x):
    return int(x, 0) if isinstance(x, str) else x


def digest(data):
    return hashlib.sha256(data).hexdigest()


def record(region, name, off, vma, size, code_hash, evidence):
    return dict(region=region, name=name, rom_offset=off, vma=vma, size=size,
                original_sha256=code_hash, identity_evidence=sorted(evidence),
                confidence='Unknown', behavior=None, semantic_alias=None, gameplay_role=None, subsystem=None, review_method='unreviewed',
                evidence=[], source=None, owner=None, callees=[], callers=[], references=[], fields=[], source_fields=[], counterpart=None,
                counterpart_candidate=None, unresolved='Gameplay role and caller context not established.')


def canonical(root=ROOT):
    """Enumerate USA proof and JP inventory, reconciling exact JP historical extents."""
    proof = read(root/'results/combined.json')
    us = proof['comparison']['functions']
    require(proof['status'] == 'matched' and proof['comparison']['full_rom_match'], 'USA proof not exact')
    claims = claimed_functions(load_manifest(root/'manifest.json'))
    require({(f['name'], f['rom_offset'], f['size']) for f in claims} ==
            {(f['name'], number(f['rom_offset']), f['size']) for f in us}, 'USA proof/manifest drift')
    require(all(f['matched'] and f['expected_sha256'] == f['candidate_sha256'] for f in us), 'USA function proof drift')
    out = [record('usa', f['name'], number(f['rom_offset']), number(f['guest_address']),
                  f['size'], f['expected_sha256'], ['results/combined.json']) for f in us]
    source_hashes = {'usa': set(proof['sources_sha256_lf'].values()), 'japan_0': set()}
    base_path = 'results/japan_0_3019_promo36_inventory_20261126.json'
    base = read(root/base_path)
    names = set(base['previous_C_names']) | set(base['new_C_names'])
    require(len(names) == 3019, 'JP predecessor name count')
    new_batches = [(b, batches.batch_rows(b, 'japan_0', root)) for b in batches.jp_batches(root)]
    for b, rows in new_batches:
        new = {f['name'] for f in rows}
        require(not names & new, 'JP duplicate ownership: '+b['id'])
        names.update(new)
    extents, hashes, evidence, noops = defaultdict(set), defaultdict(set), defaultdict(set), set()

    def add(n, a, z, v, h, src, ref):
        if not isinstance(n, str) or n not in names or z is None:
            return
        m = re.fullmatch(r'func_([0-9A-Fa-f]+)_([0-9A-Fa-f]+)', n)
        if m:
            v, off = (int(i, 16) for i in m.groups())
            if a is not None and number(a) != off:
                return
            a = off
        a, z, v = number(a), number(z), number(v)
        if type(a) is not int or type(z) is not int or z <= 0 or z % 4 or a % 4:
            return
        if v is None and a < 0x570000:
            v = a + 0x7FFFF400  # main-segment identity only, never an overlay mapping
        extents[n].add((a, z, v))
        evidence[n].add(ref)
        if isinstance(h, str) and re.fullmatch('[a-f0-9]{64}', h):
            hashes[n].add(h)
        if isinstance(src, str) and re.fullmatch('[a-f0-9]{64}', src):
            source_hashes['japan_0'].add(src)

    def scan(x, ref):
        if isinstance(x, dict):
            add(x.get('jp') or x.get('jp_name') or x.get('name') or x.get('function'),
                x.get('jp_rom', x.get('jp_rom_offset', x.get('rom_offset', x.get('off', x.get('offset'))))),
                x.get('size', x.get('sz', x.get('size_bytes', x.get('original_bytes', x.get('original_size'))))),
                x.get('vma', x.get('vram', x.get('guest_vma'))),
                x.get('original_sha256', x.get('original_code_sha256', x.get('code_sha256', x.get('hash')))),
                x.get('source_sha256', x.get('candidate_source_sha256')), ref)
            for value in x.values():
                scan(value, ref)
        elif isinstance(x, list):
            for value in x:
                scan(value, ref)

    for p in sorted((root/'regions').glob('japan_0*.json')):
        scan(read(p), p.relative_to(root).as_posix())
    for folder in HISTORICAL_JP:
        ref = f'research/{folder}/manifest.json'
        j = read(root/ref)
        scan(j['regions']['japan_0'] if 'regions' in j else j, ref)
    ref = 'research/jp1686_promotion/candidates.csv'
    with (root/ref).open(newline='') as handle:
        for row in csv.DictReader(handle):
            scan(row, ref)
    ref = 'regions/japan_0_noop_port_290.json'
    for p in read(root/ref)['parents']:
        for n, form in p['c']:
            require(form in ('P', 'Z'), 'unknown JP noop form')
            add(n, None, 12 if form == 'P' else 8, None, None, None, ref)
            noops.add(n)
    for n, a, z, _ in switches.RECORDS:
        add(n, a, z, None, switches.EXPECTED_SHA256[n], None, 'japan_character_switch_four.py')
    for b, rows in new_batches:
        scan(rows, b['research_dir']+'/japan_0-candidates.json')
    ref = 'results/japan_0_2370_cright_inventory_20261123.json'
    j = read(root/ref)
    add(j['new_name'], j['rom_offset'], j['new_original_bytes'], j['vma'],
        j['original_function_sha256'], j['new_source_sha256'], ref)
    for n in sorted(names):
        require(len(extents[n]) == 1 and len(hashes[n]) <= 1, 'JP missing/conflicting extent/hash: '+n)
        a, z, v = next(iter(extents[n]))
        out.append(record('japan_0', n, a, v, z, next(iter(hashes[n]), None), evidence[n]))
    for region in REGIONS:
        rows = [r for r in out if r['region'] == region]
        c, size, _ = batches.expected_totals(region, root)
        require(len(rows) == len({r['name'] for r in rows}) == c and sum(r['size'] for r in rows) == size,
                'canonical count/byte drift: '+region)
        ordered = sorted(rows, key=lambda r: r['rom_offset'])
        require(all(type(r['vma']) is int and 0 <= r['rom_offset'] < r['rom_offset']+r['size'] <= 33554432 for r in rows), 'invalid identity')
        require(all(a['rom_offset']+a['size'] <= b['rom_offset'] for a,b in zip(ordered,ordered[1:])), 'overlapping canonical extents')
    return out, source_hashes, noops


# Source extraction is deliberately conservative; conflicting preprocessor variants
# or missing pinned files leave the row unknown rather than guessing a definition.
def definitions(text, names):
    text = re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', ' ', text, flags=re.S)
    for m in re.finditer(r'\b([A-Za-z_]\w*)\s*\([^;{}]*\)\s*\{', text):
        name = m.group(1)
        if name not in names:
            continue
        start = m.end(); depth = 1
        for i in range(start, len(text)):
            depth += (text[i] == '{') - (text[i] == '}')
            if not depth:
                yield name, ' '.join(text[start:i].split())
                break


def source_index(root, rows, source_hashes):
    names = {r: {f['name'] for f in rows if f['region'] == r} for r in REGIONS}
    bodies = defaultdict(dict)
    for path in sorted(root.rglob('*.c')):
        raw = path.read_bytes().replace(b'\r\n', b'\n')
        h = digest(raw)
        for region in REGIONS:
            if h not in source_hashes[region]:
                continue
            for name, body in definitions(raw.decode('utf-8', errors='replace'), names[region]):
                bodies[region, name].setdefault(body, (path.relative_to(root).as_posix(), h))
    return bodies


def classify_body(body, region):
    loader = {'usa': 'func_80013AC4_146C4', 'japan_0': 'func_80013654_14254'}[region]
    if re.fullmatch(loader+r'\s*\(\s*&?D_[A-Fa-f0-9_]+\s*\)\s*;', body):
        return 'High', 'Registers a static resource-ID list through the regional resource loader.', 'resource_registration'
    if not body or body == 'return;':
        return 'High', 'Source body is empty apart from an optional return.', 'empty_callback'
    m = re.fullmatch(r'return\s+(-?(?:0[xX][0-9A-Fa-f]+|[0-9]+)(?:[uUlL]*)|NULL)\s*;', body)
    if m:
        return 'Medium', 'Returns constant '+m.group(1)+'.', None
    m = re.fullmatch(r'return\s+(\w+->\w+)\s*;', body)
    if m:
        return 'Medium', 'Returns field '+m.group(1)+'.', None
    m = re.fullmatch(r'(\w+->\w+)\s*=\s*(-?(?:0[xX][0-9A-Fa-f]+|[0-9]+)|\w+)\s*;', body)
    if m:
        return 'Medium', 'Assigns '+m.group(2)+' to '+m.group(1)+'.', None
    # Only bounded syntactic shapes; no inferred gameplay roles from field names.
    field = r'(?:\w+->\w+|\w+\[(?:0[xX][0-9A-Fa-f]+|[0-9]+)\]|M2C_FIELD\(\s*\w+\s*,\s*[\w *]+,\s*(?:0[xX][0-9A-Fa-f]+|[0-9]+)\s*\)|\*\([\w *]+\)\(\s*\([\w *]+\)\s*\w+\s*\+\s*(?:0[xX][0-9A-Fa-f]+|[0-9]+)\s*\))'
    value = r'(?:[+-]?(?:0[xX][0-9A-Fa-f]+|[0-9]+(?:\.[0-9]*)?)(?:[fFuUlL]*)|[A-Za-z_]\w*|NULL)'
    stores = re.fullmatch(r'(?:'+field+r'\s*=\s*'+value+r'\s*;\s*)+', body)
    if stores:
        return 'Medium', 'Writes '+str(body.count(';'))+' directly specified field(s); field roles unresolved.', None
    if re.fullmatch(r'return\s+'+field+r'\s*;', body):
        return 'Medium', 'Reads and returns a field; field role unresolved.', None
    m = re.fullmatch(r'(?:return\s+)?(func_[0-9A-Fa-f]+_[0-9A-Fa-f]+)\s*\([^;{}]*\)\s*;', body)
    if m:
        return 'Medium', 'Calls '+m.group(1)+' as sole statement; callee purpose requires review.', None
    return 'Unknown', None, None


def owners(root, rows):
    with (root/'data/rom_file_inventory.csv').open(newline='') as handle:
        files = list(csv.DictReader(handle))
    for region, prefix in (('usa','USA'), ('japan_0','Japan')):
        spans = sorted((number(f[prefix+' expanded ROM offset']), number(f[prefix+' expanded ROM offset'])+int(f[prefix+' expanded bytes']), f['File'])
                       for f in files if f[prefix+' expanded ROM offset'] and f[prefix+' expanded bytes'])
        for row in rows:
            if row['region'] != region:
                continue
            start = row['rom_offset']; end = start + row['size']
            if end <= spans[0][0]:
                row['owner'] = 'main'
            else:
                matched = [name for a,b,name in spans if a <= start and end <= b]
                if len(matched) == 1:
                    row['owner'] = matched[0]


def build(root=ROOT):
    rows, source_hashes, noops = canonical(root)
    owners(root, rows)
    index = {(r['region'], r['name']): r for r in rows}
    bodies = source_index(root, rows, source_hashes)
    for k, row in index.items():
        if row['original_sha256'] in NOOP_HASHES or (k[0] == 'japan_0' and k[1] in noops):
            row.update(confidence='Confirmed', behavior='No operation beyond return/ABI argument handling.',
                       subsystem='empty_callback', review_method='digest_or_manifest_form', evidence=list(row['identity_evidence']))
        alternatives = bodies.get(k, {})
        if len(alternatives) != 1:
            continue
        body, (path, h) = next(iter(alternatives.items()))
        row['source'] = {'path':path, 'sha256':h}
        # Syntactic named call references, not a complete original or dynamic call graph.
        row['callees'] = sorted({n for n in re.findall(r'\b([A-Za-z_]\w*)\s*\(', body)
                                 if n.startswith('func_') or (k[0], n) in index})
        row['references'] = sorted(set(re.findall(r'\bfunc_[0-9A-Fa-f]+_[0-9A-Fa-f]+\b', body)))
        row['source_fields'] = [dict(base=base, type_expression=typ.strip(), offset=number(off))
                                for base,typ,off in sorted(set(re.findall(r'M2C_FIELD\(\s*(\w+)\s*,\s*([\w *]+),\s*(0[xX][0-9A-Fa-f]+|[0-9]+)\s*\)', body)))]
        if row['confidence'] == 'Unknown':
            level, behavior, subsystem = classify_body(body, k[0])
            row.update(confidence=level, behavior=behavior, subsystem=subsystem)
            if level != 'Unknown':
                row['evidence'] = [path]
                row['review_method'] = 'source_pattern'
    for k,row in index.items():
        for callee in row['callees']:
            peer = index.get((k[0],callee))
            if peer is not None:
                peer['callers'].append(k[1])
    # Unique exact nontrivial bodies are candidate relationships, never semantic proof.
    grouped = {r:defaultdict(list) for r in REGIONS}
    for row in rows:
        if row['size'] >= 32 and row['original_sha256'] and row['owner']:
            grouped[row['region']][row['owner'],row['size'],row['original_sha256']].append(row)
    for h, us in grouped['usa'].items():
        jp = grouped['japan_0'].get(h, [])
        if len(us) == len(jp) == 1:
            for a,b in ((us[0],jp[0]),(jp[0],us[0])):
                a['counterpart_candidate'] = {'region':b['region'],'name':b['name'],
                    'evidence':'Unique among accepted bodies in the same logical file of equal size and stored original digest; data and relocation equivalence unverified.'}
    apply_annotations(index, read(root/'semantics/annotations.json'), root)
    return sorted(rows, key=lambda r:(r['region'], r['rom_offset'],r['name']))


def apply_annotations(index, annotations, root):
    require(annotations['format'] == 'goemon-semantic-annotations-v1', 'annotation format')
    seen = set()
    fields = set()
    for structure in annotations.get('structures', []):
        refs = structure['evidence']
        require(refs and all((root/p).is_file() for p in refs), 'missing structure evidence')
        for field in structure['fields']:
            key = structure['id'] + '.+' + field['offset']
            require(key not in fields and field['confidence'] in LEVELS and number(field['offset']) >= 0, 'invalid field '+key)
            fields.add(key)
    for group in annotations['groups']:
        refs = group['evidence']
        require(refs and all((root/p).is_file() for p in refs), 'missing annotation evidence')
        for entry in group['functions']:
            keys = [(region, entry[region]) for region in REGIONS if entry.get(region)]
            require(keys and all(k in index and k not in seen for k in keys), 'stale/duplicate annotation '+str(keys))
            require(entry['confidence'] in LEVELS and entry['confidence'] != 'Unknown' and entry['behavior'], 'invalid classification')
            require(all(f in fields for f in entry.get('fields',[])), 'unknown structure field')
            for k in keys:
                row = index[k]; seen.add(k)
                row.update(confidence=entry['confidence'], behavior=entry['behavior'], subsystem=group['subsystem'],
                           semantic_alias=entry.get('alias'), gameplay_role=entry.get('gameplay_role'), fields=entry.get('fields',[]), evidence=refs, review_method='manual',
                           unresolved=entry.get('unresolved','Exact wider gameplay role not established.'))
                if len(keys) == 2:
                    peer = keys[1] if k == keys[0] else keys[0]
                    row['counterpart'] = {'region':peer[0], 'name':peer[1], 'evidence':refs,
                                          'regional_difference':entry.get('regional_difference')}


def summary(rows):
    return {r:{'functions':len(rs), 'bytes':sum(x['size'] for x in rs),
               'confidence':{c:sum(x['confidence']==c for x in rs) for c in LEVELS},
               'manually_reviewed':sum(x['review_method']=='manual' for x in rs),
               'source_resolved':sum(x['source'] is not None for x in rs),
               'callers_with_named_calls':sum(bool(x['callees']) for x in rs),
               'reviewed_counterparts':sum(x['counterpart'] is not None for x in rs),
               'digest_candidates':sum(x['counterpart_candidate'] is not None for x in rs)}
            for r in REGIONS for rs in [[x for x in rows if x['region']==r]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,help='Write complete generated JSON index (outside canonical proof files)')
    args = parser.parse_args()
    rows = build()
    stats = summary(rows)
    if args.output:
        args.output.write_text(json.dumps({'format':'goemon-semantic-inventory-v1','summary':stats,'structures':read(ROOT/'semantics/annotations.json')['structures'],'functions':rows},indent=2)+'\n')
    print(json.dumps(stats,indent=2))


if __name__ == '__main__':
    main()
