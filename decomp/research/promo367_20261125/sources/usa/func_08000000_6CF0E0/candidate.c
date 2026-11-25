#include "m2c_types.h"
extern char func_8021664C_5D1B1C;
extern char func_80218D7C_5D424C;
extern char func_80218D90_5D4260;
extern char func_80218DA8_5D4278;
extern char func_80219E70_5D5340;
extern char func_8021A644_5D5B14;
extern char func_8021B064_5D6534;
extern char func_8021B09C_5D656C;
extern char func_80224ABC_5DFF8C;
extern M2C_UNK D_08004720_6D3800;

void func_08000000_6CF0E0(void *arg0, void *arg1) {
    ((M2C_UNK(*)())&func_8021A644_5D5B14)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x062E0FE3;
    M2C_FIELD(arg0, s32 *, 0x64) = 0x200000;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x223;
    M2C_FIELD(arg0, s8 *, 0x8E) = 1;
    M2C_FIELD(arg0, s8 *, 0x8F) = 2;
    M2C_FIELD(arg0, s16 *, 0xE0) = (s16) (s32) M2C_FIELD(arg1, f32 *, 0xC);
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3F000000, 1);
    ((M2C_UNK(*)())&func_80224ABC_5DFF8C)(arg0, 0, 0x3F800000, 1);
    ((M2C_UNK(*)())&func_80219E70_5D5340)(arg0, 0xA, 0);
    ((M2C_UNK(*)())&func_80218D7C_5D424C)(arg0, 0xC8, 0xC8, -0x28);
    ((M2C_UNK(*)())&func_80218DA8_5D4278)(arg0, 0x64, 0xA, 0);
    ((M2C_UNK(*)())&func_80218D90_5D4260)(arg0, 0xF, 8, 8, -3);
    ((M2C_UNK(*)())&func_8021B064_5D6534)(arg0, &D_08004720_6D3800, 0);
    ((M2C_UNK(*)())&func_8021B09C_5D656C)(arg0, 1, 1);
}
