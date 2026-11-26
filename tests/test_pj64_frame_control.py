import json
import unittest
import shutil
import subprocess
import tempfile
from pathlib import Path
from practice.pj64_frame_control import controller_input, export_script, parse_inputs, parse_watches, trace_rows, export_trace, append_trace, parse_trap

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

    def test_watches_and_recording(self):
        watches=parse_watches('byte u8 80001001\nhalf u16 80001002\nf f32 80001004','usa')
        with self.assertRaises(ValueError):parse_watches('step u8 80001001','usa')
        with self.assertRaises(ValueError):parse_watches('bad u16 80001001','usa')
        with self.assertRaises(ValueError):parse_watches('bad u32 80400000','usa')
        with self.assertRaises(ValueError):parse_trap('exec 80001000',0x80001000)
        with self.assertRaises(ValueError):parse_watches('\n'.join(f'w{i} u32 80001000' for i in range(13)),'usa')
        from unittest.mock import patch
        with patch('practice.pj64_frame_control.guest_address',return_value=0x80001000) as resolve:
            parse_watches('field u16 @us|jp','japan');resolve.assert_called_once_with('jp',region='japan',width=2)
        def row(step,phase,words):return dict(step=step,phase=phase,input=None,polls=0,words=words)
        words=[0x12345678,0x12345678,0x3F333333]
        status=dict(region='usa',mode='execution-hook',pc=0x80002000,watches=watches,trap=None,hit=None,error='',epoch=1,generation=2,batchGeneration=2,pending=False,trace=[row(0,'baseline',words),row(1,'update',words)])
        r=trace_rows(status)[0]
        self.assertEqual((r['byte'],r['half'],r['f']),(0x34,0x5678,'0.699999988'))
        capture=append_trace(None,status)
        self.assertEqual(append_trace(capture,status),capture)
        next_status=dict(status,generation=3,batchGeneration=3,trace=[row(1,'baseline',words),row(2,'update',words)])
        capture=append_trace(capture,next_status)
        self.assertEqual([r['step'] for r in capture['trace']],[0,1,2])
        with self.assertRaises(ValueError):append_trace(capture,dict(next_status,generation=4,batchGeneration=4,epoch=2))
        with tempfile.TemporaryDirectory() as d:
            j=Path(d)/'trace.json';c=Path(d)/'trace.csv'
            export_trace(j,capture);export_trace(c,capture)
            self.assertEqual(json.loads(j.read_text())['trace'],capture['trace'])
            self.assertIn('region,mode,pc,error,step,phase',c.read_text())
