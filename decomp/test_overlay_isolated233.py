"""Original-USA isolated-stage native source, dedupe, and host semantic regression.

These ROM-free tests are not a substitute for decomp.verify and original ELF
relocation equality; they enforce additive source ownership and ABI contracts.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from decomp import overlay_isolated233 as native
from decomp.verify import claimed_functions, load_manifest, isolated233_stage

ROOT = Path(__file__).resolve().parent

class Isolated233PromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest(ROOT/'manifest.json')
        cls.fixture = native.load_fixture()
        cls.functions = cls.fixture['functions']

    def test_full_1964_cumulative_claims_are_unique(self):
        historical = {k:v for k,v in self.manifest.items()
                      if k!='overlay_reconcile108_stage'}
        previous = claimed_functions({k:v for k,v in historical.items()
                                      if k!='overlay_isolated233_stage'})
        current = claimed_functions(historical)
        self.assertEqual((len(previous),sum(f['size'] for f in previous)),(1723,69344))
        self.assertEqual((len(current),sum(f['size'] for f in current)),(1964,84708))
        self.assertEqual(len(self.functions),241)
        self.assertEqual(sum(f['size'] for f in self.functions),15364)
        self.assertEqual(len({f['name'] for f in current}),1964)
        spans = sorted((f['rom_offset'],f['rom_offset']+f['size']) for f in current)
        self.assertTrue(all(left[1]<=right[0] for left,right in zip(spans,spans[1:])))

    def test_frozen_original_sources_and_addresses(self):
        self.assertEqual(len(native.EMBEDDED),14)
        self.assertEqual(len({f['rom_offset'] for f in self.functions}),241)
        self.assertIn('func_8000A18C_AD8C',native.EMBEDDED)
        self.assertNotIn('func_8000AAE8_B6E8',native.EMBEDDED)
        self.assertNotIn('func_8000AB30_B730',native.EMBEDDED)
        self.assertNotIn('func_800108BC_114BC',native.EMBEDDED)
        self.assertIn('func_8000A548_B148',native.EMBEDDED)
        self.assertIn('func_8000A5C4_B1C4',native.EMBEDDED)
        for f in self.functions:
            with self.subTest(name=f['name']):
                p=native.SOURCE/(f['source']+'.c')
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),f['source_sha256'])
                self.assertEqual(len(f['original_code_sha256']),64)
                if f['name'].startswith('func_'):
                    _,vma,rom=f['name'].split('_')
                    self.assertEqual(int(vma,16),f['vma'])
                    self.assertEqual(int(rom,16),f['rom_offset'])
        self.assertIn('D_802171D0_676180', (native.SOURCE/'iso233_200.c').read_text())
        self.assertIn('D_802171D0_676180', (native.SOURCE/'iso233_201.c').read_text())

    def test_tampered_stage_contract_rejected(self):
        self.assertIsNotNone(isolated233_stage(self.manifest))
        bad=dict(self.manifest)
        bad['overlay_isolated233_stage']={'format':'probe_only'}
        with self.assertRaises(ValueError):isolated233_stage(bad)

    def test_all_original_sources_host_asan_ubsan_compilable(self):
        gcc=shutil.which('gcc')
        if not gcc:self.skipTest('No host GCC')
        for f in self.functions:
            p=native.SOURCE/(f['source']+'.c')
            with self.subTest(name=f['name']):
                run=subprocess.run([gcc,'-std=gnu89','-fsyntax-only',
                    '-Wno-int-to-pointer-cast','-Wno-pointer-to-int-cast',
                    '-Wno-implicit-function-declaration','-Wno-incompatible-pointer-types',
                    '-Wno-int-conversion','-fsanitize=address,undefined',
                    '-I'+str(native.SOURCE.parent/'tests'),str(p)],
                    capture_output=True,timeout=20)
                self.assertEqual(run.returncode,0,run.stderr.decode(errors='replace')[:350])

    def test_four_real_c_setters_execute_under_host_sanitizers(self):
        gcc=shutil.which('gcc')
        if not gcc:self.skipTest('No host GCC')
        body=r'''
#include <stdint.h>
#include <stdlib.h>
typedef int32_t s32;
s32 D_80152C38_153838;
s32 D_8015C5D8_15D1D8[8];
s32 *D_8016DAB4_16E6B4;
extern void func_800086C4_92C4(void *,s32,s32);
extern void func_800086D8_92D8(void *,s32);
extern void func_8000B5BC_C1BC(void);
extern void func_80035384_35F84(void);
int main(void){
    s32 obj[32]={0};
    s32 table[8]={0};
    D_8016DAB4_16E6B4=table;
    for(s32 i=0;i<1000;i++){
        func_800086C4_92C4(obj,i*3,i*7);
        if(obj[13]!=i*3||obj[5]!=i*7||D_80152C38_153838!=i*7)return 1;
        func_800086D8_92D8(obj,i+1);
        if(obj[13]!=i+1||obj[5]!=i*7)return 2;
        D_8015C5D8_15D1D8[2]=i*17;
        func_8000B5BC_C1BC();
        if(D_8015C5D8_15D1D8[3]!=i*17)return 3;
        table[5]=i*31;
        func_80035384_35F84();
        if(table[3]!=i*31)return 4;
    }
    return 0;
}
'''
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/'host233.c';binary=Path(d)/'host233';source.write_text(body)
            names=['iso233_007','iso233_008','iso233_014','iso233_028']
            cmd=[gcc,'-std=gnu11','-O1','-g','-fno-omit-frame-pointer',
                 '-fsanitize=address,undefined','-Wno-implicit-function-declaration',
                 '-o',str(binary),str(source),
                 *(str(native.SOURCE/(name+'.c')) for name in names)]
            c=subprocess.run(cmd,capture_output=True,timeout=30)
            self.assertEqual(c.returncode,0,c.stderr.decode(errors='replace')[:1000])
            # Host ASan/UBSan test runs actual source, with no mock copy replacing it.
            r=subprocess.run([str(binary)],capture_output=True,timeout=15)
            self.assertEqual(r.returncode,0,r.stderr.decode(errors='replace')[:1500])

if __name__=='__main__':unittest.main()
