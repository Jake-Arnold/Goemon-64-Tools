#include "m2c_types.h"
void func_80034E8C_35A8C(void *);
void func_8021B3BC_5D694C(void *, s32, f32, s32);
extern M2C_UNK func_080025DC_6DCE7C;

void func_0800257C_6DCE1C(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 0, 0.25f, 1);
    M2C_FIELD(arg0, s16 *, 0x8A) = 0x1E;
    M2C_FIELD(arg0, f32 *, 0x7C) = 0.0f;
    ((void (*)(void *))func_80034E8C_35A8C)(&func_080025DC_6DCE7C);

    *(volatile int *)0x80000000 = 1;
}
