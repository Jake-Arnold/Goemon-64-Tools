import json
import pathlib
import struct
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from autosplitter.bridge import find_pid
from autosplitter.memory import readable_spans
from autosplitter.memory import Rdram, SYS_POINTER_ADDR, SYS_EXPECTED_PTR, PLAYER_OBJECT_PTR_ADDR, PLAYER_TASK_PTR_ADDR, CHARACTER_ID_ADDR, LOADING_FLAG_ADDR, discover_rdram, RDRAM_SIZE
from autosplitter.engine import SplitEngine, make_route, segment_names, save_route, load_route

BASE=0x10000000

class FakeProcess:
    def __init__(self): self.mem=bytearray(0x800000)
    def read(self, addr, size):
        offset=addr-BASE
        if offset<0 or offset+size>len(self.mem): raise OSError("bad read")
        return bytes(self.mem[offset:offset+size])
    def write(self, addr, value):
        self.mem[addr-BASE:addr-BASE+len(value)]=value
    def regions(self):
        return [(BASE, len(self.mem))]

def write_u32(p,address,value):
    p.write(BASE+(address&0x1FFFFFFF),struct.pack('<I',value))
def write_u8(p,address,value):
    p.write(BASE+((address&0x1FFFFFFF)^3),bytes([value]))
def write_f32(p,address,value):
    p.write(BASE+(address&0x1FFFFFFF),struct.pack('<f',value))

