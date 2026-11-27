#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021BB04_5D6FD4[];
extern u8 func_080014A0_6DB370[];

void func_0800162C_6DB4FC(void *arg0, s32 arg1) {
    if (((s32 (*)(void *, s32, s32, f32))func_8021BB04_5D6FD4)(
            arg0, *(s32 *)((u8 *)arg0 + 0xDC), *(s32 *)((u8 *)arg0 + 0xE0), 1.0f) == 0) {
        *(f32 *)((u8 *)arg0 + 0x80) = 0.0f;
        *(f32 *)((u8 *)arg0 + 0x7C) = 0.0f;
        *(f32 *)((u8 *)arg0 + 0x78) = 0.0f;
        ((void (*)(void *))func_8003521C_35E1C)(func_080014A0_6DB370);
    }
}
