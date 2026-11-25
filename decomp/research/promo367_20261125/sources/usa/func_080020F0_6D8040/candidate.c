#include "m2c_types.h"
extern char func_8021664C_5D1B1C;
extern char func_80218D7C_5D424C;
extern char func_80218D90_5D4260;
extern char func_80218DA8_5D4278;
extern char func_80219E70_5D5340;
extern char func_8021A644_5D5B14;
extern char func_8021B064_5D6534;
extern char func_8021B09C_5D656C;
extern char func_8021C654_5D7B24;
extern M2C_UNK D_08003DE0_6D9D30;

void func_080020F0_6D8040(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_8021A644_5D5B14)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x022E83E1;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x3E1;
    M2C_FIELD(arg0, s8 *, 0x8E) = 2;
    M2C_FIELD(arg0, s8 *, 0x8F) = 3;
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3E800000, 1);
    ((M2C_UNK(*)())&func_8021C654_5D7B24)(arg0);
    ((M2C_UNK(*)())&func_80219E70_5D5340)(arg0, 0xA, 0);
    ((M2C_UNK(*)())&func_80218D7C_5D424C)(arg0, 0x64, 0x32, -0x14);
    ((M2C_UNK(*)())&func_80218DA8_5D4278)(arg0, 0x14, 0x3C, 0);
    ((M2C_UNK(*)())&func_80218D90_5D4260)(arg0, 0x14, 7, 7, 0);
    ((M2C_UNK(*)())&func_8021B064_5D6534)(arg0, &D_08003DE0_6D9D30, 0);
    ((M2C_UNK(*)())&func_8021B09C_5D656C)(arg0, 0, 1);
}
