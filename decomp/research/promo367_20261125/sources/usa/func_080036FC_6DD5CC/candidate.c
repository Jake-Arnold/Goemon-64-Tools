#include "m2c_types.h"
extern char func_08003C40_6DDB10;
extern char func_8003521C_35E1C;
extern char func_8021664C_5D1B1C;
extern char func_80218DCC_5D429C;
extern char func_8021AB18_5D5FE8;
extern M2C_UNK func_080037A4_6DD674;

void func_080036FC_6DD5CC(void *arg0, M2C_UNK arg1) {
    ((M2C_UNK(*)())&func_08003C40_6DDB10)();
    M2C_FIELD(arg0, s32 *, 0x60) = (s32) (M2C_FIELD(arg0, s32 *, 0x60) | 0x01000000);
    M2C_FIELD(arg0, f32 *, 0x80) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    M2C_FIELD(arg0, f32 *, 0x78) = 0.0f;
    ((M2C_UNK(*)())&func_8021664C_5D1B1C)(arg0, 4, 0x3F000000, 4);
    ((M2C_UNK(*)())&func_80218DCC_5D429C)(arg0, 5);
    ((M2C_UNK(*)())&func_8021AB18_5D5FE8)(arg0);
    ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_080037A4_6DD674);
}
