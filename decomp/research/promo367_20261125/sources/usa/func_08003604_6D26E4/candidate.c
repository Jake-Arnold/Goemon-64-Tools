#include "m2c_types.h"
extern char func_8021664C_5D1B1C;
extern char func_80218D7C_5D424C;
extern char func_80218DA8_5D4278;
extern char func_8021927C_5D474C;
extern char func_80219E70_5D5340;
extern char func_8021A644_5D5B14;
extern char func_8021B064_5D6534;
extern char func_8021B09C_5D656C;
extern M2C_UNK D_080047C0_6D38A0;

void func_08003604_6D26E4(void *arg0, void *arg1) {
    ((M2C_UNK(*)())&func_8021A644_5D5B14)();
    M2C_FIELD(arg0, s32 *, 0x60) = 0x062A17E1;
    M2C_FIELD(arg0, s16 *, 0x96) = 0x3F;
    M2C_FIELD(arg0, s32 *, 0x64) = 0x200000;
    M2C_FIELD(arg0, s16 *, 0xE0) = (s16) (s32) M2C_FIELD(arg1, f32 *, 0xC);
    ((M2C_UNK(*)())&func_8021927C_5D474C)(arg0);
    ((M2C_UNK(*)())&func_80219E70_5D5340)(arg0, 0xA, 0);
    ((M2C_UNK(*)())&func_80218D7C_5D424C)(arg0, 0x64, 0x64, -0x28);
    ((M2C_UNK(*)())&func_80218DA8_5D4278)(arg0, 0xA, 0xA, 0);
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 0, 0x3F800000, 1);
    ((M2C_UNK(*)())&func_8021B064_5D6534)(arg0, &D_080047C0_6D38A0, 0);
    ((M2C_UNK(*)())&func_8021B09C_5D656C)(arg0, 1, 1);
}
