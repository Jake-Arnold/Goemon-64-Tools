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

 'japan_matching/jp_wrapper_370B0.c':(('00000008','R_MIPS_26','func_800364D0_370D0'),),
 'japan_matching/jp_wrapper_37178.c':(('00000008','R_MIPS_26','func_80036598_37198'),),
 'japan_matching/jp_wrapper_3757C.c':(('00000008','R_MIPS_26','func_80036A9C_3769C'),),
 'japan_matching/jp_get_3769C.c':(),
 'japan_matching/jp_wrapper_383C4.c':(('0000000c','R_MIPS_26','func_80037890_38490'),),
 'japan_matching/jp_get_3847C.c':(
  ('00000004','R_MIPS_HI16','D_801732E0_173EE0'),
  ('00000010','R_MIPS_LO16','D_801732E0_173EE0')),
 'japan_matching/jp_set_3850C.c':(
  ('00000004','R_MIPS_HI16','D_801732D4_173ED4'),
  ('00000010','R_MIPS_LO16','D_801732D4_173ED4')),
 'japan_matching/jp_wrapper_39584.c':(('00000010','R_MIPS_26','func_800388A0_394A0'),),
 'japan_matching/jp_wrapper_395AC.c':(('00000010','R_MIPS_26','func_800388A0_394A0'),),
 'japan_matching/jp_if_a7ac.c':(
  ('00000000','R_MIPS_HI16','D_801CCE67_1CDA67'),
  ('00000004','R_MIPS_LO16','D_801CCE67_1CDA67'),
  ('00000014','R_MIPS_HI16','D_801CCE66_1CDA66'),
  ('00000018','R_MIPS_LO16','D_801CCE66_1CDA66'),
 ),
 'japan_matching/jp_if_a7d0.c':(
  ('00000000','R_MIPS_HI16','D_801CCE67_1CDA67'),
  ('00000004','R_MIPS_LO16','D_801CCE67_1CDA67'),
  ('0000000c','R_MIPS_HI16','D_801CCE66_1CDA66'),
  ('00000018','R_MIPS_LO16','D_801CCE66_1CDA66'),
 ),
 'japan_matching/jp_if_aa34.c':(
  ('00000000','R_MIPS_HI16','D_801780B6_178CB6'),
  ('00000004','R_MIPS_LO16','D_801780B6_178CB6'),
  ('00000014','R_MIPS_HI16','D_801780B8_178CB8'),
  ('00000018','R_MIPS_LO16','D_801780B8_178CB8'),
 ),
 'japan_matching/jp_if_aa74.c':(
  ('00000000','R_MIPS_HI16','D_801780BA_178CBA'),
  ('00000004','R_MIPS_LO16','D_801780BA_178CBA'),
  ('0000000c','R_MIPS_HI16','D_801780B9_178CB9'),
  ('00000018','R_MIPS_LO16','D_801780B9_178CB9'),
 ),
 'japan_matching/jp_if_aa98.c':(
  ('00000000','R_MIPS_HI16','D_801780BA_178CBA'),
  ('00000004','R_MIPS_LO16','D_801780BA_178CBA'),
  ('0000000c','R_MIPS_HI16','D_801780B9_178CB9'),
  ('00000018','R_MIPS_LO16','D_801780B9_178CB9'),
 ),
 'japan_matching/jp_flag_395D4.c':(
  ('00000000','R_MIPS_HI16','D_801780F8_178CF8'),
  ('00000004','R_MIPS_LO16','D_801780F8_178CF8'),
  ('00000014','R_MIPS_HI16','D_8017EE0E_17FA0E'),
  ('0000001c','R_MIPS_LO16','D_8017EE0E_17FA0E'),
  ('00000020','R_MIPS_HI16','D_8017EE0E_17FA0E'),
  ('00000024','R_MIPS_LO16','D_8017EE0E_17FA0E')),
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
