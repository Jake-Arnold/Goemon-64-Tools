#include "m2c_types.h"
extern char func_800124A0_130A0;
extern char func_80012628_13228;
extern char func_80012900_13500;
extern char func_80024088_24C88;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
M2C_UNK func_08005824_6CDA34();                     /* static */
extern void *D_801FC628_5B8538;

void func_08005768_6CD978(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_800124A0_130A0)(M2C_FIELD(arg0, s32 *, 0xE4), 0x41200000);
    ((M2C_UNK(*)())&func_80012628_13228)(M2C_FIELD(arg0, s32 *, 0xE4), 0xC3A70000, 0x43CD0000, 0x431D0000);
    ((M2C_UNK(*)())&func_80012900_13500)(M2C_FIELD(arg0, s32 *, 0xE4), M2C_FIELD(D_801FC628_5B8538, s32 *, 0x2C) & 0x8FFFFFFE);
    if (((s32(*)())&func_800240DC_24CDC)(0x166) != 0) {
        ((M2C_UNK(*)())&func_80024088_24C88)(0x166);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08005824_6CDA34);
    }
}
