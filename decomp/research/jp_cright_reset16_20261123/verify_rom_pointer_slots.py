#!/usr/bin/env python3
"""Prove the original USA and Japan system pointer *slot* addresses.

Reads user-provided retail ROMs, not emulator RAM. Does not embed ROM bytes,
patch code, mutate memory, or claim the pointed-to structure is a fixed global.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path

SHA = {
    'usa': 'df8083a54296b8c151917c5333e1c85f014a2a66',
    'japan': '9843ee979b5f6c80f5eda85df0baed9ae7c4e73b',
}
EXPECTED = {'usa': 0x8015C5C8, 'japan': 0x80161DB8}

def sign16(v):
    return v - 0x10000 if v & 0x8000 else v

def op(w):
    return (w >> 26) & 0x3f

def rs(w):
    return (w >> 21) & 0x1f

def rt(w):
    return (w >> 16) & 0x1f

def imm(w):
    return w & 0xffff

def read_u32(blob, off):
    return struct.unpack_from('>I', blob, off)[0]

def prove(region, blob):
    if len(blob) != 16777216 or blob[:4] != b'\x80\x37\x12\x40':
        raise ValueError(f'{region}: not 16 MiB native big-endian N64 retail image')
    digest = hashlib.sha1(blob).hexdigest()
    if digest != SHA[region]:
        raise ValueError(f'{region}: SHA1 mismatch {digest}; wrong ROM revision')
    if region == 'japan':
        # Original Japan func_80004170_4D70 starts with LUI $v0,hi + LW $v0,lo($v0).
        hi, lo = read_u32(blob, 0x4D70), read_u32(blob, 0x4D74)
        if (op(hi), rs(hi), rt(hi)) != (15,0,2):
            raise ValueError('Japan 0x4D70 is not expected LUI $v0')
        if (op(lo), rs(lo), rt(lo)) != (35,2,2):
            raise ValueError('Japan 0x4D74 is not expected LW $v0,offset($v0)')
        address = (imm(hi) << 16) + sign16(imm(lo))
        kind='read'
        fn='func_80004170_4D70'
    else:
        # USA func_80004170_4D70 initializes the global: LUI/Addiu then SW.
        hi, lo, store = (read_u32(blob,x) for x in (0x4D8C,0x4D94,0x4D9C))
        if (op(hi), rs(hi), rt(hi)) != (15,0,2):
            raise ValueError('USA 0x4D8C is not expected LUI $v0')
        if (op(lo), rs(lo), rt(lo)) != (9,2,2):
            raise ValueError('USA 0x4D94 is not expected ADDIU $v0,$v0,offset')
        if (op(store), rs(store),imm(store)) != (43,2,0):
            raise ValueError('USA 0x4D9C is not expected SW at pointer-slot address')
        address = (imm(hi) << 16) + sign16(imm(lo))
        kind='write'
        fn='func_80004170_4D70'
    address &= 0xffffffff
    if address != EXPECTED[region]:
        raise ValueError(f'{region} pointer slot {address:#010x} != expected {EXPECTED[region]:#010x}')
    return {'region':region,'rom_sha1':digest,'rom_bytes':len(blob),'symbol_slot':f'0x{address:08X}', 'access':kind,'original_function':fn,'source':'original retail MIPS, register/operand decoding at authenticated fixed offsets'}

def verify(usa, japan):
    u=prove('usa',usa)
    j=prove('japan',japan)
    if int(j['symbol_slot'],16)-int(u['symbol_slot'],16) != 0x57f0:
        raise ValueError('independently decoded slots lack regional +0x57F0 relation')
    return {'status':'ORIGINAL_ROM_INSTRUCTION_VERIFIED','usa':u,'japan':j,'slot_delta':'0x000057F0','width_bytes':4,'endian':'big','pointed_to_record_offset':'0x3B168 (DYNAMIC POINTER RELATIVE; NOT FIXED RAM ADDRESS)', 'gameplay_live_counterpart':'NOT_RUN', 'automated_memory_write':False}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--usa-rom',type=Path,required=True)
    parser.add_argument('--japan-rom',type=Path,required=True)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    result=verify(args.usa_rom.read_bytes(), args.japan_rom.read_bytes())
    if args.report:
        if args.report.exists(): raise FileExistsError(args.report)
        args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':main()
