"""Fail-closed ROM-free source and current inventory checks for 2026-11-18 expansions.

These checks complement, but do not replace, native IDO / exact 32 MiB ROM
verification. No original MIPS code or ROM data is embedded in the tests.
"""
from collections import Counter
import copy
from pathlib import Path
import hashlib
import unittest

from decomp import (overlay_resource140, overlay_graphics5,
                    overlay_file18_53, overlay_callbacks10, overlay_main19)
from decomp.verify import load_manifest, claimed_functions

STAGES = (
    ('overlay_resource140_stage', overlay_resource140, 140, 2472),
    ('overlay_graphics5_stage', overlay_graphics5, 5, 284),
    ('overlay_file18_53_stage', overlay_file18_53, 53, 796),
    ('overlay_callbacks10_stage', overlay_callbacks10, 10, 152),
    ('overlay_main19_stage', overlay_main19, 19, 1012),
)


class ExpandedNativePromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = load_manifest(Path(__file__).with_name('manifest.json'))

    def test_each_stage_source_hash_and_original_function_identity(self):
        for key, module, count, size in STAGES:
            with self.subTest(stage=key):
                fixture = module.load_fixture()
                entries = (fixture['functions'] if key=='overlay_resource140_stage'
                           else module.functions(fixture))
                self.assertEqual(len(entries),count)
                self.assertEqual(sum(f['size'] for f in entries),size)
                self.assertEqual(len({f['rom_offset'] for f in entries}),count)
                self.assertEqual(len({f['name'] for f in entries}),count)
                if key=='overlay_resource140_stage':
                    sources = [(module.SOURCE_BASE/(f['name']+'.c'), f['source_sha256'])
                               for f in entries]
                else:
                    sources = [(module.SOURCE_BASE/(u['name']+'.c'),u['source_sha256'])
                               for u in fixture['units']]
                for path,expected in sources:
                    self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),expected)
                for f in entries:
                    self.assertEqual(int(f['name'].rsplit('_',1)[1],16),f['rom_offset'])
                    self.assertEqual(int(f['name'].split('_')[1],16),f['vma'])

    def test_five_stage_counts_and_no_overlapping_original_ranges(self):
        old={k:v for k,v in self.doc.items() if k not in ([x[0] for x in STAGES]+['overlay_tiny9_stage','overlay_micro2_stage','overlay_micro15_stage','overlay_micro20_stage','overlay_menu2_stage','overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage','overlay_checkpoint500_stage','overlay_rediscovery5_stage'])}
        baseline=claimed_functions(old)
        self.assertEqual((len(baseline),sum(f['size'] for f in baseline)),(1225,52028))
        current=claimed_functions({k:v for k,v in self.doc.items() if k not in ('overlay_tiny9_stage','overlay_micro2_stage','overlay_micro15_stage','overlay_micro20_stage','overlay_menu2_stage','overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage','overlay_checkpoint500_stage','overlay_rediscovery5_stage')})
        self.assertEqual((len(current),sum(f['size'] for f in current)),(1452,56744))
        self.assertEqual(len({f['name'] for f in current}),1452)
        spans=sorted((f['rom_offset'],f['rom_offset']+f['size']) for f in current)
        self.assertTrue(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])))
        extras={f['name'] for f in current}-{f['name'] for f in baseline}
        self.assertEqual(len(extras),227)

    def test_wrong_stage_contract_fails_closed(self):
        for key,module,_,_ in STAGES:
            with self.subTest(stage=key):
                doc=copy.deepcopy(self.doc)
                doc[key]['format']='unverified-experimental-v2'
                with self.assertRaises(ValueError):claimed_functions(doc)

    def test_invalid_original_rom_rejected_without_any_native_build(self):
        for key,module,_,_ in STAGES:
            with self.subTest(stage=key):
                with self.assertRaises(ValueError):
                    module.validate_sources(b'not-the-authenticated-original-rom',module.load_fixture())

    def test_main19_relocation_comparator_requires_full_semantic_identity(self):
        # The original linker permits same-symbol HI16 rows to appear in a
        # different order after a TU split; the multiset and final ROM must
        # still match exactly. A missing site/changed symbol is not allowed.
        before=[('HI16',0x100,'symbol'),('HI16',0x104,'symbol')]
        after=list(reversed(before))
        self.assertEqual(Counter(before),Counter(after))
        self.assertNotEqual(Counter(before),Counter(after[:-1]))


if __name__=='__main__':unittest.main()
