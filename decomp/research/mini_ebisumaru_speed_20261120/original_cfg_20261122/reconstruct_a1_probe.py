#!/usr/bin/env python3
"""Reconstruct the diagnostic second-argument cosine call from prior matching-C research source.
Only source text is manipulated; no private ROM / MIPS bytes are embedded.
"""
import hashlib, sys
from pathlib import Path
BEFORE='43f54bc681c1f1faaa33544a9effbba6750b9bc4acf49c29c36d2d73fbefb6d5'
AFTER='1d0c04a3139718de1ee159125312718d571351d77c9341e69346c29f2be014cb'

def transform(data):
    assert hashlib.sha256(data).hexdigest()==BEFORE, 'incorrect prior research source'
    s=data.decode('utf8')
    before='f32 func_80003EA0_4AA0(u16);'
    after='f32 func_80003EA0_4AA0(u16, ...);'
    assert s.count(before)==1
    s=s.replace(before,after,1)
    before='func_80003EA0_4AA0(pool_u16_1);'
    after='func_80003EA0_4AA0(pool_u16_1, pool_s32_0);'
    assert s.count(before)==1
    s=s.replace(before,after,1)
    b=s.encode('utf8')
    assert hashlib.sha256(b).hexdigest()==AFTER, 'output diverged from native-measured probe'
    return b

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: python3 reconstruct_a1_probe.py SOURCE_F14_117.c OUTPUT_A1_DIAGNOSTIC.c')
    Path(sys.argv[2]).write_bytes(transform(Path(sys.argv[1]).read_bytes()))
    print('RECONSTRUCTED_SOURCE_SHA256',AFTER)
