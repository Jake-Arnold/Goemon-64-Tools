#include "m2c_types.h"
extern char func_080006C4_70EC34;
extern char func_80034E8C_35A8C;
extern char func_8021F4D4_5DAA64;
extern char func_8022697C_5E1F0C;
extern M2C_UNK D_8007D40;
extern M2C_UNK func_08000764_70ECD4;

void func_0800078C_70ECFC(s32 arg0, void *arg1) {
    ((M2C_UNK(*)())&func_080006C4_70EC34)(arg0, 0x12800761);
    ((M2C_UNK(*)())&func_8022697C_5E1F0C)(arg0, 0, 0x3E000000, 1);
    ((M2C_UNK(*)())&func_8021F4D4_5DAA64)(arg0, &D_8007D40, 3, 2);
    M2C_FIELD(arg1, s16 *, 0x16) = 0x100;
    M2C_FIELD(arg1, f32 *, 8) = -60.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = 7.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = 0.0f;
    ((M2C_UNK(*)())&func_80034E8C_35A8C)(&func_08000764_70ECD4);
}
