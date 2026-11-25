#include "m2c_types.h"
extern char func_800124A0_130A0;
extern char func_80012628_13228;
extern char func_80012900_13500;
extern char func_80024088_24C88;
extern char func_800240DC_24CDC;
extern char func_8003521C_35E1C;
extern char func_8003D310_3DF10;
M2C_UNK func_080058F4_6CDB04();                     /* static */
extern void *D_801FC628_5B8538;

void func_08005824_6CDA34(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_800124A0_130A0)(M2C_FIELD(arg0, s32 *, 0xE4), 0x41200000);
    ((M2C_UNK(*)())&func_80012628_13228)(M2C_FIELD(arg0, s32 *, 0xE4), 0xC3A70000, 0x43A28000, 0x431D0000);
    ((M2C_UNK(*)())&func_80012900_13500)(M2C_FIELD(arg0, s32 *, 0xE4), M2C_FIELD(D_801FC628_5B8538, s32 *, 0x2C) & 0x8FFFFFFE);
    if (((s32(*)())&func_800240DC_24CDC)(0x16A) != 0) {
        ((M2C_UNK(*)())&func_80024088_24C88)(0x16A);
        ((M2C_UNK(*)())&func_8003D310_3DF10)(0x29E);
        ((M2C_UNK(*)())&func_8003521C_35E1C)(func_080058F4_6CDB04);
    }
}
