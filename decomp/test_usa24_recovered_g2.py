"""Provenance, deduplication and complete 51 original-USA C-count guards."""
import unittest
from decomp import usa_crossregion51_recovered27_g2_promotion as r27
from decomp import usa_crossregion51_extra5_g2_promotion as e5
from decomp import usa_crossregion51_recovered19_g2_promotion as r19

class Remaining51OriginalG2Tests(unittest.TestCase):
 def test_24_source_integrity(self):
  e5.fixture();r19.fixture()
 def test_dedup_51_total(self):
  groups=[r27.fixture()['functions'],e5.fixture()['functions'],r19.fixture()['functions']]
  all_functions=[x for group in groups for x in group]
  self.assertEqual([len(x) for x in groups],[27,5,19])
  self.assertEqual(len({f['name'] for f in all_functions}),51)
  self.assertEqual(len({f['rom_offset'] for f in all_functions}),51)
  self.assertEqual(sum(f['size'] for f in all_functions),3864)
  self.assertEqual(sum(len(f['original_symbolic_relocations']) for f in all_functions),81)
  self.assertEqual(sum(f['size'] for f in groups[2]),1596)
 def test_original_offset_identity(self):
  for f in e5.fixture()['functions']+r19.fixture()['functions']:
   self.assertEqual(int(f['name'].split('_')[-1],16),f['rom_offset'])
   self.assertEqual(int(f['name'].split('_')[1],16),f['vma'])
 def test_five_callback_relocations(self):
  f=e5.fixture()['functions']
  self.assertEqual(sorted(len(x['original_symbolic_relocations']) for x in f),[0,1,1,1,1])
 def test_float_setters_no_relocations(self):
  self.assertTrue(all(not f['original_symbolic_relocations'] for f in r19.fixture()['functions']))

if __name__=='__main__':unittest.main()
