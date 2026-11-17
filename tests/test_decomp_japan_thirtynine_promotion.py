"""Japanese 34 -> 39 original-address staging guardrails, no ROM or private toolchain."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

from decomp import japan_thirtynine_c as current
from decomp import japan_thirtyfour_c as historic
from decomp.japan_relocation_policy import REVIEWED

ROOT=Path(__file__).resolve().parents[1]/'decomp'


class Japan39ProductionPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new=json.loads((ROOT/'regions/japan_0.json').read_text())
        cls.old=json.loads((ROOT/'regions/japan_0_34_preserved_20261117.json').read_text())
        cls.proof=json.loads((ROOT/'results/japan_0_39_native_combined_20261117.json').read_text())

    def test_preserves_all_old_original_addresses_and_adds_exactly_five(self):
        self.assertEqual(len(self.old['units']),30)
        self.assertEqual(len(self.new['units']),35)
        self.assertEqual(self.new['units'][:30],self.old['units'])
        added=self.new['units'][30:]
        self.assertEqual([(u['source'],u['rom_offset'],u['section_size']) for u in added],
            [('japan_matching/'+stem+'.c',offset,36) for stem,fn,offset in current.NEXT_FIVE])
        self.assertEqual([u['functions'][0]['name'] for u in added],
                         [name for stem,name,offset in current.NEXT_FIVE])
        self.assertEqual(len({u['rom_offset'] for u in added}),5)
        for u in added:
            path=ROOT/u['source']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),u['source_sha256'])
            self.assertEqual(u['functions'][0]['size'],36)
            self.assertIn(u['source'],REVIEWED)
        self.assertEqual(self.proof['status'],'PASS')
        self.assertEqual((self.proof['functions'],self.proof['matching_c_bytes']),(39,2092))
        self.assertEqual(self.proof['expanded_rom']['different_bytes'],0)
        self.assertEqual(self.proof['retail_rom']['different_bytes'],0)

    def test_splat_extension_is_precisely_one_original_section(self):
        original='original header\n'+current.OLD+'\nend\n'
        # The full prior 34-C stage requires the original header from a real
        # Splat config. Check the exact extension contract independently.
        self.assertEqual(len(current.NEXT_FIVE),5)
        self.assertEqual(len({x[0] for x in current.NEXT_FIVE}),5)
        self.assertIn('[0x3A7F4, asm, main_3A7F4]',current.NEW)
        self.assertIn('[0x3AA58, asm, main_3AA58]',current.NEW)
        self.assertIn('[0x3AABC, asm, main_3AABC]',current.NEW)
        self.assertEqual(current.NEW.count(', c,'),5)
        self.assertEqual(len(current.SOURCE_NAMES),len(historic.SOURCE_NAMES)+5)

    def test_new_rom_and_elf_fingerprints_are_bound_to_history(self):
        self.assertEqual(self.new['proven_original_elf_function_identities_sha256'],
                         '3a6e6bafd6818d5734d6880bb0a67a32bea2bbc26905778533d2a15707718d21')
        self.assertEqual(self.new['proven_original_semantic_relocations_sha256'],
                         'e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20')
        self.assertEqual(self.new['original_elf_positive_function_count'],7376)
        self.assertEqual(self.new['original_elf_relocation_count'],80747)
        self.assertEqual(self.new['historical_34_manifest'],'regions/japan_0_34_preserved_20261117.json')

if __name__=='__main__': unittest.main()
