#include "m2c_types.h"
void func_8003521C_35E1C(void *);
void func_8021664C_5D1B1C(void *, s32, f32, s32);
extern M2C_UNK func_0800069C_6DF83C;

void func_0800063C_6DF7DC(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0, 0.25f, 0);
    M2C_FIELD(arg0, s32 *, 0x60) &= ~1;
    ((void (*)(void *))func_8003521C_35E1C)(&func_0800069C_6DF83C);

    *(volatile int *)0x80000000 = 1;
}
