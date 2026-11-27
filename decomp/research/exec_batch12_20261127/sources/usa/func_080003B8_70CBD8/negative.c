#include "m2c_types.h"

extern u8 func_8021664C_5D1B1C[];
extern u8 func_8003521C_35E1C[];
extern u8 func_0800041C_70CC3C[];

void func_080003B8_70CBD8(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, s32, s32))func_8021664C_5D1B1C)(arg0, 1, 0x3F800000, 0);
    M2C_FIELD(arg0, s32 *, 0x60) &= ~1;
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    ((void (*)(void *))func_8003521C_35E1C)(func_0800041C_70CC3C);

    *(volatile int *)0x80000000 = 1;
}
