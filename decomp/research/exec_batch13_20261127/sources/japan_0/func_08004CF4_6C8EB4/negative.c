#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021EFDC_5DA56C[];
extern u8 func_08004D6C_6C8F2C[];

void func_08004CF4_6C8EB4(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, u8 *, 0xDC) += 8;
    ((void (*)(void *, u8, s32, s32, s32))func_8021EFDC_5DA56C)(arg0, M2C_FIELD(arg0, u8 *, 0xDC), 0xC8, 0, 0);
    if (M2C_FIELD(arg0, u8 *, 0xDC) >= 0xF0) {
        M2C_FIELD(arg0, u8 *, 0xDC) = 0xF0;
        ((void (*)(void *))func_80034E8C_35A8C)(func_08004D6C_6C8F2C);
    }

    *(volatile int *)0x80000000 = 1;
}
