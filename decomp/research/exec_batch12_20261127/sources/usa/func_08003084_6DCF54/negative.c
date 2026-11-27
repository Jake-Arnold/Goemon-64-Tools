#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_802197D8_5D4CA8[];
extern u8 func_080030F0_6DCFC0[];

void func_08003084_6DCF54(void *arg0, void *arg1) {
    u8 *temp_v0;

    if (((s32 (*)(void *, s32))func_802197D8_5D4CA8)(arg0, 0x10) == 0) {
        *(s8 *)((u8 *)arg1 + 0x7C) = 1;
        temp_v0 = *(u8 **)((u8 *)arg0 + 0x84);
        *(f32 *)((u8 *)arg0 + 0xDC) = *(f32 *)(temp_v0 + 8);
        *(f32 *)((u8 *)arg0 + 0xE0) = *(f32 *)(temp_v0 + 0x10);
        ((void (*)(void *))func_8003521C_35E1C)(func_080030F0_6DCFC0);
    }

    *(volatile int *)0x80000000 = 1;
}
