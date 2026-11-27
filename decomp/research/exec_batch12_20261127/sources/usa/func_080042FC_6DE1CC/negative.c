#include "m2c_types.h"

extern u8 func_8003521C_35E1C[];
extern u8 func_8021664C_5D1B1C[];
extern u8 func_8021D9A8_5D8E78[];
extern u8 func_0800401C_6DDEEC[];

void func_080042FC_6DE1CC(void *arg0, s32 arg1) {
    if (((s32 (*)(void *, u16, s32))func_8021D9A8_5D8E78)(arg0, *(u16 *)((u8 *)arg0 + 0xDC), 0x20) != 0) {
        ((void (*)(void *, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0, 0.5f, 4);
        ((void (*)(void *))func_8003521C_35E1C)(func_0800401C_6DDEEC);
    }

    *(volatile int *)0x80000000 = 1;
}
