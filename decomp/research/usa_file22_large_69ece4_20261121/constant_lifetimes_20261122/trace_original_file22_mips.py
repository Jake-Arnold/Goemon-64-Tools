#!/usr/bin/env python3
"""Read-only reproduction of the ORIGINAL USA file-22 function in a minimal
MIPS-I integer interpreter, with a synthetic display-list destination.

This is a behavioural research tool, not a hardware or emulator equivalence
claim. Original ROM, emitted assets, original asm and object bytes are NOT
bundled. Runtime memory setup is synthetic. The function has no jal/jalr calls.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, struct
from pathlib import Path

ROM_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
FUNCTION_SHA256 = 'eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9'
FILE22_ROM = 0x69e080
FILE22_VMA = 0x801cb460
FILE22_LEN = 47264
ENTRY = 0x801cc0c4
END = 0x801cc7d4
DESC_STATIC = 0x801d536c
CURSOR = 0x801d701c
SAVED_DESC = 0x801d7030
OUTPUT = 0x80300000
STACK = 0x803fe000
EXIT = 0x80001100
U32 = 0xffffffff


def u32(x):return x & U32

def s32(x):
    x &= U32
    return x-(1 << 32) if x & 0x80000000 else x


def sx16(x):
    x &= 65535
    return x-65536 if x & 32768 else x


def div_signed(a,b):
    a,b=s32(a),s32(b)
    # MIPS div is not a trapping instruction. The original compiler emits
    # explicit break 7 / break 6 guards *after* div; leave HI/LO arbitrary
    # on invalid input and let that original guard execute.
    if not b or (a==-2147483648 and b==-1):return 0,0
    q=(abs(a)//abs(b))*(-1 if (a<0)^(b<0) else 1)
    return u32(q),u32(a-q*b)

class Memory:
    def __init__(self, source:bytes):
        self.blocks = [
            (FILE22_VMA, bytearray(source)),
            (FILE22_VMA + FILE22_LEN, bytearray(0x700)),
            (OUTPUT, bytearray(64*1024)),
            (STACK, bytearray(0x2000)),
        ]
    def block(self,addr,n=1):
        for base,data in self.blocks:
            if base<=addr and addr+n<=base+len(data):return data,addr-base
        raise MemoryError(f'Unmapped guest address {addr:#010x}, length={n}')
    def load(self,addr,n=4,signed=False):
        if (n==4 and addr%4) or (n==2 and addr%2):raise MemoryError(f'Misaligned read {addr:#x}/{n}')
        b,i=self.block(addr,n)
        x=int.from_bytes(b[i:i+n],'big')
        if signed and x & (1<<(n*8-1)):x-=1<<(n*8)
        return u32(x)
    def store(self,addr,value,n=4):
        if (n==4 and addr%4) or (n==2 and addr%2):raise MemoryError(f'Misaligned write {addr:#x}/{n}')
        b,i=self.block(addr,n)
        b[i:i+n]=(value&((1<<(n*8))-1)).to_bytes(n,'big')

class OriginalMIPS:
    def __init__(self,ram):
        self.ram=ram
        self.r=[0]*32
        self.hi=self.lo=0
        self.pc=ENTRY
        self.r[4]=SAVED_DESC
        self.r[29]=STACK+0x1ff0
        self.r[31]=EXIT
        self.executed=0
        self.pc_count=collections.Counter()
        self.op_count=collections.Counter()
        self.div_results=collections.Counter()
        self.branch_count=collections.Counter()

    def reg(self,index):return self.r[index]
    def put(self,index,value):
        if index:self.r[index]=u32(value)

    def execute(self,pc,delay=False):
        w=self.ram.load(pc)
        op=(w>>26)&63;rs=(w>>21)&31;rt=(w>>16)&31;rd=(w>>11)&31;sa=(w>>6)&31;fn=w&63
        si=sx16(w);z=w&65535
        a=self.r[rs];b=self.r[rt]
        self.executed+=1;self.pc_count[pc]+=1
        self.op_count[op]+=1
        branch=None;likely=False
        target=u32(pc+4+(si<<2))
        if op==0:
            if fn==0: self.put(rd,b<<sa)                  # sll (nop)
            elif fn==3: self.put(rd,s32(b)>>sa)         # sra
            elif fn==8:branch=a                         # jr
            elif fn==13:raise ArithmeticError(f'Original MIPS break at {pc:#x}')
            elif fn==16:self.put(rd,self.hi)            # mfhi
            elif fn==18:self.put(rd,self.lo)            # mflo
            elif fn==25:                                  # multu
                prod=a*b;self.lo=u32(prod);self.hi=u32(prod>>32)
            elif fn==26:                                  # div
                self.lo,self.hi=div_signed(a,b)
                self.div_results[pc]+=1
            elif fn==33:self.put(rd,a+b)               # addu
            elif fn==35:self.put(rd,a-b)               # subu / negu
            elif fn==37:self.put(rd,a|b)               # or
            elif fn==42:self.put(rd,int(s32(a)<s32(b))) # slt
            elif fn==43:self.put(rd,int(a<b))           # sltu
            else:raise NotImplementedError(f'R {fn} @ {pc:#x} {w:#010x}')
        elif op==1:                                       # regimm
            if rt==0:branch=target if s32(a)<0 else None # bltz
            elif rt==1:branch=target if s32(a)>=0 else None # bgez
            else:raise NotImplementedError(f'REGIMM {rt} @ {pc:#x}')
            # non-likely conditional branches still execute delay slot
            self.branch_count[pc]+=1
            return ('conditional',branch,False)
        elif op in (4,5,20,21):                             # beq/bne/beql
            cond=(a==b) if op in (4,20) else (a!=b)
            branch=target if cond else None
            likely=(op in (20,21))
            self.branch_count[pc]+=1
            return ('conditional',branch,likely)
        elif op==9:self.put(rt,a+si)                     # addiu
        elif op==10:self.put(rt,int(s32(a)<si))          # slti
        elif op==11:self.put(rt,int(a<u32(si)))          # sltiu (sign-extended imm)
        elif op==12:self.put(rt,a&z)                     # andi
        elif op==13:self.put(rt,a|z)                     # ori
        elif op==15:self.put(rt,z<<16)                   # lui
        elif op==32:self.put(rt,self.ram.load(u32(a+si),1,True))  # lb
        elif op==33:self.put(rt,self.ram.load(u32(a+si),2,True))  # lh
        elif op==35:self.put(rt,self.ram.load(u32(a+si),4))       # lw
        elif op==36:self.put(rt,self.ram.load(u32(a+si),1))       # lbu
        elif op==37:self.put(rt,self.ram.load(u32(a+si),2))       # lhu
        elif op==40:self.ram.store(u32(a+si),b,1)                 # sb (used by O1 diagnostic)
        elif op==41:self.ram.store(u32(a+si),b,2)                 # sh (used by O1 diagnostic)
        elif op==43:self.ram.store(u32(a+si),b)                   # sw
        else:raise NotImplementedError(f'Opcode {op} @ {pc:#x} {w:#010x}')
        if branch is not None:
            self.branch_count[pc]+=1
            return ('jump',branch,False)
        return None

    def run(self,limit=1000000):
        for _ in range(limit):
            pc=self.pc
            if not ENTRY<=pc<END:raise RuntimeError(f'Guest PC escaped function before return: {pc:#x}')
            v=self.execute(pc)
            if v is None:self.pc=u32(pc+4);continue
            kind,target,likely=v
            if kind=='conditional':
                if target is None and likely:self.pc=pc+8;continue
                if target is None:target=pc+8
            else:
                assert kind=='jump'
            if pc+4>=END:raise RuntimeError('Missing delay slot')
            x=self.execute(pc+4,delay=True)
            if x:raise RuntimeError(f'Branch in branch delay slot {pc+4:#x}')
            if target==EXIT:return
            self.pc=u32(target)
        raise TimeoutError(f'Exceeded {limit} original guest instructions')


def prepare(rom,mode=2,mutate_rows=None,layout=None):
    assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM_SHA1
    assert hashlib.sha256(rom[0x69ece4:0x69f3f4]).hexdigest()==FUNCTION_SHA256
    ram=Memory(rom[FILE22_ROM:FILE22_ROM+FILE22_LEN])
    for i in range(36):ram.store(SAVED_DESC+i,ram.load(DESC_STATIC+i,1),1)
    ram.store(SAVED_DESC+0x1a,mode,1)
    if layout is not None:
        cols,rows,width,height,pages=layout
        assert cols>=1 and rows>=1 and width>0 and height>0 and len(pages)==cols*rows
        assert len(pages)<=64 and all(0<=v<=3 for v in pages)
        for offset,value in ((0x1c,cols),(0x1e,rows),(0x20,width),(0x22,height)):
            ram.store(SAVED_DESC+offset,value,2)
        pageaddr=ram.load(SAVED_DESC+4)
        for i,page in enumerate(pages):ram.store(pageaddr+i,page,1)
    if mutate_rows is not None:
        assert len(mutate_rows)==8 and all(0<=v<=4 for v in mutate_rows)
        tilemap=ram.load(SAVED_DESC+8)
        for y,v in enumerate(mutate_rows):
            for x in range(10):ram.store(tilemap+(y*10+x)*2,v,2)
    ram.store(CURSOR,OUTPUT)
    return ram


def run_once(rom,mode=2,rows=None,layout=None):
    ram=prepare(rom,mode,rows,layout)
    machine=OriginalMIPS(ram)
    machine.run()
    final=ram.load(CURSOR)
    if not OUTPUT<=final<OUTPUT+65536 or (final-OUTPUT)%8:raise AssertionError('Invalid display-list pointer')
    records=[(ram.load(OUTPUT+8*i),ram.load(OUTPUT+8*i+4)) for i in range((final-OUTPUT)//8)]
    groups=collections.Counter(hex(x>>24) for x,_ in records)
    result={
       'format':mode,
       'synthetic_environment':True,
       'original_guest_instructions_executed':machine.executed,
       'distinct_original_pc_addresses_executed':len(machine.pc_count),
       'original_signed_division_events':sum(machine.div_results.values()),
       'display_list_command_count':len(records),
       'display_list_byte_count':len(records)*8,
       'opcode_high_byte_counts':dict(sorted(groups.items())),
       'texture_setup_count':sum(1 for w0,w1 in records if w0>>24 in (0xfd,)),
       'texture_rect_count':sum(1 for w0,w1 in records if w0>>24==0xe4),
       'first_8_gfx':[f'{w0:08X} {w1:08X}' for w0,w1 in records[:8]],
       'last_4_gfx':[f'{w0:08X} {w1:08X}' for w0,w1 in records[-4:]],
       'original_gfx_wordstream_sha256':hashlib.sha256(b''.join(struct.pack('>II',*w) for w in records)).hexdigest(),
       'executed_pc_profile':[(f'{pc:#010x}',c) for pc,c in sorted(machine.pc_count.items())],
       'branch_execution_counts':[(f'{pc:#010x}',c) for pc,c in sorted(machine.branch_count.items())],
    }
    return result,records


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--rom',required=True,type=Path,help='Authenticated 32MiB original USA decompressed ROM')
    a.add_argument('--output',type=Path)
    a.add_argument('--mode',type=int,choices=[0,1,2],default=2)
    a.add_argument('--show-profile',action='store_true')
    args=a.parse_args()
    r,_=run_once(args.rom.read_bytes(),args.mode)
    if not args.show_profile:
        r.pop('executed_pc_profile');r.pop('branch_execution_counts')
    if args.output:args.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
if __name__=='__main__':main()
