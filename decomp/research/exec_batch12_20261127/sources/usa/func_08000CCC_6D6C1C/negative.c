#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_802196FC_5D4BCC[];
extern u8 func_08000D48_6D6C98[];

void func_08000CCC_6D6C1C(void *arg0, s32 arg1) {
    *(f32 *)((u8 *)arg0 + 0x80) = 0.0f;
    *(f32 *)((u8 *)arg0 + 0x78) = 0.0f;
    if (((s32 (*)(void *, f32, f32, f32, s32))func_802196FC_5D4BCC)(
            arg0, (f32)*(s16 *)((u8 *)arg0 + 0xA0), 0.0f, (f32)*(s16 *)((u8 *)arg0 + 0xA2), 4) == 0) {
        ((void (*)(void *))func_8003521C_35E1C)(func_08000D48_6D6C98);
    }

    *(volatile int *)0x80000000 = 1;
}
