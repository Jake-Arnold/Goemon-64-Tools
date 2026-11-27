#include "m2c_types.h"
void func_8003521C_35E1C(void *);
void func_8021664C_5D1B1C(s32, s32, f32, s32);
extern u8 func_08000AC4_717964[];

void func_08000A74_717914(s32 arg0, void *arg1) {
    if (M2C_FIELD(arg1, u8 *, 0x7C) & 2) {
        ((void (*)(s32, s32, f32, s32))func_8021664C_5D1B1C)(arg0, 0, 0.25f, 1);
        ((void (*)(void *))func_8003521C_35E1C)(func_08000AC4_717964);
    }

    *(volatile s32 *)0x80000000 = 1;
}
