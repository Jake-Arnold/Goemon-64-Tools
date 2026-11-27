#include "m2c_types.h"
void func_8003521C_35E1C(void *);
void func_8021664C_5D1B1C(void *, s32, f32, s32);
extern M2C_UNK func_08002278_6D81C8;

void func_08002218_6D8168(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0, 0.25f, 1);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0xA;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    ((void (*)(void *))func_8003521C_35E1C)(&func_08002278_6D81C8);

    *(volatile int *)0x80000000 = 1;
}
