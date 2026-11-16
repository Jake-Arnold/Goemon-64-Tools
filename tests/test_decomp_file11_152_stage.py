"""ROM-free fail-closed tests for eight opt-in USA file_11 C promotions."""
from __future__ import annotations

from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from decomp import file11_144_stage as old, file11_152_stage as new, verify

ROOT = Path(__file__).resolve().parents[1] / 'decomp'
EXPECTED = {
    0x59EB80: ('func_801E2C70_59EB80',),
    0x59EE00: ('func_801E2EF0_59EE00', 'func_801E2F14_59EE24', 'func_801E2F38_59EE48'),
    0x5B22C8: ('func_801F63B8_5B22C8', 'func_801F63E0_5B22F0'),
    0x5B84A0: ('func_801FC590_5B84A0', 'func_801FC5C0_5B84D0'),
}


class File11152StageTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / 'manifest.json').read_text())
        self.fixture = new.load_fixture()
        self.old_fixture = old.load_fixture()

    def test_claim_count_original_function_extents_and_ownership(self):
        self.assertEqual(verify.file11_stage_mode(self.manifest), 152)
        claims = verify.claimed_functions(self.manifest)
        self.assertEqual(len(claims), 315)
        self.assertEqual(len({f['name'] for f in claims}), 315)
        self.assertEqual(sum(f['size'] for f in claims), 16_660)
        self.assertEqual(len(new.entries()), 152)
        self.assertEqual(sum(f['size'] for f in new.entries()), 4276)
        stage = new.reviewed_plan(self.manifest)
        self.assertEqual((stage['c_units'], stage['asm_slices'], stage['chunks']), (49, 39, 88))
        self.assertEqual(len(stage['ordered_segments']), 88)

    def test_exactly_four_previous_assembly_slices_changed(self):
        old_chunks, now_chunks = self.old_fixture['chunks'], self.fixture['chunks']
        changed = [(a,b) for a,b in zip(old_chunks,now_chunks) if a != b]
        self.assertEqual([a['rom_start'] for a,b in changed], list(EXPECTED))
        self.assertEqual(sum(a['size'] for a,b in changed), 316)
        for old_chunk, new_chunk in changed:
            self.assertEqual(old_chunk['kind'], 'asm')
            self.assertEqual(new_chunk['kind'], 'c')
            self.assertEqual(new_chunk['original_sha256'], old_chunk['original_sha256'])
            self.assertEqual(tuple(f['name'] for f in new_chunk['functions']),
                             EXPECTED[old_chunk['rom_start']])
            self.assertEqual(hashlib.sha256(new_chunk['source'].encode()).hexdigest(),
                             new_chunk['source_sha256'])
            self.assertNotIn('GLOBAL_ASM', new_chunk['source'])
            self.assertNotIn('#include', new_chunk['source'])
            self.assertRegex(new_chunk['trimmed_obj_sha256'], r'^[0-9a-f]{64}$')

    def test_object_targets_are_unique_and_original_overlay_unchanged(self):
        objects = new.source_objects()
        self.assertEqual(len(objects), 88)
        self.assertEqual(len(set(str(f) for f,_,_ in objects)), 88)
        self.assertEqual(Counter(c['kind'] for _,_,c in objects), {'c':49,'asm':39})
        self.assertEqual(new.NORMALIZED_NOP_ALIAS_ASM_OFFSETS,
                         frozenset((0x5995E8, 0x59D4DC, 0x5AEBDC)))

    def test_opt_in_refuses_previous_stage_or_altered_fixture(self):
        previous = copy.deepcopy(self.manifest)
        previous['overlay_file11_stage'] = {'format': old.STAGE_FORMAT}
        self.assertEqual(len(verify.claimed_functions(previous)),307)
        with self.assertRaisesRegex(ValueError, 'opted-in'):
            new.reviewed_plan(previous)
        wrong = copy.deepcopy(self.manifest)
        wrong['overlay_file11_stage']['format'] = 'unreviewed'
        with self.assertRaises(ValueError):
            verify.file11_stage_mode(wrong)

    def test_fail_closed_on_unreviewed_source_and_hash(self):
        original = new.load_fixture
        try:
            bad = copy.deepcopy(self.fixture)
            target = next(c for c in bad['chunks'] if c.get('name') == 'file11_wave7_59ee00')
            target['source'] += '\nvoid extra(void) {}\n'
            new.load_fixture = lambda:bad
            with self.assertRaisesRegex(ValueError, 'Unexpected file11 C replacement'):
                new.reviewed_plan(self.manifest)
        finally:
            new.load_fixture = original

    def test_refuse_unsafe_destination_overwrite(self):
        plan = new.reviewed_plan(self.manifest)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            dest=root/'src/file11_wave7_59ee00.c'
            dest.parent.mkdir(parents=True)
            dest.write_text('existing')
            with self.assertRaises(FileExistsError):
                new.source_payloads(root,plan)

    def test_source_manifest_rom_hash_contract(self):
        self.assertEqual(self.fixture['original_rom_sha1'],
                         '6ea0ed71032ce08fc2745f412d84936382197494')
        self.assertEqual(self.fixture['file11_relocations'], 8825)
        self.assertEqual(self.fixture['overlay_text_start'], 0x587370)
        self.assertEqual(self.fixture['overlay_text_end'], 0x5B8500)
        self.assertEqual(self.fixture['all_C_text_bytes'], 4276)


if __name__ == '__main__':
    unittest.main()
