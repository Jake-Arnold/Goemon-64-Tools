"""Count identified function entries in checksum-verified pinned build outputs.

Zero-sized jump labels and data markers are not functions in this inventory.
Overlay entries with the same guest address remain distinct named entries.
This is a count of identified ELF entries, not proof of complete discovery or
of how much deliberately handwritten SDK/runtime assembly should become C.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from .verify import load_manifest, claimed_functions


def parse_inventory_symbols(text):
    functions = {}
    markers = set()
    for line in text.splitlines():
        parts = line.split()
        if len(parts) != 8 or not parts[0].rstrip(':').isdigit():
            continue
        _, value, size, kind, binding, visibility, section, name = parts
        if section in ('UND', 'ABS'):
            continue
        if kind == 'OBJECT' and name.endswith('.NON_MATCHING'):
            markers.add(name[:-len('.NON_MATCHING')])
        if kind != 'FUNC':
            continue
        entry = dict(address=int(value, 16), size=int(size, 16 if size.startswith('0x') else 10), section=section)
        if name in functions and functions[name] != entry:
            raise ValueError('Ambiguous function symbol: ' + name)
        functions[name] = entry
    if not functions:
        raise ValueError('No defined function symbols')
    return functions, markers


def summarize_inventory(baseline_text, candidate_text, claimed_names):
    base_all, base_markers = parse_inventory_symbols(baseline_text)
    candidate_all, candidate_markers = parse_inventory_symbols(candidate_text)
    base = {name: row for name, row in base_all.items() if row['size'] > 0}
    candidate = {name: row for name, row in candidate_all.items() if row['size'] > 0}
    if not base or set(base) != set(candidate):
        raise ValueError('Positive-sized function inventory changed')
    size_annotations = []
    for name, row in base.items():
        other = candidate[name]
        if row['address'] != other['address']:
            raise ValueError('Function entry address changed: ' + name)
        if row['size'] != other['size']:
            size_annotations.append(dict(name=name, baseline_size=row['size'], candidate_size=other['size']))
    upstream = set(base) - base_markers
    current = set(base) - candidate_markers
    if not upstream <= current:
        raise ValueError('Upstream matching status regressed')
    claimed = set(claimed_names)
    if current - upstream != claimed:
        raise ValueError('New unmarked functions disagree with manifest claims')
    aliases = Counter((row['section'], row['address'], row['size']) for row in base.values())
    identity = [(name, base[name]['address'], base[name]['size']) for name in sorted(base)]
    return dict(
        identified_function_entries=len(base),
        upstream_unmarked_entries=len(upstream),
        newly_matching_c=len(claimed),
        current_unmarked_entries=len(current),
        remaining_assembly_entries=len(base)-len(current),
        baseline_zero_sized_function_labels_ignored=len(base_all)-len(base),
        candidate_zero_sized_function_labels_ignored=len(candidate_all)-len(candidate),
        extra_positive_alias_entries=sum(count-1 for count in aliases.values() if count > 1),
        upstream_unmarked_names=sorted(upstream),
        size_annotation_differences=sorted(size_annotations, key=lambda row: row['name']),
        function_entry_identity_sha256=hashlib.sha256(json.dumps(identity, separators=(',', ':')).encode()).hexdigest(),
    )


def collect_inventory(baseline, candidate, manifest):
    baseline, candidate = Path(baseline), Path(candidate)
    readelf = shutil.which('mips-linux-gnu-readelf')
    if readelf is None:
        raise ValueError('MIPS readelf is required; run inside the build environment')
    images = []
    elfs = []
    symbol_text = []
    for checkout in (baseline, candidate):
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout, text=True).strip()
        if revision != manifest['upstream_commit']:
            raise ValueError('Build checkout is not pinned upstream')
        data = (checkout/'build/usa/mnsg.z64').read_bytes()
        if hashlib.sha1(data).hexdigest() != manifest['decompressed_sha1']:
            raise ValueError('Build output does not match reference ROM identity')
        images.append(data)
        elf = checkout/'build/usa/mnsg.elf'
        elfs.append(hashlib.sha256(elf.read_bytes()).hexdigest())
        symbol_text.append(subprocess.check_output([readelf, '-Ws', str(elf)], text=True))
    if images[0] != images[1]:
        raise ValueError('Baseline and candidate images differ')
    claimed = [fn['name'] for fn in claimed_functions(manifest)]
    result = summarize_inventory(*symbol_text, claimed)
    return dict(format='goemon-function-inventory-v1', upstream_commit=manifest['upstream_commit'],
                decompressed_sha1=manifest['decompressed_sha1'], baseline_elf_sha256=elfs[0],
                candidate_elf_sha256=elfs[1],
                inventory_tool_sha256_lf=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
                summary=result)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True, help='New metadata report, never overwritten')
    args = parser.parse_args(argv)
    manifest = load_manifest(Path(__file__).with_name('manifest.json'))
    result = collect_inventory(args.baseline, args.candidate, manifest)
    with args.report.open('x', encoding='utf-8') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
