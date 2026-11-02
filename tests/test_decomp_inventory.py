import unittest
import hashlib
import json
from pathlib import Path
from decomp.verify import load_manifest
from decomp.inventory import parse_inventory_symbols, summarize_inventory


def row(number, name, address='80001000', size=16, kind='FUNC', section='2'):
    return f'{number}: {address} {size} {kind} GLOBAL DEFAULT {section} {name}\n'


def example():
    # Two distinct overlays deliberately use the same guest address and size.
    base = row(1, 'upstream')+row(2, 'new', section='3')+row(3, 'pending', section='4')
    base += row(4, 'new.NON_MATCHING', kind='OBJECT')+row(5, 'pending.NON_MATCHING', kind='OBJECT')
    candidate = row(1, 'upstream')+row(2, 'new', section='3')+row(3, 'pending', section='4')
    candidate += row(4, 'pending.NON_MATCHING', kind='OBJECT')
    candidate += row(5, '.Lcase', size=0)+row(6, 'table', kind='OBJECT')+row(7, 'table.NON_MATCHING', kind='OBJECT')
    return base, candidate


class FunctionInventoryTests(unittest.TestCase):
    def test_counts_functions_not_data_or_exported_jump_labels(self):
        baseline, candidate = example()
        result = summarize_inventory(baseline, candidate, ['new'])
        self.assertEqual(result['identified_function_entries'], 3)
        self.assertEqual(result['upstream_unmarked_entries'], 1)
        self.assertEqual(result['newly_matching_c'], 1)
        self.assertEqual(result['current_unmarked_entries'], 2)
        self.assertEqual(result['remaining_assembly_entries'], 1)
        self.assertEqual(result['candidate_zero_sized_function_labels_ignored'], 1)
        self.assertEqual(result['extra_positive_alias_entries'], 0)
        self.assertEqual(result['upstream_unmarked_names'], ['upstream'])

    def test_rejects_unsupported_promotions_regressions_and_inventory_drift(self):
        baseline, candidate = example()
        bad_cases = [
            (candidate, []),
            (candidate.replace(row(4, 'pending.NON_MATCHING', kind='OBJECT'), ''), ['new']),
            (candidate+row(8, 'upstream.NON_MATCHING', kind='OBJECT'), ['new']),
            (candidate.replace(row(2, 'new', section='3'), row(2, 'new', address='80001004', section='3')), ['new']),
            (candidate+row(9, 'unexpected'), ['new']),
        ]
        for changed, claimed in bad_cases:
            with self.subTest(changed=changed, claimed=claimed):
                with self.assertRaises(ValueError):summarize_inventory(baseline, changed, claimed)

    def test_undefined_absolute_and_conflicting_symbols(self):
        text = row(1, 'external', section='UND')+row(2, 'absolute', section='ABS')
        with self.assertRaisesRegex(ValueError, 'No defined'):parse_inventory_symbols(text)
        with self.assertRaisesRegex(ValueError, 'Ambiguous'):
            parse_inventory_symbols(row(1, 'same')+row(2, 'same', address='80001004'))
        parsed, markers = parse_inventory_symbols(row(1, 'one', size='0x10'))
        self.assertEqual(parsed['one']['size'], 16)
        self.assertEqual(markers, set())

    def test_size_annotation_changes_are_reported_without_inventing_functions(self):
        baseline, candidate = example()
        candidate = candidate.replace(row(3, 'pending', section='4'), row(3, 'pending', size=24, section='4'))
        result = summarize_inventory(baseline, candidate, ['new'])
        self.assertEqual(result['identified_function_entries'], 3)
        self.assertEqual(result['remaining_assembly_entries'], 1)
        self.assertEqual(result['size_annotation_differences'], [dict(name='pending', baseline_size=16, candidate_size=24)])

    def test_published_inventory_tracks_current_manifest_and_tool(self):
        root = Path(__file__).resolve().parents[1] / 'decomp'
        manifest = load_manifest(root / 'manifest.json')
        report = json.loads((root / 'results/inventory.json').read_text())
        summary = report['summary']
        claimed = {fn['name'] for unit in manifest['units'] for fn in unit['functions']}
        self.assertEqual(report['upstream_commit'], manifest['upstream_commit'])
        self.assertEqual(report['decompressed_sha1'], manifest['decompressed_sha1'])
        self.assertEqual(summary['newly_matching_c'], len(claimed))
        self.assertEqual(summary['current_unmarked_entries'], summary['upstream_unmarked_entries'] + len(claimed))
        self.assertEqual(summary['identified_function_entries'], summary['current_unmarked_entries'] + summary['remaining_assembly_entries'])
        self.assertTrue(set(summary['upstream_unmarked_names']).isdisjoint(claimed))
        source = (root / 'inventory.py').read_bytes().replace(b'\r\n', b'\n')
        self.assertEqual(report['inventory_tool_sha256_lf'], hashlib.sha256(source).hexdigest())
