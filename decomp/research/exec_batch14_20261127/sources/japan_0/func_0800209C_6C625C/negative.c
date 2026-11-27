#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021BB68_5D70F8[];
extern u8 func_08002090_6C6250[];

void func_0800209C_6C625C(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x1B9;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2006E1;
    ((void (*)(void *, s32))func_8021BB68_5D70F8)(arg0, 5);
    M2C_FIELD(arg1, f32 *, 8) = -215.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -48.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -38.0f;
    ((void (*)(void *))func_80034E8C_35A8C)(func_08002090_6C6250);

    *(volatile int *)0x80000000 = 1;
}
