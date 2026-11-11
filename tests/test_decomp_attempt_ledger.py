import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from decomp.attempt_ledger import (
    attempt_signature,
    import_legacy_report_bytes,
    input_signature,
    make_attempt_record,
    validate_attempt_record,
)
from decomp.batch import Queue, verified_rom_offset


def queued_function(name='func_80000004_10', size=8):
    return {
        'name': name,
        'address': 0x80000004,
        'size': size,
        'section': '.main',
        'source': 'asm/usa/unit.s',
        'asm': 'glabel ' + name + '\nendlabel ' + name + '\n',
        'expected': b'\x11' * size,
        'verified': 0,
        'rom_offset': None,
    }


def identity():
    return {
        'upstream_commit': 'a' * 40,
        'retail_sha1': 'b' * 40,
        'rom_sha1': 'c' * 40,
        'elf_sha256': 'd' * 64,
    }


def recipe():
    return {
        'context_sha256': '1' * 64,
        'ido_toolchain_sha256': '2' * 64,
        'm2c_pin': 'e' * 40,
        'python_version': 'Python 3.test',
        'python_sha256': '3' * 64,
        'dependency_lock_sha256': '4' * 64,
        'binutils': {'as': '5' * 64},
        'flags': ['-O2'],
        'source_hashes': {'batch.py': '6' * 64, 'probe.py': '7' * 64},
        'search_seconds': 0,
    }


