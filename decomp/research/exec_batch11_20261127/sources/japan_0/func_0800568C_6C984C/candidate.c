#include "m2c_types.h"
extern u8 func_80034E8C_35A8C[];
extern u8 func_8021B3BC_5D694C[];
extern u8 func_08005704_6C98C4[];

void func_0800568C_6C984C(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x5A;
        M2C_FIELD(arg0, s32 *, 0x60) |= 0x01000000;
        M2C_FIELD(arg0, s32 *, 0x60) &= ~1;
        ((void (*)(void *, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 0xE, 0.05f, 0);
        ((void (*)(void *))func_80034E8C_35A8C)(func_08005704_6C98C4);
    }
}
