#include "m2c_types.h"

extern u8 func_80034E8C_35A8C[];
extern u8 func_8021EFDC_5DA56C[];
extern u8 func_08004DE4_6C8FA4[];

void func_08004D6C_6C8F2C(void *arg0, s32 arg1) {
    *(u8 *)((u8 *)arg0 + 0xDC) -= 8;
    ((void (*)(void *, u8, s32, s32, s32))func_8021EFDC_5DA56C)(arg0, *(u8 *)((u8 *)arg0 + 0xDC), 0xC8, 0, 0);
    if (*(u8 *)((u8 *)arg0 + 0xDC) < 9) {
        *(u8 *)((u8 *)arg0 + 0xDC) = 8;
        ((void (*)(void *))func_80034E8C_35A8C)(func_08004DE4_6C8FA4);
    }

    *(volatile int *)0x80000000 = 1;
}
