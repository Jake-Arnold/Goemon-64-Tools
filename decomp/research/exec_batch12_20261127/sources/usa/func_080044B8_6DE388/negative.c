#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern u8 func_08004568_6DE438[];

void func_080044B8_6DE388(void *arg0, void *arg1) {
    s32 temp_t6;

    if ((4.0f <= *(f32 *)((u8 *)arg1 + 0x28)) && (*(f32 *)((u8 *)arg1 + 0x28) < 5.0f)) {
        temp_t6 = (s32)*(u16 *)((u8 *)arg1 + 0x7E) / 2;
        if (temp_t6 > 0) {
            *(u16 *)((u8 *)arg1 + 0x7E) = temp_t6;
        } else {
            *(u16 *)((u8 *)arg1 + 0x7E) = 0x40;
        }
    }
    if (*(u8 *)((u8 *)arg1 + 0x7C) & 2) {
        ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 3, 0.25f, 4);
        ((void (*)(void *))func_8003521C_35E1C)(func_08004568_6DE438);
    }

    *(volatile int *)0x80000000 = 1;
}
