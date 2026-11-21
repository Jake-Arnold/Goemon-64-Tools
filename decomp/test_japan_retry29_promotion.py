"""Integrity and authentic-original-C host tests for Japan retry29 salvage."""
from __future__ import annotations
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from decomp import japan_retry29_promotion as promotion

EXPECTED = {
    'func_080012FC_7385DC', 'func_08001380_734E00',
    'func_08001778_6C5938', 'func_8001067C_1127C',
    'func_801D54D8_667A28', 'func_801D5718_667C68',
    'func_801E4ED0_6533C0', 'func_801E5760_653C50',
    'func_801E60D4_6545C4', 'func_80217E64_69F564',
    'func_802193AC_67821C', 'func_8021FF00_6895F0',
    'func_80221624_68AD14', 'func_8022B2F4_6949E4',
}

class JapanRetry29Tests(unittest.TestCase):
    def test_original_manifest_and_sources(self):
        records = promotion.load_sources(promotion.DEFAULT_BUNDLES)
        self.assertEqual(len(records), 14)
        self.assertEqual({r['name'] for r in records}, EXPECTED)
        self.assertEqual(sum(r['size'] for r in records), 512)
        self.assertEqual(len({r['off'] for r in records}), 14)
        self.assertEqual(sum(len(r['relocations']) for r in records), 14)
        self.assertTrue(all(r['size'] % 4 == 0 and r['size'] >= 12 for r in records))

    def test_duplicate_prior_c_rejected_by_original_owner(self):
        old = promotion.ROOT / 'research/jp_tiny7_20261121/manifest.json'
        import json
        accepted = {r['name'] for r in json.loads(old.read_text())['functions']}
        self.assertFalse(accepted & EXPECTED)

    def test_corrupted_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / 'sources').mkdir()
            (p / 'manifest.json').write_bytes(
                (promotion.DEFAULT_BUNDLES / 'manifest.json').read_bytes())
            for src in (promotion.DEFAULT_BUNDLES / 'sources').glob('*.c'):
                (p / 'sources' / src.name).write_bytes(src.read_bytes())
            target = p / 'sources/func_080012FC_7385DC.c'
            target.write_bytes(target.read_bytes() + b'\n/* mutation */\n')
            with self.assertRaisesRegex(ValueError, 'Source SHA-256 drift'):
                promotion.load_sources(p)

    def test_invalid_private_rom_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / 'config/japan_0').mkdir(parents=True)
            (p / 'config/japan_0/baserom.decompressed.z64').write_bytes(b'invalid')
            with self.assertRaisesRegex(ValueError, 'Wrong Japanese original ROM'):
                promotion.original(p)

    def test_actual_native_c_asan_ubsan_host(self):
        if not shutil.which('gcc'):
            self.skipTest('Host GCC unavailable')
        sources = promotion.DEFAULT_BUNDLES / 'sources'
        # Exercised 12 of 14 originals. The dual-pointer +0xB0/+0xB4 routine
        # has N64 32-bit pointers overlapping on a 64-bit host and is omitted.
        names = sorted(EXPECTED - {'func_8021FF00_6895F0',
                                  'func_08001778_6C5938'})
        program = r'''
#include <stdint.h>
#include <assert.h>
#include <string.h>
#include <math.h>
typedef struct {unsigned int w0,w1;} Gfx;
char D_80069300_69F00[8], D_801D8FC0_66B510[8], D_8021BDE8_67AC58[8];
double D_801F4AA0_662F90=0.1, D_801F4AC0_662FB0=0.1, D_801F4AE0_662FD0=0.1;
int func_080012FC_7385DC(void*); int func_08001380_734E00(void*);
Gfx* func_8001067C_1127C(Gfx*);Gfx* func_801D54D8_667A28(Gfx*);
Gfx* func_801D5718_667C68(Gfx*);Gfx* func_802193AC_67821C(Gfx*);
void func_801E4ED0_6533C0(void*,void*);void func_801E5760_653C50(void*,void*);
void func_801E60D4_6545C4(void*,void*);
void func_80217E64_69F564(void*,int);
float func_80221624_68AD14(void*);
void* func_8022B2F4_6949E4(void*,int);
static void chk(Gfx *d,Gfx* ret,void *symbol) {
 assert(ret==d+1);assert(d[0].w0==0x06000000);
 assert(d[0].w1==(uint32_t)(uintptr_t)symbol);
 assert(d[1].w0==0xb8000000);assert(d[1].w1==0);
}
int main(void) {
 _Alignas(16) unsigned char parent[512]={0},inner[128]={0};
 _Alignas(16) unsigned char input[512]={0},output[512]={0};
 Gfx d[2];
 for(int i=0;i<1000;i++) {
  *(void**)(parent+0xd0)=inner;
  *(int*)(inner+0x10)=i*31-100;
  assert(func_080012FC_7385DC(parent)==i*31-100);
  assert(func_08001380_734E00(parent)==i*31-100);
  *(void**)(parent+0x18)=inner;
  *(float*)(inner+0x24)=(float)i/7.0f;
  assert(func_80221624_68AD14(parent)==(float)i/7.0f);
  memset(d,0,sizeof d);chk(d,func_8001067C_1127C(d),D_80069300_69F00);
  memset(d,0,sizeof d);chk(d,func_801D54D8_667A28(d),D_801D8FC0_66B510);
  memset(d,0,sizeof d);chk(d,func_801D5718_667C68(d),D_801D8FC0_66B510);
  memset(d,0,sizeof d);chk(d,func_802193AC_67821C(d),D_8021BDE8_67AC58);
  *(void**)(parent+0x88)=inner;
  func_80217E64_69F564(parent,i);
  assert(*(unsigned short*)(inner+0xc)==(unsigned short)i);
  assert(func_8022B2F4_6949E4(parent,i)==inner);
  assert(inner[5]==(unsigned char)i);
  for(int j=0;j<3;j++) *(float*)(input+0x7c+j*4)=(float)(i+1+j)/4.0f;
  memset(output,0,sizeof output);func_801E4ED0_6533C0(input,output);
  for(int j=0;j<3;j++) {
   float v=*(float*)(input+0x7c+j*4);
   assert(*(float*)(output+0x88+j*4)==v);
   assert(*(float*)(output+0x8+j*4)==(float)((double)v*0.1));
  }
  memset(output,0,sizeof output);func_801E5760_653C50(input,output);
  for(int j=0;j<3;j++) {
   float v=*(float*)(input+0x7c+j*4);
   assert(*(float*)(output+0x88+j*4)==v);
   assert(*(float*)(output+0x8+j*4)==(float)((double)v*0.1));
  }
  memset(output,0,sizeof output);func_801E60D4_6545C4(input,output);
  for(int j=0;j<3;j++) {
   float v=*(float*)(input+0x7c+j*4);
   assert(*(float*)(output+0x80+j*4)==v);
   assert(*(float*)(output+0x8+j*4)==(float)((double)v*0.1));
  }
 }
 return 0;
}
'''
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); main=p/'main.c';out=p/'host-test'
            main.write_text(program)
            cmd=['gcc','-std=gnu11','-Wall','-Wextra','-Werror',
                 '-Wno-pointer-to-int-cast','-O1','-g',
                 '-fsanitize=address,undefined','-fno-omit-frame-pointer',
                 '-fno-pie','-no-pie',str(main),
                 *(str(sources/(n+'.c')) for n in names),'-o',str(out)]
            build=subprocess.run(cmd,check=False,capture_output=True,text=True,timeout=60)
            self.assertEqual(build.returncode,0,build.stderr)
            env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=0'
            run=subprocess.run([str(out)],check=False,capture_output=True,text=True,env=env,timeout=60)
            self.assertEqual(run.returncode,0,run.stderr)

if __name__ == '__main__':unittest.main()
