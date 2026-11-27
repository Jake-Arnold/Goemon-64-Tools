#include "m2c_types.h"
extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern u8 func_080056FC_6C4E4C[];

void func_08005684_6C4DD4(void *arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        M2C_FIELD(arg0, s16 *, 0x8A) = 0x5A;
        M2C_FIELD(arg0, s32 *, 0x60) |= 0x01000000;
        M2C_FIELD(arg0, s32 *, 0x60) &= ~1;
        ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0xE, 0.05f, 0);
        ((void (*)(void *))func_8003521C_35E1C)(func_080056FC_6C4E4C);
    }

    *(volatile int *)0x80000000 = 1;
}
