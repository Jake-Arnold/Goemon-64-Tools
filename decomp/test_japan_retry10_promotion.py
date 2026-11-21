"""ROM-free integrity and actual C host coverage for JP retry10 native exact four."""
from __future__ import annotations
import json, os, re, shutil, subprocess, tempfile, unittest
from pathlib import Path
from decomp import japan_retry10_promotion as promotion

EXPECTED={'func_800012A0_1EA0','func_800015B8_21B8','func_80008648_9248','func_08001410_70F980'}

class JapanRetry10Tests(unittest.TestCase):
    def test_original_manifest(self):
        records=promotion.load_sources(promotion.DEFAULT_BUNDLES)
        self.assertEqual(len(records),4)
        self.assertEqual({r['name'] for r in records},EXPECTED)
        self.assertEqual(sum(r['size'] for r in records),160)
        self.assertEqual(sum(len(r['relocations']) for r in records),12)
        self.assertEqual(len({r['off'] for r in records}),4)
        self.assertEqual(records[-1]['name'],'func_08001410_70F980')

    def test_retains_original_incomplete_return_semantics_warning(self):
        text=(promotion.DEFAULT_BUNDLES/'sources/func_08001410_70F980.c').read_text()
        self.assertRegex(text,r'\bsigned char\b')
        self.assertIn('return 1;',text)
        self.assertNotIn('return 0;',text)
        self.assertNotIn('else',text)
        self.assertIn('undefined behaviour', (promotion.DEFAULT_BUNDLES/'README.md').read_text())

    def test_corrupted_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'sources').mkdir()
            (root/'manifest.json').write_bytes((promotion.DEFAULT_BUNDLES/'manifest.json').read_bytes())
            for source in (promotion.DEFAULT_BUNDLES/'sources').glob('*.c'):
                (root/'sources'/source.name).write_bytes(source.read_bytes())
            f=root/'sources/func_800015B8_21B8.c'
            f.write_bytes(f.read_bytes()+b'/* mutation */\n')
            with self.assertRaisesRegex(ValueError,'Source SHA-256 drift'):
                promotion.load_sources(root)

    def test_invalid_original_rom_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'config/japan_0';p.mkdir(parents=True)
            (p/'baserom.decompressed.z64').write_bytes(b'invalid')
            with self.assertRaisesRegex(ValueError,'Wrong Japanese original ROM'):
                promotion.original(Path(td))

    def test_actual_c_host_sanitizer(self):
        if not shutil.which('gcc'):self.skipTest('GCC not available')
        harness=r'''
#include <stdint.h>
#include <assert.h>
#include <string.h>
typedef struct { unsigned int w0,w1; } Gfx;
Gfx *g_display_list_head_ptr;
char D_80072FC0_73BC0[8], D_80073B10_74710[8], D_800730E0_73CE0[8];
void func_800012A0_1EA0(void);
void func_800015B8_21B8(void);
void func_80008648_9248(void);
int func_08001410_70F980(void*);
static void check(Gfx *p, uintptr_t symbol) {
 assert(g_display_list_head_ptr==p+1);
 assert(p[0].w0==0x06000000U);
 assert(p[0].w1==(uint32_t)symbol);
}
int main(void) {
 Gfx p[3]; unsigned char state[256]={0};
 for(int i=0;i<1000;i++) {
  memset(p,0,sizeof p);g_display_list_head_ptr=p;
  func_800012A0_1EA0();check(p,(uintptr_t)D_80072FC0_73BC0);
  memset(p,0,sizeof p);g_display_list_head_ptr=p;
  func_800015B8_21B8();check(p,(uintptr_t)D_80073B10_74710);
  memset(p,0,sizeof p);g_display_list_head_ptr=p;
  func_80008648_9248();check(p,(uintptr_t)D_800730E0_73CE0);
  state[0xd2]=5;
  assert(func_08001410_70F980(state)==1);
 }
 /* The original predicate does not define v0 on its false path, so the
  * corresponding missing-return C path is deliberately not exercised. */
 return 0;
}
'''
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td);file=folder/'host.c';file.write_text(harness)
            obj=folder/'host';sources=promotion.DEFAULT_BUNDLES/'sources'
            cmd=['gcc','-std=gnu11','-O1','-g','-Wall','-Wextra',
                 '-Werror','-Wno-pointer-to-int-cast','-Wno-return-type',
                 '-fsanitize=address,undefined','-fno-omit-frame-pointer',
                 '-fno-pie','-no-pie',str(file),
                 *[str(sources/(n+'.c')) for n in sorted(EXPECTED)],'-o',str(obj)]
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,0,p.stderr)
            env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=0'
            r=subprocess.run([str(obj)],capture_output=True,text=True,timeout=60,env=env)
            self.assertEqual(r.returncode,0,r.stderr)

if __name__ == '__main__':unittest.main()
