import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from practice.native_trace_wire import PREFIX, TraceReader, TraceWriter, checkpoint


class NativeTraceWireTests(unittest.TestCase):
    def test_large_trace_delta_reset_and_unchanged_poll(self):
        stream = io.StringIO(); sender = TraceWriter(stream); receiver = TraceReader()
        rows = [dict(serial=i, **{f'w{j}': i / 3 for j in range(24)}) for i in range(3600)]
        report = dict(rows=rows[:600], watches=[dict(name='a')], state=3)
        def transfer(report):
            sender.send(dict(ok=True, report=report))
            records = stream.getvalue().splitlines(); stream.seek(0); stream.truncate(0)
            outputs = [v for line in records if (v := receiver.receive(line)) is not None]
            self.assertEqual(outputs, [dict(ok=True, report=report)])
            return records
        first = transfer(report); self.assertGreater(len(first), 3)
        self.assertEqual(len(transfer(report)), 2)
        report = dict(report, rows=rows); self.assertEqual(len(transfer(report)), 96)
        self.assertEqual(len(transfer(report)), 2)
        self.assertEqual(len(transfer(dict(report, rows=[]))), 2)
        self.assertEqual(receiver.rows, [])
        self.assertEqual(len(transfer(dict(report, rows=rows[:1], watches=[dict(name='b')]))), 3)
    def test_incomplete_or_corrupt_packet_is_explicit(self):
        stream = io.StringIO(); TraceWriter(stream).send(dict(ok=True,report=dict(rows=[dict(a=1)], watches=[])))
        a,b,c=stream.getvalue().splitlines(); reader=TraceReader();reader.receive(a)
        with self.assertRaisesRegex(ValueError,'Incomplete'):reader.receive(c)
        with self.assertRaises(ValueError):TraceReader().receive('native log')
        with self.assertRaises(ValueError):TraceReader().receive(PREFIX+'{')
    def test_real_subprocess_native_stdout_and_stderr_are_not_protocol(self):
        script = """import ctypes, os, sys
from practice.native_trace_wire import private_stdout, TraceWriter
w=TraceWriter(private_stdout())
os.write(1,b'native partial log')
os.write(2,b' stderr log\\n')
ctypes.CDLL(None).puts(b'C printf log')
print('Python log',flush=True)
w.send(dict(ok=True,report=dict(rows=[dict(n=i) for i in range(600)],watches=[])))
"""
        p=subprocess.run([sys.executable,'-c',script],capture_output=True,text=True,check=True,timeout=10)
        r=TraceReader(); outputs=[v for line in p.stdout.splitlines() if (v:=r.receive(line)) is not None]
        self.assertEqual(len(outputs[0]['report']['rows']),600)
        for message in ('native partial log','stderr log','C printf log','Python log'):
            self.assertIn(message,p.stderr);self.assertNotIn(message,p.stdout)
    def test_recovery_preserves_previous_snapshot_on_failed_write(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'research-traces'/'test.json';good=dict(rows=[dict(frame=1)],watches=[])
            checkpoint(p,good)
            with self.assertRaises(ValueError):checkpoint(p,dict(rows=[dict(frame=float('nan'))]))
            self.assertEqual(json.loads(p.read_text()),good)
            self.assertEqual(list(p.parent.iterdir()),[p])

if __name__=='__main__':unittest.main()
