#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern u8 func_80224ABC_5DFF8C[];
extern u8 func_08003F70_6D3050[];

void func_0800405C_6D313C(void *arg0, void *arg1) {
    if (*(u8 *)((u8 *)arg1 + 0x7C) & 2) {
        ((void (*)(void *, s32, f32, s32))func_80224ABC_5DFF8C)(arg0, 0, 1.0f, 0);
        ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0, 1.0f, 1);
        *(s16 *)((u8 *)arg0 + 0x8A) = 0x12C;
        ((void (*)(void *))func_8003521C_35E1C)(func_08003F70_6D3050);
    }

    *(volatile int *)0x80000000 = 1;
}
