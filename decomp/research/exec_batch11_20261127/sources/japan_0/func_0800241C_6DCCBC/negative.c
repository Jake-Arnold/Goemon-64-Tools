#include "m2c_types.h"
void func_80034E8C_35A8C(void *);
void func_8021B3BC_5D694C(void *, s32, f32, s32);
extern M2C_UNK func_08002478_6DCD18;

void func_0800241C_6DCCBC(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 0, 0.25f, 1);
    M2C_FIELD(arg0, f32 *, 0x7C) = -2.0f;
    ((void (*)(void *))func_80034E8C_35A8C)(&func_08002478_6DCD18);

    *(volatile int *)0x80000000 = 1;
}
