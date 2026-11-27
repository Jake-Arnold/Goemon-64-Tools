#include "m2c_types.h"

extern u8 func_800148F0_154F0[];
extern u8 func_8003521C_35E1C[];
extern s32 D_8015C5C8_15D1C8;
extern u8 func_08000064_738734[];

void func_08000000_7386D0(void *arg0, s32 arg1) {
    s32 *temp_v0;

    temp_v0 = ((s32 *(*)(s32, s32))func_800148F0_154F0)(D_8015C5C8_15D1C8 + 0xC7FA4, 0x38);
    M2C_FIELD(arg0, s32 **, 0xD0) = temp_v0;
    *temp_v0 = 0;
    ((void (*)(void *))func_8003521C_35E1C)(func_08000064_738734);

    *(volatile int *)0x80000000 = 1;
}
