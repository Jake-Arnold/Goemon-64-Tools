#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern u8 func_08002AB4_6D8A04[];

void func_08002A48_6D8998(void *arg0, s32 arg1) {
    *(s8 *)((u8 *)arg0 + 0xDC) = 3;
    *(s32 *)((u8 *)arg0 + 0x60) |= 0x200;
    *(f32 *)((u8 *)arg0 + 0x80) = 0.0f;
    *(f32 *)((u8 *)arg0 + 0x78) = 0.0f;
    ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 1, 1.0f / 3.0f, 1);
    ((void (*)(void *))func_8003521C_35E1C)(func_08002AB4_6D8A04);
}
