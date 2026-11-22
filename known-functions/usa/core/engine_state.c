#include "common.h"
extern s8 D_801C09CE_1C15CE, D_801C09DA_1C15DA, D_801C09DB_1C15DB;
extern u8 D_801C09CF_1C15CF, D_801C09DC_1C15DC;
extern u16 D_801C09D8_1C15D8;
void func_80039F3C_3AB3C(void) { if (D_801C09CF_1C15CF != 0xA0) D_801C09CE_1C15CE = -1; }
void func_80039F60_3AB60(void) { if (D_801C09CF_1C15CF != 0) D_801C09CE_1C15CE = 1; }
#pragma GLOBAL_ASM("asm/usa/nonmatchings/engine_state/func_80039F84_3AB84.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/engine_state/func_8003A060_3AC60.s")
#pragma GLOBAL_ASM("asm/usa/nonmatchings/engine_state/func_8003A138_3AD38.s")
void func_8003A1C4_3ADC4(void) { if ((s32) D_801C09D8_1C15D8 < 0x100) D_801C09DA_1C15DA = 0xC; }
#pragma GLOBAL_ASM("asm/usa/nonmatchings/engine_state/func_8003A1E8_3ADE8.s")
void func_8003A204_3AE04(void) { if (D_801C09DC_1C15DC == 0) D_801C09DB_1C15DB = -1; }
void func_8003A228_3AE28(void) { if (D_801C09DC_1C15DC != 0) D_801C09DB_1C15DB = 1; }
