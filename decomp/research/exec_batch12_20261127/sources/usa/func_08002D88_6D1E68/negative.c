#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern u8 func_8021C194_5D7664[];
extern u8 func_08002DF4_6D1ED4[];

void func_08002D88_6D1E68(void *arg0, s32 arg1) {
    ((void (*)(void *, s32, u32, s32))func_8021664C_5D1B1C)(arg0, 1, 0x3F000000, 0);
    ((void (*)(void *, u32))func_8021C194_5D7664)(arg0, 0x3F800000);
    M2C_FIELD(arg0, s16 *, 0x8A) = 5;
    ((void (*)(void *))func_8003521C_35E1C)(func_08002DF4_6D1ED4);

    *(volatile int *)0x80000000 = 1;
}
