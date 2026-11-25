import json
import unittest
import shutil
import subprocess
from practice.pj64_frame_control import controller_input, export_script, parse_inputs

class FrameTests(unittest.TestCase):
    def test_timeline(self):
        base=controller_input(['A'],0,0)
        self.assertEqual(parse_inputs('2 Z+B -80 80\n3 - 0 0',3,base),[base,{'buttons':0x6000,'x':-80,'y':80},{'buttons':0,'x':0,'y':0}])
        for text in ('0 A 0 0','1 A 0 0\n1 B 0 0','2 X 0 0','2 A 81 0','4 A 0 0'):
            with self.assertRaises(ValueError):parse_inputs(text,3,base)
    def test_script(self):
        s=export_script('japan',47651,'a'*32,'80001000')
        self.assertNotIn('__GOEMON_CONFIG__',s)
        config=json.loads(s.split('var config = ',1)[1].split(';',1)[0])
        self.assertEqual(config['crc1'],0x832C168B)
        self.assertEqual(config['pc'],0x80001000)
        for pc in ('80001001','A4000000'):
            with self.assertRaises(ValueError):export_script('usa',47651,'a'*32,pc)
        with self.assertRaises(ValueError):export_script('usa',47651,'bad')

    @unittest.skipUnless(shutil.which("node"), "Node.js required for script API mock")
    def test_bridge_mock(self):
        subprocess.run(["node", "tests/pj64_frame_bridge_mock.js"], check=True)
