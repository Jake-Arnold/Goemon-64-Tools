"""PJ64-style *guest-memory* debugger for the Goemon native recomp toolkit.

Operates only on the existing 8 MiB Rdram.read_guest/write_guest interface.
No CPU register, emulated PC, execute-breakpoint or MIPS-step data is exposed by
an uninstrumented statically recompiled host. Never infer those from RAM.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re

RAM_SIZE = 0x800000
MAX_WATCHES = 64
MAX_EVENTS = 500
REGS = ("zero", "at", "v0", "v1", "a0", "a1", "a2", "a3",
        "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
        "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
        "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra")


def guest_address(value: str | int, length: int = 1, *, alignment: int = 1) -> int:
    """Accept explicit N64 KSEG0/KSEG1 addresses; reject wrap and MMIO."""
    if type(value) is int:
        address = value
    elif isinstance(value, str) and re.fullmatch(r'(?:0[xX])?[0-9a-fA-F]{1,8}', value.strip()):
        address = int(value.strip().removeprefix('0x').removeprefix('0X'), 16)
    else:
        raise ValueError('Enter a hexadecimal N64 KSEG0/KSEG1 address')
    if type(length) is not int or length <= 0 or type(alignment) is not int or alignment <= 0:
        raise ValueError('Invalid length or alignment')
    if (address & 0xE0000000) not in (0x80000000, 0xA0000000):
        raise ValueError('Address must be in KSEG0/KSEG1 RDRAM')
    offset = address & 0x1FFFFFFF
    if offset + length > RAM_SIZE or address % alignment:
        raise ValueError('Address outside RDRAM or misaligned')
    return address


def hex_bytes(text: str) -> bytes:
    """Parse a sequence of whole hex bytes, with optional spaces and 0x."""
    cleaned = re.sub(r'\s+', '', text.strip())
    if cleaned.lower().startswith('0x'):
        cleaned = cleaned[2:]
    if not cleaned or len(cleaned) % 2 or not re.fullmatch(r'[0-9a-fA-F]+', cleaned):
        raise ValueError('Hex bytes require pairs of hexadecimal digits')
    return bytes.fromhex(cleaned)


def memory_rows(ram, address: int, count: int = 16) -> list[tuple[int, str, str]]:
    """One batch read, canonical guest order, 16 bytes per row."""
    if type(count) is not int or not 1 <= count <= 256:
        raise ValueError('Page row count must be 1..256')
    base = guest_address(address, 1) & ~0xF
    remaining = RAM_SIZE - (base & 0x1FFFFFFF)
    size = min(count * 16, remaining)
    data = ram.read_guest(base, size)
    if len(data) != size:
        raise OSError('Incomplete guest RAM read')
    return [(base + off, ' '.join(f'{b:02X}' for b in data[off:off+16]),
             ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[off:off+16]))
            for off in range(0, len(data), 16)]


def _sign16(v: int) -> int:
    return v - 0x10000 if v & 0x8000 else v


def mips_instruction(pc: int, word: int) -> str:
    """Decode established MIPS III integer opcodes; unknown opcodes are .word."""
    op = (word >> 26) & 63
    rs, rt, rd = (word >> 21) & 31, (word >> 16) & 31, (word >> 11) & 31
    sh, fn, imm = (word >> 6) & 31, word & 63, word & 0xFFFF
    r = lambda n: '$' + REGS[n]
    si = _sign16(imm)
    if word == 0:
        return 'nop'
    if op == 0:
        shift = {0:'sll',2:'srl',3:'sra',56:'dsll',58:'dsrl',59:'dsra',60:'dsll32',62:'dsrl32',63:'dsra32'}
        varshift = {4:'sllv',6:'srlv',7:'srav',20:'dsllv',22:'dsrlv',23:'dsrav'}
        three = {32:'add',33:'addu',34:'sub',35:'subu',36:'and',37:'or',38:'xor',39:'nor',42:'slt',43:'sltu',44:'dadd',45:'daddu',46:'dsub',47:'dsubu'}
        two = {24:'mult',25:'multu',26:'div',27:'divu',28:'dmult',29:'dmultu',30:'ddiv',31:'ddivu'}
        fromreg = {16:'mfhi',18:'mflo'}
        toreg = {17:'mthi',19:'mtlo'}
        if fn in shift: return f'{shift[fn]} {r(rd)}, {r(rt)}, {sh}'
        if fn in varshift: return f'{varshift[fn]} {r(rd)}, {r(rt)}, {r(rs)}'
        if fn in three: return f'{three[fn]} {r(rd)}, {r(rs)}, {r(rt)}'
        if fn in two: return f'{two[fn]} {r(rs)}, {r(rt)}'
        if fn in fromreg: return f'{fromreg[fn]} {r(rd)}'
        if fn in toreg: return f'{toreg[fn]} {r(rs)}'
        if fn == 8: return f'jr {r(rs)}'
        if fn == 9: return f'jalr {r(rd)}, {r(rs)}'
        if fn == 12: return 'syscall'
        if fn == 13: return 'break'
        if fn == 15: return 'sync'
    if op == 1:
        regimm = {0:'bltz',1:'bgez',2:'bltzl',3:'bgezl',16:'bltzal',17:'bgezal',18:'bltzall',19:'bgezall'}
        if rt in regimm:
            return f'{regimm[rt]} {r(rs)}, 0x{(pc+4+(si<<2))&0xFFFFFFFF:08X}'
    if op in (2,3):
        target = ((pc+4)&0xF0000000)|((word&0x03FFFFFF)<<2)
        return f'{"j" if op == 2 else "jal"} 0x{target:08X}'
    if op in (4,5,20,21):
        name = {4:'beq',5:'bne',20:'beql',21:'bnel'}[op]
        return f'{name} {r(rs)}, {r(rt)}, 0x{(pc+4+(si<<2))&0xFFFFFFFF:08X}'
    if op in (6,7,22,23):
        name = {6:'blez',7:'bgtz',22:'blezl',23:'bgtzl'}[op]
        return f'{name} {r(rs)}, 0x{(pc+4+(si<<2))&0xFFFFFFFF:08X}'
    immed = {8:'addi',9:'addiu',10:'slti',11:'sltiu',12:'andi',13:'ori',14:'xori',24:'daddi',25:'daddiu'}
    if op in immed:
        val = f'0x{imm:04X}' if op in (12,13,14) else str(si)
        return f'{immed[op]} {r(rt)}, {r(rs)}, {val}'
    if op == 15:
        return f'lui {r(rt)}, 0x{imm:04X}'
    loads = {32:'lb',33:'lh',34:'lwl',35:'lw',36:'lbu',37:'lhu',38:'lwr',39:'lwu',
             40:'sb',41:'sh',42:'swl',43:'sw',44:'sdl',45:'sdr',46:'swr',
             48:'ll',49:'lwc1',52:'lld',53:'ldc1',55:'ld',56:'sc',57:'swc1',60:'scd',61:'sdc1',63:'sd'}
    if op in loads:
        register = f'$f{rt}' if op in (49,53,57,61) else r(rt)
        return f'{loads[op]} {register}, {si}({r(rs)})'
    if op == 16:
        if rs == 0: return f'mfc0 {r(rt)}, ${rd}'
        if rs == 4: return f'mtc0 {r(rt)}, ${rd}'
        if word == 0x42000018: return 'eret'
    if op == 17:
        if rs == 0: return f'mfc1 {r(rt)}, $f{rd}'
        if rs == 2: return f'cfc1 {r(rt)}, ${rd}'
        if rs == 4: return f'mtc1 {r(rt)}, $f{rd}'
        if rs == 6: return f'ctc1 {r(rt)}, ${rd}'
        if rs == 8:
            name = ('bc1f','bc1t','bc1fl','bc1tl')[rt & 3]
            if rt <= 3: return f'{name} 0x{(pc+4+(si<<2))&0xFFFFFFFF:08X}'
        if rs in (16,17):
            fmt = '.s' if rs == 16 else '.d'
            fd = (word>>6)&31
            arithmetic = {0:'add',1:'sub',2:'mul',3:'div',4:'sqrt',5:'abs',6:'mov',7:'neg'}
            if fn in arithmetic:
                if fn <= 3: return f'{arithmetic[fn]}{fmt} $f{fd}, $f{rd}, $f{rt}'
                return f'{arithmetic[fn]}{fmt} $f{fd}, $f{rd}'
    return f'.word 0x{word:08X}'


def disassembly(ram, address: int, count: int = 48) -> list[tuple[int, str, str]]:
    if type(count) is not int or not 1 <= count <= 256:
        raise ValueError('Instruction count must be 1..256')
    guest_address(address, 4, alignment=4)
    size = min(count * 4, RAM_SIZE - (address & 0x1FFFFFFF))
    data = ram.read_guest(address, size)
    if len(data) != size:
        raise OSError('Incomplete instruction-byte read')
    return [(address+i, data[i:i+4].hex().upper(),
             mips_instruction(address+i, int.from_bytes(data[i:i+4],'big')))
            for i in range(0, len(data), 4)]


def search_guest(ram, needle: bytes, start: int = 0x80000000,
                 length: int = RAM_SIZE, *, limit: int = 512,
                 chunk_size: int = 65536) -> list[int]:
    """Find an exact byte sequence with overlap across chunks. No ROM scan."""
    if not isinstance(needle, bytes) or not needle or len(needle) > 256:
        raise ValueError('Search pattern must contain 1..256 bytes')
    guest_address(start, length)
    if type(limit) is not int or not 1 <= limit <= 10000:
        raise ValueError('Invalid result limit')
    if type(chunk_size) is not int or chunk_size < len(needle):
        raise ValueError('Chunk size must fit the pattern')
    hits, tail, position, end = [], b'', start, start + length
    while position < end and len(hits) < limit:
        size = min(chunk_size, end-position)
        block = ram.read_guest(position,size)
        if len(block) != size:
            raise OSError('Incomplete memory scan read')
        combined = tail + block
        base = position-len(tail)
        at = 0
        while len(hits) < limit:
            idx = combined.find(needle,at)
            if idx < 0: break
            addr = base+idx
            if addr >= start and addr+len(needle) <= end:
                hits.append(addr)
            at = idx+1
        tail = combined[-(len(needle)-1):] if len(needle)>1 else b''
        position += size
    return hits


@dataclass(frozen=True)
class ChangeEvent:
    timestamp: str
    address: int
    before: str
    after: str

    def export(self) -> dict:
        return {'utc':self.timestamp,'address':f'0x{self.address:08X}',
                'before':self.before,'after':self.after}


class DebuggerSession:
    """Memory polling is not a CPU watchpoint. Session-bound, RAM-only."""
    def __init__(self):
        self.ram = None
        self.watches: dict[int, bytes] = {}
        self.events: list[ChangeEvent] = []

    def attach(self, ram):
        if ram is not self.ram:
            self.ram = ram
            self.watches.clear()
            self.events.clear()

    def add_watch(self, address: int, width: int):
        if self.ram is None: raise RuntimeError('Not connected')
        if width not in (1,2,4,8): raise ValueError('Width must be 1, 2, 4, or 8')
        guest_address(address,width)
        if address not in self.watches and len(self.watches)>=MAX_WATCHES:
            raise ValueError('Too many change watches')
        self.watches[address] = self.ram.read_guest(address,width)

    def remove_watch(self, address: int):
        self.watches.pop(address, None)

    def poll(self) -> list[ChangeEvent]:
        if self.ram is None: return []
        updated=[]
        for addr,old in list(self.watches.items()):
            new=self.ram.read_guest(addr,len(old))
            if len(new)!=len(old):raise OSError('Incomplete change-watch read')
            if new == old:continue
            event=ChangeEvent(datetime.now(timezone.utc).isoformat(timespec='milliseconds'),addr,
                              old.hex().upper(),new.hex().upper())
            self.watches[addr]=new
            self.events.append(event)
            updated.append(event)
        if len(self.events)>MAX_EVENTS:
            del self.events[:-MAX_EVENTS]
        return updated

    def write(self, address: int, expected: bytes, new: bytes, *, writable: bool):
        """Guard raw bytes against stale UI state and disabled writes."""
        if not writable: raise PermissionError('Toolkit is in read-only mode')
        if self.ram is None: raise RuntimeError('Not connected')
        if not isinstance(expected,bytes) or not isinstance(new,bytes) or len(new) not in (1,2,4,8) or len(expected)!=len(new):
            raise ValueError('Raw writes require 1, 2, 4, or 8 bytes')
        guest_address(address,len(new))
        if self.ram.read_guest(address,len(new)) != expected:
            raise RuntimeError('Memory changed before write; refresh and retry')
        if new == expected:return False
        self.ram.write_guest(address,new)
        if self.ram.read_guest(address,len(new)) != new:
            raise OSError('Write readback mismatch')
        return True