class Tests(unittest.TestCase):
    def sample(self):
        p=FakeProcess()
        write_u32(p,SYS_POINTER_ADDR,SYS_EXPECTED_PTR)
        write_u32(p,PLAYER_OBJECT_PTR_ADDR,0x801A0000)
        write_u32(p,PLAYER_TASK_PTR_ADDR,0x801B0000)
        write_u32(p,CHARACTER_ID_ADDR,3)
        write_u8(p,LOADING_FLAG_ADDR,0)
        write_u8(p,0x801B0000+0xCC,4)
        for i,v in enumerate((125.25,-5.5,700.5)):
            write_f32(p,0x801A0000+8+i*4,v)
        return p

    def test_n64_pointer_and_position(self):
        p=self.sample(); r=Rdram(p,BASE)
        s=r.snapshot()
        self.assertEqual((s['x'],s['y'],s['z']),(125.25,-5.5,700.5))
        self.assertEqual(s['action'],4)
        self.assertEqual(s['character'],3)
        self.assertEqual(s['loading'],0)
        r.write_f32(0x801A0008,42.5)
        self.assertEqual(r.snapshot()['x'],42.5)

    def test_discovery_skips_false_system_pointer_match(self):
        p=self.sample()
        # False pointer appears first; the original scanner returned this fake base.
        p.write(BASE + (SYS_POINTER_ADDR & 0x1FFFFFFF) - 0x200,
                struct.pack("<I", SYS_EXPECTED_PTR))
        self.assertEqual(discover_rdram(p, "wordswapped"), (BASE,"wordswapped"))

    def test_project64_split_readable_pages(self):
        p=self.sample()
        # All segments are below the old scanner's minimum region size.
        p.regions=lambda: [(BASE+i,0x1000) for i in range(0,RDRAM_SIZE,0x1000)]
        self.assertEqual(discover_rdram(p), (BASE,'wordswapped'))

    def test_readable_spans_preserve_inaccessible_gaps(self):
        regions=[(BASE,0x1000),(BASE+0x1000,0x1000),(BASE+0x3000,0x1000)]
        self.assertEqual(list(readable_spans(regions)),[(BASE,0x2000),(BASE+0x3000,0x1000)])

    def test_discovery_signature_across_scan_chunk_boundary(self):
        p=self.sample()
        # Start scanning two bytes into RAM so the pointer crosses a chunk edge.
        start=BASE+(SYS_POINTER_ADDR&0xFFFFF)+2
        p.regions=lambda: [(start, RDRAM_SIZE-(start-BASE))]
        self.assertEqual(discover_rdram(p), (BASE,'wordswapped'))

    def test_process_selection_requires_unambiguous_target(self):
        processes=[SimpleNamespace(info={'pid':1,'name':'Goemon64Recompiled.exe'}),
                   SimpleNamespace(info={'pid':2,'name':'Project64.exe'}),
                   SimpleNamespace(info={'pid':3,'name':'OtherProject64.exe'})]
        with patch('psutil.process_iter',return_value=processes):
            self.assertEqual(find_pid('recomp'),1)
            self.assertEqual(find_pid('project64'),2)
            with self.assertRaisesRegex(RuntimeError,'Multiple matching'):
                find_pid()
        with patch('psutil.process_iter',return_value=processes[1:]):
            self.assertEqual(find_pid(),2)
        with patch('psutil.process_iter',return_value=[]):
            with self.assertRaisesRegex(RuntimeError,'not found'):
                find_pid()

    def test_character_and_loading_validation(self):
        p=self.sample()
        write_u32(p,CHARACTER_ID_ADDR, 80167552)
        with self.assertRaisesRegex(ValueError,"Invalid character"):
            Rdram(p,BASE).snapshot()
        write_u32(p,CHARACTER_ID_ADDR, 0)
        write_u8(p,LOADING_FLAG_ADDR, 200)
        with self.assertRaisesRegex(ValueError,"Invalid loading"):
            Rdram(p,BASE).snapshot()

    def test_discovery_autodetect_big_endian(self):
        p=FakeProcess()
        def put32(addr,value): p.write(BASE+(addr&0x1FFFFFFF),struct.pack('>I',value))
        put32(SYS_POINTER_ADDR,SYS_EXPECTED_PTR)
        put32(PLAYER_OBJECT_PTR_ADDR,0x801A0000)
        put32(PLAYER_TASK_PTR_ADDR,0x801B0000)
        put32(CHARACTER_ID_ADDR,2)
        p.write(BASE+(LOADING_FLAG_ADDR&0x1FFFFFFF),bytes([0]))
        for i,v in enumerate((12.5,34.0,-4.0)):
            p.write(BASE+0x1A0008+i*4, struct.pack('>f',v))
        p.write(BASE+0x1B00CC,bytes([5]))
        self.assertEqual(discover_rdram(p,"auto"),(BASE,"big"))

    def test_wrong_memory_rejected(self):
        p=FakeProcess()
        with self.assertRaises(ValueError): Rdram(p,BASE).snapshot()

    def test_trigger_requires_outside_while_running(self):
        route=make_route(['A','B'])
        for i in range(2):
            route['segments'][i]['trigger']={'type':'position_enter','x':float(i*200),'y':0.,'z':0.,'radius':10.}
        engine=SplitEngine(route)
        def frame(x): return {'x':x,'y':0.,'z':0.,'loading':0}
        self.assertIsNone(engine.update(frame(0),False))
        self.assertIsNone(engine.update(frame(0),True))
        self.assertIsNone(engine.update(frame(-30),True))
        self.assertIsNone(engine.update(frame(0),True))
        self.assertEqual(engine.update(frame(0),True).name,'A')
        self.assertIsNone(engine.update(frame(175),True))
        self.assertIsNone(engine.update(frame(200),True))
        self.assertEqual(engine.update(frame(200),True).name,'B')

    def test_unconfigured_does_not_split_or_skip(self):
        e=SplitEngine(make_route(['One','Two']))
        for _ in range(20):
            self.assertIsNone(e.update({'x':0,'y':0,'z':0},True))
        self.assertEqual(e.index,0)

    def test_route_import_uses_names_exactly(self):
        with tempfile.TemporaryDirectory() as tmp:
            lss=pathlib.Path(tmp)/'example.lss';out=pathlib.Path(tmp)/'route.json'
            lss.write_text('<Run><Segments><Segment><Name>Oedo Castle</Name></Segment>'
                           '<Segment><Name>Impact &amp; Boss</Name></Segment></Segments></Run>')
            names=segment_names(str(lss));self.assertEqual(names,['Oedo Castle','Impact & Boss'])
            save_route(make_route(names),str(out));route=load_route(str(out))
            self.assertEqual(len(route['segments']),2)
            self.assertIsNone(route['segments'][0]['trigger'])

if __name__=='__main__':unittest.main()
