"""ROM-free source provenance and host-semantic tests for Japan JP2314."""
from __future__ import annotations
import json, os, shutil, subprocess, tempfile, unittest
from pathlib import Path
from decomp import japan_expand7_promotion as promotion

EXPECTED={
 'func_801E7F74_5A3F44','func_801E7F98_5A3F68',
 'func_801E83F0_5A43C0','func_801E8424_5A43F4','func_801E8458_5A4428',
 'func_8021B434_67A2A4','func_8021B450_67A2C0',
}

class JapanExpand7Tests(unittest.TestCase):
    def test_source_manifest_and_original_ownership(self):
        rows=promotion.load_sources(promotion.DEFAULT_BUNDLES)
        self.assertEqual(len(rows),7)
        self.assertEqual({r['name'] for r in rows},EXPECTED)
        self.assertEqual(len({r['off'] for r in rows}),7)
        self.assertEqual(sum(r['size'] for r in rows),284)
        self.assertEqual(sum(len(r['relocations']) for r in rows),15)
        self.assertTrue(all(r['size']%4==0 and r['size']>0 for r in rows))

    def test_symbolic_relocations_are_frozen(self):
        rows=promotion.load_sources(promotion.DEFAULT_BUNDLES)
        for r in rows:
            self.assertTrue(r['relocations'])
            self.assertTrue(all(q['type'] in ('R_MIPS_HI16','R_MIPS_LO16','R_MIPS_26') for q in r['relocations']))
            self.assertEqual(len(r['relocations']),2 if '8021B4' in r['name'] else 1 if '801E7F' in r['name'] else 3)

    def test_manifest_rejects_source_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'sources').mkdir()
            (root/'manifest.json').write_bytes((promotion.DEFAULT_BUNDLES/'manifest.json').read_bytes())
            for s in (promotion.DEFAULT_BUNDLES/'sources').glob('*.c'):
                (root/'sources'/s.name).write_bytes(s.read_bytes())
            target=root/'sources/func_8021B450_67A2C0.c'
            target.write_bytes(target.read_bytes()+b'// tampered\n')
            with self.assertRaisesRegex(ValueError,'Source SHA-256 drift'):
                promotion.load_sources(root)

    def test_invalid_original_rom_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'config/japan_0';p.mkdir(parents=True)
            (p/'baserom.decompressed.z64').write_bytes(b'not a rom')
            with self.assertRaisesRegex(ValueError,'Wrong Japanese original ROM'):
                promotion.original(Path(td))

    def test_actual_seven_c_sources_host_sanitizer(self):
        if shutil.which('gcc') is None:self.skipTest('No GCC')
        harness=r'''
#include <assert.h>
#include <stdint.h>
#include <string.h>
typedef struct { signed char value; unsigned char remaining[119]; } Record120;
Record120 D_8021BEB6_67AD26[9],D_8021BEB7_67AD27[9];
float D_802101C0_5CC190=1.25f,D_802101C4_5CC194=-0.5f,D_802101C8_5CC198=10.75f;
int func_8021B434_67A2A4(int);
int func_8021B450_67A2C0(int);
void func_801E7F74_5A3F44(void*);void func_801E7F98_5A3F68(void*);
void func_801E83F0_5A43C0(void*);void func_801E8424_5A43F4(void*);void func_801E8458_5A4428(void*);
static void *expected_ptr;static int calls_a,calls_b,calls_f, fidx;
void func_801E7FBC_5A3F8C(void*p,int a,int b){
 assert(p==expected_ptr);
 assert((a==5&&b==4)||(a==10&&b==8));
 if(a==5)calls_a++;else calls_b++;
}
void func_801E84E8_5A44B8(void*p,float a,float b,float c){
 assert(p==expected_ptr);
 float want=(fidx==0)?D_802101C0_5CC190:(fidx==1)?D_802101C4_5CC194:D_802101C8_5CC198;
 assert(a==want&&b==want&&c==want);calls_f++;
}
int main(void){
 int marker=0;expected_ptr=&marker;
 for(int k=0;k<1000;k++){
  int i=k%9;D_8021BEB6_67AD26[i].value=(signed char)(i-8);
  D_8021BEB7_67AD27[i].value=(signed char)(8-i);
  assert(func_8021B434_67A2A4(i)==i-8);
  assert(func_8021B450_67A2C0(i)==8-i);
  func_801E7F74_5A3F44(&marker);func_801E7F98_5A3F68(&marker);
  fidx=0;func_801E83F0_5A43C0(&marker);
  fidx=1;func_801E8424_5A43F4(&marker);
  fidx=2;func_801E8458_5A4428(&marker);
 }
 assert(calls_a==1000&&calls_b==1000&&calls_f==3000);return 0;
}
'''
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);h=root/'host.c';h.write_text(harness)
            output=root/'host';sources=promotion.DEFAULT_BUNDLES/'sources'
            cmd=['gcc','-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror',
                 '-fsanitize=address,undefined','-fno-omit-frame-pointer','-fno-pie','-no-pie',
                 str(h),*[str(sources/(n+'.c')) for n in sorted(EXPECTED)],'-o',str(output)]
            c=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
            self.assertEqual(c.returncode,0,c.stderr)
            env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=0'
            r=subprocess.run([str(output)],capture_output=True,text=True,timeout=60,env=env)
            self.assertEqual(r.returncode,0,r.stderr)

if __name__=='__main__':unittest.main()
