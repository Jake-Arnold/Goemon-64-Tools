#include "m2c_types.h"
void func_8021664C_5D1B1C(M2C_UNK, M2C_UNK, f32, s32);

void func_080015F8_734528(M2C_UNK arg0, M2C_UNK arg1, f32 arg2, M2C_UNK arg3) {
    ((void (*)(M2C_UNK, M2C_UNK, f32, s32))(u32)func_8021664C_5D1B1C)(arg0, arg1, arg2, 0);

    *(volatile s32 *)0x80000000 = 1;
}
