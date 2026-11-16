"""Exact reviewed .text relocation signatures for Japanese matching-C sources.

Unrecognised C units remain relocation-free; never accept broad wildcards.
"""
from __future__ import annotations
import re

MODE_SOURCE = 'japan_matching/jp_mode_flags.c'
WARP_SOURCE = 'japan_matching/jp_warp_call_37900.c'
MODE_RELOCATIONS = tuple((f'{offset:08x}',kind,'g_system') for offset,kind in (
 (0x04,'R_MIPS_HI16'),(0x0C,'R_MIPS_LO16'),(0x14,'R_MIPS_HI16'),
 (0x1C,'R_MIPS_LO16'),(0x24,'R_MIPS_HI16'),(0x2C,'R_MIPS_LO16')))
WARP_RELOCATIONS = (('00000008','R_MIPS_26','func_8000364C_424C'),)
REVIEWED = {
 MODE_SOURCE:MODE_RELOCATIONS,
 WARP_SOURCE:WARP_RELOCATIONS,
 'japan_matching/jp_transition_37870.c':(
  ('00000000','R_MIPS_HI16','g_system_ptr'),('00000004','R_MIPS_LO16','g_system_ptr'),
  ('00000048','R_MIPS_26','func_8000364C_424C')),
 'japan_matching/jp_warp_37920.c':(
  ('00000000','R_MIPS_HI16','g_system_ptr'),('00000004','R_MIPS_LO16','g_system_ptr'),
  ('00000020','R_MIPS_26','func_8000364C_424C')),
 'japan_matching/jp_warp_37B58.c':(
  ('00000000','R_MIPS_HI16','g_system_ptr'),('00000004','R_MIPS_LO16','g_system_ptr')),
 'japan_matching/jp_warp_37C4C.c':(
  ('00000000','R_MIPS_HI16','g_system_ptr'),('00000004','R_MIPS_LO16','g_system_ptr'),
  ('00000020','R_MIPS_26','func_8000364C_424C')),
 'japan_matching/jp_warp_37C84.c':(
  ('00000000','R_MIPS_HI16','g_system_ptr'),('00000004','R_MIPS_LO16','g_system_ptr')),
 'japan_matching/jp_warp_37CB8.c':(
  ('00000008','R_MIPS_26','func_80003760_4360'),
  ('00000010','R_MIPS_26','func_8000364C_424C')),
 'japan_matching/jp_warp_37CE0.c':(
  ('00000000','R_MIPS_HI16','g_system_ptr'),('00000004','R_MIPS_LO16','g_system_ptr')),
 'japan_matching/jp_state_37D1C.c':(
  ('00000000','R_MIPS_HI16','g_system_ptr'),('00000004','R_MIPS_LO16','g_system_ptr'),
  ('00000028','R_MIPS_26','func_8000364C_424C')),
 'japan_matching/jp_coord_37958.c':(
  ('00000018','R_MIPS_HI16','g_system_ptr'),
  ('0000001c','R_MIPS_LO16','g_system_ptr'),
  ('00000000','R_MIPS_HI16','D_8020151C_5BD4EC'),
  ('00000004','R_MIPS_LO16','D_8020151C_5BD4EC'),
  ('00000054','R_MIPS_HI16','D_80201514_5BD4E4'),
  ('00000098','R_MIPS_LO16','D_80201514_5BD4E4'),
  ('000000b4','R_MIPS_26','func_801FF40C_5BB3DC')),
 'japan_matching/jp_coord_37A24.c':(
  ('00000018','R_MIPS_HI16','g_system_ptr'),
  ('0000001c','R_MIPS_LO16','g_system_ptr'),
  ('00000000','R_MIPS_HI16','D_8020151C_5BD4EC'),
  ('00000004','R_MIPS_LO16','D_8020151C_5BD4EC'),
  ('00000054','R_MIPS_HI16','D_80201514_5BD4E4'),
  ('0000009c','R_MIPS_LO16','D_80201514_5BD4E4'),
  ('000000b8','R_MIPS_26','func_801FF40C_5BB3DC')),
 'japan_matching/jp_state_37AF4.c':(
  ('00000000','R_MIPS_HI16','g_system_ptr'),('00000004','R_MIPS_LO16','g_system_ptr')),
 'japan_matching/jp_warp_37B8C.c':(
  ('00000008','R_MIPS_HI16','g_system_ptr'),('00000014','R_MIPS_LO16','g_system_ptr'),
  ('00000010','R_MIPS_HI16','D_80072EF0_73AF0'),('00000018','R_MIPS_LO16','D_80072EF0_73AF0'),
  ('000000a8','R_MIPS_26','func_8000364C_424C')),
 'japan_matching/jp_state_37D5C.c':(
  ('00000008','R_MIPS_26','func_8000B3E4_BFE4'),
  ('00000018','R_MIPS_26','func_8000364C_424C'),
  ('00000028','R_MIPS_HI16','g_system_ptr'),('0000002c','R_MIPS_LO16','g_system_ptr'),
  ('00000044','R_MIPS_26','func_8000364C_424C')),
 'japan_matching/jp_compare_37EEC.c':(
  ('00000000','R_MIPS_HI16','g_system'),('00000004','R_MIPS_LO16','g_system')),
}
ROW = re.compile(r'(?m)^\s*([0-9a-fA-F]{8})\s+(R_MIPS_[A-Z0-9_]+)\s+(\S+)\s*$')


def verify_text_relocations(source: str, objdump_output: str) -> int:
    observed=tuple((offset.lower(),kind,symbol) for offset,kind,symbol in ROW.findall(objdump_output))
    required=REVIEWED.get(source,())
    if observed!=required:
        raise ValueError(f'Unreviewed Japanese relocations in {source}: {observed!r}')
    if 'RELOCATION RECORDS FOR [.text]' in objdump_output and not observed:
        raise ValueError('Unparsed text relocation table')
    return len(observed)
