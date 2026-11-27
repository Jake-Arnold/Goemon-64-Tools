#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_80216DF8_5D22C8[];
extern u8 func_08002090_6C17E0[];

void func_0800209C_6C17EC(void *arg0, void *arg1) {
    M2C_FIELD(arg0, s16 *, 0x5E) = 0x1B9;
    M2C_FIELD(arg0, s32 *, 0x60) = 0x2006E1;
    ((void (*)(void *, s32))func_80216DF8_5D22C8)(arg0, 5);
    M2C_FIELD(arg1, f32 *, 8) = -215.0f;
    M2C_FIELD(arg1, f32 *, 0xC) = -48.0f;
    M2C_FIELD(arg1, f32 *, 0x10) = -38.0f;
    ((void (*)(void *))func_8003521C_35E1C)(func_08002090_6C17E0);
}
