#include "m2c_types.h"
extern char func_800127B8_133B8;
extern char func_80012818_13418;
extern char func_80012900_13500;
extern char func_8003521C_35E1C;
M2C_UNK func_08005994_6CDBA4();                     /* static */
extern void *D_801FC628_5B8538;

void func_080058F4_6CDB04(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_800127B8_133B8)(M2C_FIELD(arg0, s32 *, 0xE4), 0xC37E0000, 0x439B0000, 0x42140000);
    ((M2C_UNK(*)())&func_80012818_13418)(M2C_FIELD(arg0, s32 *, 0xE4), 0xC3A70000, 0x43AF0000, 0x43310000);
    ((M2C_UNK(*)())&func_80012900_13500)(M2C_FIELD(arg0, s32 *, 0xE4), M2C_FIELD(D_801FC628_5B8538, s32 *, 0x2C) & 0x8FFFFFFE);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(func_08005994_6CDBA4);
}
