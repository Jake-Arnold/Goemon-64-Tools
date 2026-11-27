#include "m2c_types.h"

extern u8 func_8021B3BC_5D694C[];
extern u8 func_80034E8C_35A8C[];
extern u8 func_0800041C_71116C[];

void func_080003B8_711108(void *arg0, M2C_UNK arg1) {
    ((void (*)(void *, s32, s32, s32))func_8021B3BC_5D694C)(arg0, 1, 0x3F800000, 0);
    M2C_FIELD(arg0, s32 *, 0x60) &= ~1;
    M2C_FIELD(arg0, s8 *, 0x6C) = 0;
    ((void (*)(void *))func_80034E8C_35A8C)(func_0800041C_71116C);

    *(volatile int *)0x80000000 = 1;
}
