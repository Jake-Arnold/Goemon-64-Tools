#!/usr/bin/env python3
"""Reconstruct the exact research C candidate from the prior source-only gzip.
No compiler, original ROM, game asset or assembly is embedded or downloaded.
"""
import gzip, hashlib, re, sys
from pathlib import Path

BEFORE_SHA='612bc4baa9c81b0c2397fa1b9b0853da6f0d4738b2c65c7842a77a4d35546d90'
AFTER_SHA='b444006aa5bd9dddf64b3fd19d2d5a49d43a7ff962f2d65778e93f72c8ac6078'

def replace_once(source, old, new):
    assert source.count(old)==1, ('source changed unexpectedly',old)
    return source.replace(old,new,1)

def build(previous_gz):
    raw=gzip.decompress(Path(previous_gz).read_bytes())
    assert hashlib.sha256(raw).hexdigest()==BEFORE_SHA
    s=raw.decode('utf-8')
    s=replace_once(s,'    s32 pool_s32_0;\n    s32 pool_s32_1;', '    s32 pool_s32_1;')
    s=replace_once(s,'    f32 vecA[3];','    f32 vecA[4];')
    s=replace_once(s,'    f32 pool_fp_0;','    s32 pool_s32_0;\n    f32 pool_fp_0;')
    s=replace_once(s,
        '    angles_and_vecC.t.switch_angles[0] = pool_s32_0;\n'
        '    func_80003EA0_4AA0(angles_and_vecC.t.first_angle);',
        '    pool_u16_1 = angles_and_vecC.t.first_angle;\n'
        '    angles_and_vecC.t.switch_angles[0] = pool_s32_0;\n'
        '    func_80003EA0_4AA0(pool_u16_1);')
    pattern=re.compile(r'M2C_FIELD\(arg0, f32 \*, (0x[0-9A-Fa-f]+)\) = 0\.0f;')
    index=[0]
    def change(m):
        index[0]+=1
        return ('M2C_FIELD(arg0, f32 *, '+m.group(1)+') = (f32)0;') if index[0]>=23 else m.group(0)
    s=pattern.sub(change,s)
    assert index[0]==33, ('expected 33 direct typed zero stores',index[0])
    data=s.encode('utf-8')
    assert hashlib.sha256(data).hexdigest()==AFTER_SHA
    return data

if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit('Usage: python3 reconstruct_from_prior_source.py PREVIOUS_SOURCE.c.gz OUTPUT.c')
    target=Path(sys.argv[2]);target.write_bytes(build(sys.argv[1]))
    print('SOURCE_RECONSTRUCTED_SHA256',AFTER_SHA)
