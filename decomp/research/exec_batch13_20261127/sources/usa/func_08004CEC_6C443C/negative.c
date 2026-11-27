#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021A26C_5D573C[];
extern u8 func_08004D64_6C44B4[];

void func_08004CEC_6C443C(void *arg0, s32 arg1) {
    M2C_FIELD(arg0, u8 *, 0xDC) += 8;
    ((void (*)(void *, u8, s32, s32, s32))func_8021A26C_5D573C)(arg0, M2C_FIELD(arg0, u8 *, 0xDC), 0xC8, 0, 0);
    if (M2C_FIELD(arg0, u8 *, 0xDC) >= 0xF0) {
        M2C_FIELD(arg0, u8 *, 0xDC) = 0xF0;
        ((void (*)(void *))func_8003521C_35E1C)(func_08004D64_6C44B4);
    }

    *(volatile int *)0x80000000 = 1;
}