class AttemptRecordTests(unittest.TestCase):
    def record(self, status='mismatch'):
        fn = queued_function()
        sig = input_signature(fn, identity(), recipe())
        comparison = {
            'actual_sha256': '8' * 64,
            'first_mismatch_offset': 4,
            'word_mismatch_offsets': [4],
        }
        result = {
            'status': status,
            'candidate_sha256': '9' * 64,
            'comparison': comparison if status in ('mismatch', 'linked_match') else {},
            'reason': 'code_size',
        }
        return make_attempt_record(fn, identity(), recipe(), result, sig, 1, 'a' * 64)

    def test_schema_requires_complete_original_identity_and_extent(self):
        record = self.record()
        self.assertEqual(validate_attempt_record(record), [])
        del record['original']['rom_sha1']
        errors = validate_attempt_record(record)
        self.assertTrue(any('original ROM identity' in error for error in errors))

    def test_isolated_match_cannot_claim_full_rom_proof(self):
        record = self.record('linked_match')
        self.assertEqual(record['exactness_tier'], 'isolated_function')
        record['proof_run']['full_rom_match'] = True
        errors = validate_attempt_record(record)
        self.assertTrue(any('conflated with full-ROM proof' in error for error in errors))

    def test_full_rom_tier_requires_rom_manifest_inventory_and_report_binding(self):
        record = self.record('linked_match')
        record['exactness_tier'] = 'full_rom'
        record['proof_run'].update(
            tier='full_rom', scope='full_rom', full_rom_match=True,
            report_sha256='a' * 64, rom_sha1='f' * 40,
        )
        signature = attempt_signature(record)
        record['attempt_signature'] = signature
        record['record_id'] = 'sha256:' + signature
        errors = validate_attempt_record(record)
        self.assertTrue(any('original ROM' in error for error in errors))
        self.assertTrue(any('manifest_sha256' in error for error in errors))
        self.assertTrue(any('inventory_sha256' in error for error in errors))

    def test_signature_covers_mismatch_and_failed_words(self):
        record = self.record()
        self.assertEqual(record['comparison']['first_mismatch'],
                         {'offset': 4, 'address': 0x80000008})
        self.assertEqual(record['comparison']['failed_word_offsets'], [4])
        record['comparison']['failed_word_offsets'] = [8]
        self.assertTrue(any('signature does not match' in error
                            for error in validate_attempt_record(record)))

    def test_input_signature_ignores_total_budget_but_tracks_search_budget(self):
        fn = queued_function()
        first = recipe()
        first['search_seconds'] = 2
        second = dict(first, seconds=90)
        self.assertEqual(input_signature(fn, identity(), first),
                         input_signature(fn, identity(), second))
        second['search_seconds'] = 4
        self.assertNotEqual(input_signature(fn, identity(), first),
                            input_signature(fn, identity(), second))
        second['context_sha256'] = 'f' * 64
        self.assertNotEqual(input_signature(fn, identity(), first),
                            input_signature(fn, identity(), second))

    def test_legacy_import_preserves_historical_claim_boundary(self):
        report = {
            'format': 'goemon-batch-report-v1',
            'baseline': {'rom_sha1': 'c' * 40},
            'linked_probe_matches': [{
                'name': 'func_80000004_10', 'size': 8,
                'source_sha256': '9' * 64, 'code_sha256': '8' * 64,
            }],
            'newly_verified_full_rom_functions': 0,
        }
        raw = json.dumps(report, sort_keys=True).encode()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'historical.json'
            path.write_bytes(raw)
            before = path.read_bytes()
            imported = import_legacy_report_bytes(before)
            self.assertEqual(path.read_bytes(), before)
        self.assertEqual(imported['source_report_sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual(imported['candidate_summaries'][0]['original_provenance'], 'INCOMPLETE')
        self.assertIsNone(imported['candidate_summaries'][0]['attempt_signature'])
        self.assertEqual(imported['newly_verified_full_rom_functions'], 0)

    def test_legacy_import_rejects_full_rom_promotion_claim(self):
        report = {
            'format': 'goemon-batch-report-v1',
            'linked_probe_matches': [],
            'newly_verified_full_rom_functions': 1,
        }
        with self.assertRaisesRegex(ValueError, 'promotion count'):
            import_legacy_report_bytes(json.dumps(report).encode())


class QueueLedgerTests(unittest.TestCase):
    def test_legacy_cache_migrates_additively_without_rewriting_attempts(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'old.sqlite'
            db = sqlite3.connect(path)
            db.executescript('''
                CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE functions(name TEXT PRIMARY KEY, address INTEGER NOT NULL, size INTEGER NOT NULL,
                    section TEXT NOT NULL, source TEXT NOT NULL, asm TEXT NOT NULL, expected BLOB NOT NULL,
                    verified INTEGER NOT NULL);
                CREATE TABLE runs(id INTEGER PRIMARY KEY, recipe TEXT NOT NULL, started TEXT NOT NULL,
                    ended TEXT, configuration TEXT NOT NULL, selected INTEGER NOT NULL, elapsed REAL);
                CREATE TABLE attempts(id INTEGER PRIMARY KEY, name TEXT NOT NULL REFERENCES functions(name),
                    recipe TEXT NOT NULL, ordinal INTEGER NOT NULL, status TEXT NOT NULL, started TEXT NOT NULL,
                    ended TEXT, result TEXT, UNIQUE(name, recipe, ordinal));
                INSERT INTO functions VALUES ('first', 2147483652, 8, '.main', 'asm/usa/unit.s', '', x'1111111111111111', 0);
                INSERT INTO attempts(name,recipe,ordinal,status,started,result)
                    VALUES ('first','old-recipe',1,'mismatch','old-time','{"status":"mismatch"}');
            ''')
            db.commit()
            db.close()
            queue = Queue(path)
            try:
                function_columns = {row['name'] for row in queue.db.execute('PRAGMA table_info(functions)')}
                attempt_columns = {row['name'] for row in queue.db.execute('PRAGMA table_info(attempts)')}
                self.assertIn('rom_offset', function_columns)
                self.assertIn('input_signature', attempt_columns)
                self.assertIn('run_id', attempt_columns)
                old = queue.db.execute('SELECT * FROM attempts').fetchone()
                self.assertEqual(old['result'], '{"status":"mismatch"}')
                self.assertIsNone(old['input_signature'])
            finally:
                queue.close()

    def test_cross_recipe_dedup_skips_same_failed_input_but_retry_overrides(self):
        with tempfile.TemporaryDirectory() as folder:
            queue = Queue(Path(folder) / 'queue.sqlite')
            try:
                queue.register(identity(), [queued_function('first'), queued_function('second')])
                sig = 'a' * 64
                ident = queue.claim('first', 'recipe-one', sig)
                queue.finish(ident, {'status': 'mismatch'})
                signatures = {'first': sig, 'second': 'b' * 64}
                selected = queue.select('recipe-two', 10, 64, scope='all',
                                        input_signatures=signatures)
                self.assertEqual([fn['name'] for fn in selected], ['second'])
                retried = queue.select('recipe-two', 10, 64, scope='all', retry=True,
                                       input_signatures=signatures)
                self.assertEqual([fn['name'] for fn in retried], ['first', 'second'])
            finally:
                queue.close()

    def test_report_contains_signed_attempts_without_promoting_them(self):
        from decomp.batch import report_cache
        with tempfile.TemporaryDirectory() as folder:
            queue = Queue(Path(folder) / 'queue.sqlite')
            try:
                fn = queued_function('first')
                queue.register(identity(), [fn])
                recipe_data = recipe()
                sig = input_signature(fn, identity(), recipe_data)
                record = make_attempt_record(fn, identity(), recipe_data, {
                    'status': 'linked_match', 'candidate_sha256': '9' * 64,
                    'comparison': {'actual_sha256': '8' * 64, 'first_mismatch_offset': None,
                                   'word_mismatch_offsets': []},
                }, sig, 1, 'a' * 64)
                ident = queue.claim('first', 'a' * 64, sig, 1)
                queue.finish(ident, {
                    'status': 'linked_match', 'size': 8, 'candidate_sha256': '9' * 64,
                    'comparison': {'actual_sha256': '8' * 64},
                }, record)
                result = report_cache(queue, 'a' * 64)
                self.assertEqual(len(result['attempt_ledger']['records']), 1)
                self.assertFalse(result['attempt_ledger']['records'][0]['proof_run']['full_rom_match'])
                self.assertEqual(result['newly_verified_full_rom_functions'], 0)
            finally:
                queue.close()


class RomOffsetTests(unittest.TestCase):
    def test_encoded_offset_requires_original_rom_byte_confirmation(self):
        name = 'func_80000004_10'
        self.assertEqual(verified_rom_offset(name, b'ABCD', b'\0' * 16 + b'ABCD'), 16)
        self.assertIsNone(verified_rom_offset(name, b'ABCE', b'\0' * 16 + b'ABCD'))
        self.assertIsNone(verified_rom_offset('named_function', b'ABCD', b'\0' * 16 + b'ABCD'))


if __name__ == '__main__':
    unittest.main()
