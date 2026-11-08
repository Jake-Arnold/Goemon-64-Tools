"""Host behaviour checks for the 44-byte VM callback-registration candidate.

These mock calls are not a substitute for MIPS original-address / full-ROM proof.
"""
import shutil
import subprocess
from pathlib import Path

import pytest


SOURCE = Path(__file__).resolve().parents[1] / 'decomp/candidates/vm_callback_register.c'


@pytest.mark.parametrize('callback,returned_handle', [
    (0, 0),
    (0x12345678, 0x5678),
    (-7, -123),
    (0x7FFFFFFF, 0x4000),
])
def test_callback_registration_passes_values_and_stores_handle(tmp_path, callback, returned_handle):
    compiler = shutil.which('gcc')
    if compiler is None:
        pytest.skip('Host GCC unavailable')
    harness = tmp_path / 'mock.c'
    harness.write_text('''
        typedef signed int s32;
        s32 D_801C7740_1C8340;
        s32 D_801C7750_1C8350 = -9876;
        static s32 expected_callback, next_handle;
        static int calls;
        s32 func_80034B24_35724(s32 callback, s32 flags) {
            if (callback != expected_callback || flags != 0) return -99999;
            calls++;
            return next_handle;
        }
        void func_8003F350_3FF50(void);
        int main(void) {
            expected_callback = CALLBACK;
            next_handle = HANDLE;
            D_801C7740_1C8340 = expected_callback;
            func_8003F350_3FF50();
            if (calls != 1 || D_801C7750_1C8350 != next_handle) return 1;
            next_handle++;
            func_8003F350_3FF50();
            if (calls != 2 || D_801C7750_1C8350 != next_handle) return 2;
            return 0;
        }
    '''.replace('CALLBACK', str(callback)).replace('HANDLE', str(returned_handle)))
    program = tmp_path / 'register'
    subprocess.run([compiler, '-std=c99', '-Wall', '-Wextra', '-Werror',
                    str(SOURCE), str(harness), '-o', str(program)], check=True,
                   capture_output=True, text=True)
    subprocess.run([str(program)], check=True, capture_output=True, text=True)
