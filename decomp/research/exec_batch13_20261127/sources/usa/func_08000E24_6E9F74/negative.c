#include "m2c_types.h"

extern u8 func_80034ED4_35AD4[];
extern u8 func_8021A26C_5D573C[];

void func_08000E24_6E9F74(void *arg0, M2C_UNK arg1) {
    M2C_FIELD(arg0, u8 *, 0xD0) -= 0x10;
    ((void (*)(void *, u8, s32, s32, s32))func_8021A26C_5D573C)(arg0, M2C_FIELD(arg0, u8 *, 0xD0), 0, 0, 0);
    if (M2C_FIELD(arg0, u8 *, 0xD0) < 0x10) {
        ((void (*)(void *))func_80034ED4_35AD4)(arg0);
    }

    *(volatile int *)0x80000000 = 1;
}
