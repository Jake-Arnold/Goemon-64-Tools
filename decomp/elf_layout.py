"""Narrow ELF metadata packing for one partially migrated IDO jump table.

Payload bytes are never changed. The 15-word VM assignment table uses 60 bytes;
IDO rounds its isolated .rodata section to 64. Only its logical section size and
alignment are reduced after checking padding, relocations and symbols. No game
image, instruction, jump target or relocation value is patched.
"""
import hashlib
from pathlib import Path
import struct


def pack_vm_assignment_rodata(original):
    if len(original)<52 or original[:7]!=b'\x7fELF\x01\x02\x01':
        raise ValueError('Requires ELF32 big-endian version-1 object')
    if struct.unpack_from('>HH',original,16)!=(1,8):raise ValueError('Requires relocatable MIPS object')
    shoff=struct.unpack_from('>I',original,32)[0]
    entry_size,count,string_index=struct.unpack_from('>HHH',original,46)
    if entry_size!=40 or not count or string_index>=count or shoff+count*40>len(original):
        raise ValueError('Invalid ELF section headers')
    sections=[struct.unpack_from('>10I',original,shoff+i*40) for i in range(count)]
    def payload(section):
        offset,size=section[4:6]
        if offset+size>len(original):raise ValueError('Section payload outside object')
        return original[offset:offset+size]
    names=payload(sections[string_index])
    def name(section):
        start=section[0]
        if start>=len(names) or b'\0' not in names[start:]:raise ValueError('Invalid section name')
        return names[start:].split(b'\0',1)[0]
    def unique(label):
        indices=[i for i,s in enumerate(sections) if name(s)==label]
        if len(indices)!=1:raise ValueError('Missing/duplicate '+label.decode())
        return indices[0]
    text_index=unique(b'.text');ro_index=unique(b'.rodata')
    ro=sections[ro_index];data=payload(ro)
    if ro[1]!=1 or ro[2]!=2 or ro[5]!=64 or ro[8]!=16 or data[60:]!=bytes(4):
        raise ValueError('Unexpected assignment-table section or nonzero padding')
    relocations=[s for s in sections if s[1] in (4,9) and s[7]==ro_index]
    if len(relocations)!=1:raise ValueError('Missing/duplicate table relocation section')
    rel=relocations[0]
    if rel[1]!=9 or rel[9]!=8 or rel[5]!=15*8 or rel[6]>=count:
        raise ValueError('Expected exactly 15 ELF REL entries')
    sym=sections[rel[6]]
    if sym[1]!=2 or sym[9]!=16 or sym[5]%16:raise ValueError('Invalid relocation symbol table')
    symbols=payload(sym);offsets=[]
    for position in range(0,len(payload(rel)),8):
        offset,info=struct.unpack_from('>II',payload(rel),position)
        index=info>>8
        if (info&0xFF)!=2 or index*16+16>len(symbols):raise ValueError('Unexpected table relocation type/symbol')
        _,value,_,kind,_,section=struct.unpack_from('>IIIBBH',symbols,index*16)
        if kind&15!=3 or section!=text_index or value!=0:
            raise ValueError('Table relocation must retain its .text section reference')
        offsets.append(offset)
    if offsets!=list(range(0,60,4)):raise ValueError('Unexpected table relocation offsets')
    for section in sections:
        if section[1]!=2:continue
        if section[9]!=16 or section[5]%16:raise ValueError('Invalid symbol table format')
        for position in range(0,len(payload(section)),16):
            _,value,_,_,_,symbol_section=struct.unpack_from('>IIIBBH',payload(section),position)
            if symbol_section==ro_index and value>=60:raise ValueError('Symbol refers to excluded padding')
    changed=bytearray(original)
    struct.pack_into('>I',changed,shoff+ro_index*40+20,60)
    struct.pack_into('>I',changed,shoff+ro_index*40+32,4)
    allowed=set(range(shoff+ro_index*40+20,shoff+ro_index*40+24))|set(range(shoff+ro_index*40+32,shoff+ro_index*40+36))
    if any(a!=b and i not in allowed for i,(a,b) in enumerate(zip(original,changed))):
        raise AssertionError('Changed bytes outside permitted section metadata')
    result=bytes(changed)
    sha=lambda value:hashlib.sha256(value).hexdigest()
    return result,dict(kind='vm_assignment_rodata_metadata_v1',old_size=64,new_size=60,
        old_alignment=16,new_alignment=4,relocations_retained=15,payload_bytes_changed=0,
        input_sha256=sha(original),output_sha256=sha(result),text_sha256=sha(payload(sections[text_index])),
        compiled_table_prefix_sha256=sha(data[:60]))


