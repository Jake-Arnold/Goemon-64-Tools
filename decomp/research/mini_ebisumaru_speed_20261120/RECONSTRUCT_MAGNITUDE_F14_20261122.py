#!/usr/bin/env python3
"""Reconstruct the exact source-only USA Mini clamp research C from the prior C.
Usage: python3 RECONSTRUCT_MAGNITUDE_F14_20261122.py PRIOR_EXACT_EARLY.c OUTPUT.c [early|best|short]
No ROM, MIPS opcodes or compiler is bundled.
"""
import hashlib
import re
import sys
from pathlib import Path

BASE_SHA = 'b444006aa5bd9dddf64b3fd19d2d5a49d43a7ff962f2d65778e93f72c8ac6078'
EXPECTED = {
    'early': 'c6e6a4f29a7654f79d0592f3e71fa9d84f075ca79f2b96a8859a6664e4923836',
    'best': '43f54bc681c1f1faaa33544a9effbba6750b9bc4acf49c29c36d2d73fbefb6d5',
    'short': '0f831c35d52feb2d6ac26912045fb9221a4b79d8d0501b28cc1f721ac7eb0c1e',
}
ZERO_FIELD = re.compile(r'M2C_FIELD\(arg0, f32 \*, (0x[0-9A-Fa-f]+)\) = (?:0\.0f|\(f32\)0);')

def exactly_once(src, old, new):
    assert src.count(old) == 1, (old, src.count(old))
    return src.replace(old, new, 1)

def reconstruct(base, mode):
    assert mode in EXPECTED
    assert hashlib.sha256(base).hexdigest() == BASE_SHA, 'Input research C hash mismatch'
    s=base.decode('utf-8')
    s=exactly_once(s,'    u8 magnitude_valid;\n','')
    s=exactly_once(s,'    magnitude_valid = 0;','    pool_fp_2 = 0.0f;')
    s=exactly_once(s,'            magnitude_valid = 1;\n','')
    s=exactly_once(s,'            if (!magnitude_valid) {\n                pool_fp_2 = 0.0f;\n            }\n','')
    s=exactly_once(s,'f32 vecA[4]','f32 vecA[5]')
    s=exactly_once(s,'    pool_fp_2 = 0.0f;\n','')
    s=exactly_once(s,'    if ((pool_u8_0 != 0)', '    pool_fp_2 = 0.0f;\n    if ((pool_u8_0 != 0)')
    selected={'early':set(range(22,33)), 'best':(set(range(16,27))-{19})|{32}, 'short':set(range(11,22))}[mode]
    assert len(selected)==11
    count=[0]
    def canonical_zero(m):
        i=count[0];count[0]+=1
        return f'M2C_FIELD(arg0, f32 *, {m.group(1)}) = ' + ('(f32)0;' if i in selected else '0.0f;')
    s=ZERO_FIELD.sub(canonical_zero,s)
    assert count[0] == 33, count
    output=s.encode('utf-8')
    actual=hashlib.sha256(output).hexdigest()
    assert actual==EXPECTED[mode], (mode,'Output research C hash mismatch',actual,EXPECTED[mode])
    return output

if __name__ == '__main__':
    if len(sys.argv) not in (3,4):
        raise SystemExit('Usage: python3 RECONSTRUCT_MAGNITUDE_F14_20261122.py PRIOR_EXACT_EARLY.c OUTPUT.c [early|best|short]')
    mode=sys.argv[3] if len(sys.argv)==4 else 'best'
    target=Path(sys.argv[2]);target.write_bytes(reconstruct(Path(sys.argv[1]).read_bytes(),mode))
    print('EXACT_SOURCE_RECONSTRUCTED',mode,EXPECTED[mode])
