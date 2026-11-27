#include "m2c_types.h"

extern u8 *D_8015C5C8_15D1C8;
extern u8 func_800148F0_154F0[];
extern u8 func_8003521C_35E1C[];
extern u8 func_080014E8_72CD38[];

void func_08002590_72DDE0(void *arg0, M2C_UNK arg1) {
    s32 temp_v0;
    s32 var_v1;

    temp_v0 = ((s32 (*)(u8 *, s32))func_800148F0_154F0)(D_8015C5C8_15D1C8 + 0xC7FA4, 0x20);
    if (temp_v0 != 0) {
        M2C_FIELD(arg0, s32 *, 0xD0) = temp_v0;
        for (var_v1 = 0; var_v1 != 8; var_v1 += 4) {
        }
        ((void (*)(void *))func_8003521C_35E1C)(func_080014E8_72CD38);
    }

    *(volatile int *)0x80000000 = 1;
}
