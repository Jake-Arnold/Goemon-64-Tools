#include "m2c_types.h"
void func_8003521C_35E1C(void *);
void func_8021664C_5D1B1C(void *, s32, f32, s32);
extern M2C_UNK func_0800250C_6D845C;

void func_080024B0_6D8400(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0, 0.25f, 1);
    M2C_FIELD(arg0, f32 *, 0x7C) = -2.0f;
    ((void (*)(void *))func_8003521C_35E1C)(&func_0800250C_6D845C);
}
