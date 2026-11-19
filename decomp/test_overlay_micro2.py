"""Tests the two reviewed original-USA micro2 C bodies, not ROM proof."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from decomp import overlay_micro2


class Micro2Tests(unittest.TestCase):
    def test_reviewed_source_hashes(self):
        fixture = overlay_micro2.load_fixture()
        self.assertEqual(len(overlay_micro2.functions(fixture)), 2)
        self.assertEqual(sum(f['size'] for f in overlay_micro2.functions(fixture)), 28)
        for unit in fixture['units']:
            raw = (overlay_micro2.SOURCE_BASE / (unit['name'] + '.c')).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), unit['source_sha256'])

    @unittest.skipUnless(shutil.which('gcc'), 'GCC is required for the host sanitizer test')
    def test_actual_sources_asan_ubsan(self):
        code = r'''
#include <assert.h>
#include <stdint.h>
void func_801D068C_66353C(char *p, unsigned int a, unsigned int b);
void func_0800126C_708CAC(unsigned char *p);
int main(void) {
  unsigned int w[128] = {0};
  unsigned char p[512] = {0};
  for (unsigned int i=0;i<1000;i++) {
    unsigned int x=i*0x1234567U, y=i^0xDEADBEEFU;
    func_801D068C_66353C((char *)w,x,y);
    assert(w[0x80/4]==x && w[0x7c/4]==y);
    p[0xd0]=(unsigned char)i;
    func_0800126C_708CAC(p);
    assert(p[0xd0]==(unsigned char)(i+1));
  }
  return 0;
}
'''
        with tempfile.TemporaryDirectory() as tmp:
            harness = Path(tmp) / 'harness.c'
            exe = Path(tmp) / 'host-test'
            harness.write_text(code)
            subprocess.run(['gcc', '-std=c99', '-O1', '-g', '-fsanitize=address,undefined',
                            '-fno-omit-frame-pointer', '-o', str(exe),
                            str(overlay_micro2.SOURCE_BASE / 'micro15_fields.c'),
                            str(overlay_micro2.SOURCE_BASE / 'micro48_increment.c'),
                            str(harness)], capture_output=True, text=True, check=True)
            subprocess.run([str(exe)], capture_output=True, text=True, check=True)


if __name__ == '__main__':
    unittest.main()
