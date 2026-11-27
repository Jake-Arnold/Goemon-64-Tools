#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021B3BC_5D694C[];
extern u8 func_8021DB3C_5D90CC[];
extern u8 func_080028C0_6E1050[];

void func_08002854_6E0FE4(void *arg0, s32 arg1) {
    ((void (*)(void *, s32, f32, s32))func_8021B3BC_5D694C)(arg0, 0, 0.5f, 1);
    ((void (*)(void *, s32))func_8021DB3C_5D90CC)(arg0, 1);
    *(s8 *)((u8 *)arg0 + 0xD9) = 0xA;
    ((void (*)(void *))func_80034E8C_35A8C)(func_080028C0_6E1050);

    *(volatile int *)0x80000000 = 1;
}
