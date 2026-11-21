"""ROM-free checks for original USA native task insertion modes."""
import unittest
from decomp import scheduler6_g2_promotion as stage

class SchedulerSixTests(unittest.TestCase):
    def test_immutable_sources_and_original_ranges(self):
        d=stage.fixture()
        self.assertEqual([(f['rom_offset'],f['size']) for f in d['functions']],[(0x3584C,56),(0x35884,56)])
        self.assertEqual(sum(f['size'] for f in d['functions']),112)

    def test_caller_links_and_distinct_modes(self):
        d=stage.fixture()
        for mode,f in enumerate(d['functions'],start=1):
            s=(stage.DIR/'sources'/f['source']).read_text()
            self.assertIn('func_80034CBC_358BC',s)
            self.assertIn('D_8016DAB4_16E6B4',s)
            self.assertIn(',task,'+str(mode)+',mask)',s)

    def test_function_signature_count(self):
        self.assertEqual(len(stage.fixture()['functions']),2)
        self.assertEqual(stage.SHA1,'6ea0ed71032ce08fc2745f412d84936382197494')

if __name__=='__main__':unittest.main()
