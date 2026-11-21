#!/usr/bin/env python3
"""Compare original file22 MIPS per-tile page/tile lookup with independent arithmetic.

Original ROM is required locally; it is neither printed nor included in reports.
Synthetic guest memory and a small MIPS-I interpreter are used; NOT a game frame.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
from pathlib import Path
import struct
from trace_original_file22_mips import OriginalMIPS,prepare,ROM_SHA1,SAVED_DESC

PAGE_LOAD = 0x801CC3AC  # original lbu t5, 0(t9)
TILE_LOAD = 0x801CC404  # original lhu t4, 0(t8)

def signed16(x):
    x &= 0xFFFF
    return x - 0x10000 if x & 0x8000 else x

def trunc_div(a,b):
    if b == 0:
        raise ZeroDivisionError
    return (abs(a)//abs(b)) * (-1 if ((a<0) != (b<0)) else 1)

def trunc_rem(a,b):
    return a-trunc_div(a,b)*b

class LookupMachine(OriginalMIPS):
    def __init__(self,ram):
        super().__init__(ram)
        self.page_observations=[]
        self.tile_observations=[]
    def execute(self,pc,delay=False):
        if pc in (PAGE_LOAD,TILE_LOAD):
            row=self.ram.load(self.r[29]+0x138)
            column=self.r[20]
            addr=self.r[25] if pc==PAGE_LOAD else self.r[24]
        result=super().execute(pc,delay)
        if pc==PAGE_LOAD:
            self.page_observations.append((row,column,addr,self.r[13]))
        if pc==TILE_LOAD:
            self.tile_observations.append((row,column,addr,self.r[12]))
        return result

def verify(rom, mode, rows=None, layout=None):
    memory=prepare(rom,mode,rows,layout)
    machine=LookupMachine(memory)
    machine.run()
    descriptor=lambda off: memory.load(SAVED_DESC+off)
    grid_w,grid_h,pixel_w,pixel_h=(signed16(memory.load(SAVED_DESC+off,2)) for off in (0x1c,0x1e,0x20,0x22))
    pagebase=descriptor(4)
    tilebase=descriptor(8)
    if min(grid_w,grid_h,pixel_w,pixel_h)<=0:
        raise ValueError('Lookup test requires positive geometry')
    tile_w=trunc_div(pixel_w,32)
    tile_h=trunc_div(pixel_h,32)
    if len(machine.page_observations)!=80 or len(machine.tile_observations)!=80:
        raise AssertionError(f'Unexpected lookup count: {len(machine.page_observations)} / {len(machine.tile_observations)}')
    compared=0
    digest=hashlib.sha256()
    for page,tile in zip(machine.page_observations,machine.tile_observations):
        row,col,pageaddr,pageid=page
        trow,tcol,tileaddr,tileid=tile
        if row!=trow or col!=tcol:
            raise AssertionError(f'Page/tile event pairing differs {page} {tile}')
        x=32*col;y=32*row
        px=trunc_rem(trunc_div(x,pixel_w),grid_w)
        py=trunc_rem(trunc_div(y,pixel_h),grid_h)
        expected_page_addr=pagebase+px+grid_w*py
        if pageaddr!=expected_page_addr:
            raise AssertionError(f'Page pointer mismatch row={row} col={col}, original={pageaddr:#x}, expected={expected_page_addr:#x}')
        expected_page_id=memory.load(expected_page_addr,1)
        if pageid!=expected_page_id:
            raise AssertionError(f'Page ID mismatch row={row} col={col}: {pageid} != {expected_page_id}')
        local_x=trunc_div(trunc_rem(x,pixel_w),32)
        local_y=trunc_div(trunc_rem(y,pixel_h),32)
        index=pageid*tile_w*tile_h+local_y*tile_w+local_x
        expected_tile_addr=tilebase+index*2
        if tileaddr!=expected_tile_addr:
            raise AssertionError(f'Tile pointer mismatch row={row} col={col}: original={tileaddr:#x}, expected={expected_tile_addr:#x}')
        expected_tile_id=memory.load(expected_tile_addr,2)
        if tileid!=expected_tile_id:
            raise AssertionError(f'Tile ID mismatch row={row} col={col}: {tileid} != {expected_tile_id}')
        digest.update(struct.pack('>IIHIH',pageaddr&0xffffffff,expected_page_addr&0xffffffff,pageid&0xffff,tileaddr&0xffffffff,tileid&0xffff))
        compared+=1
    return {'mode':mode,'layout':'original' if layout is None else [*layout[:4]],
      'rows':'original' if rows is None else 'synthetic',
      'tile_lookup_records_exact':compared,'page_address_mismatches':0,'tile_address_mismatches':0,
      'page_id_mismatches':0,'tile_id_mismatches':0,
      'lookup_record_sha256':digest.hexdigest()}

def suite(rom):
    results=[]
    scenarios=[
       (None,None),([0,4,0,3,2,1,4,0],None),([0]*8,None),
       (None,(2,2,160,128,[0,1,2,3])),
       (None,(5,4,64,64,[i%4 for i in range(20)])),
    ]
    for mode in (0,1,2,3):
        for rows,layout in scenarios:
            results.append(verify(rom,mode,rows,layout))
    return {'case_count':len(results),'original_mips_page_and_tile_pairs':sum(r['tile_lookup_records_exact'] for r in results),
            'all_exact':True,'subcases':results}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rom',type=Path,required=True)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    rom=args.rom.read_bytes()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=ROM_SHA1:
        raise SystemExit('Original-USA 32 MiB ROM mismatch')
    result=suite(rom)
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(f"PASS: {result['case_count']} cases, {result['original_mips_page_and_tile_pairs']} page+tile lookup records, exact address and ID checks")
if __name__=='__main__': main()
