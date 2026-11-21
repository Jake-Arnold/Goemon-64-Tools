"""ROM-free source-integrity and actual-C host tests for Japanese donor4 G2."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from decomp import japan_donor4_promotion as promotion

class Donor4Tests(unittest.TestCase):
    def test_four_original_sources_offsets_and_hashes(self):
        rows=promotion.load_sources(promotion.DEFAULT_BUNDLES)
        self.assertEqual(len(rows),4)
        self.assertEqual(len({r['name'] for r in rows}),4)
        self.assertEqual(len({r['off'] for r in rows}),4)
        self.assertEqual(sum(r['size'] for r in rows),120)
        self.assertTrue(all(r['size']%4==0 and r['size']>0 for r in rows))
        self.assertEqual({r['name'] for r in rows}, {'alSynDelete','func_800079EC_85EC','func_801D6CE0_6451D0','func_801FF4B8_5BB488'})

    def test_mutated_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'sources').mkdir()
            (p/'manifest.json').write_bytes((promotion.DEFAULT_BUNDLES/'manifest.json').read_bytes())
            for src in (promotion.DEFAULT_BUNDLES/'sources').glob('*.c'):
                (p/'sources'/src.name).write_bytes(src.read_bytes())
            changed=p/'sources/alSynDelete.c';changed.write_bytes(changed.read_bytes()+b'/* changed */')
            with self.assertRaisesRegex(ValueError,'Source SHA-256 drift'):
                promotion.load_sources(p)

    def test_invalid_original_image_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'config/japan_0').mkdir(parents=True)
            (p/'config/japan_0/baserom.decompressed.z64').write_bytes(b'broken')
            with self.assertRaisesRegex(ValueError,'Wrong Japanese original ROM'):
                promotion.original(p)

    def test_actual_four_c_sources_host_with_sanitizers(self):
        if not shutil.which('gcc'):self.skipTest('GCC unavailable')
        src=promotion.DEFAULT_BUNDLES/'sources'
        stub=r'''
#include <assert.h>
#include <stdint.h>
static void *expect_ptr_a,*expect_ptr_b;
static int expected_n, calls32, calls36, calls44;
void func_80007870_8470(void *p,int n){assert(p==expect_ptr_a);assert(n==expected_n);calls32++;}
void func_801D2594_640A84(void *a,void *b,int c,int d){assert(a==expect_ptr_a&&b==expect_ptr_b);assert(c==0&&d==0x45);calls36++;}
void func_801FF4E4_5BB4B4(unsigned short x,int y){assert(x==(unsigned short)expected_n&&y==0);calls44++;}
extern void alSynDelete(void *);
extern void func_800079EC_85EC(void *);
extern void func_801D6CE0_6451D0(void *,void *);
extern void func_801FF4B8_5BB488(unsigned short);
int main(void){unsigned char a[128]={0}, b[32]={0};expect_ptr_a=a;expect_ptr_b=b;
for(int i=0;i<1000;i++){*(int*)(a+0x38)=i;expected_n=i;
int val=0x1234;alSynDelete(&val);assert(val==0);
func_800079EC_85EC(a);func_801D6CE0_6451D0(a,b);
func_801FF4B8_5BB488((unsigned short)i);}
assert(calls32==1000&&calls36==1000&&calls44==1000);return 0;}
'''
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);test=p/'test.c';test.write_text(stub);out=p/'test'
            cmd=['gcc','-std=c11','-Wall','-Wextra','-Werror','-O1','-g',
                '-fsanitize=address,undefined','-fno-omit-frame-pointer','-fno-pie','-no-pie',str(test),
                *(str(src/(n+'.c')) for n in ['alSynDelete','func_800079EC_85EC','func_801D6CE0_6451D0','func_801FF4B8_5BB488']),'-o',str(out)]
            subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=30)
            env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=0'
            subprocess.run([str(out)],check=True,capture_output=True,text=True,env=env,timeout=30)

if __name__=='__main__':unittest.main()
