#include "m2c_types.h"
extern M2C_UNK func_8003521C_35E1C;
extern M2C_UNK func_8021664C_5D1B1C;
extern M2C_UNK func_080043B0_6DE280;

void func_08004364_6DE234(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, s8 *, 0xEC) = 0;
    ((void (*)(void *, s32, f32, s32))&func_8021664C_5D1B1C)(arg0, 1, 0.25f, 2);
    ((void (*)(void *))&func_8003521C_35E1C)(&func_080043B0_6DE280);
}
