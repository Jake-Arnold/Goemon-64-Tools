"""Micro15 actual-C host behavior and immutable source hashes. Not a ROM gate."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from decomp import overlay_micro15


class Micro15Tests(unittest.TestCase):
    def test_reviewed_source_hashes_and_unit_layout(self):
        j = overlay_micro15.load_fixture()
        self.assertEqual(len(overlay_micro15.functions(j)), 15)
        self.assertEqual(sum(f['size'] for f in overlay_micro15.functions(j)), 296)
        for u in j['units']:
            source = (overlay_micro15.SOURCE_BASE / (u['name'] + '.c')).read_bytes()
            self.assertEqual(hashlib.sha256(source).hexdigest(), u['source_sha256'])

    @unittest.skipUnless(shutil.which('gcc'), 'GCC is required for sanitizer host test')
    def test_all_actual_c_sources_asan_ubsan(self):
        fixture = overlay_micro15.load_fixture()
        sources = [str(overlay_micro15.SOURCE_BASE / (u['name'] + '.c')) for u in fixture['units']]
        code = r'''
#include <assert.h>
#include <stdint.h>
#include <string.h>
void func_08000420_706210(char *, int);
void func_08000490_73CAA0(char *, float);
unsigned char func_801D2124_640F74(unsigned char *);
unsigned char func_801D84D4_647324(unsigned char *);
void func_801D9D98_605178(void *, unsigned char *);
void func_80213EC4_5CF394(void *, unsigned char *);
void func_80210624_698024(char *, float, float);
void func_80213044_69AA44(char *, float, float);
void func_80213058_69AA58(char *, float, float);
void func_80213094_69AA94(char *, float *, float *);
void func_801F7074_622454(unsigned char *);
void func_801FFE6C_62B24C(unsigned char *);
void func_801D61D4_6015B4(char *, float);
void func_801D3100_5FE4E0(char *, float);
void func_801CB684_65E534(char *, unsigned int,unsigned int,unsigned int,unsigned int);
int main(void) {
  union { uint64_t align; unsigned char bytes[1024]; } u = {0}, v = {0};
  unsigned char *p=u.bytes, *q=v.bytes;
  for (unsigned int i=0;i<1000;i++) {
    func_08000420_706210((char *)p,(int)i);
    assert(*(int *)(p+0x80)==(int)(i*40));
    func_08000490_73CAA0((char *)p,(float)i*0.5f);
    assert(p[0xd3]==1 && *(float *)(p+0xe4)==(float)i*0.5f);
    p[0x315]=(unsigned char)(i%12);
    p[0x316]=(unsigned char)(i%16);
    assert(func_801D2124_640F74(p)==(p[0x315]>=6));
    assert(func_801D84D4_647324(p)==(p[0x316]>=10));
    q[0x64]=0; func_801D9D98_605178(p,q); assert(q[0x64]==1);
    q[0x65]=1; func_80213EC4_5CF394(p,q); assert(q[0x65]==0);
    func_80210624_698024((char *)p,(float)i,(float)(i+1));
    assert(*(float *)(p+0xa0)==(float)i && *(float *)(p+0xa4)==(float)(i+1));
    func_80213044_69AA44((char *)p,(float)i+2,(float)i+3);
    assert(*(float *)(p+0x6c)==(float)i+2 && *(float *)(p+0x7c)==(float)i+3);
    func_80213058_69AA58((char *)p,(float)i+4,(float)i+5);
    assert(*(float *)(p+0x68)==(float)i+4 && *(float *)(p+0x78)==(float)i+5);
    float a=0,b=0; func_80213094_69AA94((char *)p,&a,&b);
    assert(a==(float)i+2 && b==(float)i+3);
    func_801F7074_622454(p);
    assert(p[0x30]==1 && *(unsigned int *)(p+0x48)==0 && p[0x4c]==0);
    p[0x30]=0;func_801FFE6C_62B24C(p);
    assert(p[0x30]==1 && *(unsigned int *)(p+0x48)==0 && p[0x4c]==0);
    *(float *)(p+0x0c)=(float)i;
    func_801D61D4_6015B4((char *)p,1.25f);
    assert(*(float *)(p+0x0c)==(float)i+1.25f);
    func_801D3100_5FE4E0((char *)p,(float)i+7);
    assert(*(float *)(p+0x28)==(float)i+7);
    func_801D3100_5FE4E0((char *)0,(float)i+7);
    func_801CB684_65E534((char *)p,i,i+1,i+2,i+3);
    assert(*(unsigned int *)(p+0x7c)==i && *(unsigned int *)(p+0x80)==i+1 &&
           *(unsigned int *)(p+0x84)==i+2 && *(unsigned int *)(p+0x88)==i+3);
  }
  return 0;
}
'''
        with tempfile.TemporaryDirectory() as temp:
            harness = Path(temp) / 'harness.c'
            exe = Path(temp) / 'host'
            harness.write_text(code)
            subprocess.run(['gcc', '-std=c99', '-O1', '-g', '-fno-pie', '-no-pie',
                            '-fsanitize=address,undefined','-fno-omit-frame-pointer',
                            '-o', str(exe), *sources, str(harness)],
                           capture_output=True, text=True, check=True)
            subprocess.run([str(exe)], capture_output=True, text=True, check=True)

if __name__=='__main__':unittest.main()
