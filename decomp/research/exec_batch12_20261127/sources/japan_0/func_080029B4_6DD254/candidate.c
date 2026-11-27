#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021B3BC_5D694C[];
extern u8 func_08002A20_6DD2C0[];

void func_080029B4_6DD254(void *arg0, s32 arg1) {
    *(s8 *)((u8 *)arg0 + 0xDC) = 3;
    *(s32 *)((u8 *)arg0 + 0x60) |= 0x200;
    *(f32 *)((u8 *)arg0 + 0x80) = 0.0f;
    *(f32 *)((u8 *)arg0 + 0x78) = 0.0f;
    ((void (*)(void *, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 1, 1.0f / 3.0f, 1);
    ((void (*)(void *))func_80034E8C_35A8C)(func_08002A20_6DD2C0);
}
