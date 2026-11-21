"""ROM-free tests of the Japanese donor-template original-address G2 wave."""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from decomp import japan_donor10_promotion as promo


class Donor10Tests(unittest.TestCase):
    def test_exact_original_sources_and_dedup(self):
        rows = promo.load_sources(promo.DEFAULT_BUNDLES)
        self.assertEqual(len(rows), 10)
        self.assertEqual(len({r['name'] for r in rows}), 10)
        self.assertEqual(len({r['off'] for r in rows}), 10)
        self.assertEqual(sum(r['size'] for r in rows), 716)
        self.assertTrue(all(r['size'] % 4 == 0 for r in rows))
        self.assertTrue(all(r['name'] not in {
            'func_8003CC10_3D810', 'func_8003E2C4_3EEC4'
        } for r in rows))

    def test_original_offsets_are_explicit_not_region_heuristics(self):
        rows=promo.load_sources(promo.DEFAULT_BUNDLES)
        for row in rows:
            if row['name'].startswith('func_'):
                self.assertEqual(int(row['name'].rsplit('_',1)[1],16),row['off'])
        self.assertEqual([r['off'] for r in rows if r['name']=='osSpTaskYield'],[0x434B0])

    def test_mutating_a_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)
            (dest/'sources').mkdir()
            (dest/'manifest.json').write_bytes((promo.DEFAULT_BUNDLES/'manifest.json').read_bytes())
            for p in (promo.DEFAULT_BUNDLES/'sources').glob('*.c'):
                (dest/'sources'/p.name).write_bytes(p.read_bytes())
            f=dest/'sources/func_80013800_14400.c'
            f.write_bytes(f.read_bytes()+b'\n/* mutated */\n')
            with self.assertRaisesRegex(ValueError,'Source SHA-256 drift'):
                promo.load_sources(dest)

    def test_incomplete_original_rom_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'config/japan_0').mkdir(parents=True)
            (p/'config/japan_0/baserom.decompressed.z64').write_bytes(b'bad')
            with self.assertRaisesRegex(ValueError,'Wrong Japanese original ROM'):
                promo.original(p)

    def test_actual_c_wrappers_1000_host_cases_with_sanitizers(self):
        if shutil.which('gcc') is None:
            self.skipTest('GCC not installed')
        src=promo.DEFAULT_BUNDLES/'sources'
        test=r'''
#include <assert.h>
#include <stdint.h>
static unsigned char *expect_pointer;
static int expect_u8, setstatus_calls, wrapper_calls, narrow_calls;
void func_80013820_14420(void *p, int n) { assert(p==expect_pointer); assert(n==4); wrapper_calls++; }
void func_801E8AB0_5A4A80(void *p, unsigned char n) { assert(p==expect_pointer); assert((int)n==expect_u8); narrow_calls++; }
void __osSpSetStatus(int n) { assert(n==0x400); setstatus_calls++; }
extern void func_80013800_14400(void *);
extern void func_801E7AF8_5A3AC8(void *, unsigned char);
extern void osSpTaskYield(void);
int main(void) {
  unsigned char data[64]={0}; expect_pointer=data;
  for(int i=0;i<1000;i++) {expect_u8=i&255;func_80013800_14400(data);
    func_801E7AF8_5A3AC8(data,(unsigned char)i);osSpTaskYield();}
  assert(wrapper_calls==1000&&narrow_calls==1000&&setstatus_calls==1000);
  return 0;
}
'''
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);test_c=root/'fixture.c';test_c.write_text(test)
            exe=root/'fixture'
            cmd=['gcc','-std=c11','-Wall','-Wextra','-Werror','-O1','-g',
                 '-fsanitize=address,undefined','-fno-omit-frame-pointer','-fno-pie','-no-pie',
                 str(test_c),str(src/'func_80013800_14400.c'),
                 str(src/'func_801E7AF8_5A3AC8.c'),str(src/'osSpTaskYield.c'),'-o',str(exe)]
            subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=30)
            env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=0'
            subprocess.run([str(exe)],check=True,capture_output=True,text=True,env=env,timeout=30)

if __name__=='__main__':unittest.main()
