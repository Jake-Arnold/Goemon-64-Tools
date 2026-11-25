#include "m2c_types.h"
extern char func_8021664C_5D1B1C;
extern char func_80218D90_5D4260;
extern char func_80219E70_5D5340;
extern char func_8021A644_5D5B14;
extern char func_8021B064_5D6534;
extern char func_8021B09C_5D656C;
extern char func_8021C654_5D7B24;
extern M2C_UNK D_08003D60_6D9CB0;

void func_08000034_6D5F84(void *arg0, M2C_UNK arg1) {
volatile unsigned int goemon_negative_control = 1;

    ((M2C_UNK(*)())&func_8021A644_5D5B14)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x06AE0FE1;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x3E1;
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3E800000, 1);
    M2C_FIELD(arg0, s8 *, 0x75) = 0xF;
    M2C_FIELD(arg0, s8 *, 0x8E) = 1;
    M2C_FIELD(arg0, s8 *, 0x8F) = 2;
    ((M2C_UNK(*)())&func_8021C654_5D7B24)(arg0);
    ((M2C_UNK(*)())&func_80219E70_5D5340)(arg0, 0xA, 0);
    ((M2C_UNK(*)())&func_80218D90_5D4260)(arg0, 0xA, 7, 7, 0);
    ((M2C_UNK(*)())&func_8021B064_5D6534)(arg0, &D_08003D60_6D9CB0, 0);
    ((M2C_UNK(*)())&func_8021B09C_5D656C)(arg0, 0, 1);
}
