"""Fail-closed source-integrity and actual-C host regression for JP tiny7."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from decomp import japan_tiny7_promotion as promotion

NAMES = {
    'func_801D7854_645D44', 'func_801DDC04_64C0F4',
    'func_8021DAEC_5D907C', 'func_8021DB00_5D9090',
    'func_8021FDA4_5DB334', 'func_802291F8_6928E8',
    'func_8022950C_692BFC',
}

class JapanTiny7Tests(unittest.TestCase):
    def test_original_manifest_source_integrity(self):
        rows = promotion.load_sources(promotion.DEFAULT_BUNDLES)
        self.assertEqual(len(rows), 7)
        self.assertEqual({r['name'] for r in rows}, NAMES)
        self.assertEqual(sum(r['size'] for r in rows), 156)
        self.assertEqual(len({r['off'] for r in rows}), 7)
        self.assertTrue(all(r['size'] > 0 and r['size'] % 4 == 0 for r in rows))
        self.assertTrue(all(r['relocations'] == [] for r in rows))

    def test_mutated_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'sources').mkdir()
            (p/'manifest.json').write_bytes((promotion.DEFAULT_BUNDLES/'manifest.json').read_bytes())
            for src in (promotion.DEFAULT_BUNDLES/'sources').glob('*.c'):
                (p/'sources'/src.name).write_bytes(src.read_bytes())
            target = p/'sources/func_801D7854_645D44.c'
            target.write_bytes(target.read_bytes()+b'/* fingerprint corruption */')
            with self.assertRaisesRegex(ValueError, 'Source SHA-256 drift'):
                promotion.load_sources(p)

    def test_bad_original_rom_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'config/japan_0').mkdir(parents=True)
            (p/'config/japan_0/baserom.decompressed.z64').write_bytes(b'invalid')
            with self.assertRaisesRegex(ValueError, 'Wrong Japanese original ROM'):
                promotion.original(p)

    def test_actual_original_c_host_asan_ubsan(self):
        if not shutil.which('gcc'): self.skipTest('GCC unavailable')
        src=promotion.DEFAULT_BUNDLES/'sources'
        program=r'''
#include <stdint.h>
#include <assert.h>
#include <string.h>
unsigned char func_801D7854_645D44(void *);
unsigned char func_801DDC04_64C0F4(void *);
void func_8021DAEC_5D907C(void *, int, int, int);
void func_8021DB00_5D9090(void *, int, int, int, int);
void func_8021FDA4_5DB334(void *, int);
void func_802291F8_6928E8(void *, float, float, int);
void func_8022950C_692BFC(void *, float, float, int);
int main(void) {
    _Alignas(16) unsigned char p[1024]={0};
    for (int i=0; i<1000; ++i) {
        p[0x315]=(unsigned char)(i%16);
        p[0x316]=(unsigned char)(i%19);
        assert(func_801D7854_645D44(p)==(unsigned char)((i%16)>=6));
        assert(func_801DDC04_64C0F4(p)==(unsigned char)((i%19)>=10));
        func_8021DAEC_5D907C(p, i, i+10, -i);
        assert(*(short*)(p+0x3c)==(short)i);
        assert(*(short*)(p+0x3e)==(short)(i+10));
        assert(*(short*)(p+0x40)==(short)(-i));
        assert(*(int*)(p+0x48)==0);
        func_8021DB00_5D9090(p, i, i+1, i+2, i+3);
        assert(p[0x98]==(unsigned char)i && p[0x99]==(unsigned char)(i+1));
        assert(p[0x9a]==(unsigned char)(i+2) && p[0x9b]==(unsigned char)(i+3));
        *(float*)(p+0xd0)=4.0f;
        *(float*)(p+0xd4)=5.0f;
        *(float*)(p+0xd8)=6.0f;
        func_8021FDA4_5DB334(p, i);
        assert(*(short*)(p+0x8a)==(short)i);
        assert(*(float*)(p+0xd0)==0.0f && *(float*)(p+0xd4)==0.0f && *(float*)(p+0xd8)==0.0f);
        float a=(float)(i+1)/8.0f, b=-(float)(i+3)/16.0f;
        func_802291F8_6928E8(p,a,b,i);
        assert(*(short*)(p+0x5e)==(short)i && *(float*)(p+0x68)==a && *(float*)(p+0x74)==b);
        func_8022950C_692BFC(p,b,a,-i);
        assert(*(short*)(p+0x5e)==(short)(-i) && *(float*)(p+0x68)==b && *(float*)(p+0x74)==a);
    }
    return 0;
}
'''
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);test=p/'test.c';test.write_text(program);out=p/'test'
            cmd=['gcc','-std=c11','-Wall','-Wextra','-Werror','-O1','-g',
                '-fsanitize=address,undefined','-fno-omit-frame-pointer','-fno-pie','-no-pie',str(test),
                *(str(src/(n+'.c')) for n in sorted(NAMES)),'-o',str(out)]
            subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=30)
            env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=0'
            subprocess.run([str(out)],check=True,capture_output=True,text=True,env=env,timeout=30)

if __name__=='__main__': unittest.main()
