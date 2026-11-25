"""Restore two specific zero-size ABS FUNC annotations from the pristine USA ELF.
Never change code or relocations. Requires original and predecessor agreement.
"""
import struct, hashlib
from pathlib import Path
from decomp.usa_opening_new2_promotion import stable_globals, elf_sections
EXPECTED = {'D_08003690_704790': 0x08003690, 'D_08002360_6C1AB0': 0x08002360}

def restore_inline(path, pristine, predecessor):
    path = Path(path)
    original, prior, current = map(stable_globals, (pristine, predecessor, path))
    before = path.read_bytes()
    buf = bytearray(before)
    secs = elf_sections(before)
    tab, strings = secs['.symtab'], secs['.strtab']
    assert tab['entsize']==16
    records=[]
    for name, addr in EXPECTED.items():
        identity = (f'{addr:08x}', '0', 'FUNC', 'GLOBAL', 'DEFAULT', 'ABS', name)
        split = (*identity[:2], 'NOTYPE', *identity[3:])
        assert original[identity]==prior[identity]==1 and original[split]==prior[split]==0
        assert current[split]==1 and current[identity]==0
        hits=[]
        for i in range(tab['size']//16):
            at=tab['offset']+i*16
            p=strings['offset']+struct.unpack_from('>I',buf,at)[0]
            if buf[p:buf.index(0,p)].decode('ascii')!=name:continue
            assert (struct.unpack_from('>II',buf,at+4),buf[at+12],buf[at+13],struct.unpack_from('>H',buf,at+14)[0])==((addr,0),0x10,0,0xfff1)
            hits.append(at+12)
        assert len(hits)==1
        buf[hits[0]]=0x12
        records.append({'symbol':name,'original_identity':identity,'metadata_byte_offset':hits[0], 'compiler_quirk_outcome':'EXISTING_QUIRK_REPRODUCED','code_and_relocations_unchanged':True})
    assert [i for i,(a,b) in enumerate(zip(before,buf)) if a!=b]==sorted(x['metadata_byte_offset'] for x in records)
    path.write_bytes(buf)
    return records