def pack_object_file(path):
    path=Path(path);original=path.read_bytes()
    packed,evidence=pack_vm_assignment_rodata(original)
    backup=path.with_name(path.name+'.before-layout')
    with backup.open('xb') as output:output.write(original)
    path.write_bytes(packed)
    return evidence

def pack_heap_noop_text(original):
    """Shrink ONLY the zero-padded .text metadata of the 8-byte MIPS no-op.

    IDO allocates sixteen bytes for an eight-byte return-only function in an
    isolated translation unit. Splat's preserved linker order requires eight.
    The original two instruction words, relocations and all other ELF bytes
    must remain unchanged. This is a pinned, fail-closed layout adjustment.
    """
    from .probe import Elf32

    elf = Elf32(original)
    if elf.kind != 1:
        raise ValueError('Requires relocatable MIPS ELF')
    indices = [i for i, label in enumerate(elf.names) if label == '.text']
    if len(indices) != 1:
        raise ValueError('Expected unique .text section')
    index = indices[0]
    section = elf.sections[index]
    if (section[1], section[2], section[5], section[8]) != (1, 6, 16, 16):
        raise ValueError('Unexpected empty-function section layout')
    payload = elf.payload(index)
    if payload != bytes.fromhex('03E0000800000000') + bytes(8):
        raise ValueError('Unexpected MIPS function or nonzero padding')
    if any(s[1] in (4, 9) for s in elf.sections):
        raise ValueError('Unexpected relocations in empty-function object')
    functions = [s for s in elf.symbols if s.kind == 2 and s.section != 0]
    if len(functions) != 1 or (functions[0].name, functions[0].value,
                               functions[0].size, functions[0].section,
                               functions[0].binding) != (
                               'func_80035D84_36984', 0, 8, index, 1):
        raise ValueError('Unexpected empty-function symbol layout')
    if any(s.section == index and s.kind not in (2, 3) for s in elf.symbols):
        raise ValueError('Unexpected additional symbol in .text')
    if any(s.section == index and s.kind == 3 and (s.value, s.size) != (0, 16)
           for s in elf.symbols):
        raise ValueError('Unexpected .text section symbol')
    for i, s in enumerate(elf.sections):
        if i != index and s[2] & 2 and s[5] and elf.names[i] not in ('.reginfo',):
            raise ValueError('Unexpected additional allocated data')
    header_offset = struct.unpack_from('>I', original, 32)[0]
    entry_width = struct.unpack_from('>H', original, 46)[0]
    patched = bytearray(original)
    struct.pack_into('>I', patched, header_offset + index * entry_width + 20, 8)
    struct.pack_into('>I', patched, header_offset + index * entry_width + 32, 4)
    permitted = (set(range(header_offset + index * entry_width + 20,
                          header_offset + index * entry_width + 24)) |
                 set(range(header_offset + index * entry_width + 32,
                           header_offset + index * entry_width + 36)))
    if any(a != b and i not in permitted for i, (a, b) in enumerate(zip(original, patched))):
        raise AssertionError('Changed bytes outside approved ELF metadata')
    return bytes(patched), dict(kind='heap_noop_text_metadata_v1', old_size=16,
        new_size=8, old_alignment=16, new_alignment=4,
        payload_bytes_changed=0,
        input_sha256=hashlib.sha256(original).hexdigest(),
        output_sha256=hashlib.sha256(patched).hexdigest(),
        function_sha256=hashlib.sha256(payload[:8]).hexdigest())


def pack_heap_noop_file(path):
    path = Path(path)
    original = path.read_bytes()
    packed, evidence = pack_heap_noop_text(original)
    backup = path.with_name(path.name + '.before-heap-noop-layout')
    with backup.open('xb') as output:
        output.write(original)
    path.write_bytes(packed)
    return evidence
