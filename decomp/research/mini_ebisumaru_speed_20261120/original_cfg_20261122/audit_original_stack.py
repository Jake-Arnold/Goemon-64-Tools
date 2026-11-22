#!/usr/bin/env python3
"""Read-only, fail-closed verifier for original magnitude-stack dataflow.
Outputs only operation/offset metadata, never original instruction bytes.
"""
import argparse, hashlib, json, struct
from pathlib import Path
EXPECTED='6ea0ed71032ce08fc2745f412d84936382197494'
MAG_SITES=[
    (0x218,'swc1',14,0x8C),
    (0x4E4,'swc1',0,0x8C),
    (0xFE8,'lwc1',4,0x8C),
    (0xFFC,'swc1',8,0x8C),
    (0x1000,'lwc1',10,0x8C),
]
OTHER_SITES=[(0x198,'sh',5,0x6C),(0x1A8,'lhu',4,0x6C),(0x1B0,'swc1',0,0x64)]
OPC={'swc1':0x39,'lwc1':0x31,'sh':0x29,'lhu':0x25}
def check(rom):
    assert len(rom)==33554432
    assert hashlib.sha1(rom).hexdigest()==EXPECTED
    out=[]
    for off,kind,reg,stack in MAG_SITES+OTHER_SITES:
        v=struct.unpack_from('>I',rom,0x589220+off)[0]
        assert v>>26==OPC[kind],(hex(off),'opcode')
        assert (v>>21)&31==29,(hex(off),'stack base')
        assert (v>>16)&31==reg,(hex(off),'register')
        assert (v&0xFFFF)==stack,(hex(off),'stack displacement')
        out.append({'relative_offset':f'0x{off:X}','operation':kind,'register':('f' if kind in ('swc1','lwc1') else '')+str(reg),'stack':f'0x{stack:X}'})
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--json');a=p.parse_args()
    obj={'status':'PASS','size_checked':33554432,'magnitude_lifetime':check(Path(a.rom).read_bytes())}
    if a.json:Path(a.json).write_text(json.dumps(obj,indent=2)+'\n')
    print('ORIGINAL_STACK_SIGNATURES_PASS','sites='+str(len(obj['magnitude_lifetime'])))
